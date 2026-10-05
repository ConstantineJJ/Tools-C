## Workflow

Use the least complex representation that can satisfy silhouette, density, animation and target-camera needs.

### Pass 1 — scale, trunk/stem and crown silhouette

Block the plant with simple curves, cylinders or low-resolution branches. Establish:
- ground/root anchor;
- overall height and crown width;
- trunk or main-stem taper;
- primary branch directions and attachment heights;
- crown mass/negative spaces;
- dominant asymmetry and lean where intended.

Use a human/player proxy or another explicit scale anchor. Check from target camera height plus front/side/3/4 views. For trees, the crown silhouette and major branch rhythm must read before individual leaves exist.

Do not add bark chips, leaf cards, veins, flowers or grass blades while the primary plant silhouette is unstable.

### Pass 2 — branch hierarchy and taper

Build branch levels from structural importance outward.

For each level, decide:
- parent branch/stem;
- attachment direction and angle range;
- length/taper relative to the parent;
- curvature/droop/uplift;
- density and spacing;
- where branches terminate into leaf/needle clusters.

Avoid perfectly even radial spacing unless the species/style requires it. Variation should be structured, not white noise: repeated growth rules plus controlled exceptions usually read more naturally than independent random transforms.

Preserve readable junctions at target distance. Do not spend topology on invisible twig junctions if a baked/card cluster will replace them.

### Pass 3 — choose leaf/blade/petal representation

Choose by projected size, depth/parallax, alpha cost and style.

Use **direct geometry** when:
- leaves/blades are large enough to affect silhouette or close parallax;
- the style is low-poly/graphic and geometry itself is the visual language;
- target platform/material pipeline makes alpha cards undesirable.

Use **cards/atlases or baked clusters** when:
- many small leaves/needles/grass blades would be expensive as unique geometry;
- a branch/leaf cluster can be represented efficiently from target distances;
- alpha/opacity is supported and acceptable for the target.

Use **hybrid** when hero leaves/outer silhouette use geometry while dense interior foliage uses cards/clusters, or when close branches remain geometric but far crown density is card-based.

Do not choose cards merely because vegetation often uses them. At close range poor cards can reveal flat intersections, alpha overdraw and repeated silhouettes; at distance excessive geometry can waste performance without improving readability.

### Pass 4 — build reusable foliage clusters

Create a small set of representative leaf/needle/flower or grass clusters before filling the whole plant.

A cluster should have:
- a clear attachment/root point;
- silhouette that reads from the expected view range;
- enough internal depth/orientation variation to avoid one flat plane;
- controlled card intersections rather than coplanar z-fighting;
- consistent material/atlas usage;
- pivot/orientation data that supports placement and, if required, downstream wind.

When using cards, cut/shape the plane around useful opacity regions rather than retaining large empty transparent rectangles if the target benefits. Add limited bends/segments when that materially improves fullness from multiple angles.

Normal editing is style-dependent. Upward or spherical/cluster normals can help specific stylized grass/canopy looks, but do not make them a universal rule; compare against the approved shading target.

### Pass 5 — grass, shrubs and patch composition

For grass/meadow/shrub assets, avoid one identical tuft repeated everywhere.

Build a compact vocabulary such as:
- short/dense patch;
- taller sparse patch;
- tufted or directional patch;
- broadleaf/weed/flower accent;
- small/medium shrub cluster;
- edge/transition patch where needed.

The exact set depends on the biome/style. Real meadows often mix blade heights and plant types; use that observation to build controlled diversity rather than random color/scale noise.

Test each patch from several angles and in a small group. A patch that looks full in front view can disappear or become obviously card-like from the side.

### Pass 6 — variation without losing species identity

Create variation from meaningful axes:
- age/size class;
- trunk lean and primary branch distribution;
- crown width/density;
- missing/dead branches;
- leaf cluster density;
- seasonal color/state;
- flowering/fruiting state;
- controlled wind-rest pose differences where appropriate.

Keep stable species/family cues: characteristic trunk taper, branch tendency, leaf scale, crown architecture and material language. Randomly scaling every branch or rotating every cluster independently can destroy identity while still looking "varied."

Prefer a small set of strong source variants plus procedural placement variation over thousands of unique meshes.
