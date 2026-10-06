"""DESCRIPTION authority and identity invariants; pixel truth remains manual QA."""
from pathlib import Path
import copy

QUALITY = {"brief_fit", "silhouette", "plausibility", "reconstruction", "low_noise"}


def identity_snapshot(packet):
    """Frozen consumer identity; unsupported claims are deliberately not promoted."""
    def locked(rows):
        return [r for r in rows if isinstance(r, dict) and r.get("certainty") in {"REQUIRED", "CANONICAL"}]
    return copy.deepcopy(dict(proportion_basis=packet.get("proportion_basis"), constraints=packet.get("constraints"),
                components=[dict(id=c.get("id"), label=c.get("label"), count=c.get("count"), claims=locked(c.get("claims", [])))
                            for c in packet.get("components", []) if isinstance(c, dict)],
                relative_dimensions=locked(packet.get("relative_dimensions", [])),
                silhouette_notes=locked(packet.get("silhouette_notes", [])),
                relationships=locked(packet.get("relationships", []))))


def validate_description(p, sources, claims, components, base, verify_files,
                         require, nonempty, rows, indexed, file_check, load_packet):
    truth = p.get("source_of_truth", [])
    brief_ids = {sid for sid, s in sources.items() if s.get("role") == "BRIEF" and sid in truth}
    require(bool(brief_ids), "DESCRIPTION needs original BRIEF authority")
    constraints = indexed(p.get("constraints"), "constraint")
    require(bool(constraints), "DESCRIPTION needs REQUIRED constraints")
    design = p.get("design_brief", {})
    if not isinstance(design, dict): design = {}; require(False, "design_brief must be an object")
    require(design.get("source_id") in brief_ids, "Design brief must retain user text")
    for field in ["intent", "strategy_reason"]: require(nonempty(design.get(field)), "Design brief needs " + field)
    for field in ["preferences", "open_decisions"]: rows(design.get(field), "design brief " + field)
    selection = p.get("candidate_selection", {})
    if not isinstance(selection, dict): selection = {}; require(False, "candidate_selection must be an object")
    require(selection.get("strategy") in {"SINGLE", "EXPLORE"}, "Invalid candidate strategy")
    require(selection.get("selector") in {"AGENT", "USER", "PENDING"}, "Invalid candidate selector")
    require(nonempty(selection.get("reason")), "Selection needs rationale")
    candidates = indexed(p.get("concept_candidates"), "candidate")
    eligible = set()
    seen_sources, seen_hashes = set(), set()
    for cid, candidate in candidates.items():
        sid = candidate.get("source_id")
        source = sources.get(sid, {}) if isinstance(sid, str) else {}
        require(source.get("role") in {"CONCEPT_CANDIDATE", "CANONICAL_CONCEPT"}, "Candidate needs concept image source")
        require(sid not in seen_sources and source.get("sha256") not in seen_hashes, "Candidates must be distinct hero images")
        if isinstance(sid, str): seen_sources.add(sid)
        seen_hashes.add(source.get("sha256"))
        require(candidate.get("generated") is True and candidate.get("views") == ["hero"], "Candidate must be one generated hero view")
        ids = rows(candidate.get("input_source_ids"), "candidate inputs")
        require(bool(ids) and all(isinstance(s, str) and s in brief_ids for s in ids), "Concept candidates must retain BRIEF lineage")
        file_check(candidate, "prompt_path", "prompt_sha256")
        reviews = indexed(candidate.get("requirement_reviews"), "requirement review")
        require(reviews.keys() == constraints.keys(), "Review every REQUIRED constraint for each candidate")
        for review in reviews.values():
            require(review.get("result") in {"PASS", "FAIL", "UNKNOWN"} and nonempty(review.get("observations")), "Invalid requirement review")
        quality = indexed(candidate.get("quality_reviews"), "quality review")
        require(quality.keys() == QUALITY, "Need five candidate quality reviews")
        for review in quality.values():
            score = review.get("score")
            require(type(score) in {int, float} and 0 <= score <= 5 and nonempty(review.get("observations")), "Invalid quality score/reason")
        if reviews.keys() == constraints.keys() and all(r.get("result") == "PASS" for r in reviews.values()): eligible.add(cid)
    if selection.get("strategy") == "SINGLE": require(len(candidates) <= 1, "SINGLE cannot contain multiple candidates")
    lock = p.get("identity_lock", {})
    if not isinstance(lock, dict): lock = {}; require(False, "identity_lock must be an object")
    require(lock.get("status") in {"LOCKED", "PENDING"}, "Invalid identity lock status")
    if lock.get("status") != "LOCKED":
        require(p.get("gate", {}).get("status") == "BLOCKED", "Pending/no canonical concept blocks Blender")
        require(not selection.get("selected_candidate_id"), "Pending lock cannot publish a selected concept")
        require(set(truth) == brief_ids, "Pending lock has no canonical source authority")
        require(not p.get("auxiliary_references"), "Do not generate multiview before Identity Lock")
        return
    selected = selection.get("selected_candidate_id")
    candidate = candidates.get(selected, {}) if isinstance(selected, str) else {}
    sid = candidate.get("source_id")
    source = sources.get(sid, {}) if isinstance(sid, str) else {}
    require(isinstance(selected, str) and selected in eligible, "Cannot lock a candidate with failed/unknown REQUIRED constraints")
    require(selection.get("selector") in {"AGENT", "USER"} and nonempty(selection.get("actor")), "Locked selection needs selector/actor")
    require(source.get("role") == "CANONICAL_CONCEPT" and set(truth) == brief_ids | {sid}, "Only selected concept and BRIEF are DESCRIPTION authority")
    require(all(s.get("role") != "CANONICAL_CONCEPT" or k == sid for k, s in sources.items()), "Only one canonical concept")
    require(lock.get("source_id") == sid and lock.get("sha256") == source.get("sha256"), "Identity Lock source/hash mismatch")
    version = lock.get("version")
    require(type(version) is int and version > 0, "Lock version must be a positive integer")
    if type(version) is int and version > 1:
        require(nonempty(lock.get("revision_reason")) and nonempty(lock.get("supersedes_packet_id")) and
                isinstance(lock.get("supersedes_sha256"), str) and len(lock["supersedes_sha256"]) == 64,
                "Relock needs explicit reason and predecessor packet/hash")
    if p.get("schema_version") == 3:
        require(not any(k in lock for k in ("manifest", "manifest_path", "manifest_sha256")),
                "Schema 3 uses the single Model Contract, not a duplicate identity manifest")
    else:
        manifest = lock.get("manifest")
        require(isinstance(manifest, dict) and manifest == identity_snapshot(p), "Packet drift from frozen Identity Lock manifest")
        file_check(lock, "manifest_path", "manifest_sha256")
        if verify_files and nonempty(lock.get("manifest_path")):
            path = Path(lock["manifest_path"])
            if not path.is_absolute(): path = Path(base) / path
            try: require(load_packet(path) == manifest, "Frozen manifest bytes differ from embedded snapshot")
            except (OSError, ValueError, TypeError) as exc: require(False, "Cannot load frozen identity manifest: " + str(exc))
    validate_required_bindings(constraints, claims, components, require, rows)
    for aux in p.get("auxiliary_references", []):
        if not isinstance(aux, dict): continue
        require(sid in aux.get("input_source_ids", []) and aux.get("lock_version") == version and
                aux.get("canonical_sha256") == lock.get("sha256"), "Auxiliary must derive from current frozen canonical image/lock")


def validate_required_bindings(constraints, claims, components, require, rows):
    """Same user requirement binding for text-only and text+image input."""
    for cid, constraint in constraints.items():
        target = constraint.get("target")
        require(target in {"count", "claim", "intent"}, "Constraint needs count/claim/intent target")
        component = components.get(constraint.get("component_id"), {})
        if target == "count":
            value = constraint.get("value")
            require(type(value) is int and value > 0 and component.get("count") == value,
                    "Component count violates REQUIRED constraint: " + cid)
        if target == "claim":
            ids = rows(constraint.get("target_claim_ids"), "constraint target claims")
            component_claims = {c.get("id") for c in component.get("claims", []) if isinstance(c, dict) and isinstance(c.get("id"), str)}
            require(bool(ids) and all(c in component_claims and c in claims and claims[c].get("certainty") == "REQUIRED" and claims[c].get("value") == constraint.get("value") and
                    cid in claims[c].get("requirement_ids", []) for c in ids), "Required geometry constraint lost: " + cid)
    for cid, claim in claims.items():
        if cid in constraints or claim.get("certainty") != "REQUIRED": continue
        ids = rows(claim.get("requirement_ids"), "required claim requirement_ids")
        require(bool(ids) and all(c in constraints and constraints[c].get("value") == claim.get("value") for c in ids),
                "REQUIRED geometry must link to matching brief constraints: " + cid)
