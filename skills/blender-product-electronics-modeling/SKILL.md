---
name: blender-product-electronics-modeling
description: Create or substantially revise appliances, consumer electronics, computers, displays and other engineered products in Blender: enclosures, panel gaps, controls, vents/grilles, ports, screens and product families. Props, vehicles, architecture, sculpt-only and export keep their owners.
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

Work the passes in order; full instructions, performance/LOD guidance and the validation checklist are in [procedure](references/procedure.md) — read it before modeling and again before acceptance.

- **Pass 1 — blockout and manufactured proportion** — Build the enclosure, screen/bezel, major handles/doors and large control zones from simple volumes.
- **Pass 2 — define enclosure architecture** — Decide what the product is physically made from at the visible assembly level:
- **Pass 3 — choose hard-surface representation** — Use **direct/mid-poly** when clean geometric bevels and editable booleans provide enough fidelity for realtime use.
- **Pass 4 — booleans, thickness and bevel language** — Booleans are useful for vents, sockets, recesses, openings, handle cutouts and panel cavities when the operands remain controlled.
- **Pass 5 — controls as reusable functional parts** — Treat buttons, keys, knobs, toggles and sliders as systems when they repeat.
- **Pass 6 — vents, grilles and speaker perforations** — Choose representation by target distance and depth cues:
- **Pass 7 — ports, connectors and cable interfaces** — For USB-like, audio, power, video, network, proprietary or fictional ports, establish:
- **Pass 8 — screens, displays, indicators and lenses** — Separate the physical display stack from its content:
- **Pass 9 — labels, legends and microdetail** — Use geometry only where raised/engraved depth is genuinely visible or affects silhouette/highlights.
- **Pass 10 — clean material identity before use wear** — Establish physical material families first:
- **Pass 11 — opening parts and service states** — For doors, lids, trays, fold-out stands, battery covers or removable modules:
- **Pass 12 — family/library strategy and product context test** — For related electronics/appliances, define shared design language before variants:

**Performance and LOD guidance:** see the procedure reference.

**Validation:** see the procedure reference.
- **Proportion and assembly** — overall dimensions match approved reference/anchors;
- **Controls and interfaces** — buttons/keys/knobs/switches have consistent spacing, travel and pivots where promised;
- **Mesh and shading** — booleans produce no unintended internal/coplanar/self-intersecting artifacts in visible regions;
- **Surface and storytelling** — plastics/metals/rubber/glass/readable material families remain distinct under varied light;
- **Reuse and context** — shared feet/controls/connectors/fasteners remain shared where intended;

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
