# Tools_C — central agent tooling

This is the primary workspace root and the only canonical source of universal
skills, checkers and contract definitions. Architecture version: 4.0.1.
Read [Project Pulse](Project-pulse.md) for the latest verified state and next work;
update it after meaningful changes with what changed, checks, blockers and next actions.
Historical reports remain evidence of their own dates, not the live project state.
Additional workspace roots do not automatically supply instructions: explicitly
read their AGENTS.md, current status and `.tooling/profile.json` before editing.

Read the matching skill **before** work; combine only the relevant routes:

| Task | Canonical skill |
|---|---|
| Audit, task scope, project integration | [project-audit](skills/project-audit/SKILL.md) |
| Godot scenes, resources, import, engine integration | [godot-project](skills/godot-project/SKILL.md) |
| Blender character blockout, proportions, silhouette and geometry revision | [blender-character-modeling](skills/blender-character-modeling/SKILL.md) |
| Blender animals, creatures, quadrupeds and anthropomorphic animal modeling | [blender-animal-anthropomorphic-modeling](skills/blender-animal-anthropomorphic-modeling/SKILL.md) |
| Blender buildings, architectural shells, modular kits and large structures | [blender-architecture-environment](skills/blender-architecture-environment/SKILL.md) |
| Blender standalone environment fixtures, street/site assets and repeatable set-dressing objects | [blender-environment-assets](skills/blender-environment-assets/SKILL.md) |
| Blender roads, sidewalks, curbs, paths, crossings, junctions and connected linear ground infrastructure | [blender-roads-infrastructure](skills/blender-roads-infrastructure/SKILL.md) |
| Blender furniture, containers, tools, clutter, decor, hand-held and interior set-dressing props | [blender-props](skills/blender-props/SKILL.md) |
| Blender cars, trucks, buses, motorcycles, trailers and other wheeled vehicle modeling | [blender-vehicle-modeling](skills/blender-vehicle-modeling/SKILL.md) |
| Blender household appliances, consumer electronics, computers, displays and product-design devices | [blender-product-electronics-modeling](skills/blender-product-electronics-modeling/SKILL.md) |
| Blender trees, shrubs, grass, flowers, vines and vegetation systems | [blender-vegetation](skills/blender-vegetation/SKILL.md) |
| Blender organic/hard-surface sculpting, remesh/Dyntopo/Multires and bounded sculpt corrections | [blender-sculpting](skills/blender-sculpting/SKILL.md) |
| Blender multi-stage work, sculpt, UV/PBR, rig, animation, external asset repair | [blender-pipeline](skills/blender-pipeline/SKILL.md) |
| Blender late material/texture finishing, wear, surface damage, emission and posteffects | [Posteffects and polishing](skills/blender-posteffects-polishing/SKILL.md) |
| Blender bones, bindings and weights | [blender-rigging-skinning](skills/blender-rigging-skinning/SKILL.md) |
| Blender Actions and motion | [blender-animation](skills/blender-animation/SKILL.md) |
| Blender GLB export and round-trip validation | [blender-export-validation](skills/blender-export-validation/SKILL.md) |
| Godot asset delivery and target playback | [godot-asset-integration](skills/godot-asset-integration/SKILL.md) |
| Checks, evidence, runtime and anti-degradation | [verification](skills/verification/SKILL.md) |
| Contracts, checker, rule lifecycle, skill maintenance | [contracts-lint](skills/contracts-lint/SKILL.md) |
| Isolated playable mechanic tuning and playtest | [production-mechanic-gym](skills/production-mechanic-gym/SKILL.md) |
| Explicitly requested parallel agent work and merge review | [production-subagent-worktree](skills/production-subagent-worktree/SKILL.md) |
| Visual baseline before producing asset families | [production-lookdev-gate](skills/production-lookdev-gate/SKILL.md) |
| Decisions, milestones, regression gates and resumable project state | [production-project-state-gates](skills/production-project-state-gates/SKILL.md) |

Work cycle: read applicable instructions → inspect current implementation → check
Git status → smallest sufficient change → automatic checks → runtime/visual
verification where applicable → anti-degradation review → inspect diff → update
documentation only when needed → commit only explicitly listed own changes when
authorized. Preserve unrelated dirty/untracked files; no blanket staging.

Skills say **how**; project profiles describe replaceable project choices;
contracts define machine-checkable invariants; Pulse records observed project
state. Never infer a skeleton, clip list, genre or supplier from another project.
Paths and installation: [README](README.md). Contracts: [format](docs/contracts.md).
