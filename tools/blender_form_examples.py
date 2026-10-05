"""Build paired editable construction fixtures in an isolated background Blender.

Usage: blender --background --factory-startup --disable-autoexec
       --python-exit-code 1 --python tools/blender_form_examples.py -- NEW_OUTPUT
"""
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from blender_forms import create_sweep, create_curve_batch


def sampled(points, widths, depths, count=10):
    """Catmull-Rom sections for fixtures, retaining independent profile dimensions."""
    values = [(*p, w, d) for p, w, d in zip(points, widths, depths)]
    rows = []
    for i in range(len(values)-1):
        a, b, c, d = (values[max(0, i-1)], values[i], values[i+1], values[min(len(values)-1, i+2)])
        for j in range(count):
            t = j/count
            rows.append(tuple(0.5*((2*y)+(-x+z)*t+(2*x-5*y+4*z-v)*t*t+(-x+3*y-3*z+v)*t*t*t)
                              for x, y, z, v in zip(a, b, c, d)))
    rows.append(values[-1])
    if any(r[3] <= 0 or r[4] <= 0 for r in rows):
        raise ValueError('Fixture interpolation overshoots a profile; adjust controls')
    return [r[:3] for r in rows], [r[3] for r in rows], [r[4] for r in rows]


def material(name, color, roughness=0.5):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color, 1)
    shader.inputs['Roughness'].default_value = roughness
    return mat


def move_to(obj, collection):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)


def ellipsoid(name, location, scale, collection, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    move_to(obj, collection)
    obj.data.materials.append(mat)
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


def sweep(name, collection, mat, points, widths, depths, normal=(1, 0, 0), count=9):
    p, w, d = sampled(points, widths, depths, count)
    obj = create_sweep(name, collection, p, w, d, sides=20, normal=normal)
    obj.data.materials.append(mat)
    modifier = obj.modifiers.new('Fixture_Surface_Refinement', 'SUBSURF')
    modifier.levels = modifier.render_levels = 1
    return obj


def label(collection, name, text, location, mat, size=0.22):
    data = bpy.data.curves.new(name + '_Text', 'FONT')
    data.body = text
    data.align_x = 'CENTER'
    data.size = size
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (math.pi/2, 0, 0)
    data.materials.append(mat)


def build(output):
    output = Path(output).resolve()
    if output.exists():
        raise ValueError('New output directory required; existing examples are never overwritten')
    output.mkdir(parents=True)
    scene = bpy.data.scenes.new('Form_Examples')
    bpy.context.window.scene = scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 24
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 850
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.view_settings.view_transform = 'AgX'
    scene.world = bpy.data.worlds.new('Example_World')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes.get('Background').inputs['Color'].default_value = (0.10, 0.12, 0.16, 1)
    scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value = 0.3
    clay = material('Neutral_clay', (0.60, 0.42, 0.27))
    hair = material('Hair_clay', (0.65, 0.49, 0.29))
    ribbon = material('Ribbon_clay', (0.36, 0.15, 0.52))
    leaf = material('Canopy_clay', (0.25, 0.43, 0.15))
    fur = material('Fur_clay', (0.68, 0.66, 0.58))
    text = material('Label', (0.82, 0.88, 0.96))
    floor = material('Ground', (0.085, 0.105, 0.14))
    cameras = {}
    for index, kind in enumerate(('limb', 'hair', 'ribbon', 'canopy', 'fur')):
        offset = index*12.0
        collection = bpy.data.collections.new(kind.title())
        scene.collection.children.link(collection)
        left, right = offset-1.45, offset+1.45
        label(collection, kind+'_title', kind.upper() + ' / CONSTRUCTION STUDY', (offset, 0.05, 3.65), text, 0.20)
        label(collection, kind+'_before', 'BLOCKOUT', (left, -0.25, 0.08), text)
        label(collection, kind+'_after', 'FORM PASS', (right, -0.25, 0.08), text)
        if kind == 'limb':
            sweep('Limb_Tube', collection, clay, [(left, 0, 0.5), (left, 0, 1.9), (left, 0, 3.35)],
                  [0.30]*3, [0.30]*3)
            sweep('Limb_Sections', collection, clay,
                  [(right, 0, 0.5), (right+0.07, 0.12, 1.18), (right-0.05, 0, 1.95), (right+0.08, 0.20, 2.67), (right, 0.13, 3.35)],
                  [0.13, 0.26, 0.22, 0.37, 0.38], [0.13, 0.30, 0.18, 0.32, 0.34])
        elif kind == 'hair':
            sweep('Hair_Slab', collection, hair, [(left, 0, 3.30), (left, 0, 1.9), (left, 0, 0.50)],
                  [0.49]*3, [0.12]*3)
            sweep('Hair_Shaped_Lock', collection, hair,
                  [(right-0.12, 0.03, 3.30), (right+0.14, 0, 2.70), (right-0.12, -0.16, 1.98), (right-0.28, -0.03, 1.22), (right+0.03, 0.14, 0.5)],
                  [0.40, 0.47, 0.36, 0.22, 0.025], [0.12, 0.14, 0.10, 0.07, 0.025])
        elif kind == 'ribbon':
            for side in (-1, 1):
                ellipsoid('Bow_Oval_' + str(side), (left+side*0.53, 0, 1.9), (0.58, 0.18, 0.30), collection, ribbon)
                # Band loop exits and returns to the knot with visible negative space.
                steps = 64
                vertices = []
                for j in range(steps+1):
                    t = math.pi*2*j/steps
                    phase = j/steps
                    x = right+side*(0.14+0.86*math.sin(math.pi*phase))
                    y = 0.27*math.sin(2*math.pi*phase)
                    z = 1.9+0.10*math.sin(2*math.pi*phase)
                    half = 0.045+0.34*math.sin(math.pi*phase)
                    for k in (-1, 0, 1):
                        vertices.append((x, y-0.055*(1-abs(k))*math.sin(math.pi*phase), z+k*half))
                faces = [(j*3+k, j*3+k+1, (j+1)*3+k+1, (j+1)*3+k) for j in range(steps) for k in range(2)]
                mesh = bpy.data.meshes.new('Ribbon_Band_' + str(side))
                mesh.from_pydata(vertices, [], faces)
                mesh.update()
                obj = bpy.data.objects.new(mesh.name, mesh)
                collection.objects.link(obj)
                mesh.materials.append(ribbon)
                for p in mesh.polygons:
                    p.use_smooth = True
                solid = obj.modifiers.new('Fabric_Thickness', 'SOLIDIFY')
                solid.thickness = 0.025
            for center in (left, right):
                ellipsoid('Knot_' + str(center), (center, -0.10, 1.9), (0.18, 0.22, 0.20), collection, ribbon)
            for side in (-1, 1):
                sweep('Ribbon_End_'+str(side), collection, ribbon,
                      [(right+side*0.1, 0.12, 1.86), (right+side*0.26, 0.03, 1.41), (right+side*0.39, 0.14, 0.96)],
                      [0.11, 0.16, 0.14], [0.028]*3)
        elif kind == 'canopy':
            for side, center in (('Blockout', left), ('Shaped', right)):
                sweep('Trunk_'+side, collection, clay,
                      [(center, 0, 0.45), (center+0.03, 0, 1.4), (center-0.02, 0.02, 2.05)],
                      [0.17, 0.13, 0.09], [0.17, 0.13, 0.09])
            for j, (x, z, radius) in enumerate(((-0.45, 2.26, 0.58), (0.42, 2.27, 0.58), (0, 2.98, 0.60))):
                ellipsoid('Crown_Ball_'+str(j), (left+x, 0, z), (radius,)*3, collection, leaf)
            masses = []
            for j, (x, y, z, scale) in enumerate(((-0.52, 0.07, 2.15, (0.55,0.42,0.34)),
                                                 (0.38, 0.12, 2.34, (0.66,0.49,0.42)),
                                                 (-0.27, 0.11, 2.77, (0.54,0.43,0.62)),
                                                 (0.30, 0.21, 3.01, (0.42,0.38,0.35)),
                                                 (-0.72, -0.02, 2.55, (0.24,0.25,0.26)))):
                obj = ellipsoid('Crown_Mass_'+str(j), (right+x,y,z), scale, collection, leaf)
                # Coherent directional lobes instead of independent vertex noise.
                for v in obj.data.vertices:
                    p = v.co
                    p.x += 0.07*math.sin(3*p.z+1.2)*p.z
                    p.z += 0.09*math.cos(3*p.x)*max(0,p.y+0.4)
                masses.append(obj)
            # Only this disposable fixture uses a volume union. Keep source
            # mass controls as hidden editable objects; no UV/rig data exists.
            vertices, faces = [], []
            bpy.context.view_layer.update()
            for obj in masses:
                start = len(vertices)
                vertices.extend(tuple(obj.matrix_world @ v.co) for v in obj.data.vertices)
                faces.extend(tuple(start+i for i in p.vertices) for p in obj.data.polygons)
                obj.hide_render = True
                obj.hide_set(True)
            mesh = bpy.data.meshes.new('Continuous_Canopy_Volume')
            mesh.from_pydata(vertices, [], faces)
            mesh.materials.append(leaf)
            volume = bpy.data.objects.new(mesh.name, mesh)
            collection.objects.link(volume)
            remesh = volume.modifiers.new('Disposable_Volume_Union', 'REMESH')
            remesh.mode, remesh.voxel_size = 'VOXEL',0.075
            remesh.use_smooth_shade = True
            smooth = volume.modifiers.new('Local_Volume_Cleanup', 'SMOOTH')
            smooth.factor, smooth.iterations = 0.65,3
        else:
            for name, center in (('Spikes', left), ('Soft', right)):
                sweep('Fur_Base_'+name, collection, fur,
                      [(center-0.80,0,1.17),(center-0.30,0.08,1.46),(center+0.45,0.05,1.91),(center+0.77,0.01,2.53)],
                      [0.20,0.40,0.40,0.05], [0.20,0.34,0.35,0.05])
            for j in range(11):
                x = left-0.62+j*0.12
                z = 1.56+j*0.06
                bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=0.16, radius2=0.0, depth=0.45, location=(x,-0.23,z))
                obj = bpy.context.object
                obj.name = 'Rigid_Spike_'+str(j)
                obj.rotation_euler = (0.6, -0.6, 0)
                move_to(obj, collection)
                obj.data.materials.append(fur)
            for j, (dx, dz, length, width) in enumerate(((-0.60,1.38,0.30,0.09),(-0.35,1.55,0.42,0.13),
                                                       (-0.05,1.65,0.27,0.10),(0.13,1.88,0.37,0.14),
                                                       (0.42,2.12,0.23,0.10),(0.51,2.30,0.20,0.07))):
                x,z = right+dx,dz
                sweep('Soft_Tuft_'+str(j), collection, fur,
                      [(x,-0.12,z),(x+length*0.42,-0.31,z+length*0.40),(x+length,-0.22,z+length*0.90)],
                      [width,width*0.70,0.008],[0.05,0.038,0.008],count=7)
            paths = []
            for j in range(9):
                group = j//3
                x = right-0.55+group*0.45+(j%3)*0.035
                z = 1.52+group*0.35+(j%3)*0.028
                length = 0.18+(j%3)*0.025
                paths.append([(x,-0.26,z,1),(x+length*0.5,-0.34,z+length*0.5,0.6),(x+length,-0.22,z+length,0.10)])
            create_curve_batch('Selective_Fibers', collection, paths, 0.006, fur)
        bpy.ops.mesh.primitive_plane_add(size=10, location=(offset,0,0))
        ground = bpy.context.object
        ground.name = kind+'_ground'
        move_to(ground, collection)
        ground.data.materials.append(floor)
        for j, (position, energy, size) in enumerate((((offset-3,-4,6),650,4),((offset+3,-1,4),400,3),((offset,3,5),600,3))):
            data = bpy.data.lights.new(kind+'_light_'+str(j),'AREA')
            obj = bpy.data.objects.new(data.name,data)
            collection.objects.link(obj)
            obj.location = position
            obj.rotation_euler = (Vector((offset,0,1.8))-obj.location).to_track_quat('-Z','Y').to_euler()
            data.energy, data.shape, data.size = energy,'DISK',size
        data = bpy.data.cameras.new(kind+'_camera')
        camera = bpy.data.objects.new(data.name,data)
        collection.objects.link(camera)
        camera.location = (offset,-10,4.2)
        camera.rotation_euler = (Vector((offset,0,1.85))-camera.location).to_track_quat('-Z','Y').to_euler()
        data.type,data.ortho_scale = 'ORTHO',6.5
        cameras[kind] = camera
        if kind in ('limb','hair'):
            data3 = data.copy()
            camera3 = bpy.data.objects.new(kind+'_threequarter_camera',data3)
            collection.objects.link(camera3)
            camera3.location=(offset+5,-10,4.2)
            camera3.rotation_euler=(Vector((offset,0,1.85))-camera3.location).to_track_quat('-Z','Y').to_euler()
            cameras[kind+'_threequarter']=camera3
    scene.camera = cameras['limb']
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'Form_Examples.blend'))
    manifest = dict(blender_version=bpy.app.version_string, structural='PASS', visual='VISUAL REVIEW REQUIRED', images=[],
                    limits='Isolated construction fixtures; no beauty, anatomy, reference-fidelity or runtime asset certificate')
    for kind, camera in cameras.items():
        scene.camera = camera
        scene.render.filepath = str(output/(kind+'.png'))
        bpy.ops.render.render(write_still=True, scene=scene.name)
        manifest['images'].append(dict(kind=kind,path=kind+'.png',sha256=hashlib.sha256((output/(kind+'.png')).read_bytes()).hexdigest()))
    scene.camera = cameras['limb']
    # Save readable controls/cameras; source is created by this generator alone.
    scene.render.filepath = '//form-example-render.png'
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'Form_Examples.blend'))
    backup = output/'Form_Examples.blend1'
    if backup.exists():
        backup.unlink()
    manifest['blend_sha256'] = hashlib.sha256((output/'Form_Examples.blend').read_bytes()).hexdigest()
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')


if __name__ == '__main__':
    if '--' not in sys.argv or len(sys.argv[sys.argv.index('--')+1:]) != 1:
        raise ValueError('Pass one NEW output directory after --')
    build(sys.argv[sys.argv.index('--')+1])
