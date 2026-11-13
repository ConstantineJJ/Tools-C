"""Real Git fixtures for preserving working-tree sources, including untracked code."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import source_bundle as bundle
from check import Violation


class SourceBundleTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='source bundle ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base/'repo'
        self.repo.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.write('tracked.cs', b'HEAD\r\n')
        self.write('deleted.cs', b'deleted\n')
        self.write('.gitignore', b'bin/\n.env\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')
        self.write('tracked.cs', b'INDEX\r\n')
        self.git('add', 'tracked.cs')
        self.write('tracked.cs', b'WORKTREE\r\n')
        self.write('apps/Класс с пробелом.cs', b'untracked\x00bytes\r\n')
        (self.repo/'deleted.cs').unlink()
        self.write('bin/app.dll', b'ignored build output')
        self.write('.env', b'PRIVATE_CANARY')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], stderr=subprocess.STDOUT)

    def write(self, name, data):
        p = self.repo/name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)

    def test_inventory_distinguishes_head_index_worktree_and_untracked(self):
        result = bundle.inventory(self.repo)
        rows = {r['path']: r for r in result['files']}
        self.assertEqual(rows['tracked.cs']['status'], 'MM')
        self.assertNotEqual(rows['tracked.cs']['head'], rows['tracked.cs']['index'])
        self.assertEqual(rows['apps/Класс с пробелом.cs']['origin'], 'untracked')
        self.assertEqual(rows['deleted.cs']['status'], ' D')
        self.assertNotIn('.env', rows)
        self.assertNotIn('bin/app.dll', rows)

    def test_capture_keeps_working_bytes_and_deletions_without_staging(self):
        before = self.git('status', '--porcelain=v1', '-z')
        index = (self.repo/'.git/index').read_bytes()
        output = self.base/'bundle'
        bundle.capture(self.repo, ['tracked.cs', 'deleted.cs', 'apps/Класс с пробелом.cs'], output)
        self.assertEqual((output/'source/tracked.cs').read_bytes(), b'WORKTREE\r\n')
        self.assertEqual((output/'source/apps/Класс с пробелом.cs').read_bytes(), b'untracked\x00bytes\r\n')
        self.assertFalse((output/'source/deleted.cs').exists())
        self.assertFalse((output/'source/.env').exists())
        self.assertEqual(index, (self.repo/'.git/index').read_bytes())
        self.assertEqual(before, self.git('status', '--porcelain=v1', '-z'))
        self.assertEqual(bundle.verify(output, project=self.repo)['status'], 'SOURCE_BUNDLE_PASS')

    def captured(self):
        output = self.base/'bundle'
        bundle.capture(self.repo, ['tracked.cs', 'deleted.cs', 'apps/Класс с пробелом.cs'], output)
        return output

    def error(self, code, fn, *args, **kwargs):
        with self.assertRaises(Violation) as raised:
            fn(*args, **kwargs)
        self.assertEqual(raised.exception.code, code)

    def resign(self, output, change):
        p = output/'manifest.json'
        manifest = json.loads(p.read_text())
        change(manifest)
        manifest.pop('manifest_sha256')
        manifest['manifest_sha256'] = bundle.digest(bundle.canonical(manifest))
        p.write_text(json.dumps(manifest), encoding='utf-8')

    def test_head_or_index_never_replaces_missing_working_file(self):
        self.git('rm', '-q', 'deleted.cs')
        output = self.base/'deleted'
        bundle.capture(self.repo, ['deleted.cs'], output)
        self.assertFalse((output/'source/deleted.cs').exists())
        self.assertEqual(json.loads((output/'manifest.json').read_text())['files'][0]['state'], 'absent')

    def test_existing_bundle_is_never_overwritten(self):
        output = self.captured()
        before = (output/'manifest.json').read_bytes()
        self.error('E_OUTPUT', bundle.capture, self.repo, ['tracked.cs'], output)
        self.assertEqual(before, (output/'manifest.json').read_bytes())

    def test_ignored_unknown_and_directory_allowlist_fail_before_output(self):
        for name in ['.env', 'bin/app.dll', 'missing.cs', 'apps']:
            with self.subTest(name=name):
                self.error('E_SCOPE', bundle.capture, self.repo, [name], self.base/'invalid')
                self.assertFalse((self.base/'invalid').exists())

    def test_unsafe_portable_paths_and_collisions_are_rejected(self):
        for names in [[], ['../outside'], ['/absolute'], ['C:/absolute'], ['a\\b'], ['file:stream'],
                      ['.git/index'], ['A/../b'], ['a//b'], ['file.'], ['file '], ['AUX.txt'],
                      ['a','a'], ['a.cs','A.cs'], ['a','a/b'], ['a\nb'], ['*.cs']]:
            with self.subTest(names=names), self.assertRaises(Violation):
                bundle.capture(self.repo, names, self.base/'unsafe')
            self.assertFalse((self.base/'unsafe').exists())

    def test_output_inside_git_or_through_symlink_is_rejected(self):
        self.error('E_OUTPUT', bundle.capture, self.repo, ['tracked.cs'], self.repo/'output')
        self.assertFalse((self.repo/'output').exists())
        self.error('E_OUTPUT', bundle.capture, self.repo, ['tracked.cs'], self.repo/'.git/unsafe')
        self.assertFalse((self.repo/'.git/unsafe').exists())

    def test_untracked_source_symlink_is_not_followed(self):
        outside = self.base/'private.txt'
        outside.write_text('PRIVATE_CANARY')
        try:
            (self.repo/'linked.cs').symlink_to(outside)
        except OSError as exc:
            self.skipTest('OS does not permit fixture symlinks: '+str(exc))
        self.error('E_PATH', bundle.capture, self.repo, ['linked.cs'], self.base/'link-output')
        self.assertFalse((self.base/'link-output').exists())

    def test_output_and_payload_symlinks_are_rejected(self):
        outside = self.base/'outside'
        outside.mkdir()
        alias = self.base/'alias'
        try:
            alias.symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.skipTest('OS does not permit fixture symlinks: '+str(exc))
        self.error('E_PATH', bundle.capture, self.repo, ['tracked.cs'], alias/'escaped')
        self.assertFalse((outside/'escaped').exists())
        output = self.captured()
        target = output/'source/tracked.cs'
        target.unlink()
        target.symlink_to(self.repo/'tracked.cs')
        self.error('E_PATH', bundle.verify, output)

    def test_capture_budget_failure_leaves_no_output(self):
        with patch.object(bundle, 'MAX_TOTAL', 2):
            self.error('E_LIMIT', bundle.capture, self.repo, ['tracked.cs'], self.base/'large')
        self.assertFalse((self.base/'large').exists())

    def test_source_change_during_capture_never_creates_completion_manifest(self):
        original = bundle.selection
        calls = [0]
        def changing(*args):
            calls[0] += 1
            if calls[0] == 3:
                self.write('tracked.cs', b'concurrent edit')
            return original(*args)
        with patch.object(bundle, 'selection', side_effect=changing):
            self.error('E_STALE', bundle.capture, self.repo, ['tracked.cs'], self.base/'interrupted')
        self.assertFalse((self.base/'interrupted/manifest.json').exists())
        self.error('E_BUNDLE', bundle.verify, self.base/'interrupted')

    def test_stale_selected_bytes_or_index_are_detected_separately_from_payload(self):
        output = self.captured()
        self.write('tracked.cs', b'different working bytes, still MM')
        self.error('E_STALE', bundle.verify, output, project=self.repo)
        self.assertEqual(bundle.verify(output)['status'], 'SOURCE_BUNDLE_PASS')
        self.write('tracked.cs', b'WORKTREE\r\n')
        self.git('add', 'tracked.cs')
        self.error('E_STALE', bundle.verify, output, project=self.repo)

    def test_corrupt_or_extra_payload_and_unexpected_root_file_fail(self):
        output = self.captured()
        self.write('other.cs', b'unrelated source')
        self.error('E_STALE', bundle.verify, output, project=self.repo)
        (output/'source/tracked.cs').write_bytes(b'tampered')
        self.error('E_HASH', bundle.verify, output)
        (output/'source/tracked.cs').write_bytes(b'WORKTREE\r\n')
        (output/'source/extra.cs').write_bytes(b'extra')
        self.error('E_SCOPE', bundle.verify, output)
        (output/'source/extra.cs').unlink()
        (output/'extra.json').write_text('{}')
        self.error('E_SCOPE', bundle.verify, output)

    def test_manifest_paths_and_deleted_metadata_remain_strict_even_if_resigned(self):
        output = self.captured()
        original = (output/'manifest.json').read_bytes()
        mutations = [lambda m: m.update(schema_version=True),
                     lambda m: m.update(extra=True),
                     lambda m: m['files'][0].update(path='../escape'),
                     lambda m: m['files'][1].update(size=1),
                     lambda m: m['project'].update(extra=True),
                     lambda m: m['files'].append(dict(m['files'][0])),
                     lambda m: m['files'][0].update(origin='implicit-HEAD')]
        for change in mutations:
            with self.subTest(change=change):
                (output/'manifest.json').write_bytes(original)
                self.resign(output, change)
                with self.assertRaises(Violation):
                    bundle.verify(output)

    def test_unborn_repo_preserves_untracked_sources(self):
        empty = self.base/'empty'
        empty.mkdir()
        subprocess.check_call(['git','-C',str(empty),'init','-q'])
        (empty/'App.cs').write_bytes(b'new project')
        output = self.base/'unborn'
        bundle.capture(empty, ['App.cs'], output)
        self.assertIsNone(json.loads((output/'manifest.json').read_text())['project']['head'])
        self.assertEqual(bundle.verify(output, project=empty)['status'], 'SOURCE_BUNDLE_PASS')

    def test_cli_is_json_only_and_reports_failures_without_source_bodies(self):
        tool = Path(bundle.__file__).resolve()
        def run(*args):
            result = subprocess.run([sys.executable, str(tool), *args], capture_output=True, text=True)
            self.assertNotIn('PRIVATE_CANARY', result.stdout+result.stderr)
            self.assertNotIn('WORKTREE', result.stdout+result.stderr)
            self.assertNotIn('Traceback', result.stderr)
            self.assertTrue(result.stdout.strip(), 'CLI did not return JSON')
            return result.returncode, json.loads(result.stdout)
        code, result = run('inventory','--project',str(self.repo))
        self.assertEqual(code, 0)
        self.assertEqual(result['kind'], 'source_inventory')
        allowlist = self.base/'allowlist.json'
        allowlist.write_text(json.dumps(['tracked.cs','apps/Класс с пробелом.cs']), encoding='utf-8')
        output = self.base/'cli'
        code, _ = run('capture','--project',str(self.repo),'--allowlist',str(allowlist),'--output',str(output))
        self.assertEqual(code,0)
        code, result = run('verify','--bundle',str(output),'--project',str(self.repo))
        self.assertEqual(code,0)
        self.assertTrue(result['source_checked'])
        allowlist.write_text('[".env"]', encoding='utf-8')
        code, result = run('capture','--project',str(self.repo),'--allowlist',str(allowlist),'--output',str(self.base/'denied'))
        self.assertEqual(code,1)
        self.assertEqual(result['code'],'E_SCOPE')

    def test_verify_does_not_implicitly_open_manifest_source_root(self):
        output = self.captured()
        with patch.object(bundle, 'git', side_effect=AssertionError('Unexpected Git/source access')):
            self.assertEqual(bundle.verify(output)['status'],'SOURCE_BUNDLE_PASS')


if __name__ == '__main__':
    unittest.main()
