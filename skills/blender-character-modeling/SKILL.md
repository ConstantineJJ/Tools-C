---
name: blender-character-modeling
description: Create or substantially revise character geometry in Blender. Use for blockout, proportions, silhouette, body forms, clothing, accessories and geometry revisions; route sculpt-only, final-retopology-only, rig, weights, animation and export tasks elsewhere.
---

# Blender character modeling

Read the required [foundation contract](../../docs/foundation.md).

## Instruction Priority

Follow the current explicit request and active project profile/contracts before general modeling guidance. Keep the task narrow. If a requested edit conflicts with a protected invariant, identify the conflict before a destructive operation. Never invent missing project-specific proportions, skeleton rules or export requirements.

## Scope

Own character blockout, proportions, silhouette, primary and secondary body forms, clothing/accessory geometry and revisions of those forms. Prepare geometry for later sculpt, retopology or rig work only when that preparation belongs to the requested modeling task.

Organic sculpting, final deformation topology, rigging, weight painting, animation, export validation and engine integration have separate owners. A visible mesh defect can originate in weights, pivots, constraints or export; diagnose before remodeling.

## Domain constraints

- Protected: approved forms/views, named objects, rig/weights, materials, modifiers and downstream contracts outside scope.
- Owned edits: named objects or regions and the minimum dependent geometry; for a narrow request, default to the smallest sufficient area.
- Acceptance: the requested form is visible in relevant views and protected data still passes its applicable checks.

Words such as improve, fix or make better do not authorize redesign of unrelated parts.

## Preflight

Inspect only what the task requires. Determine new model versus revision, broad pass versus surgical edit, target objects/regions, reference intent, proportion and silhouette constraints, symmetry, transforms, modifiers/procedural dependencies and downstream deformation needs. Record MUST PRESERVE before editing. If required reference or target data is absent, resolve that uncertainty before guessing.

## Workflow and decisions

For a broad task: blockout → primary silhouette → major forms/proportions → joint clearance → secondary forms → clothing/accessories → controlled refinement → validation → handoff. Resolve primary form before tertiary detail; keep operations editable while the design is uncertain.

For a revision: inspect → isolate the requested change and dependencies → make the smallest sufficient edit → compare the requested result and protected views/data → stop.

Choose direct editing or a procedural/modifier method according to editability and downstream needs. Use separate geometry for genuinely separate or rigid parts; use continuous geometry when continuous deformation is required. Do not join objects just to reduce count or rebuild geometry to mask a rig, weight, animation or exporter problem. Read [geometry decisions](references/geometry-decisions.md) for joint, part, hand, face or clothing choices, and [modifiers and transforms](references/modifiers-transforms.md) when those data are affected.

## Modeling priorities and routing

Prioritize task correctness, silhouette and primary proportions, major volumes, deformation-critical structure, secondary forms, then tertiary detail. Intentional stylization can override generic anatomy.

Use [Reference Reconstruction](../blender-pipeline/references/reference.md) for image registration or fidelity diagnosis; [Organic Sculpting](../blender-pipeline/references/sculpting.md) for freeform volume edits; [Retopology](../blender-pipeline/references/retopology.md) for final edge flow; [Rigging](../blender-rigging-skinning/SKILL.md) for weights/bones and [Animation](../blender-animation/SKILL.md) for Actions; [Refinement](../blender-pipeline/references/refinement.md) for repeated measured corrections; and [QA](../blender-pipeline/references/qa.md) with [verification](../verification/SKILL.md) for acceptance evidence. Load only the relevant neighbor.

## Anti-degradation and validation

After a meaningful revision, compare the requested feature, silhouette, required other views, proportions, topology, deformation-critical areas, unrelated regions and editability against the baseline. Correct a bounded regression, restore the attempted change if net quality worsens, or report a genuine constraint conflict. Do not hide regression with unrelated polish.

Validate only what is applicable: fixed relevant views, proportions, intersections, surface continuity, normals, internal/duplicate geometry, transforms, modifiers, deformation clearance and object structure. Record actual observations; unavailable visual, pose or engine evidence is SKIP with reason, never PASS.

## Handoff, completion and stop

When another stage follows, name locked forms/MUST PRESERVE, changed objects, known limits, expected deformation, topology state, modifiers to retain, next owner and validation performed.

Complete and stop when the requested form exists, SUCCESS is observed, protected data survived, relevant views remain acceptable, no out-of-scope redesign occurred and the model is suitable for the declared next stage. Stop and report instead of guessing if the target or required reference is missing, requirements conflict, a destructive edit threatens production data, the defect belongs to another workflow or required validation cannot be performed.

## Pitfalls / Lessons Learned

### MOD-001
- Symptom: a geometry edit is proposed for a defect caused by weights, pivots or export.
- Cause: visible mesh behavior was treated as proof of modeling ownership.
- Rule: identify the producing stage before changing form; preserve unrelated production data.
- Automated check: no universal checker can infer defect ownership from appearance alone.
- Verification: compare source geometry, relevant poses and target import as applicable.
- Added from / context: v3 modeling routing design risk, not a claimed production incident.
- Version: 3.0, 2026-09-23.
