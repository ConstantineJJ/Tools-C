"""Render a saved Blender candidate without MCP; never saves the source .blend."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_artifact(output, metadata):
    if metadata.get('ok') is not True or metadata.get('status') != 'VISUAL REVIEW REQUIRED':
        raise ValueError('Capture failed or incorrectly claimed visual acceptance')
    image = Path(metadata['path']).resolve(strict=True)
    if image.parent != (output / 'image').resolve() or image.suffix.lower() != '.png':
        raise ValueError('Capture artifact escaped output directory')
    if digest(image) != metadata['sha256']:
        raise ValueError('Capture artifact hash mismatch')
    return image


def capture_file(blender, source, output, *, objects, view='front', mode='solid',
                 frame=None, resolution=512, framing=None, timeout=180):
    blender, source = Path(blender).resolve(strict=True), Path(source).resolve(strict=True)
    output = Path(output).resolve()
    if not blender.is_file() or not source.is_file() or source.suffix.lower() != '.blend':
        raise ValueError('Explicit Blender executable and saved .blend candidate required')
    if output.exists():
        raise ValueError('New output directory required')
    if not objects or len(set(objects)) != len(objects):
        raise ValueError('Explicit unique object names required')
    if view not in ('front', 'side', 'back', 'top', 'bottom', 'three_quarter'):
        raise ValueError('Offline capture requires a fixed view, not a live viewport')
    if mode not in ('solid', 'material_preview', 'rendered'):
        raise ValueError('Unsupported mode')
    if type(resolution) is not int or not 64 <= resolution <= 2048:
        raise ValueError('resolution must be an integer from 64 to 2048')
    if frame is not None and (type(frame) is not int or abs(frame) > 1000000):
        raise ValueError('frame must be an integer within +/-1000000')
    before = digest(source)
    output.mkdir(parents=True)
    job = dict(source=str(source), capture=dict(output=str(output / 'image'), view=view,
               target='character', object_names=objects, mode=mode, frame=frame,
               resolution=resolution, framing=framing))
    job_path = output / 'job.json'
    job_path.write_text(json.dumps(job, indent=2, allow_nan=False), encoding='utf-8')
    command = [str(blender), '--background', '--factory-startup', '--disable-autoexec',
               '--python-exit-code', '1', '--python', str(Path(__file__).resolve()), '--', str(job_path)]
    flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    try:
        with (output / 'blender.log').open('w', encoding='utf-8') as log:
            process = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                                     timeout=timeout, creationflags=flags)
        if digest(source) != before:
            raise ValueError('Source .blend changed during capture')
        if process.returncode:
            raise RuntimeError(f'Blender capture exited {process.returncode}; see {output / "blender.log"}')
        metadata = json.loads((output / 'image/capture.json').read_text(encoding='utf-8'))
        verify_artifact(output, metadata)
        marker = json.loads((output / 'completed.json').read_text(encoding='utf-8'))
        if marker != dict(ok=True, sha256=metadata['sha256']):
            raise ValueError('Missing or mismatched Blender completion marker')
        result = dict(ok=True, status='VISUAL REVIEW REQUIRED', transport='offline Blender render',
                      source=str(source), source_sha256=before, source_file_preserved=True,
                      command=command, capture=metadata,
                      limits='Saved candidate only; unsaved live edits are absent. Autoexec is disabled; '
                             'script-dependent assets need separate validation. Open the PNG and inspect it.')
        (output / 'result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        return result
    except Exception as exc:
        (output / 'failure.json').write_text(json.dumps(dict(ok=False, error=str(exc),
            source_file_preserved=digest(source) == before), indent=2), encoding='utf-8')
        raise


def blender_probe(job_path):
    import bpy
    import runpy
    job = json.loads(Path(job_path).read_text(encoding='utf-8'))
    bpy.ops.wm.open_mainfile(filepath=job['source'], use_scripts=False)
    capture = runpy.run_path(str(ROOT / 'tools/blender_capture.py'))['capture_viewport']
    metadata = capture(**job['capture'])
    output = Path(job['capture']['output']).parent
    (output / 'completed.json').write_text(json.dumps(dict(ok=True, sha256=metadata['sha256'])), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blender', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--objects', nargs='+', required=True)
    parser.add_argument('--view', default='front')
    parser.add_argument('--mode', default='solid')
    parser.add_argument('--frame', type=int)
    parser.add_argument('--resolution', type=int, default=512)
    parser.add_argument('--framing', type=Path, help='BEFORE capture.json (keeps center/span)')
    args = parser.parse_args()
    try:
        framing = json.loads(args.framing.read_text(encoding='utf-8'))['framing'] if args.framing else None
        result = capture_file(args.blender, args.source, args.output, objects=args.objects,
                              view=args.view, mode=args.mode, frame=args.frame,
                              resolution=args.resolution, framing=framing)
        print(json.dumps(result, indent=2))
    except Exception as exc:
        print(json.dumps(dict(ok=False, error=str(exc))))
        raise SystemExit(1)


if __name__ == '__main__':
    if '--' in sys.argv:
        blender_probe(sys.argv[sys.argv.index('--') + 1])
    else:
        main()
