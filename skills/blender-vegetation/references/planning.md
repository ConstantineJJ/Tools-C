## Preflight: define the plant before modeling

Establish the minimum useful vegetation brief:

1. **Plant type** — broadleaf tree, conifer, palm-like, shrub, grass, flower, vine, reed, dead plant, fantasy plant, etc.
2. **Reference authority** — exact species, regional family, concept art, stylized shape language or mixed references.
3. **Scale and age** — mature tree, sapling, trimmed shrub, young grass, oversized fantasy plant, etc.; use a human/player or measured anchor.
4. **Target view** — hero closeup, third-person gameplay, top-down, background forest, cinematic, VR, etc.
5. **Season/state** — healthy, dry, autumn, winter, dead, pruned, storm-damaged, overgrown, flowering/fruiting.
6. **Representation target** — direct mesh, low-poly stylized geometry, foliage cards/atlas, baked branch clusters, Geometry Nodes/instances, hybrid or project-defined system.
7. **Wind/runtime needs** — static, simple root-to-tip bend, branch hierarchy, interactive foliage, engine-specific pivot/vertex data or unknown/deferred.
8. **Reuse model** — one hero plant, species family, reusable branch clusters, patch variants, procedural scatter library, etc.
9. **MUST PRESERVE** — approved silhouette, species cues, scale, root/ground anchor, branch hierarchy, card/cluster pivots, UV/atlas regions, instance/shared-data relationships and unrelated scene state.

If species identity, scale, target camera or wind requirements materially change the representation, resolve them or record a provisional assumption before building dense foliage.

## Reference and growth strategy

Collect references by plant question:

- full silhouette from several angles and ages;
- trunk/root flare and major branch junctions;
- branch hierarchy, taper, droop/uplift and crown distribution;
- leaf/needle arrangement and cluster behavior rather than only isolated leaf shape;
- underside/backlit foliage for density and translucency cues;
- bark/stem/leaf materials separately;
- seasonal, damaged, dead or pruned examples when relevant;
- grouped plants/meadows/hedges for spacing and natural variation.

Study growth as hierarchy: root/base → trunk or primary stems → primary branches → secondary/tertiary branches → twigs/leaf clusters. Stylized plants may compress or exaggerate levels, but random sticks with leaves attached uniformly rarely produce a convincing silhouette.

Do not copy one photograph's accidental asymmetry as a universal species rule. Identify repeated growth tendencies across multiple references, then preserve deliberate concept-art departures.
