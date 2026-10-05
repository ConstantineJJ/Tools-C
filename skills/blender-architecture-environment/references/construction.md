## Workflow

Use the least detailed representation that can answer the current architectural question.

### Pass 1 — massing and scale

Block the complete structure or representative slice with simple volumes. Establish footprint, height, roof volume, major negative spaces, entrances, windows, stairs/platforms and dominant silhouette.

Use a human/player proxy or another explicit scale anchor. Check the model from target camera height and from at least one orthographic-ish view. For walkable spaces, verify practical clearance before detail. For stylized work, compare both absolute scale and perceptual scale.

Do not add trim, bricks, bolts, window mullions or damage while the building's proportions are unsettled.

### Pass 2 — prove the building before decomposing it

When practical, make the blockout read as the intended whole building first. Then identify repeated spans and boundaries. This avoids designing modules in isolation that technically snap but assemble into a weak structure.

Mark each region as one of:
- **reusable module** — repeated and useful across layouts;
- **variant module** — same metric footprint with different visible design;
- **unique/hero piece** — focal or geometry-specific element with low reuse;
- **surface-only variation** — same mesh, varied by material, decal, mask or dressing;
- **handoff asset** — belongs to another specialist.

Favor the smallest kit that covers the required layouts. More pieces are not automatically more flexible: low-reuse fragments add assembly cost and failure points.

### Pass 3 — lock the modular system

Before detailed modeling, define:
- grid/increment and allowed subdivisions;
- standard horizontal spans and story/vertical increments;
- orientation convention;
- pivot/origin convention by module type;
- whether thickness is centered, inward or outward from the grid line;
- corner/intersection convention;
- naming sufficient to identify size/type/variant where the project uses such naming.

Typical functional pivot logic:
- wall modules: bottom corner or another project-consistent edge anchor on the snap plane;
- corners: the actual architectural intersection point;
- floors/ceilings: a consistent footprint corner or other engine/project convention;
- trims: an edge/end anchor that supports deterministic placement;
- free-standing modules: bottom-center or a documented attachment point when that is more useful.

The exact convention may vary, but pieces of the same family must behave predictably.

Build a minimal proof kit first — usually one straight section, one corner, one opening-bearing module and any required floor/roof interface. Assemble them repeatedly before authoring dozens of pieces.

### Pass 4 — construct final modules non-destructively where useful

For repeated architectural geometry, prefer editable source geometry plus appropriate modifiers/instances while the design is still changing.

Useful Blender patterns include:
- Mirror for symmetric facade/roof or structural elements;
- Array for repeated bays, slats, tiles, rails or prototype repetitions;
- Solidify for controlled wall/panel thickness when its limitations fit the mesh;
- Bevel for physically readable edge highlights rather than razor edges;
- linked duplicates/instances for repeated objects that should share mesh data;
- Geometry Nodes/instances for high-count repeated elements when procedural control materially helps.

Modifier use is not a mandate. Choose the simplest representation that preserves editability and target-engine behavior.

Before dimension-sensitive operations, inspect transforms. Non-unit or negative scale can change modifier behavior, normals, snapping and exported results. Apply transforms only when doing so is appropriate for the object and does not violate protected hierarchy/animation/instance relationships.

Do not apply every modifier merely to make the stack look clean. Preserve a recoverable source until the geometry is proven.

### Pass 5 — architectural geometry and shading

Model geometry where it materially affects silhouette, parallax, shadowing, opening depth, close-range readability or required collision. Prefer textures/materials for broad repeated surface detail that does not need geometry.

Check:
- wall, floor and roof intersections;
- window/door reveals and frames;
- roof ridges, eaves, fascia and gutter attachment where present;
- columns/beams actually meeting the structure rather than floating;
- stairs, rails and thresholds at believable heights relative to the chosen scale;
- coplanar overlaps that would cause z-fighting;
- accidental internal faces created by duplicated modules;
- face orientation and smoothing on visible surfaces.

Avoid topology complexity that exists only to make a large planar wall "look modeled." Spend geometry on silhouette, joins, curvature, shadow-producing depth and deformation/destruction requirements.
