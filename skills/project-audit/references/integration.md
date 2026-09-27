# Connect a project to Tools_C

Read only when the user requests project integration or repair of its Tools_C connection.

Inspect absolute primary/additional roots, each applicable AGENTS.md, current Git status, local routers and configuration. Determine which instructions and project-owned files already exist before using tools/bootstrap.py. For existing dirty paths, record the pre-edit bytes or hashes of files the integration may touch.

Bootstrap creates local .tooling configuration and one managed AGENTS.md block while preserving unrelated text. Resolve tools_root relative to the project root, or use TOOLS_C_ROOT for machine-specific location. Inspect generated profile.json, profile.md and contracts.json; specialize project choices and actual resources before changing review_state from generated_unreviewed to reviewed. Review state does not bypass invariant checks.

Run Tools_C checks on the connected project, inspect status and diff, and compare pre-existing user files. Do not use remote history, a generic template or a previous project's skeleton as authority. If an edit overlaps user work, follow the user's existing authorization and keep the change narrow.
