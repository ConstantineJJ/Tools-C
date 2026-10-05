### Pass 6 — surface and UV strategy

Choose texture allocation by reuse, size and camera needs:

- **shared/tileable materials** for generic painted metal, wood, concrete, rubber or other reusable surfaces;
- **trim/atlas/shared sheet** for families that repeat edge profiles, bands, labels, hardware or material zones;
- **unique texture** where a small/medium hero fixture needs distinctive wear, graphics or baked high-frequency detail;
- **hybrid** for a reusable material base plus local labels, decals, dirt masks or unique accents.

Use project-defined texel-density targets; do not invent a universal px/m value. Maintain coherent density across assets intended to coexist, with deliberate exceptions only for readability/hero needs.

Plan mirroring/stacking before adding unique asymmetrical wear. If UVs share or mirror regions, keep strongly recognizable damage/labels away from those shared areas unless repetition is intentional.

### Pass 7 — weathering and storytelling without noise

Wear follows material, exposure and use:
- ground-facing regions collect splash/dirt differently from upper surfaces;
- water runoff follows gravity and drainage paths;
- hand/contact zones polish or abrade differently from protected recesses;
- painted metal chips differently from plastic, galvanized steel, wood or cast concrete;
- bolts, welds and seams can trap dirt or corrosion, but not every edge needs equal wear.

Use a hierarchy: large material breakup first, medium use/environment effects second, small scratches/chips last. Avoid uniform procedural grunge over the entire asset; it destroys material identity and makes repeated props visibly identical.

For families, vary high-recognition storytelling layers while keeping shared construction/material logic. Color, decal, dirt and damage variants are often cheaper and safer than arbitrary geometry changes.

### Pass 8 — pivot, packaging and placement test

Choose pivot/origin by how the asset will actually be placed:
- freestanding object: usually a stable base point such as bottom-center or a documented corner/anchor;
- post/fixture: base center or installation anchor;
- wall-mounted object: mounting point/plane;
- fence/railing panel: deterministic endpoint/corner anchor if the panel must chain;
- hinged/moving part: its real articulation point for the moving component, not necessarily the asset root.

The exact convention is project-specific; consistency inside an asset family is the invariant.

Test at least one realistic placement context. For repeated assets, place several instances with the intended spacing/orientation and confirm that:
- scale reads correctly next to the environment;
- bases contact the ground/mount surface without sinking or floating;
- pivots support deterministic placement;
- repeated silhouettes do not create unintended visual rhythm/noise;
- intended shared data remains shared;
- variants remain compatible with the family placement logic.

Where an asset is intended for a reusable library, package meaningful dependencies together and preserve clear asset-level hierarchy. Blender's Asset Browser supports linked/appended assets and collection instances; choose a reuse method consistent with whether downstream edits should propagate.
