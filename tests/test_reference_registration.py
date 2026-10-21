"""Registration math and real context delivery; Blender side effects use a probe."""
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import blender_reference as refs
import check
import mcp_runtime


class ReferenceRegistrationTest(unittest.TestCase):
    def test_fit_recovers_uniform_scale_rotation_and_translation(self):
        pixels = [(0, 0), (200, 0), (0, 100), (130, 60)]
        a, b = .003 * math.cos(.2), .003 * math.sin(.2)
        world = [(a*x+b*y+.4, b*x-a*y+.2) for x, y in pixels]
        fit = refs.fit_landmarks(pixels, world)
        for key, value in [('a', a), ('b', b), ('tx', .4), ('ty', .2)]:
            self.assertAlmostEqual(fit[key], value)
        self.assertLess(fit['rms_error'], 1e-12)

    def test_incompatible_aspect_ratio_is_reported_without_warping(self):
        fit = refs.fit_landmarks([(0, 0), (100, 0), (0, 100)],
                                  [(0, 0), (2, 0), (0, -1)])
        self.assertGreater(fit['rms_error'], .1)
        self.assertEqual(set(fit), {'a', 'b', 'tx', 'ty', 'scale', 'rms_error', 'errors'})

    def test_invalid_or_degenerate_landmarks_are_rejected(self):
        for p, q in [([(0, 0)]*3, [(0, 0)]*3),
                     ([(0, 0), (1, 0)], [(0, 0), (1, 0)]),
                     ([(0, 0), (1, 0), (0, float('nan'))], [(0, 0)]*3),
                     ([(0, 0), (1, 0), (0, 1)], [(0, 0)]*3),
                     ([(0, 0), (1, 0), (0, 1)], [(0, 0)]*2)]:
            with self.subTest(p=p, q=q), self.assertRaises(ValueError):
                refs.fit_landmarks(p, q)

    def test_views_have_right_handed_camera_basis(self):
        for u, v, n in refs.VIEWS.values():
            cross = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
            self.assertEqual(cross, n)

    def test_cheatsheet_and_animal_recipe_can_be_read_on_demand(self):
        for path in ['skills/blender-pipeline/references/modelling-pass-cheatsheet.md',
                     'skills/blender-pipeline/references/techniques/reference-registration.md',
                     'skills/blender-animal-anthropomorphic-modeling/references/quadruped-checkpoints.md']:
            ctx = mcp_runtime.context(check.ROOT, 'blender-animal-anthropomorphic-modeling',
                                      max_chars=200000, requested_documents=[path])
            self.assertTrue(ctx['ok'], ctx.get('error'))
            self.assertIn(path, ctx['receipts'])


if __name__ == '__main__':
    unittest.main()
