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

The practical rules in this specialist skill are distilled from Blender documentation, environment-art production breakdowns, a published modular-architecture study and training/community guidance. See [research notes](research-notes.md) for supporting principles and source URLs.
