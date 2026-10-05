"""Typed timer-chunked curve operations inside Blender; no arbitrary executable jobs.

State lives in this Blender process and a bounded Tools_C receipt directory.
Reusing an ID with identical inputs reads its status; changed inputs are rejected.
After process loss, receipts expose interruption; never replay partial mutations.
"""
import hashlib
import json
import math
from pathlib import Path
import re
import time

ROOT = Path(__file__).resolve().parents[1]
STATES_KEY = '_TOOLS_C_CURVE_OPERATIONS_V1'


def _id(value):
    if not isinstance(value,str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}',value):
        raise ValueError('Operation ID must be 1..64 ASCII letters, digits, dash or underscore')
    return value


def _states():
    import bpy
    return bpy.app.driver_namespace.setdefault(STATES_KEY,{})


def _receipt(operation):
    return ROOT/'.local'/'operations'/(_id(operation)+'.json')


def _public(state):
    return {k:v for k,v in state.items() if not k.startswith('_')}


def _save(state):
    path=_receipt(state['operation_id'])
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(_public(state),sort_keys=True,allow_nan=False),encoding='utf-8')
    temporary.replace(path)


def operation_status(operation_id, cancel=False):
    states=_states(); operation_id=_id(operation_id)
    if operation_id not in states:
        path=_receipt(operation_id)
        if not path.is_file():
            return dict(ok=False,operation_id=operation_id,status='unknown',error='No receipt; inspect scene before replaying any mutation')
        state=json.loads(path.read_text(encoding='utf-8'))
        if state['status'] in ('queued','running'):
            state['status']='interrupted'
        return dict(ok=True,process_state='receipt_only',**state)
    state=states[operation_id]
    if cancel and state['status'] in ('queued','running'):
        state['cancel_requested']=True
        _save(state)
    return dict(ok=True,process_state='live',**_public(state))


def start_curve_batch(operation_id, collection_name, batches, batches_per_tick=1, radius=0.01, material_name=None):
    import bpy
    import sys
    sys.path.insert(0,str(ROOT/'tools'))
    from blender_forms import points3,create_curve_batch
    operation_id=_id(operation_id)
    if not isinstance(collection_name,str) or not collection_name.strip() or len(collection_name)>128:
        raise ValueError('Explicit new collection name required')
    if type(batches_per_tick) is not int or not 1 <= batches_per_tick <= 16 or not math.isfinite(radius) or radius <= 0:
        raise ValueError('1..16 batches per tick and positive finite radius required')
    if not isinstance(batches,list) or not 1 <= len(batches) <= 256:
        raise ValueError('1..256 named editable batches required')
    count=0
    for batch in batches:
        if not isinstance(batch,dict) or set(batch)!={'name','paths'} or not isinstance(batch['name'],str) or not batch['name'] or not isinstance(batch['paths'],list) or not batch['paths']:
            raise ValueError('Each batch has only name and nonempty paths')
        batch_count=0
        for path in batch['paths']:
            if not isinstance(path,list) or any(not isinstance(p,(list,tuple)) or len(p) not in (3,4)
                    or not all(isinstance(v,(int,float)) and math.isfinite(v) for v in p)
                    or (len(p)==4 and p[3]<=0) for p in path):
                raise ValueError('Each path has finite XYZ and optional positive radius')
            points3([p[:3] for p in path]); count+=len(path); batch_count+=len(path)
        if batch_count>10000:
            raise ValueError('Bounded tick limit: 10000 control points per batch')
    if count>200000:
        raise ValueError('Bounded operation limit: 200000 control points; split the authorized work')
    names=[batch['name'] for batch in batches]
    if len(set(names))!=len(names):
        raise ValueError('Unique batch names required')
    if material_name is not None and material_name not in bpy.data.materials:
        raise ValueError('Named material missing')
    request=dict(collection=collection_name,batches=batches,batches_per_tick=batches_per_tick,radius=radius,material=material_name)
    digest=hashlib.sha256(json.dumps(request,sort_keys=True,allow_nan=False).encode()).hexdigest()
    prior=operation_status(operation_id)
    if prior.get('ok'):
        if prior['request_sha256']!=digest:
            raise ValueError('Operation ID reused with changed inputs; inspect original status')
        return prior
    if collection_name in bpy.data.collections or any(name in bpy.data.objects for name in names):
        raise ValueError('Collection/object already exists; no mutation or implicit replacement')
    collection=bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)
    state=dict(operation_id=operation_id,kind='curve_batch',status='queued',request_sha256=digest,
               collection=collection_name,total_batches=len(batches),completed_batches=0,created_objects=[],
               started_at=time.time(),cancel_requested=False,error=None)
    _states()[operation_id]=state
    _save(state)
    def tick():
        if state['cancel_requested']:
            state['status']='cancelled'; state['finished_at']=time.time(); _save(state); return None
        state['status']='running'
        try:
            for _ in range(batches_per_tick):
                index=state['completed_batches']
                if index>=len(batches):
                    break
                batch=batches[index]
                obj=create_curve_batch(batch['name'],collection,batch['paths'],radius,
                                       bpy.data.materials.get(material_name) if material_name else None)
                state['created_objects'].append(obj.name)
                state['completed_batches']+=1
            bpy.context.view_layer.update()
            if state['completed_batches']==len(batches):
                state['status']='completed'; state['finished_at']=time.time(); _save(state); return None
            _save(state)
            return 0.02
        except Exception as exc:
            state['status']='failed'; state['error']=str(exc); state['finished_at']=time.time(); _save(state); return None
    bpy.app.timers.register(tick,first_interval=0.02)
    return operation_status(operation_id)
