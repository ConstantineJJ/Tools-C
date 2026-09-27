---
name: godot-project
description: Edit or validate Godot scenes, resources and imported assets using the project's actual engine version, ownership rules and runtime evidence. Use for Godot project work, not Blender authoring alone.
---

# Godot projects

Read the required [foundation contract](../../docs/foundation.md).

## Instruction Priority

Follow the user's requested behavior, active project instructions/profile and current scene/resource ownership, then this skill. Historical node names and another project's rig or import policy are not current evidence.

## Domain constraints

- Protected: authored overrides, shared-resource intent, scene instancing, unrelated gameplay behavior and protected project assets.
- Owned edits: named scenes, scripts, resources, import settings and necessary dependencies within scope.
- Acceptance: the requested behavior loads and runs in the actual target project; affected instances and relevant views retain their expected behavior.

For delivered 3D asset import/playback, use [godot-asset-integration](../godot-asset-integration/SKILL.md)
as the stage owner; this skill owns general scenes, resources and gameplay integration.

## Workflow

Read the local profile, project.godot, relevant scenes, scripts and current import hierarchy. Identify Godot version and the owner of each edited value. Keep authored gameplay state outside reimported content when reimport would replace it. Inspect shared Resource and instance behavior before changing a property. Read [scene ownership and instancing](references/scene-ownership.md) when imported scenes, shared resources or repeated objects are involved.

Take skeleton roles, axes, root motion, collision ownership and export format from the target profile. For imported 3D assets, compare scale, normals/tangents and material response with a known-good asset in the same scene. Do not treat Blender or another engine's display settings as Godot defaults.

Run L1 and, when applicable, bounded [engine/import probes](../../docs/engines.md). Read-only QA must not save editor or gameplay state. Use an explicit runtime assertion for changed behavior and another affected instance or view. A clean parse/import does not establish gameplay or visual acceptance.

## Anti-degradation and stop

Compare the requested behavior with previous scene overrides, another instance, asset appearance and runtime stability. Restore temporary diagnostic state. Stop when scoped checks pass at the required level; report an unavailable engine, input or visual check as SKIP with reason rather than a pass.

## Pitfalls / Lessons Learned

### GOD-001
- Symptom: a reimport or runtime spawn loses editor-authored offsets or gameplay nodes.
- Cause: imported content and scene ownership were conflated.
- Rule: inspect wrapper/instance ownership and preserve authored overrides.
- Automated check: resource existence only in V1; engine/instance assertions required for behavior.
- Verification: fresh import, two instances, reset and changed property retention.
- Added from / context: local scene-first pipeline audit; ArcEngine instancing review informed stable identity checks.
- Version: 0.1.0, 2026-09-21.
