# Finishing techniques

Use only the techniques relevant to the named asset and approved finish. The
[skill](../SKILL.md) owns scope; [surfaces](../../blender-pipeline/references/surfaces.md)
owns UV/bake mechanics. Source attribution and limitations are in
[research notes](research-notes.md).

## Material foundation and texture refinement

Identify substrate, coating and deposit separately. A painted steel panel may
have dielectric paint over conductive exposed steel, then nonmetallic dirt on
top. Rust is not shiny raw metal. Keep these regions consistent across base color,
roughness, metalness and relief rather than putting every effect in color alone.
This is a starting model for plausible opaque finishes, not a ban on intentional
stylized shaders or other material models.

Prefer a readable simple shader before adding coat, transmission, subsurface,
sheen or anisotropy; enable a layer for a reference-driven material need. Preserve
existing target conventions. A glossy plastic is not made metallic to obtain
stronger highlights. Work on roughness variation at useful scales and test it in
another light; do not brighten albedo to compensate for a bad light rig.

Color textures need their authored color space; roughness/metalness/masks and
normal/height data need the corresponding data interpretation. Route normal maps
through the correct normal-map node/tangent convention. Combine relief coherently,
not by adding RGB normal images. Avoid duplicating relief in normal and bump.
Fix missing sources, stretching, tiling, compression or mip-edge artifacts at
their cause. Upscaling a small image does not recover lost information. Preserve
legible labels, clean material boundaries and target-camera detail hierarchy.

## Cause-driven masks and weathering

Choose the simplest controllable representation: texture painting, procedural
node groups, baked masks, decals or a hybrid. Curvature, AO/cavity, position and
normal/direction masks are useful candidate regions, not evidence that a specific
patch is worn. Combine a region/contact mask with controlled breakup and local
paint; avoid the same grunge scale in every channel and every object.

| Effect | Placement and channel decisions | Avoid |
|---|---|---|
| Dust/dirt | Upward/exposed surfaces, recesses or known contact; vary color/roughness and appropriate relief | Uniform brown AO over the entire asset |
| Fingerprints/polished use | Handles, buttons, grip paths and repeated contact; often mainly roughness | Assuming all abrasion makes a surface rougher |
| Scratches/scuffs | Contact/drag direction and sparse clusters; roughness/normal or height as needed | Identical scratches over every convex edge |
| Chipped/peeling paint | Reveal the correct undercoat/substrate with a coherent mask across channels | Bare-metal color beneath wood/plastic; automatic geometry flaps |
| Rust/oxidation | Compatible substrate, moisture/exposure/fasteners and plausible streak direction | Rust on every material or in sealed regions without a cause |
| Surface cracks | Material-specific branching, stress/weather pattern and scale; shallow relief when sufficient | Deep fracture or silhouette loss hidden in a normal map |
| Leaks/stains | Origin plus gravity/runoff/contact; distinguish wetness from dried residue | Random streaks disconnected from an origin |

Use broad condition zones first, local wear second and microdetail last. Preserve
rest areas and an intentional focal hierarchy. Peeling flaps, deep splits and dents
that affect shape require the geometry/sculpt owner; return for surface treatment
after a scoped handoff. Paint can be softened/stained without being damaged.

For reusable/animated assets, inspect whether object/world/generated coordinates
stay attached to the surface; use stable coordinates or bake where needed. Test
mirrored UVs, seams and instances: repeated masks can reveal the construction.
Do not rebake an articulated assembly in an arbitrary pose and call its AO stable.

## Emission and final image effects

Start with a motivated luminous region: indicator, display, filament, light strip
or approved magical/stylized source. Mask it independently from the base material;
keep nonluminous regions intact. Judge perceived brightness with the actual
renderer, exposure and view transform. Preserve source colors and readable detail
where needed rather than increasing strength until everything clips.

Emission is the surface output; whether/how it lights other surfaces depends on
the renderer and lighting setup. Glare/bloom is an image effect, not proof of
emitted illumination. Where requested, use the installed compositor's Glare or
target-specific equivalent, controlling highlight selection, spread and mix so
the asset stays readable. Do not assume old Eevee Bloom instructions apply.

Compare the underlying render and effected image at fixed settings. Grading,
vignette, depth of field, lens streaks or chromatic effects are optional scene
presentation choices, outside a surface-only task unless requested. They must not
conceal texture/shading defects. Prefer the project's existing color pipeline;
changing view transform/exposure between BEFORE and AFTER breaks comparison.

Procedural Blender shaders and compositor graphs do not automatically survive a
game-asset export. Record material data, baked-map needs and presentation settings
separately. Route conversion to surfaces and fresh-import/target proof to delivery
owners; keep Blender-only presentation if that is the actual requested output.
