"""LR wear node group (Cycles): paint chips on edges, cavity grime, dust, soot, scratches,
panel seams, brushed streaks. Run inside Blender: exec(open(p).read()); build_wear_group().
Edge mask compares Bevel normal with True Normal (works with hardened/weighted normals).
Procedural: bake to textures before glTF delivery (see game-atlas-bake.md). Debug output = RGB(chip, grime, scratch|soot).
Origin: Laser_R / RockMind, 2026-11-18."""

import bpy
def build_wear_group():
    ng = bpy.data.node_groups.get("TC_Wear")
    if ng: bpy.data.node_groups.remove(ng)
    ng = bpy.data.node_groups.new("TC_Wear", 'ShaderNodeTree')
    I = ng.interface
    def si(n, t, d=None, mn=None, mx=None):
        s = I.new_socket(n, in_out='INPUT', socket_type=t)
        if d is not None: s.default_value = d
        if mn is not None: s.min_value = mn
        if mx is not None: s.max_value = mx
        return s
    si("Paint", 'NodeSocketColor', (0.1, 0.1, 0.1, 1)); si("Paint Rough", 'NodeSocketFloat', 0.5, 0, 1); si("Paint Metal", 'NodeSocketFloat', 0.0, 0, 1)
    si("Bare", 'NodeSocketColor', (0.55, 0.55, 0.56, 1)); si("Bare Rough", 'NodeSocketFloat', 0.35, 0, 1)
    for n, d in (("Chip", 0.5), ("Grime", 0.6), ("Scratch", 0.5), ("Dust", 0.4), ("Soot", 0.3), ("Seed", 0.0), ("Panel", 0.0), ("Brushed", 0.0)):
        si(n, 'NodeSocketFloat', d)
    for n, t in (("Color", 'NodeSocketColor'), ("Roughness", 'NodeSocketFloat'), ("Metallic", 'NodeSocketFloat'), ("Normal", 'NodeSocketVector'), ("Height", 'NodeSocketFloat'), ("Debug", 'NodeSocketColor')):
        I.new_socket(n, in_out='OUTPUT', socket_type=t)
    N, L = ng.nodes, ng.links
    gi = N.new('NodeGroupInput'); go = N.new('NodeGroupOutput')
    def nd(t, **kw):
        n = N.new(t)
        for k, v in kw.items(): setattr(n, k, v)
        return n
    def sock(n, name, out=False):
        coll = n.outputs if out else n.inputs
        for s in coll:
            if s.enabled and (s.identifier == name or s.name == name): return s
        raise KeyError(name)
    def link(a, b): L.new(a, b)
    def val(x):
        if isinstance(x, (int, float)):
            v = nd('ShaderNodeValue'); v.outputs[0].default_value = x; return v.outputs[0]
        return x
    def math(op, a, b=0.0, clamp=False):
        m = nd('ShaderNodeMath', operation=op, use_clamp=clamp)
        for i, x in enumerate((a, b)):
            if isinstance(x, (int, float)): m.inputs[i].default_value = x
            else: link(x, m.inputs[i])
        return m.outputs[0]
    def mrange(v, a, b, c=0.0, d=1.0):
        m = nd('ShaderNodeMapRange', clamp=True); link(v, m.inputs["Value"])
        m.inputs["From Min"].default_value = a; m.inputs["From Max"].default_value = b; m.inputs["To Min"].default_value = c; m.inputs["To Max"].default_value = d
        return m.outputs["Result"]
    def mix(fac, a, b):
        m = nd('ShaderNodeMix', data_type='RGBA', clamp_factor=True)
        for nm, x in (("Factor_Float", fac), ("A_Color", a), ("B_Color", b)):
            s = sock(m, nm)
            if isinstance(x, tuple): s.default_value = x
            elif isinstance(x, (int, float)): s.default_value = x
            else: link(x, s)
        return sock(m, "Result_Color", True)
    def lerp(fac, a, b):   # float lerp
        return math('ADD', math('MULTIPLY', math('SUBTRACT', 1.0, fac), a), math('MULTIPLY', fac, b))
    def noise(vec, scale, detail=6.0, rough=0.6, dist=0.0):
        n = nd('ShaderNodeTexNoise', noise_dimensions='3D'); link(vec, n.inputs["Vector"])
        n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = detail; n.inputs["Roughness"].default_value = rough; n.inputs["Distortion"].default_value = dist
        return n.outputs["Fac"]
    tc = nd('ShaderNodeTexCoord'); geo = nd('ShaderNodeNewGeometry')
    seedv = nd('ShaderNodeCombineXYZ'); link(math('MULTIPLY', gi.outputs["Seed"], 17.31), seedv.inputs[0]); link(math('MULTIPLY', gi.outputs["Seed"], 9.73), seedv.inputs[1])
    co = nd('ShaderNodeVectorMath', operation='ADD'); link(tc.outputs["Object"], co.inputs[0]); link(seedv.outputs[0], co.inputs[1]); co = co.outputs[0]
    wp = nd('ShaderNodeSeparateXYZ'); link(geo.outputs["Position"], wp.inputs[0])
    wn = nd('ShaderNodeSeparateXYZ'); link(geo.outputs["Normal"], wn.inputs[0])
    # --- edge mask (Cycles Bevel trick)
    bev = nd('ShaderNodeBevel', samples=8); bev.inputs["Radius"].default_value = 0.009
    dot = nd('ShaderNodeVectorMath', operation='DOT_PRODUCT'); link(bev.outputs["Normal"], dot.inputs[0]); link(geo.outputs["True Normal"], dot.inputs[1])
    edge = mrange(sock(dot, "Value", True), 0.9985, 0.965)
    # --- broad condition zones + exposure (front/top/upper edges get more abuse)
    zone = noise(co, 2.5, 3, 0.5)
    expo = math('ADD', math('MULTIPLY', wn.outputs[2], 0.12), math('MULTIPLY', mrange(wp.outputs[0], -0.2, -0.68), 0.15))
    # --- paint chips: edge * breakup, sharp threshold
    brk = noise(co, 32.0, 10, 0.7, 0.3)
    v = math('ADD', math('MULTIPLY', edge, 0.6), math('MULTIPLY', mrange(brk, 0.35, 0.65), 0.8))
    v = math('ADD', v, math('MULTIPLY', math('SUBTRACT', zone, 0.5), 0.6))
    v = math('ADD', v, expo)
    v = math('ADD', v, math('SUBTRACT', math('MULTIPLY', gi.outputs["Chip"], 0.6), 1.55))
    chip = mrange(v, 0.0, 0.05)
    chip_soft = mrange(v, -0.08, 0.05)          # paint thinning ring around chips
    # --- scratches: two directional sets of thin ridges, sparse
    def scratch_set(rot_z, sx, sparse_scale, seed_off):
        mp = nd('ShaderNodeMapping'); link(co, mp.inputs["Vector"]); mp.inputs["Rotation"].default_value = (0, 0, rot_z)
        mp.inputs["Scale"].default_value = (sx, 420.0, 420.0); mp.inputs["Location"].default_value = (seed_off, 0, 0)
        n = noise(mp.outputs[0], 1.0, 2, 0.5)
        ridge = math('SUBTRACT', 1.0, math('MULTIPLY', math('ABSOLUTE', math('SUBTRACT', n, 0.5)), 2.0))
        thin = math('POWER', ridge, 140.0)
        sparse = mrange(noise(co, sparse_scale, 2, 0.5), 0.62, 0.72)
        return math('MULTIPLY', thin, sparse)
    scr = math('MAXIMUM', scratch_set(0.0, 2.5, 6.0, 0.0), scratch_set(0.55, 3.5, 4.0, 3.3))
    scr = math('MULTIPLY', math('MULTIPLY', scr, gi.outputs["Scratch"]), math('SUBTRACT', 1.0, chip))
    scr = math('MINIMUM', math('MULTIPLY', scr, 1.0), 1.0)
    # --- cavity grime (AO) + gravity (downward faces) with breakup
    ao = nd('ShaderNodeAmbientOcclusion', samples=16, only_local=False); ao.inputs["Distance"].default_value = 0.05
    cav = mrange(ao.outputs["AO"], 0.7, 0.25)
    down = mrange(wn.outputs[2], -0.4, -0.95)
    gn = noise(co, 9.0, 6, 0.6)
    grime = math('MULTIPLY', math('ADD', math('MULTIPLY', cav, 0.8), math('MULTIPLY', down, 0.25)), mrange(gn, 0.35, 0.7, 0.2, 1.0))
    grime = math('MINIMUM', math('MULTIPLY', grime, gi.outputs["Grime"]), 1.0)
    # --- dust on up-facing surfaces
    dust = math('MULTIPLY', math('MULTIPLY', mrange(wn.outputs[2], 0.55, 0.95), mrange(noise(co, 14.0, 8, 0.65), 0.45, 0.75)), gi.outputs["Dust"])
    # --- soot near emitter (world -X) with streaks along the barrel
    smp = nd('ShaderNodeMapping'); link(co, smp.inputs["Vector"]); smp.inputs["Scale"].default_value = (2.0, 25.0, 25.0)
    soot = math('MULTIPLY', mrange(wp.outputs[0], -0.55, -0.70), mrange(noise(smp.outputs[0], 1.0, 4, 0.6), 0.4, 0.75, 0.1, 0.9))
    soot = math('MINIMUM', math('MULTIPLY', soot, gi.outputs["Soot"]), 1.0)

    # --- panel seams: grooves at fixed object-space stations (X) + one horizontal belt (Z)
    pxs = nd('ShaderNodeSeparateXYZ'); link(tc.outputs["Object"], pxs.inputs[0])
    def groove(coord, period, width):
        f = math('FRACT', math('DIVIDE', coord, period))
        d = math('MINIMUM', f, math('SUBTRACT', 1.0, f))
        return mrange(math('MULTIPLY', d, period), width, width*0.35)
    seam = math('MAXIMUM', groove(math('ADD', pxs.outputs[0], 0.03), 0.145, 0.0016), groove(math('SUBTRACT', pxs.outputs[2], 0.035), 0.19, 0.0014))
    seam = math('MULTIPLY', math('MULTIPLY', seam, gi.outputs["Panel"]), math('SUBTRACT', 1.0, edge))
    # --- edge lightening (paint burnished on edges, before chipping)
    burn = math('MULTIPLY', edge, mrange(noise(co, 18.0, 4, 0.6), 0.3, 0.7, 0.3, 1.0))
    # --- smudges (oily handling marks) for roughness breakup
    smudge = mrange(noise(co, 3.5, 6, 0.65, 0.6), 0.45, 0.75)
    # --- brushed streaks along the long axis
    bmp = nd('ShaderNodeMapping'); link(co, bmp.inputs["Vector"]); bmp.inputs["Scale"].default_value = (3.0, 260.0, 260.0)
    brushed = math('MULTIPLY', math('SUBTRACT', noise(bmp.outputs[0], 1.0, 6, 0.6), 0.5), gi.outputs["Brushed"])
    # --- colour
    hsv = nd('ShaderNodeHueSaturation'); link(gi.outputs["Paint"], hsv.inputs["Color"])
    link(mrange(noise(co, 5.0, 4, 0.5), 0.3, 0.7, 0.86, 1.12), hsv.inputs["Value"])
    c = mix(math('MULTIPLY', burn, 0.18), hsv.outputs[0], (0.55, 0.56, 0.6, 1.0))
    c = mix(math('MULTIPLY', chip_soft, 0.25), c, (0.32, 0.31, 0.30, 1.0))
    c = mix(math('MULTIPLY', seam, 0.6), c, (0.01, 0.01, 0.012, 1.0))     # thinned paint / primer halo
    bare = nd('ShaderNodeHueSaturation'); link(gi.outputs["Bare"], bare.inputs["Color"]); link(mrange(brk, 0.3, 0.7, 0.8, 1.1), bare.inputs["Value"])
    c = mix(chip, c, bare.outputs[0])
    c = mix(math('MULTIPLY', scr, 0.45), c, gi.outputs["Bare"])
    c = mix(math('MULTIPLY', grime, 0.75), c, (0.028, 0.024, 0.02, 1.0))
    c = mix(math('MULTIPLY', dust, 0.55), c, (0.30, 0.28, 0.25, 1.0))
    c = mix(math('MULTIPLY', soot, 0.85), c, (0.012, 0.011, 0.011, 1.0))
    # --- roughness / metallic
    r = math('ADD', gi.outputs["Paint Rough"], math('MULTIPLY', math('SUBTRACT', noise(co, 7.0, 5, 0.6), 0.5), 0.2))
    r = math('SUBTRACT', r, math('MULTIPLY', smudge, 0.16))
    r = math('ADD', r, math('MULTIPLY', brushed, 0.5))
    r = math('SUBTRACT', r, math('MULTIPLY', burn, 0.12))
    r = lerp(chip, r, gi.outputs["Bare Rough"]); r = lerp(scr, r, 0.3)
    r = lerp(grime, r, 0.82); r = lerp(dust, r, 0.88); r = lerp(soot, r, 0.72)
    m = lerp(chip, gi.outputs["Paint Metal"], 1.0); m = lerp(math('MULTIPLY', scr, 0.8), m, 1.0)
    m = lerp(math('MULTIPLY', grime, 0.8), m, 0.0); m = lerp(dust, m, 0.0); m = lerp(soot, m, 0.0)
    # --- relief: recessed chips, scratch grooves, fine orange-peel
    h = math('ADD', math('MULTIPLY', chip, -1.0), math('MULTIPLY', scr, -0.6))
    h = math('ADD', h, math('MULTIPLY', seam, -1.4))
    h = math('ADD', h, math('MULTIPLY', brushed, 0.25))
    h = math('ADD', h, math('MULTIPLY', noise(co, 180.0, 3, 0.5), 0.12))
    bump = nd('ShaderNodeBump'); bump.inputs["Strength"].default_value = 0.6; bump.inputs["Distance"].default_value = 0.0008
    link(h, bump.inputs["Height"])
    link(c, go.inputs["Color"]); link(math('MINIMUM', math('MAXIMUM', r, 0.05), 1.0), go.inputs["Roughness"])
    link(math('MINIMUM', math('MAXIMUM', m, 0.0), 1.0), go.inputs["Metallic"]); link(bump.outputs["Normal"], go.inputs["Normal"]); link(h, go.inputs["Height"])
    dbg = nd('ShaderNodeCombineColor'); link(chip, dbg.inputs[0]); link(grime, dbg.inputs[1]); link(math('MAXIMUM', scr, soot), dbg.inputs[2]); link(dbg.outputs[0], go.inputs["Debug"])
    return ng
