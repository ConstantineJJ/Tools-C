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

## Profiles — read only what the task touches

This file is the core. Detailed procedures live in four profiles; read the
profile for each region the task changes, before working on it:

| Profile | Read when the task touches | File |
|---|---|---|
| Body & outfit | new character, blockout, head/body ratio, chibi, silhouette, neck/torso/limbs, clothing, accessories | [body](references/profile-body.md) |
| Face & eyes | face planes, eyes, lids, lashes, mouth, expressions prep, face artwork | [face](references/profile-face.md) |
| Hair | fringe, sides, crown, tails, ornaments, hair silhouette and clearance | [hair](references/profile-hair.md) |
| Toon look & evidence | dark patches, toon bands, outlines, renderer/target appearance, final review | [look](references/profile-look.md) |

A new full character goes body → face → hair; open the look profile before any
appearance judgment. MCP context delivers matching profiles and lists the rest
as conditional documents: request one before working on its region.
[Source notes](references/research-notes.md) are optional study material.

## Activation and ownership

Own new or scoped revised humanoid anime/manga geometry: blockout, proportions,
facial planes, eye/lid/eyelash forms, hair silhouette, outfit volumes and accessories
belonging to the character. Human-bodied characters with animal ears/tails can use
this owner; a creature body plan or muzzle/locomotion problem goes to
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

Consume the general owner's [face and primary-form gates](../blender-character-modeling/references/workflow-gates.md).
Identify new creation versus revision, named objects/regions, approved views and
style landmarks. Inspect source geometry, modifier evaluation, shared meshes,
materials, UVs, custom normals, shape keys and any rig before changing them.
Use supplied references first; a single illustration constrains its view. Label
unseen design choices; do not invent a mandatory turnaround or outfit.

## Revision rules (all profiles)

Capture the current state, isolate the feature and its dependencies, make a
bounded change and compare protected views/data. Preserve intentional stylization
and asymmetry. Before changing vertex count/order on a mesh with shape keys or
production bindings, use the approved recovery/transfer method or stop at that
dependency. Localize edits to shared mesh/material users. Topology, UVs, material
graphs and delivery stay with their owners.

## Visual feedback and acceptance

Use [Blender evidence methods](../../docs/blender-evidence.md): open the actual
images, list observed defects, correct the authorized region and recapture under
comparable settings. An inaccessible image or metadata-only response remains a
visual blocker. Judge silhouette and face/hair at the intended viewing size and
recheck an unaffected view after a visible correction. Renderer-specific criteria
(toon bands, outlines, bloom) follow the look profile. Stills do not certify
blink, speech or poses.

## Handoff and stop

Hand off approved landmarks/projections, changed and protected objects, hair/eye/
clothing construction, topology and shape-key state, modifier/custom-normal
dependencies, inspected evidence and open render/pose/target gates. Stop when the
scoped form is observed without protected regression; stop at conflicting
references, missing identity-critical data, unsafe bound-mesh edits or an
unavailable required visual gate. No blind detail pass.

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
