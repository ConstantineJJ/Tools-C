# Skills-first pass: face transfer and character proportions

Date: 2026-10-08. Scope: **documentation-only changes to canonical Skills**.
No Blender scene, texture, geometry, rig, Hub, MCP add-on, harness checker,
router, tests, release or deployed alias was modified in this pass.

## Why

Agent_Red7 (2026-10-07) exposed visible seams after transferring face features,
hair obscuring source facial identity, inflated/revised skull and hair proportions,
and a weak distinction between structural PASS and visual acceptance. The user
requested better choices between preserving source pixels and reconstructing
missing regions. User-supplied figure charts are **illustrative proportion
references**, not a universal hard-coded anatomy or a source of exact 3D values.

## Changed canonical docs

1. `skills/blender-reference-surface-transfer/SKILL.md`
   - Three explicit strategies: DIRECT FEATURE TRANSFER,
     RECONSTRUCT-THEN-LAYER, HYBRID PRESERVATION.
   - Source/identity priority, occlusion layers, hard failure for visible pasted
     boundaries, production lesson RST-002.
2. `skills/blender-reference-surface-transfer/references/workflow.md`
   - Per-region visibility/identity decision, hair-behind/front ordering,
     landmark-to-UV registration and reversible feature ownership.
   - Dedicated Seam Integration / Patch Disguise method: align, mask,
     skin-only transition, color/gradient blend, bake, close inspection.
3. `skills/blender-reference-surface-transfer/references/record.md`
   - Map new strategy/evidence into **existing schema v1 string fields**
     without inventing rejected JSON keys or claiming machine visual QA.
4. `skills/blender-character-modeling/SKILL.md`
   - Explicit proportions owner and reference-linked landmark workflow.
5. **New** `skills/blender-character-modeling/references/body-proportions.md`
   - Head unit excluding hair, orthographic landmarks, style-family guidance,
     approved-zone protection, camera caution and pre-rig disposition.
6. `skills/blender-anime-character-modeling/SKILL.md`
   - Anime specialization consumes shared proportions without normalizing
     intentional stylization; skull/hair/face image sizes tracked separately.
7. `skills/visual-reference-reconstruction/SKILL.md`
   - PASS 0 collects supported humanoid proportions and uncertainty.
8. `skills/visual-reference-reconstruction/references/model-contract.md`
   - Reuses existing relative_dimensions/silhouette_notes/model_contract
     dimension/ratio/anchor rules; no new schema or secondary truth source.
9. `skills/blender-rigging-skinning/SKILL.md`
   - Pre-rig proportion/form handoff only; rig does not own body proportions.

## Verification and status

- **PASS (bounded):** All 9 edited/new documents were read back through Local
  Files MCP and checked for the required section names/markers.
- **PASS (bounded):** New proportions guide exists at the referenced path.
- **Not run:** Tools_C Python regression suite, `check.bat --self`, Blender MCP
  read_skill/live routing, renderer/texture/UV, saved-file reopen, Godot import,
  deployment or visual resemblance. The current connector exposes file operations,
  not arbitrary local command execution.
- The published v4.2.0 artifact remains unchanged. This **local working tree is
  ahead of the release in docs only**; release/commit acceptance is not claimed.

## Scope boundary and next passes

**Next: Harness pass.** Review actual consumers/tests and implement explicit
transfer-strategy record compatibility, proportion intake, error diagnostics
and runtime bridge health recovery in the correct authoritative source. Avoid
blind schema extension. Add focused positive/negative fixtures and run L1/regressions
in an execution-enabled workflow. Blender MCP timer health requires an actual
add-on fix plus after-open command execution; text rules alone cannot fix the queue.

**Last: cross-cutting QA pass.** Create enforceable view/evidence gates including
+/-45-degree high/low form views with perspective/foreshortening cautions,
orthographic proportion checks, closeups, before/after comparability,
protected approved zones, escalation, explicit PASS/WARN/SKIP and static versus
rig-/deformation-/engine-ready status. Test against an actual production asset.
Do not claim the QA pass is complete based on the new face seam instructions.
