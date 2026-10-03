import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import blender_capture_file as capture
import check
import read_blender_skill
import mcp_capture_response
import struct


class OfflineCaptureTests(unittest.TestCase):
    def test_failed_renderer_records_failure_and_never_claims_visual_acceptance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); source = root / 'candidate.blend'; blender = root / 'blender.exe'
            source.write_bytes(b'unchanged candidate'); blender.write_bytes(b'fixture')
            with patch.object(capture.subprocess, 'run', return_value=type('Process', (), {'returncode': 1})()):
                with self.assertRaises(RuntimeError):
                    capture.capture_file(blender, source, root / 'failure', objects=['Mesh'])
            self.assertEqual(source.read_bytes(), b'unchanged candidate')
            failure = json.loads((root / 'failure/failure.json').read_text(encoding='utf-8'))
            self.assertFalse(failure['ok']); self.assertTrue(failure['source_file_preserved'])
            self.assertFalse((root / 'failure/result.json').exists())

    def test_python_fallback_preserves_plain_responses_and_rejects_foreign_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertIsNone(mcp_capture_response.capture_image(root, dict(ok=True, data=dict(result={'value': 42}))))
            image = root / 'foreign.png'; image.write_bytes(b'foreign')
            response = dict(ok=True, data=dict(result=dict(ok=True, status='VISUAL REVIEW REQUIRED',
                capture_kind='viewport-oriented evidence render', path=str(image))))
            with self.assertRaises(ValueError):
                mcp_capture_response.capture_image(root, response)

    def test_python_fallback_requires_matching_manifest_hash_and_png_dimensions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); folder = root / '.local/captures/probe'; folder.mkdir(parents=True)
            image = folder / 'front.png'
            # Header fixture exercises validation; real rendering is a separate engine gate.
            raw = b'\x89PNG\r\n\x1a\n' + struct.pack('>I', 13) + b'IHDR' + struct.pack('>II', 512, 512) + b'\0' * 120
            image.write_bytes(raw)
            data = dict(ok=True, status='VISUAL REVIEW REQUIRED', capture_kind='viewport-oriented evidence render',
                        path=str(image), resolution=[512, 512], sha256=hashlib.sha256(raw).hexdigest())
            manifest = folder / 'capture.json'; manifest.write_text(json.dumps(data), encoding='utf-8')
            response = dict(ok=True, data=dict(result=data))
            self.assertEqual(mcp_capture_response.capture_image(root, response), raw)
            for changes in (dict(sha256='0' * 64), dict(resolution=[128, 128]), dict(status='VISUAL PASS')):
                bad = dict(data, **changes); manifest.write_text(json.dumps(bad), encoding='utf-8')
                with self.assertRaises(ValueError):
                    mcp_capture_response.capture_image(root, dict(ok=True, data=dict(result=bad)))
            manifest.write_text(json.dumps(dict(data, view='wrong')), encoding='utf-8')
            with self.assertRaises(ValueError):
                mcp_capture_response.capture_image(root, response)

    def test_rejects_reused_output_and_live_view_without_starting_blender(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, blender = root / 'candidate.blend', root / 'blender.exe'
            source.write_bytes(b'fixture'); blender.write_bytes(b'fixture')
            for output, kwargs in ((root, {}), (root / 'new', {'view': 'current'}),
                                   (root / 'new', {'objects': []})):
                args = dict(objects=['Mesh']); args.update(kwargs)
                with patch.object(capture.subprocess, 'run') as run:
                    with self.assertRaises(ValueError):
                        capture.capture_file(blender, source, output, **args)
                    run.assert_not_called()
            self.assertFalse((root / 'new').exists())

    def test_rejects_escaped_artifact_tampering_and_automatic_visual_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / 'image').mkdir()
            image = root / 'image/front.png'; image.write_bytes(b'png fixture')
            data = dict(ok=True, status='VISUAL REVIEW REQUIRED', path=str(image),
                        sha256=hashlib.sha256(image.read_bytes()).hexdigest())
            self.assertEqual(capture.verify_artifact(root, data), image)
            outside = root / 'outside.png'; outside.write_bytes(image.read_bytes())
            for wrong in (dict(data, path=str(outside)), dict(data, sha256='0' * 64),
                          dict(data, status='VISUAL PASS')):
                with self.assertRaises(ValueError):
                    capture.verify_artifact(root, wrong)

    def test_every_domain_and_legacy_entry_loads_the_actual_fallback_recipe(self):
        manifest = check.catalog(check.ROOT)
        owners = [entry['id'] for entry in manifest['skills'] if entry['id'].startswith('blender-')]
        for owner in owners + list(manifest['blender_aliases']):
            with self.subTest(owner=owner):
                content = read_blender_skill.render(check.ROOT, owner)
                self.assertIn('SOURCE: docs/blender-evidence.md', content)
                self.assertIn('tools/blender_capture_file.py --blender', content)
                self.assertIn('A JSON path alone is not visual review.', content)


if __name__ == '__main__':
    unittest.main()
