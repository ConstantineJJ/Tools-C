# Bounded sculpt operations

Read when a regional sculpt must be scripted or when deciding between non-destructive correction, brush work and remeshing.

Address the mesh by name and define object-local or world coordinates. Specify center/landmark, radius relative to the feature, falloff, strength, axis or displacement, symmetry plane, protected set and iteration count. Confirm object transforms before converting coordinates. A smooth falloff avoids a visible ring at the region boundary; sharp falloff is reserved for intentional ridges.

- Deform/grab: move a bounded vertex set by weighted delta; protect the transition.
- Inflate/deflate: move along normals or radial directions while checking silhouette taper.
- Smooth/relax: limit shrinkage, retain locked contour and sharp intended edges.
- Pinch/crease: define an axis or path and check self-intersections.
- Flatten: fit a local or reference plane without affecting neighboring curvature.

Brush strokes are appropriate for gestural surface flow, with brush, path, radius and number of passes constrained. Dyntopo and voxel remesh replace topology: use only on disposable topology with a checkpoint and a retopology plan. Set remesh resolution from the smallest required form and inspect thin parts, gaps and holes afterward. Never assume weights, UVs or shape keys survive a destructive pass.
