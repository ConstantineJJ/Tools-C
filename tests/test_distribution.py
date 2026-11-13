"""Distribution independence and public catalog regression checks."""
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import bootstrap
import check

class DistributionTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='tools-c distribution ')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / 'pack'
        # A relocated distribution must work without development state or personal bindings.
        def ignore(directory, names):
            omitted = {'.git', '.local', '__pycache__'}
            relative = Path(directory).relative_to(check.ROOT)
            if relative == Path('.'):
                omitted.update({'AGENTS.md', 'Project-pulse.md', 'PatchesAB_fix.md', 'reports', 'tasks'})
            elif relative == Path('docs'):
                omitted.update(name for name in names if name.startswith('release-'))
                omitted.add('blender-domain-skill-pack.md')
            elif relative == Path('plugins/tools-c'):
                omitted.add('.app.json')
            return omitted.intersection(names)
        shutil.copytree(check.ROOT, self.root, ignore=ignore)
        environment = patch.dict(os.environ, {'TOOLS_C_ROOT': str(self.root)})
        environment.start()
        self.addCleanup(environment.stop)

    def test_relocated_canonical_sources_are_self_contained(self):
        manifest=check.read_json(self.root/'manifest.json')
        for owner in manifest['skills']:
            self.assertTrue((self.root/owner['path']).is_file(),owner['id'])
        self.assertFalse(check.run(self.root, self.root).failed)

    def test_all_owners_need_actual_catalog_links_even_with_literal_paths(self):
        path = self.root / 'docs/skills.md'
        target = '../skills/production-mechanic-gym/SKILL.md'
        path.write_text(path.read_text(encoding='utf-8').replace('(' + target + ')', '(../README.md)')
                        + '\n' + chr(96) + target + chr(96) + '\n', encoding='utf-8')
        result = check.run(self.root, self.root)
        self.assertTrue(any(item['rule'] == 'TOOLS-CATALOG-ROUTES'
                            and item['status'] == 'FAIL' and item['code'] == 'E_ROUTE'
                            for item in result.results), result.results)

    def test_project_bootstrap_points_at_the_distributed_catalog(self):
        target = self.root.parent / 'consumer'
        target.mkdir()
        bootstrap.install(target, 'generic')
        block = (target / 'AGENTS.md').read_text(encoding='utf-8')
        self.assertIn("folder's docs/skills.md catalog", block)
        self.assertNotIn("folder's AGENTS.md", block)
        self.assertFalse(check.run(target, self.root).failed)

    def test_plugin_source_has_no_dangling_private_connection(self):
        plugin = self.root / 'plugins/tools-c'
        portable = check.read_json(plugin / 'plugin.json')
        compatibility = check.read_json(plugin / '.codex-plugin/plugin.json')
        self.assertFalse((plugin / '.app.json').exists())
        self.assertNotIn('apps', portable['extensions']['com.openai'])
        self.assertNotIn('apps', compatibility)
        self.assertEqual(portable['name'], compatibility['name'])
        self.assertEqual(portable['version'], compatibility['version'])
        for field in ('logo', 'composerIcon'):
            self.assertTrue((plugin / portable['extensions']['com.openai']['interface'][field]).is_file())

if __name__ == '__main__':
    unittest.main()
