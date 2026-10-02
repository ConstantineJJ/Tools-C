# Research notes — roads & infrastructure

Research snapshot: 2026-10-02.

This file records the external principles used to design `blender-roads-infrastructure`. Blender documentation is treated as software-behavior authority. Environment-art tutorials/interviews are treated as production practice, not universal standards. Project-specific dimensions, road standards, LOD budgets, collision rules and texel-density targets remain in project profiles/contracts.

## Blender Manual — Curve to Mesh (4.5 LTS)

Source:
https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/curve/operations/curve_to_mesh.html

Key points used:
- `Curve to Mesh` converts splines into mesh and can extrude a custom profile curve along the route;
- profile-derived sharp edges can propagate to the generated mesh;
- generated geometry is suitable for a road/path cross-section workflow, but the node itself does not solve road intersections or design constraints.

Applied in the skill as a controlled centerline + cross-section representation, not as a mandate that every road use Geometry Nodes.

## Blender Manual — Curve geometry

Source:
https://docs.blender.org/manual/en/dev/modeling/curves/properties/geometry.html

Key points used:
- curve geometry can be extruded/beveled and controlled by curve radius/tilt;
- a custom bevel/profile object defines cross-section shape;
- curve tilt/orientation matters to generated geometry.

Applied to the warning that road/curb profiles can roll or twist unexpectedly when curve orientation is not controlled.

## Blender Manual — Resample Curve (4.5 LTS)

Source:
https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/curve/operations/resample_curve.html

Key points used:
- resampling can produce approximately uniform spacing by count or segment length;
- spacing can be used for downstream repeated placement or evaluation;
- unnecessary resampling density should not be assumed to improve visible output.

Applied to procedural road markings, repeated edge elements and performance guidance.

## Blender Manual — Sample Curve (4.5 LTS)

Source:
https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/curve/sample/sample_curve.html

Key points used:
- a route can be sampled by factor or distance along the curve;
- sampled position, tangent and normal information can drive orientation or downstream attribute logic;
- distance-along-route is a useful stable basis for repeated placement and longitudinal mapping.

Applied to orientation, distance-based UV/material logic and repeated-element placement.

## Blender Manual — Curve nodes overview

Source:
https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/curve/index.html

Key points used:
- Blender exposes curve length, tangent, tilt, normals, resampling, trimming and curve-to-mesh operations as separate tools;
- modifier ordering can change whether geometry is still treated as a curve.

Applied as a safeguard against opaque node stacks where a later road operation silently receives mesh data instead of the intended curve source.

## BlenderNation — Geometry Nodes and UV Mapping in Blender (Michael Bridges, 2024)

Source:
https://www.blendernation.com/2024/06/13/geometry-nodes-and-uv-mapping-in-blender/

Source type: tutorial summary / community production workflow.

Key practices used:
- build a road from a curve and Geometry Nodes;
- generate/capture attributes along the curve for UV mapping;
- resample the route where needed;
- maintain uniform texture scale along generated road geometry;
- expose road width as an external control instead of burying it in the node graph;
- use route-length diagnostics to troubleshoot procedural behavior.

Applied as practice, not as a Blender specification. The skill generalizes this into: preserve editable route data, use stable distance metrics for longitudinal UVs, and expose meaningful parameters.

## 80 Level — Procedural Road Generator Made Using Geometry Nodes (Bbbn19, 2022)

Source:
https://80.lv/articles/geometry-road-generator-blender-geometry-nodes-new/

Source type: artist tool showcase.

Key practice used:
- curves can function as editable road centerlines and feed a customizable Geometry Nodes road generator;
- road parameters can remain editable in a modifier rather than baking the road immediately.

Used as supporting evidence for non-destructive centerline-driven workflows, not as proof that procedural roads are always better than modular meshes.

## 80 Level — Tutorial: Cutting Roads Into Terrain (XOIO, 2019)

Source:
https://80.lv/articles/tutorial-cutting-roads-into-terrain

Source type: tutorial summary.

Key practice used:
- a road can be integrated into steep terrain while maintaining controlled edge loops around the route;
- preserving usable topology around the road makes later texturing/refinement easier;
- the same approach can support serpentines/mountain streets rather than only flat roads.

Applied as the terrain-integration rule: avoid accepting an uncontrolled projection/boolean scar when an editable road-edge corridor is needed for refinement.

## 80 Level — Creating an Immersive Urban Street Scene Using Blender & Substance 3D (Pauline Ferrand, 2026)

Source:
https://80.lv/articles/creating-an-immersive-urban-street-environment-using-blender-and-substance-3d

Source type: environment-artist interview / production breakdown.

Key practices used:
- pre-production asset/material breakdown before modeling;
- blockout in Blender to establish camera, building/street proportions and scene scale;
- consistent texel density across assets intended to coexist;
- tileable materials built from large-to-medium-to-small detail rather than trying to model every surface feature;
- shader/material strategies may differ by asset class rather than forcing one universal material system.

Applied to route blockout, scale consistency and separation of geometry decisions from road-surface detail.

## 80 Level — Procedural Pathways tutorial summary (Blender 4, 2024)

Source:
https://bazaar.blendernation.com/listing/geometry-nodes-blender-4-tutorial-procedural-pathways-step-by-step/

Source type: tutorial outline.

Key practices used:
- curve-driven procedural paths can use `Curve to Mesh`, resampling and repeated blocks/instances;
- path-generated repeated elements can be varied without destroying the editable source route.

Used as supporting practice for trails/pavers and keeping route-level control separate from local detail variation.

## 80 Level — Roads add-on with junction support (2025)

Source:
https://80.lv/articles/check-out-this-blender-add-on-for-easy-road-creation

Source type: tool showcase, not a production standard.

Key observation used:
- practical road tools treat junctions as explicit features, including multi-road intersections, rather than relying only on independent strip extrusion.

Applied to the skill's requirement that intersections are first-class topology events.

## 80 Level — WIP photoreal road generator (Ethan Davis, 2024)

Source:
https://80.lv/articles/this-wip-system-allows-one-to-generate-photoreal-3d-roads

Source type: artist tool showcase.

Key observation used:
- road curvature, guardrail placement and terrain adaptation can be driven together from a procedural route;
- terrain integration is a coupled system, not merely a final visual offset.

Used as supporting evidence for treating route, terrain and roadside systems as coordinated but separately owned data.

## Synthesis used in the skill

The sources converge on several durable principles:

1. Keep the route/centerline editable as long as practical.
2. Define road/path cross-section and scale before surface detail.
3. Curves/Geometry Nodes are valuable for continuous editable runs; modular or explicit meshes remain useful for standard junctions and difficult transitions.
4. Intersections, tight corners and terrain seams require explicit validation; successful node evaluation is not acceptance.
5. Longitudinal texture mapping should be based on stable distance/route logic rather than accidental control-point topology.
6. Road/terrain integration should preserve enough controllable edge structure for later texturing/refinement.
7. Test infrastructure both from plan view and target-height ground/traversal context.
8. Keep project-specific dimensions, standards and budgets outside the universal skill.
