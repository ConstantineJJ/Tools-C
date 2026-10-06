"""Text brief provenance, identity drift and hard requirement selection gates."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from test_pass0_mechanics import fixture, auxiliary, v, ROOT
import mcp_runtime


def description_fixture():
    p=fixture();p.update(schema_version=2,mode='DESCRIPTION',object_class='mech')
    p['sources']=[dict(id='brief',path='brief.txt',sha256='a'*64,role='BRIEF',projection='text',authority_note='verbatim user text'),
                  dict(id='hero',path='hero.png',sha256='b'*64,role='CANONICAL_CONCEPT',projection='perspective',authority_note='selected designed concept')]
    p['source_of_truth']=['brief','hero']
    def claim(cid,value,certainty='CANONICAL'):
        return dict(id=cid,property=cid,value=value,certainty=certainty,basis='Adopted estimate' if certainty=='CANONICAL' else 'User clause',
                    evidence=[dict(source_id='hero' if certainty=='CANONICAL' else 'brief',region='body' if certainty=='CANONICAL' else 'clause 1',observation=str(value))])
    constraint=dict(claim('R.body',1,'REQUIRED'),target='count',component_id='body')
    p['constraints']=[constraint]
    p['components'][0]['claims']=[dict(claim('body.count',1,'REQUIRED'),requirement_ids=['R.body']),claim('body.shape','sphere')]
    p['relative_dimensions']=[dict(claim('body.width',[.3,.4]),component_id='body',axis='width',min=.3,max=.4,unit='H')]
    p['silhouette_notes']=[claim('outline','long-legged body')]
    p['design_brief']=dict(source_id='brief',intent='one scout',preferences=[],open_decisions=['hidden cooling'],strategy_reason='Single determined candidate')
    p['concept_candidates']=[dict(id='A',source_id='hero',generated=True,views=['hero'],input_source_ids=['brief'],prompt_path='concept.txt',prompt_sha256='c'*64,
        requirement_reviews=[dict(id='R.body',result='PASS',observations='One visible body')],
        quality_reviews=[dict(id=k,score=4,observations='Inspected '+k) for k in sorted(v._description.QUALITY)])]
    p['candidate_selection']=dict(strategy='SINGLE',selector='AGENT',actor='test',selected_candidate_id='A',reason='All requirements pass')
    p['identity_lock']=dict(status='LOCKED',version=1,source_id='hero',sha256='b'*64,
                            manifest_path='identity-lock.json',manifest_sha256='d'*64,manifest=v.identity_snapshot(p))
    return p


def pending_fixture():
    p=description_fixture();p['sources']=p['sources'][:1];p['source_of_truth']=['brief']
    for collection in [p['components'][0]['claims'],p['relative_dimensions'],p['silhouette_notes']]:
        for c in collection:
            if c['certainty']=='CANONICAL':c.update(certainty='SPECULATIVE',evidence=[],basis='No concept available')
    p['concept_candidates']=[];p['candidate_selection'].update(selector='PENDING',selected_candidate_id=None,reason='Generator unavailable')
    p['identity_lock']=dict(status='PENDING');p['gate'].update(status='BLOCKED',permitted_stage='NONE',limits=['No canonical image'])
    return p


class DescriptionTest(unittest.TestCase):
    def test_reference_v1_and_explicit_v2_remain_compatible(self):
        self.assertEqual(v.validate(fixture()),[])
        p=fixture();p.update(schema_version=2,mode='REFERENCE');self.assertEqual(v.validate(p),[])
        p.pop('mode');self.assertTrue(v.validate(p))

    def test_locked_description_consumes_common_stage_contract(self):
        p=description_fixture();self.assertEqual(v.validate(p),[])
        with self.assertRaisesRegex(ValueError, 'persistent contract'):
            v.require_stage(p,'MACRO_BLOCKOUT',verify_files=False)

    def test_modes_cannot_launder_fact_or_design_labels(self):
        for certainty in ['CONFIRMED','INFERRED']:
            p=description_fixture();p['components'][0]['claims'][1]['certainty']=certainty;self.assertTrue(v.validate(p))
        p=fixture();p['components'][0]['claims'][0]['certainty']='CANONICAL';self.assertTrue(v.validate(p))
        p=description_fixture();p['schema_version']=1;self.assertTrue(v.validate(p))

    def test_required_cannot_come_from_concept_and_canonical_cannot_come_from_auxiliary(self):
        p=description_fixture();p['constraints'][0]['evidence'][0]['source_id']='hero';self.assertTrue(v.validate(p))
        p=description_fixture();p['sources'][1]['role']='AUXILIARY_INPUT';self.assertTrue(v.validate(p))

    def test_required_count_and_geometry_links_cannot_disappear_even_after_resnapshot(self):
        p=description_fixture();p['components'][0]['count']=2;p['identity_lock']['manifest']=v.identity_snapshot(p)
        self.assertTrue(any('REQUIRED' in e for e in v.validate(p)))
        p=description_fixture();p['components'][0]['claims'][0]['requirement_ids']=[];p['identity_lock']['manifest']=v.identity_snapshot(p)
        self.assertTrue(v.validate(p))

    def test_drift_in_count_shape_dimensions_and_pose_requires_relock(self):
        for kind in ['count','shape','range','pose','constraint']:
            p=description_fixture()
            if kind=='count':p['components'][0]['count']=2
            elif kind=='shape':p['components'][0]['claims'][1]['value']='box'
            elif kind=='range':p['relative_dimensions'][0]['max']=.5
            elif kind=='pose':p['proportion_basis']['pose']='crouch'
            else:p['constraints'][0]['value']=2
            self.assertTrue(any('drift' in e for e in v.validate(p)),kind)

    def test_high_quality_scores_cannot_override_failed_or_unknown_requirement(self):
        for result in ['FAIL','UNKNOWN']:
            p=description_fixture();p['concept_candidates'][0]['requirement_reviews'][0]['result']=result
            for r in p['concept_candidates'][0]['quality_reviews']:r['score']=5
            self.assertTrue(any('Cannot lock' in e for e in v.validate(p)))

    def test_exploration_keeps_losing_concept_out_of_authority(self):
        p=description_fixture();b=copy.deepcopy(p['concept_candidates'][0]);b.update(id='B',source_id='loser')
        b['requirement_reviews'][0]['result']='FAIL'
        p['sources'].append(dict(p['sources'][1],id='loser',role='CONCEPT_CANDIDATE',sha256='e'*64,path='loser.png'))
        p['concept_candidates'].append(b);p['candidate_selection']['strategy']='EXPLORE'
        self.assertEqual(v.validate(p),[])
        p['source_of_truth'].append('loser');self.assertTrue(v.validate(p))

    def test_three_candidate_choice_rejects_high_scoring_violation(self):
        p=description_fixture();p['candidate_selection']['strategy']='EXPLORE'
        for name,result,score in [('B','FAIL',5),('C','PASS',3)]:
            c=copy.deepcopy(p['concept_candidates'][0]);c.update(id=name,source_id=name)
            c['requirement_reviews'][0]['result']=result
            for r in c['quality_reviews']:r['score']=score
            p['concept_candidates'].append(c)
            p['sources'].append(dict(p['sources'][1],id=name,role='CONCEPT_CANDIDATE',sha256=('e' if name=='B' else 'f')*64,path=name+'.png'))
        self.assertEqual(v.validate(p),[])
        p['candidate_selection']['selected_candidate_id']='B';self.assertTrue(v.validate(p))

    def test_required_shape_stays_required_and_attached_to_its_component(self):
        p=description_fixture();c=p['components'][0]['claims'][0]
        p['constraints'][0].update(target='claim',target_claim_ids=[c['id']])
        p['identity_lock']['manifest']=v.identity_snapshot(p);self.assertEqual(v.validate(p),[])
        c.update(certainty='CANONICAL',evidence=[dict(source_id='hero',region='body',observation='one body')])
        p['identity_lock']['manifest']=v.identity_snapshot(p);self.assertTrue(v.validate(p))

    def test_pending_interactive_choice_does_not_generate_views_or_start_modeling(self):
        p=pending_fixture();p['candidate_selection']['reason']='Waiting for user to choose an eligible candidate'
        a=auxiliary();a['input_source_ids']=['brief'];p['auxiliary_references']=[a]
        self.assertTrue(any('before Identity Lock' in e for e in v.validate(p)))

    def test_missing_review_and_unreviewed_user_choice_fail(self):
        p=description_fixture();p['concept_candidates'][0]['quality_reviews'].pop();self.assertTrue(v.validate(p))
        p=description_fixture();p['candidate_selection'].update(selector='USER',selected_candidate_id='unknown');self.assertTrue(v.validate(p))

    def test_auxiliary_must_use_frozen_hero_and_current_lock(self):
        p=description_fixture();a=auxiliary();a.update(input_source_ids=['hero'],lock_version=1,canonical_sha256='b'*64,claim_links=['body.shape'])
        p['auxiliary_references']=[a];p['generation']['status']='COMPLETE';self.assertEqual(v.validate(p),[])
        for key,value in [('input_source_ids',['brief']),('lock_version',2),('canonical_sha256','a'*64)]:
            bad=copy.deepcopy(p);bad['auxiliary_references'][0][key]=value;self.assertTrue(v.validate(bad),key)

    def test_unavailable_or_pending_selection_blocks_scene_stage(self):
        p=pending_fixture();self.assertEqual(v.validate(p),[])
        with self.assertRaises(ValueError):v.require_stage(p,'MACRO_BLOCKOUT',verify_files=False)
        p['gate'].update(status='READY',permitted_stage='MACRO_BLOCKOUT',limits=[]);self.assertTrue(v.validate(p))

    def test_revision_keeps_predecessor_and_invalidates_old_views(self):
        p=description_fixture();p['identity_lock']['version']=2;self.assertTrue(v.validate(p))
        p['identity_lock'].update(revision_reason='User changed design',supersedes_packet_id='previous',supersedes_sha256='f'*64)
        self.assertEqual(v.validate(p),[])
        a=auxiliary();a.update(input_source_ids=['hero'],lock_version=1,canonical_sha256='b'*64,claim_links=['body.shape'])
        p['auxiliary_references']=[a];self.assertTrue(any('current frozen' in e for e in v.validate(p)))

    def test_frozen_image_brief_prompt_and_manifest_bytes_are_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=description_fixture()
            for s in p['sources']:
                (root/s['path']).write_bytes(s['id'].encode());s['sha256']=hashlib.sha256((root/s['path']).read_bytes()).hexdigest()
            c=p['concept_candidates'][0];(root/c['prompt_path']).write_bytes(b'concept prompt');c['prompt_sha256']=hashlib.sha256(b'concept prompt').hexdigest()
            lock=p['identity_lock'];lock['sha256']=p['sources'][1]['sha256'];path=root/lock['manifest_path']
            path.write_text(json.dumps(lock['manifest']),encoding='utf-8');lock['manifest_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(v.validate(p,root,True),[])
            for path in [root/'hero.png',root/'brief.txt',root/'concept.txt',root/'identity-lock.json']:
                old=path.read_bytes();path.write_bytes(b'changed');self.assertTrue(v.validate(p,root,True),path.name);path.write_bytes(old)

    def test_text_design_routes_before_domain_but_stages_and_qa_stay_scoped(self):
        for task,owner in [('Create a mech from text description.','blender-robot-mechanism-modeling'),
                           ('Создай лёгкого разведывательного меха с двумя пушками и длинными ногами.','blender-robot-mechanism-modeling'),
                           ('Create a car from a text-only design brief.','blender-vehicle-modeling'),
                           ('Создай дом по описанию.','blender-architecture-environment')]:
            self.assertEqual(mcp_runtime.route_task(task),['visual-reference-reconstruction',owner])
        for task,owners in [('Create visual concept candidates from a text brief.',['visual-reference-reconstruction']),
                             ('Create a rig for the described mech.',['blender-rigging-skinning']),
                             ('Create a material for the robot from its text description.',['blender-pipeline']),
                             ('Review the described mech without edits.',['verification']),
                             ('Do not create a robot. Add scratches.',['blender-posteffects-polishing'])]:
            self.assertEqual(mcp_runtime.route_task(task),owners,task)


if __name__=='__main__':unittest.main()
