# Character workflow gates

Extends the existing [QA receipt schema 3](../../../docs/qa-receipt.md) and
[character modeling](../SKILL.md); PASS0/Model Contract stays the single design
owner. New reference-character production uses v3, retaining v2 camera setup.
Historical v1/v2 remain readable as NOT_RECORDED_LEGACY. Stage PASS proves
consistency of declared readiness, not art or enforcement of arbitrary Python.

## FACE: choose before the final face

Inspect authoritative originals; record source IDs, supported identity anchors,
occluded regions, reason, required tools and expected reviewed quality evidence:

- GEOMETRY_ONLY: identity is volumetric, or the user accepted simplification.
  Easier geometry does not justify dropping distinctive graphic identity.
- DIRECT_FEATURE_TRANSFER: preserve original features; crop, mask, register,
  integrate seams through [surface transfer](../../blender-reference-surface-transfer/SKILL.md).
- RECONSTRUCT_THEN_LAYER: provisional generated face, surviving identity anchors,
  intended hair restored in front. Hidden detail remains INFERRED/SPECULATIVE.
- HYBRID_PRESERVATION: preserve reliable source features; repair missing regions
  locally, register and integrate. Do not replace the canonical identity.

For the last two, check ImageGen in this session and execute it with real
input/mask/prompt/output lineage or declare BLOCKED. Optional PASS0 generation
never waives a selected downstream procedure. Hair alone does not mandate
ImageGen; keeping hidden regions covered can justify geometry-only.

## DETAIL: accept primary forms before mass detailing

Blockout → Proportions → Primary Forms → Secondary Forms → Detailing.
Require reviewed primary_proportions, primary_head_face, primary_neck_shoulders,
primary_torso_pelvis, primary_silhouette, matched front/side and an alternate
view, closeups as needed and the existing assembly graph's MACRO checkpoint.
FAIL/SKIP/unreviewed forms block detailing regardless of added accessories.
Numeric envelopes alone do not accept shapes. Major edits invalidate dependent
reviews; retain skull/hair separation and reference-specific proportions.

After two unsuccessful local corrections, save a .blend checkpoint, name the
prior method and a different method/owner, and escalate in the existing receipt.
A parameter tweak is not reconsideration. Stop dependent work until reviewed
resolution; independent authorized work may continue.

## FINAL: execute and verify honestly

Run tools/qa_gate.py RECEIPT --verify-files --stage FACE, DETAIL, then FINAL;
retain checkpoint results. Current state cannot prove past execution order.
The [schema specification](../../../docs/qa-receipt.md) defines exact workflow
and escalation fields and reuse of PASS0/Model Contract/transfer validators.
Record DISCOVERED → READ → SELECTED → EXECUTED → VERIFIED, or SKIPPED/BLOCKED.
Reading/hashing Markdown and tool availability are not procedure execution.
Require actual artifacts, accepted identity/occlusion/seam/binding observations
and final fixed-view coverage. Visible seams or identity drift are FAIL.
Checkers validate declarations; inspect real images and test production separately.
