# Private Tools_C plugin

Source: `plugins/tools-c`. This package contains one invocation entrypoint,
presentation and the user's original icon. It discovers existing connected
Blender/Godot/files tools. The public source omits account-specific App IDs and
contains no copied canonical procedures or validators.
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

The public directory is a portable skills entrypoint, not a preconfigured service
connection or a public-directory App submission. It requires the operator's
existing connected MCP services. Missing services are reported explicitly.

For a private account install, copy the directory to private staging outside the
repository, add a root `.app.json` using verified registered App IDs, and reference
it through `extensions.com.openai.apps` in the root manifest and `apps` in the
compatibility manifest. Package that private copy with its skill and icon, verify
the contents, then use the existing Plugin Creator account-save operation.
Keep these personal bindings out of the distributable source. An already installed
private plugin retains its own bindings when the repository is cleaned.
Uploading a plugin does not start its local services, install Python/Blender,
grant filesystem access, or guarantee the host provides ImageGen. Missing
capabilities stay explicit. Fresh-chat invocation is a separate client check.
