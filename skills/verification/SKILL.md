---
name: verification
description: Validate a scoped change with static, engine, runtime and visual evidence, including regressions and unrun checks. Use for QA or acceptance, not as permission to edit the asset.
---

# Verification

Read the required [foundation contract](../../docs/foundation.md).

## Instruction Priority

Use the user's acceptance criteria and active project contracts first, then this skill. A successful lower-level check never substitutes for required runtime, visual or human-observed behavior.

## Domain constraints

- Protected: the subject under review and comparability of baseline evidence; restore temporary probe state.
- Owned edits: diagnostic setup and evidence files within scope, or a separately requested fix.
- Acceptance: every applicable criterion has a supported PASS, WARN, FAIL or SKIP with reason and a clear remaining owner.

## Evidence levels

Use the level definitions and verdict semantics in the foundation. Read
[engine probe limits](../../docs/engines.md) before L2/L3 runs and
[evidence methods](references/evidence.md) for visual, pose or performance comparisons.
For Blender, use [snapshot/capture/export tools](../../docs/blender-evidence.md):
STRUCTURAL PASS is separate from VISUAL SKIP, VISUAL REVIEW REQUIRED and VISUAL PASS.
A PNG must be inspected for the named criterion before visual acceptance.

## Anti-degradation and stop

Compare the requested improvement and affected views, assets, topology, deformation, animation, runtime stability or complexity as applicable. Keep an improvement without material regression; correct a bounded regression; otherwise restore only your own attempted change through the project's recovery method. Stop after the required evidence is gathered and the result and open checks are reported. Test counts and exit codes alone do not establish visual or user-feel acceptance.

## Pitfalls / Lessons Learned

### VER-001
- Symptom: a better front render hides a worse profile or deformation.
- Cause: changed presentation or one-view acceptance.
- Rule: compare fixed views and affected poses; reproduce the user's actual settings.
- Automated check: V1 cannot judge visual quality; evidence remains L4.
- Verification: inspect before/after views and relevant poses explicitly.
- Added from / context: existing Blender QA/refinement procedures and ArcEngine verification reference.
- Version: 0.1.0, 2026-09-21.
