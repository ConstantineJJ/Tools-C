# UV, baking and PBR authoring

Inspect existing UVs, materials, textures, color spaces, mesh split boundaries,
target engine and texel budget before replacing anything. Preserve authored UVs
when the requested repair does not require a new unwrap.

For native production: finalize topology relevant to UV → place seams away from
critical visible bends → unwrap → inspect checker distortion and island scale →
pack with padding appropriate to resolution/mips → validate mirrored/overlapping
islands against the intended bake. Overlap may be intentional for tiling; report it
rather than treating all overlap as a defect.

For baking: identify high/low objects explicitly, align transforms, inspect cage
and ray distance, choose normal tangent basis compatible with export/import, and
test a small bake before a full pass. Keep required source detail recoverable.
Inspect skew, missed rays, seam artifacts and projection of adjacent parts. Bake
normal/AO and other maps only where needed; avoid embedding lighting in base color
unless art direction explicitly requires it.

For PBR: verify base color, roughness, metallic, normal and optional AO/emission
bindings, UV set and material slot assignment. Color textures and numeric maps
need their intended color spaces. Check channel packing against the target profile,
not guessed filename suffixes. A missing texture must be reported, not silently
replaced and called equivalent.

Evaluate neutral lighting and target-engine lighting at near and production camera
distance. Compare normal-map relief to a known-good surface under a moving light.
Recheck tangents and shading after triangulation, UV or normal edits. Validate
texture resolution, compression and material/draw-call cost where relevant.

Hard-surface workflow: establish silhouette and panel thickness → intentional
bevel/highlight widths → inspect Boolean intersections, planar faces and shading →
control edge splits/UV seams → bake and test export. Smooth shading or weighted
normals must not conceal holes, impossible intersections or deformation defects.

Handoff includes texture paths, UV sets, material slots, channel/color-space map,
bake settings and observed defects. UV/material edits require another-view and
another-asset regression checks when resources are shared.
