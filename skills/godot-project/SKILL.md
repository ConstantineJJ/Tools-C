---
name: godot-project
description: Own Godot project orientation and scene/resource ownership - engine version, project settings, instancing, shared resources and reimport-safe edits - and route to the gameplay, asset or evidence owner. Use to read or restructure a Godot project; not Blender authoring alone.
---

# Godot projects

Read the required [foundation contract](../../docs/foundation.md).

## Instruction Priority

Follow the user's requested behavior, active project instructions/profile and current scene/resource ownership, then this skill. Historical node names and another project's rig or import policy are not current evidence.

## Domain constraints

- Protected: authored overrides, shared-resource intent, scene instancing, unrelated gameplay behavior and protected project assets.
- Owned edits: named scenes, resources, project settings and necessary dependencies within scope.
- Acceptance: the requested structure loads in the actual target project, affected instances retain their expected values, and the evidence level reached is stated.

## Who owns what

| Task | Owner |
| --- | --- |
| Gameplay scripts, input actions, physics layers, signals, scene wiring for behavior | [godot-gameplay-implementation](../godot-gameplay-implementation/SKILL.md) |
| Delivered GLB/glTF import, skeleton, materials, animation playback | [godot-asset-integration](../godot-asset-integration/SKILL.md) |
| Import / parse gate / scenario / capture / export / Godot MCP evidence | [godot-runtime-evidence](../godot-runtime-evidence/SKILL.md) |
| Tuning one mechanic in isolation | [production-mechanic-gym](../production-mechanic-gym/SKILL.md) |
| Scene ownership, instancing, shared Resources, project settings, orientation | this skill |

## Workflow

1. Orient: read the local profile, `project.godot` (`config/features` is the declared engine version; also the
   main scene, InputMap, named physics layers, physics engine, autoloads, enabled plugins), the relevant scenes
   and scripts, and the current import hierarchy. Record the version the executable reports; they can differ.
2. Identify the owner of each value to be edited (imported asset, authored wrapper, per-instance override,
   shared Resource, runtime-spawned node). Keep authored state outside content that reimport replaces. Read
   [scene ownership and instancing](references/scene-ownership.md) for imported scenes, shared resources or repeated objects.
3. Take skeleton roles, axes, root motion, collision ownership and export format from the target profile, not
   from Blender or another engine's display settings.
4. Edit only the named owner. For text-format scene edits follow
   [scene and script editing](../godot-gameplay-implementation/references/editing.md).
5. Prove it with [godot-runtime-evidence](../godot-runtime-evidence/SKILL.md). Import alone and a scene-load smoke
   do not cover scripts nothing references; use the whole-project parse gate for "the project is clean".
   Read-only QA must not save editor or gameplay state.

## Anti-degradation and stop

Compare the requested structure with previous scene overrides, another instance and runtime stability.
Restore temporary diagnostic state. Stop when scoped checks pass at the required level; report an unavailable
engine, input or visual check as SKIP with reason rather than a pass.

## Pitfalls / Lessons Learned

### GOD-001
- Symptom: a reimport or runtime spawn loses editor-authored offsets or gameplay nodes.
- Cause: imported content and scene ownership were conflated.
- Rule: inspect wrapper/instance ownership and preserve authored overrides.
- Automated check: resource existence only in V1; engine/instance assertions required for behavior.
- Verification: fresh import, two instances, reset and changed property retention.
- Added from / context: local scene-first pipeline audit; ArcEngine instancing review informed stable identity checks.
- Version: 0.1.0, 2026-09-21.
