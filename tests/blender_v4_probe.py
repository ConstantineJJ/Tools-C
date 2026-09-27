"""Opt-in real Blender fixture. Never run in an interactive/production scene."""
import json
from pathlib import Path
import sys

import bpy

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from blender_capture import capture_viewport
from blender_snapshot import snapshot
from handoff_snapshot import canonical_bytes, compare


def main(output, fps_base=1.0):
    if not bpy.app.background: raise RuntimeError('Factory background process required')
    if output.exists(): raise ValueError('New output directory required')
    output.mkdir(parents=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene; scene.render.fps=30; scene.render.fps_base=fps_base
    blue=bpy.data.materials.new('FixtureBlue'); blue.diffuse_color=(.08,.28,.7,1)
    yellow=bpy.data.materials.new('FixtureMarker'); yellow.diffuse_color=(1,.55,.03,1)
    for mat in (blue,yellow):
        mat.use_nodes=True
        mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=mat.diffuse_color
    specs=[('Body',(0,0,1.5),(.5,.3,.65)),('Head',(0,0,2.5),(.38,.32,.35)),
           ('LeftLeg',(-.3,0,.45),(.18,.2,.45)),('RightLeg',(.3,0,.45),(.18,.2,.45)),
           ('LeftArm',(-.8,0,1.5),(.16,.2,.55)),('RightArm',(.8,0,1.7),(.16,.2,.55)),
           ('FrontMarker',(.18,-.33,1.7),(.15,.04,.18)),('BackMarker',(-.2,.34,1.4),(.08,.05,.3))]
    names=[]
    for name,location,scale in specs:
        bpy.ops.mesh.primitive_cube_add(size=2,location=location)
        obj=bpy.context.object; obj.name=name; obj.scale=scale
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        obj.data.materials.append(yellow if 'Marker' in name else blue); names.append(name)
    bpy.ops.object.armature_add()
    rig=bpy.context.object; rig.name='FixtureRig'
    bpy.ops.object.mode_set(mode='EDIT')
    root=rig.data.edit_bones[0]; root.name='Root'; root.head=(0,0,0); root.tail=(0,0,1)
    tip=rig.data.edit_bones.new('Tip'); tip.head=(0,0,1); tip.tail=(0,0,2); tip.parent=root
    bpy.ops.object.mode_set(mode='OBJECT')
    for name in names:
        obj=bpy.data.objects[name]
        group=obj.vertex_groups.new(name='Root'); group.add(list(range(len(obj.data.vertices))),1,'REPLACE')
        mod=obj.modifiers.new('Skin','ARMATURE'); mod.object=rig
        obj.parent=rig
    bone=rig.pose.bones['Tip']; bone.rotation_mode='XYZ'
    for frame,angle in ((1,0),(13,.5),(25,0)):
        bone.rotation_euler.z=angle; bone.keyframe_insert(data_path='rotation_euler',frame=frame,group='Tip')
    rig.animation_data.action.name='FixtureWave'; actions=['FixtureWave']; names.append(rig.name)
    scene.frame_set(1)
    bpy.ops.object.light_add(type='AREA',location=(2,-3,5)); light=bpy.context.object
    light.data.energy=800
    from mathutils import Vector
    light.rotation_euler=(Vector((0,0,1.5))-light.location).to_track_quat('-Z','Y').to_euler()
    before=snapshot('baseline',names,protected=names,action_names=actions)
    counts={key:len(getattr(bpy.data,key)) for key in ('objects','scenes','cameras','lights','worlds')}
    results={}; framing=None
    for view in ('front','side','back','three_quarter','top','bottom'):
        result=capture_viewport(output/view,view=view,target='character',object_names=names,frame=1,resolution=256,framing=framing)
        results[view]=result; framing=result['framing']
    results['repeat']=capture_viewport(output/'repeat',view='front',target='character',object_names=names,frame=1,resolution=256,framing=framing)
    if results['front']['sha256'] != results['repeat']['sha256']: raise AssertionError('Fixed capture is not deterministic')
    # Exercise BEFORE -> bounded edit -> AFTER with the original camera fit.
    head=bpy.data.objects['Head']; previous=head.location.copy()
    head.location.x+=.2; bpy.context.view_layer.update()
    changed=snapshot('baseline',names,protected=names,action_names=actions)
    if compare(before,changed)['protected_regressions']!=['Head']: raise AssertionError('Snapshot missed protected object change')
    results['after_edit']=capture_viewport(output/'after_edit',view='front',target='character',object_names=names,frame=1,resolution=256,framing=framing)
    if results['after_edit']['framing']!=framing or results['after_edit']['sha256']==results['front']['sha256']:
        raise AssertionError('Regression capture changed framing or missed visible edit')
    head.location=previous; bpy.context.view_layer.update()
    for mode in ('material_preview','rendered'):
        results[mode]=capture_viewport(output/mode,view='three_quarter',target='character',mode=mode,object_names=names,frame=13,resolution=128,framing=framing)
    scene.frame_set(1,subframe=.25)
    fractional=capture_viewport(output/'subframe',view='front',target='character',object_names=names,resolution=128,framing=framing)
    if fractional['frame']!=1.25 or scene.frame_subframe!=.25:
        raise AssertionError('Optional frame did not preserve current subframe')
    scene.frame_set(1)
    saved_selection=list(bpy.context.selected_objects)
    saved_active=bpy.context.view_layer.objects.active
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Head'].select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects['Head']
    # Include renderable parents explicitly only if required; this head's parent is an armature.
    for target in ('active','selected'):
        selected=capture_viewport(output/target,view='front',target=target,frame=1,resolution=128)
        if selected['objects']!=['Head']: raise AssertionError('Active/selected scope expanded unexpectedly')
    bpy.ops.object.select_all(action='DESELECT')
    for obj in saved_selection: obj.select_set(True)
    bpy.context.view_layer.objects.active=saved_active
    results['current']=capture_viewport(output/'current',view='current',target='character',object_names=names,frame=1,resolution=128)
    if results['current'].get('status') != 'SKIP': raise AssertionError('Background current must explicitly skip')
    after=snapshot('baseline',names,protected=names,action_names=actions)
    if canonical_bytes(before)!=canonical_bytes(after): raise AssertionError('Capture mutated source snapshot')
    if counts!={key:len(getattr(bpy.data,key)) for key in counts}: raise AssertionError('Temporary render data leaked')
    for invalid in (dict(view='invalid'),dict(resolution=0),dict(target='character',object_names=['Missing']),dict(framing={'center':[0,0,0],'span':0})):
        try:
            args=dict(output=output/'invalid',target='character',object_names=names); args.update(invalid)
            capture_viewport(**args)
        except (ValueError,KeyError): pass
        else: raise AssertionError('Invalid capture accepted')
    # Save only this disposable fixture, with the rig active so Action inclusion is explicit.
    bpy.context.view_layer.objects.active=rig
    source=output/'fixture.blend'; bpy.ops.wm.save_as_mainfile(filepath=str(source))
    (output/'snapshot.json').write_bytes(canonical_bytes(before))
    (output/'capture-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    export=dict(mode='export',source=str(source),glb=str(output/'fixture.glb'),output=str(output/'export'),
                objects=names,actions=actions,frame=1,export_options=dict(export_animation_mode='ACTIONS'))
    (output/'export-job.json').write_text(json.dumps(export,indent=2),encoding='utf-8')
    imported=dict(mode='import',glb=str(output/'fixture.glb'),output=str(output/'import'),frame=1,fps=scene.render.fps/scene.render.fps_base)
    (output/'import-job.json').write_text(json.dumps(imported,indent=2),encoding='utf-8')
    print('TOOLS_C_V4_CAPTURE '+json.dumps(dict(status='PASS',source_preserved=True,deterministic=True,views=list(results))))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    parser.add_argument('--fps-base',type=float,default=1.0)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    main(args.output.resolve(),args.fps_base)
