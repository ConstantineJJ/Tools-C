---
name: blender-anime-character-modeling
description: Create or revise anime and manga humanoid character geometry in Blender, including chibi proportions, stylized faces, eyes, hair masses and clothing. Use for anime character form and reference fidelity; stage-only sculpt, topology, materials, rigging, animation and export keep their own owners.
---

# Blender anime character modeling

Read the required [foundation](../../docs/foundation.md) and the general
[character modeling contract](../blender-character-modeling/SKILL.md). This
specialist owns anime form decisions; the general owner supplies preservation
and editable geometry practice. There is one geometry task, not two competing passes.

## Instruction Priority and task contract

Use the explicit request, current project profile and approved design first.
Establish TASK, MUST PRESERVE, MAY CHANGE and observable SUCCESS before editing.
Anime is a family of styles: do not prescribe one head/body ratio, eye size,
gender presentation, anatomy, shader, polygon count or target platform.

## Activation and ownership

Own new or scoped revised humanoid anime/manga geometry: blockout, proportions,
facial planes, eye/lid/eyelash forms, hair silhouette, outfit volumes and accessories
belonging to the character. Chibi and more anatomical styles use their own reference.
Human-bodied characters with animal ears/tails can use this owner for humanoid
forms; a creature body plan or muzzle/locomotion problem goes to
[animal modeling](../blender-animal-anthropomorphic-modeling/SKILL.md). Name any
requested regional split instead of silently replacing species anatomy.

For an existing anime asset, its style alone does not restart modeling:

| Task | Owner |
|---|---|
| Register images, diagnose likeness or resolve inconsistent projections | [reference reconstruction](../blender-pipeline/references/reference.md) |
| Sculpt-only forms or shape damage | [sculpting](../blender-sculpting/SKILL.md) |
| Final edge flow and deformation topology | [retopology](../blender-pipeline/references/retopology.md) |
| UVs, bakes, base materials and authored toon shading/normals | [surfaces](../blender-pipeline/references/surfaces.md) |
| Refine existing finish, emission, outlines or image effects | [polishing](../blender-posteffects-polishing/SKILL.md) |
| Bones, weights, facial bindings or dynamics setup | [rigging](../blender-rigging-skinning/SKILL.md) |
| Actions, expressions in motion and playback | [animation](../blender-animation/SKILL.md) |
| Export/fresh import or target appearance | [export](../blender-export-validation/SKILL.md), [Godot integration](../godot-asset-integration/SKILL.md) |
| Read-only acceptance review | [verification](../verification/SKILL.md) |

Use the [pipeline](../blender-pipeline/SKILL.md) for an explicitly requested
multi-stage task. Modeling can prepare lids, mouth space and joint clearance;
that preparation does not authorize a new rig, expressions or final retopology.

## Preflight

Identify new creation versus revision, named objects/regions, approved views and
style landmarks. Inspect source geometry, modifier evaluation, shared meshes,
materials, UVs, custom normals, shape keys and any rig before changing them.
Record projection/camera assumptions, hair/outfit silhouette, asymmetry and target
use. Use supplied references first. A single illustration constrains its view;
label unseen design choices and resolve only uncertainties that materially change
identity or protected structure. Do not invent a mandatory turnaround or outfit.

Read [face, hair and presentation decisions](references/face-hair-workflow.md)
when those features matter. [Source notes](references/research-notes.md) explain
the evidence and limitations behind the methods; they are optional study resources.

## Workflow

For creation, establish body/head/hair/outfit masses before details. Compare the
reference projection and another relevant view. Build facial planes, lids and
eye placement together so identity survives three-quarter and profile views.
Resolve hair groups and clothing clearance, then refine only identity-bearing
secondary forms. Choose polygon editing, curves or an authorized sculpt stage
according to editability and the requested result.

For a focal character in a larger scene, prove its face, pose and primary hair/body
masses in a [representative lookdev slice](../production-lookdev-gate/SKILL.md)
before spending heavily on background dressing. For a Blender-only result, use
the intended Blender renderer; target-engine checks are conditional on delivery.

For revision, capture the current state, isolate the feature and its dependencies,
make a bounded change and compare protected views/data. A dark face patch may come
from geometry, custom normals, a shadow mask or the renderer; diagnose its source
before changing the face. Preserve intentional stylization and asymmetry.

Keep final topology, UVs, material graphs and delivery choices with their owners.
Before changing vertex count/order on a mesh with shape keys or production bindings,
use the project's approved recovery/transfer method or stop at that dependency.
Localize edits to shared mesh/material users; do not recolor or reshape unrelated assets.

## Visual feedback and acceptance

Use [Blender evidence methods](../../docs/blender-evidence.md): capture through
the render operation/Render Result, open the actual images, list observed defects,
correct the authorized region and recapture under comparable settings. If the
named MCP capture is absent, try the documented Python-image or file-render fallback.
An inaccessible image or metadata-only response remains a visual blocker.

Judge whole-character silhouette and face/hair detail at the intended viewing
size. Check the reference view, three-quarter/profile as applicable, intersections,
lid/eye seating, hair roots/tips and clothing clearance. Recheck an unaffected
view after a visible correction. Still images do not certify blink, speech or poses.

Workbench/solid evidence supports geometry. The current managed material_preview
and rendered captures use Cycles and omit the production compositor; they cannot
certify an EEVEE-only Shader to RGB graph, final outlines or bloom. For those
criteria, inspect a render from the verified source renderer/compositor or the
actual target engine using an authorized acquisition path. Preserve production
settings. If unavailable, report that criterion as SKIP rather than swapping
shaders, disabling effects or accepting a different renderer's image.

## Handoff and stop

Hand off approved landmarks/projections, named changed and protected objects,
hair/eye/clothing construction, topology and shape-key state, modifier/custom-normal
dependencies, inspected evidence and unresolved render/pose/target gates.
Stop when the scoped form is observed without protected regression. Route a
diagnosed stage defect to its owner. Stop at conflicting references/invariants,
missing identity-critical data, unsafe bound-mesh edits or an unavailable required
visual gate; explain the remaining decision or capability. No blind detail pass.

## Pitfalls / Lessons Learned

### ANIME-001
- Symptom: a convincing front face loses identity in profile or under another light.
- Cause: a 2D drawing was treated as complete 3D geometry, or shading was mistaken for shape.
- Rule: diagnose form versus shading and inspect relevant alternate views without normalizing intentional stylization.
- Automated check: structural contracts cannot infer resemblance or artistic quality.
- Verification: comparable face/body images, renderer identity and reviewer observations.
- Added from / context: anime workflow design risk informed by primary sources; not a claimed production incident.
- Version: 1.0.0, 2026-10-04.

### ANIME-002
- Symptom: a generic evidence render is accepted despite missing toon bands or outlines.
- Cause: EEVEE/target-specific shading was judged through the managed Cycles capture.
- Rule: use renderer-compatible evidence for the named criterion and keep missing visual gates open.
- Automated check: context/routing tests prove delivery of guidance, not render equivalence.
- Verification: inspect the actual source/target result and distinguish geometry from final appearance.
- Added from / context: confirmed capture implementation boundary and Blender Shader to RGB documentation.
- Version: 1.0.0, 2026-10-04.
