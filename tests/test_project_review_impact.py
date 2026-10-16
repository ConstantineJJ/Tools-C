"""Bounded impact is dependency evidence, never rule execution or asset acceptance."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

TOOLS = Path(__file__).resolve().parents[1] / 'tools'
sys.path.insert(0, str(TOOLS))
import project_review as pr
from check import Violation


class ImpactTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.packet = dict(schema_version=1, scope='impact-fixture', revision=1, sources=[],
            requirements=[dict(id='CORE-001', source=dict(id='rule', line=1),
                description='Bounded rule', mandatory=True, level='L1', checks=['C1'])],
            tasks=[dict(id='B2', source=dict(id='todo', line=1), requirements=['CORE-001'])],
            artifacts=[dict(id='result', path='result.txt')],
            checks=[dict(id='C1', requirement='CORE-001', artifact='result', kind='file_exists')])
        self.source('rule', 'rules.md', 'CORE-001 Bounded rule\n')
        self.source('todo', 'todo.md', '- [ ] B2 Implement CORE-001\n')
        (self.root/'result.txt').write_bytes(b'result')

    def source(self, sid, path, content):
        target = self.root/path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
        self.packet['sources'].append(dict(id=sid, path=path, sha256=pr.digest(target.read_bytes())))

    def save(self):
        (self.root/'review.json').write_text(json.dumps(self.packet), encoding='utf-8')

    def impact(self, **kwargs):
        self.save()
        return pr.review(self.root, 'review.json', operation='impact', **(kwargs or dict(changed_source='rule')))

    def test_literal_dependency_independent_file_and_transitive_possible(self):
        self.source('skill', 'skills/sample/SKILL.md', '# Skill\n[Rule](../../rules.md)\n')
        self.source('guide', 'guide.md', '[Skill](skills/sample/SKILL.md)\n')
        self.source('unrelated', 'independent.md', 'A separate rule.\n')
        result = self.impact()
        impact = result['impact']
        self.assertIn('skill', [r['source'] for r in impact['direct']])
        self.assertIn('guide', [r['source'] for r in impact['possible']])
        self.assertIn('unrelated', impact['not_observed'])
        direct = next(r for r in impact['direct'] if r['source'] == 'skill')
        self.assertEqual(direct['evidence'][0]['line'], 2)
        self.assertEqual(result['acceptance_status'], 'NOT_EVALUATED')
        self.assertFalse(impact['coverage']['complete'])

    def test_code_comments_and_web_links_are_not_local_dependencies(self):
        self.source('quoted', 'quoted.md', '<!-- [hidden](rules.md) -->\n`[code](rules.md)`\n```md\n[example](rules.md)\n```\n[web](https://example.invalid/rules.md)\n')
        result = self.impact()['impact']
        self.assertNotIn('quoted', [r['source'] for r in result['direct']])
        self.assertTrue(result['unknown'])

    def test_rule_scope_does_not_upgrade_file_link_to_exact_rule_dependency(self):
        self.source('guide', 'guide.md', '[Rules](rules.md)\n')
        result = self.impact(changed_rule='CORE-001')
        change = result['impact']['change']
        self.assertEqual(change['requirement'], 'CORE-001')
        self.assertEqual(result['impact']['direct'][0]['evidence'][0]['granularity'], 'file')
        self.assertEqual(result['impact']['schema_migration']['status'], 'UNKNOWN')
        self.assertTrue(all(r['status'] == 'NOT_RUN' for r in result['impact']['recommended_checks']))
        self.assertTrue(all(r['level'] == 'L1' for r in result['impact']['executed_checks']))

    def test_paths_stale_sources_and_unknown_change_are_rejected(self):
        self.source('escaped', 'escaped.md', '[escape](../outside.md)\n')
        with self.assertRaises(Violation): self.impact()
        self.packet['sources'].pop()
        with self.assertRaises(Violation): self.impact(changed_source='absent')
        (self.root/'rules.md').write_text('CORE-001 changed\n', encoding='utf-8')
        with self.assertRaises(Violation): self.impact()

    def test_impact_does_not_evaluate_missing_artifacts_or_propose_tasks(self):
        (self.root/'result.txt').unlink()
        result = self.impact()
        self.assertEqual(result['checks'], [])
        self.assertEqual(result['proposed_tasks'], [])
        self.assertEqual(result['visual_status'], 'NOT_EVALUATED')

    def test_cli_is_read_only_and_source_payload_is_not_echoed(self):
        self.source('guide', 'guide.md', 'PRIVATE_CANARY_DO_NOT_ECHO\n[Rule](rules.md)\n')
        self.save()
        before = {p.relative_to(self.root).as_posix():p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = subprocess.run([sys.executable, str(TOOLS/'project_review.py'), 'impact', 'review.json',
            '--project', str(self.root), '--changed-source', 'rule'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('PRIVATE_CANARY_DO_NOT_ECHO', result.stdout)
        self.assertEqual(json.loads(result.stdout)['impact']['change']['source'], 'rule')
        self.assertEqual(before, {p.relative_to(self.root).as_posix():p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_history_is_not_resume_or_manual_acceptance(self):
        self.save()
        previous = pr.review(self.root, 'review.json', operation='converge')
        (self.root/'previous.json').write_text(json.dumps(previous), encoding='utf-8')
        self.packet['checks'][0]['kind'] = 'manual'
        self.packet['requirements'][0]['level'] = 'L4'
        self.save()
        result = pr.review(self.root, 'review.json', operation='converge', previous='previous.json')
        self.assertEqual(result['acceptance_status'], 'OPEN')
        self.assertEqual(result['visual_status'], 'NOT_EVALUATED')
        self.assertEqual(result['proposed_tasks'], [])
        with self.assertRaises(Violation): self.impact(changed_source='rule', previous='previous.json')

    def test_contract_profile_manifest_and_alias_dependencies(self):
        self.source('contract', 'core.json', json.dumps(dict(schema_version=1, id='core',
            rules=[dict(id='FILES-001', kind='files', paths=['rules.md'])])))
        self.source('skill', 'skills/sample/SKILL.md', '# Sample\n')
        self.source('manifest', 'manifest.json', json.dumps(dict(schema_version=1, version='1.0',
            skills=[dict(id='sample', path='skills/sample/SKILL.md')],
            blender_aliases={'Legacy_Sample':dict(reference='skills/sample/SKILL.md', source_sha256='0'*64, source_version='1.0')})))
        self.source('profile', '.tooling/profile.json', json.dumps(dict(schema_version=1, id='project',
            skills=['sample'], contracts=['core.json'], references=['rules.md'])))
        result = self.impact()['impact']
        direct = {r['source']:r for r in result['direct']}
        self.assertTrue({'contract', 'profile'} <= direct.keys())
        self.assertEqual(direct['contract']['kind'], 'contract')
        self.assertEqual(direct['profile']['kind'], 'profile')
        self.assertIn('pointer', direct['contract']['evidence'][0])
        skill = self.impact(changed_source='skill')['impact']
        direct = {r['source']:r for r in skill['direct']}
        self.assertTrue({'manifest', 'profile'} <= direct.keys())
        self.assertTrue(any(e['relation']=='alias_reference' for e in direct['manifest']['evidence']))

    def test_python_import_is_possible_and_never_executes_source(self):
        self.source('module', 'policy.py', 'raise RuntimeError("DO_NOT_EXECUTE")\n')
        self.source('test', 'tests/test_policy.py', 'if False:\n    import policy\n')
        result = self.impact(changed_source='module')['impact']
        entry = next(r for r in result['possible'] if r['source']=='test')
        self.assertEqual(entry['kind'], 'test')
        self.assertEqual(entry['evidence'][0]['line'], 2)
        self.assertEqual(entry['evidence'][0]['relation'], 'python_import')
        self.assertNotIn('test', [r['source'] for r in result['direct']])

    def test_unknown_targets_types_and_unresolved_ids_are_explicit(self):
        self.source('reader', 'reader.md', '[unselected](unselected.md)\n')
        self.source('other', 'opaque.cfg', 'PRIVATE_OPAQUE_DATA\n')
        self.source('profile', 'profile.json', json.dumps(dict(schema_version=1, id='project',
            skills=['unknown-skill'], contracts=['unknown.json'], references=['rules.md'])))
        result = self.impact()['impact']
        reasons = {r['reason'] for r in result['unknown']}
        self.assertTrue({'dependency_target_not_selected', 'unsupported_source_type', 'unresolved_skill_id'} <= reasons)
        self.assertFalse((self.root/'unselected.md').exists())

    def test_adapter_errors_bounds_and_output_truncation_are_not_silent_pass(self):
        self.source('json', 'core.json', '{"schema_version":1,"id":"core","rules":[{"id":"X","kind":"files","paths":["../escape"]}]}')
        with self.assertRaises(Violation): self.impact()
        self.packet['sources'].pop()
        self.source('guide', 'guide.md', '[one](rules.md)\n[two](todo.md)\n')
        import project_review_impact as impact
        with mock.patch.object(impact, 'EDGE_LIMIT', 1):
            with self.assertRaises(Violation): self.impact()
        with mock.patch.object(pr, 'FINDING_LIMIT', 1):
            result = self.impact()
        self.assertTrue(result['impact']['omitted'])
        self.assertEqual(result['acceptance_status'], 'NOT_EVALUATED')

    def test_selection_flags_are_exclusive_and_not_valid_for_convergence(self):
        self.save()
        command=[sys.executable, str(TOOLS/'project_review.py')]
        for args in [['impact'], ['impact', '--changed-source', 'rule', '--changed-rule', 'CORE-001'],
                     ['converge', '--changed-source', 'rule']]:
            result = subprocess.run(command+[args[0], 'review.json', '--project', str(self.root), *args[1:]],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, result.stdout+result.stderr)

    def test_current_canonical_pointer_does_not_expand_into_unselected_sources(self):
        self.source('config', '.tooling/config.json', json.dumps(dict(schema_version=1,
            tools_root=str(TOOLS.parent), profile='.tooling/profile.json')))
        self.packet['sources'].append(dict(id='foundation', path='docs/foundation.md', root='tools',
            sha256=pr.digest((TOOLS.parent/'docs/foundation.md').read_bytes())))
        self.source('reader', 'reader.md', 'Nothing implicitly links to foundation.\n')
        result = self.impact(changed_source='foundation')['impact']
        self.assertEqual(result['change']['root'], 'tools')
        self.assertNotIn('reader', [r['source'] for r in result['direct']])
        self.assertTrue(any(r['reason']=='dependency_target_not_selected' for r in result['unknown']))

    def test_explicit_direct_binding_wins_over_possible_import(self):
        self.source('module', 'policy.py', '# CORE-001 Rule\n')
        self.source('consumer', 'consumer.py', '# B2 task\nimport policy\n')
        self.packet['requirements'][0]['source'] = dict(id='module', line=1)
        self.packet['tasks'][0]['source'] = dict(id='consumer', line=1)
        result = self.impact(changed_source='module')['impact']
        self.assertIn('consumer', [r['source'] for r in result['direct']])
        self.assertNotIn('consumer', [r['source'] for r in result['possible']])

    def test_unknown_observations_are_bounded_too(self):
        self.source('web', 'web.md', '[one](https://example.invalid/one)\n[two](https://example.invalid/two)\n')
        import project_review_impact as impact
        with mock.patch.object(impact, 'EDGE_LIMIT', 1):
            with self.assertRaises(Violation): self.impact()

    def test_absolute_encoded_and_symlink_escape_links_fail_closed(self):
        for target in ['C:/outside.md', 'file:///outside.md', '..%2foutside.md', '//server/share']:
            with self.subTest(target=target):
                original = copy.deepcopy(self.packet)
                self.source('escape', 'escape.md', f'[escape]({target})\n')
                with self.assertRaises(Violation): self.impact()
                self.packet = original
        with tempfile.TemporaryDirectory() as elsewhere:
            try:
                (self.root/'escape').symlink_to(elsewhere, target_is_directory=True)
            except OSError as error:
                self.skipTest('symlink unavailable: '+str(error))
            self.source('escape', 'escape.md', '[escape](escape/any.md)\n')
            with self.assertRaises(Violation): self.impact()

    def test_generated_router_context_is_unknown_without_running_renderer(self):
        self.source('router', 'skills/Legacy/SKILL.md', '<!-- tools-c-router -->\n```python\nraise RuntimeError("NO_RUN")\n```\n')
        result = self.impact()['impact']
        self.assertTrue(any(r.get('source')=='router' and r['reason']=='router_runtime_context_not_evaluated' for r in result['unknown']))

    def test_impact_ids_survive_revision_and_source_hash_changes(self):
        self.source('guide', 'guide.md', '[Rule](rules.md)\n')
        first = next(r for r in self.impact()['impact']['direct'] if r['source']=='guide')
        (self.root/'guide.md').write_text('Unrelated text\n[Rule](rules.md)\n', encoding='utf-8')
        self.packet['sources'][-1]['sha256'] = pr.digest((self.root/'guide.md').read_bytes())
        self.packet['revision'] = 2
        second = next(r for r in self.impact()['impact']['direct'] if r['source']=='guide')
        self.assertEqual(first['id'], second['id'])
        self.assertNotEqual(first['sha256'], second['sha256'])
        self.assertEqual(second['evidence'][0]['target_source'], 'rule')

    def test_structured_sources_are_strict_and_ambiguous_import_is_unknown(self):
        self.source('json', 'data.json', '{"x":1,"x":2}')
        with self.assertRaises(Violation): self.impact()
        self.packet['sources'].pop()
        self.source('module1', 'one/policy.py', '# rule\n')
        self.source('module2', 'two/policy.py', '# rule\n')
        self.source('consumer', 'consumer.py', 'import policy\n')
        result = self.impact(changed_source='module1')['impact']
        self.assertNotIn('consumer', [r['source'] for r in result['possible']])
        self.assertTrue(any(r.get('source')=='consumer' and r['reason']=='import_target_not_selected_or_ambiguous' for r in result['unknown']))

    def test_markdown_physical_lines_reference_definitions_and_cycles(self):
        self.source('a', 'a.md', '<!-- comment\n[hidden](rules.md) -->\n[rule]: rules.md\n[b](b.md)\n')
        self.source('b', 'b.md', '[a](a.md)\n')
        result = self.impact()['impact']
        a = next(r for r in result['direct'] if r['source']=='a')
        self.assertEqual(a['evidence'][0]['line'], 3)
        self.assertIn('b', [r['source'] for r in result['possible']])
        self.assertEqual(len({r['source'] for r in result['direct']+result['possible']}), len(result['direct']+result['possible']))

    def test_python_file_literal_is_possible_without_claiming_runtime_consumption(self):
        self.source('gate', 'tools/check.py', 'EXPECTED = "rules.md"\nEXAMPLE = "not-selected.md"\n')
        result = self.impact()['impact']
        gate = next(r for r in result['possible'] if r['source']=='gate')
        self.assertEqual(gate['kind'], 'gate')
        self.assertEqual(gate['evidence'][0]['relation'], 'python_path_literal')
        self.assertEqual(gate['evidence'][0]['target_source'], 'rule')


if __name__ == '__main__':
    unittest.main()
