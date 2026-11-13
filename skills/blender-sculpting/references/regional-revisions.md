# Regional revisions on developed assets

Use for authorized shape changes at any stage. Initial form hierarchy guides
efficient construction; it does not prohibit later user-directed proportion edits.
Do not restart modeling, discard approved detail, or infer agent fault from the
stage at which a user requests a revision.

## Select the least destructive representation

| Current asset and change | Useful route | Check afterward |
|---|---|---|
| Production mesh, sufficient local density | Fixed-topology Move/Grab, bounded relaxation, cage/lattice where suitable | Vertex identity, UVs, weights, shape keys and protected forms |
| Clean existing Multires sculpt, broad change | Work at a suitable lower subdivision level; return to higher levels | Detail distortion and transitions at every relevant level |
| Disposable sculpt, large volume/topology change | Local rebuild or voxel remesh with recoverable source | Thin parts, gaps, normals, lost/reprojected attributes and downstream bindings |
| Existing eyelid/ear root cannot support intended form | Reconstruct a bounded patch and its transition | Eyeball/root clearance, skin continuity, shading and coat coverage |

These are choices, not a universal recipe. Multires allows broad changes at low
levels even after detail exists. It does not permit arbitrary base connectivity
changes without corrupting subdivision correspondence. Voxel remesh rebuilds
source topology; it ignores the modifier/shape-key result and is unavailable on
an object with Multires. Attribute transfer options are not a vertex-ID guarantee.

## Protect volumes as well as surface vertices

Describe the changed region, coordinate frame, displacement intent, falloff,
transition and protected neighbors. Masks and Face Sets isolate influence but do
not test hidden collisions. Protect eyeball, mouth cavity, ear opening and joint
clearance volumes explicitly when relevant; inspect sections or intersections.
Do not fix an eyelid ridge by pushing arbitrary cheek volume through the eye.

For broad support changes use a smooth displacement field/cage or a rebuilt
surface with a controlled boundary. Repeated smoothing can shrink or flatten a
surface without resolving its construction. Use mask boundaries and suitable
fairing/relaxation only where they preserve the intended landmarks. Inspect the
result, not the brush/operator name. A failure to improve calls for diagnosis of
registration, topology density, falloff, construction or dependency binding before
another equivalent operation. After two equivalent failed attempts on the same
defect, change the hypothesis/representation before trying again. Compare the
same feature and views; this is not a quota on user revisions or a full restart.

For scripted containment in a closed, consistently evaluated mesh, sort ray
crossings and classify individual entry/exit intervals with robust edge/tangent
handling or a suitable inside/outside method. The midpoint of the first and last
hit may lie in a gap of a concave/disconnected volume. Open/non-manifold or
ambiguous surfaces require an explicit uncertainty result. Numerical containment
still does not prove an anatomically valid attachment. This is an implementation
requirement for scripts using containment, not a claim of a new universal checker.

## Repair dependent surfaces

List affected dependents before the change; after the change inspect/rebind them
before claiming the scoped result. Include skin margins, teeth/eyes, ear bases,
whiskers, follicles, groom roots/directions, decals, color projection, UV/bakes and
contact surfaces as relevant. This dependency list is task-local, not a new schema.

For native Hair Curves use the correct surface and surface UV map, matching
transforms and rest/deformed position expected by the modifier stack. If the
surface UVs or topology changed, inspect attachment data and reattach/rebuild the
affected region. Snapping roots alone does not restore guide direction, regional
length, material sampling or coverage. Compare a sparse guide sample before a
full-density groom; keep the previous source recoverable until the repair works.

For a changed region use the short dependency order: skin → eye/ear contact →
roots/UV/rest positions → guide flow/length → pigment → whiskers. One sparse,
lit checkpoint should expose binding, length and color defects before density
increases. Increase topology resolution only for a named unsupported form or
detail; do not repeat a full SDF/remesh rebuild for a secondary fixed-topology fix.

Inspect clay skin, guides/roots and the final material/coat separately. Compare
the changed feature plus a second view/three-quarter view with fixed framing;
check nearby accepted features and requested dimensions. Run saved-file and
deformation checks when those outcomes are in scope. Document open criteria
without turning a local improvement into whole-asset acceptance.

Basis: [research notes](research-notes.md), Blender adaptive resolution/remeshing,
hair attachment documentation and the user's permitted late-stage revision use case.
