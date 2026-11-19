# Scenario format

Read when writing or reviewing a `--scenario` file. Implementation: `tools/probes/godot_scenario.gd`;
static validation: `tools/godot_runtime.py`.

```json
{
  "scene": "res://main.tscn",
  "frames": 60,
  "steps": [
    {"frame": 5, "action": "press", "name": "move_right"},
    {"frame": 35, "action": "release", "name": "move_right"},
    {"frame": 40, "action": "call", "node": "Player", "method": "reset", "args": []}
  ],
  "assertions": [
    {"at_frame": 2, "node": "Box", "property": "position:x", "op": "approx", "value": 0.0, "tolerance": 0.001},
    {"at_frame": 59, "node": "Box", "property": "position:x", "op": ">", "value": 0.5},
    {"at_frame": 59, "node": "Camera3D", "exists": true}
  ]
}
```

- `frames` counts physics frames; steps and assertions fire after that frame's physics tick.
- `action`: `press`, `release`, `tap` (press then release in one frame) send an InputEventAction for an
  existing InputMap action. An unknown action is logged as an error and the run fails.
- `node` is relative to the scene root; `.` is the root. `property` accepts sub-paths such as `position:y`.
- Arrays of 2 or 3 numbers compare against Vector2 / Vector3.
- `{"at_frame": 1, "input_action": "jump"}` passes only when the InputMap has that action with at least one
  event. It proves the binding exists in the project, not that a physical key reaches the engine.
- Assertions at a frame the run never reaches fail the run; a scenario with no assertions is rejected.
- Assert a changed value and an unchanged neighbor: after pressing right, the box moved and the camera did not.
- Number of physics frames is not time: with the default 60 ticks per second, 60 frames is one second
  of game time only if the project keeps that setting. Read `physics/common/physics_ticks_per_second`.

Result marker: `TOOLS_C_GODOT_SCENARIO {json}` with every assertion's expected and actual value,
`steps_applied` versus `steps_declared`, and `passed`. Exit code 1 when anything failed.

A scenario drives actions through the InputMap. It does not click UI controls and does not
exercise raw key handling that bypasses InputMap; say so when the claim covers them.
