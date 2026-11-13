"""Reference comparison must measure declared comparable evidence, not beauty."""
import copy
import hashlib
import json
from pathlib import Path
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import vision_compare as vision
import mcp_runtime
from validation_core import ROOT


def square(offset=0):
    return [[2+offset <= x < 6+offset and 2 <= y < 6 for x in range(10)] for y in range(8)]


class MaskComparisonTest(unittest.TestCase):
    def test_new_entry_intents_reuse_existing_owners(self):
        self.assertEqual(mcp_runtime.route_task('Tools_C Agent Vision'),['verification'])
        self.assertEqual(mcp_runtime.route_task('Проведи ревью архитектуры Tools_C'),['project-audit'])

    def test_landmarks_keep_occlusion_unknown_and_measure_visible_offsets(self):
        rows=[dict(id='anchor',reference=[1,2],candidate=[4,6],visibility='VISIBLE'),
              dict(id='hidden',reference=None,candidate=None,visibility='OCCLUDED')]
        result=vision.measure_landmarks(rows,[10,8])
        self.assertEqual(result[0]['distance_px'],5)
        self.assertIsNone(result[1]['distance_px'])
    def test_identical_and_shifted_silhouettes(self):
        same = vision.compare_masks(square(), square())
        self.assertEqual(same['iou'], 1)
        self.assertEqual(same['contour_distance_px']['p95'], 0)
        shifted = vision.compare_masks(square(), square(1))
        self.assertAlmostEqual(shifted['iou'], 12/20)
        self.assertEqual(shifted['different_pixels'], 8)
        self.assertEqual(shifted['difference_bbox'], [2, 2, 7, 6])
        self.assertEqual(shifted['contour_distance_px']['p95'], 1)

    def test_degenerate_masks_and_mismatched_dimensions_are_rejected(self):
        for a,b in [([], []), ([[False]], [[False]]), (square(), [[True]]),
                    ([[1]], [[True]]), ([[True], []], [[True], []])]:
            with self.subTest(a=a), self.assertRaises(ValueError):
                vision.compare_masks(a,b)

    def test_oversized_job_is_rejected_before_json_parse(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'job.json';path.write_bytes(b'x'*(1024*1024+1))
            with self.assertRaisesRegex(ValueError,'exceeds'):vision.analyze_job(path)

    def test_png_round_trip_and_contour_overlay(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'mask.png'
            rows = [[(255,255,255,255) if x else (0,0,0,0) for x in row] for row in square()]
            vision.write_png(path, rows)
            self.assertEqual(vision.read_mask(path, 'alpha'), square())
            overlay = vision.overlay(square(), square(1))
            self.assertEqual(len(overlay), 8)
            self.assertNotEqual(overlay[3][2], overlay[3][6])

    def test_rgb_photo_is_not_silently_segmented(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'photo.png'
            vision.write_png(path, [[(255,0,20,255)]])
            with self.assertRaisesRegex(ValueError, 'monochrome'):
                vision.read_mask(path, 'luminance')

    def test_job_hashes_output_containment_and_qa_freshness(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            rows=[[(255,255,255,255) if on else (0,0,0,0) for on in row] for row in square()]
            vision.write_png(root/'mask.png',rows)
            setup={'projection':'ORTHO','camera_matrix':[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
                   'resolution':[10,8],'ortho_scale':4,'lens':50,'shift':[0,0],
                   'sensor':[36,24,'AUTO'],'pixel_aspect':[1,1],'frame':1}
            def artifact(name):return dict(path=name,sha256=hashlib.sha256((root/name).read_bytes()).hexdigest())
            (root/'capture.json').write_text(json.dumps(dict(setup,channel='silhouette',sha256=artifact('mask.png')['sha256'])))
            job=dict(schema_version=1,reference=dict(mask=artifact('mask.png'),source=artifact('mask.png'),mode='alpha',authority='ORIGINAL'),
                     candidate=dict(mask=artifact('mask.png'),capture=artifact('capture.json')),
                     alignment=dict(mode='CALIBRATED',reviewed=True,pose_confirmed=True,reference_setup=setup),thresholds=dict(iou_min=.99))
            path=root/'job.json';path.write_text(json.dumps(job))
            result=vision.compare_job(path,root/'result')
            self.assertEqual(result['status'],'PASS')
            self.assertEqual(vision.verify_comparison(root/'result/comparison.json',root),result)
            import mcp_capture_response
            delivered=vision.capture_comparison(path,root/'captures/diagnostic')
            with patch.dict(os.environ,{'TOOLS_C_WORK_ROOT':str(root)}):
                response=dict(ok=True,data=dict(result=delivered))
                self.assertEqual(mcp_capture_response.capture_image(root/'canonical',response),Path(delivered['path']).read_bytes())
                delivered['status']='PASS'
                with self.assertRaises(ValueError):mcp_capture_response.capture_image(root/'canonical',response)
            # Feed the real result into the existing receipt, with real input files.
            from test_qa_gate import fixture
            import qa_gate
            receipt=fixture(profile='ASSET_FINAL',changed=False)
            for image in receipt['captures']:image['image']=artifact('mask.png')
            check=receipt['checks']['reference_proportions']
            check['comparison']=artifact('result/comparison.json')
            self.assertEqual(qa_gate.validate(receipt,root=root)['gate'],'PASS')
            wrong=copy.deepcopy(receipt)
            vision.write_png(root/'other.png',[[(0,0,0,255)]*10]*8)
            for image in wrong['captures']:image['image']=artifact('other.png')
            with self.assertRaisesRegex(ValueError,'bound'):qa_gate.validate(wrong,root=root)
            with self.assertRaises(ValueError):vision.compare_job(path,root.parent/'escape')
            report=json.loads((root/'result/comparison.json').read_text());report['metrics']['iou']=.5
            (root/'result/comparison.json').write_text(json.dumps(report))
            with self.assertRaisesRegex(ValueError,'changed'):vision.verify_comparison(root/'result/comparison.json',root)
            (root/'mask.png').write_bytes(b'stale')
            with self.assertRaisesRegex(ValueError,'stale'):vision.analyze_job(path)

    def test_calibration_and_generated_views_cannot_manufacture_acceptance(self):
        metrics=vision.compare_masks(square(), square())
        setup={'projection':'ORTHO','camera_matrix':[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
               'resolution':[10,8], 'ortho_scale':4, 'lens':50, 'shift':[0,0],
               'sensor':[36,24,'AUTO'], 'pixel_aspect':[1,1], 'frame':1}
        alignment={'mode':'CALIBRATED','reviewed':True,'pose_confirmed':True,
                   'reference_setup':setup}
        thresholds={'iou_min':.99,'contour_p95_max_px':.5}
        self.assertEqual(vision.assess(metrics,alignment,setup,'ORIGINAL',thresholds)['status'],'PASS')
        invalid=copy.deepcopy(alignment);invalid['reviewed']='false'
        self.assertEqual(vision.assess(metrics,invalid,setup,'ORIGINAL',thresholds)['status'],'NOT_COMPARABLE')
        for authority in ('GENERATED_AUXILIARY',):
            self.assertEqual(vision.assess(metrics,alignment,setup,authority,thresholds)['status'],'REVIEW_REQUIRED')
        changed=copy.deepcopy(setup);changed['shift'][0]=.1
        self.assertEqual(vision.assess(metrics,alignment,changed,'ORIGINAL',thresholds)['status'],'NOT_COMPARABLE')
        alignment['mode']='APPROXIMATE'
        self.assertEqual(vision.assess(metrics,alignment,setup,'ORIGINAL',thresholds)['status'],'REVIEW_REQUIRED')


if __name__ == '__main__': unittest.main()
