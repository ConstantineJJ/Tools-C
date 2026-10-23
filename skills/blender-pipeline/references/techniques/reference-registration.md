# Reference registration and measurement

Read for multi-view sheets, perspective concept art or a reference mismatch that cannot be solved by simple visual comparison.

Record the source images, designated primary projection, known scale, structural/decorative parts, symmetry, major landmarks and uncertain regions. Useful humanoid landmarks include head top/chin, shoulders, elbows, wrists, pelvis/hips, knees, ankles and foot extremes. Measure relationships from the supplied image; no generic proportions are defaults.

For orthographic views, share landmark heights. Front constrains width and height; side constrains depth and height; back constrains rear structure; top constrains cross-sections. Correct registration errors before modeling volume. Lock registered reference objects and exclude them from rendering/export.

For perspective art, estimate camera direction and treat occluded dimensions as uncertain. Use multiple landmarks so one foreshortened limb does not set the whole scale. Where sheets conflict, record which projection controls recognizability and the resulting compromise. Do not average incompatible measurements.

When useful, compare masks, bounding boxes, centers, silhouette overlap and landmark offsets. These measurements are diagnostics; inspect the visible result as well. At blockout, check total envelope, head/body ratio, shoulder/hip relationship, limb lengths, hands/feet, part count and primary-view silhouettes before adding detail.

## Put the references in the actual scene

For reference-led shape work, import the useful source views into a task-owned
`REFERENCE` collection (or an explicit revision name), rather than relying only
on external images. This also applies to a requested late geometry correction.
Use front/back, left/right and top roles; a cropped head/paw may have its own
regional registration. User-supplied sources remain read-only. Pack a scene copy
of each image so the saved file retains it, lock selection/transforms after
registration, and exclude the reference collection explicitly from asset export.
Collection/object hide-render flags alone are not a universal exporter filter.

When a required side is missing, Imagegen may create an auxiliary side/back/top
view using the authoritative image and locked proportions. Use the available
imagegen workflow, inspect its output and save the actual image before import.
Record `generated` authority, source relationship, uncertain regions and intended
scope; generated views may suggest hidden volume but never overrule the original
or a user-corrected profile. Do not generate every side when existing views suffice.
Use silhouette/landmark reasoning to resolve conflicts, not averaging.

## Ready operation through the existing Blender Python route

`tools/blender_reference.py` supplies `fit_landmarks` and `create_reference_set`.
No new server or public MCP input is required. Run Python preflight, then use a
task script through the existing `execute_blender_python` route, for example:

```python
import runpy
refs = runpy.run_path('E:/MyCreations/Tools_C/tools/blender_reference.py')
_result = refs['create_reference_set']([{
    'projection': 'orthographic', 'view': 'right',
    'image': 'E:/MyCreations/Work_Utility/task/reference-profile.png',
    'pixels': [[40, 440], [280, 440], [150, 120]],
    'plane_points': [[0, 0], [.24, 0], [.11, .32]],
    'landmark_types': ['visible_surface', 'visible_surface', 'coat_tip'],
    'authority': 'user-corrected profile', 'scope': 'head and forequarters',
    'confidence': 'observed silhouette; hidden width unknown'
}], collection_name='REFERENCE')
```

Replace paths/landmarks with actual task data; these numbers are explanatory,
not animal proportions. Pixels use top-left origin, x-right/y-down. Plane points
use scene units, screen-right/up in the declared view. Front looks from -Y,
right from +X, left from -X, back from +Y, top from +Z; see the helper's `VIEWS`.
Use a common ground/landmark height across compatible views. Distinguish visible
landmarks from inferred construction centers. A reference does not establish a
hidden eye center by displaying an iris.

The fit uses uniform scale, in-plane rotation and translation and returns per-point
and RMS residuals. It never changes geometry or anisotropically warps an image to
hide a mismatch. Initial uniform resizing/placement of a cropped body part is
permitted; intentional aspect correction requires source evidence and separate
registration, not an unexplained automatic fit. The cameras use fixed square
framing enclosing the rotated image; use square render resolution and square pixels
for these cameras (the helper preserves scene render settings). Do not reframe to model bounds between passes.
Residuals have no automatic likeness threshold or artistic PASS.

`landmark_types` is optional for compatibility. When supplied, it has one entry
per point: `visible_surface`, `hidden_construction` or `coat_tip`. Use scope and
confidence to name the actual features and skin/coat envelope; visible iris and
hidden eyeball center are different landmarks. Legacy untyped records are not
silently assigned types. Use a separate named collection for a head/paw crop;
retain common world landmark heights with the body registration where justified.

Call `diagnose_reference_set('REFERENCE')` after setup, parent/root changes or
reopening. It reports original fit residuals, actual world per-point residuals,
drift from the registered fit, nonuniform/sheared/reflected image transforms,
camera orientation/framing, image-size changes and incompatible render aspect.
It changes no registration or model data. Compare errors in scene units at the
feature's scale; no universal error threshold certifies a likeness. Check the
model's own local-to-world transform separately. Orientation warnings compare
the camera to the declared view; source-image handedness/pose still needs visual
inspection and cannot be inferred from the view name. An unchanged aspect-warped
source can produce fit residuals but is not automatically repaired.

Perspective sources can be imported with `projection: 'perspective'` as visual
guides, but the helper creates **no measurement camera** for them. Plane placement
is not source-camera calibration. Estimate/calibrate the actual camera separately
before using perspective contours as quantitative shape constraints.

The helper packs independent image datablocks, creates image empties and (for
orthographic views) locked cameras, and stores source/scope/confidence/fit metadata.
It refuses an existing collection name and rolls back only its own created data
on failure. It does not select objects, change the active camera, edit the model,
render evidence, generate missing views or automatically filter an export.

For a comparison, use the named camera and unchanged pose/projection/framing;
inspect reference-only, clay model and an overlay/side-by-side comparison as useful.
Image empties are viewport guides and do not render into the beauty image. Use
the existing capture/evidence workflow for real outputs, preserving its hashes
and review boundaries. Inspect a second projection and three-quarter view after
a single-view correction. Full automatic masks/multi-view optimization are not
implemented by this setup operation.
