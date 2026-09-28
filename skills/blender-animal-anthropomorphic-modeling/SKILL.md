---
name: blender-animal-anthropomorphic-modeling
description: Create or substantially revise animals, creatures, quadrupeds, stylized pets and anthropomorphic animal characters in Blender. Use when species/body-plan anatomy, animal-to-human feature blending, silhouette, locomotion-aware proportions, paws/hooves/wings/tails/ears/muzzles or deformation-ready creature forms are central; route generic character work, sculpt-only, final retopology, rigging, animation and export to their specialist owners.
---

# Blender animal & anthropomorphic modeling

Read the required [foundation contract](../../docs/foundation.md) and the general [Blender character modeling skill](../blender-character-modeling/SKILL.md). This skill is a specialist layer: it owns animal body-plan reasoning and human/animal feature integration, not the entire character pipeline.

## Instruction priority

Follow the current request, project profile, approved concept/reference and protected invariants before generic anatomy advice. Stylization is intentional design, not an error to normalize. Do not silently "correct" a creature toward realism when the target is stylized, nor force human anatomy onto an animal or animal anatomy onto a humanoid region without evidence.

## Scope

Own:
- species/body-plan identification and reference strategy;
- blockout, proportions, silhouette and major masses for animals/creatures;
- locomotion-aware limb placement and joint clearance;
- muzzle, ears, tail, paws/feet/hooves, horns/antlers and other animal-specific geometry;
- explicit human/animal blending for anthropomorphic characters;
- low-poly/stylized simplification that preserves identity, motion and silhouette;
- geometry preparation needed for later rigging/retopology when it belongs to the modeling task.

Route final deformation topology to retopology, bones/weights to rigging-skinning, motion to animation, grooming/hair systems to the appropriate surface/groom workflow, and export/engine issues to export-validation/integration.

## Preflight: define the creature before touching geometry

Record, explicitly or mentally, the minimum useful design sheet:

1. **Body plan** — biped, quadruped, winged, serpentine, hybrid, fantasy; for mammalian legs identify plantigrade, digitigrade or unguligrade where applicable.
2. **Reference species** — primary species plus any secondary influences. For invented creatures, assign a real anatomical reference to each major region rather than inventing every joint.
3. **Locomotion and actions** — walk/run/jump/climb/fly/swim, upright acting, combat, sitting, facial speech, etc. Topology and proportions depend on what must move.
4. **Style target** — realistic, semi-realistic, stylized, chibi, low-poly, mascot, game creature.
5. **Anthropomorphic blend map** when applicable — which regions are human-dominant, animal-dominant or intentionally hybrid: skull/muzzle, neck, torso, arms, hands/paws, pelvis, legs/feet, tail, ears, surface/fur.
6. **Production target** — still image, realtime game asset, animation, rigged hero, crowd/NPC, etc.
7. **MUST PRESERVE** — approved silhouette, named features, asymmetry, materials, rig/weights, object names and downstream contracts outside the requested scope.

If the body plan or reference is ambiguous enough to change joint placement or silhouette, resolve it before detailed modeling.

## Reference stack

Use multiple kinds of reference; one beauty image is not enough for anatomical decisions.

- orthographic-ish front/side/back and 3/4 views for proportion;
- skeleton and superficial muscle diagrams for major landmarks;
- real photo/video for weight distribution, shoulder/hip motion and locomotion;
- closeups for paws, hooves, claws, ears, muzzle, eyes and tail base;
- style references for simplification/exaggeration;
- for anthropomorphic work, separate human and animal references for each hybrid region.

Prefer consistent species/age/body condition. When references disagree, preserve the explicit concept and document the compromise instead of averaging blindly.

## Modeling order

Use the least detailed representation that can answer the current question.

### Pass 1 — gesture and mass
Establish line of action, head/chest/pelvis masses, spine arc, limb lengths, stance width, center of mass and ground contacts. Use primitives, low-resolution mesh or coarse sculpt. Judge silhouette in front, side and 3/4 views.

Do not add fur clumps, claws, wrinkles, nostrils or tiny facial detail while the major proportions are uncertain. Detail cannot rescue a weak body plan.

### Pass 2 — anatomical landmarks
Place joint centers and visible landmarks before surface polish. For mammalian quadrupeds, verify scapula/shoulder mass, elbow, wrist/carpus, pelvis/hip, knee/stifle, ankle/hock and digit/hoof contact from reference. The hock/heel is not a reversed knee. For non-mammals, use species-specific anatomy rather than reusing the mammal chain by habit.

Make enough room for expected joint flexion and muscle/skin compression. A neutral pose must not hide impossible articulation.

### Pass 3 — species identity and secondary forms
Refine skull/muzzle ratio, eye placement, ear origin, neck transition, ribcage/pelvis relationship, limb taper, paw/hoof shape, tail root and characteristic fat/muscle masses. Push only the features that carry the target species/style.

For furred characters, build the underlying body and large fur silhouette masses first. Do not use fur volume to conceal incorrect anatomy.

### Pass 4 — anthropomorphic integration
Do not create a generic human body with an animal head unless that is the design. Choose transitions intentionally:
- head/neck: decide skull orientation, muzzle projection and cervical posture;
- shoulder/arm: decide human clavicle/arm behavior versus animal forelimb influence;
- hand/paw: decide grasping requirements, digit count and pad/claw logic;
- pelvis/leg: decide upright human mechanics versus digitigrade/unguligrade structure;
- torso: decide ribcage, waist and spinal curve appropriate to the pose language;
- tail/ears: root them in believable underlying structure and preserve clearance.

Judge the hybrid by silhouette and motion intent, not by a numeric 50/50 mix. Different regions may use different blend ratios.

### Pass 5 — production geometry
Choose continuous geometry where skin must deform continuously; keep rigid or independently moving features separate when that improves control (for example horns, claws, some teeth, armor, accessories or stylized plates). Object count is not a quality metric.

For low-poly assets, spend polygons where they change silhouette, articulation or facial readability. Flat/hidden areas can remain sparse. Preserve intentional faceting when it is part of the style.

## Deformation-aware topology guidance

When final topology is in scope, load the retopology specialist. During modeling, prepare for it:

- loops should follow natural contours and deformation directions;
- allocate more resolution at shoulders, hips, knees/stifles, elbows, wrists/carpus, hocks/ankles, neck base, mouth and eyelids when those regions must deform;
- keep topology density reasonably gradual; avoid abrupt dense-to-sparse patches across a bending region;
- muzzle/jaw and eyelids need topology that matches required expressions, not a generic face template;
- tails need enough segments/loops for the requested curvature and should emerge cleanly from the pelvis/spine region rather than look glued on;
- do not pursue all-quads as a visual religion: production use, deformation and shading are the acceptance criteria. For deforming/subdivided organic areas, clean quad flow is usually the safest default.

Static topology inspection is not enough for an animated creature. Deformation must eventually be tested in representative poses, and for locomoting animals a walk/run or comparable motion test is especially valuable.

## Stylization rules

Stylization should simplify a believable structure, not replace structure with random shapes.

- Preserve a readable large-to-small hierarchy: primary masses → secondary forms → accents.
- Exaggerate a few identity features; do not exaggerate every feature equally.
- Keep eye, muzzle, ear, paw/foot and tail proportions coherent with the chosen style.
- In chibi/mascot work, large head/eyes and shortened limbs are valid, but joint locations and contact points still need a consistent internal logic.
- Check the model at target game/view size. Tiny details that vanish should not consume topology or visual noise.
- Introduce deliberate asymmetry only after the symmetric/base design is stable unless asymmetry is a defining requirement.

## Validation

Perform only applicable checks and record unavailable evidence as SKIP.

### Static form
- silhouette reads in front, side, back/3/4;
- primary species or creature identity is recognizable without materials;
- head/chest/pelvis scale and limb lengths are coherent;
- feet/paws/hooves make believable contact with the ground;
- tail, ears, wings/horns and muzzle have plausible roots and clearance;
- no unintended intersections, duplicate/internal geometry or broken normals;
- transforms and modifiers are appropriate for the next stage.

### Anthropomorphic consistency
- human/animal blend decisions are consistent region by region;
- no accidental conflict between upright posture and animal limb mechanics;
- hands/paws/feet match required gameplay/acting function;
- facial design supports the required expressions/speech level;
- silhouette still reads as the intended species/character rather than a generic humanoid.

### Motion readiness
Before declaring an animation-bound mesh production-ready, test or hand off for:
- deep limb bends at expected joints;
- shoulder/scapula and hip transitions;
- neck/head extremes;
- tail curvature;
- mouth/eye deformation if needed;
- representative walk/run/pose test for locomoting characters.

A static beautiful pose does not prove deformation quality.

## Pitfalls / Lessons Learned

- **Detail-first failure:** tertiary fur/skin detail appears before proportion is stable. Return to silhouette and primary masses.
- **Backward-knee myth:** digitigrade hock is treated as the knee. Re-check the skeletal chain from reference.
- **Human template drift:** animal-specific shoulder, pelvis, skull or limb mechanics are replaced by a generic human base. Restore body-plan landmarks.
- **Animal-head-on-human-body drift:** anthropomorphic design has no transition logic. Build an explicit regional blend map.
- **Reference averaging:** conflicting species or photos are blended into anatomical mush. Choose a primary source per region.
- **Fur camouflage:** fur volume hides weak anatomy. Validate the underlying body silhouette.
- **Topology-by-rule:** all-quads or uniform density is pursued even when it harms deformation or budget. Optimize for use.
- **Static-only approval:** topology is approved without representative deformation. Require a pose or motion gate for animated work.

## Handoff

When passing to retopology/rigging/animation/export, report:
- body plan and primary reference species;
- stylization and anthropomorphic blend decisions;
- protected silhouette/features;
- intended locomotion/actions and extreme poses;
- continuous versus separate geometry decisions;
- known deformation risks;
- topology state and modifiers;
- validation/evidence performed and open gates.

## Completion / stop

Complete when the requested animal/creature form exists, the body plan and silhouette are coherent, species/style identity reads at the intended viewing scale, protected data survived, and the mesh is appropriate for the declared next stage.

Stop and report instead of guessing when reference is insufficient to place major joints, hybrid anatomy requirements conflict, a requested edit would invalidate protected rig/weights, or required visual/deformation evidence cannot be obtained.

## Research basis

The practical rules in this specialist skill are distilled from current Blender documentation and production/community guidance. See [research notes](references/research-notes.md), [body plans](references/body-plans.md) and [topology/deformation](references/topology-deformation.md) for the supporting principles and URLs.
