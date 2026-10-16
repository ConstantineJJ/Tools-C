# Tools_C — patch B, B8–B10 final QA

Дата: 2026-10-16. Branch: `codex/development-control-b`.
Checkpoint B1–B7: `f878b0adaefb4b3c558e44181841b7833c66d728` (17 allowlisted paths).
Checkpoint candidate: 415/415 PASS, 222.482 s; L1 50 PASS / 0 WARN / 0 FAIL.
Review mode: SELF_REVIEW. **B8–B10 DONE / Checkpoint B-IV PASS** within R0 scope.

## Delivered scope

B8 integrates optional review in existing project-audit, contracts-lint,
verification and production-project-state-gates. Metadata discovery selects
these owners; their entrypoints link the interface only when relevant. Existing
MCP requested_documents/receipts fetch it without new schemas or tool names.
README/contracts document the opt-in boundary; core L1 checks the four routes
and required implementation/example files. No new canonical Skill, catalog,
foundation/Pulse, workflow engine or dependency is introduced.

B9 supplies a runnable four-file vehicle metadata example and integration tests.
VEHICLE-001 verifies saved metadata bytes, VEHICLE-002 leaves actual likeness OPEN,
VEHICLE-003 leaves formal PASS0 OPEN. Generic visual status NOT_EVALUATED; actual
image inspection SKIP because the fixture contains no images or scene. Existing
ASSET_FINAL receipt validation independently refuses uninspected views despite
structurally valid metadata. This does not revisit the user's acceptance of A.

B10 includes fresh full working-tree/candidate verification, read-only connector
smoke, generated router sync, scope review and R0/K1–K10 handoff below.

## Verification

Final `python -m unittest discover -s tests -v`: working tree **433/433 PASS**,
272.013 s (wrapper 272.355 s); clean candidate **421/421 PASS**, 271.470 s
(wrapper 271.813 s). Both exit 0 with no failures/errors/skips. Candidate = HEAD
`f878b0a` export + exactly 18 own paths, excluding unrelated work and 12 workflow
tests. The 66 review/integration tests (6 new) are included in both final runs.

The initial full runs found the same real regression in both trees: added
Verification text pushed required anime instructions beyond the existing 60000
context budget. Only new B8 wording/description was shortened; no test, budget or
required document was weakened. All 11 anime tests and both full suites then
passed. Runtime/test/fixture/Skill hashes were frozen before the final full runs.

Final L1 `python tools/check.py --self --json`: **51 PASS / 0 WARN / 0 FAIL** in
both working tree and candidate. `--project E:/MyCreations/Blender-MCP-Co --json`:
**9 PASS / 0 WARN / 0 FAIL**. Each L1 run separately reports expected L2–L4 SKIP.
Disk deployment audit PASS, 17 source tools. No expensive model/3D generation,
production scene mutation, service restart, push or deployment.

The already-running MCP served changed project-audit instructions and explicitly
requested interface content; contracts-lint read succeeded. Before/after server
and tool schema hashes match; 17 tools, restart_required=false. All **9 legacy
aliases** were read through the actual resident connector after the fix and their
returned bodies matched current local canonical rendering. Discovery queries
cross-artifact/traceability/convergence select project-audit/contracts-lint/
verification respectively. Explicit interface delivery and retained receipts are
verified against current normalized document SHA. Local routers use only
`python tools/sync_blender.py --project E:/MyCreations/Blender-MCP-Co`.

## Gates

| Gate | Status | Evidence / limit |
|---|---|---|
| R0 | PASS | Existing owners/source/options reviewed before B; original R0 retained |
| K1 | PASS | Same 28 canonical IDs / 9 aliases; no competing authority |
| K2 | PASS scoped | Hash/line/ID/ref binding and stable traceability; unsupported semantics not inferred |
| K3 | PASS scoped | Formal conflicts, duplicates and coverage; no arbitrary source rewriting |
| K4 | PASS scoped | Four observed gap types; unknown/manual distinct |
| K5 | PASS | Repeat state NO-OP, stable task IDs/history and linked closed recurrence |
| K6 | DEFER | Separate Ledger/resume engine unnecessary under R0; existing state reused |
| K7 | PASS scoped | Direct/possible/unknown dependency evidence; migration UNKNOWN without schema delta |
| K8 | PASS | Full 433/421; L1 51/9; live 9 aliases, same server/schema and receipt compatibility |
| K9 | PASS | 18 own paths; 423/60 outside-scope paths preserved; regression fixed; no hidden deployment |
| K10 | PASS | This report + JSON, runnable fixture, plan/todo and current Pulse; limits retained |

## Git and protected work

Unrelated QA/character/vehicle edits, workflow tests and 76 historical report
deletions remain outside both commits. `.tooling/contracts.json` is mixed:
only the B8 required-path/owner-route delta is eligible for staging; the prior
workflow-test requirement remains worktree-only. No blanket staging/reset/clean.

Integration root AGENTS/profile/README and current Git state read before sync;
only 20 generated routers/manifests changed; all other **60/60 baseline paths**,
its HEAD and user server/launcher/add-on bytes are preserved. Tools_C preserves
**423/423 outside-scope baseline paths**, including 76 missing reports. Diff and
explicit staging allowlist exclude unrelated files and the mixed contract hunk.

The generated routers reflect the installed working tree, including pre-existing
character-flow changes; they remain local/uncommitted. Their checksums do not
certify the separately tested clean publication candidate. Existing router remote
publication failure (`Repository not found` in A) remains BLOCKED; no retry,
remote/credentials change, push or deployment is performed.

## Sources, reuse and limits

Original external basis: [R0](PATCH_B_R0_2026-10-16.md), Spec Kit pinned ref
`f6e72bc8523de8ec8368129cbdea78d45f27cef8`, MIT. No external code/templates copied.
ADAPT: scoped traceability/analyze/convergence/task upsert/impact. ALREADY COVERED:
canonical authority and domain state/QA. DEFER: separate Ledger/workflow executor,
generic semantic/visual attestation and automatic engine execution.

Reuse existing stdlib helpers, contracts and snapshot/freshness/QA owners. Cost:
three focused runtime modules, bounded tests and one small domain fixture. Reports
are evidence, not another mutable task database. A report hash is not an attestation.
Semantic authority, arbitrary concurrency, unselected dependencies and actual
visual/runtime acceptance remain explicit limits; lower levels never imply higher.

Next owner: routine users may opt into the documented review workflow. A future
publication step must review integration-root changes independently and regenerate
its routers against the intended published canonical tree. A separate Ledger or
automatic engine execution requires reopening R0; no further B implementation is
pending within the accepted scope. Actual asset inspection/runtime remain SKIP,
and controlled A G5 remains its historical SKIP.

[Interfaces/example](../docs/project-review.md) · [Plan](../tasks/plan.md) · [Pulse](../Project-pulse.md)
