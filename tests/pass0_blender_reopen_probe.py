"""Fresh-load declared macro-probe state, not all Blender file contents."""
import json
from pathlib import Path
import sys
import bpy

out=Path(sys.argv[sys.argv.index('--')+1]).resolve()
expected=json.loads((out/'consumer_state.json').read_text())
for scene in bpy.data.scenes:
    for layer in scene.view_layers:layer.update()
actual={o.name:dict(matrix=[list(r) for r in o.matrix_world],vertices=len(o.data.vertices),polygons=len(o.data.polygons),mesh=o.data.name) for o in bpy.context.scene.objects if o.type=='MESH'}
assert actual==expected,'Reopened declared geometry/placement/shared mesh state changed'
result=dict(status='PASS',objects=len(actual),blender_version=bpy.app.version_string,
            file=bpy.data.filepath,scope='Independent reopen with auto-run disabled; source mesh counts, world matrices and shared datablock names only.')
(out/'consumer_reopen.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS0_REOPEN '+json.dumps(result))
