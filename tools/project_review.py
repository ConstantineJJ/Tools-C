"""Optional bounded project traceability review. No commands or engines are executed."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat

from check import ROOT, Violation, fields, identifier, local_path, require

PACKET_LIMIT = 1024 * 1024
TOTAL_LIMIT = 16 * PACKET_LIMIT
RECORD_LIMIT = 1024
FINDING_LIMIT = 100
SOURCE_LINE_LIMIT = 20000
HISTORY_LIMIT = 1024
ENGINE_VERSION = 'project-review-b4-b5-1'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def report_digest(report):
    return digest(json.dumps({k: v for k, v in report.items() if k != 'report_sha256'},
                             sort_keys=True, separators=(',', ':'), allow_nan=False).encode())


def engine_digest():
    paths = [Path(__file__), Path(__file__).with_name('project_review_tasks.py'),
             Path(__file__).with_name('project_review_impact.py')]
    return digest(b''.join(path.read_bytes() for path in paths))


def key(value):
    identifier(value)
    require(len(value) <= 128, 'Identifier budget exceeded', 'E_LIMIT')


def path_in(root, value):
    require(isinstance(value, str) and len(value) <= 4096, 'Path budget exceeded', 'E_LIMIT')
    return local_path(root, value)


def strict_json(raw):
    # check.read_json reads a whole file; decode our already bounded bytes instead.
    def pairs(rows):
        result = {}
        for key, value in rows:
            require(key not in result, 'Duplicate JSON key', 'E_JSON')
            result[key] = value
        return result

    def nonfinite(value):
        raise Violation('E_JSON', 'Non-finite JSON value')

    def finite(value):
        result = float(value)
        require(result not in (float('inf'), float('-inf')), 'Non-finite JSON number', 'E_JSON')
        return result

    try:
        return json.loads(raw.decode('utf-8-sig'), object_pairs_hook=pairs,
                          parse_constant=nonfinite, parse_float=finite)
    except (UnicodeError, ValueError, RecursionError) as error:
        raise Violation('E_JSON', 'Invalid bounded UTF-8 JSON') from error


def refs(values):
    require(isinstance(values, list) and all(isinstance(x, str) for x in values), 'Expected ID array')
    require(len(values) == len(set(values)), 'Duplicate reference', 'E_ID')
    for value in values:
        key(value)
    return values


def hash_value(value):
    require(isinstance(value, str) and re.fullmatch('[a-f0-9]{64}', value), 'Invalid SHA-256')


class Inputs:
    def __init__(self, project):
        self.project = Path(project).resolve()
        require(self.project.is_dir(), 'Project root must be a directory', 'E_PATH')
        self.cache = {}
        self.total = 0

    def read(self, path, limit=TOTAL_LIMIT):
        if path not in self.cache:
            try:
                require(stat.S_ISREG(path.stat().st_mode), 'Input must be a regular file', 'E_FILE')
                with path.open('rb') as handle:
                    require(stat.S_ISREG(os.fstat(handle.fileno()).st_mode),
                            'Input must be a regular file', 'E_FILE')
                    raw = handle.read(min(limit, TOTAL_LIMIT-self.total)+1)
            except OSError as error:
                raise Violation('E_FILE', 'Input could not be read') from error
            require(len(raw) <= limit and self.total+len(raw) <= TOTAL_LIMIT, 'Read budget exceeded', 'E_LIMIT')
            self.cache[path] = raw
            self.total += len(raw)
        require(len(self.cache[path]) <= limit, 'Input size limit exceeded', 'E_LIMIT')
        return self.cache[path]

    def source_root(self, label):
        require(label in ('project', 'tools'), 'Unknown source root', 'E_PATH')
        if label == 'project':
            return self.project
        config = strict_json(self.read(path_in(self.project, '.tooling/config.json'), PACKET_LIMIT))
        fields(config, ['schema_version', 'tools_root', 'profile'])
        require(type(config['schema_version']) is int and config['schema_version'] == 1, 'Unknown config schema')
        require(isinstance(config['tools_root'], str) and 0 < len(config['tools_root']) <= 4096, 'Invalid tools pointer')
        path_in(self.project, config['profile'])
        pointer = (self.project / config['tools_root']).resolve()
        require(pointer == ROOT.resolve(), 'Canonical pointer differs from installed Tools_C', 'E_PATH')
        return pointer


def load_packet(inputs, packet_path):
    packet = strict_json(inputs.read(path_in(inputs.project, packet_path), PACKET_LIMIT))
    fields(packet, ['schema_version', 'scope', 'revision', 'sources', 'requirements', 'tasks', 'artifacts', 'checks'])
    require(type(packet['schema_version']) is int and packet['schema_version'] == 1, 'Unknown review schema')
    key(packet['scope'])
    require(type(packet['revision']) is int and packet['revision'] > 0, 'Invalid requirement revision')
    collections = {}
    count = 0
    for name in ('sources', 'requirements', 'tasks', 'artifacts', 'checks'):
        rows = packet[name]
        require(isinstance(rows, list), 'Expected record array')
        count += len(rows)
        require(count <= RECORD_LIMIT, 'Record budget exceeded', 'E_LIMIT')
        indexed = {}
        for row in rows:
            require(isinstance(row, dict) and 'id' in row, 'Record needs ID')
            key(row['id'])
            require(row['id'] not in indexed, 'Duplicate scoped ID', 'E_ID')
            indexed[row['id']] = row
        collections[name] = indexed
    require(packet['requirements'], 'Scope needs at least one requirement')
    sources = {}
    for row in packet['sources']:
        fields(row, ['id', 'path', 'sha256'], ['root'])
        hash_value(row['sha256'])
        path = path_in(inputs.source_root(row.get('root', 'project')), row['path'])
        raw = inputs.read(path)
        require(digest(raw) == row['sha256'], 'Source binding is stale', 'E_HASH')
        try:
            lines = []
            for line in io.StringIO(raw.decode('utf-8-sig'), newline=None):
                require(len(lines) < SOURCE_LINE_LIMIT, 'Source line budget exceeded', 'E_LIMIT')
                lines.append(line.rstrip('\r\n'))
            sources[row['id']] = lines
        except UnicodeError as error:
            raise Violation('E_ENCODING', 'Source must be UTF-8 text') from error
    def binding(row):
        ref = row['source']
        fields(ref, ['id', 'line'])
        require(isinstance(ref['id'], str) and ref['id'] in sources, 'Unknown source reference', 'E_REF')
        require(type(ref['line']) is int and 1 <= ref['line'] <= len(sources[ref['id']]), 'Invalid source line', 'E_REF')
        marker = r'(?<![A-Za-z0-9_.-])' + re.escape(row['id']) + r'(?![A-Za-z0-9_.-])'
        require(re.search(marker, sources[ref['id']][ref['line']-1]), 'ID absent from bound source line', 'E_REF')
    for row in packet['requirements']:
        fields(row, ['id', 'source', 'description', 'mandatory', 'level', 'checks'])
        require(isinstance(row['description'], str) and 0 < len(row['description'].strip()) <= 2000, 'Invalid requirement summary')
        require(type(row['mandatory']) is bool and row['level'] in ('L1', 'L2', 'L3', 'L4'), 'Invalid requirement acceptance')
        binding(row)
        require(set(refs(row['checks'])) <= collections['checks'].keys(), 'Unknown check reference', 'E_REF')
    for row in packet['tasks']:
        fields(row, ['id', 'source', 'requirements'])
        binding(row)
        require(set(refs(row['requirements'])) <= collections['requirements'].keys(), 'Unknown requirement reference', 'E_REF')
    for row in packet['artifacts']:
        fields(row, ['id', 'path'])
        path_in(inputs.project, row['path'])
    for row in packet['checks']:
        fields(row, ['id', 'requirement', 'artifact', 'kind'], ['expected'])
        require(row['kind'] in ('file_exists', 'file_absent', 'sha256', 'manual'), 'Unsupported predicate')
        require(isinstance(row['requirement'], str) and row['requirement'] in collections['requirements'], 'Unknown requirement', 'E_REF')
        require(isinstance(row['artifact'], str) and row['artifact'] in collections['artifacts'], 'Unknown artifact', 'E_REF')
        require(row['id'] in collections['requirements'][row['requirement']]['checks'], 'Unassigned check', 'E_REF')
        if row['kind'] == 'sha256':
            hash_value(row.get('expected'))
        else:
            require('expected' not in row, 'Unexpected predicate value')
    for row in packet['requirements']:
        require(all(collections['checks'][cid]['requirement'] == row['id'] for cid in row['checks']), 'Check mapped to another requirement', 'E_REF')
    return packet, collections


def add_finding(report, req, code, target=None, gap=None, check_id=None, evidence=()):
    identity = [report['scope'], req['id'] if req else None, code, target, gap, check_id]
    row = dict(id='F-'+digest(json.dumps(identity, separators=(',', ':')).encode())[:24],
               requirement=req['id'] if req else None, code=code, artifact=target, check=check_id,
               gap_kind=gap, status='FAIL' if gap else 'review_required',
               source=req['source'] if req else None, evidence=list(evidence))
    if len(report['findings']) < FINDING_LIMIT:
        report['findings'].append(row)
    else:
        report['omitted_findings'] += 1


def analyze(inputs, packet, indexed, report):
    """Only explicit graph coverage and incompatible file predicates, never prose inference."""
    by_path = {}
    mapped_tasks = set()
    mapped_artifacts = set()
    for task in packet['tasks']:
        mapped_tasks.update(task['requirements'])
        if not task['requirements']:
            add_finding(report, None, 'ORPHAN_TASK', task['id'], evidence=[task['source']])
    for req in packet['requirements']:
        if req['id'] not in mapped_tasks or not req['checks']:
            add_finding(report, req, 'INCOMPLETE_TRACEABILITY')
        if not req['checks'] or all(indexed['checks'][c]['kind'] == 'manual' for c in req['checks']):
            add_finding(report, req, 'AMBIGUOUS_ACCEPTANCE')
    for check in sorted(packet['checks'], key=lambda c: c['id']):
        artifact = indexed['artifacts'][check['artifact']]
        mapped_artifacts.add(artifact['id'])
        path = path_in(inputs.project, artifact['path'])
        prior = by_path.setdefault(path, [])
        for other in prior:
            kinds = {other['kind'], check['kind']}
            conflict = ('file_absent' in kinds and bool(kinds & {'file_exists', 'sha256'})) or (
                check['kind'] == other['kind'] == 'sha256' and check['expected'] != other['expected'])
            duplicate = (check['kind'] != 'manual' and check['kind'] == other['kind']
                         and check.get('expected') == other.get('expected'))
            if conflict or duplicate:
                evidence = [dict(check=c['id'], requirement=c['requirement'],
                                 source=indexed['requirements'][c['requirement']]['source']) for c in (other, check)]
                # Emit one side per requirement so both mandatory rows remain open/failed.
                emitted = set()
                for c in (other, check):
                    side = (c['requirement'], c['artifact'])
                    if side in emitted:
                        continue
                    emitted.add(side)
                    req = indexed['requirements'][c['requirement']]
                    add_finding(report, req, 'FORMAL_CONFLICT' if conflict else 'DUPLICATE_ACCEPTANCE',
                                c['artifact'], 'contradicts' if conflict else None,
                                other['id']+'|'+check['id'], evidence)
        prior.append(check)
    for artifact in packet['artifacts']:
        if artifact['id'] not in mapped_artifacts:
            add_finding(report, None, 'UNMAPPED_ARTIFACT', artifact['id'])
    report['coverage'] = dict(boundary='declared_records_only', requirements=len(packet['requirements']),
                             tasks=len(packet['tasks']), artifacts=len(packet['artifacts']), checks=len(packet['checks']))


def assess(inputs, packet, indexed, report):
    results = {}

    def finding(req, code, target, gap=None, check_id=None):
        add_finding(report, req, code, target, gap, check_id)

    for row in packet['checks']:
        artifact = indexed['artifacts'][row['artifact']]
        path = path_in(inputs.project, artifact['path'])
        status, gap, observed, reason = 'UNKNOWN', None, None, 'not_checked'
        if row['kind'] != 'manual':
            try:
                mode = path.stat().st_mode
            except FileNotFoundError:
                status, gap = ('PASS', None) if row['kind'] == 'file_absent' else ('FAIL', 'missing')
            except OSError:
                reason = 'blocked'
            else:
                if row['kind'] == 'file_absent':
                    status, gap = 'FAIL', 'unrequested'
                elif not stat.S_ISREG(mode):
                    status, gap = 'FAIL', 'contradicts'
                elif row['kind'] == 'file_exists':
                    status = 'PASS'
                else:
                    try:
                        observed = digest(inputs.read(path))
                    except Violation as error:
                        if error.code != 'E_FILE':
                            raise
                        reason = 'blocked'
                    else:
                        status = 'PASS' if observed == row['expected'] else 'FAIL'
                        gap = None if status == 'PASS' else 'partial'
        result = dict(id=row['id'], requirement=row['requirement'], artifact=row['artifact'],
                      path=artifact['path'], status=status, observed_sha256=observed,
                      evidence_level='L1' if status != 'UNKNOWN' else None,
                      reason=reason if status == 'UNKNOWN' else None)
        report['checks'].append(result)
        results[row['id']] = result
        req = indexed['requirements'][row['requirement']]
        if status == 'FAIL':
            finding(req, 'PREDICATE_FAILED', row['artifact'], gap, row['id'])
        elif status == 'UNKNOWN':
            finding(req, 'CHECK_NOT_VERIFIED', row['artifact'], check_id=row['id'])

    for req in packet['requirements']:
        task_ids = [t['id'] for t in packet['tasks'] if req['id'] in t['requirements']]
        values = [results[c]['status'] for c in req['checks']]
        issues = [f for f in report['findings'] if f['requirement'] == req['id'] and
                  (f['code'] != 'FORMAL_CONFLICT' or all(
                      indexed['requirements'][e['requirement']]['mandatory'] for e in f['evidence']))]
        if 'FAIL' in values or any(f['code'] == 'FORMAL_CONFLICT' for f in issues):
            status = 'FAIL'
        elif not values or not task_ids or 'UNKNOWN' in values or req['level'] != 'L1' or issues or report['omitted_findings']:
            status = 'OPEN'
        else:
            status = 'PASS'
        if req['level'] != 'L1':
            finding(req, 'HIGHER_LEVEL_NOT_VERIFIED', None)
        report['requirements'].append(dict(id=req['id'], mandatory=req['mandatory'], level=req['level'],
                                           status=status, checks=req['checks'], tasks=task_ids, source=req['source']))
    required = [r['status'] for r in report['requirements'] if r['mandatory']]
    report['acceptance_status'] = ('FAIL' if 'FAIL' in required else
                                   'OPEN' if not required or 'OPEN' in required else 'PASS')


def load_report(inputs, path):
    report = strict_json(inputs.read(path_in(inputs.project, path), PACKET_LIMIT))
    fields(report, ['schema_version', 'operation', 'scope', 'revision', 'analysis_status',
                    'acceptance_status', 'visual_status', 'sources', 'checks', 'requirements',
                    'findings', 'omitted_findings', 'coverage', 'read_bytes', 'limits',
                    'engine_version', 'engine_sha256', 'packet', 'packet_sha256',
                    'proposed_tasks', 'history', 'report_sha256'])
    require(type(report['schema_version']) is int and report['schema_version'] == 1 and report['operation'] == 'converge' and
            report['engine_version'] == ENGINE_VERSION and report['analysis_status'] == 'PASS',
            'Unsupported previous report')
    hash_value(report['report_sha256'])
    require(report_digest(report) == report['report_sha256'], 'Report fingerprint differs', 'E_HASH')
    key(report['scope'])
    require(type(report['revision']) is int and report['revision'] > 0, 'Invalid report revision')
    for name in ('findings', 'history', 'proposed_tasks'):
        require(isinstance(report[name], list) and len(report[name]) <= HISTORY_LIMIT, 'Report record limit', 'E_LIMIT')
    validated_history(report)
    return report


def validated_history(report):
    history = {}
    total = 0
    for row in report['history']:
        fields(row, ['id', 'observations'])
        key(row['id'])
        require(row['id'] not in history and isinstance(row['observations'], list) and row['observations'],
                'Duplicate/empty finding history', 'E_ID')
        total += len(row['observations'])
        require(total <= HISTORY_LIMIT, 'History budget exceeded', 'E_LIMIT')
        observations = []
        for obs in row['observations']:
            fields(obs, ['revision', 'state_sha256', 'status'])
            require(type(obs['revision']) is int and 0 < obs['revision'] <= report['revision'] and
                    obs['status'] in ('FAIL', 'review_required', 'not_observed', 'not_reported'), 'Invalid history')
            hash_value(obs['state_sha256'])
            observations.append(dict(obs))
        history[row['id']] = dict(id=row['id'], observations=observations)
    return history


def observation_digest(report):
    return digest(json.dumps([report['revision'], report['packet_sha256'], report['checks']],
                             sort_keys=True, separators=(',', ':')).encode())


def convergence(report, previous):
    report['proposed_tasks'] = [dict(finding=f['id'], requirement=f['requirement'],
                                     artifact=f['artifact'], check=f['check'], gap_kind=f['gap_kind'])
                               for f in report['findings'] if f['code'] == 'PREDICATE_FAILED' and f['gap_kind']]
    history = {}
    if previous is not None:
        require(previous['scope'] == report['scope'] and previous['revision'] <= report['revision'],
                'History scope/revision mismatch', 'E_REF')
        history = validated_history(previous)
    state = observation_digest(report)
    current = {f['id']: f for f in report['findings']}
    for fid in sorted(set(history) | set(current)):
        row = history.setdefault(fid, dict(id=fid, observations=[]))
        status = current[fid]['status'] if fid in current else (
            'not_reported' if report['omitted_findings'] else 'not_observed')
        obs = dict(revision=report['revision'], state_sha256=state, status=status)
        if not row['observations'] or row['observations'][-1] != obs:
            row['observations'].append(obs)
    require(sum(len(r['observations']) for r in history.values()) <= HISTORY_LIMIT, 'History budget exceeded', 'E_LIMIT')
    report['history'] = list(history.values())


def review(project, packet_path, *, operation='validate', previous=None, _inputs=None,
           changed_source=None, changed_rule=None):
    require(operation in ('validate', 'analyze', 'converge', 'impact'), 'Operation not implemented')
    require(operation == 'impact' or (changed_source is None and changed_rule is None), 'Change selection requires impact')
    inputs = _inputs if _inputs is not None else Inputs(project)
    require(inputs.project == Path(project).resolve(), 'Input root mismatch', 'E_PATH')
    packet, indexed = load_packet(inputs, packet_path)
    require(previous is None or operation == 'converge', 'History requires convergence')
    prior = load_report(inputs, previous) if previous else None
    report = dict(schema_version=1, operation=operation, scope=packet['scope'], revision=packet['revision'],
                  analysis_status='PASS', acceptance_status='NOT_EVALUATED', visual_status='NOT_EVALUATED',
                  sources=packet['sources'], checks=[], requirements=[], findings=[], omitted_findings=0,
                  coverage=None, engine_version=ENGINE_VERSION, engine_sha256=engine_digest(),
                  packet=packet_path, packet_sha256=digest(inputs.read(path_in(inputs.project, packet_path))),
                  proposed_tasks=[], history=[])
    if operation in ('analyze', 'converge'):
        analyze(inputs, packet, indexed, report)
    if operation == 'impact':
        from project_review_impact import build
        report['impact'] = build(inputs, packet, indexed, changed_source=changed_source, changed_rule=changed_rule)
        report['coverage'] = report['impact']['coverage']
    if operation == 'converge':
        assess(inputs, packet, indexed, report)
        convergence(report, prior)
    report['read_bytes'] = inputs.total
    report['limits'] = 'Declared graph/predicates only; prose authority and semantic conflicts require review. History is not current verification. No engine/pixel evaluation, atomic read snapshot or source edits.'
    report['report_sha256'] = report_digest(report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['validate', 'analyze', 'converge', 'impact', 'apply-tasks'])
    parser.add_argument('packet')
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--previous')
    parser.add_argument('--todo')
    parser.add_argument('--expected-sha256')
    parser.add_argument('--namespace')
    parser.add_argument('--start', type=int)
    parser.add_argument('--exclusive-writer', action='store_true')
    changes = parser.add_mutually_exclusive_group()
    changes.add_argument('--changed-source')
    changes.add_argument('--changed-rule')
    args = parser.parse_args()
    if (args.operation == 'impact') != bool(args.changed_source or args.changed_rule):
        parser.error('Only impact requires one of --changed-source or --changed-rule')
    write_options = (args.todo, args.expected_sha256, args.namespace, args.start)
    if args.operation == 'apply-tasks':
        if not all(v is not None for v in write_options) or not args.exclusive_writer or args.previous:
            parser.error('apply-tasks requires --todo, --expected-sha256, --namespace, --start, --exclusive-writer; no --previous')
    elif any(v is not None for v in write_options) or args.exclusive_writer:
        parser.error('Task write options require apply-tasks')
    if args.previous and args.operation != 'converge':
        parser.error('--previous requires converge')
    try:
        if args.operation == 'apply-tasks':
            from project_review_tasks import apply_tasks
            result = apply_tasks(args.project, args.packet, args.todo, args.expected_sha256,
                                 namespace=args.namespace, start=args.start, exclusive_writer=args.exclusive_writer)
        else:
            result = review(args.project, args.packet, operation=args.operation, previous=args.previous,
                            changed_source=args.changed_source, changed_rule=args.changed_rule)
    except (Violation, OSError, ValueError, TypeError, KeyError, RecursionError) as error:
        print(json.dumps(dict(analysis_status='FAIL', acceptance_status='NOT_EVALUATED',
                             error=getattr(error, 'code', 'E_INPUT'), message='Invalid, stale, unsupported or out-of-scope review input')))
        return 1
    print(json.dumps(result, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
