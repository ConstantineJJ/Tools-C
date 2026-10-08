# Source region to surface

## Acquire and prepare

Use the best authoritative source, not a screenshot of a generated contact sheet.
Keep the original bytes immutable. Record pixel dimensions, source role and
top-left crop rectangle `(x, y, width, height)` in source pixel coordinates. Include
enough border to align landmarks and blend edges; isolate occluders/background with
a mask. Inspect face/eye details independently from general material appearance.

Start with deterministic crop/resampling and reversible adjustments using the
available image tools. Record color encoding, orientation and any conversion.
Rectify approximately planar panels with corresponding corners/homography; record
the points and transform. A single homography cannot flatten a curved face or
garment: use small patches or camera-matched projection on supporting geometry.
Do not undo intentional perspective in painted artwork without evidence.

Distinguish painted highlights from illumination. Remove photographed shadows/
specular contamination only when separable without erasing art. Uncertain regions
retain a limitation; stylized shading may be part of the locked design. Keep an
unlit color comparison separate from the lit material review.

Use non-generative cleanup before generative repair. Interpolation/upscale improves
sampling but adds no observed information. A generative upscaler can invent pores,
iris structures, glyphs or seams; treat it as regeneration with a bounded mask and
provenance. Compare valid regions before/after at native and delivery resolution.

Before regeneration, record why a better source, alternate original view or simple
cleanup cannot supply the needed data. Mask only the damaged/missing region, use
the original crop as context, and constrain expression, glyph shapes, palette,
pattern layout and boundary landmarks. Save input/output/mask and exact prompt.
Composite only the approved repair region; inspect the boundary and valid pixels
outside it. Limit retries to two per defect by default, then defer/report the
region. Never guess unreadable required markings or redraw an entire face to fill
one eye highlight. Generated repairs remain inferred and independently reviewable.

## Face feature decision and integration

The source image controls **visible identity**; its covered portions remain
unknown. Inspect all authorized original views before inventing missing pixels.
Classify each facial region (left/right eye, brow, nose, mouth, jaw/hairline)
independently:

| Strategy | Use when | Required action / limitation |
|---|---|---|
| DIRECT FEATURE TRANSFER | Landmarks and usable original pixels are visible; pose/projection can be registered | Crop with context, mask out hair, solve landmark positions, transfer valid pixels without redrawing the expression |
| RECONSTRUCT-THEN-LAYER | Occlusion removes a critical contiguous face region and partial patches cannot align convincingly; reconstruction is authorized | Generate a **provisional clean face** constrained by surviving source landmarks/approved expression; all unseen detail stays INFERRED; layer intended hair/occluder in front of the reconstructed face |
| HYBRID PRESERVATION | Some original features are reliable, others are obscured or damaged | Preserve reliable source features unchanged in identity, reconstruct only missing regions, then color/geometry-register and blend the resulting local patches |

Selection procedure:

1. Make a **visibility and identity map**: eye corners and iris/eyelid shapes,
   eye line/interocular spacing, brow arches, nose axis/tip, lip corners and
   expression, jaw/chin and hairline. Distinguish reliably observed, partially
   visible and fully unknown features. Record occlusion masks separately from
   skin masks; never treat a fringe's pixels as face color.
2. Select the lowest-invention strategy sufficient for the approved target.
   Avoid whole-face redraw if an isolated source eye, lip or nose is usable.
   A clean-face reconstruction is allowed only after recording why a complete
   local patch is insufficient and which original views constrain it.
3. If reconstructing, use original crops and approved proportions as conditioning
   input, keep hairstyle **out of the underlying facial albedo**, and generate
   only within an explicitly bounded face region. Do not invent exact covered
   eyelashes, eye color, expression or asymmetry as observed truth. Compare
   more than one candidate if needed, but cap targeted retries as specified
   above and stop rather than accept changed identity.
4. Register approved feature locations to actual face geometry/UV, not just to
   a flat pasted image. Validate outer/inner eye corners, pupil centers, nose,
   mouth corners and chin against the reference using the matched camera.
   Preserve asymmetry and the approved eye-to-mouth relationship. Distinguish
   `skull size`, `hair-shell size` and `face artwork scale`: do not enlarge
   or shrink one to hide a mismatch in another.
5. Composite skin/features **behind** the intended 3D hair cards/clumps (or
   an explicitly managed alpha/occlusion layer with the same depth semantics).
   Reintroduce hair cast shadows through lighting, not by copying dark hair
   pixels into skin color. Test visibility at front, three-quarter, side and
   the intended movement where applicable.
6. Separate the result into named approved-source features, inferred patches,
   occlusion layer and supporting geometry. An approved feature is a
   **protected zone** in later passes: change it only on explicit authorization
   or when a stated dependent geometry transform requires registration.

A reconstructed clean face must not be called an exact extraction. Missing source
or insufficient identity anchors can leave the face region BLOCKED rather than
forcing a visually plausible but unrelated person.

## Seam Integration / Patch Disguise

Patch integration is an explicit operation before texture acceptance, not an
optional finishing flourish. It applies to DIRECT, HYBRID and generated skin:

1. Establish **registration first**: source/target landmark correspondence,
   perspective/UV distortion and skin/geometry fit. Misplaced eyes cannot be
   fixed by blurring the patch boundary.
2. Prepare separate feather/alpha masks with a sufficiently broad **skin-only**
   transition band. Exclude hair, lashes, eye whites, pupil, brows, lips and
   intentional makeup edges from skin diffusion. Never soften expression-defining
   strokes to disguise an incorrect cut.
3. Match low-frequency color, exposure, saturation, local gradients and apparent
   skin texture at the receiving boundary using unaffected **adjacent valid skin**.
   Remove inherited photo lighting only where justified. Work in the appropriate
   color space for blending; avoid performing naive arithmetic on gamma-encoded
   sRGB when precision matters. Preserve deliberate blush/shadow/graphic styles.
4. Use controlled alpha, multiband or gradient-domain blending where suitable,
   with local clone/paint corrections as needed. Do not leave a uniform flat oval
   over a curved cheek/forehead. Repeat inspection after UV bake and mip/filter
   behavior, not only in the editable projection view.
5. Inspect the unlit base-color image, neutral lit frontal/three-quarter
   closeups, side view and requested target renderer; compare with original
   identity anchors at both native texel zoom and intended on-screen size.
   Note intended hair occlusion separately from texture artifacts.
6. **FAIL** the named face/skin region if a rectangular/oval insert perimeter,
   brightness/saturation ring, double facial feature, abrupt normal/shading
   mismatch or obviously floating pasted artwork remains visible on neutral
   review. A flattering beauty shot does not close this gate. Correct and
   recapture, or report the limitation explicitly (not a visual PASS).

For each relevant region, retain source, raw crop, mask, provisional
reconstruction (if any), prepared/baked textures, target-UV identification and
comparative closeups. Preserve user-approved eye/mouth geometry and material
features across later skull/hair proportion edits.

## Map, bake and clean

| Method | Appropriate use | Main failure to inspect |
|---|---|---|
| Camera/projective mapping | Photo-to-form registration, facial patches, curved panels with known view | Back projection, occlusion, foreshortening, swimming outside the matched view |
| Decal with local coordinates | Isolated insignia, tattoo, scale or panel graphic | Alpha fringe, z-fighting, curvature clipping, attachment to the wrong moving part |
| UV transfer | Stable production map, clothing print, repeated viewing or deformation | Stretching, mirrored lettering, accidental stacking, seams crossing identity anchors |

Follow [surfaces](../../blender-pipeline/references/surfaces.md) for mechanics.
Match source/target landmarks; restrict receiving faces and front visibility.
Do not project through the model onto its rear. Keep asymmetric eyes, text and
unique wear off mirrored/shared UV islands unless repetition is intentional.
Bind each decal/projection to its owning rigid part or deformation surface; check
movement and expression if required. Keep source mapping editable for corrections.

Make a small test bake to a new destination image and explicit UV map/material
slot. For artwork/base color use a color-only transfer, e.g. diffuse Color with
Direct/Indirect disabled, or a verified unlit emission transfer. Do not use Combined
as an accidental albedo bake. Never bake onto the only source image. Preserve
alpha/masks separately when needed; confirm active image nodes for all target slots.
Record engine/version, pass, light exclusions, dimensions, UV, margin and outputs.

Clean border colors, seams and island padding with local clone/paint using valid
neighbor pixels; do not blur across eyes, letters, scales or pattern boundaries.
Inspect edge dilation, alpha convention, texture filtering and mip-distance bleed.
If delivery needs a baked map, retaining a camera projection is an open gate.
Save/pack the resulting images explicitly, save a candidate and reopen it; a saved
.blend alone does not establish that external images are available.

## Material and QA

Treat color artwork and physical response as separate layers. Infer material class
and roughness/metalness from construction, coating and independent references;
record uncertainty. Dark RGB is not roughness and a white highlight is not metal.
A face photograph is not a normal/displacement map. Use color encoding for color
textures and the intended data space for numeric maps, following the target profile.

Compare original crop, prepared patch and baked result without lighting, then
inspect lit closeups plus full-asset front/oblique views at production distance.
Review identity/lettering, placement/scale, mirrored regions, seams/alpha,
photographed lighting, physical response, movement and reopened dependencies.
For faces inspect volume separately in clay and artwork in color; a successful
front view does not certify profile or expression. Exact text requires visual
comparison; OCR can assist but cannot approve invented glyphs.

Use [evidence capture](../../../docs/blender-evidence.md) and record observations
with artifacts and hashes. PASS applies to inspected named criteria only. SKIP
names the missing source/runtime and next owner; captured images awaiting review
are REVIEW_REQUIRED. Target-engine portability belongs to delivery/integration.

## Technical sources

Checked 2026-10-06 against official Blender documentation; verify sockets/options
in the actual installed version before execution. These sources support mechanics,
not automatic recovery of identity or PBR from a single image:

- [Texture Paint](https://docs.blender.org/manual/en/latest/sculpt_paint/texture_paint/introduction.html): UV images can be edited in Blender or external image tools.
- [Cycles baking](https://docs.blender.org/manual/en/5.1/render/cycles/baking.html): UV/image destination, color-only bake passes and island margins.
- [Principled BSDF](https://docs.blender.org/manual/en/5.1/render/shader_nodes/shader/principled.html): independent color, metallic and roughness material inputs.
