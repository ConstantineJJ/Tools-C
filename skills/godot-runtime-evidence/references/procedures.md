# Procedures and CLI facts

Read for command-line details, project test runners and export. Facts are from the Godot command-line
documentation and from runs on Godot 4.7.2; check the project's own version before relying on a flag.

## Command line

- `--headless` runs with a dummy display and audio driver; it has no renderer output, so it cannot capture frames.
- `--import` imports resources, then quits (implies `--editor`).
- `--script <file>` runs a script; with `--check-only` it parses and quits. A parse error or a missing path
  returned exit 1 in testing, but a runtime `SCRIPT ERROR` inside a normal run still returned 0.
- `--write-movie <file>` records a movie; a `.png` path writes a numbered PNG sequence plus a `.wav`.
  It forces `--fixed-fps`; `--quit-after <n>` bounds the number of frames. `--disable-vsync` can speed it up.
  It combines with `--script`, so a scenario can be recorded.
- `--fixed-fps` makes frame time deterministic; do not compare timing against a normal run.
- `--resolution WxH` is a request; the project window settings can win. Read the PNG size.
- `--export-release <preset> <path>`, `--export-debug`, `--export-pack` need a preset in `export_presets.cfg`
  and installed export templates; `--export-debug` implies import.

## Project test runners

If the project already contains a test framework (for example GUT or gdUnit4 under `addons/`), run it with
its documented command-line entry and judge its report plus the log rule. Do not add a framework, install
an addon or change project settings to get a runner. If none exists, use a scenario. A passing runner proves
only what its tests assert; report the test count and which tests cover the changed behavior.

## Export

Run the export only when the user asked for a build. Record preset name, output path and size. An export
that finishes proves packaging, not that the exported build starts or behaves. Launch of the built binary
is a separate check with its own log. Never write the export into the source tree; use the project's declared
output folder or a scratch folder outside tracked files.

## UID sidecars

Godot 4.4 and later writes `.uid` files next to scripts and shaders. They keep references stable when files
move, so they belong in version control with their script. After an import, `git status` listing new `.uid`
files is expected; a script with no `.uid` or a `.uid` left without its script is worth reporting.
