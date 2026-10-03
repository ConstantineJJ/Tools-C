# Posteffects and polishing — implementation and acceptance

Date: 2026-10-03. Canonical baseline: `8ac57abc02a293eaf7f90f2b043f736d188ae1f3`.
Integration baseline: `5f590e13ec6fc3f15432b032930dbdaf6ca12b02`.
Scope: add a researched late finishing skill, its consumers and structural contracts.
No production asset edits, shader-quality acceptance or additional production stage.

## Result and ownership

Added [Posteffects and polishing](../skills/blender-posteffects-polishing/SKILL.md),
canonical ID `blender-posteffects-polishing`. Catalog: 24 canonical skills, nine
unchanged legacy aliases. The original eight domain specialists retain their scope.

This stage follows the relevant geometry/topology, surface and rig/motion
prerequisites and precedes final visual QA/delivery. It owns scoped material
assignment/refinement, texture cleanup, material-aware localized dirt, scratches,
paint wear/peeling, surface cracks, motivated emission and requested presentation
effects. Clean/stylized/new assets remain legitimate; wear and glow are optional.

Surfaces retains UV/bake/baseline PBR correctness; sculpting retains shape damage;
domain owners retain construction/proportions; rigging/animation/export/Godot keep
their owners. No universal effect strengths, dimensions, shader or texture budgets.

The skill links [finishing techniques](../skills/blender-posteffects-polishing/references/finishing-techniques.md)
and [research notes](../skills/blender-posteffects-polishing/references/research-notes.md).
Eleven primary documentation/tutorial/artist sources inform clean-material-first,
roughness response, causal wear masks, editable layers, motivated emission and
separate image effects. Some Blender pages were accessible through indexed manual
excerpts while full fetches returned 402; no claim to have watched embedded videos.
Toolbag/Substance techniques are translated into decisions, not tool dependencies.

## Visual QA contract

The actual evidence recipe is loaded with the skill. Capture relevant material/
rendered views and closeups, open/inspect PNGs, diagnose defects, correct within
scope, then recapture and inspect comparable AFTER images. Missing direct capture
uses the tested Python-image route or saved-candidate offline fallback.

Managed asset captures do not certify a scene compositor. Requested glare needs an
explicit candidate-scene Render Result with its intended settings; inspect both
underlying and effected images. Material emission, emitted illumination and image
glare are separate. Capture success stays VISUAL REVIEW REQUIRED until inspection.

## Routing and compatibility correction

English/Russian finishing requests select the new stage without restarting asset
geometry. Baseline materials/UV/bakes retain surfaces; read-only requests retain
verification; mixed creation/sculpt/delivery requests retain the relevant owners.
Preservation clauses do not turn protected UVs/weights into requested stage edits.

The first actual connector smoke exposed a cached reader module: the new skill
body loaded but its new finishing reference was missing. The canonical runtime
now supplies that reference when an older two-argument reader omits it. A focused
cached-reader regression proves the complete context appears exactly once. The
second connector smoke matched current local contexts completely, including hashes.
No server/tunnel restart or adapter-source edit was needed.

Both legacy router trees were regenerated through the canonical synchronizer:
18 router hash updates and two manifests. Names, alias targets and provenance stay
unchanged; no duplicate canonical skill was installed in the integration repo.

## Machine-checkable acceptance

[Polishing contracts](../.tooling/blender-polishing-contracts.json) add five rules:
canonical ID/path, self-profile membership and active contracts, real AGENTS/pipeline
entrypoint links, prerequisite/evidence/research links, and surfaces/core handoff.
The base contract protects activation; the existing domain pipeline rule requires
the downstream polishing link. This uses existing bounded checker kinds without
new checker code. Structural rules do not prove artistic quality, semantic order
in prose, runtime routing or export portability.

| Check | Observed result |
|---|---|
| Tools_C L1 | 26 PASS, 0 WARN, 0 FAIL; L2–L4 SKIP |
| Blender-MCP-Co L1 | 9 PASS, 0 WARN, 0 FAIL; L2–L4 SKIP |
| Full regression | 94/94 PASS, 0 failures/errors/skips |
| Actual connector routing | 16/16 full contexts equal current canonical results; hashes recomputed |
| Disposable MCP SDK stdio | PASS: 15 tools, nine legacy context hashes, loaded/disk identity and syntax rejection |
| Persisted negative evidence | 6/6 intentional violations rejected with their declared rule/diagnostic |
| Legacy compatibility | All nine alias targets/provenance unchanged; regenerated routers validate |
| Unrelated integration work | All 27 pre-existing dirty files preserved byte-for-byte |
| Optional skill-creator validator | SKIP: PyYAML absent; canonical catalog/frontmatter/link validation PASS |
| Production material/visual/target acceptance | SKIP: no asset finishing requested or performed in this skill-authoring pass |

Evidence: [summary](posteffects-polishing-2026-10-03/summary.json),
[routing](posteffects-polishing-2026-10-03/live-routing.json),
[negative cases](posteffects-polishing-2026-10-03/negative-cases.json),
[Tools_C L1](posteffects-polishing-2026-10-03/l1-tools-c.json),
[integration L1](posteffects-polishing-2026-10-03/l1-integration.json),
[deployment](posteffects-polishing-2026-10-03/deployment.json).

Next separately scoped exercise: apply the skill to a named asset and inspect its
actual surface/emission/compositor results and target behavior. This implementation
does not certify production art merely from structural checks or routing evidence.

Git handoff: canonical changes use an explicit file allowlist and are pushed to
Tools_C `origin/main`. Generated integration routers use a separate local commit;
the integration's five pre-existing unpublished commits and 27 unrelated dirty
files are preserved, and that repository is not pushed by this pass.
