# Posteffects and polishing — research notes

Reviewed 2026-10-03. These are short decision summaries from primary documentation,
vendor tutorials and artist-authored breakdowns. Blender manual topics were
available through indexed official excerpts; some full-page fetches returned 402.
Manual examples span 4.5/5.2, so inspect installed nodes before use. No video was
claimed watched. Toolbag/Substance examples supply transferable ideas, not a
required application, asset pack or fixed shader recipe.

## Materials and consistency

- [Blender Principled BSDF, 4.5](https://docs.blender.org/manual/fr/4.5/render/shader_nodes/shader/principled.html):
  layered material construction and compatible PBR inputs. Applied as an existing
  material foundation with purposeful layers, not an automatic graph replacement.
- [Blender color spaces, 5.2](https://docs.blender.org/manual/sv/5.2/render/color_management/color_spaces.html):
  normal/displacement and other numeric data must not receive a color transform.
  Applied as explicit map-role review while retaining the project's color pipeline.
- [Jeff Russell — Basic Theory of PBR](https://marmoset.co/posts/basic-theory-of-physically-based-rendering/):
  microsurface response is a major part of material appearance. Applied as roughness
  refinement and relighting rather than relying entirely on albedo detail.
- [Marmoset PBR workflow and artist Q&A](https://marmoset.co/posts/physically-based-rendering-and-you-can-too/):
  material references and a base-material block-in precede final tuning; values
  adjusted for one light can fail elsewhere. Applied as clean-base and alternate-light
  checks. Its physical examples do not override stylized art direction.
- [Adobe OpenPBR FAQ](https://experienceleague.adobe.com/en/docs/substance-3d/general-knowledge/openpbr/openpbr-faq):
  prioritize a few useful base parameters and add specialized layers only for a
  clear need. OpenPBR labels and transport capabilities are not assumed identical
  across Blender versions, glTF or a game engine.

## Wear, control and production iteration

- [Adobe Painter Metal Edge Wear](https://experienceleague.adobe.com/en/docs/substance-3d-painter/using/effects/generators/metal-edge-wear):
  generates a mask from curvature, position, normal and AO inputs with controllable
  grunge. Applied as candidate masking with local control; Blender does not have
  this named generator by default and missing maps must not be fabricated.
- [Marmoset baking/texturing/rendering handbook](https://marmoset.co/posts/the-toolbag-baking-texturing-and-rendering-handbook/):
  fill/adjustment/procedural layers and direction/curvature/occlusion processors
  offer different controls. Applied as editable effect layers and spatial mask
  choice, not a compulsory material stack.
- [Ben Armstrong — Baking a Hard Surface Weapon](https://marmoset.co/posts/baking-a-hard-surface-weapon-in-toolbag/):
  specific use marks such as tool scratches near screws, recoverable damage layers,
  then base/coating/wear refinement and iterative render checks. Applied as causal
  wear and reversibility; its sculpt damage remains a separate shape-owner task.
- [Marmoset — Rendering Clothing and Armor](https://marmoset.co/posts/rendering-realistic-clothing-and-armor-materials-in-toolbag/):
  usage/age/maintenance informs fingerprints, grime and wear placement. Applied
  as a condition brief; every asset need not be old, dirty or edge-worn.
- [Marmoset Cargo Ship tutorial series](https://marmoset.co/posts/3d-hard-surface-workflow-in-toolbag-cargo-ship-series/):
  separates layered weathering, grime/decals, emission and final presentation.
  Applied as modular controls and a distinct surface-versus-image handoff.

## Glow and evidence

- [Blender Glare, 4.5](https://docs.blender.org/manual/zh-hans/4.5/compositing/types/filter/glare.html):
  bright-image regions feed bloom/fog glow/lens effects with highlight/spread
  controls. Applied as a compositor treatment distinct from emissive shading.
- [Tools_C evidence methods](../../../docs/blender-evidence.md) supply the actual
  capture, image inspection, correction and fallback contract. This project's
  implementation limits determine which scene effects a capture can demonstrate.

The scope boundaries, late-stage placement, stop conditions and QA checklist are
Tools_C synthesis from these sources and the existing owners, not quotations or
claims that an artist prescribed a universal pipeline. Exact strengths, texture
budgets, art style and target support stay project-specific. L1 certifies declared
registration and links; visual acceptance still requires inspected artifacts.
