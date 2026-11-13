"""Bounded canonical metadata discovery; full validation remains in check.catalog."""
import difflib
import re
from pathlib import Path
import runpy

from validation_core import existing, require, catalog_manifest, resolve_identifier


def _header(path):
    # No persistent cache: same-size/same-mtime edits are visible immediately.
    lines = []
    with path.open(encoding='utf-8') as stream:
        for _ in range(32):
            line = stream.readline(8193)
            require(line and sum(map(len, lines)) + len(line) <= 8192,
                    'Missing or oversized skill header', 'E_CATALOG')
            lines.append(line)
            if len(lines) > 1 and line.strip() == '---': break
        require(lines[0].strip() == '---' and lines[-1].strip() == '---', 'Invalid skill header', 'E_CATALOG')
        heading = stream.readline(1024)
        if not heading.strip(): heading = stream.readline(1024)
    front = ''.join(lines[1:-1])
    values = {}
    for key in ('name', 'description'):
        matches = re.findall(r'^'+key+r': ([^\n]+)$', front, re.M)
        require(len(matches) == 1 and matches[0].strip(), 'Invalid '+key+' in skill header', 'E_CATALOG')
        values[key] = matches[0].strip()
    return values, heading.removeprefix('# ').strip()


def _records(root):
    manifest = catalog_manifest(root)
    aliases, by_owner = [], {}
    for name, item in manifest['blender_aliases'].items():
        owner = item['reference'].replace('\\', '/').split('/')[1]
        aliases.append(dict(name=name, reference=item['reference'], canonical_owner=owner))
        by_owner.setdefault(owner, []).append(name)
    records = []
    for item in manifest['skills']:
        header, title = _header(existing(root, item['path']))
        require(header['name'] == item['id'], 'Skill name differs from manifest', 'E_CATALOG')
        records.append(dict(name=item['id'], path=item['path'], description=header['description'],
                            title=title or item['id'], aliases=sorted(by_owner.get(item['id'], []))))
    return records, aliases


def listing(root):
    records, aliases = _records(root)
    return dict(canonical_count=len(records), canonical_skills=records, compatibility_aliases=aliases)


STOP = set('a an the for on of in from with and or to this that existing create make model build fix preserve without do not its blender'.split())


def _words(text):
    return set(re.findall(r'\w+', text.casefold())) - STOP


def _excerpt(text, terms):
    match = re.search('|'.join(re.escape(t) for t in sorted(terms)), text, re.I)
    position = match.start() if match else 0
    return text[max(0, position - 100):position + 440].strip()


def search(root, query, max_results=10):
    query = (query or '').strip()
    terms = _words(query)
    if not terms: return dict(ok=False, error='Query is empty or contains no searchable terms.')
    records, _ = _records(root)
    limit = max(1, min(int(max_results), 25))
    selected = [r for r in records if query.casefold() in {n.casefold() for n in [r['name'], *r['aliases']]}]
    phase = 'metadata'
    positive_query = query
    if not selected:
        # Reuse task intent; no second RU/EN trigger registry.
        runtime = runpy.run_path(str(Path(__file__).with_name('mcp_runtime.py')))
        owners = runtime['route_task'](query, root=root)
        positive_query = runtime['action_query'](query).strip()
        terms = _words(positive_query)
        if owners != ['blender-pipeline']:
            selected = [r for owner in owners for r in records if r['name'] == owner]
        if selected: phase = 'intent'
    if not selected and terms:
        metadata = lambda r: ' '.join([r['name'], r['title'], r['description'], *r['aliases']])
        primary = lambda r: ' '.join([r['name'], r['title'], *r['aliases']])
        selected = ([r for r in records if terms <= _words(primary(r))]
                    or [r for r in records if terms <= _words(metadata(r))])
        if not selected:
            phase = 'partial_metadata'
            selected = [r for r in records if terms & _words(metadata(r))]
        # Precise recipe lookup retains entrypoint fallback, without dependencies.
        # Never scan bodies for a broad sentence or a misspelled canonical ID.
        if not selected and len(terms) == 1 and '-' not in query and '_' not in query:
            phase = 'entrypoint'
            for row in records:
                body = existing(root, row['path']).read_text(encoding='utf-8')
                if terms <= _words(body): selected.append(dict(row, _body=body))
        selected.sort(key=lambda r: (-len(terms & _words(primary(r))), -len(terms & _words(metadata(r))), r['name']))
    results = []
    for rank, row in enumerate(selected[:limit]):
        summary = row.get('_body', ' '.join([row['name'], row['title'], row['description']]))
        results.append(dict(name=row['name'], score=1000-rank, excerpt=_excerpt(summary, terms),
                            path=row['path'], description=row['description'], matched_in=phase))
    names = [r['name'] for r in records]
    return dict(ok=True, query=query, count=len(results), results=results, total_matches=len(selected),
                catalog_scope='canonical owners', search_scope=phase,
                suggestions=difflib.get_close_matches(positive_query, names, n=3, cutoff=.85) if not selected and terms else [],
                limits='Discovery suggestions only. Read the selected owner and required documents; this is not execution evidence.')
