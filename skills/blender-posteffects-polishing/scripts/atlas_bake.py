"""Async EMIT/NORMAL atlas bake helpers (INVOKE_DEFAULT + bpy.app.is_job_running) used for Laser_R.
Edit SRC/ATLAS/TEXDIR for the asset. start(kind) -> poll finish(kind) until it returns a dict."""

import bpy, os
ATLAS = 2048
TEXDIR = os.path.join(os.path.dirname(bpy.data.filepath), "Textures")
EMIT = {"LR_Emit_Core", "LR_Emit_Lens", "LR_Emit_Vent"}
SRC = ["LR_Hull_Navy", "LR_Armor_Graphite", "LR_Metal_Dark", "LR_Gold", "LR_Accent_Yellow", "LR_Barrel_HeatTint"]
def atlas_objects():
    root = bpy.data.objects["Laser_R"]
    return [o for o in root.children_recursive if o.type == 'MESH' and o.material_slots and o.material_slots[0].material and o.material_slots[0].material.name in SRC]
def img(name, noncolor):
    im = bpy.data.images.get(name)
    if im is None or tuple(im.size) != (ATLAS, ATLAS):
        if im: bpy.data.images.remove(im)
        im = bpy.data.images.new(name, ATLAS, ATLAS, alpha=False, float_buffer=False)
    im.colorspace_settings.name = 'Non-Color' if noncolor else 'sRGB'
    return im
def prep(kind, im):
    for mn in SRC:
        nt = bpy.data.materials[mn].node_tree; b = nt.nodes["BSDF"]; w = nt.nodes["Wear"]
        for n in [n for n in nt.nodes if n.name.startswith("BAKE_")]: nt.nodes.remove(n)
        t = nt.nodes.new('ShaderNodeTexImage'); t.name = "BAKE_IMG"; t.image = im; nt.nodes.active = t; t.select = True
        if kind in ("COLOR", "ROUGH", "METAL", "AO"):
            src = {"COLOR": w.outputs["Color"], "ROUGH": w.outputs["Roughness"], "METAL": w.outputs["Metallic"]}.get(kind)
            if kind == "AO":
                ao = nt.nodes.new('ShaderNodeAmbientOcclusion'); ao.name = "BAKE_AO"; ao.samples = 32; ao.inputs["Distance"].default_value = 0.06; src = ao.outputs["AO"]
            e = nt.nodes.new('ShaderNodeEmission'); e.name = "BAKE_EMIT"; nt.links.new(src, e.inputs["Color"])
            nt.links.new(e.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
def restore():
    for mn in SRC:
        nt = bpy.data.materials[mn].node_tree
        for n in [n for n in nt.nodes if n.name.startswith("BAKE_")]: nt.nodes.remove(n)
        nt.links.new(nt.nodes["BSDF"].outputs[0], nt.nodes["Material Output"].inputs["Surface"])
def bake(kind, samples=64):
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'GPU'; sc.cycles.samples = samples
    sc.cycles.use_denoising = False
    names = {"COLOR": ("LR_Laser_R_BaseColor", False), "ROUGH": ("LR_tmp_Rough", True), "METAL": ("LR_tmp_Metal", True), "AO": ("LR_tmp_AO", True), "NORMAL": ("LR_Laser_R_Normal", True)}
    nm, nc = names[kind]; im = img(nm, nc)
    objs = atlas_objects()
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    prep(kind, im)
    try:
        if kind == "NORMAL":
            bpy.ops.object.bake(type='NORMAL', normal_space='TANGENT', normal_r='POS_X', normal_g='POS_Y', normal_b='POS_Z', margin=8, margin_type='EXTEND', use_clear=True, uv_layer="UVMap")
        else:
            bpy.ops.object.bake(type='EMIT', margin=8, margin_type='EXTEND', use_clear=True, uv_layer="UVMap")
    finally:
        restore()
    os.makedirs(TEXDIR, exist_ok=True)
    return im

NAMES = {"COLOR": ("LR_Laser_R_BaseColor", False), "ROUGH": ("LR_tmp_Rough", True), "METAL": ("LR_tmp_Metal", True), "AO": ("LR_tmp_AO", True), "NORMAL": ("LR_Laser_R_Normal", True)}
def start(kind, samples):
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'GPU'; sc.cycles.samples = samples; sc.cycles.use_denoising = False
    sc.render.bake.margin = 8; sc.render.bake.margin_type = 'EXTEND'; sc.render.bake.use_clear = True
    nm, nc = NAMES[kind]; im = img(nm, nc)
    objs = atlas_objects()
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    prep(kind, im)
    win = bpy.context.window_manager.windows[0]; area = next(a for a in win.screen.areas if a.type == 'VIEW_3D')
    with bpy.context.temp_override(window=win, area=area, region=next(r for r in area.regions if r.type == 'WINDOW')):
        if kind == "NORMAL":
            r = bpy.ops.object.bake('INVOKE_DEFAULT', type='NORMAL', normal_space='TANGENT', margin=8, margin_type='EXTEND', use_clear=True, uv_layer="UVMap")
        else:
            r = bpy.ops.object.bake('INVOKE_DEFAULT', type='EMIT', margin=8, margin_type='EXTEND', use_clear=True, uv_layer="UVMap")
    return r
def finish(kind):
    if bpy.app.is_job_running('OBJECT_BAKE'): return "RUNNING"
    restore()
    nm, nc = NAMES[kind]; im = bpy.data.images[nm]
    os.makedirs(TEXDIR, exist_ok=True)
    im.filepath_raw = os.path.join(TEXDIR, nm + ".png"); im.file_format = 'PNG'; im.save()
    px = im.pixels[:]; n = len(px)//4
    s = [px[i*4:i*4+3] for i in range(0, n, n//64)]
    return dict(saved=im.filepath_raw, mean=[round(sum(c[k] for c in s)/len(s), 3) for k in range(3)])
