# Tools_C Agent Vision

An observation capability of the existing Verification owner, not another skill,
server, design authority or QA store. Existing PASS 0, reference registration,
ImageGen lineage, snapshots and artistic review keep their ownership.

## Acquisition and measurements

`tools/blender_capture.py:capture_viewport` retains its previous defaults.
Optional `channel='silhouette'` returns neutral opaque geometry coverage in PNG
alpha. It is independent of beauty lighting and does not simulate transparent
materials, volumetrics or final engine appearance. `view='camera'` requires an
explicit scene `camera_name`; its projection, lens, sensor fit, shift and clipping
are copied into the temporary evidence camera. Source objects/settings are retained.
The Python helper also accepts `[width,height]` resolution, each 64..2048;
the native MCP input remains a square integer for compatibility.

Fixed views use the existing asset-axis convention. Record a different asset
frame explicitly rather than inferring forward from a project or object name.
For BEFORE/AFTER fixed views reuse framing, frame, target, mode and resolution.
Reference comparison instead needs the registered reference camera and pose.

`tools/blender_snapshot.py:measure_objects(names,max_vertices=1000000)` returns
evaluated world bounds/dimensions, world pivot, local axes and determinant.
Scope is 1..256 explicit objects, with a total evaluated vertex budget.
Coordinates are floating-point scene units. Physical units need an actual scale
contract. Evaluation may itself be costly; scope modifiers/objects proportionally.
Use existing `blender_contacts.py` for selected-pair contacts; its sampled
proximity is not a certified global minimum clearance or a motion sweep.

## Comparison

Run `python tools/vision_compare.py TASK/job.json --output TASK/NEW_COMPARISON`.
The output must be a new directory below the job directory. Inputs are contained
relative paths with SHA-256 hashes. PNG masks are 8-bit, noninterlaced gray/RGB/RGBA,
up to 1024 pixels per side. Alpha masks use alpha >=128; luminance masks require
explicit monochrome data and use value >=128. Never silently segment a photograph,
stretch a mask, auto-fit model bounds, or move landmarks to hide a mismatch.
Prepare/review a reference mask explicitly and retain its original source hash.

```json
{
  "schema_version": 1,
  "reference": {
    "mask": {"path": "reference-mask.png", "sha256": "ACTUAL_HASH"},
    "mode": "alpha",
    "source": {"path": "original.png", "sha256": "ACTUAL_HASH"},
    "authority": "ORIGINAL"
  },
  "candidate": {
    "mask": {"path": "candidate/front.png", "sha256": "ACTUAL_HASH"},
    "capture": {"path": "candidate/capture.json", "sha256": "ACTUAL_HASH"}
  },
  "alignment": {"mode": "APPROXIMATE", "reviewed": false, "pose_confirmed": false},
  "thresholds": {},
  "landmarks": []
}
```

For CALIBRATED mode, attach `alignment.reference_setup` with the exact fields
returned by `vision_compare.camera_setup(reference_capture_metadata)`, from the
reviewed reference registration. Candidate setup is read from actual capture
metadata. Matching metadata is a reviewer declaration, not independent proof of
calibration. A camera/pose mismatch returns NOT_COMPARABLE. Approximate evidence,
unreviewed calibration and GENERATED_AUXILIARY never acquire metric acceptance.
ORIGINAL and user-adopted LOCKED_HERO can use explicitly chosen task thresholds
`iou_min` and `contour_p95_max_px`; there are no universal likeness thresholds.

Outputs: IoU, symmetric Euclidean contour distances (mean/median/p95/max), normalized
p95, differing pixel count/bounds, `difference.png`, `contours.png`, and a hashed
`comparison.json`. Green is reference-only, magenta candidate-only, gray overlap.
Optional named landmarks have id/reference/candidate/visibility; positions use
top-left-origin pixels. VISIBLE landmarks return offset/distance; PARTIAL/OCCLUDED
remain UNKNOWN. Findings identify object scope, view and affected pixel rectangle.
Inspect originals, masks and overlays before interpreting a form defect.

## Images in ordinary ChatGPT

The existing `execute_blender_python` image response also accepts a verified
`silhouette comparison diagnostic`; no additional MCP operation is needed.
Use `vision_compare.capture_comparison(job_path,new_output,channel='contours')`
or `channel='difference'`. It runs the same comparison and writes a delivery
manifest. Return that result as `_result` through the existing Python tool.

For managed delivery, the job and its relative input artifacts must stay below
the existing Work_Utility root; output is a new UUID directory directly below
its `captures` directory. The output must also be below the job directory, so
place the job at the Work_Utility root when its inputs span several captures.
Obtain this root from `mcp_capture_response.capture_directory(tools_c).parent`;
use the deployment's actual canonical root, not a hard-coded project path.
Load helpers with runpy and add `tools_c/'tools'` to sys.path when necessary.

The adapter verifies the delivery manifest, contained PNG/hash/dimensions, report
hash and recomputed job inputs before attaching the image. The wrapper remains
VISUAL REVIEW REQUIRED and reports the separate metric status. Open the attached
image in chat; a returned pathname or a metric PASS is not inspected evidence.
The source silhouette capture remains the QA check's evidence; an overlay must
not be disguised as an original scene render.

## Existing QA handoff

A named check in the existing QA receipt can add optional
`comparison: {path,sha256}` referring to comparison.json. The task root must also
contain its job JSON. With `--verify-files`, qa_gate recomputes the report from
current hashed inputs and binds its candidate image to that check's capture IDs.
Failed, approximate or mismatched comparison cannot become a PASS check.
Existing receipts without this field retain their format and behavior.

Keep TECHNICAL_QA, ARTISTIC_REVIEW, export and runtime results separate. A matching
front silhouette cannot prove depth, hidden structure, topology or other views.
Use the existing dual-review findings for semantic remarks and corrective owners.
Generated additional views/textures retain the existing PASS 0/surface procedures;
no extra ImageGen service is introduced. Depth/Normal/ID channels remain optional
future work, not implemented or implied by the silhouette capability.
