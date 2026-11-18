import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import weapon_module as wm  # noqa: E402


def interface(**overrides):
    data = {"schema_version": 1, "forward_axis": "-X", "match": "suffix", "tolerance": 0.002,
            "markers": {"socket": "SocketReceiver", "muzzle": ["Muzzle"], "optional": ["FX_Exhaust"]},
            "budgets": {"max_triangles": 1000, "max_materials": 3, "max_emissive_materials": 1}}
    data.update(overrides)
    return data


def glb(nodes, materials=None, triangles=12, position=((-0.6, 0.0, -0.15), (0.44, 0.34, 0.15))):
    gltf = {"asset": {"version": "2.0"}, "scene": 0, "scenes": [{"nodes": [0]}], "nodes": nodes,
            "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "indices": 1, "material": 0}]}],
            "accessors": [{"count": 8, "type": "VEC3", "componentType": 5126,
                           "min": list(position[0]), "max": list(position[1])},
                          {"count": triangles * 3, "type": "SCALAR", "componentType": 5123}],
            "materials": materials or [{"name": "Hull"}]}
    payload = json.dumps(gltf).encode()
    payload += b' ' * (-len(payload) % 4)
    return struct.pack('<4sII', b'glTF', 2, 20 + len(payload)) + struct.pack('<I4s', len(payload), b'JSON') + payload


def module_nodes(muzzle=(-0.61, 0.19, 0.0)):
    return [{"name": "Laser_C", "children": [1, 2, 3]},
            {"name": "Laser_C_Body", "mesh": 0},
            {"name": "Laser_C_Muzzle", "translation": list(muzzle)},
            {"name": "Laser_C_SocketReceiver", "translation": [0.0, 0.0, 0.0]}]


class WeaponModuleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, data, name='module.glb'):
        path = self.root / name
        path.write_bytes(data)
        return path

    def test_interface_is_strict(self):
        self.assertEqual(wm.validate_interface(interface())['forward_axis'], '-X')
        for bad in (interface(extra=1), interface(forward_axis='X'), interface(schema_version=2),
                    interface(markers={"muzzle": []}), interface(budgets={"max_tris": 3}),
                    interface(budgets={"max_triangles": -1}), interface(match='prefix')):
            with self.assertRaises(wm.InterfaceError):
                wm.validate_interface(bad)
        path = self.root / 'dup.json'
        path.write_text('{"schema_version": 1, "schema_version": 1}', encoding='utf-8')
        with self.assertRaises(wm.InterfaceError):
            wm.load_interface(path)

    def test_glb_module_passes_with_prefixed_markers(self):
        report = wm.check_glb(wm.validate_interface(interface()), self.write(glb(module_nodes())), 'Laser_C')
        self.assertEqual(report['status'], 'STRUCTURAL PASS', report['items'])
        muzzle = next(i for i in report['items'] if i['check'] == 'muzzle')
        self.assertIn('Laser_C_Muzzle', muzzle['message'])
        self.assertEqual(report['triangles'], 12)

    def test_muzzle_behind_the_front_fails(self):
        nodes = module_nodes(muzzle=(-0.2, 0.19, 0.0))
        report = wm.check_glb(wm.validate_interface(interface()), self.write(glb(nodes)), 'Laser_C')
        self.assertEqual(report['status'], 'FAIL')

    def test_missing_markers_and_budgets_fail(self):
        nodes = [{"name": "Laser_C", "children": [1]}, {"name": "Laser_C_Body", "mesh": 0}]
        report = wm.check_glb(wm.validate_interface(interface()), self.write(glb(nodes, triangles=2000)), 'Laser_C')
        failed = {i['check'] for i in report['items'] if i['status'] == 'FAIL'}
        self.assertEqual(failed, {'socket', 'muzzle', 'max_triangles'})

    def test_axis_conversion_follows_blender_forward(self):
        # Blender +Y forward is glTF -Z; a marker at glTF z=-0.3 leads that axis.
        nodes = [{"name": "Gun", "children": [1, 2]}, {"name": "Gun_Body", "mesh": 0},
                 {"name": "Gun_Muzzle", "translation": [0.0, 0.1, -0.3]}]
        data = interface(forward_axis='+Y', markers={"socket": None, "muzzle": ["Muzzle"]})
        report = wm.check_glb(wm.validate_interface(data),
                              self.write(glb(nodes, position=((-0.1, 0.0, -0.3), (0.1, 0.2, 0.3)))), 'Gun')
        self.assertEqual(report['status'], 'STRUCTURAL PASS', report['items'])

    def test_emissive_and_socket_origin(self):
        materials = [{"name": "Glow", "emissiveFactor": [1, 0.5, 0]}]
        data = interface(socket_origin=[0.0, 0.0, 0.0])
        report = wm.check_glb(wm.validate_interface(data), self.write(glb(module_nodes(), materials)), 'Laser_C')
        self.assertEqual(report['emissive'], ['Glow'])
        self.assertEqual(report['status'], 'STRUCTURAL PASS', report['items'])
        moved = module_nodes()
        moved[3]['translation'] = [0.1, 0.0, 0.0]
        self.assertEqual(wm.check_glb(wm.validate_interface(data), self.write(glb(moved), 'b.glb'), 'Laser_C')['status'], 'FAIL')

    def test_exact_match_rejects_prefixed_names(self):
        data = interface(match='exact')
        report = wm.check_glb(wm.validate_interface(data), self.write(glb(module_nodes())), 'Laser_C')
        self.assertEqual(report['status'], 'FAIL')

    def test_cli_exit_codes(self):
        iface = self.root / 'weapon-modules.json'
        iface.write_text(json.dumps(interface()), encoding='utf-8')
        good = self.write(glb(module_nodes()))
        self.assertEqual(wm.main(['glb', str(good), '--interface', str(iface), '--root', 'Laser_C']), 0)
        bad = self.write(glb(module_nodes(muzzle=(0.0, 0.19, 0.0))), 'bad.glb')
        self.assertEqual(wm.main(['glb', str(bad), '--interface', str(iface), '--root', 'Laser_C']), 1)
        self.assertEqual(wm.main(['glb', str(self.write(b'nope', 'x.glb')), '--interface', str(iface)]), 2)


if __name__ == '__main__':
    unittest.main()
