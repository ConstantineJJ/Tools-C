# Animal construction and regional revisions

Read for animal form construction, muzzle/ear/eye integration, or a geometry
revision on an already groomed creature. The filename is a stable reference path;
these are scoped checks, not a new compulsory stage engine.

## Construct the species in volume

Use a simplified skeletal scaffold to locate joints and support the surface.
Marshall Vandruff's animal-anatomy workshop teaches bones, muscles and torso/head
forms as volumes seen from several views; Gaël Kerchenbaum's lynx study explicitly
studies skull, skeleton and écorché. Apply that reasoning at task scale: landmark
markers and coarse masses often suffice. A complete internal skeleton mesh is
not mandatory for every asset.

- Establish ribcage, pelvis, spine arc, skull and jaw as related masses; read the
  neck and shoulder transitions as volumes rather than tubes glued to spheres.
- For mammalian quadrupeds locate scapula/shoulder, elbow, carpus, hip, stifle,
  hock and digits from the chosen species. Keep plantigrade, digitigrade and
  unguligrade contacts distinct. Birds, reptiles and hybrids need their own plan.
- In the requested stance inspect each supporting foot against the same ground
  plane and the distribution of support under the trunk. Lifted limbs are valid
  when specified. Static support does not prove a gait or deformation quality.
- Separate underlying body dimensions from the coat envelope. A long-haired
  animal's visible chest, cheeks and tail width are not all skin volume.

For comparable profile/front references use
[reference registration](../../blender-pipeline/references/techniques/reference-registration.md).
Record source authority per region. A visible iris center is a projection of an
external feature, not automatically the hidden eyeball center. Mark which kind
of landmark each measurement represents. Perspective photos constrain appearance;
they do not supply exact orthographic widths without camera reasoning.

## Head and appendage construction

Resolve skull versus muzzle length, jaw hinge/chin, cheek support and eye volume
with the chosen species references. Place the eyeball as a volume, then wrap the
eyelid margin and surrounding tissue around it. A continuous skin object can still
contain an unnatural shelf or U-shaped ridge; object count cannot certify anatomy.
Inspect a clay closeup and a profile/three-quarter view before accepting a change.
Retain intentional graphic eyelids in a stylized design.

Treat the ear as a pinna with thickness, opening, root and transition into the
head. Define the root's anatomical placement and eye clearance separately from
the tip silhouette; moving a tip does not validate its base. Surface proximity or
being inside the skull volume alone is insufficient. Use a bounded root rebuild
if the existing attachment cannot represent the requested shape. Tail roots,
wings, horns, whisker pads and paws need equivalent support/clearance reasoning.

## Revise an existing animal at any stage

A user may request broad geometry changes after grooming or texturing. Do them
within the approved scope. Before editing, identify affected skin, eye rims,
ear/tail roots, whiskers/follicles, groom guides, surface UV attachment and color
projection. Keep the last useful state for a fixed-view comparison. Do not label
the user's revision a workflow failure or impose a full restart.

After editing, treat those dependencies as needing inspection/rebinding; this is
an agent action, not an automatic Blender invalidation system. For fixed topology
and preserved surface UVs, test the existing attachment/deformation route first.
After topology/UV replacement, reattach and repair guides or regenerate the
affected groom region when preservation is unreliable. Keep unaffected grooming.
Read [sculpt revision mechanics](../../blender-sculpting/references/regional-revisions.md)
for representation selection and protected volumes.

## Coat and scoped review

Use regional guide directions and length transitions; distinguish undercoat,
guard hairs and characteristic tufts when the target needs them. Evaluate skin
alone, roots/guides and final coat/material independently. Inspect both sides,
ear backs, cheeks and seams under neutral light. Count visible/evaluated strands
separately from stored hidden or zero-radius curves; counts do not prove coverage.
Follow the surface workflow for native Hair Curves attachment and materials.

Name the feature, revision and images supporting each observation. A better nose
profile is a scoped result; the full head/body needs its own evidence. Save/reopen,
technical integrity, visual likeness, rig deformation and engine behavior remain
separate checks. Use motion/rig owners only when those outcomes are requested.

Sources and limits: [research notes](research-notes.md), refreshed 2026-10-21.
