# Form construction recipes

Use with [form development](form-development.md). Dimensions, asymmetry, anatomy
and detail density follow the project reference and target view, not these fixtures.
Sample one construction before multiplying it through the scene.

## Limb: sections instead of a universal tube

A path with one changing circular radius expresses direction and thickness but
cannot independently express a flatter shin, wider knee or offset calf.
Mark the reference-supported hip/thigh, knee, calf and ankle transitions. Choose
independent transverse width and depth at these sections, with center offsets for
the bend and calf mass. Add intermediate samples for a gradual transition. Inspect
front and profile together; a good front silhouette can conceal constant depth.

Keep stylized soft transitions when appropriate; do not add realistic muscles or
bony landmarks absent from the design. For a seated pose, inspect support, thigh
compression and knee direction. Static form does not certify rig deformation.

The limb example compares a round constant tube with a curved section-controlled
volume. The numerical sections belong to the fixture only.

## Hair: cap, layers, profile, root and tip

Prove cap/parting and the outer silhouette before individual locks. Design a few
large groups, smaller supporting groups and quiet regions; avoid identical widths,
lengths and bends. A flattened section needs separate width and thickness, not a
round pipe scaled after creation. Vary the section along the lock so it can flatten,
turn and taper. Root overlaps should support one hairstyle; scalp exposure may be
intentional only where the design calls for it.

Use a continuous local frame along the path. Re-selecting a global up vector or
forcing the sign of a normal at every sample can flip a ribbon. The helper uses
parallel transport and rejects reversing cusps. Split or resample such a cusp;
do not conceal it with smoothing. Add designed twist after frame construction,
inspect it from another view, and keep width/depth editable.

Use arc length for UV direction from root to tip. A technically aligned map still
needs artistic grouping and varied accents. Check roots, tips, neck, shoulders and
raised arms in the actual pose before increasing strand density.

The hair example isolates a slab-like lock versus a curved, narrowing flat profile.
Production identity and scalp seating remain with the anime/character owner.

## Ribbon: a folded band rather than two ellipsoids

Build a broad strip whose path leaves the knot, bows outward and returns. Choose
width changes, local orientation and slight fold ridges from how fabric is gathered.
Give the band a controlled thickness and distinguish front/back surfaces. Add the
knot and ribbon ends with a plausible connection. A loop needs a readable opening;
an inflated oval does not show where cloth folds or turns.

Gathering near the knot can be sharper than the soft outer loop. Inspect profile
thickness and highlights; smooth shading should not erase fold structure. Do not
introduce cloth simulation merely to build a static bow.

## Fur: base volume, trial tufts, then selective fibers

First shape the tail/body volume and its bend. Test a few soft tufts: their roots
enter the base, their bodies follow growth, and their tips taper with different
lengths and restrained direction changes. Avoid uniformly radial rigid scales.
Inspect silhouette and lit surface before copying the tufts.

Only add fine fibers where their projected size improves edge softness or close
readability. Group many splines into a few named editable curve layers, with shared
materials. Keep quiet areas; equal-density parallel strands can look like straw.
Check whole-frame appearance as well as a closeup. More fibers or stronger bump
is not automatically an improvement.

The fur example compares rigid repeated spikes with a shaped base, a few directed
soft tufts and selective fibers. It does not validate hair simulation or dynamics.

## Canopy: structured masses before leaves

Spheres are useful crown proxies. Before scattering leaves, reshape and arrange
those masses to describe the approved growth/style: dominant and subordinate
groups, directional extension, compressed lower areas and meaningful gaps. Inspect
front and another view without leaves. Do not add independent random noise merely
to disguise a ball.

Build a few leaf clusters with root/attachment direction and internal depth.
Place them according to branches and mass boundaries; vary density in coherent
groups. Let selected outer clusters affect contour while retaining readable space.
The vegetation owner retains species, instancing, wind and representation choices.

## Cost and method switches

Record construction time, object/datablock count, evaluated complexity where useful,
and observed benefit at the target view. Keep source layers editable. If another
attempt only increases density while the same defect survives, change profile,
mass distribution or representation. Project budgets decide acceptable cost.
