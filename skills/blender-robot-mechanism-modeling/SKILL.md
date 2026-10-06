---
name: blender-robot-mechanism-modeling
description: Create or substantially revise hard-surface robot, mech, manipulator and articulated mechanism geometry in Blender. Own macro silhouette, mechanical skeleton, axes, static articulation, armor layering and assembly clearances; consume PASS 0 for image-based work. Surface-only wear, rigging, animation and export retain their existing owners.
---

# Blender robot and mechanism modeling

Read the [foundation contract](../../docs/foundation.md). Practical failure evidence
is distilled from the user's Report4.0.3, with [traceability](references/report-lessons.md).
Report instructions and historical user corrections do not authorize a new asset change.

## Ownership and input gate

Own rigid construction geometry: masses, structural links, bearings, pivots,
actuator envelopes/attachments, armor, interfaces and static assembly. Wheeled
vehicles, buildings, props and electronic devices keep their domain owners;
co-load this skill only for requested articulated subassemblies. A humanoid robot
does not automatically need organic character modeling.

For complex new design from text or image-based creation/major reconstruction, require a current
[visual-reference-reconstruction PASS 0](../visual-reference-reconstruction/SKILL.md)
**before scene mutation**. Verify hashes and the permitted stage; consume component
and claim IDs, relative ranges, source authority, limits and auxiliary review.
`BLOCKED` stops dependent construction. `READY_WITH_LIMITS` permits only named work;
deferred rear geometry stays deferred. Consume the same packet in REFERENCE or
DESCRIPTION mode. REQUIRED constraints survive conversion to geometry; CANONICAL
choices remain locked design decisions, never CONFIRMED evidence. No concept selection
or multiview redesign belongs to this skill. An unavailable/PENDING concept blocks
the visual design workflow rather than authorizing fictitious source evidence.

Reuse the single [Model Contract](../visual-reference-reconstruction/references/model-contract.md)
without reinterpreting locked properties at each pass. Bind assembly_graph.json and
saved asset metadata to its id/revision/hash; compare hard invariants, key measured
proportions/anchors and critical relationships at meaningful stage gates. Use only
permitted generated panels. Intentional design changes require explicit Contract
revisions, not new interpretations of crop or another material/detail pass.

Do not promote inferred/speculative claims while converting them to geometry.
Attach claim IDs/uncertainty to assembly records and editable proxies. Materials,
wear or impressive rendering never compensate for unresolved shape or construction.

## Staged construction and QA gates

Follow **geometry first → clay review → materials → wear**. Each gate needs named
criteria, evidence and PASS/WARN/FAIL/SKIP; a failed prerequisite returns to its owner.
Keep projection/pose/lighting comparable and inspect source-matched 3/4 as well as
orthographic views. Capture success alone is not visual acceptance.

| Stage | Build | Checkpoint before proceeding |
|---|---|---|
| G0 — intake | Scope, recovery baseline, metric/relative unit, part graph, protected objects/data | PASS 0 supports the next stage; source count, ambiguity and conflict decisions are carried forward |
| G1 — macro | Torso/pelvis/link/foot/pod envelopes, major slopes, depth and negative spaces; no bolts | Neutral clay front/side/rear/3/4: source silhouette, width/height ratios, landmark heights, count and stance; rear unknowns use only allowed proxies |
| G2 — skeleton | Link lengths, named axes, bearings/hubs/forks, support paths, actuator anchors and permitted static pose ranges | Reachability without silent clamping/stretching; pivot invariance; attachment and representative clearance checks; believable load/support and motion paths |
| G3 — secondary | Armor layering, changing sections, inset frame, access panels, mounting collars, vents and open channels | Clay review: armor outside frame, designed gaps/thickness, access/assembly logic, no unsupported/floating parts, negative spaces open across the entire evaluated assembly |
| G4 — tertiary | Fasteners, seals, clamps and small grooves where visible/functional | Detail hierarchy and bevels relative to thickness; evaluated mesh defects; repeated/shared-data integrity and object budget; silhouette still passes with detail hidden |
| G5 — surface handoff | Material groups and approved stable geometry to UV/PBR owner | Geometry/clay acceptance recorded before color; painted metal, bare metal, rubber/seals, optics and lubricated surfaces remain distinguishable |
| G6 — finishing | Pass stable surfaces to wear/polishing owner | Wear follows exposure/contact/heat, keeps quiet areas and base material identity; compare clay and clean material views; no scratch noise hiding weak form |
| G7 — delivery | Scoped snapshots, named joints/limits, dependencies, saved editable assembly | Independent reopen/evaluated QA and inspected final views where requested; untested rig/motion/engineering/export/runtime gates remain open |

G1 and G3 are mandatory visual checkpoints for reference-based reconstruction;
if images cannot be acquired/reviewed, stop detail/material escalation and report
the missing gate. A bounded structural experiment can stop at G2 with visual SKIP.
Project fidelity and camera requirements determine tolerances; no universal mech
height, triangle budget, clearance or engineering scale is imposed.

Read [assembly and mechanical design](references/assembly-and-mechanics.md) before
skeleton/armor construction, [rigid transforms and shared data](references/rigid-transforms.md)
before scripted hierarchy/instance edits, and [QA and handoff](references/qa-and-handoff.md)
for evidence selection and delivery. For better major forms use existing
[form development](../blender-pipeline/references/techniques/form-development.md).

## Surface and downstream routes

This skill specifies surface intent and enforces sequencing, not a second material
implementation. UVs/bakes/PBR use [surfaces](../blender-pipeline/references/surfaces.md);
final wear/damage/emission use [polishing](../blender-posteffects-polishing/SKILL.md).
Geometric dents affecting silhouette return to the shape/sculpt owner.
Bones/weights use [rigging](../blender-rigging-skinning/SKILL.md), motion/actuator
drivers use [animation](../blender-animation/SKILL.md), file delivery uses
[export validation](../blender-export-validation/SKILL.md) and engine integration
its [target owner](../godot-asset-integration/SKILL.md). Only run requested stages.

## Safeguards and stop

- Stop dependent work if a major axis/interface/count conflicts with source truth
  or a hidden joint is required but not established. Use PASS 0 decisions, never
  a generated rear engine as factual architecture.
- Do not clamp an impossible leg solution or lengthen a rigid link invisibly.
  Adjust the authorized stance/body placement or report incompatibility.
- Define actuator attachment frames and allowable length range before placing
  pistons. A rod drawn beside a limb is not an attached mechanism.
- Verify hollows through all shell/insert/backplate/seam/wear geometry; a dark circle
  or a hollow cylinder alone proves neither a channel nor a through-bore. A visible
  launch-tube face does not establish an open rear; require source/design evidence.
- Do not infer geometry-edit authority from object names. Preserve linked meshes;
  transform instances, modify a prototype once, or make unique data deliberately.
- Scale bevels by local thickness and inspect evaluated geometry. Closed source
  meshes can still fail after modifiers or occlude the intended armor.
- Keep manufacturing logic plausible: distinct removable parts, fastener seating,
  access, plausible plate thickness, reinforcement and space for cables/stroke.
  This is artistic construction, not strength analysis or mechanical certification.
- Batch unneeded independent wear objects by panel/material; retain moving modules
  separately. Any performance budget belongs to the project, not this skill.

## Pitfalls / Lessons Learned

### RMM-001 — Surface detail masks weak construction
- Symptom: many bolts and scratches, but silhouette/depth or articulation is wrong.
- Cause: primary forms and mechanical interfaces were not accepted before surface work.
- Rule: geometry first, mandatory macro/secondary clay review, then materials and wear.
- Automated check: evaluated geometry and part-registry checks cannot certify resemblance.
- Verification: inspect neutral clay views and test named joints/clearances before escalation.
- Added from / context: Report4.0.3 flat panels, armor occlusion and unreachable stance.
- Version: 1.0.0, 2026-10-05.
