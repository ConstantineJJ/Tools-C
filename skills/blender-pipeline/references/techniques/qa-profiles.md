# Blender checks proportional to the change

The [foundation](../../../../docs/foundation.md) defines verdicts and evidence levels.
Select applicable checks; this does not weaken final delivery or protected data.
An expanded dependency or a newly discovered regression expands the checks.

| Change | During each meaningful iteration | Before completing the task |
|---|---|---|
| Local form | Changed evaluated mesh, named contacts, affected close/whole view, one protected alternate view | Scoped protected-data comparison and required views; reopen the saved candidate if it is the deliverable |
| Material/texture | Changed resources and shared users, channel/UV correctness, comparable actual-renderer image | Preserved form/resources, packed or resolvable files, final view and source/target limits |
| Parenting/pivot/hierarchy | World placement, parent relation/axis, affected instances, explicit functional transform test | Protected hierarchy and placement across all changed dependencies, saved-file verification |
| Final delivery | Required structure, views and contacts; declared export/target checks when requested | Independently open saved file, compare protected data, verify references/maps and inspect final images |

Do not rerun all unrelated meshes and render every scene after a tip adjustment.
Do not skip them when the tip uses a shared mesh, material or modifier whose other
users are affected. Preserve fixed comparison conditions and record concrete defects.

## Contacts

Use [selected-pair contact diagnostics](../../../../tools/blender_contacts.py) with
explicit object pairs and a project/feature-relative tolerance. It distinguishes
surface overlap, enclosed containment, proximity and separation; an allowed join
is an explicit expectation rather than a hidden exclusion. Open/non-manifold
surfaces cannot certify inside/outside. Ambiguous parity, thin gaps and coplanarity
remain review cases. No global scene-wide collision or motion certificate is implied.
Closed-volume classification assumes a non-self-intersecting evaluated surface;
edge closure alone does not validate that assumption. `separated` reports no found
surface crossing/containment or sampled near contact; it does not prove a minimum
clearance greater than the tolerance.
The [Blender BVHTree implementation](https://github.com/blender/blender/blob/main/source/blender/python/mathutils/mathutils_bvhtree.cc)
uses triangle intersection for overlap and nearest points for distance queries;
the volume classification and sampling limits belong to this helper, not Blender.

## Protected snapshots and fresh loading

[Blender snapshots](../../../../tools/blender_snapshot.py) accept optional named
data categories. Choose source geometry, UVs, normals, shape keys, weights,
modifiers, material graphs and curves according to what must survive. Omitted
categories are not protected by that snapshot. Exact representation equality does
not prove visual equivalence or export preservation.

After independent reopening, update each scene's view layers before comparing
evaluated world matrices. Compare source data separately from dependency-graph
evaluation; do not remove cameras/lights to silence a stale-evaluation mismatch.

## Long operations

[Curve batch operations](../../../../tools/blender_jobs.py) create typed, named
curve batches in timer chunks and expose queued/running/completed/failed/cancelled
status. Inspect the same operation ID after a response timeout; do not replay a
mutation with a new ID until the original outcome is known. Cancellation preserves
partial output for explicit recovery. The existing Python preflight and bridge
safety gate still apply. Arbitrary executable jobs are not accepted.
If this chat's tool discovery lacks the two named operation tools, use the existing
`execute_blender_python` bridge with `runpy.run_path` and these same typed helper
functions. Keep the same ID and safety gate; do not replace status tracking with
blind generic execution after a timeout. Parenting helpers expect fresh evaluated,
unconstrained object matrices; animation/constraints/bone dependencies need the
corresponding owner and a scoped transform check.
