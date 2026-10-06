"""Source-first routing, auditable transfer lineage and registration regressions."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check
import mcp_runtime
import read_blender_skill
import surface_transfer as transfer

OWNER = 'blender-reference-surface-transfer'
CONTRACT = '.tooling/surface-transfer-contracts.json'


def fixture():
    artifacts = {n: dict(path=n+'.dat', sha256=hashlib.sha256(n.encode()).hexdigest())
                 for n in ('source', 'crop', 'repair', 'mask', 'prompt', 'bake', 'comparison')}
    return dict(schema_version=1, artifacts=artifacts,
                source=dict(artifact='source', role='ORIGINAL', size=[200, 100], authority='User source; logo patch on approved panel'),
                crop=[10, 20, 60, 40],
                steps=[dict(operation='crop', input='source', output='crop', reason='Reuse visible logo', parameters='10,20,60,40 pixels; no resampling')],
                target=dict(objects=['Panel'], faces='front faces', uv_map='UVMap', material='Paint', method='UV', image='crop', settings='Register three logo anchors'),
                bake=dict(status='DONE', artifact='bake', settings='Cycles diffuse color only; direct/indirect off; UVMap; 512 square; margin 8'),
                seam_cleanup=dict(status='SKIP', reason='Synthetic test record; no pixels inspected'),
                pbr_basis='Keep existing dielectric painted-metal coating; no RGB-derived roughness or normals',
                qa={n: dict(status='SKIP', reviewer='', observations='Synthetic record test; no asset review', artifacts=[])
                    for n in ('identity', 'seams', 'material', 'movement', 'reopen', 'target')})


class SurfaceRoutingTest(unittest.TestCase):
    def test_source_transfer_does_not_restart_geometry_or_finishing(self):
        tasks = [OWNER, 'Reference Surface Transfer',
                 'Transfer the face and eyes from the reference to the anime character.',
                 'Crop the logo from the source image for a decal on the car.',
                 'Project the original photo graffiti onto the building facade.',
                 'Transfer the reference wear pattern onto the mech panel.',
                 'Extract the clothing print texture from the source reference.',
                 'Create a decal from the source image on the mech panel.',
                 'Transfer logos from the reference onto the car.',
                 'Preserve geometry and transfer the logo from the reference.',
                 'Сохрани геометрию и перенеси рисунок с референса.',
                 'Сделай перенос рисунка с референса на панель меха.',
                 'Перенеси лицо и глаза с референса на аниме персонажа.',
                 'Перенеси маркировку и узор с фотографии на панель меха.',
                 'Вырежи логотип из исходного изображения для декали автомобиля.',
                 'Перенеси татуировку с референса, сохрани геометрию и веса.']
        for task in tasks:
            with self.subTest(task=task):
                self.assertEqual(mcp_runtime.route_task(task), [OWNER])

    def test_other_owners_remain_available(self):
        cases = {
            'Review the reference logo transfer without editing it.': ['verification'],
            'Проверь перенос рисунка с референса без правок.': ['verification'],
            'Preserve reference surface transfer. Fix the weights.': ['blender-rigging-skinning'],
            'Unwrap UVs on the anime character.': ['blender-pipeline'],
            'Set roughness and metallic materials for the mech.': ['blender-pipeline'],
            'Add procedural scratches to the mech.': ['blender-posteffects-polishing'],
            'Analyze the reference image.': ['visual-reference-reconstruction'],
            'Transfer the logo from the reference, then unwrap UVs.': [OWNER, 'blender-pipeline'],
            'Transfer the reference tattoo and export GLB.': [OWNER, 'blender-export-validation'],
            'Transfer the source logo; then add dirt.': [OWNER, 'blender-posteffects-polishing'],
        }
        for task, expected in cases.items():
            with self.subTest(task=task):
                self.assertEqual(mcp_runtime.route_task(task), expected)

    def test_creation_preserves_pass0_and_domain_owner(self):
        owners = mcp_runtime.route_task('Create a mech from the reference, then transfer the original panel markings.')
        self.assertEqual(owners, ['visual-reference-reconstruction', 'blender-robot-mechanism-modeling', OWNER])

    def test_discovery_complete_context_and_cached_reader(self):
        owner = next(s for s in check.catalog(check.ROOT)['skills'] if s['id'] == OWNER)
        self.assertEqual(owner['path'], f'skills/{OWNER}/SKILL.md')
        context = mcp_runtime.context(check.ROOT, OWNER)
        self.assertTrue(context['ok'], context)
        paths = [f'skills/{OWNER}/references/workflow.md', f'skills/{OWNER}/references/record.md',
                 'skills/blender-pipeline/references/surfaces.md']
        content = context['skills'][0]['content']
        for path in paths:
            self.assertEqual(content.count('SOURCE: '+path+'\n\n'), 1)
        self.assertEqual(context['skills'][0]['sha256'], hashlib.sha256(content.encode()).hexdigest())
        current = read_blender_skill.render(check.ROOT, OWNER)
        cached = current.split('\n\nSOURCE: '+paths[0])[0]
        with patch.object(mcp_runtime, 'render', return_value=cached):
            self.assertEqual(mcp_runtime.render_context(check.ROOT, OWNER), current)


class TransferRecordTest(unittest.TestCase):
    def test_original_pixels_need_no_regeneration(self):
        record = fixture(); before = copy.deepcopy(record)
        self.assertEqual(transfer.validate(record)['structural'], 'PASS')
        self.assertEqual(record, before)
        self.assertEqual(transfer.validate(record)['visual'], 'NOT_EVALUATED')

    def test_bounded_repair_requires_reason_mask_prompt_and_lineage(self):
        record = fixture()
        step = dict(operation='regenerate', input='crop', output='repair', mask='mask', prompt='prompt',
                    reason='Scratch obscures edge; no alternate source, cloning would duplicate glyph', parameters='Local masked repair; source anchors fixed')
        record['steps'].append(step); record['target']['image']='repair'
        self.assertEqual(transfer.validate(record)['structural'], 'PASS')
        for field in ('mask', 'prompt', 'reason'):
            bad = copy.deepcopy(record); del bad['steps'][1][field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                transfer.validate(bad)

    def test_invalid_records_fail_closed(self):
        mutations = [lambda p:p.update(schema_version=True),
                     lambda p:p.update(crop=[190, 0, 20, 10]),
                     lambda p:p.update(crop=[True, 0, 20, 10]),
                     lambda p:p['source'].update(role='AUXILIARY_INPUT'),
                     lambda p:p['steps'][0].update(input='mask'),
                     lambda p:p['steps'][0].update(output='source'),
                     lambda p:p['steps'][0].update(operation='invent'),
                     lambda p:p['steps'][0].update(extra='ignored?'),
                     lambda p:p['target'].update(image='source'),
                     lambda p:p['bake'].update(artifact='source'),
                     lambda p:p.update(seam_cleanup=dict(status='DONE', input='source', output='repair', settings='clone border')),
                     lambda p:p.update(pbr_basis=''),
                     lambda p:p['qa']['identity'].update(status='PASS'),
                     lambda p:p['artifacts']['source'].update(path='../outside.png'),
                     lambda p:p['artifacts']['source'].update(path='C:/outside.png'),
                     lambda p:p['artifacts']['source'].update(path='crop.dat'),
                     lambda p:p['artifacts']['source'].update(path='CROP.dat'),
                     lambda p:p['artifacts']['source'].update(path='./source.dat'),
                     lambda p:p['artifacts']['source'].update(sha256='wrong')]
        for mutation in mutations:
            record = fixture(); mutation(record)
            with self.subTest(record=record), self.assertRaises(ValueError):
                transfer.validate(record)

    def test_file_hashes_and_symlink_escape(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); record = fixture()
            for name, artifact in record['artifacts'].items():
                (root/artifact['path']).write_text(name, encoding='utf-8')
            self.assertEqual(transfer.validate(record, root)['files'], 'PASS')
            (root/'transfer.json').write_text(json.dumps(record), encoding='utf-8')
            cli=subprocess.run([sys.executable, str(check.ROOT/'tools/surface_transfer.py'),
                                str(root/'transfer.json'), '--verify-files'], capture_output=True, text=True)
            self.assertEqual(cli.returncode, 0, cli.stderr)
            self.assertEqual(json.loads(cli.stdout)['files'], 'PASS')
            (root/'source.dat').write_text('changed')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                transfer.validate(record, root)
            nested=root/'nested'; nested.mkdir()
            try:
                (nested/'source.dat').symlink_to(root/'source.dat')
            except OSError:
                return  # Hash test remains valid when Windows symlinks are unavailable.
            with self.assertRaisesRegex(ValueError, 'escapes'):
                transfer.validate(record, nested)

    def test_pending_or_recorded_qa_never_implies_visual_acceptance(self):
        record = fixture(); record['bake']=dict(status='PENDING', reason='await UV handoff')
        self.assertEqual(transfer.validate(record)['visual'], 'NOT_EVALUATED')
        record['qa']['identity'].update(status='PASS', reviewer='test', artifacts=['comparison'], observations='Named source anchors compared')
        self.assertEqual(transfer.validate(record)['visual'], 'NOT_EVALUATED')

    def test_cleanup_retains_bake_and_uses_distinct_output(self):
        record = fixture()
        record['seam_cleanup']=dict(status='DONE', input='bake', output='repair', settings='Clone border; preserve glyphs')
        self.assertEqual(transfer.validate(record)['structural'], 'PASS')
        record['seam_cleanup']['output']='bake'
        with self.assertRaises(ValueError):
            transfer.validate(record)

    def test_cli_rejects_malformed_json_without_traceback(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'bad.json'
            for data in ('{"schema_version":1,"schema_version":1}', '{"value":NaN}', '{bad'):
                path.write_text(data)
                result=subprocess.run([sys.executable, str(check.ROOT/'tools/surface_transfer.py'), str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(json.loads(result.stdout)['structural'], 'FAIL')
                self.assertNotIn('Traceback', result.stderr)


class TransferContractTest(unittest.TestCase):
    def test_registration_and_activation_reject_mutations(self):
        contract = check.read_json(check.ROOT/CONTRACT)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root/'.tooling').mkdir()
            for path in ('manifest.json', '.tooling/profile.json'):
                (root/path).write_bytes((check.ROOT/path).read_bytes())
            rules = {r['id']:r for r in contract['rules']}
            for name in ('RST-REGISTRATION', 'RST-PROFILE'):
                check.check_rule(root, rules[name])
            manifest=check.read_json(root/'manifest.json')
            next(s for s in manifest['skills'] if s['id']==OWNER)['path']='skills/blender-props/SKILL.md'
            (root/'manifest.json').write_text(json.dumps(manifest))
            with self.assertRaises(check.Violation):
                check.check_rule(root, rules['RST-REGISTRATION'])
            profile = check.read_json(root/'.tooling/profile.json')
            for field, value in [('skills', OWNER), ('contracts', CONTRACT), ('contracts', '.tooling/contracts.json')]:
                bad=copy.deepcopy(profile); bad[field].remove(value)
                (root/'.tooling/profile.json').write_text(json.dumps(bad))
                with self.subTest(field=field, value=value), self.assertRaises(check.Violation):
                    check.check_rule(root, rules['RST-PROFILE'])
            activation=next(r for r in check.read_json(check.ROOT/'.tooling/contracts.json')['rules'] if r['id']=='TOOLS-SURFACE-TRANSFER-CONTRACTS')
            bad=copy.deepcopy(profile); bad['contracts'].remove(CONTRACT)
            (root/'.tooling/profile.json').write_text(json.dumps(bad))
            with self.assertRaises(check.Violation):
                check.check_rule(root, activation)


if __name__ == '__main__':
    unittest.main()
