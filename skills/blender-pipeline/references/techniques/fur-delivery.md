# Fur preview, surfaces and delivery

Read for native Hair Curves, fur materials, groom optimization or furred GLB
delivery. Anatomy stays with the animal owner, skin revisions with sculpting,
export with export-validation. These checks reuse the existing model contract,
capture and export evidence; they do not introduce another pass ledger.

## Keep iteration cheaper than a full groom

Resolve the skin, eyeball volume and eyelid/ear contact first. Preview regional
guides and a sparse lit coat before full density. Use separate muzzle, cheek,
mane, ear-back, body and tail flow/length controls as needed by the species.
Blend spatial masks continuously: avoid rectangular projection borders and hard
coordinate thresholds. Keep the face's minimum coverage independent of mane or
crown shortening. Blend pigment zones rather than replacing them with binary
rectangles; inspect the actual tabby/spot pattern, skin gaps and partings.

After skin edits inspect skin → contacts → roots/UV/rest → flow/length → pigment
→ whiskers. Preserve unaffected groom. A user may revise approved forms later;
this calls for scoped dependency repair, not blame or automatic reconstruction.
Match the source pose, framing and a second projection/three-quarter view after
profile edits; one contour cannot establish forehead/cheek width or eye sections.

## Minimal renderer and round-trip checks

Before a large groom, make a disposable sparse patch with two distinctly colored
strands or regions using the intended material-index/attribute path. Render in
the actual source renderer under neutral light. Confirm both colors in pixels;
material names/indices or a successful JSON response cannot prove shader behavior.
If a path fails, isolate it and use an explicit supported assignment; do not
describe one scene's failure as a universal Blender defect.

For GLB, test a tiny delivery patch with the actual COLOR_0 → base-color binding,
UV alpha atlas and small iris/whisker sentinels. Inspect attributes, texture links,
alpha mode/cutoff and both card sides, then export and fresh-import in a separate
factory process and render again. Keep the source-render and imported-render
checks distinct: glTF cannot carry every native shader graph or groom system.
The export probe refuses direct native `CURVES`; use an explicit delivery copy
with supported representation and confirm inclusion/coverage after import.

## Budgets, bake and LOD

Before full density, agree target renderer/platform, camera distance/resolution,
triangle/strand/texture/VRAM/frame-time/file-size budgets and protected features:
silhouette, ear-back density, brows/whiskers, pigment pattern, tail and partings.
Budgets are project choices, not species anatomy rules. Keep editable guides and
source sculpt recoverable separately from delivery copies; exclude hidden recovery
grooms and references explicitly from export. Do not turn every hair into a tube.

Use a separate lower-density skin copy and bake needed detail with explicit
high/low/cage/ray settings. Bake short undercoat coverage and pigment into base
color/normal/roughness where appropriate; inspect seams, ray misses, thin patches
and continuity under the cards. A bare smooth head plus a few cards is not an
equivalent replacement for a short native coat. Static reduction does not prove
deformation-ready topology.

Reserve narrower alpha cards/clumps for silhouette, mane, tail and characteristic
tufts; a shared atlas and supported COLOR_0 pigment can reduce material variants.
Inspect padding/dilation, mip levels, backfaces, alpha cutoff and specular under
moving light. Broad cards and strong flat highlights must not become white
leaves/needles. Reduce redundant strands adaptively; count reduction alone cannot
measure coverage. Test near/mid/far LOD and transitions at fixed screen sizes.
Target-engine alpha/shadow/fade behavior, overdraw and draw calls require actual
engine measurement; fewer triangles can still render more slowly.

Compare source and delivery at identical cameras/light/resolution: front, both
three-quarter views, profile, ear backs and face closeup as relevant. Use neutral
QA without depth of field/compositor; keep beauty settings separate. A requested
10% quality loss is a viewing criterion to agree and review, not a decimation
ratio or automatic IoU PASS. Check pigment, microstructure and silhouette.

## Compact statistics and bounded evidence

Record source vertices and evaluated triangles separately; native stored/evaluated
curve counts and all-zero-radius curves separately from actually visible strands.
Record cards, atlas resolution, material count and actual GLB bytes. Zero-radius
or hidden curves do not prove visible coverage. Without profiling, visible hairs,
draw calls, overdraw and VRAM remain UNKNOWN; do not derive them from slots/counts.
`tools/blender_snapshot.py:delivery_statistics(object_names)` reads direct
source/evaluated counts without changing the snapshot schema. Missing radius data
stays unknown. The export probe includes these statistics plus actual GLB bytes;
native GeometrySet components/instances and card/atlas roles need separate checks.

Use fixed `solid`/`material_preview` captures from
[evidence tools](../../../../docs/blender-evidence.md). References are viewport
image empties: reference-only/overlay viewing is a viewport comparison, not an
implemented render mode. Renderable overlays/masks require task-specific setup;
never claim the capture helper renders the reference empties. Keep source data
and framing unchanged when comparing clay, lit coat and references.

Split capture/export/import into separate bounded jobs with unique output paths
and completion markers using the existing file tools. After timeout inspect the
marker, log, process and artifacts before any replay; a missing marker is unknown,
not proof that no work occurred. `blender_jobs.py` statuses apply to curve batches,
not render/export jobs. For live file loads follow foundation's new health RPC
and independent scene-info requirement; offline processes never repair the bridge.

Basis: source attachment and validity are documented in Blender
[Curve Properties](https://docs.blender.org/manual/en/5.2/modeling/curves_new/properties.html)
and [Attachment Info](https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/hair/read/hair_attachment_info.html).
The cat handoff supplied the mask/card/material failure cases; they remain
case-specific observations, not a generic converter or a 90%-quality guarantee.
