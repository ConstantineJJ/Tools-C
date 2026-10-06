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
    form='skills/blender-pipeline/references/techniques/form-development.md'
    if owner in {'blender-character-modeling','blender-anime-character-modeling',
                 'blender-architecture-environment','blender-environment-assets',
                 'blender-props','blender-vegetation','blender-robot-mechanism-modeling'} and f'SOURCE: {form}\n\n' not in content:
        paths.append(form)
    pass0='skills/visual-reference-reconstruction/SKILL.md'
    if owner in {'blender-robot-mechanism-modeling','Blender_Reference_Reconstruction_SKILL'} and f'SOURCE: {pass0}\n\n' not in content:
        paths.append(pass0)
    contract='skills/visual-reference-reconstruction/references/model-contract.md'
    if owner in {'visual-reference-reconstruction','blender-robot-mechanism-modeling','Blender_Reference_Reconstruction_SKILL'} and f'SOURCE: {contract}\n\n' not in content:
        paths.append(contract)
    if owner == 'blender-reference-surface-transfer':
        for path in ['skills/blender-reference-surface-transfer/references/workflow.md',
                     'skills/blender-reference-surface-transfer/references/record.md',
                     'skills/blender-pipeline/references/surfaces.md']:
            if f'SOURCE: {path}\n\n' not in content:
                paths.append(path)
    finishing='skills/blender-posteffects-polishing/references/finishing-techniques.md'
    if owner == 'blender-posteffects-polishing' and f'SOURCE: {finishing}\n\n' not in content:
        # A live adapter can retain the earlier two-argument reader module.
        paths.append(finishing)
    if owner == "blender-anime-character-modeling":
        for path in ["skills/blender-character-modeling/SKILL.md",
                     "skills/blender-anime-character-modeling/references/face-hair-workflow.md"]:
            if f"SOURCE: {path}\n\n" not in content:
                paths.append(path)
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
        r'[^.;\n]*?(?=[.;\n]|\b(?:but|then)\b|\band\s+(?:create|repair|edit|fix|build|rebind|model|sculpt|unwrap|bake|export|review|add|polish|refine|improve|transfer|project|extract|crop)\b|'
        r'\b(?:а|но|затем|потом)\b|\bи\s+(?:созда|сдела|исправ|поправ|перепривяз|развер|запек|экспорт|добав|улучш|перенес|спроецир|выреж)|$)',
        '', task.strip().lower())


def polishing_route(query):
    """Late finishing intent; sculpted damage remains with the shape owner."""
    # Explicit later finishing remains a separate stage in mixed sculpt requests.
    clauses = re.split(r'[.;\n]|\b(?:then|and\s+(?:add|polish|refine))\b|\b(?:затем|потом|и\s+(?:добав\w*|улучш\w*))\b', query)
    if len(clauses) > 1:
        return any(polishing_route(clause) for clause in clauses if clause.strip())
    if surface_transfer_route(query):
        return False
    named = re.search(r'\bpost[- ]?effects?\b|\bpolishing\b|постэффект|финишн\w*\s+(?:отделк|доработ|материал)|финальн\w*\s+(?:отделк|материал)', query)
    finish = re.search(r'\b(?:weathering|grime|dirt|scuffs?|scratches?|chipped\s+paint|peeling\s+paint|rust|emission|emissive|glow|bloom)\b|гряз|пот[её]ртост|царапин|шелуш|облез|ржавчин|свечени|эмисси', query)
    surface = re.search(r'\b(?:surface\s+cracks?|texture\w*\s+cracks?|material\s+refinement|(?:refine|improve)\s+(?:(?:the|existing)\s+)*(?:materials?|textures?))\b|\bpolish\b[^.;\n]*\b(?:materials?|textures?|surface|finish)\b|поверхностн\w*\s+трещин|улучш\w*\s+(?:материал|текстур)', query)
    sculpt = re.search(r'\b(?:sculpt|sculpting|sculpted|dyntopo|voxel\s+remesh|multires)\b|скульпт|ремеш|динтопо|мультирез', query)
    return bool(named or ((surface or finish) and not sculpt))


def surface_transfer_route(query):
    """Source artwork reuse intent; asset nouns alone do not start geometry."""
    if re.search(r'\breference\s+surface\s+transfer\b|перенос\w*\s+(?:рисунк|график)\w*\s+с\s+референс', query):
        return True
    source = re.search(r'\b(?:reference|source|photo|photograph|image|crop)\b|референс|исходн|фото|изображени', query)
    action = re.search(r'\b(?:transfer|project|reuse|extract|crop|decal)\b|перенес|перенос|спроецир|выреж|вырез|извле', query)
    graphic = re.search(r'\b(?:face|eyes?|iris|logos?|markings?|prints?|tattoos?|panels?|scales?|graffiti|wear|patterns?|artwork|graphics?|textures?|decals?)\b|лиц|глаз|радужк|логотип|маркировк|принт|тату|панел|шкал|граффити|пот[её]ртост|узор|рисунк|рисунок|график|текстур|декал', query)
    return bool(source and action and graphic)


def procedure_routes(query):
    procedures=[]
    if re.search(r'\b(?:retopolog(?:y|ize|ise|izing|ising)|retopo)\b|ретополог|(?:repair|fix|rebuild|edit).*\b(?:edge\s+flow|mesh\s+topology)\b',query):
        procedures.append('retopology')
    foundation = re.search(r'\b(?:unwrap|uvs?)\b|\bbak(?:e|ing)\b[^.;\n]*(?:normal|ao|map|texture)|разв[её]рт|запек.*(?:нормал|карт)', query)
    material = re.search(r'\b(?:textur(?:e|es|ing)|pbr|materials?)\b|материал|текстур', query)
    if foundation or (material and not polishing_route(query) and not surface_transfer_route(query)):
        procedures.append('surfaces')
    return procedures


def anime_modeling_route(query):
    """Style-specific geometry intent; existing asset style does not own other stages."""
    if not re.search(r'\b(?:anime|manga)\b|аниме|манга|кошко(?:девуш|тян)|котодевуш', query):
        return False
    create = re.search(
        r'\b(?:create|build|make|model|remodel)\s+'
        r'(?:(?:an?|the|new|full-body|chibi|anime|manga|stylized|male|female|human)\s+)*'
        r'(?:character|humanoid|avatar|person|head|face|body|hair|hairstyle)\b|'
        r'(?:созда|сдела|смодел|передел)\w*\s+'
        r'(?:(?:нов\w*|аниме|манга|чиби|стилизованн\w*)\s+)*'
        r'(?:персонаж|гуманоид|аватар|голов|лиц|прич[её]ск|волос|кошкодевуш|кошкотян|котодевуш)\w*', query)
    # A scene-creation verb can govern an asset list after a colon or conjunction.
    # Stage-only/read-only requests return before domain routing; preserve clauses
    # have already been removed. Mere style or character mentions still do not edit.
    scene_creation = re.search(r'(?:созда|сдела|смодел|постро)\w*[^.;\n]*(?:диорам|сцен\w*\s*:)[^.;\n]*(?:аниме|кошкодевуш|кошкотян|котодевуш)', query)
    revise = re.search(
        r'\b(?:remodel|blockout)\b|'
        r'\b(?:adjust|change|fix|repair|edit|refine|improve)\s+'
        r'(?:(?:the|this|an?|existing|anime|manga|character|humanoid)\s+)*'
        r"(?:head|face|body|hair|hairstyle|proportions?|silhouette|geometry)\b|"
        r'(?:исправ|измени|поправ|передел|улучш)\w*\s+'
        r'(?:(?:аниме|манга|текущ\w*|эт\w*)\s+)*'
        r'(?:пропорц|силуэт|геометр|лиц|голов|волос|прич[её]ск)\w*|блокаут|'
        r'(?:сглад|смягч|довед)\w*\s+(?:основн\w*\s+)?(?:форм|геометр|силуэт)\w*', query)
    return bool(create or revise or scene_creation)


def primary_geometry_revision(query):
    return bool(re.search(
        r'\b(?:revise|change|fix|repair|edit|refine|improve|remodel|rebuild)\s+'
        r'(?:(?:the|this|existing|robot|mech|character|primary|body|major)\s+)*'
        r'(?:geometry|silhouette|proportions?|construction|joint\s+axes|armor\s+shape)\b|'
        r'(?:исправ|измени|поправ|улучш|передел|перестро)\w*\s+'
        r'(?:(?:основн\w*|текущ\w*|эт\w*|робот\w*|мех\w*)\s+)*'
        r'(?:геометр|силуэт|пропорц|конструкц|оси\s+шарнир)', query))


def geometry_intent(query):
    """Creation or explicit primary-shape revision, not surface finishing."""
    return bool(re.search(
        r'\b(?:create|build|make|model|remodel|rebuild|blockout)\b|'
        r'(?:созда|сдела|смодел|постро|перестро|передел)\w*|блокаут', query) or primary_geometry_revision(query))


def robot_modeling_route(query):
    domain = re.search(r'\b(?:robots?|mechs?|manipulators?|robotic\s+arms?|articulated\s+mechanisms?)\b|'
                       r'робот|\bмех(?:а|и|ов|у|ом)?\b|манипулятор|сочлен[её]нн\w*\s+механизм', query)
    create = re.search(
        r'\b(?:create|build|make|model|remodel|rebuild)\s+'
        r'(?:(?:an?|the|existing|new|hard-surface|humanoid|biped|articulated|mechanical|light|reconnaissance|scout|spherical|long-legged)\s+)*'
        r'(?:robots?|mechs?|manipulators?|robotic\s+arms?|articulated\s+mechanisms?)\b|'
        r'(?:созда|сдела|смодел|постро|передел|перестро)\w*\s+'
        r'(?:(?:модель|[а-яё]+(?:ого|ую|ый|ий|ой|ые|ое|ных|ный|кого))\s+)*'
        r'(?:робот|мех\w*|манипулятор|механизм)', query)
    return bool(domain and (create or primary_geometry_revision(query) or re.search(r'\bblockout\b|блокаут',query)))


def _route_task(task):
    query=task.strip().lower()
    explicit=re.findall(r'\b(?:visual-reference-reconstruction|blender-(?:reference-surface-transfer|robot-mechanism-modeling|anime-character-modeling|posteffects-polishing|rigging-skinning|animation|export-validation|character-modeling|architecture-environment|environment-assets|roads-infrastructure|props|vehicle-modeling|product-electronics-modeling|vegetation|sculpting)|godot-asset-integration)\b',query)
    if explicit: return list(dict.fromkeys(explicit))
    query=action_query(query)
    reviewing=bool(re.search(r'\b(?:review|inspect|audit|diagnose)\b|проверь|проверить|осмотр',query))
    if reviewing and not re.search(r'\b(?:create|build|model|remodel|fix|repair|edit|sculpt|unwrap|bake|export|retopologize|add|polish|refine|improve)\b|(?:^|[.;\n]|\bthen\b|\band\b)\s*(?:transfer|project|crop|extract)\b|созда|сдела|смодел|исправ|поправ|запек|экспорт|ретополог|добав|улучш|перенес|спроецир|выреж',query):
        return ['verification']
    # Conservative assistance, not an authorization classifier. Bare character/mesh/rig
    # mentions do not grant modeling or rig-edit ownership.
    procedures=procedure_routes(query)
    polishing=polishing_route(query)
    transfer=surface_transfer_route(query)
    routes=['verification'] if reviewing else []
    if transfer: routes.append('blender-reference-surface-transfer')
    if procedures: routes.append('blender-pipeline')
    if polishing: routes.append('blender-posteffects-polishing')
    if re.search(r'export|round.trip|glb|gltf|экспорт',query): routes.append('blender-export-validation')
    if re.search(r'godot|годот',query): routes.append('godot-asset-integration')
    if re.search(r'weight|skinning|rebind|rigging|вес[аоы]?\b|привяз|скиннинг|(?:create|repair|edit|fix|build) (?:the |an? )?(?:rig|armature|skeleton)|(?:созда|исправ|поправ|постро)\w*\s+(?:(?:нов\w*|эт\w*|текущ\w*)\s+)*(?:rig\b|риг\w*|арматур\w*|скелет\w*)',query): routes.append('blender-rigging-skinning')
    if re.search(r'(?:add|create|edit|fix|author|correct|bake).*\b(?:action|animation|clip|motion)|\banimate\b|анимиру|(?:добав|созда|исправ|запек).*анимац|loop|root motion|цикл',query): routes.append('blender-animation')
    if polishing and re.search(r'\b(?:sculpt|sculpting|sculpted|dyntopo|voxel\s+remesh|multires)\b|скульпт|ремеш|динтопо|мультирез', query):
        routes.append('blender-sculpting')
    # A stage-only request loads its existing procedure; asset nouns are context.
    # Explicit geometry creation may co-route with a requested UV/retopo stage.
    primary_revision = primary_geometry_revision(query)
    if (procedures or polishing or transfer) and not primary_revision and not re.search(
        r'\b(?:create|build|model|remodel)\s+(?!(?:(?:an?|the)\s+)?(?:retopo|uv|material|texture|normal\s+map|bake|glow|emission|dirt|weathering|surface\s+crack|decal|logo|graphic|pattern|reference\s+surface\s+transfer))|'
        r'(?:созда|сдела|смодел|постро)\w*\s+(?!(?:ретополог|uv|материал|текстур|разв[её]ртк|свечени|гряз|пот[её]ртост|декал|логотип|перенос))',query):
        return list(dict.fromkeys(routes))
    if re.search(r'\b(?:building|buildings|house|houses|architecture|architectural|facade|façade|roof|modular\s+(?:building|architecture|kit|wall)|wall\s+module|floor\s+module|building\s+blockout)\b|здани|\bдом(?:ик\w*|а|у|ом|е)?\b|постройк|архитект|фасад|крыш(?:а|и|у|ей|е)\b|модульн.*(?:здани|дом|стен)',query): routes.append('blender-architecture-environment')
    if re.search(r'\b(?:environment\s+assets?|street\s+furniture|site\s+fixtures?|bench(?:es)?|street\s*lamps?|lamp\s*posts?|bollards?|hydrants?|litter\s*bins?|trash\s*bins?|bike\s*racks?|planters?|fence\s+panels?|railing\s+panels?|traffic\s+barriers?|road\s+signs?|street\s+signs?|standalone\s+signs?)\b|скамейк|скамь|\bзабор\w*|уличн.*фонар|фонарн.*столб|урн(?:а|ы|у|ой)?\b|боллард|гидрант|велопарков|заборн.*секц|секц.*забор|огражд.*секц',query): routes.append('blender-environment-assets')
    if re.search(r'\b(?:road|roads|street\s+surface|sidewalks?|pavements?|curbs?|kerbs?|gutters?|medians?|crosswalks?|pedestrian\s+crossing|paths?|trails?|road\s+shoulders?|intersections?|roundabouts?|ramps?|roadways?|lane\s+network)\b|дорог|тротуар|бордюр|поребрик|обочин|пешеходн.*переход|переход.*дорог|перекр[её]ст|тропин|дорожк|медиан|разделительн.*полос|съезд|рамп',query): routes.append('blender-roads-infrastructure')
    if re.search(r'\b(?:prop|props|furniture|(?:dining\s+|office\s+)?chairs?|stools?|tables?|shel(?:f|ves)|shelving|cabinets?|crates?|toolbox(?:es)?|tool\s+prop|wrench|hammer|bottle|book|clutter|decor|hand[- ]?held\s+(?:object|prop)|interior\s+prop|set[- ]?dressing\s+prop)\b|реквизит|мебел|стул|табурет|стол(?:ик|а|у|ом)?\b|полк(?:а|и|у|ой)?\b|шкаф|ящик|инструмент|молоток|гаечн.*ключ|бутылк|книг|декор|интерьерн.*проп|ручн.*предмет|мелк.*проп',query): routes.append('blender-props')
    if re.search(r'\b(?:car|cars|vehicle|vehicles|truck|trucks|van|vans|bus|buses|motorcycles?|motorbikes?|scooters?|trailers?|bicycles?|bikes?|carts?|wheelbase|wheel\s+arch|vehicle\s+wheel|vehicle\s+tire|vehicle\s+tyre)\b|автомоб|грузовик|фургон|автобус|мотоцикл|скутер|прицеп|кол[её]сн.*(?:техник|транспорт|машин)',query): routes.append('blender-vehicle-modeling')
    if re.search(r'\b(?:consumer\s+electronics?|electronic\s+device|appliance|microwave|kettle|coffee\s+machine|vacuum\s+cleaner|computer|desktop\s+pc|monitor|television|\btv\b|game\s+console|console\s+device|router|keyboard|gamepad|controller|radio\s+device|speaker\s+device|camera\s+device|digital\s+device|product\s+device)\b|бытов.*техник|электрон.*устройств|цифров.*техник|компьютер|монитор|телевизор|приставк|микроволнов|чайник|кофемашин|пылесос|роутер|клавиатур|геймпад|контроллер|радиопри[её]м|колонк.*(?:аудио|электрон)',query): routes.append('blender-product-electronics-modeling')
    if re.search(r'\bradios?\b',query) and re.search(r'\b(?:ports?|controls?|enclosure|connectors?|vents?)\b',query):
        routes.append('blender-product-electronics-modeling')
    if re.search(r'\b(?:vegetation|foliage|tree|trees|sapling|saplings|shrub|shrubs|bush|bushes|grass|grasses|flower|flowers|vine|vines|reed|reeds|leaf\s+cluster|foliage\s+cluster|grass\s+patch|plants|potted\s+plant|plant\s+(?:asset|model|cluster|family))\b|растительн|дерев(?:о|ья|ьев|ьями)|сажен|куст|трав(?:а|ы|у|ой)|цвет(?:ок|ы|ов|ами)|листв|лоз(?:а|ы|у|ой)|камыш|тростник',query): routes.append('blender-vegetation')
    if re.search(r'\b(?:sculpt|sculpting|sculpted|dyntopo|dynamic\s+topology|voxel\s+remesh|multires(?:olution)?|face\s+sets?|sculpt\s+mask|clay\s+brush|crease\s+brush)\b|скульпт|скульптинг|динтопо|динамич.*тополог|воксельн.*ремеш|мультирез|мультирес',query): routes.append('blender-sculpting')
    anime = anime_modeling_route(query)
    if anime: routes.append("blender-anime-character-modeling")
    robot = robot_modeling_route(query)
    if robot: routes.append('blender-robot-mechanism-modeling')
    if not anime and not robot and re.search(r'(?:character|humanoid|fighter|person|персонаж|гуманоид|боец).*?(?:blockout|remodel|proportion|silhouette|geometry|mesh|блокаут|пропорц|силуэт|геометр|меш)|(?:blockout|remodel|proportion|silhouette|блокаут|пропорц|силуэт).*?(?:character|humanoid|fighter|person|персонаж|гуманоид|боец)',query): routes.append('blender-character-modeling')
    if not routes:
        if re.search(r'review|diagnos|deform|looks wrong|проверь|деформац',query): return ['verification']
        return ['blender-pipeline']
    return list(dict.fromkeys(routes))


def route_task(task):
    """PASS 0 precedes visual/text design; actual artifacts determine input mode."""
    query = action_query(task)
    visual = bool(re.search(r'\b(?:images?|references?|blueprints?|photos?|multiview|multi-view)\b|'
                            r'референс|изображени|картинк|черт[её]ж|фотограф', query))
    analysis = bool(re.search(r'\b(?:analy[sz]e|reconstruct|technical\s+reference\s+pack|pass\s*0)\b|'
                              r'проанализ|разбер\w*\s+референс|восстанов\w*\s+вид|пакет\s+референс', query))
    if visual and analysis and not geometry_intent(query) and not surface_transfer_route(query):
        return ['visual-reference-reconstruction']
    owners = _route_task(task)
    if visual and analysis and owners == ['blender-pipeline']:
        return ['visual-reference-reconstruction']
    if 'blender-robot-mechanism-modeling' in owners:
        owners = ['blender-robot-mechanism-modeling', *[o for o in owners if o != 'blender-robot-mechanism-modeling']]
    domain = any(o.endswith('modeling') or o in {
        'blender-props', 'blender-architecture-environment', 'blender-environment-assets',
        'blender-roads-infrastructure', 'blender-vegetation', 'blender-sculpting'} for o in owners)
    description = bool(re.search(r'\b(?:description|text[ -]only|text[ -]brief|design\s+brief|without\s+(?:images?|references?))\b|'
                                  r'описани|текстов\w*\s+(?:бриф|задани)|без\s+референс', query))
    planning = bool(re.search(r'\b(?:canonical\s+concept|hero\s+view|concept\s+candidates|visual\s+concept)\b|'
                              r'визуальн\w*\s+концепт|выбер\w*\s+концепт', query))
    new_design = bool(re.search(r'\b(?:create|build|make|model)\b|(?:созда|сдела|смодел|постро)\w*', query))
    if (description and analysis or planning) and owners == ['blender-pipeline']:
        return ['visual-reference-reconstruction']
    stage_only = bool(procedure_routes(query)) and not domain
    # Generic creation can be a trivial primitive. Domain agents assess complexity
    # from actual inputs; explicit briefs and new articulated robot design need PASS 0.
    complex_design = new_design and 'blender-robot-mechanism-modeling' in owners
    if not stage_only and (visual or description or complex_design) and geometry_intent(query) and (domain or (visual or description) and owners == ['blender-pipeline']):
        owners = ['visual-reference-reconstruction', *owners]
    return list(dict.fromkeys(owners))


def _context_documents(content):
    """Compatibility with cached two-argument readers; never reread their old body."""
    blocks = re.split(r'\n\n(?=SOURCE: [^\n]+\n\n)', content)
    result = []
    for block in blocks:
        marker, body = block.split('\n\n', 1)
        if not marker.startswith('SOURCE: '):
            raise ValueError('Canonical context has no document identity')
        result.append((marker[8:], body))
    return result


def context(root, task, max_chars=50000, known_documents=None, requested_documents=()):
    """Stateless atomic delivery. Receipts apply only to this caller's retained context.

    Clear receipts for a new agent/chat or after context loss. Missing documents
    are never cut mid-rule. Retained hashes must match current normalized UTF-8 text.
    """
    requested=route_task(task)
    procedures=procedure_routes(action_query(task)) if 'blender-pipeline' in requested else []
    known_documents = known_documents or {}
    if not isinstance(known_documents, dict) or any(not isinstance(p,str) or not isinstance(h,str)
            or not re.fullmatch(r'[0-9a-f]{64}',h) for p,h in known_documents.items()):
        raise ValueError('known_documents must map canonical paths to SHA-256 receipts')
    remaining=max(1,min(int(max_chars),200000))
    loaded=[]; documents={}; owner_documents=[]; conditional={}
    for name in requested:
        content=render_context(root,name,procedures if name == 'blender-pipeline' else ())
        blocks=_context_documents(content)
        # This pointer repeats foundation/pipeline rather than adding rules.
        defer={'skills/blender-pipeline/references/core.md':'Legacy compatibility pointer; foundation and pipeline are delivered directly'}
        if len(requested) > 1:
            # Multi-domain entry: acquire the full capture recipe when actually
            # capturing; retain the bounded renderer/fallback contract now.
            defer['docs/blender-evidence.md']='Read the full acquisition recipe before capture/snapshot/export'
            if len(requested) > 2:
                defer['skills/blender-pipeline/references/techniques/form-development.md']='Read before macro/form construction; domain entrypoints and design locks remain delivered'
            if not re.search(r'\b(?:face|eyes?|hair|hairstyle)\b|лиц|глаз|волос|прич[её]ск',action_query(task)):
                defer['skills/blender-anime-character-modeling/references/face-hair-workflow.md']='Read before face/eye/hair construction'
        for p,b in blocks:
            if p in defer: conditional[p]=dict(path=p,sha256=hashlib.sha256(b.encode()).hexdigest(),reason=defer[p])
        blocks=[(p,b) for p,b in blocks if p not in defer]
        if len(requested) > 1:
            blocks.insert(1,('docs/blender-evidence-entry.md',existing(root,'docs/blender-evidence-entry.md').read_text(encoding='utf-8')))
        owner_documents.append((name,content,blocks))
    if requested_documents:
        if not isinstance(requested_documents,(list,tuple)):
            raise ValueError('requested_documents must be canonical Markdown paths')
        for path in requested_documents:
            if not isinstance(path,str) or not path.startswith(('docs/','skills/')) or not path.endswith('.md') or '..' in Path(path).parts:
                raise ValueError('Only canonical docs/skills Markdown can be requested')
            owner_documents[0][2].append((path,existing(root,path).read_text(encoding='utf-8')))
    missing=[]
    for name,full,blocks in owner_documents:
        parts=[]; absent=[]
        for path,body in blocks:
            digest=hashlib.sha256(body.encode()).hexdigest()
            if path in documents and documents[path]['sha256'] != digest:
                raise ValueError('Document changed during context assembly: '+path)
            if path not in documents:
                state='retained' if known_documents.get(path)==digest else 'pending'
                documents[path]=dict(path=path,sha256=digest,characters=len(body),status=state)
            row=documents[path]
            if row['status'] in ('retained','delivered'):
                continue
            block='SOURCE: '+path+'\n\n'+body
            required=len(block)+(2 if parts else 0)
            if required <= remaining:
                parts.append(block); remaining-=required; row['status']='delivered'
            else:
                absent.append(path)
                if path not in missing: missing.append(path)
        emitted='\n\n'.join(parts)
        loaded.append(dict(name=name,ok=not absent,canonical_root=str(root),content=emitted,
                           truncated=bool(absent),missing_documents=absent,
                           document_paths=list(dict.fromkeys(p for p,_ in blocks)),
                           sha256=hashlib.sha256(emitted.encode()).hexdigest(),
                           full_context_sha256=hashlib.sha256(full.encode()).hexdigest()))
    # Shared documents skipped by an earlier budget can be delivered later only
    # once. Acceptance follows the final document states for every owner.
    for row in loaded:
        row['missing_documents']=[p for p in row['document_paths'] if documents[p]['status']=='pending']
        row['ok']=not row['missing_documents']; row['truncated']=not row['ok']
    missing=[p for p in missing if documents[p]['status']=='pending']
    return dict(ok=all(s['ok'] for s in loaded),task=task,skills=loaded,
                documents=list(documents.values()),missing_documents=missing,
                conditional_documents=list(conditional.values()),
                receipts={p:r['sha256'] for p,r in documents.items() if r['status']!='pending'},
                receipt_scope='Caller-retained context only; reset after compaction/context loss or a new agent/chat',
                delivery='Shared documents emitted once; SOURCE blocks remain whole. Read conditional references before their operation.',
                routing=dict(owners=requested,procedures=procedures,limits='Routing suggestions; inspect actual ownership before edits'),
                error=None if not missing else 'Required documents omitted by budget; request missing_documents with retained receipts or increase max_chars')


def fingerprints(root):
    manifest=catalog(root)
    contexts={alias:hashlib.sha256(render(root,alias).encode()).hexdigest() for alias in manifest['blender_aliases']}
    return dict(architecture=manifest['version'],canonical_root=str(root),contexts=contexts,
                context_digest=hashlib.sha256(json.dumps(contexts,sort_keys=True).encode()).hexdigest())
