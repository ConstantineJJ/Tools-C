# Research notes — vegetation

Research snapshot: 2026-10-03.

This file records external principles used to design `blender-vegetation`. Blender documentation is treated as software-behavior authority. Epic documentation and vegetation/environment-art breakdowns provide production evidence and target examples, not universal engine contracts. Exact species metrics, poly/texture/alpha/shadow/LOD/wind budgets and engine-specific vertex-data formats remain project-local.

## Blender Manual 4.5 LTS — Instance on Points

Source:
https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/instances/instance_on_points.html

Key points used:
- `Instance on Points` references source geometry instead of duplicating the underlying data;
- it can select among source instances and use point-domain attributes for per-instance selection/transform data;
- rotation and scale are instance-level controls rather than reasons to make every plant copy unique.

Applied to reusable leaves, branch clusters, grass patches and whole-plant variants.

## Blender Manual 4.5 LTS — Instances

Source:
https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/instances.html

Key points used:
- instances are references to geometry and are materially cheaper than duplicating unique geometry;
- nested instancing is supported and allows complex assemblies to remain built from a small set of unique meshes;
- geometry-processing nodes generally process unique source geometry rather than every apparent copy;
- realizing instances converts them into unique geometry and increases memory/processing cost.

Applied as the default preservation rule for repeated foliage/scatter until a concrete downstream operation requires uniqueness.

## Blender Manual 4.5 LTS — Realize Instances

Source:
https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/instances/realize_instances.html

Key points used:
- `Realize Instances` converts efficient references to real geometry;
- performance can become substantially worse for many complex instances;
- instance-domain attributes and vertex groups can propagate during realization.

Applied to a defined handoff gate: preserve source variants/attributes and realize only when export or an individual-geometry operation requires it.

## Blender Manual 4.5 LTS — Geometry to Instance

Source:
https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/geometry/geometry_to_instance.html

Key points used:
- separate generated geometries can be grouped as instances without actually joining them;
- this can be faster than building one large joined mesh and supports selection among generated variants.

Applied to procedural variant libraries where source plant/cluster geometry is generated inside the node tree.

## Epic Games — Pivot Painter Tool 1.0 / foliage hierarchy

Source:
https://dev.epicgames.com/documentation/unreal-engine/pivot-painter-tool-1.0-in-unreal-engine

Source type: engine/runtime pipeline documentation.

Key points used:
- one foliage-animation approach stores pivot and rotation information in vertex data;
- grass bends around roots, while tree branches/leaves can use hierarchical pivots and inherit parent motion;
- meaningful branch/leaf sub-object transforms are therefore production data, not merely editor convenience, when that pipeline is selected.

Applied as evidence for protecting roots, branch/cluster attachment pivots and source transforms before runtime wind handoff. The specific Unreal/Pivot Painter encoding is deliberately NOT made universal Tools_C policy.

## 80 Level — Breakdown: Crafting a Peaceful Stylized Nature Scene

Source:
https://80.lv/articles/breakdown-how-to-create-a-peaceful-fantasy-nature-environment

Source type: recent stylized vegetation/environment production breakdown.

Key practices used:
- real meadows contain several blade heights and other small plants, not one uniform grass type;
- the artist deliberately built a compact vocabulary of short/tall/tufted grass, leafy plants and moss;
- foliage/grass cards can gain extra geometry/bending so patches remain full from multiple angles;
- upward normals were important for that project's stylized grass/landscape blend.

Applied to structured patch diversity and multi-angle card QA. Upward normals are kept explicitly style-specific rather than promoted to a universal foliage rule.

## 80 Level — Creating Grasslands and Trees for a Nature Environment

Source:
https://80.lv/articles/how-to-create-grasslands-trees-and-mountains-for-a-nature-environment

Source type: recent environment-art breakdown.

Key practices used:
- individual leaf/billboard cards can be assembled into larger canopy silhouettes;
- normal treatment and wind logic can differ by foliage class/style;
- canopy shadow/detail choices may change between foreground, middle-ground and background assets.

Applied to the principle that vegetation representation/shading/LOD should follow projected size and role, not one setup for every plant.

## 80 Level — Technical Challenges of Game Environment Production

Source:
https://80.lv/articles/technical-challenges-of-game-environment-production

Source type: experienced game-environment production breakdown.

Key practices used:
- foliage readability depends on balancing sharp/dense detail with simplicity;
- branch-and-leaf textures/masks can be rendered and cut into reusable card clusters;
- grouped clusters make a tree manageable instead of treating every plane as an independent artistic unit;
- original location/rotation of individual cards had to be retained for a Pivot Painter/vertex-animation pipeline.

Applied to cluster-first organization, readability-over-density and the safeguard against flattening transforms before wind data is secured.

## 80 Level — Overgrown / vegetation modeling and texturing workflow

Source:
https://80.lv/articles/overgrown-vegetation-modeling-and-texturing-workflow

Source type: vegetation/environment breakdown.

Key practices used:
- multiple leaf variations can be baked into reusable cards/clusters;
- distant/lower-screen-percentage vegetation can use simpler representations than close hero foliage;
- asset preparation and variation should consider final screen contribution.

Applied to leaf variation atlases and LOD/readability decisions rather than fixed universal polygon targets.

## 80 Level — Stylized Diorama with Blender / foliage atlas workflow

Source:
https://80.lv/articles/creating-stylized-diorama-with-blender-substance-3d-ue5

Source type: stylized environment production breakdown.

Key practices used:
- cards can be cut from foliage atlases and duplicated/rotated to produce fuller plant silhouettes;
- vines and scattered foliage can use different generation/placement approaches inside one scene;
- normal/shading treatment can be specialized by foliage type.

Applied to hybrid vegetation representation and rejection of one universal card orientation/normal rule.

## 80 Level — Procedural Landscape Tools for Environment Design

Source:
https://80.lv/articles/procedural-landscape-tools-for-environment-design

Source type: environment/procedural-tool breakdown.

Key practices used:
- large vegetation and smaller bushes/grass can use different authoring pipelines;
- leaf cards and hand-modeled plants coexist with procedural scene tools;
- wind/material behavior is tied to asset class and target look rather than one generic setup.

Applied to separation between plant source assets and procedural scatter/delivery systems.

## Synthesis for Tools_C

The recurring durable pattern is:

1. Prove scale, trunk/stem, major branches and crown/patch silhouette before dense foliage.
2. Treat branch hierarchy, taper and cluster distribution as structured growth logic rather than independent random transforms.
3. Choose geometry, cards, baked clusters or hybrid from target screen size, depth/parallax, renderer and style.
4. Build reusable foliage/grass clusters with clear attachment pivots and multi-angle readability before mass placement.
5. Create a small vocabulary of strong plant/patch variants, then add bounded placement variation instead of cloning one source with noise.
6. Preserve instances as references; realize only for a defined downstream need and keep source/attribute identity recoverable.
7. Protect root/branch/leaf pivots, hierarchy and source transforms when the downstream wind method may encode or depend on them.
8. Treat upward/spherical normals, alpha-card density, two-sided shading and wind encoding as style/target decisions rather than universal laws.
9. Reduce distant vegetation by screen contribution while preserving silhouette, major negative spaces and species identity.
10. Keep terrain authoring, runtime wind/shader implementation and project-specific budgets outside this universal vegetation modeling skill.
