# Tools_C v4.0.3

Twenty-five canonical skills, nine legacy Blender entrypoints and the portable
skills/checker harness. This release includes the anime character specialist
added after the v4.0.2 release, plus six improvements for Blender form development.
Contract/profile/catalog schema_version remains 1.

## Changes

- [Form development](../skills/blender-pipeline/references/techniques/form-development.md)
  distinguishes shading from silhouette and mass construction. Independent
  width/depth profiles, taper, bends and credible transitions replace accidental
  tubes, slabs and balls when the design calls for developed forms.
- [Five construction recipes](../skills/blender-pipeline/references/techniques/form-recipes.md)
  cover limbs, hair, ribbons, fur and canopy masses. An
  [editable Blender comparison scene](../skills/blender-pipeline/assets/form-examples/Form_Examples.blend)
  and seven PNGs show isolated construction choices with named review criteria.
- Early representative [lookdev](../skills/production-lookdev-gate/SKILL.md)
  precedes repetition and background/detail growth. Blender-only delivery uses
  the intended Blender renderer; target-engine checks apply to engine delivery.
- Four domain entrypoints are approximately 76% shorter. Existing procedures,
  safeguards and lessons remain in conditional references under their owners.
- Context delivery deduplicates whole documents across owners, supplies SHA-256
  receipts and supports explicit continuation. Missing documents must be read
  before their affected operation; reset receipts after losing context.
- Russian routing recognizes mixed catgirl/house/bench/fence/tree/prop requests,
  form smoothing and rig creation while preserving read-only and stage boundaries.
- Tested helpers construct transported profiles with longitudinal UVs, editable
  curve batches and object parenting; selected-pair contact diagnostics and
  declared snapshot categories support proportionate local/final QA. Typed
  curve operations expose IDs, progress, cancellation and partial failure.

Clean stylized surfaces now have a short baseline path; wear, damage, emission
and bake follow the task. None of these helpers decides artistic likeness or
replaces inspection in the actual renderer.

## Download and use

Download `Tools_C-v4.0.3.zip`, verify its hash in `SHA256SUMS.txt` and extract it.
From the extracted folder:

```powershell
.\check.bat --self
python -m unittest discover -s tests -v
```

Python 3.10+ is required for the core harness. Blender/Godot and the MCP SDK are
used only for applicable opt-in probes. The ZIP excludes internal agent/workspace
instructions, project status, diagnostic reports, logs, captures and Git metadata.
Educational examples under the skill's assets directory are distributable content.

Configure the actual installation root and regenerate managed compatibility
routers using the [README](../README.md). A separate compatible MCP integration
supplies the server. Updated context parameters and the two named operation tools
require that bridge's corresponding update and possibly connector rediscovery;
the archive does not replace a running server. Helpers also work through the
existing Python execution bridge. See [MCP interfaces](mcp-deployment.md).

## Verification boundaries

`release-verification.json` identifies the exact source commit, ZIP hash, fresh
extracted-package checks and declared line-ending conversion for Windows batch
files. Structural acceptance is distinct from the bounded Blender helper probes
and the actual inspection of seven educational renders. These fixtures do not
certify a production character's anatomy, likeness, grooming, animation, export
or target-engine behavior.
