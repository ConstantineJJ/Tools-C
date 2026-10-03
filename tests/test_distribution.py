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
        shutil.copytree(check.ROOT, self.root, ignore=shutil.ignore_patterns('.git', '.local', '__pycache__'))
        environment = patch.dict(os.environ, {'TOOLS_C_ROOT': str(self.root)})
        environment.start()
        self.addCleanup(environment.stop)

    def test_self_checks_work_without_internal_project_artifacts(self):
        for path in ['AGENTS.md', 'Project-pulse.md', 'TOOLS_C_V4_MIGRATION_REPORT.md',
                     'reports', 'docs/releases', 'docs/blender-domain-skill-pack.md']:
            self.assertFalse((self.root / path).exists(), path)
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

if __name__ == '__main__':
    unittest.main()
