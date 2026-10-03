"""Anime geometry ownership, compatible contexts and opt-in invariants."""
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

OWNER = 'blender-anime-character-modeling'
CONTRACT = '.tooling/blender-anime-contracts.json'


class AnimeRoutingTest(unittest.TestCase):
    def test_creation_and_regional_revisions_select_one_geometry_owner(self):
        for task in [OWNER, 'Create an anime character.', 'Build a manga humanoid.',
                     'Model a chibi anime character blockout.', 'Make an anime avatar.',
                     'Fix the anime face proportions.', 'Refine the anime hair silhouette.',
                     'Сделай аниме персонажа.', 'Создай чиби аниме персонажа.',
                     'Смоделируй голову персонажа в стиле аниме.',
                     'Исправь пропорции аниме лица, сохрани rig и веса.']:
            with self.subTest(task=task):
                self.assertEqual(mcp_runtime.route_task(task), [OWNER])

    def test_style_mentions_do_not_restart_modeling_for_other_stages(self):
        cases = {
            'Review the anime character silhouette without editing it.': ['verification'],
            'Проверь лицо аниме персонажа, без правок.': ['verification'],
            'Retopologize the anime head without changing its silhouette.': ['blender-pipeline'],
            'Unwrap UVs on the anime character.': ['blender-pipeline'],
            'Set up toon materials for the anime character.': ['blender-pipeline'],
            'Add glow and dirt to the anime character.': ['blender-posteffects-polishing'],
            'Create a rig for the anime character.': ['blender-rigging-skinning'],
            'Fix weights on the anime character hair.': ['blender-rigging-skinning'],
            'Create an animation for the anime character.': ['blender-animation'],
            'Export the anime character as GLB.': ['blender-export-validation'],
            'Sculpt the anime cheek.': ['blender-sculpting'],
            'Create an anime-style car.': ['blender-vehicle-modeling'],
            'Create a generic character blockout.': ['blender-character-modeling'],
            'Preserve the anime character silhouette. Fix the weights.': ['blender-rigging-skinning'],
        }
        for task, expected in cases.items():
            with self.subTest(task=task):
                self.assertEqual(mcp_runtime.route_task(task), expected)

    def test_requested_creation_can_handoff_to_surfaces_and_delivery(self):
        cases = {
            'Create an anime character, then unwrap UVs.': ['blender-pipeline', OWNER],
            'Create an anime character and export GLB.': ['blender-export-validation', OWNER],
            'Создай аниме персонажа, затем добавь свечение.': ['blender-posteffects-polishing', OWNER],
        }
        for task, expected in cases.items():
            with self.subTest(task=task):
                self.assertEqual(mcp_runtime.route_task(task), expected)

    def test_default_context_delivers_geometry_and_conditional_techniques_without_truncation(self):
        result = mcp_runtime.context(check.ROOT, OWNER)
        self.assertTrue(result['ok'], result['error'])
        content = result['skills'][0]['content']
        for path in ['docs/foundation.md', 'docs/blender-evidence.md',
                     f'skills/{OWNER}/SKILL.md', 'skills/blender-character-modeling/SKILL.md',
                     f'skills/{OWNER}/references/face-hair-workflow.md']:
            self.assertIn('SOURCE: ' + path + '\n\n', content)
        self.assertEqual(result['skills'][0]['sha256'], hashlib.sha256(content.encode()).hexdigest())
        self.assertFalse(mcp_runtime.context(check.ROOT, OWNER, 50)['ok'])

    def test_cached_reader_receives_specialist_dependencies_once(self):
        current = read_blender_skill.render(check.ROOT, OWNER)
        marker = 'SOURCE: skills/blender-character-modeling/SKILL.md\n\n'
        previous = current.split('\n\n' + marker)[0]
        self.assertNotEqual(previous, current)
        with patch.object(mcp_runtime, 'render', return_value=previous):
            self.assertEqual(mcp_runtime.render_context(check.ROOT, OWNER), current)
        for path in ['skills/blender-character-modeling/SKILL.md',
                     f'skills/{OWNER}/references/face-hair-workflow.md']:
            self.assertEqual(mcp_runtime.render_context(check.ROOT, OWNER).count('SOURCE: ' + path + '\n\n'), 1)

    def test_all_legacy_aliases_retain_their_owners(self):
        aliases = check.catalog(check.ROOT)['blender_aliases']
        self.assertEqual(len(aliases), 9)
        for alias, item in aliases.items():
            with self.subTest(alias=alias):
                self.assertIn('SOURCE: ' + item['reference'] + '\n\n', read_blender_skill.render(check.ROOT, alias))


class AnimeContractsTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='anime contracts ')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / 'central'
        shutil.copytree(check.ROOT, self.root, ignore=shutil.ignore_patterns('.git', '.local', '__pycache__'))
        environment = patch.dict(os.environ, {'TOOLS_C_ROOT': str(self.root)})
        environment.start()
        self.addCleanup(environment.stop)

    def write(self, path, value):
        (self.root / path).write_text(json.dumps(value), encoding='utf-8')

    def violation(self, rule):
        result = check.run(self.root, self.root)
        self.assertTrue(any(item['rule'] == rule and item['status'] == 'FAIL'
                            for item in result.results), result.results)

    def test_valid_self_profile_with_replaceable_art_choices_passes(self):
        (self.root / '.tooling/profile.md').write_text('Choose any agreed anime style, proportions and destination.', encoding='utf-8')
        self.assertFalse(check.run(self.root, self.root).failed)

    def test_profile_membership_and_activation_cannot_be_silently_removed(self):
        baseline = check.read_json(self.root / '.tooling/profile.json')
        for field, value, rule in [('skills', OWNER, 'BAM-PROFILE'),
                                   ('contracts', CONTRACT, 'TOOLS-ANIME-CONTRACTS'),
                                   ('contracts', '.tooling/contracts.json', 'BAM-PROFILE')]:
            with self.subTest(value=value):
                data = copy.deepcopy(baseline)
                data[field].remove(value)
                self.write('.tooling/profile.json', data)
                self.violation(rule)

    def test_canonical_registration_rejects_retargeted_owner(self):
        manifest = check.read_json(self.root / 'manifest.json')
        next(s for s in manifest['skills'] if s['id'] == OWNER)['path'] = 'skills/blender-props/SKILL.md'
        self.write('manifest.json', manifest)
        rule = next(r for r in check.read_json(self.root / CONTRACT)['rules'] if r['id'] == 'BAM-REGISTRATION')
        with self.assertRaises(check.Violation) as error:
            check.check_rule(self.root, rule)
        self.assertEqual(error.exception.code, 'E_JSON_VALUE')

    def test_entrypoints_need_actual_links_not_literal_paths(self):
        rule = next(r for r in check.read_json(self.root / CONTRACT)['rules'] if r['id'] == 'BAM-ENTRYPOINTS')
        target = f'skills/{OWNER}/SKILL.md'
        for name in rule['paths']:
            path = self.root / name
            baseline = path.read_bytes()
            relative = os.path.relpath(self.root / target, path.parent).replace('\\', '/')
            replacement = os.path.relpath(self.root / 'docs/foundation.md', path.parent).replace('\\', '/')
            with self.subTest(path=name):
                path.write_text(baseline.decode().replace('(' + relative + ')', '(' + replacement + ')')
                                + '\n`' + relative + '`\n', encoding='utf-8')
                self.violation('BAM-ENTRYPOINTS')
            path.write_bytes(baseline)

    def test_prerequisite_and_evidence_links_cannot_be_silently_retargeted(self):
        path = self.root / f'skills/{OWNER}/SKILL.md'
        baseline = path.read_bytes()
        rule = next(r for r in check.read_json(self.root / CONTRACT)['rules'] if r['id'] == 'BAM-DEPENDENCIES')
        for target in rule['required_targets']:
            relative = os.path.relpath(self.root / target, path.parent).replace('\\', '/')
            with self.subTest(target=target):
                path.write_text(baseline.decode().replace('(' + relative + ')', '(../../README.md)')
                                + '\n`' + relative + '`\n', encoding='utf-8')
                self.violation('BAM-DEPENDENCIES')
            path.write_bytes(baseline)


if __name__ == '__main__':
    unittest.main()
