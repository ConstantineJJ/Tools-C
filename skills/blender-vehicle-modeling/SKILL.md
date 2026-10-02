---
name: blender-vehicle-modeling
description: Create or substantially revise cars, trucks, vans, buses, motorcycles, trailers, carts and other wheeled vehicles in Blender. Use when vehicle proportion/reference alignment, wheelbase/track, body-surface continuity, panels, wheels/tires, suspension-visible geometry, repeated/symmetric assemblies, articulation, underbody/interior visibility, game-ready representation or vehicle-specific QA are central; route generic props, street fixtures, electronics/products, vegetation, character rigging, final animation and export to their specialist owners.
---

# Blender vehicle modeling

Read the required [foundation contract](../../docs/foundation.md) and the general [Blender pipeline](../blender-pipeline/SKILL.md). This skill owns vehicle-specific geometry, proportion, construction and articulation decisions, not generic rigging/animation or the whole scene.

## Instruction priority

Follow the user's target, active project/profile, approved reference/concept and gameplay/engine constraints before generic automotive conventions. Real vehicle dimensions and mechanical layouts are calibration evidence, not authority to erase deliberate stylization or fictional engineering. Do not add invisible mechanical complexity merely because a real vehicle would contain it.

## Scope and ownership

Own:
- cars, trucks, vans, buses, wheeled utility vehicles, trailers and carts;
- motorcycles/scooters when wheeled-vehicle construction is the central problem;
- body proportion, wheelbase, track width, ride height and major overhangs;
- body panels, glass openings, lights, bumpers, grilles, wheel arches and exterior assemblies;
- wheels, tires, rims, hubs and repeated left/right or front/rear components;
- visible suspension, steering, brakes, axles, driveshaft/exhaust/underbody where required by camera/gameplay;
- vehicle interior shell, seats/dashboard/steering wheel only to the detail level required by the vehicle target;
- doors, hood/bonnet, trunk/tailgate, steering and wheel articulation decisions before handoff to rigging/animation;
- choosing subdivision/high-low/mid-poly/direct realtime or hybrid representation;
- vehicle-facing UV/material segmentation, damage/weathering strategy and LOD/readability decisions;
- vehicle-specific structural QA and handoff anchors.

Route:
- standalone tools, boxes, generic furniture/clutter and hand-held objects to `blender-props`;
- street lamps, barriers, bollards and site fixtures to `blender-environment-assets`;
- roads/curbs/sidewalks to `blender-roads-infrastructure`;
- embedded dashboards/screens/electronics only to `blender-product-electronics-modeling` when the task becomes product/device-specific rather than vehicle integration;
- generic bones, skinning and control-rig implementation to `blender-rigging-skinning` after vehicle articulation axes are defined;
- motion/actions to `blender-animation`;
- vegetation to `blender-vegetation`;
- final GLB delivery and target-engine validation to export/integration owners.

Boundary rule: vehicle modeling owns **what moves and around which physical axis**; rigging/animation owns how those parts are driven over time. A wheel hub center, steering axis or door hinge belongs here as geometry/articulation truth even when bones are created later.

## Preflight: define the vehicle before modeling

Establish the minimum useful brief:

1. **Vehicle type and role** — hero/player vehicle, traffic/background, wreck, cinematic, showroom, mount, enemy, static prop, etc.
2. **Reference authority** — exact production model/year, blueprint/drawing, photogrammetry/scan, concept art, fictional design or mixed references.
3. **Scale anchors** — wheel/tire diameter, known wheelbase, overall length/width/height, driver/passenger dimensions or another measured feature.
4. **Target camera/use** — exterior third-person, first-person cockpit, close cinematic, top-down, distant traffic, deformation/destruction, customization, etc.
5. **Required moving assemblies** — rolling wheels, steering wheels, suspension travel, doors, hood, trunk/tailgate, steering wheel, wipers, pedals, motorcycle fork/swingarm, trailer hitch, etc.
6. **Visible mechanical depth** — none, simple underbody, exposed suspension/brakes, engine bay, interior, full mechanical showcase.
7. **Representation** — direct realtime/mid-poly, subdivision high + derived low, dedicated high/low bake, CAD-assisted, sculpt-assisted or hybrid.
8. **Surface strategy** — body paint, glass, rubber, chrome/metal, plastic, interior materials, decals/logos, dirt/damage and project-specific texture scheme.
9. **MUST PRESERVE** — approved silhouette, wheelbase/track, ride height, panel gaps, articulation axes, named moving pieces, UVs/materials, hierarchy, instances and unrelated scene data.

If reference views disagree, establish which source is authoritative before locking wheelbase or body contour. Blueprints from the internet can be inaccurate or mismatched to trim/year; do not force photographs to fit a bad drawing.

## Reference and measurement strategy

Organize references by vehicle question:

- orthographic/elevation-ish views for wheelbase, track, roofline, glasshouse, overhangs and panel boundaries;
- front/rear 3/4 photos for curvature and stance that flat blueprints cannot prove;
- low/high camera photos for fender, rocker/sill, bumper and underbody relationships;
- wheel/tire closeups for sidewall profile, tread, rim offset and brake clearance;
- underside/repair/manual/parts photos for suspension and mechanical attachment;
- interior/door-open/engine-bay references only if those areas are in scope;
- clean examples for base construction and worn/damaged examples separately for storytelling.

Align multiple views using stable landmarks such as axle centers, wheel diameter, beltline, windshield corners and major panel seams. Do not chase every pixel of a perspective photo as though it were orthographic.

## Workflow

Use the least complex representation that preserves the required silhouette, reflections, articulation and target-camera detail.

### Pass 1 — wheel centers, stance and bounding proportions

Start with wheel/axle centers and a simple body envelope. Establish:
- wheelbase;
- front/rear track;
- tire outer diameter and width;
- ride height/ground clearance;
- front/rear overhang;
- overall length/width/height;
- cabin/glasshouse volume;
- major approach/departure silhouettes.

For cars/trucks, wheels are powerful scale/proportion anchors. For motorcycles/bicycles, wheel centers, frame/fork geometry and steering-head relationship are even more fundamental.

Judge the blockout from front, side, rear, top and multiple 3/4 views. A side blueprint can look correct while fender width, shoulder line or roof curvature is wrong in perspective.

Do not begin panel gaps, grilles, vents, tread or interior controls until stance and primary surfaces are credible.

### Pass 2 — primary body surfaces and reflection continuity

Vehicle quality depends heavily on broad curvature and highlight flow.

Build the hood/bonnet, roof, fenders, doors/side body, quarters, bumpers and glasshouse as simple controlled surfaces. Keep edge density low enough to adjust curvature without fighting topology.

Check:
- highlight continuity across neighboring panels;
- changes in convex/concave form around wheel arches and shoulder lines;
- symmetry around the center plane while the design is actually symmetric;
- transitions into bumpers, pillars, rocker/sill and roof;
- silhouette from target 3/4 views.

Subdivision can be useful for smooth bodywork, but additional support loops/creases should serve surface control, not merely increase density. Weighted normals can help hard-surface parts but cannot fix poor body curvature.

Use temporary glossy/neutral material and moving light/environment reflections if available; flat clay shading alone can hide surface waviness.

### Pass 3 — define panel architecture before detail

Identify real visual/functional boundaries:
- doors and shut lines;
- hood/bonnet and trunk/tailgate;
- bumper/fascia sections;
- fenders/quarters;
- grille/light housings;
- glass and seals;
- rocker/sill/cladding;
- fuel/charge door;
- removable service panels where visible.

Decide whether a boundary needs separate geometry, a gap/recess, decal/normal detail or only a material transition. Do not carve every line into the main body if a simpler representation is stable and sufficient.

Panel gaps should be consistent with the chosen scale/style and should not destroy the smoothness of adjacent body surfaces. If moving panels are required, separate them early enough to preserve hinge/clearance logic.

### Pass 4 — symmetry and repeated assemblies

Mirror and linked data are high-value for vehicles while left/right parts remain identical.

- Keep the main shell mirrored while symmetry is valid.
- Use shared wheel/tire/rim/brake geometry for identical corners where the project allows it.
- Share repeated lights, mirrors, handles and suspension pieces where truly identical.
- Split data only when front/rear or left/right geometry genuinely differs.
- Preserve a clear center plane and intentional mirror origin/object.

Asymmetrical damage, steering orientation, fuel doors, exhaust exits, wipers or trim variants are reasons to diverge intentionally; they are not reasons to discard reusable symmetry early.

### Pass 5 — wheels and tires as systems

Treat wheel assemblies as more than cylinders.

Establish:
- tire outer diameter, width and sidewall profile;
- rim diameter/width/offset appropriate to the design;
- hub/brake alignment;
- wheel-center origin exactly on the rotation axis;
- enough arch clearance for required steering/suspension travel;
- tread representation appropriate to camera distance.

For repeated tread, model one logical segment/source and array/instance/procedurally repeat it when practical. Do not keep thousands of individually unique tread blocks if shared/generated representation is sufficient.

For realtime targets, decide whether tread belongs in geometry, normal/bake, parallax/material or a hybrid based on target view. Tire sidewall text/logos are usually surface detail unless close hero shots justify geometry.

### Pass 6 — suspension, steering and visible mechanical logic

Model only the mechanical depth the target requires, but keep visible relationships plausible.

Identify:
- wheel hub/upright center;
- steering axis/tie-rod direction where visible/functional;
- suspension arms/struts/springs/dampers at the required fidelity;
- axle/differential/driveshaft or chain/belt where exposed;
- brakes behind wheels;
- exhaust and underbody volumes where camera/destruction exposes them.

Do not invent a generic suspension for a specific reference vehicle if photos/manuals show otherwise. Conversely, do not reproduce every hidden fastener in a third-person background car.

For steering wheels, verify inside-wheel/outside-wheel clearance at representative steering angles; for motorcycles verify front-fork/handlebar clearance and rear swingarm/wheel relationship.

### Pass 7 — articulation and hierarchy before rigging

Before rigging handoff, define geometry origins/axes:

- wheels: hub center, local rotation axis consistent across the vehicle;
- steering front wheels: hub center plus documented steering axis/parent arrangement;
- doors: hinge line/axis;
- hood/bonnet and trunk/tailgate: real hinge axis;
- steering wheel: steering-column axis;
- motorcycle fork/handlebar: steering-head axis;
- swingarm: pivot at frame joint;
- trailer: hitch/coupler articulation point;
- wipers: spindle pivots.

Test each required articulation with temporary transforms. Confirm panels do not obviously intersect at intended open/steer/travel ranges. Return objects to the agreed neutral state after testing.

Do not create an elaborate bone/control rig here unless explicitly in scope; hand off stable axes and hierarchy to rigging.

### Pass 8 — representation and game-ready reduction

Choose high/low/mid/direct strategy per target.

A **mid-poly/direct realtime** vehicle can be efficient when geometric bevels, body panels and normal/decal atlases support frequent iteration. A **high/low** workflow can be justified for complex sculpted/mechanical detail. A **hybrid** can use high-poly bakes for wheels/roof/interior details while keeping body panels editable mid-poly.

When deriving lower-detail geometry:
- preserve body silhouette and wheel arches first;
- preserve major reflection continuity on broad panels;
- preserve moving-part boundaries and articulation axes;
- simplify hidden underbody/interior where target cameras allow;
- bake/atlas small bolts, vents, tread and trim where appropriate;
- avoid deleting geometry that the target camera can expose through wheel wells, glass or open panels.

Do not optimize by one universal triangle number; screen size, vehicle count, damage/customization and platform determine the budget.

### Pass 9 — interior and underbody scope control

Interior detail should match actual visibility.

For exterior traffic vehicles, a simple dark interior shell, seats, steering wheel and dashboard silhouette may be sufficient. First-person/player vehicles may require full cockpit geometry, controls and material separation. Openable doors/hoods raise the required depth substantially.

Use tinted glass only as presentation, not as an excuse to omit geometry that becomes visible in the target game state.

Underbody follows the same rule: preserve major visible volumes and suspension/wheel-well depth, add engine/transmission/exhaust/frame detail only as required.

### Pass 10 — UV/material strategy and identity

Separate material logic by physical surface:
- body paint/clearcoat;
- bare/painted metal;
- glass;
- rubber tires/seals;
- chrome/polished metal;
- matte/textured plastic;
- lights/lenses;
- interior fabric/leather/plastic;
- decals/logos/license/labels;
- dirt/mud/damage masks if the project uses them.

The target engine/material model decides how many slots/maps are practical. Do not turn every visual material into a separate draw-call-heavy slot if shared materials/masks can represent it cleanly.

Maintain coherent texel density and detail scale. Highly visible wheels, front fascia or cockpit may justify different allocation, but document the exception.

For repeated wheels/tires and mirrored body regions, plan overlapping/mirroring against asymmetric logos, damage and dirt. Vehicle-specific wear often becomes obviously duplicated when both sides share high-information texture details.

### Pass 11 — damage, dirt and usage history

Wear should reflect vehicle use:
- tires/wheel wells collect road dirt and abrasion;
- lower body gets splash/mud/chipping differently from roof/upper panels;
- door handles/steps/cargo edges receive contact wear;
- exhaust areas can show heat/soot;
- brakes/wheels gather distinct dust;
- abandoned/weathered vehicles accumulate different patterns than actively maintained vehicles.

Preserve material identity under dirt. Avoid uniform edge scratches over the whole vehicle. For stylized vehicles, exaggerate wear hierarchy deliberately rather than adding equal noise everywhere.

### Pass 12 — vehicle stress test

A representative structural QA should include applicable cases:
- wheelbase/track and ride height check;
- front/side/rear/3/4 silhouette;
- wheel rotation origins;
- steering angle/clearance;
- one door/hood/trunk articulation if required;
- suspension/underbody visibility through wheel wells;
- glass/interior visibility;
- symmetry/shared-data state;
- moving-part hierarchy;
- target-camera close and distant readability.

A vehicle that looks correct in side view but fails in 3/4 reflections, wheel clearance or articulation is not accepted.

## Performance and LOD guidance

- Preserve body silhouette/reflection continuity longer than tiny trim/fasteners.
- Reuse identical wheel/tire and repeated subassembly data where practical.
- Keep procedural/repeated tread or bolt detail instanced until realization is required.
- LOD reductions should retain wheel radius/position, major arches, body outline and moving-piece boundaries before micro-detail.
- Re-check shading/normal maps and glass/interior exposure at each LOD.
- Split vehicle parts according to meaningful animation/damage/material/streaming needs, not simply one object per visible panel or one giant mesh by habit.
- Engine physics, wheel collision, suspension values and runtime handling belong to the target-engine/project owner.

## Validation

Perform applicable checks and label unavailable evidence as SKIP.

### Proportion and stance
- axle centers, wheelbase, track, tire diameter and ride height match the approved metric/reference system;
- front/rear overhang and body/glasshouse proportions are coherent;
- target 3/4 silhouette reads correctly, not only orthographic side view;
- wheels sit correctly inside arches with intended clearance.

### Surface and panel quality
- broad body surfaces have controlled highlight/reflection flow;
- neighboring surfaces meet without unintended kinks or waviness;
- panel gaps/boundaries are consistent and do not destroy adjacent curvature;
- visible normals/face orientation are correct;
- modifier stack and transforms do not depend on accidental object scale/origin.

### Mechanical/articulation
- wheel origins sit on rotation axes;
- steering axes/hierarchy are documented and representative steering does not cause obvious intersections;
- door/hood/trunk/wiper/swingarm/hitch pivots are on intended physical axes where applicable;
- visible suspension/brake/underbody elements attach plausibly;
- moving parts remain separate where downstream behavior requires it.

### Reuse and symmetry
- intended mirrored/shared components remain linked/shared;
- intentional asymmetry is explicit rather than accidental drift;
- front/rear or left/right variants keep compatible attachment/axis conventions where promised;
- repeated wheel/tire geometry has consistent dimensions and origins.

### Surface and context
- material classes remain readable under project lighting;
- mirrored UVs do not duplicate asymmetrical high-information dirt/decals unintentionally;
- interior/underbody depth is sufficient for target cameras/open states;
- damage/weathering follows use/exposure/material logic;
- representative target-camera views have been inspected before visual acceptance.

## Safeguards

- Do not lock detailed panels before wheelbase/stance and primary body surfaces are proven.
- Do not trust one blueprint sheet as ground truth when photos/known dimensions contradict it.
- Do not apply Mirror/subdivision/boolean stacks destructively before asymmetry and low/high handoff requirements are known.
- Do not break shared wheel/tire/subassembly data accidentally.
- Do not move articulation origins for cosmetic convenience after rigging/animation contracts depend on them.
- Do not merge moving panels/wheels solely to reduce object count.
- Do not generate full hidden engine/suspension/interior detail without target-camera/gameplay need.
- Do not invent universal vehicle triangle, texture, wheel-collider, suspension or LOD budgets.
- Do not accept clean topology/import as proof of body-surface reflection quality.

## Pitfalls / Lessons Learned

### VEH-001 — Blueprint tunnel vision
- Symptom: side/front views align to a sheet but the car looks wrong in 3/4.
- Cause: a perspective-inaccurate or mismatched blueprint was treated as absolute truth.
- Rule: reconcile drawings with known dimensions and multi-angle photos using stable landmarks.
- Verification: wheel centers/major dimensions remain correct while 3/4 silhouette and reflections agree with approved references.

### VEH-002 — Detail before stance
- Symptom: accurate lights, grilles and panels sit on a vehicle whose wheelbase, track or roofline feels wrong.
- Cause: secondary detail began before primary proportions were accepted.
- Rule: lock axle centers, stance and body envelope first.
- Verification: simple untextured vehicle already reads correctly at target distance.

### VEH-003 — Dense body topology hides bad curvature
- Symptom: body panels are hard to tune and show wavy reflections despite many support loops.
- Cause: density was added before primary surface continuity was solved.
- Rule: keep control topology sparse enough to tune broad curvature; add support only for real shape requirements.
- Verification: glossy/reflection inspection shows smooth intentional highlight flow across primary panels.

### VEH-004 — Wheel as decoration instead of datum
- Symptom: wheels visually fit but rotation origins, offset, brake alignment or arch clearance are inconsistent.
- Cause: wheel geometry was placed by eye after the body instead of treated as a metric/mechanical anchor.
- Rule: establish wheel centers, dimensions and axes early; build body and articulation around them.
- Verification: all wheel centers/origins are measurable, symmetric/intentional and usable for rotation/steering.

### VEH-005 — Premature asymmetry
- Symptom: mirrored parts diverge and global proportion changes require duplicate manual edits.
- Cause: symmetry/shared data was broken before any real asymmetrical requirement existed.
- Rule: preserve Mirror/linked subassemblies until geometry, damage or trim actually differs.
- Verification: source edits propagate to intended symmetrical/repeated parts; exceptions are documented.

### VEH-006 — Fake mechanical depth everywhere
- Symptom: underbody/interior contains many modeled parts that never affect the target view while visible body quality is underdeveloped.
- Cause: realism was equated with hidden part count.
- Rule: model mechanical depth to visibility, articulation and gameplay requirements.
- Verification: target-camera coverage is satisfied without large unobservable complexity.

### VEH-007 — Pivot drift after modeling
- Symptom: wheels wobble, doors swing around wrong points or steering requires corrective rig offsets.
- Cause: origins were treated as editor conveniences rather than vehicle articulation data.
- Rule: define and test physical axes before rigging handoff; protect them afterward.
- Verification: temporary transforms rotate/open required assemblies correctly with no hidden offset compensation.

## Handoff

When passing to rigging, animation, export or engine integration, report:
- vehicle role and target cameras;
- authoritative dimensions and scale anchors;
- wheelbase, track, tire/wheel dimensions and ride height;
- body representation (subdivision/high-low/mid/direct/hybrid) and modifier state;
- moving parts plus exact origins/axes/hierarchy;
- shared/mirrored component state and intentional asymmetries;
- required steering/suspension/opening ranges tested;
- interior/underbody detail scope;
- UV/material/damage strategy and protected decals/identity;
- structural/visual evidence completed;
- open rig/physics/collision/LOD/export/runtime gates.

## Completion / stop

Complete when the requested vehicle exists with approved stance/proportion, controlled primary surfaces, coherent panel/mechanical construction, usable wheel and articulation axes, appropriate representation/detail for target cameras, protected data intact, and applicable structural/visual checks passed or explicitly handed off.

Stop and report instead of guessing when reference/blueprint conflict changes wheelbase or major body shape materially, required mechanical articulation cannot be determined from available evidence, target-camera/open-state requirements are missing but necessary to scope interior/underbody work, or a requested change would invalidate protected rig/UV/pivot contracts outside scope.

## Research basis

The practical rules in this specialist are distilled from Blender documentation and vehicle-production breakdowns covering Mirror/subdivision/modifier behavior, blueprint/reference reconciliation, stance-first blockout, body-surface continuity, wheel/tire and mechanical construction, high/low versus mid-poly choices, articulation and game-ready delivery. See [research notes](references/research-notes.md) for source URLs, source type and caveats.
