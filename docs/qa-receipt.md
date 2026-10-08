# Task-local QA receipt (Pass 3, 2026-10-08)

The receipt verifies declared evidence completeness, **not** actual image
quality. PASS 0 / Model Contract remains the only owner of approved shapes,
identity, measurements and source authority. Verification and Character QA own
the review procedure.

## Run

python tools/qa_gate.py TASK/qa_receipt.json --verify-files

The checker returns structure, gate, stage, workflow, visual, final_coverage,
failures, blockers, limits. visual is always NOT_EVALUATED by this metadata
checker; final_coverage is NOT_CHECKED for FACE/DETAIL. Gate PASS
means declared mandatory evidence is present and reviewed; OPEN means a required
view or review remains unresolved; FAIL means an observed defect or
incomparable setup. Exit codes: 0=PASS, 2=OPEN/FAIL, 1=invalid receipt.
A record declaring PASS cannot prove whether the actual image looks correct.

## Dual Verification v1 (opt-in extension, 2026-10-08)

Existing schema 1/2/3 receipts retain their fields and results. Add the optional
dual_verification field to enable the
[Verification mode protocol](../skills/verification/references/dual-verification.md).
No Model Contract/schema migration or image duplication is required. New generic
asset final review can use ASSET_FINAL (same standard views and reference/contact/
protected checks, without character-specific workflow); new captures should use
schema 2 real metadata. Character schema 3 workflow remains required where scoped.

Run `python tools/qa_gate.py TASK/qa_receipt.json --verify-files --mode ARTISTIC_REVIEW`.
The result retains evidence_gate (original completeness) and adds independent
TECHNICAL_QA and ARTISTIC_REVIEW, technical_scope, artistic_gate, independence,
freshness, capture/inspection requests, delta, next and packet_sha256. Overall
gate requires all applicable evidence and both QA branches. visual remains
NOT_EVALUATED. Without file verification dual acceptance stays OPEN.

dual_verification has EXACT fields version (1),freshness,technical_checks,brief,
artistic,checkpoint,corrections,user_decision. technical_checks is a nonempty list
of existing scoped technical check names; observations/reviewer/evidence retain
the existing check format. Do not claim wider scope than the listed criteria.

brief has complexity,stage,asset_type,scope,requirements,contract,references,
protected,constraints,implementer. complexity SIMPLE/STANDARD/COMPLEX; stages
PRIMARY_FORMS/CRITICAL_FEATURES/FINAL or LOCAL for scope LOCAL (otherwise FULL).
asset_type CHARACTER/VEHICLE/ENVIRONMENT/OTHER. requirements maps region to
{views,criterion}; protected/constraints are string lists. All receipt protected
zone IDs and user PRESERVE/DO_NOT_REINTERPRET flags must remain in protected.
Use consistent explicit region IDs, not inferred object names. contract is
{artifact:{path,sha256},ref:{id,revision,sha256}} to existing pass0.json;
references maps every canonical source_of_truth image ID to its original path/hash.
The checker validates the existing locked contract, never replaces it.

The protocol specifies freshness states/capture bindings, exact artistic review,
compact checkpoint derivation and correction fields. Initial artistic=null and
empty checkpoint history leave acceptance OPEN. Generate a blind packet with
`--verify-files --critic-packet`; send it to a separate read-only critic without
modeling history, or honestly label SELF_REVIEW. The checker does not dispatch
agents, evaluate image content or prove independence; INDEPENDENT_DECLARED is a
bound declaration accompanied by the actual dispatch evidence file.

Keep the dynamic review state inside this receipt; original capture metadata and
snapshots remain immutable. A current unsuitable view requests the missing angle;
an existing uninspected current angle requests INSPECT_EXISTING. Two failures with
the same method require reconsideration, even for optional polish; three remaining
failures escalate. A minor-difference finish requires a recorded user choice.
See the [separate practical blind test](dual-verification-blind-review.md).

## Schema v3 — workflow gates for new reference characters

Retain all v2 fields/setup and add `workflow` from the canonical
[workflow specification](../skills/blender-character-modeling/references/workflow-gates.md).
Run `python tools/qa_gate.py TASK/qa_receipt.json --verify-files --stage FACE`,
then DETAIL before mass detailing, and FINAL for delivery. This same receipt
consumes PASS0, Model Contract/assembly and Surface Transfer records without
duplicating design authority. Execution and strategy reconsideration carry
evidence; file verification is necessary for v3 PASS. FACE/DETAIL PASS is stage
readiness, not final character acceptance.

Historical v1/v2 formats remain readable with workflow NOT_RECORDED_LEGACY;
they do not prove these new gates. Unreviewed declared face identity and
capabilities citing unaccepted checks cannot imply PASS.

## Schema 3 workflow fields (exact)

`workflow`: `artifacts,pass0,face_strategy,primary_assembly,skill_usage`.
The checker verifies contained files, runs the existing PASS0/source-hash and
Model Contract validators, and consumes existing Surface Transfer validation.

- artifacts: unique ID map to distinct relative `{path,sha256}` files: PASS0,
  assembly graph, saved Blender state, selected transfer and actual tool outputs.
- pass0: `{artifact,contract_ref}` with existing `{id,revision,sha256}` binding.
  Authority/identity comes from that file; it is not duplicated here.
- primary_assembly: existing assembly_graph.json artifact ID, or null during
  planning; required for DETAIL/FINAL. MACRO observations are rechecked.
- face_strategy: exact `mode,status,reason,source_ids,identity_anchors,
  occluded_regions,geometry_only_basis,generation_required,tools,execution,transfer`.
  Status SELECTED/EXECUTED/VERIFIED/BLOCKED. Sources are authoritative PASS0 images;
  identity_anchors are supported PASS0 claim IDs. geometry_only_basis is
  VOLUME_IDENTITY or USER_APPROVED_SIMPLIFICATION for GEOMETRY_ONLY, otherwise
  NOT_APPLICABLE. generation_required is Boolean, true for reconstruction/hybrid.
  Occluded regions: `{name,visibility,certainty,treatment}` with unique names,
  PARTIAL/OCCLUDED, INFERRED/SPECULATIVE and KEEP_OCCLUDED/RECONSTRUCT/
  PROVISIONAL_GEOMETRY. Tools: `{name,availability,reason,execution}` with
  AVAILABLE/UNAVAILABLE/UNCHECKED; `imagegen` required for generation. Execution
  lists actual artifact IDs; availability without outputs does not close FINAL.
  transfer is a schema-v2 record ID or null before execution (always null for
  GEOMETRY_ONLY). Modes map to DIRECT/RECONSTRUCT_THEN_LAYER/HYBRID; actual
  regeneration hashes must match tool outputs.
- skill_usage: unique `{id,status,reason,execution,verification}` rows. Status
  DISCOVERED → READ → SELECTED → EXECUTED → VERIFIED is the highest evidenced
  stage, plus SKIPPED/BLOCKED with reasons. execution references procedure
  artifacts; verification references PASS checks in this receipt. Reading a
  Markdown file/hash or selecting a route is not execution. Harness delivery
  starts at DISCOVERED; agent records later evidence. FINAL requires executed
  reconstruction/character procedures and transfer when selected. A specialist
  does not waive the general geometry owner.
- Schema-3 escalation adds `checkpoint,previous_method,next_method,evidence`
  to `issue,attempts,state,owner,note`. At two failed attempts, checkpoint is a
  saved .blend artifact, methods differ, evidence references named checks.
  ESCALATED keeps dependent stages OPEN; RESOLVED needs PASS checks.

FINAL additionally requires `face_identity`, `hair_occlusion` when applicable,
and `seam_invisibility`/`uv_binding` for transfer. It consumes transfer identity/
seams/material/reopen review and pending bake/cleanup. Visible seams or changed
identity are FAIL. Claimed capabilities must cite accepted checks. Final coverage
is still mandatory. File provenance cannot prove tool invocation or pixels;
real image review and a scoped production experiment remain necessary.

## Schema v2 — real Blender capture metadata (legacy workflow)

Non-character or historical workflows may use schema_version 2. Version 1 legacy receipts
remain readable, but their camera/framing placeholders are weaker than
Blender's real capture metadata.

For each captured fixed view or closeup, copy the actual PNG and capture.json
to the task evidence folder, preserving both. Set the receipt image to the
relative PNG path and its actual SHA-256. Build the setup by calling
setup_from_capture_metadata() from tools/qa_gate.py with the decoded
capture.json object. Never invent an arbitrary camera string, direction or
textual framing label.

The v2 setup has EXACT fields target, objects, frame, fps, framing,
resolution, mode, lighting, projection, camera_matrix, ortho_scale.
These are read directly from the capture metadata. Frame may be a finite
float (Blender reports 1.0 even for frame 1); framing is an object with
center:[x,y,z] and positive span; camera_matrix is the 16-value world
camera transform. The checker derives camera direction from that matrix
and verifies each fixed preset, including +/-45 degrees. Before/after
numeric differences at negligible floating-point precision are tolerated;
genuine recropping or camera changes are rejected.

Each real PNG capture is VISUAL REVIEW REQUIRED until the operator opens
and evaluates the pixels. A structurally valid v2 receipt is still NOT
automatic artistic approval. For real evidence paths use --verify-files
when checking the packet; missing/tampered images must fail.

Use schema v1 only when consuming historical QA receipts created before
the metadata-aligned v2 setup. A new v2 receipt does not rewrite those
older records. Surface Transfer record schema v2 and this QA receipt
schema v2 are different task-local documents.

## Schema version 1

Required top-level fields: schema_version (1), asset, profile, changed,
animated, requested_capabilities, captures, closeups, checks, protected_zones,
user_flags, capabilities, escalation.

Profile values are CHARACTER_FINAL, FACE_TRANSFER_FINAL, FOCUSED_3D_REPAIR.
The first requires front, side, back, three_quarter, high_45 and low_45
orthographic views. The face profile requires front, side, three_quarter,
high_45, low_45 and a face closeup. Focused repair requires high_45, low_45
and a changed-region closeup, not the entire asset approval.

Each capture has id, view, phase BEFORE or AFTER, status, image, setup,
reviewer and observations. An image is a {path,sha256} evidence object,
relative to the receipt directory; SKIP uses null and a reason. Each setup
stores target, frame, framing, resolution, mode, lighting, projection,
camera and direction. Fixed diagnostic projection is ORTHO; camera
direction high_45=(0,-1,+1), low_45=(0,-1,-1), normalized or equivalent.
Use values from the actual capture manifest, not invented metadata.

When changed=true the required final BEFORE and AFTER views, closeups,
camera, lighting, framing, pose/frame, resolution, target and mode must
match. Do not auto-reframe. Capture success alone is REVIEW_REQUIRED.

Checks and protected zones use status, reviewer, observations and evidence
IDs referencing captures/closeups. User flags additionally use action
MUST_FIX, PRESERVE or DO_NOT_REINTERPRET and cannot silently disappear.
The user-marked requirements are authoritative; the checker cannot detect
dishonest omission of a user instruction.

Capabilities are independent:
STATIC_VISUAL / EXPORT / RIG_READY / DEFORMATION_READY / GAME_READY.
Each records status, reviewer, observations and evidence linked to named
checks. NOT_APPLICABLE is an explicit non-PASS. GAME_READY requires
static visual, export, and actual engine_preview PASS; animated assets
add rig, deformation and animation_playback PASS. A GLB import is not
proof of deforming/playing correctly.

Escalation entries track issue, attempts, state RESOLVED/ESCALATED, owner
and note. After two unsuccessful correction passes, escalate the defect.
Do not repeatedly modify approved shapes to chase a rendering illusion.

## Visual acceptance interpretation

Oblique high/low 45-degree views show contact, underside, volumes and
intersections. Perspective can exaggerate the nearer head or feet; even
orthographic oblique views foreshorten projected length. Never resize head
or legs based on one such view. Verify via reference-matched orthographic
front/side and locked Model Contract.

Face-transfer acceptance requires original source vs prepared/baked texture,
neutral unlit albedo, neutral lit closeup, eye/nose/mouth landmarks,
intentional hair occlusion and target appearance if requested.
A visible rectangular/oval seam, color halo or altered approved expression
is FAIL. A JSON checker cannot establish that by itself.

This file is evidence protocol, not a new Skill, Model Contract, or
authority to rebuild geometry. A final gate stays OPEN if a required
criterion was skipped, uninspected or lacked real reviewed evidence.
