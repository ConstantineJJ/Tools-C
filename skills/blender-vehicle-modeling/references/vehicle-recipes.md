# Vehicle modeling — class-specific quick recipes

Read the parent [vehicle specialist](../SKILL.md), active project profile and approved PASS 0 / Model Contract first. This is a practical execution aid, not a separate modeling owner, design authority, mandatory one-size-fits-all pipeline, or authorization to edit an existing rig. For major new geometry, use the [vehicle QA and measurement gates](vehicle-qa.md). Skip irrelevant operations for a narrow correction.

## Recipe A — passenger car, sports car, compact pickup or stylized car

1. **Establish datums.** Choose documented forward/right/up directions, ground plane and units. Place four wheel-center markers, nominal tire envelopes, axle centerlines and a single vehicle envelope. Check wheelbase, tracks, ride height, front/rear overhang and roof/cabin ratios from orthographic views. If the design is fictional, treat these as locked *design* measurements, not inferred real-world facts.
2. **Make a recognisable neutral blockout.** Build hood, roof, glasshouse, rear mass, beltline and shoulder/fender volumes without lights, grills, door handles or busy vents. Compare front/side/rear/top and approved target-camera 3/4; obtain V1 before sculpting details. For strongly stylized bodies, identify the identity-defining non-car features as protected anchors.
3. **Create broad body panels as low-density controls.** Begin with continuous primary curves; use Mirror while symmetry holds, with correctly located mirror plane. Add only enough edges to control wheel arches, hood-fender transitions, waist/shoulder line, A/B/C pillars and roof crown. Test silhouette in matte/clay and curvature in a simple neutral highlight/reflection pass; fix pinches and waviness while topology is still easy to edit.
4. **Obtain V2 clay/curvature acceptance.** Compare like-for-like camera, orthographic and reflective views at target distance. If profile or reflection flow fails, return to step 2/3; do not hide this with dirt, glossy paint, trim or subdivision density.
5. **Separate purposeful boundaries.** Doors, hood, tailgate, glass seals and fascias can use separate meshes, recesses or surface detail depending on animation and budget. Place axes for every required opening and ensure clearance; avoid carving every seam into the main shell.
6. **Build reusable modules.** Tire, rim, hub, brake, headlights, handles, mirrors, wipers and underbody depth according to visibility. Reuse linked assemblies while truly identical; keep fictional hardpoints (spoiler, weapon mount, roof rack) separate, named and anchored.
7. **Validate articulation and delivery scope.** Sample both steering extrema and any suspension/opening states, measure V3, then pass to surfaces, rigging/animation and engine owner only as requested. Keep high/low/mid-poly representation conditional on camera and performance budget.

**Mini acceptance:** four axle/wheel markers and body scale are recorded; V1/V2 inspected; wheel and panel pivots make mechanical sense; no cosmetic additions mask an unresolved silhouette.

## Recipe B — motorcycle or scooter

1. **Fix two wheel centers, tire radii, wheelbase and contact plane first.** Choose the intended stance, fork rake/trail only when reference or design supports them; record which measures are known and which remain provisional.
2. **Build the load-bearing outline.** Mark steering head and front fork axis, swingarm pivot, rear wheel hub, engine/powertrain envelope, tank, seat and rider/footpeg space. For scooters, substitute the relevant step-through/floorboard/swingarm construction rather than forcing a sport-bike frame.
3. **Verify side silhouette *and* 3/4 depth.** Inspect handlebar width, fork offset, tank/seat relationship, engine exposure, exhaust route and tire/fender gaps as proxy masses. V1 must precede small bolts, cables, tread or decals.
4. **Develop visible mechanics in relation to pivots.** Build fork legs and triple clamps, frame, rear swingarm, chain/belt/driveshaft only when required, brake and hub alignment; check that attachments have logical paths and space.
5. **Apply V2 and V3 deliberately.** Check shiny or neutral highlight flow on tank/fenders; test fork steering around the steering-head axis, rear wheel rotation about its actual axle, suspension at rest and agreed min/max travel, and interference with brake lines, fenders and frame where represented.
6. **Organize modular, rig-ready objects.** Front wheel/fork/handlebars, frame/powertrain, rear wheel/swingarm and optional springs/cables stay separated only as necessary for the planned motion. Retain neutral transforms and original axes after previews.
7. **Texture/detail by visibility.** Spend geometry on the tank silhouette, brake/fork outlines, rider-facing controls and exposed motor; bake tiny fasteners, tread and cables when enough at game camera distance.

**Mini acceptance:** steering-head, swingarm and both wheel axes are named and measured, required articulation samples reviewed, identity and rider clearance preserved. A concept motorcycle need not imitate unknown engineering to claim reference fidelity.

## Recipe C — heavy truck, utility vehicle, multi-axle hauler or trailer

1. **Start with chassis + axle stations.** Mark front and every rear/bogie axle, wheel/tire envelope, chassis rails, frame width, ground plane and overall truck/trailer envelope. Record all axle-to-axle distances; do not describe a multi-axle chassis by one ambiguous wheelbase.
2. **Block the primary hierarchy.** Cab, engine hood if present, wheel arches, cargo bed/container, equipment frame, step rails, fuel/battery tanks and hitch/coupler. Confirm cab-to-bed and front/rear mass ratios in side, rear, front, top and 3/4.
3. **Run V1 before accessory escalation.** Test recognisability at camera distance, load space/ground clearance, wheel-set spacing, cab silhouette and overall mass distribution. Trucks from specific regions or periods need source-correct cab, mirrors, grille and cargo forms; do not mix random aftermarket details.
4. **Build mechanical attachment paths.** Cross-members and visible frame, spring/airbag/damper envelopes, steering axles, tandem bogie grouping, cargo mounts and any trailer articulation. Model hidden mechanical detail only to the extent it matters to visible states.
5. **Run V2 for large surfaces.** Inspect cab roof, front fascia, fenders, box sides and cargo silhouette in clay and controlled neutral highlights. Check repeated parts and intentional asymmetric exhaust, tanks, ladders or cargo hardware.
6. **Run V3 using appropriate states.** Check front steering and neighboring wheel/arch clearance, representative suspension envelope, cab/door opening, loading/tailgate movement and trailer yaw/pitch about the actual coupling when those states are required. Validate safe visual clearances, not physics performance or load capacity.
7. **Build tertiary modules last.** Lamps, mirrors, grilles, steps, straps, marker lights and other characteristic details come after macro and mechanics. Reuse wheel/tire, axle and frame modules; atlas/bake repetitive microdetail where needed.

**Mini acceptance:** axle station map, cab-to-frame anchors, wheel-set pivots, trailer/hitch relationship if applicable, inspected V1/V2 evidence and the applicable V3 motion samples.

## Cross-domain handoffs

- The [visual PASS 0](../../visual-reference-reconstruction/SKILL.md) owns concept/source certainty. Vehicle work consumes one Model Contract, it does not mint competing identities.
- The [robot/mechanism specialist](../../blender-robot-mechanism-modeling/SKILL.md) may supply techniques for a requested complex articulated module; the vehicle specialist retains overall wheel/chassis/body ownership.
- [Surfaces](../../blender-pipeline/references/surfaces.md), [rigging](../../blender-rigging-skinning/SKILL.md), [animation](../../blender-animation/SKILL.md), [polishing](../../blender-posteffects-polishing/SKILL.md), [export](../../blender-export-validation/SKILL.md) and engine integration keep their existing ownership.
- Examples are artist practice, not universal machine specs. No hard-coded triangle counts, tire sizes, steering angles or tolerance percentages.

## Evidence basis (research, not new authority)

- Irfan Haider, *Modeling Vehicles for AAA Games* (2019): dimensions + proxy box + wheel cylinders first; inspect orthographic and real player camera; optimize visible silhouette. https://80.lv/articles/modeling-vehicles-for-aaa-games
- Michael Neocleous, *Recreating Mad Max's Interceptor* (2021): clean, editable simple base geometry and proportional blockout in Blender. https://80.lv/articles/recreating-mad-max-s-interceptor-using-blender-substance-3d-painter
- Alexa Ranzola, *How to Model a Realistic Bike* (2026): multi-angle reference, distinct assemblies, prominent vs baked minor details; the motorcycle recipe's pivot checks are a Tools_C engineering extension rather than a direct quote. https://80.lv/articles/how-to-model-a-realistic-bike-based-on-a-2013-harley-davidson-sportster
- Manish Rawat, *Vehicle Modeling and Texturing* (2019): local truck authenticity, primary/secondary/tertiary blockout, source-correct accessories and staged low-poly. https://80.lv/articles/001agt-002mrs-how-to-model-a-local-truck
- Bicycle construction and pivot-relative anatomy: *Recreating a Takhion Bicycle* (2022), a reference-based geometry workflow, not a compulsory bicycle manufacturing standard. https://80.lv/articles/recreating-a-takhion-bicycle-in-blender-substance-3d-painter-marmoset
