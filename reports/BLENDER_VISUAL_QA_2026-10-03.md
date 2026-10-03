# Blender Visual QA capture and feedback repair — 2026-10-03

## Observed problems

- The integration server defines `capture_viewport`, but the connector catalog exposed in this task omits it. The v4 migration report already recorded this discovery gap; a generated router update does not refresh that catalog.
- Initially the connector returned `McpServerError: Session terminated` and the local bridge was unavailable. The user then started Blender MCP; scene access recovered. The first Python fallback produced a PNG but no image content because the running adapter predated the change. A targeted `blender-local` tunnel/MCP restart loaded the update; actual connector capture now returns a verified image. These observed failures do not prove the exact failure in the user's earlier unnamed test.
- Canonical contexts previously included a link to the evidence document without its actual capture/fallback recipe. No alternative image-return path existed in the ordinary Python tool.

## Changes

- All canonical Blender and legacy entry contexts now load `docs/blender-evidence.md` directly. The established two-argument reader API, ownership routes and nine alias names remain stable; generated routers were regenerated through the canonical generator.
- Pipeline core, QA and refinement explicitly require capture → open actual PNG → identify defect → scoped correction → capture/open AFTER with comparable settings. Read-only QA stays read-only. Missing tooling triggers applicable fallback attempts; a required unrun visual gate remains open.
- `execute_blender_python` can return verified image content for a canonical managed capture, alongside its unchanged structured result schema. The small integration glue delegates verification to `tools/mcp_capture_response.py`: managed directory, matching manifest, bounded PNG dimensions and SHA-256; arbitrary returned paths are not attached. Ordinary Python responses and syntax preflight remain unchanged.
- `tools/blender_capture_file.py` adds a local fallback when MCP is unavailable: render an explicitly saved current candidate in isolated background Blender, keep the source file unchanged, verify image/hash/completion marker and preserve logs. It uses Blender's render operation and Render Result through the existing helper. These are rendered model views, not an OS screenshot of Blender chrome. Unsaved live changes and script-dependent appearance require separate consideration.
- No dedicated contracts pass, profile/canonical-manifest/AGENTS changes, production scene replacement or unrelated launcher changes. Only the verified blender-local tunnel/MCP subtree was restarted to load the new Python image adapter; Blender and the other tunnel were preserved.

## Verification

- Tools_C and Blender-MCP-Co L1: each **9 PASS / 0 WARN / 0 FAIL**.
- Regression suite: **63/63 PASS**, no errors/failures/skips. Covers output reuse, failed renderer, managed path containment, manifest/hash/dimension mismatch, no automatic visual acceptance and fallback context delivery.
- Real Blender **5.2.2 LTS** offline captures: four actual 512px PNGs, BEFORE/AFTER front and side. Each source-file hash remained unchanged by capture. Same frame, mode, resolution, framing and per-view camera matrix before/after. Only `Head` object transform changed in the disposable correction fixture.
- **VISUAL PASS for the bounded feedback criterion**: the agent opened all four images, diagnosed the lateral head displacement from the front, corrected it, then reopened both AFTER images. The side view confirms that one view alone concealed the defect. This does not accept a production asset or its materials, deformation, animation or engine appearance.
- MCP SDK adapter probe **PASS**: a real rendered PNG returned as one image; ordinary structured Python response preserved; invalid capture rejected. Blender bridge is **stubbed in this compatibility probe**, so it proves response behavior, not live transport.
- Disposable stdio deployment **PASS**: 15 tools, all nine canonical legacy context hashes, loaded/disk server identity and syntax rejection. Additional stdio routing smoke **11/11 PASS**, including eight domain owners and review/retopo/surfaces; every context matched local bytes and included the actual fallback recipe. All eight default-budget contexts remain untruncated.
- Actual connector/live capture **PASS after user startup and targeted adapter reload**: Python fallback returned one verified image and unchanged structured metadata; the agent inspected it. Direct MCP capture returned/verified five PNGs (front/side/back/three_quarter/current), all opened and inspected; source snapshot and selection/active/camera/scene/filepath matched afterward. Actual connector routing additionally passed **11/11 full-byte context comparisons**. The connector still omits the named capture tool; the tested Python fallback works through the existing tool entry.
- Unrelated dirty integration files verified byte-for-byte against the pre-change baseline. Recovery files: `C:/Users/kosti/AppData/Local/Temp/Tools_C_visual_qa_20261003`. Full local logs/candidates: `.local/visual-qa-20261003`.

## Inspected images

| BEFORE front | AFTER front |
|---|---|
| ![Head displaced above the shoulder](visual-qa-2026-10-03/before-front.png) | ![Head centered above the torso](visual-qa-2026-10-03/after-front.png) |

Side views: [BEFORE](visual-qa-2026-10-03/before-side.png), [AFTER](visual-qa-2026-10-03/after-side.png).
Exact image hashes, reviewer observations and settings: [review.json](visual-qa-2026-10-03/review.json).
MCP context comparisons: [routing.json](visual-qa-2026-10-03/routing.json).

## Live evidence and next stage

[Actual connector capture](visual-qa-2026-10-03/live-python-fallback.png), [live capture/state evidence](visual-qa-2026-10-03/live-capture.json), [actual connector context comparisons](visual-qa-2026-10-03/live-routing.json). Direct named capture was tested through disposable stdio to the running Blender; the Python alternative was tested through the actual ChatGPT connector. A connector catalog refresh is optional for discovering the named tool; visual acquisition already works through the tested fallback. Dedicated eight-domain contracts remain a separate, unstarted stage.
