# MCP and editor rules

Read when a Godot MCP bridge or an open Godot editor is involved.

- The bridge's tool names, arguments and safety limits come from the tools the session lists. Do not call
  a tool by a remembered name; read its description first. Bridges differ per user and per version.
- Separate four layers when something fails: deployment (is the bridge running), transport (port, tunnel,
  HTTP status), editor (project open, plugin active), engine behavior (scene, script, import). Evidence for
  one layer says nothing about another. A healthy endpoint is not an import result.
- An editor that is open on a project can hold the bridge's port. A second headless engine then logs a
  port error even when import succeeded. Report it as an environment conflict. Do not close the user's
  editor, disable their plugin or filter the line out of the log.
- Prefer read-only bridge calls for QA. Do not save scenes, change project settings, run the project or
  modify files through the bridge unless the user's task asks for that edit.
- Results that came through the bridge are tagged with what ran: a scene-tree read is L1-style structure,
  a project run is L3 only if it executed the claimed behavior and its log was read.
- When the bridge cannot do a step, the headless probes in [engine probes](../../../docs/engines.md) are the
  fallback, and the report says which route produced each row.
