# Blender Organic Sculpting

Use for organic volume, contour and surface corrections in Blender. Use [modeling](../../blender-character-modeling/SKILL.md) for primary construction and [retopology](retopology.md) for edge-flow repair.

## Instruction Priority

Follow the user's target and protected regions, the project/reference contract, then [pipeline core](core.md). A preferred sculpt technique cannot justify altering final topology, weights or approved silhouette outside scope.

## Domain constraints

- Protected: approved proportions, surrounding landmarks, intentional asymmetry, and production topology/weights unless replacement is in scope.
- Owned edits: the named object/region and the minimum neighboring transition.
- Acceptance: the requested form reads in relevant fixed views without new contour, surface or deformation defects.

## Workflow

Inspect the target mesh, transforms, reference landmarks, symmetry and whether topology is disposable. Choose a bounded operation with an explicit coordinate space, center, radius, falloff, strength and protected region. Controlled region editing is useful for measured corrections; Blender brushes are suitable when gestural form matters. Read [sculpt operations](techniques/sculpt-operations.md) only when implementing a regional algorithm or choosing a destructive representation.

Work from macro volume toward medium transitions and fine surface detail. Use Dyntopo or voxel remesh only when topology replacement is in scope, a recoverable source exists and downstream weights/shape keys are accounted for. Confirm the smallest feature survives the chosen resolution.

## Anti-degradation and stop

Compare before/after fixed views and affected poses. Check silhouette, another view, surface integrity and deformation where relevant. Keep, correct or restore the pass according to the observed result. Stop when the target form is achieved, further passes add noise, or the defect belongs to reference registration, topology, rigging or weights. Hand off locked silhouette, joint landmarks, thin parts, required creases and any retopology need.
