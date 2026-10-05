# PASS 0 handoff contract v1

`pass0.json` is task-local, portable UTF-8 JSON. Paths resolve against its directory;
absolute source paths are allowed for local evidence. Hash original bytes with
SHA-256. Copy references into a deliverable when portability is required, preserving
IDs/hashes and source roles. This schema does not execute captions or report text.

Required top-level fields:

| Field | Content |
|---|---|
| schema_version, packet_id | `1`, stable task/version ID |
| task_scope, object_class | Intended next work and domain |
| source_of_truth | Nonempty list of PRIMARY/SUPPORTING source IDs |
| sources | ID, path, sha256, role (PRIMARY/SUPPORTING/AUXILIARY_INPUT/REPORT), projection, authority_note |
| proportion_basis | Unit, scale_status, axis_convention, pose, camera_notes |
| components | ID, label, count, claims; split certainty by property |
| relative_dimensions | ID, component_id, axis, min, max, unit and claim evidence; use ranges |
| silhouette_notes | Claims about envelopes, landmarks, negative spaces and proportions |
| relationships | Claim fields plus from_component, to_component, relationship |
| ambiguity_map | ID, component_ids, question, severity, decision, allowed_action, basis |
| contradictions | ID, source_ids, property, description, severity, status, resolution |
| auxiliary_references | Created files, prompt hashes, lineage, views, review matrix, permitted/forbidden uses, claim_links |
| generation | Status COMPLETE/UNAVAILABLE/FAILED/NOT_NEEDED and reason |
| gate | Status READY/READY_WITH_LIMITS/BLOCKED, permitted_stage, limits, reviewer, review_notes |

Claim format used in components, silhouette, dimensions and relationships:

```json
{
  "id": "launcher.face_count",
  "property": "visible circular faces per housing",
  "value": "4 columns x 3 rows; 12",
  "certainty": "CONFIRMED",
  "evidence": [{"source_id": "original", "region": "upper left and upper right housings", "observation": "each visible face has a 4 by 3 array"}],
  "basis": "Direct exterior observation; bore depth and rear opening are not established."
}
```

`INFERRED` requires original-source evidence plus reasoning; `SPECULATIVE` requires
reasoning/limits but may have no visual evidence. `CONFIRMED` requires only
PRIMARY/SUPPORTING evidence. REPORT and AUXILIARY_INPUT evidence can contextualize
an inference, never confirm original geometry. Estimates from perspective stay
INFERRED even when visible part count is CONFIRMED. Real-world units need a reliable
scale anchor; fictional printed dimensions do not supply one automatically.

Ambiguity severity is BLOCKING/NONBLOCKING; decision is UNRESOLVED/DEFER/PROXY/RESOLVED.
Contradiction severity uses the same terms; status OPEN/RESOLVED. Any unresolved
BLOCKING entry keeps the gate BLOCKED. Nonblocking unknowns need an explicit safe
action and go into downstream limits; unresolved entries require READY_WITH_LIMITS.
Deferred rear geometry cannot silently be modeled under a ready macro-only gate.

Auxiliary record: ID, path, sha256, prompt_path, prompt_sha256, input_source_ids,
generated=true, views, use_status, permitted_uses, forbidden_uses, consistency_checks,
claim_links. Each consistency check has criterion, result, observations. Each claim
link names a claim ID from this packet; generated details lacking source support
must first receive a SPECULATIVE claim. REJECTED/UNREVIEWED files have no permitted uses.

The validator checks IDs/references, non-finite values, range order, certainty
provenance, source roles, auxiliary review and blocked gate consistency. With
`--verify-files`, it also verifies source/image/prompt existence and hashes. It
cannot tell whether a claimed source observation is true, measure silhouette,
establish lens calibration or certify hidden construction: review actual images.
