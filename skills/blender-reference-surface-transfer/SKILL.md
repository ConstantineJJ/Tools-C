---
name: blender-reference-surface-transfer
description: Transfer distinctive graphics from source reference regions onto existing Blender surfaces, preserving faces/eyes, logos, markings, prints and patterns through crop, local repair, projection/decal/UV transfer and bake. Use for source image reuse, not new geometry or generic PBR authoring.
---

# Reference Surface Transfer

Read the [foundation contract](../../docs/foundation.md). Form is modeled;
material is reconstructed; unique artwork is transferred; a deficient region is
regenerated locally only when source information is insufficient.

## Ownership and priority

Own region selection, source provenance, image preparation, transfer decisions and
graphic identity review. Read [the transfer workflow](references/workflow.md)
before execution. Use [surfaces](../blender-pipeline/references/surfaces.md) for UV,
projection/bake mechanics and PBR bindings; this skill specifies what to preserve,
not a second UV/bake authority. Read-only review belongs to
[verification](../verification/SKILL.md).

Preserve the original image, locked design, geometry, silhouette, topology,
rig/weights/Actions, existing UVs outside the named region, shared resources and
unrelated scene data. Scope any new UV layer/material/image copy to named targets.
For complex reconstruction, consume the existing
[PASS 0 / Model Contract](../visual-reference-reconstruction/SKILL.md), its source
priority and permitted uses. A surface-only pass does not restart modeling.
An auxiliary generated view cannot replace usable original pixels or authorize a
new face, logo, lettering, ornament or pattern.

## Decision and execution

1. Inspect the actual source at native resolution and the target in Blender.
   Identify the region, visibility, lighting contamination, useful pixel density,
   graphic landmarks and required viewing distance. Record a source hash and crop.
2. Prefer a direct crop. Apply perspective correction, conservative cleanup and
   upscale only when justified; keep recoverable intermediates. Upscale cannot
   recover missing evidence. Inspect each result against the original.
3. If still deficient, document the missing information and use a bounded mask for
   targeted regeneration. Preserve valid pixels and identity anchors. Record the
   prompt, inputs, mask and output. Mark invented detail as inferred, never observed.
   If repair changes identity or needs unavailable source data, stop that region
   with a stated limitation; do not regenerate the whole design as a shortcut.
4. Choose projection, decal or UV transfer according to curvature, visibility,
   articulation and delivery. Transfer to the named faces/material, inspect an
   oblique view, then bake through surfaces and clean seams/padding locally.
   Record a justified bake SKIP only when the delivery profile accepts the retained
   editable mapping and its movement/portability limitations have been checked.
5. Reconstruct roughness, metallic, normal/height and other physical responses
   separately. RGB lighting is not material data. A graphic mask may locate an ink
   or coating region; it does not determine that region's PBR values.
6. Inspect source/crop/prepared/baked comparisons, identity closeups, seams and
   full-asset views under neutral and intended lighting. Save textures, reopen the
   candidate and recheck bindings. Use the [transfer record](references/record.md)
   for provenance and separate structural, visual and target acceptance.

## Identity and handoff

Faces and eyes require geometry supporting the face while the image preserves its
graphic identity. Preserve eye shape, iris/pupil placement, expression, asymmetry,
brow/mouth contours and facial markings. Return volume/eyelid/silhouette defects
to [character modeling](../blender-character-modeling/SKILL.md) or
[anime modeling](../blender-anime-character-modeling/SKILL.md); do not paint a frontal
illusion over broken form. Check oblique views and required expression/pose changes.

Use this route also for logos, markings, clothing prints, tattoos, mech panels,
instrument scales, graffiti, characteristic wear, ornaments and complex patterns
that do not need geometry. Preserve exact lettering, orientation and handedness;
unknown text remains unknown. Intentional wear patterns can transfer as artwork;
new procedural wear belongs to [polishing](../blender-posteffects-polishing/SKILL.md).

Handoff names source/region, processed and generated intermediates, target objects/
faces/UVs/materials, mapping settings, baked maps, channel spaces, preserved state,
observations and unresolved criteria. Stop at the authorized surface outcome.
Structural records cannot certify resemblance, mask containment or recovered PBR.

## Pitfalls / Lessons Learned

### RST-001
- Symptom: sharper texture loses the original face or exact lettering.
- Cause: whole-image generation/upscale treated as faithful data recovery.
- Rule: reuse source pixels first; repair only deficient masked regions and compare identity anchors.
- Automated check: transfer record requires repair reason, mask/prompt provenance and separate PBR basis.
- Verification: inspect original/prepared/baked regions and alternate views; record limits.
- Added from / context: requested Reference Surface Transfer workflow, not a claimed production incident.
- Version: 1.0.0, 2026-10-06.
