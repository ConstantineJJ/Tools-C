"""Canonical, provider-neutral routing/context helpers for the integration adapter."""
import hashlib
import json
from pathlib import Path
import re

from check import catalog, read_json
from read_blender_skill import render


def resolve_root(project):
    import os
    config=read_json(Path(project)/'.tooling/config.json')
    value=os.environ.get('TOOLS_C_ROOT') or config['tools_root']
    root=Path(value)
    if not root.is_absolute(): root=Path(project)/root
    root=root.resolve(strict=True)
    catalog(root)
    return root


def route_task(task):
    query=task.strip().lower()
    explicit=re.findall(r'\b(?:blender-(?:rigging-skinning|animation|export-validation|character-modeling|architecture-environment|environment-assets|roads-infrastructure)|godot-asset-integration)\b',query)
    if explicit: return list(dict.fromkeys(explicit))
    # Conservative assistance, not an authorization classifier. Bare character/mesh/rig
    # mentions do not grant modeling or rig-edit ownership.
    routes=[]
    if re.search(r'export|round.trip|glb|gltf|экспорт',query): routes.append('blender-export-validation')
    if re.search(r'godot|годот',query): routes.append('godot-asset-integration')
    if re.search(r'weight|skinning|rebind|rigging|вес[аоы]?\b|привяз|скиннинг|(?:create|repair|edit|fix|build) (?:the |an? )?(?:rig|armature|skeleton)|(?:созда|исправ|поправ).*скелет',query): routes.append('blender-rigging-skinning')
    motion_query=re.split(r'\b(?:preserve|keep|without|unchanged)\b',query)[0]
    if re.search(r'(?:add|create|edit|fix|author|correct|bake).*\b(?:action|animation|clip|motion)|(?:добав|созда|исправ|запек).*анимац|loop|root motion|цикл',motion_query): routes.append('blender-animation')
    if re.search(r'\b(?:building|buildings|house|houses|architecture|architectural|facade|façade|roof|modular\s+(?:building|architecture|kit|wall)|wall\s+module|floor\s+module|building\s+blockout)\b|здани|постройк|архитект|фасад|кры[шш]|модульн.*(?:здани|дом|стен)',query): routes.append('blender-architecture-environment')
    if re.search(r'\b(?:environment\s+asset|street\s+furniture|site\s+fixture|bench|street\s*lamp|lamp\s*post|bollard|hydrant|litter\s*bin|trash\s*bin|bike\s*rack|planter|fence\s+panel|railing\s+panel|traffic\s+barrier)\b|скамейк|уличн.*фонар|фонарн.*столб|урн(?:а|ы|у|ой)?\b|боллард|гидрант|велопарков|заборн.*секц|секц.*забор|огражд.*секц',query): routes.append('blender-environment-assets')
    if re.search(r'\b(?:road|roads|street\s+surface|sidewalk|pavement|curb|kerb|gutter|median|crosswalk|pedestrian\s+crossing|path|trail|road\s+shoulder|intersection|roundabout|ramp|roadway|lane\s+network)\b|дорог|тротуар|бордюр|поребрик|обочин|пешеходн.*переход|переход.*дорог|перекр[её]ст|тропин|дорожк|медиан|разделительн.*полос|съезд|рамп',query): routes.append('blender-roads-infrastructure')
    if re.search(r'(?:character|humanoid|fighter|person|персонаж|гуманоид|боец).*?(?:blockout|remodel|proportion|silhouette|geometry|mesh|блокаут|пропорц|силуэт|геометр|меш)|(?:blockout|remodel|proportion|silhouette|блокаут|пропорц|силуэт).*?(?:character|humanoid|fighter|person|персонаж|гуманоид|боец)',query): routes.append('blender-character-modeling')
    if not routes:
        if re.search(r'review|diagnos|deform|looks wrong|проверь|деформац',query): return ['verification']
        return ['blender-pipeline']
    return list(dict.fromkeys(routes))


def context(root, task, max_chars=50000):
    requested=route_task(task)
    loaded=[]; remaining=max(1,min(int(max_chars),200000))
    for name in requested:
        content=render(root,name)
        clipped=content[:remaining]; remaining=max(0,remaining-len(clipped))
        loaded.append(dict(name=name,ok=len(clipped)==len(content),canonical_root=str(root),content=clipped,
                           truncated=len(clipped)<len(content),sha256=hashlib.sha256(content.encode()).hexdigest()))
    return dict(ok=all(s['ok'] for s in loaded),task=task,skills=loaded,
                routing=dict(owners=requested,limits='Routing suggestions; inspect actual ownership before edits'),
                error=None if all(s['ok'] for s in loaded) else 'Context truncated; increase max_chars or request one canonical owner')


def fingerprints(root):
    manifest=catalog(root)
    contexts={alias:hashlib.sha256(render(root,alias).encode()).hexdigest() for alias in manifest['blender_aliases']}
    return dict(architecture=manifest['version'],canonical_root=str(root),contexts=contexts,
                context_digest=hashlib.sha256(json.dumps(contexts,sort_keys=True).encode()).hexdigest())
