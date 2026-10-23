# Physics preparation, reconstruction and acceptance

Required with this skill. Use the current target engine/version and project
budget; example values are not presets. A mesh package and its engine behavior
are separate acceptance levels.

## Piece identity and recoverable assembly

Preserve an editable intact source and a known rest configuration before cuts or
origin changes. Record piece ID, source component/material, body/cluster owner,
proxy IDs, support/connection pairs and rest transform relative to the asset root
(including parent and units/axis convention). Use an existing assembly graph or
a concise task-local table. If PASS0/Model Contract is already present, preserve
its binding rather than inventing a second design authority.

Moving an origin must preserve world-space vertex positions. Store the updated
rest transform after the origin change; retain the old baseline for comparison.
Restore hierarchy and transforms by ID, not by object-list order or current
selection. Keep inspection/exploded poses and simulation caches separate from
authored rest. Clustering may change bodies without losing the render-piece map.
Preserve the exact mapping in any rename/merge needed for export.

## Origins, pivots and mass

Separate placement root, fragment/body origin, center of mass and hinge/attachment
pivots. A common root supports interchangeable variants; individual fragments
need useful local frames for rotation/physics. Mesh-based Blender rigid-body
shapes use the origin as their center of gravity; primitive shapes can use their
geometric center. Verify the chosen shape's behavior instead of moving every
origin to an unweighted vertex average. A hinge pivot is not automatically the
mass center. Engines can recompute mass properties from imported shapes.

Resolve negative/nonuniform scales on scoped copies while preserving placement,
parent behavior and rest transforms. Verify dimensions after applying scale;
never apply transforms indiscriminately to rigs, animation or shared sources.

Use positive finite mass with credible relative density/volume or an explicit
gameplay allocation. For uniform-density closed solids, m = density × volume is
a useful starting estimate. Open/nonmanifold meshes and overlapping shell layers
cannot supply a trustworthy signed-volume mass; use a justified shell estimate
or authored mass instead. Keep units explicit. Compare the sum of physical piece
masses with the intended object mass, accounting for anchored parts and omitted
visual debris. Equal mass per shard usually makes tiny pieces implausibly heavy.
Do not port numerical break strengths across solvers as if their units match.

## Collision-friendly representation

Prefer simple primitives for board-like/block-like pieces, a modest convex hull
for convex rubble, and a bounded compound of simple/convex shapes for important
concavities. Dynamic concave triangle meshes are not a portable assumption.
Godot dynamic fragments need supported primitive/convex shapes; static concave
collision has a different role. A convex hull fills cavities: inspect doorways,
broken rings, hollow boxes, bent panels and cups rather than accepting the hull
because it encloses all vertices.

Maintain render/proxy correspondence without duplicating visible detail in
collision. Tiny fasteners can share a body; a compound shape is still one body
but incurs multiple shape/contact costs. Track both. Keep helpers/proxies out of
render export unless target naming/import rules explicitly consume them.

Check proxy geometry at **assembled rest**, not only after exploding the view.
Margins/contact offsets relative to thickness can make touching pieces repel or
hover. Do not prescribe zero margin globally. Inspect the actual target's margin
convention, local overlaps, scale and solver support before adjusting it.
Disable/replace intact collision when fragment collision becomes active; never
simulate two overlapping representations of the same volume. Intentional joint
contacts need the planned collision filtering/constraint policy.

Thin/fast shards may tunnel. Prefer viable proxy thickness and appropriate
velocity/CCD settings supported by the target before increasing solver cost.
Sleeping, collision layers, cleanup and pooling must match gameplay and reset;
visual disappearance alone does not prove a body stopped simulating.

## Supports and activation

Separate anchored/static remainder, kinematic staging and active fragments.
Define what stays attached before and after the event; store intended
connectivity/bonds where the engine consumes them. A shared parent does not by
itself create a physical constraint. Do not assume all near-touching pieces bond.
Stage or cluster activation if useful, but count the worst simultaneous leaf-body
burst, including multiple destroyed instances and transient overlap at swapping.

Preview quietly at rest before impact. An untriggered asset should not fall apart
or gain explosive energy because neighboring proxies overlap. Then exercise the
actual trigger and relevant impact directions/magnitudes. Do not tune physics
until all material differences disappear merely to make a preview stable.

## Verification checklist and limits

Select checks proportional to the requested deliverable. Name each result and
its evidence; do not promote lower-level checks into higher acceptance.

| Gate | Evidence and failure criteria |
|---|---|
| Source preservation | Compare intact source and protected users/data against baseline; changed source/artwork/rig outside scope is a regression |
| Geometry/interiors | Inspect newly exposed faces, normals, zero-area/sliver faces, relevant nonmanifold edges, duplicate caps, material assignment and UV test pattern; reject unintended holes or unsupported skins |
| Rest reconstruction | Restore all pieces by stored IDs/parents/rest transforms, compare outer bounds/silhouette and selected surface samples to intact source within task tolerances; inspect seams and material continuity |
| Fragment intersections | Broad-phase bounds produce candidate pairs only; inspect/contact-test candidates with actual mesh/proxy geometry, distinguishing intended touching cuts from penetration and duplicate volume |
| Budget | Count render pieces, active bodies, shapes/hulls, constraints and requested simultaneous instances; exceeding the agreed budget is FAIL, unmeasured performance stays OPEN |
| Visual breakup | Review material-specific silhouettes and size distribution, supported remainder and exposed interiors at gameplay distance plus relevant closeups; still images do not prove timing or feel |
| Export/fresh import | Export selected variants/proxies as contracted, fresh-import separately, match IDs/body map, rest transforms, scale, bounds, UV/material roles and reconstructed assembly; document intentional triangulation/splitting |
| Engine/runtime | Run actual target import/activation/impact/settling, check collisions and the gameplay opening/cover, switch/reset twice and inspect another instance; measure worst-case body/contact/frame cost when budget acceptance is requested |

For a complete solid partition, compare represented volume as well as outer
surface; exterior-only similarity can hide missing internal pieces. Sum of
volumes alone can hide overlap plus a compensating gap. Use both coverage and
intersection evidence appropriate to closed solids. Hollow/assembled objects
need component/shell coverage instead of a false solid-volume claim. Any cutter
gap, simplification or omitted debris must have an explicit tolerance/rationale.

Reset/reassembly clears velocities, transient constraints and stale simulation
state as required by the target, then restores the intact visibility/collision
policy and fragment rest transforms. Test repeated activation/reset to catch
duplicate body creation, cumulative drift or retained impulses.

## Delivery boundaries

Read [export validation](../../blender-export-validation/SKILL.md) when output is
requested. Supply piece IDs, body map and parent-relative rest transforms plus
target proxy naming/import expectations. Standard mesh GLB export alone does
not recreate Blender rigid bodies, breakable constraints, Chaos collections or
an engine damage system; preserve those settings in the target wrapper or an
explicit supported metadata/sidecar handoff and verify what was consumed.

For Godot, read [asset integration](../../godot-asset-integration/SKILL.md) and its
scene-ownership reference before wrapper/resource changes. Keep authored physics
and reset logic outside imported content that reimport replaces. For Unreal or
another engine, use the actual project integration procedure and installed
version's official docs; do not invent a Tools_C owner or treat Blender cell
pieces as an automatically configured destruction system.

If runtime was not requested/available, deliver the scoped asset evidence and
mark target physics/performance SKIP with reason. No saved Blender file, rest
snapshot, successful operator or valid GLB alone establishes engine readiness.
