# Tools_C 4.1.0

Twenty-seven reusable skills and a provider-neutral harness for Blender, Godot
and 3D production. Browse the [skills catalog](docs/skills.md) for ownership,
activation and handoff boundaries.

[Download v4.1.0](https://github.com/ConstantineJJ/Tools-C/releases/tag/v4.1.0)
with the portable ZIP, checksums and extracted-package verification.
See [release notes](docs/release-v4.1.0.md) for changes and compatibility.

[Anime character modeling](skills/blender-anime-character-modeling/SKILL.md) adds humanoid anime/manga and chibi forms,
face/eye/hair decisions and renderer-compatible visual QA, while preserving
specialist topology, surface, rigging and delivery ownership.

[Form development](skills/blender-pipeline/references/techniques/form-development.md)
adds concrete shape methods, five recipes and an editable Blender comparison
scene with seven inspected examples. Early lookdev, compact domain entrypoints,
whole-document context receipts and tested geometry/contact/job helpers support
scoped corrections before detail growth.

[Visual reference reconstruction](skills/visual-reference-reconstruction/SKILL.md)
requires a provenance-aware PASS 0 packet before complex image-based modeling.
[Robot and mechanism modeling](skills/blender-robot-mechanism-modeling/SKILL.md)
consumes it through geometry and clay gates before materials and wear.

Skills explain how to work. Project profiles hold local choices; declarative
contracts protect invariants; bounded checkers report evidence. The shared
[foundation](docs/foundation.md) defines scope, preservation and acceptance.
Nine legacy Blender names resolve to their canonical owners through generated
compatibility routers. Research references belong to their skills.

## Requirements and checks

Python 3.10+; core runtime and L1 checkers use only the standard library.
Blender, Godot and the MCP SDK are needed only for their applicable opt-in probes.

```powershell
.\check.bat --self
python -m unittest discover -s tests -v
.\check.bat --project "C:\path\to\project"
python tools/check.py --project "C:\path\to\project" --json
```

Set TOOLS_C_PYTHON to an explicit Python executable when needed. Launchers work
from another working directory and propagate failure codes.

L1 checks structure, declared contracts and links. [L2 probes](docs/engines.md)
check engine loading; L3 needs an explicit runtime probe; L4 needs inspected
visual or behavior evidence. Missing capability is SKIP with its reason.
See [contract formats and diagnostics](docs/contracts.md) and
[verification](skills/verification/SKILL.md).

## Connect a project

```powershell
.\bootstrap.bat --project "C:\path\to\project" --kind blender
```

Kinds: generic, godot, blender. Bootstrap creates local .tooling files and one
managed AGENTS block in the target project, preserving existing profiles and
unrelated text. Generated profiles start with review_state: generated_unreviewed.
Inspect and specialize profile.json, profile.md and contracts.json, then mark the
profile reviewed. Review never disables invariant checks.

Resolve tools_root from the project's .tooling/config.json or set TOOLS_C_ROOT.
For a moved installation, update that pointer and regenerate compatibility
routers. No global installation, persistent environment changes or symlinks
are required.

## Blender integration and visual evidence

```powershell
python tools/sync_blender.py --project "C:\path\to\Blender-MCP-Co"
python tools/mcp_deployment.py --project "C:\path\to\Blender-MCP-Co"
python tools/sync_blender.py --bundle "C:\path\to\NEW-package"
```

Edited or stale routers fail before writes. Existing bundle folders reject
mutation. Offline bundles contain generated context; canonical ownership stays
in this package. A separate compatible Blender MCP integration supplies the
running service. See [deployment diagnosis](docs/mcp-deployment.md).

The runtime routes focused tasks and preserves all nine legacy names.
get_skill_context reports truncation as incomplete. The Python bridge applies
syntax preflight before Blender execution.

[Blender evidence tools](docs/blender-evidence.md) provide deterministic
snapshots, render-window captures, a file-capture fallback and export/import
probes. Agents must inspect returned images, correct observed defects and capture
again. A saved image alone does not prove visual acceptance.
[Posteffects and polishing](skills/blender-posteffects-polishing/SKILL.md) owns
late surface finishing and requested image effects, with explicit handoffs to
UV/bake, sculpt, rigging, export and target-engine owners.

## Maintain the pack

Keep replaceable asset names, styles and budgets in project profiles.
Add repeatable judgment lessons to the owning skill; add reliable invariants to
contracts with positive and negative cases. Update obsolete rules and tests
together. [Harness architecture](docs/architecture-v4.md) explains the boundaries.

The [manifest](manifest.json) retains original Blender procedure source
hashes and versions. Architectural reference: [ArcEngine](https://github.com/xaidan777/ArcEngine)
at commit 70c777242c1b9dc8b2525394450472b826491c4b. Implementation here is original;
no ArcEngine code was copied. ArcEngine is MIT, copyright 2026 Tearevo.
