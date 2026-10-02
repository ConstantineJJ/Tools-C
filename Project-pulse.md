# Tools_C — Project Pulse

Updated: 2026-10-02. Architecture: 4.0.1. Canonical repository: `ConstantineJJ/Tools-C`.
Current catalog: eighteen canonical skills, nine legacy Blender compatibility aliases.

## Done

- 2026-10-02: implemented canonical `blender-roads-infrastructure` for roads, sidewalks/pavements, curbs, gutters, medians, shoulders, crossings, ramps, trails and connected linear/network ground infrastructure. Added route/network preflight, cross-section contracts, modular vs spline/procedural/hybrid selection, curve/Geometry Nodes discipline, explicit junction ownership, terrain-fit safeguards, longitudinal UV/material logic, pedestrian transitions, dirt/trail handling, stress-test guidance, seven road lessons and handoff/stop conditions.
- 2026-10-02: recorded source-backed roads/infrastructure research under `skills/blender-roads-infrastructure/references/research-notes.md`; guidance uses Blender 4.5 curve/Geometry Nodes documentation plus road/street environment-production breakdowns. Real-world lane/curb dimensions, collision, LOD and engine budgets remain project-local rather than universal rules.
- 2026-10-02: registered `blender-roads-infrastructure` in `manifest.json`, reviewed profile, self-contracts, `AGENTS.md`, Blender pipeline routing and automatic MCP runtime routing. While resuming after an interrupted pass, removed duplicate roads routing entries introduced by overlapping partial edits. Active documentation counts are now eighteen canonical skills and nine legacy Blender aliases.
- 2026-10-02: implemented canonical `blender-environment-assets` for benches, street lamps, fence/railing panels, barriers, bins, bollards, hydrants, bike racks, planters and similar standalone environment fixtures. Added asset-role/placement preflight, construction logic, family/reuse strategy, hard-surface and shading decisions, UV/shared-material guidance, weathering logic, pivot/packaging rules, LOD/readability guidance, safeguards, six environment-asset lessons and handoff/stop conditions.
- 2026-10-02: recorded source-backed environment-asset research under `skills/blender-environment-assets/references/research-notes.md`, using Blender 4.5 documentation plus environment/prop production breakdowns. Project-specific texel density, triangle/LOD targets, collision and engine budgets remain local rather than universal rules.
- 2026-10-02: registered `blender-environment-assets` in `manifest.json`, reviewed profile, self-contracts, `AGENTS.md`, Blender pipeline routing and automatic MCP runtime routing. Active documentation counts are now seventeen canonical skills and nine legacy Blender aliases.
- 2026-10-02: established [Blender domain skill pack — Pass 0](docs/blender-domain-skill-pack.md) for eight staged specialist domains: architecture, environment assets, roads/infrastructure, props, vehicles, product/electronics, vegetation and sculpting consolidation. Future specialists remain unimplemented until their own research/QA pass.
- 2026-10-02: implemented canonical `blender-architecture-environment` for buildings, architectural shells, modular construction kits and other large man-made structures. Added domain ownership, scale/reference preflight, modular decomposition, grid/pivot discipline, non-destructive construction, material/trim strategy, performance guidance, safeguards, six architecture lessons and handoff/stop conditions.
- 2026-10-02: recorded source-backed architecture research under `skills/blender-architecture-environment/references/research-notes.md`; guidance is distilled from Blender documentation plus production/training/community/academic modular-environment sources, while project-specific metrics and budgets remain local.
- 2026-10-02: registered the architecture specialist in `manifest.json`, reviewed profile, self-contracts, `AGENTS.md`, Blender pipeline routing and automatic MCP runtime routing. Fixed active stale `Project-pulse` references to the actual `Project-pulse.md` path and replaced two hard-coded eight-router test assumptions with catalog-derived alias counts.
- 2026-10-02: filled the pre-existing missing activation-suite entry/description for `Blender_Animal_Anthropomorphic_Modeling_SKILL`; no animal production rules were changed.
- Imported the user's complete Tools_C v4.0.0 source snapshot into the canonical GitHub repository and integrated the four production skills: mechanic gym, subagent worktrees, lookdev gate and project state gates.
- Added `blender-animal-anthropomorphic-modeling` as a specialist canonical skill for animals, creatures, quadrupeds, stylized pets and anthropomorphic characters, with body-plan, anatomy, anthropomorphic blending, low-poly/stylization, deformation and handoff guidance.
- Registered the animal specialist in `manifest.json`, `AGENTS.md`, the reviewed profile, self-contracts and Blender pipeline routing. Canonical catalog is now fifteen skills; Blender compatibility aliases are now nine.
- Reconciled the live Windows Tools_C content at `E:\MyCreations\Tools_C` with the canonical 4.0.1 catalog: all four production skills are now present locally together with the animal specialist, current routing/profile/contracts, README and architecture docs.
- Created a full pre-reconciliation backup at `D:\Desktop\Constantine Hub docs and backups\Tools_C_pre_sync_2026-09-28` before replacing live metadata/content.
- Updated active documentation counts to fifteen canonical skills and nine Blender aliases; historical v4.0.0 migration evidence remains historical and is not rewritten.

## Verified

- 2026-10-02 roads/infrastructure L1 self-check: 9 PASS, 0 WARN, 0 FAIL across catalog/profile/routes/skills/contracts/files/json/links/generic checks.
- 2026-10-02 roads/infrastructure Python regression suite through live Blender MCP: 55 tests run, 55 PASS, 0 failures, 0 errors.
- 2026-10-02 live Blender MCP canonical read: `read_skill("blender-roads-infrastructure")` resolved `E:\\MyCreations\\Tools_C` and loaded foundation + pipeline + roads/infrastructure + verification context.
- 2026-10-02 live automatic routing PASS in Russian for a road + curb + sidewalk + crossing task: `get_skill_context` selected `blender-roads-infrastructure`.
- 2026-10-02 bounded Blender structural exercise PASS: temporary editable main/branch centerline curves, generated road strips, sidewalk envelopes, crossing and 1.8 m human proxy validated exact branch connectivity, 6.0 m road-width contract, 1.5 m sidewalk-width contract, 0.15 m curb-height contract, preserved elevation change, separate editable source vs delivery meshes, unit positive scales and clean mesh validation. All 8 temporary QA objects and their collection were removed afterward.
- Roads/infrastructure visual/material/terrain traversal QA is SKIP for this bounded structural exercise; no polished-road appearance or target-engine traversal acceptance is claimed.
- 2026-10-02 environment-assets L1 self-check: 9 PASS, 0 WARN, 0 FAIL across catalog/profile/routes/skills/contracts/files/json/links/generic checks.
- 2026-10-02 environment-assets Python regression suite through live Blender MCP: 55 tests run, 55 PASS, 0 failures, 0 errors.
- 2026-10-02 live Blender MCP canonical read: `read_skill("blender-environment-assets")` resolved `E:\\MyCreations\\Tools_C` and loaded foundation + pipeline + environment-assets + verification context.
- 2026-10-02 live automatic routing PASS in English and Russian: reusable bench/bollard/street-fixture tasks selected `blender-environment-assets` through `get_skill_context`.
- 2026-10-02 bounded Blender structural exercise PASS: temporary two-member bench family and three repeated bollards used a 1.8 m human scale proxy, 1.8 m bench width, 0.50 m seat top, 0.90 m bollard height, bottom/ground placement anchors, shared seat/back/leg/bollard mesh data and unit positive scales. All scripted checks and mesh validation passed; all 16 temporary QA objects and their collection were removed afterward.
- Environment-assets visual QA is SKIP for this bounded structural exercise; no appearance/material/weathering acceptance is claimed from procedural geometry checks alone.
- 2026-10-02 L1 self-check after architecture registration: 9 PASS, 0 WARN, 0 FAIL across catalog/profile/routes/skills/contracts/files/json/links/generic checks.
- 2026-10-02 clean Python test state through live Blender MCP: 55 tests run, 55 PASS, 0 failures, 0 errors. Earlier in-process failures were traced to stale module/reload state plus old hard-coded alias expectations; a fresh module state is green.
- 2026-10-02 live Blender MCP canonical read: `read_skill("blender-architecture-environment")` resolved `E:\\MyCreations\\Tools_C` and loaded foundation + pipeline + architecture + verification context.
- 2026-10-02 live automatic route: a modular-building task selected `blender-architecture-environment` through `get_skill_context`.
- 2026-10-02 bounded Blender structural exercise PASS: temporary wall/corner/door/floor/human-proxy kit used 2 m wall modules, shared wall mesh data, unit object scales, deterministic snap positions, 1.2 m × 2.2 m door opening and 1.8 m scale proxy; all scripted structural checks passed. Temporary QA collection/meshes were removed afterward and the scene returned to 0 objects.
- Architecture visual QA is SKIP for this bounded routing/structure exercise; no visual acceptance is claimed from structural checks alone.
- Existing repository baseline: `python3 -m unittest discover -s tests -q`: 55 tests passed, 2 Windows-only tests skipped in the Linux workspace used for the prior transfer.
- Existing repository baseline: `python3 tools/check.py --self`: L1 9 PASS, 0 WARN, 0 FAIL for the canonical transfer baseline.
- 2026-09-28 animal-skill live check: Tools_C catalog/profile/routes/skills/contracts/file/json/link/text checks returned L1 PASS before the production-skill reconciliation.
- 2026-09-28 Blender compatibility sync after the animal skill: `PASS SYNC: 9 compatibility routers`; Blender MCP listed 9 entries and resolved `Blender_Animal_Anthropomorphic_Modeling_SKILL` to canonical root `E:\MyCreations\Tools_C`.
- 2026-09-28 post-reconciliation live check: Tools_C catalog/profile/routes/skills/contracts/file/json/link/text checks all returned L1 PASS with 0 FAIL.
- 2026-09-28 post-reconciliation Blender router sync returned `PASS SYNC: 9 compatibility routers`.

## Current / next

- `blender-architecture-environment`, `blender-environment-assets` and `blender-roads-infrastructure` are implemented and structurally accepted for their bounded passes. Visual acceptance remains intentionally SKIP because these exercises tested routing, scale/metrics, pivots, reuse/shared data, assembly/placement and network structure rather than polished production art.
- Next work before Skill 4: perform the first cross-skill integration pass across architecture + environment-assets + roads. Check ownership overlap, duplicated hard-surface/modularity guidance, routing collisions and contradictory safeguards; extract no shared hard-surface layer unless the repeated decision procedure is substantial enough to justify a single owner.
- After that integration pass, continue with `blender-props`. The remaining vehicle, product/electronics, vegetation and sculpting specialists stay unimplemented until their own research/QA passes.
- Dedicated domain contracts for this eight-skill expansion remain deferred until the specialist set is mature. Only existing Tools_C self-contract registration has been updated so far.
- The local Git metadata note from the 2026-09-28 reconciliation remains unresolved unless handled elsewhere: local `main` was then on the older standalone history with no `origin`. Re-check current Git state before acting; do not hand-edit Git object/ref files.
- Keep generic character modeling, retopology, rigging, animation, export and verification under their existing owners; the new domain specialists must not become alternate rule sources for those stages.

## Historical bridge note

- The 2026-09-27 Blender tunnel lifecycle failure and loss of the old Godot launcher with the deleted Stickmans_Duel project are historical. Constantine Hub later restored managed Blender, Local Files and Godot adapters; do not use the deleted project as an infrastructure source.

## Risks / recommendations

- The imported v4 evidence documents prior checks and is not fresh runtime evidence for every later change. Recheck actual connectors and target projects before claiming deployment or visual acceptance.
- Keep project-specific rig, clips, art direction and asset budgets in profiles/decisions rather than universal skills. Preserve a single canonical owner for each instruction and update this Pulse after substantial work.
