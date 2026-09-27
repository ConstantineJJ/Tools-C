"""Factory-process export/import evidence probe. Pass a JSON job after --."""
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

sys.path.insert(0,str(Path(__file__).resolve().parent))
from blender_snapshot import snapshot
from handoff_snapshot import canonical_bytes


def bounds(names):
    graph=bpy.context.evaluated_depsgraph_get()
    points=[o.evaluated_get(graph).matrix_world @ Vector(v) for name in names
            for o in [bpy.data.objects[name]] if o.type in {'MESH','CURVE','FONT','SURFACE'}
            for v in o.evaluated_get(graph).bound_box]
    if not points: raise ValueError('No geometry for bounds')
    return dict(min=[min(v[i] for v in points) for i in range(3)],max=[max(v[i] for v in points) for i in range(3)])


def run(job):
    if not bpy.app.background: raise ValueError('Probe requires disposable background Blender')
    if job.get('mode') not in ('export','import'): raise ValueError('Unknown probe mode')
    output=Path(job['output']).resolve()
    if output.exists(): raise ValueError('Evidence output must be new')
    if job['mode']=='export':
        source=Path(job['source']).resolve(strict=True)
        glb=Path(job['glb']).resolve()
        if glb.exists() or glb.suffix.lower()!='.glb': raise ValueError('GLB output must be new .glb')
        bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
        names=job['objects']; actions=job.get('actions',[])
        if not names or len(set(names))!=len(names): raise ValueError('Explicit unique objects required')
        bpy.context.scene.frame_set(job.get('frame',1))
        before=snapshot('source',names,protected=names,action_names=actions)
        # Fail rather than exporting shape keys or animated topology with an unproven contract.
        for name in names:
            obj=bpy.data.objects[name]
            if obj.type=='MESH' and obj.data.shape_keys: raise ValueError('Shape-key delivery needs a dedicated target contract')
        bpy.ops.object.select_all(action='DESELECT')
        for name in names: bpy.data.objects[name].select_set(True)
        bpy.context.view_layer.objects.active=bpy.data.objects[names[0]]
        options=dict(filepath=str(glb),export_format='GLB',use_selection=True,export_animations=bool(actions),
                     export_cameras=False,export_lights=False)
        supplied=job.get('export_options',{})
        if set(supplied)&set(options): raise ValueError('Cannot override bounded export scope/output')
        available=set(bpy.ops.export_scene.gltf.get_rna_type().properties.keys())
        if set(supplied)-available: raise ValueError('Unknown exporter option')
        options.update(supplied)
        glb.parent.mkdir(parents=True,exist_ok=True)
        result=bpy.ops.export_scene.gltf(**options)
        if 'FINISHED' not in result or not glb.is_file(): raise RuntimeError('Export did not finish')
        after=snapshot('source',names,protected=names,action_names=actions)
        if canonical_bytes(before)!=canonical_bytes(after): raise RuntimeError('Export changed declared source snapshot')
        data=before
    else:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        # Import converts seconds to Blender frames using the scene time base.
        # Set it before invoking the importer, including fractional frame rates.
        fps=job.get('fps',24)
        if type(fps) not in (int,float) or not 1 <= fps <= 1000:
            raise ValueError('Invalid import FPS')
        bpy.context.scene.render.fps=round(fps)
        bpy.context.scene.render.fps_base=round(fps)/fps
        startup_objects=set(bpy.context.scene.objects)
        import_options=dict(filepath=str(Path(job['glb']).resolve(strict=True)))
        if 'disable_bone_shape' in bpy.ops.import_scene.gltf.get_rna_type().properties:
            import_options['disable_bone_shape']=True
        result=bpy.ops.import_scene.gltf(**import_options)
        if 'FINISHED' not in result: raise RuntimeError('Fresh import did not finish')
        names=sorted(o.name for o in bpy.context.scene.objects if o not in startup_objects)
        actions=sorted(a.name for a in bpy.data.actions)
        bpy.context.scene.frame_set(job.get('frame',1))
        data=snapshot('fresh-import',names,action_names=actions)
    output.mkdir(parents=True)
    (output/'snapshot.json').write_bytes(canonical_bytes(data))
    result=dict(mode=job['mode'],blender=bpy.app.version_string,objects=names,actions=actions,bounds=bounds(names),
                limits='Static declared snapshot and bounds; clip samples and visual review are separate')
    if job['mode']=='import':
        result['startup_objects_excluded']=sorted(o.name for o in startup_objects)
        result['import_options']=import_options
    (output/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('TOOLS_C_EXPORT_PROBE '+json.dumps(result))
    return result


if __name__=='__main__':
    run(json.loads(Path(sys.argv[sys.argv.index('--')+1]).read_text(encoding='utf-8-sig')))
