# Scoped QA and handoff

Use [QA profiles](../../blender-pipeline/references/techniques/qa-profiles.md) and
[verification](../../verification/SKILL.md); this reference specifies mechanical
criteria, not a competing general evidence system.

At macro/secondary clay gates, hide textures, decals, wear and microdetail.
Inspect front/side/rear/3/4 with neutral light, source-matched pose/lens and a
silhouette/landmark comparison. Mark rear review as proxy review if unseen.
Record reviewer, image paths/hashes, measured or estimated deviations and residual
uncertainty. Clean topology does not prove visual likeness or shell seating.

For mechanics use a registry-selected module test: joint origins remain fixed
under temporary rotation, child links retain length, actuator endpoints connect,
required samples have clearance, armor does not block travel and feet contact the
intended support plane. State tested angles/coverage. Restore transient test state.
No motion/physics/strength PASS follows from these static checks.

For geometry inspect evaluated meshes: zero-area faces, loose elements, unintended
open/nonmanifold boundaries, inverted normals/scales, bevel collapse and occlusions.
Some open sheets/channels may be intentional; judge by role rather than require
every object to be a solid. Capture pre/post triangle and object counts where
budgets matter. Use dimension/thickness-aware bevels rather than one global stack.

For material/wear stages retain a clean clay comparison. Verify material classes,
quiet regions and scale of wear; batch geometry damage by panel/material when
independent objects serve no useful editing purpose. Recheck holes after damage.
Packed 4K images and Blender-only triplanar materials do not certify UV atlas,
bake, glTF or target-engine behavior.

Deliver the editable assembly, graph/axes, source packet ID/hash, certainty-linked
part records, protected baseline comparison, stable pose/clearance results,
geometry/clay evidence and unresolved gates. If requested, reopen the saved file
independently with script auto-run disabled and compare evaluated counts, hierarchy,
matrix state and dependencies. Report simplified source contours as visual WARN.
Stop at the user's stage; downstream handoff is information, not authorization.
