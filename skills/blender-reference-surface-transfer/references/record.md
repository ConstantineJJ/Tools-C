# Transfer record v1 (backward compatible) / v2 (face strategy)

Schema v1 remains valid for existing assets and old records. **New face
transfers should use schema_version=2**, which retains every v1 field and adds
one mandatory `face_strategy` object validated structurally by the same
`tools/surface_transfer.py` checker. Non-face transfers may stay on v1.
No v1 file is rewritten automatically, and schema v2 does not certify art.

## Version 2 face_strategy

Exact keys: `mode`, `regions`, `occluder`, `occlusion_mask`,
`occlusion_layer`, `reason`. Mode is `DIRECT`,
`RECONSTRUCT_THEN_LAYER` or `HYBRID`.

- Each `regions[]` object has `name` (unique stable string),
  `visibility` (VISIBLE/PARTIAL/OCCLUDED), `source`
  (ORIGINAL/INFERRED), `landmarks` (unique nonempty string list), and
  `protected` (Boolean). Fully OCCLUDED regions cannot claim ORIGINAL
  observed pixels; entirely VISIBLE regions cannot be relabeled INFERRED.
  Landmark labels describe what will be checked visually, not measurements.
- `occluder` is NONE/HAIR/OTHER. If non-NONE, `occlusion_mask`
  must refer to an existing artifact and `occlusion_layer` must be
  GEOMETRY/ALPHA; if NONE, the mask must be null and layer NONE.
- DIRECT preserves source regions and cannot have regeneration steps;
  RECONSTRUCT_THEN_LAYER requires a masked regeneration step and at
  least one inferred region; HYBRID requires source+inferred regions
  and masked regeneration. All regenerate steps retain v1 prompt/mask
  provenance. `reason` describes why this strategy was selected.

Example additional field (append beside the existing v1 required fields):

```json
"face_strategy": {
  "mode": "HYBRID",
  "regions": [
    {"name": "left_eye", "visibility": "VISIBLE", "source": "ORIGINAL",
     "landmarks": ["outer_corner", "iris"], "protected": true},
    {"name": "right_eye", "visibility": "OCCLUDED", "source": "INFERRED",
     "landmarks": ["eye_line"], "protected": false}
  ],
  "occluder": "HAIR",
  "occlusion_mask": "mask",
  "occlusion_layer": "GEOMETRY",
  "reason": "Preserve visible eye; reconstruct only hair-covered region."
}
```

The checker verifies only schema, categorical consistency, artifacts and
declared provenance. An agent can still lie in a field. Final seam visibility,
face likeness, hair-depth occlusion and 3D registration require actual
visual inspection and the later cross-cutting QA pass.


Keep one JSON record per transferred patch; store it beside a contained artifact
package. This record supplements the existing PASS 0/Model Contract; it does not
create a new design authority. `source.authority` names the source decision and,
when present, the existing Contract id/revision/hash and component/claim IDs.

Run `python tools/surface_transfer.py path/to/transfer.json --verify-files` from
Tools_C. All artifact paths are relative to the record directory; copy originals
into the package without changing their bytes. The standard-library checker checks
schema, lineage, source crop bounds, distinct paths and optional file hashes. It
never processes pixels, invokes a generator or certifies a recorded visual verdict.

Required fields (unknown fields fail):

| Field | Content |
|---|---|
| `schema_version` | Integer `1` |
| `artifacts` | Map of stable IDs to `{path, sha256}` for originals, crops, masks, prompts, prepared/baked images and evidence |
| `source` | `{artifact, role, size, authority}`; role ORIGINAL or LOCKED_HERO; size `[width,height]` in pixels |
| `crop` | `[x,y,width,height]`, integer source pixels, top-left origin |
| `steps` | Ordered nonempty list; first operation crop, then optional rectify/upscale/cleanup/regenerate |
| `target` | `{objects, faces, uv_map, material, method, image, settings}`; objects is a nonempty name list; method PROJECTION, DECAL or UV; image is last step's artifact ID |
| `bake` | `{status:"DONE", artifact, settings}` or `{status:"PENDING"/"SKIP", reason}` |
| `seam_cleanup` | `{status:"DONE", input, output, settings}` consuming the bake artifact into a distinct final artifact, or `{status:"PENDING"/"SKIP", reason}`; SKIP explains why no correction was needed or why bake was skipped |
| `pbr_basis` | Separate roughness/metallic/normal reconstruction basis and uncertainty; unchanged existing PBR is valid with its basis |
| `qa` | Named records for identity, seams, material, movement, reopen and target |

Every step contains `{operation, input, output, reason, parameters}` with artifact
IDs for input/output. Each consumes the preceding output without overwriting it.
Parameters record actual crop/rectification correspondence, sampling/color-space
decisions and tool/version as appropriate. `regenerate` additionally requires
`mask` and `prompt` artifact IDs; reason states insufficient source data and why
deterministic cleanup was inadequate. Generative upscale uses regenerate, with its
upscale settings in parameters. Do not label it ordinary upscale to bypass lineage.

## Recording face strategies without changing schema v1

The checker requires **exact existing fields**. Do not add `strategy`,
`protected_zones`, `occlusion` or `seam_metrics` as new top-level keys: it
will reject them. For legacy schema-v1 records, store the chosen
DIRECT / RECONSTRUCT-THEN-LAYER / HYBRID strategy, visibility notes, preserved
landmarks and rejected alternatives in `steps[].reason` and
`steps[].parameters` (**both are required strings**, not nested objects),
plus `target.settings` and `qa.identity.observations` as appropriate.
Use separate per-region records/artifacts for eyes and mouth when provenance
or masks differ. Each `regenerate` operation still requires unique mask/prompt
artifacts; retain original pixels as separate immutable inputs.

Keep skin-mask/occlusion-mask provenance and pre/post seam closeups as artifact
IDs, referenced in existing fields. Record the protected approved features in
observations and the task's existing Model Contract/hand-off notes, not a new
second identity registry. An imagined covered eye remains INFERRED even if the
generated clean face looks convincing.

For a facial patch, `qa.identity` and `qa.seams` cannot honestly be PASS while
a feature has drifted or a cutout border is visible under neutral lighting.
`qa.reopen` requires evidence after saving/reopening; target/deformation may
remain SKIP with concrete reason when outside the assigned task. A structural
PASS from `surface_transfer.py` only validates record consistency, **not** face
likeness, color integration or the absence of visible seams.

Every QA item has `{status, reviewer, observations, artifacts}`. Status is PASS,
FAIL, SKIP or REVIEW_REQUIRED; artifacts is an ID list. PASS/FAIL require a reviewer
and evidence; REVIEW_REQUIRED requires evidence awaiting inspection. SKIP requires
a concrete reason in observations. For reopen include a saved-file/binding report;
movement/target may be SKIP when out of scope. Identity/seams/material need inspected
images for visual acceptance even though the checker cannot judge file contents.
Pending bake, failed criteria and missing required review remain open delivery
gates even when the provenance record is STRUCTURAL PASS.

Record artifacts and hashes for the source, crop, prepared image, baked image,
comparison views and reopened dependency report. Check pixel dimensions, actual
mask containment, outside-mask preservation, image encoding, Blender bindings,
source priority and Contract consistency during execution/review; a JSON field
declaring these is not proof. Do not use the checker as a production-ready switch.
