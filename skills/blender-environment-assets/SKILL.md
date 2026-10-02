---
name: blender-environment-assets
description: Create or substantially revise standalone environment fixtures and repeatable site/street assets in Blender: benches, lamps, fences/railings, barriers, bins, bollards, hydrants, posts and similar objects. Use when environmental placement, family consistency, mounting/ground contact, reuse, repeated-instance strategy, outdoor material logic or fixture-specific construction are central; route building-integrated modules, continuous roads/curbs, portable/interior props, vehicles, vegetation, electronics/products, sculpt-only work and final export to their specialist owners.
---

# Blender environment assets

Read the required [foundation contract](../../docs/foundation.md) and the general [Blender pipeline](../blender-pipeline/SKILL.md). This skill owns discrete reusable environment fixtures, not the whole environment scene.

## Instruction priority

Follow the user's request, active project/profile, approved references and target-engine constraints before generic environment-art conventions. Real-world construction is evidence for believable proportions, attachment and wear; it is not authority to erase deliberate stylization. Do not turn every object into a modular kit, high-poly bake or unique texture merely because those workflows are common.

## Scope and ownership

Own:
- benches, street lamps, posts, signs, bins, bollards, hydrants, barriers, standalone railings and fence panels, planters, bike racks and similar site/street fixtures;
- reusable outdoor/service fixtures whose identity depends on how they are mounted, repeated or placed in an environment;
- blockout, proportion, silhouette and construction logic for those assets;
- family/variant planning for repeated fixture sets;
- placement-facing pivots, ground/attachment contact and repeated-instance strategy;
- asset-facing hard-surface decisions, bevel/shading strategy, material segmentation and UV/texture strategy;
- environment-specific wear and variation decisions;
- bounded LOD/readability preparation when explicitly part of the asset task.

Route:
- integral windows, doors, facade trims and building modules to `blender-architecture-environment`;
- continuous roads, curbs, sidewalks, gutters, paths, medians and network geometry to `blender-roads-infrastructure` when implemented;
- furniture, containers, tools, handheld/interior clutter and narrative small objects to `blender-props` when implemented;
- vehicles to `blender-vehicle-modeling`;
- appliances/electronics to `blender-product-electronics-modeling`;
- vegetation to `blender-vegetation`;
- primary sculpting/damage sculpt to `blender-sculpting` when available, otherwise the current sculpting route;
- final GLB delivery to export validation and target-engine integration.

Boundary rule: classify by production role, not size alone. A freestanding public bench belongs here; a movable dining chair usually belongs to props. A discrete fence panel/gate can belong here; a kilometer-long fence network or spline-managed corridor belongs to the infrastructure owner.

## Preflight: define the asset before touching geometry

Establish the minimum useful brief:

1. **Asset role** — hero fixture, repeated background asset, family member, kit component, close interactive object or distant dressing.
2. **Placement context** — street, park, industrial yard, interior-adjacent exterior, rooftop, rural site, etc.
3. **Scale anchors** — human/player height, curb/road width, hand height, seat height, doorway or measured reference.
4. **Reference authority** — exact product/reference, regional design language, concept art, photo set, or intentionally invented object.
5. **Construction logic** — primary structural parts, fasteners/joints, thicknesses, mounting, moving parts if any, likely materials and weather exposure.
6. **Reuse model** — one-off, repeated identical object, repeated object with cosmetic variants, interchangeable family or modular sequence.
7. **Surface strategy** — unique texture, shared atlas, trim/tileable, material library, decal/mask or hybrid.
8. **Production target** — realtime game asset, prototype, cinematic, marketplace pack, etc.
9. **MUST PRESERVE** — approved silhouette, dimensions, pivots, mount points, UVs, materials, linked data/instances, names and unrelated scene state.

If reference ambiguity would change human interaction, ground contact, attachment or silhouette materially, resolve it or document a provisional assumption before detail work.

## Reference strategy

Gather references by question rather than only by appearance:

- front/side/3/4 views for proportion and silhouette;
- human-scale context for height and reach;
- underside/back views for mounting, bases, brackets and hidden structural logic;
- closeups for hinges, welds, bolts, seams, drainage, lenses, grilles or fasteners;
- material references for paint, galvanized metal, cast iron, wood, plastic, glass, rubber and concrete;
- weathering references appropriate to placement: ground splash, sun, water runoff, contact abrasion, corrosion, repainting, dirt collection;
- family references when multiple fixtures must share a design language.

Do not invent random mechanical seams, bolts or damage where the construction would not support them. Believable secondary detail follows assembly and material logic.

## Workflow

Use the least detailed representation that answers the current production question.

### Pass 1 — blockout, scale and silhouette

Build the complete asset from simple volumes. Establish overall height/width/depth, support spacing, major negative spaces, contact points and dominant silhouette. Place a human/player proxy or another explicit scale reference when use is human-facing.

Judge from the target gameplay/viewing distance as well as a close inspection view. For repeated fixtures, test several copies early; a shape that looks fine alone can create excessive visual noise when repeated.

Do not add bolts, weld beads, panel seams, decorative cutouts or edge damage while proportions and mounting are unsettled.

### Pass 2 — prove function and construction

Before polishing, identify what physically supports or connects each major part:
- what reaches the ground or mounting surface;
- where loads would transfer through legs/posts/brackets;
- which pieces are cast, bent, welded, extruded, bolted, molded or assembled;
- which parts should be separate objects for motion, replacement, material or production reasons;
- whether thickness and gaps are visible at the target distance.

For an interactive or functional fixture, test the required clearance: sitting, walking around it, passing through a gate, reading a sign, approaching a bin, etc. Do not model hidden engineering detail that has no visible or gameplay consequence.

### Pass 3 — decide asset family and reuse strategy

When the object belongs to a family, define shared design invariants before variants:
- common post/leg/profile dimensions;
- repeated material palette and bevel language;
- shared mounting height or base dimensions where applicable;
- repeated fastener family;
- compatible attachment points;
- common pivot/origin convention;
- what is allowed to vary: length, top shape, arm count, panel infill, color, sign face, damage state, etc.

Build and approve one representative member first. Then derive variants from shared data or source modules where practical. A family should feel related without forcing every member to be a scaled copy.

For repeated identical geometry, prefer linked mesh data or collection instances where independent geometry is unnecessary. Make data unique only when the variant requires a real geometric difference.

### Pass 4 — hard-surface construction and edge language

Choose the simplest modeling approach that preserves silhouette, construction and editability:
- direct polygon modeling for simple welded/cast/extruded forms;
- Mirror for meaningful symmetry;
- Array for repeated slats, bars, bolts or prototype repetitions;
- Boolean for controlled openings/cutouts when it remains stable and editable;
- Solidify for sheet/panel thickness when its behavior fits the shape;
- Bevel for real geometric edge width and readable highlights;
- linked duplicates/instances for repeated components;
- Geometry Nodes when procedural repetition or variation materially improves the workflow.

Modifiers are tools, not quality badges. Preserve source editability until the object is proven. Before dimension-sensitive bevel/solidify/array work, inspect transforms; non-unit or negative scale can change results and exported behavior.

Edge treatment should reflect scale and material. Razor-sharp manufactured edges often shade unnaturally, but an oversized bevel can make a small metal fixture look soft or toy-like. Judge bevel width at target scale and camera distance. Weighted/custom normals can improve flat-face shading after bevels, but they do not repair bad geometry or replace a correct silhouette.

### Pass 5 — topology, shading and visible complexity

Spend geometry where it changes:
- silhouette;
- specular highlight shape;
- curvature;
- openings and depth;
- contact/mounting readability;
- moving or separable pieces;
- close-range shadow/parallax.

Keep broad hidden/planar regions simple when no downstream requirement justifies extra topology. All-quads are not a universal acceptance criterion for static realtime fixtures; stable shading, editing needs, baking and target use are more important.

Check for:
- accidental coplanar overlaps and z-fighting;
- internal duplicate faces from booleans/duplication;
- floating fasteners or brackets;
- inconsistent panel thickness;
- broken face orientation/normals;
- shading pinches near bevels, booleans or non-planar faces;
- parts that visually intersect without a believable joint.

### Pass 6 — surface and UV strategy

Choose texture allocation by reuse, size and camera needs:

- **shared/tileable materials** for generic painted metal, wood, concrete, rubber or other reusable surfaces;
- **trim/atlas/shared sheet** for families that repeat edge profiles, bands, labels, hardware or material zones;
- **unique texture** where a small/medium hero fixture needs distinctive wear, graphics or baked high-frequency detail;
- **hybrid** for a reusable material base plus local labels, decals, dirt masks or unique accents.

Use project-defined texel-density targets; do not invent a universal px/m value. Maintain coherent density across assets intended to coexist, with deliberate exceptions only for readability/hero needs.

Plan mirroring/stacking before adding unique asymmetrical wear. If UVs share or mirror regions, keep strongly recognizable damage/labels away from those shared areas unless repetition is intentional.

### Pass 7 — weathering and storytelling without noise

Wear follows material, exposure and use:
- ground-facing regions collect splash/dirt differently from upper surfaces;
- water runoff follows gravity and drainage paths;
- hand/contact zones polish or abrade differently from protected recesses;
- painted metal chips differently from plastic, galvanized steel, wood or cast concrete;
- bolts, welds and seams can trap dirt or corrosion, but not every edge needs equal wear.

Use a hierarchy: large material breakup first, medium use/environment effects second, small scratches/chips last. Avoid uniform procedural grunge over the entire asset; it destroys material identity and makes repeated props visibly identical.

For families, vary high-recognition storytelling layers while keeping shared construction/material logic. Color, decal, dirt and damage variants are often cheaper and safer than arbitrary geometry changes.

### Pass 8 — pivot, packaging and placement test

Choose pivot/origin by how the asset will actually be placed:
- freestanding object: usually a stable base point such as bottom-center or a documented corner/anchor;
- post/fixture: base center or installation anchor;
- wall-mounted object: mounting point/plane;
- fence/railing panel: deterministic endpoint/corner anchor if the panel must chain;
- hinged/moving part: its real articulation point for the moving component, not necessarily the asset root.

The exact convention is project-specific; consistency inside an asset family is the invariant.

Test at least one realistic placement context. For repeated assets, place several instances with the intended spacing/orientation and confirm that:
- scale reads correctly next to the environment;
- bases contact the ground/mount surface without sinking or floating;
- pivots support deterministic placement;
- repeated silhouettes do not create unintended visual rhythm/noise;
- intended shared data remains shared;
- variants remain compatible with the family placement logic.

Where an asset is intended for a reusable library, package meaningful dependencies together and preserve clear asset-level hierarchy. Blender's Asset Browser supports linked/appended assets and collection instances; choose a reuse method consistent with whether downstream edits should propagate.

## Performance and LOD guidance

Optimization follows expected screen size, repetition count and target engine, not a universal triangle number.

- Repeated identical fixtures benefit from shared mesh/material data and instancing.
- Remove geometry first where its loss is least visible at the target distance: hidden loops, small bevel segments, tiny fasteners, subtle backside details.
- Preserve silhouette and large negative spaces longer than small surface detail.
- Generate LODs from a proven highest required realtime mesh rather than from an unstable blockout.
- Verify that UVs/material IDs/normals survive simplification where those properties matter.
- Collision, LOD naming, streaming and draw-call budgets belong to the project/engine profile or export owner unless explicitly requested here.

## Validation

Perform applicable checks and label unavailable evidence as SKIP.

### Form and scale
- silhouette reads at target distance and close enough for intended use;
- overall dimensions are coherent with declared scale anchors;
- human-facing heights/clearances are plausible for the project intent;
- major negative spaces and support spacing match reference/design;
- ground/mount contact is deliberate and stable.

### Construction
- visible parts have believable attachment/support logic;
- thickness, gaps, fasteners and seams are intentional;
- moving/separable parts are split appropriately for downstream needs;
- no floating or impossible joints are introduced merely for visual detail.

### Family and reuse
- family members share intended proportions/material/edge language;
- interchangeable or repeating pieces preserve promised dimensions/anchors;
- identical repeated components still share data/instances where intended;
- variants differ deliberately rather than through accidental scale/pivot drift.

### Mesh and shading
- no unintended duplicate/internal/coplanar geometry;
- face orientation and visible normals are correct;
- bevels produce stable highlights at target scale;
- broad faces remain visually flat where intended;
- modifier behavior is not accidentally dependent on unapplied/negative scale;
- complexity is concentrated in silhouette/readability rather than hidden areas.

### Surface consistency
- texel density follows the project target;
- shared materials/trim/atlas usage is coherent across the family;
- mirroring/stacking does not duplicate obvious unique wear unintentionally;
- weathering follows material/exposure/use logic instead of uniform noise.

### Placement and visual QA
Inspect the asset in at least one environment-context view. For repeated fixtures, inspect multiple placed copies. A clean isolated turntable is not enough to prove environmental scale, repetition quality or ground contact.

## Safeguards

- Do not destroy an approved blockout/source before final geometry and placement are proven.
- Do not apply destructive booleans, joins, remeshes or instance realization without a concrete downstream need and recoverable source.
- Do not make linked/shared mesh data unique accidentally when the task depends on propagated edits.
- Do not random-scale structural family members just to hide repetition if that breaks height, clearance, contact or design language.
- Do not bake arbitrary project-specific texel density, LOD ratios, collision rules or triangle budgets into this universal skill.
- Do not add high-frequency bolts/scratches/damage to compensate for weak scale, silhouette or construction logic.
- Do not delete back/underside geometry solely as an optimization if target cameras, shadows, collision, destruction or placement can expose it.
- Do not turn a discrete fixture task into roads, buildings, props or scene dressing outside the authorized scope.

## Pitfalls / Lessons Learned

### ENVA-001 — Isolated-model scale drift
- Symptom: the asset looks convincing alone but oversized/undersized in the actual environment.
- Cause: modeling without a human/environment scale anchor or target camera context.
- Rule: prove dimensions and environmental context during blockout, not after texturing.
- Verification: context placement beside the declared scale anchor reads correctly without compensating scene scale.

### ENVA-002 — Detail before construction
- Symptom: bolts, welds and scratches look rich but brackets/supports make no physical sense.
- Cause: secondary detail was invented before assembly and load paths were understood.
- Rule: identify support, attachment and material logic before micro-detail.
- Verification: simplified material view still explains how the object is built and mounted.

### ENVA-003 — Variant by accidental scale
- Symptom: a family appears varied but seat heights, post widths or mounting points drift.
- Cause: object-level scaling was used instead of controlled compatible variants.
- Rule: vary named dimensions/material/story layers deliberately; preserve family anchors and interaction metrics.
- Verification: repeated/family placement needs no per-instance corrective transforms.

### ENVA-004 — Unique texture for every repeated fixture
- Symptom: texture memory and authoring effort grow linearly with a street full of related assets.
- Cause: reuse/material strategy was decided after modeling.
- Rule: evaluate shared materials, trims, atlases and hybrid decals before committing unique textures.
- Verification: related assets reuse resources where appropriate without losing required readability.

### ENVA-005 — Procedural grunge everywhere
- Symptom: every edge is equally chipped/dirty and materials become indistinguishable.
- Cause: weathering was generated from masks without exposure/use reasoning.
- Rule: drive wear from material, orientation, contact and environment; reserve high-information damage for plausible zones.
- Verification: removing color still leaves physically understandable wear placement rather than uniform noise.

### ENVA-006 — Broken reuse through premature uniqueness
- Symptom: repeated lamps/posts no longer update together and small fixes require editing many copies.
- Cause: linked data or instances were made unique/real before uniqueness was required.
- Rule: preserve shared sources until a concrete geometric variant demands divergence.
- Verification: editing the approved source updates intended repeats and variants remain intentionally separate.

## Handoff

When passing to another specialist, export or engine integration, report:
- asset role and placement context;
- scale anchors and key dimensions;
- construction/material assumptions;
- family/variant/reuse strategy;
- pivot/mount/attachment convention;
- linked/instance state and modifiers that must remain intact;
- UV/material/texel-density strategy;
- protected silhouette and functional clearances;
- LOD/collision/export gates still owned elsewhere;
- structural and visual evidence completed;
- known risks or assumptions.

## Completion / stop

Complete when the requested environment fixture or family exists, scale and silhouette are proven in context, visible construction and mounting are coherent, reuse/variant strategy fits the intended repetition, pivots and shared data behave as declared, protected data survived, and applicable structural/visual checks have passed or are explicitly handed off.

Stop and report instead of guessing when the asset's role/scale/reference is too ambiguous to determine interaction or mounting, a required family rule conflicts with approved variants, target-engine constraints are necessary but unavailable, or a requested change would invalidate protected pivots/UVs/instances outside scope.

## Research basis

The practical rules in this specialist are distilled from Blender documentation and environment/prop production breakdowns covering blockout, modular/repeated assets, Asset Browser reuse, bevel/normals, texel-density planning, trim/shared texture strategies, LOD thinking and environment-specific wear. See [research notes](references/research-notes.md) for source URLs, scope and caveats.
