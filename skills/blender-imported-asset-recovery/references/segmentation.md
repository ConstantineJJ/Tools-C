# Semantic segmentation and part extraction

Use for editable separation of an imported model: glasses, clothing, shoes,
armor, wheels, doors, accessories or assembled product parts. Use
[destruction](../../blender-destruction-assets/SKILL.md) only when physical breakage,
fragments/debris or intact/destroyed variants are requested.

1. Identify requested parts and their actual representation: separate objects,
   disconnected islands, material regions or fused continuous geometry. Inspect
   multiple views, occluded attachments and thickness. Do not infer a part's
   existence from a texture that only paints it onto a flat surface.
2. Specify the extraction boundary and whether the source should lose the part,
   retain a duplicate or form a separate deliverable. Choose the reading implied
   by the task; clarify only if the difference would materially change the result.
3. Separate by Selection for deliberate semantic regions; By Loose Parts or By
   Material only when connectivity or assignments match the requested components.
   Do not explode every triangle/island or every material slot into an object.
4. For fused geometry, cut/reconstruct the local boundary. Fill newly unintended
   holes and create necessary interior/thickness with compatible topology, UVs
   and materials. Do not cap intentional garment openings. Hidden source surfaces
   may be absent; reconstructed surfaces are inferred and require visual review.
5. Use descriptive part names and a compact source-to-part map. Preserve world
   placement, scale, hierarchy and intended origins. Choose a hinge/wheel origin
   only when needed by requested movement; test that motion for collisions/gaps.
6. Retain UV corner data, material slots, image links and relevant vertex groups,
   armature modifiers and shape keys. Separate/duplicate operations may lose or
   invalidate dependent data; verify it instead of assuming operator success.
7. Inspect each part and the reassembled model: missing faces, overlaps, open cuts,
   duplicate surfaces, seams, pivot behavior and original silhouette. After replacing
   an imported part, inspect hidden/rear sides and the old source mesh for leftover
   tabs, brackets, supports and disconnected fragments that pierce the new part. If requested,
   export each named part individually and fresh-import each file, verifying the
   expected part is present and the retained original/checkpoint is excluded.

For shared datablocks isolate only the edited instance. Do not rename bones,
Actions or resource paths that consumers rely on simply to make names tidier.
Segmentation is complete when the requested components work separately and still
fit together; an increased object count is not acceptance.
