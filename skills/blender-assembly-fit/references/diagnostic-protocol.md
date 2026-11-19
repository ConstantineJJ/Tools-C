# FIT_INTEGRATION — diagnostic protocol

Scope: first version of `blender-assembly-fit`. **Read-only interpretation, not a new automatic contact solver.** For future `FIT_FLOAT / FIT_BURIED / FIT_POKE`, author separate behavior and tests; do not claim those detectors run here.

## Inputs, evidence, and sampling

- Identify the asset and explicitly named visible components, Blender version, units, evaluated scene, frame/pose, active Model Contract/reference and current status. On a full asset, begin with high-value suspect components and inspect neighbouring structural parts; do not compare all pairs by default.
- Record objective data only from actual Blender responses. Capture names, parents, `matrix_world`, local dimensions/world bounds, modifiers, active mesh visibility, material roles and source-linked constraints. A shared parent or socket name is a clue, not proof of physical attachment.
- Evaluate modifiers through depsgraph where available (`evaluated_get` / `to_mesh`); release temporary evaluated meshes. Include object-to-world transforms in geometric comparisons, especially non-uniform scale or mirrored objects.
- Use `tools/blender_snapshot.py` `measure_objects` when available (current bound: 1–256 named objects and 1,000,000 evaluated vertices). `tools/blender_contacts.py` handles selected pairs; sampled proximity gives an **upper bound on a nearest gap**, not an exact minimum separation for the whole surface.
- Candidate discovery: coarse bounding-box overlap / nearby bounds -> named pairs -> sample vertices/surface nearest queries -> optional targeted `BVHTree` ray/overlap checks. BVH can detect intersecting triangles but cannot alone classify intentional embed vs accidental penetration. Invisible or fully nested closed solids can have no crossing triangles.
- For meshes with open boundaries, degenerate topology, thin ribbons, disconnected components, curve/instance surprises or missing volume proof, **do not report definite buried/interior or stability results**. A normal can face either way on a sheet. `Non-Manifold` is a symptom, not a verdict.
- Prefer actual body/part relationships (socket, strap seat, shoulder collar, support beam, flush inset) over a generic proximity threshold. Record the physical unit, scale-relative tolerance and reason; never retrofit threshold after a failure.
- For a moving assembly, inspect neutral plus relevant extremes only when they are already defined and available. No still frame can prove clearance through a continuous sweep.

## Visual/functional integration cues

| ID | Suspicious pattern | What to confirm before `WARN` |
|---|---|---|
| I-01 seating | Plate or housing looks pasted onto another surface | Is there a collar, recessed seam, mounting land, bracket, or intended kitbash joint? Check side, 3/4 and closeup |
| I-02 shape language | One part uses conflicting bevel radius, curvature rhythm, mass or visual weight | Compare adjacent primary and secondary forms, reference and intended style; asymmetry may be deliberate |
| I-03 function | Cylinder has no plausible anchor, actuator has no opposing seat, cable route ends nowhere | Identify actual role/path, not only appearance; fantasy/sci-fi mechanics need internal consistency, not real-world dimensions |
| I-04 scale | Bolt, eye, foot, vent or trim differs unexpectedly from peers | Normalize for part size, perspective, camera distance, hierarchy, and user-requested exaggeration |
| I-05 silhouette | Detail obstructs focal area, creates accidental tangent, consumes negative space | View at intended distance and from more than one angle; functional projections may be required |
| I-06 material intent | Component looks imported due to unrelated roughness, panel color/edge treatment | Check clay view first: shader mismatch must not be misreported as poor geometry |
| I-07 assembly order | Fastener inaccessible, hinged cover apparently clips a frame or service door | Check the intended motion/access plan; route actual kinematics to robot/mechanism specialist |
| I-08 identity | Named required feature obscured, displaced or visually overwhelmed | Use only source-backed reference or approved design invariant; record the exact view and protected feature |

Use reference-based comparison only if a reviewed source/setup exists. A generated image does not certify hidden parts. For stylized humanoids review front, side, back and high/low views where relevant; full humanoid acceptance remains with foundation QA. For props/vehicles, choose camera views based on actual asset axes; do not assume that forward is always -Y.

## Triage without invented certainty

1. **Observed**: precise world-space measurement, named connection, and/or inspected visual evidence. Label L1 or L4 accordingly.
2. **Interpretation**: explain the strongest plausible reason it looks foreign or poorly integrated, plus at least one alternative (intentional style, concealed brace, motion clearance, material mismatch).
3. **Status**: use WARN for a subjective finding; FAIL only against a specific MUST PRESERVE/HARD invariant demonstrated by direct evidence; SKIP if evidence or comparator absent; PASS only for named verified criteria.
4. **Recommendation**: identify *smallest local action* and its modeling owner, not a command to mutate through this diagnostic skill.
5. **Regression concerns**: warn if the proposed correction may remove negative space, ruin silhouette, change pivots/slots, collide in another pose, break UV/rig or hide named identity.

Report e.g.:

`FIT_INTEGRATION | WARN | /Robot/Arm_R/ShoulderPlate | visual seam floats above shoulder collar in side view | sampled surface gap approx. 0.018 scene units (not exact global min) | side/frame 1 | compared to approved plate seating sketch | medium | owner: blender-robot-mechanism-modeling, inspect attachment land`

Do not output invented coordinates, a computed gap, or PASS without actually inspecting the scene and images.

## Performance and failure behavior

- Cost grows with overlapping part pairs, evaluated triangles and poses. Broad-phase before BVH; scope suspicion to ≤32 named pairs per exploratory pass unless user/contract requires more; record truncated/untested regions. This is a *work cap*, not an acceptance threshold.
- If the Blender MCP bridge is unavailable, return `SKIP / blocked` with the missing operation. A user-supplied still can support a tentative visual WARN but cannot certify contact, hidden parts or actual material properties.
- On a timeout or unknown execution result, inspect the live scene and existing outputs before retrying. Diagnosis alone must not save or edit the user scene.
- Keep capture settings stable (target/frame/framing/resolution/light/mode) for comparison; open actual PNGs before visual PASS. Existing `verification` owns receipts, no duplicate checker.
