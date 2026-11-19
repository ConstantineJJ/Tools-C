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

## Godot whole-project, scenario and capture probes

Godot exits 0 even when scripts fail to parse or resources are missing, so a result is
judged by the log (`SCRIPT ERROR:` / `ERROR:` lines) plus a marker line, never by exit
code alone. Observed on Godot 4.7.2: a script or scene that nothing references is not
touched by import or by a scene-load smoke, so a broken orphan file passes both.

Extra opt-in flags (all require `--godot` and a successful import):

```powershell
python tools/engine_check.py --project P --godot auto --parse-gate [--skip res://addons/x/] [--include-imported]
python tools/engine_check.py --project P --godot auto --scenario tests/scenarios/move.json
python tools/engine_check.py --project P --godot auto --scenario tests/scenarios/move.json --capture --fps 30
```

- `--parse-gate` (L2, `tools/probes/godot_parse_gate.gd`): loads every `.gd`, `.tscn`,
  `.scn`, `.tres`, `.res` under `res://`, including unreferenced ones. A script fails when
  `reload()` reports an error (a broken script still loads as a non-null object, so a null
  check is not enough). A scene or resource fails on a missing dependency or unresolved UID.
  Not checked: `.gdshader`, C#, GDExtension binaries, runtime behavior. Vendored addons are
  excluded with `--skip`, and every skipped prefix is recorded in the marker.
- `--scenario` (L3, `tools/probes/godot_scenario.gd`): JSON with `scene`, `frames`, `steps`
  (press/release/tap an InputMap action, or call a method at a frame) and `assertions`
  (node exists, or property op value at a frame; ops `== != < <= > >= approx`).
  `tools/godot_runtime.py` rejects a scenario with no assertions, an assertion beyond the
  last frame or an unknown key before the engine starts, so it cannot pass by proving nothing.
  An unknown input action, a missing call target or a node that is not found is a failed
  assertion or logged error, not a skip. The scenario proves only what it asserts.
- `--capture` (L4 input): reruns the scenario with a real renderer (needs a GPU and display;
  not `--headless`) and `--write-movie` as a PNG sequence under `<logs>/godot-capture/`.
  The row is WARN with `VISUAL REVIEW REQUIRED`, the frame count, the number of distinct
  frames and first/middle/last sample paths. Identical frames mean nothing moved. A capture
  never becomes PASS by itself; a reviewer or the user looks at the sampled frames.
  The requested `--resolution` may be overridden by project window settings; read the real
  size from the PNG, not from the flag.

Scenario files and project probes belong to the target project (for example
`tests/scenarios/`); they are not stored under `.local/`.
