# Optional MCP Helper integration

MCP Helper 0.1.1 is an independent C# navigation and rename-preview service.
Constantine Hub 0.3.1 can manage the same standalone package. Tools_C remains the
canonical owner of Skills, contracts, project review and QA; Helper is optional.
It is not required for Blender/Godot work and does not replace their MCP bridges.

## Connect and discover

Configure one explicit workspace in Helper or Hub. A client-owned process uses
`McpHelper.exe stdio --config <local-json-path>`. The service mode uses authenticated
loopback Streamable HTTP; Hub's Connection button copies the configured endpoint
and header for the intended MCP client. Do not put connection tokens into source,
reports, tool arguments or logs. No new tunnel or client registration is automatic.

Read `helper_status` and `helper_info` before querying. Require the configured
workspace/version and actual backend capabilities; a PID/TCP listener is not an
analysis result. An unavailable Helper does not invalidate existing Tools_C checks.

## Scoped workflow

1. `helper_find_symbol` with `query`, optional `offset` and `limit`. Overloads have
   distinct `symbol_id` values; choose the intended signature/location.
2. `helper_find_references` or `helper_impact` with `symbolId` and
   `expectedSnapshot` from the returned `snapshot_id`. Treat partial/truncated
   results as bounded evidence; page explicitly when necessary.
3. `helper_refactor_preview` with `symbolId`, `newName`, `expectedSnapshot` returns
   edits and base raw-file SHA-256 values. This version never applies edits.
4. Recheck scope and freshness before any separately authorized editing operation.
   On `E_CONFLICT`, choose a nonconflicting name; no edits are returned.
   On `E_STALE`, inspect current files and repeat discovery; do not silently rebind.

`helper_outline` reads declarations in one relative workspace `file`, without
method bodies. All seven tools are read-only; there is no apply, shell or project
execution tool. Source positions use zero-based UTF-16 line/character offsets;
convert to one-based line numbers for human-facing file links.

## Interpretation and existing owners

Helper uses a disk-only Roslyn AdhocWorkspace. It reads UTF-8 source/project files
and project references without evaluating MSBuild, running restore, analyzers,
generators or project scripts. Conditional project rules, external packages,
generated/dynamic calls and unsaved editor buffers may be unresolved. Compilation
diagnostics describe the safe workspace, not a real project build result.

`operation_status=PASS` never implies `analysis_coverage=complete`. Missing
references are not proof of no impact. Check warnings, snapshot, exact overload,
pagination and affected files before drawing conclusions.

Existing [project review](project-review.md) owns declarative requirements/task/
artifact dependencies. Helper contributes semantic code facts; do not create a
second ledger or replace the existing graph with these partial results. Existing
L1–L4 checks retain their scopes. Build, runtime and visual acceptance require
their own evidence; preview success is not refactor/build PASS.

For dirty/untracked sources, preserve the current working bytes and Git state
using a reviewed [source bundle](source-bundles.md). HEAD alone may omit the app.
Capture/integrity checks do not authorize restore, staging or cleanup.
