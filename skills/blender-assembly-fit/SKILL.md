---
name: blender-assembly-fit
description: Read-only assessment of how parts integrate into an existing Blender 3D assembly: suspicious pasted-on details, weak visual/functional attachment, inconsistent proportions, foreign-looking components, and broken design flow. Use for FIT_INTEGRATION reviews of props, machinery, characters, vehicles, architecture and other assembled assets. Do not use for asset creation, automatic geometry repair, standalone collision/physics testing, animation, or export.
---

# Blender Assembly Fit — FIT_INTEGRATION

Read the [foundation contract](../../docs/foundation.md) and, for live Blender evidence, [capture and measurement limits](../../docs/blender-evidence.md). This skill is **diagnostic-only**. It does not create, reposition, delete, join, remesh, save or export geometry.

## Ownership and handoff

Own: evidence-backed assessment of whether an existing component belongs, is suitably seated in its assembly, follows the intended shape language, scale/detail hierarchy and credible attachment design. This is usable across genres and industries; never import a specific game's slot conventions.

The actual domain owner fixes defects: character, robot-mechanism, weapon-module, vehicle, props, environment, architecture, destruction or recovery. [Verification](../verification/SKILL.md) owns final acceptance and L1–L4 evidence; [reference reconstruction](../visual-reference-reconstruction/SKILL.md) owns new reference interpretation and PASS 0. Read-only diagnosis does not re-run PASS 0 or grant repair permission.

Not owned in this first version: automated `FIT_FLOAT`, `FIT_BURIED`, `FIT_POKE`, structural load calculation, exact volume intersection, true physical stability, motion simulation, new MCP operations, global gating or automatic redesign. An apparent gap or buried surface may be recorded as a *suspected symptom*, never claimed as a completed specialized test.

## Activation guard

Trigger when the user asks why an already available model has foreign-looking, poorly fitted, unmotivated, disconnected-looking or proportionally inconsistent pieces, or explicitly requests `FIT_INTEGRATION` / assembly-coherence QA.

Do not trigger from the mere presence of many meshes, hard-surface style, a model name, an export request, a geometry creation task, or another specialist's normal intake. If the user requests an edit, provide findings and refer the scoped fix to the relevant modeling owner; do not edit through this skill.

## Read-only diagnosis

1. **Scope and design authority.** Name the asset, object set, scene/frame/pose, project units, requested views, original reference/Model Contract, accepted silhouette and intentional asymmetry. Record `TASK / MUST PRESERVE / MAY CHANGE=none / SUCCESS`. Unavailable references remain unknown, not inferred facts.
2. **Assembly graph.** Inspect actual scene object names, parent hierarchy, transforms, modifiers, material roles, visible collections, mesh users, pivots and declared optional properties. Differentiate independent decorations, connected structure, joints, internal parts, deliberately detached or hovering elements.
3. **Geometric candidates (L1).** On a *bounded, explicit* set of parts, compare evaluated world-space dimensions, orientation and relative scale; use broad-phase bounds only to select plausible neighbours. Use sampled nearest-surface/BVH/contact diagnostics for targeted pairs, not to declare a physically valid attachment. Document tolerance in actual scene units and sample limitations. Read [diagnostic protocol](references/diagnostic-protocol.md).
4. **Artistic integration (L4).** Capture front, side, back, three-quarter and affected closeups as appropriate, from fixed, documented views. Inspect the actual images; where a baseline exists compare identical camera, framing, frame, lighting and material mode. Check mounting transition, silhouette/negative space, primary-to-tertiary shape hierarchy, functional plausibility, local style, detail density and the viewer's intended distance. Use the matching [domain subgroup](references/domain-cues.md) (machinery/weapons, vehicles, characters/wearables, architecture/props, organic) for seating cues, usual false positives, views and repair owner.
5. **Classify with restraint.** Separate objective observations from interpretation. Treat plausible deliberate asymmetry, kitbash joints, visible fasteners, gaps, suspension clearance, transparent/cloth parts and articulated extreme poses as exceptions to investigate, not errors. If a claimed defect depends on unseen geometry or missing user intent, return `WARN` or `SKIP` rather than an invented `FAIL`.
6. **Produce actionable findings.** For each suspected integration problem, give stable object path, named view/pose, location or relationship, measurable observation (if available), visual reasoning, reference/constraint, severity, confidence, affected design invariant and bounded recommendation. State the owning repair skill, but change nothing. Use existing QA receipt and verification conventions; do not invent another certification schema.
7. **Stop.** End when all scoped candidates are reviewed or evidence is unavailable, with explicit coverage and unreviewed regions. A clean sample does not certify the full model, animation or game runtime.

## FIT_INTEGRATION decision policy

| Result | Allowed meaning |
|---|---|
| `PASS` | Named, inspected criterion has supporting evidence in the specified pose/views; only scoped pass |
| `WARN` | Plausible design/assembly mismatch needing human judgment; **default for aesthetic concerns** |
| `FAIL` | Explicit user/contract invariant demonstrably broken by a named object with reproducible evidence; never merely an unusual style |
| `SKIP` | Required source, geometry, pose, capture or analysis is unavailable/inapplicable; explain which |

Keep `STRUCTURAL` and `VISUAL` findings separate. A structural/capture PASS is not artistic approval. A screenshot existing on disk but unreviewed is `VISUAL REVIEW REQUIRED`, not `VISUAL PASS`. Use `SELF_REVIEW` unless another actual independent reviewer provided a documented verdict. No fabricated confidence percentages or universal size/contact thresholds.

## Evidence/output contract

Use one compact table or QA receipt-compatible observation per issue:

`FIT_INTEGRATION | status | path A [vs B] | what/where | numerical or visible evidence | view/frame | constraint/intent | confidence | suggested repair owner`

Avoid repeating the entire object inventory when only one component is in scope. For a negative result, state: reviewed object count, measured pair count, views/poses opened, known exclusions, and what remains untested. Preserve actual capture paths/hashes if supplied by tools.

## Safety and precision

- Never assume `bbox overlap = contact`, `BVH triangle overlap = unwanted penetration` or `nearest sampled distance = certified minimum`. Thin shells, curves, modifiers, non-manifold/open geometry and occlusion demand qualified conclusions.
- User intent and protected design outrank aesthetic norms. Do not demand photoreal engineering on deliberately stylized, surreal, floating or modular art.
- Never replace deliberate mechanical clearance with a visual weld, or change socket/pivot origins merely to make a screenshot look aligned.
- Avoid applying modifiers, adding temporary objects in the production scene, changing user selection/render settings or opening a different blend in a read-only request.
- Bound pair counts and evaluated vertex work to the task. If a long operation times out, inspect state before retry; never claim unseen results.

## Pitfalls / Lessons Learned

### FIT-001 — Overlap reported as a defect
- Symptom: a bolt set into a panel or a kitbash joint is reported as a fit failure.
- Cause: bounding-box or triangle overlap treated as unwanted penetration.
- Rule: overlap only nominates a candidate; confirm seating against intent and views.
- Verification: the finding names the views and the evidence beyond the overlap.

### FIT-002 — Taste reported as FAIL
- Symptom: an unusual but intended part (asymmetry, stylised scale) gets `FAIL`.
- Cause: aesthetic judgement treated as a broken requirement.
- Rule: aesthetic concerns are `WARN`; `FAIL` needs a named MUST PRESERVE/HARD invariant.
- Verification: every `FAIL` cites its invariant source and the view that breaks it.

### FIT-003 — Diagnosis drifts into editing
- Symptom: a fit review moves, welds or re-pivots parts to make a screenshot look right.
- Cause: the diagnostic owner acting as the repair owner.
- Rule: report the smallest local action and its domain owner; change nothing.
- Verification: scene state and file hash are unchanged after the review.

Version: 1.0.0, 2026-11-19 (registered; lessons from the skill's own design rules, not from a recorded incident).

## Supporting references

- [Diagnostic protocol](references/diagnostic-protocol.md) — geometry evidence, review criteria and false-positive guards.
- [Domain subgroups](references/domain-cues.md) — G1 machinery/weapons, G2 vehicles, G3 characters/wearables, G4 architecture/props, G5 organic; planned automated detectors.
- [Research notes and search tags](references/research-notes.md) — source-backed concepts, Blender 5.3/API notes, search vocabulary.
- [Behavioral acceptance cases](references/acceptance-cases.md) — smoke-test scenarios for later routing and skill review.

**State:** registered canonical owner for read-only FIT_INTEGRATION diagnosis (2026-11-19, unreleased; the repository version changes only after the reviewed PR merge). Routing tests cover activation and non-activation; live Blender behaviour of AF-01…AF-16 is still to be exercised on real assets.
