"""Tools_C 4.3.0: export grouping/markers, scene state, capture views."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))
import ast  # noqa: E402
import blender_scene_state  # noqa: E402
import export_validate  # noqa: E402
from test_weapon_module import glb, interface, module_nodes  # noqa: E402


class ExportGroupingTests(unittest.TestCase):
    def test_expected_differences_collapse_per_kind(self):
        lines = [f'Part_{i}: source mesh representation differs; bounds/other gates checked separately'
                 for i in range(9)] + ['Label: procedural geometry became mesh']
        rows = export_validate.group_differences(lines)
        self.assertEqual([r['count'] for r in rows], [9, 1])
        self.assertIn('+3 more', rows[0]['objects'])
        self.assertTrue(rows[0]['note'].startswith('expected'))

    def test_markers_and_weapon_interface_after_export(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'asset.glb'
            path.write_bytes(glb(module_nodes()))
            (root / 'weapon.json').write_text(json.dumps(interface()), encoding='utf-8')
            job = dict(markers=['Laser_C_Muzzle'], weapon_interface='weapon.json', weapon_root='Laser_C')
            failures, report = export_validate.post_export_checks(job, path, root)
            self.assertEqual(failures, [])
            self.assertEqual(report['weapon_interface']['status'], 'STRUCTURAL PASS')
            failures, _ = export_validate.post_export_checks(dict(markers=['Muzzle']), path, root)
            self.assertEqual(failures, ['Marker missing from GLB: Muzzle'])
            path.write_bytes(glb(module_nodes(muzzle=(-0.2, 0.19, 0.0))))
            failures, _ = export_validate.post_export_checks(job, path, root)
            self.assertTrue(failures and failures[0].startswith('Weapon interface:'))
            with self.assertRaises(ValueError):
                export_validate.check_markers(path, 'Muzzle')


class SceneStateTests(unittest.TestCase):
    def state(self, **overrides):
        data = dict(file='C:/work/a.blend', is_dirty=False, objects=[
            dict(name='A', hidden=False, hide_viewport=False),
            dict(name='B', hidden=True, hide_viewport=False)])
        data.update(overrides)
        return blender_scene_state.summarize(data)

    def test_baseline_guidance_follows_file_state(self):
        self.assertEqual(self.state()['hidden_objects'], ['B'])
        self.assertIn('Saved file is the baseline', self.state()['baseline'])
        self.assertIn('unsaved changes', self.state(is_dirty=True)['baseline'])
        unsaved = self.state(file=None, is_dirty=True)
        self.assertTrue(unsaved['unsaved_session'])
        self.assertIn('copy=True', unsaved['baseline'])


class WeaponRoutingTests(unittest.TestCase):
    def owners(self, task):
        import mcp_runtime
        return mcp_runtime.route_task(task)

    def test_weapon_subject_vs_attribute(self):
        redesign = self.owners('Переделай этот лазер примерно как на референсе, излучатель фиолетовый')
        self.assertIn('blender-weapon-module', redesign)
        self.assertIn('blender-weapon-module', self.owners('Model a plasma cannon turret head'))
        mech = self.owners('Создай лёгкого разведывательного меха с двумя пушками')
        self.assertIn('blender-robot-mechanism-modeling', mech)
        self.assertNotIn('blender-weapon-module', mech)
        self.assertIn('blender-weapon-module', self.owners('Build a weapon module for the car with a laser'))
        self.assertNotIn('blender-weapon-module', self.owners('Review the laser export'))


class CaptureViewTests(unittest.TestCase):
    def test_mirrored_and_rear_views_exist(self):
        # blender_capture imports bpy; read its VIEWS literal without Blender.
        tree = ast.parse((ROOT / 'tools/blender_capture.py').read_text(encoding='utf-8'))
        node = next(n.value for n in tree.body if isinstance(n, ast.Assign)
                    and any(getattr(t, 'id', None) == 'VIEWS' for t in n.targets))
        views = ast.literal_eval(node)
        for name in ('left', 'three_quarter_left', 'rear_three_quarter', 'rear_three_quarter_left'):
            self.assertIn(name, views)
        x, y, _ = views['three_quarter']
        self.assertEqual(views['three_quarter_left'][:2], (-x, y))
        self.assertGreater(views['rear_three_quarter'][1], 0)


if __name__ == '__main__':
    unittest.main()
