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

| Work | Procedure |
|---|---|
| Match supplied views or diagnose resemblance | [reference reconstruction](references/reference.md) |
| Create or substantially revise character geometry | [character modeling](../blender-character-modeling/SKILL.md) |
| Sculpt an organic form or region | [organic sculpting](references/sculpting.md) |
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
