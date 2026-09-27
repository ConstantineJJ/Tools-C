---
name: blender-export-validation
description: Preflight and export scoped Blender assets to GLB, inspect skeletons, skins, materials and animations, then validate a fresh import against source evidence. Use for delivery and export regressions, not source remodeling or engine scene setup.
---

# Blender export validation

Read the required [foundation](../../docs/foundation.md). Preserve source objects,
geometry, rig/rest pose, materials and Actions. Export settings and a new delivery
file are the normal change scope. Never export from a viewer scene containing
helpers or a repaired in-memory object without checking the intended source copy.

1. Inspect explicit object selection, dependencies, units/axes/transforms, modifiers,
   shape keys, skin bindings, materials/textures and Action/slot/NLA inclusion.
   Record Blender/exporter version and available RNA options; unknown options fail.
2. Save baseline [snapshot and fixed views](../../docs/blender-evidence.md). Export
   selected objects to a new GLB, excluding helpers. A successful operator is only
   export execution evidence. Run the [bounded GLB inspector](../../tools/glb_inspect.py).
3. Inspect expected node/joint hierarchy, skin attachment, material roles, channels,
   clip durations at source FPS, root motion and mesh bounds. Use an explicit target
   contract; names/counts from K-01 or another project are never universal defaults.
4. Fresh-import in a separate factory Blender process using the
   [export probe](../../docs/blender-evidence.md). Compare scale/orientation, effective
   materials, joint/attachment behavior and sampled animation. Capture the same
   views/poses after import and review the images. Protect the live source session.
5. Record source-vs-output differences and evidence. Handoff target-engine checks
   to [Godot asset integration](../godot-asset-integration/SKILL.md) if applicable.

Triangulation, vertex splitting, CURVE/FONT becoming MESH, bone-tail reconstruction,
time-origin normalization and emission color/strength factorization can be harmless.
Prove equivalence of the affected runtime meaning before accepting a difference.
Missing skin/clip/material, hierarchy changes, root drift and transformed bounds
are regressions until explained. Equal counts/hashes are neither necessary nor
sufficient for round-trip equivalence. Unsupported compression/extensions/accessors
must be reported as limits, never silently counted as validated.

## Pitfalls / Lessons Learned

### EXP-001
- Symptom: structural export success is reported as final visual acceptance.
- Cause: no post-import visual evidence; source screenshots stood in for delivery.
- Rule: keep STRUCTURAL PASS and VISUAL SKIP/REVIEW REQUIRED/PASS separate.
- Automated check: GLB container/references and snapshot comparisons only.
- Verification: fresh process, sampled poses and inspected post-import images.
- Added from / context: K-01 Pass 6; imported playback aesthetics remained unreviewed.
