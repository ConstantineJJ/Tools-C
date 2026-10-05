# MCP deployment and evidence boundaries

Canonical Tools_C → generated routers in integration repository → configured MCP
wrapper/process → local tunnel → ChatGPT connector. Each edge has its own evidence.

## Context delivery and bounded operations

`get_skill_context(task, max_chars=50000, known_documents={}, requested_documents=[])`
delivers whole canonical Markdown documents once across mixed owners. Each document
has a SHA-256 receipt. `ok=false` and `missing_documents` require a continuation
before the affected edit; pass delivered `receipts` and request the named missing
documents. Retain receipts only for bodies still available to this caller. Clear
them after context loss/compaction, for a new chat or agent. Stale hashes cause
redelivery. Conditional references are identified separately and must be fetched
before the corresponding operation. A successful short entry does not mean every
optional procedure has been read. Budget limits never clip a rule mid-document.

`start_curve_batch(operation_id, collection_name, batches, batches_per_tick=1,
radius=0.01, material_name=None)` creates editable named curve objects in a new
collection. Each batch has `name` and `paths`; points are XYZ with optional positive
radius multiplier. Limits: 256 batches, 10000 points per batch, 200000 total points,
1–16 batches per timer tick. Chunk limits reduce blocking; they are not time guarantees.
`blender_operation_status(operation_id, cancel=False)` reads progress or requests
cancellation. After timeout inspect the same ID; identical inputs do not replay,
changed inputs fail. Cancellation/failure retain partial output. Receipt-only
status after Blender process loss is historical evidence, not proof of current
scene objects; unfinished receipts become `interrupted`. Inspect before recovery.
The existing Python preflight/bridge safety gate applies to both tools.

Use `tools/mcp_deployment.py --project PATH` for read-only disk validation. It checks
the target config, canonical resolution, both router trees, manifest integrity,
required source tool registrations and hashes. No service starts/restarts implicitly.
With `--python EXE --stdio`, explicitly launch a disposable MCP process from that
target, initialize via MCP SDK, compare tool schemas, resolve every legacy alias
against canonical bytes and call deployment_info. This needs the installed MCP SDK.

`deployment_info` returns the loaded server hash, current disk hash, canonical root,
architecture version and a stable catalog/schema digest. A mismatch between loaded
and disk server hashes requires a normal restart. Changed canonical content is loaded
on each request. Sync only generated routers; edited/unlisted copies fail before any
writes. Manifests record current context hashes in addition to router hashes.

Local sync PASS proves neither a live process nor a connector. Record actual
connector list/read/context calls separately. After adding capture_viewport and
deployment_info, compare the connector-visible catalog with the stdio catalog.
An old connector catalog after a successful process restart is a schema-refresh
problem; reconnect/refresh the connector through its normal settings. Do not invent
a remote refresh capability or treat HTTP health as MCP tool execution.

If a tunnel returns 404, check its configured profile/wrapper and health endpoint,
then the upstream MCP process. Preserve credentials; reports should use paths,
hashes and status, not token-bearing settings or full environment dumps. No broader
launcher rewrite, safety gate replacement or micro-tool registry is needed.

Python preflight parses/compiles without executing before all Blender payloads in
the integration bridge. A syntax diagnostic includes line/column. Advisory state
warnings do not disable generic execution; existing approval/safety behavior remains.
Follow [bounded-call guidance](foundation.md) on an actual blocked call.

Optional `--tunnel-profile PROFILE.yaml` checks the configured and live loopback
health target without recording secrets. `--connector-tools TOOLS.json` compares an
observed JSON array of connector tool names to the source catalog and reports
missing/extra entries. Names alone cannot validate remote input schemas.
