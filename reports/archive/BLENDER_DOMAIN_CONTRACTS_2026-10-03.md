# Blender domain pack — dedicated contracts pass

Date: 2026-10-03. Baseline: `43018cfaa68df543b56993bdd294575aafabb97c`.
Canonical root: `E:/MyCreations/Tools_C`.

## Reproduced gaps

An isolated baseline copy returned L1 PASS after each mutation: remove vegetation
from the self-profile; retarget the legacy sculpt alias to props; replace the
vegetation pipeline link with props. Existing checks validated selected entries and
link existence, but did not require the reviewed domain pack or its exact targets.
All three mutations now produce the expected rule-specific failures:
[negative evidence](domain-contracts-2026-10-03/negative-results.json).

## Accepted contracts

[Domain declarations](../.tooling/blender-domain-contracts.json) define seven rules:

| Rule | Machine-proven invariant |
|---|---|
| BDP-REGISTRATION | The eight reviewed owner IDs keep their canonical skill paths. |
| BDP-PROFILE | Tools_C's self-profile includes all eight owners and both contract files. |
| BDP-LEGACY | The nine legacy aliases retain their reviewed canonical reference targets. |
| BDP-AGENTS | AGENTS has actual local links to the eight owner files. |
| BDP-PIPELINE | Pipeline links to the eight owners and existing character/animal/retopo/surfaces/rigging/animation/export/Godot/verification owners. |
| BDP-FOUNDATION | Every domain skill links to the shared foundation. |
| BDP-SCULPT-COMPAT | The legacy sculpt procedure links to canonical blender-sculpting. |

Two base rules retain the Tools_C self-profile location and domain-contract
activation. These are Tools_C project declarations; ordinary projects keep their
own profiles and may activate only the relevant domains. Additions/reordering stay
allowed; migration provenance hashes and current skill bytes are not frozen.

## Checker changes

- `json_subset`: finite declarative JSON only; recursive object keys, required
  array members and exact scalar types/values. It runs no selectors, expressions
  or contract-supplied code. New mismatch diagnostic: `E_JSON_VALUE`.
- Markdown `required_targets`: project-relative targets must appear as local
  links/reference definitions in every declared document. Code, comments and
  images do not satisfy routes. Shape/path errors remain hard failures, including
  advisory rules and symlink escapes. New missing-route diagnostic: `E_ROUTE`.
- Strict JSON now rejects overflow numbers such as `1e999` with `E_JSON`.
- Existing base file coverage also protects the domain definitions/tests and
  previously added Visual QA fallback helper files.

## Deliberately not contracted

No universal asset identity, dimensions, wheel/bone/clip counts, triangle/texture/
texel/LOD/collision/wind budgets, provider, engine target or artistic tuning.
Presence of a link does not certify surrounding prose ownership or actual routing.
Safeguards/stop conditions, handoff quality and visual acceptance remain judgment
under the reviewed skills and verification. Runtime routes remain regression/live
evidence. Source files, domain bodies, legacy names and the Visual QA feedback loop
are unchanged; no router regeneration, service restart or asset edits were needed.

## Verification

- Tools_C L1: **19 PASS / 0 WARN / 0 FAIL**; Blender-MCP-Co L1: **9 PASS / 0 WARN / 0 FAIL**.
- Full regression suite: **84/84 PASS**, 0 failures/errors/skips; includes 21 new positive/negative test methods. Coverage includes all eight missing profile owners, all nine retargeted aliases, canonical path relocation, stage links, foundation/compatibility links, activation removal/retargeting, malformed rule fields, exact scalar types, advisory semantics, CLI exit/diagnostics and target/symlink escapes.
- Actual connector smoke: **13/13 full-byte context comparisons PASS**, covering eight owners, read-only review, retopo/surfaces and two intentional mixed-owner tasks. The already-running Blender MCP was sufficient; no restart or geometry edit.
- Disposable stdio deployment: **15 tools / nine legacy contexts PASS**, matching disk/loaded identity and syntax rejection. Integration routers and server files were unchanged; all 27 pre-existing dirty integration file hashes were preserved.
- `git diff --check`: PASS. New rule schema and diagnostic documentation match the implementation. L1 stayed read-only and engine-free.
- [Machine evidence summary](domain-contracts-2026-10-03/summary.json), [baseline gaps](domain-contracts-2026-10-03/baseline-gaps.json), [live comparisons](domain-contracts-2026-10-03/live-routing.json), [Tools_C L1](domain-contracts-2026-10-03/l1-tools-c.json), [integration L1](domain-contracts-2026-10-03/l1-integration.json). Full local logs under `.local/domain-contracts-20261003`.
Production asset L2/L3/L4 gates are inapplicable to this declarative checker pass;
prior Visual QA evidence remains evidence of its own bounded capture test.

## Completion boundary

This pass ends at machine-checkable registration/reference integrity and its
positive/negative evidence. Further semantic reviews or production asset work
require their own scope. Historical review/Visual QA reports retain their original
pre-contract milestone status.
