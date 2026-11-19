# Game atlas bake (procedural → glTF PBR)

Owner: [surfaces](../surfaces.md). Use when procedural/wear materials must reach a GLB.
Proven on Laser_R (36 meshes, 10.7K tris, Blender 5.3, RTX OptiX, 2026-11-19).

1. **Backup, then freeze geometry.** One rotation copy; apply Booleans/bevels via
   `bpy.data.meshes.new_from_object(evaluated)` (keeps custom normals). Delete cutters.
   Remove empty material slots left by Booleans.
2. **One atlas for opaque parts.** Emissive/animated materials stay separate (glTF can
   animate material factors, not baked pixels). Smart UV (≈55°) → average island scale →
   pack (margin ≈0.004). Record coverage and px/m (Laser_R: 49%, ≈800 px/m at 2K).
3. **Bake through EMIT, not DIFFUSE.** Diffuse Color is black on metallic surfaces. For each
   channel route the shader output (colour, roughness, metallic, AO node) into an Emission
   shader, set one Image node active in every source material, select all atlas objects.
   Base colour image sRGB; everything else Non-Color. Normal: `type='NORMAL'`, tangent space,
   OpenGL (+Y) — matches glTF. Margin 8 px, `EXTEND`.
4. **Never bake synchronously over MCP.** Use `bpy.ops.object.bake('INVOKE_DEFAULT', ...)`
   inside a VIEW_3D context override, return immediately, poll
   `bpy.app.is_job_running('OBJECT_BAKE')`, then restore nodes and save. A blocking bake
   times out the bridge (`UNKNOWN_EXECUTION`). Helper: [atlas_bake.py](../../../blender-posteffects-polishing/scripts/atlas_bake.py).
5. **Pack ORM** with numpy: R=AO, G=roughness, B=metallic (Non-Color PNG).
6. **Delivery material:** Principled with BaseColor, ORM (G→Roughness, B→Metallic),
   Normal Map node (same UV map); feed ORM.R into a `glTF Material Output` group input
   `Occlusion` so the exporter writes `occlusionTexture`. Store the source material name in
   an object property and keep sources with fake user for re-bake.
7. **Verify:** render the same cameras procedural vs baked; inspect GLB material slots
   (base/MR/normal/occlusion) with `tools/glb_inspect.py`; fresh-import probe.

Size note: three 2K PNGs ≈ 8.5 MB in GLB. JPEG base colour or WebP needs target-engine
confirmation first.
