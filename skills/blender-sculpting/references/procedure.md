# Blender sculpting — procedure, performance and validation

Detailed passes for [the skill](../SKILL.md). Moved verbatim from SKILL.md in 4.4.0.

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

Prefer masks, Face Sets, visibility and smooth falloff over repeated whole-object smoothing. Read [bounded sculpt operations](../../blender-pipeline/references/techniques/sculpt-operations.md) when implementing a scripted regional correction.

A regional edit is accepted only if the requested area improves without introducing a ring, dent, surface ripple or silhouette regression at the transition.

For late-stage geometry corrections, protected anatomical volumes, Multires
coarse-level edits and surface/groom rebinding, read
[regional revisions](regional-revisions.md). Requested broad changes
remain valid after detailing; assess their dependencies rather than forbidding them.
When selecting a new human sculpt base, evaluate
[MPFB](../../blender-character-modeling/references/mpfb.md); preserve its parametric
source if topology-changing sculpt work is needed on a separate working copy.

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
