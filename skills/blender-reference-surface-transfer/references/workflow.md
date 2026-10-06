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
