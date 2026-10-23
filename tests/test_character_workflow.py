"""Real routing/validator consumers with synthetic file-backed evidence, not art QA."""
import copy
import hashlib
import io
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import mcp_runtime as runtime
import qa_gate as qa
import read_blender_skill
from test_qa_gate import fixture as receipt, check
from test_model_contract import contract_fixture, assembly, m, v
from test_surface_transfer import fixture as transfer_fixture

ROOT = Path(__file__).resolve().parents[1]


def write(root, name, value):
    data = json.dumps(value, ensure_ascii=False).encode() if isinstance(value, dict) else value
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return dict(path=name, sha256=hashlib.sha256(data).hexdigest())


def workflow_fixture(root, mode="GEOMETRY_ONLY"):
    p = receipt(changed=False)
    p["schema_version"] = 3
    for item in p["captures"]:
        vector = qa.CANONICAL_DIRECTIONS[item["view"]]
        length = math.sqrt(sum(x*x for x in vector))
        x,y,z = (n/length for n in vector)
        item["setup"] = dict(target="character",objects=["Body"],frame=1.0,fps=24.0,
                             framing=dict(center=[0,0,1],span=2),resolution=[512,512],mode="solid",
                             lighting="neutral",projection="ORTHO",ortho_scale=2,
                             camera_matrix=[1,0,x,0,0,1,y,0,0,0,z,0,0,0,0,1])
        write(root, item["image"]["path"], b"sample reviewed frame")
    for name in (*qa.PRIMARY_CHECKS, "face_identity", "hair_occlusion", "seam_invisibility", "uv_binding"):
        p["checks"][name] = check(name)
    design = contract_fixture()
    # Construct a new synthetic packet with real fixture file hashes, then lock
    # it once. This is not a revision of a production design.
    design["model_contract"].pop("sha256")
    design["object_class"] = "character"
    for source in design["sources"]:
        source["path"] = source["id"] + ".png"
        source["sha256"] = write(root, source["path"], b"source" if source["id"]=="original" else b"auxiliary")["sha256"]
    m.seal(design)
    artifacts = dict(pass0=write(root,"pass0.json",design),
                     assembly=write(root,"assembly_graph.json",assembly(design)),
                     saved=write(root,"state.blend",b"synthetic saved state"))
    face = dict(mode=mode,status="EXECUTED",reason="Reviewed method appropriate to source and requested identity",
                source_ids=["original"],identity_anchors=["body.exterior"],occluded_regions=[],
                geometry_only_basis="VOLUME_IDENTITY" if mode=="GEOMETRY_ONLY" else "NOT_APPLICABLE",
                generation_required=mode in ("RECONSTRUCT_THEN_LAYER","HYBRID_PRESERVATION"),
                tools=[],execution=["saved"],transfer=None)
    usage = [dict(id="visual-reference-reconstruction",status="EXECUTED",reason="Inspected sources and sealed contract",
                  execution=["pass0"],verification=[]),
             dict(id="blender-character-modeling",status="EXECUTED",reason="Saved geometry and reviewed primary forms",
                  execution=["saved"],verification=[])]
    if mode != "GEOMETRY_ONLY":
        record = transfer_fixture()
        record["schema_version"] = 2
        visible = dict(name="visible_eye",visibility="VISIBLE",source="ORIGINAL",landmarks=["eye_corner"],protected=True)
        hidden = dict(name="hidden_eye",visibility="OCCLUDED",source="INFERRED",landmarks=["eye_line"],protected=False)
        regenerate = face["generation_required"]
        record["face_strategy"] = dict(mode={"DIRECT_FEATURE_TRANSFER":"DIRECT","RECONSTRUCT_THEN_LAYER":"RECONSTRUCT_THEN_LAYER",
                                            "HYBRID_PRESERVATION":"HYBRID"}[mode],
                    regions=[visible,hidden] if mode=="HYBRID_PRESERVATION" else [hidden] if regenerate else [visible],
                    occluder="HAIR" if regenerate else "NONE",occlusion_mask="mask" if regenerate else None,
                    occlusion_layer="GEOMETRY" if regenerate else "NONE",reason=face["reason"])
        if regenerate:
            record["artifacts"]["repair"]["path"] = "repair.png"
            record["steps"].append(dict(operation="regenerate",input="crop",output="repair",reason="Hidden eye provisional repair",
                                        parameters="Bounded source-conditioned edit",mask="mask",prompt="prompt"))
            record["target"]["image"] = "repair"
            face["occluded_regions"] = [dict(name="hidden_eye",visibility="OCCLUDED",certainty="INFERRED",treatment="RECONSTRUCT")]
            artifacts["generated"] = copy.deepcopy(record["artifacts"]["repair"])
            face["tools"] = [dict(name="imagegen",availability="AVAILABLE",reason="Current session tool checked",
                                   execution=["generated"])]
        for aid, artifact in record["artifacts"].items():
            write(root,artifact["path"],aid.encode())
        for row in record["qa"].values():
            row.update(status="PASS",reviewer="fixture",observations="Synthetic declared review",artifacts=["comparison"])
        artifacts["transfer"] = write(root,"surface_transfer.json",record)
        face.update(execution=["transfer"],transfer="transfer")
        usage.append(dict(id="blender-reference-surface-transfer",status="EXECUTED",reason="Selected transfer has lineage and QA",
                          execution=["transfer"],verification=[]))
    p["workflow"] = dict(artifacts=artifacts,pass0=dict(artifact="pass0",contract_ref=m.reference(design)),
                         face_strategy=face,primary_assembly="assembly",skill_usage=usage)
    return p


class CharacterWorkflowTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)

    def fixture(self, mode="GEOMETRY_ONLY"):
        return workflow_fixture(self.root, mode)

    def result(self, p, stage="FINAL"):
        return qa.validate(p,root=self.root,stage=stage)

    def replace_artifact(self, p, aid, value):
        a = p["workflow"]["artifacts"]
        a[aid] = write(self.root,a[aid]["path"],value)

    def test_all_four_face_strategies_pass_declared_final_gate(self):
        for mode in sorted(qa.FACE_MODES):
            with self.subTest(mode=mode):
                p = self.fixture(mode)
                self.assertEqual(self.result(p)["gate"],"PASS")

    def test_face_gate_does_not_require_mass_detail_or_final_coverage(self):
        p = self.fixture(); p["captures"] = []; p["checks"] = {}
        p["protected_zones"] = []; p["user_flags"] = []
        p["capabilities"]["STATIC_VISUAL"].update(status="SKIP",reviewer="",evidence=[])
        p["workflow"]["face_strategy"].update(status="SELECTED",execution=[])
        p["workflow"]["primary_assembly"] = None
        self.assertEqual(self.result(p,"FACE")["gate"],"PASS")
        self.assertEqual(self.result(p,"DETAIL")["gate"],"OPEN")
        self.assertEqual(self.result(p)["gate"],"OPEN")

    def test_stage_readiness_without_verified_files_is_open(self):
        p = self.fixture()
        for stage in ("FACE","DETAIL","FINAL"):
            self.assertEqual(qa.validate(p,stage=stage)["gate"],"OPEN")

    def test_usable_source_selection_excludes_generated_derivative(self):
        p = self.fixture(); p["workflow"]["face_strategy"]["source_ids"]=["generated_input"]
        with self.assertRaisesRegex(ValueError,"authoritative"):
            self.result(p)

    def test_stale_contract_binding_cannot_switch_canonical_identity(self):
        p = self.fixture(); p["workflow"]["pass0"]["contract_ref"]["sha256"]="f"*64
        with self.assertRaisesRegex(ValueError,"stale"):
            self.result(p)

    def test_identity_lock_and_contract_reject_unreviewed_hero_drift(self):
        design = contract_fixture(description=True)
        self.assertEqual(v.validate(design),[])
        design["identity_lock"]["source_id"]="brief"
        self.assertTrue(v.validate(design))
        design = contract_fixture(description=True)
        design["components"][0]["count"]=3
        self.assertTrue(v.validate(design))

    def test_occluded_eye_keeps_uncertainty_and_hair_review(self):
        p = self.fixture("HYBRID_PRESERVATION")
        p["workflow"]["face_strategy"]["occluded_regions"][0]["certainty"]="CONFIRMED"
        with self.assertRaisesRegex(ValueError,"hidden detail"):
            self.result(p)
        p = self.fixture("HYBRID_PRESERVATION")
        p["checks"]["hair_occlusion"]["status"]="FAIL"
        self.assertEqual(self.result(p)["gate"],"FAIL")

    def test_geometry_only_can_keep_hidden_eye_without_generator(self):
        p = self.fixture()
        p["workflow"]["face_strategy"]["occluded_regions"]=[dict(name="eye",visibility="OCCLUDED",
                certainty="INFERRED",treatment="KEEP_OCCLUDED")]
        self.assertEqual(self.result(p)["gate"],"PASS")

    def test_geometry_only_rejects_waiving_graphic_identity(self):
        p = self.fixture();p["workflow"]["face_strategy"]["geometry_only_basis"]="GRAPHIC_IDENTITY_REQUIRED"
        with self.assertRaisesRegex(ValueError,"graphic identity"):
            self.result(p)
        p = self.fixture();p["checks"]["face_identity"]["status"]="FAIL"
        self.assertEqual(self.result(p)["gate"],"FAIL")

    def test_available_generator_without_execution_cannot_complete(self):
        p = self.fixture("RECONSTRUCT_THEN_LAYER")
        p["workflow"]["face_strategy"]["tools"][0]["execution"]=[]
        self.assertEqual(self.result(p)["gate"],"OPEN")
        self.assertEqual(self.result(p,"FACE")["gate"],"PASS")

    def test_unavailable_generator_blocks_dependent_stages(self):
        p = self.fixture("HYBRID_PRESERVATION")
        f = p["workflow"]["face_strategy"]
        f.update(status="BLOCKED",execution=[])
        f["tools"][0].update(availability="UNAVAILABLE",execution=[],reason="No current tool")
        for stage in ("FACE","DETAIL","FINAL"):
            self.assertEqual(self.result(p,stage)["gate"],"OPEN")

    def test_unavailable_generator_cannot_claim_execution(self):
        p = self.fixture("HYBRID_PRESERVATION")
        p["workflow"]["face_strategy"]["tools"][0]["availability"]="UNAVAILABLE"
        with self.assertRaisesRegex(ValueError,"unavailable tool"):
            self.result(p)

    def test_generation_requirement_cannot_be_removed(self):
        p = self.fixture("HYBRID_PRESERVATION")
        p["workflow"]["face_strategy"]["generation_required"]=False
        with self.assertRaisesRegex(ValueError,"contradicts"):
            self.result(p)

    def test_generated_output_must_match_transfer_lineage(self):
        p = self.fixture("HYBRID_PRESERVATION")
        p["workflow"]["artifacts"]["generated"]=write(self.root,"unrelated.png",b"unrelated output")
        with self.assertRaisesRegex(ValueError,"lineage"):
            self.result(p)

    def test_read_skill_is_not_execution(self):
        p = self.fixture(); row = p["workflow"]["skill_usage"][1]
        row.update(status="READ",execution=[])
        self.assertEqual(self.result(p)["gate"],"OPEN")
        row["execution"]=["saved"]
        with self.assertRaisesRegex(ValueError,"not execution"):
            self.result(p)

    def test_executed_skill_needs_procedure_artifact(self):
        p = self.fixture();p["workflow"]["skill_usage"][1]["execution"]=["pass0"]
        with self.assertRaisesRegex(ValueError,"saved Blender"):
            self.result(p)

    def test_verified_skill_needs_accepted_checks(self):
        p = self.fixture();row=p["workflow"]["skill_usage"][1]
        row.update(status="VERIFIED",verification=["primary_head_face"])
        self.assertEqual(self.result(p)["gate"],"PASS")
        p["checks"]["primary_head_face"]["status"]="REVIEW_REQUIRED"
        with self.assertRaisesRegex(ValueError,"VERIFIED"):
            self.result(p)

    def test_unaccepted_primary_forms_block_detail_and_final(self):
        for status, expected in (("FAIL","FAIL"),("SKIP","OPEN"),("REVIEW_REQUIRED","OPEN")):
            p = self.fixture(); p["checks"]["primary_neck_shoulders"]["status"]=status
            for stage in ("DETAIL","FINAL"):
                with self.subTest(status=status,stage=stage):
                    self.assertEqual(self.result(p,stage)["gate"],expected)

    def test_missing_primary_review_or_assembly_blocks_detail(self):
        p=self.fixture();del p["checks"]["primary_torso_pelvis"]
        self.assertEqual(self.result(p,"DETAIL")["gate"],"OPEN")

    def test_primary_pass_cannot_cite_skipped_or_past_images(self):
        p=self.fixture()
        for row in p["captures"]:
            row.update(status="SKIP",reviewer="",image=None)
        self.assertEqual(self.result(p,"DETAIL")["gate"],"OPEN")
        p=self.fixture();p["captures"]=[x for x in p["captures"] if x["view"] != "side"]
        self.assertEqual(self.result(p,"DETAIL")["gate"],"OPEN")
        p=self.fixture();p["workflow"]["primary_assembly"]=None
        self.assertEqual(self.result(p,"DETAIL")["gate"],"OPEN")

    def test_primary_dimensions_are_rechecked_against_contract(self):
        p=self.fixture(); graph=json.loads((self.root/"assembly_graph.json").read_text())
        row=next(x for x in graph["observations"] if x["rule_id"]=="p.body")
        row["value"]=9
        self.replace_artifact(p,"assembly",graph)
        self.assertEqual(self.result(p,"DETAIL")["gate"],"FAIL")

    def test_transfer_source_strategy_and_visual_seams_are_not_waived(self):
        for scenario in ("source","mode","seams","pending"):
            p=self.fixture("DIRECT_FEATURE_TRANSFER")
            record=json.loads((self.root/"surface_transfer.json").read_text())
            if scenario=="source":
                record["artifacts"]["source"]=write(self.root,"wrong_source.dat",b"wrong face")
            elif scenario=="mode":
                p["workflow"]["face_strategy"]["mode"]="HYBRID_PRESERVATION"
                p["workflow"]["face_strategy"]["generation_required"]=True
                p["workflow"]["face_strategy"]["tools"]=[dict(name="imagegen",availability="AVAILABLE",reason="checked",execution=[])]
            elif scenario=="seams": record["qa"]["seams"]["status"]="FAIL"
            else: record["seam_cleanup"]=dict(status="PENDING",reason="not integrated")
            self.replace_artifact(p,"transfer",record)
            with self.subTest(scenario=scenario):
                if scenario in ("source","mode"):
                    with self.assertRaises(ValueError): self.result(p)
                else:
                    self.assertEqual(self.result(p)["gate"],"FAIL" if scenario=="seams" else "OPEN")

    def escalation(self):
        return dict(issue="face volume",attempts=2,state="ESCALATED",owner="character/surface review",
                    note="Two local failures; change method before continuation",checkpoint="saved",
                    previous_method="local primitive corrections",next_method="continuous topology and registered source",
                    evidence=["primary_head_face"])

    def test_two_failed_corrections_require_checkpoint_and_new_method(self):
        for scenario in ("checkpoint","method","evidence"):
            p=self.fixture();row=self.escalation();p["escalation"]=[row]
            if scenario=="checkpoint":row["checkpoint"]=None
            elif scenario=="method":row["next_method"]=row["previous_method"]
            else:row["evidence"]=[]
            with self.subTest(scenario=scenario),self.assertRaises(ValueError):self.result(p)

    def test_escalation_stays_open_until_reviewed_resolution(self):
        p=self.fixture();p["escalation"]=[self.escalation()]
        self.assertEqual(self.result(p,"DETAIL")["gate"],"OPEN")
        p["escalation"][0]["state"]="RESOLVED"
        self.assertEqual(self.result(p)["gate"],"PASS")
        p["checks"]["primary_head_face"]["status"]="SKIP"
        with self.assertRaisesRegex(ValueError,"resolution"):self.result(p)

    def test_false_pass_and_legacy_compatibility(self):
        for version in (1,2):
            p=receipt(changed=False)
            if version==2:
                p=self.fixture();p["schema_version"]=2;p.pop("workflow")
            result=qa.validate(p)
            self.assertEqual(result["gate"],"PASS")
            self.assertEqual(result["workflow"],"NOT_RECORDED_LEGACY")
            p["checks"]["face_identity"]=check("face_identity")
            p["checks"]["face_identity"]["status"]="SKIP"
            self.assertEqual(qa.validate(p)["gate"],"OPEN")
        p=receipt();p["checks"]["pending_export"]=check("pending_export")
        p["checks"]["pending_export"]["status"]="REVIEW_REQUIRED"
        p["capabilities"]["EXPORT"].update(status="PASS",reviewer="test",evidence=["pending_export"])
        self.assertEqual(qa.validate(p)["gate"],"OPEN")

    def test_unknown_fields_path_escape_and_tampered_files(self):
        for scenario in ("unknown","escape","tamper"):
            p=self.fixture()
            if scenario=="unknown":p["workflow"]["unexpected"]=True
            elif scenario=="escape":p["workflow"]["artifacts"]["saved"]["path"]="../state.blend"
            else:(self.root/"state.blend").write_bytes(b"changed")
            with self.subTest(scenario=scenario),self.assertRaises(ValueError):self.result(p)

    def test_actual_cli_reports_stage_and_exit_code(self):
        p=self.fixture();file=self.root/"qa_receipt.json";write(self.root,file.name,p)
        output=io.StringIO()
        with patch.object(sys,"argv",["qa_gate",str(file),"--verify-files","--stage","DETAIL"]),redirect_stdout(output):
            self.assertEqual(qa.main(),0)
        result=json.loads(output.getvalue())
        self.assertEqual(result["stage"],"DETAIL")
        self.assertEqual(result["visual"],"NOT_EVALUATED")
        self.assertEqual(result["final_coverage"],"NOT_CHECKED")
        self.assertIn("not prove",result["limits"])

    def test_malformed_transfer_json_cli_fails_without_traceback(self):
        p=self.fixture("DIRECT_FEATURE_TRANSFER")
        for data in (b'{"schema_version":2,"schema_version":2}',b'{"value":NaN}'):
            p["workflow"]["artifacts"]["transfer"]=write(self.root,"surface_transfer.json",data)
            file=self.root/"qa_receipt.json";write(self.root,file.name,p)
            output=io.StringIO()
            with patch.object(sys,"argv",["qa_gate",str(file),"--verify-files"]),redirect_stdout(output):
                self.assertEqual(qa.main(),1)
            self.assertEqual(json.loads(output.getvalue())["structure"],"FAIL")


class CharacterContextTest(unittest.TestCase):
    def test_generic_reference_creation_routes_actual_character_owner(self):
        for task in ("Create a character from the reference images.","Создай персонажа по референсам."):
            self.assertEqual(runtime.route_task(task),["visual-reference-reconstruction","blender-character-modeling"])

    def test_face_strategy_gate_delivered_before_long_recipes(self):
        task="Create an anime character from references, hair covers one eye."
        c=runtime.context(ROOT,task)
        delivered={x["path"] for x in c["documents"] if x["status"]=="delivered"}
        self.assertIn(runtime.CHARACTER_GATES,delivered)
        self.assertIn("skills/blender-character-modeling/SKILL.md",delivered)
        self.assertEqual(c["workflow_requirements"][0]["stages"],["FACE","DETAIL","FINAL"])
        self.assertTrue(all(x["status"]=="DISCOVERED" for x in c["skill_usage"]))
        self.assertTrue(runtime.context(ROOT,task,max_chars=200000)["ok"])
        follow=runtime.context(ROOT,task,max_chars=60000,known_documents=c["receipts"],requested_documents=c["missing_documents"])
        self.assertTrue(follow["ok"],follow["missing_documents"])

    def test_tiny_budget_cannot_claim_gate_was_delivered(self):
        c=runtime.context(ROOT,"Create a character from reference images.",max_chars=500)
        self.assertFalse(c["ok"])
        self.assertIn(runtime.CHARACTER_GATES,c["missing_documents"])

    def test_direct_and_compatibility_readers_include_gate(self):
        for name in ("blender-character-modeling","blender-anime-character-modeling","Blender_Character_Modeling_SKILL"):
            self.assertIn(runtime.CHARACTER_GATES,read_blender_skill.document_paths(ROOT,name))

    def test_noncharacter_and_stage_only_routes_do_not_gain_geometry(self):
        cases={"Create a chair from reference images.":["visual-reference-reconstruction","blender-props"],
               "Unwrap UVs on the anime character.":["blender-pipeline"],
               "Review a character from reference images.":["verification"],
               "Transfer the face from the reference to the anime character.":["blender-reference-surface-transfer"],
               "Fix the weights on the character.":["blender-rigging-skinning"]}
        for task,expected in cases.items():
            self.assertEqual(runtime.route_task(task),expected)
            self.assertEqual(runtime.context(ROOT,task,max_chars=200000)["workflow_requirements"],[])

    def test_incidental_character_mention_does_not_authorize_modeling(self):
        for task in ("Create a camera near the character.","Create a light next to the character.",
                     "Создай камеру рядом с персонажем.","Create a texture for the character."):
            self.assertNotIn("blender-character-modeling",runtime.route_task(task))


if __name__=="__main__":
    unittest.main()
