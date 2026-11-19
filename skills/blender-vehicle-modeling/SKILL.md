---
name: blender-vehicle-modeling
description: Create or substantially revise cars, trucks, buses, motorcycles, trailers and other wheeled vehicles in Blender: stance, wheelbase/track, body surfaces, panels, wheels, visible suspension, articulation and game-ready reduction. Props, electronics, rigging, animation and export keep their owners.
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

For a concrete class-specific build sequence, select exactly the applicable [vehicle quick recipe](references/vehicle-recipes.md): passenger/stylized car, motorcycle/scooter, or heavy truck/multi-axle/trailer. Recipes are execution aids, not separate owners or substitute source authority. Do not load all recipes or run unneeded stages for a narrow edit.

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

Work the passes in order; full instructions, performance/LOD guidance and the validation checklist are in [procedure](references/procedure.md) — read it before modeling and again before acceptance.

- **Vehicle-specific acceptance gates** — For new or substantially rebuilt vehicles, follow the [V0–V4 gate and measurement guide](references/vehicle-qa.md):
- **Pass 1 — wheel centers, stance and bounding proportions** — Start with wheel/axle centers and a simple body envelope.
- **Pass 2 — primary body surfaces and reflection continuity** — Vehicle quality depends heavily on broad curvature and highlight flow.
- **Pass 3 — define panel architecture before detail** — Identify real visual/functional boundaries:
- **Pass 4 — symmetry and repeated assemblies** — Mirror and linked data are high-value for vehicles while left/right parts remain identical.
- **Pass 5 — wheels and tires as systems** — Treat wheel assemblies as more than cylinders.
- **Pass 6 — suspension, steering and visible mechanical logic** — Model only the mechanical depth the target requires, but keep visible relationships plausible.
- **Pass 7 — articulation and hierarchy before rigging** — Before rigging handoff, define geometry origins/axes:
- **Pass 8 — representation and game-ready reduction** — Choose high/low/mid/direct strategy per target.
- **Pass 9 — interior and underbody scope control** — Interior detail should match actual visibility.
- **Pass 10 — UV/material strategy and identity** — Separate material logic by physical surface:
- **Pass 11 — damage, dirt and usage history** — Wear should reflect vehicle use:
- **Pass 12 — vehicle stress test** — A representative structural QA should include applicable cases:

**Performance and LOD guidance:** see the procedure reference.

**Validation:** see the procedure reference.
- **Proportion and stance** — axle centers, wheelbase, track, tire diameter and ride height match the approved metric/reference system;
- **Surface and panel quality** — broad body surfaces have controlled highlight/reflection flow;
- **Mechanical/articulation** — wheel origins sit on rotation axes;
- **Reuse and symmetry** — intended mirrored/shared components remain linked/shared;
- **Surface and context** — material classes remain readable under project lighting;

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

Complete when the requested vehicle exists with approved stance/proportion, controlled primary surfaces, coherent panel/mechanical construction, usable wheel and articulation axes, appropriate representation/detail for target cameras, protected data intact, and applicable structural/visual checks passed or explicitly handed off. For a major build, **V1 and V2 are prerequisites** for claiming completed body geometry; V3 is required only for moving assemblies in scope, and V4 is a handoff record rather than automatic rig/export/GameReady acceptance. Document FAIL, unavailable/unknown evidence and required rework without declaring them PASS.

Stop and report instead of guessing when reference/blueprint conflict changes wheelbase or major body shape materially, required mechanical articulation cannot be determined from available evidence, target-camera/open-state requirements are missing but necessary to scope interior/underbody work, or a requested change would invalidate protected rig/UV/pivot contracts outside scope.

## Research basis

The practical rules in this specialist are distilled from Blender documentation and vehicle-production breakdowns covering Mirror/subdivision/modifier behavior, blueprint/reference reconciliation, stance-first blockout, body-surface continuity, wheel/tire and mechanical construction, high/low versus mid-poly choices, articulation and game-ready delivery. See [research notes](references/research-notes.md) for source URLs, source type and caveats.
