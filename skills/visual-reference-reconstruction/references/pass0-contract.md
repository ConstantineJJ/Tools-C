# PASS 0 handoff contract — common consumer shape

`pass0.json` is task-local, portable UTF-8 JSON. Paths resolve against its directory;
absolute source paths are allowed for local evidence. Hash original bytes with
SHA-256. Copy references into a deliverable when portability is required, preserving
IDs/hashes and source roles. This schema does not execute captions or report text.

Required top-level fields:

| Field | Content |
|---|---|
| schema_version, mode, packet_id | New packets: `3`, REFERENCE/DESCRIPTION, stable task/version ID. Historical 1/2 still parse for audit. |
| task_scope, object_class | Intended next work and domain |
| source_of_truth | REFERENCE: PRIMARY/SUPPORTING IDs. DESCRIPTION: BRIEF IDs plus the single locked CANONICAL_CONCEPT ID; PENDING has only BRIEF authority. |
| sources | ID, path, sha256, role, projection, authority_note. REFERENCE roles: PRIMARY/SUPPORTING/AUXILIARY_INPUT/REPORT. DESCRIPTION also BRIEF/CONCEPT_CANDIDATE/CANONICAL_CONCEPT. |
| proportion_basis | Unit, scale_status, axis_convention, pose, camera_notes |
| components | ID, label, count, claims, parent_id, symmetry; split certainty by property |
| relative_dimensions | ID, component_id, axis, min, max, unit and claim evidence; use ranges |
| silhouette_notes | Claims about envelopes, landmarks, negative spaces and proportions |
| relationships | Claim fields plus from_component, to_component, relationship |
| ambiguity_map | ID, component_ids, question, severity, decision, allowed_action, basis |
| contradictions | ID, source_ids, property, description, severity, status, resolution |
| auxiliary_references | Created files, prompt hashes, lineage, views, review matrix, permitted/forbidden uses, claim_links |
| generation | Status COMPLETE/UNAVAILABLE/FAILED/NOT_NEEDED and reason |
| gate | Status READY/READY_WITH_LIMITS/BLOCKED, permitted_stage, limits, reviewer, review_notes |
| model_contract | Single persistent design policy, revision/hash, constraints referencing existing graph fields; see [Model Contract](model-contract.md). Mandatory before modeling. |

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

## DESCRIPTION additions (schema 2/3)

The common components/dimensions/silhouette/relationships/ambiguity/auxiliary/gate
fields remain identical for both modes. Only authority labels and preparation
metadata differ. New DESCRIPTION fields:

| Field | Content |
|---|---|
| design_brief | source_id (verbatim user BRIEF file), intent, preferences, open_decisions, strategy_reason |
| constraints | REQUIRED claim records with brief clause evidence; target count/claim/intent. count uses component_id and integer value; claim uses target_claim_ids and matching values/requirement_ids. intent covers functional/global criteria manually reviewed in candidates. |
| concept_candidates | ID, source_id, generated=true, views=[hero], input_source_ids (BRIEF only), prompt_path/prompt_sha256, requirement_reviews, quality_reviews |
| candidate_selection | strategy SINGLE/EXPLORE, selector AGENT/USER/PENDING, actor, reason, selected_candidate_id (only after selection) |
| identity_lock | status LOCKED/PENDING, positive version, source_id/sha256. Schema 3 uses model_contract for graph identity; schema 2 retains historical manifest fields. Hero revision >1 requires revision_reason, supersedes_packet_id and supersedes_sha256. |

Candidate requirement_reviews use each constraint's ID, result PASS/FAIL/UNKNOWN
and observations. Every hard requirement must PASS before lock. quality_reviews use
IDs brief_fit/silhouette/plausibility/reconstruction/low_noise, score 0–5 and
observations. Quality scores inform choice; they never override a failed requirement.
Record a rejected candidate's failure even when another wins; losing candidates
remain CONCEPT_CANDIDATE, never source_of_truth.

REQUIRED claims cite BRIEF only. Geometry claims repeat the required value and link
requirement_ids to constraints; they do not infer user intent from generated pixels.
CANONICAL claims cite the single chosen CANONICAL_CONCEPT with visible region and
design adoption reason. SPECULATIVE remains undecided/hidden. These labels express
design authority, not photographic certainty or engineering feasibility. Do not use
CONFIRMED/INFERRED in DESCRIPTION or CANONICAL in REFERENCE. Schema 3 REFERENCE
may carry explicit REQUIRED clauses from a saved BRIEF, ahead of image evidence.

For historical schema 2 only, the frozen manifest is `identity_snapshot(packet)` from the validator: required
constraints, component IDs/labels/counts, REQUIRED/CANONICAL property claims,
dimensions, silhouette, relationships and proportion basis. Save these exact UTF-8
JSON bytes once, hash them, embed the same object in identity_lock.manifest.
`--verify-files` checks the immutable file/hash and its equality to the packet.
Keep a previous packet/lock on revision, and invalidate affected auxiliaries.
Schema 3 replaces that duplicate manifest with the embedded Model Contract and
assembly/view hash references. Explicitly review locks/tolerances during migration;
do not create them automatically. Hashes detect altered declared bytes; they do not prove honest extraction from
language or protect against someone rewriting the lock and all its receipts.

DESCRIPTION auxiliary records additionally require lock_version and
canonical_sha256, and input_source_ids must include the frozen hero source ID.
Auxiliaries cannot become new CANONICAL evidence. COMPLETE refers to auxiliary
generation; if a reviewed hero is usable but derived views fail/unavailable, record
FAILED/UNAVAILABLE and a restricted source-only handoff. Without a canonical image,
retain provisional REQUIRED/SPECULATIVE analysis but use PENDING + BLOCKED/NONE.

Structural checks cannot know whether requirements were omitted from a brief,
whether an image review is truthful, or whether a hidden joint works. Manual brief
coverage, hero inspection and actual 3D clay/mechanics QA remain mandatory.

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
