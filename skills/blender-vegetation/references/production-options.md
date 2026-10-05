### Pass 7 — instancing and procedural scatter

Use shared mesh data, collection instances or Geometry Nodes instances for repeated foliage and plant placement when practical.

Blender instances store references to geometry instead of duplicating the underlying data. `Instance on Points` can carry point-domain attributes into the instance domain and select among source variants. Keep source leaves, branches, grass patches and whole-plant variants instanced while unique geometry is unnecessary.

Use scatter controls based on meaningful masks/attributes such as:
- density;
- slope or surface normal;
- height/biome zone;
- distance from roads/buildings;
- moisture or hand-authored masks when the project supplies them;
- variant index;
- controlled scale/rotation ranges.

Do not bury artistic control inside an opaque node graph. Expose the parameters that the project actually needs and preserve a recoverable source collection.

### Pass 8 — realize only at a defined handoff

`Realize Instances` converts efficient instance references into real geometry and can significantly increase memory/evaluation cost. Do it only when a concrete downstream operation needs per-instance geometry, export requires it, or an individual edit cannot be represented otherwise.

Before realization, record or preserve:
- source variant identity;
- placement transforms;
- per-instance attributes needed for wind/color/variation;
- original source collections/objects.

Do not realize an entire forest or dense crown merely to make the scene graph look simpler.

### Pass 9 — wind-ready hierarchy and pivot data

Vegetation modeling owns the source structure required for believable deformation; runtime wind implementation belongs to the target engine/shader owner.

When wind is required, identify which deformation model the target expects:
- simple root-to-tip grass bend;
- trunk plus branch hierarchy;
- branch plus leaf flutter;
- interactive bending;
- bone-based or shader/vertex-data method.

Preserve meaningful roots/pivots:
- grass blade/patch at ground/root;
- branch cluster at its parent attachment;
- leaf cluster at branch attachment;
- whole tree at ground/root anchor.

Some engine workflows encode branch/leaf pivot and hierarchy information into vertex data for shader animation. If that pipeline is possible, do not destroy original object/cluster transforms or merge everything before the required data is baked/exported. Do not hard-code one engine's Pivot Painter layout into this universal skill; treat it as target-specific handoff data.

### Pass 10 — UV, atlas and material organization

Choose a vegetation surface strategy by repetition and target renderer:
- bark/trunk tileable or trim-like materials where appropriate;
- leaf/needle/flower atlases for card-based foliage;
- unique textures for justified hero species/details;
- shared atlases/materials across a plant family where that reduces cost without obvious repetition;
- masks/vertex color/attributes for hue, seasonal or wind variation where the target supports them.

For alpha cards, provide enough texture margin and test mip-distance behavior in the target pipeline when possible. Avoid overly dense overlapping cards that create dark noisy masses or expensive transparency with little silhouette benefit.

Keep leaf front/back treatment consistent with the intended renderer. Two-sided shading, transmission/subsurface and alpha mode are target-material decisions; vegetation geometry should preserve the surfaces and normals needed for them.

### Pass 11 — LOD and distant readability

Vegetation LOD is primarily a silhouette/density problem.

Reduce in this order where appropriate:
- invisible twig/leaf microdetail;
- interior cluster density;
- card segments and small branch levels;
- high-frequency bark/leaf geometry;
while preserving:
- plant height/width;
- crown outline and major negative spaces;
- trunk/primary branch read where visible;
- species-defining leaf/cluster scale;
- wind/root anchors required by runtime.

Far representations may use simplified cluster cards, canopy cards, impostors/billboards or project-specific systems. Do not prescribe one LOD ratio or transition distance universally; screen size, biome density, hardware and renderer determine them.

### Pass 12 — seasonal/damage variants

Seasonal and damaged variants should reuse the proven growth structure where possible.

Examples:
- leaf color/density change without rebuilding branches;
- autumn/dead leaf cluster variants;
- bare/winter branch state;
- broken/pruned major branches;
- dry grass versus green grass;
- flowering/fruiting overlays or cluster swaps.

Do not fake all age/state differences through color if silhouette/density materially changes. Conversely, do not duplicate the entire plant geometry when a shared trunk plus alternate foliage clusters is sufficient.

### Pass 13 — context and stress test

Test more than one isolated beauty view.

For a reusable vegetation set, inspect:
- one plant alone at target camera distance;
- several variants together to expose clone repetition;
- dense placement to expose alpha/density/shading problems;
- side/back views for card disappearance;
- ground/root contact;
- representative wind pivot/hierarchy data if required;
- near and far representation or at least the planned LOD boundary.

A tree that looks convincing as one hero asset but collapses into a noisy repeated forest is not accepted as a reusable vegetation system.
