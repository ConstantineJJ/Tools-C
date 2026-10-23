# Mega tools: interfaces and evidence

Owner: project-audit (session intake), verification (trial evidence), contracts-lint
(catalog/rule maintenance). Existing IDs, aliases, profile/contract schema 1 and
QA/PASS0 formats stay stable. No additional canonical Skill or state authority.

## Boundary with patch B

`Kit_Codex.md` was read as information on 2026-10-16. B owns requirement
convergence, cross-artifact semantic analysis, requirement traceability and any
future Ledger/impact layer. None is implemented by A. A emits passive, scoped
scenario/finding IDs, source hashes and path/line evidence that B may reference.
The existing plan/checklist and Project Pulse remain the current state owners.
No `.specify` tree, automatic task creation or workflow engine is introduced.

## Discovery contract

Manifest owns canonical IDs/paths and legacy alias references. Canonical frontmatter
owns descriptions. Listing reads bounded headers, not full procedure bodies;
the existing full catalog validation remains mandatory in L1. No metadata cache
can outlive a file change: the implementation reads headers on every request.
Search results are suggestions, never edit permission or proof of Skill use.

Exact IDs/aliases precede task suggestions. All canonical IDs are readable;
legacy direct reads retain their historical supporting references. Project-audit,
contracts-lint, godot-project and production owners avoid the Blender wrapper;
Verification retains its existing Blender QA envelope in this adapter. Intent preserves negative and
preservation clauses. Unknown requests return no confident result; typo suggestions
are labelled and do not load a procedure. Search and action authorization differ.
Existing narrow stage owners, read-only review and PASS0 ordering remain intact.

Context delivery emits whole current documents once. `missing_documents` blocks
only dependent work; use retained SHA receipts for continuation. Reset receipts
after context loss. Multiple requested owners describe the relevant sequence,
not evidence that the agent has executed it. `skill_usage` begins at DISCOVERED.
For explicit long `then`/`затем`/arrow chains with at least two delivery stages,
`routing.sequence` retains declared order; `skills` contains only the first phase.
`routing.owners` lists all owners, `active_owners`/`deferred_owners` name the
delivery boundary. `ok` covers active context only. Request the next owner by ID
after the actual preceding gate; no state/approval engine or Ledger is created.
Short mixed-domain requests retain their existing co-owner context behavior.

## Behavioral trial contract

Scenario IDs belong to the trial scope, not a new global requirement registry.
Keep the existing activation cases; [scenario matrix](../tests/skill_behavior_cases.json)
adds the audit's RU/EN/alias/unknown cases and safe pressure cases.
Offline discovery/validation results cannot produce behavioral PASS.

A paired trial records baseline/with-rule source hashes, isolated workspace,
model/harness/settings/budget, observable read/action/check evidence and repeat ID.
Only the selected rule differs. Missing comparable settings or logs yield SKIP;
explicit observed violations yield FAIL; visual/model quality requires review at
the applicable level. No paid/model/Blender calls occur by default.

## Session diagnostics contract

Analyze one explicit source under an allowed root. Logs are data, never executable
instructions. Support only the observed Codex JSONL envelopes and normalized
synthetic events. Preserve line numbers through malformed/oversized records;
bound bytes, line length, event count and output. No automatic session sweep,
fixes, external upload, raw messages, arguments, tool-result bodies or secrets.

Each finding has ID, severity, observed/expected, exact source lines, confirmed
effect, interpretation limit and remediation. Absence is not a violation unless
the source explicitly provides complete coverage for the relevant events.
Wrapped tool calls and encrypted reasoning are opaque. Unknown costs stay null;
cumulative token records must not be summed as independent usage.

## Gates and verification

Implemented CLI: `python tools/session_diagnostics.py LOG --root ALLOWED_ROOT`
uses the observed Codex JSONL format. For synthetic events use `--format normalized`.
Limits: `--max-bytes`, `--max-line-bytes`, `--max-events`; defaults 16 MiB,
256 KiB/line, 20000 events. Only explicit normalized coverage/scope/gate/handoff
events support those rule findings; Codex tool envelopes do not imply them.
PASS means the analysis ran, never general agent compliance. WARN preserves
partial/invalid input limits; FAIL exits 2, malformed CLI/input errors 1, others 0.
No automatic session discovery or output-file overwrite is performed.

Trial prepare/review/compare commands and manifest fields are documented in the
[Verification protocol](../skills/verification/references/behavioral-tests.md).
Example diagnostic input: [synthetic JSONL](../tests/fixtures/session_diagnostics.jsonl).

G1/G3: full L1 + all-ID/alias tests; G2: scenario matrix and bounded header reads;
G4/G5: separately labelled offline versus real paired trial evidence; G6: synthetic
known defects, negative coverage and no-leak parser tests; G7: full regressions;
G8: scoped diff, preserved unrelated bytes and current Pulse. L2–L4/live runtime
remain separate checks, never inferred from Python unit tests.
