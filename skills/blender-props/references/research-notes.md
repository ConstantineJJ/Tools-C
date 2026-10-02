# Research notes — props

Research snapshot: 2026-10-02.

This file records external principles used to design `blender-props`. Blender documentation is treated as software-behavior authority. Artist interviews/tutorials and community discussions provide workflow evidence and heuristics, not universal contracts. Exact triangle counts, texture sizes, texel-density targets, LOD ratios, collision rules and engine budgets remain project-local.

## Blender Manual 4.5 LTS — Asset Browser

Source:
https://docs.blender.org/manual/en/4.5/editors/asset_browser.html

Key points used:
- Link keeps the asset read-only and lets later source-file changes propagate;
- Append makes local independent copies;
- Append (Reuse Data) reuses mesh/material data across repeated asset placements where possible;
- collection assets can be placed as collection instances;
- reuse mode changes whether downstream edits should propagate or diverge.

Applied to prop-library packaging, family reuse and the rule that repeated props should not be made unique accidentally.

## Blender Manual 4.5 LTS — Bevel Modifier

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/bevel.html

Key points used:
- Bevel creates real edge geometry non-destructively;
- width/segments/limit methods can be controlled rather than applying the same bevel everywhere;
- Harden Normals and Face Strength can cooperate with later normal processing;
- bevel width is actual geometric scale and therefore must be judged against object size and target camera.

Applied as an edge-readability tool, not a quality ritual.

## Blender Manual 4.5 LTS — Weighted Normal Modifier

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/normals/weighted_normal.html

Key points used:
- weighted normals change shading/custom normals and can help broad faces appear flatter;
- they do not change the actual silhouette or repair incorrect geometry.

Applied as an optional shading aid after geometry is structurally valid.

## Blender Manual 4.5 LTS — Cycles Render Baking

Source:
https://docs.blender.org/manual/en/4.5/render/cycles/baking.html

Key points used:
- baking requires UVs and an active image/color-attribute target;
- tangent-space normals are the usual choice for reusable/game assets;
- Selected to Active projects from high/source objects to the active low object;
- Max Ray Distance, extrusion and a cage control projection coverage;
- a manually edited cage can be used when simple extrusion fails;
- bake margins matter because texture filtering/mipmapping can otherwise expose seams.

Applied to the skill's bake checklist and the rule to fix projection/systemic issues rather than paint over them.

## Blender Manual 4.5 LTS — glTF 2.0 normal maps

Source:
https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html

Key points used:
- glTF expects tangent-space normal-map setup through a Normal Map node;
- the image should be treated as non-color data;
- Blender's bake workflow can generate tangent-space normal textures suitable for export.

Applied only as a delivery-awareness note; final export remains owned by `blender-export-validation`.

## Blender Manual 4.5 LTS — UV tools

Source:
https://docs.blender.org/manual/en/4.5/modeling/meshes/editing/uv.html

Key points used:
- Blender supports explicit UV unwrapping and multi-object texture-space workflows;
- UV layout is a production representation decision rather than something guaranteed by object topology alone.

Applied to deliberate unique/mirrored/stacked UV decisions and project-level texel-density ownership.

## 80 Level — Rafael Murta, Felco C12 Wirecutter (2026)

Source:
https://80.lv/articles/modeling-texturing-a-felco-c12-wirecutter-using-blender-substance-3d

Source type: recent prop-artist production breakdown using Blender.

Key practices used:
- auction/used-product listings are valuable because they often show many angles of one real object;
- reference gathering continues during production whenever a hidden part/material/detail becomes unclear;
- choose an orthographic-ish image to establish proportion in blockout;
- keep Mirror/non-destructive construction while symmetry is valid, then break it when true asymmetry is required;
- iterate the low/realtime mesh with quick test bakes rather than over-optimizing once and hoping the bake works;
- overlapping similar/symmetrical UV regions can save texture space, but high-information/asymmetrical regions should remain unique;
- establish clean base material properties before adding damage/dirt;
- roughness variation is a major part of material readability;
- not every region needs maximal detail.

The source includes author-specific software/settings and numeric values; those are not promoted to Tools_C contracts.

## 80 Level — Sasha Bernert, Stylized PBR Weapons / Props (2020)

Source:
https://80.lv/articles/stylized-pbr-weapons-workflow-for-creating-props

Source type: environment/prop artist workflow breakdown.

Key practices used:
- reference should be gathered by production need and revisited continuously;
- prop design can communicate world/story through construction, shape language, materials, wear and dirt;
- iterate from big shapes to medium to small rather than detailing too early;
- consider mechanism/function, identity, silhouette/aesthetics and gameplay/view angle together;
- several valid low/high/sculpt/final-low orders exist; the representation should match the job;
- allocate UV uniqueness according to what the player actually sees and where unique storytelling is needed;
- baking often exposes mesh/topology/UV problems and should be treated iteratively;
- roughness deserves the same intentional design attention as base color.

Applied as staged form hierarchy, storytelling questions, target-view UV priority and iterative bake diagnosis.

## 80 Level — Creating Weapons for a Mobile Game (2022)

Source:
https://80.lv/articles/creating-weapons-for-a-mobile-game-in-zbrush-marmoset-toolbag

Source type: prop/weapon production breakdown.

Key practices used:
- a common pipeline can be blockout → mid/high → low → UV/texturing → LOD, but topology and representation may remain pragmatic during early passes;
- units/axes are worth checking before detailed work;
- reducing the low mesh too aggressively before baking can create projection problems; test bakes should inform optimization.

Applied to transform/scale preflight and "clean bake before minimum polygon count" guidance.

## Polycount — low/high game prop workflow discussion

Source:
https://polycount.com/discussion/97381/some-questions-about-low-high-poly-game-prop-development

Source type: long-running professional/community technical discussion, not formal documentation.

Key practices used:
- blockout is not the final low mesh; its purpose is to settle proportions before dense detail;
- for many high/low props, the final low is refined around the proven high/source result;
- temporary UVs and test bakes can be iterated before final UV/bake;
- high/low shape agreement materially affects bake quality.

Applied cautiously: the skill preserves this as one valid high/low workflow, not a universal requirement for every prop.

## 80 Level — Forget-Me-Not Studios, lived-in game scenes (2026)

Source:
https://80.lv/articles/how-an-art-team-created-lived-in-scenes-for-a-detective-game

Source type: recent team production breakdown.

Key practices used:
- real-world furniture references help establish believable props;
- meshes can be reused while material/texture variants create diversity;
- optimization should preserve enough geometry for the intended realistic result;
- consistent texel density and shared/atlas strategies can reduce production/memory cost across many props;
- different asset families can be grouped according to room/theme/use rather than forcing each prop into a unique material set.

Applied to family reuse and library-scale material strategy; the source's exact texture resolutions/channel packing belong to its project and are not universalized.

## 80 Level — Props for The Callisto Protocol

Source:
https://80.lv/articles/creating-props-for-the-callisto-protocol

Source type: professional AAA prop/environment artist interview.

Key practice used:
- storytelling comes from asking how an object was made, what its function is, who owns/uses it and what physical history it experienced;
- fingerprints, drops, repairs and other history are meaningful only when they follow that usage story.

Applied to the prop-history questions and safeguard against random uniform damage.

## 80 Level — Vintage furniture/prop reference and auction sites

Source:
https://80.lv/articles/working-on-a-primadonna-s-dressing-table-with-vintage-props

Source type: prop/environment production breakdown.

Key practices used:
- furniture/antique references benefit from auction listings that provide multiple angles, dimensions and close-up wear;
- a family of small objects can communicate a character/story more effectively when their age/style/use is coordinated.

Applied to furniture reference gathering and family storytelling.

## 80 Level — Carpenter's Workshop (2021)

Source:
https://80.lv/articles/carpenter-s-workshop-making-a-detailed-game-ready-environment-in-ue4

Source type: senior environment artist production breakdown.

Key practices used:
- wear should follow use/exposure: dirt can accumulate in grain/recesses, sun affects exposed regions, contact produces different marks than protected surfaces;
- props in one believable space can have different ages and maintenance histories;
- storytelling details should be layered after the underlying material is established.

Applied to wear hierarchy and the rule that not every prop in a set should receive identical aging.

## Synthesis for Tools_C

The recurring durable pattern is:

1. Gather enough multi-angle/function/material reference to understand the object; return for more when uncertainty appears.
2. Prove scale, silhouette and function in target context before detail.
3. Choose direct realtime, high/low, sculpt-assisted or hybrid production from visible need rather than habit.
4. Preserve editable symmetry/modifiers while useful; break them only for real asymmetry or downstream need.
5. Treat low mesh, UVs, normals, cage and baking as an iterative system when baking is used.
6. Allocate UV uniqueness and texture budget to visible/story-critical regions; mirror/stack only where duplicated detail is acceptable.
7. Establish clean material identity—especially roughness—before damage and dirt.
8. Make wear explainable by use, contact, environment and age; leave quiet areas.
9. Choose pivots/hierarchy from placement, hand attachment and articulation.
10. Validate in target context and preserve project-specific budgets outside the universal skill.
