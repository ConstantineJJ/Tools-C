# Character body proportions: reference-led modeling guide

This is a **character-modeling** aid, not a second anatomy owner, fixed skeleton
specification, retopology rule or rig prescription. Use it for a new/revised
humanoid blockout when proportions matter. The approved character design,
user-supplied references and the existing PASS 0 / Model Contract outrank these
heuristics. A deliberate stylization is not an anatomical defect.

## Source and measurement

1. Identify the reference role (original, adopted concept, auxiliary), pose,
   age/style intent, framing and camera projection. A perspective screenshot
   or fashion drawing is not calibrated orthographic measurement. Flag occluded
   joints and cropped feet/head as UNKNOWN; do not derive hard ratios from them.
2. Establish a **head unit** consistently: estimated crown of the skull to chin
   (exclude hair volume, hats and accessories). Record full standing height
   from sole/ground to skull crown in the same pose and projection. Keep
   hair silhouette height as a separate measurement.
3. Mark visible landmarks: crown, chin, shoulder line, sternum/chest, waist,
   pelvis/crotch, hip width, elbows, wrists, fingertips, knees, ankles and
   foot-ground contact. Do not equate all drawn horizontal grid lines with
   anatomical joints; pose and illustration conventions can shift them.
4. Prefer orthographic/near-orthographic front and side views for comparative
   ratios. Compare head width and depth, neck, shoulder span, torso length,
   pelvis width/depth, upper/lower leg, arm span and hand/foot mass. Verify
   left/right features separately where asymmetric.
5. Record only a few meaningful numeric **ranges**, ratios and positional
   anchors supported by the reference or the adopted design; otherwise state
   qualitative intent and uncertainty. Choose tolerances before measuring the
   candidate, not after it fails. Do not infer a child's age or real human
   measurements from a stylized proportion sheet.

## Style families (heuristics, NEVER automatic gates)

Choose and document the intended silhouette before blockout. These are useful
starting families, not sex/age requirements or fixed pass thresholds:

| Profile | Typical artistic emphasis | What not to normalize |
|---|---|---|
| Realistic adult / realistic feminine | Natural head-to-body balance, differentiated rib cage/waist/pelvis, functional joints | Reference-specific shoulder/hip relationships, posture, body diversity |
| Stylized slim | Clear long-line silhouette, controlled torso/leg balance, simplified masses | Deliberate narrowness or enlarged hands/feet |
| Anime stylized / chibi | Highly variable head scale and facial emphasis; match the approved substyle | Do not force an eight-head body or realistic facial planes |
| Heroic / broader | Intentionally strong shoulder/torso silhouettes, enlarged masses or elongated limbs | Do not "repair" approved heroic exaggeration |
| Child / young character | Age-/design-specific changes in relative head, torso and limb proportions | Do not apply adult ratios or use a single age chart as universal fact |

Traditional drawing charts sometimes use roughly 7–8 head units for an adult
figure and fewer for children; other stylized art deliberately falls outside
these examples. Such grids are **drawing scaffolds**, not empirical measurements
and not a substitute for the actual character reference. Do not use hair
height to inflate the head-unit calculation.

## Checkpoints and protected features

- **Blockout:** compare overall height, separate skull/hair volume, shoulders,
  waist, pelvis, torso/leg division and foot placement in reference-matched
  and neutral orthographic views before fine detailing.
- **Developed form:** check profile volume (skull back, upper back, glutes,
  knees/elbows), continuous shoulder/neck/waist transitions and clothing fit;
  verify that masses are not independent inflated spheres unless intended.
- **Revision:** specify WHAT MAY CHANGE vs APPROVED/PROTECTED landmarks,
  for example preserve eye spacing/mouth and foot-ground anchors while
  reducing only rear skull or external hair volume. Track changed geometry
  and re-evaluate its dependent clothes/straps/ornaments.
- **Pre-rig handoff:** declare an explicit proportion/form disposition
  (ACCEPTED, OPEN with named defects, or NOT_EVALUATED), supporting views,
  Model Contract reference if present, intended bend clearances and locked
  measurements. Rigging cannot turn an unchecked silhouette into a validated one.

## Camera and projection caution

A 45-degree high/low view can expose contact defects, underside anatomy and
volume discontinuities, but its apparent head/feet scale may be distorted by
perspective and foreshortening. Treat it as shape/contact evidence, **not** an
independent reason to resize a correctly proportioned head or legs. Confirm a
proportion concern on comparable orthographic views and against the locked
reference before changing geometry. Orthographic oblique views still
foreshorten lengths along the viewing direction.

For PASS 0 use existing `relative_dimensions`, `silhouette_notes` and
`model_contract.rules` (dimension/ratio/anchor) with supported evidence and
explicit uncertainty; do not create a competing proportions.json, alter the
schema or promote guesses into HARD/PROPORTION LOCK rules.
