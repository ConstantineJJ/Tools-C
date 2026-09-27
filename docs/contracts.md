# Contract format v1

Tools_C architecture 4.0 retains this format version. The v4 catalog also requires
each canonical skill to reference [foundation](foundation.md). Generated Blender
routers carry the SHA-256 of their current canonical context; sync and adapters
detect stale content and duplicate/unlisted routes before accepting deployment.

Python 3.10+ standard library validates configuration, profiles, catalog and contracts
strictly. Unknown fields/kinds/versions, duplicate JSON keys/IDs and non-finite JSON
constants fail. No YAML/schema package is required. The validator in
[check.py](../tools/check.py) is the executable structural specification.

`.tooling/config.json`: required fields `schema_version: 1`, `tools_root` (relative
to project root or absolute), `profile` (project-relative JSON file). TOOLS_C_ROOT
overrides tools_root for a machine; the resolved folder must match this checker.
Only this configured pointer can cross project roots.

Profile: required `schema_version: 1`, `id`, nonempty string arrays `skills`,
`contracts`, `references`. Optional `local_skill_roots` lists project-relative
directories; optional `adapter` is a supported adapter object. All references must
exist. Skill IDs must resolve in the central catalog. No duplicate IDs/references.

Optional `review_state`: `generated_unreviewed` or `reviewed`. Bootstrap writes the
former. An absent status (legacy v1 profile) or generated_unreviewed produces
W_UNREVIEWED/WARN, not FAIL. Audit and specialize the selected profile/contracts,
then deliberately set reviewed; bootstrap never upgrades it automatically. This
records review intent, not engine/visual acceptance. All checks still execute;
misspelled status fails E_SCHEMA. Mark it unreviewed again when replacing its scope.

Contract example:

```json
{
  "schema_version": 1,
  "id": "project-core",
  "rules": [
    {"id": "CORE-001", "kind": "files", "paths": ["README.md"]},
    {"id": "CORE-002", "kind": "json", "paths": [".tooling/profile.json"]}
  ]
}
```

Contract fields above are required; rules cannot be empty. Each rule requires
`id`, `kind`, nonempty `paths`. Optional `severity` is `FAIL` (default) or `WARN`.
IDs are unique across all loaded contracts and rules. Canonical lesson IDs use
`### PREFIX-001` headings and are unique across the central skills tree.

| kind | Extra required fields | Proven property |
|---|---|---|
| files | none | Exact files exist |
| json | none | Strict JSON parsing; not arbitrary JSON-schema compliance |
| markdown | none | Local links in supported Markdown syntax resolve |
| text | required, forbidden: string arrays, at least one nonempty | Case-sensitive literal presence/absence |
| sha256 | expected: lowercase 64-digit hex; exactly one path | Exact bytes match a declared protected artifact |

Paths are exact, forward-slash relative paths; no globs. Resolution includes
symlinks/junctions before containment checking. Parent references are allowed only
when the final target remains inside the project root. Absolute, drive, UNC and
alternate-stream paths are rejected. This is an offline integrity guard, not an
OS security sandbox against concurrent hostile filesystem changes.

Markdown subset: inline links/images and reference definitions; code fences/spans
excluded; percent-encoded paths supported. Web URLs, anchors and inline-code paths
are not verified. Nested-parenthesis destinations and full CommonMark parsing are
outside V1. List important backtick resource references explicitly in contracts.

Profile adapters live in [profile_adapters.py](../tools/profile_adapters.py):

- `{"kind":"godot","resources":["scenes/main.tscn"]}` requires project.godot and
  follows literal res:// ext_resource paths from declared .tscn/.tres files.
  It does not parse GDScript, resolve UID-only references or validate engine semantics.
- `{"kind":"blender","manifest":"skills/PIPELINE_MANIFEST.json"}` verifies
  exact generated compatibility routers, expected aliases and manifest byte/line/hash
  values. This never changes the MCP bridge or invokes its synchronization routine.
  Optional `mirrors: ["mcp-server"]` validates the same generated routers at legacy
  server-relative lookup roots, with identical coverage and integrity requirements.

Catalog: `schema_version`, `version`, `skills` (`id`, `path`) and `blender_aliases`
(`reference`, `source_sha256`, `source_version`). Every central SKILL.md must be
listed and routed; another declared project tree cannot contain the same canonical
skill ID. Compatibility routers are generated references, not extra canonical copies.
The alias source hash/version record the audited migrated source, not the current
version of a living canonical Skill.
Scope of duplicate detection is the central tree and configured local_skill_roots,
not every installed MCP mirror or arbitrary folder on the computer.

Stable diagnostics: E_SCHEMA structure; E_JSON parse/duplicate keys; E_ID duplicate
IDs; E_PATH containment; E_FILE missing file; E_LINK broken Markdown reference;
E_TEXT literal contract; E_HASH protected bytes; E_CATALOG routing/skill drift;
E_TOOLS_ROOT wrong central source; E_IO filesystem/encoding; E_BOOTSTRAP/E_SYNC
installer conflicts. Shape/JSON/ID/path errors always FAIL, even in advisory rules.
Exit 0 means no FAIL; exit 1 means FAIL; argparse usage errors use exit 2.
PASS/WARN/FAIL/SKIP are printed separately; L1 always reports L2–L4 as SKIP.

Add a contract by choosing an actual invariant, adding a uniquely named rule,
listing its file in the profile and running positive/negative fixtures and the
affected project. Avoid freezing tuning or asset identity as universal policy.
Retire an obsolete rule by updating/removing its active definition and consumers
together, with the reason in Git history. A replaced rule must not remain active
in another copy. Lessons lifecycle: [contracts-lint](../skills/contracts-lint/SKILL.md).
