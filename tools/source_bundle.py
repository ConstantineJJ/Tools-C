"""Capture an explicit working-tree allowlist, including untracked code. Never stage.

Receipts prove scoped source bytes/provenance, not build or deployment readiness.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess

from check import Violation, fields, read_json, require

MAX_FILES = 10000
MAX_FILE = 32 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
JSON_LIMIT = 8 * 1024 * 1024


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(',', ':'), allow_nan=False).encode()


def git(root, *args, optional=False):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')
    result = subprocess.run(['git', '-c', 'core.fsmonitor=false', '-c', 'core.untrackedCache=false',
                             '-C', str(root), *args], capture_output=True, env=env, timeout=30)
    require(optional or result.returncode == 0, 'Git read failed: '+args[0], 'E_GIT')
    return result.stdout if result.returncode == 0 else b''


def no_links(path):
    for part in [*reversed(path.parents), path]:
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        require(not stat.S_ISLNK(info.st_mode) and not getattr(info, 'st_file_attributes', 0) & 0x400,
                'Symlink/reparse point is outside source-bundle scope', 'E_PATH')


def project_root(project):
    root = Path(project).absolute()
    no_links(root)
    root = root.resolve(strict=True)
    actual = git(root, 'rev-parse', '--show-toplevel').decode('utf-8').strip()
    require(Path(actual).resolve() == root, 'Use the exact Git worktree root', 'E_PATH')
    return root


def git_state(root):
    head = git(root, 'rev-parse', '--verify', 'HEAD', optional=True).decode().strip() or None
    branch = git(root, 'symbolic-ref', '--short', '-q', 'HEAD', optional=True).decode('utf-8').strip() or None
    tree, index = {}, {}
    if head:
        for entry in git(root, 'ls-tree', '-r', '-z', head).split(b'\0'):
            if entry:
                meta, path = entry.split(b'\t', 1)
                mode, kind, oid = meta.decode().split()
                tree[path.decode('utf-8')] = dict(mode=mode, oid=oid)
    for entry in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if entry:
            meta, path = entry.split(b'\t', 1)
            mode, oid, stage = meta.decode().split()
            require(stage == '0', 'Unmerged index needs review before capture', 'E_CONFLICT')
            index[path.decode('utf-8')] = dict(mode=mode, oid=oid)
    others = {p.decode('utf-8') for p in git(root, 'ls-files', '--others', '--exclude-standard', '-z').split(b'\0') if p}
    status_raw = git(root, 'status', '--porcelain=v1', '-z', '--untracked-files=all', '--no-renames')
    status = {p[3:].decode('utf-8'): p[:2].decode() for p in status_raw.split(b'\0') if p}
    names = sorted(set(tree) | set(index) | others)
    require(len(names) <= MAX_FILES, 'Git inventory file budget exceeded', 'E_LIMIT')
    rows = [dict(path=p, origin='tracked' if p in tree or p in index else 'untracked',
                 head=tree.get(p), index=index.get(p), status=status.get(p, '')) for p in names]
    return dict(project=dict(root=str(root), head=head, branch=branch, index_sha256=digest(canonical(index)),
                             status_sha256=digest(status_raw)), files=rows)


def inventory(project):
    return dict(kind='source_inventory', schema_version=1, **git_state(project_root(project)),
                limits='Git-visible paths only; ignored files omitted; no source bodies or readiness claim')


def paths(values):
    require(isinstance(values, list) and 0 < len(values) <= MAX_FILES, 'Nonempty exact allowlist required', 'E_LIMIT')
    seen = set()
    for value in values:
        require(isinstance(value, str) and 0 < len(value) <= 4096, 'Invalid allowlist path', 'E_PATH')
        parts = value.split('/')
        require(all(p not in ('', '.', '..') and p.casefold() != '.git' and not p.endswith((' ', '.'))
                    and not re.fullmatch(r'(?i:con|prn|aux|nul|conin\$|conout\$|com[1-9]|lpt[1-9])(?:\..*)?', p)
                    for p in parts) and not any(ord(c) < 32 or c in '\\:*?<>|"' for c in value),
                'Use portable relative file paths, excluding .git', 'E_PATH')
        require(value.casefold() not in seen, 'Duplicate/case-colliding path', 'E_PATH')
        seen.add(value.casefold())
    # A file cannot also be a parent directory of another selected file.
    require(not any('/'.join(v.split('/')[:i]).casefold() in seen
                    for v in values for i in range(1, len(v.split('/')))), 'File/directory path collision', 'E_PATH')
    return sorted(values)


def read_file(root, name, limit=MAX_FILE):
    path = root/name
    no_links(path)
    try:
        info = path.stat()
    except FileNotFoundError:
        return None
    require(stat.S_ISREG(info.st_mode), 'Selected entry is not a regular file', 'E_PATH')
    require(info.st_size <= limit, 'File size budget exceeded', 'E_LIMIT')
    with path.open('rb') as stream:
        raw = stream.read(limit+1)
    require(len(raw) <= limit, 'File size budget exceeded', 'E_LIMIT')
    return raw


def selection(root, names):
    state = git_state(root)
    available = {r['path']: r for r in state['files']}
    rows, content, total = [], {}, 0
    for name in names:
        require(name in available, 'Unknown or ignored allowlist path: '+name, 'E_SCOPE')
        row = dict(available[name])
        raw = read_file(root, name)
        require(raw is not None or row['origin'] == 'tracked', 'Missing untracked file', 'E_STALE')
        total += len(raw) if raw is not None else 0
        require(total <= MAX_TOTAL, 'Bundle byte budget exceeded', 'E_LIMIT')
        row.update(state='absent' if raw is None else 'present', size=len(raw) if raw is not None else 0,
                   sha256=digest(raw) if raw is not None else None)
        rows.append(row)
        if raw is not None:
            content[name] = raw
    return dict(schema_version=1, kind='source_bundle', project=state['project'], files=rows), content


def capture(project, allowlist, output):
    root, names = project_root(project), paths(allowlist)
    output = Path(output).absolute()
    no_links(output)
    require(output.parent.is_dir() and not output.exists(), 'Use a new output with an existing parent', 'E_OUTPUT')
    require(not git(output.parent, 'rev-parse', '--git-dir', optional=True),
            'Bundle output must be outside Git repositories/metadata', 'E_OUTPUT')
    manifest, content = selection(root, names)
    # Recheck metadata and bytes before creating anything; never silently take HEAD/index bytes.
    require(selection(root, names)[0] == manifest, 'Source changed while reading', 'E_STALE')
    output.mkdir()
    (output/'source').mkdir()
    for name, raw in content.items():
        target = output/'source'/name
        target.parent.mkdir(parents=True, exist_ok=True)
        no_links(target.parent)
        with target.open('xb') as stream:
            stream.write(raw)
    require(selection(root, names)[0] == manifest, 'Source changed during capture; no completion manifest', 'E_STALE')
    manifest['manifest_sha256'] = digest(canonical(manifest))
    with (output/'manifest.json').open('xb') as stream:
        stream.write(canonical(manifest)+b'\n')
    return dict(status='SOURCE_BUNDLE_PASS', bundle=str(output), files=len(names),
                untracked=sum(r['origin'] == 'untracked' for r in manifest['files']),
                manifest_sha256=manifest['manifest_sha256'],
                limits='Selected source bytes only; not a commit, runnable package or migration approval')


def validate_manifest(manifest):
    fields(manifest, ['schema_version', 'kind', 'project', 'files', 'manifest_sha256'])
    require(type(manifest['schema_version']) is int and manifest['schema_version'] == 1
            and manifest['kind'] == 'source_bundle', 'Unknown bundle format')
    project = manifest['project']
    fields(project, ['root', 'head', 'branch', 'index_sha256', 'status_sha256'])
    require(isinstance(project['root'], str) and bool(project['root']), 'Missing provenance root')
    require(project['branch'] is None or isinstance(project['branch'], str), 'Invalid branch')
    require(project['head'] is None or isinstance(project['head'], str) and
            re.fullmatch(r'[a-f0-9]{40}|[a-f0-9]{64}', project['head']), 'Invalid HEAD')
    for value in [manifest['manifest_sha256'], project['index_sha256'], project['status_sha256']]:
        require(isinstance(value, str) and re.fullmatch('[a-f0-9]{64}', value), 'Invalid SHA-256')
    require(isinstance(manifest['files'], list) and 0 < len(manifest['files']) <= MAX_FILES, 'Invalid file records')
    total = 0
    for row in manifest['files']:
        fields(row, ['path', 'origin', 'head', 'index', 'status', 'state', 'size', 'sha256'])
        require(row['origin'] in ('tracked', 'untracked'), 'Invalid source origin')
        require(row['status'] == '' or isinstance(row['status'], str) and
                re.fullmatch('[ MADRCU?!T]{2}', row['status']), 'Invalid Git status')
        for value in [row['head'], row['index']]:
            if value is not None:
                fields(value, ['mode', 'oid'])
                require(value['mode'] in ('100644', '100755', '120000', '160000') and
                        isinstance(value['oid'], str) and re.fullmatch('[a-f0-9]{40}|[a-f0-9]{64}', value['oid']),
                        'Invalid Git entry')
        require((row['origin'] == 'tracked') == (row['head'] is not None or row['index'] is not None),
                'Origin disagrees with Git provenance')
        require(type(row['size']) is int and 0 <= row['size'] <= MAX_FILE, 'Invalid file size', 'E_LIMIT')
        total += row['size']
        if row['state'] == 'absent':
            require(row['origin'] == 'tracked' and row['size'] == 0 and row['sha256'] is None,
                    'Invalid deleted-file record')
        else:
            require(row['state'] == 'present' and isinstance(row['sha256'], str) and
                    re.fullmatch('[a-f0-9]{64}', row['sha256']), 'Invalid present-file record')
    require(total <= MAX_TOTAL, 'Bundle byte budget exceeded', 'E_LIMIT')
    return paths([r['path'] for r in manifest['files']])


def verify(bundle, project=None):
    root = Path(bundle).absolute()
    no_links(root)
    require(read_file(root, 'manifest.json', JSON_LIMIT) is not None, 'Missing completion manifest', 'E_BUNDLE')
    manifest = read_json(root/'manifest.json')
    names = validate_manifest(manifest)
    require({p.name for p in root.iterdir()} == {'source', 'manifest.json'}, 'Unexpected bundle entries', 'E_SCOPE')
    expected = dict(manifest)
    checksum = expected.pop('manifest_sha256')
    require(checksum == digest(canonical(expected)), 'Manifest checksum mismatch', 'E_HASH')
    present = set()
    for row in manifest['files']:
        raw = read_file(root/'source', row['path'])
        if row['state'] == 'present':
            present.add(row['path'])
            require(raw is not None and len(raw) == row['size'] and digest(raw) == row['sha256'], 'Payload mismatch', 'E_HASH')
        else:
            require(row['state'] == 'absent' and raw is None, 'Deleted path unexpectedly present', 'E_HASH')
    actual = set()
    require((root/'source').is_dir(), 'Missing source directory', 'E_BUNDLE')
    for directory, dirs, files in os.walk(root/'source', followlinks=False):
        for name in dirs+files:
            no_links(Path(directory)/name)
        actual.update((Path(directory)/name).relative_to(root/'source').as_posix() for name in files)
        require(len(actual) <= MAX_FILES, 'Payload file budget exceeded', 'E_LIMIT')
    require(actual == present, 'Unexpected payload files', 'E_SCOPE')
    if project is not None:
        current, _ = selection(project_root(project), names)
        require(current == expected, 'Source metadata or selected bytes changed', 'E_STALE')
    return dict(status='SOURCE_BUNDLE_PASS', bundle=str(root), files=len(names),
                source_checked=project is not None, manifest_sha256=checksum,
                limits='Integrity only; a checksum is not a signature or build/runtime acceptance')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='operation', required=True)
    listing = commands.add_parser('inventory', help='Read Git-visible provenance; no source bodies')
    listing.add_argument('--project', required=True, type=Path)
    copying = commands.add_parser('capture', help='Copy an exact working-tree allowlist to new external output')
    copying.add_argument('--project', required=True, type=Path)
    copying.add_argument('--allowlist', required=True, type=Path, help='JSON array of exact relative file paths')
    copying.add_argument('--output', required=True, type=Path)
    checking = commands.add_parser('verify', help='Validate payload; optional explicit source freshness check')
    checking.add_argument('--bundle', required=True, type=Path)
    checking.add_argument('--project', type=Path)
    args = parser.parse_args()
    try:
        if args.operation == 'inventory':
            result = inventory(args.project)
        elif args.operation == 'capture':
            allowlist = args.allowlist.absolute()
            require(read_file(allowlist.parent, allowlist.name, JSON_LIMIT) is not None, 'Missing allowlist', 'E_FILE')
            result = capture(args.project, read_json(allowlist), args.output)
        else:
            result = verify(args.bundle, project=args.project)
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
        return 0
    except (Violation, OSError, ValueError, RecursionError, subprocess.TimeoutExpired) as error:
        print(json.dumps(dict(status='FAIL', code=getattr(error, 'code', 'E_IO'), error=str(error)), ensure_ascii=True))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
