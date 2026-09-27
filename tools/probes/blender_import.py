"""Run only inside a disposable background Blender process; never save input files."""
import bpy
import json
from pathlib import Path
import sys

paths = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if not paths:
    # Probe Python API availability in the factory scene without a user asset.
    print("TOOLS_C_BLENDER " + json.dumps(dict(version=bpy.app.version_string, api=True)))
for value in paths:
    path = Path(value)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if path.suffix.lower() in (".glb", ".gltf"):
        bpy.ops.import_scene.gltf(filepath=str(path))
    elif path.suffix.lower() == ".blend":
        bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=False)
    else:
        raise ValueError("Unsupported probe format: " + str(path))
    meshes = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    rigs = [obj for obj in bpy.data.objects if obj.type == "ARMATURE"]
    if not meshes:
        raise ValueError("No mesh imported: " + str(path))
    result = dict(source=str(path), version=bpy.app.version_string, meshes=len(meshes),
                  vertices=sum(len(obj.data.vertices) for obj in meshes),
                  uv_meshes=sum(bool(obj.data.uv_layers) for obj in meshes),
                  armatures=[dict(name=obj.name, bones=len(obj.data.bones)) for obj in rigs],
                  actions=[action.name for action in bpy.data.actions],
                  materials=len(bpy.data.materials))
    print("TOOLS_C_BLENDER " + json.dumps(result))
