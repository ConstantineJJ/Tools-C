# Private Tools_C plugin

Source: `plugins/tools-c`. This package contains one invocation entrypoint,
presentation, the user's original icon and references to existing registered
Blender/Godot/files Apps. It contains no copied canonical procedures or validators.
The canonical manifest, router, skills, project profiles and QA remain in Tools_C.

The plugin reads deployment_info, list_skills and get_skill_context. Generic
project-audit, godot-project and contracts-lint contexts already work through the
existing adapter without a Blender scene connection. Actual engine operations
still need their own connected engine and project scope.

`tools_c_check(project=None)` adds one read-only operation to the existing MCP
server. It calls the current check.py in a fixed, shell-free Python subprocess,
with a 30-second deadline and bounded returned output. It never certifies runtime
or visual acceptance. Default allowed projects are canonical Tools_C and its
integration repository. An operator can register other exact absolute roots in
private `.local/mcp-projects.json`: `{"projects":["C:/actual/project"]}`.
Project-authored contracts cannot add themselves to this machine allowlist.
This is not an arbitrary shell runner and needs no open Blender scene.

After server changes, restart the existing tunnel/MCP process normally and
refresh client metadata. Existing 17 operation names remain; tools_c_check is
additive and capture_viewport gains only optional camera_name/channel inputs.
Existing scalar square resolution and capture defaults remain supported.

For a private account install, package the directory with its root plugin.json,
.app.json, compatibility manifest, skill and icon. Verify registered App IDs and
archive contents, then use the existing Plugin Creator account-save operation.
Uploading a plugin does not start its local services, install Python/Blender,
grant filesystem access, or guarantee the host provides ImageGen. Missing
capabilities stay explicit. Fresh-chat invocation is a separate client check.
