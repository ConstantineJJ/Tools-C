---
name: blender-props
description: Create or substantially revise prop-centric discrete assets in Blender: furniture, containers, tools, clutter, decor, hand-held objects, interior set dressing and similar small/medium reusable or storytelling assets. Use when object function, handling/placement, construction, hero-vs-background fidelity, high/low representation, UV/bake strategy, material separation, wear/storytelling or prop-library packaging are central; route building-integrated geometry, standalone street/site fixtures, road networks, vehicles, product/electronics-specialized devices, vegetation, sculpt-only work and final export to their specialist owners.
---

# Blender props

Read the required [foundation contract](../../docs/foundation.md) and the general [Blender pipeline](../blender-pipeline/SKILL.md). This skill owns prop-centric discrete assets, not every small object in a scene.

## Instruction priority

Follow the user's request, active project/profile, approved reference/concept and target-engine constraints before generic prop-art conventions. Real products and manufacturing are useful evidence for believable construction and scale; they do not override deliberate stylization. Do not force every prop through a high-poly/low-poly bake, sculpt pass, unique texture or destructive cleanup when a simpler representation satisfies the target.

## Scope and ownership

Own:
- furniture such as chairs, tables, shelves, cabinets, stools and movable interior pieces;
- containers, cases, crates, boxes, cans, bottles and storage objects;
- hand tools, workshop items, kitchenware, books, decor, clutter and small narrative set dressing;
- hand-held or character-interaction props where the asset itself is the modeling task;
- one-off hero props and families/sets of related props;
- blockout, scale, silhouette, functional construction and handling/placement logic;
- choosing direct realtime geometry versus high/low/baked, sculpt-assisted or hybrid production;
- prop-specific UV allocation, mirroring/stacking decisions, bake preparation and material separation;
- wear, damage, labels and storytelling that follow use/material history;
- prop-library pivots, subassembly hierarchy, variants and reuse packaging;
- bounded LOD/readability decisions when explicitly requested.

Route:
- building-integrated walls, doors, windows, stairs, architectural trims and built-in structural modules to `blender-architecture-environment`;
- benches, street lamps, bollards, hydrants, public bins, site barriers and similar standalone street/site fixtures to `blender-environment-assets`;
- roads, curbs, sidewalks, paths, crossings and connected network infrastructure to `blender-roads-infrastructure`;
- cars and wheeled vehicles to `blender-vehicle-modeling`;
- appliances, computers, monitors, TVs, consoles and engineered consumer/digital devices whose product-design construction is central to `blender-product-electronics-modeling` when implemented;
- vegetation to `blender-vegetation`;
- a primary sculpting task to `blender-sculpting` when implemented, otherwise the current sculpting route;
- final GLB delivery to export validation and target-engine integration.

Boundary rule: classify by **production role**, not physical size. A dining chair is normally a prop; a public park bench is environment-assets. A simple decorative radio can remain a prop if the task is scene dressing, but a close product-accurate electronic device with connectors, controls, vents and engineered assembly should route to product/electronics once that owner exists.

## Preflight: define the prop before modeling

Establish the minimum useful brief:

1. **Role** — hero/inspectable, gameplay-interaction, hand-held, midground repeated, background clutter, furniture, set-dressing family, etc.
2. **Reference authority** — exact real object, concept art, style guide, mixed references or intentionally invented design.
3. **Scale anchors** — hand, character/player, tabletop, doorway, seat height, known dimensions or measured reference.
4. **Viewing/interaction context** — first-person closeup, third-person hand use, static interior, cinematic, inventory preview, destruction, animation or distant dressing.
5. **Construction/function** — what supports what, hinges/handles/lids/moving parts, fasteners/joints, material boundaries and likely manufacturing process where visible.
6. **Representation** — direct realtime mesh, high-to-low bake, subdivision high + low, sculpt-assisted, trim/shared material or hybrid.
7. **Surface strategy** — unique set, shared material/atlas, mirrored/stacked UVs, labels/decals, tileables or project-defined scheme.
8. **Reuse model** — one-off, repeated identical asset, cosmetic variants, geometric family, subassembly reuse or asset-library item.
9. **MUST PRESERVE** — approved silhouette, dimensions, functional clearances, pivots/articulation axes, UVs, materials, names, linked/shared data, hierarchy and unrelated scene state.

If missing reference would materially change silhouette, interaction, articulation or construction, resolve it or record a provisional assumption before committing detail.

## Reference strategy

Collect references by question rather than filling one board with beauty shots:

- front/side/top/3/4 views for proportion and silhouette;
- auction/product listings and repair/teardown photos for additional angles, underside/back and construction;
- human/hand context for interaction scale;
- closeups for seams, joints, fasteners, handles, hinges, welds, labels and material transitions;
- clean/new examples to understand the base object before aging it;
- used/damaged examples to understand where wear actually appears;
- material-specific examples for wood grain, painted/oxidized metal, plastic, rubber, glass, paper, fabric, leather, ceramics, etc.;
- family references when several props must share a visual/manufacturing language.

Reference gathering is iterative. If a hidden joint or material response becomes unclear during modeling/texturing, gather targeted evidence instead of inventing detail from habit.

## Workflow

Use the least complex representation that can satisfy silhouette, shading, interaction and delivery needs.

### Pass 1 — blockout, scale and silhouette

Build the complete object from simple volumes. Establish bounding dimensions, major negative spaces, center of mass/readability, interaction points and dominant silhouette.

Use the appropriate scale anchor: hand proxy for hand-held props, seated/standing human for furniture, shelf/table/door context for interior props. Inspect the target gameplay/camera view, not only a neutral turntable.

For first-person or inventory props, identify the surfaces that dominate the actual view. Those regions may justify more geometric/texture attention than hidden undersides.

Do not add screws, scratches, fabric wrinkles, embossed logos or edge damage while primary proportions remain unstable.

### Pass 2 — prove function and assembly

Before polishing, identify:
- which pieces carry load or provide structure;
- which parts are separate because they move, open, fold, detach or use a different material/process;
- where clearances/gaps are functionally necessary;
- how handles, hinges, knobs, fasteners and panels actually attach;
- what can be simplified because it is never seen or used;
- what must remain separate for animation, interaction, variants or export.

A believable prop does not need every hidden internal component, but visible construction should explain how the object holds together. If stylized, preserve the same functional logic while exaggerating intentionally.

### Pass 3 — choose direct mesh versus high/low/bake

Do not treat one production pipeline as universal.

Use **direct realtime geometry** when:
- the form is simple enough to shade well directly;
- target view benefits more from geometric bevels/silhouette than baked micro-detail;
- the prop is low-detail/background or stylized;
- maintaining editability is more valuable than a separate high poly.

Use a **high/low bake** when:
- complex bevels, sculpted wear, engravings, relief or high-frequency shape detail would be expensive in realtime geometry;
- hero/close-view fidelity warrants a dedicated high source;
- the target pipeline explicitly expects baked tangent-space detail.

Use **hybrid** when some pieces are best modeled directly and others justify baking/sculpting.

Blockout remains upstream of all three choices. If the high source changes silhouette materially, revise the low/source representation rather than forcing the bake to conceal mismatch.

### Pass 4 — hard-surface construction and editability

Choose tools by function:
- Mirror for true or temporary symmetry;
- Bevel for real edge width/highlight shape;
- Boolean for stable cutouts/recesses where it saves work;
- Solidify for sheet thickness when appropriate;
- Array/linked duplicates for repeated slats, screws or repeated subcomponents;
- subdivision where smooth controlled curvature is needed;
- weighted/custom normals only as a shading aid after geometry is sound.

Keep symmetry/modifiers live while they support iteration. Break symmetry deliberately when the reference/design requires different geometry or unique wear, not merely because the model is "almost finished."

Inspect transforms before dimension-sensitive bevels, solidify, arrays, baking or export. Apply transforms only when appropriate for the hierarchy/animation/instance state; do not destructively normalize objects by habit.

### Pass 5 — final realtime mesh / bake target

When a low/realtime mesh is required, optimize by visible contribution:
- preserve silhouette and large curvature first;
- preserve articulation and interaction clearances;
- spend edges where they stabilize shading or bake projection;
- simplify hidden/internal regions when no downstream requirement needs them;
- retain enough geometry to produce a clean bake rather than chasing the minimum triangle count before testing.

All-quads are not a universal requirement for static props. Ngons/triangles can be valid where they are planar/stable and do not harm shading, subdivision, deformation or bake behavior. The acceptance criterion is predictable output and downstream use, not topology aesthetics in isolation.

For high/low workflows, make quick test bakes before final UV/polish where practical. If projection errors appear, fix low geometry, normals, UV splits, ray distance or cage rather than painting over systemic artifacts.

### Pass 6 — UV, mirroring, stacking and bake plan

Choose unique versus shared UV space deliberately.

Consider mirroring/stacking when:
- surfaces are genuinely symmetric/repeated;
- unique labels/wear are not required there;
- shared detail meaningfully improves texel allocation.

Keep unique UV space where:
- asymmetrical storytelling is important;
- the target camera sees both mirrored regions together and repetition would be obvious;
- labels, dirt, damage, directional materials or baked lighting/AO require distinction.

Prioritize UV area according to target visibility, not only surface area. Maintain the project's texel-density policy unless a documented hero/readability exception applies.

For baked props:
- verify high and low alignment;
- use tangent-space normals when that matches the delivery target;
- use selected-to-active/cage/ray settings deliberately;
- provide sufficient bake margin to avoid seam/filtering artifacts;
- re-check hard edges/UV boundaries/normals where projection errors cluster.

Do not universalize one resolution or padding value; these depend on project texture size, mip behavior and target distance.

### Pass 7 — materials before damage

Establish the clean material identity first:
- base color range;
- roughness response;
- metallic/dielectric classification where applicable;
- grain/fiber/directionality;
- molded/cast/machined/painted surface character;
- glass/rubber/fabric/paper behavior as relevant.

Then add use/environment history. Roughness often carries as much material identity as color; evaluate the prop under more than one light direction so a texture is not accidentally tuned to one studio setup.

Separate materials according to physical/material logic, not arbitrary color regions. Two similarly colored parts can still need different roughness/normal behavior because one is plastic and one is painted metal.

### Pass 8 — storytelling, wear and damage

Ask concrete questions:
- Who owns/uses this object?
- How often is it handled?
- What contacts the floor/table/hand/other parts?
- Where does dust accumulate versus get wiped away?
- Where can moisture, grease, rust, sun bleaching, dents, chipped paint or abrasion plausibly occur?
- Which repairs, labels, stickers, tape, replacement parts or age differences support the intended story?

Build history in layers: construction/material variation → broad age/use → contact/exposure patterns → selective small damage. Avoid uniform edge wear, random scratch noise and equal dirt on every face.

Not every prop must be heavily aged. A clean/new object can be more believable in context than forcing "storytelling" through damage. Different props in one scene may have different ages and maintenance histories.

### Pass 9 — hierarchy, pivots and interaction

Choose origin/pivot from use:
- movable furniture: stable base/bottom-center or project placement convention;
- hand-held prop: root/handle anchor suitable for attachment to the character/project socket convention;
- hinged lid/door: separate moving component with pivot on the real hinge axis;
- drawer: translation axis aligned with intended travel;
- wheel/knob/lever: pivot on its real rotational axis;
- stackable/container object: deterministic base/footprint anchor if placement depends on it.

Keep the asset root and moving subcomponents conceptually separate. Do not place every object's origin at world zero or geometric center if that makes actual placement/animation harder.

For interactive props, perform a simple clearance/articulation test before finalizing: hand fit, lid opening, drawer travel, seated clearance, door/cabinet collision, etc., as applicable.

### Pass 10 — library reuse, variants and scene-context test

For a reusable asset library, decide whether copies should remain linked to the source, append independent data, reuse mesh/material data, or instantiate a collection. Use the reuse mode that matches whether later source edits should propagate.

For prop families:
- share subcomponents/materials where truly identical;
- vary color/labels/wear first when geometry does not need to change;
- preserve common dimensions/attachment anchors where compatibility is promised;
- make geometry unique only for real silhouette/function changes.

Place the prop in one representative target context. For clutter/family assets, test several together. Confirm scale, visual hierarchy, repetition, ground/surface contact and target-camera readability. An isolated beauty render alone is not acceptance for an in-game set-dressing prop.

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

The practical rules in this specialist are distilled from Blender documentation and prop/environment production breakdowns covering Asset Browser reuse, bevel/normal behavior, UV and selected-to-active baking, blockout/reference practice, iterative low/high/bake workflows, prop storytelling, material roughness, wear logic and context-driven asset reuse. See [research notes](references/research-notes.md) for source URLs, source type and caveats.
