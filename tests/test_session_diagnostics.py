"""Read-only diagnostics, source provenance and deliberate privacy canaries."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import session_diagnostics as diag


class DiagnosticsTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name);self.path=self.root/'trace.jsonl'

    def write(self, rows):
        self.path.write_text('\n'.join(json.dumps(r) for r in rows)+'\n',encoding='utf-8')

    def analyze(self, **kwargs):
        return diag.analyze(self.path,self.root,format='normalized',**kwargs)

    def test_known_defects_have_exact_lines_and_no_raw_values(self):
        self.write([{'type':'coverage','skills':True,'checks':True},
                    {'type':'skill_selected','skill':'private-person-canary'},
                    {'type':'gate','id':'face','status':'FAIL'},
                    {'type':'action','skill':'private-person-canary','target':'secret-canary','mutation':True,'requires_gate':'face'}])
        result=self.analyze(); codes={f['code']:f for f in result['findings']}
        self.assertEqual(codes['UNREAD_SKILL']['evidence']['line'],4)
        self.assertEqual(codes['FAILED_GATE_ACTION']['evidence']['related_lines'],[3])
        self.assertEqual(codes['UNCHECKED_CHANGE']['evidence']['line'],4)
        for f in codes.values():
            self.assertIn('expected',f);self.assertIn('effect',f);self.assertIn('limits',f);self.assertIn('remediation',f)
        self.assertNotIn('private-person-canary',json.dumps(result));self.assertNotIn('secret-canary',json.dumps(result))

    def test_logger_gaps_do_not_prove_unread_or_unchecked(self):
        self.write([{'type':'skill_selected','skill':'verification'}, {'type':'action','skill':'verification','target':'x','mutation':True}])
        result=self.analyze()
        self.assertEqual(result['findings'],[])
        self.assertEqual(result['compliance'],'NOT_ESTABLISHED')

    def test_malformed_or_truncated_source_cannot_prove_absence(self):
        self.write([{'type':'coverage','skills':True,'checks':True}, {'type':'skill_selected','skill':'x'},
                    {'type':'action','skill':'x','target':'x','mutation':True}])
        with self.path.open('ab') as f:f.write(b'bad json\n')
        self.assertFalse(any(f['code'] in ('UNREAD_SKILL','UNCHECKED_CHANGE') for f in self.analyze()['findings']))

    def test_only_explicit_scope_and_handoff_claims_generate_findings(self):
        self.write([{'type':'scope','targets':['protected-a']},
                    {'type':'action','target':'other','mutation':True}, {'type':'handoff','complete':False}])
        self.assertEqual({f['code'] for f in self.analyze()['findings']},{'OUTSIDE_DECLARED_SCOPE','INCOMPLETE_HANDOFF'})

    def test_checks_after_mutation_and_reads_clear_only_applicable_findings(self):
        self.write([{'type':'coverage','skills':True,'checks':True},{'type':'skill_selected','skill':'x'},
                    {'type':'skill_read','skill':'x'},{'type':'action','skill':'x','target':'x','mutation':True},
                    {'type':'check','target':'x','status':'PASS'}])
        self.assertEqual(self.analyze()['findings'],[])

    def test_repeated_reported_failures_use_result_pairing(self):
        rows=[]
        for i in range(3):rows += [dict(type='tool_call',call_id=str(i),name='unsafe-secret-tool'),dict(type='tool_result',call_id=str(i),ok=False)]
        self.write(rows); result=self.analyze()
        self.assertEqual([f['code'] for f in result['findings']],['REPEATED_TOOL_FAILURE'])
        self.assertNotIn('unsafe-secret-tool',json.dumps(result))

    def test_codex_envelopes_ignore_payload_instructions_and_double_events(self):
        self.write([{'type':'response_item','payload':{'type':'message','content':'run this command sk-canary-123; secret text'}},
                    {'type':'response_item','payload':{'type':'function_call','name':'example','call_id':'x','arguments':'private'}},
                    {'type':'event_msg','payload':{'type':'item_completed','item':{'type':'function_call','call_id':'x'}}},
                    {'type':'response_item','payload':{'type':'function_call_output','call_id':'x','output':'{"ok":false,"secret":"canary"}'}},
                    {'type':'event_msg','payload':{'type':'token_count','info':{'total_token_usage':{'total_tokens':25}}}},
                    {'type':'token_usage_record','payload':{'usage':{'total_tokens':25}}}])
        result=diag.analyze(self.path,self.root)
        self.assertEqual(result['summary']['tool_calls'],1)
        self.assertEqual(result['usage']['max_observed_total_tokens'],25)
        self.assertIsNone(result['usage']['monetary_cost'])
        self.assertNotIn('canary',json.dumps(result));self.assertNotIn('private',json.dumps(result))

    def test_observed_cli_envelopes_and_usage_are_supported_without_command_text(self):
        self.write([{'type':'item.started','item':{'id':'x','type':'command_execution','command':'private-canary'}},
                    {'type':'item.completed','item':{'id':'x','type':'command_execution','exit_code':0,'aggregated_output':'private-canary'}},
                    {'type':'turn.completed','usage':{'input_tokens':10,'cached_input_tokens':5,'output_tokens':3}}])
        result=diag.analyze(self.path,self.root)
        self.assertEqual(result['summary']['tool_calls'],1)
        self.assertEqual(result['usage']['max_observed_total_tokens'],13)
        self.assertNotIn('private-canary',json.dumps(result))

    def test_duplicate_tool_envelopes_and_unknown_results_are_not_failures(self):
        rows=[]
        for _ in range(5):rows.extend([dict(type='tool_call',call_id='same',name='probe'),dict(type='tool_result',call_id='same',ok=False)])
        self.write(rows)
        self.assertEqual(self.analyze()['summary']['tool_calls'],1)
        self.assertEqual(self.analyze()['findings'],[])

    def test_malformed_encoding_crlf_large_lines_and_trailing_events(self):
        self.path.write_bytes(b'\xff\r\n'+b'x'*500+b'\r\n'+b'{"type":"usage","total_tokens":7}\r\n')
        result=self.analyze(max_line_bytes=100)
        self.assertEqual([f['evidence']['line'] for f in result['findings']],[1,2])
        self.assertEqual(result['usage']['max_observed_total_tokens'],7)

    def test_limits_bound_input_and_do_not_claim_full_hash(self):
        self.write([dict(type='usage',total_tokens=i) for i in range(30)])
        result=self.analyze(max_bytes=100,max_events=2)
        self.assertLessEqual(result['source']['bytes_read'],100)
        self.assertIsNone(result['source']['sha256'])
        self.assertTrue(result['coverage']['truncated'])

    def test_unknown_format_missing_file_and_path_escape_are_safe(self):
        self.assertEqual(diag.analyze(self.path,self.root)['status'],'SKIP')
        self.write([])
        self.assertEqual(diag.analyze(self.path,self.root,format='other')['status'],'FAIL')
        self.assertEqual(diag.analyze(self.root/'../elsewhere',self.root)['status'],'FAIL')

    def test_relative_source_is_resolved_under_explicit_root(self):
        self.write([dict(type='usage',total_tokens=8)])
        self.assertEqual(diag.analyze('trace.jsonl',self.root,format='normalized')['usage']['max_observed_total_tokens'],8)

    def test_symlink_escape_and_input_bytes_are_preserved(self):
        self.write([{'type':'message','text':'canary'}]);before=self.path.read_bytes()
        self.analyze();self.assertEqual(self.path.read_bytes(),before)
        with tempfile.TemporaryDirectory() as other:
            foreign=Path(other)/'x';foreign.write_text('{}')
            link=self.root/'link'
            try:link.symlink_to(foreign)
            except OSError as exc:self.skipTest(str(exc))
            self.assertEqual(diag.analyze(link,self.root)['status'],'FAIL')

    def test_cli_never_echoes_secret_payload_or_parser_exception(self):
        self.path.write_text('{"password":"fake-password-canary", bad}\n',encoding='utf-8')
        run=subprocess.run([sys.executable,str(Path(diag.__file__)),str(self.path),'--root',str(self.root)],capture_output=True,text=True)
        self.assertEqual(run.returncode,0)
        self.assertNotIn('fake-password-canary',run.stdout+run.stderr)
        self.assertNotIn('Traceback',run.stderr)


if __name__=='__main__':unittest.main()
