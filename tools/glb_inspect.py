"""Bounded glTF 2 GLB structure/accessor inspector; not the full Khronos validator."""
import argparse
import json
import math
from pathlib import Path
import struct

COMPONENTS = {5120: ('b',1), 5121: ('B',1), 5122: ('h',2), 5123: ('H',2), 5125: ('I',4), 5126: ('f',4)}
WIDTHS = {'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}


def need(ok, message):
    if not ok: raise ValueError(message)


def index(items, value, label):
    need(type(value) is int and 0 <= value < len(items), f'Invalid {label} index: {value}')
    return items[value]


def parse(raw):
    need(len(raw) >= 20, 'Truncated GLB')
    magic, version, length = struct.unpack_from('<4sII',raw)
    need(magic == b'glTF' and version == 2 and length == len(raw), 'Invalid GLB header/length')
    offset, chunks = 12, []
    while offset < length:
        need(offset + 8 <= length, 'Truncated chunk header')
        size, kind = struct.unpack_from('<II',raw,offset); offset += 8
        need(size % 4 == 0 and offset + size <= length, 'Invalid chunk alignment/length')
        chunks.append((kind,raw[offset:offset+size])); offset += size
    need(chunks and chunks[0][0] == 0x4e4f534a, 'JSON must be first GLB chunk')
    need(len(chunks) <= 2 and (len(chunks)==1 or chunks[1][0] == 0x004e4942), 'Unsupported/duplicate GLB chunks')
    def pairs(items):
        result = {}
        for k,v in items:
            need(k not in result, f'Duplicate JSON key {k}'); result[k]=v
        return result
    def constant(x): raise ValueError(f'Nonfinite JSON {x}')
    doc=json.loads(chunks[0][1].decode('utf-8'),object_pairs_hook=pairs,parse_constant=constant)
    need(doc.get('asset',{}).get('version')=='2.0','Expected glTF 2.0 asset')
    return doc, chunks[1][1] if len(chunks)>1 else b''


def accessor(doc, binary, accessor_index):
    a=index(doc.get('accessors',[]),accessor_index,'accessor')
    need('sparse' not in a, 'Sparse accessor unsupported; external validator required')
    need(a.get('type') in WIDTHS and a.get('componentType') in COMPONENTS, 'Unsupported accessor representation')
    fmt,size=COMPONENTS[a['componentType']]; width=WIDTHS[a['type']]
    need(not (a['type'].startswith('MAT') and size < 4), 'Packed matrix accessor unsupported')
    count=a.get('count'); need(type(count) is int and 0 < count <= 10000000,'Invalid/oversized accessor count')
    v=index(doc.get('bufferViews',[]),a.get('bufferView'),'bufferView')
    need(v.get('buffer') == 0, 'External buffer unsupported')
    start=v.get('byteOffset',0); length=v.get('byteLength'); local=a.get('byteOffset',0)
    stride=v.get('byteStride',size*width)
    need(all(type(x) is int and x>=0 for x in (start,length,local,stride)), 'Invalid accessor offsets')
    need(stride >= size*width and stride % size == 0 and local % size == 0 and start % size == 0, 'Invalid accessor stride/alignment')
    need(start+length <= len(binary) and local+(count-1)*stride+size*width <= length, 'Accessor exceeds bufferView')
    values=[struct.unpack_from('<'+fmt*width,binary,start+local+i*stride) for i in range(count)]
    need(all(math.isfinite(x) for row in values for x in row),'Nonfinite accessor data')
    if a.get('normalized'):
        need(a['componentType'] != 5126,'Float normalization invalid')
        divisor={5120:127,5121:255,5122:32767,5123:65535,5125:4294967295}[a['componentType']]
        values=[tuple(max(-1,x/divisor) for x in row) for row in values]
    return values


def inspect(path):
    raw=Path(path).read_bytes(); doc,binary=parse(raw)
    for key in ('nodes','meshes','skins','materials','animations','accessors','bufferViews','buffers','scenes'):
        need(isinstance(doc.get(key,[]),list),f'{key} must be an array')
    buffers=doc.get('buffers',[])
    need(len(buffers)<=1 and all('uri' not in b for b in buffers),'Only embedded GLB buffer supported')
    if buffers:
        n=buffers[0].get('byteLength'); need(type(n) is int and 0<=len(binary)-n<=3,'Buffer byteLength mismatch')
        binary=binary[:n]
    elif binary: raise ValueError('Unreferenced BIN buffer')
    for v in doc.get('bufferViews',[]):
        need(v.get('buffer') == 0 and buffers,'Invalid bufferView buffer')
        off,n=v.get('byteOffset',0),v.get('byteLength')
        need(type(off) is int and type(n) is int and off>=0 and n>0 and off+n<=len(binary),'BufferView exceeds buffer')
    # Fail explicitly for required extensions whose runtime semantics we cannot establish.
    known={'KHR_materials_emissive_strength','KHR_materials_unlit'}
    need(set(doc.get('extensionsRequired',[])) <= known,'Unsupported required extension; full validation required')
    values=[accessor(doc,binary,i) for i in range(len(doc.get('accessors',[])))]
    nodes=doc.get('nodes',[]); meshes=doc.get('meshes',[]); skins=doc.get('skins',[]); materials=doc.get('materials',[])
    images=doc.get('images',[]); textures=doc.get('textures',[])
    for image in images:
        need('uri' not in image,'External/data-URI image validation unsupported in this GLB inspector')
        view=index(doc.get('bufferViews',[]),image.get('bufferView'),'image bufferView')
        need(image.get('mimeType') in {'image/png','image/jpeg'},'Unsupported image encoding')
        start=view.get('byteOffset',0); payload=binary[start:start+view['byteLength']]
        need(payload.startswith(b'\x89PNG\r\n\x1a\n') if image['mimeType']=='image/png' else payload.startswith(b'\xff\xd8\xff'), 'Image payload signature mismatch')
    for texture in textures:
        index(images,texture.get('source'),'texture image')
        if 'sampler' in texture: index(doc.get('samplers',[]),texture['sampler'],'texture sampler')
    def factors(value,size,label):
        need(isinstance(value,list) and len(value)==size and all(type(x) in (int,float) and math.isfinite(x) and x>=0 for x in value),f'Invalid {label}')
    for material in materials:
        pbr=material.get('pbrMetallicRoughness',{})
        factors(pbr.get('baseColorFactor',[1,1,1,1]),4,'base color')
        factors(material.get('emissiveFactor',[0,0,0]),3,'emission')
        for key in ('metallicFactor','roughnessFactor'):
            value=pbr.get(key,1); need(type(value) in (int,float) and 0<=value<=1,f'Invalid {key}')
        for owner,key in [(pbr,'baseColorTexture'),(pbr,'metallicRoughnessTexture'),(material,'normalTexture'),(material,'occlusionTexture'),(material,'emissiveTexture')]:
            if key in owner: index(textures,owner[key].get('index'),key)
    parents={}
    for i,node in enumerate(nodes):
        for k,size in [('matrix',16),('translation',3),('rotation',4),('scale',3)]:
            if k in node:
                need(isinstance(node[k],list) and len(node[k])==size and all(type(x) in (int,float) and math.isfinite(x) for x in node[k]),'Invalid node transform')
        need(not ('matrix' in node and any(k in node for k in ('translation','rotation','scale'))),'Matrix and TRS coexist')
        for child in node.get('children',[]):
            index(nodes,child,'child'); need(child not in parents,'Multiple parents/duplicate child'); parents[child]=i
        if 'mesh' in node: index(meshes,node['mesh'],'mesh')
        if 'skin' in node:
            index(skins,node['skin'],'skin'); need('mesh' in node,'Skin node has no mesh')
    for i in range(len(nodes)):
        seen=set(); cursor=i
        while cursor in parents:
            need(cursor not in seen,'Node hierarchy cycle'); seen.add(cursor); cursor=parents[cursor]
    for scene in doc.get('scenes',[]):
        for n in scene.get('nodes',[]):
            index(nodes,n,'scene node'); need(n not in parents,'Scene root has parent')
    if 'scene' in doc: index(doc.get('scenes',[]),doc['scene'],'scene')
    primitives=triangles=0
    for mesh in meshes:
        need(bool(mesh.get('primitives')),'Empty mesh')
        for primitive in mesh['primitives']:
            need(primitive.get('mode',4)==4,'Nontriangle primitive unsupported')
            attrs=primitive.get('attributes',{}); need('POSITION' in attrs,'Missing POSITION')
            p=index(values,attrs['POSITION'],'POSITION'); need(len(p[0])==3,'POSITION must be VEC3')
            for semantic, a in attrs.items():
                need(len(index(values,a,semantic))==len(p),'Attribute count mismatch')
            if 'material' in primitive: index(materials,primitive['material'],'material')
            if 'indices' in primitive:
                a=index(doc['accessors'],primitive['indices'],'indices')
                need(a['type']=='SCALAR' and a['componentType'] in (5121,5123,5125) and not a.get('normalized'),'Invalid index accessor')
                ids=[v[0] for v in values[primitive['indices']]]
                need(all(0<=i<len(p) for i in ids),'Primitive index exceeds POSITION')
                count=len(ids)
            else: count=len(p)
            need(count%3==0,'Incomplete triangle'); triangles+=count//3; primitives+=1
    skin_rows=[]
    for skin in skins:
        joints=skin.get('joints',[]); need(bool(joints) and len(set(joints))==len(joints),'Invalid skin joints')
        for joint in joints: index(nodes,joint,'joint')
        if 'skeleton' in skin: index(nodes,skin['skeleton'],'skeleton')
        if 'inverseBindMatrices' in skin:
            a=index(doc['accessors'],skin['inverseBindMatrices'],'bind matrices')
            need(a['type']=='MAT4' and a['componentType']==5126 and len(values[skin['inverseBindMatrices']])==len(joints),'Invalid inverse bind matrices')
        skin_rows.append(dict(name=skin.get('name'),joints=[nodes[j].get('name',f'#{j}') for j in joints]))
    for node in nodes:
        if 'skin' not in node: continue
        joint_count=len(skins[node['skin']]['joints'])
        for primitive in meshes[node['mesh']]['primitives']:
            attrs=primitive['attributes']; need('JOINTS_0' in attrs and 'WEIGHTS_0' in attrs,'Skinned primitive lacks bindings')
            joints=values[attrs['JOINTS_0']]; weights=values[attrs['WEIGHTS_0']]
            need(all(len(row)==4 and all(type(x) is int and 0<=x<joint_count for x in row) for row in joints),'Skin joint index invalid')
            need(all(len(row)==4 and all(x>=0 for x in row) and abs(sum(row)-1)<.02 for row in weights),'Skin weights invalid')
    animation_rows=[]
    for animation in doc.get('animations',[]):
        channels=[]
        for channel in animation.get('channels',[]):
            sampler=index(animation.get('samplers',[]),channel.get('sampler'),'animation sampler')
            target=channel['target']; node=index(nodes,target.get('node'),'animation target')
            kind=target.get('path'); need(kind in {'translation','rotation','scale','weights'},'Unsupported animation channel')
            times=index(values,sampler.get('input'),'animation input'); output=index(values,sampler.get('output'),'animation output')
            a=doc['accessors'][sampler['input']]; need(a['type']=='SCALAR' and a['componentType']==5126,'Invalid animation time accessor')
            times=[row[0] for row in times]; need(times[0]>=0 and all(a<b for a,b in zip(times,times[1:])),'Animation times must increase')
            interp=sampler.get('interpolation','LINEAR'); need(interp in ('LINEAR','STEP','CUBICSPLINE'),'Unknown interpolation')
            if kind=='weights': raise ValueError('Morph animation comparison unsupported; external validation required')
            need(len(output)==len(times)*(3 if interp=='CUBICSPLINE' else 1),'Animation sample count mismatch')
            need(len(output[0])==(4 if kind=='rotation' else 3),'Animation value width mismatch')
            channels.append(dict(node=node.get('name',f"#{target['node']}"),path=kind,start=times[0],end=times[-1],
                                 samples=len(times),value_min=[min(row[i] for row in output) for i in range(len(output[0]))],
                                 value_max=[max(row[i] for row in output) for i in range(len(output[0]))]))
        need(bool(channels),'Empty animation')
        animation_rows.append(dict(name=animation.get('name'),channels=channels))
    return dict(status='STRUCTURAL PASS',bytes=len(raw),nodes=len(nodes),meshes=len(meshes),primitives=primitives,
                triangles=triangles,skins=skin_rows,skinned_nodes=sum('skin' in n for n in nodes),
                materials=[m.get('name') for m in materials],animations=animation_rows,
                limits=['Bounded GLB subset, not full Khronos conformance','Texture payloads, shading equivalence, arbitrary extensions and visual quality require separate checks'])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('glb',type=Path); args=p.parse_args()
    try: print(json.dumps(inspect(args.glb),indent=2))
    except (ValueError,KeyError,TypeError,IndexError,OSError) as exc:
        print(json.dumps(dict(status='FAIL',reason=str(exc)))); raise SystemExit(1)
