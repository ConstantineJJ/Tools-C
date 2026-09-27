---
name: godot-asset-integration
description: Integrate delivered 3D assets into Godot and validate import settings, skeletons, materials and animation playback in the target scene. Use for asset handoff; general gameplay code and Blender authoring have separate owners.
---

# Godot asset integration

Read the required [foundation](../../docs/foundation.md), current target AGENTS,
profile, project.godot and status. Preserve authored wrappers/overrides, other
instances, existing controllers and gameplay. The requested imported asset,
import settings and its wrapper are the ordinary change scope.

Require the export path/hash and upstream blockers. Identify actual engine version,
import hierarchy, skeleton/bone mapping, FPS, clips/root motion, material behavior,
scale and axes. Read [scene ownership](../godot-project/references/scene-ownership.md)
before changing imported or shared resources. Keep authored state outside content
that reimport replaces. No fixed skeleton, AnimationTree graph or collision design
is implied by this skill.

Run a bounded import/load, then explicit target-scene playback and another affected
instance. Compare material appearance and sampled poses in target lighting; an HTTP
health endpoint or tunnel success does not prove engine import. Record bridge
failures separately using [MCP diagnosis](../../docs/mcp-deployment.md).

An output-file defect returns to [export validation](../blender-export-validation/SKILL.md);
a source rig defect returns to its owner. General gameplay/controller work routes
to [godot-project](../godot-project/SKILL.md) only when requested. Handoff unresolved
target playback/visual checks explicitly.

## Pitfalls / Lessons Learned

### GAI-001
- Symptom: an export is blamed for a missing runtime probe.
- Cause: transport failure confused with engine or asset failure.
- Rule: separate deployment, tunnel, import and scene behavior evidence.
- Automated check: bounded engine load; transport diagnostics are independent.
- Verification: actual import and playback in the target project.
- Added from / context: K-01 audit reported Godot tunnel 404 at the next stage.
