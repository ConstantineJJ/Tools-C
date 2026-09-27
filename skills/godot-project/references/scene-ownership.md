# Scene ownership and instancing

Read when changing imported scenes, shared Resources, instanced scenes or large sets of repeated objects.

Identify whether a value belongs to the imported asset, an authored wrapper scene, a per-instance override, a shared Resource or a runtime-spawned node. Reimport can replace imported hierarchy and values; keep reusable authored gameplay nodes and intentional offsets under a stable owner. Inspect the actual hierarchy and overrides before moving a value.

For per-instance edits, check whether a Resource is shared. A local-looking material or configuration change can affect another instance. Test at least one other consumer and a fresh/reinstantiated copy after an ownership edit. Use stable logical IDs for authored entities; scatter indices can change when generation order changes.

For many repeated props, measure draw calls and frame time before adopting MultiMesh or batching. Account for material compatibility, culling bounds, independent animation, collision and interaction. No universal object-count cutoff is reliable across projects.

For imported meshes, verify target scale/orientation, normals/tangents and materials in the project scene against a known-good asset. Diagnose exporter, importer and authored-scene effects separately. A clean import is only structural evidence.
