"""Explicit factory-Blender fixtures for recovery recipes; no user-scene access.

Run: blender --background --factory-startup --python this_file -- NEW_OUTPUT_DIR
Exercises native operations, not an autonomous agent or artistic acceptance.
"""
import json
from pathlib import Path
import sys

import bmesh
import bpy


def boundary_count(mesh):
    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        return sum(e.is_boundary for e in bm.edges)
    finally:
        bm.free()


def attributes(obj):
    return {
        'vertices': [tuple(v.co) for v in obj.data.vertices],
        'faces': [tuple(p.vertices) for p in obj.data.polygons],
        'uv': [tuple(loop.uv) for loop in obj.data.uv_layers.active.data] if obj.data.uv_layers else [],
        'material_indices': [p.material_index for p in obj.data.polygons],
        'materials': [m.name for m in obj.data.materials],
        'groups': [[(g.group, g.weight) for g in v.groups] for v in obj.data.vertices],
    }


def make_mesh(name, verts, faces):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def main(output):
    if output.exists() and any(output.iterdir()):
        raise ValueError('Use a new or empty output directory')
    output.mkdir(parents=True, exist_ok=True)
    bpy.context.preferences.filepaths.save_version = 0
    results = []
    # An unrelated intentionally open sheet must remain untouched throughout.
    sheet = make_mesh('ProtectedOpenSheet', [(0, 5, 0), (1, 5, 0), (1, 6, 0), (0, 6, 0)], [(0, 1, 2, 3)])
    protected = attributes(sheet)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2)
    bm.normal_update()
    bmesh.ops.delete(bm, geom=[max(bm.faces, key=lambda f: f.normal.z)], context='FACES_ONLY')
    hole = bpy.data.meshes.new('AccidentalHole')
    bm.to_mesh(hole)
    before = boundary_count(hole)
    boundary = [e for e in bm.edges if e.is_boundary]
    bmesh.ops.holes_fill(bm, edges=boundary, sides=4)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(hole)
    bm.free()
    assert before == 4 and boundary_count(hole) == 0 and len(hole.polygons) == 6
    hole_obj = bpy.data.objects.new('RepairedHole', hole)
    bpy.context.scene.collection.objects.link(hole_obj)
    results.append({'case': 'selected_accidental_hole_fill', 'status': 'PASS', 'boundary_before': before, 'boundary_after': 0})

    weld = make_mesh('WeldRegion', [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0)], [(0, 1, 2), (4, 2, 3)])
    uv = weld.data.uv_layers.new(name='UVMap')
    for i, loop in enumerate(uv.data):
        loop.uv = (i / 8, (i % 2) / 2)
    for name in ('MaterialA', 'MaterialB'):
        weld.data.materials.append(bpy.data.materials.new(name))
    weld.data.polygons[1].material_index = 1
    prior = attributes(weld)
    bm = bmesh.new()
    bm.from_mesh(weld.data)
    bm.verts.ensure_lookup_table()
    bmesh.ops.remove_doubles(bm, verts=[bm.verts[0], bm.verts[4]], dist=0.00001)
    bm.to_mesh(weld.data)
    bm.free()
    after = attributes(weld)
    assert len(weld.data.vertices) == 4 and len(weld.data.polygons) == 2
    assert boundary_count(weld.data) == 4
    assert prior['uv'] == after['uv'] and prior['material_indices'] == after['material_indices']
    results.append({'case': 'bounded_weld_preserves_corner_uv_and_materials', 'status': 'PASS', 'vertices_before': 5, 'vertices_after': 4})

    part = make_mesh('Assembly', [(x + offset, y, 0) for offset in (0, 3) for x, y in ((0, 0), (1, 0), (1, 1), (0, 1))], [(0, 1, 2, 3), (4, 5, 6, 7)])
    part.data.materials.append(weld.data.materials[0])
    part.data.materials.append(weld.data.materials[1])
    part.data.polygons[1].material_index = 1
    uv = part.data.uv_layers.new(name='UVMap')
    for i, loop in enumerate(uv.data):
        loop.uv = (i / 10, (i % 2) / 2)
    part.vertex_groups.new(name='KeepWeights').add(list(range(8)), 0.75, 'REPLACE')
    part.location = (2, 3, 4)
    # Force dependency update before recording world transforms.
    bpy.context.view_layer.update()
    expected_world = sorted(tuple(part.matrix_world @ v.co) for v in part.data.vertices)
    expected_uv = sorted(tuple(loop.uv) for loop in part.data.uv_layers.active.data)
    bpy.ops.object.select_all(action='DESELECT')
    part.select_set(True)
    bpy.context.view_layer.objects.active = part
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    bpy.ops.object.mode_set(mode='EDIT')
    edit_mesh = bmesh.from_edit_mesh(part.data)
    for face in edit_mesh.faces:
        face.select_set(False)
    for edge in edit_mesh.edges:
        edge.select_set(False)
    for vert in edit_mesh.verts:
        vert.select_set(False)
    for face in edit_mesh.faces:
        if face.calc_center_median().x > 2:
            face.select_set(True)
    bmesh.update_edit_mesh(part.data)
    bpy.ops.mesh.separate(type='SELECTED')
    bpy.ops.object.mode_set(mode='OBJECT')
    pieces = [o for o in bpy.context.selected_objects if o.name.startswith('Assembly')]
    assert len(pieces) == 2
    assert sum(len(o.data.polygons) for o in pieces) == 2
    assert sorted(tuple(o.matrix_world @ v.co) for o in pieces for v in o.data.vertices) == expected_world
    assert sorted(tuple(loop.uv) for o in pieces for loop in o.data.uv_layers.active.data) == expected_uv
    assert sorted(o.data.materials[o.data.polygons[0].material_index].name for o in pieces) == ['MaterialA', 'MaterialB']
    assert all(abs(o.vertex_groups['KeepWeights'].weight(v.index) - 0.75) < 1e-6 for o in pieces for v in o.data.vertices)
    results.append({'case': 'selected_segmentation_preserves_world_uv_material_weights', 'status': 'PASS', 'parts': 2})

    image = bpy.data.images.new('RecoveryPixels', width=8, height=8)
    pixels = [0.2, 0.4, 0.6, 1.0] * 64
    image.pixels[:] = pixels
    image.filepath_raw = str(output / 'recovered.png')
    image.file_format = 'PNG'
    image.save()
    loaded = bpy.data.images.load(str(output / 'recovered.png'), check_existing=False)
    assert tuple(loaded.size) == (8, 8) and max(abs(a-b) for a, b in zip(loaded.pixels, pixels)) < 0.02
    results.append({'case': 'explicit_texture_save_reload', 'status': 'PASS'})
    assert attributes(sheet) == protected and boundary_count(sheet.data) == 4
    results.append({'case': 'intentional_open_surface_and_unrelated_data_preserved', 'status': 'PASS'})
    expected = {o.name: attributes(o) for o in [sheet, hole_obj, weld, *pieces]}
    bpy.ops.wm.save_as_mainfile(filepath=str(output / 'recovery-fixture.blend'))
    bpy.ops.wm.open_mainfile(filepath=str(output / 'recovery-fixture.blend'))
    assert all(attributes(bpy.data.objects[name]) == value for name, value in expected.items())
    results.append({'case': 'saved_blend_reopen_retains_repaired_data', 'status': 'PASS'})
    report = {'blender': bpy.app.version_string, 'results': results,
              'scope': 'Native isolated recipe fixtures only; not autonomous Skill execution',
              'visual': 'SKIP: no artistic asset acceptance requested',
              'rig_animation_engine': 'SKIP: full rig, animation and engine behavior not exercised'}
    (output / 'result.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('RECOVERY_NATIVE_PASS ' + str(len(results)))


if __name__ == '__main__':
    main(Path(sys.argv[sys.argv.index('--') + 1]).resolve())
