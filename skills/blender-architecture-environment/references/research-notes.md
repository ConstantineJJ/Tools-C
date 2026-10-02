# Research notes — architecture & large structures

Research snapshot: 2026-10-02.

This file records the external principles used to design the specialist skill. Blender documentation is used for software behavior. Production interviews, training material and community/industry guides are used for workflow practice where they converge; they are not treated as universal law. Project-specific grid sizes, budgets, LOD rules and engine constraints stay project-local.

## Blender Manual — Modifiers / Array / transforms

Sources:
https://docs.blender.org/manual/en/latest/modeling/modifiers/introduction.html
https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/array_legacy.html
https://docs.blender.org/manual/en/5.2/scene_layout/object/editing/apply.html

Key points used:
- modifier stacks are non-destructive and order-dependent;
- repeated architecture can be developed with Array-style workflows without immediately changing base geometry;
- object scale affects dimension-sensitive modifier behavior, so transforms must be inspected rather than ignored;
- applying transforms/modifiers changes data and can affect linked/hierarchical behavior, so destructive cleanup is not automatically desirable.

Applied in the skill as a preference for recoverable, editable construction while the design is changing rather than a requirement to use any specific modifier.

## Blender Manual — linked duplicates and Geometry Nodes instances

Sources:
https://docs.blender.org/manual/id/5.2/scene_layout/object/editing/duplicate_linked.html
https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/instances.html
https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/instances/instance_on_points.html
https://docs.blender.org/manual/en/5.0/modeling/geometry_nodes/instances/realize_instances.html
https://docs.blender.org/manual/id/5.2/modeling/geometry_nodes/performance.html

Key points used:
- linked duplicates share object data while retaining independent transforms;
- instances avoid duplicating the underlying geometry and are materially more efficient for high-count repeated meshes;
- Realize Instances converts those references into unique geometry and can increase memory/evaluation cost;
- Geometry Nodes performance benefits from minimizing processed geometry and avoiding unnecessary realization or expensive operations.

Applied as the rule to preserve linked/instanced repeated architecture until a concrete downstream operation needs uniqueness.

## Blender Manual — measurement, snapping and normals

Sources:
https://docs.blender.org/manual/en/3.6/editors/3dview/toolbar/measure.html
https://docs.blender.org/manual/en/5.2/scene_layout/object/editing/transform/control/precision.html
https://docs.blender.org/manual/id/5.1/modeling/meshes/editing/mesh/normals.html

Key points used:
- Blender provides direct distance/angle measurement and snapping for precise architectural checks;
- transform snapping supports discrete placement and geometry targets;
- Face Orientation and normal recalculation are practical checks for visible surface direction.

The skill therefore treats dimensions, grid placement and visible normals as observable QA rather than assumptions.

## 80 Level — Building a Desert Scene with Modular Kit & Trim Sheets — Chris Sims

Source:
https://80.lv/articles/building-a-desert-scene-with-modular-kit-trim-sheets

Key practices used:
- inspect references for genuinely repeating elements before designing a modular kit;
- keep modules on a consistent grid and test assembly before detailed production;
- design larger and smaller module sizes so they divide/compose predictably;
- use trim sheets for repeatedly reused architectural details such as frames/moldings;
- repeated trim use can save texture memory, but material/UV orientation should still follow the physical construction where visible.

The article uses project-specific 10 cm / powers-of-two choices; the skill generalizes only the discipline, not those exact numbers.

## 80 Level — SanXia Street 1940: Modular Approach, Trim Sheets, Decals — Cliff Chen

Source:
https://80.lv/articles/005cg-001agt-sanxia-street-1940-modular-approach-trim-sheets-decals

Key practices used:
- decompose reference architecture by distinguishing reusable sections rather than blindly splitting every visible part;
- aim for as few modules as practical while retaining useful reuse;
- build a blockout kit and assemble it before final modeling to expose missing/unnecessary pieces;
- trim sheets help keep modular materials consistent and support variations of the same mesh;
- avoid large highly recognizable stains/cracks in heavily repeated trim content because repetition becomes obvious.

This strongly informed the `reusable module / variant / unique / surface-only variation` classification and the warning against module explosion.

## 80 Level — Complex Modular Architecture Environment / 17th Century Roman Environment

Sources:
https://80.lv/articles/001agt-004adk-17th-century-roman-modular-environment-in-ue4/
https://80.lv/articles/001agt-004adk-17th-century-roman-modular-environment-in-ue4

Key practices used:
- blockout is a major production gate, not disposable busywork;
- architecture metrics should be tested before final geometry;
- human figures or other scale anchors become especially important when real-world dimensions are unusual or intentionally oversized;
- material planning and composition can start during blockout so final effort is focused where it matters;
- when blockout pieces already respect the intended metrics, replacing them with final modular pieces becomes straightforward.

Applied as "prove massing and metrics before detail," while keeping exact engine-specific constraints local.

## 80 Level — Vertical Slice: Building a Medieval City

Source:
https://80.lv/articles/vertical-slice-building-a-medieval-city

Key practices used:
- gather multiple primary/secondary architectural references and select compatible features rather than copying unrelated details;
- quick blockouts help rearrange architectural sections before committing;
- use a successful modular pack as a proportion/design-language reference so later buildings remain cohesive.

Applied as a reference-stack and consistency rule, not as a requirement to copy one historical source.

## 80 Level — Modeling and Texturing Assets and Foliage for a Detailed 3D Scene — Elie Paquiet

Source:
https://80.lv/articles/modeling-and-texturing-assets-and-foliage-for-a-detailed-3d-environment

Key practices used:
- modular building kits can deliberately use multiple compatible spans/scales rather than one module size;
- modularity and material systems are planned together;
- professional environment production benefits from reusable architecture/material systems rather than treating every building as an isolated asset.

The specific 3 m / 4.5 m / 6 m dimensions belong to that project and are not copied into the skill.

## 80 Level — How to Design a Medieval European Environment Using Unreal Engine and Substance 3D

Source:
https://80.lv/articles/how-to-design-a-medieval-european-environment-using-unreal-engine-and-substance-3d

Key practice used:
- one valid workflow is to prove the whole building's proportions first, then deconstruct that successful shell into modular pieces.

This supports the skill's "prove the building before decomposing it" rule and helps prevent modules that snap technically but do not produce a coherent whole.

## 80 Level — Modular Interior Environment Design in UE4

Source:
https://80.lv/articles/modular-interior-environment-design-in-ue4

Key practices used:
- modular environment planning should establish scale, measurements and assembly before detail;
- measuring real objects and comparing against references is useful when exact dimensions are unavailable;
- blockout is the cheap stage for major scale corrections.

Applied as a scale-anchor and metric-sheet practice, not as a demand for strict realism.

## 80 Level — Creating a Modular Snowy Church Environment in Unreal Engine 5

Source:
https://80.lv/articles/building-a-modular-snowy-church-environment-in-unreal-engine-5

Key practices used:
- combine real-world scale with deliberate stylization for mood/readability;
- evaluate both distant silhouette and reusable breakdown during blockout;
- use a human reference throughout to keep entrances, stairs, roof height and overall scale believable from gameplay perspective.

Applied as an explicit distinction between absolute measurements and perceptual/gameplay scale.

## Level Design Book — Environment Art / modular kits

Source:
https://book.leveldesignbook.com/process/env-art

Key principles used:
- environment materials are heavily reused, so texture/material systems should be designed for broad reuse;
- modular kits are most effective for regular man-made structures where pieces can snap into multiple arrangements;
- not every organic/irregular form benefits from forcing modularity.

Applied as the boundary between architectural modules and unique/organic specialist work.

## Game Environment Art with Modular Architecture — Statham, Jacob, Fridenfalk (Entertainment Computing, 2021/2022)

Source:
https://www.researchgate.net/publication/357348511_Game_Environment_Art_with_Modular_Architecture
DOI: 10.1016/j.entcom.2021.100476

Key findings used:
- consistent grid/standard measurements and planning are central to modular architecture for games;
- modular kits can reduce production cost and support flexible level design when designed systematically;
- modular architecture is a production system, not simply a collection of repeated meshes.

Used to reinforce the skill's emphasis on pre-production metrics, reusable kit logic and assembly testing.

## CG Cookie — Building Modular Game Assets — Kent Trammell

Source:
https://www.cgcookie.com/courses/building-modular-game-assets

Key practice used:
- modular production is a complete modeling/texturing/export workflow, including walls, corners, floors/ramps and UV/material consolidation rather than isolated mesh creation.

Used as supporting training evidence for treating corners, floors and interfaces as first-class kit pieces.

## Roblox Creator Hub — modular environments / pivot discipline

Sources:
https://create.roblox.com/docs/tutorials/use-case-tutorials/modeling/assemble-modular-environments
https://d2gbj0c64xar4a.cloudfront.net/docs/tutorials/curriculums/environmental-art/develop-polished-assets

Key practice used:
- consistent pivot locations are critical for predictable snapping and assembly;
- pivot position should be chosen for functional placement rather than visual tidiness.

The engine-specific units and exact workflow are not copied; the general pivot discipline is applicable to Blender-authored modular kits targeting any engine.
