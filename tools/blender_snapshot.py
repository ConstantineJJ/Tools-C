"""Run inside Blender; inspect explicit objects without saving or changing scene state."""
import hashlib
import json
import struct

import bpy


def snapshot(stage, object_names, protected=(), action_names=(), blockers=()):
    if not object_names or len(set(object_names)) != len(object_names):
        raise ValueError("Use a nonempty unique explicit object set")
    rows = []
    for name in sorted(object_names):
        obj = bpy.data.objects[name]
        geometry = None
        if obj.type == "MESH":
            mesh = obj.data
            digest = hashlib.sha256()
            for vertex in mesh.vertices:
                digest.update(struct.pack('<3d', *vertex.co))
            for edge in mesh.edges:
                digest.update(struct.pack('<2I', *edge.vertices))
            for polygon in mesh.polygons:
                digest.update(struct.pack('<I', len(polygon.vertices)))
                digest.update(struct.pack('<' + 'I' * len(polygon.vertices), *polygon.vertices))
                digest.update(struct.pack('<I', polygon.material_index))
            geometry = dict(vertices=len(mesh.vertices), edges=len(mesh.edges), polygons=len(mesh.polygons),
                            triangles=sum(max(0, len(p.vertices)-2) for p in mesh.polygons), sha256=digest.hexdigest())
        rows.append(dict(name=name, type=obj.type, parent=obj.parent.name if obj.parent else None,
                         parent_bone=obj.parent_bone, matrix_world=[float(x) for row in obj.matrix_world for x in row],
                         geometry=geometry, bones=[dict(name=b.name, parent=b.parent.name if b.parent else None)
                             for b in sorted(obj.data.bones, key=lambda b: b.name)] if obj.type == 'ARMATURE' else [],
                         materials=sorted({slot.material.name for slot in obj.material_slots if slot.material})))
    scene = bpy.context.scene
    return dict(schema_version=1, stage=stage, blender_version=bpy.app.version_string,
                frame=scene.frame_current + scene.frame_subframe, fps=scene.render.fps / scene.render.fps_base,
                objects=rows, actions=[dict(name=name, range=list(map(float, bpy.data.actions[name].frame_range)))
                    for name in sorted(set(action_names))], protected_objects=sorted(set(protected)),
                blockers=list(blockers), verification=dict(structural='SKIP', visual='SKIP', evidence=[],
                    reason='Snapshot captured; acceptance checks have not run'))
