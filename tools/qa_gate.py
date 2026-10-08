"""Task-local character QA evidence completeness gate.

Checks declared coverage, provenance and before/after comparability; NEVER assesses
visual likeness or correctness by parsing JSON. V1 retains legacy setup format;
v2 uses real Blender camera matrices/framing/fractional frames; v3 adds workflow
readiness and execution evidence. No second Model Contract authority.
"""
import argparse
import hashlib
import json
import math
import importlib.util
from pathlib import Path, PureWindowsPath
import re

STATUSES = {"PASS", "WARN", "FAIL", "SKIP", "REVIEW_REQUIRED"}
CAPABILITIES = ("STATIC_VISUAL", "EXPORT", "RIG_READY", "DEFORMATION_READY", "GAME_READY")
PROFILES = {
    "ASSET_FINAL": {
        "views": ("front", "side", "back", "three_quarter", "high_45", "low_45"),
        "checks": ("reference_proportions", "form_contacts", "protected_state"),
        "closeups": (),
    },
    "CHARACTER_FINAL": {
        "views": ("front", "side", "back", "three_quarter", "high_45", "low_45"),
        "checks": ("reference_proportions", "form_contacts", "protected_state"),
        "closeups": (),
    },
    "FACE_TRANSFER_FINAL": {
        "views": ("front", "side", "three_quarter", "high_45", "low_45"),
        "checks": ("face_identity", "seam_invisibility", "hair_occlusion", "uv_binding"),
        "closeups": ("face",),
    },
    "FOCUSED_3D_REPAIR": {
        "views": ("high_45", "low_45"),
        "checks": ("scope_result", "protected_state"),
        "closeups": ("changed_region",),
    },
}
CHECKER_LEVEL = "L1-METADATA_ONLY"
SHA = re.compile(r"[0-9a-f]{64}\Z")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def exact(value, fields, label):
    require(isinstance(value, dict) and set(value) == set(fields), label + ": missing or unknown fields")


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def verify_artifact(value, label, root=None, *, png_only=True):
    exact(value, ("path", "sha256"), label)
    name = value["path"]
    require(nonempty(name) and "\\" not in name and ":" not in name
            and not Path(name).is_absolute() and not PureWindowsPath(name).is_absolute()
            and not any(x in ("", ".", "..") or x.endswith((" ", ".")) for x in name.split("/")),
            label + ": invalid contained evidence path")
    require(not png_only or name.lower().endswith(".png"), label + ": visual evidence must be a PNG")
    require(isinstance(value["sha256"], str) and SHA.fullmatch(value["sha256"]),
            label + ": invalid sha256")
    if root is not None:
        base = Path(root).resolve(strict=True)
        dest = (base / name).resolve(strict=True)
        require(dest.is_relative_to(base) and dest.is_file(), label + ": missing/escaped evidence")
        require(hashlib.sha256(dest.read_bytes()).hexdigest() == value["sha256"],
                label + ": hash mismatch")


def review(row, label, evidence_ids, root=None):
    require(row["status"] in STATUSES, label + ": invalid status")
    require(isinstance(row["reviewer"], str) and nonempty(row["observations"]),
            label + ": observations required")
    evidence = row["evidence"]
    require(isinstance(evidence, list) and all(nonempty(x) and x in evidence_ids for x in evidence),
            label + ": evidence ids invalid")
    if row["status"] in ("PASS", "FAIL", "WARN"):
        require(nonempty(row["reviewer"]) and len(evidence) >= 1,
                label + ": reviewer and inspected evidence required")
    if row["status"] == "REVIEW_REQUIRED":
        require(evidence, label + ": captured image required for review")


def capture_setup(row, view):
    exact(row, ("target", "frame", "framing", "resolution", "mode",
                "lighting", "projection", "camera", "direction"), "setup")
    require(nonempty(row["target"]) and nonempty(row["framing"])
            and nonempty(row["lighting"]) and nonempty(row["camera"])
            and row["mode"] in ("solid", "material_preview", "rendered")
            and row["projection"] == "ORTHO", "invalid final fixed-view capture setup")
    require(type(row["frame"]) is int and
            isinstance(row["resolution"], list) and len(row["resolution"]) == 2
            and all(type(x) is int and 64 <= x <= 4096 for x in row["resolution"]),
            "invalid frame or resolution")
    d = row["direction"]
    require(isinstance(d, list) and len(d) == 3 and
            all(type(x) in (int, float) and math.isfinite(x) for x in d),
            "invalid camera direction")
    expected = {"high_45": (0, -1, 1), "low_45": (0, -1, -1)}
    if view in expected:
        target = expected[view]
        length = math.sqrt(sum(x*x for x in d))
        require(length > 0 and all(abs(d[i]/length-target[i]/math.sqrt(2)) < .015
                                   for i in range(3)),
                view + ": not a 45-degree front oblique")
    return row



CAPTURE_SETUP_V2 = ("target", "objects", "frame", "fps", "framing",
                    "resolution", "mode", "lighting", "projection",
                    "camera_matrix", "ortho_scale")
CANONICAL_DIRECTIONS = {
    "front": (0,-1,0), "side": (1,0,0), "back": (0,1,0),
    "three_quarter": (1,-1,.6), "high_45": (0,-1,1),
    "low_45": (0,-1,-1),
}


def setup_from_capture_metadata(metadata):
    """Build v2 setup from an actual Blender capture.json, never invented labels."""
    require(isinstance(metadata,dict) and metadata.get("ok") is True and
            metadata.get("status") == "VISUAL REVIEW REQUIRED" and
            metadata.get("capture_kind") == "viewport-oriented evidence render",
            "not a successful raw Blender capture manifest")
    require(metadata.get("view") in CANONICAL_DIRECTIONS,
            "capture manifest is not a supported fixed view")
    require(all(field in metadata for field in CAPTURE_SETUP_V2),
            "incomplete Blender capture metadata")
    setup={name:metadata[name] for name in CAPTURE_SETUP_V2}
    capture_setup_v2(setup, metadata["view"])
    return setup


def _numeric_equal(a,b):
    if isinstance(a,bool) or isinstance(b,bool):
        return a is b
    if isinstance(a,(int,float)) and isinstance(b,(int,float)):
        return math.isclose(a,b,rel_tol=1e-6,abs_tol=1e-5)
    if isinstance(a,list) and isinstance(b,list):
        return len(a)==len(b) and all(_numeric_equal(x,y) for x,y in zip(a,b))
    if isinstance(a,dict) and isinstance(b,dict):
        return a.keys()==b.keys() and all(_numeric_equal(a[k],b[k]) for k in a)
    return a == b


def capture_setup_v2(row,view):
    exact(row,CAPTURE_SETUP_V2,"capture setup v2")
    require(nonempty(row["target"]) and
            isinstance(row["objects"],list) and bool(row["objects"]) and
            all(nonempty(x) for x in row["objects"]) and
            len(row["objects"]) == len(set(row["objects"])) and
            row["mode"] in ("solid","material_preview","rendered") and
            nonempty(row["lighting"]) and row["projection"] == "ORTHO",
            "invalid capture v2 objects/mode/lighting/projection")
    def number(value):
        return type(value) in (int,float) and math.isfinite(value)
    require(number(row["frame"]) and number(row["fps"]) and row["fps"]>0
            and number(row["ortho_scale"]) and row["ortho_scale"]>0,
            "invalid frame/fps/ortho_scale")
    require(isinstance(row["resolution"],list) and
            len(row["resolution"])==2 and
            all(type(x) is int and 64<=x<=2048 for x in row["resolution"]),
            "invalid capture resolution")
    framing=row["framing"]
    exact(framing,("center","span"),"framing")
    require(isinstance(framing["center"],list) and len(framing["center"])==3
            and all(number(x) for x in framing["center"])
            and number(framing["span"]) and framing["span"]>0,
            "invalid capture framing")
    matrix=row["camera_matrix"]
    require(isinstance(matrix,list) and len(matrix)==16 and
            all(number(x) for x in matrix) and
            all(abs(x-y)<1e-4 for x,y in zip(matrix[12:],[0,0,0,1])),
            "invalid Blender camera matrix")
    if view in CANONICAL_DIRECTIONS:
        d=(matrix[2],matrix[6],matrix[10])  # camera local +Z in world
        target=CANONICAL_DIRECTIONS[view]
        norm=math.sqrt(sum(x*x for x in d))
        expected=math.sqrt(sum(x*x for x in target))
        require(norm>0 and all(abs(d[i]/norm-target[i]/expected)<.015
                              for i in range(3)),
                view+": camera matrix does not match declared view")
    return row


def compatible_setup(a,b):
    return _numeric_equal(a,b)

PRIMARY_CHECKS = ("primary_proportions", "primary_head_face", "primary_neck_shoulders",
                  "primary_torso_pelvis", "primary_silhouette")
FACE_MODES = {"GEOMETRY_ONLY", "DIRECT_FEATURE_TRANSFER", "RECONSTRUCT_THEN_LAYER",
              "HYBRID_PRESERVATION"}
USAGE_STATES = {"DISCOVERED", "READ", "SELECTED", "EXECUTED", "VERIFIED", "SKIPPED", "BLOCKED"}


def workflow_gate(packet, *, root=None, stage="FINAL"):
    """V3 extends this receipt, consuming existing PASS0 and transfer validators.

    A stage PASS is declared readiness for one operation, never artistic approval
    or a Python mutation sandbox. File verification is mandatory for readiness.
    """
    require(stage in ("FACE", "DETAIL", "FINAL"), "unknown workflow stage")
    w = packet["workflow"]
    exact(w, ("artifacts", "pass0", "face_strategy", "primary_assembly", "skill_usage"), "workflow")
    artifacts = w["artifacts"]
    require(isinstance(artifacts, dict) and artifacts, "workflow artifacts required")
    paths = set()
    for aid, artifact in artifacts.items():
        require(nonempty(aid), "empty workflow artifact id")
        verify_artifact(artifact, aid, root, png_only=False)
        require(artifact["path"].casefold() not in paths, "duplicate workflow artifact path")
        paths.add(artifact["path"].casefold())
    require(w["primary_assembly"] is None or
            isinstance(w["primary_assembly"], str) and w["primary_assembly"] in artifacts,
            "primary_assembly must be an artifact id or null")

    def refs(ids, label, *, required=False):
        require(isinstance(ids, list) and (bool(ids) or not required) and
                all(nonempty(x) and x in artifacts for x in ids) and
                len(ids) == len(set(ids)), label + ": invalid artifact ids")

    def artifact_path(aid, suffix):
        require(isinstance(aid, str) and aid in artifacts and
                artifacts[aid]["path"].lower().endswith(suffix), "missing " + suffix + " artifact")
        return Path(root) / artifacts[aid]["path"] if root is not None else None

    failures, blockers = [], []
    if root is None:
        blockers.append("workflow files not verified; use --verify-files")
    binding = w["pass0"]
    exact(binding, ("artifact", "contract_ref"), "PASS0 binding")
    exact(binding["contract_ref"], ("id", "revision", "sha256"), "contract_ref")
    require(nonempty(binding["contract_ref"]["id"]) and
            type(binding["contract_ref"]["revision"]) is int and binding["contract_ref"]["revision"] > 0 and
            isinstance(binding["contract_ref"]["sha256"], str) and
            SHA.fullmatch(binding["contract_ref"]["sha256"]), "invalid contract_ref")
    pass_path = artifact_path(binding["artifact"], ".json")
    design = None
    if pass_path is not None:
        spec = importlib.util.spec_from_file_location("qa_pass0", Path(__file__).resolve().parents[1] /
                    "skills/visual-reference-reconstruction/scripts/validate_pass0.py")
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        design = validator.load_packet(pass_path)
        errors = validator.validate(design, pass_path.parent, True)
        require(not errors, "PASS0: " + "; ".join(errors))
        require(design.get("schema_version") == 3 and design["gate"]["status"] != "BLOCKED",
                "workflow requires usable schema-3 PASS0")
        require(not validator.model_contract.validate_contract(design), "invalid Model Contract")
        require(binding["contract_ref"] == validator.model_contract.reference(design), "stale Model Contract binding")

    face = w["face_strategy"]
    exact(face, ("mode", "status", "reason", "source_ids", "identity_anchors", "occluded_regions",
                 "geometry_only_basis", "generation_required", "tools", "execution", "transfer"), "face strategy")
    mode = face["mode"]
    require(mode in FACE_MODES and face["status"] in ("SELECTED", "EXECUTED", "VERIFIED", "BLOCKED") and
            nonempty(face["reason"]), "invalid face strategy/status/reason")
    for key in ("source_ids", "identity_anchors"):
        require(isinstance(face[key], list) and face[key] and all(nonempty(x) for x in face[key]) and
                len(face[key]) == len(set(face[key])), "face needs unique " + key)
    if design is not None:
        sources = {x["id"]: x for x in design["sources"]}
        require(set(face["source_ids"]) <= set(design["source_of_truth"]) and
                all(sources[x]["role"] in ("PRIMARY", "SUPPORTING", "CANONICAL_CONCEPT") for x in face["source_ids"]),
                "face sources must be authoritative visual references")
        locked = validator.model_contract.claims(design)
        require(all(x in locked and locked[x]["certainty"] in ("CONFIRMED", "INFERRED", "CANONICAL", "REQUIRED")
                    for x in face["identity_anchors"]), "face identity anchors must reference supported PASS0 claims")
    require(type(face["generation_required"]) is bool, "generation_required must be boolean")
    reconstruct = mode in ("RECONSTRUCT_THEN_LAYER", "HYBRID_PRESERVATION")
    require(face["generation_required"] == reconstruct, "generation requirement contradicts selected face strategy")
    require(face["geometry_only_basis"] in ("VOLUME_IDENTITY", "USER_APPROVED_SIMPLIFICATION", "NOT_APPLICABLE"),
            "invalid geometry-only basis; graphic identity cannot be waived")
    require((mode == "GEOMETRY_ONLY") == (face["geometry_only_basis"] != "NOT_APPLICABLE"),
            "geometry-only needs reviewed volume identity or user-approved simplification")
    require(isinstance(face["occluded_regions"], list), "occluded_regions must be a list")
    names = set()
    for region in face["occluded_regions"]:
        exact(region, ("name", "visibility", "certainty", "treatment"), "occluded region")
        require(nonempty(region["name"]) and region["name"] not in names and
                region["visibility"] in ("PARTIAL", "OCCLUDED") and
                region["certainty"] in ("INFERRED", "SPECULATIVE") and
                region["treatment"] in ("KEEP_OCCLUDED", "RECONSTRUCT", "PROVISIONAL_GEOMETRY"),
                "invalid/duplicate occluded region; hidden detail cannot be CONFIRMED")
        names.add(region["name"])
    refs(face["execution"], "face execution", required=face["status"] in ("EXECUTED", "VERIFIED"))
    if face["status"] in ("EXECUTED", "VERIFIED"):
        if mode == "GEOMETRY_ONLY":
            require(any(artifacts[x]["path"].lower().endswith(".blend") for x in face["execution"]),
                    "geometry execution needs saved Blender state")
        else:
            require(face["transfer"] in face["execution"], "face execution must cite the selected transfer record")
    require(isinstance(face["tools"], list), "face tools must be a list")
    tool_names = set()
    for tool in face["tools"]:
        exact(tool, ("name", "availability", "reason", "execution"), "face tool")
        require(nonempty(tool["name"]) and tool["name"] not in tool_names and nonempty(tool["reason"]) and
                tool["availability"] in ("AVAILABLE", "UNAVAILABLE", "UNCHECKED"), "invalid tool availability")
        tool_names.add(tool["name"])
        refs(tool["execution"], "tool execution")
        require(not tool["execution"] or tool["availability"] == "AVAILABLE", "unavailable tool cannot claim execution")
        if tool["availability"] != "AVAILABLE":
            blockers.append("required face tool " + tool["name"] + " " + tool["availability"])
    generator = next((x for x in face["tools"] if x["name"] == "imagegen"), None)
    if reconstruct:
        require(generator is not None, "reconstruction needs an ImageGen availability check")
        require(all(artifacts[x]["path"].lower().endswith(".png") for x in generator["execution"]),
                "ImageGen execution needs image outputs")
        if stage == "FINAL" and not generator["execution"]:
            blockers.append("selected reconstruction has no actual ImageGen output")
    if face["status"] == "BLOCKED" or stage == "FINAL" and face["status"] not in ("EXECUTED", "VERIFIED"):
        blockers.append("face strategy not executed: " + face["status"])
    if mode == "GEOMETRY_ONLY":
        require(face["transfer"] is None, "geometry-only cannot claim a transfer")
    elif face["transfer"] is not None:
        transfer_path = artifact_path(face["transfer"], ".json")
        if transfer_path is not None:
            import surface_transfer
            record = validator.load_packet(transfer_path)
            surface_transfer.validate(record, transfer_path.parent)
            expected = {"DIRECT_FEATURE_TRANSFER": "DIRECT", "RECONSTRUCT_THEN_LAYER": "RECONSTRUCT_THEN_LAYER",
                        "HYBRID_PRESERVATION": "HYBRID"}[mode]
            require(record.get("schema_version") == 2 and record["face_strategy"]["mode"] == expected,
                    "transfer strategy differs from selected face method")
            if design is not None:
                require(record["artifacts"][record["source"]["artifact"]]["sha256"] in
                        {sources[x]["sha256"] for x in face["source_ids"]}, "transfer source differs from canonical face source")
            if reconstruct and stage == "FINAL" and generator["execution"]:
                output_hashes = {artifacts[x]["sha256"] for x in generator["execution"]}
                require(all(record["artifacts"][s["output"]]["sha256"] in output_hashes for s in record["steps"]
                            if s["operation"] == "regenerate"), "ImageGen outputs do not match reconstruction lineage")
            if stage == "FINAL":
                for name in ("identity", "seams", "material", "reopen"):
                    if record["qa"][name]["status"] != "PASS":
                        (failures if record["qa"][name]["status"] == "FAIL" else blockers).append("transfer QA not accepted: " + name)
                if record["bake"]["status"] == "PENDING" or record["seam_cleanup"]["status"] == "PENDING":
                    blockers.append("transfer bake/seam integration pending")
    elif stage == "FINAL":
        blockers.append("selected face transfer has no executed transfer record")

    usage = w["skill_usage"]
    require(isinstance(usage, list) and usage, "skill usage evidence required")
    seen = {}
    for row in usage:
        exact(row, ("id", "status", "reason", "execution", "verification"), "skill usage")
        require(nonempty(row["id"]) and row["id"] not in seen and row["status"] in USAGE_STATES and
                nonempty(row["reason"]), "invalid/duplicate skill usage")
        seen[row["id"]] = row
        executed = row["status"] in ("EXECUTED", "VERIFIED")
        refs(row["execution"], "skill execution", required=executed)
        require(executed or not row["execution"], "reading/selecting a skill is not execution")
        require(isinstance(row["verification"], list) and all(nonempty(x) and x in packet["checks"]
                for x in row["verification"]), "invalid skill verification checks")
        if row["status"] == "VERIFIED":
            require(row["verification"] and all(packet["checks"][x]["status"] == "PASS" for x in row["verification"]),
                    "VERIFIED skill requires accepted review evidence")
    required_skills = ["visual-reference-reconstruction", "blender-character-modeling"]
    if mode != "GEOMETRY_ONLY":
        required_skills.append("blender-reference-surface-transfer")
    if stage == "FINAL":
        for name in required_skills:
            if name not in seen or seen[name]["status"] not in ("EXECUTED", "VERIFIED"):
                blockers.append("required procedure not executed: " + name)
            else:
                output = seen[name]["execution"]
                if name == "visual-reference-reconstruction":
                    require(binding["artifact"] in output, "reconstruction execution must cite PASS0")
                elif name == "blender-reference-surface-transfer":
                    require(face["transfer"] in output, "transfer execution must cite its actual record")
                else:
                    require(any(artifacts[x]["path"].lower().endswith(".blend") for x in output),
                            "character execution needs saved Blender state")
    if stage in ("DETAIL", "FINAL"):
        assembly_path = artifact_path(w["primary_assembly"], ".json") if w["primary_assembly"] is not None else None
        if w["primary_assembly"] is None:
            blockers.append("primary forms need the existing assembly graph checkpoint")
        elif assembly_path is not None:
            assembly = validator.load_packet(assembly_path)
            result = validator.model_contract.verify_assembly(design, assembly, "MACRO")
            if result["status"] != "PASS":
                failures.append("primary Model Contract checkpoint not accepted: " + result["status"])
        for name in PRIMARY_CHECKS:
            if name not in packet["checks"] or packet["checks"][name]["status"] != "PASS":
                (failures if packet["checks"].get(name, {}).get("status") == "FAIL" else blockers).append("primary form not accepted: " + name)
            else:
                evidence = {x["id"]: x for x in (*packet["captures"], *packet["closeups"])}
                if not any(evidence[x]["phase"] == "AFTER" and evidence[x]["image"] is not None and
                           evidence[x]["status"] == "PASS" for x in packet["checks"][name]["evidence"]):
                    blockers.append("primary review lacks accepted current image: " + name)
        for view in ("front", "side", "three_quarter"):
            rows = [x for x in packet["captures"] if x["view"] == view and x["phase"] == "AFTER"]
            if len(rows) != 1 or rows[0]["status"] != "PASS":
                blockers.append("primary forms need an accepted current " + view + " view")
    if stage == "FINAL":
        needed = ["face_identity"]
        if face["occluded_regions"]:
            needed.append("hair_occlusion")
        if mode != "GEOMETRY_ONLY":
            needed.extend(("seam_invisibility", "uv_binding"))
        for name in needed:
            if name not in packet["checks"] or packet["checks"][name]["status"] != "PASS":
                (failures if packet["checks"].get(name, {}).get("status") == "FAIL" else blockers).append("face criterion not accepted: " + name)
    return failures, blockers


def validate(packet, *, root=None, stage="FINAL", mode="STANDARD"):
    require(isinstance(packet, dict), "qa packet must be an object")
    version = packet.get("schema_version")
    fields = ("schema_version", "asset", "profile", "changed",
                   "animated", "requested_capabilities", "captures", "closeups",
                   "checks", "protected_zones", "user_flags", "capabilities",
                   "escalation")
    extensions = ("dual_verification",) if "dual_verification" in packet else ()
    exact(packet, (*fields, "workflow", *extensions) if version == 3 else (*fields, *extensions), "qa packet")
    require(mode in ("STANDARD", "ARTISTIC_REVIEW"), "unsupported verification mode")
    require(mode != "ARTISTIC_REVIEW" or extensions, "ARTISTIC_REVIEW requires dual_verification")
    require(type(version) is int and version in (1,2,3),
            "unsupported QA schema")
    require(stage in ("FACE", "DETAIL", "FINAL") and (version == 3 or stage == "FINAL"),
            "stage gating requires QA schema 3")
    require(nonempty(packet["asset"]) and packet["profile"] in PROFILES,
            "missing asset / invalid profile")
    require(type(packet["changed"]) is bool and type(packet["animated"]) is bool,
            "changed/animated must be boolean")
    wanted = packet["requested_capabilities"]
    require(isinstance(wanted, list) and bool(wanted) and len(wanted)==len(set(wanted))
            and set(wanted) <= set(CAPABILITIES), "invalid requested capabilities")
    required = PROFILES[packet["profile"]]
    captures = {}
    phases = ("BEFORE", "AFTER") if packet["changed"] else ("AFTER",)
    blockers, failures = [], []
    final_blockers, final_failures = [], []

    for item in packet["captures"]:
        exact(item, ("id", "view", "phase", "status", "image",
                     "setup", "reviewer", "observations"), "capture")
        require(nonempty(item["id"]) and item["id"] not in captures, "duplicate capture id")
        require(item["view"] in (*required["views"], "front", "side", "back",
                                 "three_quarter", "high_45", "low_45"), "unsupported view")
        require(item["phase"] in phases, "unexpected capture phase")
        (capture_setup_v2(item["setup"], item["view"]) if version>=2
         else capture_setup(item["setup"], item["view"]))
        require(item["status"] in STATUSES and nonempty(item["observations"])
                and isinstance(item["reviewer"], str), "invalid capture review")
        if item["status"] != "SKIP":
            verify_artifact(item["image"], item["id"], root)
        else:
            require(item["image"] is None, "SKIP cannot imply captured image")
        if item["status"] in ("PASS", "FAIL", "WARN"):
            require(nonempty(item["reviewer"]) and item["image"] is not None,
                    "inspected capture requires reviewer/image")
        captures[item["id"]] = item
        if item["status"] == "FAIL":
            failures.append("failed captured view " + item["id"])

    for view in required["views"]:
        for phase in phases:
            selected = [x for x in captures.values() if x["view"]==view and x["phase"]==phase]
            if len(selected) != 1:
                final_blockers.append("missing or duplicate " + phase + " view " + view)
                continue
            item = selected[0]
            if item["status"] != "PASS":
                (final_failures if item["status"]=="FAIL" else final_blockers).append(
                    view + " " + phase + " not visually accepted ("+item["status"]+")")
        if packet["changed"]:
            before = next((x for x in captures.values() if x["view"]==view and x["phase"]=="BEFORE"), None)
            after = next((x for x in captures.values() if x["view"]==view and x["phase"]=="AFTER"), None)
            if before and after and not compatible_setup(before["setup"],after["setup"]):
                failures.append("non-comparable BEFORE/AFTER setup for " + view)

    closeups={}
    for item in packet["closeups"]:
        exact(item, ("id", "region", "phase", "status", "image", "setup",
                     "reviewer", "observations"), "closeup")
        require(nonempty(item["id"]) and item["id"] not in captures and
                item["id"] not in closeups and nonempty(item["region"]) and
                item["phase"] in phases, "invalid closeup id/phase/region")
        (capture_setup_v2(item["setup"], None) if version>=2
         else capture_setup(item["setup"], "front"))
        require(item["status"] in STATUSES and isinstance(item["reviewer"], str)
                and nonempty(item["observations"]), "invalid closeup review")
        if item["status"] != "SKIP":
            verify_artifact(item["image"], item["id"], root)
        else:
            require(item["image"] is None, "SKIP closeup cannot claim image")
        if item["status"] in ("PASS", "FAIL", "WARN"):
            require(nonempty(item["reviewer"]), "closeup needs reviewer")
        closeups[item["id"]]=item
        if item["status"] == "FAIL":
            failures.append("failed closeup " + item["id"])
    for region in required["closeups"]:
        for phase in phases:
            rows=[x for x in closeups.values() if x["region"]==region and x["phase"]==phase]
            if len(rows)!=1 or rows[0]["status"]!="PASS":
                final_blockers.append("missing/unreviewed " + phase + " closeup of "+region)
        if packet["changed"]:
            x=next((x for x in closeups.values() if x["region"]==region and x["phase"]=="BEFORE"),None)
            y=next((x for x in closeups.values() if x["region"]==region and x["phase"]=="AFTER"),None)
            if x and y and not compatible_setup(x["setup"],y["setup"]):
                failures.append("non-comparable closeup "+region)

    evidence_ids = set(captures)|set(closeups)
    checks = packet["checks"]
    require(isinstance(checks, dict), "checks must be a named map")
    for name,row in checks.items():
        require(nonempty(name), "empty check name")
        exact(row, ("status", "reviewer", "observations", "evidence"), name)
        review(row, name, evidence_ids)
        if row["status"] == "FAIL":
            failures.append("failed named criterion " + name)
    for name in required["checks"]:
        if name not in checks:
            final_blockers.append("missing required check "+name)
        elif checks[name]["status"]!="PASS":
            (final_failures if checks[name]["status"]=="FAIL" else final_blockers).append(
                name+" not accepted ("+checks[name]["status"]+")")
    zone_ids=set()
    for zone in packet["protected_zones"]:
        exact(zone, ("id", "status", "reviewer", "observations", "evidence"), "protected zone")
        require(nonempty(zone["id"]) and zone["id"] not in zone_ids, "empty/duplicate protected zone")
        zone_ids.add(zone["id"])
        review(zone, zone["id"], evidence_ids)
        if zone["status"] != "PASS":
            (failures if zone["status"]=="FAIL" else blockers).append("protected zone not passed "+zone["id"])
    flag_ids=set()
    for flag in packet["user_flags"]:
        exact(flag, ("id", "action", "status", "reviewer", "observations", "evidence"), "user flag")
        require(nonempty(flag["id"]) and flag["id"] not in flag_ids and
                flag["action"] in ("MUST_FIX", "PRESERVE", "DO_NOT_REINTERPRET"),
                "invalid or duplicate user flag/action")
        flag_ids.add(flag["id"])
        review(flag, flag["id"], evidence_ids)
        if flag["status"] != "PASS":
            (failures if flag["status"]=="FAIL" else blockers).append("user flag unresolved "+flag["id"])

    cap=packet["capabilities"]
    exact(cap, CAPABILITIES, "capabilities")
    for name, row in cap.items():
        exact(row, ("status", "reviewer", "observations", "evidence"), "capability "+name)
        require(row["status"] in (*STATUSES, "NOT_APPLICABLE"), "invalid capability status")
        require(nonempty(row["observations"]) and isinstance(row["reviewer"], str)
                and isinstance(row["evidence"],list)
                and all(isinstance(v,str) and v in checks for v in row["evidence"]),
                "invalid capability evidence")
        if row["status"]=="PASS":
            require(nonempty(row["reviewer"]) and row["evidence"], "capability PASS needs reviewed checks")
        if name in wanted and row["status"]!="PASS":
            (final_failures if row["status"]=="FAIL" else final_blockers).append(
                "requested capability not PASS: "+name+" ("+row["status"]+")")
        if row["status"] == "PASS" and any(checks[x]["status"] != "PASS" for x in row["evidence"]):
            (final_failures if any(checks[x]["status"] == "FAIL" for x in row["evidence"]) else final_blockers).append(
                "capability PASS cites unaccepted checks: " + name)
    if cap["STATIC_VISUAL"]["status"]=="PASS" and (failures or blockers or final_failures or final_blockers):
        final_blockers.append("STATIC_VISUAL claimed PASS with unresolved required visual coverage")
    if cap["GAME_READY"]["status"]=="PASS":
        for upstream in ("STATIC_VISUAL","EXPORT"):
            if cap[upstream]["status"]!="PASS":
                final_failures.append("GAME_READY requires "+upstream+" PASS")
        if "engine_preview" not in checks or checks["engine_preview"]["status"]!="PASS":
            final_failures.append("GAME_READY needs inspected engine_preview")
        if packet["animated"]:
            for upstream in ("RIG_READY","DEFORMATION_READY"):
                if cap[upstream]["status"]!="PASS":
                    final_failures.append("animated GAME_READY requires "+upstream+" PASS")
            if "animation_playback" not in checks or checks["animation_playback"]["status"]!="PASS":
                final_failures.append("animated GAME_READY needs actual animation_playback")

    require(isinstance(packet["escalation"],list), "escalation list required")
    for item in packet["escalation"]:
        extra = ("checkpoint", "previous_method", "next_method", "evidence") if version == 3 else ()
        exact(item, ("issue","attempts","state","owner","note", *extra),"escalation")
        require(nonempty(item["issue"]) and type(item["attempts"]) is int and
                item["attempts"] >= 1 and item["state"] in ("RESOLVED","ESCALATED") and
                nonempty(item["owner"]) and nonempty(item["note"]),
                "invalid escalation")
        if version == 3 and item["attempts"] >= 2:
            checkpoint = item["checkpoint"]
            require(isinstance(checkpoint, str) and checkpoint in packet["workflow"]["artifacts"] and
                    packet["workflow"]["artifacts"][checkpoint]["path"].lower().endswith(".blend"),
                    "two failed attempts require a saved Blender checkpoint")
            require(nonempty(item["previous_method"]) and nonempty(item["next_method"]) and
                    item["previous_method"].strip().casefold() != item["next_method"].strip().casefold(),
                    "two failed attempts require strategy reconsideration")
            require(isinstance(item["evidence"], list) and item["evidence"] and
                    all(x in checks for x in item["evidence"]), "reconsideration needs reviewed checks")
            if item["state"] == "RESOLVED":
                require(all(checks[x]["status"] == "PASS" for x in item["evidence"]), "unreviewed resolution")
        if item["state"]=="ESCALATED":
            blockers.append("persistent defect escalated: "+item["issue"])

    if version == 3:
        wf_failures, wf_blockers = workflow_gate(packet, root=root, stage=stage)
        failures.extend(wf_failures); blockers.extend(wf_blockers)
    elif packet["profile"] == "CHARACTER_FINAL" and "face_identity" in checks and checks["face_identity"]["status"] != "PASS":
        (failures if checks["face_identity"]["status"] == "FAIL" else blockers).append("declared face identity not accepted")
    if stage == "FINAL":
        failures.extend(final_failures); blockers.extend(final_blockers)
    status = "FAIL" if failures else ("OPEN" if blockers else "PASS")
    result = {
        "structure": "PASS", "gate":status, "profile":packet["profile"],
        "stage":stage, "workflow":"RECORDED" if version == 3 else "NOT_RECORDED_LEGACY",
        "visual":"NOT_EVALUATED", "final_coverage":"CHECKED" if stage == "FINAL" else "NOT_CHECKED",
        "failures":failures,"blockers":blockers,
        "limits":"L1 provenance and declared coverage only. File hashes do not prove inspected visual quality; human/agent review of actual images and scene is necessary."
    }
    if extensions:
        import qa_artistic
        dual = qa_artistic.evaluate(packet["dual_verification"], packet, root=root, verify_artifact=verify_artifact)
        result["mode"] = mode
        result["evidence_gate"] = status
        result["dual_verification"] = {k:v for k,v in dual.items() if k != "critic_packet"}
        if status == "FAIL" or dual["TECHNICAL_QA"] == "FAIL" or dual["artistic_gate"] == "FAIL":
            result["gate"] = "FAIL"
        elif status != "PASS" or dual["TECHNICAL_QA"] != "PASS" or dual["artistic_gate"] != "PASS":
            result["gate"] = "OPEN"
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet",type=Path)
    parser.add_argument("--verify-files",action="store_true")
    parser.add_argument("--stage", choices=("FACE", "DETAIL", "FINAL"), default="FINAL")
    parser.add_argument("--mode", choices=("STANDARD", "ARTISTIC_REVIEW"), default="STANDARD")
    parser.add_argument("--critic-packet", action="store_true", help="Emit blind objective packet; does not dispatch a critic")
    args=parser.parse_args()
    try:
        def unique_pairs(items):
            out={}
            for key,value in items:
                if key in out:
                    raise ValueError("duplicate JSON key: "+key)
                out[key]=value
            return out
        packet=json.loads(args.packet.read_text(encoding="utf-8-sig"),
                          object_pairs_hook=unique_pairs,
                          parse_constant=lambda x: (_ for _ in ()).throw(ValueError("non-finite JSON constant "+x)))
        if args.critic_packet:
            import copy
            import qa_artistic
            require(args.verify_files and "dual_verification" in packet, "critic packet requires dual receipt and --verify-files")
            draft=copy.deepcopy(packet)
            draft["dual_verification"]["artistic"]=None
            validate(draft, root=args.packet.parent, stage=args.stage, mode="ARTISTIC_REVIEW")
            images={x["id"]:x for x in draft["captures"]+draft["closeups"]}
            dual=qa_artistic.evaluate(draft["dual_verification"],draft,root=args.packet.parent,verify_artifact=verify_artifact)
            print(json.dumps(dict(packet_sha256=dual["packet_sha256"],packet=dual["critic_packet"])))
            return 0 if not dual["requests"] else 2
        result=validate(packet,root=args.packet.parent if args.verify_files else None, stage=args.stage, mode=args.mode)
    except (OSError,ValueError,TypeError,KeyError) as error:
        print(json.dumps({"structure":"FAIL","gate":"FAIL","error":str(error)}))
        return 1
    print(json.dumps(result))
    return 0 if result["gate"]=="PASS" else 2


if __name__=="__main__":
    raise SystemExit(main())
