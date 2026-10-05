---
name: blender-environment-assets
description: Create or revise standalone site fixtures such as benches, lamps, fences and bollards. Own construction, mounting, placement and fixture families; route building-integrated parts and roads elsewhere.
---

# Blender environment assets

Read the required [foundation contract](../../docs/foundation.md) and the general [Blender pipeline](../blender-pipeline/SKILL.md). This skill owns discrete reusable environment fixtures, not the whole environment scene.

## Instruction priority

Follow the user's request, active project/profile, approved references and target-engine constraints before generic environment-art conventions. Real-world construction is evidence for believable proportions, attachment and wear; it is not authority to erase deliberate stylization. Do not turn every object into a modular kit, high-poly bake or unique texture merely because those workflows are common.

## Scope and ownership

Own:
- benches, street lamps, posts, signs, bins, bollards, hydrants, barriers, standalone railings and fence panels, planters, bike racks and similar site/street fixtures;
- reusable outdoor/service fixtures whose identity depends on how they are mounted, repeated or placed in an environment;
- blockout, proportion, silhouette and construction logic for those assets;
- family/variant planning for repeated fixture sets;
- placement-facing pivots, ground/attachment contact and repeated-instance strategy;
- asset-facing hard-surface decisions, bevel/shading strategy, material segmentation and UV/texture strategy;
- environment-specific wear and variation decisions;
- bounded LOD/readability preparation when explicitly part of the asset task.

Route:
- integral windows, doors, facade trims and building modules to `blender-architecture-environment`;
- continuous roads, curbs, sidewalks, gutters, paths, medians and network geometry to `blender-roads-infrastructure`;
- furniture, containers, tools, handheld/interior clutter and narrative small objects to `blender-props`;
- vehicles to `blender-vehicle-modeling`;
- appliances/electronics to `blender-product-electronics-modeling`;
- vegetation to `blender-vegetation`;
- primary sculpting/damage sculpt to `blender-sculpting`;
- final GLB delivery to export validation and target-engine integration.

Boundary rule: classify by production role, not size alone. A freestanding public bench belongs here; a movable dining chair usually belongs to props. A discrete fence panel/gate can belong here; a kilometer-long fence network or spline-managed corridor belongs to the infrastructure owner.

## Domain constraints

- Protected: approved form, scale, placement/attachment pivots, shared sources,
  materials/UVs and downstream data outside scope. Establish the foundation task contract.
- Owned changes: the named domain geometry and necessary scoped dependencies.
- Acceptance: inspected target and alternate views prove the requested form;
  applicable protected data and context placement survive.

## Workflow and conditional reading

Prove scale, supports, mounting and placement in context before fasteners or wear. A single bench does not require a library. Repeated fixtures preserve intended shared geometry and anchors.

Inspect → blockout → [develop primary/secondary forms](../blender-pipeline/references/techniques/form-development.md)
→ representative construction test → scoped detail/surfaces → compare → handoff.
For a revision, isolate the named defect and stop after its evidence passes.

Read only the relevant procedure:

| Need | Reference |
|---|---|
| Scale, reference authority or representation unclear | [Planning](references/planning.md) |
| Domain construction and editable form decisions | [Construction](references/construction.md) |
| Reuse/variants, bake/UV, wind, LOD or other requested production options | [Production options](references/production-options.md); select applicable sections |
| Domain checks, safeguards, complexity and next-owner handoff | [Validation and handoff](references/validation-and-handoff.md); select applicable sections |
| Color, soft highlights and restrained directional texture | [Clean stylized surfaces](../blender-pipeline/references/techniques/clean-stylized-surfaces.md) |
| A representative visual sample before repetition | [Lookdev gate](../production-lookdev-gate/SKILL.md) |

## Anti-degradation and stop

Use [QA profiles](../blender-pipeline/references/techniques/qa-profiles.md).
Compare fixed relevant views, form, attachments and affected shared users.
Keep source editability; do not blindly join/remesh/realize or remove hidden
geometry that the target may expose. Project dimensions and budgets stay local.
Correct bounded regressions or restore only the attempted change. Stop when the
scoped form and applicable checks pass; report missing required evidence or a
protected-data conflict with its next owner. Do not start unrelated stages.

## Pitfalls / Lessons Learned

The maintained domain lessons are in [validation and handoff](references/validation-and-handoff.md).
Their IDs and substantive procedures are retained. Optional [research notes](references/research-notes.md)
explain sources and limitations; they are not mandatory production context.
