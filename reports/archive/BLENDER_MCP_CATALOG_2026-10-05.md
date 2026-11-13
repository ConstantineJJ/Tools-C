# Blender MCP catalog and metadata — 2026-10-05

Implemented user-approved proposal points 1, 3, 4 and 5. Point 2 was excluded:
the user refreshed permissions/connection and demonstrated all seventeen tools.

## Changes

- All seventeen existing tool names and input schemas are retained. Every tool
  declares four explicit impact/idempotency hints. Six reads: list_skills,
  read_skill, find_skills, get_scene_info, get_skill_context, deployment_info.
  Eleven writes include capture artifacts and the mixed status/cancellation tool.
  Delete/overwrite, shared material/slot replacement, active-camera replacement,
  arbitrary Python and cancellation disclose destructive effects. Arbitrary Python
  and unrestricted save destinations disclose open-world access. Existing bridge
  syntax/safety checks are unchanged.
- Eight empty descriptions are filled. Context routing descriptions/server
  instructions cover the actual Blender domains and document continuation.
  Camera/material/save side effects are explicit.
- list_skills adds 25 canonical owners with separate alias metadata. Legacy
  skills/count/skills_dir still enumerate nine routers, preserving existing callers.
  find_skills returns unique readable owner IDs, prioritizing names/aliases/titles,
  then purpose metadata, then owner-entrypoint text. It does not expand nine shared
  contexts. Full catalog/path/link validation remains in place. No persistent cache
  can hide changed source metadata.
- Cube/sphere descriptions and shared server instructions identify starting
  primitives/intentional simple shapes and direct developed organic forms toward
  width/depth profiles, bends, taper and continuous transitions. No new primitive
  ban or extra tool was introduced.
- deployment_info separately fingerprints descriptions/annotations while keeping
  the existing input-schema digest. Tools_C owns the provider-neutral catalog
  helper; Blender-MCP-Co owns its MCP adapter. Constantine Hub was not changed.

## Measured local search sample

| Query | Before, seconds | After, seconds | Canonical results |
|---|---:|---:|---|
| anime | 1.7405 | 0.2003 | blender-anime-character-modeling |
| vegetation | 1.8792 | 0.2268 | blender-vegetation |
| Face Sets | 2.2268 | 0.2499 | blender-sculpting |

Each old query expanded nine contexts totaling 281,128 characters. The new search
expands none and returns one relevant owner for each of these three examples.
These are sequential measurements on this checkout, not a production latency SLA.

## Acceptance and limits

- Standard-library suite: 126 PASS. Final focused catalog tests: 9 PASS.
  Public distribution catalog compatibility fixture: PASS.
- Tools_C L1: 32 PASS / 0 WARN / 0 FAIL; integration L1: 9 PASS / 0 WARN / 0 FAIL.
  L1's three engine/runtime/visual system entries remain SKIP by design.
- Actual disposable MCP SDK session: 14 PASS, 1 SKIP. All seventeen names and
  input schemas match the previous baseline; hints/descriptions, 25-owner catalog,
  nine legacy aliases, search→read, mixed routing and metadata hash verified.
  Scene comparison is SKIP because the Blender addon is unavailable.
- Twenty-seven unrelated integration files and the canonical teaching blend/seven
  PNG hashes are unchanged. No production scene/model, Hub source or release was edited.
- Hub/Blender/tunnel processes and the loopback tunnel listener were absent at
  verification. Source changes will load on the next normal Hub/MCP start.
  External metadata/UI acceptance remains SKIP until that startup and client refresh;
  expected grouping is six Read and eleven Write. No services started implicitly.

## Live connector acceptance after startup

After the user started MCP and refreshed the plugin, the actual Blender_MCP
connector verified the fresh server: loaded/disk SHA-256 match, no restart needed,
all 17 commands, six read-only hints and eleven writes. The schema and metadata
digests match the tested disposable SDK server. Discovery returns 25 canonical
owners and nine aliases; vegetation search returns its single owner, and
search-to-read plus mixed architecture/anime context delivery succeed.

Two successful Blender scene snapshots are identical (three objects, frame 1).
The earlier scene/connector SKIP is now closed for these scoped read-only checks.
Client metadata remains WARN: this existing chat still exposes the old tool
descriptions. Updated server metadata is confirmed; the client's visual Read/Write
grouping was not inspected and remains a separate acceptance boundary.

[Live connector evidence](blender-mcp-live-2026-10-05.json).

[Original machine-readable evidence](blender-mcp-catalog-2026-10-05.json).
Sources: [OpenAI tool annotation reference](https://developers.openai.com/plugins/reference#annotations),
[tool descriptions/impact guidance](https://developers.openai.com/plugins/plugin-guidelines),
[metadata refresh](https://developers.openai.com/plugins/deploy/connect-chatgpt).
