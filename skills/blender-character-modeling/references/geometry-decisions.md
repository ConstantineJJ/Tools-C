# Character geometry decisions

Read when a modeling task needs construction choices for forms, joints or separate parts.

Start a blockout with editable low-detail volumes suited to the shape: simple rounded forms, low-resolution custom meshes, curves or mirrored half-meshes where useful. Name production objects semantically from the start. Check head/body relationship, torso taper, shoulder/hip width, limb lengths, hand/foot mass and major costume silhouette against the active reference.

Reserve space for intended motion before rigging. Shoulders need room for the required arm range; elbows and knees need a bend region rather than a razor hinge; wrists and ankles need a transition; hips should avoid uncontrolled pinch. These are modeling allowances, not a substitute for final deformation topology or weight tests.

Separate armor, belts, accessories or cloth pieces when they function as separate surfaces. A continuous deforming body surface may need continuous geometry. For hands and faces, choose detail from intended view distance and interaction needs: silhouette and thumb opposition may matter more than fully articulated fingers; eyes should read from relevant views without accidental floating or z-fighting.

Classify clothing as rigid, skinned, bone-driven, baked or engine-simulated only when downstream behavior is known. Geometry needs enough segments for its intended bend, but avoid density that adds no visible or deformation value. Blender live Cloth is not automatically live cloth in a GLB target.

Spend detail on the forms that read at the target distance. Large silhouette and body masses come first; medium details follow; tiny seams, folds and bevels wait until primary proportion is accepted. Do not infer a universal gameplay camera, polygon count or anatomy template.
