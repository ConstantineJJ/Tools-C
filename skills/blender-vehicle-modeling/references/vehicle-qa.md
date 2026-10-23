# Vehicle geometry QA — measured datums and gated acceptance

This reference defines a *repeatable review procedure*, not a numerical tolerance standard or a new checker implementation. Use only for new/major vehicle geometry, vehicle-related reconstruction or the named impacted checkpoints of a surgical correction. Read the [vehicle specialist](../SKILL.md), project/profile, current Model Contract, [Blender evidence](../../../docs/blender-evidence.md) and [verification](../../verification/SKILL.md). Do not confuse data collection, image capture or successful test scripts with actual artistic acceptance.

## V0–V4: stage gates without a second contract

| Gate | Entry / required proof | Decision / failure route |
|---|---|---|
| **V0 — source and measurements** | User goal, vehicle class, source authority, target cameras, project units/coordinate basis, axle/hardpoint register, approved PASS 0/Model Contract where applicable, recovery baseline | If mandatory identity/dimensions are unresolved, record UNKNOWN/BLOCKED; do not invent a real-world spec or reconstruct hidden mechanics |
| **V1 — neutral blockout / stance** | Untextured proxy mesh, all intended wheel/axle centers, body/cab/cargo envelopes; measured baseline; inspected front/side/rear/top and target 3/4 at matched framing | FAIL blocks panels, grills, detailed wheels, UV, wear and ornament; return to proportion/blockout owner |
| **V2 — developed clay / primary surface** | V1 passed; major fenders, glasshouse, roof/hood/tank/cab/cargo and broad panel volumes; matching matte/clay and controlled neutral highlight views, inspected for shape, reflection flow and silhouette | FAIL blocks tiny trim, decorative surfaces and final polish; fix source geometry/curvature, not gloss, modifiers, decals or generated reference reinterpretation |
| **V3 — mechanical/articulation** | Stable geometry, named wheel/steer/swingarm/door/hood/hitch axes; before/after neutral transforms; sampled *required* joint and clearance states with numeric results | FAIL blocks rig/animation handoff for affected mechanisms; UNKNOWN/SKIP is explicit if movement is out of scope or unavailable |
| **V4 — scoped handoff** | V1–V3 applicable records, clean object hierarchy/instances, source/contract revisions, chosen representation/LOD/material interfaces, target camera evidence, unresolved owner gates | Geometry completion only for proven scope; UV, rig, GLB, engine behavior and game-ready status remain separate owners |

For a *narrow edit* check the affected gate(s) and impacted protected data only. For example, a requested wheel-pivot correction needs V3 and enough V1 reference to prove its location, but does not rerun all body/modeling stages. Preserve previously accepted gates unless the current change invalidates their source/revision. Existing project QA receipts and statuses remain authoritative; do not create a competing ledger or schema.

## Measurement convention (record this before numbers)

Use the **agreed vehicle-local orthonormal frame**: F = longitudinal/forward unit vector, R = lateral/right unit vector, U = up unit vector, origin O. Record ground plane, scene unit scaling and reference/contract revision. These are conventions for projection; they do not impose Blender world axes or Godot import axes.

For point P, measured local coordinates are: f = dot(P-O, F); r = dot(P-O, R); u = dot(P-O, U). Use evaluated transforms/geometry when modifiers, parenting or unapplied object scale change actual dimensions.

| Quantity | How to obtain it | What the result proves |
|---|---|---|
| **Wheel center/hub** | Sample each hub/axle rotation center from evaluated object transform or explicit marker; record center coordinates, corresponding physical rotation axis and left/right identity | Rotation anchor alignment, not rolling/handling quality |
| **Wheelbase (two-axle)** | Absolute longitudinal difference between front and rear axle center averages in the local frame; for >2 axles report each station and spacing individually | Longitudinal axle layout, not suspension simulation |
| **Front and rear track** | Absolute lateral distance between corresponding left/right hub centers for that axle group; report separately when different | Axle width/stance, not contact patch physics |
| **Tire outside diameter and width** | Measure the evaluated tire envelope on axes perpendicular/parallel to the wheel spin axis, distinguishing rim and tire; include tread if represented | Visual tire envelope rather than a generic cylinder radius |
| **Ride height / body ground clearance** | State neutral/reference stance and ground plane; measure minimum relevant *non-wheel* underside-to-ground separation using actual evaluated geometry or explicit sampling. Distinguish clearance at fixed points from whole-body minimum | Visible static clearance under the declared pose, not off-road capability |
| **Front/rear overhang** | Longitudinal distance between body exterior extremum and the relevant outer axle station (sign/direction explicit) | Front/back packaging proportion |
| **Steering/head/fork/swingarm/hinges** | Axis defined by origin + normalized direction, parent/child hierarchy, expected rotation limits or UNKNOWN, sampled neutral/extreme states | Mechanical placement and intended range, not a functioning rig |
| **Interference/clearance** | In evaluated pose(s), inspect wheel-to-arch, tire-to-suspension, door-to-body, fork-to-frame, cargo-to-frame and hitch-to-trailer as applicable. Use mesh intersection/BVH or reliable closest-surface queries for precise claims; AABB-only overlap is a *candidate*, not collision proof | Geometry overlap/clearance only for tested states; no claim of continuous sweep unless swept or adequately sampled |

**Tolerance policy:** expected value/range and permitted deviation must come from the user's approved reference, project profile or Model Contract. Where absent, report the measured values and acceptance as REVIEW_REQUIRED/UNKNOWN rather than inventing a universal +/- percentage, angle or millimeter. Stylized vehicles deliberately may exceed standard real-world proportions. Do not average incompatible reference views to manufacture authority.

## How to perform the evidence pass

1. **Freeze comparable presentation.** Record camera matrices, orthographic scale or FOV, view, crop, object state, scene units, source revisions and actual file/scene identity; inspect returned images, not just paths. For V1/V2 capture front, side, rear, top (where possible) and source-matched 3/4 plus the actual gameplay camera if distinct.
2. **Visual separation.** V1 matte/clay answers *silhouette, volume, stance*. V2 neutral clay answers *secondary form*. V2 a simple controlled highlight/reflection material and same lighting answers *pinches, waviness, panel continuity*. A beautiful car-paint render cannot substitute for clay or original design comparison.
3. **Export local numbers.** Record for each measurement: ID/region, expected source/contract range or UNKNOWN, actual value + unit/frame, deviation if expected known, stage/pose, measurement method, inspected visual path and confidence/limitations.
4. **Exercise mechanics non-destructively.** Duplicate/restore recoverable state or use temporary transforms that can be reliably reverted. Sample named relevant angles/travel/poses; a zero-pose check alone never proves steering/door/suspension clearance. Compare evaluated meshes, mirrored/linked wheel data, parent transforms and origin placement.
5. **Record review verdict.** Use the existing Tools_C PASS / WARN / FAIL / SKIP semantics with evidence and remaining owner. Add REVIEW_REQUIRED/UNKNOWN wording only as an explanation for an unresolved visual or numeric criterion; do not relabel unsupported claims PASS. Gate status must respect the parent verification/QA protocol.
6. **Act on FAIL.** Keep V1/V2 structural defects with vehicle-modeling; UV/bake/material defects route to surfaces; moving rig mechanics beyond geometry to rigging; gameplay wheel physics to Godot; runtime/GLB acceptance to their owners.

## Compact measurement receipt (example schema for a note, NOT a new mandatory file)

Example, with intentionally invented sample numbers to demonstrate formatting only:

- Subject: SampleTruck; contract: placeholder; local F/R/U basis: documented; ground plane: declared.
- VEH-WB: front/rear axle stations; expected: UNKNOWN; actual: measured in scene units; status: REVIEW_REQUIRED.
- VEH-CLR: chassis point/ground clearance; neutral and compressed pose; expected: project-specific; actual: measured; status based on that declared tolerance.
- VEH-STR: left/right tire arch at min/neutral/max representative steering; collision method and results; status: recorded only for tested poses.
- V1 / V2 / V3: evidence image IDs, observer, findings and PASS/FAIL/SKIP; link existing task receipt/Pulse rather than duplicating it.

The example contains no real tested vehicle values; never copy it into a production QA claim.

## Source basis

- Irfan Haider, *Modeling Vehicles for AAA Games*: dimension proxy + wheel cylinders; orthographic and gameplay cameras; part-placement awareness. https://80.lv/articles/modeling-vehicles-for-aaa-games
- Michael Neocleous, *Recreating Mad Max's Interceptor*: simple editable base mesh, vehicle blockout and incremental panel refinement. https://80.lv/articles/recreating-mad-max-s-interceptor-using-blender-substance-3d-painter
- Manish Rawat, *Vehicle Modeling and Texturing*: truck blockout first, regional authenticity, tiered detail. https://80.lv/articles/001agt-002mrs-how-to-model-a-local-truck
- Blender Manual 4.5: Mirror relative to origin/Mirror Object and non-destructive modifier evaluation. https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/mirror.html ; https://docs.blender.org/manual/en/4.5/modeling/modifiers/introduction.html
- The axis-projection measurement definitions, sampled interference test protocol and gate labels here are **Tools_C engineering syntheses**, not quotes, official vehicle-industry tolerance standards or existing executable Blender validators.
