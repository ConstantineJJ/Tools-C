# Working-tree source bundles

Use `tools/source_bundle.py` before a scoped migration when HEAD is not the full
application source. It reads Git-visible working files, including untracked files,
and copies only an explicit allowlist into a new external directory. It never
stages, commits, resets, cleans, restores deletions, changes ignores, contacts a
remote, loads project code or manages application/tunnel processes.

This is a scoped source receipt, not another task ledger, requirements packet,
deployment manager or replacement for project-review/deployment tools.

## Inventory, select, capture, verify

Run from Tools_C. Substitute the observed project and external evidence directory:

```powershell
$sourceProject = 'E:/MyCreations/Constantine-Hub'
$evidenceRoot = 'E:/MyCreations/Work_Utility/patch-c-source'
New-Item -ItemType Directory -Path $evidenceRoot -Force | Out-Null
python tools/source_bundle.py inventory --project $sourceProject
```

Inventory lists HEAD paths, index paths and non-ignored untracked paths, with
HEAD/index blob IDs and modes, two-character Git status and origin. HEAD is
provenance, never an assumption that tracked files are the entire app. Ignored
files are not implicitly admitted. Use the exact Git worktree root; linked
worktrees and unborn repositories are supported. Optional Git locks/fsmonitor
are disabled; the source index is not updated.

Review the inventory and write `allowlist.json` as a JSON array of **exact files**:

```json
[
  "apps/ConstantineHub/ConstantineHub.csproj",
  "apps/ConstantineHub/Program.cs",
  "apps/ConstantineHub/Adapters/Blender/BlenderAdapter.cs"
]
```

These are examples, **not a complete Hub allowlist**. Include required source
dependencies, tests, assets and build/CI definitions after inspection. Do not infer
closure from `.csproj` alone. Review omitted paths; exclude build products, caches,
logs, secrets and unrelated work deliberately. There is no secret scanner or
automatic publication approval. Directories, globs, unknown paths and ignored
files are rejected rather than silently expanded.

```powershell
python tools/source_bundle.py capture --project $sourceProject --allowlist "$evidenceRoot/allowlist.json" --output "$evidenceRoot/hub-source"
python tools/source_bundle.py verify --bundle "$evidenceRoot/hub-source"
python tools/source_bundle.py verify --bundle "$evidenceRoot/hub-source" --project $sourceProject
```

Capture reads current raw bytes. HEAD/index versions never replace working bytes.
Selected tracked files absent from the working tree become `absent` records and
are not restored. An untracked application remains untracked. The original
index/staged work and Git history stay in the source repository; the bundle is
not their backup.

Output must be new, its parent must exist, and it must be outside Git repositories
and their metadata. It contains only `source/` and completion `manifest.json`.
The manifest records source root/HEAD/branch, full index/status fingerprints,
per-file origin/HEAD/index/status, presence, size and SHA-256. It is written last
after repeated source checks. A failed/interrupted external output may remain
without a valid completion manifest; no automatic deletion/overwrite/resume occurs.
Inspect it, then use a new output for another attempt.

## Meaning of verification

- `verify --bundle` checks strict manifest fields/checksum, exact payload file
  membership and bytes. It never opens the recorded source root or runs Git.
- Explicit `--project` also checks current HEAD/branch/index/status and selected
  bytes. Drift returns `E_STALE`; no silent receipt refresh. Even a new unrelated
  Git-visible path makes this conservative check stale. Ignored files and bytes
  of unselected already-dirty files are outside its preservation claim.
- `SOURCE_BUNDLE_PASS` proves scoped integrity, not complete build inputs,
  a successful build, runnable Python/.NET environments, installed-app behavior,
  MCP compatibility, rollback or cutover readiness.

SHA-256 is a checksum, not a signature/authority. A source bundle is not
automatically redistributable. Git modes remain provenance; OS permissions,
ACLs and timestamps are not restored. There is no checkout, overlay/apply,
migration mapping or implicit move into another repository. Keep original
Git history/attribution in the later migration plan.

## Boundaries and errors

The tool rejects traversal, absolute/ADS/backslash paths, Git metadata payloads,
common Windows reserved/ambiguous names, case/file-directory collisions, symlinks,
junctions/reparse points and non-regular files such as submodule directories.
Use a stable, trusted workspace: this is not a hostile-filesystem sandbox,
OS lock or atomic snapshot across repositories.

Limits: 10,000 Git-visible/selected files, 32 MiB per source file, 256 MiB selected
bytes, 8 MiB JSON and 30 seconds per Git read. Git enumeration is collected before
the count limit is checked; this is not a hard process memory cap. Inherited
`GIT_*` overrides are cleared: the tool inspects the normal repository index,
not a caller-supplied alternate index. No filters/checkout commands run.

CLI emits JSON without source bodies. Exit `0` means the named source operation
succeeded, `1` is invalid input/integrity/stale/I/O failure, `2` is CLI usage.
Errors include `E_SCOPE` (unknown/ignored/extra paths), `E_PATH`, `E_LIMIT`,
`E_OUTPUT`, `E_STALE`, `E_HASH`, `E_BUNDLE`, `E_GIT`, `E_SCHEMA`, `E_JSON`, `E_IO`.

## Patch C use

Keep independent Hub and Blender-MCP-Co allowlists/bundles and reverify both before
C1. Preserve untracked `apps/`, adapter/add-on/tests and selected modified sources.
Keep `.gitignore` and user Git state unchanged. Tooling preparation does not
require committing the worktree or switching the working tunnel.

Use the existing [deployment audit](mcp-deployment.md) for resolver/router and MCP
checks, [project review](project-review.md) for an explicit old→new→consumer→test
map, and [contracts](contracts.md) for L1. A bundle does not create these mappings
or claim their acceptance. Builds and staging probes are separate authorized
steps using the captured files in isolation.
