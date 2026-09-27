# Blender Character QA

Use for a requested asset review or to validate a Blender change. QA reports observed results and routes defects to the owning procedure; it does not silently redesign the asset.

## Instruction Priority

Use the user's acceptance criteria, project/target contracts, [pipeline core](core.md), then this checklist. Never promote a lower verification level to visual or runtime acceptance; see [verification](../../verification/SKILL.md).

## Domain constraints

- Protected: source asset and diagnostic comparability; QA is read-only unless a specific fix is requested.
- Owned edits: temporary diagnostic state only, restored afterward.
- Acceptance: each applicable criterion has evidence, severity and owner; unrun checks are marked SKIP with a reason.

## Choose evidence

Use only applicable checks: object hierarchy, transforms and normals for geometry; fixed front/side and relevant other views for silhouette/reference; mesh integrity and seam/shading for topology; neutral plus required bend/twist poses for deformation; Action channels, extremes and loop endpoints for animation; selected objects, materials, skeleton, clips and scale for export.

Use [capture_viewport](../../../docs/blender-evidence.md) to keep before/after target,
frame, framing, resolution, lighting and mode identical. Keep STRUCTURAL PASS separate
from VISUAL SKIP / VISUAL REVIEW REQUIRED / VISUAL PASS; inspect the returned images. A beauty render, successful API call or clean import cannot prove other views, deformations or target-engine behavior. For export, fresh-import when feasible and inspect the specific target engine when that is part of acceptance. See [QA evidence matrix](techniques/qa-evidence.md) for detailed checks and severity examples.

## Anti-degradation and stop

Compare requested improvement with other views, silhouette, topology, deformation, animation, materials and other affected assets. Classify defects as blocker, major, minor or note; give evidence and likely owner. Stop when all scoped checks are reported as PASS, FAIL, WARN or SKIP with reason. Do not claim production acceptance when a required visual, pose or engine check was not run.
