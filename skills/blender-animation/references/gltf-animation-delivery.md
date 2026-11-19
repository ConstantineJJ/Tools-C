# glTF animation delivery (Blender 5.x)

Read with [animation](../SKILL.md) and [export validation](../../blender-export-validation/SKILL.md)
when clips must survive GLB export. Observed on Blender 5.3 / glTF I/O 5.3.43 (2026-11-18).

## One clip = one NLA track name

- Blender 5.x Actions are slotted: an Action stores channels per slot. When pushing to
  NLA, set `strip.action_slot` to the slot that holds the curves, or the strip plays nothing.
- Name every NLA track with the clip name (`Laser_R_Fire`). Export with
  `export_animation_mode='NLA_TRACKS'` and `export_merge_animation='NLA_TRACK'`; tracks
  with the same name on objects and material node trees merge into one glTF clip.
- Clear `animation_data.action` after pushing to NLA so the active Action does not leak
  into every clip.
- Key clips from frame 0 and keep `export_anim_slide_to_zero` at its default (False).
  Blender 5.3 raises `KeyError` in `get_sk_drivers` when slide-to-zero meets material
  NLA tracks; the export aborts. Fix the data, not the flag.

## Material / shader animation

- Shader node values (emission colour/strength, base colour, roughness, metallic) export
  only through `KHR_animation_pointer` with `export_pointer_animation=True`. Channels then
  target `/materials/N/...`, not nodes. Custom node groups and procedural inputs are not
  animatable in glTF: drive a Principled BSDF socket directly.
- Godot import support for `KHR_animation_pointer` is version-dependent. Verify the clip
  in the target engine (see [Godot asset integration](../../godot-asset-integration/SKILL.md));
  if unsupported, deliver the state as a named material parameter driven by game code.
- `tools/glb_inspect.py` validates a bounded pointer subset (emissive, base colour,
  metallic/roughness, emissive strength, node TRS) and reports `target`/`pointer` per channel.

## Rotating parts

- Put the object origin on the physical axis before keying; animate one Euler axis with
  linear interpolation for a constant spin. A loop of N full turns keys 0 and N·2π.
- After export, the node rotation channel must exist and the node origin must stay on the
  axis in the fresh import; capture two frames to see the rotation.
