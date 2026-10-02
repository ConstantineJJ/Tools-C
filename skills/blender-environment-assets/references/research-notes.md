# Research notes — environment assets

Research snapshot: 2026-10-02.

This file records the external principles used to design the specialist skill for discrete environment fixtures such as benches, lamps, fences/railings, bins, bollards, hydrants and barriers. Blender documentation is treated as software authority. Production articles/community material supplies workflow evidence and heuristics, not universal contracts. Project-specific budgets, texel density, LOD targets and engine rules remain local.

## Blender Manual 4.5 LTS — Modifiers

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/introduction.html

Key points used:
- modifiers are non-destructive operations over editable base geometry;
- modifier stacks allow repeated/generated operations to remain editable until application is actually needed;
- applying a modifier makes its result permanent, so destructive application should be justified by a downstream need rather than done automatically.

Applied as the skill's preference for editable source geometry while proportions/family design are still changing.

## Blender Manual 4.5 LTS — Bevel Modifier

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/bevel.html

Key points used:
- Bevel provides controlled edge width/segments and can be limited by angle, weight or vertex group;
- Harden Normals/Face Strength can be part of a stable hard-surface shading setup;
- bevel geometry affects real edge shape, unlike a purely shading-only trick.

Applied as a scale/readability tool, not a mandate to bevel every edge. Width and segment count remain asset/view-distance decisions.

## Blender Manual 4.5 LTS — Weighted Normal Modifier

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/normals/weighted_normal.html

Key points used:
- weighted normals can help broad faces retain a visually flat appearance around beveled geometry;
- the modifier can cooperate with face strength from Bevel;
- normal editing changes shading, not underlying geometry.

Applied as an optional shading aid after geometry is correct; the skill explicitly rejects using normals to conceal a broken silhouette or topology.

## Blender Manual 4.5 LTS — Asset Browser

Source:
https://docs.blender.org/manual/en/4.5/editors/asset_browser.html

Key points used:
- Asset Browser supports Link, Append and Append (Reuse Data) behavior;
- repeated appended/reused objects can share mesh/material data;
- collection assets can be placed as collection instances;
- link/append choice determines whether later source changes propagate or whether the scene owns an independent copy.

Applied to repeated fixture/family packaging and the rule that reuse method should match whether downstream source updates must propagate.

## Blender Manual 4.5 LTS — Collections / instancing

Source:
https://docs.blender.org/manual/en/4.5/scene_layout/collections/collections.html

Key points used:
- collections support instancing and instance offsets;
- collections can act as meaningful asset/export boundaries;
- repeated collection-level assets need not be duplicated into unrelated independent meshes.

Applied to reusable fixture assemblies and placement-oriented packaging.

## 80 Level — Creating Ready Assets for the Market

Source:
https://80.lv/articles/creating-ready-assets-for-the-market

Key points used:
- begin from broad reference gathering, including understanding how the object works, is assembled and what materials it uses;
- blockout exposes scale/proportion/design problems before high-detail work;
- production quality benefits from solving major form before technical polish.

Applied as reference-by-question, construction-first and blockout-first guidance.

## 80 Level — Props for Games: Sculpting, Retopology, LODs

Source:
https://80.lv/articles/001agt-props-for-games-sculpting-retopology-lods

Key points used:
- scale/proportion and functional clearance should be tested in blockout against the target character/context;
- texel density is normally a project/world target rather than an arbitrary value invented per asset;
- mirrored/shared UV regions affect where unique details can be placed;
- LOD reduction should preserve the most noticeable silhouette/readability first.

The article includes example density and reduction numbers from one production context. Those numbers are deliberately NOT promoted to universal rules in Tools_C.

## 80 Level — Highway Scene: Blender modeling and vegetation workflow

Source:
https://80.lv/articles/highway-scene-using-blender-for-modeling-and-vegetation-workflow

Key points used:
- modularity is useful where objects genuinely repeat: construction pieces, fences, barriers and similar environment elements;
- unique/non-modular treatment can be preferable for major scene pieces where repetition would hurt composition;
- the author used unique textures for small props and tiling/layered materials for medium/large environment assets in that project.

Applied as a decision heuristic: choose reuse/modularity by repeated function, not as a universal requirement. Texture strategy is framed as a reusable-vs-unique decision, not as a size-only law.

## 80 Level — Cathedral of the Dead: Environment Production

Source:
https://80.lv/articles/cathedral-of-the-dead-environment-production

Key points used:
- establish scene/project texel-density rules before final UV allocation;
- preserve blockout proportions/measurements while refining assets so reintegration does not break snapping or scene layout;
- geometry bevels and weighted normals can improve hard-surface edge/shading quality;
- material wear should differ by material rather than use one uniform treatment.

The source's exact texel-density number is project-specific and not copied into the skill.

## Beyond Extent — Balancing Modularity and Uniqueness in Environment Art

Source:
https://www.beyondextent.com/articles/balancing-modularity-and-uniqueness-in-environment-art

Key points used:
- trim sheets are shared texture resources intended to reuse bands/patterns across multiple meshes;
- trim use often requires planning geometry/UVs around the shared sheet rather than treating UV work as an afterthought;
- modularity should be balanced with uniqueness so repeated assets do not become visually mechanical.

Applied to family/trim planning and to the separation between shared construction language and local variation.

## 80 Level — The Workflow Behind an Abandoned Bar Modular Environment

Source:
https://80.lv/articles/the-workflow-behind-an-abandoned-bar-modular-environment

Key points used:
- decide early which assets/parts justify trims/tileables versus unique textures;
- include a detail in a shared trim only if its frequency and UV practicality make the reuse worthwhile;
- up-front planning costs time but can substantially reduce later texturing work.

Applied as a frequency/reuse test rather than a blanket 'use trims' rule.

## 80 Level — Environment & Prop Artist on Creating Different Environments & Props

Source:
https://80.lv/articles/3d-environment-prop-artist-on-creating-different-environments-props

Key points used:
- blockout is used to establish structure/proportion before mid/high detail;
- decals can add local variation and break repetition without requiring unique geometry for every repeated prop;
- mixed workflows are normal: the representation should follow the asset's actual needs.

Applied to staged detail and cosmetic variation layers.

## Polycount — Questions about game-ready asset modeling workflows

Sources:
https://polycount.com/discussion/234552/questions-about-game-ready-asset-modeling-workflows
https://polycount.com/discussion/comment/2787413/

Key practice used:
- real game-ready hard-surface production does not have one universally correct topology path; low-to-high, boolean/high-to-low and other workflows can all be valid depending on baking, shading, editability and target needs.

This is community discussion, not a formal standard. The skill therefore avoids prescribing 'perfect quads first' or one mandatory high/low pipeline and judges the representation by stable output and downstream use.

## Synthesis for Tools_C

The recurring high-value pattern across these sources is:

1. prove scale, silhouette, placement and construction in blockout;
2. classify whether the asset is one-off, repeated, family-based or part of a modular sequence;
3. preserve shared data/instances when repetition is real;
4. use bevels/normals/modifiers as controlled production tools rather than automatic rituals;
5. choose shared/trim/tileable/unique surface strategy from reuse and camera needs;
6. place wear according to material, exposure and contact rather than uniform grunge;
7. validate in environment context and repeated placement, not only an isolated turntable;
8. leave project-specific triangle, texel, LOD, collision and export budgets to the active project contracts/owners.
