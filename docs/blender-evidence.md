# Blender evidence tools

All tools keep source acceptance separate from schema validation. Python helpers
are canonical in Tools_C; the integration server calls them without copying bodies.

## Stage snapshot

In Blender, load `tools/blender_snapshot.py` with runpy and call
`snapshot(stage, object_names, protected=(), action_names=(), blockers=())`.
Supply explicit object/Action lists, not a project-name heuristic. Validate with
`tools/handoff_snapshot.py SNAPSHOT.json`; compare unchanged source scope with
`--compare AFTER.json`. Serialization is stable, sorted and finite; schema is 1.
It includes per-object counts/local mesh hash, finite world matrices, bone names and
parents, materials, Action ranges, time base, protected objects and blockers.

The hash includes base mesh coordinates/connectivity/material indices. It excludes
evaluated modifiers, weights, UVs, shape keys, bone rest matrices and Action curve
values. Use targeted baseline checks for those when protected; no whole-scene
equivalence claim follows from a snapshot. Counts are summaries, not acceptance.

## Universal MCP capture

`capture_viewport(view, target, mode, frame, resolution, object_names, framing)`
supports front/side/back/top/bottom/three_quarter/current, active/selected/character/scene,
solid/material_preview/rendered. Character scope requires explicit object_names.
Resolution is one integer 64–2048 for a square image. Frame may be omitted for an
initial capture; every response records the resolved frame. Repeat that frame in
AFTER captures. Pass the BEFORE `framing` (center and span) to all AFTER views;
automatic reframing after an edit would conceal bounds regressions.

Fixed views are orthographic: front looks from -Y, side from +X, back from +Y,
top/bottom from +/-Z; three_quarter is a fixed (1,-1,.6) direction. The same sphere
fit is used for each view. `current` derives orientation/projection from a live
VIEW_3D; no area means SKIP. This is a viewport-oriented evidence render in a
temporary scene, not an exact screenshot of the UI. Current uses square framing.

Solid uses fixed Workbench studio lighting/material colors. Material preview uses
actual materials with three fixed area lights and Cycles CPU, Standard color
transform, fixed seed and bounded samples. Rendered uses source lights/world with
bounded Cycles CPU and no compositor; it is not a final production-render promise.
Source geometry/materials/selection/camera/render settings are preserved; frame is
restored even on failure. A new output directory contains PNG and capture.json;
MCP returns the image plus metadata. Captures never save the production .blend.

BEFORE snapshot + capture → scoped edit → AFTER snapshot + same target/frame/
framing/resolution/mode → inspect images and compare invariants. Repeated calls at
named frames support pose review; stills do not replace playback. Record image
hashes and reviewer observations before marking VISUAL PASS. Capture itself returns
VISUAL REVIEW REQUIRED. Material differences still require target-engine review.

For offline/factory probes, run the helper in Blender Python using
`capture_viewport(NEW_OUTPUT_DIRECTORY, ...)`. The same API underlies the MCP tool.

## Export and round trip

`tools/blender_export_probe.py` runs in a disposable background Blender process:

```text
blender --background --factory-startup --python-exit-code 1 --python tools/blender_export_probe.py -- JOB.json
```

Jobs choose export (open an explicit .blend read-only, explicit objects/Actions,
new GLB path) or import (factory scene, existing GLB, new evidence directory).
Invoke each mode in a separate process. The probe writes snapshot/bounds and a
completion marker. Read `tools/glb_inspect.py OUTPUT.glb` separately. A test fixture
demonstrates the flow; arbitrary asset equivalence requires its own contract and
poses. Source JSON counts must not be blindly equated to triangulated glTF counts.

For the complete bounded run use `python tools/export_validate.py JOB.json
--blender EXE --output NEW_DIRECTORY` (one command). It exports and imports in
separate factory processes, inspects GLB and compares names, skeleton hierarchy,
material/clip inclusion, clip durations and bounds. It does not auto-accept source
versus imported raw geometry hashes or arbitrary deformation. Blender 5.2 importer
creates an Icosphere for bone display; the probe uses the available
`disable_bone_shape` option so that importer-only helper is not counted as geometry.
