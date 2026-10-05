"""PASS 0 provenance/gates and robot stage routing; no wording-based quality proof."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
import shutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import mcp_runtime
import read_blender_skill
import check

spec = importlib.util.spec_from_file_location('pass0_validator', ROOT / 'skills/visual-reference-reconstruction/scripts/validate_pass0.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def fixture():
    source = dict(id='original', path='source.png', sha256='a'*64, role='PRIMARY',
                  projection='perspective', authority_note='original')
    derivative = dict(source, id='generated_input', role='AUXILIARY_INPUT', sha256='b'*64)
    claim = dict(id='body.exterior', property='visible exterior', value='one shell', certainty='CONFIRMED',
                 evidence=[dict(source_id='original', region='center', observation='one visible shell')], basis='Direct visible fact')
    dim = dict(copy.deepcopy(claim), id='body.width', property='relative width', value=[.3,.4],
               certainty='INFERRED', basis='Perspective estimate', component_id='body', axis='width', min=.3,max=.4,unit='H')
    return dict(schema_version=1,packet_id='test',task_scope='macro blockout',object_class='prop',
                source_of_truth=['original'],sources=[source,derivative],
                proportion_basis=dict(unit='H',scale_status='RELATIVE_ONLY',axis_convention='Z up',pose='neutral',camera_notes='lens unknown'),
                components=[dict(id='body',label='body',count=1,claims=[claim])],relative_dimensions=[dim],
                silhouette_notes=[dict(copy.deepcopy(claim),id='silhouette',property='outline')],relationships=[],
                ambiguity_map=[],contradictions=[],auxiliary_references=[],
                generation=dict(status='UNAVAILABLE',reason='No generator; honest source-only packet'),
                gate=dict(status='READY',permitted_stage='MACRO_BLOCKOUT',limits=[],reviewer='test',review_notes='source inspected'))


def auxiliary():
    return dict(id='sheet',path='sheet.png',sha256='c'*64,prompt_path='prompt.txt',prompt_sha256='d'*64,
                input_source_ids=['original'],generated=True,views=['front','side','rear','3/4'],use_status='ACCEPTED',
                permitted_uses=['coarse envelope'],forbidden_uses=['hidden facts'],claim_links=['body.exterior'],
                consistency_checks=[dict(criterion=k,result='PASS',observations='Reviewed specific view') for k in sorted(v.CRITERIA)])


class Pass0Test(unittest.TestCase):
    def test_source_only_without_generator_is_usable_and_not_mutated(self):
        p=fixture(); before=copy.deepcopy(p)
        self.assertEqual(v.validate(p),[])
        self.assertEqual(v.require_stage(p,'MACRO_BLOCKOUT',verify_files=False)['status'],'READY')
        self.assertEqual(p,before)

    def test_generated_and_report_evidence_cannot_confirm_original_geometry(self):
        for role in ['AUXILIARY_INPUT','REPORT']:
            p=fixture();p['sources'][1]['role']=role
            p['components'][0]['claims'][0]['evidence'][0]['source_id']='generated_input'
            self.assertTrue(any('CONFIRMED' in e for e in v.validate(p)))
        p=fixture();p['source_of_truth']=['generated_input']
        self.assertTrue(v.validate(p))

    def test_unsupported_inference_must_remain_speculative(self):
        p=fixture();c=p['components'][0]['claims'][0];c['certainty']='INFERRED';c['evidence']=[]
        self.assertTrue(v.validate(p))
        c['certainty']='SPECULATIVE';c['basis']='Unknown hidden shell; proxy only'
        self.assertEqual(v.validate(p),[])

    def test_blocking_unknown_and_conflict_cannot_advance(self):
        for entry in ['ambiguity','conflict']:
            p=fixture()
            if entry=='ambiguity': p['ambiguity_map']=[dict(id='A',component_ids=['body'],question='unknown rear?',severity='BLOCKING',decision='UNRESOLVED',allowed_action='stop rear work',basis='not visible')]
            else: p['contradictions']=[dict(id='C',source_ids=['original','generated_input'],property='count',description='counts conflict',severity='BLOCKING',status='OPEN',resolution='needs decision')]
            self.assertTrue(v.validate(p))
            p['gate'].update(status='BLOCKED',permitted_stage='NONE',limits=['needs source decision'])
            self.assertEqual(v.validate(p),[])
            with self.assertRaises(ValueError):v.require_stage(p,'MACRO_BLOCKOUT',verify_files=False)

    def test_nonblocking_deferred_region_requires_limited_gate(self):
        p=fixture();p['ambiguity_map']=[dict(id='A',component_ids=['body'],question='rear?',severity='NONBLOCKING',decision='DEFER',allowed_action='skip rear detail',basis='not visible')]
        self.assertTrue(v.validate(p));p['gate'].update(status='READY_WITH_LIMITS',limits=['skip rear'])
        self.assertEqual(v.validate(p),[])
        with self.assertRaises(ValueError):v.require_stage(p,'DETAIL_MODELING',verify_files=False)

    def test_auxiliary_count_failure_cannot_be_accepted(self):
        p=fixture();a=auxiliary();p['auxiliary_references']=[a];p['generation']['status']='COMPLETE'
        self.assertEqual(v.validate(p),[])
        next(c for c in a['consistency_checks'] if c['criterion']=='part_counts')['result']='FAIL'
        self.assertTrue(v.validate(p));a.update(use_status='RESTRICTED',permitted_uses=['front envelope only'],forbidden_uses=['part counts','rear'])
        p['gate'].update(status='READY_WITH_LIMITS',limits=['auxiliary count mismatch; source count wins'])
        self.assertEqual(v.validate(p),[])
        a['use_status']='REJECTED'
        self.assertTrue(v.validate(p));a['permitted_uses']=[]
        self.assertEqual(v.validate(p),[])

    def test_missing_lineage_review_claim_link_and_same_bytes_fail(self):
        for change in ['lineage','review','claim','hash']:
            p=fixture();a=auxiliary();p['auxiliary_references']=[a]
            if change=='lineage':a['input_source_ids']=['generated_input']
            elif change=='review':a['consistency_checks'].pop()
            elif change=='claim':a['claim_links']=['missing.claim']
            else:a['sha256']=p['sources'][0]['sha256']
            self.assertTrue(v.validate(p),change)

    def test_file_hash_verification_detects_source_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=fixture();root=Path(tmp)
            for s in p['sources']:
                s['path']=s['id']+'.png';(root/s['path']).write_bytes(s['id'].encode())
                s['sha256']=hashlib.sha256((root/s['path']).read_bytes()).hexdigest()
            self.assertEqual(v.validate(p,root,True),[])
            (root/p['sources'][0]['path']).write_bytes(b'changed')
            self.assertTrue(any('hash mismatch' in e for e in v.validate(p,root,True)))

    def test_duplicate_ids_ranges_unknown_evidence_and_invalid_values_fail(self):
        for change in ['id','range','source','certainty','finite','malformed']:
            p=fixture()
            if change=='id':p['components'].append(copy.deepcopy(p['components'][0]))
            elif change=='range':p['relative_dimensions'][0]['min']=.9
            elif change=='source':p['components'][0]['claims'][0]['evidence'][0]['source_id']='missing'
            elif change=='certainty':p['components'][0]['claims'][0]['certainty']='TRUE'
            elif change=='finite':p['relative_dimensions'][0]['max']=float('inf')
            else:p['components'][0]['claims'][0]['evidence']='bad'
            self.assertTrue(v.validate(p),change)

    def test_strict_json_duplicate_and_nan_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'packet.json'
            for text in ['{"a":1,"a":2}','{"a":NaN}']:
                path.write_text(text)
                with self.assertRaises(ValueError):v.load_packet(path)

    def test_relative_estimate_cannot_claim_another_unit(self):
        p=fixture();p['relative_dimensions'][0]['unit']='mm'
        self.assertTrue(v.validate(p))


class RegistrationTest(unittest.TestCase):
    def test_new_contract_cannot_be_removed_and_stage_routes_stay_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'central'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','.local','reports','__pycache__'))
            # Existing profile references Pulse/docs, not reports; route checks resolve inside copied root.
            profile=root/'.tooling/profile.json';data=json.loads(profile.read_text())
            data['contracts'].remove('.tooling/pass0-mechanics-contracts.json')
            profile.write_text(json.dumps(data))
            result=check.run(root,tools_root=root)
            self.assertTrue(any(r['rule']=='TOOLS-PASS0-CONTRACTS' and r['status']=='FAIL' for r in result.results),result.results)
            data['contracts'].append('.tooling/pass0-mechanics-contracts.json');profile.write_text(json.dumps(data))
            pipeline=root/'skills/blender-pipeline/SKILL.md'
            pipeline.write_text(pipeline.read_text().replace('../visual-reference-reconstruction/SKILL.md','references/core.md'))
            result=check.run(root,tools_root=root)
            self.assertTrue(any(r['rule']=='VRM-PIPELINE' and r['status']=='FAIL' for r in result.results),result.results)


class RoutingTest(unittest.TestCase):
    def test_cross_domain_image_modeling_starts_pass0(self):
        for task,owner in [
            ('Create a mech from the reference image.','blender-robot-mechanism-modeling'),
            ('Сделай меха по референсу.','blender-robot-mechanism-modeling'),
            ('Build a car from reference photos.','blender-vehicle-modeling'),
            ('Build a house from the image.','blender-architecture-environment'),
            ('Create a crate from reference images.','blender-props'),
            ('Create an anime character from an image.','blender-anime-character-modeling')]:
            self.assertEqual(mcp_runtime.route_task(task),['visual-reference-reconstruction',owner])
        self.assertEqual(mcp_runtime.route_task('Model a robot from images and create a material for it.'),
                         ['visual-reference-reconstruction','blender-robot-mechanism-modeling','blender-pipeline'])

    def test_mixed_geometry_and_wear_orders_geometry_before_surface(self):
        for task in ['Substantially revise the robot silhouette from images and add scratches.',
                     'Существенно переделай силуэт меха по референсу и добавь царапины.']:
            self.assertEqual(mcp_runtime.route_task(task),['visual-reference-reconstruction','blender-robot-mechanism-modeling','blender-posteffects-polishing'])

    def test_stage_only_and_read_only_do_not_restart_robot_or_pass0(self):
        cases={
            'Add scratches to the robot materials from the reference image.':['blender-posteffects-polishing'],
            'Create a rig for the robot.':['blender-rigging-skinning'],
            'Animate the robot piston.':['blender-animation'],
            'Анимируй поршень робота.':['blender-animation'],
            'Export the robot to GLB.':['blender-export-validation'],
            'Unwrap UVs on the mech.':['blender-pipeline'],
            'Review the robot silhouette against the reference image.':['verification'],
            'Do not rebuild the mech from images. Add scratches.':['blender-posteffects-polishing'],
            'Create a mech.':['blender-robot-mechanism-modeling'],
            'Analyze the vehicle reference images.':['visual-reference-reconstruction'],
            'Create a technical reference pack for a robot from images.':['visual-reference-reconstruction']}
        for task,owners in cases.items():self.assertEqual(mcp_runtime.route_task(task),owners,task)

    def test_complete_context_and_legacy_pointer_have_single_owner(self):
        result=mcp_runtime.context(ROOT,'Create a mech from the reference image.')
        self.assertTrue(result['ok'],result['error'])
        self.assertEqual(result['routing']['owners'],['visual-reference-reconstruction','blender-robot-mechanism-modeling'])
        paths=[d['path'] for d in result['documents']]
        self.assertEqual(len(paths),len(set(paths)))
        self.assertIn('skills/visual-reference-reconstruction/SKILL.md',paths)
        legacy=read_blender_skill.render(ROOT,'Blender_Reference_Reconstruction_SKILL')
        self.assertIn('SOURCE: skills/visual-reference-reconstruction/SKILL.md',legacy)


if __name__=='__main__':unittest.main()
