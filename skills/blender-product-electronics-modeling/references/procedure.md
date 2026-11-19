# Blender product & electronics modeling — procedure, performance and validation

Detailed passes for [the skill](../SKILL.md). Moved verbatim from SKILL.md in 4.4.0.

## Workflow

Use the simplest representation that preserves the product's manufactured read, interaction and target-camera fidelity.

### Pass 1 — blockout and manufactured proportion

Build the enclosure, screen/bezel, major handles/doors and large control zones from simple volumes. Establish:
- overall width/height/depth;
- base/feet relationship;
- major chamfers/radii;
- screen/opening proportions;
- control clusters;
- removable/opening parts;
- cable/port side or back zones;
- dominant negative spaces.

Use published dimensions or a hand/desk/counter proxy where appropriate. Judge from the actual target camera as well as clean front/side/3/4 views.

Do not add screw heads, ventilation perforations, printed labels or micro-seams while the enclosure and interaction layout are unstable.

### Pass 2 — define enclosure architecture

Decide what the product is physically made from at the visible assembly level:
- front/back or top/bottom shell halves;
- removable service/battery panels;
- bezel versus main housing;
- metal chassis versus plastic exterior;
- separate feet, handles, stands or mounts;
- doors/lids/trays;
- glass/display/lens inserts;
- gaskets/rubber interfaces where visible.

Panel/seam placement should follow assembly logic. Use separate geometry where parts move, need different material/thickness, create visible depth or must be replaceable/variant-controlled. Use a seam/groove/normal/decal where a separate object would add no useful control.

Do not cut arbitrary panel lines solely to make a device look "technical."

### Pass 3 — choose hard-surface representation

Use **direct/mid-poly** when clean geometric bevels and editable booleans provide enough fidelity for realtime use.

Use **subdivision** when broad smooth molded surfaces or controlled consumer-product curvature require continuous high-quality surfaces.

Use **high/low bake** when numerous recessed details, engravings, embossed patterns or fine manufactured shapes are cheaper to transfer than keep in realtime geometry.

Use **CAD-assisted/hybrid** when product-like solids and fillets are best solved parametrically elsewhere, but clean/game-ready Blender organization, shading, UVs and delivery remain required.

The workflow choice is not a quality ranking. Choose by editability, curvature, target view, bake cost and delivery requirements.

### Pass 4 — booleans, thickness and bevel language

Booleans are useful for vents, sockets, recesses, openings, handle cutouts and panel cavities when the operands remain controlled. Keep cutters organized and recoverable while the design is changing.

Boolean behavior is most predictable on suitable manifold geometry; inspect for artifacts, self-intersections and unexpected internal faces rather than trusting a successful modifier evaluation.

Use Solidify or explicit shell geometry where sheet/panel thickness matters. Confirm normal direction and corner behavior before relying on automatic thickness.

Use bevel width/segments according to product scale/material/manufacturing language:
- injection-molded plastic generally needs readable softened transitions;
- thin stamped metal may use smaller rolled/chamfered edges;
- rubber controls can be softer;
- glass/screens need their own edge treatment.

Weighted normals can improve broad flat manufactured surfaces after bevels, but they do not repair poor geometry, non-planarity or a wrong silhouette.

### Pass 5 — controls as reusable functional parts

Treat buttons, keys, knobs, toggles and sliders as systems when they repeat.

Define:
- control footprint and spacing;
- resting and pressed/rotated positions if interaction matters;
- travel/clearance;
- pivot or translation axis;
- shared versus unique geometry;
- cap/legend separation if labels vary;
- material/tactile difference from the enclosure.

Use linked data, arrays or instances for truly identical repeated controls. Make them unique only when shape/function changes.

For keyboards/keypads, prove row/column spacing and edge clearances before adding legends. For knobs/dials, center the origin on the rotational axis. For appliance doors/lids, test representative open states before handoff.

### Pass 6 — vents, grilles and speaker perforations

Choose representation by target distance and depth cues:
- geometry for large/close holes where silhouette/parallax/interior darkness matters;
- boolean/array/procedural repetition for editable medium-detail openings;
- normal/opacity/mask/bake for high-count fine perforations where geometry cost adds little;
- hybrid when a few edge holes need geometry but the central field can be baked/masked.

Build one source perforation/slat and repeat it when practical. Keep spacing/offset consistent and preserve an editable source until the pattern is proven.

Do not model thousands of individually unique holes merely because they are visible in a macro photo. Conversely, do not fake a large vent with a flat texture if target closeups reveal its depth and interior.

Vent placement should make visual/functional sense for the design. Do not invent random ventilation fields as decorative noise.

### Pass 7 — ports, connectors and cable interfaces

For USB-like, audio, power, video, network, proprietary or fictional ports, establish:
- outer opening shape;
- recess depth and bezel/chamfer;
- connector orientation;
- spacing/clearance between adjacent ports;
- visible internal tongue/pins only to the required target fidelity;
- cable insertion direction where interaction matters.

Printed port icons/legends normally belong to decals/textures rather than geometry. Small contacts can be baked or simplified for normal game views.

For removable cables, keep cable/plug as independent assets or subassemblies when reuse/animation requires it. Cable routing can use curves, but connector alignment and attachment remain product-specific truths.

### Pass 8 — screens, displays, indicators and lenses

Separate the physical display stack from its content:
- outer glass/lens surface;
- bezel/frame;
- recessed display/emissive plane if visible;
- screen content/graphics as material/texture/UI handoff;
- indicator lenses/LEDs with appropriate depth only where useful.

Do not bake one fixed screen image into geometry decisions if the runtime/UI system will replace it. Preserve a stable screen plane/aspect/UV region and hand off content ownership.

For powered-off products, screen roughness/reflection can dominate readability. For powered-on products, emissive intensity and UI rendering are material/runtime issues, not reasons to distort the physical enclosure.

### Pass 9 — labels, legends and microdetail

Use geometry only where raised/engraved depth is genuinely visible or affects silhouette/highlights. Printed logos, compliance markings, key legends, warning text and port icons are usually more efficient as decals/textures/masks.

Plan label asymmetry before mirroring/stacking UVs. If left/right or front/back surfaces share UVs, avoid duplicating serial numbers, text or unique wear unintentionally.

Small screws, seams, knurling and embossed texture should be allocated according to target screen size. Do not let microdetail consume more geometry/texture effort than the enclosure, control spacing or material read.

### Pass 10 — clean material identity before use wear

Establish physical material families first:
- matte/gloss injection-molded plastic;
- painted/powder-coated metal;
- anodized/brushed/polished metal;
- rubber/silicone;
- glass/display/lens;
- translucent indicator plastic;
- fabric/mesh on speakers where applicable;
- ceramic/enamel or appliance-specific finishes.

Roughness, micro-normal and edge response often differentiate products more reliably than color alone. Judge under more than one light direction.

Then add fingerprints, hand polish, dust, kitchen grease, heat discoloration, scuffs, cable wear or service marks according to use. A frequently touched glossy button should not age like a protected rear panel.

### Pass 11 — opening parts and service states

For doors, lids, trays, fold-out stands, battery covers or removable modules:
- place the pivot on the physical hinge/slide axis;
- test the required range;
- verify surrounding shell clearance;
- include hidden/revealed geometry only to the depth visible in the open state;
- keep parent hierarchy simple enough for later rig/animation/export.

For high/low baking, opening parts may need temporary separation/exploded positioning to prevent projection contamination; preserve a recoverable neutral assembly and return it after baking.

Do not merge opening parts into the enclosure solely for object-count tidiness.

### Pass 12 — family/library strategy and product context test

For related electronics/appliances, define shared design language before variants:
- corner radius/bevel family;
- vent/perforation style;
- feet/fastener/control families;
- material palette;
- panel-gap language;
- screen/indicator treatment;
- common port/control modules where appropriate.

Use linked/shared components for identical feet, screws, knobs, buttons, vents or connectors. Variants can change color, labels, screen state or selected modules without duplicating all geometry.

Place the product in its intended context—desk, TV stand, kitchen counter, workshop, hand, wall mount—and confirm scale, cable/door clearance, visual hierarchy and target-camera detail.

## Performance and LOD guidance

- Preserve enclosure silhouette, screen/opening proportions and major control layout before tiny screws/perforations.
- Repeated keys, buttons, holes, feet and fasteners should share/generate data where possible.
- Fine vents/grilles/knurling are strong candidates for normal/opacity/baked representation at lower LODs.
- Keep interactive controls and opening-part pivots stable across LODs where runtime behavior depends on them.
- Simplify hidden internals first when open/transparent states do not expose them.
- Re-check transparent/display surfaces, normals and material IDs after LOD reduction.
- Texture resolution, draw-call, material-slot, collision and runtime UI/emissive budgets remain project-specific.

## Validation

Perform applicable checks and label unavailable evidence as SKIP.

### Proportion and assembly
- overall dimensions match approved reference/anchors;
- shell halves/panels/bezel/base relationships are coherent;
- panel gaps and visible thicknesses are intentional;
- underside/back geometry is sufficient for target camera/placement;
- removable/opening pieces fit both neutral and tested open states.

### Controls and interfaces
- buttons/keys/knobs/switches have consistent spacing, travel and pivots where promised;
- connector openings have plausible orientation/clearance;
- repeated controls/ports remain shared where intended;
- cable insertion/attachment direction is usable when interaction requires it;
- display/screen plane and aspect are stable for material/UI handoff.

### Mesh and shading
- booleans produce no unintended internal/coplanar/self-intersecting artifacts in visible regions;
- shell thickness and face orientation are correct;
- bevel/shading language is consistent with product scale/material;
- broad flat surfaces remain visually flat where intended;
- smooth molded surfaces have controlled highlight continuity;
- modifiers/transforms are deliberate and recoverable where ongoing edits matter.

### Surface and storytelling
- plastics/metals/rubber/glass/readable material families remain distinct under varied light;
- printed labels/legends are not duplicated by accidental mirrored UVs;
- fingerprints/dust/scuffs follow touch/exposure rather than uniform noise;
- emissive/display treatment does not substitute for physical screen/bezel correctness.

### Reuse and context
- shared feet/controls/connectors/fasteners remain shared where intended;
- family variants preserve common attachment/layout rules;
- pivots support placement/opening/rotation without corrective hidden offsets;
- target context confirms scale and clearance;
- visual acceptance includes representative target views, not only clean orthographic alignment.
