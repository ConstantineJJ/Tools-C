# Anime character modeling — source notes

Reviewed 2026-10-04. These are concise Tools_C decisions informed by primary
documentation, published research and an instructor's public course description.
Paid lessons and embedded videos were not watched. Some Blender manual pages
returned 402; indexed official excerpts and accessible API documentation supplied
the stated node/modifier limits. Inspect the installed Blender version before use.

## Form and production

- [Grant Abbitt / GameDev.tv — Blender Anime Character Creator](https://gamedev.tv/courses/blender-anime-character):
  the public curriculum separates face/body construction, hair/clothing, texturing
  and rig/pose work, emphasizing polygon modeling and deformation-aware edge flow.
  Applied as editable anime form preparation with distinct downstream owners.
  This is not a summary of inaccessible lesson instructions or a prescribed body ratio.
- [Junya Christopher Motomura / Arc System Works — GuiltyGearXrd at GDC](https://www.gdcvault.com/play/1022031/GuiltyGearXrd-s-Art-Style-The):
  the accessible abstract establishes intentional preservation of a 2D art identity
  within a 3D production framework. Applied as art-direction-first acceptance.
  Specific normal, camera or animation recipes are not attributed to an unwatched talk.
- [He et al. — CHARM, SIGGRAPH Asia 2025](https://arxiv.org/abs/2509.21114):
  describes structured anime hairstyles using controllable hair-card geometry.
  Applied as editable clump/card organization, not mandatory model generation,
  dataset download or a guarantee that a paper's learned method exists in Blender.

## Blender techniques and boundaries

- [Blender curves geometry](https://docs.blender.org/manual/en/3.0/modeling/curves/properties/geometry.html):
  profile/bevel and taper support editable curve-based forms. Applied conditionally
  to hair clumps; versioned documentation is not an API compatibility guarantee.
- [Blender Normal Edit, 5.2](https://docs.blender.org/manual/sv/latest/modeling/modifiers/normals/normal_edit.html)
  and [NormalEditModifier API](https://docs.blender.org/api/4.0/bpy.types.NormalEditModifier.html):
  custom shading normals can be generated and mixed independently of vertex shape.
  Applied to diagnosis and a surface-owner handoff. Old Auto Smooth setup advice
  must not become a universal instruction for current Blender versions.
- [Blender EEVEE supported nodes, 5.2](https://docs.blender.org/manual/en/5.2/render/eevee/limitations/nodes_support.html)
  and [Shader to RGB](https://docs.blender.org/UATEST/manual/en/dev/render/shader_nodes/color/shader_to_rgb.html):
  Shader to RGB is renderer-specific. Applied as a requirement for compatible
  evidence, with geometry and final toon appearance accepted separately.

## Destination appearance

- [VRM Consortium — MToon](https://vrm.dev/en/univrm/shaders/shader_mtoon/):
  documents lit/shade treatment, shadow controls, outline width spaces and
  transparency limitations. Applied as a surface/finishing/target checklist;
  published defaults do not prescribe every character's look.
- [VRMC_materials_mtoon](https://vrm.dev/en/vrm1/mtoon/):
  defines a dedicated material extension. Applied as an explicit destination
  support decision, not automatic portability through a generic GLB export.

Multi-view likeness, reversible edits, stage boundaries and the visual correction
loop are Tools_C synthesis combined with the existing foundation/evidence contract.
Sources do not establish universal ratios, topology budgets, rig names or beauty
criteria. Structural contracts certify registration and links; resemblance,
expressions and target appearance require actual reviewed artifacts.
