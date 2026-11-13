"""Disposable native Blender acceptance for the existing evidence helpers."""
import hashlib
import json
import math
from pathlib import Path
import runpy
import sys

import bpy

root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tools'))
import vision_compare as vision


def probe(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    capture=runpy.run_path(str(root/'tools/blender_capture.py'))['capture_viewport']
    measure=runpy.run_path(str(root/'tools/blender_snapshot.py'))['measure_objects']
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    bpy.ops.mesh.primitive_cube_add();obj=bpy.context.object;obj.name='VehicleEnvelope'
    obj.scale=(2,3,1);bpy.context.view_layer.update()
    stats=measure([obj.name]);assert stats['objects'][0]['world_dimensions']==[4,6,2]
    bpy.ops.object.camera_add(location=(0,-12,0));camera=bpy.context.object
    camera.rotation_euler=(math.pi/2,0,0);camera.data.type='ORTHO';camera.data.ortho_scale=10
    camera.data.shift_x=.07;camera.data.shift_y=-.04
    before=(len(bpy.data.objects),len(bpy.data.scenes),bpy.context.scene.frame_current,bpy.context.scene.camera)
    def take(name,view='camera',**kw):
        args=dict(output=str(output/name),view=view,target='character',object_names=[obj.name],frame=1,
                  resolution=[128,96],channel='silhouette')
        if view=='camera':args['camera_name']=camera.name
        args.update(kw);return capture(**args)
    ref=take('reference');same=take('same')
    assert ref['sha256']==same['sha256']
    assert ref['shift']==[camera.data.shift_x,camera.data.shift_y]
    mask=vision.read_mask(Path(ref['path']),'alpha')
    assert 0<sum(map(sum,mask))<128*96
    # A depth change has the same front contour but a different side contour.
    side_before=take('side_before','side')
    obj.scale.y*=1.4;bpy.context.view_layer.update()
    front_depth=take('front_depth')
    assert front_depth['sha256']==ref['sha256']
    side_after=take('side_after','side',framing=side_before['framing'])
    assert side_after['sha256']!=side_before['sha256']
    obj.scale.x*=1.3;bpy.context.view_layer.update()
    candidate=take('candidate')
    metrics=vision.compare_masks(mask,vision.read_mask(Path(candidate['path']),'alpha'))
    assert metrics['iou']<.9 and metrics['contour_distance_px']['p95']>0
    def artifact(path):
        path=Path(path);return dict(path=path.relative_to(output).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    job=dict(schema_version=1,reference=dict(mask=artifact(ref['path']),source=artifact(ref['path']),mode='alpha',authority='ORIGINAL'),
        candidate=dict(mask=artifact(candidate['path']),capture=artifact(Path(candidate['path']).parent/'capture.json')),
        alignment=dict(mode='CALIBRATED',reviewed=True,pose_confirmed=True,reference_setup=vision.camera_setup(ref)),
        thresholds=dict(iou_min=.98,contour_p95_max_px=1))
    (output/'comparison-job.json').write_text(json.dumps(job),encoding='utf-8')
    result=vision.compare_job(output/'comparison-job.json',output/'comparison')
    assert result['status']=='FAIL'
    assert vision.verify_comparison(output/'comparison/comparison.json',output)==result
    camera.data.shift_x+=.1
    mismatch=take('wrong_camera')
    assert vision.assess(metrics,job['alignment'],vision.camera_setup(mismatch),'ORIGINAL',job['thresholds'])['status']=='NOT_COMPARABLE'
    camera.data.shift_x-=.1
    # A second asset family includes a hole: its interior contour must survive.
    bpy.ops.mesh.primitive_torus_add(major_radius=2,minor_radius=.5)
    obj=bpy.context.object;obj.name='MechanicalRing'
    ring=take('ring','top',resolution=128)
    ring_mask=vision.read_mask(Path(ring['path']),'alpha')
    assert not ring_mask[64][64] and any(map(any,ring_mask))
    assert len(bpy.data.scenes)==before[1]
    assert bpy.context.scene.frame_current==before[2] and bpy.context.scene.camera==before[3]
    summary=dict(status='PASS',blender=bpy.app.version_string,measurements=stats,comparison=result['metrics'],
        checks=['world dimensions','camera shift and rectangular aspect','repeatable PNG bytes','binary alpha coverage',
                'same front / different depth','silhouette drift','camera mismatch rejection','ring inner contour','source frame/camera restored'])
    (output/'probe.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    return summary


if __name__=='__main__':print(json.dumps(probe(sys.argv[sys.argv.index('--')+1]),indent=2))
