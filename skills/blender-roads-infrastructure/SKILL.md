---
name: blender-roads-infrastructure
description: Create or substantially revise roads, sidewalks, curbs, paths, crossings, junctions and other connected linear ground infrastructure in Blender: network layout, cross-sections, splines, terrain fit and longitudinal UVs. Buildings, street furniture, props and export keep their owners.
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
- hand-held/interior or narrative small objects to `blender-props`;
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

Work the passes in order; full instructions, performance/LOD guidance and the validation checklist are in [procedure](references/procedure.md) — read it before modeling and again before acceptance.

- **Pass 1 — centerlines, route hierarchy and scale** — Start with simple curves/lines or low-resolution strips.
- **Pass 2 — define a cross-section contract** — Before generating final geometry, define the cross-section for each road/path class.
- **Pass 3 — choose representation: modular, spline/procedural or hybrid** — Choose based on the network rather than fashion.
- **Pass 4 — curve/spline discipline in Blender** — When using Blender curves or Geometry Nodes:
- **Pass 5 — intersections and transitions as first-class assets** — Treat junctions as topology events, not incidental overlap.
- **Pass 6 — terrain fit, cuts and embankments** — Decide whether the road should:
- **Pass 7 — UVs, markings and longitudinal materials** — Roads are long surfaces, so material scale must remain stable along length.
- **Pass 8 — sidewalks, curbs, gutters and pedestrian transitions** — Treat curb/sidewalk systems as connected infrastructure rather than decoration.
- **Pass 9 — dirt roads, trails and irregular paths** — Not every route should look engineered.
- **Pass 10 — assembly and network stress test** — Test more than one straight segment.

**Performance and procedural guidance:** see the procedure reference.

**Validation:** see the procedure reference.
- **Network and layout** — every intended route endpoint/branch connects correctly;
- **Cross-section and geometry** — road/path, curb, gutter, sidewalk, shoulder/median relationships remain coherent;
- **Terrain integration** — road does not float or sink unintentionally;
- **Materials and markings** — longitudinal texture scale remains stable along routes;
- **Context and traversal QA** — Inspect the network from a plan/top view and at least one target-height ground view.

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
