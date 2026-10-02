# Tools_C architecture 4.0.1

Central, provider-neutral agent tooling for Godot/Blender/3D projects.
[Current project state](Project-pulse.md) records the latest completed work, checks,
open issues and next actions.
[AGENTS.md](AGENTS.md) routes to twenty-one canonical skills. A shared
[foundation](docs/foundation.md) owns scope, preservation, evidence and handoff
semantics. Rigging/skinning, animation, GLB export validation and Godot asset
integration now have separate owners. Nine legacy Blender names remain compatible.

Four production skills coordinate a playable [mechanic gym](skills/production-mechanic-gym/SKILL.md),
[parallel worktrees](skills/production-subagent-worktree/SKILL.md), a representative
[lookdev gate](skills/production-lookdev-gate/SKILL.md) and compact
[project state and regression gates](skills/production-project-state-gates/SKILL.md).
They guide specialist work; project profiles, contracts and the applicable
Blender/Godot skills still own concrete requirements and checks.

Skills describe how to work. Project profiles hold replaceable local choices.
Contracts declare invariants, checkers prove bounded properties, and project Pulse
files record observed status. A future character, genre or model generator does
not require changing the core. Native Blender and external-assisted production
are equal paths; Tripo is an optional source note.

Requirements: Python 3.10+. Tools_C runtime/checkers use only the Python standard
library; no third-party packages to install. Its own contracts/checkers are
authoritative. Optional external validators (including skill-creator quick_validate)
have their own dependencies; their absence does not invalidate Tools_C checks.
Engine probes, full live MCP service dependencies and human review are separate.
Current migration and evidence: [v4 report](TOOLS_C_V4_MIGRATION_REPORT.md).
Historical acceptance: [V1 final report](reports/V1_FINAL.md) and [V1 report](reports/V1.md). Godot and Blender are optional for
L1 and required only for their applicable engine/runtime checks.

From Tools_C in PowerShell:

```powershell
.\check.bat --self
.\check.bat --project "E:\MyCreations\Stickmans_Duel\stickmans-duel-project"
.\check.bat --project "E:\MyCreations\Blender-MCP-Co"
python -m unittest discover -s tests -v
python tools/check.py --project "C:\path\to\project" --json
```

Set TOOLS_C_PYTHON to an explicit Python executable if `python` is unavailable.
The launchers work from another working directory and propagate failure codes.

Connect a future existing folder:

```powershell
.\bootstrap.bat --project "C:\path\to\project" --kind godot
```

Kinds: generic, godot, blender. Bootstrap creates only `.tooling` files and appends
one managed AGENTS block; it preserves existing profiles and unrelated router bytes.
New profiles carry `review_state: generated_unreviewed`; checks emit WARN with exit 0
if there are no failures. Inspect and specialize the profile/contracts, then set
`review_state` to `reviewed` explicitly. Missing legacy status also warns; review
never disables invariant checks. Project choices belong in `.tooling/profile.md`
and profile.json, with machine-checkable invariants in contracts.json. For a moved
Tools_C folder, update tools_root or set TOOLS_C_ROOT; regenerate Blender routers
with `python tools/sync_blender.py --project "C:\path\to\Blender-MCP-Co"`.
No global installation, environment-variable mutation or symlinks are required.

Blender MCP compatibility: list/read/context keep the nine legacy names. The
integration server resolves canonical text on each read; direct canonical names
are also readable. `get_skill_context` selects stage owners and reports truncation
as incomplete. `capture_viewport` returns PNG evidence and metadata; `deployment_info`
reports loaded/disk identity and tool-schema/context digests. The generic Python
bridge applies non-executing syntax preflight before Blender execution.

Generate both managed router trees (edited or stale copies fail before writes):

```powershell
python tools/sync_blender.py --project "C:\path\to\Blender-MCP-Co"
python tools/mcp_deployment.py --project "C:\path\to\Blender-MCP-Co"
python tools/sync_blender.py --bundle "C:\path\to\NEW-package"
```

Offline packages contain generated context, not editable authorities. Existing
bundle directories fail without writes. Router hashes include current canonical
context identity. The integration launcher's current behavior is read-only router
verification, not the historical destructive sync. After server changes, the normal
tunnel/MCP restart loads code; connector schema refresh is a separate boundary.
See [deployment diagnosis](docs/mcp-deployment.md). Local sync is never live PASS.

Use [Blender evidence tools](docs/blender-evidence.md) for deterministic snapshots,
fixed/current views and isolated export/fresh-import validation. Images require
review; structural checks do not certify visual quality. Architecture 4.0 keeps
JSON schema_version 1 and historical lesson/report versions unchanged.

L1 structural/contracts/static checks: [format, codes, limits and adding rules](docs/contracts.md).
L2 engine/import probes: [selection, commands and evidence](docs/engines.md).
L3 requires an explicit runtime behavior probe; L4 requires actual engineering/
visual evidence via [verification](skills/verification/SKILL.md). Missing capability
is SKIP with reason. Import success cannot certify appearance or gameplay feel.
Tools_C does not replace engines, MCP services, project design or human acceptance.

Add repeatable judgment-based lessons to the owning skill, using its existing
Pitfalls / Lessons Learned format. Add reliable checks to contracts instead of
another prose prohibition. Update obsolete active rules and tests together; use
Git history rather than duplicate archives.

Architectural reference: [ArcEngine](https://github.com/xaidan777/ArcEngine), audited
at commit 70c777242c1b9dc8b2525394450472b826491c4b: router, verification/render
conventions, check runner, instancing and lint tests. Implementation here is original;
no ArcEngine code was copied. ArcEngine is MIT, copyright 2026 Tearevo. Blender
procedures were migrated from the user's local pipeline with authorization;
original source hashes/versions are retained in [manifest](manifest.json).
