### Pass 5 — final realtime mesh / bake target

When a low/realtime mesh is required, optimize by visible contribution:
- preserve silhouette and large curvature first;
- preserve articulation and interaction clearances;
- spend edges where they stabilize shading or bake projection;
- simplify hidden/internal regions when no downstream requirement needs them;
- retain enough geometry to produce a clean bake rather than chasing the minimum triangle count before testing.

All-quads are not a universal requirement for static props. Ngons/triangles can be valid where they are planar/stable and do not harm shading, subdivision, deformation or bake behavior. The acceptance criterion is predictable output and downstream use, not topology aesthetics in isolation.

For high/low workflows, make quick test bakes before final UV/polish where practical. If projection errors appear, fix low geometry, normals, UV splits, ray distance or cage rather than painting over systemic artifacts.

### Pass 6 — UV, mirroring, stacking and bake plan

Choose unique versus shared UV space deliberately.

Consider mirroring/stacking when:
- surfaces are genuinely symmetric/repeated;
- unique labels/wear are not required there;
- shared detail meaningfully improves texel allocation.

Keep unique UV space where:
- asymmetrical storytelling is important;
- the target camera sees both mirrored regions together and repetition would be obvious;
- labels, dirt, damage, directional materials or baked lighting/AO require distinction.

Prioritize UV area according to target visibility, not only surface area. Maintain the project's texel-density policy unless a documented hero/readability exception applies.

For baked props:
- verify high and low alignment;
- use tangent-space normals when that matches the delivery target;
- use selected-to-active/cage/ray settings deliberately;
- provide sufficient bake margin to avoid seam/filtering artifacts;
- re-check hard edges/UV boundaries/normals where projection errors cluster.

Do not universalize one resolution or padding value; these depend on project texture size, mip behavior and target distance.

### Pass 7 — materials before damage

Establish the clean material identity first:
- base color range;
- roughness response;
- metallic/dielectric classification where applicable;
- grain/fiber/directionality;
- molded/cast/machined/painted surface character;
- glass/rubber/fabric/paper behavior as relevant.

Then add use/environment history. Roughness often carries as much material identity as color; evaluate the prop under more than one light direction so a texture is not accidentally tuned to one studio setup.

Separate materials according to physical/material logic, not arbitrary color regions. Two similarly colored parts can still need different roughness/normal behavior because one is plastic and one is painted metal.

### Pass 8 — storytelling, wear and damage

Ask concrete questions:
- Who owns/uses this object?
- How often is it handled?
- What contacts the floor/table/hand/other parts?
- Where does dust accumulate versus get wiped away?
- Where can moisture, grease, rust, sun bleaching, dents, chipped paint or abrasion plausibly occur?
- Which repairs, labels, stickers, tape, replacement parts or age differences support the intended story?

Build history in layers: construction/material variation → broad age/use → contact/exposure patterns → selective small damage. Avoid uniform edge wear, random scratch noise and equal dirt on every face.

Not every prop must be heavily aged. A clean/new object can be more believable in context than forcing "storytelling" through damage. Different props in one scene may have different ages and maintenance histories.

### Pass 9 — hierarchy, pivots and interaction

Choose origin/pivot from use:
- movable furniture: stable base/bottom-center or project placement convention;
- hand-held prop: root/handle anchor suitable for attachment to the character/project socket convention;
- hinged lid/door: separate moving component with pivot on the real hinge axis;
- drawer: translation axis aligned with intended travel;
- wheel/knob/lever: pivot on its real rotational axis;
- stackable/container object: deterministic base/footprint anchor if placement depends on it.

Keep the asset root and moving subcomponents conceptually separate. Do not place every object's origin at world zero or geometric center if that makes actual placement/animation harder.

For interactive props, perform a simple clearance/articulation test before finalizing: hand fit, lid opening, drawer travel, seated clearance, door/cabinet collision, etc., as applicable.

### Pass 10 — library reuse, variants and scene-context test

For a reusable asset library, decide whether copies should remain linked to the source, append independent data, reuse mesh/material data, or instantiate a collection. Use the reuse mode that matches whether later source edits should propagate.

For prop families:
- share subcomponents/materials where truly identical;
- vary color/labels/wear first when geometry does not need to change;
- preserve common dimensions/attachment anchors where compatibility is promised;
- make geometry unique only for real silhouette/function changes.

Place the prop in one representative target context. For clutter/family assets, test several together. Confirm scale, visual hierarchy, repetition, ground/surface contact and target-camera readability. An isolated beauty render alone is not acceptance for an in-game set-dressing prop.
