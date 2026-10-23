# Research notes — vehicle modeling

Research snapshot: 2026-10-02.

This file records external principles used to design `blender-vehicle-modeling`. Blender documentation is treated as software-behavior authority. Vehicle/prop artist breakdowns supply production practice and heuristics, not universal project contracts. Exact triangle counts, texture resolutions, wheel-collider setup, physics values, LOD ratios and platform budgets remain project-local.

## Blender Manual 4.5 LTS — Mirror Modifier

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/mirror.html

Key points used:
- Mirror operates around object origin or a separate Mirror Object and can remain non-destructive;
- merge/clipping can maintain a clean symmetry plane;
- the mirror plane/origin must be positioned deliberately for exact symmetry;
- UV mirroring/offset controls exist, which matters for later baking/asymmetrical texturing.

Applied as the default preference to keep symmetric vehicle body/components mirrored while symmetry remains valid, and to treat the center plane/origin as production data rather than a cosmetic transform.

## Blender Manual 4.5 LTS — Modifiers / stack order

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/introduction.html

Key points used:
- modifiers are non-destructive until applied;
- stack order changes the result;
- Mirror/Subdivision and other vehicle-friendly combinations should be kept editable while primary surfaces are changing.

Applied as a safeguard against destructive cleanup before body shape and low/high handoff are proven.

## Blender Manual 4.5 LTS — Subdivision Surface

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/subdivision_surface.html

Key points used:
- Catmull-Clark smooths a low-control mesh into a higher-density surface;
- support loops/creases control sharpness;
- topology and normal continuity strongly affect the smooth result;
- more subdivision is not a replacement for well-placed control geometry.

Applied to sparse-control body-surface modeling and the warning against adding dense loops before primary curvature is solved.

## Blender Manual 4.5 LTS — Weighted Normal Modifier

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/normals/weighted_normal.html

Key point used:
- weighted normals can make broad hard-surface faces shade flatter while preserving sharp edges, but they only affect normals/shading.

Applied to hard-surface components, not as a way to fix wavy car-body geometry.

## Blender Manual 4.5 LTS — Shrinkwrap Modifier

Source:
https://docs.blender.org/manual/en/4.5/modeling/modifiers/deform/shrinkwrap.html

Key points used:
- Shrinkwrap can project or move vertices to a target surface with offsets/limits;
- projection direction and target surface control the result.

Applied as an optional helper for conforming badges, trim, decals/secondary geometry or bounded surface-following parts. It is not treated as a general body-surface solution because projection can inherit target defects and can produce unsuitable topology for moving panels.

## 80 Level — Jakub Piotrowski, Volkswagen Kübelwagen Type 82 (2023)

Source:
https://80.lv/articles/making-a-ww2-era-vehicle-with-blender-substance-3d-painter-marmoset-toolbag

Source type: senior environment artist vehicle-production breakdown using Blender.

Key practices used:
- gather extensive reference before modeling, including mechanical/undercarriage evidence as required;
- start from broad vehicle proportion/blockout before detailed pieces;
- game-ready vehicle work benefits from understanding how the real vehicle is assembled rather than treating panels as arbitrary shapes;
- retopology/optimization decisions should follow the target and visible detail rather than be done blindly.

Applied to reference-by-system and visibility-scoped mechanical detail.

## 80 Level — Creating Realistic Vehicles (general workflow)

Source:
https://80.lv/articles/creating-realistic-vehicles-in-3ds-max-substance-3d-painter

Source type: professional vehicle/prop artist workflow breakdown.

Key practices used:
- begin with a clear final target and extensive references of both whole vehicle and details;
- blockout prioritizes final shape/proportions rather than polycount/topology;
- blueprints are useful vehicle references, but detail work follows only after the overall form is established;
- vehicle panels/hard edges need to be planned with the final high/realtime representation in mind.

Applied as stance/body-first modeling and representation-aware panel planning.

## 80 Level — Abandoned Toyota Corolla E70 (2025)

Source:
https://80.lv/articles/telling-the-story-of-abandoned-toyota-corolla-e70-in-3d

Source type: recent vehicle modeling/texturing breakdown.

Key practices used:
- select the most accurate available blueprint and align/scale views before modeling;
- block major vehicle parts on one half and mirror while symmetry is valid;
- keep base topology manageable, then add support loops/subdivision or bevels where needed;
- non-destructive modifiers can make it easier to derive a lower-detail version later;
- wheel/suspension and body can justify different texture/material allocation depending on target fidelity.

The source's exact triangle/texture-set numbers are project-specific and deliberately not copied into the universal skill.

## 80 Level — Modeling Vehicles for AAA Games (Irfan Haider)

Source:
https://80.lv/articles/modeling-vehicles-for-aaa-games

Source type: senior vehicle artist interview with Forza/DiRT/F1 experience.

Key practices used:
- vehicle work requires dedicated attention to material, decals, visible mechanical pieces and performance target;
- the amount of detail and optimization differs heavily by game/camera/platform;
- production vehicles are systems of body, wheels, interior and repeated parts rather than one undifferentiated mesh.

Applied as scoped detail/LOD guidance and rejection of universal polygon budgets.

## 80 Level — Vehicle Production for Games

Source:
https://80.lv/articles/vehicle-production-for-games

Source type: vehicle-production workflow article.

Key practices used:
- establish an outline/3D blueprint and plan topology/surfaces before pushing density;
- smooth surface continuity and reflection flow across neighboring vehicle elements are critical, especially in mid-poly/smoothed-normal workflows;
- suspension/underbody design varies widely by vehicle class and must be researched rather than copied from one generic mechanical template;
- visible mechanical detail should be selected by importance, optimization and available production time.

Applied directly to body reflection QA and mechanical-depth scoping.

## 80 Level — Mad Max Interceptor in Blender

Source:
https://80.lv/articles/recreating-mad-max-s-interceptor-using-blender-substance-3d-painter

Source type: Blender vehicle/hard-surface workflow breakdown.

Key practices used:
- Mirror, Solidify, Subdivision and Boolean support a non-destructive vehicle workflow;
- modeling progresses from blockout to increasingly smaller detail;
- added accessories/props should support concept/story rather than replace the vehicle's core form.

Applied as tool-choice evidence and primary-before-secondary detail hierarchy.

## 80 Level — Takhion Bicycle in Blender (2022)

Source:
https://80.lv/articles/recreating-a-takhion-bicycle-in-blender-substance-3d-painter-marmoset

Source type: prop/vehicle mechanical modeling breakdown.

Key practices used:
- realistic wheeled assets benefit from researching actual frame geometry, dimensions and angles rather than relying only on perspective photos;
- build big shapes first (wheels/frame/fork), then medium mechanical parts;
- high/low workflows remain valid when close mechanical fidelity justifies them.

Applied to motorcycle/bicycle wheel-center/frame-first logic and mechanical reference gathering.

## 80 Level — Game-Ready Peugeot 403 (2026)

Source:
https://80.lv/articles/creating-a-game-ready-peugeot-403-using-unreal-engine-substance-3d

Source type: recent game-ready vehicle breakdown.

Key practices used:
- a mid-poly approach can be preferable when ongoing iteration matters and maintaining separate synchronized high/low bodies would slow changes;
- hybrid production is practical: some vehicle regions can keep dedicated high sources while others remain editable mid-poly;
- small repeated/details such as screws, lights, tire pattern and bevel-like information can be moved into normal/decal/atlas strategies when appropriate.

Applied as explicit support for direct/mid/high-low/hybrid choice rather than one mandatory vehicle pipeline.

## 80 Level — Sedan-like car + rigging (2025)

Source:
https://80.lv/articles/creating-a-sedan-like-3d-car-using-unreal-engine-5

Source type: game/environment artist vehicle breakdown.

Key practices used:
- modeling and rigging requirements should be considered together because wheel/body/moving-part segmentation affects downstream setup;
- weathering/material treatment and body construction remain separate concerns from runtime rig/physics.

Applied to early articulation-axis ownership and clear rigging handoff rather than building a generic rig inside this modeling skill.

## 80 Level — Toyota Land Cruiser FJ60 / drivable vehicle

Source:
https://80.lv/articles/process-of-making-realistic-3d-toyota-land-cruiser-fj60-in-unreal-engine-5

Source type: vehicle modeling + target-engine preparation breakdown.

Key practice used:
- a drivable vehicle requires clear body/wheel segmentation and stable wheel centers before target-engine vehicle setup;
- runtime tire grip/suspension stiffness/handling are target-engine tuning, not Blender modeling rules.

Applied to the boundary: modeling owns physical axes and pieces; engine/rigging owns runtime driving behavior.

## 80 Level — tire repetition tutorial

Source:
https://80.lv/articles/tutorial-making-of-jeep-willys

Source type: older vehicle tutorial.

Key practice used:
- tire tread is inherently repeated geometry and can be authored from a representative segment then repeated/bent/generated;
- transform/pivot accuracy matters when closing a repeated pattern around a wheel.

Applied as repeat-source guidance without copying the tutorial's exact segment count or tool sequence.

## Synthesis for Tools_C

The recurring durable pattern is:

1. Establish trustworthy axle/wheel metrics, stance and body envelope before detail.
2. Reconcile blueprints with known dimensions and perspective photos rather than treating one sheet as absolute truth.
3. Keep broad body curvature/control topology sparse enough to tune reflection continuity.
4. Preserve symmetry and shared wheel/subassembly data until real asymmetry requires divergence.
5. Treat wheels/tires as metric and articulation anchors, not decorative cylinders added late.
6. Research visible suspension/steering/underbody per vehicle; scale mechanical detail to camera/gameplay need.
7. Define physical pivots/axes before rigging, and hand those truths to rigging/animation rather than duplicating ownership.
8. Allow mid-poly, high/low, direct realtime and hybrid approaches according to iteration and target-fidelity needs.
9. Scope interior/underbody and texture allocation by actual visibility/open states.
10. Validate 3/4 silhouette, reflections, wheel clearance and articulation—not only orthographic alignment or mesh cleanliness.

## 2026-10-15 addendum — gated vehicle blockout, quick recipes, measurable QA

**Scope and method.** Reviewed further interviews/tutorials for professional vehicle production. Adopted only portable modeling practice. The newly linked [vehicle recipes](vehicle-recipes.md) and [vehicle QA/measurements](vehicle-qa.md) are original Tools_C syntheses. They do not copy third-party text/code, invent a chassis physics solver, establish fixed millimeter tolerances, or add a new QA schema or Skills owner.

### Irfan Haider — vehicle proxy, playable-camera review, topology economy

Source: https://80.lv/articles/modeling-vehicles-for-aaa-games (2019), senior vehicle artist with Forza/DiRT/F1 credits.
- Artist uses real dimensions, proxy box and wheel cylinders/camera alignment as initial anchors, and advises orthographic checks, gameplay-camera checks and purposeful polygons.
- **Applied:** V0/V1 axle markers, wheelbase/track/stance, source-matched views, wheel/body envelope, early target-camera inspection. Existing body/LOD guidance already covered other aspects.
- **Limit:** No universal wheel clearance tolerance, sampling interval or measured acceptance formula provided by article; those are proposed Tools_C measurement conventions, conditional on project data.

### Michael Neocleous — simple editable base mesh and non-destructive body modeling

Source: https://80.lv/articles/recreating-mad-max-s-interceptor-using-blender-substance-3d-painter (2021), senior environment artist.
- Artist emphasizes proportional blockout, simple base mesh, restrained support loops, and modifiers where justified.
- **Applied:** stricter V2 controlled body-surface/clay checkpoint before small panel/detail escalation.
- **Limit:** No empirical threshold for highlight waviness; V2 relies on inspected comparable views and specific visible defects, not a textual or modifier-count score.

### Manish Rawat — truck-specific layout and authenticity

Source: https://80.lv/articles/001agt-002mrs-how-to-model-a-local-truck (2019), game vehicle artist (Forza, Metro Exodus, Days Gone).
- Truck production starts with major dimensions and the arrangement of primary forms; details need local, period and vehicle authenticity, rather than attractive random additions. The artist explains staged blockout, mid/high/low-poly and reference-driven texturing.
- **Applied:** heavy truck/hauler recipe: axle stations, chassis/cab/cargo massing and region-appropriate detail added only after V1/V2.
- **Limit:** The article does not prescribe a universal articulated trailer model, axle grouping formula or physical payload test. V3 articulation examples are engineering synthesis.

### Alexa Ranzola — motorcycle breakdown, distinct moving assemblies and baked small details

Source: https://80.lv/articles/how-to-model-a-realistic-bike-based-on-a-2013-harley-davidson-sportster (2026), Viper Cruiser.
- Artist collects multi-angle references, separates core parts for rig/animation and prioritizes prominent detail while baking small parts. Exact published triangle figure is project-specific and deliberately not generalized.
- **Applied:** motorcycle recipe focusing on wheel/frame/fork/tank/swingarm breakdown, intent-aware geometry and handoff boundaries.
- **Limit:** Steering-head and swingarm axis review, geometric clearances and V3 sampling are Tools_C original QA proposals, not claims about the author's particular rig checks.

### Blender official semantics and project-owned numeric checks

Source: https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/mirror.html and https://docs.blender.org/manual/en/4.5/modeling/modifiers/introduction.html
- Blender Mirror uses origin or Mirror Object; modifiers affect evaluated output without necessarily changing editable base topology.
- **Applied:** measure in declared vehicle-local F/R/U directions from evaluated geometry, preserve mirror source and distinguish geometry from shading when reviewing actual body.
- **Limit:** Vehicle wheelbase, track and ground-clearance formulas in [vehicle QA](vehicle-qa.md) are coordinate-geometry definitions written for our workflow, *not* assertions that Blender supplies a certified vehicle metrology feature. Test scripts or Blender live captures have not been run in this documentation-only pass.

### Exclusions

- No copying paid add-on-specific modeling workflows (HardOps, Substance Painter, CAD packages, Vehicle Rig add-ons) as mandatory dependencies.
- No fixed steering angle, tire geometry segments, clearance millimeters, polygon/LOD percentages, suspension travel or texture sizes.
- No claims of verified vehicle appearance, rig behavior, collision correctness or engine import from the research alone.
