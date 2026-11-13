# Tools_C — Project Pulse

## 4.2.1 — 2026-11-13

Canonical source: this repository. Thirty skill owners, nine legacy aliases;
profile/catalog/registration schema_version remains 1. Main Tools_C and Tools_C
Light remain distinct. The private package is a thin entrypoint, not another canon.

Implemented: named-camera and silhouette capture through the existing helper,
evaluated world measurements, bounded mask/contour/landmark comparison with
input hashes, localized findings and existing QA artifact binding/recomputation.
The existing MCP adapter adds tools_c_check; old operation names remain.
Checker subprocesses use closed stdin, no shell, a 30-second deadline and bounded
returned output. Private exact-root registration stays outside project contracts.

See [release notes](docs/release-v4.2.1.md), [Agent Vision](docs/agent-vision.md),
[private plugin](docs/tools-c-plugin.md), and [approved work](tasks/v4.2.1.md).

Verified final source: **497/497 PASS**, 279.026 s; source/integration L1 **52/9 PASS**;
bridge lifecycle/authentication **16/16 PASS**. All 30 default contexts complete
(largest 59,979 / 60,000 chars). Blender 5.3.0 live/factory geometry, camera,
alpha, depth-ambiguity and ring probes PASS. Fresh MCP client exposes 18 tools,
executes central checks in about one second, rejects an unregistered root and
returns actual PNG ImageContent for the comparison overlay. Current report:
[4.2.1 verification](reports/v4.2.1.md).

Private USER Tools_C 4.2.1 was created, release
`pluginrel_6af6f776a3248191a6376a0651f37f44`:
[Tools_C](https://chatgpt.com/plugins/plugins_6af6f77558b481918b344e1d58bba65f).
App/routing/YAML readback matches; service-normalized presentation retains the
original icon, name, version and prompts. The package contains one thin entrypoint.

Deployment handoff: the live server reports restart_required=true for the final
comparison image-kind delegation change. The user stopped UI automation with
physical Escape; no alternative restart was attempted. Press Blender MCP Restart
in ConHub, then check deployment_info. No Blender scene save/restart is required.
Fresh @Tools_C selection in a new chat remains a separate user-facing check.

Obsolete 4.0.1 release/publication files and 30 early archived report files were
removed; later feature evidence remains historical. The user removed the ignored
.local/archived_reports/2026-10-08 directory after shell cleanup was blocked.
Original bytes remain in checkpoint/history; source/lesson provenance is retained.
Published catalog changes were merged with canonical development, preserving
active instructions and stricter source checks. Bootstrap uses docs/skills.md;
legacy installs without it retain the AGENTS router fallback.

Known limits: explicit reference masks and declared camera/pose calibration;
metrics do not certify artistic likeness, hidden depth, topology or runtime.
Depth/Normal/ID analysis is not part of this implementation. Godot runtime was
not launched. Blender-MCP-Co's old remote URL returns repository-not-found;
its local checkpoint and adapter patch are retained. No new remote was invented.
