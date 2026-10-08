"""Pass 3 QA receipt: positive/negative metadata and final-view gates."""
import copy
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import qa_gate as qa

DUMMY_HASH=hashlib.sha256(b"sample reviewed frame").hexdigest()


def setup(view):
    directions = {
        "front":[0,-1,0], "side":[1,0,0], "back":[0,1,0],
        "three_quarter":[1,-1,.6], "high_45":[0,-1,1], "low_45":[0,-1,-1],
    }
    return dict(target="Agent_Red7",frame=1,framing="fixed:center0-span4",
                resolution=[512,512],mode="solid",lighting="neutral_studio",
                projection="ORTHO",camera="FIXED:"+view,direction=directions[view])


def capture(view,phase="AFTER"):
    return dict(id=view+"_"+phase,view=view,phase=phase,status="PASS",
                image=dict(path="frames/"+view+"_"+phase+".png",sha256=DUMMY_HASH),
                setup=setup(view),reviewer="asset-reviewer",
                observations="Image opened; shape and contacts inspected at named angle")


def check(name,evidence="front_AFTER"):
    return dict(status="PASS",reviewer="asset-reviewer",
                observations="Compared against approved reference and before/after evidence",
                evidence=[evidence])


def capabilities():
    result={key:dict(status="NOT_APPLICABLE",reviewer="",
                     observations="Not required by this scoped acceptance",
                     evidence=[]) for key in qa.CAPABILITIES}
    result["STATIC_VISUAL"]=dict(status="PASS",reviewer="asset-reviewer",
                                 observations="Reviewed required visual frames",
                                 evidence=["reference_proportions","form_contacts"])
    return result


def fixture(*,profile="CHARACTER_FINAL",changed=True):
    views=qa.PROFILES[profile]["views"]
    captures=[capture(view,phase) for view in views
              for phase in (("BEFORE","AFTER") if changed else ("AFTER",))]
    closeups=[]
    for region in qa.PROFILES[profile]["closeups"]:
        for phase in (("BEFORE","AFTER") if changed else ("AFTER",)):
            item=capture("front",phase)
            item.update(id="close_"+region+"_"+phase,region=region)
            del item["view"]
            closeups.append(item)
    checks={name:check(name,captures[-1]["id"])
            for name in qa.PROFILES[profile]["checks"]}
    caps=capabilities()
    caps["STATIC_VISUAL"]["evidence"] = list(checks)[:2]
    return dict(schema_version=1,asset="Agent_Red7",profile=profile,
                changed=changed,animated=False,
                requested_capabilities=["STATIC_VISUAL"],captures=captures,
                closeups=closeups,checks=checks,
                protected_zones=[dict(id="eye_spacings",**check("eye_spacings",captures[-1]["id"]))],
                user_flags=[dict(id="keep_expression",action="PRESERVE",
                                 **check("keep_expression",captures[-1]["id"]))],
                capabilities=caps, escalation=[])


class QAReceiptTest(unittest.TestCase):
    def test_full_character_with_orthographic_and_two_45_views_pass(self):
        p=fixture()
        result=qa.validate(p)
        self.assertEqual(result["gate"],"PASS",result)

    def test_unmodified_asset_no_before_needed(self):
        p=fixture(changed=False)
        self.assertEqual(qa.validate(p)["gate"],"PASS")

    def test_missing_or_unreviewed_view_never_passes(self):
        for scenario in ("missing_high","review_needed","skipped_low"):
            p=fixture()
            if scenario=="missing_high":
                p["captures"]=[c for c in p["captures"] if c["id"]!="high_45_AFTER"]
            elif scenario=="review_needed":
                row=next(c for c in p["captures"] if c["id"]=="side_AFTER")
                row.update(status="REVIEW_REQUIRED",reviewer="")
            else:
                row=next(c for c in p["captures"] if c["id"]=="low_45_AFTER")
                row.update(status="SKIP",reviewer="",image=None,observations="No usable camera")
            with self.subTest(scenario=scenario):
                self.assertEqual(qa.validate(p)["gate"],"OPEN")

    def test_invalid_45_vector_and_perspective_claims_are_rejected(self):
        for change in ("angle","projection"):
            p=fixture()
            entry=next(c for c in p["captures"] if c["id"]=="high_45_AFTER")
            if change=="angle": entry["setup"]["direction"]=[0,-1,.1]
            else: entry["setup"]["projection"]="PERSP"
            with self.subTest(change=change),self.assertRaises(ValueError):
                qa.validate(p)

    def test_before_after_comparability_is_required(self):
        p=fixture()
        entry=next(c for c in p["captures"] if c["id"]=="front_AFTER")
        entry["setup"]["lighting"]="new_light"
        self.assertEqual(qa.validate(p)["gate"],"FAIL")

    def test_protected_zone_or_red_flag_cannot_be_silent(self):
        p=fixture();p["protected_zones"][0]["status"]="FAIL"
        self.assertEqual(qa.validate(p)["gate"],"FAIL")
        p=fixture();p["user_flags"][0]["status"]="SKIP"
        p["user_flags"][0]["reviewer"]=""
        p["user_flags"][0]["evidence"]=[]
        p["user_flags"][0]["observations"]="User preservation check was not performed"
        self.assertEqual(qa.validate(p)["gate"],"OPEN")

    def test_face_transfer_requires_closeup_and_seam_check(self):
        p=fixture(profile="FACE_TRANSFER_FINAL")
        self.assertEqual(qa.validate(p)["gate"],"PASS")
        p["checks"]["seam_invisibility"]["status"]="FAIL"
        self.assertEqual(qa.validate(p)["gate"],"FAIL")
        p=fixture(profile="FACE_TRANSFER_FINAL")
        p["closeups"]=[x for x in p["closeups"] if x["phase"]!="AFTER"]
        self.assertEqual(qa.validate(p)["gate"],"OPEN")

    def test_closeup_comparable_and_focused_3d_is_scoped(self):
        p=fixture(profile="FOCUSED_3D_REPAIR")
        self.assertEqual(qa.validate(p)["gate"],"PASS")
        p["closeups"][-1]["setup"]["framing"]="auto_reframed"
        self.assertEqual(qa.validate(p)["gate"],"FAIL")

    def test_capability_ladder_never_conflates_game_ready(self):
        p=fixture()
        p["capabilities"]["GAME_READY"].update(status="PASS",
                       reviewer="agent",evidence=["form_contacts"],
                       observations="Incorrect assumed readiness")
        self.assertEqual(qa.validate(p)["gate"],"FAIL")
        p=fixture()
        p["requested_capabilities"]=["STATIC_VISUAL","EXPORT"]
        self.assertEqual(qa.validate(p)["gate"],"OPEN")

    def test_noncomparable_proportion_face_repair_blocks_static_claim(self):
        p=fixture()
        p["checks"]["reference_proportions"]["status"]="REVIEW_REQUIRED"
        p["checks"]["reference_proportions"]["reviewer"]=""
        self.assertEqual(qa.validate(p)["gate"],"OPEN")
        self.assertTrue(any("STATIC_VISUAL" in s for s in qa.validate(p)["blockers"]))

    def test_escalation_keeps_open_issue_blocked(self):
        p=fixture()
        p["escalation"]=[dict(issue="eye seam",attempts=2,state="ESCALATED",
                              owner="facial surfacing",note="needs new source")]
        self.assertEqual(qa.validate(p)["gate"],"OPEN")

    def test_capture_metadata_v2_uses_real_matrix_and_framing(self):
        import math
        p=fixture(profile="FOCUSED_3D_REPAIR",changed=False)
        p["schema_version"]=2
        def make_meta(view):
            direction=qa.CANONICAL_DIRECTIONS.get(view,(0,-1,0))
            length=math.sqrt(sum(x*x for x in direction))
            x,y,z=(c/length for c in direction)
            return {
                "ok":True,"status":"VISUAL REVIEW REQUIRED",
                "capture_kind":"viewport-oriented evidence render",
                "view":view,"target":"character","objects":["R7_Face_Head"],
                "frame":1.0,"fps":24.0,
                "framing":{"center":[0.0,0.0,1.4],"span":1.7},
                "resolution":[512,512],"mode":"solid",
                "lighting":"fixed studio solid",
                "projection":"ORTHO","ortho_scale":1.7,
                "camera_matrix":[1,0,x,0,0,1,y,0,0,0,z,0,0,0,0,1]
            }
        for item in p["captures"]:
            item["setup"]=qa.setup_from_capture_metadata(make_meta(item["view"]))
        for item in p["closeups"]:
            item["setup"]=qa.setup_from_capture_metadata(make_meta("front"))
        self.assertEqual(qa.validate(p)["gate"],"PASS")
        tampered=copy.deepcopy(p)
        target=next(x for x in tampered["captures"] if x["view"]=="high_45")
        target["setup"]["camera_matrix"][10] = 0.01
        with self.assertRaisesRegex(ValueError,"camera matrix"):
            qa.validate(tampered)
        bad=make_meta("low_45")
        bad["framing"]="manually-invented-flat-label"
        with self.assertRaises(ValueError):
            qa.setup_from_capture_metadata(bad)

    def test_capture_v2_before_after_real_setup_comparison(self):
        p=fixture(changed=True)
        p["schema_version"]=2
        import math
        for item in p["captures"]:
            vector=qa.CANONICAL_DIRECTIONS[item["view"]]
            norm=math.sqrt(sum(v*v for v in vector))
            x,y,z=(v/norm for v in vector)
            item["setup"]={
                "target":"character","objects":["R7_Face_Head"],
                "frame":1.0,"fps":24.0,
                "framing":{"center":[0.0,0.0,1.4],"span":1.7},
                "resolution":[512,512],"mode":"solid",
                "lighting":"fixed studio solid",
                "projection":"ORTHO","ortho_scale":1.7,
                "camera_matrix":[1,0,x,0,0,1,y,0,0,0,z,0,0,0,0,1]
            }
        self.assertEqual(qa.validate(p)["gate"],"PASS")
        after=next(x for x in p["captures"] if x["id"]=="front_AFTER")
        after["setup"]["framing"]["span"]=2.0
        self.assertEqual(qa.validate(p)["gate"],"FAIL")

    def test_canonical_capture_helper_contains_true_45_degree_directions(self):
        import ast
        source=ast.parse((Path(__file__).resolve().parents[1] /
                          "tools/blender_capture.py").read_text(encoding="utf-8"))
        row=next(node for node in source.body if isinstance(node,ast.Assign)
                 and any(isinstance(x,ast.Name) and x.id=="VIEWS" for x in node.targets))
        vectors=ast.literal_eval(row.value)
        self.assertEqual(vectors["high_45"],(0,-1,1))
        self.assertEqual(vectors["low_45"],(0,-1,-1))

    def test_optional_failed_criteria_are_not_silently_accepted(self):
        p=fixture()
        p["checks"]["seam_invisibility"]=check("seam_invisibility")
        p["checks"]["seam_invisibility"]["status"]="FAIL"
        self.assertEqual(qa.validate(p)["gate"],"FAIL")

    def test_duplicate_user_flag_or_protected_zone_rejected(self):
        for kind in ("user_flags","protected_zones"):
            p=fixture()
            p[kind].append(copy.deepcopy(p[kind][0]))
            with self.subTest(kind=kind),self.assertRaises(ValueError):
                qa.validate(p)

    def test_strict_unknown_fields_and_escaped_artifact_paths(self):
        p=fixture();p["unexpected"]="ignored?"
        with self.assertRaises(ValueError):qa.validate(p)
        p=fixture();p["captures"][0]["image"]["path"]="../escape.png"
        with self.assertRaises(ValueError):qa.validate(p)

    def test_non_png_and_duplicate_json_keys_fail_closed(self):
        import io
        import json
        import tempfile
        from contextlib import redirect_stdout
        from unittest.mock import patch
        p=fixture()
        p["captures"][0]["image"]["path"]="frames/text-not-image.txt"
        with self.assertRaisesRegex(ValueError, "PNG"):
            qa.validate(p)
        with tempfile.TemporaryDirectory() as folder:
            file=Path(folder)/"duplicate.json"
            file.write_text('{"schema_version":1,"schema_version":1}',encoding="utf-8")
            output=io.StringIO()
            with patch.object(sys,"argv",["qa_gate",str(file)]),redirect_stdout(output):
                exit_code=qa.main()
            self.assertEqual(exit_code,1)
            self.assertEqual(json.loads(output.getvalue())["structure"],"FAIL")

    def test_file_hashes_can_be_checked_without_claiming_pixel_visual_truth(self):
        with tempfile.TemporaryDirectory() as root:
            p=fixture(changed=False)
            for item in p["captures"]:
                path=Path(root)/item["image"]["path"]
                path.parent.mkdir(exist_ok=True,parents=True)
                path.write_bytes(b"sample reviewed frame")
            self.assertEqual(qa.validate(p,root=root)["gate"],"PASS")
            file=Path(root)/p["captures"][0]["image"]["path"]
            file.write_bytes(b"tampered evidence")
            with self.assertRaisesRegex(ValueError,"hash mismatch"):
                qa.validate(p,root=root)


if __name__ == "__main__":
    unittest.main()
