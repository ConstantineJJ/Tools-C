---
name: blender-animation
description: Author or correct Blender Actions, timing, loops, root motion and baked secondary motion on an existing rig. Use for motion edits; armature, weights and export validation remain separate.
---

# Blender animation

Read the required [foundation](../../docs/foundation.md). Preserve geometry, rig/rest
pose, weights, materials and baseline Actions outside the requested clips. Define
clip names, slots/channels, frame ranges, FPS, loop and root-motion policy locally.

Inspect the active Action, slots, NLA and constraints before keying. Keep new clips
separate; identify source channels before replacing keys. Review intent, extremes,
contact/recovery, arcs, support frames, foot sliding, Euler flips and unwanted scale
keys. Check first/last pose and transitions at the intended camera. Secondary motion
must have a target behavior: baked keys, runtime bones, or engine simulation;
Blender Cloth is not live engine cloth in a GLB.

Read [motion details](references/motion.md) for clips and secondary chains. Capture
named frames/poses and playback evidence; stills alone do not establish motion feel.
Handoff Actions/ranges/FPS and blockers through a [snapshot](../../docs/blender-evidence.md)
to [export validation](../blender-export-validation/SKILL.md). A rig defect goes to
[rigging and skinning](../blender-rigging-skinning/SKILL.md) before bone edits.

## Pitfalls / Lessons Learned

### ANIM-001
- Symptom: an exporter workaround changes accepted source motion.
- Cause: source Actions were baked or overwritten without isolating transfer behavior.
- Rule: prove inclusion/sampling settings first; bake only the requested delivery copy.
- Automated check: source snapshot and exported channel/time inspection.
- Verification: loop, root motion and contact before and after fresh import.
- Added from / context: K-01 Pass 6 used Action export without rewriting source curves.
