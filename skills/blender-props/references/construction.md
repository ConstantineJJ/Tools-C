## Workflow

Use the least complex representation that can satisfy silhouette, shading, interaction and delivery needs.

### Pass 1 — blockout, scale and silhouette

Build the complete object from simple volumes. Establish bounding dimensions, major negative spaces, center of mass/readability, interaction points and dominant silhouette.

Use the appropriate scale anchor: hand proxy for hand-held props, seated/standing human for furniture, shelf/table/door context for interior props. Inspect the target gameplay/camera view, not only a neutral turntable.

For first-person or inventory props, identify the surfaces that dominate the actual view. Those regions may justify more geometric/texture attention than hidden undersides.

Do not add screws, scratches, fabric wrinkles, embossed logos or edge damage while primary proportions remain unstable.

### Pass 2 — prove function and assembly

Before polishing, identify:
- which pieces carry load or provide structure;
- which parts are separate because they move, open, fold, detach or use a different material/process;
- where clearances/gaps are functionally necessary;
- how handles, hinges, knobs, fasteners and panels actually attach;
- what can be simplified because it is never seen or used;
- what must remain separate for animation, interaction, variants or export.

A believable prop does not need every hidden internal component, but visible construction should explain how the object holds together. If stylized, preserve the same functional logic while exaggerating intentionally.

### Pass 3 — choose direct mesh versus high/low/bake

Do not treat one production pipeline as universal.

Use **direct realtime geometry** when:
- the form is simple enough to shade well directly;
- target view benefits more from geometric bevels/silhouette than baked micro-detail;
- the prop is low-detail/background or stylized;
- maintaining editability is more valuable than a separate high poly.

Use a **high/low bake** when:
- complex bevels, sculpted wear, engravings, relief or high-frequency shape detail would be expensive in realtime geometry;
- hero/close-view fidelity warrants a dedicated high source;
- the target pipeline explicitly expects baked tangent-space detail.

Use **hybrid** when some pieces are best modeled directly and others justify baking/sculpting.

Blockout remains upstream of all three choices. If the high source changes silhouette materially, revise the low/source representation rather than forcing the bake to conceal mismatch.

### Pass 4 — hard-surface construction and editability

Choose tools by function:
- Mirror for true or temporary symmetry;
- Bevel for real edge width/highlight shape;
- Boolean for stable cutouts/recesses where it saves work;
- Solidify for sheet thickness when appropriate;
- Array/linked duplicates for repeated slats, screws or repeated subcomponents;
- subdivision where smooth controlled curvature is needed;
- weighted/custom normals only as a shading aid after geometry is sound.

Keep symmetry/modifiers live while they support iteration. Break symmetry deliberately when the reference/design requires different geometry or unique wear, not merely because the model is "almost finished."

Inspect transforms before dimension-sensitive bevels, solidify, arrays, baking or export. Apply transforms only when appropriate for the hierarchy/animation/instance state; do not destructively normalize objects by habit.
