## Performance and LOD guidance

Optimization follows screen size, repetition count, interaction and target hardware.

- Preserve silhouette and large negative spaces longer than tiny fasteners or micro-bevel segments.
- If the prop is repeated heavily, shared mesh/material data can matter more than shaving a few triangles from one copy.
- Generate LODs from a proven realtime mesh, not from an unstable blockout.
- Re-check normals, UVs and material IDs after simplification.
- Collision, LOD naming, streaming, texture budgets and engine-specific draw-call rules remain project/engine decisions unless explicitly requested.
- Do not collapse articulated/interactive pieces into one mesh if downstream behavior requires them separate.

## Validation

Perform applicable checks and label unavailable evidence as SKIP.

### Form and function
- scale matches the declared anchor/context;
- silhouette and major proportions match approved reference/design;
- visible construction explains how the object is assembled;
- handles, hinges, drawers, lids, seating or other interaction zones have plausible clearance;
- intended moving parts are separated/pivoted correctly.

### Geometry and shading
- no unintended duplicate/internal/coplanar geometry;
- visible normals/face orientation are correct;
- bevels/curvature produce stable highlights at target scale;
- broad faces remain visually flat where intended;
- modifiers/transforms are intentional rather than accidental dependencies;
- realtime geometry complexity is concentrated where visible/functional.

### UV and bake
- texel density follows project policy with documented exceptions;
- mirrored/stacked regions do not duplicate unique storytelling unintentionally;
- seams/hard edges/normals do not create unacceptable bake artifacts;
- cage/ray settings cover the high source without obvious projection contamination;
- normal-map space and material setup match the target export pipeline where applicable.

### Materials and storytelling
- materials remain distinguishable through roughness/normal response, not color alone;
- wear follows contact, exposure, age and material logic;
- labels/damage support rather than obscure form readability;
- repeated family assets do not show identical high-information wear unless intentional.

### Context and reuse
- origin/pivot supports intended placement/attachment;
- linked/shared data remains shared where promised;
- variants preserve required dimensions/anchors;
- target-camera/context view confirms scale and readability;
- isolated presentation quality is not substituted for required gameplay/context evidence.

## Safeguards

- Do not destroy the approved blockout/high source or recoverable pre-bake state before the realtime result is proven.
- Do not assume every prop needs high/low, sculpting, all-quads or unique textures.
- Do not use weighted normals or baked normals to hide broken silhouette, intersections or invalid geometry.
- Do not make mirrored/stacked UVs unique accidentally, or keep them shared when unique labels/wear are required.
- Do not apply destructive booleans/modifiers/joins across unrelated subassemblies without a concrete need and recoverable baseline.
- Do not merge moving/interactive parts solely to reduce object count.
- Do not invent universal triangle, texture-resolution, texel-density, LOD or collision budgets.
- Do not add wear/noise to compensate for weak proportions, materials or construction.
- Do not absorb environment fixtures, building modules, roads, vehicles or product/electronics work merely because the object is small.

## Pitfalls / Lessons Learned

### PROP-001 — Beauty render scale trap
- Symptom: the prop looks convincing alone but wrong beside a hand, character, table or room.
- Cause: blockout was judged only in isolation.
- Rule: prove scale with the actual interaction/context anchor before detail.
- Verification: context placement works without corrective object scaling.

### PROP-002 — Bake pipeline by habit
- Symptom: a simple prop accumulates high-poly, retopo and bake work with little visible benefit.
- Cause: high/low was treated as mandatory rather than a representation choice.
- Rule: justify high/low by visible/detail/performance needs; use direct realtime geometry when sufficient.
- Verification: chosen representation meets target shading/readability with less unnecessary production state.

### PROP-003 — Lowest-poly-before-bake failure
- Symptom: projection artifacts appear around curves/bevels and require excessive cage fixes.
- Cause: realtime mesh was reduced below what clean shading/baking needed before test bakes.
- Rule: iterate low geometry against quick bakes; optimize after the required surface transfer is stable.
- Verification: final realtime mesh meets both performance target and clean bake criteria.

### PROP-004 — Mirrored story duplication
- Symptom: the same sticker, stain, scratch or chipped edge appears symmetrically on both sides.
- Cause: UV mirroring/stacking was chosen before unique storytelling needs were identified.
- Rule: decide unique-visible regions before final packing; stack only surfaces that can legitimately share detail.
- Verification: high-information details appear only where intended.

### PROP-005 — Material defined by color only
- Symptom: painted metal, plastic and rubber read as the same substance with different colors.
- Cause: roughness/normal/microstructure and construction cues were secondary to base color.
- Rule: establish clean material response before aging; judge under varied light directions.
- Verification: materials remain distinguishable in grayscale/base-color-suppressed inspection through specular/roughness/normal behavior.

### PROP-006 — Uniform storytelling noise
- Symptom: scratches, dirt and edge wear cover every surface equally and the prop feels procedurally aged.
- Cause: masks/generators were used without contact/exposure history.
- Rule: age from use, material and environment; leave quiet areas.
- Verification: wear distribution can be explained by a plausible interaction/exposure history.

### PROP-007 — Wrong pivot for actual use
- Symptom: furniture floats during placement, lids rotate around their center, or hand-held props need corrective parent offsets.
- Cause: origin was chosen for modeling convenience instead of placement/articulation.
- Rule: choose root and subcomponent pivots from downstream use before final handoff.
- Verification: placement/attachment/articulation works with documented transforms and no hidden corrective offset.

## Handoff

When passing to animation, export, engine integration or another domain owner, report:
- prop role, target camera and interaction context;
- scale anchors and key dimensions;
- approved silhouette/construction assumptions;
- direct mesh versus high/low/sculpt/hybrid representation;
- high/low/cage/bake state where applicable;
- UV mirroring/stacking and material strategy;
- hierarchy, root pivot and moving-part axes;
- linked/shared-data/variant state;
- protected labels, wear/story beats or functional clearances;
- structural/visual/context evidence completed;
- open LOD/collision/export/runtime gates and known risks.

## Completion / stop

Complete when the requested prop or prop family exists, scale/silhouette/function are proven for the intended context, representation and bake/material decisions are appropriate to the target, pivots/hierarchy support placement or interaction, protected data survived, and applicable structural/visual/context checks have passed or are explicitly handed off.

Stop and report instead of guessing when reference ambiguity would materially change function/articulation, the target camera/interaction is required to allocate detail but unavailable, a bake/export constraint conflicts with protected UV/hierarchy state, or the requested edit crosses into another specialist's protected domain.

## Research basis

The practical rules in this specialist are distilled from Blender documentation and prop/environment production breakdowns covering Asset Browser reuse, bevel/normal behavior, UV and selected-to-active baking, blockout/reference practice, iterative low/high/bake workflows, prop storytelling, material roughness, wear logic and context-driven asset reuse. See [research notes](research-notes.md) for source URLs, source type and caveats.
