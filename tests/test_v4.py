import copy
import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import check
import glb_inspect
import handoff_snapshot as handoff
import mcp_runtime
import mcp_deployment
import export_validate
import python_preflight
import read_blender_skill
import sync_blender


def snapshot():
    return dict(schema_version=1,stage='animation',blender_version='fixture',frame=1,fps=24,
                objects=[dict(name='Mesh',type='MESH',parent=None,parent_bone='',matrix_world=[1.,0,0,0,0,1.,0,0,0,0,1.,0,0,0,0,1.],
                    geometry=dict(vertices=3,edges=3,polygons=1,triangles=1,sha256='a'*64),bones=[],materials=['Mat'])],
                actions=[dict(name='Wave',range=[1,25])],protected_objects=['Mesh'],blockers=[],
                verification=dict(structural='PASS',visual='SKIP',evidence=[],reason='Fixture structure only'))


def glb(doc=None,binary=None):
    if binary is None: binary=struct.pack('<9f',0,0,0,1,0,0,0,1,0)
    if doc is None:
        doc=dict(asset=dict(version='2.0'),buffers=[dict(byteLength=len(binary))],
                 bufferViews=[dict(buffer=0,byteLength=len(binary))],
                 accessors=[dict(bufferView=0,componentType=5126,count=3,type='VEC3')],
                 meshes=[dict(primitives=[dict(attributes=dict(POSITION=0))])],nodes=[dict(mesh=0)],scenes=[dict(nodes=[0])],scene=0)
    raw=json.dumps(doc).encode(); raw+=b' '*((-len(raw))%4)
    data=binary+b'\0'*((-len(binary))%4)
    return struct.pack('<4sII',b'glTF',2,28+len(raw)+len(data))+struct.pack('<II',len(raw),0x4e4f534a)+raw+struct.pack('<II',len(data),0x004e4942)+data


class V4Test(unittest.TestCase):
    def test_snapshot_deterministic_and_protected_geometry_regression(self):
        before=snapshot(); after=copy.deepcopy(before)
        self.assertEqual(handoff.canonical_bytes(before),handoff.canonical_bytes(dict(reversed(list(before.items())))))
        after['objects'][0]['geometry']['sha256']='b'*64
        self.assertEqual(handoff.compare(before,after)['protected_regressions'],['Mesh'])
        after['objects']=[]; after['protected_objects']=[]
        self.assertEqual(handoff.compare(before,after)['protected_regressions'],['Mesh'])

    def test_snapshot_schema_rejects_malformed_and_visual_claims(self):
        for field,value in [('schema_version',True),('frame',float('nan')),('fps',0),('protected_objects',['Missing']),('objects',{}),('actions',[dict(name='Clip',range=[25,1])])]:
            data=snapshot(); data[field]=value
            with self.subTest(field=field),self.assertRaises(check.Violation): handoff.validate(data)
        data=snapshot(); data['verification']['visual']='PASS'
        with self.assertRaises(check.Violation): handoff.validate(data)
        data=snapshot(); data['extra']=1
        with self.assertRaises(check.Violation): handoff.validate(data)

    def test_time_and_actions_are_not_silently_equal(self):
        before=snapshot(); after=copy.deepcopy(before); after['frame']=12; after['actions'][0]['range']=[1,26]
        result=handoff.compare(before,after)
        self.assertFalse(result['comparable_time']); self.assertTrue(result['actions_changed'])

    def test_python_preflight_rejects_before_any_execution(self):
        for code in ['if :\n pass','return 3','break','x="\0"']:
            with self.subTest(code=code): self.assertFalse(python_preflight.preflight(code)['ok'])
        self.assertTrue(python_preflight.preflight('import bpy\n_result = bpy.app.version_string')['ok'])
        self.assertTrue(python_preflight.preflight("raise Exception('must never execute')")['ok'])
        self.assertEqual(len(python_preflight.preflight('bpy.ops.object.delete()')['warnings']),1)

    def test_routing_boundaries_and_collisions(self):
        cases={
            'Add a jump Action to the existing rig.':['blender-animation'],
            'Fix shoulder weights and preserve all current clips.':['blender-rigging-skinning'],
            'Export the unchanged character as GLB and validate it in Godot.':['blender-export-validation','godot-asset-integration'],
            'Build a character blockout.':['blender-character-modeling'],
            'The elbow deforms badly; diagnose the cause.':['verification'],
            'Review the mesh without editing it.':['verification'],
            'Continue the asset task.':['blender-pipeline'],
        }
        for prompt,expected in cases.items():
            with self.subTest(prompt=prompt): self.assertEqual(mcp_runtime.route_task(prompt),expected)
        for name in read_blender_skill.SPECIALISTS:
            self.assertEqual(mcp_runtime.route_task(name),[name])
            result=mcp_runtime.context(check.ROOT,name)
            self.assertTrue(result['ok']); self.assertIn('SOURCE: docs/foundation.md',result['skills'][0]['content'])
        self.assertFalse(mcp_runtime.context(check.ROOT,'blender-animation',5)['ok'])

    def test_legacy_combined_route_resolves_all_replacements(self):
        context=read_blender_skill.render(check.ROOT,'Blender_Character_Rigging_Animation_Godot_SKILL')
        for name in read_blender_skill.SPECIALISTS:
            self.assertIn('SOURCE: skills/'+name+'/SKILL.md',context)
        self.assertEqual(context.count('SOURCE: docs/foundation.md'),1)

    def test_router_detects_changed_context_without_editing_router_body(self):
        alias='Blender_Character_Modeling_SKILL'
        first=read_blender_skill.router(check.ROOT,alias)
        with patch.object(read_blender_skill,'render',return_value='changed canonical context'):
            second=read_blender_skill.router(check.ROOT,alias)
        self.assertNotEqual(first,second)

    def test_sync_rejects_stale_or_duplicate_entries_before_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); sync_blender.generate(root)
            manifest=root/'skills/PIPELINE_MANIFEST.json'; data=json.loads(manifest.read_text()); data['skills'].append(data['skills'][0])
            manifest.write_text(json.dumps(data))
            with patch.object(Path,'write_bytes',side_effect=AssertionError('mutation before rejection')):
                with self.assertRaises(check.Violation): sync_blender.generate(root)

    def test_nested_duplicate_router_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); sync_blender.generate(root)
            extra=root/'skills/nested/Blender_Character_Modeling_SKILL/SKILL.md'
            extra.parent.mkdir(parents=True); extra.write_text('duplicate')
            with self.assertRaises(check.Violation): sync_blender.generate(root)

    def test_stale_connector_catalog_is_not_live_pass(self):
        result=mcp_deployment.compare_catalog(['read_skill','capture_viewport'],['read_skill'])
        self.assertEqual(result['status'],'WARN'); self.assertEqual(result['missing'],['capture_viewport'])

    def test_export_comparison_accepts_representation_and_catches_regressions(self):
        source=snapshot(); imported=copy.deepcopy(source)
        info=dict(bounds=dict(min=[0,0,0],max=[1,1,1]))
        gltf=dict(animations=[dict(name='Wave',channels=[dict(start=0,end=1)])],materials=['Mat'],skins=[])
        imported['objects'][0]['geometry']['vertices']=12
        result=export_validate.compare(source,imported,info,info,gltf)
        self.assertEqual(result['status'],'STRUCTURAL PASS')
        self.assertEqual(result['semantic_review'],'REVIEW REQUIRED')
        moved=dict(bounds=dict(min=[0,0,0],max=[2,1,1]))
        self.assertEqual(export_validate.compare(source,imported,info,moved,gltf)['status'],'FAIL')
        imported['objects'][0]['materials']=[]
        self.assertEqual(export_validate.compare(source,imported,info,info,gltf)['status'],'FAIL')
        imported=copy.deepcopy(source); gltf['animations']=[]
        self.assertEqual(export_validate.compare(source,imported,info,info,gltf)['status'],'FAIL')

    def test_glb_rejects_broken_material_texture(self):
        doc,binary=glb_inspect.parse(glb())
        doc['materials']=[dict(pbrMetallicRoughness=dict(baseColorTexture=dict(index=0)))]
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'bad.glb'; path.write_bytes(glb(doc,binary))
            with self.assertRaisesRegex(ValueError,'baseColorTexture'): glb_inspect.inspect(path)

    def test_glb_valid_triangle_and_bad_container(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'mesh.glb'; path.write_bytes(glb())
            self.assertEqual(glb_inspect.inspect(path)['triangles'],1)
            for raw in [b'',glb()[:-1],b'BAD!'+glb()[4:]]:
                path.write_bytes(raw)
                with self.assertRaises(ValueError): glb_inspect.inspect(path)

    def test_glb_rejects_range_cycle_missing_skin_and_nonfinite(self):
        doc,binary=glb_inspect.parse(glb())
        variants=[]
        d=copy.deepcopy(doc); d['accessors'][0]['count']=4; variants.append((d,binary))
        d=copy.deepcopy(doc); d['nodes'][0]['children']=[0]; variants.append((d,binary))
        d=copy.deepcopy(doc); d['nodes'][0]['skin']=0; variants.append((d,binary))
        d=copy.deepcopy(doc); d['skins']=[dict(joints=[0])]; d['nodes'][0]['skin']=0; variants.append((d,binary))
        d=copy.deepcopy(doc); d['accessors'][0]['sparse']={}; variants.append((d,binary))
        variants.append((doc,struct.pack('<9f',float('nan'),0,0,1,0,0,0,1,0)))
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'bad.glb'
            for d,b in variants:
                path.write_bytes(glb(d,b))
                with self.assertRaises(ValueError): glb_inspect.inspect(path)


if __name__=='__main__': unittest.main()
