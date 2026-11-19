# Blender roads & infrastructure — procedure, performance and validation

Detailed passes for [the skill](../SKILL.md). Moved verbatim from SKILL.md in 4.4.0.

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
