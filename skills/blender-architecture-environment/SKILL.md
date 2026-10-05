---
name: blender-architecture-environment
description: Create or revise buildings, architectural shells and modular structure kits. Own building proportions, openings and assembly; route standalone fixtures and roads to their owners.
---

# Blender architecture & large structures

Read the required [foundation contract](../../docs/foundation.md) and the general [Blender pipeline](../blender-pipeline/SKILL.md). This skill owns architectural reasoning and reusable large-structure construction, not the whole environment pipeline.

## Instruction priority

Follow the user's target, active project/profile, approved concept/reference and engine constraints before generic architectural conventions. Real-world dimensions are a calibration aid, not authority to override an explicit stylized design. Never normalize intentional exaggeration, impossible architecture or asymmetry unless the task asks for it.

## Scope and ownership

Own:
- buildings, houses, sheds, towers, halls, industrial structures and similar large man-made forms;
- exterior shells and interior architectural shells when both are part of the same structure;
- blockout, scale, story height, wall/floor/roof relationships and major openings;
- deciding unique versus modular versus hybrid construction;
- reusable wall, corner, window, door, floor, roof, trim, column, beam and structural-detail modules;
- grid and pivot conventions for architectural pieces;
- architecture-facing use of tileable materials, trim sheets, decals and reusable material regions;
- assembly validation, repetition control and large-structure optimization decisions.

Route:
- benches, lamps, fences, bins, bollards and similar standalone environment objects to `blender-environment-assets`;
- roads, curbs, sidewalks, paths, gutters and network infrastructure to `blender-roads-infrastructure`;
- furniture and hand-held/interior detail objects to `blender-props`;
- vehicles to `blender-vehicle-modeling`;
- appliances/electronics to `blender-product-electronics-modeling`;
- vegetation to `blender-vegetation`;
- organic or damage sculpting as the primary task to `blender-sculpting`;
- final GLB delivery to export validation and target-engine integration.

A building can contain work owned by several specialists. Keep the architectural shell here and hand off embedded assets instead of turning this skill into a universal environment owner.

## Domain constraints

- Protected: approved form, scale, placement/attachment pivots, shared sources,
  materials/UVs and downstream data outside scope. Establish the foundation task contract.
- Owned changes: the named domain geometry and necessary scoped dependencies.
- Acceptance: inspected target and alternate views prove the requested form;
  applicable protected data and context placement survive.

## Workflow and conditional reading

Prove whole-building mass, openings and depth before decomposing a kit. A unique stylized house does not require a modular library. Lock grid/pivots only when reuse is part of the task.

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
