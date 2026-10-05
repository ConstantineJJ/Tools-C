# Tools_C v4.1.0

Twenty-seven canonical skills and nine legacy Blender entrypoints. This release
adds a required reference-understanding pass and a separate robot/mechanism
construction owner. Contract/profile/catalog schema_version remains 1.

## Added

- [Visual reference reconstruction](../skills/visual-reference-reconstruction/SKILL.md)
  runs PASS 0 before scene mutation for complex image-based modeling across
  robots, vehicles, machinery, buildings, props and other asset domains.
  The structured packet records components, relative ranges, silhouette notes,
  design relationships, ambiguity, contradictions and auxiliary image lineage.
- Per-property CONFIRMED / INFERRED / SPECULATIVE labels preserve the distinction
  between visible evidence, supported interpretation and unobserved hypotheses.
  Original references remain authoritative. Optional generated front/side/rear/3/4,
  top and detail sheets require a consistency review and may be restricted or
  rejected; they never confirm hidden geometry. Source-only operation is supported.
- [Robot and mechanism modeling](../skills/blender-robot-mechanism-modeling/SKILL.md)
  consumes the packet through staged geometry and clay checkpoints, mechanical
  skeletons, axes, bearings, actuator anchors, reachability, armor clearances and
  manufacturing logic. Materials and wear follow accepted form. Existing UV,
  surface, rig, animation, export and verification owners retain their boundaries.
- A standard-library PASS 0 validator and positive/negative regression cases
  check provenance, unresolved blockers, image reviews, file hashes and stage routing.

## Changed

The existing `Blender_Reference_Reconstruction_SKILL` alias resolves to the new
PASS 0 owner. Regenerate compatibility routers after upgrading; other legacy
names and MCP operation interfaces remain compatible. Modeling routes now place
PASS 0 before the relevant geometry owner. Surface-only, rigging, animation,
export and read-only requests retain their existing routes.

## Download and use

Download `Tools_C-v4.1.0.zip`, verify `SHA256SUMS.txt` and extract it. Run:

```powershell
.\check.bat --self
python -m unittest discover -s tests -v
python tools/sync_blender.py --project "C:\path\to\Blender-MCP-Co"
```

Python 3.10+ is required for the core harness. Blender and the MCP SDK are only
needed for applicable opt-in probes. Image generation is optional; no provider
or persistent API key is required by either skill. The ZIP contains canonical
skills and helpers; a separate compatible MCP integration supplies the server.
Internal instructions, project status, personal source images, diagnostic reports,
logs, captures and Git metadata are excluded from the public package.

## Verification boundaries

`release-verification.json` identifies the exact public commit, archive hashes
and fresh extracted-package checks. The supplied-mech workflow separately tested
the packet, one generated multiview sheet and a saved/reopened Blender macro
consumer. The generated sheet was RESTRICTED and the consumer's developed-form
clay review failed: the gates correctly stopped detail/material/wear escalation.
This demonstrates bounded handoff and refusal behavior, not production mech
quality, recovered hidden mechanisms, engineering certification or image-generator
geometric consistency. The validator checks structure and provenance declarations;
an agent must still inspect original images and actual rendered geometry.

The previous v4.0.3 release remains available for rollback.
