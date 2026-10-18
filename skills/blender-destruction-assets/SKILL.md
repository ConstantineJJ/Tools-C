---
name: blender-destruction-assets
description: Prepare material-aware destructible game assets in Blender, including structural segmentation, fracture interiors, collision proxies, physics budgets and intact/destroyed variants. Use for breakable-asset preparation; surface wear, sculpt-only damage, animation-only work and export-only delivery keep their owners.
---

# Blender destruction assets

Read the required [foundation contract](../../docs/foundation.md),
[Blender pipeline](../blender-pipeline/SKILL.md), and
[physics and verification](references/physics-and-verification.md).
Prepare an editable game asset whose breakup follows construction, material and
gameplay. A fracture operator completing successfully is not asset acceptance.

## Instruction priority and ownership

Follow user scope, current project/engine constraints, approved source and existing
design locks before example fracture recipes. Keep numeric budgets, dimensions,
damage thresholds, networking policy and cleanup times project-local. A new
destruction stage on an approved model does not restart source modeling or PASS0.
Complex new designs still follow the pipeline's applicable design guidance.

Own destruction planning, detachable-component segmentation, material-aware
fracture geometry, newly exposed interiors, piece/body mapping, physics proxies,
rest transforms and intact/destroyed variants. Preserve the original intact source
and unrelated UVs, artwork, rigs, Actions, shared users and scene contents. Work on
a scoped copy before topology replacement; never globally remesh a mixed-material
assembly just to make a cutter succeed.

| Adjacent task | Owner and boundary |
|---|---|
| New crate, wall, bench, vehicle, device, tree or road form | Matching prop/architecture/environment/vehicle/product/vegetation/infrastructure owner; reuse its construction and approved dimensions |
| Sculpted dents, chips, cracks or torn edges as the main operation | [Sculpting](../blender-sculpting/SKILL.md); return its result to this owner when actual detachable pieces are required |
| Cosmetic scratches, crack textures, rust or chipped paint | [Polishing](../blender-posteffects-polishing/SKILL.md); a crack decal does not make a breakable asset |
| UV/bake/PBR mechanics beyond new fragment interiors | [Surfaces](../blender-pipeline/references/surfaces.md); retain exterior mappings and material roles |
| Bones/weights or authored collapse motion/Actions | [Rigging](../blender-rigging-skinning/SKILL.md) or [animation](../blender-animation/SKILL.md); Blender physics preview here does not authorize rebuilding those systems |
| Output file and fresh import | [Export validation](../blender-export-validation/SKILL.md), carrying the piece/body map and rest transforms |
| Godot asset wrapper, collision and imported-resource behavior | [Godot integration](../godot-asset-integration/SKILL.md); general damage/controller/gameplay implementation belongs to [godot-project](../godot-project/SKILL.md) when requested |
| Read-only assessment | [Verification](../verification/SKILL.md); a reported defect alone does not authorize fracture edits |

## Destruction plan before cutting

Inspect actual geometry/connectivity, thickness, units, transforms, modifiers,
material regions, attachment construction and target platform. Name the trigger
(impact, damage threshold, scripted event), affected zone, parts that remain,
support/anchor behavior and intended result (opening, loss of cover, debris or
visual rubble). Separate observed construction from inferred hidden structure.
If the target engine is unspecified, prepare a neutral mesh/metadata handoff and
state the assumption; do not invent engine settings or claim runtime acceptance.

Choose the least costly representation that achieves that behavior:

- intact-to-destroyed static swap when no moving debris is needed;
- a small set of detachable constructed components for assembled objects;
- pre-fractured solids with authored impact zones and optional clusters;
- hybrid large physical pieces plus nonphysical chips/dust or baked motion.

Specify **render-piece count, maximum simultaneously active bodies, shapes per
body/total hulls, simultaneous destroyed instances, fragment minimum scale,
render/material budget, and sleep/removal/reset policy**. Several visible pieces
may share one body; one body may use several simple collision shapes. More
clusters do not guarantee a cheaper worst-case burst when all leaves activate.
If no measured budget exists, propose a conservative provisional budget and
identify it as untested. Eight readable bodies can be better than one hundred
small bodies; neither number is a universal default.

## Construction and material decisions

Read the applicable sections of [material recipes](references/material-recipes.md)
before segmentation. Choose separation at real joints first, then fracture within
components only where the brief requires it. Mixed materials keep distinct rules
and connections. Uniform random Voronoi/Cell Fracture is a tool for suitable solid
regions, never the universal material model.

- **Wooden crate:** boards, braces, frame and metal fittings remain identifiable;
  splits follow each member's grain, with selective cross-grain breaks.
- **Masonry wall:** stones/bricks and mortar joints determine breakup; preserve
  the supported remainder. A concrete slab has different fracture logic.
- **Glass:** decide pane/vessel and glass type; shards, impact cracks or retained
  laminated webs follow that choice. Do not apply a flat-pane recipe to a bottle.
- **Metal/plastic/composites:** prefer seams, joints, panels, bending/tearing or
  shell failure as appropriate; do not automatically treat ductile metal as rock.

Prove one representative joint, break and exposed interior before multiplying
fragments. Keep stable piece IDs, source component/material, body/cluster owner,
support/connection pairs and parent-relative **rest transforms** in the task's
existing assembly graph or a small task-local table. Record seed/settings only
for procedural regions; names or a random seed alone cannot restore assembly.

## Geometry, interiors and variants

1. Isolate the authorized break region and keep an editable intact source.
   Ensure solids have usable thickness/closed cuts; fix only the relevant defects.
   Check installed Blender/add-on/operator versions before invoking them. If Cell
   Fracture is absent, use bounded manual/Boolean/bisect cuts on copies or report
   that tool limitation; do not silently install tools or change the whole asset.
2. Cut along the chosen joints/pattern. Cap new break faces, orient normals,
   remove duplicate/internal cut artifacts and repair slivers. Thin shells need
   believable thickness; do not fill a hollow vessel with a solid interior.
3. Retain an explicit inside/outside face distinction. Preserve exterior UVs and
   graphics; unwrap newly exposed faces with useful texel scale and padding.
   Give interiors the correct substrate/end-grain/aggregate rather than stretching
   exterior paint, labels or glass textures across caps. Bake procedural surfaces
   when the selected exporter/engine cannot reproduce them.
4. Review intact, reconstructed rest assembly, exploded inspection and requested
   destroyed state. Exploded inspection is a temporary diagnostic view, not the
   authored rest state. Match root scale/orientation and attachment placement
   between variants; exclude source backups, proxies and inspection helpers from
   render delivery unless explicitly part of the export contract.
5. Prepare physics and execute the scoped checks in the required
   [physics/verification reference](references/physics-and-verification.md).

Deliver an intact source, the requested fragment/destroyed variant, collision
proxies or their declared generation recipe, and enough piece/rest/body data to
rebuild the assembly. Use existing task records; no new global schema, report
engine or default dossier is required. Static rubble, pre-fracture rest assembly
and simulated collapse are different deliverables; provide the ones requested.

## Acceptance and stop

Keep structural, visual, export and target-runtime results separate. Inspect
material-specific breakup, cut interiors, reconstructed seams and supported
remainder at gameplay distance and in close-up. Check actual contact geometry;
an overlapping bounding box is only a candidate pair, not proof of penetration.
Recover assembly from stored transforms without manual alignment. If engine work
is in scope, test impact, quiet rest, variant switching and reset in the actual
target scene with the declared concurrent-body budget. A Blender preview or GLB
import cannot certify that behavior. Report unrun required checks as OPEN/SKIP
with the missing evidence/next owner; stop after the authorized scope passes.

## Pitfalls / Lessons Learned

- Identical pebble-like chunks on wood, metal and masonry indicate the algorithm
  replaced material/assembly reasoning. Revisit the construction plan first.
- An instant explosion at activation often comes from proxy penetration, inflated
  margins or duplicate intact collision. Inspect those before adding solver cost.
- Visible gaps after fracture often come from cutter gaps, bevels or rest-transform
  drift. Fix reconstruction; do not conceal them by expanding all pieces.
- Tiny screws and splinters rarely need independent bodies. Attach/cluster or
  represent them visually when gameplay permits.

Optional [research notes](references/research-notes.md) record primary sources,
version limits and which guidance is a Tools_C synthesis rather than a quoted rule.
