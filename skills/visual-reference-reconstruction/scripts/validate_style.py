"""Validate a PASS 0 STYLE packet: a reference that is a style example, not geometry authority."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

KEYS = {'schema', 'mode', 'task', 'sources', 'baseline', 'adopt', 'reject', 'user_deltas',
        'invariants', 'gate', 'notes'}
ROLES = {'style', 'existing_asset', 'user_sketch'}
# A style example cannot carry measured geometry; those claims belong to REFERENCE MODE.
GEOMETRY_KEYS = {'dimensions', 'counts', 'proportions', 'certainty', 'model_contract', 'components'}


class StyleError(ValueError):
    pass


def need(ok, message):
    if not ok:
        raise StyleError(message)


def text(value, label):
    need(isinstance(value, str) and value.strip(), f'{label} must be non-empty text')


def validate(packet, base=None, verify_files=False):
    need(isinstance(packet, dict), 'Packet must be an object')
    extra = set(packet) - KEYS
    need(not extra & GEOMETRY_KEYS, f'STYLE packet cannot carry geometry claims: {sorted(extra & GEOMETRY_KEYS)}')
    need(not extra, f'Unknown keys: {sorted(extra)}')
    need(packet.get('schema') == 'style-1' and packet.get('mode') == 'STYLE', 'schema style-1, mode STYLE required')
    text(packet.get('task'), 'task')
    sources = packet.get('sources')
    need(isinstance(sources, list) and sources, 'sources must be a non-empty list')
    paths = {}
    for source in sources:
        need(isinstance(source, dict) and set(source) <= {'path', 'sha256', 'role', 'note'}, 'Bad source entry')
        text(source.get('path'), 'source.path')
        need(source.get('role') in ROLES, f'source.role must be one of {sorted(ROLES)}')
        need(isinstance(source.get('sha256'), str) and len(source['sha256']) == 64, 'source.sha256 must be hex sha256')
        need(source['path'] not in paths, f'Duplicate source {source["path"]}')
        paths[source['path']] = source['role']
        if verify_files:
            path = Path(source['path'])
            path = path if path.is_absolute() or base is None else Path(base) / path
            need(path.is_file(), f'Missing source file {path}')
            need(hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'], f'Hash mismatch {path}')
    need('style' in paths.values(), 'At least one source with role "style" is required')
    adopt, reject = packet.get('adopt'), packet.get('reject', [])
    need(isinstance(adopt, list) and adopt, 'adopt must list the borrowed traits')
    for item in adopt:
        need(isinstance(item, dict) and set(item) <= {'trait', 'source', 'note'}, 'Bad adopt entry')
        text(item.get('trait'), 'adopt.trait')
        need(paths.get(item.get('source')) in {'style', 'user_sketch'},
             f'adopt "{item.get("trait")}" must cite a style/user_sketch source')
    need(isinstance(reject, list), 'reject must be a list')
    for item in reject:
        need(isinstance(item, dict) and set(item) <= {'trait', 'reason'}, 'Bad reject entry')
        text(item.get('trait'), 'reject.trait'); text(item.get('reason'), 'reject.reason')
    deltas = packet.get('user_deltas', [])
    need(isinstance(deltas, list), 'user_deltas must be a list')
    for item in deltas:
        need(isinstance(item, dict) and set(item) <= {'requirement', 'status'}, 'Bad user_deltas entry')
        text(item.get('requirement'), 'user_deltas.requirement')
        need(item.get('status') in {'REQUIRED', 'DONE'}, 'user_deltas.status must be REQUIRED or DONE')
    adopted = {i['trait'].strip().lower() for i in adopt}
    rejected = {i['trait'].strip().lower() for i in reject}
    need(not adopted & rejected, f'Traits both adopted and rejected: {sorted(adopted & rejected)}')
    invariants = packet.get('invariants', [])
    need(isinstance(invariants, list) and all(isinstance(i, str) and i.strip() for i in invariants),
         'invariants must be a list of text')
    if 'existing_asset' in paths.values() or packet.get('baseline'):
        need(isinstance(packet.get('baseline'), dict) and packet['baseline'].get('source'),
             'A redesign needs baseline.source (saved copy or file) before mutation')
        need(invariants, 'A redesign must state invariants kept from the existing asset')
    need(packet.get('gate') in {'READY', 'BLOCKED'}, 'gate must be READY or BLOCKED')
    if packet['gate'] == 'BLOCKED':
        text(packet.get('notes'), 'notes (why BLOCKED)')
    return dict(status='PASS', gate=packet['gate'], adopted=len(adopt), rejected=len(reject),
                deltas=len(deltas), scope='Style intent only; geometry/visual acceptance stays with the domain owner')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet', type=Path)
    parser.add_argument('--verify-files', action='store_true')
    args = parser.parse_args(argv)
    try:
        packet = json.loads(args.packet.read_text(encoding='utf-8'))
        report = validate(packet, args.packet.resolve().parent, args.verify_files)
    except (StyleError, OSError, json.JSONDecodeError) as error:
        print(json.dumps(dict(status='FAIL', error=str(error)), indent=2))
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
