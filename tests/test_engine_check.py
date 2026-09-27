"""Resolution fixtures use mocks; these are not live engine/MCP acceptance."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import engine_check as engine
from check import Violation


class EngineResolutionTest(unittest.TestCase):
    def test_explicit_then_environment_and_invalid_selection_never_falls_back(self):
        with tempfile.TemporaryDirectory(prefix='engine fixtures ') as folder:
            binary = Path(folder) / 'binary.exe'
            binary.touch()
            for kind in ('godot', 'blender'):
                with patch.dict(os.environ, {'TOOLS_C_' + kind.upper(): str(binary)}):
                    self.assertEqual(engine.resolve_engine(kind, 'auto')[0], binary.resolve())
                    self.assertEqual(engine.resolve_engine(kind, str(binary))[1], 'explicit argument')
                    with self.assertRaises(Violation):
                        engine.resolve_engine(kind, str(binary) + '.missing')
                    self.assertIsNone(engine.resolve_engine(kind, None)[0])
                with patch.dict(os.environ, {'TOOLS_C_' + kind.upper(): str(binary) + '.missing'}):
                    with self.assertRaises(Violation):
                        engine.resolve_engine(kind, 'auto')

    @unittest.skipUnless(os.name == 'nt', 'Windows versioned installation discovery')
    def test_newest_blender_install_precedes_stale_path(self):
        with tempfile.TemporaryDirectory() as folder:
            for version in ('5.1', '5.2', '5.10'):
                binary = Path(folder) / 'Blender Foundation' / ('Blender ' + version) / 'blender.exe'
                binary.parent.mkdir(parents=True)
                binary.touch()
            candidates = list(Path(folder).glob('Blender Foundation/*/blender.exe'))
            with patch.dict(os.environ, {'TOOLS_C_BLENDER': ''}), \
                 patch('engine_check.windows_blender_candidates', return_value=candidates), \
                 patch('engine_check.engine_identity', side_effect=lambda kind, path, source:
                       {'version': path.parent.name.split()[1]}), \
                 patch('engine_check.shutil.which', return_value='stale/blender.exe') as which:
                path, source = engine.resolve_engine('blender', 'auto')
                self.assertEqual(path.parent.name, 'Blender 5.10')
                which.assert_not_called()

    def test_path_fallback_and_missing_engine(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.dict(os.environ, {'TOOLS_C_BLENDER': '', 'TOOLS_C_GODOT': ''}), \
                 patch('engine_check.windows_blender_candidates', return_value=[]):
                for kind in ('blender', 'godot'):
                    with patch('engine_check.shutil.which', return_value=str(Path(folder) / kind)):
                        self.assertEqual(engine.resolve_engine(kind, 'auto')[1], 'PATH fallback')
                    with patch('engine_check.shutil.which', return_value=None):
                        self.assertIsNone(engine.resolve_engine(kind, 'auto')[0])

    def test_identity_records_real_path_and_version_or_fails(self):
        for kind, output, expected in [('blender', 'Blender 5.2.0\nbuild date', '5.2.0'),
                                       ('godot', '4.7.2.stable.steam.id\n', '4.7.2.stable.steam.id')]:
            with patch('engine_check.subprocess.run', return_value=subprocess.CompletedProcess([], 0, output, '')):
                info = engine.engine_identity(kind, Path('binary.exe'), 'fixture')
                self.assertEqual(info['version'], expected)
                self.assertEqual(info['executable'], 'binary.exe')
            with patch('engine_check.subprocess.run', return_value=subprocess.CompletedProcess([], 0, 'unknown', '')):
                with self.assertRaises(Violation):
                    engine.engine_identity(kind, Path('binary.exe'), 'fixture')

    def test_errors_nonzero_and_missing_marker_never_pass(self):
        for code, output in [(1, 'MARK'), (0, ''), (0, 'MARK\nERROR: bad'),
                             (0, 'MARK\nTraceback (most recent call last):'), (0, 'MARK\nError: Python: bad')]:
            self.assertFalse(engine.evaluate(code, output, 'MARK')[0])

    def test_probe_records_command_and_detects_real_child_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            command = [sys.executable, '-c', "print('MARK'); print('ERROR: fixture'); exit(0)"]
            row = engine.probe(command, 'MARK', Path(folder) / 'probe.log')
            self.assertEqual(row['status'], 'FAIL')
            self.assertEqual(row['command'], command)
            self.assertEqual(row['exit_code'], 0)

    def test_invalid_explicit_cli_returns_failure(self):
        result = subprocess.run([sys.executable, str(engine.ROOT / 'tools/engine_check.py'),
                                 '--project', str(engine.ROOT), '--blender', 'missing-engine.exe'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Configured blender executable missing', result.stdout)
