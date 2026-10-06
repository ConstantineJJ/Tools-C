"""Validate PASS 0 structure/provenance; never certify image or 3D accuracy."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import importlib.util

_spec = importlib.util.spec_from_file_location("pass0_description", Path(__file__).with_name("description_contract.py"))
_description = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_description)
identity_snapshot = _description.identity_snapshot
_spec = importlib.util.spec_from_file_location("pass0_model_contract", Path(__file__).resolve().parents[3] / "tools/model_contract.py")
model_contract = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(model_contract)

CERTAINTY = {"CONFIRMED", "INFERRED", "SPECULATIVE"}
SOURCE_ROLES = {"PRIMARY", "SUPPORTING", "AUXILIARY_INPUT", "REPORT"}
CRITERIA = {"identity", "proportions", "part_counts", "construction", "handedness", "silhouette"}
REQUIRED = {"schema_version", "packet_id", "task_scope", "object_class", "source_of_truth",
            "sources", "proportion_basis", "components", "relative_dimensions",
            "silhouette_notes", "relationships", "ambiguity_map", "contradictions",
            "auxiliary_references", "generation", "gate"}


def load_packet(path):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError("Duplicate JSON key: " + key)
            obj[key] = value
        return obj
    def reject(value):
        raise ValueError("Non-finite JSON constant: " + value)
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique,
                      parse_constant=reject)


def validate(packet, base=Path("."), verify_files=False):
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())
    def rows(value, name):
        require(isinstance(value, list), name + " must be a list")
        return value if isinstance(value, list) else []
    def indexed(value, name):
        result = {}
        for row in rows(value, name):
            if not isinstance(row, dict) or not nonempty(row.get("id")):
                errors.append(name + " entry needs an id"); continue
            require(row["id"] not in result, "Duplicate " + name + " id: " + row["id"])
            result[row["id"]] = row
        return result
    def file_check(row, path_key="path", hash_key="sha256"):
        path, digest = row.get(path_key), row.get(hash_key)
        require(nonempty(path), "Missing " + path_key)
        require(isinstance(digest, str) and len(digest) == 64 and
                all(c in "0123456789abcdef" for c in digest), "Invalid " + hash_key)
        if verify_files and nonempty(path):
            candidate = Path(path)
            if not candidate.is_absolute(): candidate = Path(base) / candidate
            try:
                require(hashlib.sha256(candidate.read_bytes()).hexdigest() == digest,
                        "File hash mismatch: " + str(candidate))
            except OSError as exc:
                errors.append("Cannot read " + str(candidate) + ": " + str(exc))
    def finite(value):
        if isinstance(value, float): require(math.isfinite(value), "Non-finite numeric value")
        elif isinstance(value, dict):
            for child in value.values(): finite(child)
        elif isinstance(value, list):
            for child in value: finite(child)

    if not isinstance(packet, dict): return ["Packet must be an object"]
    finite(packet)
    require(REQUIRED <= packet.keys(), "Missing packet fields: " + ", ".join(sorted(REQUIRED - packet.keys())))
    version = packet.get("schema_version")
    require(type(version) is int and version in {1, 2, 3}, "Unsupported schema_version")
    mode = packet.get("mode", "REFERENCE" if version == 1 else None)
    require(mode in {"REFERENCE", "DESCRIPTION"}, "Explicit mode required for schema 2/3")
    require(version != 1 or mode == "REFERENCE", "Schema 1 supports REFERENCE only")
    description = mode == "DESCRIPTION"
    roles = SOURCE_ROLES | {"BRIEF", "CONCEPT_CANDIDATE", "CANONICAL_CONCEPT"} if description else SOURCE_ROLES
    truth_roles = {"BRIEF", "CANONICAL_CONCEPT"} if description else {"PRIMARY", "SUPPORTING"}
    if version == 3 and not description:
        roles = roles | {"BRIEF"}; truth_roles = truth_roles | {"BRIEF"}
    for key in ["packet_id", "task_scope", "object_class"]:
        require(nonempty(packet.get(key)), "Missing " + key)
    sources = indexed(packet.get("sources"), "source")
    for source in sources.values():
        require(source.get("role") in roles, "Invalid source role")
        for key in ["projection", "authority_note"]: require(nonempty(source.get(key)), "Source needs " + key)
        file_check(source)
    truth = rows(packet.get("source_of_truth"), "source_of_truth")
    require(bool(truth) and len(set(map(str, truth))) == len(truth), "Need unique source_of_truth IDs")
    require(all(isinstance(s, str) and s in sources and sources[s].get("role") in truth_roles
                for s in truth), "Source of truth has invalid authority for input mode")
    if not description:
        require(any(sources.get(s, {}).get("role") in {"PRIMARY", "SUPPORTING"} for s in truth if isinstance(s, str)),
                "REFERENCE needs original image authority, not only text")
    basis = packet.get("proportion_basis", {})
    if not isinstance(basis, dict): basis = {}; errors.append("proportion_basis must be an object")
    for key in ["unit", "scale_status", "axis_convention", "pose", "camera_notes"]:
        require(nonempty(basis.get(key)), "Proportion basis needs " + key)
    require(basis.get("scale_status") in {"RELATIVE_ONLY", "CALIBRATED"}, "Invalid scale_status")
    if basis.get("scale_status") == "CALIBRATED":
        require(nonempty(basis.get("scale_anchor")), "Calibrated scale needs a scale_anchor")
    components = indexed(packet.get("components"), "component")
    require(bool(components), "No main components")
    claims = {}
    def claim(row):
        if not isinstance(row, dict): errors.append("Claim must be an object"); return
        cid = row.get("id")
        require(nonempty(cid) and cid not in claims, "Missing/duplicate claim id: " + str(cid))
        if isinstance(cid, str): claims[cid] = row
        require(nonempty(row.get("property")), "Claim needs property")
        require("value" in row, "Claim needs value")
        certainty = row.get("certainty")
        allowed = {"REQUIRED", "CANONICAL", "SPECULATIVE"} if description else CERTAINTY | ({"REQUIRED"} if version == 3 else set())
        require(certainty in allowed, "Invalid certainty: " + str(cid))
        require(nonempty(row.get("basis")), "Claim needs basis: " + str(cid))
        evidence = rows(row.get("evidence"), "claim evidence")
        authoritative = False
        for item in evidence:
            if not isinstance(item, dict): errors.append("Invalid evidence entry"); continue
            sid = item.get("source_id")
            require(isinstance(sid, str) and sid in sources, "Unknown evidence source: " + str(sid))
            for key in ["region", "observation"]:
                require(nonempty(item.get(key)), "Evidence needs " + key)
            role = sources.get(sid, {}).get("role") if isinstance(sid, str) else None
            authoritative |= sid in truth and role in {"PRIMARY", "SUPPORTING"}
            if certainty in {"REQUIRED", "CANONICAL"}:
                expected = "BRIEF" if certainty == "REQUIRED" else "CANONICAL_CONCEPT"
                require(sid in truth and role == expected, certainty + " has wrong provenance: " + str(cid))
            if certainty == "CONFIRMED":
                require(sid in truth and role in {"PRIMARY", "SUPPORTING"},
                        "CONFIRMED claim cannot use derivative/report evidence: " + str(cid))
        if certainty in {"CONFIRMED", "INFERRED"}:
            require(authoritative, certainty + " needs source-of-truth evidence: " + str(cid))
        if certainty in {"REQUIRED", "CANONICAL"}:
            require(bool(evidence), certainty + " needs evidence: " + str(cid))
    if description or version == 3:
        for constraint in rows(packet.get("constraints", []), "constraints"):
            claim(constraint)
            if isinstance(constraint, dict): require(constraint.get("certainty") == "REQUIRED", "Constraints must be REQUIRED")
    for component in components.values():
        require(nonempty(component.get("label")), "Component needs label")
        require(type(component.get("count")) is int and component["count"] > 0, "Component count must be positive integer")
        entries = rows(component.get("claims"), "component claims")
        require(bool(entries), "Component needs property-level claims")
        for item in entries: claim(item)
    dimensions = rows(packet.get("relative_dimensions"), "relative_dimensions")
    require(bool(dimensions), "Need relative dimension ranges")
    for dim in dimensions:
        claim(dim)
        if not isinstance(dim, dict): continue
        require(dim.get("component_id") in components, "Unknown dimension component")
        require(nonempty(dim.get("axis")) and nonempty(dim.get("unit")), "Dimension needs axis/unit")
        require(dim.get("unit") == basis.get("unit"), "Dimension unit differs from proportion basis")
        lo, hi = dim.get("min"), dim.get("max")
        require(type(lo) in {int, float} and type(hi) in {int, float} and 0 < lo <= hi,
                "Invalid dimension range: " + str(dim.get("id")))
    silhouette = rows(packet.get("silhouette_notes"), "silhouette_notes")
    require(bool(silhouette), "Need silhouette/proportion notes")
    for note in silhouette: claim(note)
    for relation in rows(packet.get("relationships"), "relationships"):
        claim(relation)
        if not isinstance(relation, dict): continue
        require(relation.get("from_component") in components and relation.get("to_component") in components,
                "Unknown relationship component")
        require(nonempty(relation.get("relationship")), "Relationship needs relationship")
    ambiguities = indexed(packet.get("ambiguity_map"), "ambiguity")
    conflicts = indexed(packet.get("contradictions"), "contradiction")
    blocked, limited = False, False
    for entry in ambiguities.values():
        for key in ["question", "allowed_action", "basis"]: require(nonempty(entry.get(key)), "Ambiguity needs " + key)
        ids = rows(entry.get("component_ids"), "ambiguity component_ids")
        require(bool(ids) and all(c in components for c in ids), "Unknown ambiguity components")
        require(entry.get("severity") in {"BLOCKING", "NONBLOCKING"}, "Invalid ambiguity severity")
        require(entry.get("decision") in {"UNRESOLVED", "DEFER", "PROXY", "RESOLVED"}, "Invalid ambiguity decision")
        unresolved = entry.get("decision") != "RESOLVED"
        blocked |= unresolved and entry.get("severity") == "BLOCKING"
        limited |= unresolved
    for entry in conflicts.values():
        for key in ["property", "description", "resolution"]: require(nonempty(entry.get(key)), "Contradiction needs " + key)
        ids = rows(entry.get("source_ids"), "contradiction source_ids")
        require(len(set(map(str, ids))) >= 2 and all(s in sources for s in ids), "Contradiction needs two known sources")
        require(entry.get("severity") in {"BLOCKING", "NONBLOCKING"}, "Invalid contradiction severity")
        require(entry.get("status") in {"OPEN", "RESOLVED"}, "Invalid contradiction status")
        blocked |= entry.get("status") == "OPEN" and entry.get("severity") == "BLOCKING"
        limited |= entry.get("status") == "OPEN"
    aux = indexed(packet.get("auxiliary_references"), "auxiliary")
    for entry in aux.values():
        file_check(entry); file_check(entry, "prompt_path", "prompt_sha256")
        require(entry.get("generated") is True, "Auxiliary generation lineage is required")
        ids = rows(entry.get("input_source_ids"), "input_source_ids")
        require(bool(ids) and any(s in truth for s in ids) and all(s in sources for s in ids), "Auxiliary must retain original input lineage")
        require(bool(rows(entry.get("views"), "views")), "Auxiliary needs views")
        uses = rows(entry.get("permitted_uses"), "permitted_uses")
        forbidden = rows(entry.get("forbidden_uses"), "forbidden_uses")
        status = entry.get("use_status")
        require(status in {"ACCEPTED", "RESTRICTED", "REJECTED", "UNREVIEWED"}, "Invalid auxiliary status")
        checks = {}
        for item in rows(entry.get("consistency_checks"), "consistency_checks"):
            if not isinstance(item, dict): errors.append("Invalid consistency check"); continue
            criterion = item.get("criterion")
            require(criterion not in checks, "Duplicate consistency criterion")
            checks[criterion] = item.get("result")
            require(criterion in CRITERIA and item.get("result") in {"PASS", "FAIL", "WARN", "SKIP"}, "Invalid consistency result")
            require(nonempty(item.get("observations")), "Consistency review needs observations")
        require(CRITERIA == checks.keys(), "Need all six auxiliary consistency checks")
        if status == "ACCEPTED":
            require(all(v == "PASS" for v in checks.values()) and bool(uses), "Accepted auxiliary has incomplete/failed review")
        if status == "RESTRICTED": require(bool(uses) and bool(forbidden), "Restricted auxiliary needs explicit permitted/forbidden uses")
        if status in {"UNREVIEWED", "REJECTED"}: require(not uses, "Unreviewed/rejected auxiliary cannot instruct modeling")
        limited |= status != "ACCEPTED"
        require(all(c in claims for c in rows(entry.get("claim_links"), "claim_links")), "Unknown auxiliary claim link")
        # Byte-identical generated images cannot be laundered as authoritative originals.
        require(not any(s.get("sha256") == entry.get("sha256") for sid, s in sources.items() if sid in truth),
                "Generated auxiliary is also listed as source of truth")
    generation = packet.get("generation", {})
    if not isinstance(generation, dict): generation = {}; errors.append("generation must be an object")
    require(generation.get("status") in {"COMPLETE", "UNAVAILABLE", "FAILED", "NOT_NEEDED"}, "Invalid generation status")
    require(nonempty(generation.get("reason")), "Generation status needs reason")
    if generation.get("status") == "COMPLETE": require(bool(aux), "Complete generation needs saved outputs")
    gate = packet.get("gate", {})
    if not isinstance(gate, dict): gate = {}; errors.append("gate must be an object")
    status = gate.get("status")
    if description:
        _description.validate_description(packet, sources, claims, components, base, verify_files,
                                          require, nonempty, rows, indexed, file_check, load_packet)
    elif version == 3:
        constraints = indexed(packet.get("constraints", []), "constraint")
        _description.validate_required_bindings(constraints, claims, components, require, rows)
    require(status in {"READY", "READY_WITH_LIMITS", "BLOCKED"}, "Invalid PASS 0 gate")
    for key in ["permitted_stage", "reviewer", "review_notes"]: require(nonempty(gate.get(key)), "Gate needs " + key)
    limits = rows(gate.get("limits"), "gate limits")
    if blocked: require(status == "BLOCKED", "Unresolved blocker cannot pass PASS 0")
    if limited: require(status != "READY", "Unresolved/restricted evidence needs READY_WITH_LIMITS or BLOCKED")
    if status != "READY": require(bool(limits), "Limited/blocked gate needs explicit limits")
    if status == "BLOCKED": require(gate.get("permitted_stage") == "NONE", "Blocked gate cannot permit modeling")
    if version == 3 and (status != "BLOCKED" or packet.get("model_contract") is not None):
        contract_errors = model_contract.validate_contract(packet)
        errors.extend(contract_errors)
        if not contract_errors:
            for entry in aux.values(): errors.extend(model_contract.verify_auxiliary(packet, entry))
    return errors


def require_stage(packet, stage, base=Path("."), verify_files=True):
    errors = validate(packet, base, verify_files)
    if errors: raise ValueError("; ".join(errors))
    if packet["gate"]["status"] == "BLOCKED" or packet["gate"]["permitted_stage"] != stage:
        raise ValueError("PASS 0 does not permit stage " + stage)
    if packet.get("schema_version") != 3:
        raise ValueError("Modeling requires schema 3 and a reviewed persistent contract; historical packets are audit-only")
    errors = model_contract.validate_contract(packet)
    if errors: raise ValueError("; ".join(errors))
    return packet["gate"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--verify-files", action="store_true")
    parser.add_argument("--allow-blocked", action="store_true", help="Inspect a blocked packet; no modeling authorization")
    args = parser.parse_args()
    try:
        packet = load_packet(args.packet)
        errors = validate(packet, args.packet.parent, args.verify_files)
    except (OSError, ValueError, TypeError) as exc:
        errors = [str(exc)]; packet = {}
    gate = packet.get("gate", {}).get("status", "INVALID")
    print(json.dumps(dict(structural_status="FAIL" if errors else "PASS", gate=gate,
                          visual_status="NOT_CERTIFIED_BY_VALIDATOR", errors=errors), ensure_ascii=False))
    return 1 if errors else (2 if gate == "BLOCKED" and not args.allow_blocked else 0)


if __name__ == "__main__":
    sys.exit(main())
