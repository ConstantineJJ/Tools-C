# Tools_C Dual Verification v1 — 2026-10-08

Scope authorized by the user's «Реализовывай!» after the supplied specification.
Canonical root: E:/MyCreations/Tools_C; branch main; starting HEAD
f0bb426d9dec7bb63f20e80b87265e2b2493e138. Existing uncommitted work, including
the preceding Character Pipeline audit and 76 missing historical report files,
was treated as the baseline. No commit, release or asset mutation.

## ARCHITECTURE

The existing [Verification Skill](../skills/verification/SKILL.md) gains
ARTISTIC_REVIEW through the existing [QA receipt](../docs/qa-receipt.md).
Optional dual_verification v1 extends receipt schemas 1/2/3; older receipts retain
their original output and semantics. ASSET_FINAL provides standard review coverage
for vehicles/environments/other assets without character-specific workflow.

[qa_freshness.py](../tools/qa_freshness.py) and
[qa_artistic.py](../tools/qa_artistic.py) are bounded helper modules called by
[qa_gate.py](../tools/qa_gate.py), not independent contract systems/services.
PASS0/Model Contract remains the single design authority; canonical references
must match its source_of_truth and file hashes. Existing workflow, delivery,
protected-zone and capability gates remain enforced.

Results separately record TECHNICAL_QA for the explicitly listed technical_scope,
ARTISTIC_REVIEW, artistic_gate, evidence_gate, freshness, requests, delta and next.
Technical PASS / artistic REVISION_REQUIRED and artistic ACCEPTED / technical FAIL
both block overall acceptance. visual remains NOT_EVALUATED even when declared
evidence gates pass. Full quality cannot be inferred from a subset of named checks.

## FRESHNESS MVP

Implemented and tested before artistic integration: actual snapshot row hashes,
explicit region/object membership, revision and verified-probe journal bindings,
visibility dependencies and CURRENT/PARTIAL/STALE/UNKNOWN assessments. Original
capture metadata/snapshots are not rewritten. Multiple captures can share a series
while referring to different revisions. No additional image storage/tracking hooks.

Hair change makes hair STALE, dependent face PARTIAL, unaffected torso/legs CURRENT.
Unknown dependencies/state, uncontrolled edits, missing files, conflicting same
revision fingerprints and failed hashes never produce CURRENT. Image checks verify
contained paths, SHA-256, PNG signature, chunk CRC and bounded decoded scanlines.
Timestamp alone cannot establish freshness. Current unsuitable angles remain
insufficient; existing suitable images are reused rather than recaptured.

Limits: verified is an operator's synchronous-probe/coverage attestation. The
checker cannot detect later live changes or omitted appearance dependencies. The
existing snapshot covers explicit source representation/categories, not every
evaluated Blender property, external texture pixel, visibility or lighting change.
Uncontrolled or incomplete state must be marked unverified until adequately probed.
PNG support is bounded noninterlaced capture PNG, up to 4096 pixels per side/64 MiB;
file integrity does not establish which visual region the pixels actually depict.

## ARTISTIC REVIEW

`--verify-files --critic-packet` builds a hash-bound objective packet; it never
dispatches an agent. `--mode ARTISTIC_REVIEW` validates the returned review against
that packet and recomputed evidence. English/Russian explicit artistic requests
route to read-only verification and deliver the complete canonical protocol.

Critic may return zero issues. Up to five issues include WHAT/WHERE/WHY/EVIDENCE/FIX,
priority, approximate impact/cost/risk and rationale. Issues must cite canonical
reference plus inspected CURRENT region evidence. Proportion allegations require
orthographic front AND side; high/low 45 alone is rejected. Occluded/partial
features cannot be asserted absent. Protected areas require escalation, not edit
authorization. Minor verdicts cannot hide a P0/P1 or medium/high-impact defect.

Real likeness, significant defect judgment, intentional styling, region visibility
and approximate costs/risks remain actual human/AI visual judgments. No image
scoring or automatic similarity estimate was implemented or claimed.

## CRITIC INDEPENDENCE

The initial packet excludes implementer artistic observations, verdicts and
justifications. It includes design locks, user constraints, standard objective
captures and approved region names. Different reviewer identity plus an actual
bound dispatch receipt is required for INDEPENDENT_DECLARED; same-agent review is
explicit SELF_REVIEW. A new display name alone cannot establish independence.
The checker cannot independently attest dispatch, isolation, inspection or honesty.

A separate read-only subagent actually reviewed this implementation's code without
editing files. Five reproduced issues were corrected: minor polishing bypassed
method reconsideration; accepted regions were absent from preservation packets;
checkpoint memory/failures were unbound; correction evidence could describe the
wrong region; unopened existing views triggered new captures. Follow-up tests fixed
resolved-issue handoff and OPEN stage promotion. Final independent technical review
reported no remaining blockers and 148 scoped tests PASS. This is technical review,
not an independent artistic judgment of AgentBlue2 or the control asset.

## ADAPTIVE GATES

Executable selection: SIMPLE FINAL; STANDARD PRIMARY_FORMS + FINAL; COMPLEX adds
CRITICAL_FEATURES; LOCAL reviews changed scope/affected protected regions. Standard
view coverage cannot be replaced by a favorable single angle. Earlier full stage
receipts are required for later full-stage acceptance. Incomplete/uninspected
ACCEPTED declarations remain OPEN and cannot close prerequisites at handoff.

Invocation timing, complexity choice and actually pausing before mass detailing
remain agent production actions; this implementation validates their recorded
state rather than intercepting Blender edits. Character FACE/DETAIL/FINAL workflow
is retained separately; early artistic readiness does not imply final delivery.

## DELTA TRACKING

checkpoint_from_receipt derives compact defects, approved regions/hashes,
protected zones, failed methods and completed gates from the preceding existing QA
receipt. The source receipt is file/hash bound and rechecked; inline memory cannot
erase available historical state. Corrections remain an immutable prefix. Resolved
issues do not reappear as required corrections merely because another receipt was
created. Critic receives approved region names without previous failure narratives;
after the initial verdict, compact defect delta is compared.

RESOLVED/IMPROVED/UNRESOLVED/NEW_REGRESSION are checked against outstanding IDs and
current inspected evidence. Accepted-region correction needs new evidence/hash
and explicit NEW_REGRESSION. Snapshot state, not timestamp, determines currency.
Receipt ancestry is bounded to 16 preceding links; longer tasks require an explicit
verified rebaseline. No chat-history archive or per-element critic service.

## CORRECTION LOOP

Contiguous maximum-three correction batches reference actual saved .blend
checkpoints and inspected AFTER evidence for each affected region. Improvement or
resolution requires new image hashes for that particular region versus its prior
issue/pass; an unrelated new torso PNG cannot establish improved hair. Latest
claimed improvement/resolution must agree with critic delta and current region
evidence; historical captures can become stale after subsequent changes.

Two same-method UNRESOLVED outcomes produce RECONSIDER_METHOD, including optional
polish. The failed method cannot be repeated after handoff. Demonstrated improvement
can permit a further bounded pass; three unresolved passes escalate, never auto-PASS.
ACCEPTED_WITH_MINOR_DIFFERENCES waits for user FINISH/POLISH. Fix selection, strategy
change, actual mesh/material edits and capture execution remain agent responsibilities.

## TEST RESULTS

- Freshness MVP: **17 tests PASS** before artistic integration; legacy QA: 19 PASS.
- Dual Verification: **50 tests PASS**, including real byte/hash PNG fixtures,
  technical/artistic split, adaptive gates, unchanged contract/data, protected and
  accepted areas, false independence, insufficiency vs unopened captures,
  reference bounds, checkpoint chains, failed methods, three-pass limit, zero
  issues, legacy compatibility and other asset types.
- Anime context regression found during the first full run (324 PASS / 1 FAIL):
  the expanded Verification entrypoint exceeded the default context budget.
  Corrected by keeping the entrypoint compact and detailed protocol in the review
  route. The unchanged default budget now delivers every required anime document;
  its 11 focused tests PASS. No failing test/required document was weakened.
- Final full regression: **325 tests PASS**, 185.012 s, exit 0, no failures,
  errors or skips. This follows the budget fix; the earlier failed runs are
  retained as diagnostics, not reported as passing validation.
- Tools_C L1: **50 PASS / 0 WARN / 0 FAIL**; Blender-MCP-Co L1:
  **9 PASS / 0 WARN / 0 FAIL**. Existing file/link guards include the new modules,
  tests and owning protocol; no new catalog owner or universal contract schema.
- Both generated router locations synchronized through sync_blender.py, nine aliases
  per location. Live MCP at default 60000 returns ARTISTIC_REVIEW, verification as
  sole owner, five whole canonical documents and zero missing documents.
  Their source hashes match local normalized UTF-8; loaded/disk MCP server hashes
  match, 17 tools, restart_required=false. Server/add-on code was unchanged.
- Actual legacy AgentBlue2 Old_version schema-2 receipt still returns **OPEN**,
  workflow NOT_RECORDED_LEGACY and visual NOT_EVALUATED: facial/hair likeness is
  escalated; contacts and STATIC_VISUAL remain WARN. No automatic upgrade of old art.
- Read-only live Blender scene probe succeeds: Scene/frame 1, Camera and Light only.
  Asset practical review, correction geometry, export and target runtime: **NOT_RUN**.
  L1 checker correctly labels engine/runtime/visual levels SKIP.

Tests evaluate declared protocol decisions, not artistic quality. Synthetic PNGs
and saved-checkpoint bytes in unit fixtures are never claimed as modeled assets or
valid engine-opened .blend files. The real old receipt is compatibility evidence.

## PERFORMANCE IMPACT

Measured locally, 20 iterations with six actual noninterlaced 512×512 RGBA PNGs
(uniform pixels), four small synthetic region rows and no receipt ancestry:
legacy file gate median **2.331 ms** (max 2.678), freshness **5.778 ms** (max 7.332),
dual file gate **9.608 ms** (max 10.757). This measures metadata/file decoding;
production mesh size, texture entropy, render duration and AI review are excluded.
The independent reviewer also measured small ancestry fixtures: 1 receipt 0.009 s,
3 receipts 0.037 s, 8 receipts 0.097 s, 17 receipts 0.208 s; bound rejection checked.

There are no extra render calls in the checker, no stored image copies, no critic
process service and no per-element agent. Reuse is executable through sufficiency
and INSPECT_EXISTING decisions. Avoided renders, artistic time saved and production
ROI were not measured. Ancestry revalidation costs file reads; the explicit bound
prevents unlimited growth. Large real assets require the separate experiment.

## KNOWN LIMITATIONS

Technically automated: scoped fingerprint/file integrity, freshness/sufficiency,
blind packet construction, declared independent/self identity binding, gate/delta
validation, checkpoint consistency and bounded correction transitions.

Agent instructions: synchronous snapshot/capture journal, adequate dependency
coverage, choosing task complexity, actual critic dispatch with no inherited
history, batch image inspection, checkpoint persistence, feedback comparison,
bounded edits and before-detail gate timing. Tooling does not claim to automate
unsupported environment isolation or model execution.

Visual decisions: canonical likeness/severity, actual presence/occlusion, intentional
asymmetry/style, successful material finish, relevance of proposed fixes and real
regressions. JSON/hashes cannot establish them. The user's minor-difference choice
is recorded, not cryptographically proven. Old receipts remain supported but do
not retroactively prove dual review. A no-PASS bound is preferable to inventing art.

## NEXT EXPERIMENT

[Blind experiment instructions](../docs/dual-verification-blind-review.md) are
prepared for three previous AgentBlue2 versions plus one previously user-approved
control, randomized as A/B/C/D. Hide order, AI/model names and prior opinions;
inspect comparable current views, freeze independent verdicts, then adjudicate
confirmed defects/false positives, accepted regions and priorities against the
canonical reference. Coordinator must verify the actual control approval and
conceal identifying filenames/metadata without altering the locked contract.

**PLANNED / NOT_RUN**: no four candidates were rendered or artistically reviewed
in this implementation task; no false-positive or likeness result is claimed.

Evidence: [machine receipt](dual-verification-v1-2026-10-08.json). User-owned dirty
work and missing historical files remain preserved; Git index untouched. No
server/launcher/add-on code, original capture metadata or production assets changed.
