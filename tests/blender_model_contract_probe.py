"""Disposable Blender factory scene probe; run manually with --background.

No production modeling, materials, rig or animation acceptance. This verifies real
object bindings/envelopes, negative drift and persistence of the same contract.
"""
from pathlib import Path
import copy
import importlib.util
import json
import math
import sys
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import model_contract as m
spec=importlib.util.spec_from_file_location('probe_pass0',ROOT/'skills/visual-reference-reconstruction/scripts/validate_pass0.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
OUT=Path(args[0]).resolve()
p=v.load_packet(OUT/'pass0.json')
v.require_stage(p,'MACRO_BLOCKOUT',OUT)
H=10.0
parts=[]

def bind(obj,cid,instance,parent=None):
    obj['component_id']=cid;obj['instance_id']=instance
    if parent:
        matrix=obj.matrix_world.copy();obj.parent=parent;obj.matrix_world=matrix
    parts.append(dict(part_id=obj.name,object_name=obj.name,component_id=cid,instance_id=instance,
                      parent_id=parent.name if parent else None,role='macro proxy',pass0_claim_ids=[]))
    return obj

def sphere(name,location,radius,cid,instance,parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=radius,location=location)
    obj=bpy.context.object;obj.name=name
    return bind(obj,cid,instance,parent)

def box(name,location,size,cid,instance,parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=location)
    obj=bpy.context.object;obj.name=name;obj.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return bind(obj,cid,instance,parent)

def rod(name,a,b,radius,cid,instance,parent=None):
    a,b=Vector(a),Vector(b)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=radius,depth=(b-a).length,location=(a+b)/2)
    obj=bpy.context.object;obj.name=name;obj.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
    return bind(obj,cid,instance,parent)

def bounds(objects):
    dg=bpy.context.evaluated_depsgraph_get()
    coords=[obj.evaluated_get(dg).matrix_world@Vector(corner) for obj in objects for corner in obj.evaluated_get(dg).bound_box if obj.type=='MESH']
    return [min(c[i] for c in coords) for i in range(3)],[max(c[i] for c in coords) for i in range(3)]

def extent(cid,axis):
    instances={o['instance_id'] for o in bpy.data.objects if o.get('component_id')==cid}
    values=[]
    for instance in instances:
        lo,hi=bounds([o for o in bpy.data.objects if o.get('component_id')==cid and o.get('instance_id')==instance])
        values.append((instance,(hi[axis]-lo[axis])/H))
    # Check the smallest and largest item separately rather than average away drift.
    return dict(values)

def checkpoint():
    bpy.context.view_layer.update()
    dimensions={d['id']:extent(d['component_id'],{'width':0,'depth':1,'height':2,'length':1}[d['axis']]) for d in p['relative_dimensions']}
    observations=[]
    for r in p['model_contract']['rules']:
        if 'MACRO' not in r['checkpoints'] or r['kind']=='count':continue
        want=m.expected(p,r)
        evidence='macro-probe.blend / evaluated scene objects; explicit fixture construction'
        obs=dict(rule_id=r['id'],state='MEASURED',method='Macro fixture geometry/design review; no engineering or polished likeness claim',evidence=evidence,value=want,unit=r.get('unit'))
        if r['kind']=='dimension':
            values=list(dimensions[r['target_id']].values());lo,hi=want
            obs['value']=next((a for a in values if not lo<=a<=hi),values[0]);obs['method']='Evaluated world bounds of each physical instance / H=10'
            obs['instance_values']=dimensions[r['target_id']]
        elif r['kind']=='ratio':
            num,den=dimensions[r['numerator_id']],dimensions[r['denominator_id']]
            assert len(den)==1,'Fixture ratios use one torso as denominator'
            ratio_values={instance:value/next(iter(den.values())) for instance,value in num.items()}
            ratios=list(ratio_values.values());lo,hi=want
            obs['value']=next((a for a in ratios if not lo<=a<=hi),ratios[0]);obs['method']='Measured instance extent ratio in canonical world axes'
            obs['instance_values']=ratio_values
        elif r['kind']=='anchor':
            name='Hip.L' if r['target_id']=='anchor.hip_z' else 'Gun.L'
            obs['value']=[bpy.data.objects[name].matrix_world.translation.z/H];obs['method']='Named hip/gun center world Z / H=10'
        elif r['level']=='SOFT CANONICAL':
            obs['value']='primitive macro envelope; detail intentionally deferred'
        elif r['kind']=='symmetry':
            cid=r['target_id'];centers=[]
            for suffix in ['L','R']:
                obj=bpy.data.objects['Gun.'+suffix if cid=='guns' else 'Hip.'+suffix]
                centers.append(obj.matrix_world.translation)
            if abs(centers[0].x+centers[1].x)>1e-6 or (Vector((0,centers[0].y,centers[0].z))-Vector((0,centers[1].y,centers[1].z))).length>1e-6:
                obs['value']={'type':'NONE'}
            obs['method']='Measured bilateral root centers, X=0 symmetry plane; internal topology not certified'
        observations.append(obs)
    actual_parts=[]
    for obj in bpy.data.objects:
        if obj.get('component_id'):
            actual_parts.append(dict(part_id=obj.name,object_name=obj.name,component_id=obj['component_id'],instance_id=obj['instance_id'],parent_id=obj.parent.name if obj.parent else None,role='macro proxy'))
    assembly=dict(contract_ref=json.loads(bpy.context.scene['model_contract_ref']),parts=actual_parts,observations=observations)
    result=m.verify_assembly(p,assembly,'MACRO');assembly['verification']=result
    return assembly,result

def save_json(name,value):
    (OUT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

if '--reopen' in args:
    bpy.ops.wm.open_mainfile(filepath=str(OUT/'macro-probe.blend'))
    assembly,result=checkpoint()
    assert result['status']=='PASS',result
    assert assembly['contract_ref']==m.reference(p)
    save_json('saved-reopen.json',result)
    print('MODEL_CONTRACT_REOPEN_PASS')
    raise SystemExit(0)

# Factory-only scene, never invoked against the user's live Blender scene.
assert bpy.data.filepath=='', 'Requires disposable factory-startup scene'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
torso=sphere('Torso',(0,0,7.8),1.575,'torso','torso.0')
for suffix,x in [('L',-1.85),('R',1.85)]:
    box('Gun.'+suffix,(x,-1.15,7.8),(.5,2.2,.45),'guns','guns.'+suffix,torso)
for suffix,x in [('L',-1.1),('R',1.1)]:
    hip=sphere('Hip.'+suffix,(x,0,6.2),.16,'legs','legs.'+suffix,torso)
    knee=(x,.30,3.35);ankle=(x,-.12,.55)
    rod('Upper.'+suffix,(x,0,6.2),knee,.12,'legs','legs.'+suffix,hip)
    sphere('Knee.'+suffix,knee,.20,'legs','legs.'+suffix,hip)
    rod('Lower.'+suffix,knee,ankle,.10,'legs','legs.'+suffix,hip)
    sphere('Ankle.'+suffix,ankle,.16,'legs','legs.'+suffix,hip)
    box('Foot.'+suffix,(x,-.6,.225),(.6,2,.45),'feet','feet.'+suffix,hip)
sphere('Optic.Front',(0,-1.5,7.8),.32,'optics','optics.front',torso)
sphere('Optic.Top',(0,-.25,9.58),.25,'optics','optics.top',torso)
rod('Antenna',(.5,.4,9.28),(.5,.4,10),.025,'antenna','antenna.0',torso)
bpy.context.scene['model_contract_ref']=json.dumps(m.reference(p))
bpy.context.scene['pass0_packet']='pass0.json'
assembly,result=checkpoint();assert result['status']=='PASS',result
save_json('assembly_graph.json',assembly)
# A real geometry change must fail without changing the Contract or receipt.
gun=bpy.data.objects['Gun.L'];original=gun.scale.copy();gun.scale.y*=.4
_,shortened=checkpoint();assert shortened['status']=='FAIL',shortened
save_json('shortened-gun-negative.json',shortened);gun.scale=original
extra=box('Gun.EXTRA',(2.5,-1.15,7.8),(.5,2.2,.45),'guns','guns.EXTRA',torso)
_,count=checkpoint();assert count['status']=='FAIL',count
save_json('extra-gun-negative.json',count);bpy.data.objects.remove(extra,do_unlink=True)
assembly,result=checkpoint();assert result['status']=='PASS',result
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=12
scene.render.resolution_x=640;scene.render.resolution_y=800;scene.render.resolution_percentage=100
scene.world.color=(.18,.18,.18)
mat=bpy.data.materials.new('Plain clay');mat.diffuse_color=(.55,.55,.55,1)
for obj in bpy.data.objects:
    if obj.type=='MESH':obj.data.materials.append(mat)
bpy.ops.object.light_add(type='AREA',location=(5,-8,13));light=bpy.context.object;light.data.energy=1800;light.data.shape='DISK';light.data.size=8
bpy.ops.object.camera_add(location=(13,-22,12));camera=bpy.context.object
camera.rotation_euler=(Vector((0,0,5))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=12
scene.camera=camera;scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUT/'macro-clay.png')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'macro-probe.blend'))
bpy.ops.render.render(write_still=True)
save_json('assembly_graph.json',assembly)
print('MODEL_CONTRACT_MACRO_PASS_WITH_REAL_NEGATIVE_DRIFT')
