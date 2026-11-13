# UV, material and texture recovery

Read existing [surface mechanics](../../blender-pipeline/references/surfaces.md)
for UV authoring, bake setup and PBR. Use [Reference Surface Transfer](../../blender-reference-surface-transfer/SKILL.md)
for original artwork/source-region projection; use [polishing](../../blender-posteffects-polishing/SKILL.md)
only when late artistic finishing is requested. These remain their method owners.

## Diagnose before repainting

Trace material slot → shader node → image → UV/coordinate source. Resolve missing
images from authorized source locations, then check packed data, channel mapping,
normal interpretation and color spaces. Color images and numeric data maps have
different roles; inspect actual encoding instead of changing every image to sRGB.
Treat normal/roughness/metallic data appropriately. Check alpha and target shader
support. A correct image with wrong UVs or shader wiring does not need ImageGen.

For blur inspect original pixels, effective texel density at viewing distance,
UV stretching, filtering/mipmaps and source resolution. Reconnecting a better
original is preferable to inventing its detail. Sharpening/upscaling may improve
perception but cannot recover information absent from the source. Label generated
or inferred detail as reconstruction; do not promise exact restoration.

## Preserve appearance through UV repair

Keep a usable source layout/image before rewrapping. Correct only affected seams,
islands, stretch, orientation or packing when possible. Preserve intentional
mirrors/stacking, tiling and UDIMs. Choose padding against final image resolution
and filtering; do not impose universal 0–1 layout or density.

Changing UV coordinates changes where existing paint lands. Plan mesh-to-mesh or
old-to-new-layout transfer/rebake before repacking established artwork. Match the
source and destination UV sets explicitly. Retain clean originals for projection;
avoid baking onto the same source image. Verify a checker and actual artwork,
especially faces, text/logos, asymmetric markings, seams and occluded regions.

## Select a recovery mode

1. Restore usable originals and material links/settings.
2. Repair a bounded image/paint region while protecting valid surrounding pixels.
3. Transfer existing appearance to repaired geometry or a new layout.
4. Reconstruct missing imagery from reliable references or controlled materials.
5. Regenerate a region or texture set when requested or when usable data is absent.

For AI-assisted image work use the available image-generation/editing capability
and its instructions. It is optional; never claim a missing tool ran. Supply the
actual reference and affected region, protected colors/markings, material role and
desired visual result. Treat generated pixels as candidates; they do not guarantee
UV alignment, exact symbols, consistent unseen views or physically correct PBR.
For base color request diffuse appearance without baked directional light, cast
shadows or highlights. Author/derive numeric channels independently from valid
maps, geometry baking or controlled material methods; color is not a normal map.

Project/paint a candidate onto the identified surface with masks and deliberate
view alignment. Resolve occlusions separately, blend boundaries, inspect multiple
views and bake to the final UV layout if needed. Do not stretch one flat generated
view around a complex model or claim inferred back-side details are source facts.
Use suitable cages/ray distances for mesh transfer and prevent neighboring parts
from contaminating the bake. Check island dilation, tangent orientation and seams.

## Acceptance

Review before/after mapped surfaces under comparable neutral lighting, with
closeups and alternate views. Reject an improvement that damages other views,
mirrors text, repeats facial features, shifts markings or changes protected colors.
Save generated/edited/baked images explicitly and verify reload; saving the blend
alone is not proof that external pixels were saved. Check requested exports in a
fresh import. When Blender node mixes or color multipliers do not survive the
chosen export format, bake the intended result into supported image/factor inputs;
open the exported PNGs and compare the fresh import with fixed source views.
Separate emissive material, actual lights and render-only glow in the handoff. Report source-derived versus reconstructed regions and limitations.
