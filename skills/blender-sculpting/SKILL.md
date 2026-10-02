---
name: blender-sculpting
description: Sculpt or substantially revise organic and hard-surface forms in Blender when primary/secondary/tertiary form hierarchy, bounded regional correction, Dyntopo/voxel-remesh/Multires choice, masks/Face Sets, surface cleanup, folds, damage/weathering sculpt, topology-loss safeguards or retopology handoff are central. Use for disposable concept sculpts, high-poly form development and controlled sculpt corrections; route reference registration, final deformation topology, rigging/weights, animation, product/vehicle/vegetation ownership and final export to their specialist owners.
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

### Fixed existing topology

Use when production topology or vertex identity must survive.

Suitable for:
- bounded Move/Grab/Inflate/Smooth/Crease-like corrections;
- contour and volume changes that current density can represent;
- already-rigged/skinned/UV'd assets where topology replacement is outside scope.

Use masks, Face Sets, hidden geometry and auto-masking to isolate the authorized region. If the mesh lacks enough density for the requested feature, stop or hand off instead of silently remeshing production topology.

### Multiresolution

Use when a clean base topology already exists and the task benefits from sculpting at multiple subdivision levels while preserving that base.

Use low levels for broad proportion/volume corrections and higher levels only for smaller forms. A Multires workflow is not compatible with arbitrary voxel-remesh replacement of the same sculpt state. Protect the base topology and document the active level before downstream handoff.

### Voxel Remesh

Use when topology is disposable and the sculpt needs a clean, roughly uniform volume for continued form development. It is especially useful for concept/blockout phases and for merging/intersection cleanup where the source is treated as a volume.

Choose voxel size from the **smallest form that must survive the next pass**, not from a desire for the highest possible density. Lower voxel size keeps finer detail but produces much denser topology. Inspect thin parts, narrow gaps, holes and sharp creases immediately after remesh.

Blender's voxel remesh replaces vertex/edge/face identity and connectivity. Blender documentation warns about associated mesh-data loss, while exact attribute reprojection/preservation can vary by Blender version, operator state and options; never infer that UVs, weights, Face Sets, color attributes or other downstream data survived merely because similarly named layers still exist. It also operates on the source mesh rather than treating modifier/rig/shape-key evaluation as a stable preservation contract. Use it only with a recoverable baseline and explicit permission to replace topology, then verify every required data layer explicitly.

### Dyntopo

Use when topology is disposable and local, adaptive detail is genuinely useful while sculpting complex evolving shapes. Dyntopo adds/removes topology under the brush and supports local resolution, but it carries performance cost and can lose/corrupt UVs, color attributes and Face Sets.

Do not enable Dyntopo simply because the mesh feels difficult to sculpt. If a uniform voxel remesh or a clean Multires base better matches the task, use that instead.

## Form hierarchy: big before small

Sculpt in ordered frequency bands.

### Primary forms

Own the largest masses, silhouette, gesture, proportions and major plane relationships. Examples: ribcage/pelvis/head mass, overall creature torso, dominant fold mass, major dent, broad armor bulge or large chipped corner.

Work zoomed out and from several views. Keep resolution low enough that tertiary detail is inconvenient to add. If the silhouette or proportion is wrong, no amount of pores, scratches or wrinkles can rescue the sculpt.

### Secondary forms

Explain the primary masses: major muscle/fat transitions, eye/nose/mouth structure, large folds, plate transitions, medium dents, cut planes, tendons, edge breaks, large cracks, bark masses or broad manufactured wear.

Secondary forms should reinforce structure and material, not become equal-strength noise everywhere.

### Tertiary forms

Small wrinkles, pores, fine creases, small chips, scratches, surface pitting and other high-frequency information. Add only after primary and secondary forms survive target-view review.

Do not sculpt microtexture that would be cheaper, more controllable and equally visible as a normal/detail material unless the high-poly/bake target explicitly benefits from geometry.

## Bounded regional correction

For a surgical sculpt fix, define:
- named object and region;
- local/world coordinate frame;
- center/landmark and radius relative to the feature;
- desired displacement/volume change;
- falloff and transition zone;
- protected neighboring landmarks/silhouette;
- symmetry behavior;
- before/after fixed views and affected pose if relevant.

Prefer masks, Face Sets, visibility and smooth falloff over repeated whole-object smoothing. Read [bounded sculpt operations](../blender-pipeline/references/techniques/sculpt-operations.md) when implementing a scripted regional correction.

A regional edit is accepted only if the requested area improves without introducing a ring, dent, surface ripple or silhouette regression at the transition.

## Masks, Face Sets and isolation

Use Sculpt visibility, Masks, Face Sets and auto-masking to reduce accidental edits.

- Masks protect vertices from sculpt influence.
- Face Sets group regions and can be isolated/hidden or used to derive masks.
- Hiding unneeded geometry reduces accidental strokes and can improve viewport performance.
- Face Sets can be initialized from materials, UV seams, sharp edges or other existing boundaries when those boundaries are meaningful to the task.

Do not confuse masking/isolation with ownership: hidden geometry remains protected project data.

## Symmetry and intentional asymmetry

Keep symmetry while it accelerates primary/secondary construction and the design is genuinely symmetric. Break it only when:
- the reference/design requires asymmetry;
- pose/gesture requires side-specific correction;
- damage/weathering/history requires it;
- left/right anatomical variation is part of the approved target.

When breaking symmetry, preserve a comparable checkpoint. Avoid accidental asymmetry caused by camera angle, uneven brush strength or non-applied transforms.

## Organic/anatomical sculpting

Use anatomy and construction landmarks to explain the surface rather than sculpting muscle names as separate lumps.

For characters/creatures:
- establish gesture and skeletal masses first;
- place large bony landmarks before soft tissue detail;
- let secondary fat/muscle/tendon forms connect primary masses;
- judge contour and plane changes from several angles;
- keep the approved character/creature owner responsible for proportion/body-plan decisions.

For stylized anatomy, simplify or exaggerate consistently with the concept. Real anatomy is a support system for readable form, not a requirement to normalize the design.

## Cloth and fold sculpting

Build folds from force and attachment:
- identify anchors/support points;
- tension directions;
- compression zones;
- hanging weight/gravity direction;
- material stiffness/thickness;
- collision/contact points.

Start with large fold rhythms and silhouette, then medium compression/tension folds. Fine wrinkles are tertiary. Do not distribute folds uniformly across quiet fabric areas.

## Hard-surface sculpting and planar forms

Sculpting can support manufactured or stylized hard-surface assets when the high-poly form benefits from direct plane/edge manipulation, damage or hand-shaped surfaces.

Preserve hierarchy:
1. major plane/layout and silhouette;
2. secondary bevels, seams, recesses and transitions;
3. damage/edge breakup;
4. fine scratches/pitting only when justified.

Use trim/scrape/flatten/crease behavior with controlled boundaries. Keep planar regions planar and curved regions intentionally curved; smoothing should not turn engineered surfaces into melted forms.

When the object is fundamentally better represented by precise parametric/boolean/subdivision modeling, hand it back to the domain hard-surface owner rather than forcing sculpting onto every manufactured asset.

## Damage, cracks and weathering sculpt

Treat damage as material/process history, not a noise layer.

Plan from large to small:
- structural break/dent/bend/chip that changes silhouette;
- medium fracture edges, torn material or compression;
- small chips/cracks/scratches;
- micro-pitting/grain last, often in materials instead of geometry.

Ask what force caused the damage, where material would compress, tear, fracture or abrade, and how thick the underlying material is. Avoid identical edge chipping around every border or cracks with no structural origin.

Preserve an undamaged source or a recoverable layer/version when damage is a variant rather than a permanent asset identity.

## Surface cleanup without killing form

Use smoothing/fairing/relaxation only to remove unintended noise, not to erase designed plane changes or landmarks.

Check:
- silhouette before and after cleanup;
- large plane transitions;
- pinching around masks/Face Set boundaries;
- lumps caused by excessive brush accumulation;
- stair-stepping or voxel artifacts;
- thin parts after remesh;
- self-intersections introduced by aggressive moves.

If a surface repeatedly requires smoothing to hide topology problems, diagnose the representation/resolution instead of polishing symptoms indefinitely.

## Detail and brush discipline

Choose the brush operation that matches the form problem, but judge the result rather than the brush name.

Useful categories:
- Move/Grab — primary silhouette and landmark placement;
- Clay/Build — add/subtract volume and secondary transitions;
- Smooth/Relax — remove unintended high-frequency noise while protecting form;
- Inflate/Deflate — bounded thickness/volume change;
- Crease/Pinch — intentional grooves/ridges and controlled sharp transitions;
- Flatten/Scrape/Trim — planar hard-surface or stylized plane control;
- mask/Face Set extraction — only when a separate piece is actually required.

Use the fewest passes necessary. Repeated low-intent brush strokes often create lumpy frequency noise that later requires destructive cleanup.

## Resolution escalation rule

Increase detail resolution only after the current frequency band is accepted.

Before increasing voxel density, Dyntopo detail or Multires level, ask:
- which smaller form cannot be represented now?
- is that form visible/required downstream?
- is its parent form already approved?
- will the increase make later proportion correction harder?

If no concrete smaller form needs more geometry, keep the current resolution.

## Retopology and bake handoff

Before handoff, lock the sculpt's important information:
- approved silhouette and proportions;
- anatomical/construction landmarks;
- sharp/hard boundaries and intended creases;
- thin parts and negative spaces that retopo must preserve;
- moving/deformation regions and their required motion owner;
- high-poly damage/details expected to bake;
- details that should remain geometry versus move to texture/material;
- scale/orientation and symmetry state;
- which sculpt copy is authoritative.

Do not treat voxel/Dyntopo topology as animation-ready final topology. Blender documentation explicitly distinguishes remeshing useful for sculpting from topology designed for deformation. Handoff to the retopology owner when edge flow/deformation becomes the problem.

## Validation

Perform applicable checks and mark unavailable gates as SKIP.

### Form hierarchy
- primary silhouette/proportions read at target distance before tertiary detail;
- secondary forms reinforce the primary structure instead of competing with it;
- tertiary noise does not obscure material/form readability;
- intended gesture, plane changes and negative spaces survive multiple views.

### Regional correction
- named defect improved under comparable before/after views;
- protected landmarks and neighboring silhouette remain within scope;
- transition has no visible ring, pinching or unintended flattening;
- affected deformation pose is checked when the sculpted region participates in motion.

### Topology/resolution state
- chosen fixed/Multires/voxel/Dyntopo regime matches protected data;
- no destructive topology replacement occurred without a recoverable baseline;
- thin parts/gaps/creases survived remesh at required scale;
- Multires base and active level are known before handoff;
- UV/weights/shape-key assumptions are not made after remesh/Dyntopo.

### Surface quality
- no unintended lumps, brush chatter, voxel stair-stepping or melted planar regions;
- hard-surface sculpt retains deliberate planes/edges;
- organic surfaces retain major landmarks under smoothing;
- damage/wear follows plausible material/force logic;
- self-intersections and collapsed thin regions are absent where required.

### Handoff readiness
- authoritative sculpt/high source is named;
- retopo/bake owner knows silhouette, creases, thin parts and high-frequency transfer requirements;
- protected data and open gates are explicit;
- visual acceptance is based on inspected views, not only mesh validation or brush completion.

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
