# Weapon module interface

Owner: [weapon module](../SKILL.md). Read at W0 and W5.

The interface is project data, not a Tools_C default. A project declares it in
`.tooling/weapon-modules.json` (schema 1). Without that file, record the existing
asset's conventions (forward axis, socket object, pivots) in the task report and
run the checker with an equivalent temporary file outside the project.

```json
{
  "schema_version": 1,
  "forward_axis": "-X",
  "markers": {
    "socket": "Holder_SocketReceiver",
    "muzzle": ["Muzzle"],
    "optional": ["FX_Exhaust", "Shell_Eject"]
  },
  "match": "suffix",
  "socket_origin": [0.0, 0.0, 0.0],
  "tolerance": 0.002,
  "budgets": {"max_triangles": 12000, "max_materials": 10, "max_emissive_materials": 4}
}
```

- `forward_axis`: firing direction in Blender object space of the module root
  (`+X`, `-X`, `+Y`, `-Y`, `+Z`, `-Z`). glTF conversion is handled by the checker.
- `markers`: names of objects/nodes. `match: "suffix"` accepts project prefixes such
  as `Laser_C_Muzzle`; `exact` requires the literal name. Muzzle markers must lie at the
  front of the module along the forward axis (within `tolerance`).
- `socket_origin`: where the socket must stay relative to the module root; omit when
  the project has no fixed socket point.
- `budgets`: project limits; `null` or omitted means not evaluated (reported as SKIP).

## Checks

In Blender (source, evaluated meshes, through `execute_blender_python`):

```python
import runpy
wm = runpy.run_path(r"<Tools_C>/tools/weapon_module.py")
_result = wm["check_blender"](wm["load_interface"](r"<project>/.tooling/weapon-modules.json"), "Laser_C")
```

On the delivered file (no Blender needed):

```text
python tools/weapon_module.py glb OUTPUT.glb --interface PROJECT/.tooling/weapon-modules.json
```

Both report PASS/WARN/FAIL/SKIP items: marker presence, muzzle leading the forward
axis, socket offset, triangle/material/emissive budgets. A PASS is interface and
budget evidence only; silhouette, function map and visual quality remain W1–W4 reviews.
Export validation can run the GLB check automatically with `"weapon_interface"` in
its job file (see [export validation](../../blender-export-validation/SKILL.md)).
