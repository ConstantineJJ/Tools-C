# Character QA practical test playbook — isolated session

Date: 2026-10-08. Read this in the separate test conversation after the user
provides the reference. It does not authorize a Hub update or irreversible
modification of the approved source character.

## Before work

Read Project-pulse.md and the QA, Verification, Reference Surface Transfer,
Character Modeling and Model Contract Skills. Until Blender MCP Server is
restarted, pass max_chars=60000 explicitly to get_skill_context; the running
server may still use the historical 50000 default. Never silently accept
truncated skill context. Capture protected source geometry, UV, approved eyes,
mouth and expression, head-to-body sizes, skull separately from hair, and
authoritative original reference. Keep source/BEFORE evidence untouched.

Plan a controlled Blender MCP Server restart only when idle. Inspect loaded
versus disk hashes; after opening a .blend verify actual queue health and
get_scene_info through a second RPC.

## Face-transfer comparison

- DIRECT: original observed facial pixels visible and projection-compatible.
- HYBRID: hair covers an eye/brow; preserve the visible features, generate only
  the missing bounded region and keep hair in front of the face.
- RECONSTRUCT-THEN-LAYER: significant occlusion with explicit authorization;
  the clean face is inferred, never an exact recovered source.
- All strategies: verify UV landmark registration, neutral unlit albedo, neutral
  lighting, preserved expression/identity and no pasted oval/rectangular seam.
  Visible seam or changed protected identity is FAIL.

## Final QA evidence

Capture fixed orthographic front, side, back, three_quarter, high_45 and low_45;
add critical face, hairline, neck, shoulder, torso/waist, hands/feet and changed
region closeups as applicable. Inspect the actual returned PNGs, not just status.
For a changed asset keep BEFORE and AFTER view, frame, target, resolution,
projection, lighting, pose and framing comparable. A high/low 45-degree view
reveals form and contacts; do not reshape head or legs on that view alone
without orthographic/reference-matched corroboration.

Each Blender capture outputs real capture.json metadata including numeric
frame (1.0 is valid), framing object, camera_matrix (16 floats), camera
projection, source object names, SHA-256 and PNG file. For new QA packets use
schema_version=2; build setup with qa_gate.setup_from_capture_metadata(data)
instead of making up a manual camera string or direction. Copy the actual PNG
into the task receipt folder, retain hashes, and run the checker:

    python tools/qa_gate.py TASK/qa_receipt.json --verify-files

Capture itself always starts as VISUAL REVIEW REQUIRED. The checker verifies
declared evidence consistency, not beauty or truth of the review. Keep separate
STATIC_VISUAL, EXPORT, RIG_READY, DEFORMATION_READY and GAME_READY statuses;
do not infer deformation or runtime readiness from appearance.

After one targeted correction recapture relevant views. After two failures,
escalate with evidence rather than repeatedly changing approved geometry.

## Report

Record the chosen transfer strategy and inferred regions, protected zones and
user MUST_FIX/PRESERVE/DO_NOT_REINTERPRET items, image paths/hashes, actual visual
observations, QA receipt result, limitations, runtime/bridge incidents and any
regression. Final acceptance remains OPEN if a mandatory view is uninspected.

Constantine Hub stays on v0.2.9. No application upgrade is required for QA.
