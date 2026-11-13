# Tools_C 4.2.1

Provider-neutral agent tooling for Blender, Godot and 3D projects. The main
Tools_C has [30 canonical skills](docs/skills.md), nine compatible legacy Blender
routes, reusable checkers and project integration. Tools_C Light is a separate
product. [Release 4.2.1](https://github.com/ConstantineJJ/Tools-C/releases/tag/v4.2.1)
contains the distributable toolkit and checksums.

Skills own procedures; project profiles hold replaceable project choices;
contracts declare machine-checkable invariants. The shared
[foundation](docs/foundation.md) defines scope, preservation, evidence and handoff.
Canonical procedures are read from this repository rather than copied into plugins.

## Install and check

Clone or extract the release into a permanent directory. Python 3.10+ is required;
the core tools use the standard library. Blender, Godot and live MCP dependencies
are needed only for their corresponding operations.

From the Tools_C directory in PowerShell:

```powershell
.\check.bat --self
.\bootstrap.bat --project "C:\path\to\project" --kind godot
.\check.bat --project "C:\path\to\project"
python -m unittest discover -s tests -v
```

Kinds: `generic`, `godot`, `blender`. Bootstrap creates project-local `.tooling`
files and one managed `AGENTS.md` block, preserving existing profiles and unrelated
content. Review the generated profile/contracts before explicitly marking the
profile `reviewed`; new profiles start `generated_unreviewed`.

Set `TOOLS_C_PYTHON` to a Python executable if needed. After moving Tools_C, update
the consuming project's `tools_root` or set `TOOLS_C_ROOT`. No global installation,
environment mutation or symlinks are required. The launchers propagate exit codes.

## Plugin and MCP

The [Tools_C plugin source](docs/tools-c-plugin.md) is one thin invocation
entrypoint with the supplied Tools_C icon. It discovers current connected tools
and routes to existing canonical contexts. Public source contains no personal
App bindings; private installation connects the operator's existing services.
It does not install or start engines or MCP services.

The [Blender MCP integration](docs/mcp-deployment.md) supports skill discovery,
stage-specific context, captures, deployment identity and bounded central checks.
Regenerate managed routers for an existing integration:

```powershell
python tools/sync_blender.py --project "C:\path\to\Blender-MCP-Co"
python tools/mcp_deployment.py --project "C:\path\to\Blender-MCP-Co"
```

The [4.2.1 adapter patch](adapters/blender-mcp-4.2.1.patch) wires the existing
server to the canonical helpers; it is not another MCP server. See
[deployment diagnosis](docs/mcp-deployment.md) for loaded/disk identity checks.
After server changes, restart the existing MCP process and refresh client metadata.
Local synchronization alone does not prove the live service has loaded changes.

## Capabilities and evidence

- [Skill catalog](docs/skills.md): domain modeling, reference reconstruction,
  surface transfer, sculpting, rigging, animation, export and Godot integration.
- [Anime character modeling](skills/blender-anime-character-modeling/SKILL.md):
  stylized humanoid form, faces, eyes, hair and clothing with scoped visual QA.
- [Agent Vision](docs/agent-vision.md): fixed/named-camera captures, silhouettes,
  world-space measurements, calibrated contour/landmark comparison, difference
  maps and localized findings through existing capture and QA helpers.
- [Blender evidence](docs/blender-evidence.md) and [QA receipts](docs/qa-receipt.md):
  scoped snapshots, comparable views, export checks and hash-bound evidence.
- [Project review](docs/project-review.md), [source bundles](docs/source-bundles.md)
  and [Mega tools](docs/mega-tools.md): optional traceability, source preservation,
  metadata discovery and behavioral-trial analysis.
- [Contracts](docs/contracts.md) and [engine checks](docs/engines.md): explicit
  invariants, stable diagnostics and bounded structural/import probes.

Structural, engine, runtime and visual results remain separate. Missing capability
is reported as SKIP with a reason. Generated ImageGen views/textures remain auxiliary
evidence under the existing reference workflow; they do not establish hidden geometry.
Silhouette metrics require declared masks and comparable camera/pose setup.
Automatic metric success does not certify artistic likeness, deformation or gameplay.

The repository includes functional documentation, tests and minimal test fixtures.
Internal reports, task histories, local state and account-specific connection files
are excluded from the current distribution. Schema versions and historical skill
provenance are independent of the toolkit release version.

Architectural reference: [ArcEngine](https://github.com/xaidan777/ArcEngine), audited
at commit `70c777242c1b9dc8b2525394450472b826491c4b`. Implementation here is original;
no ArcEngine code was copied. ArcEngine is MIT, copyright 2026 Tearevo. Blender
procedures were migrated from the user's local pipeline with authorization;
source hashes/versions remain in [manifest.json](manifest.json).
