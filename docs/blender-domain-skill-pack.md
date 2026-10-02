# Blender domain skill pack — Pass 0 architecture

Status: all eight specialist implementation passes complete; cross-pack review completed 2026-10-03. Dedicated contracts pass is NOT STARTED. Shared invariants stay in `docs/foundation.md`, project-specific budgets stay in project profiles/contracts, and each specialist owns only its domain decisions.

## Purpose

Extend the Blender MCP knowledge layer beyond character production with scoped specialist skills for large environment/game-asset domains. These are decision procedures for an agent operating Blender through inspection and bounded actions, not click-by-click Blender tutorials.

Every specialist should answer:
- what evidence/reference is needed before touching geometry;
- what decisions belong to this domain;
- which representation/workflow is appropriate and why;
- what data must be preserved;
- what common failure modes to avoid;
- what structural and visual evidence proves the result;
- when to stop or hand off to another owner.

## Implemented specialist owners

### 1. `blender-architecture-environment` — buildings and large structures
Own buildings, houses, halls, towers, industrial structures, architectural shells, modular building kits, facade/roof/opening systems, architectural scale, grid/pivot conventions and architecture-facing trim/tileable material strategy.

Do not own roads/curbs, standalone street objects, furniture/props, vegetation, vehicles or appliances except where required as temporary scale/reference context.

Status: first implementation pass complete.

### 2. `blender-environment-assets` — standalone environment objects
Own benches, street lamps, fences, railings, barriers, bins, bollards, hydrants, posts, simple utility/street fixtures and other repeatable set-dressing objects whose main role is environmental structure rather than hand-held/interior prop detail.

Boundary with architecture: if the item is an integral building module, architecture owns it; if it is a reusable standalone object placed around structures, environment-assets owns it.

Boundary with roads/infrastructure: continuous/network geometry belongs to roads/infrastructure; discrete fixtures belong here.

Status: second implementation pass complete.

### 3. `blender-roads-infrastructure` — roads, paths and networked ground infrastructure
Own roads, sidewalks/pavements, curbs, gutters, medians, paths, trails, ramps, crossings, road shoulders and other connected linear/network systems, including modular intersections, splines/curves and transition logic.

Do not own vehicles, standalone street furniture, terrain/vegetation or building shells.

Status: third implementation pass complete.

### 4. `blender-props` — small and medium props
Own furniture, containers, tools, clutter, decor, hand-held objects, interior set dressing and miscellaneous discrete assets whose production logic is prop-centric rather than architectural, botanical, vehicular or electronic-product-specific.

Boundary with environment-assets: props are generally portable/interior/detail storytelling objects; environment-assets are generally site/street fixtures tied to an environment system. Ambiguous objects should be routed by intended reuse and placement, not by size alone.

Status: fourth implementation pass complete.

### 5. `blender-vehicle-modeling` — cars and wheeled vehicles
Own cars, trucks, vans, buses, trailers, motorcycles where applicable, carts and other wheeled vehicles: proportion/reference alignment, body panels, wheel/tire systems, suspension-visible geometry, repeated/symmetric parts, hard-surface topology, moving assemblies and vehicle-specific QA.

Do not own generic electronics, environment props or character rigs. Vehicle animation/rigging may hand off to general rigging/animation after vehicle-specific articulation decisions are established.

Status: fifth implementation pass complete.

### 6. `blender-product-electronics-modeling` — household and digital equipment
Own appliances, consumer electronics, computers, monitors, TVs, consoles, kitchen devices and product-design-like hard-surface assets where manufactured assembly, panel gaps, bevel language, vents, connectors, display surfaces and material separation are central.

Boundary with props: a generic decorative object stays in props; an engineered appliance/device with product-design construction belongs here.

Status: sixth implementation pass complete.

### 7. `blender-vegetation` — plants and foliage
Own trees, shrubs, grass, flowers, vines and plant clusters: botanical reference, branching hierarchy, silhouette, cards/mesh choices, variation, instancing, wind-ready segmentation and performance-aware vegetation construction.

Do not own terrain, roads or generic environment props. Organic sculpting can support trunk/rock-like forms but vegetation remains the production owner.

Status: seventh implementation pass complete.

### 8. `blender-sculpting` — expanded sculpting specialist
Replaced the former narrow organic-sculpting reference with a canonical specialist for controlled organic and hard-surface sculpt passes, form hierarchy, brush/remesh decisions, regional correction, damage/weathering sculpt, topology-loss safeguards and handoff to retopology.

This skill must absorb useful current sculpting guidance rather than creating a competing rule source. Existing pipeline references should become compatibility/routing pointers where appropriate.

Status: eighth implementation pass complete; the former organic-sculpting pipeline reference is compatibility-only and the legacy alias resolves the canonical specialist directly. The dedicated domain contracts pass remains the next separate milestone.

## Shared principles — do not duplicate as independent policy

The following already have canonical owners and should be referenced, not redefined inconsistently:
- task scope, preserve/change/success, evidence levels, destructive baseline and handoff: `docs/foundation.md`;
- broad Blender stage routing: `skills/blender-pipeline/SKILL.md`;
- retopology/deformation: current retopology owner;
- UV/PBR/surface procedures: current surfaces owner;
- rigging/skinning: `blender-rigging-skinning`;
- animation: `blender-animation`;
- GLB/fresh-import checks: `blender-export-validation`;
- Godot target integration: `godot-asset-integration`;
- verification and anti-degradation: `verification`;
- project-specific visual baseline: `production-lookdev-gate` where relevant.

## Cross-skill hard-surface reuse

Architecture, vehicles, product/electronics, environment assets and props will share recurring techniques such as bevels, booleans, arrays, symmetry, instancing, normals and manufactured-material logic. Do not create a shared hard-surface contract pre-emptively. If three or more completed specialist skills converge on the same substantial decision procedure, extract one shared reference later and replace duplicates deliberately.

Technique overlap alone is not ownership overlap: the domain specialist decides why/where a technique is appropriate; Blender documentation defines software behavior.

## Integration pass 1 — architecture + environment assets + roads

Reviewed after the first three specialists were implemented and structurally exercised.
The ownership split is intentionally based on production role and continuity, not size:

| Subject | Canonical owner | Boundary rule |
|---|---|---|
| Building shell, facade, integrated window/door/trim, architectural stairs/railings | `blender-architecture-environment` | If it is structurally part of the building and follows the building kit/metric contract, architecture owns it. |
| Road, sidewalk, curb, gutter, median, path/trail, crossing, connected junction/network | `blender-roads-infrastructure` | Continuous route/cross-section/network geometry stays with roads, including its junction and terrain interfaces. |
| Bench, lamp, bin, bollard, hydrant, planter, bike rack, standalone sign/barrier | `blender-environment-assets` | Discrete reusable fixtures remain independent assets even when they snap to road or building anchors. |
| Fence/railing | Depends on role | Building-integrated railing: architecture. Reusable panel/gate: environment-assets. Path-following/procedural corridor generated as part of a route system: roads. |
| Building entrance meeting sidewalk | Split handoff | Architecture owns threshold/entrance geometry; roads owns exterior sidewalk/curb continuity. Exchange an explicit elevation/edge anchor instead of duplicating geometry. |
| Roadside fixture placement | Split handoff | Roads may expose placement anchors; environment-assets owns the fixture mesh, family, pivot and variants. |

Cross-cutting techniques such as scale anchors, transforms, instancing, variants,
modifiers, tileables/trims and recoverable sources appear in all three skills, but
their decisions are domain-specific and currently do not justify a new shared
hard-surface owner. The shared foundation already owns preservation/evidence rules.
Revisit extraction only if later props/vehicles/product skills expose a substantial
identical decision procedure rather than merely the same Blender tools.

Routing is allowed to return multiple owners for genuinely mixed requests. A task
that asks for a building entrance plus connected sidewalk should load architecture
and roads; a task that asks for bollards along a new sidewalk should load
environment-assets and roads. This is deliberate collaboration, not a collision.

## Integration pass 2 — props + vehicles + product/electronics

Reviewed after the three manufactured-object specialists were implemented. Their
shared Blender techniques are substantial, but their decision owners remain distinct:

| Subject | Canonical owner | Boundary rule |
|---|---|---|
| Furniture, containers, tools, decor, hand-held and narrative clutter | `blender-props` | Use when the object's prop/story/interaction role dominates and engineered product architecture is not the main modeling problem. |
| Cars, trucks, motorcycles, trailers and wheeled vehicle assemblies | `blender-vehicle-modeling` | Vehicle stance, wheelbase/track, body surfaces, wheel systems and vehicle articulation axes remain vehicle-owned even when the cabin contains product-like parts. |
| Appliances, computers, consoles, displays, radios, peripherals and engineered consumer devices | `blender-product-electronics-modeling` | Use when enclosure architecture, controls, vents, connectors, screens and manufactured assembly are central. |
| Vehicle dashboard / infotainment | Usually vehicle | Keep integrated dashboard geometry with the vehicle; route a removable/standalone device to product/electronics only when it becomes its own asset task. |
| Decorative radio / simple box-like scene dressing | Depends on burden | A simple narrative dressing prop can remain props; a close accurate device with shell splits, ports, controls and ventilation belongs to product/electronics. |
| Tool or appliance mounted on a vehicle | Split handoff | Vehicle owns mounting envelope/attachment context; props or product/electronics owns the reusable asset itself. Exchange explicit mount dimensions/pivots rather than duplicating geometry. |

All three use blockout-first reasoning, bevel/boolean/modifier discipline, shared data,
UV/bake choices, material-before-wear logic and physical pivots. This is still not
one identical decision procedure: vehicles are dominated by stance/body-surface and
mechanical articulation; product/electronics by enclosure/control/interface systems;
props by role, handling and storytelling. Keep these procedures in their domain
owners for now. Do not extract a shared hard-surface owner/reference merely to reduce
repeated mentions of Blender tools. Revisit only if later maintenance shows the same
multi-step representation/shading procedure changing in lockstep across owners.

Mixed requests may intentionally route to multiple owners. A scene task that asks
for a wooden crate beside a detailed game console should load props plus
product/electronics; a vehicle task that separately includes a removable consumer
device may load vehicle plus product/electronics. This is collaboration, not a
routing defect.

## Research/implementation sequence

1. Architecture & large structures.
2. Environment assets.
3. Roads/infrastructure.
4. Props.
5. Vehicles.
6. Product/electronics.
7. Vegetation.
8. Sculpting consolidation/upgrade.

After every 2–3 specialists, perform an integration pass for duplicate rules, routing ambiguity and contradictory safeguards. The final 8/8 review is recorded in [review report](../reports/BLENDER_DOMAIN_PACK_REVIEW_2026-10-03.md). The dedicated contracts pass remains a separate next stage: promote only stable, machine-checkable invariants; do not turn tuning advice or asset identity into contracts.

## Acceptance for each specialist

A specialist is not accepted merely because `SKILL.md` exists. Require:
- targeted external research recorded with source URLs and source type;
- clear activation and exclusion boundaries;
- agent-oriented workflow and decision points;
- explicit safeguards and stop conditions;
- domain-specific QA/evidence;
- unique lesson IDs;
- catalog/profile/route registration and structural checks;
- one bounded live Blender MCP exercise when the connector is available;
- Project Pulse update with PASS/WARN/SKIP and remaining gates.

The live Blender exercise should test the specialist's decision logic on a small representative asset or module, not attempt to create a polished production asset merely to prove routing.
