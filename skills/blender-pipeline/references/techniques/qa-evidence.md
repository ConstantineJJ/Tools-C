# QA evidence matrix

Use this detail only for a scoped review that needs a repeatable checklist.

| Area | Evidence |
|---|---|
| Geometry | object count/names, hierarchy, transforms, normals, missing or duplicate shells, visible intersections |
| Reference | same-projection overlays, landmarks, part count, silhouette and depth |
| Topology | counts, non-manifold/loose/degenerate geometry, mirrored seams, density where deformation needs it |
| Rig | expected names/hierarchy/deform flags, rest pose, binding, constraints, intended scale |
| Deformation | neutral and required bent/twisted poses, volume, pinch, intersections and shading |
| Animation | exact Actions/ranges/channels, extremes/contact, loop endpoints, root motion, pops and foot sliding |
| Export | selected objects, helpers excluded, transforms, materials, skeleton, clips, fresh import |
| Target engine | scale/orientation, actual playback, material appearance and runtime behavior when applicable |

Use fixed diagnostic views appropriate to the asset; front, back, left, right and three-quarter views are a useful character default, while a focused repair may need fewer views. Diagnostic lighting should reveal shape. Restore temporary poses, cameras and display state after inspection.

BLOCKER prevents required use or export. MAJOR is a visible or functional defect. MINOR does not block the scoped stage. NOTE is an optional issue outside scope. Report evidence and likely owner for each finding. Missing access or unrun probes are SKIP with reason, never PASS.
