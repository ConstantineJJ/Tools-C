# Tools_C 0.1.0 — final acceptance, 2026-09-22

## Decision and scope

Acceptance of the bounded tooling implementation: **PASS**, with the deployment
warning and concurrent-editor limitation below. No gameplay/art redesign, new
provider, dependency install, destructive deployment, push or history rewrite.
This is a finalization of 0.1.0, not a new framework or a full game QA claim.

Canonical skills → replaceable project profiles → declarative contracts → bounded
checkers → evidence/Pulse remains the architecture. Five skills and eight legacy
aliases are unchanged; substantive Blender knowledge remains only in Tools_C.
Native and external-assisted workflows remain equal; Tripo stays optional.

## Baseline and exact revisions

| Repository | Start of this pass | Validated implementation / integration commit |
|---|---|---|
| Tools_C, main | 7acc2acd9db9b4ff0243b2e6df823c03e21e79aa | 963e9efeebb0a23393b355d7d8c0adfca5f9cc83 |
| Stickmans Duel, master | 88194aa0d6fc6f74c5d30ed1da752f348f3d1beb | 700acacb92162de11b81cc609b95977d15e3ec1c |
| Blender-MCP-Co, main | 9f057f93c9b9e573463786f6ffa8d70c36ea62fa | a995612a2e88c484d5a32e62e8076f9a1b5a5e53 |

These are the exact tested code revisions. This report and its evidence are sealed
in a subsequent documentation-only commit, which changes no tested implementation.
Its containing revision is available in the repository's history for this file;
the table is intentionally the reproducible code provenance, not a self-referential
hash of a document containing its own commit hash. No provenance depends on chat.
The original [V1 report](V1.md) now records its actual Tools_C commit; its historical
FAIL and version observations were not rewritten into present-day PASS.

Tools_C began clean. Blender had 42 dirty/untracked files; the game had five dirty
Resources/scenes. Full paths/status/hashes: [baseline](final-preflight.json).
All requested core docs, five skills, implementations and tests were read before
editing; additional roots' routers, profiles, status and relevant local skills/
resource consumers were inspected explicitly.

## Changes and preservation

- Tools_C implementation commit: `.tooling/profile.json`, README, docs/contracts,
  new docs/engines, V1 provenance correction, final-preflight evidence, bootstrap,
  checker, engine checker, existing test module and new engine test module (11 files).
- Game commit: profile review marker, appended Pulse evidence and two staged
  resource-reference ID lines. Working-tree repair replaces the empty embedded
  Resource with an ExtResource to the existing Green Fighter3DProfile, keeping the
  local resource ID. HEAD already held a valid typed link under a different ID;
  staging was built from HEAD plus only the two reference-ID replacements. User
  UID/serialization/default-value edits remain unstaged. No model/profile content,
  animation, controls, movement, combat logic or balance changed.
- Blender commit: only `.tooling/profile.json` review marker. Launcher, server,
  README, user assets, release outputs and both sets of routers were not changed.
- Audit seal: this report, final-evidence.json, final-preservation.json and the
  README link to this report. Audit-specific probe sources live inside evidence,
  not in universal runtime policy.

[Preservation evidence](final-preservation.json): all 42 baseline Blender files and
the four untouched dirty game files are byte-identical. Both GLBs, project.godot
and protected Active_hand are unchanged. P1 matches exactly the two authorized
byte replacements; all other bytes are retained. Pulse retains the entire previous
content and adds dated results. Canonical skills/references, provider notes,
manifest, engine probes, reader, synchronizer and compatibility mirrors have no
diff against baseline. Every commit used an exact staged allowlist, cached diff
inspection and whitespace checks; no blanket staging. Remaining dirty game data
is user work, not incomplete tooling changes.

## Engine identity and resolution

| Engine | Exact executable | Observed version |
|---|---|---|
| Godot | `F:\SteamLibrary\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe` | `4.7.2.stable.steam.ed1daf0bf` / runtime `4.7.2-stable (steam)` |
| Current Blender | `C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe` | `5.2.2 LTS` |
| Older installed Blender | `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe` | `5.1.1` |

V1 used an explicit older executable; it had no auto-resolution. The current
launcher config explicitly selects Steam Blender. Registry/install discovery,
direct --version, live process path and live Blender API agree on 5.2.2 LTS.
An early repeat on 5.1.1 passed but was not used as current-version acceptance.

Resolution now uses explicit argument → local environment configuration → bounded
Windows Blender installed-app discovery with actual numeric version comparison →
PATH fallback. Godot's configured path and environment resolution were exercised.
The Steam Blender wins over the older Foundation install. Missing explicit paths
fail instead of silently selecting something else; absent discovery is SKIP.
Every executed probe records executable/version/source/command/log/results.
Details and reproducible commands: [engine documentation](../docs/engines.md).

## Verification results

Full outputs, commands, logs, hashes and audit-specific probe sources are embedded
in [durable evidence](final-evidence.json); ignored raw copies also remain under
`.local/final/`. No result relies on an unavailable screenshot or chat-only log.

| Level / scope | Result | Observed criterion and limit |
|---|---|---|
| L1 Tools_C / game / Blender | PASS | check.bat: 9 / 11 / 9 check groups, zero WARN/FAIL; higher levels separately SKIP |
| Automated fixtures | PASS | 38 tests, zero failures/skips on this Windows host, Python 3.14.2 |
| Documentation links | PASS | All Tools_C Markdown and integration/router/profile/local skill Markdown; supported local-link subset, including final report; web URLs not fetched |
| L2 Godot, standalone import after repair | PASS | Exit 0, engine marker, no captured errors |
| L3 main-scene load after repair | PASS | 30 physics frames, 102 nodes, no captured errors (before repair: 93 nodes and three real errors) |
| L3 targeted profile repair | PASS | Both slots use typed/shared Fighter3DProfile; valid target fighter IDs, three hurtboxes each, zero setup errors |
| L2 current Blender import | PASS | 5.2.2 LTS imported both supplied GLBs without captured errors |
| Later Godot import with editor open | FAIL | Existing editor owned 127.0.0.1:6262; plugin logged listen error 22 despite exit 0; corresponding chained L3 correctly SKIP |
| Offline MCP loader | PASS | All 8 real loader list/read paths, 3 context queries and canonical render equality; registration stub explicitly offline |
| Live Blender canonical chain | PASS | Real MCP SDK/stdio server, 8 read aliases, 3 contexts, generated snippet executed by live TCP addon, canonical SHA-256 equality, scene unchanged |
| Live connector Blender / Godot editor | PASS | Both answered after initial tunnel HTTP 429 cleared; Godot confirmed exact project/executable/editor scene |
| Live Godot game session | SKIP | Editor was not playing; standalone L3 above is separate runtime evidence |
| L4 engineering review | PASS | Preservation, scope, dependency boundaries and anti-degradation reviewed below |
| L4 mesh/rig/animation/visual/input/feel | SKIP | Assets and controls unchanged; no manual or rendered comparison performed |
| Optional skill-creator quick_validate | SKIP | Core Python lacks PyYAML; external helper is not authoritative; no package installed |

The before-repair run reproduced missing/mismatched P1 profile and Nil fighter_id
with exit 0. The unchanged error detector overrode its success marker. The later
port-collision failure is also retained as FAIL, not relabeled PASS/WARN or filtered
away. No open user editor was stopped, and no MCP plugin was disabled. The earlier
standalone L2/L3 passes remain valid for the same unchanged source; concurrent
editor import remains an environmental limitation documented in engine instructions.

Blender observations match the previous import: Green 2 meshes / 2,918 vertices /
2 UV meshes / 65 bones / 7 Actions / 1 material; White 2 / 8,531 / 2 / 65 / 9 / 1.
The unused prompt-named White clip is still present; no asset cleanup was attempted.

## Safety, review state and live-path boundaries

Bootstrap generic/Godot/Blender, Unicode/space paths, idempotence, user-byte
preservation, malformed markers and symlink escape fixtures pass. Generated profiles
carry generated_unreviewed; missing legacy status also emits W_UNREVIEWED/WARN and
exit 0 when otherwise valid. Explicit reviewed suppresses only that warning; a
missing required file still fails. All three audited profiles are now reviewed.

Bundle generation was already non-destructive. New directory creates eight complete
contexts; existing empty and nonempty directories fail with NEW-directory guidance,
exit 1 and unchanged bytes. No force option or delete path was added. Router/mirror
drift blocks writes before mutation; exact checksums and all aliases remain checked.
Tests also cover malformed JSON, duplicate IDs, missing files, broken/escaped links,
protected hashes, invalid adapters, engine errors with exit 0, explicit missing
executables and batch exit-code propagation from outside Tools_C.

Live Blender used the existing installed MCP SDK through
`C:\Users\kosti\AppData\Local\Python\pythoncore-3.14-64\python.exe`, the unchanged
repository server in a temporary real stdio session and the running 5.2.2 addon.
No mocks were used for that live result. The modeling router's canonical context
returned SHA-256 `abf8b079848930859f59bcf9781f1aa283006b7e809e9003caf2dcf90b5fb1e5`;
the three-object scene before/after was identical. The temporary server closed normally.

**WARN — existing external deployment:** the tunnel-configured server at
`C:/Users/kosti/chatgpt-blender-mcp/` still has an older, project-specific modeling
skill (Version 1.0). Its basic scene connector works, but its installed knowledge
was not silently refreshed. The canonical live acceptance above proves the actual
repository implementation plus live bridge, not that stale deployed skill store.
For future deployment, use the documented new-directory bundle or reviewed router
refresh; do not invoke the launcher's destructive folder sync automatically.

Initial connector calls returned HTTP 429 and were recorded SKIP; after newly
running processes/listeners were observed, one retry succeeded. A supplementary
Godot file-read connector call rejected the valid res:// path at its schema layer;
that optional call remains SKIP. No admin-policy settings were altered. Godot's
successful editor status call is the live smoke criterion, not a claim that every
connector tool works. L1 and standalone runtime validation do not depend on MCP.

## Anti-degradation and closure

| Question | Finding |
|---|---|
| Requested feature improved? | PASS: explicit review warning, correct current Blender, durable provenance and real live proof |
| Another part became worse? | PASS within tested scope: 38 fixtures and byte-preservation checks; no unrelated source edits |
| Another view/silhouette/topology/deformation/animation worse? | SKIP: no asset edit or visual comparison |
| Routing diverged or canonical knowledge duplicated? | PASS: unchanged five canonical skills and exact eight aliases; no new editable copy |
| Compatibility mirrors diverged? | PASS for both repository locations; external deployment drift is explicitly WARN above |
| Bootstrap or sync became destructive? | PASS: creation/preservation/negative fixtures; existing output rejection unchanged |
| Project/provider policy leaked into core? | PASS: P1 assertion source is audit evidence only; provider and asset choices stay local |
| Verification weakened or errors hidden? | PASS: unchanged error detector catches both P1 and occupied-port failures at exit 0 |
| Complexity disproportionate? | PASS: one optional profile field plus bounded executable resolution; stdlib-only core |
| Runtime stability/responsiveness? | Profile initialization repaired and both slots checked; broader gameplay/input/performance SKIP |

Known WARNs: stale external skill deployment and the already-existing unused White
clip (observation, not an asset acceptance failure). New generated profiles warn
until consciously reviewed by design. Known environmental FAIL: simultaneous Godot
editor import's fixed port collision. Known SKIPs are enumerated above; none are
represented as successful visual/gameplay acceptance.

Deferred deliberately: external mirror deployment/restart, full visual/deformation/
animation and input/feel acceptance, future art/genre/skeleton/clip/root-motion/
combat/Active Hand choices, Asset Doctor, GUI, package manager, cloud, auto-updates
and additional providers. They are outside this bounded tooling acceptance.
No further feature work is required for this implementation pass; stop here.
