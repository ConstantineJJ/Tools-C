"""Destruction discovery, stage boundaries and complete canonical delivery.

These tests prove routing/transport, not fracture aesthetics or engine physics.
"""
import hashlib
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check
import mcp_runtime as runtime
import read_blender_skill as reader
import skill_catalog


OWNER = 'blender-destruction-assets'
PHYSICS = 'skills/' + OWNER + '/references/physics-and-verification.md'
MATERIALS = 'skills/' + OWNER + '/references/material-recipes.md'


class DestructionAssetsTests(unittest.TestCase):
    def test_live_style_discovery_routes_material_aware_preparation_in_ru_and_en(self):
        for query in [
            'Prepare an existing wooden crate as a destructible game asset with 8 bodies.',
            'Fracture the existing stone wall along masonry joints.',
            'Shatter this glass pane into game-ready fragments.',
            'Destruction planning for an existing metal cabinet.',
            'Подготовь разрушаемый деревянный ящик для игрового движка.',
            'Раздели каменную стену на обломки для разрушения.',
            'Подготовь осколки стекла с внутренними поверхностями.',
            'Сделай существующую скамейку разрушаемой, основание сохранить.',
            'Разбей деревянный ящик на доски и распорки.',
            'Break the existing crate into planks.',
        ]:
            with self.subTest(query=query):
                self.assertEqual(runtime.route_task(query), [OWNER])
                result = skill_catalog.search(check.ROOT, query)
                self.assertEqual([r['name'] for r in result['results']], [OWNER])

    def test_preservation_surface_sculpt_review_and_export_keep_their_owners(self):
        for query, expected in [
            ('Model a wooden crate; preserve destruction fragments.', ['blender-props']),
            ('Model a wooden crate without destruction.', ['blender-props']),
            ('Добавь царапины и поверхностные трещины на ящик.', ['blender-posteffects-polishing']),
            ('Sculpt cracks and chips on the existing stone wall.', ['blender-sculpting']),
            ('Review the destructible crate collision proxies without changing geometry.', ['verification']),
            ('Export the existing destruction fragments as GLB.', ['blender-export-validation']),
            ('Export the unchanged fractured asset as GLB to Godot.', ['blender-export-validation', 'godot-asset-integration']),
            ('Add a collapse animation to the existing fragments.', ['blender-animation']),
            ('Create a collapse animation for the existing fragments.', ['blender-animation']),
            ('Create textures for the existing fracture fragments.', ['blender-pipeline']),
            ('Create UVs for the existing destructible crate.', ['blender-pipeline']),
            ('Model a portable wooden crate.', ['blender-props']),
        ]:
            with self.subTest(query=query):
                self.assertEqual(runtime.route_task(query), expected)

    def test_explicit_owner_in_sentence_and_mixed_authorized_stage(self):
        self.assertEqual(runtime.route_task('Use blender-destruction-assets for this asset.'), [OWNER])
        self.assertEqual(runtime.route_task('Prepare a destructible asset and export GLB to Godot.'),
                         [OWNER, 'blender-export-validation', 'godot-asset-integration'])
        self.assertEqual(runtime.route_task('Create a wooden crate and prepare it as a destructible asset.'),
                         [OWNER, 'blender-props'])
        self.assertEqual(runtime.route_task('Review the crate and prepare destruction fragments.'),
                         [OWNER, 'verification'])
        self.assertEqual(runtime.route_task('Create a destructible glass pane from reference images.'),
                         ['visual-reference-reconstruction', OWNER])
        self.assertEqual(runtime.route_task('Make the existing crate destructible using reference images.'),
                         [OWNER])

    def test_registered_owner_and_complete_context_fit_default_budget(self):
        records = skill_catalog.listing(check.ROOT)
        row = next(r for r in records['canonical_skills'] if r['name'] == OWNER)
        self.assertEqual(row['path'], 'skills/' + OWNER + '/SKILL.md')
        self.assertEqual(len(records['compatibility_aliases']), 9)
        context = runtime.context(check.ROOT, OWNER)
        self.assertTrue(context['ok'], context['missing_documents'])
        self.assertEqual(context['routing']['owners'], [OWNER])
        self.assertIn(PHYSICS, context['receipts'])
        direct = reader.render(check.ROOT, OWNER)
        for path in reader.document_paths(check.ROOT, OWNER):
            self.assertIn('SOURCE: ' + path + '\n\n' + (check.ROOT/path).read_text(encoding='utf-8'), direct)

    def test_material_reference_is_available_on_demand_with_real_receipts(self):
        first = runtime.context(check.ROOT, OWNER)
        second = runtime.context(check.ROOT, OWNER, known_documents=first['receipts'],
                                 requested_documents=[MATERIALS])
        self.assertTrue(second['ok'], second['missing_documents'])
        body = (check.ROOT/MATERIALS).read_text(encoding='utf-8')
        self.assertEqual(second['receipts'][MATERIALS], hashlib.sha256(body.encode()).hexdigest())
        self.assertIn(body, second['skills'][0]['content'])
        states = {d['path']: d['status'] for d in second['documents']}
        self.assertEqual(states['docs/foundation.md'], 'retained')


if __name__ == '__main__':
    unittest.main()
