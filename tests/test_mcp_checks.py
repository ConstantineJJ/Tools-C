"""A thin read-only adapter reuses the existing checker in a bounded process."""
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import mcp_checks


class CheckAdapterTest(unittest.TestCase):
    def test_unregistered_path_is_refused_before_starting_a_process(self):
        with tempfile.TemporaryDirectory() as d, patch('mcp_checks.subprocess.run') as run:
            root=Path(d)/'canonical';root.mkdir()
            result=mcp_checks.run_checks(root,Path(d)/'outside',allowed_projects=[root])
            self.assertEqual(result['code'],'E_PROJECT_ACCESS')
            run.assert_not_called()

    def test_current_checker_is_invoked_without_shell_and_higher_gates_stay_open(self):
        with tempfile.TemporaryDirectory() as d, patch('mcp_checks.subprocess.run') as run:
            root=Path(d);(root/'tools').mkdir();(root/'tools/check.py').write_text('')
            run.return_value.returncode=0
            def execute(*args,**kwargs):
                kwargs['stdout'].write(json.dumps([dict(level='L1',status='PASS',code='OK',rule='fixture',message='ok')]).encode())
                return run.return_value
            run.side_effect=execute
            result=mcp_checks.run_checks(root,root,allowed_projects=[root])
            self.assertTrue(result['ok'])
            self.assertEqual(result['scope'],'L1_READ_ONLY')
            self.assertEqual(result['runtime_status'],'NOT_EVALUATED')
            args,kwargs=run.call_args
            self.assertEqual(args[0][1:],[str(root/'tools/check.py'),'--project',str(root),'--json'])
            self.assertFalse(kwargs.get('shell',False))
            self.assertEqual(kwargs['stdin'],subprocess.DEVNULL)
            self.assertLessEqual(kwargs['timeout'],30)


if __name__ == '__main__': unittest.main()
