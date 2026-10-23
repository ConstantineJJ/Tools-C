# Blender Character QA

Use for a requested asset review or to validate a Blender change. QA reports observed results and routes defects to the owning procedure; it does not silently redesign the asset.

## Instruction Priority

For new reference characters, consume the [existing receipt's workflow gates](../../blender-character-modeling/references/workflow-gates.md):
FACE technology choice, accepted primary forms before DETAIL, evidence of actual
procedure execution, and saved-state method reconsideration after two failures.
Final QA does not retroactively prove that these production checkpoints ran.

Use the user's acceptance criteria, project/target contracts, [pipeline core](core.md), then this checklist. Never promote a lower verification level to visual or runtime acceptance; see [verification](../../verification/SKILL.md).

## Domain constraints

- Protected: source asset and diagnostic comparability; QA is read-only unless a specific fix is requested.
- Owned edits: temporary diagnostic state only, restored afterward.
- Acceptance: each applicable criterion has evidence, severity and owner; unrun checks are marked SKIP with a reason.

## Required final character QA matrix (not every iteration)

For final visual acceptance of a 3D humanoid, regardless of whether the operator
modified geometry or only facial surfaces, capture and **inspect**:
1. Orthographic front, side, back and front three-quarter, with the
   reference-matched pose/camera when proportional comparison is claimed.
2. Named orthographic oblique **high_45** and **low_45** (camera direction from
   subject (0,-1,+1) / (0,-1,-1)). These expose head/shoulder, sole, junctions,
   clothing overlap, surface attachment and concealed defects.
3. Closeups of all changed or disputed areas; for a face transfer,
   compare source/clean patch/baked face and neutral base color, neutral lit
   plus target material if part of the task.
4. Every **user-marked** MUST_FIX, PRESERVE and DO_NOT_REINTERPRET zone with
   specific evidence, before/after where the source exists.

**Projection warning:** the high/low views foreshorten depth and length; a
perspective version additionally changes apparent head/foot scale with distance.
Neither is independent evidence of disproportionate head, feet or legs. A
proportion-driven geometry fix needs confirmation against a reference-matched
orthographic/near-orthographic frontal or lateral view and the locked Model
Contract. Do not "repair" geometry to cancel camera distortion.

The final QA profile requires comparable BEFORE/AFTER captures of changed
assets: same view, target, pose, frame, projection, camera preset, framing,
resolution, lighting and material mode. If comparison is unavailable, report
why rather than substitute an automatic recrop. A scoped local iteration may
inspect fewer views, but cannot call itself full CHARACTER_FINAL acceptance.

Face identity and seam integration: visible patch perimeter, tone halo, doubled
features, floating eye/mouth or inconsistent hair ordering is a named FAIL.
Preserve approved eyes/mouth and other protected regions between attempts.
After one bounded correction, recapture focused views; after two failed attempts
escalate to user/owner with unresolved risk instead of infinite touch-ups.

Report statuses per named criterion: PASS, WARN (nonblocking), FAIL,
SKIP (unrun/inapplicable with reason), REVIEW_REQUIRED (captured but not
reviewed). A required SKIP/REVIEW_REQUIRED never closes final acceptance.
Separate STATIC_VISUAL, EXPORT, RIG_READY, DEFORMATION_READY and GAME_READY
statuses; successful import or render cannot certify the others. Use the
task-local [QA receipt](../../../tools/qa_gate.py) for strict completeness
when full acceptance is requested; the checker validates metadata/provenance,
not the visual quality of pixels.

## Choose evidence

Use only applicable checks: object hierarchy, transforms and normals for geometry; fixed front/side and relevant other views for silhouette/reference; mesh integrity and seam/shading for topology; neutral plus required bend/twist poses for deformation; Action channels, extremes and loop endpoints for animation; selected objects, materials, skeleton, clips and scale for export.

Use [capture_viewport](../../../docs/blender-evidence.md) to keep before/after target,
frame, framing, resolution, lighting and mode identical. Keep STRUCTURAL PASS separate
from VISUAL SKIP / VISUAL REVIEW REQUIRED / VISUAL PASS; open and inspect the actual images.
If the capture tool is missing or fails, attempt the Blender Python or offline-render
fallback documented there before reporting a blocked required visual gate. A beauty render, successful API call or clean import cannot prove other views, deformations or target-engine behavior. For export, fresh-import when feasible and inspect the specific target engine when that is part of acceptance. See [QA evidence matrix](techniques/qa-evidence.md) for detailed checks and severity examples.

## Anti-degradation and stop

Compare requested improvement with other views, silhouette, topology, deformation, animation, materials and other affected assets. Classify defects as blocker, major, minor or note; give evidence and likely owner. Stop when all scoped checks are reported as PASS, FAIL, WARN or SKIP with reason. Do not claim production acceptance when a required visual, pose or engine check was not run.
