"""Run inside Blender; inspect explicit objects without saving or changing scene state."""
import hashlib
import json
import struct

import bpy

DATA_CATEGORIES = {'uvs', 'normals', 'shape_keys', 'weights', 'modifiers', 'curves', 'material_graphs'}


def delivery_statistics(object_names):
    """Read source/evaluated budgets separately; never estimate visible hairs/costs.

    Native counters cover direct CURVES datablocks, not arbitrary GeometrySet
    instances/components. All-zero-radius means every stored point has radius zero;
    an absent radius attribute is unknown rather than an invisible curve.
    """
    if not object_names or len(set(object_names)) != len(object_names):
        raise ValueError('Use a nonempty unique explicit object set')
    graph = bpy.context.evaluated_depsgraph_get()
    rows = []
    for name in object_names:
        obj = bpy.context.scene.objects[name]
        evaluated = obj.evaluated_get(graph)
        row = dict(name=name, stored_vertices=len(obj.data.vertices) if obj.type == 'MESH' else None,
                   stored_native_curves=len(obj.data.curves) if obj.type == 'CURVES' else 0,
                   evaluated_native_curves=len(evaluated.data.curves) if evaluated.type == 'CURVES' else 0,
                   stored_zero_radius_curves=None, evaluated_triangles=None,
                   materials=[s.material.name if s.material else None for s in obj.material_slots],
                   hide_render=obj.hide_render)
        if obj.type == 'CURVES':
            radius = obj.data.attributes.get('radius')
            if radius is not None and radius.domain == 'POINT' and radius.data_type == 'FLOAT':
                row['stored_zero_radius_curves'] = sum(
                    all(radius.data[i].value == 0 for i in range(c.first_point_index, c.first_point_index+c.points_length))
                    for c in obj.data.curves)
        if evaluated.type in {'MESH', 'CURVE', 'SURFACE', 'FONT'}:
            mesh = evaluated.to_mesh()
            try:
                mesh.calc_loop_triangles()
                row['evaluated_triangles'] = len(mesh.loop_triangles)
            finally:
                evaluated.to_mesh_clear()
        rows.append(row)
    return dict(objects=rows, visible_strands=None, draw_calls=None, vram_bytes=None,
                overdraw=None, card_count=None, atlas_resolution=None,
                limits='Direct source/evaluated budgets only; cards/atlas need declared roles; '
                       'hidden components, shader visibility and renderer costs require separate inspection/profiling')


def _digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',', ':'),allow_nan=False).encode()).hexdigest()


def _value(value):
    if value is None or isinstance(value,(bool,int,float,str)):
        return value
    if isinstance(value,bpy.types.ID):
        return dict(type=value.bl_rna.identifier,name=value.name_full,
                    library=value.library.filepath if value.library else None)
    if isinstance(value,bpy.types.bpy_struct):
        return dict(type=value.bl_rna.identifier,name=getattr(value,'name',None))
    if isinstance(value,set):
        return sorted(_value(v) for v in value)
    try:
        return [_value(v) for v in value]
    except TypeError:
        raise ValueError('Unsupported snapshot value: '+type(value).__name__)


def _properties(rna):
    result={}
    for prop in rna.bl_rna.properties:
        if prop.identifier=='rna_type' or prop.type=='COLLECTION' or prop.is_readonly:
            continue
        result[prop.identifier]=_value(getattr(rna,prop.identifier))
    return result


def _graph(tree, seen=()):
    if tree is None:
        return None
    if tree in seen:
        return dict(reference=tree.name)
    nodes=[]
    for node in sorted(tree.nodes,key=lambda n:n.name):
        row=dict(name=node.name,type=node.bl_idname,properties=_properties(node),
                 inputs=[dict(identifier=s.identifier,default=_value(s.default_value) if hasattr(s,'default_value') else None)
                         for s in node.inputs])
        if hasattr(node,'node_tree'):
            row['group']=_graph(node.node_tree,(*seen,tree))
        if hasattr(node,'color_ramp'):
            ramp=node.color_ramp
            row['color_ramp']=dict(interpolation=ramp.interpolation,color_mode=ramp.color_mode,
                                  elements=[dict(position=e.position,color=list(e.color)) for e in ramp.elements])
        for key in ('mapping','texture_mapping'):
            if hasattr(node,key): row[key]=_properties(getattr(node,key))
        nodes.append(row)
    links=sorted((l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier) for l in tree.links)
    return dict(nodes=nodes,links=links)


def data_fingerprints(obj, categories):
    """Declared source representation, not all possible Blender properties/resources."""
    result={}
    for category in sorted(categories):
        value=None
        if category=='uvs' and obj.type=='MESH':
            value=[dict(name=l.name,active_render=l.active_render,uv=[list(p.uv) for p in l.data]) for l in obj.data.uv_layers]
        elif category=='normals' and obj.type=='MESH':
            value=dict(corner=[list(n.vector) for n in obj.data.corner_normals],
                       smooth=[p.use_smooth for p in obj.data.polygons],
                       sharp_edge=[v.value for v in obj.data.attributes['sharp_edge'].data] if 'sharp_edge' in obj.data.attributes else [])
        elif category=='shape_keys' and obj.type=='MESH' and obj.data.shape_keys:
            value=[dict(name=k.name,relative=k.relative_key.name,value=k.value,slider_min=k.slider_min,
                        slider_max=k.slider_max,interpolation=k.interpolation,vertex_group=k.vertex_group,
                        coordinates=[list(v.co) for v in k.data]) for k in obj.data.shape_keys.key_blocks]
        elif category=='weights' and obj.type=='MESH':
            groups={g.index:g.name for g in obj.vertex_groups}
            value=dict(groups=[g.name for g in obj.vertex_groups],
                       weights=[sorted((groups[g.group],g.weight) for g in v.groups) for v in obj.data.vertices])
        elif category=='modifiers':
            value=[dict(type=m.type,properties=_properties(m)) for m in obj.modifiers]
        elif category=='curves' and obj.type=='CURVE':
            value=dict(properties=_properties(obj.data),splines=[dict(type=s.type,properties=_properties(s),
                points=[dict(co=list(p.co),radius=p.radius,tilt=p.tilt) for p in s.points],
                bezier=[dict(co=list(p.co),left=list(p.handle_left),right=list(p.handle_right),
                             left_type=p.handle_left_type,right_type=p.handle_right_type,radius=p.radius,tilt=p.tilt)
                        for p in s.bezier_points]) for s in obj.data.splines])
        elif category=='material_graphs':
            value=[None if not slot.material else dict(name=slot.material.name,
                    properties=_properties(slot.material),graph=_graph(slot.material.node_tree)) for slot in obj.material_slots]
        result[category]=_digest(value)
    return result


def measure_objects(object_names, max_vertices=1000000):
    """Evaluated world bounds, pivots and local axes in declared scene units."""
    import math
    if not object_names or len(object_names)>256 or len(set(object_names))!=len(object_names):
        raise ValueError('Explicit unique object scope required (1..256)')
    if type(max_vertices) is not int or not 1<=max_vertices<=1000000:
        raise ValueError('Vertex budget must be 1..1000000')
    graph=bpy.context.evaluated_depsgraph_get();rows=[];remaining=max_vertices
    for name in object_names:
        obj=bpy.context.scene.objects[name];evaluated=obj.evaluated_get(graph)
        mesh=evaluated.to_mesh() if evaluated.type in ('MESH','CURVE','SURFACE','FONT','META') else None
        try:
            if mesh is None or not mesh.vertices:raise ValueError('No evaluated surface: '+name)
            if len(mesh.vertices)>remaining:raise ValueError('Evaluated vertex budget exceeded')
            remaining-=len(mesh.vertices)
            points=[evaluated.matrix_world@v.co for v in mesh.vertices]
            if not all(math.isfinite(float(v)) for p in points for v in p):raise ValueError('Non-finite world geometry')
            low=[min(p[i] for p in points) for i in range(3)];high=[max(p[i] for p in points) for i in range(3)]
            basis=evaluated.matrix_world.to_3x3()
            rows.append(dict(object=name,world_bounds=dict(min=low,max=high),
                world_dimensions=[b-a for a,b in zip(low,high)],pivot=list(evaluated.matrix_world.translation),
                local_axes_world=[list(basis.col[i].normalized()) for i in range(3)],
                determinant=basis.determinant(),evaluated_vertices=len(points)))
        finally:
            if mesh is not None:evaluated.to_mesh_clear()
    units=bpy.context.scene.unit_settings
    return dict(objects=rows,units=dict(system=units.system,scale_length=units.scale_length,length_unit=units.length_unit),
                measurement_unit='SCENE_UNITS',limits='Floating-point evaluated surfaces; physical units require calibration. Not minimum clearance or whole-scene QA.')


def snapshot(stage, object_names, protected=(), action_names=(), blockers=(), data_categories=(), update_scenes=True):
    if not object_names or len(set(object_names)) != len(object_names):
        raise ValueError("Use a nonempty unique explicit object set")
    if len(set(data_categories))!=len(data_categories) or set(data_categories)-DATA_CATEGORIES:
        raise ValueError('Unknown or duplicate protected-data category')
    if update_scenes:
        for source_scene in bpy.data.scenes:
            for layer in source_scene.view_layers:
                layer.update()
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
        row=dict(name=name, type=obj.type, parent=obj.parent.name if obj.parent else None,
                         parent_bone=obj.parent_bone, matrix_world=[float(x) for row in obj.matrix_world for x in row],
                         geometry=geometry, bones=[dict(name=b.name, parent=b.parent.name if b.parent else None)
                             for b in sorted(obj.data.bones, key=lambda b: b.name)] if obj.type == 'ARMATURE' else [],
                         materials=sorted({slot.material.name for slot in obj.material_slots if slot.material}))
        if data_categories:
            row['data_fingerprints']=data_fingerprints(obj,data_categories)
        rows.append(row)
    scene = bpy.context.scene
    result=dict(schema_version=1, stage=stage, blender_version=bpy.app.version_string,
                frame=scene.frame_current + scene.frame_subframe, fps=scene.render.fps / scene.render.fps_base,
                objects=rows, actions=[dict(name=name, range=list(map(float, bpy.data.actions[name].frame_range)))
                    for name in sorted(set(action_names))], protected_objects=sorted(set(protected)),
                blockers=list(blockers), verification=dict(structural='SKIP', visual='SKIP', evidence=[],
                    reason='Snapshot captured; acceptance checks have not run'))
    if data_categories:
        result['data_categories']=sorted(data_categories)
    return result
