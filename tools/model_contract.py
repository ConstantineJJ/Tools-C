"""Persistent PASS0 design constraints and bounded checkpoint verification (stdlib).

Reads declared observations, not pixels. PASS is agreement with reviewed evidence,
not automatic visual/engineering certification. Contract lives only in pass0.json.
"""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path

LEVELS = {"HARD INVARIANT", "PROPORTION LOCK", "SOFT CANONICAL"}
CHECKPOINTS = {"VIEWS", "MACRO", "MECHANICS", "GEOMETRY", "FINAL"}
SUPPORTED = {"REQUIRED", "CANONICAL", "CONFIRMED", "INFERRED"}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    allow_nan=False, separators=(",", ":")).encode()).hexdigest()


def claims(packet):
    rows = packet.get("constraints", []) + packet.get("relative_dimensions", []) + packet.get("silhouette_notes", []) + packet.get("relationships", [])
    for c in packet.get("components", []):
        rows += c.get("claims", [])
    return {r["id"]: r for r in rows if isinstance(r, dict) and isinstance(r.get("id"), str)}


def identity(packet):
    """Hash one existing graph, without duplicating it in a second manifest."""
    def supported(rows):
        return [r for r in rows if r.get("certainty") in SUPPORTED]
    return dict(mode=packet.get("mode", "REFERENCE"),
                sources=[s for s in packet.get("sources", []) if s.get("id") in packet.get("source_of_truth", [])],
                proportion_basis=packet.get("proportion_basis"), constraints=packet.get("constraints", []),
                components=[{k: v for k, v in c.items() if k != "claims"} | {"claims": supported(c.get("claims", []))}
                            for c in packet.get("components", []) if c.get("certainty") != "SPECULATIVE"],
                relative_dimensions=supported(packet.get("relative_dimensions", [])),
                silhouette_notes=supported(packet.get("silhouette_notes", [])),
                relationships=supported(packet.get("relationships", [])),
                hero={k: packet.get("identity_lock", {}).get(k) for k in ("source_id", "sha256", "version")})


def fingerprint(packet):
    contract = {k: v for k, v in packet["model_contract"].items() if k != "sha256"}
    return digest(dict(identity=identity(packet), contract=contract))


def reference(packet):
    c = packet["model_contract"]
    return {k: c[k] for k in ("id", "revision", "sha256")}


def expected(packet, rule):
    """Selectors resolve existing data; only new ratio/tolerance policy is in rules."""
    components = {c["id"]: c for c in packet["components"]}
    cs = claims(packet)
    kind = rule["kind"]
    if kind in {"count", "hierarchy", "symmetry"}:
        return components[rule["target_id"]][{"count": "count", "hierarchy": "parent_id", "symmetry": "symmetry"}[kind]]
    if kind in {"claim", "relationship", "anchor"}:
        row = cs[rule["target_id"]]
        if kind == "relationship":
            return {k: row[k] for k in ("from_component", "to_component", "relationship", "value")}
        return row["value"]
    if kind == "dimension":
        row = cs[rule["target_id"]]
        return [row["min"], row["max"]]
    if kind == "ratio":
        # IDs must resolve even though the reviewed, tighter bound is explicit.
        cs[rule["numerator_id"]]; cs[rule["denominator_id"]]
        return rule["bounds"]
    raise ValueError("Unknown constraint kind")


def validate_contract(packet):
    errors = []
    def need(ok, message):
        if not ok: errors.append("MODEL_CONTRACT: " + message)
    c = packet.get("model_contract")
    if not isinstance(c, dict): return ["MODEL_CONTRACT: missing persistent contract; review and seal before Blender"]
    try:
        need(type(c.get("schema_version")) is int and c["schema_version"] == 1 and c.get("status") == "LOCKED", "unsupported/unlocked contract")
        need(isinstance(c.get("id"), str) and bool(c["id"].strip()), "missing id")
        need(type(c.get("revision")) is int and c["revision"] > 0, "invalid revision")
        need(bool(c.get("reviewer")) and bool(c.get("reason")), "missing lock reviewer/reason")
        components = {r["id"]: r for r in packet["components"]}
        for cid, comp in components.items():
            parent = comp.get("parent_id")
            need("parent_id" in comp and (parent is None or parent in components), "unknown/missing parent: " + cid)
            need(isinstance(comp.get("symmetry"), dict) and comp["symmetry"].get("type") in {"NONE", "BILATERAL", "RADIAL", "REPEAT", "UNKNOWN"}, "symmetry needs explicit state: " + cid)
            visited = {cid}
            while parent in components:
                need(parent not in visited, "hierarchy cycle: " + cid)
                if parent in visited: break
                visited.add(parent); parent = components[parent].get("parent_id")
        cs = claims(packet); rules = c.get("rules")
        need(isinstance(rules, list) and bool(rules), "no constraints")
        ids, counts, proportions, targets = set(), set(), set(), set()
        for r in rules or []:
            rid = r["id"]; need(isinstance(rid, str) and bool(rid.strip()) and rid not in ids, "missing/duplicate rule id"); ids.add(rid)
            level, kind = r["level"], r["kind"]
            need(level in LEVELS, "invalid level: " + rid)
            checkpoints = r.get("checkpoints")
            need(isinstance(checkpoints, list) and bool(checkpoints) and set(checkpoints) <= CHECKPOINTS and len(set(checkpoints)) == len(checkpoints), "invalid checkpoints: " + rid)
            need(bool(r.get("basis")), "missing tolerance/authority basis: " + rid)
            value = expected(packet, r)
            if kind in {"claim", "relationship", "anchor", "dimension"}:
                target = cs[r["target_id"]]; targets.add(r["target_id"])
                need(target.get("certainty") in SUPPORTED or level == "SOFT CANONICAL", "speculative geometry cannot be locked: " + rid)
                if target.get("certainty") == "REQUIRED": need(level == "HARD INVARIANT", "REQUIRED cannot be softened: " + rid)
                if target.get("critical") is True: need(level != "SOFT CANONICAL", "critical relationship/anchor cannot be softened: " + rid)
            if kind == "count":
                counts.add(r["target_id"])
                need(level == "HARD INVARIANT" and set(checkpoints) == CHECKPOINTS, "counts must persist at all significant checkpoints: " + rid)
                need(components[r["target_id"]].get("certainty") != "SPECULATIVE", "speculative component count cannot be locked")
                need(type(value) is int and value > 0, "count must be a positive integer: " + rid)
            if kind in {"dimension", "ratio", "anchor"}:
                need(level == "PROPORTION LOCK", "geometry anchors need PROPORTION LOCK: " + rid)
                need({"VIEWS", "MACRO", "GEOMETRY", "FINAL"} <= set(checkpoints), "proportions need meaningful checkpoints: " + rid)
                need(isinstance(r.get("unit"), str) and bool(r["unit"]), "missing measurement unit: " + rid)
                if kind != "anchor":
                    need(isinstance(value, list) and len(value) == 2 and all(type(v) in {int, float} and math.isfinite(v) for v in value) and 0 < value[0] <= value[1], "invalid bounds: " + rid)
                else:
                    need(isinstance(value, list) and bool(value) and all(type(v) in {int, float} and math.isfinite(v) for v in value), "invalid anchor coordinates: " + rid)
                    need(type(r.get("tolerance")) in {int, float} and math.isfinite(r["tolerance"]) and r["tolerance"] >= 0, "invalid anchor tolerance: " + rid)
                if kind == "dimension": proportions.add(r["target_id"])
                if kind == "ratio":
                    dims = {d["id"]: d for d in packet["relative_dimensions"]}
                    a, b = dims[r["numerator_id"]], dims[r["denominator_id"]]
                    need(a.get("certainty") in SUPPORTED and b.get("certainty") in SUPPORTED and a["unit"] == b["unit"] and r["unit"] == "ratio", "invalid ratio lineage/unit: " + rid)
                    need(value[0] >= a["min"] / b["max"] - 1e-9 and value[1] <= a["max"] / b["min"] + 1e-9, "ratio exceeds authoritative envelopes: " + rid)
                elif kind == "dimension": need(r["unit"] == cs[r["target_id"]]["unit"], "dimension unit mismatch: " + rid)
            completeness = r.get("view_completeness")
            if completeness is not None:
                need(isinstance(completeness, dict) and completeness.get("required") is True and bool(completeness.get("basis")) and bool(completeness.get("source_ids")) and set(completeness["source_ids"]) <= set(packet["source_of_truth"]), "invalid VIEW COMPLETENESS provenance: " + rid)
        need(counts == {cid for cid, comp in components.items() if comp.get("certainty") != "SPECULATIVE"}, "every established component needs a count invariant")
        need(proportions >= {d["id"] for d in packet["relative_dimensions"] if d.get("certainty") in SUPPORTED}, "key dimension missing proportion lock")
        for cid, row in cs.items():
            if row.get("certainty") == "REQUIRED" and row.get("target") != "count":
                need(cid in targets, "REQUIRED property missing hard rule: " + cid)
            if row.get("critical") is True: need(cid in targets, "critical relationship/anchor missing rule: " + cid)
        if c.get("revision", 0) > 1:
            need(isinstance(c.get("supersedes_sha256"), str) and len(c["supersedes_sha256"]) == 64 and bool(c.get("change_note")), "revision needs predecessor hash and explicit change note")
        need(c.get("sha256") == fingerprint(packet), "design drift from locked hash; explicit revision required")
    except (KeyError, TypeError, ValueError, OverflowError, AttributeError, IndexError) as exc:
        errors.append("MODEL_CONTRACT: malformed graph/rule: " + str(exc))
    return errors


def seal(packet, *, previous=None):
    """Seal only a reviewed definition. Never infer rules or widen tolerances."""
    c = packet["model_contract"]
    candidate = copy.deepcopy(packet)
    candidate["model_contract"]["sha256"] = fingerprint(candidate)
    errors = validate_contract(candidate)
    if errors: raise ValueError("; ".join(errors))
    if previous is not None:
        if validate_contract(previous): raise ValueError("Invalid predecessor contract")
        old = previous["model_contract"]
        if c["id"] != old["id"] or c["revision"] != old["revision"] + 1 or c.get("supersedes_sha256") != old["sha256"]:
            raise ValueError("Explicit revision must name immediate predecessor")
        if digest(previous.get("constraints", [])) != digest(packet.get("constraints", [])):
            old_brief = [s["sha256"] for s in previous["sources"] if s["role"] == "BRIEF"]
            new_brief = [s["sha256"] for s in packet["sources"] if s["role"] == "BRIEF"]
            if old_brief == new_brief or c.get("requirement_change_authority") != "USER":
                raise ValueError("REQUIRED change needs explicit USER authority and revised brief bytes")
    elif c.get("revision") != 1:
        raise ValueError("Revision requires predecessor packet")
    elif c.get("sha256") and c["sha256"] != candidate["model_contract"]["sha256"]:
        raise ValueError("Already locked: changed design needs explicit revision and predecessor")
    c["sha256"] = candidate["model_contract"]["sha256"]
    return reference(packet)


def verify_observations(packet, checkpoint, observations):
    """Every selected rule is covered once; UNKNOWN never authorizes lower truth."""
    errors = validate_contract(packet)
    if checkpoint not in CHECKPOINTS: errors.append("Unknown checkpoint")
    if errors: return dict(status="FAIL", errors=errors, checks=[])
    selected = {r["id"]: r for r in packet["model_contract"]["rules"] if checkpoint in r["checkpoints"]}
    checks, seen = [], set()
    if not isinstance(observations, list): return dict(status="FAIL", errors=["Observations must be a list"], checks=[])
    for obs in observations:
        if not isinstance(obs, dict) or obs.get("rule_id") not in selected or obs.get("rule_id") in seen:
            errors.append("Unknown/duplicate observation rule"); continue
        rid = obs["rule_id"]; seen.add(rid); rule = selected[rid]
        status, reason = "PASS", "within locked design"
        if not obs.get("method") or not obs.get("evidence"):
            status, reason = "UNKNOWN", "missing measurement/review evidence"
        elif checkpoint == "VIEWS" and rule.get("view_completeness") and obs.get("completeness") == "CROPPED":
            status, reason = "FAIL", "VIEW COMPLETENESS: known geometry is cropped; never shorten it"
        elif obs.get("state") != "MEASURED" or (checkpoint == "VIEWS" and rule.get("view_completeness") and obs.get("completeness") != "FULL"):
            status, reason = "UNKNOWN", "occluded/foreshortened/missing; authoritative geometry still wins"
        else:
            actual, want, kind = obs.get("value"), expected(packet, rule), rule["kind"]
            if kind in {"dimension", "ratio", "anchor"}:
                if obs.get("unit") != rule["unit"]:
                    status, reason = "UNKNOWN", "incomparable unit/projection/pose"
                elif kind == "anchor":
                    if not isinstance(actual, list) or len(actual) != len(want) or any(type(a) not in {int, float} or not math.isfinite(a) for a in actual):
                        status, reason = "UNKNOWN", "invalid measured anchor"
                    elif any(abs(a - w) > rule["tolerance"] + 1e-9 for a, w in zip(actual, want)):
                        status, reason = "FAIL", "silhouette anchor outside tolerance"
                else:
                    dims = {d["id"]: d for d in packet["relative_dimensions"]}
                    dim = dims[rule["target_id"] if kind == "dimension" else rule["numerator_id"]]
                    comp = next(c for c in packet["components"] if c["id"] == dim["component_id"])
                    samples = obs.get("instance_values")
                    if comp["count"] > 1 and (not isinstance(samples, dict) or len(samples) != comp["count"]):
                        status, reason = "UNKNOWN", "measure every physical instance; averages cannot hide drift"
                    else:
                        values = list(samples.values()) if isinstance(samples, dict) else [actual]
                        if not values or any(type(a) not in {int, float} or not math.isfinite(a) for a in values):
                            status, reason = "UNKNOWN", "invalid measurement"
                        elif any(not want[0] - 1e-9 <= a <= want[1] + 1e-9 for a in values):
                            status, reason = "FAIL", "proportion outside locked envelope"
            elif type(actual) is not type(want) or actual != want:
                status, reason = "FAIL", "hard identity/relationship mismatch"
        if rule["level"] == "SOFT CANONICAL" and status != "PASS":
            status, reason = "WARN", "adaptable detail: " + reason
        checks.append(dict(rule_id=rid, result=status, reason=reason))
    for rid in selected.keys() - seen:
        checks.append(dict(rule_id=rid, result="WARN" if selected[rid]["level"] == "SOFT CANONICAL" else "UNKNOWN", reason="checkpoint evidence missing"))
    status = "FAIL" if errors or any(c["result"] == "FAIL" for c in checks) else "UNKNOWN" if any(c["result"] == "UNKNOWN" for c in checks) else "PASS"
    return dict(status=status, errors=errors, checks=checks, contract_ref=reference(packet), checkpoint=checkpoint)


def verify_auxiliary(packet, aux):
    review = aux.get("contract_review", {})
    if not isinstance(review, dict) or review.get("contract_ref") != reference(packet) or review.get("image_sha256") != aux.get("sha256"):
        return ["Auxiliary has missing/stale Model Contract review"]
    rows = review.get("views", [])
    if not isinstance(rows, list): return ["Invalid contract view reviews"]
    reviewed, permitted, errors = set(), set(), []
    for row in rows:
        if not isinstance(row, dict) or row.get("view") not in aux.get("views", []) or row.get("view") in reviewed:
            errors.append("Unknown/duplicate contract view review"); continue
        view = row["view"]; reviewed.add(view)
        result = verify_observations(packet, "VIEWS", row.get("observations"))
        if result["status"] == "PASS": permitted.add(view)
    if reviewed != set(aux.get("views", [])): errors.append("Review each generated view against Model Contract")
    allowed = aux.get("permitted_views", [])
    if not isinstance(allowed, list) or len(set(allowed)) != len(allowed) or not set(allowed) <= permitted:
        errors.append("Inconsistent/unverifiable views cannot be permitted for modeling")
    if aux.get("use_status") == "ACCEPTED" and (permitted != reviewed or set(allowed) != reviewed):
        errors.append("Accepted sheet violates Model Contract / VIEW COMPLETENESS")
    if aux.get("use_status") == "RESTRICTED" and not allowed: errors.append("Restricted sheet needs a consistent permitted view; otherwise reject it")
    if aux.get("use_status") in {"REJECTED", "UNREVIEWED"} and allowed: errors.append("Rejected/unreviewed views cannot instruct Blender")
    return errors


def verify_assembly(packet, assembly, checkpoint):
    if assembly.get("contract_ref") != reference(packet):
        return dict(status="FAIL", errors=["Assembly contract revision/hash is stale"], checks=[])
    parts = assembly.get("parts", [])
    if not isinstance(parts, list): return dict(status="FAIL", errors=["Invalid assembly parts"], checks=[])
    ids, instances, objects, errors = set(), {}, set(), []
    components = {c["id"]: c for c in packet["components"]}
    for p in parts:
        if not isinstance(p, dict) or not isinstance(p.get("part_id"), str) or p["part_id"] in ids:
            errors.append("Missing/duplicate assembly part id"); continue
        ids.add(p["part_id"])
        cid, instance = p.get("component_id"), p.get("instance_id")
        if cid not in components or not isinstance(instance, str) or not instance or not p.get("object_name"):
            errors.append("Part needs known component, physical instance and object name"); continue
        if p["object_name"] in objects: errors.append("A scene object cannot bind multiple physical parts/instances")
        objects.add(p["object_name"])
        instances.setdefault(cid, set()).add(instance)
    part_map = {p["part_id"]: p for p in parts if isinstance(p, dict) and isinstance(p.get("part_id"), str)}
    for p in parts:
        if isinstance(p, dict) and p.get("parent_id") is not None and p["parent_id"] not in ids:
            errors.append("Unknown assembly parent")
        if not isinstance(p, dict): continue
        seen, parent = {p.get("part_id")}, p.get("parent_id")
        while parent in part_map:
            if parent in seen: errors.append("Assembly hierarchy cycle"); break
            seen.add(parent); parent=part_map[parent].get("parent_id")
        # Physical component attachment must agree with the canonical hierarchy.
        parent = p.get("parent_id"); seen = {p.get("part_id")}
        while parent in part_map and parent not in seen and part_map[parent].get("component_id") == p.get("component_id"):
            seen.add(parent); parent=part_map[parent].get("parent_id")
        actual_parent = part_map.get(parent, {}).get("component_id")
        cid = p.get("component_id")
        if cid in components and actual_parent != components[cid].get("parent_id"):
            errors.append("Physical assembly hierarchy differs from contract: " + str(p.get("part_id")))
    # Counts derive from physical instance bindings, never number of meshes/bolts.
    observations = copy.deepcopy(assembly.get("observations", []))
    if not isinstance(observations, list): return dict(status="FAIL", errors=["Invalid assembly observations"], checks=[])
    count_rules = [r for r in packet["model_contract"]["rules"] if r["kind"] == "count" and checkpoint in r["checkpoints"]]
    count_ids = {r["id"] for r in count_rules}
    observations = [o for o in observations if isinstance(o, dict) and o.get("rule_id") not in count_ids]
    dims = {d["id"]: d for d in packet["relative_dimensions"]}
    rules = {r["id"]: r for r in packet["model_contract"]["rules"]}
    for obs in observations:
        rule = rules.get(obs.get("rule_id"), {})
        if rule.get("kind") in {"dimension", "ratio"} and isinstance(obs.get("instance_values"), dict):
            dim = dims[rule["target_id"] if rule["kind"] == "dimension" else rule["numerator_id"]]
            if set(obs["instance_values"]) != instances.get(dim["component_id"], set()):
                errors.append("Measurement instance bindings differ from physical assembly")
    for r in count_rules:
        observations.append(dict(rule_id=r["id"], state="MEASURED", value=len(instances.get(r["target_id"], set())), method="physical instance bindings", evidence="assembly_graph.parts (must be checked against scene objects)"))
    result = verify_observations(packet, checkpoint, observations)
    result["errors"].extend(errors)
    if errors: result["status"] = "FAIL"
    result["observations_sha256"] = digest(dict(parts=parts, observations=assembly.get("observations", [])))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--assembly", type=Path)
    parser.add_argument("--checkpoint", choices=sorted(CHECKPOINTS), default="MACRO")
    parser.add_argument("--seal", action="store_true", help="Explicitly seal reviewed rules; edits packet only")
    parser.add_argument("--previous", type=Path, help="Required predecessor for revision >1")
    args = parser.parse_args()
    # Same strict JSON reader and provenance gate as all PASS0 consumers.
    import importlib.util
    spec = importlib.util.spec_from_file_location("pass0_contract_cli", Path(__file__).resolve().parents[1] / "skills/visual-reference-reconstruction/scripts/validate_pass0.py")
    validator = importlib.util.module_from_spec(spec); spec.loader.exec_module(validator)
    try:
        packet = validator.load_packet(args.packet)
        if args.seal:
            if args.assembly: raise ValueError("Seal and assembly verification are separate operations")
            seal(packet, previous=validator.load_packet(args.previous) if args.previous else None)
        errors = validator.validate(packet, args.packet.parent, True)
        if errors: raise ValueError("; ".join(errors))
        if args.seal: args.packet.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result = verify_assembly(packet, validator.load_packet(args.assembly), args.checkpoint) if args.assembly else dict(status="PASS", errors=validate_contract(packet))
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0 if result["status"] == "PASS" and not result["errors"] else 1
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps(dict(status="FAIL", errors=[str(exc)]))); return 1


if __name__ == "__main__":
    raise SystemExit(main())
