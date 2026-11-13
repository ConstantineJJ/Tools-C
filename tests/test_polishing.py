"""Finishing ownership, full context, legacy compatibility and active contracts."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check
import mcp_runtime
import read_blender_skill

OWNER = 'blender-posteffects-polishing'
CONTRACT = '.tooling/blender-polishing-contracts.json'


class PolishingRoutingTest(unittest.TestCase):
    def test_finishing_selects_stage_without_restarting_asset_geometry(self):
        cases = [
            OWNER, 'Posteffects and polishing',
            'Add dirt and chipped paint to the existing car materials.',
            'Refine the materials and texture scratches on the microwave.',
            'Improve the existing textures of the crate.',
            'Preserve UVs and weights and improve the existing textures of the crate.',
            'Polish the vehicle materials without changing its UVs or rig.',
            'Add masked emission and glow to the console display.',
            'Create a glow material for the existing street lamp.',
            'Add surface cracks to the stone facade texture.',
            'Добавь грязь, потёртости и шелушение краски на автомобиль.',
            'Улучши материалы и текстуры чайника, добавь свечение индикатора.',
            'Сохрани UV и веса и добавь грязь на ящик.',
            'Preserve UVs and weights and add dirt to the crate.',
        ]
        for task in cases:
            with self.subTest(task=task):
                self.assertEqual(mcp_runtime.route_task(task), [OWNER])
                self.assertEqual(mcp_runtime.procedure_routes(mcp_runtime.action_query(task)), [])

    def test_read_only_and_negated_finishing_keep_their_owner(self):
        cases = {
            'Review the car dirt and glow without editing it.': ['verification'],
            'Проверь потёртости и свечение на приставке, без правок.': ['verification'],
            'Do not add dirt or glow. Retopologize the vehicle body.': ['blender-pipeline'],
            'Unwrap UVs on the car. No weathering or glow.': ['blender-pipeline'],
            'Fix shoulder weights and preserve the glowing materials.': ['blender-rigging-skinning'],
            'Inspect the chipped paint and then add localized grime.': ['verification', OWNER],
        }
        for task, expected in cases.items():
            with self.subTest(task=task): self.assertEqual(mcp_runtime.route_task(task), expected)

    def test_baseline_surfaces_sculpt_and_delivery_remain_distinct(self):
        cases = {
            'Unwrap UVs and bake normal maps for the car.': ['blender-pipeline'],
            'Set up PBR materials for the microwave.': ['blender-pipeline'],
            'Исправь UV и материалы чайника, геометрию не меняй.': ['blender-pipeline'],
            'Sculpt cracks and dents on the car.': ['blender-vehicle-modeling', 'blender-sculpting'],
            'Sculpt surface cracks without changing the materials.': ['blender-sculpting'],
            'Sculpt scratches, then add masked glow.': [OWNER, 'blender-sculpting'],
            'Unwrap the crate and add chipped paint.': ['blender-pipeline', OWNER],
            'Create a crate, then add dirt and peeling paint.': [OWNER, 'blender-props'],
            'Add glow to the console and export GLB.': [OWNER, 'blender-export-validation'],
            'Add emissive material and validate the asset in Godot.': [OWNER, 'godot-asset-integration'],
        }
        for task, expected in cases.items():
            with self.subTest(task=task): self.assertEqual(mcp_runtime.route_task(task), expected)
        self.assertEqual(mcp_runtime.procedure_routes('unwrap the crate and add chipped paint.'), ['surfaces'])

    def test_full_context_contains_finish_and_capture_procedures(self):
        result = mcp_runtime.context(check.ROOT, OWNER)
        self.assertTrue(result['ok'], result['error'])
        content = result['skills'][0]['content']
        for path in ['docs/foundation.md', 'docs/blender-evidence.md',
                     f'skills/{OWNER}/SKILL.md', f'skills/{OWNER}/references/finishing-techniques.md']:
            self.assertIn('SOURCE: ' + path, content)
        self.assertEqual(result['skills'][0]['sha256'], hashlib.sha256(content.encode()).hexdigest())
        mixed = mcp_runtime.context(check.ROOT, 'Unwrap the crate and add chipped paint.', 160000)
        self.assertEqual(mixed['routing']['procedures'], ['surfaces'])
        self.assertIn('SOURCE: skills/blender-pipeline/references/surfaces.md', mixed['skills'][0]['content'])
        self.assertFalse(mcp_runtime.context(check.ROOT, OWNER, 50)['ok'])

    def test_legacy_names_remain_usable_with_updated_pipeline_context(self):
        aliases = check.catalog(check.ROOT)['blender_aliases']
        self.assertEqual(len(aliases), 9)
        for alias in aliases:
            with self.subTest(alias=alias):
                result = read_blender_skill.render(check.ROOT, alias)
                self.assertIn('SOURCE: ' + aliases[alias]['reference'], result)
                self.assertIn('SOURCE: docs/blender-evidence.md', result)

    def test_cached_legacy_reader_still_receives_new_finishing_reference_once(self):
        current = read_blender_skill.render(check.ROOT, OWNER)
        marker = 'SOURCE: skills/blender-posteffects-polishing/references/finishing-techniques.md\n\n'
        previous = current.split('\n\n' + marker)[0]
        self.assertNotEqual(previous, current)
        with patch.object(mcp_runtime, 'render', return_value=previous):
            self.assertEqual(mcp_runtime.render_context(check.ROOT, OWNER), current)
        self.assertEqual(mcp_runtime.render_context(check.ROOT, OWNER).count(marker), 1)


class PolishingContractsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='finishing contracts ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'central'
        shutil.copytree(check.ROOT, self.root, ignore=shutil.ignore_patterns('.git', '.local', '__pycache__'))
        self.env = patch.dict(os.environ, {'TOOLS_C_ROOT': str(self.root)})
        self.env.start(); self.addCleanup(self.env.stop)

    def write(self, path, value):
        (self.root / path).write_text(json.dumps(value), encoding='utf-8')

    def violation(self, rule, code):
        report = check.run(self.root, self.root)
        self.assertTrue(any(r['rule'] == rule and r['status'] == 'FAIL' and r['code'] == code
                            for r in report.results), report.results)

    def test_profile_membership_and_contract_activation_are_required(self):
        baseline = check.read_json(self.root / '.tooling/profile.json')
        for value, field, rule in [(OWNER, 'skills', 'BPP-PROFILE'),
                                   (CONTRACT, 'contracts', 'TOOLS-POLISHING-CONTRACTS'),
                                   ('.tooling/contracts.json', 'contracts', 'BPP-PROFILE')]:
            with self.subTest(value=value):
                profile = copy.deepcopy(baseline); profile[field].remove(value)
                self.write('.tooling/profile.json', profile)
                self.violation(rule, 'E_JSON_VALUE')

    def test_each_real_entrypoint_and_surface_handoff_is_required(self):
        cases = [('docs/skills.md', f'../skills/{OWNER}/SKILL.md', '../README.md', 'BPP-ENTRYPOINTS'),
                 ('skills/blender-pipeline/SKILL.md', f'../{OWNER}/SKILL.md', 'references/core.md', 'BPP-ENTRYPOINTS'),
                 ('skills/blender-pipeline/references/surfaces.md', f'../../{OWNER}/SKILL.md', '../SKILL.md', 'BPP-SURFACES-HANDOFF'),
                 ('skills/blender-pipeline/references/core.md', f'../../{OWNER}/SKILL.md', '../SKILL.md', 'BPP-SURFACES-HANDOFF')]
        for path, target, other, rule in cases:
            file = self.root / path; before = file.read_bytes()
            with self.subTest(path=path):
                file.write_text(before.decode().replace(f'({target})', f'({other})') + '\n`' + target + '`\n', encoding='utf-8')
                self.violation(rule, 'E_ROUTE')
            file.write_bytes(before)

    def test_skill_dependencies_cannot_be_silently_retargeted(self):
        path = self.root / f'skills/{OWNER}/SKILL.md'; before = path.read_bytes()
        rule = next(r for r in check.read_json(self.root / CONTRACT)['rules'] if r['id'] == 'BPP-DEPENDENCIES')
        for target in rule['required_targets']:
            relative = os.path.relpath(self.root / target, path.parent).replace('\\', '/')
            with self.subTest(target=target):
                path.write_text(before.decode().replace(f'({relative})', '(../../README.md)') + '\n`' + relative + '`\n', encoding='utf-8')
                self.violation('BPP-DEPENDENCIES', 'E_ROUTE')
            path.write_bytes(before)

    def test_registration_rule_rejects_missing_or_retargeted_canonical_owner(self):
        rule = next(r for r in check.read_json(self.root / CONTRACT)['rules'] if r['id'] == 'BPP-REGISTRATION')
        manifest = check.read_json(self.root / 'manifest.json')
        for retarget in [False, True]:
            changed = copy.deepcopy(manifest)
            if retarget:
                next(s for s in changed['skills'] if s['id'] == OWNER)['path'] = 'skills/blender-props/SKILL.md'
            else:
                changed['skills'] = [s for s in changed['skills'] if s['id'] != OWNER]
            self.write('manifest.json', changed)
            with self.subTest(retarget=retarget), self.assertRaises(check.Violation) as error:
                check.check_rule(self.root, rule)
            self.assertEqual(error.exception.code, 'E_JSON_VALUE')


if __name__ == '__main__':
    unittest.main()
