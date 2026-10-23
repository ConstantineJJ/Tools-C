"""Landmark registration and opt-in Blender reference-set creation. No geometry edits."""
import json
import math
from pathlib import Path

# Screen right, screen up, toward viewer. Front agrees with blender_capture.
VIEWS = {
    'front': ((1, 0, 0), (0, 0, 1), (0, -1, 0)),
    'back': ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
    'right': ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
    'left': ((0, -1, 0), (0, 0, 1), (-1, 0, 0)),
    'top': ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
}
LANDMARK_TYPES = {'visible_surface', 'hidden_construction', 'coat_tip'}


def _points(values):
    if not isinstance(values, (list, tuple)) or len(values) < 3:
        raise ValueError('At least three corresponding landmarks are required')
    if any(not isinstance(p, (list, tuple)) or len(p) != 2 or
           any(type(x) not in (int, float) or not math.isfinite(x) for x in p) for p in values):
        raise ValueError('Landmarks must be finite numeric 2D points')
    return values


def fit_landmarks(pixels, plane_points):
    """Fit x-right/y-down image pixels to world-unit screen-right/up coordinates.

    A single positive scale, in-plane rotation and translation; never aspect warp.
    Residuals diagnose inconsistent landmarks, not artistic acceptance.
    """
    p, q = _points(pixels), _points(plane_points)
    if len(p) != len(q):
        raise ValueError('Landmark counts differ')
    n = len(p)
    px, py = sum(x for x, y in p)/n, -sum(y for x, y in p)/n
    qx, qy = sum(x for x, y in q)/n, sum(y for x, y in q)/n
    centered = [(x-px, -y-py, u-qx, v-qy) for (x, y), (u, v) in zip(p, q)]
    den = sum(x*x+y*y for x, y, u, v in centered)
    if den <= 0:
        raise ValueError('Coincident source landmarks')
    a = sum(x*u+y*v for x, y, u, v in centered)/den
    b = sum(x*v-y*u for x, y, u, v in centered)/den
    scale = math.hypot(a, b)
    tx, ty = qx-a*px+b*py, qy-b*px-a*py
    errors = [math.hypot(a*x+b*y+tx-u, b*x-a*y+ty-v) for (x, y), (u, v) in zip(p, q)]
    if scale <= 0 or not all(math.isfinite(x) for x in [a, b, tx, ty, *errors]):
        raise ValueError('Degenerate or overflowing fit')
    return dict(a=a, b=b, tx=tx, ty=ty, scale=scale,
                rms_error=math.hypot(*errors)/math.sqrt(n), errors=errors)


def create_reference_set(records, collection_name='REFERENCE', camera_distance=10.0):
    """Create packed image empties and fixed orthographic cameras, leaving assets alone.

    Each record declares orthographic or perspective projection, view, absolute image
    path, matching pixels/plane_points, authority, scope and confidence strings.
    Existing collections are never overwritten. Failure removes only this call's data.
    """
    import bpy
    from mathutils import Matrix, Vector

    if not isinstance(collection_name, str) or not collection_name.strip() or len(collection_name.encode()) > 50:
        raise ValueError('Use a nonblank collection name of at most 50 UTF-8 bytes')
    if collection_name in bpy.data.collections:
        raise ValueError('Reference collection already exists; choose a new revision name')
    if type(camera_distance) not in (int, float) or not math.isfinite(camera_distance) or camera_distance <= .01:
        raise ValueError('camera_distance must be finite and greater than .01 scene units')
    if not isinstance(records, (list, tuple)) or not 1 <= len(records) <= 5:
        raise ValueError('Supply one to five explicit orthographic views')
    planned, seen = [], set()
    required = {'projection', 'view', 'image', 'pixels', 'plane_points', 'authority', 'scope', 'confidence'}
    for record in records:
        if not isinstance(record, dict) or not required <= set(record) or set(record)-required-{'landmark_types'}:
            raise ValueError('Required reference fields: '+', '.join(sorted(required))+'; optional: landmark_types')
        view = record['view']
        if not isinstance(view, str) or view not in VIEWS or view in seen:
            raise ValueError('Views must be unique: front, back, right, left, top')
        if record['projection'] not in ('orthographic', 'perspective'):
            raise ValueError('Projection must be orthographic or perspective')
        for key in ('image', 'authority', 'scope', 'confidence'):
            if not isinstance(record[key], str) or not record[key].strip():
                raise ValueError(key+' must be a nonblank string')
        path = Path(record['image'])
        if not path.is_absolute() or not path.is_file():
            raise ValueError('Reference image must be an existing absolute local file')
        fit = fit_landmarks(record['pixels'], record['plane_points'])
        if 'landmark_types' in record:
            kinds = record['landmark_types']
            if not isinstance(kinds, (list, tuple)) or len(kinds) != len(record['pixels']) or any(
                    not isinstance(kind, str) or kind not in LANDMARK_TYPES for kind in kinds):
                raise ValueError('landmark_types must match pixels and use visible_surface, hidden_construction or coat_tip')
        planned.append((record, path.resolve(), fit))
        seen.add(view)
    created_objects, created_cameras, created_images = [], [], []
    collection = None
    result = []
    try:
        # Load independent datablocks: never pack or alter an existing scene image.
        loaded = []
        for record, path, fit in planned:
            img = bpy.data.images.load(str(path), check_existing=False)
            created_images.append(img)
            width, height = img.size
            if width <= 0 or height <= 0 or img.source != 'FILE' or img.type != 'IMAGE':
                raise ValueError('Expected a still raster image: '+str(path))
            if any(not 0 <= x <= width or not 0 <= y <= height for x, y in record['pixels']):
                raise ValueError('Pixel landmarks fall outside the image')
            img.pack()
            loaded.append((record, fit, img, width, height))
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)
        collection.hide_render = True
        collection['tools_c_reference'] = True
        for record, fit, img, width, height in loaded:
            view = record['view']
            u, v, normal = (Vector(axis) for axis in VIEWS[view])
            a, b, s = fit['a'], fit['b'], fit['scale']
            cx = a*width/2+b*height/2+fit['tx']
            cy = b*width/2-a*height/2+fit['ty']
            center = u*cx+v*cy
            image = bpy.data.objects.new(collection_name+'_'+view+'_image', None)
            created_objects.append(image)
            collection.objects.link(image)
            image.empty_display_type = 'IMAGE'
            image.data = img
            image.empty_display_size = max(width, height)*s
            image.empty_image_depth = 'BACK'
            image.empty_image_offset = (-.5, -.5)
            image.color[3] = .4
            image.matrix_world = Matrix((u*(a/s)+v*(b/s), u*(-b/s)+v*(a/s), normal)).transposed().to_4x4()
            image.location = center
            camera = None
            if record['projection'] == 'orthographic':
                data = bpy.data.cameras.new(collection_name+'_'+view+'_camera')
                created_cameras.append(data)
                camera = bpy.data.objects.new(data.name, data)
                created_objects.append(camera)
                collection.objects.link(camera)
                camera.matrix_world = Matrix((u, v, normal)).transposed().to_4x4()
                camera.location = center+normal*camera_distance
                data.type = 'ORTHO'
                # Square framing encloses the entire rotated reference. Never auto-fit to asset bounds.
                data.ortho_scale = max(abs(a)*width+abs(b)*height, abs(b)*width+abs(a)*height)
                data.clip_start, data.clip_end = .001, camera_distance*4
            metadata = dict(record, fit=fit, source_path=str(Path(record['image']).resolve()),
                            pixel_size=[width, height],
                            export_policy='exclude this collection explicitly')
            for obj in (image, camera) if camera is not None else (image,):
                obj.hide_select = True
                obj.hide_render = True
                obj.lock_location = obj.lock_rotation = obj.lock_scale = (True, True, True)
                obj['tools_c_reference'] = True
                obj['registration'] = json.dumps(metadata, ensure_ascii=False, allow_nan=False)
            result.append(dict(view=view, image=image.name, camera=camera.name if camera is not None else None, fit=fit))
        bpy.context.view_layer.update()
        return dict(collection=collection.name, views=result,
                    limits='Setup and residuals only; no mesh edits, automatic likeness PASS or export filter')
    except Exception:
        for obj in reversed(created_objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        for data in created_cameras:
            bpy.data.cameras.remove(data)
        if collection is not None:
            bpy.data.collections.remove(collection)
        for img in created_images:
            bpy.data.images.remove(img)
        raise


def diagnose_reference_set(collection_name, tolerance=1e-5):
    """Read actual world registration; warnings are diagnostics, never likeness PASS.

    Existing untyped metadata remains readable. Source-side naming, model transforms,
    source-camera calibration and anatomy need separate inspection.
    """
    import bpy
    from mathutils import Vector

    if type(tolerance) not in (int, float) or not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError('Positive finite scene-unit tolerance required')
    collection = bpy.data.collections[collection_name]
    if not collection.get('tools_c_reference'):
        raise ValueError('Not a Tools_C reference collection')
    bpy.context.view_layer.update()
    rows = []
    render = bpy.context.scene.render
    square = (render.resolution_x == render.resolution_y and
              abs(render.pixel_aspect_x-render.pixel_aspect_y) < 1e-6)
    for image in sorted(collection.objects, key=lambda o: o.name):
        if image.type != 'EMPTY' or not image.get('tools_c_reference'):
            continue
        meta = json.loads(image['registration'])
        view, fit = meta['view'], meta['fit']
        u, v, n = map(Vector, VIEWS[view])
        width, height = meta['pixel_size']
        errors, drift = [], []
        for (x, y), (qx, qy) in zip(meta['pixels'], meta['plane_points']):
            local = Vector(((x+image.empty_image_offset[0]*width)/max(width, height),
                            (height-y+image.empty_image_offset[1]*height)/max(width, height), 0))*image.empty_display_size
            actual = image.matrix_world @ local
            fitted = u*(fit['a']*x+fit['b']*y+fit['tx'])+v*(fit['b']*x-fit['a']*y+fit['ty'])
            errors.append((actual-u*qx-v*qy).length)
            drift.append((actual-fitted).length)
        warnings = []
        if 'landmark_types' not in meta:
            warnings.append('untyped_landmarks')
        basis = image.matrix_world.to_3x3()
        axes = [basis.col[i] for i in range(3)]
        scales = [axis.length for axis in axes]
        if max(scales)-min(scales) > 1e-6 or min(scales) <= 1e-8:
            warnings.append('nonuniform_transform')
        if any(abs(axes[i].normalized().dot(axes[j].normalized())) > 1e-6
               for i, j in ((0, 1), (0, 2), (1, 2))) or basis.determinant() <= 0:
            warnings.append('sheared_or_reflected_transform')
        if max(drift) > tolerance:
            warnings.append('registration_drift')
        if list(image.data.size) != list(meta['pixel_size']):
            warnings.append('image_aspect_or_size_changed')
        if meta['projection'] == 'orthographic':
            if not square:
                warnings.append('render_aspect')
            camera = bpy.data.objects.get(collection_name+'_'+view+'_camera')
            if camera is None or camera.type != 'CAMERA':
                warnings.append('missing_camera')
            else:
                rotation = camera.matrix_world.to_3x3()
                if any((rotation.col[i]-axis).length > 1e-5 for i, axis in enumerate((u,v,n))):
                    warnings.append('camera_orientation')
                center = u*(fit['a']*width/2+fit['b']*height/2+fit['tx'])+v*(fit['b']*width/2-fit['a']*height/2+fit['ty'])
                offset = camera.matrix_world.translation-center
                span = max(abs(fit['a'])*width+abs(fit['b'])*height,
                           abs(fit['b'])*width+abs(fit['a'])*height)
                if (camera.data.type != 'ORTHO' or abs(camera.data.ortho_scale-span) > tolerance or
                        abs(camera.data.shift_x)*camera.data.ortho_scale > tolerance or
                        abs(camera.data.shift_y)*camera.data.ortho_scale > tolerance or
                        abs(offset.dot(u)) > tolerance or abs(offset.dot(v)) > tolerance or
                        not camera.data.clip_start < offset.dot(n) < camera.data.clip_end):
                    warnings.append('camera_framing')
        rows.append(dict(view=view, scope=meta['scope'], landmark_types=meta.get('landmark_types'),
                         fit_errors=fit['errors'], fit_rms_error=fit['rms_error'],
                         world_errors=errors, world_rms_error=math.hypot(*errors)/math.sqrt(len(errors)),
                         transform_errors=drift, warnings=warnings))
    return dict(collection=collection_name, views=rows, status='DIAGNOSTICS_ONLY',
                limits='No source-side recognition, model transform check, camera calibration or artistic acceptance')
