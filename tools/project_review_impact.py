"""Read-only dependency observations over hash-bound, explicitly selected sources."""
from collections import deque
from bisect import bisect_right
import ast
import json
import re
from urllib.parse import unquote, urlsplit

import project_review as pr
from check import fields, local_path, require, strings, validate_contract

EDGE_LIMIT = 4096


def masked_markdown(text):
    """Same small link grammar as L1; preserve physical lines without unbounded reads."""
    def blank(value):
        return re.sub(r'[^\n]', ' ', value)
    lines, fence = [], None
    for line in text.splitlines(keepends=True):
        match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)', line)
        if fence is not None:
            lines.append(blank(line))
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                fence = None
        elif match:
            fence = match[1]
            lines.append(blank(line))
        else:
            lines.append(line)
    text = ''.join(lines)
    start, cursor, pieces = text.find('<!--'), 0, []
    while start >= 0:
        end = text.find('-->', start+4)
        end = len(text) if end < 0 else end+3
        pieces.extend([text[cursor:start], blank(text[start:end])])
        cursor = end
        start = text.find('<!--', end)
    pieces.append(text[cursor:])
    text = ''.join(pieces)
    return re.sub(r'`+[^`\n]*`+', lambda m: blank(m[0]), text)


def markdown_refs(text):
    text = masked_markdown(text)
    newlines = [m.start() for m in re.finditer('\n', text)]
    # Excluding nested '[' avoids a failed match scanning a whole line per '['.
    inline = r'\[[^\[\]\n]*\]\((<[^<>\n]*>|[^()\s]+)(?:[ \t]+"[^"\n]*")?\)'
    definitions = r'(?m)^ {0,3}\[[^\[\]\n]+\]:[ \t]*(<[^<>\n]*>|[^\s]+)'
    for pattern in (inline, definitions):
        for match in re.finditer(pattern, text):
            yield match[1].strip('<>'), bisect_right(newlines, match.start())+1


def source_kind(path):
    if path.name == 'SKILL.md': return 'skill'
    if path.name.startswith('test_'): return 'test'
    if path.name in ('check.py', 'qa_gate.py'): return 'gate'
    if path.suffix == '.py': return 'cli_mcp'
    if path.suffix == '.md': return 'doc'
    return 'other'


def build(inputs, packet, indexed, *, changed_source=None, changed_rule=None):
    require((changed_source is None) != (changed_rule is None), 'Select one changed source or requirement')
    if changed_rule is not None:
        pr.key(changed_rule)
        require(changed_rule in indexed['requirements'], 'Unknown changed requirement', 'E_REF')
        changed_source = indexed['requirements'][changed_rule]['source']['id']
    pr.key(changed_source)
    require(changed_source in indexed['sources'], 'Unknown changed source', 'E_REF')
    sources, selected = {}, {}
    for row in sorted(packet['sources'], key=lambda r: r['id']):
        root = inputs.source_root(row.get('root', 'project'))
        path = pr.path_in(root, row['path'])
        source = dict(row=row, root=root, path=path, text=inputs.read(path).decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n'))
        sources[row['id']] = source
        selected.setdefault(path, source)
    changed = sources[changed_source]
    edges, unknown, supported = [], [], set()
    catalog = {}
    parsed = {}
    literal_paths = {}
    for path, source in selected.items():
        literal_paths.setdefault(source['row']['path'], set()).add(path)

    def observe():
        require(len(edges)+len(unknown) < EDGE_LIMIT, 'Impact observation budget exceeded', 'E_LIMIT')

    def note(**row):
        observe()
        unknown.append(row)

    def edge(source, target, kind, **evidence):
        observe()
        target_row = selected[target]['row'] if target in selected else None
        edges.append(dict(consumer=source['path'], target=target, kind=kind,
                          evidence=dict(source=source['row']['id'],
                                        target_source=target_row['id'] if target_row else None, **evidence)))

    def file_edge(source, target, relation, pointer):
        edge(source, pr.path_in(source['root'], target), 'direct',
             relation=relation, pointer=pointer, granularity='file')

    # Parse only selected JSON; never call catalog/profile loaders that traverse files.
    for path, source in selected.items():
        if path.suffix.lower() != '.json':
            continue
        raw = inputs.read(path, pr.PACKET_LIMIT)
        data = pr.strict_json(raw)
        parsed[path] = data
        if isinstance(data, dict) and 'blender_aliases' in data:
            fields(data, ['schema_version', 'version', 'skills', 'blender_aliases'])
            require(type(data['schema_version']) is int and data['schema_version'] == 1, 'Unsupported manifest')
            require(isinstance(data['version'], str) and isinstance(data['skills'], list) and
                    isinstance(data['blender_aliases'], dict), 'Invalid manifest mappings')
            ids = set()
            for i, row in enumerate(data['skills']):
                fields(row, ['id', 'path'])
                pr.key(row['id'])
                require(row['id'] not in ids, 'Duplicate manifest identity', 'E_ID')
                ids.add(row['id'])
                target = pr.path_in(source['root'], row['path'])
                catalog.setdefault(row['id'], set()).add(target)
                file_edge(source, row['path'], 'catalog_skill', f'/skills/{i}/path')
            for alias, row in data['blender_aliases'].items():
                pr.key(alias)
                fields(row, ['reference', 'source_sha256', 'source_version'])
                require(alias not in ids, 'Alias collides with canonical identity', 'E_ID')
                pr.hash_value(row['source_sha256'])
                require(isinstance(row['source_version'], str), 'Invalid alias provenance')
                target = pr.path_in(source['root'], row['reference'])
                catalog.setdefault(alias, set()).add(target)
                file_edge(source, row['reference'], 'alias_reference', f'/blender_aliases/{alias}/reference')
            source['kind'] = 'manifest'
            supported.add(path)

    for path, source in selected.items():
        if path.suffix.lower() == '.md':
            supported.add(path)
            if path.name == 'SKILL.md' and '<!-- tools-c-router -->' in source['text']:
                source['kind'] = 'alias_router'
                note(source=source['row']['id'], reason='router_runtime_context_not_evaluated')
            for target, line in markdown_refs(source['text']):
                uri = urlsplit(target)
                if uri.scheme or uri.netloc:
                    require(not uri.netloc or bool(uri.scheme), 'Network path is outside scope', 'E_PATH')
                    require(uri.scheme.lower() in ('http', 'https', 'mailto', 'app', 'codex', 'plugin'),
                            'Unsupported/absolute local URI', 'E_PATH')
                    note(source=source['row']['id'], reason='external_link_not_followed', line=line)
                elif uri.path:
                    relative = unquote(uri.path)
                    # The same containment rule as L1, with document-relative resolution.
                    require(len(relative) <= 4096, 'Reference path budget exceeded', 'E_LIMIT')
                    resolved = local_path(source['root'], relative, path.parent)
                    edge(source, resolved, 'direct', line=line, relation='markdown_link', granularity='file')
        elif path.suffix.lower() == '.json':
            data = parsed[path]
            if path in supported:
                continue
            if isinstance(data, dict) and 'rules' in data and 'id' in data:
                validate_contract(data, set())
                for i, rule in enumerate(data['rules']):
                    for name in ('paths', 'required_targets'):
                        for j, target in enumerate(rule.get(name, [])):
                            file_edge(source, target, 'contract_'+name, f'/rules/{i}/{name}/{j}')
                source['kind'] = 'contract'
                supported.add(path)
            elif isinstance(data, dict) and {'skills', 'contracts', 'references'} <= data.keys():
                fields(data, ['schema_version', 'id', 'skills', 'contracts', 'references'],
                       ['adapter', 'local_skill_roots', 'review_state'])
                require(type(data['schema_version']) is int and data['schema_version'] == 1, 'Unsupported profile')
                pr.key(data['id'])
                for name in ('contracts', 'references'):
                    for i, target in enumerate(strings(data[name])):
                        file_edge(source, target, 'profile_'+name, f'/{name}/{i}')
                for i, sid in enumerate(pr.refs(data['skills'])):
                    candidates = catalog.get(sid, set())
                    if len(candidates) == 1:
                        edge(source, next(iter(candidates)), 'direct', relation='profile_skill',
                             pointer=f'/skills/{i}', granularity='file')
                    else:
                        note(source=source['row']['id'], reason='unresolved_skill_id', pointer=f'/skills/{i}')
                source['kind'] = 'profile'
                supported.add(path)
            else:
                note(source=source['row']['id'], reason='unsupported_json_schema')
        elif path.suffix.lower() == '.py':
            require(len(inputs.read(path)) <= pr.PACKET_LIMIT, 'Python source budget exceeded', 'E_LIMIT')
            try:
                tree = ast.parse(source['text'])
            except (SyntaxError, ValueError, RecursionError):
                note(source=source['row']['id'], reason='python_syntax_not_analyzed')
                continue
            supported.add(path)
            for count, node in enumerate(ast.walk(tree)):
                require(count < 50000, 'Python AST budget exceeded', 'E_LIMIT')
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in literal_paths:
                    candidates = literal_paths[node.value]
                    if len(candidates) == 1:
                        edge(source, next(iter(candidates)), 'possible', relation='python_path_literal',
                             line=node.lineno, granularity='file')
                    else:
                        note(source=source['row']['id'], reason='ambiguous_path_literal', line=node.lineno)
                if not isinstance(node, (ast.Import, ast.ImportFrom)):
                    continue
                modules = [a.name for a in node.names] if isinstance(node, ast.Import) or node.module is None else [node.module]
                for module in modules:
                    candidates = [p for p in selected if p.suffix == '.py' and p.stem == module.split('.')[-1]]
                    if len(candidates) == 1:
                        edge(source, candidates[0], 'possible', relation='python_import', line=node.lineno, granularity='module')
                    else:
                        note(source=source['row']['id'], reason='import_target_not_selected_or_ambiguous', line=node.lineno)
        else:
            note(source=source['row']['id'], reason='unsupported_source_type')

    # Existing explicit traceability also proves a source-file dependency.
    for task in packet['tasks']:
        source = sources[task['source']['id']]
        for rid in task['requirements']:
            if changed_rule is not None and rid != changed_rule:
                continue
            target = sources[indexed['requirements'][rid]['source']['id']]['path']
            edge(source, target, 'direct', line=task['source']['line'], relation='task_requirement',
                 requirement=rid, granularity='requirement' if changed_rule else 'file')

    for row in edges:
        if row['target'] not in selected:
            note(source=row['evidence']['source'], reason='dependency_target_not_selected')

    reverse = {}
    for row in sorted(edges, key=lambda r: r['kind'] != 'direct'):
        reverse.setdefault(row['target'], []).append(row)
    reached = {changed['path']: []}
    queue = deque([changed['path']])
    while queue:
        for row in reverse.get(queue.popleft(), []):
            if row['consumer'] not in reached:
                reached[row['consumer']] = [row]+reached[row['target']]
                queue.append(row['consumer'])
    result = dict(change=dict(source=changed_source, requirement=changed_rule,
                              selection='operator_supplied; no before/after delta inferred', **changed['row']),
                  direct=[], possible=[], unknown=[], not_observed=[], omitted={},
                  coverage=dict(complete=False, boundary='selected_hash_bound_sources_only', selected_sources=len(sources),
                                observed_edges=len(edges), observed_unknowns=len(unknown),
                                limits='No all-project/external scan or semantic proof; AST imports do not resolve runtime search paths'),
                  schema_migration=dict(status='UNKNOWN', reason='No before/after schema compatibility evidence supplied'),
                  executed_checks=[dict(level='L1', check='packet_source_binding_and_graph_validation', status='PASS')],
                  recommended_checks=[dict(level=level, check=check, status='NOT_RUN', applicability='scope_review_required')
                                      for level, check in [('L1', 'affected_reference_and_contract_checks'),
                                                           ('L2', 'affected_engine_integration'),
                                                           ('L3', 'affected_runtime_consumers'),
                                                           ('L4', 'human_rule_or_visual_review')]])
    budget = 0
    def append(bucket, row):
        nonlocal budget
        if budget < pr.FINDING_LIMIT:
            result[bucket].append(row)
            budget += 1
        else:
            result['omitted'][bucket] = result['omitted'].get(bucket, 0)+1
    for path, source in sorted(selected.items(), key=lambda item: item[1]['row']['id']):
        if path == changed['path']:
            continue
        chain = reached.get(path)
        if chain:
            bucket = 'direct' if len(chain) == 1 and chain[0]['kind'] == 'direct' else 'possible'
            # Include all one-hop reasons (e.g. catalog skill plus legacy alias).
            rows = [r for r in edges if r['consumer'] == path and r['target'] == changed['path']] if len(chain) == 1 else chain
            evidence = [dict(row['evidence'], kind=row['kind']) for row in rows[:16]]
            identity = [packet['scope'], changed_source, source['row']['id'], bucket]
            append(bucket, dict(id='I-'+pr.digest(json.dumps(identity, separators=(',', ':')).encode())[:24], source=source['row']['id'],
                                path=source['row']['path'], root=source['row'].get('root', 'project'),
                                sha256=source['row']['sha256'], kind=source.get('kind', source_kind(path)),
                                evidence=evidence, omitted_evidence=max(0,len(rows)-16)))
        elif path in supported:
            append('not_observed', source['row']['id'])
    for row in unknown:
        append('unknown', row)
    append('unknown', dict(source=None, reason='unselected_and_external_consumers_not_scanned'))
    return result
