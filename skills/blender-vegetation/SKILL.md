---
name: blender-vegetation
description: Create or substantially revise trees, shrubs, bushes, grass, flowers, vines and plant clusters in Blender. Use when botanical/growth hierarchy, trunk and branch silhouette, leaf or blade representation, cards/atlases, foliage clustering, structured variation, instancing/scattering, wind-ready pivots/data, seasonal variants, vegetation LOD/readability or plant-specific QA are central; route terrain, roads, architecture, props, generic sculpt-only work and final export/runtime integration to their specialist owners.
---

# Blender vegetation

Read the required [foundation contract](../../docs/foundation.md) and the general [Blender pipeline](../blender-pipeline/SKILL.md). This skill owns plant-specific modeling, clustering, variation and wind-ready source structure, not terrain authoring or the runtime wind shader itself.

## Instruction priority

Follow the user's target, active project/profile, approved species/reference and art direction before generic botanical conventions. Real growth patterns are evidence for convincing structure; they are not authority to erase deliberate stylization, fantasy anatomy or low-poly simplification. Do not turn every plant into a procedural system, alpha-card asset or photoreal scan workflow when the target does not benefit.

## Scope and ownership

Own:
- trees, saplings, shrubs, bushes, grass, flowers, reeds, vines and plant clusters;
- trunk/root flare and branch hierarchy required to make the plant read;
- crown/canopy silhouette and branch/leaf density distribution;
- leaf, needle, blade and petal representation decisions: direct geometry, alpha cards/atlases, baked clusters, procedural instances or hybrid;
- foliage clusters, grass patches and reusable plant subassemblies;
- plant-family/species variation while preserving recognizable growth logic;
- vegetation-facing Geometry Nodes, linked data and instancing/scatter source design;
- wind-ready separation, branch/leaf pivots and source attributes when downstream deformation requires them;
- vegetation UV/atlas/material organization, normals strategy and seasonal/damage variants;
- vegetation-specific LOD/readability and structural QA.

Route:
- terrain sculpting, landscape grading and non-plant ground shape to the appropriate terrain/project workflow;
- roads, sidewalks and paths to `blender-roads-infrastructure`;
- buildings and architectural supports to `blender-architecture-environment`;
- planters, benches, pots and other non-plant environment fixtures to `blender-environment-assets` or `blender-props` by role;
- a primary generic sculpting task to `blender-sculpting`, while vegetation retains ownership of plant growth logic;
- generic rig implementation or animation Actions to rigging/animation owners when bones/Actions are explicitly required;
- final GLB delivery and target-engine wind/material validation to export/integration owners.

Boundary rule: classify by the **living plant system** being authored. A tree growing through a planter remains vegetation for the tree and environment-assets/props for the planter. A vine attached to a wall is vegetation; architecture owns the wall and provides attachment/reference surfaces.

## Preflight: define the plant before modeling

Establish the minimum useful vegetation brief:

1. **Plant type** — broadleaf tree, conifer, palm-like, shrub, grass, flower, vine, reed, dead plant, fantasy plant, etc.
2. **Reference authority** — exact species, regional family, concept art, stylized shape language or mixed references.
3. **Scale and age** — mature tree, sapling, trimmed shrub, young grass, oversized fantasy plant, etc.; use a human/player or measured anchor.
4. **Target view** — hero closeup, third-person gameplay, top-down, background forest, cinematic, VR, etc.
5. **Season/state** — healthy, dry, autumn, winter, dead, pruned, storm-damaged, overgrown, flowering/fruiting.
6. **Representation target** — direct mesh, low-poly stylized geometry, foliage cards/atlas, baked branch clusters, Geometry Nodes/instances, hybrid or project-defined system.
7. **Wind/runtime needs** — static, simple root-to-tip bend, branch hierarchy, interactive foliage, engine-specific pivot/vertex data or unknown/deferred.
8. **Reuse model** — one hero plant, species family, reusable branch clusters, patch variants, procedural scatter library, etc.
9. **MUST PRESERVE** — approved silhouette, species cues, scale, root/ground anchor, branch hierarchy, card/cluster pivots, UV/atlas regions, instance/shared-data relationships and unrelated scene state.

If species identity, scale, target camera or wind requirements materially change the representation, resolve them or record a provisional assumption before building dense foliage.

## Reference and growth strategy

Collect references by plant question:

- full silhouette from several angles and ages;
- trunk/root flare and major branch junctions;
- branch hierarchy, taper, droop/uplift and crown distribution;
- leaf/needle arrangement and cluster behavior rather than only isolated leaf shape;
- underside/backlit foliage for density and translucency cues;
- bark/stem/leaf materials separately;
- seasonal, damaged, dead or pruned examples when relevant;
- grouped plants/meadows/hedges for spacing and natural variation.

Study growth as hierarchy: root/base → trunk or primary stems → primary branches → secondary/tertiary branches → twigs/leaf clusters. Stylized plants may compress or exaggerate levels, but random sticks with leaves attached uniformly rarely produce a convincing silhouette.

Do not copy one photograph's accidental asymmetry as a universal species rule. Identify repeated growth tendencies across multiple references, then preserve deliberate concept-art departures.

## Workflow

Use the least complex representation that can satisfy silhouette, density, animation and target-camera needs.

### Pass 1 — scale, trunk/stem and crown silhouette

Block the plant with simple curves, cylinders or low-resolution branches. Establish:
- ground/root anchor;
- overall height and crown width;
- trunk or main-stem taper;
- primary branch directions and attachment heights;
- crown mass/negative spaces;
- dominant asymmetry and lean where intended.

Use a human/player proxy or another explicit scale anchor. Check from target camera height plus front/side/3/4 views. For trees, the crown silhouette and major branch rhythm must read before individual leaves exist.

Do not add bark chips, leaf cards, veins, flowers or grass blades while the primary plant silhouette is unstable.

### Pass 2 — branch hierarchy and taper

Build branch levels from structural importance outward.

For each level, decide:
- parent branch/stem;
- attachment direction and angle range;
- length/taper relative to the parent;
- curvature/droop/uplift;
- density and spacing;
- where branches terminate into leaf/needle clusters.

Avoid perfectly even radial spacing unless the species/style requires it. Variation should be structured, not white noise: repeated growth rules plus controlled exceptions usually read more naturally than independent random transforms.

Preserve readable junctions at target distance. Do not spend topology on invisible twig junctions if a baked/card cluster will replace them.

### Pass 3 — choose leaf/blade/petal representation

Choose by projected size, depth/parallax, alpha cost and style.

Use **direct geometry** when:
- leaves/blades are large enough to affect silhouette or close parallax;
- the style is low-poly/graphic and geometry itself is the visual language;
- target platform/material pipeline makes alpha cards undesirable.

Use **cards/atlases or baked clusters** when:
- many small leaves/needles/grass blades would be expensive as unique geometry;
- a branch/leaf cluster can be represented efficiently from target distances;
- alpha/opacity is supported and acceptable for the target.

Use **hybrid** when hero leaves/outer silhouette use geometry while dense interior foliage uses cards/clusters, or when close branches remain geometric but far crown density is card-based.

Do not choose cards merely because vegetation often uses them. At close range poor cards can reveal flat intersections, alpha overdraw and repeated silhouettes; at distance excessive geometry can waste performance without improving readability.

### Pass 4 — build reusable foliage clusters

Create a small set of representative leaf/needle/flower or grass clusters before filling the whole plant.

A cluster should have:
- a clear attachment/root point;
- silhouette that reads from the expected view range;
- enough internal depth/orientation variation to avoid one flat plane;
- controlled card intersections rather than coplanar z-fighting;
- consistent material/atlas usage;
- pivot/orientation data that supports placement and, if required, downstream wind.

When using cards, cut/shape the plane around useful opacity regions rather than retaining large empty transparent rectangles if the target benefits. Add limited bends/segments when that materially improves fullness from multiple angles.

Normal editing is style-dependent. Upward or spherical/cluster normals can help specific stylized grass/canopy looks, but do not make them a universal rule; compare against the approved shading target.

### Pass 5 — grass, shrubs and patch composition

For grass/meadow/shrub assets, avoid one identical tuft repeated everywhere.

Build a compact vocabulary such as:
- short/dense patch;
- taller sparse patch;
- tufted or directional patch;
- broadleaf/weed/flower accent;
- small/medium shrub cluster;
- edge/transition patch where needed.

The exact set depends on the biome/style. Real meadows often mix blade heights and plant types; use that observation to build controlled diversity rather than random color/scale noise.

Test each patch from several angles and in a small group. A patch that looks full in front view can disappear or become obviously card-like from the side.

### Pass 6 — variation without losing species identity

Create variation from meaningful axes:
- age/size class;
- trunk lean and primary branch distribution;
- crown width/density;
- missing/dead branches;
- leaf cluster density;
- seasonal color/state;
- flowering/fruiting state;
- controlled wind-rest pose differences where appropriate.

Keep stable species/family cues: characteristic trunk taper, branch tendency, leaf scale, crown architecture and material language. Randomly scaling every branch or rotating every cluster independently can destroy identity while still looking "varied."

Prefer a small set of strong source variants plus procedural placement variation over thousands of unique meshes.

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

## Performance and procedural guidance

- Keep high-count foliage/grass/forest elements instanced as long as practical.
- Use the minimum source-cluster complexity that preserves silhouette and density at target distance.
- Avoid evaluating heavy modifiers/procedural operations independently on thousands of realized copies.
- Separate source assets from scatter/delivery objects so the source remains editable.
- Alpha-card overdraw, shadow cost, texture memory, draw calls, Nanite/forward/deferred specifics, runtime wind and exact LOD budgets are target-project decisions.
- Avoid one giant joined vegetation mesh unless the target pipeline explicitly needs it; avoid thousands of unique objects when shared/instanced data is sufficient.

## Validation

Perform applicable checks and label unavailable evidence as SKIP.

### Growth and silhouette
- plant scale matches the declared anchor;
- trunk/stem, major branches and crown distribution follow the approved species/style;
- taper and branch hierarchy read coherently;
- major negative spaces and asymmetry survive target viewing distance;
- root/ground contact is deliberate.

### Foliage and clustering
- leaf/blade/card representation matches projected size and target style;
- clusters have usable attachment pivots and multi-angle fullness;
- no unintended coplanar card z-fighting or obvious flat-card gaps at required views;
- normals/shading strategy is intentional and consistent;
- repeated clusters remain shared/instanced where promised.

### Variation and instancing
- species variants differ through controlled structural dimensions rather than arbitrary noise;
- repeated plants do not expose identical high-information silhouettes everywhere;
- source meshes/collections remain recoverable;
- instances are not realized without a documented downstream need;
- scatter attributes/variant indices needed downstream are preserved.

### Wind-ready data
- ground/root and branch/cluster pivots remain on their intended attachment points;
- hierarchy required by the selected wind model is preserved;
- temporary bend/rotation tests pivot from the correct anchors where applicable;
- target-specific vertex/pivot data is handed off explicitly rather than assumed.

### Surface and context
- bark, leaves, grass and flowers maintain coherent scale/material identity;
- alpha-card density does not create unacceptable visual blackening/noise in representative clusters;
- context views show plausible ground contact and plant-to-plant scale;
- near/far representations preserve plant identity enough for the project target;
- visual acceptance requires inspected target views; mesh validation alone is not visual PASS.

## Safeguards

- Do not add dense leaves before trunk/branch/crown silhouette is proven.
- Do not treat biological randomness as independent random transforms; preserve growth hierarchy and species cues.
- Do not realize high-count instances without a concrete downstream need and recoverable sources.
- Do not join/flatten branch and leaf transforms before target wind/pivot data is secured when wind may depend on them.
- Do not force upward/spherical normals onto all vegetation; those are style-specific shading techniques.
- Do not model thousands of unique leaf cards, grass blades or perforated alpha planes when shared clusters/instances are sufficient.
- Do not infer terrain, biome, wind, texture, LOD, alpha, shadow or engine budgets from another project.
- Do not use noise, hue variation or random scale to compensate for weak plant silhouette/growth structure.
- Do not let the vegetation owner mutate roads, buildings, terrain or planters outside the authorized attachment/context scope.

## Pitfalls / Lessons Learned

### VEG-001 — Leaves before tree
- Symptom: thousands of leaves exist but the tree silhouette feels generic or wrong.
- Cause: foliage density was built before trunk, primary branches and crown masses were accepted.
- Rule: prove scale, trunk/branch hierarchy and crown silhouette first.
- Verification: simplified branch-only or cluster-proxy view still reads as the intended plant.

### VEG-002 — Randomness without growth logic
- Symptom: every branch angle differs, yet the plant feels procedural/noisy rather than natural.
- Cause: transforms were randomized independently without parent-child growth tendencies.
- Rule: vary within structured branch/taper/density rules and preserve species cues.
- Verification: multiple variants look related while remaining recognizably different.

### VEG-003 — Dense cards, poor readability
- Symptom: foliage becomes a dark alpha-heavy mass or card intersections dominate close views.
- Cause: density was increased instead of designing readable clusters and negative space.
- Rule: optimize cluster silhouette/orientation first; add density only when it improves the target read.
- Verification: near and target-distance views retain crown shape and internal separation without unnecessary card count.

### VEG-004 — Premature instance realization
- Symptom: a forest or crown becomes heavy to edit and global leaf/branch fixes require thousands of changes.
- Cause: linked/Geometry Nodes instances were realized before uniqueness was required.
- Rule: preserve source clusters/variants and instance transforms until a concrete handoff needs real geometry.
- Verification: editing the source updates intended repeats and performance remains appropriate.

### VEG-005 — Wind data destroyed by cleanup
- Symptom: grass bends around its center or branches/leaf clusters need corrective shader offsets after export.
- Cause: pivots, hierarchy or source transforms were flattened before wind data was authored.
- Rule: define wind deformation needs early enough to protect root/attachment pivots and required attributes.
- Verification: representative temporary rotations/bends occur around documented roots/attachments before handoff.

### VEG-006 — Shading trick used as universal rule
- Symptom: upward/spherical normals improve one stylized asset but make another species/realistic target look flat or incorrectly lit.
- Cause: a style-specific normal technique was copied without target comparison.
- Rule: choose foliage normals from approved shading style and validate several views/light directions.
- Verification: normal strategy improves the named target without erasing required volume/material cues.

### VEG-007 — Clone forest
- Symptom: repeated trees/grass patches expose the same silhouette, dead branch or leaf cluster pattern.
- Cause: only transform jitter was added to one source asset.
- Rule: provide a small set of structurally distinct variants and then apply bounded placement variation.
- Verification: a representative group has no dominant repeated high-information silhouette at the target view.

## Handoff

When passing to export, engine integration, runtime wind or another owner, report:
- plant/species/style and scale/age assumptions;
- trunk/branch hierarchy and root/ground convention;
- leaf/blade/card/cluster representation and source assets;
- shared/instance/procedural state and whether anything has been realized;
- foliage atlas/material/normal strategy;
- plant variants and what dimensions/states differ;
- wind model assumptions plus protected pivots/attributes/hierarchy;
- LOD/impostor state and unresolved target budgets;
- structural/context/visual evidence completed;
- open terrain/scatter/runtime-wind/export gates and known risks.

## Completion / stop

Complete when the requested plant or vegetation family exists with approved scale, growth hierarchy and silhouette, foliage representation fits the target, source variation/instancing is intentional, wind-required pivots/data are protected, context/structural checks pass, and unavailable visual/runtime/LOD gates are explicitly handed off.

Stop and report instead of guessing when species/reference conflict materially changes growth structure, target distance/renderer is necessary to choose cards versus geometry but unavailable, wind data requirements would be destroyed by the requested cleanup, or a requested edit crosses into terrain/architecture/road/export ownership outside scope.

## Research basis

The practical rules in this specialist are distilled from Blender 4.5 instancing/Geometry Nodes documentation, Epic's pivot-based foliage-animation documentation and vegetation/environment-art production breakdowns covering grass patch composition, foliage cards, cluster readability, plant variation and preservation of branch/leaf pivot data. See [research notes](references/research-notes.md) for source URLs, source type and caveats.
