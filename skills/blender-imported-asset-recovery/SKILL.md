---
name: blender-imported-asset-recovery
description: Repair existing imported Blender assets with diagnosed geometry or topology defects, holes, unsafe joins, damaged UVs or textures, and semantic part separation. Use for recovery of supplied meshes; creation from scratch, read-only review, rig-only, animation-only and export-only tasks retain their owners.
---

# Imported asset recovery

Read the required [foundation contract](../../docs/foundation.md) and
[inspection procedure](references/inspection.md). Work on the model the user
already imported, or inspect a supplied file in an isolated scene when needed.
Do not require a second import or a reference-image reconstruction to repair an
available mesh. Sources may be scans, third-party assets or generated models;
no supplier, paid service, target engine or character type is required.

## Ownership and scope

Own recovery diagnosis, local mesh repairs, preservation decisions and semantic
segmentation of existing models. Reuse the specialists below for their methods.
Choose only the necessary operation; these are conditional routes, not sequential
PASS0–PASS7 stages or new MCP tools. Read-only inspection stays read-only even
when these procedures are explicitly loaded.

| Actual operation | Read before execution |
|---|---|
| Holes, weld candidates, degenerate geometry, normals, local topology | [Geometry repair](references/geometry.md); [retopology](../blender-pipeline/references/retopology.md) for replacement edge flow |
| Separate joined parts, detach glasses/clothes/wheels, repair cut boundaries | [Segmentation](references/segmentation.md) |
| UV/material faults, blurry maps, retexturing, baking or regeneration | [Surface recovery](references/surfaces.md) plus existing [UV/PBR mechanics](../blender-pipeline/references/surfaces.md) |
| Preserve or transfer existing logos, eyes, paint or reference artwork | [Reference Surface Transfer](../blender-reference-surface-transfer/SKILL.md) |
| Local sculpt correction or substantial form redesign | [Sculpting](../blender-sculpting/SKILL.md) or the actual domain modeling owner |
| Bone/rest-pose/weight changes; clip edits | [Rigging](../blender-rigging-skinning/SKILL.md); [animation](../blender-animation/SKILL.md), only for the requested or repair-dependent change |
| Fracture/debris, physical breakage, intact/destroyed variants | [Destruction](../blender-destruction-assets/SKILL.md); ordinary part extraction is not fracture |
| Output file/fresh import; target Godot integration | [Export validation](../blender-export-validation/SKILL.md); [Godot integration](../godot-asset-integration/SKILL.md), when requested |

Preserve silhouette, proportions, functional clearances, identity, existing UVs,
images, shape keys, weights, rest pose, Actions/NLA and dependencies unless the
requested repair requires a bounded change. Inspect linked/shared mesh, material
and image users before editing; isolate affected data when unrelated users must
remain unchanged. Do not globally purge or apply modifiers/transforms to clean up.
Keep the original source and at most one intentional recovery checkpoint; exclude
it from delivery exports. Save dirty image pixels explicitly, not just the blend.

Reuse existing design locks and valid Model Contract bindings. A local repair of
an existing asset does not invent or restart PASS0. Substantial new design or
reference reconstruction follows the current pipeline's applicable prerequisites;
the recovery label cannot exempt it from those gates.

## Repair cycle

1. Inspect actual scene, selection/mode and named target objects; establish a
   recoverable baseline and comparable views of the requested defect.
2. Locate the cause and affected region. Distinguish confirmed defect, suspected
   cause and intentional feature. A count of non-manifold edges is not a verdict.
3. Choose the smallest sufficient repair and name attributes/dependencies at risk.
   Preserve working source data through transfer/rebake if topology or UVs change.
4. Execute on that scope using available Blender operations; check the installed
   version/API and follow MCP Python preflight. Never assume an operation ran after
   an ambiguous timeout; inspect actual state before retrying.
5. Re-measure the defect and review comparable before/after views. Test affected
   deformation or part motion when relevant. If a local method repeatedly fails,
   recheck the cause and change method instead of increasing destructive strength.
6. Save the requested native asset and textures; export only when part of the task.

### Before replacing an imported part

A new mesh is not the default remedy for an imperfect original. Before a local
replacement or major separation, identify the exact object/region and ask:

- Which accepted silhouette, proportions, functional gaps, UV artwork and
  distinctive details must survive? Compare the relevant fixed views.
- Have all pieces of the old part been found, including back faces, hidden
  brackets, tabs and loose remnants? Check the assembled result for intersections.
- Does the replacement have believable anchors and enough clearance through
  its intended motion? Test affected pivots/axes, not just the neutral pose.
- Can the existing UVs, texture pattern and material identity be transferred or
  locally repaired instead of replaced with generic shapes or textures?
- If export is requested, has a fresh import preserved visible materials,
  images, axes and parts? A Blender-only shader or driver is not an engine feature.

Stop after the agreed repair is accepted. Further redesign is a separate scope;
a numerical geometry improvement alone cannot justify changing protected form.

Do not default to whole-mesh welding, closing all openings, voxel remesh, automatic
retopology, smoothing or decimation. No universal weld distance, polygon budget,
texture size or bone count. A critical operation with unresolved target identity
or preservation conflict stops only dependent edits; continue independent work.

## Verification and delivery

Use existing [verification](../verification/SKILL.md) and QA receipts where the
domain requires them. Record PASS / WARN / FAIL / SKIP with scope and evidence;
SKIP distinguishes inapplicable from unrun required checks in its reason. Missing
required checks keep acceptance OPEN. Do not invent a second recovery schema,
validator or certification system. A structural/import PASS does not prove visual
quality, texture fidelity, animation or engine readiness.

Report concisely: actual repairs and preserved features; relevant before/after
measurements; regenerated versus source-derived texture detail; real saved paths;
remaining defects and untested gates. For segmentation include part names and
requested individual exports. Do not produce a full operator dossier for a minor
fix. Full humanoid/face-transfer final acceptance still follows foundation QA;
local repair acceptance must not claim whole-character approval.

## Pitfalls / Lessons Learned

### RECOVERY-001
- Symptom: a repaired mesh has fewer boundary edges but lost openings, UV alignment or moving parts.
- Cause: treating diagnostic counts as defects and applying global cleanup.
- Rule: classify each affected region and compare preserved attributes before accepting the local repair.
- Automated check: routing and context tests prove discovery only; native fixtures exercise selected Blender operations.
- Verification: inspect the actual repaired asset, preserved openings, seams and requested part behavior.
- Added from / context: imported-asset recovery integration, 2026-10-28.
- Version: 0.1.0.

### RECOVERY-002
- Symptom: imported vehicle repair looks heavier or loses distinctive arches, wheel art and attachment detail despite fewer visible mesh defects.
- Cause: replacing broad regions with generic pieces before identifying protected source form and occluded remnants.
- Rule: run the local replacement gate; preserve accepted source artwork and proportions, inspect hidden leftovers and test anchors/motion before accepting a replacement.
- Automated check: structural checks can confirm named parts and pivots only when the asset declares them; silhouette, visual clearance and export appearance require inspected views/fresh import.
- Verification: compare protected angles, original UV/pattern, hidden interfaces and affected articulation; fresh-import the requested delivery format.
- Added from / context: user-accepted AdventurerHD imported vehicle recovery lessons, 2026-10-31; case-specific wheel and suspension counts are not universal thresholds.
- Version: 0.1.1.
