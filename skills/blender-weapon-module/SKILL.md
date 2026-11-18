---
name: blender-weapon-module
description: Create or substantially revise game weapon modules in Blender — vehicle/turret weapon heads, cannons, launchers, energy weapons and hand-held guns — when functional anatomy, purposeful detail, internal moving parts, mount/muzzle interface markers and game-camera readability are central. Mount/turret pivots stay with the project or robot-mechanism owner; finishing, rig, animation and export keep their owners.
---

# Blender weapon module

Read the required [foundation contract](../../docs/foundation.md) and the general
[Blender pipeline](../blender-pipeline/SKILL.md). Image-based or substantial redesign
consumes [PASS 0](../visual-reference-reconstruction/SKILL.md); a style-only reference
uses its STYLE mode. This skill owns the weapon's form, function and interface truth.

## Ownership

Own: module silhouette, functional anatomy, purposeful secondary/tertiary detail,
weapon-internal moving parts (recoil slides, rotating barrels, hatches, feeds,
pistons, springs, gears, winches, rails), interface markers (socket, muzzle, optional
effect points) and representation for the target camera.
Route: the mount/yoke/turret pivots the module sits on to the project's mount owner
or [robot and mechanism modeling](../blender-robot-mechanism-modeling/SKILL.md);
vehicle bodies to [vehicle modeling](../blender-vehicle-modeling/SKILL.md);
UV/PBR to [surfaces](../blender-pipeline/references/surfaces.md); wear and glow to
[polishing](../blender-posteffects-polishing/SKILL.md); bones/clips to rigging and
animation; delivery to [export validation](../blender-export-validation/SKILL.md).

## Gates

| Gate | Build | Pass before continuing |
|---|---|---|
| W0 intake | Baseline copy, interface datum, anatomy sheet, target camera, budget | Interface file or recorded existing conventions; every anatomy line answered or N/A |
| W1 macro | Primary masses, forward axis, socket fit, muzzle placement | Clay views from the side, top and a **muzzle-facing** view at game distance; silhouette reads without detail |
| W2 function map | Secondary parts, each tagged with an anatomy function | No untagged detail except a few declared cosmetic accents; focal areas and rest areas both exist |
| W3 mechanisms | Moving parts as separate objects with real pivots/stroke | Neutral and extreme poses captured; anchors, travel and clearance stated |
| W4 surface intent | Material roles by function; emission follows the energy path | Accent colours small and purposeful; finishing handed to its owner |
| W5 delivery | Interface check on source, export validation, GLB interface check | [Weapon module checker](../../tools/weapon_module.py) PASS for both; visual gates reviewed separately |

**Anatomy sheet (W0).** Answer for the module, briefly: energy or ammunition source
and feed; firing/emission path and muzzle; heat handling; recoil or reaction path;
aiming and sighting; power/data link to the mount; maintenance access; protection of
fragile parts. Every visible detail must trace back to one of these lines.
Read [functional detail](references/functional-detail.md) before W2/W3 and
[module interface](references/module-interface.md) before W0 and W5.

## Construction rules

- Block primary forms first, as if machined or cast from stock; refine with cuts and
  insets. Name each part by its function; a part you cannot name is not understood yet.
- Keep a clear size hierarchy: one dominant mass, a few medium blocks, small detail
  in clusters. Vary spacing (roughly 2:1) instead of halving forms or repeating gaps.
- Detail density follows the camera: leave calm surfaces, concentrate detail at the
  muzzle, energy path, joints and access points. Drop anything unreadable at game
  distance; avoid long thin parts that vanish or alias.
- Mid-poly: bevel width scales with part thickness and visibility, weighted normals keep
  flat faces clean, cylinder segments follow screen size. Separate objects only for
  motion, interface, material or damage needs; merge static parts.
- Moving parts get origins on their physical axis and documented travel. A piston
  needs anchors at both ends; a gear needs a partner and an axle; a spring needs seats.
- Preserve the socket receiver/mount interface and project pivots exactly; never move
  them for cosmetic reasons. Add a muzzle marker even when the old asset had none.

## Safeguards

- Do not add greebles to fill space; empty, calm areas are part of the design.
- Do not let colour, glow or wear hide a weak silhouette — return to geometry.
- Do not invent another project's mount names, axes or budgets; read the interface
  file or the existing asset and record what was used.
- Do not claim gameplay feel, engine appearance or animation from stills.

## Pitfalls / Lessons Learned

### WPN-001 — Greeble without purpose
- Symptom: many bolts, vents and panels, yet the weapon looks like a box with noise.
- Cause: detail added for density, not tied to function or focus.
- Rule: W2 function map; remove or justify every untagged part.
- Verification: each secondary part has a function tag; rest areas remain visible.

### WPN-002 — Interface drift
- Symptom: the new module fits the editor scene but sits wrong on the vehicle.
- Cause: socket receiver, pivot or forward axis moved during the redesign.
- Rule: keep the receiver/mount data unchanged; check markers on source and GLB.
- Verification: weapon module checker PASS on both, socket offset within tolerance.

### WPN-003 — Hidden muzzle
- Symptom: the emitter or bore is never seen in review; firing effects spawn at the origin.
- Cause: fixed review views look from the rear, and no muzzle marker exists.
- Rule: review a muzzle-facing view; place a named muzzle marker at the bore face.
- Verification: muzzle view inspected; checker confirms the marker leads the forward axis.

### WPN-004 — Decorative mechanism
- Symptom: pistons, springs or gears that could not move or carry load.
- Cause: mechanical parts placed as texture, without anchors, partners or travel.
- Rule: model the load path and the extreme pose; otherwise remove the part.
- Verification: neutral/extreme captures show anchors, travel and clearance.

Version: 1.0.0, 2026-11-18. Sources and caveats: [research notes](references/research-notes.md).
