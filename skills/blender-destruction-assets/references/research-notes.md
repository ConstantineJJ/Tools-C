# Research and source boundaries

Researched 2026-10-17. Primary vendor documentation and professional learning
material inform this skill; procedures are a Tools_C synthesis, not copied
tutorials. Houdini concepts inform Blender authoring decisions and do not add a
Houdini dependency. Engine UI/settings must be rechecked for the installed version.

## Material and construction

- [SideFX: RBD Material Fracture](https://www.sidefx.com/docs/houdini/nodes/sop/rbdmaterialfracture-.html).
  Describes separate concrete, wood and glass methods, local control and clustering.
  Its glass method is explicitly for flat panes, not curved glass. This supports
  choosing a material/piece model before an operator; it does not make the same
  Houdini algorithm available in Blender.
- [SideFX: Introduction to Material Based Destruction](https://www.sidefx.com/docs/houdini/destruction/tutorials/intro_to_mbd_2.html).
  A mixed wall example distinguishes wood members, drywall and glazing. It
  demonstrates why fracture orientation must be evaluated per member, why
  between-material connections differ from within-material bonds, and how proxy
  geometry can drive detailed pieces through stable names. Tutorial strength
  values are example-specific and must not become cross-engine defaults.
- [SideFX: Destruction overview](https://www.sidefx.com/docs/houdini/destruction/overview.html).
  Pre-fracture gives artistic control; lower-resolution proxy geometry and named
  pieces separate simulation from rendered complexity. This motivates explicit
  render-piece/body mapping, not a requirement to pre-fracture every asset.

## Exposed surfaces

- [SideFX Labs: Inside Face UVs](https://www.sidefx.com/docs/houdini/nodes/sop/labs--inside_face_uvs-1.0.html).
  Interior faces need explicit UV treatment and inside/outside classification;
  generated cuts do not imply useful UVs. The skill retains exterior artwork and
  treats cut substrates separately.
- [SideFX: Fracturing objects for simulation](https://www.sidefx.com/docs/houdini/dyno/fracturing.html).
  Describes local fracture controls and an interior-detail operation. This informs
  localized detail after a usable primary partition rather than noisy cuts on
  every component.

## Physics and realtime cost

- [Blender Manual: Rigid-body collisions](https://docs.blender.org/UATEST/manual/en/dev/physics/rigid_body/properties/collisions.html).
  Retrieved official development-manual mirror; version banner can change.
  Describes primitive/convex/mesh/compound choices, shape-dependent center of
  gravity and margin behavior. Main current-manual URLs could not be fetched by
  the research browser. Use the installed Blender version's documentation/API
  before operations; do not infer that all origins or margins behave identically.
- [Epic: Cluster Geometry Collections](https://dev.epicgames.com/documentation/unreal-engine/cluster-geometry-collections-user-guide-in-unreal-engine).
  Describes staged fracture hierarchy and clustering's collision benefit. Embedded
  visual geometry adds detail without becoming collision/simulation geometry.
  These principles inform coherent clusters and decorative attachments; they do
  not guarantee a performance budget for a particular asset or machine.
- [Epic: Destruction Quick Start](https://dev.epicgames.com/documentation/en-us/unreal-engine/destruction-quick-start).
  Establishes Geometry Collections and strain applied through a connection graph.
  An exported set of meshes is therefore only source content for this runtime
  system, not proof that the runtime system was configured or tested.
- [Godot: Collision shapes (3D)](https://docs.godotengine.org/en/4.4/tutorials/physics/collision_shapes_3d.html).
  Version-pinned 4.4 reference: favors simple shapes for dynamic bodies, describes
  convex/concave tradeoffs and the cost of many shapes. Recheck the target Godot
  version and physics backend before integration.
- [Blender Manual 3.2: Cell Fracture](https://docs.blender.org/manual/en/3.2/addons/object/cell_fracture.html).
  Historical workflow reference only. It advises starting small and describes
  the old add-on/operator path. Its bundled-add-on installation claim is not
  current-version evidence; check actual availability rather than silently
  installing or assuming an old menu path.

## Synthesis, assumptions and remaining acceptance

The crate/masonry/glass/metal/plastic recipes, rest-transform handoff and acceptance
matrix adapt those principles to Tools_C game-asset work. Specific material
subtypes and connection failures need visual/construction references. In
particular, laminated glass, ductile tearing, layered plastics and gameplay
mass/threshold choices are design decisions to justify, not a claim that a vendor
tutorial supplies a physically predictive model for every case.

No universal fragment count, density, cut noise, solver iteration, CCD threshold
or frame-time promise follows from these sources. Eight bodies versus one hundred
is an illustrative budget decision from the brief. Source-backed instructions,
catalog tests and LIVE loading do not prove a real generated asset's fracture
quality, reassembly/export fidelity or target-engine performance; those require
the asset-level evidence specified in the skill.
