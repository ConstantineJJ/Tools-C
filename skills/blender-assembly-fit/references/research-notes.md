# Assembly Fit — research notes and search tags

Research date: **2026-11-19**. Scope: professional assembly/design practice plus official Blender 5.3 manual, Python API and selected official release notes. The cited references are English-language sources outside Latvian domains. These are original paraphrases and research prompts, not copied code, templates, or test fixtures from Construct or other projects.

## High-value search phrases / tags

| Tag | Search phrase to revisit | Operational lesson for FIT_INTEGRATION |
|---|---|---|
| `silhouette-first` | "hard surface mass-out primary secondary tertiary forms" | Evaluate component from target camera and silhouette before micro detail |
| `functional-assembly` | "believable machinery assemble take apart support joints" | A detail should have plausible assembly role, mounting land or intentional nonstructural status |
| `negative-space` | "hard surface negative space readability accidental tangent" | Surfaces and gaps should direct the eye; busy texture cannot repair wrong large masses |
| `visual-weight` | "hard surface proportions visual hierarchy focal areas" | Compare volumes and emphasis, not arbitrary absolute symmetry |
| `purposeful-greeble` | "kitbash greebles functional detail real hardware" | Explain each prominent accessory's purpose or decorative intention |
| `blockout-early` | "mechanical asset mass out blockout design review" | Spot inappropriate features early while redesign is cheap |
| `evaluated-depsgraph` | "bpy evaluated_get depsgraph object to_mesh" | Measure geometry as evaluated, not merely original mesh vertices |
| `BVH-broadphase` | "Blender BVHTree overlap find_nearest ray_cast" | Use broad phase to limit candidate pairs; overlap alone is not wrongness |
| `surface-proximity` | "Geometry Proximity nearest surface Blender 5.3" | Use real surfaces for narrow-phase sampling; preserve uncertainty |
| `open-mesh-trap` | "non manifold open mesh ambiguous inside outside" | Open/thin sheets do not support watertight-volume assumptions |
| `fixed-camera-QA` | "orthographic front side back 3/4 same camera comparison" | Unchanged framing, light, scale and pose protect honest comparison |
| `intentional-asymmetry` | "stylized asymmetric hard surface design visual weight" | Differences from mirror side are questions, not automatic failures |
| `read-only-safety` | "mesh modifier destructive geometry QA" | Inspect rather than apply Booleans, remesh or scene cleanup during review |
| `contact-vs-design` | "mesh intersection intentional overlap normal bake assembly" | A physical contact does not prove a coherent, believable design |

## Primary source index

| ID | English-language source | Adopted concept | Boundary / caveat |
|---|---|---|---|
| B01 | [Blender 5.3 manual: Geometry Proximity](https://docs.blender.org/manual/en/5.3/modeling/geometry_nodes/geometry/sample/geometry_proximity.html) | Closest point on target geometry for local sampling | Closest sample is not certified global part-to-part gap |
| B02 | [Blender Python API: BVHTree](https://docs.blender.org/api/current/mathutils.bvhtree.html) | Surface acceleration, triangle overlap, raycast, nearest query | Overlap and nearest alone do not determine design intent or complete containment |
| B03 | [Blender Python API: Depsgraph](https://docs.blender.org/api/5.3/bpy.types.Depsgraph.html) | Inspect evaluated object geometry and instances | Different evaluated/instanced paths need explicit scope |
| B04 | [Blender 5.3 manual: Mesh Boolean node](https://docs.blender.org/manual/en/5.3/modeling/geometry_nodes/mesh/operations/mesh_boolean.html) | Reference for Boolean semantics and implementation choices | Do not execute destructive Boolean for a read-only fit review |
| B05 | [Blender 5.3 manual: Clean Up](https://docs.blender.org/manual/en/5.3/modeling/meshes/editing/mesh/cleanup.html) | Loose geometry and cleanup terms can indicate mesh anomalies | Do not auto-clean; open surfaces or loose geometry can be intended |
| B06 | [Blender 4.5 LTS modeling notes](https://developer.blender.org/docs/release_notes/4.5/modeling/) | Boolean solver evolution makes version-specific method verification necessary | Release notes are not a performance guarantee for arbitrary meshes |
| B07 | [Blender 5.3 bugfix notes](https://developer.blender.org/docs/release_notes/5.3/bugfixes/) | Geometry Boolean and modifier edge cases still exist | Prefer stable read-only narrow-phase queries and bounded probes |
| B08 | [Blender 5.3 UI notes](https://developer.blender.org/docs/release_notes/5.3/user_interface/) | Data inspection overlays aid validation of geometry attributes | Optional diagnostic UI, not algorithmic proof |
| P01 | [CG Cookie: POTHEAD Hard Surface Character](https://www.cgcookie.com/courses/pothead-create-a-hard-surface-character-in-blender/) | Character hard-surface decisions should preserve crisp notches, joints and coherent panel transitions | A modeling course, not an automated integrity test |
| P02 | [Frank Polygon, ArtStation: Boolean + Sub-D 123 Blocks](https://frankpolygon.artstation.com/blog/oebM/boolean-sub-d-hard-surface-modeling-123-blocks-exercise-tutorial) | Recognize primary/secondary shapes; assess intersection layout, modifier order and available bevel room | Dimensional modeling example, not evidence of design intent |
| P03 | [CG Cookie: Modeling Heavy Equipment Backhoe](https://www.cgcookie.com/courses/modeling-heavy-equipment-backhoe-series) | Parts built against reference, reviewed piece by piece and ordered for assembly | Course workflow, not evidence of automated support detection |
| P04 | [CG Cookie: The Art of Good Topology](https://blog.cgcookie.com/posts/the-art-of-good-topology-blender/) | Non-destructive editability and distinguishing intentional separate pieces from malformed topology | Topology alone cannot decide whether design looks foreign |
| P05 | [Polycount: Modeling TV](https://polycount.com/discussion/236930/modeling-tv) | Detail that contributes nothing to silhouette may belong in textures, not separate game meshes | Community discussion, not a universal modeling rule |
| P06 | [CG Cookie: Introduction to Hard Surface Modeling](https://www.cgcookie.com/courses/introduction-to-hard-surface-modeling) | Start with dimensions and necessary segments before detailing | Intro training, not an assembly-validation algorithm |

## Feature-scope decisions

- Version 1 focuses on **human/agent visual assessment supported by Blender measurements**; it does not promise an implemented automated detector.
- `FIT_INTEGRATION` is a visual assembly quality question. A measurable gap can support a WARN; contact does not automatically PASS styling, and no contact does not automatically FAIL.
- Keep pure geometry classifiers (`FIT_FLOAT`, `FIT_BURIED`, `FIT_POKE`) and static stability for independent future patches, not this first one.
- Use existing Tools_C `verification` / `blender_contacts.py` / `capture_viewport`; no new MCP operation, Model Contract schema, arbitrary thresholds, or test harness required.
- Preserve project-neutrality. A project-specific slot, forward axis or chassis rule is evidence from the active project, not a default in this skill.

**Licensing:** only general ideas learned from public sources are used. Original descriptions and procedures are authored for Tools_C; no third-party code, images, examples or substantial document text are bundled.
