"""Editable form helpers. Pure geometry math works without Blender.

These helpers construct a chosen profile, not anatomy or an artistic design.
Dimensions are half-width/half-thickness in the path's transported local frame.
"""
import math


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, value):
    return tuple(x * value for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def unit(a):
    length = math.sqrt(dot(a, a))
    if length < 1e-12:
        raise ValueError('Zero-length direction; remove duplicate samples or split a cusp')
    return mul(a, 1/length)


def points3(points):
    result = [tuple(float(x) for x in p) for p in points]
    if len(result) < 2 or any(len(p) != 3 or not all(map(math.isfinite, p)) for p in result):
        raise ValueError('At least two finite 3D samples required')
    for a, b in zip(result, result[1:]):
        unit(sub(b, a))
    return result


def transported_frames(points, normal=None):
    """Parallel transport avoids independent up-vector/sign choices per ring.

    Exact reversing tangents are ambiguous; reject them rather than silently flip.
    Returns (tangent, width_direction, thickness_direction) for each point.
    """
    points = points3(points)
    segments = [unit(sub(b, a)) for a, b in zip(points, points[1:])]
    tangents = [segments[0]]
    for a, b in zip(segments, segments[1:]):
        if dot(a, b) < -0.999999:
            raise ValueError('Reversing path cusp; split or resample the path')
        tangents.append(unit(add(a, b)))
    tangents.append(segments[-1])
    if normal is None:
        normal = min(((1, 0, 0), (0, 1, 0), (0, 0, 1)), key=lambda a: abs(dot(a, tangents[0])))
    if len(normal) != 3 or not all(math.isfinite(x) for x in normal):
        raise ValueError('Finite initial normal required')
    width = unit(sub(normal, mul(tangents[0], dot(normal, tangents[0]))))
    result = [(tangents[0], width, unit(cross(tangents[0], width)))]
    for old, tangent in zip(tangents, tangents[1:]):
        axis = cross(old, tangent)
        sine = math.sqrt(dot(axis, axis))
        cosine = max(-1.0, min(1.0, dot(old, tangent)))
        if cosine < -0.999999:
            raise ValueError('Ambiguous frame reversal')
        if sine > 1e-10:
            axis = mul(axis, 1/sine)
            width = add(add(mul(width, cosine), mul(cross(axis, width), sine)),
                        mul(axis, dot(axis, width)*(1-cosine)))
        width = unit(sub(width, mul(tangent, dot(width, tangent))))
        result.append((tangent, width, unit(cross(tangent, width))))
    return result


def sweep_geometry(points, widths, thicknesses, sides=12, normal=None):
    """Closed ellipse-profile sweep with root-to-tip arc-length UV coordinates.

    Small positive terminal sections avoid a collapsed ring of degenerate faces.
    Width and thickness are independent, so this is not a universal round tube.
    """
    points = points3(points)
    if type(sides) is not int or not 4 <= sides <= 128:
        raise ValueError('sides must be an integer from 4 to 128')
    if len(widths) != len(points) or len(thicknesses) != len(points):
        raise ValueError('One width and thickness per path sample required')
    if any(not math.isfinite(v) or v <= 0 for v in list(widths) + list(thicknesses)):
        raise ValueError('Positive finite profile dimensions required')
    frames = transported_frames(points, normal)
    distances = [0.0]
    for a, b in zip(points, points[1:]):
        distances.append(distances[-1] + math.sqrt(dot(sub(b, a), sub(b, a))))
    vertices = []
    for point, width, thickness, (_, u, v) in zip(points, widths, thicknesses, frames):
        for j in range(sides):
            angle = 2*math.pi*j/sides
            vertices.append(add(point, add(mul(u, width*math.cos(angle)), mul(v, thickness*math.sin(angle)))))
    faces, uvs = [], []
    for i in range(len(points)-1):
        for j in range(sides):
            k = (j+1) % sides
            faces.append((i*sides+j, i*sides+k, (i+1)*sides+k, (i+1)*sides+j))
            uvs.append(((j/sides, distances[i]/distances[-1]), ((j+1)/sides, distances[i]/distances[-1]),
                        ((j+1)/sides, distances[i+1]/distances[-1]), (j/sides, distances[i+1]/distances[-1])))
    for index, reverse in ((0, True), (len(points)-1, False)):
        ring = tuple(index*sides+j for j in range(sides))
        if reverse:
            ring = ring[::-1]
        faces.append(ring)
        uvs.append(tuple((0.5+0.5*math.cos(2*math.pi*(v % sides)/sides),
                          0.5+0.5*math.sin(2*math.pi*(v % sides)/sides)) for v in ring))
    return dict(vertices=vertices, faces=faces, loop_uvs=uvs, frames=frames)


def create_sweep(name, collection, points, widths, thicknesses, **options):
    """Create new mesh only; no selection operators, joins, remesh or source edits."""
    import bpy
    if name in bpy.data.objects:
        raise ValueError('Object name already exists: ' + name)
    data = sweep_geometry(points, widths, thicknesses, **options)
    mesh = bpy.data.meshes.new(name + '_Mesh')
    mesh.from_pydata(data['vertices'], [], data['faces'])
    mesh.update()
    uv = mesh.uv_layers.new(name='RootToTip')
    for polygon, face_uv in zip(mesh.polygons, data['loop_uvs']):
        polygon.use_smooth = len(polygon.vertices) == 4
        for index, value in zip(polygon.loop_indices, face_uv):
            uv.data[index].uv = value
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    return obj


def create_curve_batch(name, collection, paths, radius=0.01, material=None):
    """Many POLY splines in one editable curve; one data update after the batch.

    Each path is a list of (x,y,z[,radius_multiplier]). All inputs are validated
    before creating any datablock. Use several named batches for editable layers.
    """
    import bpy
    if name in bpy.data.objects:
        raise ValueError('Object name already exists: ' + name)
    if not math.isfinite(radius) or radius <= 0:
        raise ValueError('Positive finite radius required')
    clean = []
    for path in paths:
        rows = [tuple(float(v) for v in p) for p in path]
        if any(len(p) not in (3, 4) or not all(map(math.isfinite, p)) or (len(p) == 4 and p[3] <= 0) for p in rows):
            raise ValueError('Finite XYZ and optional positive radius multiplier required')
        points3([p[:3] for p in rows])
        clean.append(rows)
    if not clean:
        raise ValueError('Nonempty curve batch required')
    curve = bpy.data.curves.new(name + '_Curve', 'CURVE')
    curve.dimensions = '3D'
    curve.resolution_u = 1
    curve.bevel_depth = radius
    curve.bevel_resolution = 2
    for path in clean:
        spline = curve.splines.new('POLY')
        spline.points.add(len(path)-1)
        spline.points.foreach_set('co', [v for p in path for v in (*p[:3], 1.0)])
        for point, row in zip(spline.points, path):
            point.radius = row[3] if len(row) == 4 else 1.0
    if material:
        curve.materials.append(material)
    obj = bpy.data.objects.new(name, curve)
    collection.objects.link(obj)
    return obj


def parent_keep_world(child, parent):
    """Keep world placement while assigning an object parent (no bone parenting)."""
    if child == parent:
        raise ValueError('Cannot parent an object to itself')
    ancestor = parent
    while ancestor:
        if ancestor == child:
            raise ValueError('Parenting cycle')
        ancestor = ancestor.parent
    inverse = parent.matrix_world.inverted()
    world = child.matrix_world.copy()
    child.parent = parent
    child.parent_type = 'OBJECT'
    child.parent_bone = ''
    child.matrix_parent_inverse = inverse
    child.matrix_world = world
