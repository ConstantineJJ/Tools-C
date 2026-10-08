# Dual Verification v1

This is a mode of [Verification](../SKILL.md) using the existing
[QA receipt](../../../docs/qa-receipt.md), snapshots, PASS0/Model Contract and
task checkpoints. No new Skill, design authority, service or image repository.

## Procedure and ownership

Record technical geometry/topology, UV/material/texture, file integrity and
contract checks as named receipt checks. Select their names in technical_checks;
the checker reports that exact scope separately as TECHNICAL_QA PASS/OPEN/FAIL.
Configure applicable checks from the user/task, never omit a failed criterion to
improve the verdict. Artistic review judges canonical likeness, primary forms,
silhouette/proportions, face/hair/design details and visual artifacts. Neither
result implies the other; all existing receipt gates still apply.

Select complexity before modeling: SIMPLE → FINAL; STANDARD → PRIMARY_FORMS,
FINAL; COMPLEX → PRIMARY_FORMS, CRITICAL_FEATURES, FINAL. PRIMARY_FORMS precedes
mass detailing; review silhouette, head/shoulders/torso/pelvis and reference-led
volumes. CRITICAL_FEATURES covers face/hair/characteristic costume for characters,
body/cabin/wheels for vehicles, architecture/composition/scale for environments.
FINAL reviews the finished scoped appearance. Full stages use standard views;
local iterations use LOCAL and cover changed regions and affected protected
regions. Local approval cannot replace final delivery. An early artistic gate
can pass while the broader receipt remains OPEN for unfinished final work.

## Freshness MVP

Add dual_verification v1 inside an existing v1/v2/v3 receipt. Keep original
capture.json and snapshot files immutable. Dynamic assessment is returned by
the same checker. Use existing image paths/hashes; never create another store.

freshness has exactly states, current, captures. states maps task-local state IDs
to {revision,snapshot,regions,verified}. revision is a nonnegative monotonic scene
journal revision; snapshot is the existing {path,sha256} JSON artifact; regions
maps named reviewed regions to explicit object-name lists in that snapshot.
The checker hashes actual snapshot rows, frame/fps and data-category coverage.
Different revisions can share unchanged region fingerprints. Matching timestamps
or revision numbers alone cannot establish currency.

verified=true is an operator's attestation of a synchronous state probe with
adequate scope, not automatic surveillance. Use the existing snapshot function
with the affected geometry and appropriate material_graphs, curves, modifiers,
UV/normal/weight/shape-key categories. Do not certify appearance from geometry
alone. External image pixels, lighting, visibility, evaluated modifiers and
other omitted scene dependencies need separate coverage/verification; mark
verified=false when coverage or live state is uncertain. An uncontrolled edit
invalidates the current probe. Reprobe the latest scoped state before review;
do not mark it verified from yesterday's saved file or an old receipt.

Each captures binding has exactly id,capture_series,captured_at,state,dependencies.
id refers to an existing capture/closeup. captured_at is actual timezone-aware
ISO capture time from the journal (old unknown times are not invented). state
points to a snapshot state. dependencies maps checked/visible regions to other
regions affecting their visibility/reading; [] means explicitly no such
dependencies, null means unknown. Include occluders such as hair → face.
One series can contain many views and several revisions. Probe before/after a
capture batch and confirm matching scoped state; if interrupted by edits, split
the state bindings instead of assigning one revision to all views.

The assessment returns per-region CURRENT, STALE (changed region), PARTIAL
(changed visibility dependency), UNKNOWN (unverified/missing state, unknown
dependencies, conflicting same-revision fingerprints or invalid file). Mixed
current/stale regions give overall PARTIAL. UNKNOWN never becomes CURRENT.
PNG verification checks contained paths/hash, signature, chunk CRC and bounded
decoded scanlines; supported capture PNGs are noninterlaced up to 4096 pixels
per side/64 MiB. This does not inspect artistic content. Freshness does not prove
sufficiency: a current FRONT cannot establish the back of the head.

brief.requirements maps region to {views,criterion}; use named fixed views or
closeup. Include the actual required views of each region, not a favorable subset.
Full PRIMARY_FORMS/CRITICAL_FEATURES needs front, side, three_quarter coverage;
full FINAL also needs back, high_45, low_45. Current suitable AFTER evidence is
reused. Missing/stale/unknown evidence requests a capture; available but unopened
evidence requests INSPECT_EXISTING. The critic must actually open the images.

## Blind critic dispatch

Run `python tools/qa_gate.py TASK/qa_receipt.json --verify-files --critic-packet`.
The stdout packet is an allowlist: canonical images, design/contract locks,
user constraints, protected and previously accepted region names, stage criteria,
objective captures and recomputed freshness/sufficiency. It excludes implementer
review text, artistic verdicts, excuses and chat history. Hash binds its content.
Paths are relative to TASK; tell the critic that root when dispatching.

Use one independent read-only subagent for the batch when available, with no
inherited modeling history. Give the complete packet and instructions to inspect
its canonical reference and objective standard views; no asset edits or Model
Contract changes. Record the actual returned agent/dispatch ID. A human review is
also acceptable when identified truthfully. SELF_REVIEW must name the implementer
and cannot carry an independent dispatch receipt. Do not simulate independence by
changing a reviewer label. Compare with implementer conclusions only after the
initial independent verdict. After that verdict, compare compact checkpoint
defects/deltas; do not prime the initial critique with previous failure narratives.

INDEPENDENT dispatch artifact is an existing task evidence JSON with exactly
{implementer,critic,dispatch_id,packet_sha256,blind:true}. Checker verifies files,
different identities and binding, reports INDEPENDENT_DECLARED. It cannot prove
tool invocation, isolation or honesty; actual dispatch is an agent responsibility.
The CLI builds packets and validates returns; it does not launch agents or vision.

## Reference-bounded delta

Critic may return NO SIGNIFICANT ISSUES / zero issues. Do not invent percentages,
request extra realism/detail/symmetry or redesign intentional stylization. Use
canonical references and locked constraints; high/low 45 diagnose volume/contact,
not skull or limb length. PROPORTION issues need inspected orthographic front AND
side confirmation. MISSING issues require unobstructed VISIBLE evidence; hidden
features request investigation rather than reconstruction as an asserted defect.

Return at most five issues, prioritizing P0 critical, P1 visible deviation, P2
optional polish while accounting for regression risk. Each issue records exactly
id,priority,what,where,why,evidence,reference,fix,kind,visibility,impact,fix_cost,
regression_risk,rationale. where is a review region; evidence is inspected capture
IDs whose region is CURRENT; reference is a canonical source ID. kind is
PROPORTION/FORM/CONTACT/SURFACE/MISSING, visibility VISIBLE/PARTIAL/OCCLUDED.
IMPACT/FIX_COST/REGRESSION_RISK use LOW/MEDIUM/HIGH with a brief approximate rationale.

artistic has exactly stage,verdict,mode,reviewer,packet_sha256,dispatch,inspected,
issues,delta,preserve,leave_as_is,do_not_change,next,observations. verdict is
ACCEPTED (zero issues), ACCEPTED_WITH_MINOR_DIFFERENCES (only LOW/P2),
REVISION_REQUIRED (confirmed defect) or ESCALATE. mode SELF_REVIEW/INDEPENDENT.
Use preserve/leave_as_is for accepted regions and do_not_change for all locks;
next is a compact action list. Unrun artistic review is null, never ACCEPTED.

delta rows have {id,status,evidence}: RESOLVED, IMPROVED, UNRESOLVED or
NEW_REGRESSION. All preceding outstanding issues must be accounted for. Changes
in resolution/improvement need new region evidence; a new defect in an accepted
region needs a new image hash and explicit NEW_REGRESSION. Accepted does not mean
immune to demonstrated later defects. Explicit protected locks require escalation,
not an automatic asset-edit authorization. Critic never edits identity or contract.

## Checkpoints and corrections

checkpoint has artifact,issues,accepted,protected,failed_methods,gates. First
review: artifact=null, issues=[], accepted={}, protected=declared regions,
failed_methods=[], gates={}. Subsequent reviews point artifact to the preceding
existing QA receipt; derive the compact state with checkpoint_from_receipt() in
[qa_artistic.py](../../../tools/qa_artistic.py), passing root and the existing
artifact verifier. It rechecks the preceding review and copies only supported
state. Do not manually erase defects, accepted regions or failed methods. Reuse
immutable relative images/checkpoints instead of copying an entire image history.

issues are {id,region,evidence:[PNG hashes]}; accepted maps region to approved
image hashes. gates records completed stage verdict, contract_ref, evidence IDs,
reviewer and packet_sha256. A declared ACCEPTED with incomplete review is OPEN and
cannot close a later prerequisite through a checkpoint. Corrections are retained
as an immutable prefix, including resolved issues. Checkpoint chains are bounded
to 16 receipts; longer projects explicitly archive/rebaseline verified scope.

corrections is up to three contiguous batches, each with pass,method,outcomes,
checkpoint,evidence. checkpoint is a verified saved .blend; evidence contains
inspected AFTER IDs for every affected region. outcomes maps issue ID to
RESOLVED/IMPROVED/UNRESOLVED. Improvement/resolution needs new evidence for that
specific region versus its prior issue/pass; another region's new PNG cannot
reset failures. The latest claimed result must agree with critic delta and current
AFTER region state. Earlier captures can be historical after later passes.

After two UNRESOLVED outcomes by the same method: RECONSIDER_METHOD, including
minor-difference polishing. Do not repeat that method automatically; a changed
method can justify the third batch. Significant demonstrated improvement permits
another bounded pass. Three unresolved passes: ESCALATE, never auto-PASS. The
executor checks feedback against Model Contract, selects bounded changes, preserves
approved areas, captures required AFTER views, rechecks freshness and dispatches
scoped review. Method choice and model edits remain agent actions.

user_decision is PENDING/FINISH/POLISH. ACCEPTED_WITH_MINOR_DIFFERENCES stays OPEN
for PENDING; the user chooses finishing or further bounded polishing. Never lower
the canonical standard because attempts ran out. Automated transitions enforce
the declared evidence/limits; genuine likeness, defect severity, visibility,
cost/risk and region dependency judgments require visual review.

## Execute and practical validation

`python tools/qa_gate.py TASK/qa_receipt.json --verify-files --mode ARTISTIC_REVIEW`
returns separate TECHNICAL_QA and ARTISTIC_REVIEW plus artistic_gate, next,
freshness, requests, delta and packet hash. Existing broader evidence gate is
preserved. Neither can bypass a failure in the other. Keep visual=NOT_EVALUATED
for this checker even when all declared gates pass.

Use [the separate blind experiment](../../../docs/dual-verification-blind-review.md)
to evaluate real critic behavior and false positives. Regression fixtures prove
state transitions and metadata policy, never character likeness or artistic skill.
