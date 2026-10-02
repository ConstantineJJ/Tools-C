# Research notes — sculpting

Research snapshot: 2026-10-03.

This file records the basis for the canonical `blender-sculpting` specialist. It consolidates the previous Tools_C organic sculpting guidance and bounded sculpt-operation safeguards instead of creating a second rule source. Blender documentation is software authority; production interviews are workflow evidence and are generalized only where several sources converge. Project-specific topology, bake, polygon and engine requirements remain local.

## Existing Tools_C sculpting guidance — migration source

Sources:
- `skills/blender-pipeline/references/sculpting.md`
- `skills/blender-pipeline/references/techniques/sculpt-operations.md`

Useful rules preserved:
- protected regions and approved proportions take precedence over brush technique;
- bounded corrections should define object/region, coordinate frame, center, radius, falloff, strength, symmetry and protected neighbors;
- work macro volume → medium transitions → fine detail;
- Dyntopo and voxel remesh are topology-replacing operations and require disposable topology/recoverable source;
- remesh resolution must preserve the smallest form that matters;
- fixed before/after views, silhouette and affected deformation are anti-degradation gates;
- stop when the defect belongs to reference registration, topology, rigging or weights.

The former `sculpting.md` becomes a compatibility pointer after this pass. `sculpt-operations.md` remains a bounded implementation reference used by this canonical owner.

## Blender Manual 4.5 LTS — Adaptive Resolution

Source:
https://docs.blender.org/manual/en/4.5/sculpt_paint/sculpting/introduction/adaptive.html

Key points used:
- Voxel Remesher creates evenly distributed topology and is especially useful for initial shape/blockout work;
- Dyntopo adds/removes topology under the brush and supports local adaptive resolution, but is slower and has limited support for some sculpt features;
- Dyntopo can lose/corrupt custom attributes such as UV maps, color attributes and Face Sets;
- Multiresolution is subdivision-based sculpting and is recommended on a clean topology base mesh.

Applied as an explicit topology-regime decision rather than a universal recommendation to enable adaptive topology.

## Blender Manual 4.5 / 5.2 — Sculpt Remesh

Sources:
https://docs.blender.org/manual/en/4.5/sculpt_paint/sculpting/tool_settings/remesh.html
https://docs.blender.org/manual/en/5.2/sculpt_paint/sculpting/tool_settings/remesh.html

Key points used:
- voxel size determines the scale of resulting topology: smaller voxels preserve finer detail but create much denser meshes;
- Preserve Volume and several re-projection options exist, but remeshing still replaces vertex/edge/face identity and connectivity;
- current documentation warns that mesh-data layers associated with the original mesh can be lost and that remesh operates on original mesh data rather than treating modifier/shape-key/rig evaluation as a preservation contract;
- remesh is not available with Multiresolution.

Live bounded evidence on the connected Blender 5.2.2 LTS runtime added an important caveat: a 42-vertex test mesh remeshed to 272 vertices while its named UV layer and vertex-group values were still present/reprojected. This does **not** restore vertex identity or prove all production attributes survive. The canonical rule is therefore version-robust: topology identity is replaced, attribute preservation/reprojection is operator/version/options-dependent, and every required UV/weight/Face Set/color/custom-data contract must be verified explicitly after remesh rather than assumed.

Applied as the safeguard that production topology/UV/weights/shape-key identity cannot be assumed to survive a remesh, and resolution must be chosen from required form scale.

## Blender Manual 4.5 LTS — Remeshing / retopology

Source:
https://docs.blender.org/manual/en/4.5/modeling/meshes/retopology.html

Key points used:
- voxel remesh is suitable for changing sculpt resolution and cleaning messy/intersecting geometry;
- it produces uniform grid-like topology and is not appropriate as final deformation topology;
- topology for animated deformation must follow the form/motion and still requires deliberate retopology;
- Quad remesh has a different role and also is not a guaranteed replacement for final deformation topology.

Applied to the canonical sculpt-to-retopology handoff and the rule that successful remesh does not certify animation-ready topology.

## Blender Manual 4.5 LTS — Multiresolution

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/multiresolution.html

Key points used:
- Multiresolution subdivides a mesh while allowing sculpting on the subdivision levels;
- it has modifier-stack constraints because geometry/data-changing modifiers cannot simply precede it;
- Multires is a different representation from destructive voxel/Dyntopo workflows.

Applied to low-level/broad-form versus high-level/detail discipline and to protecting the clean base topology during a Multires workflow.

## Blender Manual 4.5 LTS — Visibility, Masks and Face Sets

Source:
https://docs.blender.org/manual/en/4.5/sculpt_paint/sculpting/introduction/visibility_masking_face_sets.html

Key points used:
- hidden faces cannot be sculpted and hiding can improve viewport performance;
- Masks control which vertices are affected;
- Face Sets group mesh regions for visibility/isolation and fast mask workflows;
- auto-masking can isolate geometry without manually painting a full mask.

Applied to bounded corrections and the principle that isolation reduces accidental edits but does not change project ownership.

## Blender Manual 4.5 LTS — Edit Face Set / fairing

Source:
https://docs.blender.org/manual/en/4.5/sculpt_paint/sculpting/tools/edit_face_set.html

Key points used:
- Face Sets can be grown/shrunk and used as controlled region boundaries;
- Fair Positions can create a flat/smooth patch while preserving vertex IDs, useful where IDs cannot change;
- Fair Tangency targets smooth curved surfaces while minimizing tangent changes.

Applied as examples of topology-preserving regional cleanup where global remesh/smoothing would be unnecessarily destructive.

## 80 Level — Sculpting a Comic Book-Style Batman Bust

Source:
https://80.lv/articles/sculpting-a-comic-book-style-batman-bust-in-zbrush

Source type: sculptor production breakdown.

Key practice used:
- establish big forms, silhouette and proportions before secondary and tertiary details;
- primary/secondary forms are explicitly treated as prerequisites for tertiary detail.

Applied as a general frequency hierarchy, independent of the source application's brush names.

## 80 Level — Sculpting a Dream Reader Statue

Source:
https://80.lv/articles/sculpting-a-dream-reader-using-zbrush-blender-substance-3d-painter

Source type: digital-sculptor interview.

Key practices used:
- keeping resolution low during primary-form blockout helps prevent premature wrinkles/fine detail;
- resolution is increased gradually as smaller forms are needed;
- gesture and contour remain important even in a static sculpt.

Applied as the Tools_C resolution-escalation gate: add density because a named smaller form needs it, not because higher density feels more finished.

## 80 Level — Goblin Knight: ZBrush to Maya Workflow

Source:
https://80.lv/articles/goblin-knight-zbrush-to-maya-workflow-and-grooming-in-xgen

Source type: character-production breakdown.

Key practices used:
- primary, secondary and tertiary passes have different structural roles;
- topology can be treated as disposable during a primary sculpt stage when downstream retopology is planned;
- symmetry can remain useful through substantial secondary-form development and be broken later deliberately.

Applied as a production-state distinction rather than a universal character workflow.

## 80 Level — Sculpting Scars / Henby portrait workflow

Source:
https://80.lv/articles/sculpting-scars-the-zbrush-workflow-behind-the-henby-portrait

Source type: high-poly character/clothing breakdown.

Key practices used:
- rough primary form and silhouette are established across all pieces before detailing one part deeply;
- secondary forms are developed across the whole asset before local refinement;
- high-frequency textile fibers can be left to texture/shader stages rather than sculpted into every high-poly surface.

Applied to whole-asset form balance and the safeguard against sculpting shader-scale microtexture by default.

## 80 Level — Studying Organic Character Art: Anatomy & Skin

Source:
https://80.lv/articles/001agt-studying-organic-character-art-anatomy-skin

Source type: character-art study/interview.

Key practice used:
- proportions and primary shapes matter before intricate anatomical detail;
- working zoomed out helps expose primary/silhouette errors before close-up nuance.

Applied to multi-view/target-distance primary-form QA.

## 80 Level — Wayfinder-Style Scythe / Big–Medium–Small

Source:
https://80.lv/articles/creating-hand-painted-wayfinder-inspired-scythe-with-substance-3d

Source type: stylized hard-surface/organic prop breakdown.

Key practices used:
- primary forms precede cleanup and detailing;
- a Big–Medium–Small hierarchy helps keep stylized forms readable;
- masks and controlled secondary sculpting can shape hard-surface/organic hybrid forms;
- tertiary cracks and microdetails must be restrained or they can destroy stylized readability.

Applied to hard-surface sculpt hierarchy and damage/noise control.

## 80 Level — Stylized creature / sculpt to retopology

Source:
https://80.lv/articles/designing-a-stylized-creature-in-zbrush-blender-marmoset-toolbag

Source type: game-ready creature production breakdown.

Key practices used:
- sculpting is effective for establishing a clean strong silhouette and primary/secondary shapes before low-poly retopology;
- retopology is a distinct downstream stage rather than evidence that sculpt topology was already production-ready.

Applied to the explicit sculpt→retopology handoff.

## Synthesis for Tools_C

The durable cross-source pattern is:

1. Classify whether topology is disposable or protected before selecting Dyntopo/remesh/Multires/fixed-topology sculpting.
2. Work primary → secondary → tertiary; keep early resolution low enough that small detail is inconvenient.
3. Escalate density only when a named smaller required form cannot be represented at the current level.
4. Use Masks, Face Sets, visibility and bounded falloff to protect neighboring regions during surgical corrections.
5. Treat Dyntopo/voxel remesh as topology replacement, never as harmless cleanup for a rigged/UV'd/shape-keyed asset.
6. Preserve symmetry while it is useful, then break it deliberately for approved asymmetry, pose or damage.
7. For hard-surface/damage sculpting, keep plane/silhouette and big–medium–small hierarchy ahead of scratches/pitting.
8. Move shader-scale repetitive microdetail out of geometry unless the bake/high-poly target actually requires it.
9. Finish with a handoff that identifies silhouette, landmarks, creases, thin parts, deformation regions and bake-vs-geometry detail intent for retopology/downstream owners.
