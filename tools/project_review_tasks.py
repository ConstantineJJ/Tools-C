"""Explicit task-only writer for project_review; no implementation or task completion."""
import json
from contextlib import contextmanager
import os
from pathlib import Path
import re
import tempfile

import project_review as pr
from check import fields, require


@contextmanager
def owned_lock(path):
    handle = path.open('xb')
    try:
        with handle:
            yield
    finally:
        path.unlink()


def marker(scope, edge):
    return f'<!-- tools-c:convergence {scope} {edge} -->'.encode()


def proposal_identity(scope, proposal):
    fields(proposal, ['finding', 'requirement', 'artifact', 'check', 'gap_kind'])
    for name in ('finding', 'requirement', 'artifact', 'check'):
        pr.key(proposal[name])
    require(proposal['gap_kind'] in ('missing', 'partial', 'contradicts', 'unrequested'), 'Invalid gap kind')
    identity = [scope, proposal['requirement'], 'PREDICATE_FAILED', proposal['artifact'], proposal['gap_kind'], proposal['check']]
    expected = 'F-'+pr.digest(json.dumps(identity, separators=(',', ':')).encode())[:24]
    require(proposal['finding'] == expected, 'Finding identity differs', 'E_TASKS')
    return {k: v for k, v in proposal.items() if k != 'finding'}


def finding_history(report, finding):
    row = next((r for r in report['history'] if r['id'] == finding), None)
    require(row is not None and row['observations'], 'Missing finding observation', 'E_TASKS')
    require(row['observations'][-1] == dict(revision=report['revision'],
            state_sha256=pr.observation_digest(report), status='FAIL'),
            'Finding history does not end at the current gap', 'E_TASKS')
    return row['observations']


def history_tokens(history):
    # Prefix fingerprints distinguish a new occurrence from a replay, in O(n).
    token = ''
    for observation in history:
        token = pr.digest((token+json.dumps(observation, sort_keys=True, separators=(',', ':'))).encode())
        yield token


def task_observation(report, finding):
    tokens = list(history_tokens(finding_history(report, finding)))
    return dict(revision=report['revision'], state_sha256=pr.observation_digest(report),
                report_sha256=report['report_sha256'], history_sha256=tokens[-1])


def observation_recorded(entries, report, finding):
    existing = [e for e in entries if e['data']['finding'] == finding]
    if not existing:
        return False
    history = finding_history(report, finding)
    last = existing[-1]['data']['observations'][-1]
    if last['state_sha256'] != history[-1]['state_sha256']:
        return False
    tokens = list(history_tokens(history))
    if 'history_sha256' in last:
        # An extension past the recorded observation proves a later occurrence,
        # even if the final state is byte-identical to the original failure.
        return last['history_sha256'] not in tokens[:-1]
    # Legacy task metadata has only a state fingerprint. Recognize a return to
    # that state only with an explicit intervening different observation.
    seen = False
    for observation in history[:-1]:
        if seen and observation['state_sha256'] != last['state_sha256']:
            return False
        seen = seen or observation['state_sha256'] == last['state_sha256']
    return True


def read_section(raw, scope, namespace):
    begin, end = marker(scope, 'begin'), marker(scope, 'end')
    require(raw.count(begin) == raw.count(end) and raw.count(begin) <= 1, 'Ambiguous managed section', 'E_TASKS')
    if begin not in raw:
        return raw, [], b''
    start, finish = raw.index(begin), raw.index(end)
    require(start < finish and (start == 0 or raw[start-1:start] == b'\n') and
            raw[start+len(begin):start+len(begin)+1] in (b'\r', b'\n') and raw[finish-1:finish] == b'\n' and
            raw[finish+len(end):finish+len(end)+1] in (b'', b'\r', b'\n'), 'Invalid section boundary', 'E_TASKS')
    body = raw[start+len(begin):finish].decode('utf-8').strip('\r\n')
    lines = body.splitlines()
    require(len(lines) % 2 == 0 and len(lines) <= 2*pr.RECORD_LIMIT, 'Invalid task section', 'E_TASKS')
    entries, ids = [], set()
    for i in range(0, len(lines), 2):
        match = re.fullmatch(r'- \[([ xX])\] ('+re.escape(namespace)+r'[1-9][0-9]*) .+', lines[i])
        require(match is not None, 'Managed task was edited incompatibly', 'E_TASKS')
        meta = re.fullmatch(r'<!-- tools-c:task (.+) -->', lines[i+1])
        require(meta is not None, 'Missing managed metadata', 'E_TASKS')
        data = pr.strict_json(meta[1].encode())
        fields(data, ['id', 'finding', 'identity', 'observations', 'previous'])
        require(data['id'] == match[2] and data['id'] not in ids, 'Duplicate task identity', 'E_TASKS')
        pr.key(data['id'])
        pr.key(data['finding'])
        proposal_identity(scope, dict(data['identity'], finding=data['finding']))
        require(data['previous'] is None or isinstance(data['previous'], str), 'Invalid recurrence')
        if data['previous'] is not None:
            require(data['previous'] in ids, 'Recurrence must reference an earlier task', 'E_TASKS')
        require(isinstance(data['observations'], list) and data['observations'], 'Missing history', 'E_TASKS')
        for obs in data['observations']:
            fields(obs, ['revision', 'report_sha256', 'state_sha256'], ['history_sha256'])
            require(type(obs['revision']) is int and obs['revision'] > 0, 'Invalid task history')
            pr.hash_value(obs['report_sha256'])
            pr.hash_value(obs['state_sha256'])
            if 'history_sha256' in obs:
                pr.hash_value(obs['history_sha256'])
        ids.add(data['id'])
        entries.append(dict(line=lines[i], closed=match[1] != ' ', data=data))
    require(sum(len(e['data']['observations']) for e in entries) <= pr.HISTORY_LIMIT, 'Task history limit', 'E_LIMIT')
    return raw[:start], entries, raw[finish+len(end):]


def task_update(raw, report, namespace, start):
    require(len(raw) <= pr.PACKET_LIMIT, 'Todo input budget exceeded', 'E_LIMIT')
    prefix, entries, suffix = read_section(raw, report['scope'], namespace)
    created, updated = [], []
    known = set(re.findall(rb'^\s*[-*] \[[ xX]\] ('+namespace.encode()+rb'[1-9][0-9]*)\b', raw, re.M))
    known.update(t.encode() for r in report['requirements'] for t in r['tasks'])
    numbers = [int(t[len(namespace):]) for t in known if re.fullmatch(namespace.encode()+rb'[1-9][0-9]*', t)]
    next_id = max([start-1]+numbers)+1
    for proposal in report['proposed_tasks']:
        existing = [e for e in entries if e['data']['finding'] == proposal['finding']]
        identity = proposal_identity(report['scope'], proposal)
        require(all(e['data']['identity'] == identity for e in existing), 'Conflicting task identity', 'E_TASKS')
        require(sum(not e['closed'] for e in existing) <= 1, 'Duplicate active occurrence', 'E_TASKS')
        obs = task_observation(report, proposal['finding'])
        if observation_recorded(entries, report, proposal['finding']):
            continue
        if existing and not existing[-1]['closed']:
            existing[-1]['data']['observations'].append(obs)
            updated.append(existing[-1]['data']['id'])
            continue
        previous = existing[-1]['data']['id'] if existing else None
        task_id = namespace+str(next_id)
        pr.key(task_id)
        next_id += 1
        # Only validated IDs/classifiers, never untrusted prose or commands.
        title = f"- [ ] {task_id} Review {proposal['requirement']}: {proposal['gap_kind']} ({proposal['artifact']}); {proposal['finding']}"
        if previous:
            title += f'; previous {previous}'
        entries.append(dict(line=title, closed=False, data=dict(id=task_id, finding=proposal['finding'], identity=identity,
                            observations=[obs], previous=previous)))
        created.append(task_id)
    require(len(entries) <= pr.RECORD_LIMIT and sum(len(e['data']['observations']) for e in entries) <= pr.HISTORY_LIMIT,
            'Task/history budget exceeded', 'E_LIMIT')
    if not created and not updated:
        return raw, created, updated
    nl = b'\r\n' if b'\r\n' in raw else b'\n'
    if prefix and not prefix.endswith(b'\n'):
        prefix += nl
    body = []
    for entry in entries:
        body.extend([entry['line'].encode(), ('<!-- tools-c:task '+json.dumps(entry['data'], sort_keys=True)+' -->').encode()])
    output = prefix+marker(report['scope'], 'begin')+nl+nl.join(body)+nl+marker(report['scope'], 'end')
    output += suffix if suffix else nl
    require(len(output) <= pr.PACKET_LIMIT, 'Todo output budget exceeded', 'E_LIMIT')
    return output, created, updated


def apply_tasks(project, report_path, todo_path, expected_sha256, *, namespace, start, exclusive_writer=False):
    require(exclusive_writer is True, 'Exclusive writer ownership must be confirmed', 'E_TASKS')
    require(isinstance(namespace, str) and re.fullmatch('[A-Za-z]{1,16}', namespace), 'Invalid task namespace')
    require(type(start) is int and 1 <= start <= 1000000, 'Invalid starting task number')
    pr.hash_value(expected_sha256)
    inputs = pr.Inputs(project)
    report = pr.load_report(inputs, report_path)
    target = pr.path_in(inputs.project, todo_path)
    require(target.suffix.lower() == '.md', 'Task target must be existing Markdown', 'E_PATH')
    require(target != pr.path_in(inputs.project, report_path) and target != pr.path_in(inputs.project, report['packet']),
            'Task target cannot overwrite report/packet', 'E_PATH')
    raw = inputs.read(target, pr.PACKET_LIMIT)
    require(pr.digest(raw) == expected_sha256, 'Todo changed since selection', 'E_HASH')
    require(not report['omitted_findings'] and not any(f['code'] == 'FORMAL_CONFLICT' for f in report['findings']),
            'Incomplete/conflicting analysis requires manual review', 'E_TASKS')
    # A report already represented in the owned block is a safe replay NO-OP,
    # even if that previous append invalidated the old source hash. No PASS reused.
    _, entries, _ = read_section(raw, report['scope'], namespace)
    for p in report['proposed_tasks']:
        proposal_identity(report['scope'], p)
    if report['proposed_tasks'] and all(observation_recorded(entries, report, p['finding'])
                                      for p in report['proposed_tasks']):
        return dict(written=False, created=[], updated=[], todo_sha256=expected_sha256, reason='already_recorded')
    fresh = pr.review(project, report['packet'], operation='converge', _inputs=inputs)
    # History/read byte counts may differ; no old predicate/status/proposal is trusted.
    for field in ('packet_sha256', 'scope', 'revision', 'sources', 'checks', 'requirements', 'findings',
                  'omitted_findings', 'coverage', 'engine_version', 'engine_sha256', 'acceptance_status', 'proposed_tasks'):
        require(report[field] == fresh[field], 'Report is stale or modified', 'E_HASH')
    new_raw, created, updated = task_update(raw, report, namespace, start)
    if new_raw == raw:
        return dict(written=False, created=[], updated=[], todo_sha256=expected_sha256, reason='no_actionable_gap')
    lock = target.with_name(target.name+'.tools-c-review.lock')
    temp_path = None
    # This guard coordinates cooperating writers only. The caller must own the
    # target exclusively; atomic replace is not an OS compare-and-swap primitive.
    with owned_lock(lock):
        try:
            inputs.cache.pop(target, None)
            require(pr.path_in(inputs.project, todo_path) == target and
                    pr.digest(inputs.read(target, pr.PACKET_LIMIT)) == expected_sha256,
                    'Concurrent todo edit', 'E_HASH')
            mode = target.stat().st_mode
            with tempfile.NamedTemporaryFile(mode='wb', dir=target.parent, prefix='.tools-c-review-', delete=False) as handle:
                temp_path = Path(handle.name)
                handle.write(new_raw)
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(temp_path, mode)
            inputs.cache.pop(target, None)
            require(pr.path_in(inputs.project, todo_path) == target and
                    pr.digest(inputs.read(target, pr.PACKET_LIMIT)) == expected_sha256,
                    'Concurrent todo edit before replace', 'E_HASH')
            os.replace(temp_path, target)
            temp_path = None
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)
    return dict(written=True, created=created, updated=updated, todo_sha256=pr.digest(new_raw))
