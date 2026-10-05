"""Design drift, incomplete views, stale state and meaningful checkpoint behavior."""
import copy
import unittest
from test_pass0_mechanics import fixture, auxiliary, v
from test_pass0_description import description_fixture, pending_fixture

m = v.model_contract
ALL = sorted(m.CHECKPOINTS)


def rule(rid, kind, target, level="HARD INVARIANT", **extra):
    return dict(id=rid, kind=kind, target_id=target, level=level, checkpoints=ALL,
                basis="Reviewed original/hero geometry; explicit task tolerance", **extra)


def contract_fixture(description=False):
    p = description_fixture() if description else fixture()
    p.update(schema_version=3, mode="DESCRIPTION" if description else "REFERENCE")
    if description:
        for k in ["manifest", "manifest_path", "manifest_sha256"]: p["identity_lock"].pop(k)
    body = p["components"][0]
    body.update(parent_id=None, symmetry=dict(type="BILATERAL", axis="X"))
    gun = copy.deepcopy(body); gun.update(id="guns", label="guns", count=2, parent_id="body")
    gun["claims"] = [dict(copy.deepcopy(body["claims"][-1]), id="gun.form", value="two barrels")]
    p["components"].append(gun)
    d = dict(copy.deepcopy(p["relative_dimensions"][0]), id="gun.length", component_id="guns", min=.18, max=.26, value=[.18, .26])
    p["relative_dimensions"].append(d)
    anchor = dict(copy.deepcopy(body["claims"][-1]), id="anchor.gun", value=[-.2, .7], critical=True)
    p["silhouette_notes"].append(anchor)
    relation = dict(copy.deepcopy(body["claims"][-1]), id="mount", from_component="guns", to_component="body", relationship="side mounts", value="bilateral", critical=True)
    p["relationships"] = [relation]
    rules = [rule("n.body", "count", "body"), rule("n.guns", "count", "guns"),
             rule("p.body", "dimension", "body.width", "PROPORTION LOCK", unit="H"),
             rule("p.gun", "dimension", "gun.length", "PROPORTION LOCK", unit="H",
                  view_completeness=dict(required=True, source_ids=["hero" if description else "original"], basis="Complete barrel visible")),
             rule("ratio.gun", "ratio", "unused", "PROPORTION LOCK", unit="ratio", numerator_id="gun.length", denominator_id="body.width", bounds=[.5, .7]),
             rule("anchor", "anchor", "anchor.gun", "PROPORTION LOCK", unit="H", tolerance=.02),
             rule("mount", "relationship", "mount"), rule("parent", "hierarchy", "guns"), rule("symmetry", "symmetry", "guns"),
             rule("detail", "claim", "gun.form", "SOFT CANONICAL")]
    if description:
        rules += [rule("required.count", "claim", "body.count")]
    p["model_contract"] = dict(schema_version=1, id="test-design", status="LOCKED", revision=1, reviewer="test", reason="Reviewed constraints", rules=rules)
    m.seal(p)
    return p


def observations(p, checkpoint="MACRO"):
    rows = []
    for r in p["model_contract"]["rules"]:
        if checkpoint not in r["checkpoints"]: continue
        value = copy.deepcopy(m.expected(p, r))
        if r["kind"] in {"dimension", "ratio"}: value = sum(value)/2
        rows.append(dict(rule_id=r["id"], state="MEASURED", value=value, unit=r.get("unit"), completeness="FULL",
                         method="comparable neutral pose measurement / explicit visual review", evidence="test-artifact"))
        if r['kind']=='dimension' and r['target_id']=='gun.length' or r['kind']=='ratio':
            rows[-1]['instance_values']={'guns.L':value,'guns.R':value}
    return rows


def assembly(p):
    return dict(contract_ref=m.reference(p),
                parts=[dict(part_id="body.mesh", object_name="Body", component_id="body", instance_id="body.0", parent_id=None),
                       dict(part_id="gunL.mesh", object_name="GunL", component_id="guns", instance_id="guns.L", parent_id="body.mesh"),
                       dict(part_id="gunR.mesh", object_name="GunR", component_id="guns", instance_id="guns.R", parent_id="body.mesh")],
                observations=observations(p))


class ModelContractTest(unittest.TestCase):
    def test_reference_and_description_share_stage_contract(self):
        for description in [False, True]:
            p=contract_fixture(description); self.assertEqual(v.validate(p), [])
            self.assertEqual(v.require_stage(p, "MACRO_BLOCKOUT", verify_files=False)["status"], "READY")

    def test_pending_without_image_can_remain_blocked_without_fake_contract(self):
        p=pending_fixture(); p["schema_version"]=3
        self.assertEqual(v.validate(p), [])
        with self.assertRaises(ValueError): v.require_stage(p, "MACRO_BLOCKOUT", verify_files=False)

    def test_no_second_manifest_in_description_v3(self):
        p=contract_fixture(True); p["identity_lock"]["manifest"]={}
        self.assertTrue(any("duplicate" in e for e in v.validate(p)))

    def test_count_property_proportion_hierarchy_symmetry_pose_and_source_drift(self):
        for kind in ["count", "property", "proportion", "hierarchy", "symmetry", "pose", "source", "rule"]:
            p=contract_fixture()
            if kind=="count": p["components"][1]["count"]=1
            if kind=="property": p["components"][0]["claims"][0]["value"]="box"
            if kind=="proportion": p["relative_dimensions"][1]["max"] = .4
            if kind=="hierarchy": p["components"][1]["parent_id"]=None
            if kind=="symmetry": p["components"][1]["symmetry"]["type"]="NONE"
            if kind=="pose": p["proportion_basis"]["pose"]="crouching"
            if kind=="source": p["sources"][0]["sha256"]="f"*64
            if kind=="rule": p["model_contract"]["rules"][3]["view_completeness"]=None
            self.assertTrue(any("drift" in e for e in m.validate_contract(p)), kind)

    def test_auxiliary_and_speculative_claims_do_not_rewrite_identity(self):
        p=contract_fixture(); old=m.reference(p)
        p["components"][0]["claims"].append(dict(id="hidden", property="cooling", value="hypothesis", certainty="SPECULATIVE", basis="unknown", evidence=[]))
        p["auxiliary_references"].append(auxiliary())
        self.assertEqual(m.fingerprint(p), old["sha256"])

    def test_crop_shortened_barrel_and_foreshortening_are_distinct(self):
        p=contract_fixture(); rows=observations(p, "VIEWS"); gun=next(o for o in rows if o["rule_id"]=="p.gun")
        gun.update(completeness="CROPPED", value=.22)
        self.assertEqual(m.verify_observations(p, "VIEWS", rows)["status"], "FAIL")
        gun.update(completeness="FULL", value=.1, instance_values={'guns.L':.1,'guns.R':.22})
        self.assertEqual(m.verify_observations(p, "VIEWS", rows)["status"], "FAIL")
        gun.update(completeness="OCCLUDED", state="UNKNOWN", value=.22)
        self.assertEqual(m.verify_observations(p, "VIEWS", rows)["status"], "UNKNOWN")

    def test_ratio_anchors_relationships_and_symmetry_detect_geometric_drift(self):
        for rid,value in [("ratio.gun",.4), ("anchor",[-.2,.8]), ("mount",{}), ("symmetry",{"type":"NONE"}), ("parent",None)]:
            p=contract_fixture(); rows=observations(p); next(o for o in rows if o["rule_id"]==rid)["value"]=value
            if rid=='ratio.gun':next(o for o in rows if o['rule_id']==rid)['instance_values']['guns.L']=value
            self.assertEqual(m.verify_observations(p, "MACRO", rows)["status"], "FAIL", rid)

    def test_soft_change_is_warn_without_changing_persistent_design(self):
        p=contract_fixture(); before=copy.deepcopy(p); rows=observations(p)
        next(o for o in rows if o["rule_id"]=="detail")["value"]="simpler cover"
        result=m.verify_observations(p, "MACRO", rows)
        self.assertEqual(result["status"], "PASS"); self.assertTrue(any(c["result"]=="WARN" for c in result["checks"]))
        self.assertEqual(p, before)

    def test_missing_duplicate_fake_units_and_bool_measurements_cannot_pass(self):
        for kind in ["missing", "duplicate", "units", "bool", "evidence"]:
            p=contract_fixture(); rows=observations(p)
            if kind=="missing": rows.pop(0)
            if kind=="duplicate": rows.append(copy.deepcopy(rows[0]))
            if kind=="units": next(o for o in rows if o["rule_id"]=="p.gun")["unit"]="pixels"
            if kind=="bool": next(o for o in rows if o["rule_id"]=="p.gun")["value"]=True
            if kind=="bool": next(o for o in rows if o["rule_id"]=="p.gun")["instance_values"]['guns.L']=True
            if kind=="evidence": rows[0]["evidence"]=""
            self.assertNotEqual(m.verify_observations(p, "MACRO", rows)["status"], "PASS", kind)

    def test_failed_views_can_only_be_rejected_or_excluded(self):
        p=contract_fixture(); aux=auxiliary(); aux["views"]=["front", "side"]
        aux.update(permitted_views=["front", "side"], contract_review=dict(contract_ref=m.reference(p), image_sha256=aux["sha256"], views=[dict(view=view, observations=observations(p,"VIEWS")) for view in aux["views"]]))
        self.assertEqual(m.verify_auxiliary(p,aux), [])
        obs=aux["contract_review"]["views"][0]["observations"]
        next(o for o in obs if o["rule_id"]=="p.gun")["completeness"]="CROPPED"
        self.assertTrue(m.verify_auxiliary(p,aux))
        aux.update(use_status="RESTRICTED", permitted_views=["side"])
        self.assertEqual(m.verify_auxiliary(p,aux), [])
        aux["permitted_views"]=["front"]; self.assertTrue(m.verify_auxiliary(p,aux))
        aux.update(use_status="REJECTED", permitted_views=[]); self.assertEqual(m.verify_auxiliary(p,aux), [])

    def test_meshes_and_bolts_do_not_inflate_physical_count(self):
        p=contract_fixture(); a=assembly(p)
        a["parts"].append(dict(a["parts"][1],part_id="gunL.bolt",object_name="BoltL"))
        self.assertEqual(m.verify_assembly(p,a,"MACRO")["status"], "PASS")
        a["parts"].append(dict(a["parts"][1],part_id="gunX.mesh",object_name="GunX",instance_id="guns.X"))
        self.assertEqual(m.verify_assembly(p,a,"MACRO")["status"], "FAIL")

    def test_assembly_cannot_claim_expected_count_without_actual_bindings(self):
        p=contract_fixture(); a=assembly(p); a["parts"].pop()
        self.assertEqual(m.verify_assembly(p,a,"MACRO")["status"], "FAIL")

    def test_receipt_pins_observations_and_contract_not_small_operations(self):
        p=contract_fixture(); a=assembly(p); result=m.verify_assembly(p,a,"MACRO")
        self.assertEqual(result["status"], "PASS"); old=result["observations_sha256"]
        a["observations"][2]["value"]=.38
        self.assertNotEqual(m.verify_assembly(p,a,"MACRO")["observations_sha256"], old)
        self.assertEqual(m.verify_assembly(p,a,"BOLT_ADDED")["status"], "FAIL")

    def test_explicit_revision_invalidates_old_auxiliary_and_assembly(self):
        p=contract_fixture(); a=assembly(p); aux=auxiliary(); aux["contract_review"]={"contract_ref":m.reference(p)}
        new=copy.deepcopy(p); c=new["model_contract"]; c.update(revision=2, supersedes_sha256=c["sha256"], change_note="Approved longer gun within source envelope")
        next(r for r in c["rules"] if r["id"]=="ratio.gun")["bounds"]=[.55,.75]
        m.seal(new, previous=p)
        self.assertEqual(m.verify_assembly(new,a,"MACRO")["status"], "FAIL")
        self.assertTrue(m.verify_auxiliary(new,aux))
        with self.assertRaises(ValueError): m.seal(new)

    def test_required_change_needs_user_authority_and_new_brief(self):
        p=contract_fixture(True); new=copy.deepcopy(p); c=new["model_contract"]
        c.update(revision=2, supersedes_sha256=c["sha256"], change_note="User changed body requirement")
        new["constraints"][0]["value"]=2
        with self.assertRaisesRegex(ValueError,"USER"): m.seal(new,previous=p)

    def test_required_property_cannot_be_softened_or_lost(self):
        p=contract_fixture(True)
        next(r for r in p["model_contract"]["rules"] if r["id"]=="required.count")["level"]="SOFT CANONICAL"
        with self.assertRaisesRegex(ValueError,"REQUIRED"): m.seal(p)

    def test_cannot_silently_reseal_or_launder_duplicate_scene_object(self):
        p=contract_fixture(); p["components"][0]["claims"][0]["value"]="box"
        with self.assertRaisesRegex(ValueError,"explicit revision"): m.seal(p)
        p=contract_fixture(); a=assembly(p)
        a["parts"][2]["object_name"]=a["parts"][1]["object_name"]
        self.assertEqual(m.verify_assembly(p,a,"MACRO")["status"], "FAIL")

    def test_physical_hierarchy_and_cycles_checked_without_trusting_review(self):
        p=contract_fixture(); a=assembly(p); a["parts"][1]["parent_id"]=None
        self.assertEqual(m.verify_assembly(p,a,"MACRO")["status"], "FAIL")
        a=assembly(p); a["parts"][0]["parent_id"]="gunL.mesh"
        self.assertEqual(m.verify_assembly(p,a,"MACRO")["status"], "FAIL")

    def test_speculative_proportion_cannot_be_promoted_by_generator(self):
        p=contract_fixture(); p["relative_dimensions"][1]["certainty"]="SPECULATIVE"
        with self.assertRaisesRegex(ValueError,"speculative"): m.seal(p)

    def test_cycles_removed_counts_and_widened_ratio_policy_are_rejected(self):
        for kind in ["cycle", "count", "ratio"]:
            p=contract_fixture()
            if kind=="cycle": p["components"][0]["parent_id"]="guns"
            if kind=="count": p["model_contract"]["rules"].pop(0)
            if kind=="ratio": next(r for r in p["model_contract"]["rules"] if r["id"]=="ratio.gun")["bounds"]=[.1,1]
            with self.assertRaises(ValueError): m.seal(p)

    def test_malformed_rules_produce_diagnostics(self):
        for value in [None, {}, "bad", [None], [{"id":"bad"}]]:
            p=contract_fixture(); p["model_contract"]["rules"]=value
            self.assertTrue(m.validate_contract(p))

    def test_reference_keeps_required_marking_ahead_of_pixels(self):
        p=contract_fixture(); source=dict(p['sources'][0],id='brief',path='brief.txt',role='BRIEF',sha256='f'*64)
        p['sources'].append(source);p['source_of_truth'].append('brief')
        mark=dict(id='body.mark',property='mandatory marking and location',value='SCOUT-02 on front shell',certainty='REQUIRED',basis='User clause',
                  requirement_ids=['R.mark'],evidence=[dict(source_id='brief',region='clause 1',observation='SCOUT-02 on front shell')])
        p['constraints']=[dict(copy.deepcopy(mark),id='R.mark',target='claim',component_id='body',target_claim_ids=['body.mark'])]
        p['components'][0]['claims'].append(mark)
        p['model_contract']['rules'] += [rule('mark','claim','body.mark'),rule('mark.required','claim','R.mark')]
        p['model_contract'].pop('sha256');m.seal(p)
        self.assertEqual(v.validate(p),[])
        rows=observations(p);next(o for o in rows if o['rule_id']=='mark')['value']='SCOUT-20'
        self.assertEqual(m.verify_observations(p,'MACRO',rows)['status'],'FAIL')
        p['constraints'][0]['value']='drop marking';self.assertTrue(v.validate(p))

    def test_critical_relationship_cannot_be_declared_soft(self):
        p=contract_fixture();next(r for r in p['model_contract']['rules'] if r['id']=='mount')['level']='SOFT CANONICAL'
        with self.assertRaisesRegex(ValueError,'critical'):m.seal(p)

    def test_harness_delivers_contract_once_and_preserves_stage_only_routing(self):
        from test_pass0_mechanics import ROOT
        import mcp_runtime
        result=mcp_runtime.context(ROOT,'Create a reconnaissance mech from a text description.')
        path='skills/visual-reference-reconstruction/references/model-contract.md'
        self.assertTrue(result['ok'], result['error'])
        self.assertEqual([d['path'] for d in result['documents']].count(path),1)
        self.assertNotIn('visual-reference-reconstruction',mcp_runtime.route_task('Add wear to the existing contracted mech.'))

    def test_cached_reader_still_receives_contract_dependency(self):
        from unittest.mock import patch
        from test_pass0_mechanics import ROOT
        import mcp_runtime
        path='skills/visual-reference-reconstruction/references/model-contract.md'
        with patch.object(mcp_runtime,'render',return_value='SOURCE: docs/foundation.md\n\nold context'):
            text=mcp_runtime.render_context(ROOT,'visual-reference-reconstruction')
        self.assertEqual(text.count('SOURCE: '+path),1)

    def test_progressive_recipes_remain_available_without_losing_design_rules(self):
        from test_pass0_mechanics import ROOT
        from test_form_tools import ContextDeliveryTest
        import mcp_runtime
        first=mcp_runtime.context(ROOT,ContextDeliveryTest.mixed)
        self.assertTrue(first['ok'])
        path='skills/blender-pipeline/references/techniques/form-development.md'
        self.assertIn(path,[d['path'] for d in first['conditional_documents']])
        next_context=mcp_runtime.context(ROOT,ContextDeliveryTest.mixed,known_documents=first['receipts'],requested_documents=[path])
        self.assertTrue(next_context['ok'])
        self.assertEqual([d['path'] for d in next_context['documents']].count(path),1)

    def test_per_instance_measurements_cannot_average_short_and_long_guns(self):
        p=contract_fixture(); rows=observations(p); obs=next(o for o in rows if o['rule_id']=='p.gun')
        obs['instance_values']={'guns.L':.1,'guns.R':.34};obs['value']=.22
        self.assertEqual(m.verify_observations(p,'MACRO',rows)['status'],'FAIL')
        obs.pop('instance_values')
        self.assertEqual(m.verify_observations(p,'MACRO',rows)['status'],'UNKNOWN')
        a=assembly(p);next(o for o in a['observations'] if o['rule_id']=='p.gun')['instance_values']={'unknown.1':.22,'unknown.2':.22}
        self.assertEqual(m.verify_assembly(p,a,'MACRO')['status'],'FAIL')


if __name__ == "__main__": unittest.main()
