# Blender domain skill pack — Pass 0 architecture

Status: architecture baseline established 2026-10-02. Implement specialist skills one at a time; do not pre-fill future skills with copied generic rules. Shared invariants stay in `docs/foundation.md`, project-specific budgets stay in project profiles/contracts, and each specialist owns only its domain decisions.

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

## Planned specialist owners

### 1. `blender-architecture-environment` — buildings and large structures
Own buildings, houses, halls, towers, industrial structures, architectural shells, modular building kits, facade/roof/opening systems, architectural scale, grid/pivot conventions and architecture-facing trim/tileable material strategy.

Do not own roads/curbs, standalone street objects, furniture/props, vegetation, vehicles or appliances except where required as temporary scale/reference context.

Status: first implementation pass active/implemented in this workstream.

### 2. `blender-environment-assets` — standalone environment objects
Own benches, street lamps, fences, railings, barriers, bins, bollards, hydrants, posts, simple utility/street fixtures and other repeatable set-dressing objects whose main role is environmental structure rather than hand-held/interior prop detail.

Boundary with architecture: if the item is an integral building module, architecture owns it; if it is a reusable standalone object placed around structures, environment-assets owns it.

Boundary with roads/infrastructure: continuous/network geometry belongs to roads/infrastructure; discrete fixtures belong here.

Status: second implementation pass active/implemented in this workstream.

### 3. `blender-roads-infrastructure` — roads, paths and networked ground infrastructure
Own roads, sidewalks/pavements, curbs, gutters, medians, paths, trails, ramps, crossings, road shoulders and other connected linear/network systems, including modular intersections, splines/curves and transition logic.

Do not own vehicles, standalone street furniture, terrain/vegetation or building shells.

Status: first implementation pass active/implemented in this workstream.

### 4. `blender-props` — small and medium props
Own furniture, containers, tools, clutter, decor, hand-held objects, interior set dressing and miscellaneous discrete assets whose production logic is prop-centric rather than architectural, botanical, vehicular or electronic-product-specific.

Boundary with environment-assets: props are generally portable/interior/detail storytelling objects; environment-assets are generally site/street fixtures tied to an environment system. Ambiguous objects should be routed by intended reuse and placement, not by size alone.

### 5. `blender-vehicle-modeling` — cars and wheeled vehicles
Own cars, trucks, vans, buses, trailers, motorcycles where applicable, carts and other wheeled vehicles: proportion/reference alignment, body panels, wheel/tire systems, suspension-visible geometry, repeated/symmetric parts, hard-surface topology, moving assemblies and vehicle-specific QA.

Do not own generic electronics, environment props or character rigs. Vehicle animation/rigging may hand off to general rigging/animation after vehicle-specific articulation decisions are established.

### 6. `blender-product-electronics-modeling` — household and digital equipment
Own appliances, consumer electronics, computers, monitors, TVs, consoles, kitchen devices and product-design-like hard-surface assets where manufactured assembly, panel gaps, bevel language, vents, connectors, display surfaces and material separation are central.

Boundary with props: a generic decorative object stays in props; an engineered appliance/device with product-design construction belongs here.

### 7. `blender-vegetation` — plants and foliage
Own trees, shrubs, grass, flowers, vines and plant clusters: botanical reference, branching hierarchy, silhouette, cards/mesh choices, variation, instancing, wind-ready segmentation and performance-aware vegetation construction.

Do not own terrain, roads or generic environment props. Organic sculpting can support trunk/rock-like forms but vegetation remains the production owner.

### 8. `blender-sculpting` — expanded sculpting specialist
Promote/replace the current narrow organic-sculpting reference with a canonical specialist for controlled organic and hard-surface sculpt passes, form hierarchy, brush/remesh decisions, regional correction, damage/weathering sculpt, topology-loss safeguards and handoff to retopology.

This skill must absorb useful current sculpting guidance rather than creating a competing rule source. Existing pipeline references should become compatibility/routing pointers where appropriate.

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

## Research/implementation sequence

1. Architecture & large structures.
2. Environment assets.
3. Roads/infrastructure.
4. Props.
5. Vehicles.
6. Product/electronics.
7. Vegetation.
8. Sculpting consolidation/upgrade.

After every 2–3 specialists, perform an integration pass for duplicate rules, routing ambiguity and contradictory safeguards. After all eight, perform the dedicated contracts pass: promote only stable, machine-checkable invariants; do not turn tuning advice or asset identity into contracts.

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
