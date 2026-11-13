"""Recovery discovery and transport, not artistic or autonomous repair acceptance."""
import hashlib
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check
import mcp_runtime as runtime
import read_blender_skill as reader
import skill_catalog

OWNER = 'blender-imported-asset-recovery'
BASE = 'skills/' + OWNER + '/'


class ImportedAssetRecoveryTests(unittest.TestCase):
    def test_local_repair_and_segmentation_discovery_ru_en(self):
        for query in [
            'Repair this imported model.',
            'Fix holes in the imported car mesh.',
            'Weld duplicate vertices on the selected mesh.',
            'Repair topology on the supplied scan.',
            'Repair the geometry of the imported car.',
            'Исправь геометрию импортированного автомобиля.',
            'Fix UVs on an imported character; preserve weights and Actions.',
            'Restore blurred textures on the imported model.',
            'Retexture the imported asset.',
            'Separate glasses from the imported character mesh.',
            'Split the existing model into editable parts.',
            'Исправь импортированную модель.',
            'Завари дырки в импортированном меше.',
            'Свари вершины на выделенном меше.',
            'Исправь UV развёртку импортированной модели, сохрани риг.',
            'Восстанови размытые текстуры готовой модели.',
            'Отдели очки и обувь у импортированного персонажа.',
            'Сегментируй модель на отдельные части.',
            'Исправь дырки в импортированном GLB.',
        ]:
            with self.subTest(query=query):
                self.assertEqual(runtime.route_task(query), [OWNER])
                found = skill_catalog.search(check.ROOT, query)
                self.assertEqual([r['name'] for r in found['results']], [OWNER])

    def test_unrelated_and_preservation_only_requests_keep_owners(self):
        for query, expected in [
            ('Review the imported mesh without changing geometry.', ['verification']),
            ('Проверь импортированную модель, не меняй геометрию.', ['verification']),
            ('Fix weights on the imported character.', ['blender-rigging-skinning']),
            ('Fix animation on the imported character.', ['blender-animation']),
            ('Export the imported asset as GLB.', ['blender-export-validation']),
            ('Model a new car from reference images.', ['visual-reference-reconstruction', 'blender-vehicle-modeling']),
            ('Create textures for an existing asset.', ['blender-pipeline']),
            ('Prepare an existing wooden crate as a destructible game asset.', ['blender-destruction-assets']),
            ('Model a car; preserve imported textures and separate parts.', ['blender-vehicle-modeling']),
            ('Restore a blurred photograph.', []),
        ]:
            with self.subTest(query=query):
                self.assertEqual(runtime.route_task(query), expected)

    def test_explicit_owner_and_requested_delivery(self):
        self.assertEqual(runtime.route_task('Inspect the imported mesh then close the holes.'), ['verification', OWNER])
        self.assertEqual(runtime.route_task('Use ' + OWNER + ' for this task.'), [OWNER])
        self.assertEqual(runtime.route_task('Fix holes in the imported mesh and export GLB to Godot.'),
                         [OWNER, 'blender-export-validation', 'godot-asset-integration'])
        self.assertEqual(runtime.route_task('Fix holes in the imported mesh from reference images.'), [OWNER])
        self.assertEqual(runtime.route_task('Create a new car from reference images and fix UVs on an imported model.'),
                         ['visual-reference-reconstruction', OWNER, 'blender-vehicle-modeling'])

    def test_full_default_context_and_unchanged_legacy_alias_count(self):
        listing = skill_catalog.listing(check.ROOT)
        self.assertEqual(sum(row['name'] == OWNER for row in listing['canonical_skills']), 1)
        self.assertEqual(len(listing['compatibility_aliases']), 9)
        context = runtime.context(check.ROOT, OWNER)
        self.assertTrue(context['ok'], context['missing_documents'])
        self.assertIn(BASE + 'references/inspection.md', context['receipts'])
        self.assertEqual(context['execution_status'], 'NOT_EVALUATED')
        self.assertEqual(context['acceptance_status'], 'NOT_EVALUATED')
        self.assertNotIn(BASE + 'references/surfaces.md', context['receipts'])
        direct = reader.render(check.ROOT, OWNER)
        for path in reader.document_paths(check.ROOT, OWNER):
            self.assertIn('SOURCE: ' + path + '\n\n' + (check.ROOT/path).read_text(encoding='utf-8'), direct)

    def test_conditional_recipes_load_with_actual_hashes(self):
        first = runtime.context(check.ROOT, OWNER)
        for recipe in ('geometry', 'segmentation', 'surfaces'):
            path = BASE + 'references/' + recipe + '.md'
            with self.subTest(recipe=recipe):
                result = runtime.context(check.ROOT, OWNER, known_documents=first['receipts'], requested_documents=[path])
                self.assertTrue(result['ok'], result['missing_documents'])
                body = (check.ROOT/path).read_text(encoding='utf-8')
                self.assertEqual(result['receipts'][path], hashlib.sha256(body.encode()).hexdigest())
                self.assertIn(body, result['skills'][0]['content'])
                self.assertEqual(next(d['status'] for d in result['documents'] if d['path'] == 'docs/foundation.md'), 'retained')

    def test_low_budget_is_not_false_complete(self):
        result = runtime.context(check.ROOT, OWNER, max_chars=100)
        self.assertFalse(result['ok'])
        self.assertTrue(result['missing_documents'])


if __name__ == '__main__':
    unittest.main()
