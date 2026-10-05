# Auxiliary technical references

Use available image generation through its supported adapter. Keep provider, model,
resolution and retry cost replaceable; never install a generator or switch paid
providers merely to satisfy this skill. If unavailable, record the limitation and
deliver analysis with source crops/landmark notes. Crops do not recover hidden views.

## Prompt contract

Save the exact prompt and list original inputs. Start from analyzed source facts,
not from a previous generated design. Include:

```text
Purpose: auxiliary technical reconstruction for the modeling agent, not CAD.
Source of truth: original image IDs [...]. Preserve observed design over stylistic polish.
Object/pose/axes: [...]; same pose and scale across panels; neutral light/background.
Locked identity: component IDs, number of repeated parts, silhouette ratios/ranges,
landmark heights, left/right distinctions and attachment relationships [...].
Views: front, object-right side, rear, source-matched 3/4. Prefer near-orthographic
front/side/rear without calling them metrically exact. Add top/close-ups only as needed.
Uncertainty: hidden regions [...] are SPECULATIVE; use minimal plain placeholder
envelopes, visually mark them; do not add invented engine vents/cables/doors as fact.
No redesign, no new parts, no conflicting counts, no numeric engineering annotations.
Readable separation of structure and armor; minimal wear so shapes can be reviewed.
```

Keep generated labels as aids only; the external JSON is the reliable confidence
record. A generated rear view cannot prove what the original rear looks like.
Front/side/rear and close-ups must retain one manifest version, same handedness,
feature counts, size relationships, number of joints and construction. Prefer a
single sheet with shared scale/ground/height landmarks; separate generations still
need pairwise review. Lens/pose differences must be recorded rather than mistaken
for changed proportions. A source 3/4 pose can coexist with a proposed neutral pose
only if their correspondence is explicit; do not measure them as identical poses.

## Acceptance matrix

Review actual pixels, not the generator's success message. For each auxiliary file
record `identity`, `proportions`, `part_counts`, `construction`, `handedness` and
`silhouette`, with PASS/FAIL/WARN/SKIP and observations. Name regions/views affected.

- **ACCEPTED**: all six checks PASS, useful within the stated estimate precision.
  Still auxiliary; exact thickness, dimensions and hidden details remain uncertain.
- **RESTRICTED**: useful for named roles only (e.g. coarse side depth). List permitted
  and forbidden uses per region/view. Never use a count/construction FAIL as a modeling
  instruction. Crop/exclude a failed panel if that makes the remaining role clear.
- **REJECTED**: primary identity, count or construction cannot be trusted, or no
  reliable useful region remains. Keep a record; do not use it for construction.
- **UNREVIEWED**: image exists but cannot advance the gate as an accepted reference.

Compare original and generated launcher counts, wheel counts, window bays, handles,
major armor breaks, joint axes and attachment positions where applicable. Compare
normalized widths/heights/depth cues to analysis ranges; declare which dimensions
cannot be measured in the perspective source. Do not assert exact multiview
consistency from eyeballing a contact sheet.

Target one defect per corrective attempt, preserving locked source facts. After
two failed corrections, proceed only from reliable source information or stop
dependent work. Save failed attempts with their status; do not hide drift through
an increasingly detailed prompt or select an attractive new design.
