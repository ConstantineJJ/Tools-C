"""CLI orchestration for project review; importable engine stays independent."""
import argparse
import json
from pathlib import Path
from validation_core import Violation
from project_review import review


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
    parser.add_argument('--require-acceptance', action='store_true',
                        help='converge only: exit 2 unless declared acceptance is PASS; not runtime/visual certification')
    changes = parser.add_mutually_exclusive_group()
    changes.add_argument('--changed-source')
    changes.add_argument('--changed-rule')
    args = parser.parse_args()
    if args.require_acceptance and args.operation != 'converge':
        parser.error('--require-acceptance requires converge')
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
    if args.require_acceptance and result.get('acceptance_status') != 'PASS':
        return 2
    return 0


