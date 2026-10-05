---
name: blender-vegetation
description: Create or revise trees, shrubs, grass, flowers and vines. Own growth hierarchy, canopy/cluster shape and vegetation representation; wind, seasonal variants and LOD are conditional on the task.
---

# Blender vegetation

Read the required [foundation contract](../../docs/foundation.md) and the general [Blender pipeline](../blender-pipeline/SKILL.md). This skill owns plant-specific modeling, clustering, variation and wind-ready source structure, not terrain authoring or the runtime wind shader itself.

## Instruction priority

Follow the user's target, active project/profile, approved species/reference and art direction before generic botanical conventions. Real growth patterns are evidence for convincing structure; they are not authority to erase deliberate stylization, fantasy anatomy or low-poly simplification. Do not turn every plant into a procedural system, alpha-card asset or photoreal scan workflow when the target does not benefit.

## Scope and ownership

Own:
- trees, saplings, shrubs, bushes, grass, flowers, reeds, vines and plant clusters;
- trunk/root flare and branch hierarchy required to make the plant read;
- crown/canopy silhouette and branch/leaf density distribution;
- leaf, needle, blade and petal representation decisions: direct geometry, alpha cards/atlases, baked clusters, procedural instances or hybrid;
- foliage clusters, grass patches and reusable plant subassemblies;
- plant-family/species variation while preserving recognizable growth logic;
- vegetation-facing Geometry Nodes, linked data and instancing/scatter source design;
- wind-ready separation, branch/leaf pivots and source attributes when downstream deformation requires them;
- vegetation UV/atlas/material organization, normals strategy and seasonal/damage variants;
- vegetation-specific LOD/readability and structural QA.

Route:
- terrain sculpting, landscape grading and non-plant ground shape to the appropriate terrain/project workflow;
- roads, sidewalks and paths to `blender-roads-infrastructure`;
- buildings and architectural supports to `blender-architecture-environment`;
- planters, benches, pots and other non-plant environment fixtures to `blender-environment-assets` or `blender-props` by role;
- a primary generic sculpting task to `blender-sculpting`, while vegetation retains ownership of plant growth logic;
- generic rig implementation or animation Actions to rigging/animation owners when bones/Actions are explicitly required;
- final GLB delivery and target-engine wind/material validation to export/integration owners.

Boundary rule: classify by the **living plant system** being authored. A tree growing through a planter remains vegetation for the tree and environment-assets/props for the planter. A vine attached to a wall is vegetation; architecture owns the wall and provides attachment/reference surfaces.

## Domain constraints

- Protected: approved form, scale, placement/attachment pivots, shared sources,
  materials/UVs and downstream data outside scope. Establish the foundation task contract.
- Owned changes: the named domain geometry and necessary scoped dependencies.
- Acceptance: inspected target and alternate views prove the requested form;
  applicable protected data and context placement survive.

## Workflow and conditional reading

Prove trunk/branch rhythm, crown masses and negative spaces before leaves. Test a few shaped clusters before density. Preserve growth hierarchy and intentional species/style cues; random transforms do not repair a spherical crown.

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
