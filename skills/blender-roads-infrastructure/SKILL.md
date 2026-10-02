---
name: blender-roads-infrastructure
description: Create or substantially revise roads, sidewalks, curbs, gutters, paths, trails, medians, crossings, ramps, shoulders and other connected linear/network ground infrastructure in Blender. Use when network topology, centerlines/splines, cross-sections, junctions, terrain fit, repeated roadside structure, longitudinal UV/material flow or route continuity are central; route buildings, standalone street furniture, props, vehicles, vegetation, sculpt-only work and final export to their specialist owners.
---

# Blender roads & infrastructure

Read the required [foundation contract](../../docs/foundation.md) and the general [Blender pipeline](../blender-pipeline/SKILL.md). This skill owns connected ground/network infrastructure and its construction logic, not every object placed beside a road.

## Instruction priority

Follow the user's target, active project/profile, approved layout/reference and engine constraints before generic civil or real-world standards. Real infrastructure dimensions are reference evidence, not universal law. Do not silently replace a stylized road width, impossible city layout or game-driven traversal design with a real-world standard unless the task asks for realism.

## Scope and ownership

Own:
- roads, lanes, highways where applicable, service roads and alleys;
- sidewalks/pavements, curbs, gutters, medians, shoulders, ramps and crossings;
- trails, footpaths, dirt roads and other connected path systems;
- intersections/junctions, T-junctions, forks, merges, turnouts and transition pieces;
- linear retaining/edge strips when they are inseparable from the road/path system;
- centerline/network planning, spline/curve representation and road cross-sections;
- terrain-road interface, cut/fill/embedding decisions and seam management;
- longitudinal UV/material flow, lane/edge markings and road-surface variation strategy;
- road-facing modularity, repetition, instancing and procedural generation choices;
- placement anchors for infrastructure-owned repeating elements such as curb segments or road markings.

Route:
- building shells, entrances, drive-through architecture and facade modules to `blender-architecture-environment`;
- standalone lamps, benches, signs, bollards, hydrants, barriers and discrete fence/railing assets to `blender-environment-assets`;
- hand-held/interior or narrative small objects to `blender-props` when implemented;
- vehicles to `blender-vehicle-modeling`;
- vegetation to `blender-vegetation`;
- primary terrain sculpting or erosion to the appropriate terrain/sculpt workflow when that becomes the actual task;
- final GLB delivery and engine checks to export validation and target integration.

Boundary rule: **continuous network geometry belongs here; discrete reusable fixtures do not.** A curb run is infrastructure; a bollard beside it is an environment asset. A short fence panel asset belongs to environment-assets; a kilometer-long procedural fence corridor belongs here only if the task is the network/path system and the fence is generated as part of that corridor.

## Preflight: define the network before modeling

Establish the minimum useful infrastructure brief:

1. **Network role** — hero street, background road, gameplay route, sidewalk system, trail, parking/service lane, city block network, etc.
2. **Reference authority** — plan/map, concept art, survey/drawing, photo/video, real location, game layout or intentionally invented/stylized design.
3. **Users and traversal** — pedestrians, cars, bikes, heavy vehicles, creatures, camera rails or purely visual use.
4. **Scale anchors** — character/player, vehicle, lane/sidewalk width, doorway/curb, known map scale or another explicit metric.
5. **Network topology** — centerlines, branches, endpoints, intersections, one-way/visual hierarchy if relevant, and required connectivity.
6. **Cross-section** — carriageway/path width, curb/shoulder/gutter/sidewalk/median arrangement and vertical offsets where applicable.
7. **Terrain relationship** — floating on flat ground, projected to terrain, terrain cut/embankment, bridge/retaining handoff, or mixed.
8. **Representation** — direct mesh, modular pieces, curves/splines, Geometry Nodes, hybrid or project-defined tool.
9. **Surface strategy** — tileable road material, longitudinal UVs, trim/atlas, decals/markings, vertex/mask blending, unique hero sections or hybrid.
10. **MUST PRESERVE** — approved route/layout, junction locations, elevations/grades, road widths, named splines, UV scale, terrain, pivots/anchors, instances and unrelated scene data.

If route connectivity, width or elevation is ambiguous enough to change intersections or gameplay clearance, resolve it or record a provisional assumption before detail work.

## Reference and layout strategy

Collect references by system question:

- overhead/plan view for route topology and intersections;
- street-level perspective for width, curb height, slope and visual rhythm;
- cross-sections for road/sidewalk/curb/gutter relationships;
- junction and corner closeups for how widths transition;
- terrain-road examples for cuts, drainage, retaining edges and embankments;
- material references separately for asphalt, paving, dirt, gravel, markings and repairs;
- wear references for wheel paths, pedestrian zones, puddle/drainage areas, cracks and patching.

Do not infer hidden engineering layers that have no visible/gameplay effect. The skill is about believable and controllable visible infrastructure, not civil-engineering certification.

## Workflow

Use the least detailed representation that can answer the current network question.

### Pass 1 — centerlines, route hierarchy and scale

Start with simple curves/lines or low-resolution strips. Establish endpoints, intersections, route hierarchy, major bends, slopes and traversal width before curbs, markings or surface breakup.

Use a character/player and, where relevant, representative vehicle proxy. Inspect both plan/top view and ground-level target view. A network that reads well from above can still have implausible clearances or corner radii from gameplay height.

For stylized scenes, test perceptual width at the actual camera/FOV rather than blindly copying real dimensions.

Do not add cracks, lane markings, paving stones, drains or roadside clutter while the route itself is unstable.

### Pass 2 — define a cross-section contract

Before generating final geometry, define the cross-section for each road/path class. Record which elements are present and their relationship:
- road/path surface;
- curb or edge;
- gutter/drain strip if visible;
- sidewalk/pavement;
- median/shoulder/verge;
- vertical offset/camber/bank if required;
- attachment boundary to terrain or adjacent architecture.

A project may have several classes (main road, alley, footpath, dirt trail). Each class needs internal consistency, not universal real-world numbers.

Use shared profiles or parameterized source geometry when many routes use the same cross-section. Keep class differences deliberate instead of accumulating accidental width/height drift.

### Pass 3 — choose representation: modular, spline/procedural or hybrid

Choose based on the network rather than fashion.

**Modular pieces** fit:
- orthogonal/grid-like city blocks;
- repeated standard intersections;
- engine kits with fixed snapping;
- stylized or low-complexity layouts.

**Curves/splines or Geometry Nodes** fit:
- long continuous bends;
- terrain-following roads/trails;
- frequently edited routes;
- systems where width, markings or edge assets should follow a path.

**Hybrid** often fits production best:
- curves for long runs;
- explicit authored junction/intersection meshes;
- modular curbs/markings/edge pieces at controlled regions;
- unique hero transitions where procedural output fails.

Do not force every intersection through one procedural graph if a bounded explicit junction mesh is simpler and more reliable.

### Pass 4 — curve/spline discipline in Blender

When using Blender curves or Geometry Nodes:
- keep a recoverable centerline source;
- control curve tilt/normal/orientation so the road profile does not roll unexpectedly;
- use explicit profile geometry/cross-section when the road has curb/sidewalk/shoulder structure;
- use `Curve to Mesh` or equivalent only after the profile and centerline conventions are understood;
- resample where stable spacing is needed for downstream instances, markings or terrain interaction;
- retain length/tangent data when UVs or repeated elements depend on distance along the route;
- expose useful parameters such as width or profile selection rather than burying them inside opaque node graphs.

Blender's `Curve to Mesh` extrudes a profile along a curve, while `Resample Curve` can create approximately uniform point spacing. `Sample Curve` can provide position/tangent/normal information along length. Use those capabilities deliberately; they do not solve intersection topology automatically.

At sharp bends, inspect profile distortion and inside/outside edge behavior. A mathematically generated strip can self-intersect or create extreme miter-like stretching on tight corners. Tight-radius regions may need width reduction, additional authored topology or a unique transition.

### Pass 5 — intersections and transitions as first-class assets

Treat junctions as topology events, not incidental overlap.

For each required intersection type, verify:
- all incoming widths/classes match their connection boundaries;
- road surface and curb/sidewalk elevations connect continuously;
- turning/visual flow is coherent for the intended traversal;
- UV/material direction does not create obvious tearing or impossible rotation;
- no coplanar overlapping road strips remain under the junction;
- markings and curb cuts/ramps have a clear owner;
- terrain seams around the intersection are controllable.

Prefer a small library of proven intersection types over dozens of nearly identical bespoke pieces when the layout allows it. Keep unique intersections unique when the design genuinely demands them.

### Pass 6 — terrain fit, cuts and embankments

Decide whether the road should:
- conform to an existing terrain;
- cut into terrain;
- raise/embank above terrain;
- flatten a corridor;
- transition between those behaviors.

Do not merely shrinkwrap/project a finished road and accept all distortion. Check width, cross-section, banking and texture scale after terrain fitting.

When cutting roads into steep terrain, preserve controllable topology near road edges so the road/terrain seam can be textured and refined rather than becoming an uneditable boolean scar. Production tutorials also show value in maintaining road-adjacent edge flow specifically to make later texturing/refinement easier.

Avoid hidden terrain directly z-fighting with the road. Either define a clean separation/offset, remove/reshape underlying terrain where appropriate, or use a project-approved blending solution.

### Pass 7 — UVs, markings and longitudinal materials

Roads are long surfaces, so material scale must remain stable along length.

Useful strategies include:
- UV distance based on path length for asphalt/paving textures;
- cross-section coordinates for left/right placement;
- tileable materials for broad surfaces;
- trim/atlas regions for curbs, gutters and edges;
- decals or separate geometry for lane markings, arrows, cracks and repairs;
- masks/vertex data for dirt, wetness, patching or edge variation.

For procedural roads, preserve or construct a predictable longitudinal coordinate before converting/realizing geometry if downstream UVs depend on it. Procedural-road tutorials often store/capture attributes along the curve specifically to keep UVs aligned and texture scale consistent.

Do not stretch a single unique texture over an arbitrarily long road. Do not put high-recognition cracks or patches into the base tile if they will repeat every few meters.

### Pass 8 — sidewalks, curbs, gutters and pedestrian transitions

Treat curb/sidewalk systems as connected infrastructure rather than decoration.

Check:
- consistent curb top/bottom relationship along runs;
- corners that do not collapse or grow huge wedges;
- sidewalk width continuity through bends;
- curb cuts/ramps/crossings where required by the design;
- stairs/steep transitions handed off or authored explicitly instead of stretching a flat sidewalk through impossible grade changes;
- clean interfaces with building entrances and plazas.

Standalone benches, lamps, bins, bollards and signs remain environment-assets even when they snap to infrastructure anchors.

### Pass 9 — dirt roads, trails and irregular paths

Not every route should look engineered.

For dirt/gravel/trails:
- preserve the route and traversal width, but allow controlled irregularity at edges;
- vary surface height/edge breakup without destroying walkability or spline continuity;
- use material/displacement/scatter for fine irregularity before adding dense geometry everywhere;
- keep major wheel ruts, drainage channels or erosion features aligned with plausible use/terrain flow;
- avoid uniform noise that makes every meter equally damaged.

If a trail is generated from curves, distinguish route-level variation from high-frequency surface noise. The centerline should remain editable after adding local breakup where practical.

### Pass 10 — assembly and network stress test

Test more than one straight segment.

A representative QA network should include, where relevant:
- straight run;
- curved run;
- elevation/grade change;
- one intersection or branch;
- curb/sidewalk transition;
- terrain seam;
- repeated marking or edge asset.

Verify connectivity from start to end and inspect seams from both top and ground-level views. A road system that works only as isolated pieces is not accepted as network infrastructure.

## Performance and procedural guidance

- Keep high-count repeated roadside elements instanced until unique geometry is required.
- Resample curves only as densely as downstream placement/deformation needs; excessive point density increases evaluation cost without improving visible quality.
- Avoid realizing every procedural instance merely to make export feel simpler; realize only at a defined handoff if required.
- Separate route source data from final delivery meshes when continued editing matters.
- For very large networks, split at meaningful streaming/culling/editing boundaries rather than one enormous mesh or thousands of tiny fragments by habit.
- Polygon, draw-call, material-slot, collision and LOD budgets remain project-specific.

## Validation

Perform applicable checks and label unavailable evidence as SKIP.

### Network and layout
- every intended route endpoint/branch connects correctly;
- widths/classes stay consistent where promised;
- intersections have no gaps, accidental overlaps or disconnected curbs/sidewalks;
- route hierarchy and major bends match the approved plan/reference;
- slopes/grades are acceptable for the intended traversal and style.

### Cross-section and geometry
- road/path, curb, gutter, sidewalk, shoulder/median relationships remain coherent;
- profile does not roll/twist unexpectedly along curves;
- tight bends do not self-intersect or produce extreme stretched wedges;
- curbs/sidewalks preserve believable thickness and elevation;
- mesh normals/face orientation are correct on visible surfaces;
- no unintended coplanar road/terrain overlap causes z-fighting.

### Terrain integration
- road does not float or sink unintentionally;
- terrain cuts/embankments transition deliberately;
- width/cross-section remains stable after terrain fitting;
- road-edge topology/material blend is controllable at representative steep/curved sections.

### Materials and markings
- longitudinal texture scale remains stable along routes;
- UV/material direction behaves through curves/intersections;
- lane/edge/crosswalk markings follow the intended network and do not drift off surface;
- repeated cracks/patches/decals do not create obvious periodic artifacts unless intentional.

### Context and traversal QA
Inspect the network from a plan/top view and at least one target-height ground view. Use the actual character/vehicle scale anchor when available. For gameplay paths, traverse or simulate the relevant clearance rather than approving from aerial view alone.

## Safeguards

- Do not destroy the editable centerline/network source before final geometry is proven.
- Do not apply destructive boolean/realize/join operations across the whole network without a recoverable source and concrete need.
- Do not change road-class width, curb height or route elevation globally to fix one local junction unless the whole class is intentionally being revised.
- Do not treat procedural output as correct merely because it evaluates without errors; inspect intersections, tight bends and terrain seams.
- Do not random-scale infrastructure modules when that breaks width, height, snap or traversal continuity.
- Do not infer real-world lane/curb/sidewalk standards as universal project rules.
- Do not merge standalone environment fixtures into the road owner just because they are placed beside roads.
- Do not accept lower-level import/mesh success as visual or traversal acceptance.

## Pitfalls / Lessons Learned

### ROAD-001 — Detail before network
- Symptom: beautiful asphalt, drains and markings exist but the route proportions/intersections are wrong.
- Cause: surface work began before centerlines, widths and topology were proven.
- Rule: approve route and cross-section first; delay surface detail.
- Verification: simplified untextured network still reads and connects correctly in plan and ground views.

### ROAD-002 — Procedural intersection pile-up
- Symptom: generated road strips overlap, z-fight or create unusable wedges at junctions.
- Cause: independent curve extrusion was allowed to intersect without junction ownership.
- Rule: treat intersections as explicit topology events; author/solve them separately when necessary.
- Verification: representative T/cross/fork junction has one coherent surface and continuous edges.

### ROAD-003 — Curve roll / profile twist
- Symptom: curbs or road cross-section rotate unpredictably along 3D curves.
- Cause: curve normals/tilt/orientation were not controlled.
- Rule: establish orientation convention and inspect profile axes on elevation changes/bends.
- Verification: cross-section remains upright/banked only where intentionally specified.

### ROAD-004 — Texture stretching by distance drift
- Symptom: asphalt or markings visibly stretch/compress as curve density or length changes.
- Cause: UVs were tied to control-point topology instead of stable distance along the route.
- Rule: derive longitudinal mapping from route length/distance or another stable metric where possible.
- Verification: equal real/world route lengths show comparable texture scale across straight and curved sections.

### ROAD-005 — Terrain projection destroys width
- Symptom: road narrows/widens or kinks after being projected onto uneven terrain.
- Cause: finished geometry was deformed blindly onto terrain.
- Rule: validate cross-section after terrain fitting; use centerline/profile-aware methods or local authored transitions.
- Verification: representative slope retains declared usable width and clean edge relationship.

### ROAD-006 — Curb/sidewalk ownership drift
- Symptom: curb runs, sidewalk corners and nearby fixtures are authored by different rules and no longer meet.
- Cause: boundaries between network infrastructure and discrete environment assets were not explicit.
- Rule: roads owner keeps continuous curb/sidewalk network; environment-assets owns standalone placed fixtures.
- Verification: road/sidewalk geometry is continuous while fixtures remain independently reusable.

### ROAD-007 — Excessive procedural density
- Symptom: a simple road becomes slow to edit because curves are oversampled and every repeated element is realized.
- Cause: generation resolution was chosen without downstream need.
- Rule: use the minimum point/segment/instance density that preserves visible geometry and placement accuracy.
- Verification: lowering hidden procedural density causes no material visual/network regression at target view.

## Handoff

When passing to environment-assets, architecture, export or engine integration, report:
- network role and approved route/layout;
- road/path classes and key cross-sections;
- centerline/spline sources and whether final meshes are generated or realized;
- junction/intersection ownership and any unique transition pieces;
- terrain-fit method and unresolved seam/grade risks;
- UV/material/marking strategy and distance/scale assumptions;
- continuous infrastructure boundaries such as curb/sidewalk anchors;
- placement anchors offered to standalone fixtures;
- protected route/width/elevation invariants;
- structural/visual/traversal evidence completed and open gates.

## Completion / stop

Complete when the requested road/path/infrastructure network exists, route connectivity and cross-sections are coherent, intersections and terrain transitions are controlled, longitudinal material scale is stable enough for the target, protected data survived, and applicable structural/context checks have passed or are explicitly handed off.

Stop and report instead of guessing when route topology or scale is too ambiguous to determine connectivity, terrain constraints materially conflict with the approved path, a required intersection cannot be solved without changing protected layout, or target-engine traversal/collision rules are necessary but unavailable.

## Research basis

The practical rules in this specialist are distilled from Blender curve/Geometry Nodes documentation and road/environment production guidance covering curve-to-mesh workflows, resampling, tangents/normals, procedural UVs, road/terrain cutting, blockout, tileable materials and network validation. See [research notes](references/research-notes.md) for source URLs, source type and caveats.
