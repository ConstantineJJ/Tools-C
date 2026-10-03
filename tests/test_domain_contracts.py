"""Positive/negative evidence for declarative Blender domain-pack invariants."""
import copy
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check

OWNER_IDS = ['blender-architecture-environment', 'blender-environment-assets',
             'blender-roads-infrastructure', 'blender-props', 'blender-vehicle-modeling',
             'blender-product-electronics-modeling', 'blender-vegetation', 'blender-sculpting']


class DomainContractsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='domain pack contracts ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'central'
        shutil.copytree(check.ROOT, self.root, ignore=shutil.ignore_patterns('.git', '.local', '__pycache__'))
        self.env = patch.dict(os.environ, {'TOOLS_C_ROOT': str(self.root)})
        self.env.start(); self.addCleanup(self.env.stop)

    def load(self, path):
        return check.read_json(self.root / path)

    def write(self, path, value):
        (self.root / path).write_text(json.dumps(value), encoding='utf-8')

    def result(self):
        return check.run(self.root, tools_root=self.root)

    def violation(self, rule, code):
        result = self.result()
        self.assertTrue(result.failed, result.results)
        self.assertTrue(any(item['rule'] == rule and item['code'] == code and item['status'] == 'FAIL'
                            for item in result.results), result.results)

    def test_valid_pack_and_additive_project_choices_pass_without_mutation(self):
        profile = self.load('.tooling/profile.json')
        profile['skills'].reverse()  # Membership does not freeze ordering.
        profile['references'].append('docs/engines.md')
        self.write('.tooling/profile.json', profile)
        watched = ['manifest.json', '.tooling/profile.json', '.tooling/blender-domain-contracts.json']
        before = {path: (self.root / path).read_bytes() for path in watched}
        with patch.object(subprocess, 'run', side_effect=AssertionError('L1 must not launch engines')):
            self.assertFalse(self.result().failed)
        self.assertEqual(before, {path: (self.root / path).read_bytes() for path in watched})

    def test_each_of_eight_profile_owners_is_required(self):
        baseline = self.load('.tooling/profile.json')
        for owner in OWNER_IDS:
            with self.subTest(owner=owner):
                profile = copy.deepcopy(baseline); profile['skills'].remove(owner)
                self.write('.tooling/profile.json', profile)
                self.violation('BDP-PROFILE', 'E_JSON_VALUE')

    def test_domain_contract_cannot_be_silently_removed_from_self_profile(self):
        profile = self.load('.tooling/profile.json')
        profile['contracts'].remove('.tooling/blender-domain-contracts.json')
        self.write('.tooling/profile.json', profile)
        self.violation('TOOLS-DOMAIN-CONTRACTS', 'E_JSON_VALUE')

    def test_base_contract_cannot_be_removed_while_domain_contract_remains(self):
        profile = self.load('.tooling/profile.json')
        profile['contracts'].remove('.tooling/contracts.json')
        self.write('.tooling/profile.json', profile)
        self.violation('BDP-PROFILE', 'E_JSON_VALUE')

    def test_self_config_cannot_point_checks_at_an_unrelated_profile(self):
        profile = self.load('.tooling/profile.json')
        profile['contracts'].remove('.tooling/blender-domain-contracts.json')
        self.write('.tooling/other-profile.json', profile)
        config = self.load('.tooling/config.json'); config['profile'] = '.tooling/other-profile.json'
        self.write('.tooling/config.json', config)
        self.violation('TOOLS-SELF-PROFILE', 'E_JSON_VALUE')

    def test_all_nine_legacy_aliases_keep_their_canonical_targets(self):
        baseline = self.load('manifest.json')
        for alias, item in baseline['blender_aliases'].items():
            with self.subTest(alias=alias):
                manifest = copy.deepcopy(baseline)
                replacement = 'skills/blender-props/SKILL.md'
                if item['reference'] == replacement:
                    replacement = 'skills/blender-vegetation/SKILL.md'
                manifest['blender_aliases'][alias]['reference'] = replacement
                self.write('manifest.json', manifest)
                self.violation('BDP-LEGACY', 'E_JSON_VALUE')

    def test_legacy_migration_provenance_is_not_a_current_content_lock(self):
        manifest = self.load('manifest.json')
        item = manifest['blender_aliases']['Blender_Organic_Sculpting_SKILL']
        item['source_sha256'] = 'a' * 64; item['source_version'] = 'audited-fixture'
        self.write('manifest.json', manifest)
        self.assertFalse(self.result().failed)

    def test_canonical_owner_path_cannot_move_silently(self):
        manifest = self.load('manifest.json')
        item = next(item for item in manifest['skills'] if item['id'] == 'blender-vegetation')
        old = self.root / item['path']; new = old.parent / 'relocated/SKILL.md'
        new.parent.mkdir(); old.rename(new)
        item['path'] = new.relative_to(self.root).as_posix()
        self.write('manifest.json', manifest)
        for value in ['AGENTS.md', 'skills/blender-pipeline/SKILL.md']:
            path = self.root / value
            path.write_text(path.read_text(encoding='utf-8').replace('blender-vegetation/SKILL.md', 'blender-vegetation/relocated/SKILL.md'), encoding='utf-8')
        # Make the relocated skill structurally valid; only the stable path rule should reject it.
        text = re.sub(r'\]\((?!https?:)([^)]+)\)', lambda match: '](../' + match[1] + ')',
                      new.read_text(encoding='utf-8'))
        new.write_text(text, encoding='utf-8')
        self.violation('BDP-REGISTRATION', 'E_JSON_VALUE')

    def test_each_pipeline_domain_route_is_required(self):
        path = self.root / 'skills/blender-pipeline/SKILL.md'
        baseline = path.read_text(encoding='utf-8')
        for owner in OWNER_IDS:
            with self.subTest(owner=owner):
                target = f'../{owner}/SKILL.md'
                path.write_text(baseline.replace(f'({target})', '(references/core.md)'), encoding='utf-8')
                self.violation('BDP-PIPELINE', 'E_ROUTE')

    def test_downstream_stage_routes_remain_with_their_owners(self):
        path = self.root / 'skills/blender-pipeline/SKILL.md'
        baseline = path.read_text(encoding='utf-8')
        for target in ['references/retopology.md', 'references/surfaces.md',
                       '../blender-rigging-skinning/SKILL.md', '../blender-animation/SKILL.md',
                       '../blender-export-validation/SKILL.md', '../godot-asset-integration/SKILL.md']:
            with self.subTest(target=target):
                path.write_text(baseline.replace(f'({target})', '(references/core.md)'), encoding='utf-8')
                self.violation('BDP-PIPELINE', 'E_ROUTE')

    def test_agents_route_requires_a_link_not_a_literal_path(self):
        path = self.root / 'AGENTS.md'
        target = 'skills/blender-vegetation/SKILL.md'
        path.write_text(path.read_text(encoding='utf-8').replace(f'({target})', '(README.md)') + '\n`' + target + '`\n', encoding='utf-8')
        self.violation('BDP-AGENTS', 'E_ROUTE')

    def test_every_owner_has_an_actual_shared_foundation_link(self):
        for owner in OWNER_IDS:
            path = self.root / f'skills/{owner}/SKILL.md'; baseline = path.read_bytes()
            with self.subTest(owner=owner):
                path.write_text(baseline.decode('utf-8').replace('(../../docs/foundation.md)', '(../../README.md)') + '\n`../../docs/foundation.md`\n', encoding='utf-8')
                self.violation('BDP-FOUNDATION', 'E_ROUTE')
            path.write_bytes(baseline)

    def test_compatibility_pointer_cannot_route_to_another_existing_owner(self):
        path = self.root / 'skills/blender-pipeline/references/sculpting.md'
        path.write_text(path.read_text(encoding='utf-8').replace('../../blender-sculpting/SKILL.md', '../../blender-props/SKILL.md'), encoding='utf-8')
        self.violation('BDP-SCULPT-COMPAT', 'E_ROUTE')

    def test_renamed_labels_and_encoded_reference_links_are_valid(self):
        doc = self.root / 'probe.md'
        target = 'docs/foundation.md'
        for text in ['[new wording](docs/foundation.md#anchor)', '[owner]: docs/foundation.md',
                     '[new wording](docs/%66oundation.md)']:
            doc.write_text(text, encoding='utf-8')
            check.markdown_links(self.root, doc, [target])

    def test_code_comments_and_images_do_not_satisfy_required_routes(self):
        doc = self.root / 'probe.md'
        for text in ['`[owner](docs/foundation.md)`', '```text\n[owner](docs/foundation.md)\n```',
                     '<!-- [owner](docs/foundation.md) -->', '![owner](docs/foundation.md)']:
            with self.subTest(text=text):
                doc.write_text(text, encoding='utf-8')
                with self.assertRaises(check.Violation) as error:
                    check.markdown_links(self.root, doc, ['docs/foundation.md'])
                self.assertEqual(error.exception.code, 'E_ROUTE')

    def test_malformed_new_rule_shapes_are_rejected(self):
        rules = [dict(id='BAD', kind='json_subset', paths=['manifest.json'], expected=value)
                 for value in [None, [], {}, 42, {'number': float('nan')}]]
        rules += [dict(id='BAD', kind='markdown', paths=['AGENTS.md'], required_targets=value)
                  for value in [None, [], 'README.md', [42]]]
        rules += [dict(id='BAD', kind='json_subset', paths=['manifest.json', 'README.md'], expected={'id': 'x'}),
                  dict(id='BAD', kind='json_subset', paths=['manifest.json'], expected={'id': 'x'}, typo=True)]
        for rule in rules:
            with self.subTest(rule=rule), self.assertRaises(check.Violation) as error:
                check.validate_contract(dict(schema_version=1, id='test', rules=[rule]), set())
            self.assertEqual(error.exception.code, 'E_SCHEMA')

    def test_required_target_escape_is_a_hard_failure_even_for_warn(self):
        contract = dict(schema_version=1, id='target-escape', rules=[dict(id='ESCAPE', kind='markdown',
            paths=['AGENTS.md'], required_targets=['../outside.md'], severity='WARN')])
        self.write('.tooling/blender-domain-contracts.json', contract)
        self.violation('.tooling/blender-domain-contracts.json', 'E_PATH')

    def test_json_subset_warn_stays_advisory_and_scalar_types_are_exact(self):
        contract = dict(schema_version=1, id='advisory', rules=[dict(id='ADVISORY', kind='json_subset',
            paths=['manifest.json'], expected={'schema_version': True}, severity='WARN')])
        self.write('.tooling/blender-domain-contracts.json', contract)
        result = self.result()
        self.assertFalse(result.failed)
        self.assertTrue(any(item['rule'] == 'ADVISORY' and item['status'] == 'WARN' and
                            item['code'] == 'E_JSON_VALUE' for item in result.results))

    def test_json_overflow_numbers_are_rejected_before_subset_matching(self):
        for value in ['1e999', '-1e999']:
            path = self.root / 'probe.json'; path.write_text('{"number":' + value + '}', encoding='utf-8')
            with self.assertRaises(check.Violation) as error:
                check.read_json(path)
            self.assertEqual(error.exception.code, 'E_JSON')

    def test_required_target_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            outside = Path(directory); (outside / 'outside.md').write_text('external')
            try:
                (self.root / 'escape').symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(str(exc))
            contract = dict(schema_version=1, id='target-escape', rules=[dict(id='ESCAPE', kind='markdown',
                paths=['AGENTS.md'], required_targets=['escape/outside.md'])])
            self.write('.tooling/blender-domain-contracts.json', contract)
            self.violation('.tooling/blender-domain-contracts.json', 'E_PATH')

    def test_cli_reports_new_diagnostic_and_nonzero_exit(self):
        profile = self.load('.tooling/profile.json')
        profile['skills'].remove('blender-sculpting')
        self.write('.tooling/profile.json', profile)
        process = subprocess.run([sys.executable, str(self.root / 'tools/check.py'),
                                  '--self', '--json'], capture_output=True, text=True)
        self.assertEqual(process.returncode, 1, process.stderr)
        self.assertNotIn('Traceback', process.stderr)
        self.assertTrue(any(item['rule'] == 'BDP-PROFILE' and item['code'] == 'E_JSON_VALUE'
                            for item in json.loads(process.stdout)))


if __name__ == '__main__':
    unittest.main()
