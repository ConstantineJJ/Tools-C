---
name: godot-gameplay-implementation
description: Implement or change Godot gameplay - GDScript, scene wiring, input actions, physics layers, signals, autoloads and resources - for the project's declared engine version. Use for gameplay code and behavior edits; imports, scene-ownership review and runtime proof keep their owners.
---

# Godot gameplay implementation

Read the required [foundation contract](../../docs/foundation.md). Then read the project's AGENTS/profile,
`project.godot`, the scenes and scripts you will touch, and any existing tests.

Sibling owners: [godot-project](../godot-project/SKILL.md) for scene/resource ownership and instancing,
[godot-asset-integration](../godot-asset-integration/SKILL.md) for delivered 3D assets,
[production-mechanic-gym](../production-mechanic-gym/SKILL.md) for tuning one mechanic in isolation,
[godot-runtime-evidence](../godot-runtime-evidence/SKILL.md) for proof. A behavior is not done until the
evidence skill's check for that claim has run.

## Instruction priority

User request, project instructions and locked design decisions, existing code conventions, then this skill.
Match the project's naming, typing and folder layout; do not import another project's architecture, genre
assumptions, node names or controller design.

## Before editing

- Engine version: `config/features` in `project.godot` and the executable's reported version. Check a
  class, method or setting against that version's documentation before using it; APIs change between 4.x releases.
- Physics engine: read `physics/3d/physics_engine` and the 2D equivalent. New 3D projects default to
  Jolt since 4.6 (it was experimental from 4.4), but an existing project keeps what it declares.
  Do not change the engine as a side effect of a gameplay fix.
- Input: read the InputMap in `project.godot`. Gameplay reads actions (`Input.is_action_pressed`,
  `event.is_action_pressed`), never raw keycodes. A new action is added to the project InputMap, not
  invented in code, and is named in the report.
- Layers: read named layers (`layer_names/3d_physics/layer_N`). Set `collision_layer` and
  `collision_mask` from named intent. A mask is what a body detects; a layer is what it is.
- Ownership: decide whether a value lives in the script, the scene, a shared Resource or an imported
  asset (see [scene ownership](../godot-project/references/scene-ownership.md)). Edit the owner.

## Implementation rules

- Physics-driven motion and forces belong in `_physics_process` / `_integrate_forces`; per-frame visuals in
  `_process`. Scale motion by `delta`. Do not move a physics body by writing its position every frame.
- Prefer signals and exported references over hard-coded absolute node paths. A script that needs a child
  uses an `@export` node reference or a unique-name node, not `get_node("../../X")`.
- Type GDScript where the project does. Declare `@export` values with sensible ranges so tuning does not
  require code edits. Keep tunable numbers out of logic.
- One responsibility per script. Cross-scene communication goes through signals, groups or a named
  autoload that already exists; add an autoload only when state is genuinely global and the user agrees.
- Free what you create: remove spawned nodes, disconnect long-lived signals, stop timers on exit.
- Do not leave debug prints, test-only inputs or temporary nodes behind. Restore diagnostic edits.
- Do not add an addon or third-party dependency for a feature the engine already provides.

## Editing scenes and resources as text

Read [scene and script editing](references/editing.md) before hand-editing a `.tscn` or `.tres`. Short form:
make the smallest text change, keep existing `ext_resource` ids and UIDs, never regenerate a scene
wholesale, and treat a missing `.uid` or an unresolved reference as a defect. Use the editor or the project's
tooling when a change touches animation tracks, imported scene internals or many sub-resources.

## Verify and hand off

Run [godot-runtime-evidence](../godot-runtime-evidence/SKILL.md): import, `--parse-gate`, then a scenario
asserting the new behavior and one unchanged neighbor. Report PASS only for what ran. Feel, timing quality
and visuals stay with the user unless a reviewer has looked at captured frames. If the change needs a new
imported asset, route that to godot-asset-integration instead of faking it with placeholders in shipped scenes.

## Pitfalls / Lessons Learned

### GGI-001
- Symptom: a gameplay change works in the editor but breaks another instance or a fresh spawn.
- Cause: a shared Resource or scene-level override was edited as if it were local, or code assumed a node path.
- Rule: find the owner of the value, test a second instance and a freshly instantiated copy.
- Automated check: a `--scenario` that instantiates twice and asserts both; whole-project `--parse-gate`.
- Verification: change one instance, assert the other keeps its value.
- Added from / context: Godot skills pass 2026-11.
