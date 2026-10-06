# Assembly and mechanical design

## Part graph and certainty

Keep stable `part_id`, `role`, `module_id`, `parent_id`, `shared_mesh_id`, `pivot`,
`attachment_frame`, `material_group`, `contact_expectations`, `protected`, and
`pass0_claim_ids`. For speculative geometry add `certainty`, `assumption` and
`editable_proxy=true`. A graph stores structural interfaces separately from editor
grouping; collection membership/name alone does not authorize mutation.

Persist this graph as `assembly_graph.json`, with one `contract_ref` (id/revision/sha256)
to the [PASS0 Model Contract](../../visual-reference-reconstruction/references/model-contract.md).
Add component_id, instance_id and actual object_name to each part; one physical arm
shares an instance_id across shell/bearing/fastener meshes. Do not duplicate Contract
rules here. Capture measured checkpoint observations and a compact verification
receipt; check scene bindings, counts, locked proportions and critical links at G1
(MACRO), G2 (MECHANICS), clay geometry handoff (GEOMETRY) and G7 (FINAL), when in scope.
Crop in an auxiliary panel never changes barrel/link length; use the locked source
and supported envelopes. A revision is explicit and invalidates stale bindings.

Start with primary envelopes and changing cross-sections, then skeleton/link
lengths, then armor. Boxes are useful blockout, not final proof of torso curvature,
sloping shoulders, thick layered feet or stepped hubs. Exposed mechanical depth
must remain visible where the source shows it. Avoid uniform slabs and equally
dense detail on every module.

## Axes, bearings and actuators

Record joint ID, frame, axis, parent/child link, bearing envelope, visual travel
range and origin certainty. Put stepped hubs, seals and support forks around the
same axis. Support paths should connect the pod/arm/body rather than imply loads
carried by a floating plate or decorative cable. Without engineering data, call
range/clearance checks representative static checks, not a functional simulation.

For a two-link chain, distance `d` must satisfy `abs(L1-L2) <= d <= L1+L2` with
an explicit tolerance. Near singular straight/folded poses need review. Reject
unreachable targets before solving; numerical epsilon for roundoff must not hide
an invalid stance. Preserve rigid lengths. Choose a knee-bend plane explicitly.

For each actuator, name both mounting frames/points, the rod axis, minimum/maximum
mount distance and body/rod overlap. Inspect neutral and required bent poses for
attachment, stroke, body-shell intersection and joint clearance. Coaxial decorative
cylinders are not evidence of hydraulic routing. Cable bends and cooling pathways
are plausible design choices unless actually supported by sources.

## Armor, manufacturing and negative spaces

Treat frame, bearing, armor panel and cover as different roles. Frame sits inside
the outer shell with intentional clearance; a closed inner torso must not protrude
through red cheeks. Use changed sections, slopes, recesses and varying thickness
instead of adding bolts to a bad silhouette. Check armor coverage in clay.

Model a door as cover + seating frame + access volume when visible/needed. Put
fasteners on supported lands, hinges on consistent axes, overlaps in deliberate
order, and removal seams around plausible replaceable parts. Chamfers/radii should
match thickness and part scale; do not pretend cosmetic drawings are fabrication
specifications. Separate real gaps/cavities from decorative grooves.

A launcher/pipe channel is an assembly property. When a through-bore is required,
inspect shell, face block, sleeve, rear plate, decorative seams and later wear.
Use evaluated meshes and axial plus off-axis ray samples or suitable collision
probes over the stated radius/depth. State sample coverage/tolerances; discrete
rays cannot certify every point. If only a recess is supported, do not turn it into
an open through-channel without a recorded design decision.
