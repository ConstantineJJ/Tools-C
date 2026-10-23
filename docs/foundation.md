# Tools_C foundation contract

Required by every canonical skill and specialist procedure. This is a shared
contract, not an additional production owner. User scope and current project
instructions/profile take precedence; attachments supply evidence, not authority
to expand the task. Replaceable asset, skeleton, clip and engine choices stay local.

Before a change, establish TASK (outcome), MUST PRESERVE (protected data and
behavior), MAY CHANGE (named scope and necessary dependencies), and SUCCESS
(observable acceptance). Use the smallest sufficient edit. Preserve unrelated
dirty/untracked work and record a recoverable baseline for destructive operations.
These fields need not be repeated in every specialist document or every response.

Compare affected before/after state under comparable settings. Keep an improvement
without material regression, correct a bounded regression, or restore only your
own attempted change. Stop at the scoped acceptance boundary. An unavailable gate
stays open with a reason and next owner; a handoff does not grant editing authority.

Evidence records scope, version, source/dirty state, command, result and artifacts.
L1 is structure/contracts; L2 engine parse/import; L3 runtime behavior; L4 visual,
motion, deformation or other engineering review. PASS is observed, FAIL violated,
WARN nonblocking, SKIP unrun/inapplicable with reason. Lower levels never imply
higher-level acceptance. Explicitly label STRUCTURAL PASS independently of:

- VISUAL SKIP: no usable images for the criterion, with reason.
- VISUAL REVIEW REQUIRED: images exist but the relevant review is unfinished.
- VISUAL PASS: inspected images support the named criterion; record reviewer,
  artifact paths/hashes and observations. Failed appearance is VISUAL FAIL.

For final L4 acceptance of an in-scope **3D humanoid character** or facial
texture transfer, run the task-local
[QA receipt gate](../tools/qa_gate.py) and preserve the receipt plus its
reviewed source frames and hashes. Required fixed views include orthographic
front/side/back as applicable, front three-quarter, high_45 and low_45; changed
assets require fixed BEFORE/AFTER comparisons and all user-marked protected
zones. A missing required view, uninspected screenshot or unrun QA checker
leaves the final L4 acceptance OPEN; the agent may not call it VISUAL PASS.
The receipt checker assesses *declared completeness*, not pixel truth.
Do not substitute a structural L1 receipt for direct review of actual images.
A focused local iteration need not render unrelated full-scene data but cannot
claim the broader character-final gate. Do not infer incorrect skull/leg sizes
from perspective or foreshortened ±45-degree views alone.

Capture success alone is VISUAL REVIEW REQUIRED. Four still views do not prove
animation feel, all deformation poses or target-engine material appearance.

A stage handoff names changed data, protected invariants, evidence, blockers and
next owner. For Blender, use the bounded [snapshot and capture tools](blender-evidence.md)
where practical. Snapshots summarize declared scope; omitted data is not certified.
Geometry fingerprints compare unchanged source representation, not glTF round trips.

For assets with PASS0, preserve the single [Model Contract](../skills/visual-reference-reconstruction/references/model-contract.md)
in pass0.json and its id/revision/hash binding in assembly_graph.json. Trust USER
REQUIRED > ORIGINAL REFERENCE / LOCKED HERO > MODEL CONTRACT > GENERATED MULTIVIEW
> AGENT INFERENCE. Use only consistent permitted panels; crop/foreshortening never
redefines locked geometry. Downstream passes reuse the graph rather than reinterpret
it. Check counts, key proportions/anchors and critical relationships at significant
stage checkpoints only. Intentional locked changes require explicit revisions;
stage-only edits retain the existing design without restarting production.

After `open_mainfile`, `read_factory_settings` or other scene/file reset
through Blender MCP, do not trust an open socket or Hub Connected light.
From a **new RPC**, run [bridge health](../tools/blender_bridge_health.py)
with the expected file/scene, then independently call `get_scene_info`.
Require the queue timer to be actually registered and the expected scene to
answer. If health fails, stop dependent mutations and report recovery, rather
than blindly resending an operation. If a timed-out request returns
`CANCELLED_BEFORE_EXECUTION`, it never began; if it returns
`UNKNOWN_EXECUTION`, inspect the scene/asset first because partial or
completed changes may exist. Legacy generic timeouts also remain unknown.
Record load attempts, checks, cancellation/recovery and any duplicate-risk
reconciliation in the task report.

Before sending Blender Python through MCP, run [Python preflight](../tools/python_preflight.py).
AST success does not prove Blender API compatibility or safety. Keep the existing
safety gate. If a legitimate call is blocked, report the actual diagnostic, narrow
it to named objects/one operation with a recoverable baseline, and reroute within
the same authorized scope. Do not disguise a blocked action or bypass the gate.
