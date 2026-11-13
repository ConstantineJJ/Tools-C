"""Behavioral regressions for architecture audit findings R4/R5/R8/R9."""
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS=Path(__file__).resolve().parents[1]/'tools'
sys.path.insert(0,str(TOOLS))
import blender_jobs
import check
import mcp_runtime
import mcp_capture_response


class ReceiptStorageTests(unittest.TestCase):
    def test_receipts_write_outside_tools_and_survive_process_loss(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'Tools_C';root.mkdir()
            work=Path(directory)/'work'
            with patch.object(blender_jobs,'ROOT',root),patch.dict(os.environ,{'TOOLS_C_WORK_ROOT':str(work)}),patch.object(blender_jobs,'_states',return_value={}):
                state=dict(operation_id='probe',status='running',request_sha256='a'*64)
                blender_jobs._save(state)
                self.assertTrue((work/'operations/probe.json').is_file())
                self.assertEqual(list(root.iterdir()),[])
                self.assertEqual(blender_jobs.operation_status('probe')['status'],'interrupted')
                self.assertEqual(mcp_capture_response.capture_directory(root),work/'captures')

    def test_invalid_work_root_is_rejected_before_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with patch.object(blender_jobs,'ROOT',root):
                for value in (str(root),str(root/'nested'),'relative'):
                    with patch.dict(os.environ,{'TOOLS_C_WORK_ROOT':value}),self.assertRaises(ValueError):
                        blender_jobs._save(dict(operation_id='probe'))
            self.assertEqual(list(root.iterdir()),[])

    def test_legacy_receipt_remains_read_only_and_prevents_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'Tools_C'
            old=root/'.local/operations/prior.json';old.parent.mkdir(parents=True)
            raw=json.dumps(dict(operation_id='prior',status='queued',request_sha256='a'*64))
            old.write_text(raw)
            with patch.object(blender_jobs,'ROOT',root),patch.dict(os.environ,{'TOOLS_C_WORK_ROOT':str(Path(directory)/'work')}),patch.object(blender_jobs,'_states',return_value={}):
                result=blender_jobs.operation_status('prior')
                self.assertEqual(result['status'],'interrupted')
                self.assertEqual(result['request_sha256'],'a'*64)
                self.assertEqual(old.read_text(),raw)
                self.assertFalse((Path(directory)/'work').exists())


class DependencyAndContextTests(unittest.TestCase):
    def test_leaf_validation_has_no_orchestration_back_edges(self):
        parsed=ast.parse((TOOLS/'validation_core.py').read_text())
        imported={n.module for n in ast.walk(parsed) if isinstance(n,ast.ImportFrom)}
        imported|={a.name for n in ast.walk(parsed) if isinstance(n,ast.Import) for a in n.names}
        self.assertFalse(imported & {'check','profile_adapters','read_blender_skill','mcp_runtime','skill_catalog'})
        for order in ('check profile_adapters read_blender_skill','profile_adapters read_blender_skill check',
                      'skill_catalog mcp_runtime','mcp_runtime skill_catalog',
                      'project_review_tasks project_review_impact project_review'):
            result=subprocess.run([sys.executable,'-c',';'.join('import '+m for m in order.split())],
                                  cwd=TOOLS,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)

    def test_robot_contract_fits_default_and_deferred_recipe_can_be_loaded(self):
        task='blender-robot-mechanism-modeling'
        first=mcp_runtime.context(check.ROOT,task)
        self.assertTrue(first['ok'],first['missing_documents'])
        self.assertIn('skills/visual-reference-reconstruction/references/model-contract.md',first['receipts'])
        self.assertLessEqual(sum(len(s['content']) for s in first['skills']),60000)
        self.assertEqual(first['status_scope'],'CONTEXT_DELIVERY')
        self.assertEqual(first['acceptance_status'],'NOT_EVALUATED')
        recipe='docs/blender-evidence.md'
        self.assertIn(recipe,[d['path'] for d in first['conditional_documents']])
        follow=mcp_runtime.context(check.ROOT,task,known_documents=first['receipts'],requested_documents=[recipe])
        self.assertTrue(follow['ok'])
        self.assertIn(recipe,follow['receipts'])


if __name__=='__main__': unittest.main()
