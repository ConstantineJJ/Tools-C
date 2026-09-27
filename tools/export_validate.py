"""Run source export and fresh import in separate Blender processes, compare bounded semantics."""
import argparse
import json
from pathlib import Path
import sys

from check import read_json
from engine_check import engine_identity, probe, resolve_engine
from glb_inspect import inspect
from handoff_snapshot import validate


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
                representation_differences=differences,tolerance=tolerance,visual='SKIP',
                semantic_review='REVIEW REQUIRED' if differences else 'Not established by this bounded comparison',
                limits='Static sampled-frame bounds, names/hierarchy/inclusion/duration only; not material shading, rest-matrix/weight equivalence, root-motion policy, arbitrary poses or playback feel')


def run(job,engine,output):
    if output.exists(): raise ValueError('Output must be a new directory')
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
    report=dict(engine=identity,probes=rows,glb=structural,comparison=compared)
    (output/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('job',type=Path)
    p.add_argument('--blender',required=True); p.add_argument('--output',required=True,type=Path)
    args=p.parse_args()
    try:
        report=run(read_json(args.job),args.blender,args.output.resolve())
        print(json.dumps(report,indent=2)); raise SystemExit(1 if report['comparison']['status']=='FAIL' else 0)
    except Exception as exc:
        print(json.dumps(dict(status='FAIL',reason=str(exc)))); raise SystemExit(1)
