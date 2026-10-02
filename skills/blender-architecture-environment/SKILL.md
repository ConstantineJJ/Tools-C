---
name: blender-architecture-environment
description: Create or substantially revise buildings, houses, architectural shells, modular construction kits and other large man-made structures in Blender. Use when building scale, architectural proportion, modular breakdown, grid/pivot discipline, facades, roofs, walls, openings, reusable structural pieces, trim/tileable material strategy or large-structure assembly are central; route roads, street infrastructure, small environment assets, props, vegetation, vehicles, appliances/electronics, sculpt-only work and final export to their specialist owners.
---

# Blender architecture & large structures

Read the required [foundation contract](../../docs/foundation.md) and the general [Blender pipeline](../blender-pipeline/SKILL.md). This skill owns architectural reasoning and reusable large-structure construction, not the whole environment pipeline.

## Instruction priority

Follow the user's target, active project/profile, approved concept/reference and engine constraints before generic architectural conventions. Real-world dimensions are a calibration aid, not authority to override an explicit stylized design. Never normalize intentional exaggeration, impossible architecture or asymmetry unless the task asks for it.

## Scope and ownership

Own:
- buildings, houses, sheds, towers, halls, industrial structures and similar large man-made forms;
- exterior shells and interior architectural shells when both are part of the same structure;
- blockout, scale, story height, wall/floor/roof relationships and major openings;
- deciding unique versus modular versus hybrid construction;
- reusable wall, corner, window, door, floor, roof, trim, column, beam and structural-detail modules;
- grid and pivot conventions for architectural pieces;
- architecture-facing use of tileable materials, trim sheets, decals and reusable material regions;
- assembly validation, repetition control and large-structure optimization decisions.

Route:
- benches, lamps, fences, bins, bollards and similar standalone environment objects to `blender-environment-assets` when that specialist exists;
- roads, curbs, sidewalks, paths, gutters and network infrastructure to `blender-roads-infrastructure`;
- furniture and hand-held/interior detail objects to `blender-props`;
- vehicles to `blender-vehicle-modeling`;
- appliances/electronics to `blender-product-electronics-modeling`;
- vegetation to `blender-vegetation`;
- organic or damage sculpting as the primary task to `blender-sculpting` when available, otherwise the current sculpting route;
- final GLB delivery to export validation and target-engine integration.

A building can contain work owned by several specialists. Keep the architectural shell here and hand off embedded assets instead of turning this skill into a universal environment owner.

## Preflight: define the structure before modeling

Establish the minimum useful architectural brief:

1. **Target type** — one-off hero structure, reusable modular kit, kit-built hero, background structure, interior shell, exterior shell or complete building.
2. **Reference authority** — concept art, measured real building, photo set, floor plan/elevation, style reference, or intentionally invented design.
3. **Use and viewing distance** — walkable gameplay, close hero camera, distant skyline, cinematic, VR, fixed view, destructible or static.
4. **Scale anchors** — character/player height, doorway, stair, floor height, known object, drawing dimensions or another explicit metric.
5. **Modularity goal** — what must repeat, what may vary, what is unique, and whether the kit must assemble multiple buildings rather than only reconstruct one facade.
6. **Material strategy** — unique bake, tileable, trim-sheet, hybrid, atlas, decals/masks, or project-defined material system.
7. **Production target** — realtime engine, offline render, level kit, marketplace pack, prototype, etc.
8. **MUST PRESERVE** — approved footprint, openings, floor plan, silhouette, named modules, materials, UVs, origins/pivots, collection structure, instances and unrelated dirty scene data.

If a missing dimension would materially change floor height, opening size, player clearance or modular spacing, resolve or explicitly choose a provisional assumption before detail work.

## Reference and metric strategy

Use references by function instead of collecting only beauty images:

- overall massing and silhouette;
- front/side/elevation or orthographic-ish views for proportion;
- closeups for windows, doors, cornices, gutters, roofs, joints and construction logic;
- human figures, cars, doors, stairs or known objects for scale when dimensions are absent;
- material/weathering references separately from geometry references;
- construction references when the visible form depends on how parts meet or age.

For historical or regional architecture, identify repeated design rules before copying isolated decorative details. For invented/stylized buildings, use real construction as support for believable joins and scale, while preserving the concept's deliberate departures.

Record a small metric sheet before committing the kit: base grid or increment, story height, typical wall thickness if exposed, standard module widths, primary opening sizes and pivot convention. These are project choices, not universal constants.

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

### Pass 6 — material and UV strategy

Choose texture strategy from reuse and camera needs:

- **tileable materials** for broad walls, floors, roof fields and repeating surfaces;
- **trim sheets** for repeated edge bands, frames, moldings, beams, rails and architectural motifs;
- **unique bakes** for hero elements whose distinctive detail justifies the texture cost;
- **hybrid** for architecture that combines large tileable surfaces with unique inserts or trim-driven details;
- **decals/masks/secondary UVs** for local storytelling, dirt, signage, repairs and variation when supported by the target pipeline.

Maintain project-consistent texel density unless an explicit hero/readability reason justifies a different allocation. Do not bake unique large textures for every wall merely because it is convenient.

When a trim sheet or tileable material repeats widely, avoid large unique stains/cracks that reveal obvious periodic repetition. Put high-recognition variation into decals, vertex/mask layers, dressing or controlled variants.

### Pass 7 — variation without breaking the kit

Break repetition while preserving dimensions and snap behavior. Useful variation layers:
- interchangeable window/door/facade modules with the same footprint;
- roof/dormer/end-cap variants;
- material or UV offsets where valid;
- decals, signs, damage overlays and color changes;
- handoff props/vegetation;
- selective unique hero sections.

Do not "add uniqueness" by scaling modular pieces off-grid or arbitrarily moving pivots. Variation should preserve the assembly contract unless the piece is deliberately reclassified as unique.

### Pass 8 — assembly and target-context test

Assemble at least one representative structure from the final modules. If the kit is intended for multiple layouts, assemble a second materially different layout or stress case.

Verify:
- modules snap without manual micro-adjustment;
- corner, opening, floor and roof interfaces close cleanly;
- no visible cracks, doubled surfaces or z-fighting at common joins;
- repeated parts retain shared data/instances where intended;
- silhouette and scale still match the blockout/reference;
- material scale and direction stay coherent across adjacent pieces;
- target-engine import, collision, lightmap/UV or LOD requirements are handed to the appropriate owner rather than assumed.

A structurally valid module library is not visually accepted until representative assembled views have been reviewed.

## Performance and scene-structure guidance

Large structures fail as often from duplication strategy as from polygon count.

- Prefer linked geometry or instances for high-count repeated elements when independent geometry is unnecessary.
- Keep instances unrealized until downstream operations require unique geometry.
- Avoid expensive procedural evaluation on more geometry than necessary.
- Separate modules at meaningful reuse/culling/streaming boundaries when the target engine benefits; do not fragment every decorative strip into a separate object by habit.
- Do not merge the whole kit into one giant mesh merely to reduce object count unless the target pipeline explicitly requires it.
- Polygon, material-slot, draw-call, LOD and collision budgets are project/engine decisions. Record them in the profile/target rules rather than inventing universal numbers here.

## Validation

Perform applicable checks and label unavailable evidence as SKIP.

### Architectural form
- target silhouette and major masses match the approved blockout/reference;
- floor/story/roof relationships are coherent;
- doors, windows, stairs and walkable clearances match the declared scale anchors;
- exposed wall/roof/floor thickness is intentional and visually plausible;
- major architectural connections do not float or intersect unintentionally.

### Modular integrity
- declared module dimensions land on the chosen grid/increments;
- pivots/origins follow the family convention;
- representative straight/corner/opening/floor/roof assemblies fit without manual offsets;
- variants preserve compatible dimensions where interchangeability is promised;
- no unnecessary one-off pieces duplicate an existing reusable function;
- linked/instanced elements are still linked/instanced where intended.

### Mesh and shading
- no unintended duplicate/internal/copanar geometry at seams;
- visible normals/face orientation are correct;
- bevel/shading choices produce stable highlights at the target distance;
- modifier stacks are intentional and do not depend on accidental transforms;
- no large hidden complexity without a production reason.

### Surface consistency
- texel density/material scale is coherent with the project target;
- trim/tile directions follow construction logic where it matters;
- obvious repeated high-information stains/patterns are controlled;
- material seams across modular joins are intentional or visually acceptable.

### Context and visual QA
Capture or inspect representative exterior and/or interior views appropriate to the task. Include target camera/player-height evidence where scale/readability matters. For a reusable kit, inspect at least one assembled facade/room rather than only isolated modules.

## Safeguards

- Do not destroy the blockout or approved source before final modules are proven.
- Do not apply destructive booleans/remesh/realize/join operations across unrelated modules without a recoverable baseline and explicit need.
- Do not alter a family pivot convention mid-kit without migrating all affected modules and re-running assembly QA.
- Do not make linked data unique accidentally when the task depends on shared edits.
- Do not delete hidden/back faces solely as an optimization if interiors, shadows, destruction or future camera access require them.
- Do not infer collision, lightmap, LOD or engine draw-call rules from another project.
- Do not use microscopic geometric detail to compensate for weak massing, scale or material hierarchy.

## Pitfalls / Lessons Learned

### ARCH-001 — Detail before massing
- Symptom: ornate windows, trims or brick detail exist, but the building feels wrong.
- Cause: secondary/tertiary work started before footprint, height, openings and roof mass were proven.
- Rule: return to blockout and target-view silhouette before adding more detail.
- Verification: simplified shaded view still reads as the intended structure at target distance.

### ARCH-002 — Modular pieces that only work once
- Symptom: many modules exist but most can only reconstruct the original building.
- Cause: decomposition followed visible object boundaries instead of repeat/use value.
- Rule: prove reuse and compatibility before expanding the kit; keep true hero geometry unique.
- Verification: a representative alternate assembly works without bespoke repair pieces for every join.

### ARCH-003 — Grid without pivot discipline
- Symptom: dimensions are nominally modular but every placement needs manual nudging.
- Cause: inconsistent origins, thickness side, orientation or corner convention.
- Rule: grid, pivot and thickness conventions are one system; validate them together.
- Verification: clean assembly from numeric/grid placement without per-piece micro-offsets.

### ARCH-004 — Repetition hidden with broken metrics
- Symptom: variation exists, but modules no longer align or walls drift.
- Cause: scale/transform variation was used on structural kit pieces.
- Rule: vary surfaces, dressing or compatible variants; preserve structural dimensions.
- Verification: all interchangeable pieces retain the declared bounding/anchor dimensions.

### ARCH-005 — Unique texture everywhere
- Symptom: texture count and authoring time scale with every wall/facade section.
- Cause: repeated architecture was treated like a set of hero props.
- Rule: evaluate tileable/trim/hybrid approaches before unique bakes; reserve unique textures for justified focal information.
- Verification: repeated architectural detail reuses material resources without unacceptable visual repetition.

### ARCH-006 — Premature realization/merge
- Symptom: repeated geometry becomes heavy and later design changes require many manual edits.
- Cause: instances/linked modules were realized or joined before the design stabilized.
- Rule: keep shared data procedural/linked until uniqueness is required by a concrete downstream operation.
- Verification: editing a source module updates intended repeats and scene performance remains reasonable.

## Handoff

When passing the structure to another specialist or export/integration, report:
- target type and use/viewing distance;
- scale anchors and key metrics;
- grid/module/pivot convention;
- unique versus reusable/variant pieces;
- modifier/instance state and any transforms that must remain intact;
- material/UV strategy and texel-density assumptions;
- protected silhouette/openings/footprint;
- known seam, shading, performance or target-engine risks;
- assembly and visual evidence completed;
- open gates for props, roads, vegetation, collision, LOD, export or runtime QA.

## Completion / stop

Complete when the requested large structure or architectural kit exists, the major proportions and scale are proven, modular pieces assemble according to the declared contract, repeated geometry/material strategy is appropriate for the target, protected data survived, and required structural/visual checks have passed or are explicitly handed off.

Stop and report instead of guessing when scale/reference conflicts would change the architecture materially, modular rules are not defined enough to author interchangeable pieces, target-engine constraints are required but unavailable, or the requested edit would invalidate protected layout/UV/pivot/instance contracts outside scope.

## Research basis

The practical rules in this specialist skill are distilled from Blender documentation, environment-art production breakdowns, a published modular-architecture study and training/community guidance. See [research notes](references/research-notes.md) for supporting principles and source URLs.
