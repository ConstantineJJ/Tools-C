# Blender domain skill pack 8/8 — review and correction pass

Date: 2026-10-03. Reviewed baseline: `073bdb627bb1adc685d675812773b5e11ecf0436`.
Canonical root: `E:/MyCreations/Tools_C`.

The first phase was read-only: all eight specialist bodies, pipeline procedures,
routing/reader consumers, catalog/profile/self-registration and integration were
inspected before any edits. Tools_C remained clean when findings were presented.
The second phase fixes only the confirmed findings below. Dedicated domain
contracts, checker rules, manifest entries and profile choices are outside this pass.

## Critical

None found. Routing is assistance, not authorization to modify an asset. Existing
foundation/preservation requirements and execution safety boundaries remain active.

## Important

### I-01 — Stage requests do not load the stage procedure

Files: [runtime routing](../tools/mcp_runtime.py),
[canonical reader](../tools/read_blender_skill.py),
[pipeline](../skills/blender-pipeline/SKILL.md).

Baseline reproduced locally and through the live connector:

| Request | Baseline result | Missing behavior |
|---|---|---|
| `Retopologize the vehicle body without changing its silhouette.` | vehicle modeling context | Retopology procedure body |
| `Сделай ретопологию скульпта, сохрани силуэт.` | sculpting context | Retopology procedure body |
| `Unwrap UVs and bake normal maps for the microwave; preserve its geometry.` | product modeling context | Surfaces procedure body |
| `Исправь UV и материалы чайника, геометрию не меняй.` | product modeling context | Surfaces procedure body |

The pipeline links were correct, but the reader could not supply surfaces as a
selected procedure and automatic routing did not load either stage. This left the
requested operation with domain modeling instructions instead of its execution rules.

Correction: stage-only requests select the existing `blender-pipeline` owner with
the selected canonical retopology/surfaces body. A bounded reference allowlist
prevents arbitrary paths. Retopology also loads its existing deformation reference.
Explicit geometry creation plus UV work can load pipeline and the domain together.
No new canonical skill or legacy alias is introduced.

### I-02 — Negated and review-only work activates modeling owners

File: [runtime routing](../tools/mcp_runtime.py).

`Make a mesh-only tree with no sculpting.` selected vegetation plus sculpting.
`Review the vehicle without editing it.` selected vehicle modeling rather than
verification. The latter was also confirmed through the live connector. The
rendered domain context did include verification, but its advertised owner did not
reflect the explicitly read-only request.

Correction: bounded filtering of preservation/exclusion clauses before inferred
routing; review/inspection without an active edit selects verification. Later
explicit edits after a preservation clause remain visible, including animation
and weight repair. Explicit canonical skill names still take precedence. These
heuristics are deliberately not a full natural-language parser or permission gate.

### I-03 — Missing common asset names and plural forms

File: [runtime routing](../tools/mcp_runtime.py).

`Create chairs and tables.`, `Create bicycles.`, `Create game-ready plants.` and
`Create a close-view radio with ports and controls.` fell back to pipeline despite
clear documented domain owners. `Create road signs beside an existing road.`
loaded roads but omitted the fixture owner. Additional plural curb/sidewalk and
toolbox coverage was included in the same correction.

Correction: supported noun/plural forms route to their existing owners. Radio
routes to product/electronics when port/control/enclosure construction is explicit;
a decorative radio prop remains props. No claim of exhaustive bilingual vocabulary
or resolution of a bare ambiguous request such as `Create a lamp.` is made.

## Minor

### M-01 — Stale implementation-state wording

Files: [domain pack plan](../docs/blender-domain-skill-pack.md) and routing clauses
in [architecture](../skills/blender-architecture-environment/SKILL.md),
[environment assets](../skills/blender-environment-assets/SKILL.md),
[roads](../skills/blender-roads-infrastructure/SKILL.md),
[props](../skills/blender-props/SKILL.md),
[products](../skills/blender-product-electronics-modeling/SKILL.md) and
[vegetation](../skills/blender-vegetation/SKILL.md).

Seven status lines still said active/implemented, roads was labeled the first pass,
and implemented owner links retained `when implemented/available` fallback wording.
Correction is limited to these stale status/availability phrases; workflows,
safeguards, lessons and ownership decisions are preserved.

### M-02 — Legacy sculpt discovery description is narrower than its owner

File: [canonical reader](../tools/read_blender_skill.py).

The legacy organic sculpt alias loaded the expanded canonical skill correctly,
but discovery described only character organic corrections. Its description now
includes organic/hard-surface sculpting and damage. The legacy name is preserved.
Compatibility outputs are regenerated through the existing managed sync.

## No action

- Architecture owns building-integrated modules; environment-assets owns discrete
  reusable fixtures; roads owns continuous route/network geometry. Entrance edges,
  corridor fences and fixture placement have explicit split handoffs.
- Props/product/vehicle boundaries use production role and engineering burden.
  Vehicle-integrated dashboards stay vehicle-owned; separate removable devices
  may intentionally co-route. A decorative radio need not become product modeling.
- Vegetation owns growth structure and wind-ready source data; sculpting owns its
  form-changing technique, not botanical identity or the runtime wind shader.
- Repeated bevel, modifier, instancing, UV and wear guidance is domain-specific.
  No identical substantial shared decision procedure justified extracting another
  hard-surface owner or reference.
- All eight skills have safeguards, handoff and stop conditions. Protected state,
  recoverable sources and structural versus visual acceptance are consistent.
- No fixed universal dimensions, triangle/texture/texel/LOD/collision/wind budgets
  were found in the specialist bodies. Target-specific choices remain in profiles.
- Final retopology, UV/PBR execution, rigging/animation and export retain their
  existing owners. Domain UV/bake planning and physical articulation axes are
  appropriate domain decisions rather than competing final-stage authorities.
- Catalog/profile/self-registration/AGENTS/pipeline links cover all eight owners:
  23 canonical skills and nine legacy aliases. Local skill/reference links pass L1;
  domain lesson IDs are unique. Original alias source hashes remain migration
  provenance, distinct from generated current-context hashes.
- Mixed contexts can exceed the existing default text budget. Truncation is
  explicitly reported as incomplete; request a larger budget or one owner.
- The Blender-MCP-Co integration profile is an adapter choice, not a duplicate
  universal catalog. Existing unrelated launcher/source/build changes are preserved
  and excluded from the Tools_C commit scope.

## Validation after corrections

- FIXED: I-01, I-02, I-03, M-01 and M-02. No Critical finding and no open
  confirmed blocker in this review scope.
- PASS: Tools_C L1 and Blender-MCP-Co L1 each returned 9 PASS / 0 WARN / 0 FAIL.
- PASS: `python -m unittest discover -s tests -q` returned 57 tests, 0 failures,
  0 errors, 0 skips. Added behavioral coverage includes actual selected procedure
  bodies, mixed modeling+UV work, rejected unknown procedure paths, preservation,
  negation, review-only requests, common names and the cached reader interface.
- PASS: 21 live connector context requests covered all eight explicit domain owners
  and 13 stage/boundary/negative/mixed requests. Every loaded context was complete
  at the requested 120000-character budget and matched current local canonical
  output by SHA-256, owners and selected procedures.
- PASS: managed-router regeneration and disposable stdio MCP smoke checked nine
  legacy contexts against canonical text, all 15 source/runtime tool names, existing
  downstream stage routes, loaded/disk server identity and syntax rejection before
  execution. Existing legacy names are preserved.
- A first live smoke attempt exposed a cached two-argument reader behind the running
  adapter. The interim three-argument call failed despite cold-process tests passing.
  The final correction keeps the established reader API and appends allowlisted
  procedures in runtime context composition. The 21-request retry passed without
  a service restart; the interim failure is not counted as successful evidence.
- PASS: `git diff --check`; manifest/profile/contracts/AGENTS are unchanged.
- Managed-router baseline and deployment JSON are under
  `C:/Users/kosti/AppData/Local/Temp/Tools_C_domain_review_20261003`. Unrelated
  Blender-MCP-Co files were fingerprinted before regeneration and checked again.

No production geometry, rigging, materials, export, visual-art acceptance or new
dedicated contracts are claimed by this review. Those asset-level gates remain
SKIP/inapplicable; the next dedicated contracts pass is NOT STARTED.
