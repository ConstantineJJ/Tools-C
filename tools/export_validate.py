"""Run source export and fresh import in separate Blender processes, compare bounded semantics."""
import argparse
import json
from pathlib import Path
import sys

from check import read_json
from engine_check import engine_identity, probe, resolve_engine
from glb_inspect import inspect
from handoff_snapshot import validate


POST_EXPORT_KEYS=('markers','weapon_interface','weapon_root')
EXPECTED={'source mesh representation differs':'expected after modifier evaluation, triangulation or split normals',
          'procedural geometry became mesh':'expected: glTF stores curves/text/surfaces as meshes'}


def group_differences(differences, shown=6):
    """Collapse per-object expected differences into one line per kind."""
    groups={}
    for line in differences:
        name,_,kind=line.partition(': ')
        groups.setdefault(kind.split(';')[0],[]).append(name)
    rows=[]
    for kind,names in groups.items():
        listed=', '.join(names[:shown])+(f', +{len(names)-shown} more' if len(names)>shown else '')
        rows.append(dict(kind=kind,count=len(names),objects=listed,note=EXPECTED.get(kind,'review')))
    return rows


def check_markers(glb_path, markers):
    """Required marker nodes must survive export with their exact names."""
    from weapon_module import read_gltf
    if not isinstance(markers,list) or not all(isinstance(m,str) and m for m in markers):
        raise ValueError('markers must be a list of node names')
    present={n.get('name') for n in read_gltf(glb_path).get('nodes',[])}
    return ['Marker missing from GLB: '+m for m in markers if m not in present]


def post_export_checks(job, glb_path, job_dir=None):
    failures=[]; report={}
    if 'markers' in job:
        report['markers']=dict(required=job['markers'],missing=check_markers(glb_path,job['markers']))
        failures+=report['markers']['missing']
    if 'weapon_interface' in job:
        from weapon_module import check_glb, load_interface
        path=Path(job['weapon_interface'])
        if not path.is_absolute() and job_dir is not None: path=Path(job_dir)/path
        weapon=check_glb(load_interface(path),glb_path,job.get('weapon_root'))
        report['weapon_interface']=weapon
        failures+=['Weapon interface: '+i['message'] for i in weapon['items'] if i['status']=='FAIL']
    return failures,report


def compare(source, imported, source_result, imported_result, glb, tolerance=1e-5):
    validate(source); validate(imported)
    failures=[]; differences=[]
    old={o['name']:o for o in source['objects']}; new={o['name']:o for o in imported['objects']}
    if set(old)!=set(new): failures.append('Object identity differs: '+str(sorted(set(old)^set(new))))
    for name in sorted(set(old)&set(new)):
        a,b=old[name],new[name]
        if a['type']!=b['type']:
            if a['type'] in {'CURVE','FONT','SURFACE'} and b['type']=='MESH': differences.append(name+': procedural geometry became mesh')
            else: failures.append(name+': object type differs')
        if a['bones']!=b['bones']: failures.append(name+': bone identity/hierarchy differs')
        if a['materials']!=b['materials']: failures.append(name+': material identities differ')
        if a['parent_bone']!=b['parent_bone']: failures.append(name+': bone attachment differs')
        if a['geometry']!=b['geometry']: differences.append(name+': source mesh representation differs; bounds/other gates checked separately')
    for key in ('min','max'):
        if any(abs(a-b)>tolerance for a,b in zip(source_result['bounds'][key],imported_result['bounds'][key])):
            failures.append('World bounds differ: '+key)
    if source['actions']!=imported['actions']: failures.append('Action names/ranges differ')
    expected_actions={a['name'] for a in source['actions']}
    if {a['name'] for a in glb['animations']} != expected_actions: failures.append('Exported animation inclusion differs')
    expected_materials={m for o in old.values() for m in o['materials']}
    if set(glb['materials'])!=expected_materials: failures.append('Exported material inclusion differs')
    expected_joints=sorted(b['name'] for o in old.values() for b in o['bones'])
    actual_joints=sorted(b for s in glb['skins'] for b in s['joints'])
    if expected_joints!=actual_joints: failures.append('Exported skin joints differ')
    for action in source['actions']:
        matching=[a for a in glb['animations'] if a['name']==action['name']]
        if matching:
            channels=matching[0]['channels']; duration=max(c['end'] for c in channels)-min(c['start'] for c in channels)
            expected=(action['range'][1]-action['range'][0])/source['fps']
            if abs(duration-expected)>tolerance: failures.append(action['name']+': exported duration differs')
    return dict(status='FAIL' if failures else 'STRUCTURAL PASS',failures=failures,
                representation_differences=group_differences(differences),difference_count=len(differences),
                tolerance=tolerance,visual='SKIP',
                semantic_review='REVIEW REQUIRED' if differences else 'Not established by this bounded comparison',
                limits='Static sampled-frame bounds, names/hierarchy/inclusion/duration only; not material shading, rest-matrix/weight equivalence, root-motion policy, arbitrary poses or playback feel')


def run(job,engine,output,job_dir=None):
    if output.exists(): raise ValueError('Output must be a new directory')
    post={k:job[k] for k in POST_EXPORT_KEYS if k in job}
    job={k:v for k,v in job.items() if k not in POST_EXPORT_KEYS}
    output.mkdir(parents=True)
    executable,resolution=resolve_engine('blender',engine)
    if executable is None: raise ValueError(resolution)
    identity=engine_identity('blender',executable,resolution)
    script=Path(__file__).with_name('blender_export_probe.py')
    export=dict(job,mode='export',glb=str(output/'asset.glb'),output=str(output/'source'))
    jobs=[export,dict(mode='import',glb=export['glb'],output=str(output/'import'),frame=job.get('frame',1))]
    rows=[]
    for index,data in enumerate(jobs):
        if index:
            source=read_json(output/'source/snapshot.json'); data['fps']=source['fps']
        file=output/(data['mode']+'-job.json'); file.write_text(json.dumps(data,indent=2),encoding='utf-8')
        cmd=[str(executable),'--background','--factory-startup','--python-exit-code','1','--python',str(script),'--',str(file)]
        result=probe(cmd,'TOOLS_C_EXPORT_PROBE',output/(data['mode']+'.log'),timeout=180)
        rows.append(result)
        if result['status']!='PASS': raise RuntimeError('Probe failed; inspect '+str(output))
    structural=inspect(output/'asset.glb')
    compared=compare(read_json(output/'source/snapshot.json'),read_json(output/'import/snapshot.json'),
                     read_json(output/'source/result.json'),read_json(output/'import/result.json'),structural)
    post_failures,post_report=post_export_checks(post,output/'asset.glb',job_dir)
    if post_failures:
        compared['failures']+=post_failures; compared['status']='FAIL'
    report=dict(engine=identity,probes=rows,glb=structural,comparison=compared,interface=post_report)
    (output/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('job',type=Path)
    p.add_argument('--blender',required=True); p.add_argument('--output',required=True,type=Path)
    args=p.parse_args()
    try:
        report=run(read_json(args.job),args.blender,args.output.resolve(),args.job.resolve().parent)
        print(json.dumps(report,indent=2)); raise SystemExit(1 if report['comparison']['status']=='FAIL' else 0)
    except Exception as exc:
        print(json.dumps(dict(status='FAIL',reason=str(exc)))); raise SystemExit(1)
