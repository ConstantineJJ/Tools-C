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

## Visual feedback loop and capture fallbacks

For geometry creation or a visible revision, the agent must capture and **open the
actual PNGs**, review silhouette/proportions/intersections/shading against the scoped
criteria, list visible defects, correct them through the appropriate owner, and
recapture/review affected views. Keep another relevant view as a regression check.
Use the BEFORE objects, frame (including subframe), framing, resolution, mode and
lighting for AFTER. For a captured fractional frame, leave `frame=None` and restore
that source frame/subframe explicitly before recapturing; the capture frame argument
accepts integers. Record reviewer, image paths/hashes, observation and KEEP/CORRECT/
REVERT. Read-only review identifies defects without authorizing geometry edits.
Stop at scoped acceptance or an explained blocker; no blind/unbounded polishing.

Use these routes in order; tool discovery failure is a reason to try the next route:

1. `capture_viewport` MCP returns image content plus metadata. Open/inspect the image.
2. If that named tool is absent, but `execute_blender_python` works, invoke the same
   canonical helper below. It uses Blender's render operation/Render Result and
   saves a PNG without needing a live VIEW_3D or an OS screenshot tool. Run
   `tools/python_preflight.py` on the payload first; the existing safety gate applies.
   Resolve the canonical root from the active project configuration or TOOLS_C_ROOT;
   replace the example root, output path and object names with verified project values.

```python
import runpy, uuid
from pathlib import Path
tools_c = Path("E:/MyCreations/Tools_C")
capture = runpy.run_path(str(tools_c / "tools/blender_capture.py"))["capture_viewport"]
output = tools_c / ".local/captures" / uuid.uuid4().hex
_result = capture(output=str(output),
                  view="front", target="character", object_names=["Body", "Head"],
                  mode="solid", frame=1, resolution=512)
print(_result)
```

The updated Tools_C integration adapter recognizes this managed capture and
returns a verified MCP image alongside the unchanged structured Python result.
Its loaded server must include that adapter update; discovery of a new tool is
not required. It accepts only matching capture manifests and PNG hashes beneath
Tools_C `.local/captures`; arbitrary Python-returned file paths are not attached.
With an older adapter, the response is metadata only: open `_result['path']` with
the client's local image-view capability (for example `view_image`) or an authorized
image attachment/download mechanism. Verify the PNG against `_result['sha256']`.
A JSON path alone is not visual review. If a remote client cannot retrieve image
bytes, report that image-access blocker instead of claiming that Python solved it.
Do not overwrite the evidence folder; use a new directory for each capture.

3. If the Blender bridge/session is down, a local agent can render an explicitly
   saved current candidate in an isolated Blender process without MCP:

```text
python tools/blender_capture_file.py --blender "C:/path/to/blender.exe" --source "C:/project/candidate.blend" --output "C:/project/evidence/NEW_before_front" --objects Body Head --view front --frame 1 --resolution 512
```

For AFTER or another comparable fixed view, use a new output directory and pass
`--framing "C:/project/evidence/NEW_before_front/image/capture.json"`. Supports
front/side/back/top/bottom/three_quarter and solid/material_preview/rendered.
The tool opens the source with autoexec disabled, uses the same capture helper,
verifies the PNG/hash/completion marker and source-file hash, and writes `result.json`
and `blender.log`. Open `result.capture.path` and inspect it. It never saves the
source .blend or changes an open editor. Unsaved edits are absent: use a separately
saved current candidate within authorized scope, or report stale/missing source.
Script/driver-dependent appearance may require interactive validation; disabling
autoexec is not proof of its equivalence. An offline render does not repair MCP.

If all applicable routes fail or images cannot be inspected, record attempts,
diagnostics and remaining owner as VISUAL SKIP. Keep required visual acceptance
open; do not report the modeling task as fully accepted. A blank/clipped/wrong-target
image is failed evidence setup to fix before judging the model. Capture output
always remains VISUAL REVIEW REQUIRED until the agent records actual observations.


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
