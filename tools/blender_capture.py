"""Bounded viewport-oriented evidence render in Blender; restores source frame/state.

Fixed views use a temporary scene/camera, not an OS screenshot. `current` derives
the camera from the active VIEW_3D. Output records this distinction explicitly.
"""
import hashlib
import json
import math
from pathlib import Path

import bpy
from mathutils import Vector

VIEWS = {"front": (0, -1, 0), "side": (1, 0, 0), "back": (0, 1, 0),
         "top": (0, 0, 1), "bottom": (0, 0, -1), "three_quarter": (1, -1, 0.6)}


def capture_viewport(output, view="front", target="selected", mode="solid", frame=None,
                     resolution=512, object_names=None, framing=None):
    if view not in (*VIEWS, 'current') or mode not in ('solid', 'material_preview', 'rendered'):
        raise ValueError('Unsupported view or mode')
    if target not in ('active', 'selected', 'character', 'scene'):
        raise ValueError('Unsupported target')
    if type(resolution) is not int or not 64 <= resolution <= 2048:
        raise ValueError('resolution must be an integer from 64 to 2048 (square pixels)')
    if frame is not None and (type(frame) is not int or abs(frame) > 1000000):
        raise ValueError('frame must be an explicit integer within +/-1000000')
    source = bpy.context.scene
    visible_render = set()
    def collect(collection):
        if collection.hide_render:
            return
        visible_render.update(o for o in collection.objects if not o.hide_render)
        for child in collection.children:
            collect(child)
    collect(source.collection)
    if target == 'character':
        if not object_names or len(set(object_names)) != len(object_names):
            raise ValueError('character requires explicit unique object_names; no name-prefix inference')
        objects = [source.objects[name] for name in object_names]
    elif object_names:
        raise ValueError('object_names applies only to character; use target=character for repeatable scope')
    elif target == 'selected':
        objects = list(bpy.context.selected_objects)
    elif target == 'active':
        objects = [bpy.context.active_object] if bpy.context.active_object else []
    else:
        objects = [o for o in source.objects if o in visible_render]
    if not objects:
        raise ValueError('Empty target')
    geometry = [o for o in objects if o.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}]
    if not geometry:
        raise ValueError('Target has no renderable geometry')
    if any(o not in visible_render for o in geometry):
        raise ValueError('Target contains hidden render geometry; resolve visibility explicitly')
    current = None
    if view == 'current':
        if bpy.app.background:
            return dict(ok=False, status='SKIP', reason='current requires an interactive VIEW_3D, not a background startup screen')
        areas = [a for a in bpy.context.screen.areas if a.type == 'VIEW_3D'] if bpy.context.screen else []
        area = bpy.context.area if bpy.context.area and bpy.context.area.type == 'VIEW_3D' else (areas[0] if areas else None)
        if area is None:
            return dict(ok=False, status='SKIP', reason='current requires a live VIEW_3D area')
        region = area.spaces.active.region_3d
        current = (region.view_matrix.inverted().copy(), region.view_perspective,
                   float(region.view_distance), float(area.spaces.active.lens))
    output = Path(output).resolve()
    if output.exists():
        raise ValueError('Capture output must be a new directory')
    old_frame, old_subframe = source.frame_current, source.frame_subframe
    temp = camera = camera_data = world = None
    light_objects, light_data = [], []
    try:
        source.frame_set(old_frame if frame is None else frame,
                         subframe=old_subframe if frame is None else 0)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        corners = [obj.evaluated_get(depsgraph).matrix_world @ Vector(p)
                   for obj in geometry for p in obj.evaluated_get(depsgraph).bound_box]
        lo = Vector([min(p[i] for p in corners) for i in range(3)])
        hi = Vector([max(p[i] for p in corners) for i in range(3)])
        if framing is None:
            center = (lo + hi) * .5
            span = max((hi-lo).length * 1.15, .01)
            framing = dict(center=list(center), span=span)
        else:
            if not isinstance(framing, dict) or set(framing) != {'center', 'span'}:
                raise ValueError('framing needs exactly center and span from BEFORE capture')
            if (not isinstance(framing['center'], (list, tuple)) or len(framing['center']) != 3
                    or not all(type(x) in (int, float) and math.isfinite(x) for x in framing['center'])
                    or type(framing['span']) not in (int, float) or not math.isfinite(framing['span']) or framing['span'] <= 0):
                raise ValueError('Invalid finite framing')
            center, span = Vector(framing['center']), float(framing['span'])
        temp = bpy.data.scenes.new('Tools_C_Evidence')
        temp.render.resolution_x = temp.render.resolution_y = resolution
        temp.render.resolution_percentage = 100
        temp.render.image_settings.file_format = 'PNG'
        # Blender embeds date/render-time text even when no visible stamp is drawn.
        # Disable those metadata fields so identical pixels can have identical bytes.
        for prop in temp.render.bl_rna.properties:
            if prop.identifier.startswith('use_stamp'):
                setattr(temp.render, prop.identifier, False)
        temp.render.film_transparent = False
        temp.render.fps, temp.render.fps_base = source.render.fps, source.render.fps_base
        temp.view_settings.view_transform = 'Standard'
        temp.view_settings.look = 'None'
        temp.view_settings.exposure = 0
        temp.view_settings.gamma = 1
        linked = set(objects)
        pending = list(objects)
        while pending:
            obj = pending.pop()
            dependencies = [obj.parent] + [getattr(m, 'object', None) for m in obj.modifiers if m.type == 'ARMATURE']
            for dep in filter(None, dependencies):
                if dep not in linked:
                    linked.add(dep); pending.append(dep)
        # Dependencies can include helper meshes: link only non-renderable dependencies.
        if any(o not in objects and o.type in {'MESH','CURVE','FONT','SURFACE','META'} for o in linked):
            raise ValueError('Renderable parent dependency outside target; include it explicitly')
        for obj in linked:
            if obj.type not in {'CAMERA', 'LIGHT'}:
                temp.collection.objects.link(obj)
        temp.frame_set(source.frame_current, subframe=source.frame_subframe)
        camera_data = bpy.data.cameras.new('Tools_C_EvidenceCamera')
        camera = bpy.data.objects.new('Tools_C_EvidenceCamera', camera_data)
        temp.collection.objects.link(camera); temp.camera = camera
        camera_data.clip_start, camera_data.clip_end = max(span*.0001, .00001), span*100
        camera_data.type = 'ORTHO'; camera_data.ortho_scale = span
        if current:
            camera.matrix_world = current[0]
            camera_data.type = 'ORTHO' if current[1] == 'ORTHO' else 'PERSP'
            camera_data.ortho_scale = current[2] * 2
            camera_data.lens = current[3]
            if current[1] == 'CAMERA' and source.camera:
                camera.matrix_world = source.camera.matrix_world.copy()
                camera_data.type = source.camera.data.type
                camera_data.lens = source.camera.data.lens
                camera_data.ortho_scale = source.camera.data.ortho_scale
        else:
            direction = Vector(VIEWS[view]).normalized()
            camera.location = center + direction * span * 2
            camera.rotation_euler = (-direction).to_track_quat('-Z', 'Y').to_euler()
        if mode == 'solid':
            temp.render.engine = 'BLENDER_WORKBENCH'
            shading = temp.display.shading
            shading.light = 'STUDIO'; shading.studiolight_rotate_z = 0
            shading.color_type = 'MATERIAL'; shading.show_shadows = True
            shading.show_cavity = True; shading.background_type = 'WORLD'
            shading.background_color = (.06, .06, .06)
        else:
            temp.render.engine = 'CYCLES'
            temp.cycles.samples = 16; temp.cycles.seed = 0; temp.cycles.use_animated_seed = False
            temp.cycles.time_limit = 30
            temp.cycles.device = 'CPU'
        if mode == 'rendered':
            temp.world = source.world
            for obj in source.objects:
                if obj.type == 'LIGHT' and not obj.hide_render:
                    temp.collection.objects.link(obj)
            lighting = 'source world and visible source lights; bounded Cycles CPU render, no compositor'
        else:
            world = bpy.data.worlds.new('Tools_C_EvidenceWorld'); world.color = (.06, .06, .06)
            temp.world = world
            lighting = 'fixed studio solid' if mode == 'solid' else 'fixed three area lights, Standard transform, Cycles CPU'
            if mode == 'material_preview':
                world.use_nodes = True
                world.node_tree.nodes['Background'].inputs['Color'].default_value = (.12, .12, .12, 1)
                world.node_tree.nodes['Background'].inputs['Strength'].default_value = .3
                for index, offset in enumerate(((1,-2,3),(-2,-1,1),(0,2,2))):
                    data = bpy.data.lights.new('Tools_C_Studio', 'AREA'); light_data.append(data)
                    data.energy = span * span * (80 if index == 0 else 40); data.size = span
                    obj = bpy.data.objects.new('Tools_C_Studio', data); light_objects.append(obj)
                    temp.collection.objects.link(obj); obj.location = center + Vector(offset) * span
                    obj.rotation_euler = (center-obj.location).to_track_quat('-Z','Y').to_euler()
        output.mkdir(parents=True)
        png = output / (view + '.png')
        temp.render.filepath = str(png)
        # Explicitly evaluate this scene: the active source scene is intentionally
        # unchanged, so reading matrix_world there can otherwise return stale data.
        with bpy.context.temp_override(scene=temp, view_layer=temp.view_layers[0]):
            temp.view_layers[0].update()
            bpy.ops.render.render(write_still=True, scene=temp.name)
        if not png.is_file() or png.stat().st_size < 100:
            raise RuntimeError('Render produced no usable image')
        metadata = dict(ok=True, status='VISUAL REVIEW REQUIRED', capture_kind='viewport-oriented evidence render',
                        view=view, target=target, objects=sorted(o.name for o in objects), mode=mode,
                        frame=source.frame_current + source.frame_subframe, fps=source.render.fps/source.render.fps_base,
                        resolution=[resolution,resolution], framing=framing, lighting=lighting,
                        camera_matrix=[float(v) for row in camera.matrix_world for v in row],
                        projection=camera_data.type, ortho_scale=camera_data.ortho_scale,
                        blender_version=bpy.app.version_string, path=str(png),
                        sha256=hashlib.sha256(png.read_bytes()).hexdigest(),
                        bounds=dict(min=list(lo), max=list(hi)),
                        limits='Current uses viewport orientation with square framing; not an exact UI screenshot. Stills do not certify motion or engine appearance.')
        (output/'capture.json').write_text(json.dumps(metadata, indent=2, allow_nan=False), encoding='utf-8')
        return metadata
    finally:
        if temp: bpy.data.scenes.remove(temp)
        for obj in light_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        for data in light_data: bpy.data.lights.remove(data)
        if camera: bpy.data.objects.remove(camera, do_unlink=True)
        if camera_data: bpy.data.cameras.remove(camera_data)
        if world: bpy.data.worlds.remove(world)
        source.frame_set(old_frame, subframe=old_subframe)
