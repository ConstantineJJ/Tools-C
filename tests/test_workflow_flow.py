"""Flow regressions: routing, context parity and honest acceptance strength."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_qa_gate import fixture
import qa_gate as qa
import mcp_runtime as runtime
import read_blender_skill as reader

ROOT = Path(__file__).resolve().parents[1]


class FlowTest(unittest.TestCase):
    def test_russian_review_is_not_geometry_creation(self):
        for task in ('Ревью модели стула.', 'Аудит персонажа по фото.',
                     'Сделай ревью бюста этого парня в Blender.',
                     'Проведи проверку геометрии персонажа.',
                     'Сделай обзор blender-character-modeling без правок.'):
            with self.subTest(task=task):
                self.assertEqual(runtime.route_task(task), ['verification'])

    def test_review_with_authorized_fix_keeps_both_owners(self):
        owners = runtime.route_task('Сделай ревью стула, затем исправь геометрию стула.')
        self.assertIn('verification', owners)
        self.assertIn('blender-props', owners)

    def test_reference_bust_and_head_route_to_character(self):
        for task in ('Blender_MCP Сделай 3D модель бюста этого парня в Блендере.',
                     'Model a 3D bust of this man in Blender from reference.',
                     'Создай голову человека по фото.',
                     'Create a 3D model of this woman.',
                     'Sculpt a human head from reference.'):
            with self.subTest(task=task):
                owners = runtime.route_task(task)
                self.assertEqual(owners[0], 'visual-reference-reconstruction')
                self.assertIn('blender-character-modeling', owners)

    def test_incidental_mentions_and_preservation_do_not_build_a_face(self):
        for task in ('Create a camera near this person in Blender.',
                     'Создай камеру рядом с этим персонажем в Blender.',
                     'Не создавай бюст этого человека. Проверь материал.',
                     'Create a face texture from this image.',
                     'Draw a portrait of this woman.',
                     'Improve materials on this character.'):
            with self.subTest(task=task):
                self.assertNotIn('blender-character-modeling', runtime.route_task(task))

    def test_existing_sculpt_repair_does_not_restart_design(self):
        self.assertEqual(runtime.route_task('Sculpt scratches on the existing head from reference.'),
                         ['blender-sculpting'])

    def test_cached_reader_gets_the_same_required_documents(self):
        current = reader.render(ROOT, 'blender-character-modeling')
        first = current.split('\n\nSOURCE: ')[0]
        with patch.object(runtime, 'render', return_value=first):
            self.assertEqual(runtime.render_context(ROOT, 'blender-character-modeling'), current)

    def test_flow_is_delivered_and_budget_loss_is_explicit(self):
        task = 'Сделай 3D модель бюста этого парня в Blender.'
        result = runtime.context(ROOT, task)
        content = '\n'.join(row['content'] for row in result['skills'])
        self.assertIn('## Execution flow between gates', content)
        self.assertTrue(runtime.context(ROOT, task, max_chars=200000)['ok'])
        tiny = runtime.context(ROOT, task, max_chars=100)
        self.assertFalse(tiny['ok'])
        self.assertIn(runtime.CHARACTER_GATES, tiny['missing_documents'])

    def test_failed_gate_never_suggests_dependent_work(self):
        packet = fixture(changed=False)
        packet['checks']['form_contacts']['status'] = 'FAIL'
        result = qa.validate(packet)
        self.assertEqual(result['acceptance_gate'], 'FAIL')
        self.assertNotIn(result['next_action'], ('CONTINUE_SCOPED_DETAIL', 'HANDOFF_DECLARED_EVIDENCE'))

    def test_base_missing_reviews_still_block_dual_progression(self):
        from test_qa_artistic import fixture as dual_fixture
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packet = dual_fixture(root)
            for item in packet['captures']:
                item['status'] = 'REVIEW_REQUIRED'
            packet['dual_verification']['artistic'] = None
            # Base evidence coverage still blocks progression regardless of a critic.
            result = qa.validate(packet, root=root)
            self.assertEqual(result['acceptance_gate'], 'OPEN')
            self.assertEqual(result['next_action'], 'RESOLVE_GATE')

    def test_dual_technical_blocker_cannot_suggest_acceptance(self):
        from test_qa_artistic import fixture as dual_fixture
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packet = dual_fixture(root)
            packet['dual_verification']['technical_checks'].append('missing_probe')
            result = qa.validate(packet, root=root)
            self.assertEqual(result['acceptance_gate'], 'OPEN')
            self.assertEqual(result['next_action'], 'RESOLVE_GATE')

    def test_metadata_only_pass_cannot_claim_acceptance_readiness(self):
        result = qa.validate(fixture(changed=False))
        self.assertEqual(result['gate'], 'PASS')  # legacy declaration compatibility
        self.assertEqual(result['acceptance_gate'], 'OPEN')
        self.assertEqual(result['file_verification'], 'NOT_RUN')
        self.assertEqual(result['next_action'], 'VERIFY_FILES')

    def test_verified_files_are_not_visual_judgment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packet = fixture(changed=False)
            for capture in packet['captures']:
                path = root / capture['image']['path']
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'sample reviewed frame')
            result = qa.validate(packet, root=root)
            self.assertEqual(result['acceptance_gate'], 'PASS')
            self.assertEqual(result['file_verification'], 'PASS')
            self.assertEqual(result['visual'], 'NOT_EVALUATED')
            packet['captures'][0]['status'] = 'REVIEW_REQUIRED'
            result = qa.validate(packet, root=root)
            self.assertEqual(result['acceptance_gate'], 'OPEN')
            self.assertEqual(result['next_action'], 'RESOLVE_GATE')


if __name__ == '__main__':
    unittest.main()
