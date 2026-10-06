"""Validate bounded surface-transfer provenance; never certify pixel/visual quality."""
import argparse
import hashlib
import json
from pathlib import Path, PureWindowsPath
import re

from check import Violation, read_json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, names, label):
    require(isinstance(value, dict) and set(value) == set(names.split()),
            label + ': missing or unknown fields')


def text(value):
    return isinstance(value, str) and bool(value.strip())


def validate(record, root=None):
    """Raise ValueError on invalid records; root enables contained file/hash checks."""
    fields(record, 'schema_version source crop artifacts steps target bake seam_cleanup pbr_basis qa', 'record')
    require(type(record['schema_version']) is int and record['schema_version'] == 1, 'schema_version must be 1')
    artifacts = record['artifacts']
    require(isinstance(artifacts, dict) and bool(artifacts), 'artifacts must be a nonempty object')
    paths = set()
    for name, artifact in artifacts.items():
        require(text(name), 'artifact id must be nonempty')
        fields(artifact, 'path sha256', name)
        path, digest = artifact['path'], artifact['sha256']
        require(text(path) and '\\' not in path and ':' not in path and
                not PureWindowsPath(path).is_absolute() and not Path(path).is_absolute() and
                not any(part in ('', '.', '..') or part.endswith((' ', '.')) for part in path.split('/')),
                name + ': use contained relative artifact path')
        require(path.casefold() not in paths, 'artifact paths must be distinct')
        paths.add(path.casefold())
        require(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest), name + ': invalid sha256')
        if root is not None:
            base = Path(root).resolve(strict=True)
            candidate = (base / path).resolve(strict=True)
            require(candidate.is_relative_to(base) and candidate.is_file(), name + ': artifact escapes root or is not a file')
            require(hashlib.sha256(candidate.read_bytes()).hexdigest() == digest, name + ': hash mismatch')

    def ref(value):
        require(isinstance(value, str) and value in artifacts, 'unknown artifact reference')

    source = record['source']
    fields(source, 'artifact role size authority', 'source')
    ref(source['artifact'])
    require(source['role'] in ('ORIGINAL', 'LOCKED_HERO'), 'source must be original or locked hero')
    require(text(source['authority']), 'source authority/Model Contract binding is required')
    size = source['size']
    require(isinstance(size, list) and len(size) == 2 and all(type(n) is int and n > 0 for n in size), 'invalid source size')
    crop = record['crop']
    require(isinstance(crop, list) and len(crop) == 4 and all(type(n) is int for n in crop), 'crop must be integer x,y,width,height')
    x, y, w, h = crop
    require(x >= 0 and y >= 0 and w > 0 and h > 0 and x+w <= size[0] and y+h <= size[1], 'crop outside source')
    steps = record['steps']
    require(isinstance(steps, list) and bool(steps), 'steps required')
    previous = source['artifact']
    outputs = {previous}
    for index, step in enumerate(steps):
        require(isinstance(step, dict), 'step must be an object')
        operation = step.get('operation')
        require(operation in ('crop', 'rectify', 'upscale', 'cleanup', 'regenerate'), 'unknown operation')
        extra = ' mask prompt' if operation == 'regenerate' else ''
        fields(step, 'operation input output reason parameters' + extra, 'step')
        require((index == 0) == (operation == 'crop'), 'first and only first step must crop')
        require(step['input'] == previous, 'broken processing lineage')
        ref(step['output'])
        require(step['output'] not in outputs, 'source/intermediate overwrite')
        require(text(step['reason']) and text(step['parameters']), 'step reason and parameters required')
        if operation == 'regenerate':
            ref(step['mask']); ref(step['prompt'])
            require(len({step['input'], step['output'], step['mask'], step['prompt']}) == 4,
                    'repair input/output/mask/prompt must be distinct')
        outputs.add(step['output'])
        previous = step['output']
    target = record['target']
    fields(target, 'objects faces uv_map material method image settings', 'target')
    require(isinstance(target['objects'], list) and bool(target['objects']) and all(text(n) for n in target['objects']), 'target objects required')
    require(all(text(target[k]) for k in ('faces', 'uv_map', 'material', 'settings')), 'target bindings/settings required')
    require(target['method'] in ('PROJECTION', 'DECAL', 'UV'), 'invalid transfer method')
    require(target['image'] == previous, 'target must use final prepared image')
    bake = record['bake']
    require(isinstance(bake, dict), 'bake must be an object')
    if bake.get('status') == 'DONE':
        fields(bake, 'status artifact settings', 'bake')
        ref(bake['artifact'])
        require(bake['artifact'] not in outputs, 'bake overwrites source/intermediate')
        require(text(bake['settings']), 'bake settings required')
    else:
        fields(bake, 'status reason', 'bake')
        require(bake['status'] in ('PENDING', 'SKIP') and text(bake['reason']), 'unbaked reason required')
    cleanup = record['seam_cleanup']
    require(isinstance(cleanup, dict), 'seam_cleanup must be an object')
    if cleanup.get('status') == 'DONE':
        fields(cleanup, 'status input output settings', 'seam_cleanup')
        require(bake['status'] == 'DONE' and cleanup['input'] == bake['artifact'], 'cleanup must follow bake')
        ref(cleanup['output'])
        require(cleanup['output'] not in outputs | {bake['artifact']}, 'cleanup overwrites source/intermediate')
        require(text(cleanup['settings']), 'cleanup settings required')
    else:
        fields(cleanup, 'status reason', 'seam_cleanup')
        require(cleanup['status'] in ('PENDING', 'SKIP') and text(cleanup['reason']), 'cleanup reason required')
    require(text(record['pbr_basis']), 'separate PBR reconstruction basis required')
    qa = record['qa']
    fields(qa, 'identity seams material movement reopen target', 'qa')
    for criterion, review in qa.items():
        fields(review, 'status reviewer observations artifacts', criterion)
        require(review['status'] in ('PASS', 'FAIL', 'SKIP', 'REVIEW_REQUIRED'), 'invalid QA status')
        require(text(review['observations']), criterion + ': observations or SKIP reason required')
        require(isinstance(review['reviewer'], str) and isinstance(review['artifacts'], list), 'invalid review evidence')
        for artifact in review['artifacts']:
            ref(artifact)
        if review['status'] != 'SKIP':
            require(bool(review['artifacts']), criterion + ': evidence required')
        if review['status'] in ('PASS', 'FAIL'):
            require(text(review['reviewer']), criterion + ': reviewer required')
    return {'structural': 'PASS', 'files': 'PASS' if root is not None else 'SKIP',
            'visual': 'NOT_EVALUATED', 'limits': 'Recorded QA verdicts are not verified by this checker.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--verify-files', action='store_true')
    args = parser.parse_args()
    try:
        result = validate(read_json(args.record), args.record.parent if args.verify_files else None)
    except (ValueError, OSError, Violation) as error:
        print(json.dumps({'structural': 'FAIL', 'error': str(error)}))
        return 1
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
