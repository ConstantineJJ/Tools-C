"""Offline Blender consumer exercise: actual PASS 0 -> named macro/clay assembly.

This is a disposable acceptance probe, not production mech reconstruction.
Run with Blender --background --factory-startup --python ... -- OUTPUT_DIRECTORY.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector, Matrix

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[sys.argv.index('--')+1]).resolve()
PACKET=OUT/'pass0.json'
spec=importlib.util.spec_from_file_location('pass0',ROOT/'skills/visual-reference-reconstruction/scripts/validate_pass0.py')
pass0=importlib.util.module_from_spec(spec);spec.loader.exec_module(pass0)
packet=pass0.load_packet(PACKET)
pass0.require_stage(packet,'MACRO_BLOCKOUT',OUT,verify_files=True)
if bpy.data.filepath:raise ValueError('Factory-only probe; never overwrite a production blend')
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
scene=bpy.context.scene
assembly=bpy.data.collections.new('PASS0 MACRO PROBE — uncertain interfaces, no materials or wear')
scene.collection.children.link(assembly)
registry=[];checks=[]

def check(condition,name,details):
    checks.append(dict(check=name,status='PASS' if condition else 'FAIL',details=details))
    if not condition:raise AssertionError(name+': '+details)

def dim(cid,axis,default=None):
    row=next((d for d in packet['relative_dimensions'] if d['component_id']==cid and d['axis']==axis),None)
    if row:return (row['min']+row['max'])/2
    if default is None:raise ValueError('Missing PASS 0 dimension '+cid+'.'+axis)
    return default

def register(o,pid,component,role,certainty='INFERRED',claim_ids=None):
    for coll in list(o.users_collection):coll.objects.unlink(o)
    assembly.objects.link(o)
    o['part_id']=pid;o['component_id']=component;o['certainty']=certainty
    o['editable_proxy']=True;o['pass0_packet_id']=packet['packet_id']
    linked=claim_ids or [component+'.presence']
    o['pass0_claim_ids']=json.dumps(linked)
    registry.append(dict(part_id=pid,role=role,module_id=component,parent_id=None,
                         shared_mesh_id=o.data.name if o.type=='MESH' else None,pivot=list(o.location),
                         attachment_frame='macro world frame',material_group='clay',
                         contact_expectations=[],protected=False,certainty=certainty,
                         editable_proxy=True,pass0_claim_ids=linked))
    return o

def cube(pid,component,loc,size,claim_ids=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object;o.name=pid
    o.scale=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    bevel=o.modifiers.new('macro edge break, no tertiary detail','BEVEL');bevel.width=min(size)*.055;bevel.segments=2
    return register(o,pid,component,'macro envelope',claim_ids=claim_ids)

def cylinder(pid,component,loc,radius,depth,axis=(0,1,0),prototype=None,claim_ids=None):
    if prototype:
        o=bpy.data.objects.new(pid,prototype.data);assembly.objects.link(o);o.location=loc
        o.rotation_euler=prototype.rotation_euler
    else:
        bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=radius,depth=depth,location=loc)
        o=bpy.context.object;o.name=pid;o.rotation_euler=Vector((0,0,1)).rotation_difference(Vector(axis)).to_euler()
    return register(o,pid,component,'visible face / joint proxy',claim_ids=claim_ids)

cube('torso.envelope','torso',(0,0,.62),(dim('torso','width'),dim('torso','depth'),dim('torso','height')))
cube('hatch.envelope','hatch',(0,-dim('torso','depth')/2-.012,.61),(dim('hatch','width'),.025,dim('hatch','height')))
cube('pelvis.envelope','pelvis',(0,0,.415),(.17,.16,dim('pelvis','height')))
cube('waist.proxy','pelvis',(0,0,.48),(.14,.12,.065))
face_prototype=None
for side in [-1,1]:
    tag='L' if side<0 else 'R'
    pod=cube(tag+'.pod','launcher',(side*.21,0,.87),(dim('launcher','width'),dim('launcher','depth'),dim('launcher','height')))
    for row in range(3):
        for col in range(4):
            loc=(side*.21+(col-1.5)*.043,-dim('launcher','depth')/2-.009,.87+(row-1)*.043)
            face=cylinder(f'{tag}.pod.face.{row}.{col}','launcher',loc,.016,.013,
                          prototype=face_prototype,claim_ids=['launcher.face_count','launcher.hidden_bore'])
            if face_prototype is None:face_prototype=face
    cube(tag+'.shoulder','shoulder_armor',(side*.245,-.005,.67),(.10,.16,.12))
    cube(tag+'.upper_arm','arm',(side*.27,0,.56),(.075,.11,.14))
    cube(tag+'.forearm','forearm_weapon',(side*.285,-.035,.455),(.11,.17,.13))
    cylinder(tag+'.barrel.envelope','forearm_weapon',(side*.285,-.15,.455),.030,.13)
    cube(tag+'.thigh','thigh',(side*.112,0,.335),(.13,.15,dim('thigh','link_length')))
    cylinder(tag+'.knee.proxy','knee',(side*.112,0,.237),.047,.13,axis=(1,0,0))
    cube(tag+'.shin','shin',(side*.116,0,.16),(.12,.15,.17))
    cube(tag+'.ankle.proxy','shin',(side*.116,0,.063),(.065,.085,.064))
    cube(tag+'.foot','foot',(side*.116,-.045,.031),(dim('foot','width'),dim('foot','depth'),.062))
scene.view_layers[0].update()
faces=[o for o in assembly.objects if '.pod.face.' in o.name]
check(len(faces)==24,'source exterior count retained','Two housings with 12 visible face proxies each; not through-bores.')
check(len({o.data.as_pointer() for o in faces})==1,'shared face prototype','All 24 proxy faces share data; no per-instance vertex edits.')
check(len(registry)==len(assembly.objects) and all(r['module_id'] in {c['id'] for c in packet['components']} for r in registry),
      'only declared macro components constructed','Every object has an explicit packet component record; visual review must confirm deferred regions remain undetailed.')
check(all(o['editable_proxy'] for o in assembly.objects),'uncertainty retained','All macro geometry is explicitly tagged editable and no confirmed hidden construction is claimed.')
for side in ['L','R']:
    foot=bpy.data.objects[side+'.foot']
    check(abs(min((foot.matrix_world@Vector(v)).z for v in foot.bound_box))<1e-6,
          side+' foot support plane','Macro stance contacts Z=0; no engineering stability claim.')

# Independent analytic mechanics safeguard: exercise failure semantics without
# pretending the packet supplies a solved mech mechanism or authorizing G2 detail.
def reachable(a,b,d):
    if not abs(a-b)<=d<=a+b:raise ValueError('Unreachable target; no silent clamp/stretch')
    return True
check(reachable(.19,.25,.40),'two-link valid sample','Illustrative fixed links, not calibrated source mechanism.')
rejected=False
try:reachable(.19,.25,.47)
except ValueError:rejected=True
check(rejected,'unreachable target rejected','Beyond sum of rigid lengths; no hidden clamp.')

triangles=0;zero=0
depsgraph=bpy.context.evaluated_depsgraph_get()
for o in assembly.objects:
    evaluated=o.evaluated_get(depsgraph);mesh=evaluated.to_mesh()
    triangles+=sum(len(p.vertices)-2 for p in mesh.polygons)
    zero+=sum(p.area<1e-12 for p in mesh.polygons)
    evaluated.to_mesh_clear()
check(zero==0,'evaluated macro geometry','Zero-area polygon count: '+str(zero))
mesh_state={o.name:dict(matrix=[list(r) for r in o.matrix_world],vertices=len(o.data.vertices),polygons=len(o.data.polygons),mesh=o.data.name) for o in assembly.objects}
(OUT/'consumer_registry.json').write_text(json.dumps(registry,indent=2)+'\n',encoding='utf-8')
(OUT/'consumer_state.json').write_text(json.dumps(mesh_state,indent=2)+'\n',encoding='utf-8')
blend=OUT/'PASS0_Macro_Consumer_Probe.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend))

sys.path.insert(0,str(ROOT/'tools'))
from blender_capture import capture_viewport
captures=[]
for view in ['front','side','back','three_quarter']:
    metadata=capture_viewport(output=str(OUT/('clay_'+view)),view=view,target='character',
                              mode='solid',frame=1,resolution=768,object_names=[o.name for o in assembly.objects])
    if not metadata.get('ok'):raise ValueError(metadata)
    captures.append(metadata)
result=dict(status='PASS',blender_version=bpy.app.version_string,packet_id=packet['packet_id'],
            packet_sha256=hashlib.sha256(PACKET.read_bytes()).hexdigest(),gate=packet['gate'],
            checks=checks,objects=len(assembly.objects),evaluated_triangles=triangles,captures=captures,
            scope='Real packet consumed in separate factory Blender; macro handoff only. Not likeness, full robot mechanics or material/wear acceptance.')
(OUT/'consumer_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS0_CONSUMER '+json.dumps({k:result[k] for k in ['status','blender_version','objects','evaluated_triangles','scope']}))
