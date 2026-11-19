---
name: blender-sculpting
description: Sculpt or substantially revise organic and hard-surface forms in Blender: form hierarchy, bounded regional correction, Dyntopo/voxel/Multires choice, masks, cleanup, sculpted damage and retopology handoff. Final topology, rigging, domain ownership and export keep their owners.
---

# Blender sculpting

Read the required [foundation contract](../../docs/foundation.md) and the general [Blender pipeline](../blender-pipeline/SKILL.md). This skill replaces the former narrow organic-sculpting owner. The old pipeline reference is compatibility-only; this file is the canonical sculpting rule source.

## Instruction priority

Follow the user's target, active project/profile, approved reference and protected production data before any preferred sculpt technique. Sculpting is a representation choice, not permission to replace topology, UVs, shape keys, weights, rigs or approved silhouettes. Preserve deliberate stylization and asymmetry unless the task explicitly asks to change them.

## Scope and ownership

Own:
- concept/blockout sculpting where topology is intentionally disposable;
- organic primary, secondary and tertiary form development;
- bounded regional volume/contour correction on an existing mesh;
- sculpt-assisted stylized forms, folds, soft transitions and hard-surface shape refinement;
- controlled planar/crease/trim sculpting for high-poly manufactured or damaged surfaces when sculpting is actually the chosen stage;
- masks, Face Sets, visibility and isolation decisions for sculpt scope;
- choosing among fixed topology, Multiresolution, Voxel Remesh and Dyntopo;
- remesh/detail-resolution decisions and topology-loss safeguards;
- sculpted damage, dents, chips, tears, cracks and weathering forms where geometry/high-poly transfer is justified;
- preparing a stable high sculpt for retopology/bake handoff;
- sculpt-specific structural/visual QA and anti-degradation.

Route:
- game-ready detachable fragments, fracture interiors, physics proxies and intact/destroyed states to [destruction assets](../blender-destruction-assets/SKILL.md); sculpt-only cracks/dents remain here;
- matching supplied orthographic/photo references and deciding landmarks to reference reconstruction;
- generic character construction/proportion ownership to `blender-character-modeling` when the task is primarily modeling rather than sculpt execution;
- animal/creature body-plan decisions to `blender-animal-anthropomorphic-modeling`;
- plant growth/branch/foliage systems to `blender-vegetation`, even when trunk surface forms are sculpt-assisted;
- vehicle body proportion/surface ownership to `blender-vehicle-modeling`;
- prop/product/environment ownership to their domain specialists when sculpting is only one production technique inside that asset task;
- final deformation topology/edge flow to the retopology owner;
- rigging, weights and shape-key deformation to their respective owners;
- final UV/bake/material/export/integration to the relevant downstream owners.

Boundary rule: this skill owns **how a sculpting stage changes form while protecting the rest of the asset**. It does not seize ownership of the asset's domain merely because a sculpt brush is used.

## Preflight: choose the sculpt regime before the first stroke

Establish:

1. **Sculpt intent** — concept/blockout, primary-form build, secondary-form refinement, bounded correction, tertiary/detail pass, hard-surface/damage pass, fold pass, or high-poly bake source.
2. **Topology state** — disposable, production topology that must survive, clean base intended for Multires, already-remeshed sculpt, skinned/shape-keyed mesh, etc.
3. **Protected data** — silhouette regions, landmarks, UVs, vertex IDs, weights, shape keys, materials, modifiers, rig relationships, symmetry/asymmetry, named Face Sets and unrelated objects.
4. **Target evidence** — concept/reference, fixed views, anatomical/construction references, before/after screenshots, measured landmarks or defect description.
5. **Required detail scale** — largest form being changed, smallest form that must survive, and whether microdetail belongs in geometry or later texturing/shading.
6. **Symmetry state** — symmetric construction pass, deliberately asymmetric final form, or one-sided correction with the opposite side protected.
7. **Downstream stage** — continue sculpting, retopology, bake, rig, export, statue/print, cinematic high-poly, etc.
8. **Recoverable baseline** — duplicate/version/snapshot required before any destructive remesh, Dyntopo or topology replacement.

If the requested correction must preserve vertex IDs, UVs, weights or shape keys, treat Dyntopo and topology-replacing remesh as unavailable unless the user explicitly authorizes replacement and downstream recovery is defined.

## Choose the topology/resolution strategy

Work the passes in order; full instructions, performance/LOD guidance and the validation checklist are in [procedure](references/procedure.md) — read it before modeling and again before acceptance.

- **Fixed existing topology** — Use when production topology or vertex identity must survive.
- **Multiresolution** — Use when a clean base topology already exists and the task benefits from sculpting at multiple subdivision levels while preserving that base.
- **Voxel Remesh** — Use when topology is disposable and the sculpt needs a clean, roughly uniform volume for continued form development.
- **Dyntopo** — Use when topology is disposable and local, adaptive detail is genuinely useful while sculpting complex evolving shapes.

**Form hierarchy: big before small:** see the procedure reference.
- **Primary forms** — Own the largest masses, silhouette, gesture, proportions and major plane relationships.
- **Secondary forms** — Explain the primary masses:
- **Tertiary forms** — Small wrinkles, pores, fine creases, small chips, scratches, surface pitting and other high-frequency information.

**Bounded regional correction:** see the procedure reference.

**Masks, Face Sets and isolation:** see the procedure reference.

**Symmetry and intentional asymmetry:** see the procedure reference.

**Organic/anatomical sculpting:** see the procedure reference.

**Cloth and fold sculpting:** see the procedure reference.

**Hard-surface sculpting and planar forms:** see the procedure reference.

**Damage, cracks and weathering sculpt:** see the procedure reference.

**Surface cleanup without killing form:** see the procedure reference.

**Detail and brush discipline:** see the procedure reference.

**Resolution escalation rule:** see the procedure reference.

**Retopology and bake handoff:** see the procedure reference.

**Validation:** see the procedure reference.
- **Form hierarchy** — primary silhouette/proportions read at target distance before tertiary detail;
- **Regional correction** — named defect improved under comparable before/after views;
- **Topology/resolution state** — chosen fixed/Multires/voxel/Dyntopo regime matches protected data;
- **Surface quality** — no unintended lumps, brush chatter, voxel stair-stepping or melted planar regions;
- **Handoff readiness** — authoritative sculpt/high source is named;

## Safeguards

- Do not enable Dyntopo or voxel-remesh production topology merely to make brushing easier.
- Do not assume UVs, vertex IDs, weights, shape keys, Face Sets or color attributes survive destructive topology changes.
- Do not increase sculpt resolution before primary/secondary forms are accepted.
- Do not add tertiary pores/scratches/folds to distract from proportion or silhouette errors.
- Do not smooth globally when the problem is a bounded region or topology/resolution mismatch.
- Do not apply symmetry across approved asymmetrical anatomy, damage or design features.
- Do not mutate unrelated objects or hidden geometry outside the authorized sculpt scope.
- Do not treat voxel/Dyntopo topology as final deformation topology without explicit retopology acceptance.
- Do not sculpt shader-scale microtexture into geometry by default.
- Do not let a sculpting technique override the domain specialist's asset requirements.

## Pitfalls / Lessons Learned

### SCULPT-001 — Detail before structure
- Symptom: pores, wrinkles or scratches look finished but the form still feels wrong.
- Cause: tertiary detail began before silhouette, gesture and primary/secondary masses were accepted.
- Rule: work primary → secondary → tertiary and keep early resolution low enough to discourage microdetail.
- Verification: simplified/untextured distant views still read correctly before the detail layer matters.

### SCULPT-002 — Remesh destroys production data
- Symptom: UVs, weights, shape keys or vertex-dependent downstream work disappears after a sculpt cleanup.
- Cause: voxel remesh/Dyntopo was used on topology that was not disposable.
- Rule: classify topology state before sculpting; destructive topology change requires explicit scope and recoverable baseline.
- Verification: protected data is byte/structurally comparable or the approved replacement/handoff plan is documented.

### SCULPT-003 — Resolution escalation trap
- Symptom: the mesh becomes heavy and broad proportion changes are difficult while visible form quality does not improve.
- Cause: density was increased without a smaller required form to represent.
- Rule: raise resolution only when the next accepted frequency band cannot be represented at current density.
- Verification: each density increase has a named form/detail purpose and lower-frequency forms remain editable.

### SCULPT-004 — Global smoothing erases landmarks
- Symptom: surface noise decreases but anatomy, creases or hard planes become mushy.
- Cause: smoothing was applied broader than the defect.
- Rule: isolate with masks/Face Sets and protect intentional contour/landmarks; diagnose representation if smoothing is repeatedly required.
- Verification: before/after fixed views show cleaner surface without lost approved landmarks or silhouette.

### SCULPT-005 — Brush noise mistaken for detail
- Symptom: the surface has many bumps/creases but no readable hierarchy.
- Cause: repeated strokes accumulated without primary/secondary intent.
- Rule: every detail pass must reinforce a larger form, material or damage cause; leave quiet areas.
- Verification: tertiary detail can be reduced or blurred without exposing a weak underlying structure.

### SCULPT-006 — Hard-surface melt
- Symptom: a manufactured sculpt loses planar faces and controlled edges after organic brush cleanup.
- Cause: surface smoothing and freehand sculpting ignored construction planes.
- Rule: preserve plane/edge hierarchy with bounded flatten/trim/crease operations and hand off precision modeling when appropriate.
- Verification: reflection/plane inspection shows deliberate faces and transitions rather than soft wobble.

### SCULPT-007 — Damage without cause
- Symptom: every edge has equal chips/cracks and the asset looks procedurally distressed.
- Cause: damage was added as visual noise rather than material/force history.
- Rule: place structural damage first, then medium fracture, then selective small detail; keep an undamaged source for variants.
- Verification: major damage direction and material response can be explained by plausible force/use history.

### SCULPT-008 — Sculpt handed off without topology intent
- Symptom: retopology/bake loses silhouette, creases or deformation landmarks because the next artist/agent cannot tell what matters.
- Cause: high sculpt was treated as self-explanatory.
- Rule: hand off authoritative sculpt plus protected silhouette, creases, thin regions, deformation zones and bake-vs-geometry detail intent.
- Verification: retopo/bake plan names the sculpt features that must survive before topology work starts.

## Handoff

When passing to retopology, baking, rigging or another domain owner, report:
- sculpt intent and authoritative source object/version;
- topology regime used: fixed, Multires, voxel, Dyntopo or hybrid;
- remesh/detail settings that materially affect reproducibility;
- protected silhouette, proportions and landmarks;
- symmetry/asymmetry state;
- Face Sets/masks or separated subparts that carry semantic boundaries;
- details that must remain geometry versus transfer to normal/displacement/material;
- thin parts, sharp creases, openings and negative spaces that must survive retopo;
- damage/fold/material assumptions;
- structural/visual evidence completed and open deformation/bake/export gates.

## Completion / stop

Complete when the requested sculpting outcome is visible under the required comparable views, primary/secondary/tertiary hierarchy is appropriate to scope, destructive topology choices are justified and recoverable, protected regions/data survived, surface cleanup did not erase intended form, and downstream retopo/bake requirements are explicit.

Stop and report instead of guessing when the requested form conflicts with protected reference/landmarks, current topology cannot represent the change without unauthorized replacement, a Dyntopo/remesh step would destroy required production data, or the actual defect belongs to reference registration, retopology, weights/rigging, materials or another domain owner.

## Research basis

This canonical specialist consolidates the former Tools_C organic-sculpting rules and bounded sculpt-operation safeguards, then extends them with Blender 4.5 documentation for adaptive resolution, voxel remesh, Dyntopo, Multiresolution, masks and Face Sets plus production sculpting breakdowns emphasizing primary/secondary/tertiary hierarchy, low-resolution blockout, silhouette, controlled detail and retopology handoff. See [research notes](references/research-notes.md).
