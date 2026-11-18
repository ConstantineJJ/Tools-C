# Functional detail and mechanisms

Owner: [weapon module](../SKILL.md). Use during W2 (function map) and W3 (mechanisms).
A detail earns its place when it answers an anatomy line, sits where that function
would physically act, and reads at the target camera. Otherwise remove it.

## Detail grammar

| Detail | Function it shows | Place it where | Avoid |
|---|---|---|---|
| Sight, optic, sensor | Aiming | On the aiming axis, clear line of sight, rigid mount | Optic blocked by other parts or skewed to the bore |
| Indicator lamp | State: charge, ready, heat, fault | Near the system it reports, visible to the operator/camera | Lamps scattered evenly as decoration |
| Vents, fins, heat sinks | Heat removal | Around the heat source (chamber, emitter, coils), open to air | Vents on a sealed, cold or hidden face |
| Handles, grips, lifting eyes | Carrying, servicing, swapping | Balance points, access panels, removable modules | Handles that a hand or hook could not reach |
| Brackets, clamps, collars | Holding one part to another | At joints and load transfer points, sized to the load | Floating parts with no visible attachment |
| Fasteners | Panel removal, assembly | Panel edges and flanges, consistent size per panel | Uniform bolt rows on every face |
| Access hatch, panel line | Maintenance, part boundaries | Over serviceable internals | Panel lines crossing hinges or moving parts |
| Cables, conduits, hoses | Power, data, coolant flow | Source to consumer, clipped, with slack across joints | Cables that would pinch, stretch or end nowhere |
| Hazard stripes, markings | Danger zones, orientation, ID | Muzzle zone, moving parts, high voltage, lifting points | Stripes as filler colour |
| Counterweight, armour plate | Balance, protection | Behind/around fragile or heavy parts | Armour that blocks function (vents, optics) |
| Muzzle device, emitter | Output and its effects | At the bore face, coaxial with the barrel | Off-axis emitters, no marker |
| Wear, scuffs, soot | Use history | Contact, handling, heat and ejection paths | Uniform edge scratches everywhere |

Colour accents: keep the base material dominant and use accent colours sparingly for
function (energy path, hazards, controls, identity). Emission marks energy or state,
not random surfaces. Stylized wear exaggerates hierarchy; it still follows use.

## Mechanisms

Model the load path and both extremes of motion. Put origins on physical axes, keep
each moving part a separate object, and state travel and clearance.

| Mechanism | Must show | Check |
|---|---|---|
| Piston / actuator | Cylinder and rod, an eye or clevis at each end, brackets on two different bodies | Retracted length ≥ stroke + housing; rod stays inside the cylinder at full extension; pivots move on arcs without clipping |
| Spring | Seats at both ends, a guide rod or tube | Compressed length > coil-bind length; spring sits between parts that move relative to each other |
| Gear train | Meshing partner, axle and bearing or housing | Matching tooth size, centre distance = sum of pitch radii, sensible ratio (small drives large for torque) |
| Winch, drum | Drum with flanges, cable anchor, fairlead or guide, brake or motor | Cable leaves tangentially toward the guide; drum mounted on a frame |
| Rail, slide | Rail fixed to the frame, carriage with bearings, end stops | Carriage travel stays on the rail; stops at both ends |
| Hinge, hatch | Hinge axis on the edge, knuckles, stop or latch | Opened state clears neighbours; axis matches the origin |
| Rotating barrel / drum | Central axle, bearing collar, drive gear or motor | Barrels are equal and evenly spaced around the axle |
| Recoil / buffer | Sliding barrel or block, guide, buffer spring or damper | Recoil travel is along the bore axis and clears the mount |

A mechanism that cannot be finished honestly (missing anchors, impossible travel)
becomes a simple covered housing instead. A covered housing is a valid design choice;
a fake mechanism is a defect.

## Mid-poly readability

- Use bevels with weighted normals for the main readable edges; skip bevels on
  edges that will never catch light at game distance.
- Prefer insets, panel cuts and layered plates over floating micro details.
- Check silhouettes at the real camera size: if a part disappears, remove or enlarge it.
- Repeated parts share mesh data; mirror only while left/right are truly identical.
