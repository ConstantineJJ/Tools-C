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
    diagnostic = refs.diagnose_reference_set('REFERENCE')
    assert all(not row['warnings'] for row in diagnostic['views']), diagnostic
    assert json.loads(images[0]['registration'])['landmark_types'] == [
        'visible_surface', 'hidden_construction', 'coat_tip']
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
    bpy.context.scene.render.resolution_x = bpy.context.scene.render.resolution_y = 512
    bpy.context.scene.render.pixel_aspect_x = bpy.context.scene.render.pixel_aspect_y = 1
    records = [dict(projection='orthographic', view=view, image=str(image_path),
                    pixels=[[0, 0], [320, 0], [0, 240]],
                    plane_points=[[-.16, .24], [.16, .24], [-.16, 0]],
                    authority='synthetic test fixture', scope='test plane', confidence='known',
                    landmark_types=['visible_surface', 'hidden_construction', 'coat_tip'])
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
    for types in [[], ['iris']*3, 'visible_surface', None]:
        try:
            refs.create_reference_set([dict(records[0], landmark_types=types)], 'BAD_TYPES')
            raise AssertionError('Expected invalid landmark type rejection')
        except ValueError:
            pass
        assert state == inventory()
    image = bpy.data.objects['REFERENCE_front_image']
    parent = bpy.data.objects.new('Nonuniform_parent', None)
    bpy.context.scene.collection.objects.link(parent)
    image.parent = parent
    parent.scale = (1, 2, 3)
    bpy.context.view_layer.update()
    row = next(r for r in refs.diagnose_reference_set('REFERENCE')['views'] if r['view'] == 'front')
    assert {'nonuniform_transform', 'registration_drift'} <= set(row['warnings']), row
    image.parent = None
    bpy.data.objects.remove(parent, do_unlink=True)
    image.empty_image_offset = (0, 0)
    row = next(r for r in refs.diagnose_reference_set('REFERENCE')['views'] if r['view'] == 'front')
    assert 'registration_drift' in row['warnings'], row
    image.empty_image_offset = (-.5, -.5)
    cam = bpy.data.objects['REFERENCE_front_camera']
    original = cam.matrix_world.copy()
    cam.rotation_euler.z += 3.141592653589793
    bpy.context.view_layer.update()
    row = next(r for r in refs.diagnose_reference_set('REFERENCE')['views'] if r['view'] == 'front')
    assert 'camera_orientation' in row['warnings'], row
    cam.matrix_world = original
    for axis in ('shift_x', 'shift_y'):
        setattr(cam.data, axis, .5)
        row = next(r for r in refs.diagnose_reference_set('REFERENCE')['views'] if r['view'] == 'front')
        assert 'camera_framing' in row['warnings'], (axis, row)
        setattr(cam.data, axis, 0)
    assert not refs.diagnose_reference_set('REFERENCE')['views'][0]['warnings']
    large = dict(records[0], plane_points=[[x*100, y*100] for x, y in records[0]['plane_points']])
    refs.create_reference_set([large], 'REFERENCE_LARGE')
    large_cam = bpy.data.objects['REFERENCE_LARGE_front_camera']
    for axis in ('shift_x', 'shift_y'):
        setattr(large_cam.data, axis, .25)
        assert 'camera_framing' in refs.diagnose_reference_set('REFERENCE_LARGE', tolerance=1)['views'][0]['warnings'], axis
        setattr(large_cam.data, axis, .01)
        assert not refs.diagnose_reference_set('REFERENCE_LARGE', tolerance=1)['views'][0]['warnings'], axis
        setattr(large_cam.data, axis, 0)
    bpy.context.scene.render.resolution_x = 1024
    assert 'render_aspect' in refs.diagnose_reference_set('REFERENCE')['views'][0]['warnings']
    bpy.context.scene.render.resolution_x = 512
    # Legacy records without the optional field still work and remain untyped.
    legacy = dict(records[0], projection='perspective')
    del legacy['landmark_types']
    refs.create_reference_set([legacy], 'PERSPECTIVE_GUIDE')
    assert refs.diagnose_reference_set('PERSPECTIVE_GUIDE')['views'][0]['warnings'] == ['untyped_landmarks']
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
