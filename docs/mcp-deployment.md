# MCP deployment and evidence boundaries

Canonical Tools_C → generated routers in integration repository → configured MCP
wrapper/process → local tunnel → ChatGPT connector. Each edge has its own evidence.

## External capture storage

Native `capture_viewport` and managed Python image delivery share
`tools/mcp_capture_response.py:capture_directory`. Default output is
`Work_Utility/captures/<unique-id>` beside canonical Tools_C, currently
`E:/MyCreations/Work_Utility/captures`. Optional `TOOLS_C_WORK_ROOT` must be
absolute and outside canonical Tools_C; set it consistently for server and Blender.
Path resolution, manifest equality, PNG bounds and hashes remain enforced.
Old `.local/captures` evidence is preserved, but is no longer an attachment source.
Restart the MCP server normally after its capture route update. Until reloaded,
use the managed Python recipe in [evidence](blender-evidence.md), which reads the
current helper per call. This does not require reopening or restarting Blender.

## Context delivery and bounded operations

The original seventeen public tool names remain. 4.2.1 adds read-only tools_c_check
and optional camera_name/channel capture inputs; prior calls retain their behavior. All tools
declare explicit `readOnlyHint`, `destructiveHint`, `openWorldHint` and
`idempotentHint` annotations. Seven are read-only: `list_skills`, `read_skill`,
`find_skills`, `get_scene_info`, `get_skill_context`, `deployment_info`, `tools_c_check`.
The other eleven remain writes, including captures that save files and
`blender_operation_status`, whose optional cancellation changes job state.
Deletion, slot replacement/shared-material edits, active-camera replacement,
file overwrite, arbitrary Python and cancellation declare destructive effects.
Arbitrary Python and unrestricted save destinations declare open-world access.
These hints describe behavior; they do not replace the existing bridge checks.

`list_skills` adds `canonical_count`, `canonical_skills` and
`compatibility_aliases`. Existing `skills`, `count` and `skills_dir` retain their
nine-router discovery meaning for compatibility. Canonical entries contain
owner ID, title, purpose, relative path and aliases, without procedure bodies.
`read_skill(name)` accepts either a canonical owner ID or an existing alias.

`find_skills(query, max_results=10)` searches owner IDs/aliases/titles first,
then purpose metadata, with entrypoint-text fallback for detailed terms. It
returns at most one result per canonical owner. The three legacy result fields
`name`, `score`, `excerpt` remain; the name is a readable canonical owner ID.
Shared/dependency contexts are not expanded or ranked as owner-specific content.
Excerpts are discovery only. The provider-neutral
[catalog helper](../tools/skill_catalog.py) keeps this logic in Tools_C.

Metadata listing reads bounded current Skill headers; full structural/link checks
remain in L1. Natural-language search reuses the existing task intent before lexical
fallback; precise single-term recipe fallback can read entrypoints, never expanded
dependencies. Typo suggestions do not select/load a procedure. Explicit canonical
IDs and legacy aliases resolve from the manifest, including in a warm MCP process.

`deployment_info` retains the input-schema digest and separately adds a metadata
digest covering descriptions and annotations, plus `tool_annotations`.
After a server update, verify its loaded identity and refresh client metadata to
consume changed descriptions/hints. Local stdio success does not certify the
external UI. The explicit read-only
[metadata probe](../tests/mcp_metadata_probe.py) compares existing input
schemas against a saved stdio baseline, allowing the documented optional capture fields and exercises discovery/read/context calls.
An absent Blender addon makes its scene comparison SKIP; no process starts implicitly.

`get_skill_context(task, max_chars=60000, known_documents={}, requested_documents=[])`
delivers whole canonical Markdown documents once across mixed owners. Each document
has a SHA-256 receipt. `ok=false` and `missing_documents` require a continuation
before the affected edit; pass delivered `receipts` and request the named missing
documents. Retain receipts only for bodies still available to this caller. Clear
them after context loss/compaction, for a new chat or agent. Stale hashes cause
redelivery. Conditional references are identified separately and must be fetched
before the corresponding operation. A successful short entry does not mean every
optional procedure has been read. Budget limits never clip a rule mid-document.

For explicit long stage chains, `routing.owners` retains all owners in declared
order; `active_owners`/`deferred_owners` and `sequence` identify the current delivery
scope. `skills` and `ok` cover only the first phase. Ask for the next owner by ID
after actual upstream evidence. Short mixed-domain contexts retain co-owner loading;
no stages are executed or marked complete by context delivery. Project-audit,
contracts-lint, godot-project and production reads avoid Blender-only scaffolding;
Verification keeps its existing QA envelope. See [Mega tools](mega-tools.md).

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

## Authenticated bridge and bounded work (2026-10-25)

Deploy the matching `blender_mcp_server.py` and `chatgpt_blender_mcp.py` together.
Reload the addon and restart the MCP server process to activate these source changes.
The server probes authenticated bridge protocol 2 before sending executable Python;
an older addon is rejected before the executable payload is sent.

Starting the addon creates a random 256-bit bearer token in
`%LOCALAPPDATA%/BlenderMCP/bridge-token` (other platforms: `~/.config/BlenderMCP/bridge-token`).
The MCP process reads the same user-local file. `BLENDER_MCP_TOKEN_FILE` selects an
absolute private file, or `BLENDER_MCP_TOKEN` supplies 64 lowercase hex characters
to both processes. Invalid/missing credentials fail closed. Never copy tokens into
repository files, plugin archives or diagnostic reports. File access inherits the
Windows user-profile ACL; on POSIX new files use mode 0600. Protect any custom file
with equivalent permissions. This authenticates local callers; it is not a Python
sandbox or protection from a compromised process running as the same user/admin.

The bridge remains bound to `127.0.0.1`. Requests are limited to 4 MiB, 16 client
slots, 16 queued items and a 5-second read deadline. A timer callback handles at
most two items and stops starting items after 20 ms. A single running Python call
cannot be preempted safely; use typed curve batches for divisible work.

Every request has an echoed ID and explicit execution wait (60 seconds normally,
180 seconds for captures); the transport waits an additional 10 seconds for the
addon verdict. Rejected and cancelled-before-execution requests did not execute.
An interrupted transport after sending or a running timeout is `UNKNOWN_EXECUTION`:
inspect the scene/operation receipt before retrying. IDs correlate responses; they
do not provide automatic deduplication of arbitrary Python or rollback.

Curve receipts now use `TOOLS_C_WORK_ROOT/operations`, beside managed `captures`,
defaulting to sibling `Work_Utility`. Both output categories reject the canonical
Tools_C tree. Old `.local/operations` receipts are read-only interruption/history
evidence and are not automatically replayed or moved.

Token and timeout primitives follow the Python documentation for
[secrets](https://docs.python.org/3/library/secrets.html) and
[sockets](https://docs.python.org/3/library/socket.html).
