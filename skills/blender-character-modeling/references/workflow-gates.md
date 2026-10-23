# Character workflow gates

Use [QA schema 3](../../../docs/qa-receipt.md) and the [character owner](../SKILL.md).
PASS0 owns design; v1/v2 are audit-only NOT_RECORDED_LEGACY. Gates validate
declared readiness, not art or arbitrary Blender operations.

## Execution flow between gates

Continue authorized work without per-stage permission. Reuse receipts/checkpoints;
resume at the first unresolved gate. Read, execute, inspect at meaningful boundaries.
Ask only for missing design decisions or scope conflicts. No second stage ledger.

Reference head/bust: FACE → skull/jaw/profile/facial volumes → DETAIL →
surface/hair finish → FINAL. Rough hair may establish silhouette early; review
obscured geometry without hair and also inspect the final silhouette. Hidden
anatomy follows Contract/deformation needs, not a universal two-eye rule.
A bust does not authorize a full body.
Use Dual Verification at selected stages: inspect current images first, recapture
changed regions/dependencies, batch corrections. No critic after every small edit.
Block dependent work only; report the blocker and next action.

## FACE: choose before the final face

Inspect authoritative originals; record sources, supported identity anchors,
occlusion, method reason, required tools and expected visual evidence:

- GEOMETRY_ONLY: volumetric identity or user-approved simplification, never an
  excuse to drop distinctive graphics.
- DIRECT_FEATURE_TRANSFER: crop/mask/register original features through
  [surface transfer](../../blender-reference-surface-transfer/SKILL.md).
- RECONSTRUCT_THEN_LAYER: provisional generated face with surviving anchors,
  then original hair in front; hidden detail stays INFERRED/SPECULATIVE.
- HYBRID_PRESERVATION: retain reliable features, locally repair missing regions
  and integrate without replacing canonical identity.

The last two require available ImageGen and actual input/mask/prompt/output
lineage, otherwise BLOCKED. PASS0 generation cannot substitute downstream work.
Hair alone does not mandate generation; keeping hidden regions covered may
justify geometry-only.

## DETAIL: accept primary forms before mass detailing

Blockout → proportions → primary → secondary → detail. Require reviewed
primary_proportions, primary_head_face, primary_neck_shoulders,
primary_torso_pelvis, primary_silhouette, front/side/alternate views, relevant
closeups and the assembly graph MACRO checkpoint. Evaluate the scoped asset;
do not invent absent body regions. FAIL/SKIP/unreviewed forms block detail.
Numbers alone do not accept shapes; major edits invalidate dependent reviews.
Keep skull separate from hair in proportion measurements.

After two unsuccessful corrections, save .blend, record the previous and a
different method/owner in existing escalation. A parameter tweak is insufficient.
Resume dependent work only after reviewed resolution.

## FINAL: execute and verify

Run qa_gate.py RECEIPT --verify-files --stage FACE, DETAIL, then FINAL at their
boundaries; retain results. Current state cannot prove past execution order.
Record DISCOVERED → READ → SELECTED → EXECUTED → VERIFIED (or SKIPPED/BLOCKED).
Reading is not execution. Require artifacts, reviewed identity/occlusion/seam/
binding evidence and final fixed views.
Seams or identity drift fail. Metadata is not visual QA.
