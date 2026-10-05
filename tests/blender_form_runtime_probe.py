"""Disposable Blender probe: --background --factory-startup --python this_file -- OUTPUT [reopen]."""
import json
import math
from pathlib import Path
import runpy
import sys

import bpy
from mathutils import Matrix

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import blender_contacts
import blender_forms
import handoff_snapshot

capture=runpy.run_path(str(ROOT/'tools/blender_snapshot.py'))['snapshot']
output=Path(sys.argv[sys.argv.index('--')+1]).resolve()
output.mkdir(parents=True,exist_ok=True)
categories=['uvs','normals','shape_keys','weights','modifiers','curves','material_graphs']
checks=[]

def require(condition,label):
    if not condition: raise AssertionError(label)
    checks.append(dict(check=label,status='PASS'))

def cube(name,center,size):
    bpy.ops.mesh.primitive_cube_add(size=size,location=center)
    obj=bpy.context.object; obj.name=name
    return obj

if 'reopen' in sys.argv:
    bpy.ops.wm.open_mainfile(filepath=str(output/'probe.blend'),load_ui=False,use_scripts=False)
    before=json.loads((output/'saved-snapshot.json').read_text())
    after=capture('FORM_PROBE', [o['name'] for o in before['objects']],protected=before['protected_objects'],data_categories=categories)
    diff=handoff_snapshot.compare(before,after)
    require(not diff['protected_regressions'] and not diff['changed_objects'],'saved-file declared categories and fresh world transforms preserved')
    (output/'reopen-result.json').write_text(json.dumps(dict(checks=checks,diff=diff),indent=2))
    print(json.dumps(checks)); raise SystemExit(0)

collection=bpy.data.collections.new('Runtime_Form_Probe'); bpy.context.scene.collection.children.link(collection)
sweep=blender_forms.create_sweep('ProbeSweep',collection,[(0,0,0),(0.2,0,1),(0.4,0.1,2)],
                                [0.5,0.7,0.1],[0.2,0.3,0.05],sides=16)
require(len(sweep.data.uv_layers)==1 and len(sweep.data.polygons)==34,'editable sweep mesh and UVs created')
counts=(len(bpy.data.objects),len(bpy.data.meshes),len(bpy.data.curves))
try: blender_forms.create_curve_batch('BadBatch',collection,[[(0,0,0),(0,0,0)]])
except ValueError: pass
else: raise AssertionError('invalid curve accepted')
require(counts==(len(bpy.data.objects),len(bpy.data.meshes),len(bpy.data.curves)),'invalid paths rejected before datablock mutation')
paths=[[(i*0.001,0,0),(i*0.001,0.1,1)] for i in range(1300)]
fibres=blender_forms.create_curve_batch('ProbeFibres',collection,paths,radius=0.002)
require(len(fibres.data.splines)==1300 and fibres.type=='CURVE','1300 fibres remain one editable curve object')
parent=bpy.data.objects.new('ProbeParent',None); collection.objects.link(parent)
parent.location=(3,-2,0.5); parent.rotation_euler=(0.1,0.3,0.4); parent.scale=(1.2,0.8,1.4)
bpy.context.view_layer.update(); world=sweep.matrix_world.copy()
blender_forms.parent_keep_world(sweep,parent); bpy.context.view_layer.update()
require(max(abs(a-b) for row1,row2 in zip(world,sweep.matrix_world) for a,b in zip(row1,row2))<1e-6,'parent assignment preserves world placement')
try: blender_forms.parent_keep_world(parent,sweep)
except ValueError: pass
else: raise AssertionError('parent cycle accepted')
require(parent.parent is None,'parent cycle rejected without mutation')

import blender_jobs
job_counts=(len(bpy.data.objects),len(bpy.data.curves),len(bpy.data.collections))
try:
    blender_jobs.start_curve_batch('invalid-form-probe','InvalidFormCollection',
        [dict(name='InvalidCurve',paths=[[[0,0,i*0.001] for i in range(10001)]])])
except ValueError: pass
else: raise AssertionError('oversized timer batch accepted')
require(job_counts==(len(bpy.data.objects),len(bpy.data.curves),len(bpy.data.collections)),'oversized timer batch rejected before scene mutation')
try: blender_jobs.operation_status('../private')
except ValueError: pass
else: raise AssertionError('unsafe operation ID accepted')
require(True,'operation IDs cannot escape receipt directory')
receipt_id='runtime-form-interrupted-probe'
receipt=blender_jobs._receipt(receipt_id)
assert not receipt.exists(), 'probe receipt ID already used'
receipt.parent.mkdir(parents=True,exist_ok=True)
receipt.write_text(json.dumps(dict(operation_id=receipt_id,status='running',request_sha256='0'*64)))
try:
    state=blender_jobs.operation_status(receipt_id)
    require(state['status']=='interrupted' and state['process_state']=='receipt_only','unfinished historical receipt reports interruption without replay')
finally: receipt.unlink()

outer=cube('ContactOuter',(10,0,0),4)
inner=cube('ContactInner',(10,0,0),1)
intersect=cube('ContactIntersection',(11.9,0.3,0.2),1)
far=cube('ContactFar',(20,0,0),1)
near=cube('ContactNear',(12.52,0,0),1)
bpy.ops.mesh.primitive_plane_add(size=1,location=(30,0,0)); plane=bpy.context.object; plane.name='ContactOpen'
pairs=[dict(a=outer.name,b=b.name,expected=[expected]) for b,expected in
       [(inner,'containment'),(intersect,'surface_intersection'),(far,'separated'),(near,'proximity'),(plane,'inconclusive')]]
contacts=blender_contacts.diagnose_pairs(pairs,tolerance=0.025)
require([p['relationship'] for p in contacts['pairs']]==[p['expected'][0] for p in pairs],'contact diagnostics distinguish containment, crossing, distance, near and open surface')
require(contacts['pairs'][-1]['status']=='REVIEW REQUIRED','open surface cannot get volume acceptance')
limited=blender_contacts.diagnose_pairs([pairs[0]],0.01,max_vertices=1)
require(limited['pairs'][0]['relationship']=='inconclusive','limited volume sampling stays inconclusive')

sweep.shape_key_add(name='Basis'); key=sweep.shape_key_add(name='Shape')
group=sweep.vertex_groups.new(name='Bone'); group.add([0],0.5,'REPLACE')
modifier=sweep.modifiers.new('Surface','SUBSURF'); modifier.levels=1
material=bpy.data.materials.new('ProbeMaterial'); material.use_nodes=True
sweep.data.materials.append(material)
node=material.node_tree.nodes.get('Principled BSDF')
names=[sweep.name,fibres.name,parent.name]

def fingerprints():
    return capture('FORM_PROBE',names,protected=names,data_categories=categories)

mutations=[('uvs',lambda: setattr(sweep.data.uv_layers[0].data[0],'uv',(0.17,0.29))),
           ('normals',lambda: setattr(sweep.data.polygons[0],'use_smooth',False)),
           ('shape_keys',lambda: setattr(key.data[0],'co',(key.data[0].co.x+0.03,key.data[0].co.y,key.data[0].co.z))),
           ('weights',lambda: group.add([0],0.7,'REPLACE')),
           ('modifiers',lambda: setattr(modifier,'levels',2)),
           ('curves',lambda: setattr(fibres.data.splines[0].points[0],'radius',0.8)),
           ('material_graphs',lambda: setattr(node.inputs['Roughness'],'default_value',0.63))]
for category,mutation in mutations:
    before=fingerprints(); mutation(); after=fingerprints()
    changed=[o['name'] for o in after['objects'] if o['data_fingerprints'][category]!=next(b for b in before['objects'] if b['name']==o['name'])['data_fingerprints'][category]]
    require(bool(changed) and bool(handoff_snapshot.compare(before,after)['protected_regressions']),category+' mutation detected on protected data')

inactive=bpy.data.scenes.new('ProbeInactiveScene'); camera=bpy.data.objects.new('InactiveCamera',bpy.data.cameras.new('InactiveCameraData'))
inactive.collection.objects.link(camera); camera.location=(7,8,9)
names.append(camera.name)
saved=fingerprints()
row=next(o for o in saved['objects'] if o['name']==camera.name)
require([row['matrix_world'][i] for i in (3,7,11)]==[7,8,9],'snapshot evaluates inactive scene transforms before capture')
(output/'saved-snapshot.json').write_text(json.dumps(saved,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(output/'probe.blend'))
(output/'runtime-result.json').write_text(json.dumps(dict(blender=bpy.app.version_string,checks=checks,contacts=contacts),indent=2))
print(json.dumps(checks))
