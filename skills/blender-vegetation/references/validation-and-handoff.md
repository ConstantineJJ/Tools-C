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

The practical rules in this specialist are distilled from Blender 4.5 instancing/Geometry Nodes documentation, Epic's pivot-based foliage-animation documentation and vegetation/environment-art production breakdowns covering grass patch composition, foliage cards, cluster readability, plant variation and preservation of branch/leaf pivot data. See [research notes](research-notes.md) for source URLs, source type and caveats.
