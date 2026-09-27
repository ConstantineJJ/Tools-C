# Blender Retopology and Deformation

Use for production mesh topology, edge flow and deformation repair. Diagnose weights, pivots and rest pose before replacing mesh topology for a bend defect.

## Instruction Priority

Follow the user's deformation target and target-engine contract, then [pipeline core](core.md) and approved form. Quad preference and generic mesh rules do not outrank observed deformation or silhouette.

## Domain constraints

- Protected: approved silhouette, UV/material dependencies, vertex groups and rig data outside the repair.
- Owned edits: the specified mesh region, local density and necessary skinning dependencies.
- Acceptance: affected joints survive required poses, shading and silhouette remain valid, and no topology defect blocks the target export.

## Workflow

Confirm form and joint landmarks are stable, then identify deforming versus rigid zones and required motion range. Place density where silhouette and bending require it. Test the topology in neutral and relevant extreme poses; use the target project's ranges rather than a fixed humanoid checklist. Read [deformation checks](techniques/deformation-checks.md) when planning joint loops or diagnosing pose failures.

Quads help in deforming/subdivided areas, while intentional triangles can be valid in game meshes. Keep poles away from high-bend or critical highlight areas. Auto-retopo is a starting point, not acceptance evidence. For a failed bend, inspect pivot, weights, loop distribution and volume in that order; use a local corrective shape only for a known residual pose issue.

## Anti-degradation and stop

Compare fixed views, pose tests, shading, seams, UVs, material slots and vertex groups affected by the edit. Stop when required pose range and export checks pass without material regression. If primary form is still changing, defer final topology unless the user requested an interim mesh. Hand off mesh names, rest pose, joint landmarks, extreme poses and topology exceptions.
