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

The practical rules in this specialist are distilled from Blender documentation and environment/prop production breakdowns covering blockout, modular/repeated assets, Asset Browser reuse, bevel/normals, texel-density planning, trim/shared texture strategies, LOD thinking and environment-specific wear. See [research notes](research-notes.md) for source URLs, scope and caveats.
