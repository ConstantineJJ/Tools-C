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

## Face transfer strategy (choose before editing)

For an occluded or stylized face, select **one strategy per affected region**;
mixed regions may use a composite strategy. Details and identity constraints live
in [face transfer / seam integration](references/workflow.md#face-feature-decision-and-integration):

- **DIRECT FEATURE TRANSFER**: usable eyes/brows/nose/mouth pixels and compatible
  projection; transfer original source features with local registration.
- **RECONSTRUCT-THEN-LAYER**: a critical feature is hidden or incomplete; after
  checking original alternate views, explicitly authorize a bounded clean-face
  reconstruction from the authoritative source. Preserve observed facial anchors,
  mark occluded content INFERRED, and place intended hair/occluders back **in front
  of** the face in geometry/material layering.
- **HYBRID PRESERVATION**: keep every usable original feature and reconstruct
  only genuinely missing features/zones. Prefer this to wholesale redraw when a
  partial face is still reliable.

A clean-looking generated face is **not** proof of source identity. Never claim
that unseen pixels were recovered. Use the structured `face_strategy` in transfer-record schema v2 for new facial
transfers; schema v1 remains valid for legacy/non-face records. Neither schema
certifies visual likeness, seam invisibility or the truth of declared observations.

## Decision and execution

1. Inspect the actual source at native resolution and the target in Blender.
   Identify the region, visibility, lighting contamination, useful pixel density,
   graphic landmarks and required viewing distance. Record a source hash and crop.
2. Select DIRECT, RECONSTRUCT-THEN-LAYER or HYBRID using source visibility,
   landmark integrity, lens/projection compatibility and the intended result.
   Prefer a direct crop where possible. Correction/upscale cannot recover
   missing evidence; inspect all intermediates against original pixels.
3. For any generated face feature, document missing evidence and use a bounded
   mask, source identity anchors and controlled prompt/output lineage. A clean
   complete face is an **intermediate under review**, not a replacement for
   usable original regions or permission to redesign expression. Stop when
   identity cannot be supported.
4. Register landmarks to supporting geometry and existing UVs. Restore
   intentional occluding hair in front of the face; preserve its silhouette.
   Choose projection/decal/UV for articulation and delivery. Run the
   [seam integration](references/workflow.md#seam-integration--patch-disguise)
   sequence before accepting the result. Bake through surfaces and clean
   seams/padding locally.
   Record a justified bake SKIP only when the delivery profile accepts the retained
   editable mapping and its movement/portability limitations have been checked.
5. Reconstruct roughness, metallic, normal/height and other physical responses
   separately. RGB lighting is not material data. A graphic mask may locate an ink
   or coating region; it does not determine that region's PBR values.
6. Inspect original/prepared/baked facial landmarks and their real 3D placement
   under neutral unlit/flat evaluation, neutral lighting and intended lighting.
   **Visible hard patch contours, rectangular/oval borders, skin-tone halos or
   pasted-on features mean seam/identity FAIL** for that named region, even if
   a distant beauty shot looks acceptable. Protect approved features during
   rework. Save textures, reopen the candidate and recheck bindings. Use the
   [transfer record](references/record.md) for provenance and separate
   structural, visual and target acceptance.

For final character acceptance, consume the shared
[character QA matrix](../blender-pipeline/references/qa.md) and record
`face_identity`, `seam_invisibility`, `hair_occlusion` and
`uv_binding` as named observations. A checked transfer JSON alone
cannot waive high_45/low_45 views or human visual review.

## Identity and handoff

Use the upstream [Face Strategy Gate](../blender-character-modeling/references/workflow-gates.md)
before constructing a final reference face, even when transfer was not explicitly
named. Reading this skill is not execution. If generation is selected, check
ImageGen and retain actual output lineage or report BLOCKED. QA schema 3 consumes
the existing transfer record.

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

### RST-002 — Occluded face and visible patch
- Symptom: a usable eye/mouth crop is pasted onto a face with visible rectangular seams, or hidden anatomy is improvised beneath hair.
- Cause: feature extraction, occlusion reconstruction, landmark registration and skin integration were collapsed into one unchecked paste.
- Rule: select DIRECT/RECONSTRUCT/HYBRID per region; preserve valid source pixels, separate occluders, align to face UV/volume, integrate seams and reject visibly pasted boundaries.
- Automated check: schema-v1 record proves lineage only; no structural field or hash proves invisible seams or identity.
- Verification: real closeups of the baked/imported face under neutral and target conditions compared with authoritative original; visual FAIL remains open until corrected.
- Added from / context: Agent_Red7 report, 2026-10-07, and requested improvement, 2026-10-08.
- Version: 1.1.0, 2026-10-08.


### RST-001
- Symptom: sharper texture loses the original face or exact lettering.
- Cause: whole-image generation/upscale treated as faithful data recovery.
- Rule: reuse source pixels first; repair only deficient masked regions and compare identity anchors.
- Automated check: transfer record requires repair reason, mask/prompt provenance and separate PBR basis.
- Verification: inspect original/prepared/baked regions and alternate views; record limits.
- Added from / context: requested Reference Surface Transfer workflow, not a claimed production incident.
- Version: 1.0.0, 2026-10-06.
