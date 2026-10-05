"""Read-only selected-pair surface/volume diagnostics inside Blender.

No nearest-normal sign test. Closed oriented meshes use several parity rays;
open/ambiguous volumes remain inconclusive. Proximity is a sampled upper bound,
not a certified global minimum clearance or motion-collision test.
"""
import math


def _surface(obj, depsgraph):
    from collections import Counter
    from mathutils.bvhtree import BVHTree
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    if mesh is None:
        raise ValueError('Object has no evaluated surface: ' + obj.name)
    try:
        mesh.calc_loop_triangles()
        vertices = [evaluated.matrix_world @ v.co for v in mesh.vertices]
        triangles = [tuple(t.vertices) for t in mesh.loop_triangles]
        if not vertices or not triangles:
            raise ValueError('Empty evaluated surface: ' + obj.name)
        edges = Counter()
        orientations = Counter()
        for p in mesh.polygons:
            ids = list(p.vertices)
            for a,b in zip(ids,ids[1:]+ids[:1]):
                key=tuple(sorted((a,b)))
                edges[key]+=1
                orientations[key]+=1 if a < b else -1
        closed=all(n==2 and orientations[e]==0 for e,n in edges.items())
        tree=BVHTree.FromPolygons(vertices,triangles,all_triangles=True,epsilon=0.0)
        low=tuple(min(v[i] for v in vertices) for i in range(3))
        high=tuple(max(v[i] for v in vertices) for i in range(3))
        return dict(vertices=vertices,triangles=triangles,tree=tree,closed=closed,low=low,high=high)
    finally:
        evaluated.to_mesh_clear()


def _inside(point, surface, epsilon):
    from mathutils import Vector
    if not surface['closed']:
        return None
    if any(point[i] < surface['low'][i]-epsilon or point[i] > surface['high'][i]+epsilon for i in range(3)):
        return False
    nearest=surface['tree'].find_nearest(point)
    if nearest[0] is not None and nearest[3] <= epsilon:
        return None
    votes=[]
    for direction in ((1,0.371,0.193),(0.217,1,0.419),(0.313,0.173,1)):
        ray=Vector(direction).normalized()
        origin=point.copy()
        count=0
        for _ in range(len(surface['triangles'])+1):
            location,normal,index,distance=surface['tree'].ray_cast(origin,ray)
            if location is None:
                break
            count+=1
            origin=location+ray*epsilon*4
        else:
            return None
        votes.append(bool(count%2))
    return votes[0] if len(set(votes))==1 else None


def diagnose_pairs(pairs, tolerance, max_vertices=10000):
    import bpy
    if not math.isfinite(tolerance) or tolerance < 0 or type(max_vertices) is not int or max_vertices < 1:
        raise ValueError('Nonnegative finite world-space tolerance and positive vertex limit required')
    if not pairs:
        raise ValueError('Explicit nonempty object pairs required')
    allowed={'separated','proximity','surface_intersection','containment','partial_containment','inconclusive'}
    for pair in pairs:
        if set(pair)-{'a','b','expected'} or not all(isinstance(pair.get(k),str) and pair[k] in bpy.data.objects for k in ('a','b')):
            raise ValueError('Each pair names existing a/b objects and optional expected relationships')
        if pair['a']==pair['b'] or not isinstance(pair.get('expected',[]),list) or set(pair.get('expected',[]))-allowed:
            raise ValueError('Distinct objects and known expected relationships required')
    for scene in bpy.data.scenes:
        for layer in scene.view_layers:
            layer.update()
    depsgraph=bpy.context.evaluated_depsgraph_get()
    cache={name:_surface(bpy.data.objects[name],depsgraph) for pair in pairs for name in (pair['a'],pair['b'])}
    results=[]
    for pair in pairs:
        a,b=cache[pair['a']],cache[pair['b']]
        extent=max(max(s['high'][i]-s['low'][i] for i in range(3)) for s in (a,b))
        epsilon=max(1e-8,extent*1e-7)
        overlap=a['tree'].overlap(b['tree'])
        points_a=a['vertices'][:max_vertices]; points_b=b['vertices'][:max_vertices]
        limited=len(points_a)!=len(a['vertices']) or len(points_b)!=len(b['vertices'])
        distances=[target['tree'].find_nearest(p)[3] for source,target in ((points_a,b),(points_b,a)) for p in source]
        proximity=min(d for d in distances if d is not None)
        checks_a=[_inside(p,b,epsilon) for p in points_a] if not overlap else []
        checks_b=[_inside(p,a,epsilon) for p in points_b] if not overlap else []
        if overlap:
            relationship='surface_intersection'
        elif limited or not a['closed'] or not b['closed'] or None in checks_a+checks_b:
            relationship='inconclusive'
        elif all(checks_a) or all(checks_b):
            relationship='containment'
        elif any(checks_a) or any(checks_b):
            relationship='partial_containment'
        else:
            relationship='proximity' if proximity <= tolerance else 'separated'
        expected=pair.get('expected',[])
        verdict='REVIEW REQUIRED' if relationship=='inconclusive' or not expected else ('PASS' if relationship in expected else 'FAIL')
        results.append(dict(**pair,relationship=relationship,status=verdict,surface_triangle_pairs=len(overlap),
                            closed_a=a['closed'],closed_b=b['closed'],sample_limit_reached=limited,
                            sampled_distance_upper_bound=proximity,tolerance=tolerance))
    return dict(pairs=results,limits='Selected current-pose surfaces only; coplanarity/near-boundary cases need review. '
                'Sampled proximity is not a certified global minimum clearance; no motion or global-scene certificate.')
