# Modeling modifiers, transforms and handoff

Read when a modeling edit changes modifier stacks, object naming, transforms or downstream editability.

Choose modifier order from the actual mesh and intended result. Mirror, structural operations, bevel/support, subdivision and correction may be useful, but there is no universal stack. Keep Mirror editable while symmetry is useful; inspect Boolean output before subdivision; do not add subdivision merely to raise vertex count. Check the evaluated mesh and exporter behavior before applying a modifier.

Use project naming conventions where they exist; otherwise use stable semantic object names instead of temporary names such as Cube.013. Do not encode temporary topology state in a production name. Record which modifiers must stay editable and which downstream tools require applied geometry.

Before rig or export handoff, inspect unit scale, object transforms, origins, mirrored negative scale, normals and visible shading. Applying scale can alter distance-based modifiers; applying armature transforms after binding can invalidate downstream work. Diagnose before changing transforms. Smooth shading does not repair bad geometry.

Check the affected front/side/back and three-quarter views as appropriate, then inspect surface continuity, unintended intersections, duplicate/internal faces, transform sanity and modifier state. Handoff the locked silhouette, changed objects, symmetry, expected deformation, topology status and remaining limitations.
