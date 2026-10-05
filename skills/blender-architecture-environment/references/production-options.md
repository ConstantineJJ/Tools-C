### Pass 6 — material and UV strategy

Choose texture strategy from reuse and camera needs:

- **tileable materials** for broad walls, floors, roof fields and repeating surfaces;
- **trim sheets** for repeated edge bands, frames, moldings, beams, rails and architectural motifs;
- **unique bakes** for hero elements whose distinctive detail justifies the texture cost;
- **hybrid** for architecture that combines large tileable surfaces with unique inserts or trim-driven details;
- **decals/masks/secondary UVs** for local storytelling, dirt, signage, repairs and variation when supported by the target pipeline.

Maintain project-consistent texel density unless an explicit hero/readability reason justifies a different allocation. Do not bake unique large textures for every wall merely because it is convenient.

When a trim sheet or tileable material repeats widely, avoid large unique stains/cracks that reveal obvious periodic repetition. Put high-recognition variation into decals, vertex/mask layers, dressing or controlled variants.

### Pass 7 — variation without breaking the kit

Break repetition while preserving dimensions and snap behavior. Useful variation layers:
- interchangeable window/door/facade modules with the same footprint;
- roof/dormer/end-cap variants;
- material or UV offsets where valid;
- decals, signs, damage overlays and color changes;
- handoff props/vegetation;
- selective unique hero sections.

Do not "add uniqueness" by scaling modular pieces off-grid or arbitrarily moving pivots. Variation should preserve the assembly contract unless the piece is deliberately reclassified as unique.

### Pass 8 — assembly and target-context test

Assemble at least one representative structure from the final modules. If the kit is intended for multiple layouts, assemble a second materially different layout or stress case.

Verify:
- modules snap without manual micro-adjustment;
- corner, opening, floor and roof interfaces close cleanly;
- no visible cracks, doubled surfaces or z-fighting at common joins;
- repeated parts retain shared data/instances where intended;
- silhouette and scale still match the blockout/reference;
- material scale and direction stay coherent across adjacent pieces;
- target-engine import, collision, lightmap/UV or LOD requirements are handed to the appropriate owner rather than assumed.

A structurally valid module library is not visually accepted until representative assembled views have been reviewed.
