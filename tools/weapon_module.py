"""Weapon module interface and budget checks for a Blender source or a delivered GLB.

Interface data belongs to the project (.tooling/weapon-modules.json, schema 1).
Results are interface/budget evidence only, never visual or gameplay acceptance.
"""
import argparse
import json
import math
import struct
import sys
from pathlib import Path

AXES = {'+X': (0, 1), '-X': (0, -1), '+Y': (1, 1), '-Y': (1, -1), '+Z': (2, 1), '-Z': (2, -1)}
INTERFACE_KEYS = {'schema_version', 'forward_axis', 'markers', 'match', 'socket_origin', 'tolerance', 'budgets'}
MARKER_KEYS = {'socket', 'muzzle', 'optional'}
BUDGET_KEYS = {'max_triangles', 'max_materials', 'max_emissive_materials'}
SEPARATORS = '_-. '


class InterfaceError(ValueError):
    pass


def _no_duplicates(pairs):
    data = {}
    for key, value in pairs:
        if key in data:
            raise InterfaceError(f'Duplicate key: {key}')
        data[key] = value
    return data


def validate_interface(data):
    if not isinstance(data, dict):
        raise InterfaceError('Interface must be a JSON object')
    unknown = set(data) - INTERFACE_KEYS
    if unknown:
        raise InterfaceError(f'Unknown interface keys: {sorted(unknown)}')
    if data.get('schema_version') != 1:
        raise InterfaceError('schema_version must be 1')
    if data.get('forward_axis') not in AXES:
        raise InterfaceError(f'forward_axis must be one of {sorted(AXES)}')
    markers = data.get('markers')
    if not isinstance(markers, dict) or set(markers) - MARKER_KEYS:
        raise InterfaceError('markers must be an object with socket/muzzle/optional')
    muzzle = markers.get('muzzle')
    if not isinstance(muzzle, list) or not muzzle or not all(isinstance(m, str) and m for m in muzzle):
        raise InterfaceError('markers.muzzle must be a non-empty list of names')
    socket = markers.get('socket')
    if socket is not None and (not isinstance(socket, str) or not socket):
        raise InterfaceError('markers.socket must be a name or null')
    optional = markers.get('optional', [])
    if not isinstance(optional, list) or not all(isinstance(m, str) and m for m in optional):
        raise InterfaceError('markers.optional must be a list of names')
    match = data.get('match', 'exact')
    if match not in ('exact', 'suffix'):
        raise InterfaceError('match must be exact or suffix')
    origin = data.get('socket_origin')
    if origin is not None and (not isinstance(origin, list) or len(origin) != 3
                               or not all(isinstance(v, (int, float)) and math.isfinite(v) for v in origin)):
        raise InterfaceError('socket_origin must be three finite numbers')
    tolerance = data.get('tolerance', 0.002)
    if not isinstance(tolerance, (int, float)) or not 0 <= tolerance < 1:
        raise InterfaceError('tolerance must be a number in [0, 1)')
    budgets = data.get('budgets', {})
    if not isinstance(budgets, dict) or set(budgets) - BUDGET_KEYS:
        raise InterfaceError('budgets accepts max_triangles/max_materials/max_emissive_materials')
    for key, value in budgets.items():
        if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
            raise InterfaceError(f'budgets.{key} must be a non-negative integer or null')
    return dict(forward_axis=data['forward_axis'], socket=socket, muzzle=list(muzzle), optional=list(optional),
                match=match, socket_origin=origin, tolerance=float(tolerance), budgets=dict(budgets))


def load_interface(path):
    text = Path(path).read_text(encoding='utf-8')
    return validate_interface(json.loads(text, object_pairs_hook=_no_duplicates))


def _find(names, wanted, match):
    if match == 'exact':
        return [wanted] if wanted in names else []
    found = []
    for name in names:
        if name == wanted or (name.endswith(wanted) and name[-len(wanted) - 1] in SEPARATORS):
            found.append(name)
    return sorted(found)


def evaluate(interface, facts):
    """facts: markers {name: [x,y,z] in module-root space}, bounds ([min],[max]) of meshes,
    triangles int|None, materials set, emissive set."""
    items = []

    def add(status, check, message):
        items.append(dict(status=status, check=check, message=message))

    names = facts['markers']
    axis, sign = AXES[interface['forward_axis']]
    tol = interface['tolerance']
    bounds = facts.get('bounds')
    if interface['socket']:
        found = _find(names, interface['socket'], interface['match'])
        if not found:
            add('FAIL', 'socket', f"Socket marker '{interface['socket']}' not found")
        elif len(found) > 1:
            add('FAIL', 'socket', f'Ambiguous socket markers: {found}')
        elif interface['socket_origin'] is not None:
            pos = names[found[0]]
            offset = max(abs(a - b) for a, b in zip(pos, interface['socket_origin']))
            add('PASS' if offset <= tol else 'FAIL', 'socket',
                f'{found[0]} offset {offset:.4f} (tolerance {tol})')
        else:
            add('PASS', 'socket', f'{found[0]} present; no fixed socket_origin declared')
    else:
        add('SKIP', 'socket', 'Project declares no socket marker')
    for wanted in interface['muzzle']:
        found = _find(names, wanted, interface['match'])
        if not found:
            add('FAIL', 'muzzle', f"Muzzle marker '{wanted}' not found")
            continue
        for name in found:
            if not bounds:
                add('SKIP', 'muzzle', f'{name} present; no mesh bounds to compare')
                continue
            front = max(bounds[0][axis] * sign, bounds[1][axis] * sign)
            lead = names[name][axis] * sign
            add('PASS' if lead >= front - tol else 'FAIL', 'muzzle',
                f'{name} at {lead:.4f} along {interface["forward_axis"]}; mesh front {front:.4f}')
    for wanted in interface['optional']:
        found = _find(names, wanted, interface['match'])
        add('PASS' if found else 'SKIP', 'optional_marker',
            f"{wanted}: {', '.join(found) if found else 'not present'}")
    budgets = interface['budgets']
    measured = dict(max_triangles=facts.get('triangles'), max_materials=len(facts.get('materials', ())),
                    max_emissive_materials=len(facts.get('emissive', ())))
    for key in sorted(BUDGET_KEYS):
        limit = budgets.get(key)
        value = measured[key]
        if limit is None:
            add('SKIP', key, f'{value} measured; no project limit declared')
        elif value is None:
            add('SKIP', key, 'Not measurable from this input')
        else:
            add('PASS' if value <= limit else 'FAIL', key, f'{value} / {limit}')
    status = 'FAIL' if any(i['status'] == 'FAIL' for i in items) else \
        'WARN' if any(i['status'] == 'WARN' for i in items) else 'STRUCTURAL PASS'
    return dict(status=status, items=items, triangles=facts.get('triangles'),
                materials=sorted(facts.get('materials', ())), emissive=sorted(facts.get('emissive', ())),
                bounds=bounds, scope='Interface and budget evidence only; visual, functional and runtime review remain open')


# ---------------------------------------------------------------- Blender source

def check_blender(interface, root_name):
    import bpy  # noqa: F401 - available only inside Blender
    root = bpy.data.objects[root_name]
    objects = [root, *root.children_recursive]
    inverse = root.matrix_world.inverted()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    markers, lo, hi = {}, [math.inf] * 3, [-math.inf] * 3
    triangles, materials, emissive = 0, set(), set()
    for obj in objects:
        if obj is not root:
            markers[obj.name] = list(inverse @ obj.matrix_world.translation)
        if obj.type != 'MESH':
            continue
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        try:
            mesh.calc_loop_triangles()
            triangles += len(mesh.loop_triangles)
            matrix = inverse @ obj.matrix_world
            for vertex in mesh.vertices:
                co = matrix @ vertex.co
                for i in range(3):
                    lo[i], hi[i] = min(lo[i], co[i]), max(hi[i], co[i])
        finally:
            evaluated.to_mesh_clear()
        for slot in obj.material_slots:
            if slot.material:
                materials.add(slot.material.name)
                if _blender_emissive(slot.material):
                    emissive.add(slot.material.name)
    bounds = (lo, hi) if math.isfinite(lo[0]) else None
    report = evaluate(interface, dict(markers=markers, bounds=bounds, triangles=triangles,
                                      materials=materials, emissive=emissive))
    report.update(source='blender', root=root_name, objects=len(objects))
    return report


def _blender_emissive(material):
    if not material.use_nodes or not material.node_tree:
        return False
    for node in material.node_tree.nodes:
        if node.type == 'EMISSION' and node.inputs['Strength'].default_value > 0:
            return True
        if node.type == 'BSDF_PRINCIPLED':
            strength = node.inputs['Emission Strength'].default_value
            color = node.inputs['Emission Color'].default_value
            if strength > 0 and max(color[:3]) > 0:
                return True
    return False


# ---------------------------------------------------------------- GLB delivery

def read_gltf(path):
    data = Path(path).read_bytes()
    if len(data) < 20 or data[:4] != b'glTF':
        raise ValueError('Not a binary glTF file')
    length, kind = struct.unpack_from('<I4s', data, 12)
    if kind != b'JSON':
        raise ValueError('First GLB chunk is not JSON')
    return json.loads(data[20:20 + length].decode('utf-8'))


def _matmul(a, b):
    return [[sum(a[r][k] * b[k][c] for k in range(4)) for c in range(4)] for r in range(4)]


def _node_matrix(node):
    if 'matrix' in node:
        m = node['matrix']
        return [[m[c * 4 + r] for c in range(4)] for r in range(4)]
    tx, ty, tz = node.get('translation', [0, 0, 0])
    qx, qy, qz, qw = node.get('rotation', [0, 0, 0, 1])
    sx, sy, sz = node.get('scale', [1, 1, 1])
    rot = [[1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy - qz * qw), 2 * (qx * qz + qy * qw)],
           [2 * (qx * qy + qz * qw), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz - qx * qw)],
           [2 * (qx * qz - qy * qw), 2 * (qy * qz + qx * qw), 1 - 2 * (qx * qx + qy * qy)]]
    return [[rot[r][0] * sx, rot[r][1] * sy, rot[r][2] * sz, (tx, ty, tz)[r]] for r in range(3)] + [[0, 0, 0, 1]]


def _invert(m):
    a = [row[:] + [1.0 if i == j else 0.0 for j in range(4)] for i, row in enumerate(m)]
    for col in range(4):
        pivot = max(range(col, 4), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) < 1e-12:
            raise ValueError('Singular node transform')
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [v / scale for v in a[col]]
        for r in range(4):
            if r != col:
                factor = a[r][col]
                a[r] = [v - factor * p for v, p in zip(a[r], a[col])]
    return [row[4:] for row in a]


def _apply(m, p):
    return [sum(m[r][c] * (list(p) + [1])[c] for c in range(4)) for r in range(3)]


def _to_blender(p):
    """glTF is +Y up; Blender exporter maps Blender (x, y, z) to glTF (x, z, -y)."""
    return [p[0], -p[2], p[1]]


def check_glb(interface, path, root_name=None):
    gltf = read_gltf(path)
    nodes = gltf.get('nodes', [])
    scene = gltf.get('scenes', [{}])[gltf.get('scene', 0)] if gltf.get('scenes') else {}
    world = {}

    def walk(index, parent):
        world[index] = _matmul(parent, _node_matrix(nodes[index]))
        for child in nodes[index].get('children', []):
            walk(child, world[index])

    identity = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    for root in scene.get('nodes', range(len(nodes))):
        walk(root, identity)
    base, members = identity, set(world)
    if root_name is not None:
        index = next((i for i, n in enumerate(nodes) if n.get('name') == root_name), None)
        if index is None:
            raise ValueError(f'Root node not found: {root_name}')
        base = _invert(world[index])
        members, stack = set(), [index]
        while stack:
            current = stack.pop()
            members.add(current)
            stack.extend(nodes[current].get('children', []))
    markers, lo, hi = {}, [math.inf] * 3, [-math.inf] * 3
    triangles, used = 0, set()
    accessors, meshes = gltf.get('accessors', []), gltf.get('meshes', [])
    for index in sorted(members):
        node, matrix = nodes[index], _matmul(base, world[index])
        if node.get('name') and index in world and (root_name is None or nodes[index].get('name') != root_name):
            markers[node['name']] = _to_blender(_apply(matrix, (0, 0, 0)))
        if 'mesh' not in node:
            continue
        for primitive in meshes[node['mesh']].get('primitives', []):
            position = accessors[primitive['attributes']['POSITION']]
            if primitive.get('mode', 4) == 4:
                count = accessors[primitive['indices']]['count'] if 'indices' in primitive else position['count']
                triangles += count // 3
            if 'material' in primitive:
                used.add(primitive['material'])
            pmin, pmax = position.get('min'), position.get('max')
            if pmin and pmax:
                for corner in ([x, y, z] for x in (pmin[0], pmax[0]) for y in (pmin[1], pmax[1]) for z in (pmin[2], pmax[2])):
                    point = _to_blender(_apply(matrix, corner))
                    for i in range(3):
                        lo[i], hi[i] = min(lo[i], point[i]), max(hi[i], point[i])
    materials_data = gltf.get('materials', [])
    materials = {materials_data[i].get('name', f'material_{i}') for i in used}
    emissive = {materials_data[i].get('name', f'material_{i}') for i in used
                if any(v > 0 for v in materials_data[i].get('emissiveFactor', [0, 0, 0]))
                and materials_data[i].get('extensions', {}).get('KHR_materials_emissive_strength', {}).get('emissiveStrength', 1) > 0}
    bounds = (lo, hi) if math.isfinite(lo[0]) else None
    report = evaluate(interface, dict(markers=markers, bounds=bounds, triangles=triangles,
                                      materials=materials, emissive=emissive))
    report.update(source='glb', file=str(path), root=root_name)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    glb = sub.add_parser('glb', help='Check a delivered GLB against a project weapon interface')
    glb.add_argument('file')
    glb.add_argument('--interface', required=True)
    glb.add_argument('--root', default=None, help='Module root node name (default: whole scene)')
    args = parser.parse_args(argv)
    try:
        report = check_glb(load_interface(args.interface), args.file, args.root)
    except (InterfaceError, ValueError, OSError, KeyError, IndexError) as error:
        print(json.dumps(dict(status='FAIL', error=str(error)), indent=2))
        return 2
    print(json.dumps(report, indent=2))
    return 1 if report['status'] == 'FAIL' else 0


if __name__ == '__main__':
    sys.exit(main())
