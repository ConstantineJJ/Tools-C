# Transfer record v1

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
