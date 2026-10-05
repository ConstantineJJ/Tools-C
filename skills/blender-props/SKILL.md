---
name: blender-props
description: Create or revise portable/interior furniture, containers, tools, hand-held objects and decor. Own prop form, construction and interaction; route street fixtures and specialized devices to their owners.
---

# Blender props

Read the required [foundation contract](../../docs/foundation.md) and the general [Blender pipeline](../blender-pipeline/SKILL.md). This skill owns prop-centric discrete assets, not every small object in a scene.

## Instruction priority

Follow the user's request, active project/profile, approved reference/concept and target-engine constraints before generic prop-art conventions. Real products and manufacturing are useful evidence for believable construction and scale; they do not override deliberate stylization. Do not force every prop through a high-poly/low-poly bake, sculpt pass, unique texture or destructive cleanup when a simpler representation satisfies the target.

## Scope and ownership

Own:
- furniture such as chairs, tables, shelves, cabinets, stools and movable interior pieces;
- containers, cases, crates, boxes, cans, bottles and storage objects;
- hand tools, workshop items, kitchenware, books, decor, clutter and small narrative set dressing;
- hand-held or character-interaction props where the asset itself is the modeling task;
- one-off hero props and families/sets of related props;
- blockout, scale, silhouette, functional construction and handling/placement logic;
- choosing direct realtime geometry versus high/low/baked, sculpt-assisted or hybrid production;
- prop-specific UV allocation, mirroring/stacking decisions, bake preparation and material separation;
- wear, damage, labels and storytelling that follow use/material history;
- prop-library pivots, subassembly hierarchy, variants and reuse packaging;
- bounded LOD/readability decisions when explicitly requested.

Route:
- building-integrated walls, doors, windows, stairs, architectural trims and built-in structural modules to `blender-architecture-environment`;
- benches, street lamps, bollards, hydrants, public bins, site barriers and similar standalone street/site fixtures to `blender-environment-assets`;
- roads, curbs, sidewalks, paths, crossings and connected network infrastructure to `blender-roads-infrastructure`;
- cars and wheeled vehicles to `blender-vehicle-modeling`;
- appliances, computers, monitors, TVs, consoles and engineered consumer/digital devices whose product-design construction is central to `blender-product-electronics-modeling`;
- vegetation to `blender-vegetation`;
- a primary sculpting task to `blender-sculpting`;
- final GLB delivery to export validation and target-engine integration.

Boundary rule: classify by **production role**, not physical size. A dining chair is normally a prop; a public park bench is environment-assets. A simple decorative radio can remain a prop if the task is scene dressing, but a close product-accurate electronic device with connectors, controls, vents and engineered assembly should route to product/electronics.

## Domain constraints

- Protected: approved form, scale, placement/attachment pivots, shared sources,
  materials/UVs and downstream data outside scope. Establish the foundation task contract.
- Owned changes: the named domain geometry and necessary scoped dependencies.
- Acceptance: inspected target and alternate views prove the requested form;
  applicable protected data and context placement survive.

## Workflow and conditional reading

Prove scale, silhouette, assembly and grip/interaction before microdetail. Choose direct mesh or high/low/bake from the actual target; neither a bake nor a unique texture is mandatory.

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
