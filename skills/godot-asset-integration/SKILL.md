---
name: godot-asset-integration
description: Integrate delivered 3D assets into Godot and validate import settings, skeletons, materials and animation playback in the target scene. Use for asset handoff; gameplay code and Blender authoring have separate owners, and appearance acceptance also loads verification.
---

# Godot asset integration

Read the required [foundation](../../docs/foundation.md), current target AGENTS,
profile, project.godot and status. Preserve authored wrappers/overrides, other
instances, existing controllers and gameplay. The requested imported asset,
import settings and its wrapper are the ordinary change scope.

Require the export path/hash and upstream blockers. Identify actual engine version,
import hierarchy, skeleton/bone mapping, FPS, clips/root motion, material behavior,
scale and axes. Read [import settings and conventions](references/import-settings.md)
before changing import options, import hints or the wrapper, and
[scene ownership](../godot-project/references/scene-ownership.md) before changing imported
or shared resources. Keep authored state outside content that reimport replaces. No fixed
skeleton, AnimationTree graph or collision design is implied by this skill.

For [destruction assets](../blender-destruction-assets/SKILL.md), consume the
piece/body/proxy map and rest transforms explicitly. Validate intact/fragment
collision switching, supported remainders, impact, settling and repeat reset in
the requested target scope. Blender physics properties are not an implicit GLB
runtime contract. New damage/controller logic goes to
[godot-gameplay-implementation](../godot-gameplay-implementation/SKILL.md).

Evidence: run import, then the whole-project parse gate, then an explicit target-scene
playback scenario and another affected instance, using
[godot-runtime-evidence](../godot-runtime-evidence/SKILL.md). Compare material
appearance and sampled poses in target lighting; capture frames are reviewed, not
auto-accepted. An HTTP health endpoint or tunnel success does not prove engine import.
Record bridge failures separately using [MCP diagnosis](../../docs/mcp-deployment.md).

An output-file defect returns to [export validation](../blender-export-validation/SKILL.md);
a source rig defect returns to its owner. General gameplay/controller work routes
to godot-gameplay-implementation only when requested. Handoff unresolved
target playback/visual checks explicitly.

## Pitfalls / Lessons Learned

### GAI-001
- Symptom: an export is blamed for a missing runtime probe.
- Cause: transport failure confused with engine or asset failure.
- Rule: separate deployment, tunnel, import and scene behavior evidence.
- Automated check: bounded engine load; transport diagnostics are independent.
- Verification: actual import and playback in the target project.
- Added from / context: K-01 audit reported Godot tunnel 404 at the next stage.

### GAI-002
- Symptom: a GLB looks wrong in Godot (flat, dark, wrong scale or facing) and the export is blamed.
- Cause: import options, tangents, orientation convention or project lighting differ from the source viewer.
- Rule: compare against a known-good asset in the same scene and diagnose exporter, importer and scene separately.
- Automated check: none for appearance; parse gate and scenario cover structure and playback only.
- Verification: reviewed capture of both assets under the same lighting and camera.
- Added from / context: Godot skills pass 2026-11.
