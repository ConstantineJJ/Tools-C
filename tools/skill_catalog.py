"""Canonical skill discovery/search without expanding procedural contexts."""
import re

from check import catalog, existing


def _records(root):
    manifest = catalog(root)
    aliases = []
    by_owner = {}
    for name, item in manifest['blender_aliases'].items():
        owner = item['reference'].replace('\\', '/').split('/')[1]
        aliases.append(dict(name=name, reference=item['reference'], canonical_owner=owner))
        by_owner.setdefault(owner, []).append(name)
    records = []
    for item in manifest['skills']:
        text = existing(root, item['path']).read_text(encoding='utf-8')
        front = text.split('---', 2)[1]
        description = re.search(r'^description: (.+)$', front, re.M).group(1).strip()
        heading = re.search(r'^# (.+)$', text, re.M)
        row = dict(name=item['id'], path=item['path'], description=description,
                   title=heading.group(1) if heading else item['id'],
                   aliases=sorted(by_owner.get(item['id'], [])))
        records.append((row, text))
    return records, aliases


def listing(root):
    """All declared owners, with compatibility aliases separate from owners."""
    records, aliases = _records(root)
    return dict(canonical_count=len(records), canonical_skills=[r for r, _ in records],
                compatibility_aliases=aliases)


def _words(text):
    return set(re.findall(r'\w+', text.casefold()))


def _excerpt(text, terms):
    pattern = r'\b(?:' + '|'.join(re.escape(t) for t in sorted(terms)) + r')\b'
    match = re.search(pattern, text, re.I)
    position = match.start() if match else 0
    return text[max(0, position - 160):position + 540].strip()


def search(root, query, max_results=10):
    """Prefer complete metadata matches; fall back to each owner's entrypoint."""
    query = (query or '').strip()
    if not query:
        return dict(ok=False, error='Query is empty.')
    terms = _words(query)
    if not terms:
        return dict(ok=False, error='Query contains no searchable terms.')
    limit = max(1, min(int(max_results), 25))
    records, _ = _records(root)
    candidates = []
    for row, body in records:
        metadata = ' '.join([row['name'], row['title'], row['description'], *row['aliases']])
        hits = terms & _words(metadata)
        exact = query.casefold() in {n.casefold() for n in [row['name'], *row['aliases']]}
        name_hits = terms & _words(row['name'])
        score = 1000 * exact + 100 * len(hits) + 20 * len(name_hits)
        primary_hits = terms & _words(' '.join([row['name'], row['title'], *row['aliases']]))
        candidates.append(dict(row=row, body=body, hits=hits, primary_hits=primary_hits, score=score, metadata=metadata))
    complete = ([c for c in candidates if c['primary_hits'] == terms]
                or [c for c in candidates if c['hits'] == terms])
    phase = 'metadata'
    if not complete:
        phase = 'entrypoint'
        for c in candidates:
            body_hits = terms & _words(c['body'])
            if body_hits == terms:
                c['score'] += len(body_hits) + 20 * (query.casefold() in c['body'].casefold())
                complete.append(c)
    if not complete:
        phase = 'partial_metadata'
        complete = [c for c in candidates if c['hits']]
    complete.sort(key=lambda c: (-c['score'], c['row']['name']))
    results = []
    for c in complete[:limit]:
        row = c['row']
        results.append(dict(name=row['name'], score=c['score'],
                            excerpt=_excerpt(c['body'] if phase == 'entrypoint' else c['metadata'], terms),
                            path=row['path'], description=row['description'], matched_in=phase))
    return dict(ok=True, query=query, count=len(results), results=results,
                total_matches=len(complete), catalog_scope='canonical owners', search_scope=phase,
                limits='Search excerpts are discovery only; read the selected owner and required documents before work.')
