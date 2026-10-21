"""Disposable real-Blender reference setup/save/reopen probe; never use on a user scene."""
import argparse
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import blender_reference as refs

args = argparse.ArgumentParser()
args.add_argument('--work', type=Path, required=True)
args.add_argument('--phase', choices=['create', 'reopen'], required=True)
opts = args.parse_args(sys.argv[sys.argv.index('--')+1:])
opts.work.mkdir(parents=True, exist_ok=True)


def inventory():
    return tuple(tuple(sorted(item.name for item in group)) for group in
                 (bpy.data.objects, bpy.data.collections, bpy.data.images, bpy.data.cameras))


def check_set():
    coll = bpy.data.collections['REFERENCE']
    assert coll.hide_render and coll['tools_c_reference']
    images = [o for o in coll.objects if o.type == 'EMPTY']
    cameras = [o for o in coll.objects if o.type == 'CAMERA']
    assert len(images) == len(cameras) == 5
    for image in images:
        assert image.data.packed_file and image.hide_select and image.hide_render
        assert all(image.lock_location) and all(image.lock_rotation) and all(image.lock_scale)
        meta = json.loads(image['registration'])
        u, v, n = map(Vector, refs.VIEWS[meta['view']])
        width, height = meta['pixel_size']
        for (x, y), (qx, qy) in zip(meta['pixels'], meta['plane_points']):
            local = Vector(((x-width/2)/max(width, height),
                            (height/2-y)/max(width, height), 0)) * image.empty_display_size
            world = image.matrix_world @ local
            assert abs(world.dot(u)-qx) < 1e-6, (world, qx)
            assert abs(world.dot(v)-qy) < 1e-6, (world, qy)
        camera = bpy.data.objects['REFERENCE_'+meta['view']+'_camera']
        assert camera.data.type == 'ORTHO' and camera.hide_select
        assert (camera.matrix_world.to_3x3() @ Vector((0, 0, 1))-n).length < 1e-6
        assert (camera.location-image.location).normalized().dot(n) > .99999
    perspective = bpy.data.collections['PERSPECTIVE_GUIDE']
    assert len(perspective.objects) == 1
    assert all(o.type == 'EMPTY' for o in perspective.objects)
    return dict(packed_images=len(images)+1, orthographic_cameras=len(cameras),
                perspective_measurement_cameras=0, landmarks='matched actual image-object transforms')


if opts.phase == 'create':
    # Fixture only: this process was launched with --factory-startup.
    bpy.context.preferences.filepaths.save_version = 0
    source = bpy.data.images.new('Fixture', width=320, height=240)
    source.generated_color = (.2, .4, .6, 1)
    image_path = opts.work / 'fixture-reference.png'
    source.filepath_raw = str(image_path)
    source.file_format = 'PNG'
    source.save()
    records = [dict(projection='orthographic', view=view, image=str(image_path),
                    pixels=[[0, 0], [320, 0], [0, 240]],
                    plane_points=[[-.16, .24], [.16, .24], [-.16, 0]],
                    authority='synthetic test fixture', scope='test plane', confidence='known')
               for view in refs.VIEWS]
    active, selected, camera = bpy.context.view_layer.objects.active, list(bpy.context.selected_objects), bpy.context.scene.camera
    cube = bpy.data.objects['Cube']
    before = ([tuple(v.co) for v in cube.data.vertices], cube.matrix_world.copy())
    result = refs.create_reference_set(records)
    assert bpy.context.view_layer.objects.active == active
    assert list(bpy.context.selected_objects) == selected and bpy.context.scene.camera == camera
    assert before == ([tuple(v.co) for v in cube.data.vertices], cube.matrix_world.copy())
    state = inventory()
    try:
        refs.create_reference_set(records)
        raise AssertionError('Expected duplicate collection refusal')
    except ValueError:
        pass
    assert state == inventory()
    invalid = [dict(records[0]), dict(records[1], pixels=[[500, 0], [320, 0], [0, 240]])]
    try:
        refs.create_reference_set(invalid, 'INVALID')
        raise AssertionError('Expected invalid landmark rollback')
    except ValueError:
        pass
    assert state == inventory(), 'Failed setup leaked or changed datablocks'
    refs.create_reference_set([dict(records[0], projection='perspective')], 'PERSPECTIVE_GUIDE')
    result.update(check_set())
    bpy.ops.wm.save_as_mainfile(filepath=str(opts.work/'reference-fixture.blend'))
    result['asset_and_selection_preserved'] = True
    result['invalid_setup_rollback'] = True
else:
    result = check_set()
    assert bpy.data.objects['Cube'].type == 'MESH'
    result['fresh_process_reopen'] = True

(opts.work/(opts.phase+'.json')).write_text(json.dumps(result, indent=2), encoding='utf-8')
print('TOOLS_C_REFERENCE_PASS '+json.dumps(result))
