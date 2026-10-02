---
name: blender-pipeline
description: Route multi-stage Blender asset work and specialist sculpting, topology, surface, rigging, import and QA tasks. Use blender-character-modeling for a focused character geometry task.
---

# Blender pipeline

Read the required [foundation contract](../../docs/foundation.md).

## Instruction Priority and task contract

Follow the user's request, active project/target rules and approved asset decisions.
Apply the foundation contract before changing an asset. Complete only the selected workflow and its evidence gate.

## Activation routing

Select only the reference matching the task:

For stage-only work, the named asset supplies context: follow the retopology,
surfaces, rigging, animation or export owner without restarting domain modeling.
For a read-only review, use verification. Load a domain owner alongside a stage
only when its geometry or domain decisions are also part of the request.

| Work | Procedure |
|---|---|
| Match supplied views or diagnose resemblance | [reference reconstruction](references/reference.md) |
| Create or substantially revise generic character geometry | [character modeling](../blender-character-modeling/SKILL.md) |
| Model animals, creatures, quadrupeds or anthropomorphic animal characters | [animal & anthropomorphic modeling](../blender-animal-anthropomorphic-modeling/SKILL.md) |
| Model buildings, architectural shells, modular building kits or large man-made structures | [architecture & large structures](../blender-architecture-environment/SKILL.md) |
| Model standalone environment fixtures, street/site furniture or repeatable outdoor set-dressing assets | [environment assets](../blender-environment-assets/SKILL.md) |
| Build roads, sidewalks, curbs, paths, crossings, medians or connected linear ground infrastructure | [roads & infrastructure](../blender-roads-infrastructure/SKILL.md) |
| Model furniture, containers, tools, clutter, decor, hand-held or interior set-dressing props | [props](../blender-props/SKILL.md) |
| Model cars, trucks, buses, motorcycles, trailers or other wheeled vehicles | [vehicle modeling](../blender-vehicle-modeling/SKILL.md) |
| Model household appliances, consumer electronics, computers, displays or other engineered product devices | [product & electronics](../blender-product-electronics-modeling/SKILL.md) |
| Model trees, shrubs, grass, flowers, vines or vegetation families | [vegetation](../blender-vegetation/SKILL.md) |
| Sculpt organic/hard-surface forms, use remesh/Dyntopo/Multires, or make bounded sculpt corrections | [sculpting](../blender-sculpting/SKILL.md) |
| Repair edge flow or deformation | [retopology](references/retopology.md) |
| Author UVs, bakes or PBR materials | [surfaces](references/surfaces.md) |
| Bones, bindings and weights | [rigging and skinning](../blender-rigging-skinning/SKILL.md) |
| Actions, loops and secondary motion | [animation](../blender-animation/SKILL.md) |
| GLB delivery and fresh import | [export validation](../blender-export-validation/SKILL.md) |
| Target Godot asset playback | [Godot integration](../godot-asset-integration/SKILL.md) |
| Inspect or repair a supplied model | [external intake](references/external-import.md) |
| Validate visual or structural quality | [character QA](references/qa.md) and [verification](../verification/SKILL.md) |
| Iterate on measured defects | [refinement](references/refinement.md) |

Blender-native and external-assisted production are both supported. Neither path implies a fixed skeleton, provider, genre or character. Read the [Tripo note](../../adapters/tripo.md) only for that source.

Use available Blender MCP inspection or bounded operations after confirming the actual scene, objects, selection, mode and Blender version. Legacy Blender entrypoints render this canonical context through tools/read_blender_skill.py; their generated routers contain no independent rules.

## Pitfalls / Lessons Learned

### BLD-001
- Symptom: adding animation unexpectedly remeshes or changes the rig.
- Cause: full production pipeline applied to a surgical task.
- Rule: load only relevant procedures, record preserved objects/Actions and compare afterward.
- Automated check: V1 proves declared file/provenance integrity; asset snapshots need task-specific QA.
- Verification: original Action channels, rig/rest pose, materials and fixed views remain valid.
- Added from / context: migrated Blender Core scope-lock and rigging procedures.
- Version: 0.1.0, 2026-09-21.
