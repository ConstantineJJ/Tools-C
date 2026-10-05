# Canonical Design Graph / Model Contract

Both input modes converge here immediately after reference analysis / Identity
Lock, **before** auxiliary generation and Blender. One persistent graph lives in
`pass0.json`; `assembly_graph.json` binds real objects to it. No parallel design
manifest or new MCP service is needed. Read this at intake, reuse it across passes.

Trust order is strict:
**USER REQUIRED > ORIGINAL REFERENCE / LOCKED HERO > MODEL CONTRACT > GENERATED
MULTIVIEW > AGENT INFERENCE**. The Contract records higher authority; it cannot
override it. If extraction contradicts user requirements or the source, stop,
correct extraction explicitly and revise the Contract. Do not let a sheet repair
the disagreement by redefining the design. Attachments remain evidence.

## One graph, two independent classifications

Keep existing component IDs, counts, claims, dimensions, silhouette and relationships.
Add `parent_id` (component ID or null) and `symmetry` (object with type
NONE/BILATERAL/RADIAL/REPEAT/UNKNOWN, plus axis/pairing/basis as relevant) to components.
Mark unresolved component existence `certainty=SPECULATIVE`; do not give it an
established count invariant. Unknown symmetry stays UNKNOWN, not automatically mirrored.

Certainty describes authority: DESCRIPTION REQUIRED/CANONICAL/SPECULATIVE;
REFERENCE CONFIRMED/INFERRED/SPECULATIVE plus REQUIRED for explicit user clauses
in schema 3 (cite an immutable BRIEF source). Constraint strength is separate:

| Level | Meaning and comparison |
|---|---|
| HARD INVARIANT | Exact established counts; required features, shape categories, eyes/antennas/weapons, markings (content and placement), handedness and critical attachment relationships. Missing/changed = FAIL. |
| PROPORTION LOCK | Existing relative dimension envelopes, reviewed ratios and numeric silhouette anchors with explicit units, basis and tolerance. Outside envelope = FAIL. |
| SOFT CANONICAL | Covers, seam layout, minor surface detail that can adapt while preserving identity. Variation = WARN; does not rewrite the baseline. |

Do not lock invisible hypotheses as fact. REQUIRED is binding even when pixels
are ambiguous; CANONICAL is an adopted visible choice, not proof of hidden mechanics.
Use only a handful of meaningful geometry anchors, not every vertex or fastener.
Set tolerances from camera/pose uncertainty and modeling goals; never enlarge them
after seeing a failure. No universal 5% tolerance or exact dimensions from perspective.

## Embedded definition

`model_contract` fields: schema_version=1, id, revision (positive integer), status=LOCKED,
reviewer, reason, rules, sha256. Each rule has id, level, kind, checkpoints, basis.
Rules reference existing fields; they do not copy a second component list:

| kind | Selector / expected value |
|---|---|
| count | target_id=component; expected component.count |
| claim | target_id=claim/constraint; exact value (including mandatory marking or intent review) |
| dimension | target_id=relative_dimension; existing min/max; unit matches proportion_basis |
| ratio | numerator_id/denominator_id=dimension IDs; reviewed bounds=[min,max], unit=ratio; bounds within source envelopes |
| anchor | target_id=silhouette claim whose value is a numeric vector; unit and absolute tolerance in those coordinates |
| relationship | target_id=relationship; exact from_component/to_component/relationship/value |
| hierarchy / symmetry | target_id=component; expected parent_id / symmetry object |

Every established component needs a HARD count rule. Every supported key dimension
needs a PROPORTION rule. Every REQUIRED property and `critical=true` relationship/
anchor needs a rule. Prefer a few critical hierarchy/symmetry/relationship checks.
Constraints with target=count reuse the component rule; other REQUIRED constraints
and their bound property claims remain hard. Numeric geometry goes in dimension/
anchor fields with appropriate certainty, not a REQUIRED dimension with invented precision.

```json
{
  "id": "gun.body_ratio", "kind": "ratio", "level": "PROPORTION LOCK",
  "numerator_id": "guns.length", "denominator_id": "torso.width",
  "bounds": [0.58, 0.78], "unit": "ratio",
  "checkpoints": ["VIEWS", "MACRO", "GEOMETRY", "FINAL"],
  "basis": "Reviewed full gun in locked Hero; comparable pose; estimated envelope",
  "view_completeness": {"required": true, "source_ids": ["hero"], "basis": "Both muzzle and mount visible in Hero"}
}
```

`tools/model_contract.py` hashes the supported graph, authoritative source records,
brief, hierarchy/symmetry, hero selection and rule policy. Speculative claims and
auxiliary reviews stay outside the identity hash. The graph is not repeated in a
snapshot file. Schema 3 DESCRIPTION retains image identity_lock source/hash/version
only; the former manifest fields must be removed during explicit migration.
Historical schema 1/2 packets still parse for audit, but `require_stage()` requires
a reviewed Model Contract; do not automatically invent locks to upgrade them.

Seal reviewed rules once:
`python tools/model_contract.py TASK/pass0.json --seal`
Then run the existing PASS0 validator with `--verify-files`. No lock is needed for
a PENDING/BLOCKED provisional brief without a canonical image.

## Generated views: reconstruction, never redesign

Prompt from the original/locked image **and** the compact Contract. Preserve complete
weapon extent, module sizes, repeat counts, pose, anchors and construction; provide
margin around the full object. Never generate independent designs from text after lock.

Add auxiliary `permitted_views` and `contract_review` with contract_ref={id,revision,sha256},
image_sha256 (the reviewed auxiliary file) and views=[{view,observations}]. Review
each named panel. Each applicable rule receives one observation: rule_id, state
MEASURED/UNKNOWN, value, method, evidence (actual file/region or Blender measurement),
unit for numeric geometry, and completeness FULL/CROPPED/OCCLUDED/UNKNOWN when needed.
Repeated dimensions/ratios require instance_values={instance_id:measured_value} for
every physical item; each must fit tolerance. Do not average away a short left gun
with a long right gun. Assembly sample IDs must match actual physical bindings.
State MEASURED only for comparable projection/pose or a justified reconstruction;
raw foreshortened pixels are not a 3D length. Read pixels before writing review.

VIEW COMPLETENESS applies wherever higher authority establishes the full element.
A clipped muzzle, foot or antenna = FAIL even if the visible remainder fits tolerance.
Never treat crop as a shorter design. Real self-occlusion / insufficient projection
= UNKNOWN: retain the locked geometry and exclude that view from geometric authority.
Cross-view context can establish counts, but cannot fabricate a measurable length.

All hard/proportion observations must PASS for a permitted panel. ACCEPTED means
all panels pass; RESTRICTED explicitly lists only passing panels; otherwise REJECTED
with empty permitted_uses/permitted_views. A file can be retained as diagnostic
evidence while being forbidden for Blender. Six existing artistic consistency checks
remain: mechanical plausibility and appearance still need visual review.
Correct/regenerate the affected panel/feature (at most two attempts per defect),
re-review, or hand off source-only with explicit limits. Never change the Contract
to accommodate generated drift. No consistent view does not invalidate a usable Hero.

## Persistent assembly and cheap Verification Loop

`assembly_graph.json` retains its existing parts/pivots/attachment fields. Add one
contract_ref and each part's component_id, instance_id (physical item, shared by
its meshes/armor/bolts) and object_name. Count physical instances, not mesh objects.
Parent parts must resolve to the canonical component hierarchy. Bindings must be
checked against actual evaluated scene objects; a JSON assertion is not scene proof.

Store current checkpoint observations and the compact returned receipt under
verification (contract_ref, checkpoint, status, observations_sha256, checks). Refresh
only at **VIEWS intake, MACRO silhouette, MECHANICS interfaces, GEOMETRY clay handoff,
FINAL delivery**. Select only stages present in the task; this is not five mandatory
production passes. Counts persist at all; proportion rules cover VIEWS/MACRO/GEOMETRY/FINAL;
critical mechanics run when represented. No checks after each bolt/edit.

`python tools/model_contract.py TASK/pass0.json --assembly TASK/assembly_graph.json --checkpoint MACRO`

Hard/proportion FAIL or UNKNOWN blocks the dependent checkpoint. Fix geometry or
defer unsupported work; texture/wear cannot hide it. Numeric bounds use measured
geometry in declared axes/pose; silhouettes require matched clay views. Save/reopen
the assembly's pinned reference with the asset, verify the same id/revision/hash
at resume/handoff, and invalidate stale observations. Stage-only work on an already
contracted asset preserves the same locks without restarting PASS0.

Intentional changes: retain the old packet; same id, revision+1,
supersedes_sha256 and change_note naming affected properties/reason/decision authority.
Seal with `--previous OLD/pass0.json`. REQUIRED changes additionally need explicit
USER authority (`requirement_change_authority=USER`) and revised verbatim brief bytes.
Old view reviews and assemblies become stale until reconciled. Never silently reseal
revision 1 or revise requirements because a generator failed.

The checker cannot read pixels, detect omitted brief clauses, validate fabricated
measurements, or defeat someone rewriting every hash/receipt. Visible evidence,
bounded Blender measurements and honest UNKNOWN states are necessary. Contract
agreement does not certify hidden construction, articulation, manufacturing or final likeness.
