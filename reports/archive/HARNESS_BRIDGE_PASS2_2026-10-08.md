# Pass 2 — Harness, Blender bridge lifecycle and reports cleanup

**Date:** 2026-10-08. **Scope:** Tools_C contracts/checkers/tests and
Blender-MCP-Co Blender-side bridge source/installed add-on. This pass implements
structured evidence/checks, not the deferred global visual QA redesign.
No release was published and no commit was created.

## 1. Reference Surface Transfer record schema v2

- `tools/surface_transfer.py` supports **schema v1 unchanged** plus strict
  schema v2 `face_strategy` for new face records.
- v2 requires explicit strategy DIRECT / RECONSTRUCT_THEN_LAYER / HYBRID,
  per-region observed/inferred provenance, visibility, landmarks, protected
  markers, occluder/layer/mask and reason.
- DIRECT refuses invented face detail; RECONSTRUCT needs masked regeneration
  and inferred regions; HYBRID requires both preserved and inferred regions.
  Fully hidden source pixels cannot be declared ORIGINAL; visible features
  cannot be silently regenerated; all mask/prompt lineage rules remain.
- Docs updated under `skills/blender-reference-surface-transfer/`.
  These assertions are **structural** and do not imply pixel-level
  occlusion correctness, reconstructed identity or invisible seams.
- `tests/test_surface_transfer.py` gains positive/negative v2 cases and
  retains existing v1 fixtures and their compatibility.

## 2. Character proportions within the existing Model Contract

- No second proportion manifest, fixed generic body canon or Model Contract
  schema migration. The existing dimensions, ratio and anchor constraints
  remain authoritative.
- `tests/test_model_contract.py` now exercises distinct skull-height,
  outer-hair-height and full-height envelopes, one reviewed ratio and a
  negative out-of-source-range ratio. Explicit contract revision and
  predecessor proof are respected.

## 3. Blender MCP timer and expired queue lifecycle

**Root cause revalidated:** Installed Blender 5.2.2 add-on originally used a
nonpersistent `process_queue` timer and trusted `_state["timer_active"]`
instead of checking `bpy.app.timers.is_registered()`. Commands timed out
despite apparent TCP/Hub readiness, and queued expired mutations could later
execute.

**Patch:** `E:/MyCreations/Blender-MCP-Co/mcp-server/chatgpt_blender_mcp.py`

- Persistent queue timer and persistent load_post recovery.
- Start-on-running path checks registration, not only cached flag.
- Queue item lock/started/cancelled state avoids replay of jobs timed out
  **before** execution, returning `CANCELLED_BEFORE_EXECUTION`.
- A timed-out command that **has begun** returns `UNKNOWN_EXECUTION`;
  it may complete and must be reconciled in the real scene before retry.
- Add-on source staged, AST/compile checked, isolated queue test passed,
  then deployed with a byte-for-byte pre-patch backup.
- Installed add-on:
  `C:/Users/kosti/AppData/Roaming/Blender Foundation/Blender/5.2/scripts/addons/chatgpt_blender_mcp.py`
- Backup:
  `chatgpt_blender_mcp.py.backup-2026-10-08-pass2` in the same folder.
- Running session was patched without restarting the bridge; on-disk installed
  source matches the staged canonical file.

**Actual live test:** Opened
`D:/Desktop/My Labarotory/TESTS/Agent_Red7.blend` by Blender MCP
`bpy.ops.wm.open_mainfile(load_ui=False)`.
Follow-up `get_scene_info` from a **separate RPC** returned scene
`Agent_Red7`, 477 objects; queue timer remained registered, handler
registered, running flag true and pending queue 0. Model original SHA-256:
`f71ee07a612aad4793de69ab86e7bb2c50116ff22092dabf959b532985b66221`;
matched 7 October delivery; `bpy.data.is_dirty=False`.

Dedicated `Blender-MCP-Co/tests/test_bridge_lifecycle.py` covers start,
load repair, cancelled-before-start and already-started unknown execution,
plus normal job processing (5 tests PASS).

## 4. New health check and mandatory handoff protocol

- `Tools_C/tools/blender_bridge_health.py` provides an executable,
  read-only receipt for live interpreter, timer registration, connected
  loaded add-on and expected file/scene.
- Foundation now requires a **new** health RPC plus separate
  `get_scene_info` after file-load/reset operations; unknown-completion
  mutations must be reconciled before resending.
- Live positive receipt after opening Red7: all seven checks PASS;
  intentional wrong-scene negative returned FAIL.
- `tests/test_blender_bridge_health.py`: four tests PASS for true health,
  stale/false state, file mismatch and missing load handler.

## 5. Reports cleanup

Active `E:/MyCreations/Tools_C/reports` retained October work,
current Model Contract / transfer evidence and all four release
publication records under `reports/releases/`.

**Archived without data loss** nine September V1/v4 items:
`V1.md`, `V1_FINAL.md`, `engine-evidence.json`,
`final-evidence.json`, `final-preflight.json`,
`final-preservation.json`, `preflight.json`,
`preservation.json`, full `v4/` folder.
Destination:
`E:/MyCreations/Tools_C/.local/archived_reports/2026-10-08/`.
`manifest.json` maps original and destination paths.
Removed redundant `reports/model-contract-workflow/macro-probe.blend1`
after preserving `macro-probe.blend`.

L1 initially exposed a stale `TOOLS-JSON` dependency on archived
`reports/preflight.json`. Removed this historical-only required
check; README no longer links moved V1 files. No active contract
should require a dated output report for its own validity.

## Verification receipts

| Gate | Status |
|---|---|
| 19 scoped Python regression cases (6 transfer, 4 Model Contract, 4 bridge health, 5 addon) | **PASS 19/19** inside running Blender Python |
| Tools_C self L1 after changes/cleanup | **50 PASS / 0 WARN / 0 FAIL** |
| Live Blender MCP reopened Agent_Red7 | **PASS**, 477 objects, next RPC returned |
| Read-only bridge health (correct file and scene) | **PASS** |
| Negative bridge-health scene mismatch | **FAIL expected** |
| Live canonical Skills delivery | PASS with 85k context budget; single-domain routes transfer/character. Low 35k context cap intentionally returned not-complete. |
| Full Python regression discovery / all 201 prior tests | **NOT RUN**; not claimed |
| Cold Blender restart and repeated open/reset/timeout stress | **NOT RUN** |
| Actual texture transfer, reconstructed face appearance and seam visual QA | **NOT RUN** |
| Cross-cutting ±45° viewing / L4 global QA redesign | **DEFERRED to Pass 3** |

No system-wide source export, user project mutation or Git publication was requested.
The installed bridge and repo-local source are now modified; restart will load the
new on-disk add-on but requires a separate cold-start test. Keep versioned backup
until that acceptance is complete. All changes were bounded to this pass.
