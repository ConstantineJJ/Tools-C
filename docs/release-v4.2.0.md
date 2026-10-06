# Tools_C v4.2.0

Twenty-eight canonical skills and nine legacy Blender entrypoints. This release
adds Reference Surface Transfer and brings the post-v4.1.0 DESCRIPTION workflow
and persistent Model Contract into the portable distribution. Architecture remains
4.0.1; catalog/profile/registration contract schema_version remains 1.

## Changes

- [Reference Surface Transfer](../skills/blender-reference-surface-transfer/SKILL.md)
  uses original reference regions for faces/eyes, logos, markings, prints, tattoos,
  decorative panels and distinctive patterns. The workflow prioritizes original
  pixels: crop, justified correction/cleanup/upscale, masked regeneration only
  where information is insufficient, projection/decal/UV transfer, bake, local seam
  cleanup and identity QA. Physical material response is reconstructed separately.
- The [transfer-record checker](../tools/surface_transfer.py) validates provenance,
  crop bounds, ordered processing lineage, mask/prompt references for regeneration,
  bake/seam-cleanup records and optional contained-file hashes. It always leaves
  visual acceptance to inspected evidence; a valid record can retain pending work.
- [DESCRIPTION mode](../skills/visual-reference-reconstruction/references/description-mode.md)
  derives a canonical concept from a text brief, reviews required constraints,
  locks one hero design and derives auxiliary views from that image. Supplied-image
  REFERENCE mode retains its original-source priority.
- One [Model Contract](../skills/visual-reference-reconstruction/references/model-contract.md)
  persists inside PASS 0 schema 3 and binds assemblies/view reviews by id, revision
  and hash. It preserves counts, proportion envelopes, anchors, soft details and
  critical relationships. Cropped/generated views cannot redefine locked geometry.
- Canonical discovery helper supports Blender MCP `list_skills` and `find_skills`
  from the extracted package, including the new surface-transfer owner.
- English/Russian routing keeps surface-only transfer separate from geometry,
  generic PBR, finishing and read-only QA; explicit mixed tasks keep their relevant
  owners. Full canonical contexts retain document receipts and continuation.

## Compatibility and upgrade

Existing MCP operation names and nine legacy aliases are unchanged. After
extracting the new package, regenerate managed routers from its canonical root:

```powershell
.\check.bat --self
python -m unittest discover -s tests -q
python tools/sync_blender.py --project "C:\path\to\Blender-MCP-Co"
```

Python 3.10+ runs the core harness using the standard library. Blender/MCP and
image tools are required only for applicable asset work. No image provider or API
key is required for source-only planning and provenance checks.

New PASS 0 packets use schema 3. Historical schema 1/2 packets remain parseable for
audit, but resuming modeling requires reviewing/sealing the persistent Contract.
This is an intentional production gate; unchanged surface-only work does not
restart PASS 0. Upgrade affected packets before continuing geometry construction.

## Verification and limits

`release-verification.json` identifies the exact public commit, archive contents,
hashes, fresh extracted-package regression/L1 checks and Windows launcher smoke.
The prior local implementation passed 198 regressions and seven live MCP contexts;
those counts include local-only catalog tests and are distinct from package tests.

This release verifies skill/harness structure, provenance rejection and context
delivery. Actual transfer quality, face likeness, regenerated pixels, bake/seams,
Blender saved-file dependencies, deformation and target-engine appearance require
an asset-specific exercise. RGB does not directly prove roughness, metallic or
normal data. Structural PASS does not certify image identity or physical accuracy.

Download `Tools_C-v4.2.0.zip`, verify `SHA256SUMS.txt` and extract it. Internal
instructions/status, personal reference images, reports, logs, captures and Git
metadata are excluded. The previous v4.1.0 package remains available for rollback.
