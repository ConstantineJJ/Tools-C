# Material-aware segmentation recipes

Read only the relevant material/assembly sections. These are authored game-asset
decisions synthesized from the linked [research](research-notes.md), not a promise
of engineering fracture accuracy. User style and observed construction take
precedence. The same material can fail differently under different loads.

## Wood and assembled containers

Read the construction: plank box versus plywood crate, grain per member, frame,
braces, lid, nails/screws, bands and glued joints. A plywood sheet is not a set of
solid-wood boards. Use existing seams if modeled; a single mesh may contain
disconnected boards, while one connected scan may require reconstruction of
hidden contact surfaces. Separate by actual component evidence, not material slot
alone. A shared wood material does not mean two boards are one physical member.

For a board crate, start with separable boards/side panels, base, braces and
fittings. Let weak fastenings release before arbitrarily cutting every plank.
Add longitudinal splinters and selected cross-grain snaps near impact/bending
locations when the budget and camera justify them. Preserve grain orientation
per board; the assembly's longest bounding-box axis is not a reliable grain axis.
Metal bands may stay with one side or detach as a separate component, according
to the intended failure. Keep nails visual/attached unless they matter to play.

Plan a low-body option first. For an illustrative **8-body** crate, use several
board groups/panels plus chosen braces/fittings; retain individual board meshes
as children of those bodies if useful. Explain grouping so it still reads as a
crate, not eight arbitrary cells. Select actual grouping from the source rather
than forcing an exact panel count on every design. Fine splinters can be particles
or visual meshes without independent collision. End-grain caps differ from long
grain and painted exterior; retain the board's thickness at every new cut.

Review: do primary pieces read as boards/braces? Are long splits consistent with
grain? Do exposed ends, nails and straps belong to the intended surviving piece?
If bending before break matters, hand off authored deformation or target joints;
a rigid board falling intact does not prove bending.

## Masonry, stone and concrete

Distinguish laid stone/brick, irregular rubble masonry, cut-stone blocks and cast
concrete. For masonry, use stones/bricks as primary components and mortar as
weaker connections. Cluster neighboring blocks when individual stones exceed
the physics budget; preserve the visual joints within those groups. Add a few
broken blocks near the hit when appropriate, rather than cutting every brick
into identical cells. Decide whether mortar travels with pieces, remains as a
broken joint surface or becomes visual dust; do not leave unsupported mortar
films as accidental physical bodies.

For concrete, use larger irregular bulk pieces plus locally finer impact damage.
Choose directional/planar cuts for the actual structure/load when justified.
Noise should enrich the break surface without changing the approved outer form
or producing needle-shaped contacts. Reinforcement can retain connections;
explicitly decide whether bars are visual attachments, physical constraints or
part of an authored animation. A Boolean cut through all materials at once must
not silently sever every bar or turn it into stone fragments.

Keep a supported remainder or anchors where the plan requires the wall to stand.
For a localized hole, exterior modules outside the damage zone remain aligned
and connected to their original neighbors. Cap the hole boundary and fragment
faces; expose stone/aggregate and mortar rather than stretching facade textures.
Check that cover/opening dimensions still serve gameplay in the destroyed state.

Review: reconstructed silhouette and masonry coursing, stable remainder,
recognizable blocks versus fractured concrete, no floating veneer, and useful
collision at the new opening. Rock can use irregular solid fracture, but avoid
uniform cell sizes unless the art direction asks for that pattern.

## Glass, ceramics and thin brittle shells

Decide the glass construction before generating shards. Ordinary annealed glass,
tempered glass and laminated glass need different visual failure choices.
An impact-centered pane can use radial cracks plus irregular cross/ring breaks;
tempered glass can use many small visual granules without a body per granule;
laminated glazing may retain a cracked web and attached pieces. These are visual
recipes to validate against reference, not safety or structural predictions.

Preserve a frame/edge-retained region when the design requires one. Give panes
or shard proxies enough thickness for the target physics system, keeping visible
thickness credible. Do not globally thicken a thin sheet until it looks like a
slab just to stabilize collision. Use fewer representative physical shards,
nonphysical detail and appropriate target collision settings instead.

For bottles, bulbs, cups and curved glass, cut the actual shell and retain its
cavity and wall thickness. A flat-pane generator does not by itself solve curved
vessels. Ceramic shells may break into curved broad fragments with local chips;
their glazed outside, unglazed interior and fresh substrate can have different
roles. Closed fragment solids must not imply a filled bottle or cup.

Review backfaces, normals, cut edges and material alpha/transmission in the
intended renderer. Blender glass appearance is not a portable engine shader
contract. Test target import with the export/integration owners. Avoid extremely
thin physical needles; retain their silhouette as nonphysical geometry when
needed. Collision thickness/margins and visible shard geometry may differ, but
the proxy must not cause obvious hovering, overlap or blocked passages.

## Metal, plastic and layered assemblies

Inspect seams, welds, hinges, fasteners, panel thickness and reinforcement.
Ductile metal commonly detaches, bends, buckles or tears; a cast brittle part may
need a different recipe. A metal cabinet can release doors/panels while keeping
its frame. A vehicle can detach approved panels without rebuilding chassis,
wheel pivots, glass or mechanical animation. Keep those source decisions with
their domain owners. Cosmetic dents need no detached bodies.

Thin plastic housings can split at seams, snap around tabs or crack into shell
sections. Soft plastic, rubber and fabric do not become rigid rock chips merely
because a fracture tool supports them. Select static torn variants, authored
deformation or a specialist simulation handoff as required by the brief.

For appliances/electronics, sandwich panels and mixed assemblies, keep layers
and materials distinct: outer shell, glass, frame, substrate, board or internal
supports. Interior content should match visible evidence and required exposure,
not become an excuse for an unsolicited full internal rebuild. Small screws,
cables, rebar or fittings may follow a parent piece as visual attachments.
Choose where attachments release and where they remain; geometric proximity
alone does not define a weld, nail or glue bond.

Review recognizable construction, plausible tear/cut substrates and retained
attachments. Bent sheets need a usable collision approximation; use limited
compound convex shapes rather than a single hull that seals an important opening.

## Budget adaptation across materials

Prioritize recognizable primary pieces and the gameplay opening/remaining
support. Keep visual fracture detail separate from independent simulation.
Combine physically coherent neighbors into clusters, retain detail under those
transforms, replace tiny debris with effects or use a static destroyed variant.
Check the worst concurrent activation across multiple instances. Polygon count
alone does not measure body, contact, constraint or draw-call cost.

A representative test should show intact/rest, exploded labels or colors,
exposed interiors and destroyed gameplay view. Inspect the actual images and
playback when required; written material names are not proof of material-aware
breakup. Revisit the plan if every recipe produces the same silhouette/size
distribution, or if grouping destroys the intended construction read.
