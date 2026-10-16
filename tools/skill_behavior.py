"""Prepare/review bounded trial evidence. Never launches agents, models or engines."""
import argparse
import hashlib
import json
from pathlib import Path
import re

from check import ROOT, Violation, existing, fields, identifier, read_json, require


def scenarios():
    data = read_json(ROOT/'tests/skill_behavior_cases.json')
    fields(data, ['schema_version', 'scope', 'discovery', 'pressure'])
    require(type(data['schema_version']) is int and data['schema_version'] == 1, 'Unsupported scenario schema')
    seen = set()
    for row in data['discovery'] + data['pressure']:
        identifier(row['id'])
        require(row['id'] not in seen, 'Duplicate scenario ID')
        seen.add(row['id'])
    return dict(discovery=data['discovery'], pressure=data['pressure'])


def prepare(scenario_id, condition, root, skill_id, rule):
    require(condition in ('baseline', 'with-rule'), 'Invalid condition')
    identifier(skill_id)
    case = next((r for r in scenarios()['pressure'] if r['id'] == scenario_id), None)
    require(case is not None, 'Unknown pressure scenario')
    path = existing(Path(root), rule)
    return dict(schema_version=1, scenario_id=scenario_id, condition=condition,
                run_kind='agent', rule=dict(id=skill_id, path=rule, sha256=hashlib.sha256(path.read_bytes()).hexdigest()),
                environment=dict(model=None, harness=None, settings=None, budget=None),
                controls={}, transcript=None, review=dict(status='NOT_RUN', reviewer=None),
                checkpoints=[dict(id=c, status='NOT_RUN', evidence=[]) for c in case['checkpoints']])


def _artifact(row, root):
    fields(row, ['path', 'sha256'])
    require(isinstance(row['sha256'], str) and re.fullmatch('[a-f0-9]{64}', row['sha256']), 'Invalid artifact hash')
    path = existing(root, row['path'])
    require(path.stat().st_size <= 16*1024*1024, 'Artifact exceeds bounded trial limit')
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == row['sha256'], 'Stale artifact')
    return raw


def evaluate(trial, root):
    """Validate attestations and file bindings, not the truth of reviewer opinions."""
    try:
        root = Path(root).resolve(strict=True)
        fields(trial, ['schema_version', 'scenario_id', 'condition', 'run_kind', 'rule', 'environment',
                       'controls', 'transcript', 'review', 'checkpoints'])
        require(type(trial['schema_version']) is int and trial['schema_version'] == 1, 'Unsupported trial schema')
        require(trial['condition'] in ('baseline', 'with-rule') and trial['run_kind'] in ('offline', 'agent'), 'Invalid trial kind')
        rule = trial['rule']; fields(rule, ['id', 'path', 'sha256']); identifier(rule['id'])
        _artifact(dict(path=rule['path'], sha256=rule['sha256']), root)
        case = next((r for r in scenarios()['pressure'] if r['id'] == trial['scenario_id']), None)
        require(case is not None, 'Unknown scenario')
        environment = trial['environment']; fields(environment, ['model', 'harness', 'settings', 'budget'])
        fields(trial['review'], ['status', 'reviewer'])
        require(trial['review']['status'] in ('NOT_RUN', 'REVIEWED'), 'Invalid review state')
        require(isinstance(trial['checkpoints'], list) and len(trial['checkpoints']) == len(case['checkpoints']), 'Incomplete checkpoint set')
        require([r['id'] for r in trial['checkpoints']] == case['checkpoints'], 'Checkpoint identity/order differs')
        transcript = trial['transcript']
        line_count = len(_artifact(transcript, root).splitlines()) if transcript else 0
        complete = bool(transcript)
        failed = False
        for row in trial['checkpoints']:
            fields(row, ['id', 'status', 'evidence'])
            require(row['status'] in ('PASS', 'FAIL', 'SKIP', 'NOT_RUN'), 'Invalid checkpoint status')
            require(isinstance(row['evidence'], list) and len(row['evidence']) <= 32, 'Invalid evidence list')
            complete = complete and row['status'] in ('PASS', 'FAIL') and bool(row['evidence'])
            failed = failed or row['status'] == 'FAIL'
            for ref in row['evidence']:
                fields(ref, ['path', 'sha256', 'line'])
                require(transcript and ref['path'] == transcript['path'] and ref['sha256'] == transcript['sha256'], 'Evidence is not bound to this transcript')
                require(type(ref['line']) is int and 1 <= ref['line'] <= line_count, 'Evidence line outside transcript')
        require(isinstance(trial['controls'], dict), 'Invalid controls')
        require(all(isinstance(k, str) and isinstance(v, str) and re.fullmatch('[a-f0-9]{64}', v)
                    for k, v in trial['controls'].items()), 'Controls must be fingerprints')
        available = (all(isinstance(environment[k], str) and environment[k].strip() for k in ('model', 'harness'))
                     and isinstance(environment['settings'], dict)
                     and isinstance(environment['settings'].get('budget_unit'), str)
                     and bool(environment['settings']['budget_unit'].strip())
                     and type(environment['budget']) is int and environment['budget'] > 0)
        reviewed = (trial['review']['status'] == 'REVIEWED' and isinstance(trial['review']['reviewer'], str)
                    and bool(trial['review']['reviewer'].strip()))
        status = ('FAIL' if failed else 'PASS') if complete and available and reviewed and trial['run_kind'] == 'agent' else 'SKIP'
        return dict(evidence_status='PASS' if complete else 'SKIP', behavioral_status=status,
                    scenario_id=trial['scenario_id'], condition=trial['condition'],
                    reason='Observed checkpoints reviewed' if status != 'SKIP' else 'Real comparable run, complete trace or review unavailable',
                    limits='File/line bindings validate reviewer attestations; no agent was run by this utility and reviewer truth is not inferred from strings.')
    except (Violation, ValueError, TypeError, KeyError, OSError, AttributeError):
        return dict(evidence_status='FAIL', behavioral_status='SKIP', reason='Invalid, stale or out-of-root trial evidence',
                    limits='No execution or behavioral claim can be made from invalid evidence')


def compare(baseline, with_rule, root):
    a, b = evaluate(baseline, root), evaluate(with_rule, root)
    comparable = (a['evidence_status'] == b['evidence_status'] == 'PASS'
                  and baseline['condition'] == 'baseline' and with_rule['condition'] == 'with-rule'
                  and baseline['scenario_id'] == with_rule['scenario_id']
                  and baseline['rule']['id'] == with_rule['rule']['id']
                  and baseline['rule']['sha256'] != with_rule['rule']['sha256']
                  and baseline['environment'] == with_rule['environment']
                  and baseline['controls'] == with_rule['controls']
                  and set(baseline['controls']) >= {'fixtures', 'tools'})
    status = 'SKIP'
    if comparable and a['behavioral_status'] != 'SKIP' and b['behavioral_status'] != 'SKIP':
        status = b['behavioral_status']
    return dict(status=status, comparable=comparable, baseline=a, with_rule=b,
                improvement_observed=comparable and a['behavioral_status'] == 'FAIL' and b['behavioral_status'] == 'PASS',
                limits='A pair is an observed trial, not a statistical reliability claim; protected-condition fingerprints are declared by the coordinator.')


def _load(path):
    path = Path(path)
    require(path.stat().st_size <= 1024*1024, 'Trial manifest too large')
    return read_json(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare')
    p.add_argument('scenario'); p.add_argument('--condition', choices=['baseline', 'with-rule'], required=True)
    p.add_argument('--skill-id', required=True); p.add_argument('--rule', required=True); p.add_argument('--root', type=Path, required=True)
    p = sub.add_parser('review'); p.add_argument('trial'); p.add_argument('--root', type=Path, required=True)
    p = sub.add_parser('compare'); p.add_argument('baseline'); p.add_argument('with_rule'); p.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'prepare': result = prepare(args.scenario, args.condition, args.root, args.skill_id, args.rule)
        elif args.command == 'review': result = evaluate(_load(args.trial), args.root)
        else: result = compare(_load(args.baseline), _load(args.with_rule), args.root)
        print(json.dumps(result, indent=2))
        status = result.get('behavioral_status', result.get('status'))
        return 2 if result.get('evidence_status') == 'FAIL' or status == 'FAIL' else 0
    except (Violation, OSError, ValueError, TypeError):
        print(json.dumps(dict(status='FAIL', error='Invalid trial input; no private input is echoed')))
        return 1


if __name__ == '__main__': raise SystemExit(main())
