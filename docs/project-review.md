# Optional project review packet v1

Implemented B2–B7 entrypoint: `tools/project_review.py`. Python stdlib only.
This is a scoped traceability map; existing contracts/profiles/receipts keep
their own schemas. A project without this packet remains valid.

```powershell
python tools/project_review.py validate review.json --project PROJECT
python tools/project_review.py analyze review.json --project PROJECT
python tools/project_review.py converge review.json --project PROJECT
python tools/project_review.py converge review.json --project PROJECT --previous previous.json
python tools/project_review.py impact review.json --project PROJECT --changed-source SOURCE_ID
python tools/project_review.py impact review.json --project PROJECT --changed-rule REQUIREMENT_ID
```

The packet/report paths are relative to PROJECT. These commands read inputs only and emit
JSON to stdout. `validate` checks structure, source hashes, exact source ID/line
bindings and references; acceptance stays NOT_EVALUATED. `converge` additionally
checks the declared predicates and maps results through requirements/tasks.
`analyze` inspects only the declared graph and formal predicate compatibility;
it does not inspect artifact contents or evaluate acceptance. These commands
never run source code, a shell command, engines, models or plugins.

Exit 0 means a report was constructed, including when acceptance is FAIL/OPEN.
Exit 1 means invalid/stale/unreadable/out-of-scope input; exit 2 means invalid CLI
usage. Consumers must inspect `acceptance_status`, never infer acceptance from
exit 0 or `analysis_status: PASS`.

## Exact packet fields

All fields below are required except the stated optional fields. Unknown fields,
versions, duplicate JSON keys/IDs/references, non-finite numbers and wrong types
are rejected. IDs use the existing Tools_C identifier syntax. Uniqueness is per
collection inside `scope`; requirement revision is a positive integer.

| Record | Fields |
|---|---|
| Packet | `schema_version: 1`, `scope`, `revision`, `sources`, `requirements`, `tasks`, `artifacts`, `checks` |
| Source | `id`, `path`, `sha256`; optional `root: project` (default) or `tools` |
| Requirement | `id`, `source: {id, line}`, `description`, `mandatory: bool`, `level: L1/L2/L3/L4`, `checks: [check IDs]` |
| Task ref | `id`, `source: {id, line}`, `requirements: [requirement IDs]` |
| Artifact | `id`, `path` |
| Check | `id`, `requirement`, `artifact`, `kind`; `expected` required only for `sha256` |

Source hashes bind raw file bytes, including newline encoding. Source text must
be UTF-8; line is 1-based and must contain the bound requirement/task ID as a
separate identifier. This proves a structural reference, not semantic equivalence
or the authority/truth of its prose. Summaries never override the approved source.
Task records reference the existing plan/todo; completed checkbox state is not
copied or trusted as verification. Changes in source bytes require explicit rebind.

All paths are relative forward-slash paths inside their permitted root, including
resolved symlinks/junctions. Only source records may select `root: tools`, through
an existing strict `.tooling/config.json` pointer matching this installed Tools_C.
Artifacts are project-local. Config cannot authorize arbitrary extra roots.

## Predicate and acceptance boundaries

- `file_exists`: actual path must be a regular file. Observed absence → `missing`;
  an existing non-file → `contradicts`; inaccessible/unknown state → UNKNOWN.
- `file_absent`: an explicitly forbidden resolved path must not exist. Observed
  existence → `unrequested`; observed absence → PASS; inaccessible → UNKNOWN.
  This is an additive optional predicate; it never infers scope from an unmapped
  object. Review the source-to-predicate mapping before relying on it. The ID/line
  binding alone does not establish semantic agreement or source authority.
- `sha256`: actual bounded file bytes must match lowercase 64-digit `expected`.
  A differing existing file yields `partial`; this is a fingerprint requirement,
  not an assessment of its visual or runtime quality.
- `manual`: always UNKNOWN in this slice. No supplied claim can turn it into PASS.

Every check must belong to exactly its named requirement and appear in that
requirement's check list. Incomplete task/check coverage remains OPEN with
`gap_kind: null`, not a claim that implementation is missing. Check failures give
the affected requirement FAIL. L1 predicates can certify only L1 requirements;
higher-level requirements stay OPEN even when their files exist. `visual_status`
is always NOT_EVALUATED. Existing QA/engine/visual review remains necessary.

Overall acceptance concerns mandatory requirements: a mandatory failure → FAIL;
unknown/incomplete/higher-level mandatory evidence → OPEN; otherwise PASS.
No mandatory requirements → OPEN. Optional failures remain visible in rows/findings.
Finding IDs bind scope/requirement/detector/logical target/check; evidence hashes
and revision are excluded so unchanged defects retain identity across reruns.
Read-only operations do not create or update tasks. Check results distinguish
UNKNOWN with `reason: not_checked` (manual) or `blocked` (unreadable observation).

## Cross-artifact analysis and history

`analyze` reports orphan tasks, unmapped artifacts, incomplete traceability and
manual/unspecified acceptance requiring review. Dangling references and duplicate
IDs remain invalid input, rejected before analysis. Graph coverage is explicitly
`declared_records_only`; unknown project files are not scanned.

Checks sharing a resolved artifact path conflict when they require both existence
and absence, or two different SHA-256 values. Evidence names both checks and their
requirement source lines. Equal predicates produce DUPLICATE_ACCEPTANCE requiring
review; this does not prove duplicate intentions. Prose keywords never establish
a semantic conflict or execute an instruction. Semantic review remains manual;
there is no generic reviewer attestation import in this checkpoint.

`converge` adds actual predicate observations. Formal conflicts between mandatory
requirements fail those rows; optional conflicts remain visible without upgrading
an optional rule into a mandatory failure. Duplicate/incomplete mandatory acceptance
stays OPEN. Truncated analysis cannot close acceptance and blocks task application.

`--previous` accepts a fingerprinted convergence report of the same scope, compatible
engine version and no later revision. It appends bounded observation history keyed
by stable finding ID. Unchanged state adds no history entry; changed evidence or
revision retains the earlier entries. `not_observed` means absent from this fresh
declared analysis, not an automatic task completion; truncated reports use
`not_reported`. Previous PASS never supplies current verification.

Reports bind packet SHA, engine source SHA and version. `report_sha256` detects
accidental modification; it is not a signature or independent attestation. B2/B3
report output predates these fields: regenerate it; packet v1 remains supported.

## Explicit task application

Only `apply-tasks` writes. Its implementation is isolated in
[project_review_tasks.py](../tools/project_review_tasks.py), keeping write/locking
mechanics separate from read-only analysis. Example, with a real old todo SHA:

```powershell
python tools/project_review.py apply-tasks report.json --project PROJECT --todo tasks/todo.md --expected-sha256 OLD_SHA256 --namespace B --start 11 --exclusive-writer
```

The report must be a current convergence report. The caller selects the existing
project-local Markdown todo, old raw SHA, task namespace and initial number explicitly.
`--exclusive-writer` asserts that the caller owns this write interval; without that
ownership use the read-only report/manual handoff. It is a local CLI precondition,
not a request for a new user approval each time. Engines, code fixes and task
completion are never run by this operation.

Before a new write, the helper reconstructs analysis from the bound packet and
compares current sources, checks, results, proposals and engine fingerprint. Only
observed predicate gaps create proposed tasks: missing, partial, contradicts or
unrequested. Unknown/manual/semantic suspicions do not create implementation tasks.
Formal conflicts or omitted findings refuse application; resolve/review them first.
No actionable gap means no task or todo write.

Tasks occupy one marked `tools-c:convergence SCOPE begin/end` section of the existing
todo. Prefix/suffix bytes stay intact; existing checkboxes and titles are preserved.
Inline strict JSON metadata binds finding identity, observation hashes and recurrence
links; it is not another task database or a workflow Ledger. IDs skip existing todo
and mapped task IDs. An open finding keeps its task ID and appends new observations.
Repeated state leaves bytes unchanged, even if `--previous` changed report read counts.
A completed task stays completed; a newly observed state creates a linked occurrence
with a new task ID. The operation never silently reopens a checkbox.

New task observations also store an optional `history_sha256` prefix fingerprint
of that finding's normalized report history. An explicit `FAIL → not_observed →
FAIL` history extension is a new occurrence even when the packet, revision and
final state hash match the original failure. Replay compares the latest task
observation, not every state ever seen; open tasks retain `A → B → A` transitions.
Legacy observations without this field remain readable and are not rewritten on
NO-OP. A standalone identical state without intervening history cannot establish
a new closed-task occurrence; supply `--previous` history or an explicit revision.
History fingerprints bind coordinator-supplied observations, not an attestation
that unobserved intermediate events happened.

Use the returned `todo_sha256` as the expected hash for a repeat. An already recorded
state returns NO-OP without claiming current acceptance. This handles a first append
invalidating the bound todo source hash: for any new analysis/write, explicitly review
and rebind the source SHA in the packet. Source bindings are never refreshed silently.

Malformed/duplicate sections, altered finding identity, stale target/report and an
active cooperating lock refuse writes. A sibling exclusive-create lock, repeated
hash/path checks, fsynced temporary file and atomic replace protect cooperating
writers. Atomic replace is not compare-and-swap against an arbitrary concurrent
writer; external filesystem changes are not an OS-isolated snapshot. Locks and
temporary files are cleaned on handled errors; after a process crash inspect a
leftover lock manually, it is not auto-removed as stale.

## Limits and reproducible example

Packet ≤1 MiB; all unique file reads together ≤16 MiB, including config/sources
and hash-predicate artifacts (writer rechecks count again); ≤20,000 physical lines per source (LF/CRLF/CR),
IDs ≤128 characters, paths ≤4096 characters, ≤1024 declared records,
≤100 output findings with
an omitted count; ≤1024 total history observations. Report/todo input and todo
output are each ≤1 MiB. Reading is limited before JSON decoding. Input must be a
regular file. Bounds failures never yield a partial PASS. Reports contain IDs,
declared paths, hashes, source line references and results, not raw source text.
The filesystem observations are not an atomic snapshot or OS security sandbox.

## State reuse boundary (B6)

Separate resume/Ledger/workflow engine remains DEFER. Current scope, next task and
decisions live in Pulse/plan/todo; immutable reports and the managed task section
retain observed history. `--previous` is a report comparison, not a checkpoint
that runs or skips production steps. A report from a different scope/later revision
is rejected; a prior PASS cannot satisfy current missing/manual/L4 evidence.

Use existing domain owners for actual reuse decisions: `handoff_snapshot.validate`
and `compare` bind the declared scene state; `qa_freshness.assess` checks scoped
current/capture dependencies and artifact hashes. These APIs do not certify pixels
or control the next engine operation. The generic review helper does not call them
implicitly. A future adapter must be trusted installed code with explicit scoped
inputs, current provenance and domain acceptance; packet text never names executable
commands. No resume CLI, Ledger file, scheduler or new task authority is introduced.

## Read-only Sync Impact (B7)

Select exactly one source ID or requirement ID already bound in the packet.
Changing a source requires an explicit packet SHA rebind before analysis. The
selection identifies the change being reviewed; it is not automatic before/after
diff detection. Existing packet fields and schemas are unchanged.

[project_review_impact.py](../tools/project_review_impact.py) observes only selected
hash-bound sources and the existing traceability graph:

- Direct: literal Markdown links/reference definitions, v1 contract paths/required
  targets, v1 profile contracts/references and resolvable skill IDs, selected
  manifest skill/alias references, explicit task → requirement source bindings.
- Possible: transitive paths, AST imports and exact selected-file path literals
  in Python. These do not prove execution, import search resolution or semantic use.
- Unknown: unselected targets/consumers, external links, unresolved/ambiguous IDs
  or modules, unsupported schemas/types/syntax and generated router runtime context.
  No linked file, URL, renderer or dynamic import is followed/executed implicitly.

Structured adapters extract declared edges; they do not replace full catalog,
profile, contract or link-existence checks. Markdown uses the small L1-style subset,
excluding code/comments; this bounded extractor retains line numbers without
calling the unbounded checker's file reader. JSON evidence uses pointers. Every
reported chain names its selected source and target IDs; hashes/lines/pointers
bind current evidence. Physical selected aliases are deduplicated by resolved path.
Source kind labels help scan the report; they do not establish rule ownership.

For a selected requirement, a link to its file remains `granularity: file`; it
does not prove dependence on that exact rule. `not_observed` means no edge was
found in supported selected declarations, never global independence. Coverage is
always explicitly incomplete; output truncation has per-bucket omitted counts and
per-chain omitted evidence. Stable impact IDs exclude hashes, lines and revision.

`executed_checks` records only the actual L1 packet/source/graph work.
`recommended_checks` lists L1–L4 suggestions as NOT_RUN, requiring scope review;
it does not mandate an engine or model run for every edit. Schema migration stays
UNKNOWN without before/after compatibility evidence, not automatically required.
Acceptance/visual state stay NOT_EVALUATED; no corrective tasks are proposed/applied.
Only `converge` accepts `--previous`; impact rejects task-write options.

Bounds: existing packet/source/read limits plus 4096 observed edges/unknowns,
JSON/Python sources ≤1 MiB each, ≤50,000 AST nodes per Python source; ≤100 combined
output rows, ≤16 evidence rows per reported chain. Exceeding an input/work budget
fails closed, rather than emitting partial PASS. Changing the installed helper
changes `engine_sha256` (core/writer/impact); regenerate convergence reports before
new task writes. Historical report comparison remains separate from fresh evidence.

```powershell
python -m unittest discover -s tests -p test_project_review.py -v
```

`test_real_vertical_slice_and_stable_missing_finding` creates real temporary
spec/todo/result files and a hash-bound packet: CORE-001 → B2 → result → C1.
It verifies PASS, removes result, observes FAIL/missing, changes revision and
checks the same finding ID. The CLI test runs the actual subprocess and verifies
unchanged input bytes; other cases cover source staleness, wrong references,
strict parsing/bounds, canonical pointer isolation and unopened L4 evidence.

## Deferred functions

[R0](../reports/PATCH_B_R0_2026-10-16.md) defers a separate Ledger/workflow engine;
no external model trial or generic visual/manual PASS adapter is added. Impact
analysis reports dependencies without auto edits, generation or deployment.
Owner integration and domain verification are recorded in the
[final B report](../reports/PATCH_B_FINAL_2026-10-16.md).

## Existing owners and runnable domain example

Use this optional workflow only for requested review or a current scoped packet:

| Owner | Responsibility |
|---|---|
| project-audit | Intake, selected scope, read-only analyze/impact |
| contracts-lint | Packet/ID/source validation; existing formats remain authoritative |
| verification | Current convergence and existing domain acceptance |
| production-project-state-gates | Guarded task application and handoff in existing todo/Pulse |

These entrypoints link here without forcing the full interface into every context.
MCP-only clients may fetch it through the existing `get_skill_context` request:
`task="project-audit", requested_documents=["docs/project-review.md"]`; reuse
current receipts only while retaining those exact documents. No MCP schema or
tool name is added. Review data never authorizes source fixes or engine execution.

```powershell
python tools/project_review.py converge review.json --project tests/fixtures/project_review_vehicle
```

The checked-in metadata-only fixture produces VEHICLE-001 PASS (actual saved
bytes), VEHICLE-002 OPEN (unreviewed likeness) and VEHICLE-003 OPEN (formal PASS0
not established); overall OPEN, visual NOT_EVALUATED, no proposed corrective tasks.
No scene/images are included, so actual image inspection is SKIP. This does not
reassess the user's accepted visual improvement after A. The isolated
`test_existing_asset_receipt_blocks_uninspected_vehicle_views` also exercises the
existing ASSET_FINAL receipt owner: structurally valid metadata with unreviewed
views cannot yield its final gate PASS.
