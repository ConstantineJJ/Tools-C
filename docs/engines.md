# Explicit engine probes

L1 never starts an engine. Opt in with `--godot [EXE]` or `--blender [EXE]`;
omitting EXE, or using `auto`, enables resolution for that engine only.

Resolution order:

1. Explicit executable argument, resolved relative to the calling directory.
2. For auto: process environment `TOOLS_C_GODOT` / `TOOLS_C_BLENDER` (local configuration).
3. Blender on Windows: existing versioned Blender Foundation folders plus Blender
   InstallLocation entries in user/system 32/64-bit uninstall registry views.
   Run each candidate's `--version`, select the highest reported numeric version;
   deterministic path order breaks ties. This includes registered Steam installs.
4. PATH fallback: `godot`, then `godot4`; or `blender`.

Explicit/configured missing executable, unreadable discovered version or version
timeout is FAIL; there is no silent substitution. No discovery result is SKIP with
instructions for configuration. Discovery is bounded, not a drive scan; portable,
unregistered, prerelease or other preferred installations should use an explicit
path. Newest installed is a discovery policy, not a claim about project compatibility.
Godot installations outside PATH require explicit configuration. No global settings
or third-party launcher configuration are modified.

```powershell
$env:TOOLS_C_GODOT = 'C:\your\Godot\godot.exe'
python tools/engine_check.py --project 'C:\your\project' --godot auto --runtime-scene res://scenes/main.tscn
python tools/engine_check.py --project 'C:\your\project' --blender auto --asset Assets/character.glb
```

Each executed probe records the resolved executable, version, resolution source,
exact command, exit code, log and observed marker/error evidence in JSON stdout.
Capture stdout to preserve machine-readable evidence. Full logs default to the
ignored `.local/engine/`; use `--logs` for separate runs. Version queries time out
after 15 seconds per candidate, probes after 120 seconds.

Godot import is L2. The explicit scene-load L3 smoke instantiates the selected scene
and advances 30 physics frames; it does not test all gameplay or input. Blender uses
a factory background process, disables autoexec, imports supplied GLB/glTF/blend
inputs and reports structure without saving. No assets means API availability only.
Zero exit without the required marker, or any captured engine/script/Python error,
is FAIL. L4 visuals/deformation/animation/feel remain SKIP unless separately observed.

An open editor may already own a project's fixed MCP port. A second headless editor
then fails the import probe when that plugin logs an error, even with exit 0. Preserve
that diagnostic; do not filter it out, disable the user's plugin or stop their editor
automatically. Run standalone import when that project's editor has been closed,
or report the port conflict separately from an earlier successful import/runtime run.
