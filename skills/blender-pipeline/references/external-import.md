# External model intake and repair

This workflow accepts any supplier, generator or licensed source; no provider is
required. Identify format, source/provenance, target use and the delivered data.
Open in a disposable scene/process for inspection; do not replace a production
asset before understanding its consumers. Unknown provenance stays unknown.

1. Inventory objects, mesh count, hierarchy, hidden helpers and material slots.
2. Measure dimensions, units, transforms and forward/up axes; compare target scale.
3. Inspect normals, face orientation, tangents and mirrored transforms using
   diagnostic light/views. Do not diagnose orientation from silhouette alone.
4. Inspect UV sets, seams/stretch/overlap and intended tiling; resolve image paths,
   PBR channels, color spaces, texture dimensions and material assignments.
5. Diagnose topology, loose/degenerate geometry, internal faces, mesh separation and
   density. Separate rigid pieces may be intentional; automatic retopo is optional.
6. List skeleton names, hierarchy, rest transforms and deform flags; map only the
   semantic roles required by the target profile. Never impose a global bone count.
7. Inspect weights and test actual joint bends/twist. Distinguish weights, topology,
   pivots and rest-pose causes before choosing the repair owner.
8. List clip names, ranges, FPS assumptions, channels, loop behavior, root motion
   and stray tracks. Preserve source names through mapping when renaming would
   break consumers. Preview contact/extreme poses and transitions.
9. Make the minimum Blender repairs via modeling/sculpt/retopo/surface/rigging
   references. Optimize only against a declared target budget and measured cost.
10. Export to target format, fresh-import, compare skeleton, clips, materials,
    scale/orientation and deformation, then validate in the target engine.

Use [QA](qa.md) and the central verification checklist. Import success alone does
not establish topology, animation quality, production readiness or release rights.
Report which delivered features were retained, repaired, rejected or unverified.
