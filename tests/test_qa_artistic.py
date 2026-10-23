"""Dual review decisions/transitions, not artistic-quality assertions."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_qa_freshness import artifact, png, snapshot
from test_qa_gate import fixture as legacy, check
from test_model_contract import contract_fixture, m
import qa_artistic as art
import qa_gate as qa
import mcp_runtime


def fixture(root, *, mode='SELF_REVIEW', asset_type='CHARACTER'):
    packet = legacy(changed=False)
    packet['protected_zones'] = [dict(id='legs', **check('legs'))]
    packet['user_flags'] = []
    for image in packet['captures']:
        image['image'] = artifact(root,image['image']['path'],png())
    pass0 = contract_fixture()
    source = artifact(root,'source.png',png())
    predecessor = copy.deepcopy(pass0)
    previous = pass0['model_contract']['sha256']
    pass0['sources'][0].update(source)
    pass0['model_contract'].update(revision=2,supersedes_sha256=previous,change_note='Bind fixture to actual test PNG bytes')
    m.seal(pass0, previous=predecessor)
    contract = artifact(root,'pass0.json',json.dumps(pass0).encode())
    state = snapshot(root,'snapshot.json')
    bindings = [dict(id=x['id'], capture_series='QA-1', captured_at='2026-10-08T10:00:00Z', state='r12',
                     dependencies={r:[] for r in state['regions']}) for x in packet['captures']]
    dual = dict(version=1, freshness=dict(states={'r12':state}, current='r12', captures=bindings),
                technical_checks=['protected_state'],
                brief=dict(complexity='SIMPLE',stage='FINAL',asset_type=asset_type,scope='FULL',
                           requirements={r:dict(views=list(art.VIEWS),criterion='reference likeness') for r in state['regions']},
                           contract=dict(artifact=contract,ref=m.reference(pass0)),references={'original':source},
                           protected=['legs'],constraints=['Preserve approved stylization'],implementer='builder'),
                artistic=None,checkpoint=dict(artifact=None,issues=[],accepted={},protected=['legs'],failed_methods=[],gates={}),
                corrections=[], user_decision='PENDING')
    packet['dual_verification'] = dual
    attach_review(packet,root,mode=mode)
    return packet


def attach_review(packet, root, *, mode='SELF_REVIEW'):
    dual = packet['dual_verification']
    dual['artistic'] = None
    result = art.evaluate(dual,packet,root=root,verify_artifact=qa.verify_artifact)
    reviewer = 'builder' if mode=='SELF_REVIEW' else 'critic-1'
    dispatch = None
    if mode=='INDEPENDENT':
        dispatch = artifact(root,'dispatch.json',json.dumps(dict(implementer='builder',critic=reviewer,
                dispatch_id='test-dispatch-not-real-art-review',packet_sha256=result['packet_sha256'],blind=True)).encode())
    dual['artistic'] = dict(stage=dual['brief']['stage'],verdict='ACCEPTED',mode=mode,reviewer=reviewer,
                packet_sha256=result['packet_sha256'],dispatch=dispatch,
                inspected=[x['id'] for x in packet['captures']],issues=[],delta=[],preserve=['legs'],
                leave_as_is=['face'],do_not_change=['legs'],next=[],observations='Synthetic test declaration: no significant issues')


def issue(*, region='hair', kind='FORM', evidence=None):
    return dict(id='hair-form',priority='P1',what='Visible form differs',where=region,why='Canonical outline differs',
                evidence=evidence or ['front_AFTER','side_AFTER'],reference='original',fix='Bounded outline correction',
                kind=kind,visibility='VISIBLE',impact='MEDIUM',fix_cost='LOW',regression_risk='MEDIUM',
                rationale='Local change; adjacent accepted surfaces must be preserved')


class DualReviewTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.packet = fixture(self.root)
        self.dual = self.packet['dual_verification']

    def evaluate(self):
        return qa.validate(self.packet,root=self.root,mode='ARTISTIC_REVIEW')

    def revise(self, defect=None):
        self.dual['artistic'].update(verdict='REVISION_REQUIRED',issues=[defect or issue()])

    def rebind(self):
        review=copy.deepcopy(self.dual['artistic'])
        attach_review(self.packet,self.root)
        review['packet_sha256']=self.dual['artistic']['packet_sha256']
        self.dual['artistic']=review

    def history(self, *, issues=False, accepted=()):
        previous=copy.deepcopy(self.packet)
        previous['dual_verification']['checkpoint']=dict(artifact=None,issues=[],accepted={},protected=['legs'],failed_methods=[],gates={})
        previous['dual_verification']['corrections']=[]
        for image in previous['captures']:
            image['image']=artifact(self.root,'previous/'+image['id']+'.png',png(b'\0\0\xff\xff'))
        attach_review(previous,self.root)
        review=previous['dual_verification']['artistic']
        review.update(preserve=list(accepted),leave_as_is=[])
        if issues:
            review.update(verdict='REVISION_REQUIRED',issues=[issue()])
        ref=artifact(self.root,'previous_receipt.json',json.dumps(previous).encode())
        self.dual['checkpoint']=art.checkpoint_from_receipt(previous,ref,root=self.root,verify_artifact=qa.verify_artifact)
        self.rebind()
        return previous

    def corrections(self, outcomes=('UNRESOLVED','UNRESOLVED'), methods=None):
        checkpoint = artifact(self.root,'checkpoint.blend',b'BLENDER synthetic checkpoint; not engine proof')
        ids=[]
        for i in range(1,len(outcomes)+1):
            image=copy.deepcopy(self.packet['captures'][0]);image.pop('view')
            image.update(id='pass-'+str(i),region='hair',image=artifact(self.root,'pass-'+str(i)+'.png',png(bytes([i,0,0,255]))))
            self.packet['closeups'].append(image);ids.append(image['id'])
            self.dual['freshness']['captures'].append(dict(id=image['id'],capture_series='QA-1',captured_at='2026-10-08T10:00:00Z',state='r12',dependencies={'hair':[]}))
        self.dual['corrections'] = [dict(**{'pass':i},method=(methods or ['same']*len(outcomes))[i-1],
                                        outcomes={'hair-form':outcome},checkpoint=checkpoint,evidence=[ids[i-1]])
                                    for i,outcome in enumerate(outcomes,1)]
        self.rebind()

    def test_technical_pass_artistic_revision_blocks_acceptance(self):
        self.revise()
        result = self.evaluate()
        self.assertEqual(result['dual_verification']['TECHNICAL_QA'],'PASS')
        self.assertEqual(result['dual_verification']['ARTISTIC_REVIEW'],'REVISION_REQUIRED')
        self.assertEqual(result['gate'],'FAIL')

    def test_artistic_accepted_technical_failure_remains_failure(self):
        self.packet['checks']['protected_state']['status']='FAIL'
        result = self.evaluate()
        self.assertEqual(result['dual_verification']['ARTISTIC_REVIEW'],'ACCEPTED')
        self.assertEqual(result['dual_verification']['TECHNICAL_QA'],'FAIL')
        self.assertEqual(result['gate'],'FAIL')

    def test_zero_issues_can_finish(self):
        self.assertEqual(self.evaluate()['gate'],'PASS')
        self.assertEqual(self.evaluate()['dual_verification']['next'],'FINISH')

    def test_adaptive_gates(self):
        self.assertEqual(art.gates('SIMPLE'),('FINAL',))
        self.assertEqual(art.gates('STANDARD'),('PRIMARY_FORMS','FINAL'))
        self.assertEqual(art.gates('COMPLEX'),('PRIMARY_FORMS','CRITICAL_FEATURES','FINAL'))
        self.assertEqual(art.gates('COMPLEX',local=True),('LOCAL',))

    def test_missing_earlier_gate_not_auto_accepted(self):
        self.dual['brief']['complexity']='COMPLEX'
        attach_review(self.packet,self.root)
        result=self.evaluate()['dual_verification']
        self.assertEqual(result['artistic_gate'],'OPEN')
        self.assertEqual(result['missing_gates'],['PRIMARY_FORMS','CRITICAL_FEATURES'])

    def test_contract_cannot_change(self):
        self.dual['brief']['contract']['ref']['revision']=3
        with self.assertRaisesRegex(ValueError,'cannot revise'):
            self.evaluate()

    def test_no_model_or_contract_mutation(self):
        before=copy.deepcopy(self.packet)
        files={p.name:p.read_bytes() for p in self.root.iterdir() if p.is_file()}
        self.evaluate()
        self.assertEqual(self.packet,before)
        self.assertEqual(files,{p.name:p.read_bytes() for p in self.root.iterdir() if p.is_file()})

    def test_protected_zone_cannot_disappear(self):
        self.dual['brief']['protected']=[]
        with self.assertRaisesRegex(ValueError,'protected zones/user locks'):
            self.evaluate()

    def test_critic_cannot_drop_do_not_change(self):
        self.dual['artistic']['do_not_change']=[]
        with self.assertRaisesRegex(ValueError,'retain protected'):
            self.evaluate()

    def test_protected_defect_escalates_no_correction(self):
        self.revise(issue(region='legs'))
        self.assertEqual(self.evaluate()['dual_verification']['next'],'ESCALATE')

    def test_insufficient_inspected_views_reuse_existing_captures(self):
        self.dual['artistic']['inspected']=['front_AFTER']
        result=self.evaluate()['dual_verification']
        self.assertEqual(result['artistic_gate'],'OPEN')
        self.assertEqual(result['next'],'INSPECT_EXISTING')
        self.assertTrue(all(x['action']=='INSPECT_EXISTING' for x in result['requests']))

    def test_stale_region_never_satisfies_acceptance(self):
        self.dual['freshness']['states']['r12']['verified']=False
        attach_review(self.packet,self.root)
        self.assertEqual(self.evaluate()['dual_verification']['next'],'REQUEST_CAPTURE')

    def test_45_degree_cannot_establish_proportions(self):
        self.revise(issue(kind='PROPORTION',evidence=['high_45_AFTER','low_45_AFTER']))
        with self.assertRaisesRegex(ValueError,'cannot establish proportions'):
            self.evaluate()

    def test_orthographic_confirmation_allows_proportion_defect(self):
        self.revise(issue(kind='PROPORTION'))
        self.assertEqual(self.evaluate()['dual_verification']['next'],'CORRECT')

    def test_occluded_not_missing(self):
        defect=issue(kind='MISSING');defect['visibility']='OCCLUDED';self.revise(defect)
        with self.assertRaisesRegex(ValueError,'occluded does not mean absent'):
            self.evaluate()

    def test_self_review_is_explicit(self):
        self.assertEqual(self.evaluate()['dual_verification']['independence'],'SELF_REVIEW')

    def test_independent_dispatch_bound_to_blind_packet(self):
        attach_review(self.packet,self.root,mode='INDEPENDENT')
        self.assertEqual(self.evaluate()['dual_verification']['independence'],'INDEPENDENT_DECLARED')

    def test_false_independence_same_agent_rejected(self):
        attach_review(self.packet,self.root,mode='INDEPENDENT')
        self.dual['artistic']['reviewer']='builder'
        with self.assertRaisesRegex(ValueError,'different dispatched agent'):
            self.evaluate()

    def test_different_name_without_dispatch_not_independent(self):
        self.dual['artistic'].update(mode='INDEPENDENT',reviewer='other')
        with self.assertRaisesRegex(ValueError,'different dispatched agent'):
            self.evaluate()

    def test_nonblind_dispatch_rejected(self):
        attach_review(self.packet,self.root,mode='INDEPENDENT')
        row=json.loads((self.root/'dispatch.json').read_text());row['blind']=False
        self.dual['artistic']['dispatch']=artifact(self.root,'dispatch.json',json.dumps(row).encode())
        with self.assertRaisesRegex(ValueError,'nonblind'):
            self.evaluate()

    def test_accepted_region_needs_new_evidence(self):
        previous=self.history(accepted=['hair'])
        for image,old in zip(self.packet['captures'],previous['captures']):
            image['image']=old['image']
        self.rebind()
        self.revise()
        with self.assertRaisesRegex(ValueError,'without new evidence'):
            self.evaluate()

    def test_new_regression_in_accepted_region_tracked(self):
        self.history(accepted=['hair'])
        self.revise()
        self.dual['artistic']['delta']=[dict(id='hair-form',status='NEW_REGRESSION',evidence=['front_AFTER'])]
        result=self.evaluate()['dual_verification']
        self.assertEqual(result['delta'][0]['status'],'NEW_REGRESSION')
        self.assertEqual(result['next'],'CORRECT')

    def test_previous_issue_cannot_disappear(self):
        self.history(issues=True)
        with self.assertRaisesRegex(ValueError,'silently disappear'):
            self.evaluate()

    def test_resolved_delta_uses_new_evidence(self):
        self.history(issues=True)
        self.dual['artistic']['delta']=[dict(id='hair-form',status='RESOLVED',evidence=['front_AFTER'])]
        self.assertEqual(self.evaluate()['dual_verification']['next'],'FINISH')

    def test_two_failed_corrections_reconsider_method(self):
        self.revise();self.corrections()
        self.assertEqual(self.evaluate()['dual_verification']['next'],'RECONSIDER_METHOD')

    def test_third_same_method_failure_rejected(self):
        self.revise();self.corrections(('UNRESOLVED',)*3)
        with self.assertRaisesRegex(ValueError,'same method repeated'):
            self.evaluate()

    def test_three_passes_never_auto_pass(self):
        self.revise();self.corrections(('UNRESOLVED',)*3,methods=['first','first','different'])
        result=self.evaluate()
        self.assertEqual(result['gate'],'FAIL')
        self.assertEqual(result['dual_verification']['next'],'ESCALATE')

    def test_improvement_can_justify_next_pass(self):
        self.history(issues=True);self.revise();self.corrections(('IMPROVED','IMPROVED'))
        self.dual['artistic']['delta']=[dict(id='hair-form',status='IMPROVED',evidence=['front_AFTER'])]
        self.assertEqual(self.evaluate()['dual_verification']['next'],'CORRECT')

    def test_minor_differences_need_user_choice(self):
        defect=issue();defect.update(priority='P2',impact='LOW')
        self.dual['artistic'].update(verdict='ACCEPTED_WITH_MINOR_DIFFERENCES',issues=[defect])
        self.assertEqual(self.evaluate()['dual_verification']['next'],'USER_DECISION')
        self.assertEqual(self.evaluate()['gate'],'OPEN')
        self.dual['user_decision']='FINISH'
        self.assertEqual(self.evaluate()['gate'],'PASS')

    def test_minor_verdict_cannot_hide_major_issue(self):
        self.revise();self.dual['artistic']['verdict']='ACCEPTED_WITH_MINOR_DIFFERENCES'
        with self.assertRaisesRegex(ValueError,'major deviation'):
            self.evaluate()

    def test_blind_packet_excludes_implementer_assessment(self):
        self.packet['checks']['protected_state']['observations']='SECRET_BUILDER_OPINION'
        result=art.evaluate(self.dual,self.packet,root=self.root,verify_artifact=qa.verify_artifact)
        self.assertNotIn('SECRET_BUILDER_OPINION',json.dumps(result['critic_packet']))
        self.assertNotIn('reviewer',result['critic_packet']['captures'][0])
        self.assertNotIn('observations',result['critic_packet']['captures'][0])

    def test_no_cherry_picked_standard_views(self):
        for requirement in self.dual['brief']['requirements'].values():
            requirement['views']=['front']
        with self.assertRaisesRegex(ValueError,'cherry-picked'):
            self.evaluate()

    def test_vehicle_environment_and_other_use_same_review(self):
        for asset_type in ('VEHICLE','ENVIRONMENT','OTHER'):
            self.packet=fixture(self.root,asset_type=asset_type)
            self.packet['profile']='ASSET_FINAL'
            self.assertEqual(qa.validate(self.packet,root=self.root)['gate'],'PASS')

    def test_old_receipt_unchanged_and_art_mode_requires_extension(self):
        packet=legacy()
        self.assertEqual(qa.validate(packet)['gate'],'PASS')
        self.assertNotIn('dual_verification',qa.validate(packet))
        with self.assertRaisesRegex(ValueError,'requires dual'):
            qa.validate(packet,mode='ARTISTIC_REVIEW')

    def test_missing_files_never_dual_pass(self):
        result=qa.validate(self.packet)
        self.assertEqual(result['gate'],'OPEN')
        self.assertEqual(result['dual_verification']['next'],'VERIFY_FILES')

    def test_cli_emits_bound_blind_packet(self):
        path=self.root/'qa_receipt.json';path.write_text(json.dumps(self.packet),encoding='utf-8')
        result=subprocess.run([sys.executable,str(Path(qa.__file__)),str(path),'--verify-files','--critic-packet'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        packet=json.loads(result.stdout)
        self.assertEqual(packet['packet_sha256'],self.dual['artistic']['packet_sha256'])
        self.assertNotIn('artistic',packet['packet'])

    def test_minor_polish_still_reconsiders_two_failed_methods(self):
        self.revise();self.corrections()
        self.dual['artistic']['verdict']='ACCEPTED_WITH_MINOR_DIFFERENCES'
        self.dual['artistic']['issues'][0].update(priority='P2',impact='LOW')
        self.dual['user_decision']='POLISH'
        self.assertEqual(self.evaluate()['dual_verification']['next'],'RECONSIDER_METHOD')

    def test_accepted_regions_reach_blind_packet_and_preservation_plan(self):
        self.history(accepted=['face'])
        self.assertIn('face',art.evaluate(self.dual,self.packet,root=self.root,verify_artifact=qa.verify_artifact)['critic_packet']['accepted'])
        self.dual['artistic']['leave_as_is']=[]
        with self.assertRaisesRegex(ValueError,'silently dropped'):
            self.evaluate()

    def test_checkpoint_inline_state_cannot_hide_prior_defect(self):
        self.history(issues=True)
        self.dual['checkpoint']['issues']=[]
        with self.assertRaisesRegex(ValueError,'differs from preceding'):
            self.evaluate()

    def test_unbound_prior_memory_never_passes(self):
        self.dual['checkpoint']['accepted']={'face':['a'*64]}
        with self.assertRaisesRegex(ValueError,'requires its existing QA receipt'):
            self.evaluate()

    def test_correction_wrong_region_does_not_reset_failure_count(self):
        self.history(issues=True);self.revise();self.corrections(('IMPROVED',))
        self.dual['freshness']['captures'][-1]['dependencies']={'torso':[]}
        self.rebind()
        self.dual['artistic']['delta']=[dict(id='hair-form',status='IMPROVED',evidence=['front_AFTER'])]
        with self.assertRaisesRegex(ValueError,'evidence of each affected region'):
            self.evaluate()

    def test_unrelated_new_pixels_do_not_prove_hair_improved(self):
        previous=self.history(issues=True);self.revise();self.corrections(('IMPROVED',))
        self.dual['freshness']['captures'][-1]['dependencies']={'torso':[]}
        self.packet['captures'][0]['image']=previous['captures'][0]['image']
        self.dual['corrections'][0]['evidence'].append('front_AFTER')
        self.rebind()
        self.dual['artistic']['delta']=[dict(id='hair-form',status='IMPROVED',evidence=['side_AFTER'])]
        with self.assertRaisesRegex(ValueError,'new region evidence'):
            self.evaluate()

    def test_latest_improvement_requires_agreeing_critic_delta(self):
        self.history(issues=True);self.revise();self.corrections(('IMPROVED',))
        self.dual['artistic']['delta']=[dict(id='hair-form',status='UNRESOLVED',evidence=['front_AFTER'])]
        with self.assertRaisesRegex(ValueError,'matching critic delta'):
            self.evaluate()

    def test_resolved_correction_survives_next_receipt(self):
        self.history(issues=True);self.corrections(('RESOLVED',))
        self.dual['artistic']['delta']=[dict(id='hair-form',status='RESOLVED',evidence=['front_AFTER'])]
        self.assertEqual(self.evaluate()['gate'],'PASS')
        previous=copy.deepcopy(self.packet)
        ref=artifact(self.root,'resolved_receipt.json',json.dumps(previous).encode())
        self.dual['checkpoint']=art.checkpoint_from_receipt(previous,ref,root=self.root,verify_artifact=qa.verify_artifact)
        self.dual['artistic']['delta']=[]
        self.rebind()
        self.assertEqual(self.evaluate()['gate'],'PASS')
        # Attempts remain pinned even after resolution.
        self.dual['corrections']=[]
        with self.assertRaisesRegex(ValueError,'cannot be removed'):
            self.evaluate()

    def test_prior_failed_method_cannot_be_reused_after_handoff(self):
        self.revise();self.corrections()
        self.assertEqual(self.evaluate()['dual_verification']['next'],'RECONSIDER_METHOD')
        previous=copy.deepcopy(self.packet)
        ref=artifact(self.root,'failed_receipt.json',json.dumps(previous).encode())
        self.dual['checkpoint']=art.checkpoint_from_receipt(previous,ref,root=self.root,verify_artifact=qa.verify_artifact)
        self.dual['corrections'].append(dict(self.dual['corrections'][-1],**{'pass':3}))
        with self.assertRaisesRegex(ValueError,'known failed method'):
            self.evaluate()

    def test_primary_and_critical_gates_run_without_all_three(self):
        for stage,complexity in [('PRIMARY_FORMS','STANDARD'),('CRITICAL_FEATURES','COMPLEX')]:
            self.packet=fixture(self.root);self.dual=self.packet['dual_verification']
            self.dual['brief'].update(stage=stage,complexity=complexity)
            attach_review(self.packet,self.root)
            result=self.evaluate()['dual_verification']
            self.assertEqual(result['artistic_gate'],'PASS' if stage=='PRIMARY_FORMS' else 'OPEN')

    def test_local_review_only_changed_and_affected_regions(self):
        self.dual['brief'].update(scope='LOCAL',stage='LOCAL',complexity='COMPLEX',
                    requirements={'hair':dict(views=['front','side'],criterion='hair silhouette')})
        attach_review(self.packet,self.root)
        self.assertEqual(self.evaluate()['dual_verification']['artistic_gate'],'PASS')

    def test_open_primary_gate_cannot_be_promoted_by_checkpoint(self):
        self.dual['brief'].update(stage='PRIMARY_FORMS',complexity='STANDARD')
        attach_review(self.packet,self.root)
        self.dual['artistic']['inspected']=['front_AFTER']
        self.assertEqual(self.evaluate()['dual_verification']['artistic_gate'],'OPEN')
        previous=copy.deepcopy(self.packet)
        ref=artifact(self.root,'open_primary.json',json.dumps(previous).encode())
        self.dual['checkpoint']=art.checkpoint_from_receipt(previous,ref,root=self.root,verify_artifact=qa.verify_artifact)
        self.assertNotIn('PRIMARY_FORMS',self.dual['checkpoint']['gates'])
        self.dual['brief']['stage']='FINAL'
        attach_review(self.packet,self.root)
        self.assertEqual(self.evaluate()['dual_verification']['next'],'REVIEW_MISSING_GATES')

    def test_completed_primary_gate_allows_standard_final(self):
        self.dual['brief'].update(stage='PRIMARY_FORMS',complexity='STANDARD')
        attach_review(self.packet,self.root)
        previous=copy.deepcopy(self.packet)
        ref=artifact(self.root,'accepted_primary.json',json.dumps(previous).encode())
        self.dual['checkpoint']=art.checkpoint_from_receipt(previous,ref,root=self.root,verify_artifact=qa.verify_artifact)
        self.dual['brief']['stage']='FINAL'
        attach_review(self.packet,self.root)
        self.assertEqual(self.evaluate()['gate'],'PASS')

    def test_artistic_mode_routes_read_only_and_delivers_whole_protocol(self):
        root=Path(__file__).resolve().parents[1]
        for task in ('ARTISTIC_REVIEW character face and hair', 'Художественная проверка автомобиля'):
            result=mcp_runtime.context(root,task,max_chars=200000)
            self.assertTrue(result['ok'])
            self.assertEqual(result['routing']['owners'],['verification'])
            self.assertEqual(result['verification_mode'],'ARTISTIC_REVIEW')
            self.assertIn(mcp_runtime.DUAL_REVIEW,[r['path'] for r in result['documents'] if r['status']!='pending'])
            self.assertTrue(result['review_requirements'])


if __name__=='__main__':
    unittest.main()
