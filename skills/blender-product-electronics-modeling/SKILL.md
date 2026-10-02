---
name: blender-product-electronics-modeling
description: Create or substantially revise household appliances, consumer electronics, computers, monitors, TVs, consoles, audio devices, kitchen equipment and other engineered product-design assets in Blender. Use when enclosure construction, manufactured panel gaps, buttons/knobs, vents/grilles, connectors/ports, display surfaces, cable interfaces, repeated controls, material separation or product-family consistency are central; route generic props, vehicles, architecture, street fixtures, vegetation, sculpt-only work and final export to their specialist owners.
---

# Blender product & electronics modeling

Read the required [foundation contract](../../docs/foundation.md) and the general [Blender pipeline](../blender-pipeline/SKILL.md). This skill owns manufactured household/digital product geometry and interaction construction, not electrical engineering or generic scene dressing.

## Instruction priority

Follow the user's target, active project/profile, approved product/reference and engine constraints before generic industrial-design conventions. A real device is useful evidence for dimensions, assembly and material behavior; it is not permission to redesign a stylized fictional product. Do not model invisible circuitry or internal fasteners simply because a real device would contain them.

## Scope and ownership

Own:
- consumer electronics such as computers, monitors, TVs, consoles, radios, speakers, cameras, routers, peripherals and similar devices;
- household appliances such as microwaves, kettles, coffee machines, vacuum cleaners, fans, heaters, kitchen devices and small/medium appliances;
- product-like workshop/office equipment where enclosure and manufactured assembly dominate the task;
- enclosure shells, bezels, removable panels, doors/lids, battery/service covers and visible assembly seams;
- buttons, switches, keys, knobs, sliders, dials, handles and other product controls;
- vents, grilles, speaker perforations and repeated manufactured openings;
- connectors, sockets, ports, plugs, cable interfaces and visible mounting details;
- displays, screens, indicator lenses, LEDs and emissive surfaces as geometry/material interfaces;
- manufactured material separation: injection-molded plastic, stamped/cast/machined metal, rubber, glass, coated/painted surfaces;
- choosing direct realtime, subdivision, boolean/bevel, high/low bake, CAD-assisted or hybrid representation;
- product-family reuse, repeated components, pivots/articulation and product-specific QA.

Route:
- generic furniture, tools, decor, containers and narrative clutter to `blender-props` when product/device construction is not central;
- cars, vehicle body/interior assemblies and vehicle articulation to `blender-vehicle-modeling`; a dashboard remains vehicle-owned unless a removable/standalone device becomes the specific modeling subject;
- building-integrated geometry to `blender-architecture-environment`;
- street/site fixtures to `blender-environment-assets`;
- roads/network infrastructure to `blender-roads-infrastructure`;
- vegetation to `blender-vegetation`;
- primary sculpting to `blender-sculpting`;
- final GLB/export/runtime validation to the existing export and engine owners.

Boundary rule: classify by the asset's **engineering/product-design burden**, not size. A decorative box with a label can stay `blender-props`; a close-view game console with shell halves, vents, ports, controls and display/LED interfaces belongs here.

## Preflight: define the product before modeling

Establish the minimum useful brief:

1. **Product role** — hero/product render, close interactive game object, handheld device, appliance, background electronics, family/set member, etc.
2. **Reference authority** — exact make/model, product photos, dimensions/manuals, teardown/repair photos, concept art or fictional design.
3. **Scale anchors** — published dimensions, screen size, connector dimensions, human hand, desk/counter context or another measured feature.
4. **Viewing/use context** — product showcase, first-person interaction, third-person prop, cinematic closeup, static set dressing, open/service state, destruction, etc.
5. **Assembly architecture** — shell halves/panels, removable doors/lids, fasteners, bezel, base/feet, internal cavity visibility and visible seams.
6. **Interaction set** — buttons, keys, knobs, switches, hinges, sliders, detachable parts, cable plugs, removable batteries/covers, etc.
7. **Representation** — direct realtime/mid-poly, subdivision, boolean/bevel, high-low bake, CAD-assisted or hybrid.
8. **Surface strategy** — shared/unique materials, trim/atlas where appropriate, baked details, decals/labels, emissive/display textures, project-defined texel density.
9. **MUST PRESERVE** — approved silhouette, dimensions, shell gaps, control spacing, display/port positions, articulation axes, UVs/materials, hierarchy, linked/shared data and unrelated scene state.

If missing evidence would materially change enclosure fit, button/port placement or open-state clearance, resolve it or record a provisional assumption before final detail.

## Reference strategy

Gather references by engineering question:

- orthographic-ish front/side/top/back views for overall enclosure and control placement;
- product listings/manuals/spec sheets for dimensions and exact model variants;
- teardown/repair photos for shell splits, screw locations, vent depth, port mounting and open-state construction;
- underside/back images, often omitted from marketing photography;
- closeups for button travel, keycap spacing, rotary controls, vents, speaker holes, connectors, feet and seams;
- powered-on views for display framing, indicator behavior and emissive regions;
- clean/new examples for base manufacturing and used examples separately for fingerprints, polish, dust or wear;
- family references when multiple devices/appliances must share design language.

Do not infer a motherboard, fan duct or hidden mechanism if it never affects visible geometry or interaction. When the product opens or has transparent areas, internal depth becomes in-scope only to the required visibility.

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

## Safeguards

- Do not add detailed vents, labels or ports before enclosure proportion/control layout is stable.
- Do not trust successful booleans without inspecting manifold/shading/internal-face artifacts.
- Do not apply destructive boolean/bevel/subdivision stacks before the product architecture and high/low strategy are known.
- Do not model invisible circuit boards, fans, wiring or fasteners without open-state/transparent/gameplay need.
- Do not make repeated buttons/keys/feet/ports unique accidentally.
- Do not move hinge/knob/control pivots after downstream animation/interaction depends on them.
- Do not use random panel lines, vents or screws merely to make a fictional device look complex.
- Do not invent universal gap widths, bevel radii, texture sizes, texel density, triangle counts or LOD ratios.
- Do not merge interactive/removable pieces solely to reduce object count.
- Do not let emissive screens or decals hide wrong enclosure geometry or material response.

## Pitfalls / Lessons Learned

### PROD-001 — Marketing-photo blind spot
- Symptom: the front looks accurate but the back, underside, port layout or shell seams are invented.
- Cause: only beauty/product-front images were gathered.
- Rule: use manuals, listings and teardown/repair references for hidden/functional views when they matter.
- Verification: all target-visible sides and interaction surfaces are supported by reference or explicitly marked as designed assumptions.

### PROD-002 — Technical noise before product architecture
- Symptom: many vents, screws and panel lines exist but the device feels generically "sci-fi" rather than designed.
- Cause: secondary technical detail replaced enclosure/control hierarchy.
- Rule: establish silhouette, shell architecture and interaction zones first; secondary detail must follow function/manufacturing logic.
- Verification: simplified untextured product still reads clearly and explains its main use.

### PROD-003 — Boolean success mistaken for clean geometry
- Symptom: a port/vent cut evaluates, but shading pinches or hidden internal faces remain.
- Cause: modifier completion was treated as validation.
- Rule: inspect topology, normals, manifold conditions and target highlights after important booleans.
- Verification: visible surfaces shade cleanly and no unintended internal/coplanar geometry remains in required regions.

### PROD-004 — Geometry overload in repeated perforations
- Symptom: speaker/vent holes dominate object count/evaluation with little visible benefit.
- Cause: every small perforation was modeled uniquely.
- Rule: choose geometry, arrays/instances, bake or mask from target depth/parallax and screen size.
- Verification: lower-cost representation preserves required close/distant read with stable editability.

### PROD-005 — Controls without interaction axes
- Symptom: knobs rotate off-center, buttons slide inconsistently or appliance doors need rig offsets.
- Cause: controls were modeled visually without downstream motion/clearance truth.
- Rule: define control pivots/travel and test representative interaction before handoff.
- Verification: temporary transforms operate each required control/opening part around the documented axis with no corrective parent offset.

### PROD-006 — Printed detail trapped in geometry
- Symptom: every legend/logo/icon becomes high-maintenance mesh detail and variants require geometry edits.
- Cause: printed versus physical depth was not classified.
- Rule: reserve geometry for real relief/silhouette/highlight; keep ordinary print in decals/textures/UI surfaces.
- Verification: product variants can change labels/screens without reconstructing the enclosure.

### PROD-007 — Material sameness
- Symptom: glass, matte plastic, rubber and painted metal differ mainly by color.
- Cause: roughness/microstructure/edge response were underdesigned.
- Rule: establish clean material response before aging and inspect under varied lighting.
- Verification: major material classes remain distinguishable with base-color differences reduced.

## Handoff

When passing to animation, export, runtime/UI or another specialist, report:
- product role, target camera and authoritative dimensions;
- enclosure architecture and required open/service states;
- representation (direct/subdivision/boolean/high-low/CAD-assisted/hybrid) and modifier state;
- moving controls/doors/lids plus exact origins/axes/travel;
- repeated/shared modules such as feet, keys, knobs, ports or vents;
- screen/display plane, UV/aspect and content ownership;
- UV mirroring/stacking and material/label strategy;
- hidden/internal detail scope and protected visible interfaces;
- structural/visual/bake/context evidence completed;
- open LOD/collision/UI/emissive/export/runtime gates.

## Completion / stop

Complete when the requested appliance/electronic product exists with approved scale and enclosure architecture, controls/ports/displays fit and articulate as required, hard-surface/shading representation is appropriate to target views, material classes and labels have a coherent plan, protected data survived, and applicable structural/visual/context checks passed or are explicitly handed off.

Stop and report instead of guessing when product variant/reference conflicts materially change enclosure/control layout, required connector/open-state geometry cannot be determined, target interaction/view is missing but necessary to scope detail, or the requested edit would invalidate protected pivots/UVs/material/runtime interfaces outside scope.

## Research basis

The practical rules in this specialist are distilled from Blender documentation and product/electronics production breakdowns covering booleans, bevel/weighted normals, solidify, arrays, Asset Browser reuse, baking, enclosure-first blockout, shared measurements, repeated vents/controls, open-part baking, roughness/material identity and product storytelling. See [research notes](references/research-notes.md) for source URLs, source type and caveats.
