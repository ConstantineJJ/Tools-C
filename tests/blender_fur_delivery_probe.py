"""Disposable fur export guards and COLOR_0/alpha material round-trip fixture."""
import argparse
import json
from pathlib import Path
import struct
import sys

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import blender_export_probe as exporter
import blender_snapshot as snapshots
from blender_capture import capture_viewport


def material(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = color
    mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = .8
    return mat


def quad(name, x0, x1, y=.0):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([(x0,y,0),(x1,y,0),(x1,y,2),(x0,y,2)], [], [(0,1,2,3)])
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj

parser = argparse.ArgumentParser()
parser.add_argument('--work', type=Path, required=True)
parser.add_argument('--phase', choices=['create', 'import'], required=True)
args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
if not bpy.app.background:
    raise RuntimeError('Use a disposable factory background process')
args.work.mkdir(parents=True, exist_ok=True)

if args.phase == 'create':
    bpy.ops.wm.read_factory_settings(use_empty=True)
    native = bpy.data.hair_curves.new('Native')
    native.add_curves([2, 2])
    hair = bpy.data.objects.new('NativeHair', native)
    bpy.context.scene.collection.objects.link(hair)
    helper = bpy.data.objects.new('Reference', None)
    bpy.context.scene.collection.objects.link(helper)
    helper['tools_c_reference'] = True
    radius = native.attributes.new('radius', 'FLOAT', 'POINT')
    radius.data.foreach_set('value', [.01, .01, 0, 0])
    stats = snapshots.delivery_statistics(['NativeHair'])
    assert stats['objects'][0]['stored_native_curves'] == 2, stats
    assert stats['objects'][0]['stored_zero_radius_curves'] == 1, stats
    assert stats['visible_strands'] is None and stats['draw_calls'] is None, stats
    for name, message in [('NativeHair', 'CURVES'), ('Reference', 'reference')]:
        try:
            exporter.validate_export_objects([name])
            raise AssertionError('Export guard accepted '+name)
        except ValueError as exc:
            assert message in str(exc), exc
    # Also reject an untagged object nested in a tagged reference collection.
    coll = bpy.data.collections.new('REFERENCE')
    bpy.context.scene.collection.children.link(coll)
    coll['tools_c_reference'] = True
    nested = bpy.data.objects.new('NestedReference', None)
    coll.objects.link(nested)
    try:
        exporter.validate_export_objects(['NestedReference'])
        raise AssertionError('Reference collection guard failed')
    except ValueError as exc:
        assert 'reference' in str(exc)
    # Unknown radius is distinct from known invisible curves.
    native.attributes.remove(radius)
    assert snapshots.delivery_statistics(['NativeHair'])['objects'][0]['stored_zero_radius_curves'] is None
    bpy.data.objects.remove(hair, do_unlink=True)

    red, green = material('RedStrand', (1,.01,.01,1)), material('GreenStrand', (.01,1,.01,1))
    native_names = []
    for x, mat in [(-.5,red), (.5,green)]:
        data = bpy.data.hair_curves.new(mat.name)
        data.add_curves([3])
        data.attributes['position'].data.foreach_set('vector', [x,0,0,x,0,1,x+.1,0,2])
        data.attributes.new('radius','FLOAT','POINT').data.foreach_set('value', [.08,.07,.02])
        data.materials.append(mat)
        obj = bpy.data.objects.new(mat.name, data)
        bpy.context.scene.collection.objects.link(obj)
        native_names.append(obj.name)
    backdrop = quad('Backdrop', -1, 1, y=.1)
    backdrop.data.materials.append(material('Backdrop', (.06,.06,.06,1)))
    framing = dict(center=[0,0,1], span=2.5)
    native_capture = capture_viewport(args.work/'native', view='front', target='character',
        object_names=[backdrop.name,*native_names], mode='material_preview', resolution=256, framing=framing)
    # Delivery fixture tests COLOR_0 pigment and alpha texture, not strand equivalence.
    atlas = bpy.data.images.new('FurAlpha', width=64, height=64, alpha=True)
    pixels = []
    for y in range(64):
        for x in range(64):
            alpha = float(abs((x+.5)/64-.5) < .36*(1-(y+.5)/64)+.04)
            if y < 3 or y > 60:
                alpha = 0  # Padding prevents the repeated bottom edge leaking above the tip.
            pixels.extend((1,1,1,alpha))
    atlas.pixels.foreach_set(pixels)
    atlas.file_format = 'PNG'
    atlas.filepath_raw = str(args.work/'fur-alpha.png')
    atlas.save()
    atlas.pack()
    mat = material('FurCards', (1,1,1,1))
    mat.surface_render_method = 'DITHERED'
    tree = mat.node_tree
    color = tree.nodes.new('ShaderNodeVertexColor')
    color.layer_name = 'Pigment'
    texture = tree.nodes.new('ShaderNodeTexImage')
    texture.image = atlas
    texture.extension = 'EXTEND'
    bsdf = tree.nodes['Principled BSDF']
    tree.links.new(color.outputs['Color'], bsdf.inputs['Base Color'])
    tree.links.new(texture.outputs['Alpha'], bsdf.inputs['Alpha'])
    names = []
    for name, x0, x1, pigment in [('RedCard',-.9,-.1,(1,.01,.01,1)),('GreenCard',.1,.9,(.01,1,.01,1))]:
        obj = quad(name,x0,x1)
        obj.data.materials.append(mat)
        uv = obj.data.uv_layers.new(name='UVMap')
        for entry, coord in zip(uv.data, [(0,0),(1,0),(1,1),(0,1)]):
            entry.uv = coord
        attr = obj.data.color_attributes.new(name='Pigment', type='FLOAT_COLOR', domain='CORNER')
        for item in attr.data:
            item.color = pigment
        names.append(name)
    # A blue iris and narrow whisker sentinel expose accidental export omission.
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=.1, location=(0,-.12,1.8))
    iris = bpy.context.object
    iris.name = 'IrisSentinel'
    iris.data.materials.append(material('IrisBlue', (.01,.05,1,1)))
    names.append(iris.name)
    whisker = quad('WhiskerSentinel', -.7,.7,y=-.1)
    for vertex in whisker.data.vertices:
        vertex.co.z = .6+vertex.co.z*.01
    whisker.data.materials.append(material('WhiskerWhite',(1,1,1,1)))
    names.append(whisker.name)
    card_capture = capture_viewport(args.work/'cards', view='front', target='character',
        object_names=names, mode='material_preview', resolution=256, framing=framing)
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(args.work/'fur-fixture.blend'))
    job = dict(mode='export', source=str(args.work/'fur-fixture.blend'), objects=names,
               output=str(args.work/'export'), glb=str(args.work/'fur-fixture.glb'))
    result = exporter.run(job)
    assert result['glb_bytes'] > 0
    blob = (args.work/'fur-fixture.glb').read_bytes()
    length = struct.unpack_from('<I',blob,12)[0]
    gltf = json.loads(blob[20:20+length])
    card_primitives = [p for mesh in gltf['meshes'] for p in mesh['primitives'] if 'COLOR_0' in p['attributes']]
    assert len(card_primitives) == 2, gltf
    card_material = next(m for m in gltf['materials'] if m['name'] == 'FurCards')
    assert card_material['alphaMode'] in {'MASK','BLEND'}, card_material
    assert 'baseColorTexture' in card_material['pbrMetallicRoughness'], card_material
    assert {'IrisSentinel','WhiskerSentinel'} <= {n.get('name') for n in gltf['nodes']}
    assert not {'Reference','NestedReference',*native_names} & {n.get('name') for n in gltf['nodes']}
    (args.work/'fixture.json').write_text(json.dumps(dict(names=names, framing=framing,
        native_capture=native_capture, card_capture=card_capture, guards='PASS', statistics=stats),indent=2),encoding='utf-8')
else:
    fixture = json.loads((args.work/'fixture.json').read_text(encoding='utf-8'))
    exporter.run(dict(mode='import',glb=str(args.work/'fur-fixture.glb'),output=str(args.work/'import')))
    names = fixture['names']
    assert all(name in bpy.context.scene.objects for name in names)
    for name in ['RedCard','GreenCard']:
        assert bpy.data.objects[name].data.color_attributes
    capture = capture_viewport(args.work/'import-cards', view='front', target='character',
        object_names=names, mode='material_preview', resolution=256, framing=fixture['framing'])
    (args.work/'import-checked.json').write_text(json.dumps(capture,indent=2),encoding='utf-8')

print('TOOLS_C_FUR_DELIVERY_PASS '+args.phase)
