# Animation and export details

Read when constructing Actions, secondary-motion chains or diagnosing exporter/engine differences.

Animation starts with intent, key extremes, timing, arcs and cleanup. For attacks inspect anticipation, contact and recovery at the target viewing camera when one is defined. For locomotion inspect support/contact frames, foot sliding, facing policy and first/last loop continuity. For idle inspect stance readability and unnecessary noise. Use project clip names and root-motion policy; example action names from another character are never defaults.

Cloth-like accessories need a target behavior choice: engine-driven bone chain, baked animation or engine-native simulation. For a bone chain, inspect anchor, segment spacing, roll, progressive weights and mesh bend resolution. Test lag, turn, sudden motion and recovery. Blender constraints or IK used for authoring may require baking because the target runtime may not reproduce them.

Inspect F-curves for accidental keys, Euler flips, scale keys, drift, pops and intersections.
Export inclusion and round-trip acceptance belong to [export validation](../../blender-export-validation/SKILL.md).
