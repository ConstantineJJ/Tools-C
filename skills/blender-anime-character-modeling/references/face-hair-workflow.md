# Anime face, hair and presentation decisions

Read only the sections relevant to the modeling task. Ratios, colors, renderers,
expression sets and budgets come from the design and project profile.

## Translating a drawing into form

Identify silhouette, skull/jaw shape, eye line/spacing, brow rhythm, nose/mouth
placement, hair outline and head/body relationship. Separate observed landmarks
from perspective and graphic conventions. Register the intended reference view;
do not distort the whole model to fit an illustration's incompatible projections.
For a free design, choose a coherent style brief rather than averaging unrelated
anime references. Chibi proportions are an explicit design choice, not a universal default.

Start with skull, jaw, neck, torso and primary hair/outfit masses. Check whether a
front correction flattens the profile or whether a profile correction changes the
approved face width. Keep hidden-view assumptions editable until accepted.

## Face, eyes and mouth

Shape forehead, cheek, jaw, chin and nose as connected volumes. A small drawn nose
does not automatically require a flat skull or zero depth. Favor the reference's
facial planes and graphic rhythm over added realistic creases.

Choose spherical/ellipsoidal eyes, a shallow eye form or a graphic surface according
to expected views and expressions. Inspect lid seating and globe intersections;
avoid a floating iris or a silhouette hole behind lashes. Place iris/pupil, highlights
and lash geometry so they remain readable at the intended distance. Painted eye
details and highlights are surface decisions; physical corneas are conditional.

Model the neutral lid/mouth forms needed for the request. If blink/speech is required,
reserve closure and mouth-interior space and hand the planned expressions to topology,
rigging and animation. Existing shape keys preserve vertex correspondence; no silent
remesh, dissolve or join on a protected expressive face. Symmetry is a starting aid;
preserve designed asymmetry and separate its causes from accidental drift.

## Hair as designed masses

Use [form recipes](../../blender-pipeline/references/techniques/form-recipes.md)
when round tubes or constant slabs cannot describe the intended locks, limb
sections, cloth loops or fur. Prove one editable sample before multiplying it.

Block the cap, parting and large clumps first: fringe, sides, crown/back and any
separate tails or ornaments. Follow the intended root-to-tip flow. Compare negative
spaces and the outer contour before subdividing or adding strands.

Choose editable ribbons/cards, solid clumps or curves with a profile/taper to suit
the silhouette, viewing distance and downstream needs. Inspect curve twist, cross
section, root overlap, sharp tips, scalp exposure and neck/shoulder clearance.
Cards need the surface owner's alpha/culling strategy; solid clumps need controlled
thickness. Neither method is compulsory. Keep construction editable while uncertain;
conversion/application must preserve any downstream bindings and data.

One fringe can obscure an eye intentionally; accidental bald gaps, jagged card edges
or collisions require review. A static hair mesh does not establish dynamics or
collision behavior. Rigging owns any requested hair bindings/dynamics setup.

## Body and outfit

Carry the chosen proportions consistently through neck/shoulders, torso/hips,
hands/feet and clothing. Use folds to describe garment cut and support, not to
hide an incorrect body blockout. Identify rigid ornaments versus flexible cloth.
Keep garment/body layers separate where useful for editing and deformation;
separation is not proof of pose clearance. Do not delete hidden body geometry,
apply thickness or change costume identity without task authorization.

## Shading diagnosis and handoff

Read the form with neutral solid lighting before blaming geometry for a toon shadow.
Then compare the actual renderer and intended material. Surface ownership covers
UVs, masks, color regions, normal edits/transfers and base toon graphs; finishing
owns refinement of an existing look. Preserve custom normals and modifiers while
isolating a geometry defect.

Shader to RGB is an EEVEE-specific technique. A Cycles render or a generic GLB
material cannot certify its appearance. MToon is a target shader/extension contract,
not a guarantee that Blender nodes export to standard glTF. Decide the destination
shader with the export/integration owners before expensive look development.
Verify installed node/modifier APIs instead of copying legacy Auto Smooth commands.

Outline methods may use a hull, shader or image stage. Keep any hull separately
identified; avoid inflating the source form to hide a line-width defect. Compare
line coverage at the target distance and inspect inner seams, eyelids and hair tips.
An outline's world/screen width and transparency behavior depend on its implementation.

## Evidence and correction

Use the skill's [visual feedback contract](../SKILL.md) and shared
[capture guidance](../../../docs/blender-evidence.md). Inspect the full silhouette
and a face/hair close view. After a correction, repeat the affected projection and
a protected alternate view with the same camera/frame/framing/resolution/light.
Record the actual defect, changed region and KEEP/CORRECT/REVERT result.
If the criterion is toon bands, masks, outlines or compositor effects, acquire the
actual source-renderer/target image rather than a substitute Cycles preview.
Expression and deformation acceptance needs the requested poses/playback from
the appropriate owner; absence of those checks remains explicit.
