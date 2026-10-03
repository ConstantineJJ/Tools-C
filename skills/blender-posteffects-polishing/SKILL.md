---
name: blender-posteffects-polishing
description: Finish an existing Blender asset with refined materials/textures, localized dirt, scratches, chipped or peeling paint, surface cracks and motivated emission/glow. Use for late surface finishing and posteffects; route UV layout/baking, structural sculpt damage, rigging and export to their owners.
---

# Posteffects and polishing

Read the required [foundation contract](../../docs/foundation.md) and
[Blender pipeline](../blender-pipeline/SKILL.md). This is a late finishing stage
across asset domains, after the relevant shape/topology and surface prerequisites,
before final visual QA and delivery. It is not an additional geometry domain.

## Instruction Priority

Use the user's finish, active project profile, approved look/reference and delivery
constraints first. An asset can be clean, stylized, freshly manufactured or heavily
used. Wear and glow are choices justified by its brief, not mandatory decoration.
Exact map sizes, texel density, shader complexity, effect strength, light rig and
quality budgets belong to the project; do not promote example values into policy.

## Task contract and ownership

- **TASK:** improve the named asset's surface read and requested final effects.
- **MUST PRESERVE:** approved silhouette/topology, UVs, scale, hierarchy, pivots,
  rig/weights/Actions, authored labels, identity, unrelated materials/images and
  scene state. Name any authorized exception before using it.
- **MAY CHANGE:** scoped material assignments, node parameters/groups, texture
  layers/masks, decals and expressly requested presentation effects. A material
  slot change is in scope only on named faces/objects; preserve slot references.
- **SUCCESS:** inspected comparable images show the requested finish without
  losing form/readability; changed dependencies and delivery limitations are
  recorded. A generated PNG or green contract alone does not establish this.

Own final material refinement/assignment, texture cleanup and scale, material-aware
weathering, surface-only damage, motivated emissive regions and approved render
posteffects. Adding a missing finish material is allowed within this scope.

Ownership boundaries:

- [Surfaces](../blender-pipeline/references/surfaces.md) owns UV layout, high/low
  projection, bake settings and baseline channel/binding correctness. Hand off
  broken UVs, missing bakes or incorrect tangents before covering them with grunge.
- [Sculpting](../blender-sculpting/SKILL.md) owns dents, tears, fractures and damage
  that changes shape. Use texture/normal/bump for surface relief when it meets the
  brief; do not remesh or displace a protected silhouette as a finishing shortcut.
- [Retopology](../blender-pipeline/references/retopology.md) owns edge-flow repair;
  the original domain owner owns changes to construction/proportions.
- [Rigging](../blender-rigging-skinning/SKILL.md) and
  [animation](../blender-animation/SKILL.md) retain their owners. Static glow does
  not authorize animated flicker, a particle system or simulation.
- [Export validation](../blender-export-validation/SKILL.md) owns delivery and
  fresh-import checks; [Godot integration](../godot-asset-integration/SKILL.md)
  owns target-engine behavior. Blender compositor effects are presentation data,
  not an automatically portable material effect.
- Read-only inspection belongs to [verification](../verification/SKILL.md).
  A defect report is not permission to apply this finishing stage.

## Preflight and finishing workflow

Inspect the actual Blender version/renderer, named objects and their shared
materials/images, UVs, existing maps, shader outputs, target camera/distance and
delivery target. Establish the condition story: substrate/coating, age, use,
contact, gravity, moisture, maintenance and intended focal areas. Keep uncertain
choices provisional; use existing references rather than inventing new asset lore.

1. Capture and inspect a clean BEFORE under comparable neutral and intended
   lighting. Separate existing shading/UV defects from the desired finish.
2. Establish readable base materials before damage. Refine color, roughness,
   metalness and relevant layers; keep numeric maps in their intended data space.
   Change shared resources only at the intended sharing scope; use a recoverable
   copy/variant for an isolated asset or painted image.
3. Build named, adjustable effect layers/masks from broad condition zones to local
   wear to microdetail. Use causal placement and material transitions, with quiet
   areas. Inspect masks and channels independently when diagnosing artifacts.
4. Add emission or image effects only where the brief calls for them. Distinguish
   luminous material, emitted illumination and glare in the image. Inspect the
   underlying render with effects bypassed as well as the finished image.
5. Run the visual correction loop below, then hand off changed textures/materials
   and any unverified target behavior to QA/delivery.

Read [finishing techniques](references/finishing-techniques.md) when choosing masks,
damage representation, channel treatment, emission or compositor operations.
[Research notes](references/research-notes.md) identify the source-backed decisions
and their limits; they do not require Substance, Toolbag or paid assets.

## Visual QA and bounded correction

Use [Blender evidence methods](../../docs/blender-evidence.md). Render/capture
relevant full-asset views plus affected closeups and production-distance views;
open and inspect the actual PNGs returned by the tool or saved on disk. Solid views
help check protected form; material/rendered views are needed to judge this stage.

Record concrete defects: repeated grunge, uniform edge halos, implausible substrate,
wrong map space, seams, swimming projections, oversized bump, washed-out emissive
regions or bloom hiding labels. Correct only defects within the authorized owner,
recapture using the same camera/framing/light/exposure/view transform, and inspect
the AFTER. Record observations and artifact paths/hashes with the verdict.

If direct capture is unavailable, follow the documented Python-image route, then
the saved-candidate offline-render fallback. Inspect the produced image; do not
skip Visual QA because one tool is absent. A managed asset capture may omit the
scene compositor/world/lights: it can prove surface appearance only under its
documented setup. Use an explicit candidate-scene Render Result to judge requested
glare/compositing with the intended camera and settings. Preserve the working scene.
If no usable images or target renderer are available, mark that criterion SKIP
with its blocker and next owner rather than claiming finished visual acceptance.

## Safeguards, handoff and stop

- Keep editable layer controls and source texture versions; do not paint over the
  only original image or rewrite unrelated shared node groups.
- Check UV seams, mirrored/repeated sections, decal edges/alpha and moving-part
  boundaries. Object/world projections must not swim when the asset moves.
- Use actual available nodes/sockets in the installed version. Do not assume an
  old Eevee Bloom toggle or a tutorial's compositor socket layout exists.
- Test shader portability against the delivery profile. Bake unsupported procedural
  layers through surfaces when needed; identify compositor-only effects separately.
- Do not hide shading, geometry or bake defects with dirt, bright lights, grading,
  depth of field or bloom. Do not claim increased texture resolution adds detail.
- Keep effect density and material cost appropriate to the actual viewing distance;
  do not flatten deliberate stylization into universal photorealism.

Handoff names objects/faces, changed and shared resources, layer/mask controls,
texture paths and channel spaces, procedural dependencies, emission versus scene
posteffects, source versions, inspected BEFORE/AFTER evidence, protected-state
checks and blockers/next owner. Stop when the requested finish and relevant visual
criteria pass without material regression, or when a missing prerequisite/target
prevents acceptance. Do not start export, structural damage or another style pass
without it being part of the request.

## Pitfalls / Lessons Learned

### POL-001
- Symptom: every edge is bright and every recess is equally dirty.
- Cause: curvature/AO masks treated as final wear history.
- Rule: combine them with exposure, contact, direction and local edits; preserve quiet regions.
- Automated check: structural contracts do not judge believable wear.
- Verification: inspect masks and rendered wide/close views against the condition brief.
- Added from / context: source-backed finishing design, not a claimed asset incident.
- Version: 0.1.0, 2026-10-03.

### POL-002
- Symptom: glow looks impressive but labels disappear or delivery has no halo.
- Cause: emission, scene illumination and compositor glare conflated.
- Rule: keep the three controls distinct and declare target-dependent presentation effects.
- Automated check: routing/link contracts only; no image-quality certificate.
- Verification: inspect bypassed and finished renders plus the target when in scope.
- Added from / context: Blender Glare documentation and existing Visual QA fallback boundary.
- Version: 0.1.0, 2026-10-03.
