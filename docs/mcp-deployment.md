# MCP deployment and evidence boundaries

Canonical Tools_C → generated routers in integration repository → configured MCP
wrapper/process → local tunnel → ChatGPT connector. Each edge has its own evidence.

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
