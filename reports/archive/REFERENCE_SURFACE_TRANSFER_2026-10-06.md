# Reference Surface Transfer — 2026-10-06

## Scope and result

Added canonical [blender-reference-surface-transfer](../skills/blender-reference-surface-transfer/SKILL.md)
to the existing Tools_C Skills/Harness. The route preserves useful original pixels
and graphic identity: select region → crop → justified rectification/upscale/cleanup
→ masked regeneration only for insufficient data → projection/decal/UV transfer
→ bake → local seam cleanup → QA. Shape remains with geometry owners, UV/bake
mechanics and baseline PBR with surfaces. Roughness/metallic/normal are reconstructed
separately; RGB is not blindly repurposed as physical data.

Face/eye identity, exact markings, asymmetric prints and unique wear receive
explicit protection. Supporting geometry is still required. Generated auxiliary
views and generative upscale cannot become new observed source evidence. Existing
PASS 0/Model Contract decisions are reused, without restarting surface-only work.

## Integration

- Catalog/profile/AGENTS/pipeline and relevant PASS 0, surfaces, anime and finishing
  handoffs point to the new owner. Catalog: 28 canonical skills, nine legacy aliases.
- English/Russian routing covers focused transfer, protected geometry, read-only QA
  and mixed creation/UV/export/finishing. Full source/workflow/record/surfaces context
  is delivered, including cached-reader compatibility.
- [Registration contract](../.tooling/surface-transfer-contracts.json) protects
  activation, owner path, entrypoint/dependency links and required checker/test files.
- [Transfer-record checker](../tools/surface_transfer.py) uses the standard library
  and validates strict JSON, bounded crop coordinates, ordered input/output lineage,
  masked repair provenance, separate PBR basis, bake/seam-cleanup records and
  evidence declarations. Optional file checks validate containment and SHA-256.
- Managed routers were regenerated with `tools/sync_blender.py --project
  E:/MyCreations/Blender-MCP-Co`, in both managed trees. No bridge API changes.

## Evidence

- [Self L1](surface-transfer-2026-10-06/self-check.json): 50 PASS, 0 WARN/FAIL, 3 SKIP.
- [Integration L1](surface-transfer-2026-10-06/integration-check.json): 9 PASS,
  0 WARN/FAIL, 3 SKIP.
- [Regression output](surface-transfer-2026-10-06/regressions.txt): **198 tests PASS**,
  0 failures/errors/skips; includes existing suites and 12 new tests with positive/negative subcases.
- [Live connector](surface-transfer-2026-10-06/live-routing.json): seven actual MCP
  contexts match local owners, every delivered document hash and context digest.
  English/Russian transfer, original wear, read-only QA, PASS 0 → robot → transfer,
  UV handoff and preservation clauses pass without missing/truncated documents.
  Live catalog reports 28 canonical owners. No server restart was needed.
- [Preservation baseline](surface-transfer-2026-10-06/preservation.json): all 37
  previously dirty/untracked files matched before the required additive Pulse
  update. Other pre-existing files stay byte-identical; old Pulse content is retained
  apart from its date/catalog header and the new scoped entries.
- `git diff --check` passed in both roots. Skill-creator optional quick validator
  SKIP: its Python environment lacks PyYAML. Canonical dependency-free L1 passed.

An early attempted baseline test overlapped the not-yet-registered new skill and
failed catalog checks; it is not counted as a baseline or final result. The first
completed integrated suite passed 196 tests. A focused review-noun routing failure
and a temporary test placement error were corrected before the final run. Failed
direct manual-page fetches were supplemented by indexed official Blender excerpts;
technical source links and scope are in the workflow reference.

## Limits and next use

This validates skill/harness structure, rejection cases and live context delivery.
No production asset, image, Blender scene or material was edited. Asset transfer,
actual crop/rectification, regeneration quality, bake, seams, saved Blender reopen,
facial likeness/deformation and target-engine visual acceptance are SKIP for this
system extension. A scoped source/asset exercise is the next evidence gate.

The checker does not inspect image pixels, mask containment, text legibility,
semantic reason quality, source authority or PBR correctness. A structurally valid
record can honestly contain pending bake and SKIP/FAIL reviews. It always reports
visual NOT_EVALUATED; recorded PASS is never promoted into machine-certified art.

Changes remain local and uncommitted; no release/publication requested. Starting
HEADs: Tools_C `c662b3576d9a613b9e091ddd43d696cb19197936`, integration
`6632fea7940dae8158eaebc1c6b8aaa0bd7da37e`. Existing branch divergence and unrelated
launcher/catalog changes were preserved.
