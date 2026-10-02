"""Canonical, provider-neutral routing/context helpers for the integration adapter."""
import hashlib
import json
from pathlib import Path
import re

from check import catalog, read_json, existing
from read_blender_skill import render


PROCEDURES = {
    'retopology': 'skills/blender-pipeline/references/retopology.md',
    'surfaces': 'skills/blender-pipeline/references/surfaces.md',
}


def render_context(root, owner, procedures=()):
    # Keep the reader's two-argument API: a live adapter may cache that module.
    content=render(root,owner)
    paths=[]
    for procedure in procedures:
        if procedure not in PROCEDURES:
            raise ValueError(f'Unknown Blender procedure: {procedure}')
        paths.append(PROCEDURES[procedure])
        if procedure == 'retopology':
            paths.append('skills/blender-pipeline/references/techniques/deformation-checks.md')
    return content+''.join(f"\n\nSOURCE: {path}\n\n{existing(root,path).read_text(encoding='utf-8')}"
                           for path in dict.fromkeys(paths))


def resolve_root(project):
    import os
    config=read_json(Path(project)/'.tooling/config.json')
    value=os.environ.get('TOOLS_C_ROOT') or config['tools_root']
    root=Path(value)
    if not root.is_absolute(): root=Path(project)/root
    root=root.resolve(strict=True)
    catalog(root)
    return root


def action_query(task):
    """Bounded clause filtering for suggestions, never an authorization decision."""
    return re.sub(
        r'(?:\b(?:preserve|preserving|keeping|keep(?!\s+(?:sculpting|modeling|working)\b)|without|no|do\s+not)\b|'
        r'(?:сохрани(?:ть)?|не\s+меняя|без|не\s+(?:делай|используй|меняй|трогай)))'
        r'[^.;\n]*?(?=[.;\n]|\b(?:but|then)\b|\band\s+(?:create|repair|edit|fix|build|rebind|model|sculpt|unwrap|bake|export|review)\b|'
        r'\b(?:а|но|затем|потом)\b|\bи\s+(?:созда|сдела|исправ|поправ|перепривяз|развер|запек|экспорт)|$)',
        '', task.strip().lower())


def procedure_routes(query):
    procedures=[]
    if re.search(r'\b(?:retopolog(?:y|ize|ise|izing|ising)|retopo)\b|ретополог|(?:repair|fix|rebuild|edit).*\b(?:edge\s+flow|mesh\s+topology)\b',query):
        procedures.append('retopology')
    if re.search(r'\b(?:unwrap|uvs?|textur(?:e|es|ing)|pbr|materials?)\b|\bbak(?:e|ing)\b[^.;\n]*(?:normal|ao|map|texture)|разв[её]рт|материал|текстур|запек.*(?:нормал|карт)',query):
        procedures.append('surfaces')
    return procedures


def route_task(task):
    query=task.strip().lower()
    explicit=re.findall(r'\b(?:blender-(?:rigging-skinning|animation|export-validation|character-modeling|architecture-environment|environment-assets|roads-infrastructure|props|vehicle-modeling|product-electronics-modeling|vegetation|sculpting)|godot-asset-integration)\b',query)
    if explicit: return list(dict.fromkeys(explicit))
    query=action_query(query)
    reviewing=bool(re.search(r'\b(?:review|inspect|audit|diagnose)\b|проверь|проверить|осмотр',query))
    if reviewing and not re.search(r'\b(?:create|build|model|remodel|fix|repair|edit|sculpt|unwrap|bake|export|retopologize)\b|созда|сдела|смодел|исправ|поправ|запек|экспорт|ретополог',query):
        return ['verification']
    # Conservative assistance, not an authorization classifier. Bare character/mesh/rig
    # mentions do not grant modeling or rig-edit ownership.
    procedures=procedure_routes(query)
    routes=['verification'] if reviewing else []
    if procedures: routes.append('blender-pipeline')
    if re.search(r'export|round.trip|glb|gltf|экспорт',query): routes.append('blender-export-validation')
    if re.search(r'godot|годот',query): routes.append('godot-asset-integration')
    if re.search(r'weight|skinning|rebind|rigging|вес[аоы]?\b|привяз|скиннинг|(?:create|repair|edit|fix|build) (?:the |an? )?(?:rig|armature|skeleton)|(?:созда|исправ|поправ).*скелет',query): routes.append('blender-rigging-skinning')
    if re.search(r'(?:add|create|edit|fix|author|correct|bake).*\b(?:action|animation|clip|motion)|(?:добав|созда|исправ|запек).*анимац|loop|root motion|цикл',query): routes.append('blender-animation')
    # A stage-only request loads its existing procedure; asset nouns are context.
    # Explicit geometry creation may co-route with a requested UV/retopo stage.
    if procedures and not re.search(
        r'\b(?:create|build|model|remodel)\s+(?!(?:(?:an?|the)\s+)?(?:retopo|uv|material|texture|normal\s+map|bake))|'
        r'(?:созда|сдела|смодел|постро)\w*\s+(?!(?:ретополог|uv|материал|текстур|разв[её]ртк))',query):
        return list(dict.fromkeys(routes))
    if re.search(r'\b(?:building|buildings|house|houses|architecture|architectural|facade|façade|roof|modular\s+(?:building|architecture|kit|wall)|wall\s+module|floor\s+module|building\s+blockout)\b|здани|постройк|архитект|фасад|крыш(?:а|и|у|ей|е)\b|модульн.*(?:здани|дом|стен)',query): routes.append('blender-architecture-environment')
    if re.search(r'\b(?:environment\s+assets?|street\s+furniture|site\s+fixtures?|bench(?:es)?|street\s*lamps?|lamp\s*posts?|bollards?|hydrants?|litter\s*bins?|trash\s*bins?|bike\s*racks?|planters?|fence\s+panels?|railing\s+panels?|traffic\s+barriers?|road\s+signs?|street\s+signs?|standalone\s+signs?)\b|скамейк|уличн.*фонар|фонарн.*столб|урн(?:а|ы|у|ой)?\b|боллард|гидрант|велопарков|заборн.*секц|секц.*забор|огражд.*секц',query): routes.append('blender-environment-assets')
    if re.search(r'\b(?:road|roads|street\s+surface|sidewalks?|pavements?|curbs?|kerbs?|gutters?|medians?|crosswalks?|pedestrian\s+crossing|paths?|trails?|road\s+shoulders?|intersections?|roundabouts?|ramps?|roadways?|lane\s+network)\b|дорог|тротуар|бордюр|поребрик|обочин|пешеходн.*переход|переход.*дорог|перекр[её]ст|тропин|дорожк|медиан|разделительн.*полос|съезд|рамп',query): routes.append('blender-roads-infrastructure')
    if re.search(r'\b(?:prop|props|furniture|(?:dining\s+|office\s+)?chairs?|stools?|tables?|shel(?:f|ves)|shelving|cabinets?|crates?|toolbox(?:es)?|tool\s+prop|wrench|hammer|bottle|book|clutter|decor|hand[- ]?held\s+(?:object|prop)|interior\s+prop|set[- ]?dressing\s+prop)\b|мебел|стул|табурет|стол(?:ик|а|у|ом)?\b|полк(?:а|и|у|ой)?\b|шкаф|ящик|инструмент|молоток|гаечн.*ключ|бутылк|книг|декор|интерьерн.*проп|ручн.*предмет|мелк.*проп',query): routes.append('blender-props')
    if re.search(r'\b(?:car|cars|vehicle|vehicles|truck|trucks|van|vans|bus|buses|motorcycles?|motorbikes?|scooters?|trailers?|bicycles?|bikes?|carts?|wheelbase|wheel\s+arch|vehicle\s+wheel|vehicle\s+tire|vehicle\s+tyre)\b|автомоб|грузовик|фургон|автобус|мотоцикл|скутер|прицеп|кол[её]сн.*(?:техник|транспорт|машин)',query): routes.append('blender-vehicle-modeling')
    if re.search(r'\b(?:consumer\s+electronics?|electronic\s+device|appliance|microwave|kettle|coffee\s+machine|vacuum\s+cleaner|computer|desktop\s+pc|monitor|television|\btv\b|game\s+console|console\s+device|router|keyboard|gamepad|controller|radio\s+device|speaker\s+device|camera\s+device|digital\s+device|product\s+device)\b|бытов.*техник|электрон.*устройств|цифров.*техник|компьютер|монитор|телевизор|приставк|микроволнов|чайник|кофемашин|пылесос|роутер|клавиатур|геймпад|контроллер|радиопри[её]м|колонк.*(?:аудио|электрон)',query): routes.append('blender-product-electronics-modeling')
    if re.search(r'\bradios?\b',query) and re.search(r'\b(?:ports?|controls?|enclosure|connectors?|vents?)\b',query):
        routes.append('blender-product-electronics-modeling')
    if re.search(r'\b(?:vegetation|foliage|tree|trees|sapling|saplings|shrub|shrubs|bush|bushes|grass|grasses|flower|flowers|vine|vines|reed|reeds|leaf\s+cluster|foliage\s+cluster|grass\s+patch|plants|potted\s+plant|plant\s+(?:asset|model|cluster|family))\b|растительн|дерев(?:о|ья|ьев|ьями)|сажен|куст|трав(?:а|ы|у|ой)|цвет(?:ок|ы|ов|ами)|листв|лоз(?:а|ы|у|ой)|камыш|тростник',query): routes.append('blender-vegetation')
    if re.search(r'\b(?:sculpt|sculpting|sculpted|dyntopo|dynamic\s+topology|voxel\s+remesh|multires(?:olution)?|face\s+sets?|sculpt\s+mask|clay\s+brush|crease\s+brush)\b|скульпт|скульптинг|динтопо|динамич.*тополог|воксельн.*ремеш|мультирез|мультирес',query): routes.append('blender-sculpting')
    if re.search(r'(?:character|humanoid|fighter|person|персонаж|гуманоид|боец).*?(?:blockout|remodel|proportion|silhouette|geometry|mesh|блокаут|пропорц|силуэт|геометр|меш)|(?:blockout|remodel|proportion|silhouette|блокаут|пропорц|силуэт).*?(?:character|humanoid|fighter|person|персонаж|гуманоид|боец)',query): routes.append('blender-character-modeling')
    if not routes:
        if re.search(r'review|diagnos|deform|looks wrong|проверь|деформац',query): return ['verification']
        return ['blender-pipeline']
    return list(dict.fromkeys(routes))


def context(root, task, max_chars=50000):
    requested=route_task(task)
    procedures=procedure_routes(action_query(task)) if 'blender-pipeline' in requested else []
    loaded=[]; remaining=max(1,min(int(max_chars),200000))
    for name in requested:
        content=render_context(root,name,procedures if name == 'blender-pipeline' else ())
        clipped=content[:remaining]; remaining=max(0,remaining-len(clipped))
        loaded.append(dict(name=name,ok=len(clipped)==len(content),canonical_root=str(root),content=clipped,
                           truncated=len(clipped)<len(content),sha256=hashlib.sha256(content.encode()).hexdigest()))
    return dict(ok=all(s['ok'] for s in loaded),task=task,skills=loaded,
                routing=dict(owners=requested,procedures=procedures,limits='Routing suggestions; inspect actual ownership before edits'),
                error=None if all(s['ok'] for s in loaded) else 'Context truncated; increase max_chars or request one canonical owner')


def fingerprints(root):
    manifest=catalog(root)
    contexts={alias:hashlib.sha256(render(root,alias).encode()).hexdigest() for alias in manifest['blender_aliases']}
    return dict(architecture=manifest['version'],canonical_root=str(root),contexts=contexts,
                context_digest=hashlib.sha256(json.dumps(contexts,sort_keys=True).encode()).hexdigest())
