---
name: blender-rigging-skinning
description: Create or repair Blender armatures, bindings and weights, and validate required deformation poses. Use for diagnosed rig or skin defects; clip authoring and export have separate owners.
---

# Blender rigging and skinning

Read the required [foundation](../../docs/foundation.md). Preserve approved geometry,
materials, bone identities/rest pose and baseline Actions except the named rig/skin
scope. Skeleton roles and deformation requirements come from the current profile.

Inspect bindings, hierarchy, bone roll/rest matrices, groups, constraints and
modifiers. Diagnose a bad bend as weights, pivot/rest pose, topology, or animation
before editing; route topology changes through the pipeline. Test neutral and
required extreme poses. Rebinding/rest-pose changes require a recoverable baseline
and checks of every affected existing clip. Authoring IK/constraints need an explicit
bake or runtime reproduction decision with the animation/export owner.

Handoff a snapshot of bone names/parents, bound objects, protected geometry and
known deformation blockers. Capture affected poses using [evidence tools](../../docs/blender-evidence.md).
Route clip edits to [animation](../blender-animation/SKILL.md) and delivery to
[export validation](../blender-export-validation/SKILL.md).

## Pitfalls / Lessons Learned

### RIG-001
- Symptom: a weight correction changes neutral form or existing motion.
- Cause: rebinding or rest-pose edits performed before diagnosing the bend.
- Rule: compare named poses and baseline Actions; do not repair weights by remeshing.
- Automated check: snapshot catches declared source changes; pose quality requires images.
- Verification: neutral and affected extremes, plus existing clip playback.
- Added from / context: migration of the combined rigging procedure.
