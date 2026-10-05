# Developing forms beyond blockout

Read for visible cubes, balls, tubes or slabs that still look like construction
placeholders. This is a shared technique, not another domain owner. Keep deliberate
toy, graphic and low-poly shape language when the design calls for it.

## Diagnose before smoothing

| Visible problem | Change that addresses it | What does not address it |
|---|---|---|
| Faceted lighting, acceptable silhouette | Inspect normals/sharp edges; suitable smooth shading | Rebuilding unrelated forms |
| Angular outline on an intended curved surface | Sufficient path/profile sampling or controlled subdivision | Shade Smooth alone |
| Razor edges on manufactured parts | Scale-aware geometric bevel, retaining broad planes | Rounding every face into a cushion |
| Smooth but obviously spherical/tubular/slab-like form | Redesign mass distribution, sections, taper and bends | More segments, bump or strand count |
| Visible intersections at a continuous organic junction | Construct a continuous transition in the scoped geometry | Joining object containers alone |

Smooth shading changes normal interpolation, not the silhouette. Subdivision can
smooth geometry but cannot choose the correct anatomy, growth pattern or garment
construction. Compare evaluated output; avoid a universal modifier stack. The
[modifier contract](../../../blender-character-modeling/references/modifiers-transforms.md)
protects existing data. Remesh is conditional on disposable topology and the
[sculpting owner's safeguards](../../../blender-sculpting/SKILL.md), not a default
cleanup of bound/UV-authored assets.

## Form pass

1. **Read the whole object.** Identify intended contour, big masses, main direction,
   cross-section changes and negative spaces. Choose the primary reference/view;
   describe uncertain depth instead of inventing reference measurements.
2. **Replace placeholders where needed.** Use an editable control mesh or sections
   with independent width and depth. Locate bends and changes of volume deliberately.
   Keep actual separate boards, cloth layers and ornaments separate.
3. **Develop transitions.** Maintain a gradual change of section and direction in
   continuous skin, branch junctions and soft fabric. Check roots and attachment
   zones as well as tips. Preserve intentional seams and creases.
4. **Choose edge treatment.** Use smooth normals for appropriate surfaces, enough
   samples for the intended outline, controlled bevels for rigid edges, and local
   smoothing for unwanted ripples. Retain designed planes and sharp features.
5. **Prove the result before detail.** Inspect a silhouette and a neutral untextured
   view at production distance plus the affected close view and an alternate view.
   Then check the intended material. Keep fixed camera, light and exposure for each
   BEFORE/AFTER pair. Do not hide a mass error with fur, leaves, scratches or bloom.

There is no mandatory human-approval pause between these steps within an authorized
task. Record KEEP/CORRECT/REVERT and autonomously repair defects inside scope.

## Acceptance observations

Name the actual visual criterion rather than claiming universal beauty:

- Does the silhouette express the intended object, rather than expose accidental
  assembly primitives? A watermelon or deliberately spherical ornament may pass.
- Do sections describe its anatomy, growth, construction or material at this style?
- Are continuous transitions free of accidental necks, bulges, rings and corners?
- Are separate pieces connected credibly, without erasing their construction?
- Does the form still read when tertiary detail and color patterns are hidden?
- Did smoothing lose approved landmarks, volume, planes or clearance?
- Did the protected alternate view improve or remain acceptable?

A triangle count, successful mesh validation or a modifier name cannot answer these
questions. Fail the named visual criterion when the inspected image still shows it.
Use [QA profiles](qa-profiles.md) to select checks proportional to the change.

## Recipes and editable examples

Use [form recipes](form-recipes.md) for limbs, hair, ribbons, fur and foliage.
The examples deliberately isolate one construction decision; they are not
production anatomy, approved art direction or presets to copy into every project.

- [Editable comparison scene](../../assets/form-examples/Form_Examples.blend)
- [Limb sections](../../assets/form-examples/limb.png)
- [Limb alternate view](../../assets/form-examples/limb_threequarter.png)
- [Hair width and thickness](../../assets/form-examples/hair.png)
- [Hair alternate view](../../assets/form-examples/hair_threequarter.png)
- [Ribbon construction](../../assets/form-examples/ribbon.png)
- [Canopy masses](../../assets/form-examples/canopy.png)
- [Fur hierarchy](../../assets/form-examples/fur.png)

Rebuild with [the example generator](../../../../tools/blender_form_examples.py)
in a separate background Blender process. It refuses to overwrite an existing
example output. [Form helpers](../../../../tools/blender_forms.py) supply transported
frames, independent ellipse profiles, arc-length UVs, curve batches and parenting
with world placement retained. They do not decide artistic shape or validate likeness.

## Sources and scope

Blender's [smooth shading](https://docs.blender.org/manual/en/4.5/scene_layout/object/editing/shading.html),
[geometric bevel](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/bevel.html)
and [subdivision](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/subdivision_surface.html)
explain the separate technical operations. The need for a form pass and the paired
recipes comes from the 2026-10-04 watermelon-diorama report and inspected images.
These examples demonstrate construction, not a guaranteed artistic score.
