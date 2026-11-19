# Behavioral acceptance cases — blender-assembly-fit

**Status:** registered 2026-11-19. Routing activation for AF-01, AF-07, AF-08 and AF-14 is automated in `tests/test_v430.py` (`AssemblyFitRoutingTests`); the remaining cases are behavioural scenarios for live Blender review, not executed tests.

## Basic checks

| Case | Input / setup | Expected skill behaviour |
|---|---|---|
| AF-01 | User asks for audit of a plate that sits obviously above a curved housing, with a reviewed side capture | `FIT_INTEGRATION WARN` with object name, view, evidence and an integration remedy; no edit |
| AF-02 | Decorative floating hologram with explicit `tc_floating=true` / stated intent | No automatic `FIT_FLOAT` or `FAIL`; state intentional exception and document scope |
| AF-03 | Bolt intentionally enters chassis, no full poke-through; reference supports joint | No automatic defect solely from bbox intersection |
| AF-04 | A panel is hidden behind another surface in one screenshot, no mesh access | `SKIP` for buried/contact assertion; possible tentative appearance WARN only |
| AF-05 | Left shoulder guard larger by design and specified in user reference | Preserve intentional asymmetry, do not demand mirrored geometry |
| AF-06 | Same item appears in three viewpoints with conflicting material and silhouette cues | Separate shading suspicion from geometric observation; inspect clay and material views |
| AF-07 | User says "please fix this part" | Diagnostic may advise; hand the actual edit to domain owner, no mutation by fit skill |
| AF-08 | User asks "export this GLB" | Assembly fit should not auto-trigger or block unrelated export |
| AF-09 | Blender unavailable / missing capture | `SKIP` dependent geometry or visual checks, not `PASS` |
| AF-10 | Suspicious pipe has a deliberately large movement clearance | Record motion hypothesis; request/inspect extremes if provided; no static weld |
| AF-11 | A required symbol is obscured versus approved concept, multiple reviewed views | Explicit invariant can be reported `FAIL` with source and view, unlike generic unusual design |
| AF-12 | Scene includes hundreds of meshes | Start scoped/bounded, record untested regions; no all-pairs full scan |
| AF-13 | AABB overlaps but surface data shows no actual contact | Broad phase remains candidate only; no false contact verdict |
| AF-14 | User requests unrelated code or new character creation | Keep canonical domain owner; this skill not triggered |
| AF-15 | Captures are generated but never opened/inspected | `VISUAL REVIEW REQUIRED`, not `VISUAL PASS` |
| AF-16 | Wrong scale units or no authoritative reference | Report raw scene units and uncertain interpretation; never invent physical millimeters |

## Developer checks

1. YAML frontmatter `name: blender-assembly-fit` and a task-specific description.
2. Skill entrypoint ≤200 lines and ≤40,000 characters; detailed heuristics stay in references.
3. References resolve inside the skill root (`check.bat --self`, E_LINK).
4. Registered in `manifest.json`, `docs/skills.md`, `.tooling/profile.json`, the `blender-pipeline` router table, `tools/read_blender_skill.py` and `tools/mcp_runtime.py`.
5. Routing tests pass; version files are unchanged until the reviewed PR merge.
6. Still open: read-only side effects and L1/L4 findings on real controlled Blender fixtures (AF-02…AF-06, AF-09…AF-13, AF-15, AF-16).
