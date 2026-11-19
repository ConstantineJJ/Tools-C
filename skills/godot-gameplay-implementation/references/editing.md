# Scene and script editing

Read before hand-editing `.tscn`, `.tres` or adding scripts. TSCN facts are from the Godot file-format
documentation; the engine you run is the final judge, so re-run `--parse-gate` after every text edit.

## TSCN structure

- Header `[gd_scene format=3 uid="uid://..."]`. `format=3` is Godot 4. `load_steps` is deprecated since 4.6;
  do not add it to a new file or fix its count by hand.
- `[ext_resource type=... uid=... path=... id="..."]` for files, `[sub_resource type=... id="..."]` for
  embedded resources. A node refers to them as `ExtResource("id")` / `SubResource("id")`. Keep existing ids;
  pick a new unique id for an addition. Keep `path` and `uid` consistent; the engine may resolve by
  uid, so a stale path can hide a broken reference until the file moves.
- Exactly one root `[node name=... type=...]` without `parent`. Children use `parent="."` or a path
  relative to the root. A wrong `parent` path breaks scene loading; the parse gate and the scenario will show it.
- Properties equal to the class default are not stored. Do not add them to "make it explicit".
- `unique_id=` on `[node]` lines exists in scenes saved by Godot 4.6 or later. Do not invent or
  renumber them; keep existing ones, and omit them on a new node unless the project's files all carry them.
- Instanced scenes appear as a node with `instance=ExtResource("id")`; overrides are listed under it.
  An override you delete falls back to the instanced scene's value.

## Safe text-edit procedure

1. Copy the original (or rely on version control). Edit the smallest block.
2. Add or reuse an `ext_resource` before referring to it.
3. Run `--parse-gate`, then the scenario. A missing dependency or a bad parent path is reported there.
4. Never hand-write binary `.scn` or `.res`; use the editor or an engine script and say which.

## Scripts

- A new `.gd` file gets a `.uid` sidecar when the editor or an import creates it. Commit the pair. Do not
  delete or hand-write a `.uid` to silence a warning.
- Moving or renaming a script or scene: use the editor or a script that updates references; a file move in
  the shell leaves `res://` paths in other files pointing nowhere. Search for the old path afterward.
- Class names declared with `class_name` are cached by the engine (the global class list under `.godot/`).
  After adding or renaming one, run an import before judging "unknown identifier" errors.
- `.godot/` is generated cache. Never edit it, and do not treat its absence as a defect.

## Adding an input action to project.godot

The editor is the normal route. When no editor is available, copy an existing action's block under `[input]`
in the same file, rename it and change only `physical_keycode` (Space is 32); never invent the event fields.
Then prove the binding with a scenario assertion `{"at_frame": 1, "input_action": "<name>"}` and a press/release
step that changes the asserted state. An unknown action name in a step is logged as an error, so a typo fails.
Say that the edit was by hand. A key press in a real window is still unproven.

## When not to hand-edit

Animation tracks, imported scene internals (edit the import settings or an inherited scene instead) and large
sub-resource graphs are safer through the editor, an import hint or a short engine script. Say which route was used.
