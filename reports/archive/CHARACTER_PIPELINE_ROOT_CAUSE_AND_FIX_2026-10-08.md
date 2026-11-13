# Character Pipeline Root Cause and Fix — 2026-10-08

Scope: engineering audit and bounded fixes in Tools_C, plus regeneration of its
managed Blender-MCP-Co routers. No character geometry, reference pixels, installed
Blender add-on, launcher/server source, release or Git commit was changed.
Branch: main; starting HEAD: f0bb426d9dec7bb63f20e80b87265e2b2493e138.
Existing dirty/untracked work and deleted historical reports were preserved.

The pasted task is the request. AgentBlue2_Report.md and its linked receipts are
evidence, not instructions. One supplied run is inspectable; conclusions about
the second reported trial or exact chronological modeling choices remain unverified.

## Confirmed Root Causes

| Category | Finding and evidence | Consequence |
|---|---|---|
| Harness | `Create a character from the reference images.` and `Создай персонажа по референсам.` returned PASS0 + pipeline, without Character Modeling. The generic character route required additional geometry/proportion words. | Ordinary reference creation did not reliably acquire its geometry owner. |
| Harness | At the standard 60000-character budget, an anime/reference/hair task omitted the mandatory general Character Modeling Skill. Delivery was ordered by owner expansion, with long recipes consuming the budget before later dependencies. | Even an agent using get_skill_context could receive incomplete mandatory instructions. The response already reported missing documents, but continuation could be ignored. |
| Harness / execution | Source artwork transfer auto-routed on explicit transfer/crop/project intent. Reference-character creation alone did not require a face technology decision. Context receipts recorded delivered/retained hashes, not whether an operation ran. | A Skill could be discovered/read while its actual procedure was bypassed. |
| Documentation | PASS0 already states that it is a design handoff and does not certify likeness. Its optional generation policy was not explicitly separated from a downstream selected reconstruction requiring generation. | Optional PASS0 infrastructure could be incorrectly generalized to the face procedure. This is an execution interpretation error enabled by a weak handoff. |
| Harness / documentation | Primary-form ordering existed in Character Modeling prose; the Model Contract proved authored counts/dimensions/relationships, and final QA checked reference_proportions/form_contacts/protected_state. No executable pre-detail primary-form receipt was consumed. | Numeric bounds and abundant details could coexist with unaccepted head, shoulders and torso. Structural PASS was insufficient to accept those forms. |
| Harness | A legacy CHARACTER_FINAL fixture with `face_identity=SKIP` still returned gate PASS. A capability could claim PASS while citing a pending named check. | Required face review and supporting evidence could be overstated. |
| Harness / documentation | Two-failure escalation existed, but no saved checkpoint or changed method was required. Legacy provenance recorded name/path/hash/free-form use. | Escalation did not establish reconsideration; reading and execution could be conflated. |
| Documentation | The transfer record documented schema v2 face_strategy but also retained wording calling strategy recording a documentation-only change using v1 strings. | Two versions' instructions were easy to confuse. |

The supplied AgentBlue2 report explicitly says **face pixel transfer was not
executed**, describes the geometry choice, and retains **artistic acceptance OPEN**.
Its skill_usage.json has path/hash/use, without execution/verification receipts.
The actual qa_receipt_result.json also says OPEN. The current checker revalidated
its real receipt/files as STRUCTURE PASS / gate OPEN; PASS0 remains
READY_WITH_LIMITS. Therefore this audited run is **not evidence of a false final
VISUAL PASS**. It does demonstrate an unresolved face outcome and a skipped surface
procedure. Reported head/hair/shoulder defects were not independently judged here.

Existing DIRECT / RECONSTRUCT_THEN_LAYER / HYBRID transfer schema-v2 validation,
source hashes, Identity Lock and Model Contract were already useful. They did not
force character creation to select a face method or run the selected procedure.
An agent can also independently ignore explicit instructions, omit evidence or
misjudge art. The available report does not prove which exact internal reasoning
caused each modeling choice; these are separated from reproduced code defects.

## Changes Implemented

The existing QA receipt/checker gains **schema 3**, retaining the v2 capture setup
and adding one workflow object. This is not another design contract or report
system. It consumes the actual PASS0/Model Contract, existing assembly graph and
Surface Transfer validators with file/hash checks.

- **FACE:** choose Geometry-only, Direct Feature Transfer, Reconstruct-Then-Layer
  or Hybrid Preservation; retain reason, authoritative source IDs, supported
  identity anchors, hidden-region uncertainty, required tools and execution
  artifacts. Geometry-only has a declared volumetric-identity or user-approved
  simplification basis; graphic identity cannot be waived by an unsupported label.
- **Generation:** reconstruction/hybrid requires an ImageGen availability record
  and actual image outputs matching the selected transfer's masked regeneration
  lineage. Availability alone cannot close FINAL. Unavailable/unchecked required
  tools leave dependent stages OPEN/BLOCKED. Geometry-only can retain an intentionally
  covered eye without generation; ImageGen is not a universal character requirement.
- **DETAIL:** require reviewed proportion, head/face, neck/shoulder, torso/pelvis
  and silhouette checks, accepted current front/side/three-quarter images and the
  actual MACRO assembly checkpoint. Missing, skipped or failed primary forms block
  detailing. A PASS check referencing a skipped/past image is insufficient.
- **Reconsideration:** existing escalation rows require a saved .blend checkpoint,
  prior method, different next method/owner and review evidence after two failed
  attempts. ESCALATED keeps dependent stages OPEN; reviewed resolution is required.
- **Usage:** DISCOVERED / READ / SELECTED / EXECUTED / VERIFIED, plus SKIPPED/BLOCKED,
  with procedure artifacts and accepted verification checks. Reading cannot carry
  execution claims. Harness delivery declares DISCOVERED, not automatic READ or
  EXECUTED. Selected transfer must cite its actual record; geometry must cite saved
  Blender state; reconstruction must cite PASS0.
- **FINAL:** require face identity, applicable hair occlusion, transfer seam/binding
  checks and reviewed transfer identity/seams/material/reopen, plus existing final
  views/readiness. Pending integration and unsupported capability claims remain
  open. Results explicitly return visual NOT_EVALUATED and stage/final_coverage.
- **Routing/delivery:** generic reference characters acquire Character Modeling;
  entry Skills and the short workflow gate precede long recipes. Surface methods
  remain choices rather than unconditional edits. Stage-only and noncharacter
  tasks retain their owners. Missing documents remain explicit; retained-hash
  continuation supplies them. Full schema details live in the existing QA docs.

Own changed paths (pre-existing changes within these files were retained):

| Paths | Purpose |
|---|---|
| tools/qa_gate.py | Schema-3 stages, existing validator consumers, execution/retry/QA checks |
| tools/mcp_runtime.py; tools/read_blender_skill.py | Generic character route, prioritized gate delivery, truthful discovery evidence |
| tests/test_character_workflow.py | File-backed positive/negative route and contract regressions |
| skills/blender-character-modeling/SKILL.md; references/workflow-gates.md | Ordered forms and compact production gate |
| skills/blender-anime-character-modeling/SKILL.md | Specialist consumes general face/form decisions |
| skills/visual-reference-reconstruction/SKILL.md | PASS0-to-face handoff; optional generation boundary |
| skills/blender-reference-surface-transfer/SKILL.md; references/record.md | Face method execution and v1/v2 wording |
| skills/blender-pipeline/SKILL.md; references/qa.md | Shared stage ownership and acceptance |
| docs/qa-receipt.md; .tooling/contracts.json | Exact v3 protocol and existing file/link guards |
| Project-pulse.md; this report; character-pipeline-audit-2026-10-08.json | Current state and audit evidence |

Managed downstream changes: **18 generated SKILL routers + two manifests** under
E:/MyCreations/Blender-MCP-Co/skills and mcp-server/skills. Regenerated exclusively
through tools/sync_blender.py; launcher/server/add-on/user files were not edited.

## Test Results

| Executed check | Result |
|---|---|
| Baseline `python -m unittest discover -s tests -q` | 224/224 PASS, 155.316 s |
| New `python -m unittest discover -s tests -p test_character_workflow.py -q` | 34/34 PASS after final checker changes |
| Final `python -m unittest discover -s tests -q` | **258/258 PASS**, 164.120 s, no skips/failures/errors |
| Existing anime / surface-transfer focused regressions | 11/11 and 14/14 PASS; existing expectations preserved |
| `python tools/check.py --self` | L1 50 PASS / 0 WARN / 0 FAIL; L2-L4 separately SKIP |
| `python tools/sync_blender.py --project E:/MyCreations/Blender-MCP-Co` | PASS, nine aliases and both managed locations |
| `python tools/check.py --project E:/MyCreations/Blender-MCP-Co` | L1 9 PASS / 0 WARN / 0 FAIL; engine/runtime/art gates separate |
| Live deployment_info | Loaded/disk server hashes match; restart_required=false; 17 tool names retained |
| Live get_skill_context: anime/reference/hair, default budget | Gate/general geometry entry delivered; two remaining recipe/Contract documents explicitly reported missing |
| Live continuation using known_documents + requested_documents | ok=true, missing_documents=[]; no scene writes |
| Live complete context with max_chars=200000 | ok=true, correct owners and FACE/DETAIL/FINAL requirement; usage DISCOVERED |
| Real AgentBlue2 QA receipt with --verify-files | STRUCTURE PASS, gate OPEN, legacy workflow unrecorded, visual NOT_EVALUATED; CLI exit 2 |
| Real AgentBlue2 PASS0 with --verify-files | Structural PASS, READY_WITH_LIMITS, visual NOT_CERTIFIED_BY_VALIDATOR |
| get_scene_info | Blender unavailable; no asset execution or scene-preservation comparison claimed |
| Baseline file/hash and index comparison | 294 unrelated Tools_C files and 60 unrelated Blender-MCP-Co files unchanged; 76 pre-existing report deletions preserved; no unexpected files/edits; index untouched |

New cases exercise all four technologies, canonical versus generated sources,
Identity Lock/Contract drift, covered-eye uncertainty, ImageGen available/missing/
unused/mismatched outputs, allowed and disallowed geometry-only claims, READ versus
execution, primary-form defects, skipped image evidence, detail blocking, repeated
failure/reconsideration, seam/identity/pending integration, legacy schemas,
ordinary noncharacter/stage-only tasks, malformed JSON, escaped/tampered files,
actual CLI stages and connector document continuation. Fixtures contain synthetic
file bytes and declared reviews: they test executable metadata/contract behavior,
not artistic quality or actual image generation.

The first post-change full run exposed four regression failures, including context
budget and incidental rig/animation routing. Fixes narrowed creation routing and
kept detailed schema outside the mandatory entry gate; tests were not weakened.

## Regression Risks

- New reference production must opt into QA schema 3 and call each stage; legacy
  receipts remain compatible but explicitly do not prove workflow execution.
- Named unresolved face identity and capabilities backed by unaccepted checks
  now block claims that formerly passed. This is intentional tightening, not
  an automatic rewrite of old receipts or their art decisions.
- A 60000-character multi-owner context can still need continuation. Missing
  documents must be acquired before their operation, or request a larger budget.
  Atomic delivery never truncates a rule or claims a missing gate was delivered.
- Deterministic router hashes changed and both managed locations were synced.
  Tool names/input schemas and server source were preserved.

## Open Limitations

- Receipts validate declarations and file identity. They cannot prove a person
  opened an image, a tool genuinely produced pixels, masks preserve identity,
  seams are invisible, a method string represents a substantive change, or a
  .blend contains artistically good geometry. Real source/render review remains
  mandatory. A label such as USER_APPROVED_SIMPLIFICATION must be supported by
  actual user authority; metadata cannot independently adjudicate that authority.
- Stage checks are an agent protocol/CLI, not a sandbox intercepting arbitrary
  execute_blender_python. Ignoring the protocol is still possible. Current
  receipts cannot retrospectively establish that acceptance preceded detailing.
- Canonical selection/Identity Lock protect recorded authority, not truthfulness
  of upstream judgment. The second trial and full chronological tool trace were
  not available for this audit. AgentBlue2 geometry/source art was not reviewed.
- Blender is currently unreachable. Modeling, real ImageGen reconstruction,
  3D seam integration, saved production-file reopening and art L4 are SKIP for
  this tooling pass. No character completion or universal aesthetic guarantee
  is claimed. No service restart, new asset task, commit or publication occurred.

## Next Experiment

After Blender becomes available, run one separately scoped reference-character
experiment through the actual connector, with a deliberately hair-covered face
region and sufficient original anchors. Preserve the canonical reference and
Identity Lock; record FACE choice/tool availability, actual selected procedure
artifacts and generator lineage only when needed. Review front/side/three-quarter
primary forms before DETAIL. Exercise a failed primary check and two unsuccessful
corrections to confirm saved-state reconsideration and continuation behavior.
Finish with original/prepared/baked identity and seam closeups, required final
fixed views, an independently reopened .blend and schema-3 FINAL receipt.
Have an art reviewer judge identity and forms independently of structural PASS.
