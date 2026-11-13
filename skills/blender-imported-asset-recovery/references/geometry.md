# Local geometry and topology repair

Inspect editable base mesh and evaluated result separately: a modifier can cause
the visible defect while the base mesh is sound. Establish scale and transforms
without automatically applying them. Distances in object-local BMesh coordinates
need conversion/interpretation under nonuniform object scale.

## Welding

Identify the accidental seam or duplicate cluster and its intended adjacency.
Choose a tolerance from measured local separation and the smallest protected
feature/clearance. Preview candidate pairs; select only the intended region and
eligible partners. Never run a scene-wide Merge by Distance as diagnosis.

Use selected Merge by Distance or bounded `bmesh.ops.remove_doubles` only after
the correspondence is justified. For two edge loops, inspect vertex correspondence
and consider stitching/bridging rather than proximity collapse. UV seams are loop
attributes and can remain split across shared mesh vertices; welding is not a
reason to average distinct UV corners. Preserve material assignments, normals,
weights and shape keys or establish their repair before changing topology.

Check vertex/face deltas, connectivity, normals, seam alignment and small-feature
survival. A reduced vertex count alone does not prove successful welding. Closely
spaced eyelids, lips, fingers, cloth layers and moving joints must remain separate.

## Holes and shading

Find boundary edges and trace loops; inspect adjacent surfaces and thickness to
classify accidental versus intentional openings. Select the exact defective loop.
Use Fill for an appropriate simple boundary, Grid Fill for a suitable loop, Bridge
Edge Loops between compatible boundaries, or local reconstruction for complex
curvature. Do not span unrelated holes, cap mouths/sleeves or make every asset solid.

After filling inspect winding, tessellation, continuity, thickness, intersections
and expected boundary count. Assign the patch's material and UVs; check texture
coverage. A large n-gon over a curved gap is not a finished surface repair.

Inspect zero-length edges, zero-area faces and loose unused elements before
selected cleanup. Preserve intentional helper geometry and tiny functional parts.
For normals distinguish geometric winding, sharp edges/smoothing, custom corner
normals and mirrored transforms; correct the cause locally. Recalculate Outside
is not an unambiguous solution for an open two-sided surface. Check diagnostic
lighting, face orientation and the export target when applicable.

## Topology replacement

Use [retopology](../../blender-pipeline/references/retopology.md) for controlled
edge-flow changes; use [sculpting](../../blender-sculpting/SKILL.md) for remesh/sculpt
methods. Prefer local reconstruction while most of the source is usable. Triangles
and n-gons are not defects merely by type; judge deformation, shading and delivery.

Before retopology/remesh/decimation, identify what loses correspondence: UVs,
vertex colors, normals, shape keys, weights, vertex-index consumers and materials.
Retain source geometry for projection/baking and establish attribute transfer and
validation. A working skinned character is not a default voxel-remesh candidate.
Do not silently drop shape keys or assume weight transfer reproduces all poses.

Compare silhouette, dimensions, surface deviation at protected regions, mechanical
clearances and joint bends as relevant. Test original morphs/poses when retained.
Accept only a repair with no material regression outside its authorized scope.
