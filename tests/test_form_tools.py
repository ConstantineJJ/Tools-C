"""Observable geometry/context regressions; Blender probes are separate."""
import copy
import hashlib
import json
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import blender_forms as forms
import check
import handoff_snapshot
import mcp_runtime
import read_blender_skill


class FormMathTest(unittest.TestCase):
    def test_transported_frames_remain_orthonormal_across_global_up_direction(self):
        path=[(math.sin(i*0.07),0.15*math.sin(i*0.12),math.cos(i*0.07)) for i in range(48)]
        frames=forms.transported_frames(path)
        for tangent,u,v in frames:
            for vector in (tangent,u,v): self.assertAlmostEqual(forms.dot(vector,vector),1)
            self.assertAlmostEqual(forms.dot(tangent,u),0)
            self.assertAlmostEqual(forms.dot(tangent,v),0)
            self.assertAlmostEqual(forms.dot(u,v),0)
            self.assertGreater(forms.dot(forms.cross(tangent,u),v),0.9999)
        self.assertTrue(all(forms.dot(a[1],b[1])>0.95 for a,b in zip(frames,frames[1:])))

    def test_invalid_cusps_and_parallel_initial_normal_are_rejected(self):
        for path,normal in [([(0,0,0),(0,0,1),(0,0,0)],None),
                            ([(0,0,0),(0,0,0)],None), ([(0,0,0),(0,0,1)],(0,0,1))]:
            with self.subTest(path=path,normal=normal),self.assertRaises(ValueError):
                forms.transported_frames(path,normal)

    def test_independent_sections_and_arc_length_uvs(self):
        data=forms.sweep_geometry([(0,0,0),(0,0,1),(0,0,3)],[0.5,0.8,0.1],[0.2,0.3,0.1],sides=8,normal=(1,0,0))
        self.assertAlmostEqual(data['vertices'][0][0],0.5)
        self.assertAlmostEqual(data['vertices'][2][1],0.2)
        self.assertAlmostEqual(data['vertices'][8][0],0.8)
        self.assertAlmostEqual(data['loop_uvs'][0][2][1],1/3)
        self.assertAlmostEqual(data['loop_uvs'][8][2][1],1)
        from collections import Counter
        edges=Counter()
        for face in data['faces']:
            for a,b in zip(face,face[1:]+face[:1]): edges[tuple(sorted((a,b)))]+=1
        self.assertTrue(all(v==2 for v in edges.values()))

    def test_collapsed_or_nonfinite_profiles_are_not_created(self):
        for widths in ([0,1],[float('nan'),1],[1]):
            with self.subTest(widths=widths),self.assertRaises(ValueError):
                forms.sweep_geometry([(0,0,0),(0,0,1)],widths,[1,1])


class ContextDeliveryTest(unittest.TestCase):
    mixed='Создай аниме кошкодевушку и арбузный домик, скамью, фонарь, забор, дерево.'

    def test_natural_russian_assets_and_mixed_creation(self):
        expected=['blender-architecture-environment','blender-environment-assets','blender-vegetation','blender-anime-character-modeling']
        self.assertEqual(mcp_runtime.route_task(self.mixed),expected)
        for task in ['Создай кошкотян.', 'Сделай аниме кошкодевушку.', 'Сгладь основные формы аниме кошкотян.']:
            self.assertEqual(mcp_runtime.route_task(task),['blender-anime-character-modeling'])
        self.assertEqual(mcp_runtime.route_task('Создай арбузный домик.'),['blender-architecture-environment'])
        self.assertEqual(mcp_runtime.route_task('Сделай скамью и забор.'),['blender-environment-assets'])
        self.assertEqual(mcp_runtime.route_task('Создай реквизит для диорамы.'),['blender-props'])

    def test_protected_background_and_stage_only_requests_stay_scoped(self):
        for task,owners in {
            'Проверь кошкотян рядом с домиком и скамьёй без правок.':['verification'],
            'Улучши материал волос кошкотян; не меняй домик, скамью, дерево и геометрию.':['blender-posteffects-polishing'],
            'Создай rig для аниме кошкодевушки.':['blender-rigging-skinning'],
            'Сохрани rig кошкодевушки. Создай домик.':['blender-architecture-environment'],
            'Сохрани домик и скамью. Создай дерево.':['blender-vegetation'],
            'Создай домашний компьютер.':['blender-product-electronics-modeling'],
            'Create an anime-style car.':['blender-vehicle-modeling'],
        }.items():
            with self.subTest(task=task): self.assertEqual(mcp_runtime.route_task(task),owners)

    def test_default_mixed_context_has_each_entrypoint_and_shared_documents_once(self):
        c=mcp_runtime.context(check.ROOT,self.mixed)
        self.assertTrue(c['ok'],c['error'])
        combined='\n\n'.join(s['content'] for s in c['skills'])
        for owner in c['routing']['owners']:
            self.assertEqual(combined.count('SOURCE: skills/'+owner+'/SKILL.md\n\n'),1)
        self.assertEqual(combined.count('SOURCE: docs/foundation.md\n\n'),1)
        self.assertLessEqual(sum(len(s['content']) for s in c['skills']),50000)
        self.assertTrue(any(d['path'].endswith('face-hair-workflow.md') for d in c['conditional_documents']))

    def test_receipts_are_explicit_current_and_resettable(self):
        first=mcp_runtime.context(check.ROOT,'blender-character-modeling')
        retained=mcp_runtime.context(check.ROOT,'blender-character-modeling',known_documents=first['receipts'])
        self.assertTrue(retained['ok'])
        self.assertEqual(retained['skills'][0]['content'],'')
        stale=dict(first['receipts']); stale['docs/foundation.md']='0'*64
        reread=mcp_runtime.context(check.ROOT,'blender-character-modeling',known_documents=stale)
        self.assertIn('SOURCE: docs/foundation.md',reread['skills'][0]['content'])
        reset=mcp_runtime.context(check.ROOT,'blender-character-modeling')
        self.assertEqual(reset['skills'][0]['content'],first['skills'][0]['content'])

    def test_tight_budget_defers_whole_documents_and_can_continue(self):
        first=mcp_runtime.context(check.ROOT,self.mixed,12000)
        self.assertFalse(first['ok'])
        for s in first['skills']:
            for path,body in mcp_runtime._context_documents(s['content']) if s['content'] else []:
                self.assertEqual(body,check.existing(check.ROOT,path).read_text(encoding='utf-8'))
        follow=mcp_runtime.context(check.ROOT,self.mixed,50000,known_documents=first['receipts'],
                                 requested_documents=first['missing_documents'])
        self.assertTrue(follow['ok'],follow['error'])
        self.assertTrue(set(first['missing_documents'])<=set(follow['receipts']))

    def test_conditional_reference_is_fetchable_but_arbitrary_paths_are_rejected(self):
        c=mcp_runtime.context(check.ROOT,self.mixed)
        face='skills/blender-anime-character-modeling/references/face-hair-workflow.md'
        follow=mcp_runtime.context(check.ROOT,self.mixed,known_documents=c['receipts'],requested_documents=[face])
        self.assertIn('SOURCE: '+face,follow['skills'][0]['content'])
        for path in ['../secrets.md','.local/private.md','docs/../../private.md','docs/blender-evidence.md:stream']:
            with self.subTest(path=path),self.assertRaises((ValueError,check.Violation)):
                mcp_runtime.context(check.ROOT,self.mixed,requested_documents=[path])


class ExtendedSnapshotTest(unittest.TestCase):
    def sample(self):
        from test_v4 import snapshot
        return snapshot()

    def test_declared_uv_weight_change_is_a_protected_regression(self):
        before=self.sample()
        before['data_categories']=['uvs','weights']
        for obj in before['objects']:
            obj['data_fingerprints']={'uvs':'1'*64,'weights':'2'*64}
        after=copy.deepcopy(before)
        protected=before['protected_objects'][0]
        next(o for o in after['objects'] if o['name']==protected)['data_fingerprints']['weights']='3'*64
        self.assertIn(protected,handoff_snapshot.compare(before,after)['protected_regressions'])

    def test_missing_or_unknown_category_cannot_pass(self):
        before=self.sample(); before['data_categories']=['uvs']
        with self.assertRaises(check.Violation): handoff_snapshot.validate(before)
        before['data_categories']=['unknown']
        with self.assertRaises(check.Violation): handoff_snapshot.validate(before)


if __name__=='__main__': unittest.main()
