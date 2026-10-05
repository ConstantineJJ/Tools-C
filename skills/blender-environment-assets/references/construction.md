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
