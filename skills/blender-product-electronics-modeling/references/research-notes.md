# Research notes — product & electronics modeling

Research snapshot: 2026-10-02.

This file records external principles used to design `blender-product-electronics-modeling`. Blender documentation is treated as software-behavior authority. Product/hard-surface artist breakdowns provide production practice and heuristics, not universal contracts. Exact gap widths, bevel radii, texture sizes, texel-density targets, triangle budgets, LOD ratios and engine/UI behavior remain project-local.

## Blender Manual 4.5 LTS — Boolean Modifier

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/booleans.html

Key points used:
- Boolean supports Difference, Union and Intersect operations for controlled hard-surface openings/assembly;
- manifold inputs are the most predictable; non-manifold geometry may produce glitches/artifacts;
- a successful modifier evaluation does not guarantee desirable topology/shading.

Applied to ports, vents, recesses and handle openings with explicit post-boolean inspection rather than treating boolean completion as acceptance.

## Blender Manual 4.5 LTS — Bevel Modifier

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/bevel.html

Key points used:
- Bevel adds real edge geometry with controllable width, segments and limit methods;
- Harden Normals/Face Strength can support stable manufactured shading;
- bevel width is actual geometry and should reflect product scale/material language.

Applied to enclosure edge hierarchy and the rule that plastic, thin metal, rubber and glass should not all use one arbitrary bevel treatment.

## Blender Manual — Weighted Normal Modifier

Source:
https://docs.blender.org/manual/en/5.2/modeling/modifiers/normals/weighted_normal.html

Key points used:
- weighted normals modify custom shading normals and can make broad faces appear flatter;
- Face Influence can cooperate with Bevel Face Strength;
- the modifier changes shading, not underlying geometry.

Applied as an optional flat-surface shading aid after enclosure geometry is correct.

## Blender Manual 4.5 LTS — Solidify Modifier

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/solidify.html

Key points used:
- Solidify adds thickness/depth to surface geometry;
- simple mode has limitations on non-manifold/problematic surface arrangements;
- normal orientation matters to generated thickness.

Applied to sheet-metal/plastic shell panels only where automatic thickness behavior is suitable and verified.

## Blender Manual 4.5 LTS — Array Modifier

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/array.html

Key points used:
- Array repeats a base object using controlled offsets/counts/length;
- repeated manufactured forms are natural candidates for a single editable source rather than many independent copies.

Applied to vents, keys, grille slats, repeated buttons and similar product patterns while preserving a recoverable source.

## Blender Manual 4.5 LTS — Cycles Baking

Source:
https://docs.blender.org/manual/en/4.5/render/cycles/baking.html

Key points used:
- baking requires UVs and an active image/color target;
- tangent-space normals are usually suitable for reusable/game assets;
- Selected to Active projects from selected high/source geometry to the active low object;
- Max Ray Distance, extrusion and cage control projection;
- bake margin matters for filtering/mip seams.

Applied to fine manufactured relief/perforations and high/low workflows without making baking mandatory for every device.

## Blender Manual 4.5 LTS — Asset Browser

Source:
https://docs.blender.org/manual/en/4.5/editors/asset_browser.html

Key points used:
- Link, Append and reuse/instancing approaches differ in whether source changes propagate;
- asset libraries support reusable product modules/materials/collections.

Applied to product families and shared buttons/feet/knobs/ports while keeping local versus propagated ownership explicit.

## 80 Level — Creating a Game Boy Color in Blender & Substance

Source:
https://80.lv/articles/creating-a-game-boy-color-in-blender-substance

Source type: collaborative product/electronics prop breakdown.

Key practices used:
- start from a shared blockout/cross-section so separate shell halves and internal/visible components retain the same measurements;
- screw holes and motherboard/shell interfaces require coordinated alignment when open/internal detail is visible;
- hard edges/UV islands and bake planning are related decisions in a hard-surface workflow;
- roughness/fingerprints materially contribute to the story/read of handled consumer electronics.

Applied as evidence for shared product metrics, enclosure-first assembly and material-use history. The source's specific addon stack is not made a Tools_C requirement.

## 80 Level — Retro-inspired imaginary device / Synthron 5000

Source:
https://80.lv/articles/creating-retro-inspired-imaginary-device-with-blender-substance-3d

Source type: Blender hard-surface device production breakdown.

Key practices used:
- blockout establishes proportions/overall product language before technical detail;
- buttons and vents can be repeated with Array and kept non-destructive through design changes;
- opening product parts can be parented/pivoted and temporarily separated during baking to reduce projection contamination;
- bake organization should preserve the neutral product assembly so it can be restored after exploded/separated bake preparation.

Applied directly to repeated controls/vents and opening-part/bake safeguards.

## 80 Level — Sci-Fi Radio Device with Plasticity & Blender (2025)

Source:
https://80.lv/articles/creating-realistic-sci-fi-radio-device-using-plasticity-blender

Source type: professional hard-surface concept/product workflow.

Key practice used:
- product/device modeling may validly combine CAD-like solid modeling with Blender cleanup/lookdev rather than insisting on one polygon-only pipeline;
- design language and material/render feedback can guide hard-surface decisions alongside topology concerns.

Applied as support for CAD-assisted/hybrid representation being a first-class option, not a fallback.

## 80 Level — Soviet Hospital modeling/texturing workflow

Source:
https://80.lv/articles/soviet-hospital-modeling-and-texturing-workflows

Source type: Blender environment/prop production breakdown.

Key practices used:
- small/medium hard-surface assets can remain entirely Blender-based when that reduces unnecessary tool round-tripping;
- speaker holes and similar manufactured openings are practical boolean candidates;
- some fine details can be transferred through height/normal information rather than geometry.

Applied to representation-by-need for speaker grilles/holes and rejection of toolchain complexity for its own sake.

## 80 Level — Creating Ready Assets for the Market

Source:
https://80.lv/articles/creating-ready-assets-for-the-market

Source type: game-asset production workflow.

Key practices used:
- collect enough views to understand how an object works, is assembled and what materials it uses;
- blockout catches proportion/scale errors early;
- construction/material understanding should precede polish.

Applied to manuals/listings/teardown-driven reference strategy and enclosure-first modeling.

## 80 Level — Warhammer 40K-style hard-surface environment breakdown

Source:
https://80.lv/articles/creating-a-warhammer-40k-inspired-scene-with-blender-ue5-s-substrate

Source type: Blender hard-surface production breakdown.

Key practices used:
- large/main boolean passes can establish primary forms before smaller secondary recesses/details;
- bevel/refinement follows the major visual read rather than starting from micro-cutters;
- different asset regions can switch techniques when that is faster/more appropriate.

Applied as a large-to-small boolean/detail hierarchy rather than an addon-specific workflow.

## 80 Level — Hard-surface workflow mentorship / functionality analysis

Source:
https://80.lv/articles/hard-surface-program-new-live-mentorship-announced

Source type: training overview from experienced hard-surface production.

Key principle used:
- shape/functionality and mechanical articulation should influence final hard-surface design;
- blockout and reconstruction/retopology choices belong upstream of final presentation.

Applied to controls, hinges, removable panels and product function being part of geometry reasoning rather than decoration.

## 80 Level — hard-surface artistic workflow / Ahmed Yahya

Source:
https://80.lv/articles/artist-shared-how-to-make-hard-surface-modeling-more-artistic-easy

Source type: experienced environment/prop artist workflow discussion.

Key principle used:
- hard-surface production should not let topology/tool technique overshadow the intended visual/product design;
- CAD/Blender/ZBrush pipelines can be mixed when the target benefits.

Applied as a safeguard against turning product modeling into a modifier checklist instead of solving the device's shape/function/design language.

## Synthesis for Tools_C

The recurring durable pattern is:

1. Establish accurate enclosure dimensions, major controls/openings and product role before technical microdetail.
2. Use manuals, listings and teardown/repair photos when marketing views omit backs, undersides and assembly details.
3. Treat shell halves/panels/doors/bezels as an assembly system, not arbitrary panel-line decoration.
4. Keep booleans, arrays, repeated controls and vents editable until the design is stable; inspect output rather than trusting modifier success.
5. Choose geometry versus bake/mask for perforations and microdetail according to target depth/parallax/screen size.
6. Define pivots/travel for controls and opening parts before animation/runtime handoff.
7. Separate physical screen/display surfaces from replaceable UI/content.
8. Establish clean plastic/metal/rubber/glass material response before fingerprints, dust, grease or wear.
9. Use shared product-family components where identical while keeping label/screen/story variants independent.
10. Keep electrical/runtime/UI and project-specific performance budgets outside this universal modeling skill.
