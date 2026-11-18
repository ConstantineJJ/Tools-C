# Anime profile — toon look and evidence

Part of the [anime character skill](../SKILL.md). Geometry stays with this skill;
UVs, masks and base toon graphs belong to [surfaces](../../blender-pipeline/references/surfaces.md),
refinement of an existing look to [polishing](../../blender-posteffects-polishing/SKILL.md).

## Shading diagnosis

Read the form with neutral solid lighting before blaming geometry for a toon
shadow. Then compare the actual renderer and intended material. Preserve custom
normals and modifiers while isolating a geometry defect.

Shader to RGB is an EEVEE-specific technique. A Cycles render or a generic GLB
material cannot certify its appearance. MToon is a target shader/extension contract,
not a guarantee that Blender nodes export to standard glTF. Decide the destination
shader with the export/integration owners before expensive look development.
Verify installed node/modifier APIs instead of copying legacy Auto Smooth commands.

Outline methods may use a hull, shader or image stage. Keep any hull separately
identified; avoid inflating the source form to hide a line-width defect. Compare
line coverage at the target distance and inspect inner seams, eyelids and hair tips.

## Renderer-compatible evidence

Use [Blender evidence methods](../../../docs/blender-evidence.md). Workbench/solid
evidence supports geometry. Managed material_preview and rendered captures use
Cycles without the production compositor; they cannot certify an EEVEE-only
Shader to RGB graph, final outlines or bloom. For those criteria inspect a render
from the verified source renderer/compositor or the target engine through an
authorized path. Preserve production settings. If unavailable, report the
criterion as SKIP rather than swapping shaders, disabling effects or accepting a
different renderer's image (ANIME-002).

## Correction record

Inspect the full silhouette and a face/hair close view. After a correction repeat
the affected projection and a protected alternate view with the same camera/frame/
framing/resolution/light. Record the defect, changed region and KEEP/CORRECT/REVERT.
Expression and deformation acceptance needs the requested poses/playback from the
appropriate owner; absence of those checks remains explicit.
