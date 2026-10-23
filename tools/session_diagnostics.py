"""Bounded read-only session analysis. Raw messages/arguments/results are never emitted."""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime


def _key(value):
    if not isinstance(value, str) or not 0 < len(value) <= 512:
        raise ValueError('Invalid identifier')
    return hashlib.sha256(value.encode()).hexdigest()[:16]


def _json(text):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result: raise ValueError('Duplicate key')
            result[k] = v
        return result
    def constant(_): raise ValueError('Nonfinite value')
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def _normalized(row):
    kind = row.get('type')
    out = dict(type=kind)
    if kind == 'coverage':
        for k in ('skills', 'checks'):
            if type(row.get(k, False)) is not bool: raise ValueError('Invalid coverage')
            out[k] = row.get(k, False)
    elif kind == 'scope':
        targets = row.get('targets')
        if not isinstance(targets, list) or len(targets) > 256: raise ValueError('Invalid scope')
        out['targets'] = {_key(t) for t in targets}
    elif kind == 'handoff':
        if type(row.get('complete')) is not bool: raise ValueError('Invalid handoff')
        out['complete'] = row['complete']
    elif kind in ('skill_selected', 'skill_read'):
        out['skill'] = _key(row.get('skill'))
    elif kind == 'action':
        if type(row.get('mutation', False)) is not bool: raise ValueError('Invalid action')
        out.update(mutation=row.get('mutation', False), target=_key(row.get('target')))
        for k in ('skill', 'requires_gate', 'checkpoint'):
            if k in row: out[k] = _key(row[k])
    elif kind in ('gate', 'checkpoint', 'check'):
        if row.get('status') not in ('PASS', 'FAIL', 'OPEN', 'SKIP'): raise ValueError('Invalid status')
        out.update(status=row['status'], key=_key(row.get('target' if kind == 'check' else 'id')))
    elif kind == 'tool_call':
        out.update(call_id=_key(row.get('call_id')), tool=_key(row.get('name')))
    elif kind == 'tool_result':
        if row.get('ok') is not None and type(row['ok']) is not bool: raise ValueError('Invalid result')
        out.update(call_id=_key(row.get('call_id')), ok=row.get('ok'))
    elif kind == 'usage':
        value = row.get('total_tokens')
        if type(value) is not int or not 0 <= value <= 10**12: raise ValueError('Invalid measurement')
        out['total_tokens'] = value
    else:
        return None
    return out


def _codex(row):
    if row.get('type') in ('item.started', 'item.completed'):
        item = row.get('item')
        if isinstance(item, dict) and item.get('type') == 'command_execution':
            if row['type'] == 'item.started':
                return _normalized(dict(type='tool_call', call_id=item.get('id'), name='command_execution'))
            code = item.get('exit_code')
            return _normalized(dict(type='tool_result', call_id=item.get('id'), ok=code == 0 if type(code) is int else None))
        return None
    if row.get('type') == 'turn.completed':
        usage = row.get('usage')
        if isinstance(usage, dict) and all(type(usage.get(k)) is int for k in ('input_tokens', 'output_tokens')):
            return _normalized(dict(type='usage', total_tokens=usage['input_tokens']+usage['output_tokens']))
        return None
    payload = row.get('payload')
    if not isinstance(payload, dict): return None
    if row.get('type') == 'response_item':
        kind = payload.get('type')
        if kind in ('function_call', 'custom_tool_call'):
            return _normalized(dict(type='tool_call', call_id=payload.get('call_id'), name=payload.get('name')))
        if kind in ('function_call_output', 'custom_tool_call_output'):
            output = payload.get('output')
            if isinstance(output, str):
                try: output = _json(output)
                except (ValueError, RecursionError): output = None
            ok = None
            if isinstance(output, dict):
                if type(output.get('ok')) is bool: ok = output['ok']
                elif type(output.get('exit_code')) is int: ok = output['exit_code'] == 0
                elif output.get('isError') is True: ok = False
                elif output.get('error_code') and output.get('error'): ok = False
            return _normalized(dict(type='tool_result', call_id=payload.get('call_id'), ok=ok))
    if row.get('type') == 'token_usage_record':
        usage = payload.get('usage', {})
    elif row.get('type') == 'event_msg' and payload.get('type') == 'token_count':
        info = payload.get('info') or {}
        usage = info.get('total_token_usage', {}) if isinstance(info, dict) else {}
    else:
        return None  # item_completed duplicates, reasoning, user messages, commands
    if isinstance(usage, dict) and 'total_tokens' in usage:
        return _normalized(dict(type='usage', total_tokens=usage['total_tokens']))
    return None


def analyze(source, root, *, format='codex', max_bytes=16*1024*1024,
            max_line_bytes=256*1024, max_events=20000):
    """PASS means analysis ran; it never establishes general agent compliance."""
    try:
        source, root = Path(source), Path(root).resolve(strict=True)
        if '..' in source.parts: raise ValueError('Escaped input')
        if not source.is_absolute(): source = root/source
        source = source.resolve()
        if not source.is_relative_to(root) or format not in ('codex', 'normalized'):
            raise ValueError('Unsupported source')
        if not source.is_file(): return dict(status='SKIP', reason='no session transcript', compliance='NOT_ESTABLISHED')
        if not (type(max_bytes) is int and 0 < max_bytes <= 64*1024*1024
                and type(max_line_bytes) is int and 0 < max_line_bytes <= 1024*1024
                and type(max_events) is int and 0 < max_events <= 100000):
            raise ValueError('Invalid limits')
    except (OSError, ValueError, TypeError):
        return dict(status='FAIL', reason='Invalid source, allowed root, format or limits', compliance='NOT_ESTABLISHED')

    findings, dropped = [], 0
    selected, read, gates, checkpoints, changed, checked = {}, set(), {}, {}, {}, {}
    calls, results = {}, set()
    coverage = dict(skills=False, checks=False, truncated=False)
    counts = dict(lines=0, events=0, tool_calls=0, ignored=0, invalid=0)
    tokens, span, failure_run = None, [], []
    unread, allowed_targets = [], None
    bytes_read, digest = 0, hashlib.sha256()
    before = source.stat()

    def finding(code, line, related, observed, expected, effect, limit, remedy, severity='P2'):
        nonlocal dropped
        if len(findings) >= 100:
            dropped += 1
            return
        findings.append(dict(finding_id='SD-'+hashlib.sha256((str(source)+code+str(line)).encode()).hexdigest()[:12],
                             code=code, severity=severity, observed=observed, expected=expected,
                             evidence=dict(path=str(source), line=line, related_lines=related),
                             effect=effect, limits=limit, remediation=remedy))

    def consume(event, line):
        nonlocal tokens, failure_run, allowed_targets
        kind = event['type']
        if kind == 'coverage':
            coverage.update(skills=event['skills'], checks=event['checks'])
        elif kind == 'scope': allowed_targets = event['targets']
        elif kind == 'handoff' and not event['complete']:
            finding('INCOMPLETE_HANDOFF', line, [], 'Logger explicitly marks handoff incomplete',
                    'Supply the required scoped handoff evidence', 'Incomplete handoff is reported',
                    'No missing task or requirement is inferred', 'Review source handoff and name the remaining owner')
        elif kind == 'skill_selected': selected[event['skill']] = line
        elif kind == 'skill_read': read.add(event['skill'])
        elif kind in ('gate', 'checkpoint'):
            (gates if kind == 'gate' else checkpoints)[event['key']] = (event['status'], line)
        elif kind == 'action':
            skill = event.get('skill')
            if coverage['skills'] and skill in selected and skill not in read:
                unread.append((line, selected[skill]))
            if event['mutation'] and allowed_targets is not None and event['target'] not in allowed_targets:
                finding('OUTSIDE_DECLARED_SCOPE', line, [], 'Mutation targets an object outside the declared target set',
                        'Preserve scope or explicitly revise it before mutation', 'Declared target boundary crossed',
                        'Uses only explicit normalized scope; no semantic scope inference', 'Inspect the action and restore only authorized own changes', 'P1')
            gate = gates.get(event.get('requires_gate'))
            if gate and gate[0] != 'PASS':
                finding('FAILED_GATE_ACTION', line, [gate[1]], 'Action declares dependency on a non-passing gate',
                        'Resolve the dependent gate first', 'Recorded action followed unresolved gate',
                        'Only explicitly declared dependency is assessed', 'Stop dependent work and inspect the gate evidence', 'P1')
            checkpoint = checkpoints.get(event.get('checkpoint'))
            if checkpoint and checkpoint[0] == 'PASS':
                finding('REPEATED_CHECKPOINT', line, [checkpoint[1]], 'Action repeats a completed checkpoint',
                        'Reuse current accepted evidence unless invalidated', 'Repeated action is observed',
                        'May be intentional; no cost or regression is inferred', 'Review freshness and reason for repeat')
            if event['mutation']: changed[event['target']] = line
        elif kind == 'check': checked[event['key']] = line
        elif kind == 'tool_call':
            if event['call_id'] not in calls:
                calls[event['call_id']] = (event['tool'], line)
                counts['tool_calls'] += 1
        elif kind == 'tool_result' and event['call_id'] in calls and event['call_id'] not in results:
            results.add(event['call_id'])
            tool, call_line = calls[event['call_id']]
            if event['ok'] is False:
                if failure_run and failure_run[-1][0] != tool: failure_run = []
                failure_run.append((tool, line))
                if len(failure_run) == 3:
                    finding('REPEATED_TOOL_FAILURE', line, [n for _, n in failure_run[:-1]],
                            'Three consecutive results report failure for the same tool',
                            'Inspect the failure before another attempt', 'Three reported failures observed',
                            'Root cause, identical arguments and wasted work are not inferred', 'Inspect cited results in the original source')
            else: failure_run = []
        elif kind == 'usage': tokens = max(tokens or 0, event['total_tokens'])

    try:
        with source.open('rb') as stream:
            while bytes_read < max_bytes and counts['events'] < max_events:
                chunk = stream.readline(min(max_line_bytes+1, max_bytes-bytes_read))
                if not chunk: break
                counts['lines'] += 1
                line = counts['lines']; bytes_read += len(chunk); digest.update(chunk)
                oversized = len(chunk) > max_line_bytes
                ended = chunk.endswith(b'\n')
                # Drain without retaining a huge line; keep its one physical number.
                while not ended and stream.tell() < before.st_size and bytes_read < max_bytes:
                    oversized = True
                    tail = stream.readline(min(max_line_bytes+1, max_bytes-bytes_read))
                    if not tail: break
                    bytes_read += len(tail); digest.update(tail); ended = tail.endswith(b'\n')
                if oversized:
                    counts['invalid'] += 1
                    finding('LINE_LIMIT', line, [], 'Oversized physical line omitted', 'Bounded parseable input',
                            'Record not analyzed', 'No contents are echoed', 'Provide a bounded prepared transcript')
                    continue
                try:
                    row = _json(chunk.decode('utf-8-sig'))
                    if not isinstance(row, dict): raise ValueError('Expected object')
                    timestamp = row.get('timestamp')
                    if isinstance(timestamp, str):
                        try: span.append(datetime.fromisoformat(timestamp.replace('Z', '+00:00')))
                        except ValueError: pass
                    event = _normalized(row) if format == 'normalized' else _codex(row)
                    if event:
                        counts['events'] += 1; consume(event, line)
                    else: counts['ignored'] += 1
                except (ValueError, UnicodeError, TypeError, RecursionError, KeyError, AttributeError):
                    counts['invalid'] += 1
                    finding('INVALID_RECORD', line, [], 'Malformed record omitted', 'A valid supported JSONL record',
                            'Record not analyzed', 'No input or parser exception is echoed', 'Prepare a valid bounded record')
            coverage['truncated'] = stream.tell() < source.stat().st_size
    except OSError:
        return dict(status='FAIL', reason='Cannot read selected transcript', compliance='NOT_ESTABLISHED')
    after = source.stat()
    stable = (before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns)
    if not stable: coverage['truncated'] = True
    if coverage['skills'] and not coverage['truncated'] and not counts['invalid']:
        for line, selection in unread:
            finding('UNREAD_SKILL', line, [selection], 'Selected skill has no prior read event',
                    'Read the selected full Skill before its action', 'Action follows selection without recorded reading',
                    'Requires explicit complete skill coverage; not pixel or behavior quality proof',
                    'Acquire full current Skill and review the trace', 'P1')
    if coverage['checks'] and not coverage['truncated'] and not counts['invalid']:
        for target, line in changed.items():
            if checked.get(target, 0) < line:
                finding('UNCHECKED_CHANGE', line, [], 'Mutation lacks a subsequent recorded check',
                        'Verify changed scope after its latest mutation', 'No later matching check in complete declared coverage',
                        'Only the normalized logger\'s declared scope is assessed', 'Verify the current affected artifact', 'P1')
    elapsed = None
    if len(span) >= 2:
        try: elapsed = max(0, (max(span)-min(span)).total_seconds())
        except TypeError: pass
    return dict(status='WARN' if findings or coverage['truncated'] else 'PASS', compliance='NOT_ESTABLISHED',
                source=dict(path=str(source), bytes_read=bytes_read, sha256=digest.hexdigest() if not coverage['truncated'] else None,
                            prefix_sha256=digest.hexdigest(), stable_during_read=stable),
                format=format, coverage=coverage, summary=counts, findings=findings, findings_omitted=dropped,
                usage=dict(max_observed_total_tokens=tokens, aggregation='maximum observed record total; counters can be cumulative or per-turn; never sum duplicate envelopes',
                           observed_span_seconds=elapsed, monetary_cost=None),
                limits='Analysis of observable records only. Raw payloads are omitted; wrappers and encrypted reasoning are opaque. No absence proof without explicit complete coverage. No fixes or uploads performed.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path); p.add_argument('--root', type=Path, required=True)
    p.add_argument('--format', choices=['codex', 'normalized'], default='codex')
    p.add_argument('--max-bytes', type=int, default=16*1024*1024)
    p.add_argument('--max-line-bytes', type=int, default=256*1024)
    p.add_argument('--max-events', type=int, default=20000)
    args = p.parse_args()
    try:
        result = analyze(args.source, args.root, format=args.format, max_bytes=args.max_bytes,
                         max_line_bytes=args.max_line_bytes, max_events=args.max_events)
        print(json.dumps(result, indent=2))
        return 2 if result['status'] == 'FAIL' else 0
    except (OSError, ValueError, TypeError, RecursionError):
        print(json.dumps(dict(status='FAIL', reason='Input unavailable or invalid; private data omitted')))
        return 1


if __name__ == '__main__': raise SystemExit(main())
