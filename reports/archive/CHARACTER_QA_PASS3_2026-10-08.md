# Pass 3 — Mandatory character QA and visual evidence gate

Date: 2026-10-08
Scope: Tools_C canonical QA/Verification workflow, evidence contracts,
Blender capture helper and Blender-MCP-Co capture tool description.
No source character mesh/material/animation edits and no Hub upgrade.

## Review and changes

1. Tools_C/tools/blender_capture.py now provides stable ORTHO high_45 and
   low_45 camera presets, directions (0,-1,+1)/(0,-1,-1). The capture output
   is deliberately VISUAL REVIEW REQUIRED until the image is inspected.
   Blender-MCP-Co/mcp-server/blender_mcp_server.py description is updated;
   loaded server needs restart to pick up modified source metadata.
2. skills/blender-pipeline/references/qa.md establishes final acceptance views
   (front, side, back, three_quarter, high_45, low_45), changed-area closeups,
   source and post-bake face/seam comparisons, before/after alignment,
   protected approved features, user-marked MUST_FIX/PRESERVE/
   DO_NOT_REINTERPRET, escalation after two unsuccessful corrections, and
   separate readiness statuses.
3. skills/blender-pipeline/references/techniques/qa-evidence.md,
   qa-profiles.md, skills/verification/SKILL.md,
   skills/verification/references/evidence.md, and
   blender-reference-surface-transfer/SKILL.md consume those rules.
4. docs/foundation.md, AGENTS.md and blender-pipeline/SKILL.md now explicitly
   require a final QA receipt before claiming full humanoid VISUAL PASS.
   An unrun or skipped mandatory visual gate is OPEN, not assumed PASS.
5. tools/qa_gate.py: new task-local *evidence completeness* checker.
   It does NOT replace PASS 0/Model Contract and cannot assess image quality.
   Schemas are closed and images have contained PNG path/SHA-256 evidence.
   Profiles: CHARACTER_FINAL, FACE_TRANSFER_FINAL, FOCUSED_3D_REPAIR.
   Strict required captures, high/low directions, projection, before/after
   settings, affected closeups, named checks, user flags, protected zones,
   escalation, and five separate capability statuses.
   CLI codes 0 PASS, 2 OPEN/FAIL, 1 malformed/error.
6. tests/test_qa_gate.py: 17 positive and negative tests.
7. docs/qa-receipt.md defines consumer packet and truthful scope.
   .tooling/contracts.json includes checker/test/protocol source paths.
8. README.md and docs/blender-evidence.md updated to document new
   usage and selected renderable-parent dependencies.

## Technical limits and projection warning

At +45/-45 degrees the head or feet may appear distorted even when the
model is correct, due to foreshortening. Perspective can additionally
magnify near parts. Do not adjust skull, legs or foot scale based solely
on oblique views. Confirm in reference-matched orthographic views and
existing persistent Model Contract, protecting approved features.

A QA receipt recording PASS asserts that the operator reviewed actual
image evidence. The checker verifies only presence, declared reviewer,
hashes and comparable capture setup; it cannot know whether the operator
looked carefully or whether the visual verdict is truthful.

New named views do not by themselves make the final candidate game-ready.
STATIC_VISUAL / EXPORT / RIG_READY / DEFORMATION_READY / GAME_READY
have separate statuses and conditional dependencies.

## Verification receipts

- QA receipt focused tests: 17/17 PASS after refreshing the in-memory
  Python module (a stale imported module initially caused misleading
  test results; reloaded and retested).
- Tools_C self L1: 50 PASS, 0 WARN, 0 FAIL.
- New capture presets tested live against unchanged Agent_Red7.blend:
  high_45 and low_45 both produced real ORTHO PNG + SHA-256,
  status VISUAL REVIEW REQUIRED. Both files are in Tools_C/.local/captures.
  Required renderable parent mesh R7_Body_Torso included with R7_Face_Head.
- 129 relative Markdown links read and resolved successfully.
- Agent_Red7.blend: 477 objects, bpy.data.is_dirty=False,
  original SHA-256 f71ee07a612aad4793de69ab86e7bb2c50116ff22092dabf959b532985b66221.
- Blender MCP source metadata changed; deployment_info.restart_required=true.
  Managed capture reads the canonical helper dynamically, so the two
  new views were already executed via Blender Python. Do not claim a
  clean server cold-restart until actually tested.
- All prior full 201+ regression cases NOT RUN for this pass.
- No full real-asset visual resemblance, seam-invisibility or production
  animation acceptance has been claimed: next step is hands-on test.
- Local Files MCP tunnel was temporarily unavailable during this pass
  (client did not poll); changes were applied via the working Blender
  MCP Python runtime to local canonical text files, without scene edits.

## Constantine Hub v0.3.0 recommendation

Supplied Hub log shows running v0.2.9 and at startup says there is no
newer stable release. Later it contains Blender MCP CallToolRequest
error markers; some Local Files edit_text exceptions were expected
precondition failures when one replacement was requested but two matched.
The provided log does not establish that v0.3.0 is published or safe.
Do not install the unverified update during the QA baseline and active
MCP sessions. First verify tag, release SHA-256, updater rollback and
adapter health/restart compatibility, then schedule a controlled update.

## Next test (user-guided)

1. Restart Blender MCP server at a controlled point to load modified tool
   descriptions, then check deployment_info and live bridge after cold start.
2. Prepare a task-local final QA receipt with original/reference, BEFORE/
   AFTER captures for the scoped character, including both 45-degree views.
3. Inspect source features, neutral base-color, seams, occlusion, protected
   eye/mouth/head/body anchors, silhouette and required closeups.
4. Verify saved-file reopen and Godot/GLB target only when requested;
   use separate capability status instead of blanket game-ready PASS.
5. After successful full QA, revisit Hub v0.3.0 release validation.

No commit, version bump or GitHub release in this pass.


## Post-pass interoperability fix — 2026-10-08

Additional review exposed a mismatch between the original qa_gate v1
setup fields (invented camera/direction strings, integer frame and flat
framing) and the real Blender capture.json (16-element camera_matrix,
float frame, dict framing). This was not caught by the initial 17 QA tests.

- Added backward-compatible qa_gate schema_version=2 with
  setup_from_capture_metadata() and validation against the real camera
  world matrix, frame, fps, framing, object list, projection and scale.
  No guessed high_45/low_45 direction: it is derived from the matrix.
  Before/after comparisons use bounded numeric tolerance.
- Version 1 receipts remain valid; docs/qa-receipt.md now recommends
  version 2 for new work. Two real high/low 45 capture.json files from
  unchanged Agent_Red7 were parsed with the new helper; source PNG hashes
  matched. No art/identity judgment is claimed.
- Regression growth exceeded old skill context default 50000 chars.
  Three canonical routes failed full delivery. Tools_C mcp_runtime and
  Blender MCP Server on-disk default were raised to 60000; intentional
  explicitly smaller budgets still return missing_documents and receipts.
  Current live server requires a controlled restart to pick up its new
  signature. Until then specify max_chars>=60000 explicitly.
- Relevant independent Python 3.14 tests: QA 19/19, Surface Transfer
  14/14, Model Contract 28/28, Bridge Health 4/4, Form/Context Delivery
  12/12; total 77/77 selected tests PASS. Tools_C L1 50 PASS,
  0 WARN, 0 FAIL. Full unittest discover was attempted but exceeded the
  MCP request limit; test_check also timed out in a bounded run. Therefore
  the entire suite is NOT YET VERIFIED.
- The QA test-handoff procedure is docs/qa-test-playbook.md, intended for
  the separate practical test chat.
- The Local Files MCP tunnel was still disconnected in this work session;
  Blender MCP remained accessible. No running tunnel, Hub application or
  Blender scene was restarted/modified. Do not publish a release before
  the full suite and visual gate.
