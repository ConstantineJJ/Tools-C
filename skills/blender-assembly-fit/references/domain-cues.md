# FIT_INTEGRATION — domain subgroups

Read the subgroup that matches the asset under review; a mixed asset (a robot with a
weapon, a vehicle with cargo props) uses each relevant subgroup on its own parts.
Cues are questions to confirm in the scene and captures, not defects by themselves.
The repair owner named per subgroup fixes; this skill only reports.

## G1 — Hard-surface machinery, robots, weapon modules

- **Seating:** plates, housings and pods sit on a land, collar, bracket or recess;
  a panel that floats 1–2 bevel widths above a curved surface reads pasted on.
- **Load path:** pistons need anchors at both ends, gears a partner and an axle,
  hoses and cables a start and an end. A dangling route is an I-03 question.
- **Shape language:** bevel width, corner radius and panel-line rhythm match the
  neighbouring primary form; a single part with a foreign radius reads imported.
- **Interfaces:** socket, muzzle and mount markers are protected data. Report a
  visual misalignment, never suggest moving the marker to make it look aligned.
- **Usual false positives:** visible fasteners and kitbash seams by design, motion
  clearance around joints, armour layers with intended gaps.
- **Views:** side and muzzle-facing/front for seating; three-quarter for layering;
  extreme poses only when they are already defined.
- **Repair owner:** robot-mechanism, weapon-module or props by asset type.

## G2 — Vehicles

- **Seating:** body panels meet with consistent gaps; lights, mirrors, bumpers and
  roof racks sit in recesses or on mounts, not on the paint surface.
- **Running gear:** wheels sit inside arches with plausible clearance; suspension
  parts connect hub to body. Gaps here are often intended travel, not defects.
- **Proportion:** a single accessory at a different detail density or scale than
  its peers (oversized bolts, toy-like antenna) is an I-04 question.
- **Usual false positives:** panel gaps, wheel-arch clearance, suspension travel,
  deliberately oversized stylised parts.
- **Views:** side and top for body fit; front for track and wheel seating; low_45
  for underbody connections.
- **Repair owner:** vehicle-modeling.

## G3 — Characters, creatures and wearables

- **Seating:** armour, straps, belts, pouches and accessories follow the body
  surface with a believable thickness and contact; a straight-edged plate over a
  curved shoulder reads foreign unless it is designed as rigid armour.
- **Deformation zones:** parts crossing joints (shoulder, hip, knee, neck) are
  questions for rigging, not fit failures in a single still pose.
- **Style:** silhouette and detail density stay consistent between body and
  accessories; anime or stylised exaggeration is intent, not a mismatch.
- **Usual false positives:** cloth and hair intersecting by a few millimetres,
  layered clothing, deliberate asymmetry.
- **Views:** front, side, back, high_45 and low_45; closeups at the joint.
- **Repair owner:** character, anime-character or animal-anthropomorphic modeling.

## G4 — Architecture, environment fixtures and props

- **Seating:** objects stand on the floor or a support, with feet or a base that
  touches; attachments to walls have a fixing (bracket, frame, anchor).
- **Construction logic:** beams rest on supports, roofs on walls, shelves on
  brackets; a modular piece with a mismatched edge or trim height breaks the kit.
- **Scale:** doors, steps, handles and railings stay at a consistent human scale
  within the scene unless stylisation is declared.
- **Usual false positives:** intentionally hovering decorative elements
  (`tc_floating=True` or a stated intent), set-dressing overlaps hidden from the
  game camera.
- **Views:** front and side for seating; top for layout; the game camera distance.
- **Repair owner:** architecture-environment, environment-assets, props or roads.

## G5 — Organic and vegetation assets

- **Seating:** trunks enter the ground, branches leave the trunk with a collar,
  leaf clusters attach to twigs; floating cards or detached clusters read wrong.
- **Usual false positives:** alpha cards that overlap by design, ground-cover
  intersections, wind-animated extremes.
- **Views:** side and three-quarter at game distance, plus a closeup at the base.
- **Repair owner:** vegetation or sculpting.

## Planned, not active

Automated `FIT_FLOAT`, `FIT_BURIED`, `FIT_POKE`, `FIT_GLASS`, `FIT_OPEN`,
`FIT_THIN_SUPPORT` and `STAB_TIPS` are planned for a later tool (Tools_C 4.5.0 plan,
block A). Until that tool exists, report these only as *suspected symptoms*
with the evidence you actually inspected.
