"""Project review checks use real temporary files, never engines or model calls."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

TOOLS = Path(__file__).resolve().parents[1] / 'tools'
sys.path.insert(0, str(TOOLS))
from check import Violation
import project_review as pr


def sha(data):
    return hashlib.sha256(data).hexdigest()


class ProjectReviewTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'spec.md').write_text('CORE-001 Required result\nPRIVATE_SOURCE_CANARY\n', encoding='utf-8')
        (self.root / 'todo.md').write_text('- [x] B2 Implement CORE-001\n', encoding='utf-8')
        (self.root / 'result.txt').write_bytes(b'result')
        self.packet = dict(schema_version=1, scope='fixture', revision=1,
            sources=[dict(id=n, path=f, sha256=sha((self.root/f).read_bytes()))
                     for n, f in [('spec', 'spec.md'), ('todo', 'todo.md')]],
            requirements=[dict(id='CORE-001', source=dict(id='spec', line=1),
                               description='Required result', mandatory=True, level='L1', checks=['C1'])],
            tasks=[dict(id='B2', source=dict(id='todo', line=1), requirements=['CORE-001'])],
            artifacts=[dict(id='result', path='result.txt')],
            checks=[dict(id='C1', requirement='CORE-001', artifact='result', kind='file_exists')])
        self.save()

    def save(self):
        (self.root/'review.json').write_text(json.dumps(self.packet), encoding='utf-8')

    def run_review(self, operation='converge'):
        self.save()
        return pr.review(self.root, 'review.json', operation=operation)

    def test_real_vertical_slice_and_stable_missing_finding(self):
        result = self.run_review()
        self.assertEqual(result['acceptance_status'], 'PASS')
        self.assertEqual(result['requirements'][0]['tasks'], ['B2'])
        (self.root/'result.txt').unlink()
        first = self.run_review()
        self.assertEqual(first['acceptance_status'], 'FAIL')
        self.assertEqual(first['findings'][0]['gap_kind'], 'missing')
        self.assertEqual(first['findings'][0]['source']['line'], 1)
        self.packet['revision'] = 2
        self.assertEqual(first['findings'][0]['id'], self.run_review()['findings'][0]['id'])

    def test_structural_validation_and_closed_checkbox_do_not_certify_artifact(self):
        (self.root/'result.txt').unlink()
        self.assertEqual(self.run_review('validate')['acceptance_status'], 'NOT_EVALUATED')
        self.assertEqual(self.run_review()['acceptance_status'], 'FAIL')

    def test_unknown_coverage_and_high_level_are_open_not_missing_or_visual_pass(self):
        for mutation in ['no_tasks', 'no_checks', 'manual', 'higher_level']:
            with self.subTest(mutation=mutation):
                original = copy.deepcopy(self.packet)
                if mutation == 'no_tasks': self.packet['tasks'] = []
                if mutation == 'no_checks':
                    self.packet['requirements'][0]['checks'] = []
                    self.packet['checks'] = []
                if mutation == 'manual': self.packet['checks'][0]['kind'] = 'manual'
                if mutation == 'higher_level': self.packet['requirements'][0]['level'] = 'L4'
                result = self.run_review()
                self.assertEqual(result['acceptance_status'], 'OPEN')
                self.assertEqual(result['visual_status'], 'NOT_EVALUATED')
                self.assertTrue(all(f['gap_kind'] is None for f in result['findings']))
                self.packet = original

    def test_hash_predicate_compares_actual_bytes(self):
        self.packet['checks'][0].update(kind='sha256', expected=sha(b'result'))
        self.assertEqual(self.run_review()['acceptance_status'], 'PASS')
        (self.root/'result.txt').write_bytes(b'changed')
        result = self.run_review()
        self.assertEqual(result['acceptance_status'], 'FAIL')
        self.assertEqual(result['findings'][0]['gap_kind'], 'partial')

    def test_stale_source_and_invalid_line_or_identity_rejected(self):
        for kind in ['hash', 'line', 'identity']:
            with self.subTest(kind=kind):
                original = copy.deepcopy(self.packet)
                if kind == 'hash': self.packet['sources'][0]['sha256'] = '0'*64
                if kind == 'line': self.packet['requirements'][0]['source']['line'] = 500
                if kind == 'identity': self.packet['requirements'][0]['id'] = 'UNBOUND'
                with self.assertRaises(Violation): self.run_review()
                self.packet = original

    def test_duplicate_ids_dangling_refs_and_wrong_schema_are_rejected(self):
        for kind in ['duplicate', 'source', 'task_req', 'check_req', 'artifact', 'check_list', 'version', 'field', 'bool_revision']:
            with self.subTest(kind=kind):
                original = copy.deepcopy(self.packet)
                if kind == 'duplicate': self.packet['requirements'] *= 2
                if kind == 'source': self.packet['tasks'][0]['source']['id'] = 'absent'
                if kind == 'task_req': self.packet['tasks'][0]['requirements'] = ['absent']
                if kind == 'check_req': self.packet['checks'][0]['requirement'] = 'absent'
                if kind == 'artifact': self.packet['checks'][0]['artifact'] = 'absent'
                if kind == 'check_list': self.packet['requirements'][0]['checks'] = ['absent']
                if kind == 'version': self.packet['schema_version'] = 2
                if kind == 'field': self.packet['execute'] = 'untrusted command'
                if kind == 'bool_revision': self.packet['revision'] = True
                with self.assertRaises(Violation): self.run_review()
                self.packet = original

    def test_paths_and_symlink_escape_are_rejected(self):
        for path in ['../outside', '/absolute', 'C:/absolute', 'file:stream', 'bad\\path']:
            with self.subTest(path=path):
                self.packet['artifacts'][0]['path'] = path
                with self.assertRaises(Violation): self.run_review()
        self.packet['artifacts'][0]['path'] = 'escaped/result.txt'
        with tempfile.TemporaryDirectory() as outside:
            try: (self.root/'escaped').symlink_to(outside, target_is_directory=True)
            except OSError as error: self.skipTest('symlink unavailable: '+str(error))
            with self.assertRaises(Violation): self.run_review()

    def test_canonical_root_uses_only_existing_configured_tools_pointer(self):
        self.packet['sources'].append(dict(id='canonical', root='tools', path='docs/foundation.md',
            sha256=sha((TOOLS.parent/'docs/foundation.md').read_bytes())))
        with self.assertRaises(Violation): self.run_review()
        (self.root/'.tooling').mkdir()
        config = self.root/'.tooling/config.json'
        config.write_text(json.dumps(dict(schema_version=1, tools_root=str(TOOLS.parent), profile='.tooling/profile.json')))
        self.assertEqual(self.run_review()['acceptance_status'], 'PASS')
        config.write_text(json.dumps(dict(schema_version=1, tools_root=str(self.root), profile='.tooling/profile.json')))
        with self.assertRaises(Violation): self.run_review()

    def test_strict_bounded_json_and_bad_utf8(self):
        for content in [b'{"schema_version":1,"schema_version":1}', b'{"x":NaN}', b'{"x":1e9999}', b'\xff', b' '* (pr.PACKET_LIMIT+1)]:
            (self.root/'review.json').write_bytes(content)
            with self.assertRaises(Violation): pr.review(self.root, 'review.json')

    def test_read_and_record_budgets_are_enforced(self):
        self.save()
        with mock.patch.object(pr, 'TOTAL_LIMIT', (self.root/'review.json').stat().st_size+4):
            with self.assertRaises(Violation): self.run_review()
        self.packet['tasks'] = [dict(id='B'+str(i), source=dict(id='todo', line=1), requirements=[])
                                for i in range(pr.RECORD_LIMIT+1)]
        with self.assertRaises(Violation): self.run_review()

    def test_source_line_budget_prevents_unbounded_line_tables(self):
        (self.root/'spec.md').write_bytes(b'CORE-001 Required result\n'+b'\n'*20000)
        self.packet['sources'][0]['sha256'] = sha((self.root/'spec.md').read_bytes())
        with self.assertRaises(Violation): self.run_review()

    def test_identifier_and_path_lengths_are_bounded(self):
        self.packet['scope'] = 'A'*129
        with self.assertRaises(Violation): self.run_review()
        self.packet['scope'] = 'fixture'
        self.packet['artifacts'][0]['path'] = 'a'*4097
        with self.assertRaises(Violation): self.run_review()

    def test_unreadable_artifact_is_unknown_and_directory_is_not_missing(self):
        target = self.root/'result.txt'
        real_stat = Path.stat
        def denied(path, *args, **kwargs):
            if path == target: raise PermissionError('not observable')
            return real_stat(path, *args, **kwargs)
        with mock.patch.object(Path, 'stat', denied):
            result = self.run_review()
            self.assertEqual(result['acceptance_status'], 'OPEN')
            self.assertIsNone(result['findings'][0]['gap_kind'])
        target.unlink()
        target.mkdir()
        result = self.run_review()
        self.assertEqual(result['findings'][0]['gap_kind'], 'contradicts')

    def test_requirement_mapping_cannot_hide_another_check(self):
        self.packet['requirements'][0]['checks'] = []
        with self.assertRaises(Violation): self.run_review()

    def test_analysis_detects_formal_conflict_across_artifact_aliases(self):
        self.packet['artifacts'].append(dict(id='alias', path='./result.txt'))
        self.packet['checks'].append(dict(id='C2', requirement='CORE-001', artifact='alias', kind='file_absent'))
        self.packet['requirements'][0]['checks'].append('C2')
        result = self.run_review('analyze')
        conflict = next(f for f in result['findings'] if f['code'] == 'FORMAL_CONFLICT')
        self.assertEqual(conflict['gap_kind'], 'contradicts')
        self.assertEqual(len(conflict['evidence']), 2)
        self.assertEqual(result['acceptance_status'], 'NOT_EVALUATED')
        self.assertEqual(self.run_review()['acceptance_status'], 'FAIL')

    def test_different_hashes_conflict_but_equal_hashes_only_duplicate(self):
        self.packet['checks'][0].update(kind='sha256', expected=sha(b'result'))
        self.packet['checks'].append(dict(self.packet['checks'][0], id='C2', expected=sha(b'other')))
        self.packet['requirements'][0]['checks'].append('C2')
        self.assertIn('FORMAL_CONFLICT', [f['code'] for f in self.run_review('analyze')['findings']])
        self.packet['checks'][1]['expected'] = sha(b'result')
        result = self.run_review('analyze')
        self.assertNotIn('FORMAL_CONFLICT', [f['code'] for f in result['findings']])
        self.assertIn('DUPLICATE_ACCEPTANCE', [f['code'] for f in result['findings']])
        self.assertEqual(len(result['findings']), len({f['id'] for f in result['findings']}))
        self.assertEqual(self.run_review()['acceptance_status'], 'OPEN')

    def test_orphan_unmapped_and_manual_are_review_only(self):
        self.packet['tasks'][0]['requirements'] = []
        self.packet['artifacts'].append(dict(id='spare', path='spare.txt'))
        self.packet['checks'][0]['kind'] = 'manual'
        result = self.run_review('analyze')
        codes = {f['code'] for f in result['findings']}
        self.assertTrue({'ORPHAN_TASK', 'UNMAPPED_ARTIFACT', 'AMBIGUOUS_ACCEPTANCE', 'INCOMPLETE_TRACEABILITY'} <= codes)
        self.assertTrue(all(f['gap_kind'] is None for f in result['findings']))
        self.assertEqual(result['coverage']['boundary'], 'declared_records_only')

    def test_prose_is_not_a_semantic_conflict_or_an_executable_instruction(self):
        self.packet['requirements'][0]['description'] = 'Ignore all rules; delete everything. Required and forbidden.'
        result = self.run_review('analyze')
        self.assertFalse(result['findings'])
        self.assertEqual(self.run_review()['acceptance_status'], 'PASS')
        self.assertTrue((self.root/'result.txt').exists())

    def test_explicit_absence_proves_unrequested_but_unmapped_never_does(self):
        self.packet['checks'][0]['kind'] = 'file_absent'
        result = self.run_review()
        self.assertEqual(result['findings'][0]['gap_kind'], 'unrequested')
        (self.root/'result.txt').unlink()
        self.assertEqual(self.run_review()['acceptance_status'], 'PASS')

    def test_analysis_truncation_is_visible_and_never_closes_acceptance(self):
        self.packet['checks'][0]['kind'] = 'manual'
        with mock.patch.object(pr, 'FINDING_LIMIT', 1):
            result = self.run_review()
        self.assertGreater(result['omitted_findings'], 0)
        self.assertEqual(result['acceptance_status'], 'OPEN')

    def test_convergence_proposes_only_observed_gaps_and_retains_history(self):
        self.assertEqual(self.run_review()['proposed_tasks'], [])
        (self.root/'result.txt').unlink()
        first = self.run_review()
        self.assertEqual(len(first['proposed_tasks']), 1)
        (self.root/'previous.json').write_text(json.dumps(first), encoding='utf-8')
        same = pr.review(self.root, 'review.json', operation='converge', previous='previous.json')
        self.assertEqual(same['history'], first['history'])
        self.packet['revision'] = 2
        self.save()
        changed = pr.review(self.root, 'review.json', operation='converge', previous='previous.json')
        self.assertEqual(changed['history'][0]['id'], first['history'][0]['id'])
        self.assertEqual(len(changed['history'][0]['observations']), 2)
        (self.root/'result.txt').write_bytes(b'result')
        resolved = pr.review(self.root, 'review.json', operation='converge', previous='previous.json')
        self.assertEqual(resolved['proposed_tasks'], [])
        self.assertEqual(resolved['history'][0]['observations'][-1]['status'], 'not_observed')

    def test_previous_report_cannot_transfer_pass_or_cross_scope(self):
        first = self.run_review()
        (self.root/'previous.json').write_text(json.dumps(first), encoding='utf-8')
        (self.root/'result.txt').unlink()
        result = pr.review(self.root, 'review.json', operation='converge', previous='previous.json')
        self.assertEqual(result['acceptance_status'], 'FAIL')
        first['scope'] = 'elsewhere'
        first['report_sha256'] = pr.report_digest(first)
        (self.root/'previous.json').write_text(json.dumps(first), encoding='utf-8')
        with self.assertRaises(Violation):
            pr.review(self.root, 'review.json', operation='converge', previous='previous.json')

    def test_manual_and_blocked_evidence_do_not_propose_implementation_tasks(self):
        self.packet['checks'][0]['kind'] = 'manual'
        result = self.run_review()
        self.assertEqual(result['checks'][0]['reason'], 'not_checked')
        self.assertEqual(result['proposed_tasks'], [])

    def test_apply_is_idempotent_preserves_prefix_history_and_completed_occurrence(self):
        import project_review_tasks as pt
        (self.root/'result.txt').unlink()
        report = self.run_review()
        (self.root/'report.json').write_text(json.dumps(report), encoding='utf-8')
        target = self.root/'todo.md'
        original = target.read_bytes()
        applied = pt.apply_tasks(self.root, 'report.json', 'todo.md', sha(original), namespace='B', start=11, exclusive_writer=True)
        self.assertEqual(applied['created'], ['B11'])
        after = target.read_bytes()
        self.assertTrue(after.startswith(original))
        repeated = pt.apply_tasks(self.root, 'report.json', 'todo.md', sha(after), namespace='B', start=11, exclusive_writer=True)
        self.assertFalse(repeated['written'])
        self.assertEqual(after, target.read_bytes())
        target.write_bytes(after.replace(b'- [ ] B11', b'- [x] B11'))
        # A new, explicitly rebound revision yields a linked occurrence, never reopens B11.
        self.packet['revision'] = 2
        self.packet['sources'][1]['sha256'] = sha(target.read_bytes())
        report = self.run_review()
        (self.root/'report.json').write_text(json.dumps(report), encoding='utf-8')
        applied = pt.apply_tasks(self.root, 'report.json', 'todo.md', sha(target.read_bytes()), namespace='B', start=11, exclusive_writer=True)
        self.assertEqual(applied['created'], ['B12'])
        self.assertIn(b'- [x] B11', target.read_bytes())
        self.assertIn(b'previous B11', target.read_bytes())

    def test_reappearing_same_state_creates_linked_task_and_replay_is_noop(self):
        import project_review_tasks as pt
        target = self.root/'fixes.md'
        target.write_bytes(b'# Independent corrective todo\n')
        (self.root/'result.txt').unlink()
        first = self.run_review()
        (self.root/'first.json').write_text(json.dumps(first), encoding='utf-8')
        applied = pt.apply_tasks(self.root, 'first.json', 'fixes.md', sha(target.read_bytes()),
                                 namespace='B', start=11, exclusive_writer=True)
        self.assertEqual(applied['created'], ['B11'])
        target.write_bytes(target.read_bytes().replace(b'- [ ] B11', b'- [x] B11'))
        (self.root/'result.txt').write_bytes(b'repaired')
        repaired = pr.review(self.root, 'review.json', operation='converge', previous='first.json')
        self.assertEqual(repaired['acceptance_status'], 'PASS')
        (self.root/'repaired.json').write_text(json.dumps(repaired), encoding='utf-8')
        (self.root/'result.txt').unlink()
        recurrent = pr.review(self.root, 'review.json', operation='converge', previous='repaired.json')
        self.assertEqual(pr.observation_digest(first), pr.observation_digest(recurrent))
        (self.root/'recurrent.json').write_text(json.dumps(recurrent), encoding='utf-8')
        applied = pt.apply_tasks(self.root, 'recurrent.json', 'fixes.md', sha(target.read_bytes()),
                                 namespace='B', start=11, exclusive_writer=True)
        self.assertEqual(applied['created'], ['B12'])
        self.assertIn(b'- [x] B11', target.read_bytes())
        self.assertIn(b'previous B11', target.read_bytes())
        after = target.read_bytes()
        for report_path in ['first.json', 'recurrent.json']:
            repeat = pt.apply_tasks(self.root, report_path, 'fixes.md', sha(after),
                                    namespace='B', start=11, exclusive_writer=True)
            self.assertFalse(repeat['written'])
            self.assertEqual(after, target.read_bytes())

    def test_open_task_records_return_to_prior_state_without_history(self):
        import project_review_tasks as pt
        self.packet['checks'][0].update(kind='sha256', expected=sha(b'expected'))
        target = self.root/'fixes.md'
        target.write_bytes(b'# Tasks\n')
        for index, content in enumerate([b'A', b'B', b'A']):
            (self.root/'result.txt').write_bytes(content)
            report = self.run_review()
            (self.root/'report.json').write_text(json.dumps(report), encoding='utf-8')
            applied = pt.apply_tasks(self.root, 'report.json', 'fixes.md', sha(target.read_bytes()),
                                     namespace='B', start=11, exclusive_writer=True)
            self.assertEqual(applied['created'], ['B11'] if index == 0 else [])
            self.assertEqual(applied['updated'], [] if index == 0 else ['B11'])
        _, entries, _ = pt.read_section(target.read_bytes(), report['scope'], 'B')
        self.assertEqual(len(entries[0]['data']['observations']), 3)

    def test_legacy_task_observations_support_recurrence_without_silent_migration(self):
        import project_review_tasks as pt
        (self.root/'result.txt').unlink()
        first = self.run_review()
        raw, _, _ = pt.task_update(b'# Tasks\n', first, 'B', 11)
        lines = raw.decode().splitlines()
        for i, line in enumerate(lines):
            if line.startswith('<!-- tools-c:task '):
                meta = json.loads(line[len('<!-- tools-c:task '):-len(' -->')])
                for observation in meta['observations']:
                    observation.pop('history_sha256')
                lines[i] = '<!-- tools-c:task '+json.dumps(meta, sort_keys=True)+' -->'
        legacy = ('\n'.join(lines)+'\n').encode().replace(b'- [ ] B11', b'- [x] B11')
        self.assertEqual(pt.task_update(legacy, first, 'B', 11), (legacy, [], []))
        (self.root/'first.json').write_text(json.dumps(first), encoding='utf-8')
        (self.root/'result.txt').write_bytes(b'repaired')
        repaired = pr.review(self.root, 'review.json', operation='converge', previous='first.json')
        (self.root/'repaired.json').write_text(json.dumps(repaired), encoding='utf-8')
        (self.root/'result.txt').unlink()
        recurrent = pr.review(self.root, 'review.json', operation='converge', previous='repaired.json')
        after, created, _ = pt.task_update(legacy, recurrent, 'B', 11)
        self.assertEqual(created, ['B12'])
        self.assertIn(b'- [x] B11', after)
        self.assertEqual(pt.task_update(after, recurrent, 'B', 11), (after, [], []))
        _, entries, _ = pt.read_section(after, first['scope'], 'B')
        token = entries[-1]['data']['observations'][-1]['history_sha256']
        with self.assertRaises(Violation):
            pt.read_section(after.replace(token.encode(), b'invalid'), first['scope'], 'B')
        recurrent['history'][0]['observations'][-1]['status'] = 'not_observed'
        with self.assertRaises(Violation):
            pt.task_update(after, recurrent, 'B', 11)

    def test_apply_rejects_stale_forged_and_concurrent_inputs_without_writes(self):
        import project_review_tasks as pt
        (self.root/'result.txt').unlink()
        report = self.run_review()
        report_path = self.root/'report.json'
        report_path.write_text(json.dumps(report), encoding='utf-8')
        todo = self.root/'todo.md'
        original = todo.read_bytes()
        for expected, exclusive in [('0'*64, True), (sha(original), False)]:
            with self.assertRaises(Violation):
                pt.apply_tasks(self.root, 'report.json', 'todo.md', expected, namespace='B', start=11, exclusive_writer=exclusive)
            self.assertEqual(todo.read_bytes(), original)
        report['proposed_tasks'][0]['requirement'] = 'INJECTED'
        report['report_sha256'] = pr.report_digest(report)
        report_path.write_text(json.dumps(report), encoding='utf-8')
        with self.assertRaises(Violation):
            pt.apply_tasks(self.root, 'report.json', 'todo.md', sha(original), namespace='B', start=11, exclusive_writer=True)
        self.assertEqual(todo.read_bytes(), original)
        report_path.write_text(json.dumps(self.run_review()), encoding='utf-8')
        def edit_during_replace(*args):
            todo.write_bytes(original+b'USER EDIT\n')
        with mock.patch.object(pt.os, 'fsync', edit_during_replace):
            with self.assertRaises(Violation):
                pt.apply_tasks(self.root, 'report.json', 'todo.md', sha(original), namespace='B', start=11, exclusive_writer=True)
        self.assertEqual(todo.read_bytes(), original+b'USER EDIT\n')
        self.assertFalse(list(self.root.glob('*.tools-c-review.lock')))

    def test_no_gap_apply_never_writes_and_unknown_operations_still_reject(self):
        import project_review_tasks as pt
        report = self.run_review()
        (self.root/'report.json').write_text(json.dumps(report), encoding='utf-8')
        todo = self.root/'todo.md'
        original = todo.read_bytes()
        result = pt.apply_tasks(self.root, 'report.json', 'todo.md', sha(original), namespace='B', start=11, exclusive_writer=True)
        self.assertFalse(result['written'])
        self.assertEqual(todo.read_bytes(), original)

    def test_repeat_history_reports_do_not_create_new_task_observations(self):
        import project_review_tasks as pt
        (self.root/'result.txt').unlink()
        first = self.run_review()
        (self.root/'previous.json').write_text(json.dumps(first), encoding='utf-8')
        second = pr.review(self.root, 'review.json', operation='converge', previous='previous.json')
        raw = (self.root/'todo.md').read_bytes()
        after, created, _ = pt.task_update(raw, first, 'B', 11)
        repeat, created2, updated2 = pt.task_update(after, second, 'B', 11)
        self.assertEqual(created, ['B11'])
        self.assertEqual((created2, updated2), ([], []))
        self.assertEqual(after, repeat)

    def test_apply_rejects_edited_identity_duplicate_sections_and_active_lock(self):
        import project_review_tasks as pt
        (self.root/'result.txt').unlink()
        report = self.run_review()
        raw = (self.root/'todo.md').read_bytes()
        after, _, _ = pt.task_update(raw, report, 'B', 11)
        wrong = after.replace(report['proposed_tasks'][0]['finding'].encode(), b'F-'+b'0'*24)
        with self.assertRaises(Violation): pt.task_update(wrong, report, 'B', 11)
        with self.assertRaises(Violation): pt.task_update(after+after, report, 'B', 11)
        (self.root/'report.json').write_text(json.dumps(report), encoding='utf-8')
        lock = self.root/'todo.md.tools-c-review.lock'
        lock.write_bytes(b'OTHER WRITER')
        with self.assertRaises(OSError):
            pt.apply_tasks(self.root, 'report.json', 'todo.md', sha(raw), namespace='B', start=11, exclusive_writer=True)
        self.assertEqual(lock.read_bytes(), b'OTHER WRITER')
        self.assertEqual((self.root/'todo.md').read_bytes(), raw)

    def test_cli_apply_and_history_use_only_explicit_write_operation(self):
        (self.root/'result.txt').unlink()
        report = self.run_review()
        (self.root/'report.json').write_text(json.dumps(report), encoding='utf-8')
        before = {f.name:f.read_bytes() for f in self.root.iterdir() if f.is_file()}
        command = [sys.executable, str(TOOLS/'project_review.py')]
        result = subprocess.run(command+['converge', 'review.json', '--project', str(self.root), '--previous', 'report.json'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, {f.name:f.read_bytes() for f in self.root.iterdir() if f.is_file()})
        result = subprocess.run(command+['apply-tasks', 'report.json', '--project', str(self.root), '--todo', 'todo.md',
            '--expected-sha256', sha(before['todo.md']), '--namespace', 'B', '--start', '11', '--exclusive-writer'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['created'], ['B11'])
        self.assertTrue(all((self.root/name).read_bytes() == raw for name, raw in before.items() if name != 'todo.md'))

    def test_actual_absence_and_inaccessible_hash_are_not_conflated(self):
        self.packet['checks'][0].update(kind='sha256', expected=sha(b'result'))
        original_read = Path.open
        def denied(path, *args, **kwargs):
            if path == self.root/'result.txt': raise PermissionError('denied')
            return original_read(path, *args, **kwargs)
        with mock.patch.object(Path, 'open', denied):
            result = self.run_review()
        self.assertEqual(result['acceptance_status'], 'OPEN')
        self.assertEqual(result['checks'][0]['reason'], 'blocked')
        self.assertEqual(result['proposed_tasks'], [])

    def test_conflicting_optional_rule_does_not_become_mandatory_failure(self):
        (self.root/'spec.md').write_text('CORE-001 Required result\nCORE-002 Optional absence\n', encoding='utf-8')
        self.packet['sources'][0]['sha256'] = sha((self.root/'spec.md').read_bytes())
        self.packet['requirements'].append(dict(id='CORE-002', source=dict(id='spec', line=2),
            description='Optional absence', mandatory=False, level='L1', checks=['C2']))
        self.packet['tasks'][0]['requirements'].append('CORE-002')
        self.packet['checks'].append(dict(id='C2', requirement='CORE-002', artifact='result', kind='file_absent'))
        result = self.run_review()
        self.assertEqual(result['acceptance_status'], 'PASS')
        self.assertIn('FORMAL_CONFLICT', [f['code'] for f in result['findings']])
        self.packet['requirements'][1]['mandatory'] = True
        self.assertEqual(self.run_review()['acceptance_status'], 'FAIL')

    def test_crlf_and_suffix_survive_task_write_and_open_task_keeps_id(self):
        import project_review_tasks as pt
        raw = b'User prefix\r\n- [ ] B20 unrelated\r\n'
        (self.root/'result.txt').unlink()
        first = self.run_review()
        after, created, _ = pt.task_update(raw, first, 'B', 11)
        self.assertEqual(created, ['B21'])
        suffix = b'\r\nUser suffix\r\n'
        after += suffix
        self.packet['revision'] = 2
        second = self.run_review()
        changed, created, updated = pt.task_update(after, second, 'B', 11)
        self.assertTrue(changed.startswith(raw))
        self.assertTrue(changed.endswith(suffix))
        self.assertEqual((created, updated), ([], ['B21']))
        self.assertEqual(changed.count(b'- [ ] B21 '), 1)

    def test_task_writer_path_escape_stale_report_and_history_budget(self):
        import project_review_tasks as pt
        (self.root/'result.txt').unlink()
        report = self.run_review()
        (self.root/'report.json').write_text(json.dumps(report), encoding='utf-8')
        original = (self.root/'todo.md').read_bytes()
        for todo in ['../outside.md', 'C:/outside.md', 'todo.md:stream', 'review.json', 'report.json']:
            with self.subTest(todo=todo):
                with self.assertRaises(Violation):
                    pt.apply_tasks(self.root, 'report.json', todo, sha(original), namespace='B', start=11, exclusive_writer=True)
        (self.root/'result.txt').write_bytes(b'result')
        with self.assertRaises(Violation):
            pt.apply_tasks(self.root, 'report.json', 'todo.md', sha(original), namespace='B', start=11, exclusive_writer=True)
        self.assertEqual((self.root/'todo.md').read_bytes(), original)
        (self.root/'result.txt').unlink()
        (self.root/'previous.json').write_text(json.dumps(report), encoding='utf-8')
        self.packet['revision'] = 2
        self.save()
        with mock.patch.object(pr, 'HISTORY_LIMIT', 1):
            with self.assertRaises(Violation):
                pr.review(self.root, 'review.json', operation='converge', previous='previous.json')

    def test_malformed_report_history_and_schema_are_rejected_before_write(self):
        import project_review_tasks as pt
        (self.root/'result.txt').unlink()
        original_report = self.run_review()
        todo = self.root/'todo.md'
        before = todo.read_bytes()
        for mutation in ['bool_schema', 'bad_history_hash', 'bad_history_fields', 'duplicate_history']:
            with self.subTest(mutation=mutation):
                report = copy.deepcopy(original_report)
                if mutation == 'bool_schema': report['schema_version'] = True
                if mutation == 'bad_history_hash': report['history'][0]['observations'][0]['state_sha256'] = 'bad'
                if mutation == 'bad_history_fields': report['history'][0]['observations'][0]['execute'] = 'payload'
                if mutation == 'duplicate_history': report['history'] *= 2
                report['report_sha256'] = pr.report_digest(report)
                (self.root/'report.json').write_text(json.dumps(report), encoding='utf-8')
                with self.assertRaises(Violation):
                    pt.apply_tasks(self.root, 'report.json', 'todo.md', sha(before), namespace='B', start=11, exclusive_writer=True)
                self.assertEqual(todo.read_bytes(), before)

    def test_failed_replace_cleans_owned_temporary_files_without_changing_todo(self):
        import project_review_tasks as pt
        (self.root/'result.txt').unlink()
        report = self.run_review()
        (self.root/'report.json').write_text(json.dumps(report), encoding='utf-8')
        todo = self.root/'todo.md'
        before = todo.read_bytes()
        with mock.patch.object(pt.os, 'replace', side_effect=PermissionError('target busy')):
            with self.assertRaises(OSError):
                pt.apply_tasks(self.root, 'report.json', 'todo.md', sha(before), namespace='B', start=11, exclusive_writer=True)
        self.assertEqual(todo.read_bytes(), before)
        self.assertFalse(list(self.root.glob('*.tools-c-review.lock')))
        self.assertFalse(list(self.root.glob('.tools-c-review-*')))

    def test_late_finding_truncation_cannot_close_acceptance_in_any_order(self):
        original = copy.deepcopy(self.packet)
        for count in [99, 100, 101]:
            for mandatory_first in [True, False]:
                with self.subTest(count=count, mandatory_first=mandatory_first):
                    self.packet = copy.deepcopy(original)
                    lines = ['CORE-001 Required result']
                    for i in range(count):
                        rid, cid, aid = f'OPTION-{i}', f'CHECK-{i}', f'FILE-{i}'
                        lines.append(rid+' Optional visual check')
                        path = f'optional-{i}.txt'
                        (self.root/path).write_bytes(b'present')
                        self.packet['requirements'].append(dict(id=rid, source=dict(id='spec', line=i+2),
                            description='Optional visual check', mandatory=False, level='L4', checks=[cid]))
                        self.packet['tasks'][0]['requirements'].append(rid)
                        self.packet['artifacts'].append(dict(id=aid, path=path))
                        self.packet['checks'].append(dict(id=cid, requirement=rid, artifact=aid, kind='file_exists'))
                    (self.root/'spec.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
                    self.packet['sources'][0]['sha256'] = sha((self.root/'spec.md').read_bytes())
                    if not mandatory_first:
                        self.packet['requirements'].reverse()
                    result = self.run_review()
                    self.assertEqual(result['omitted_findings'], max(0, count-100))
                    self.assertEqual(result['acceptance_status'], 'OPEN' if count > 100 else 'PASS')
                    if count > 100:
                        import project_review_tasks as pt
                        (self.root/'report.json').write_text(json.dumps(result), encoding='utf-8')
                        before = (self.root/'todo.md').read_bytes()
                        with self.assertRaises(Violation):
                            pt.apply_tasks(self.root, 'report.json', 'todo.md', sha(before),
                                           namespace='B', start=11, exclusive_writer=True)
                        self.assertEqual((self.root/'todo.md').read_bytes(), before)
        (self.root/'result.txt').unlink()
        self.assertEqual(self.run_review()['acceptance_status'], 'FAIL')

    def test_optional_failure_does_not_close_unestablished_mandatory_scope(self):
        self.packet['requirements'][0]['mandatory'] = False
        (self.root/'result.txt').unlink()
        result = self.run_review()
        self.assertEqual(result['requirements'][0]['status'], 'FAIL')
        self.assertEqual(result['acceptance_status'], 'OPEN')

    def test_malformed_cli_returns_structured_failure(self):
        (self.root/'review.json').write_bytes(b'{"unknown":true}')
        result = subprocess.run([sys.executable, str(TOOLS/'project_review.py'), 'validate', 'review.json',
                                 '--project', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['analysis_status'], 'FAIL')
        self.assertNotIn('Traceback', result.stderr)

    def test_cli_failed_acceptance_is_not_inferred_from_process_exit(self):
        (self.root/'result.txt').unlink()
        result = subprocess.run([sys.executable, str(TOOLS/'project_review.py'), 'converge', 'review.json',
                                 '--project', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report['analysis_status'], 'PASS')
        self.assertEqual(report['acceptance_status'], 'FAIL')
        self.assertEqual(report['findings'][0]['gap_kind'], 'missing')

    def test_cli_opt_in_acceptance_gate_distinguishes_pass_fail_and_open(self):
        command=[sys.executable,str(TOOLS/'project_review.py'),'converge','review.json',
                 '--project',str(self.root),'--require-acceptance']
        passed=subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(passed.returncode,0,passed.stderr)
        (self.root/'result.txt').unlink()
        failed=subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(failed.returncode,2,failed.stderr)
        self.assertEqual(json.loads(failed.stdout)['acceptance_status'],'FAIL')
        self.packet['checks']=[]
        self.packet['requirements'][0]['checks']=[]
        self.save()
        opened=subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(opened.returncode,2,opened.stderr)
        self.assertEqual(json.loads(opened.stdout)['acceptance_status'],'OPEN')

    def test_read_only_cli_and_no_source_payload_or_unimplemented_operations(self):
        before = {f.name:f.read_bytes() for f in self.root.iterdir() if f.is_file()}
        result = subprocess.run([sys.executable, str(TOOLS/'project_review.py'), 'converge', 'review.json',
                                 '--project', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['acceptance_status'], 'PASS')
        self.assertNotIn('PRIVATE_SOURCE_CANARY', result.stdout)
        self.assertEqual(before, {f.name:f.read_bytes() for f in self.root.iterdir() if f.is_file()})
        unsupported = subprocess.run([sys.executable, str(TOOLS/'project_review.py'), 'apply-tasks',
                                     'review.json', '--project', str(self.root)], capture_output=True)
        self.assertEqual(unsupported.returncode, 2)


if __name__ == '__main__':
    unittest.main()
