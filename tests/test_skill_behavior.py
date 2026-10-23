"""Evidence validation is separate from actually running an agent."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import skill_behavior as behavior


class BehaviorTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup); self.root=Path(temp.name)
        (self.root/'rule.md').write_text('new rule', encoding='utf-8')
        (self.root/'old.md').write_text('old rule', encoding='utf-8')
        (self.root/'trace.jsonl').write_text('read rule\ninspect evidence\nwithhold claim\n', encoding='utf-8')

    def trial(self, condition='with-rule', kind='agent'):
        t=behavior.prepare('unreviewed-image',condition,self.root,'verification','rule.md')
        t['run_kind']=kind
        t['environment']={'model':'test-model','harness':'manual-real-agent','settings':{'temperature':0,'budget_unit':'tokens'},'budget':100}
        t['controls']={'fixtures':'1'*64,'tools':'2'*64}
        t['transcript']=dict(path='trace.jsonl',sha256=hashlib.sha256((self.root/'trace.jsonl').read_bytes()).hexdigest())
        t['review']={'status':'REVIEWED','reviewer':'human-reviewer'}
        for i,row in enumerate(t['checkpoints'],1):
            row['status']='PASS'; row['evidence']=[dict(path='trace.jsonl',sha256=t['transcript']['sha256'],line=i)]
        if condition=='baseline':
            t['rule']['path']='old.md';t['rule']['sha256']=hashlib.sha256((self.root/'old.md').read_bytes()).hexdigest()
        return t

    def test_prepared_trial_is_not_a_behavioral_pass(self):
        result=behavior.evaluate(behavior.prepare('unreviewed-image','with-rule',self.root,'verification','rule.md'),self.root)
        self.assertEqual(result['behavioral_status'],'SKIP')

    def test_offline_cannot_become_agent_pass(self):
        self.assertEqual(behavior.evaluate(self.trial(kind='offline'),self.root)['behavioral_status'],'SKIP')

    def test_reviewed_observations_are_explicitly_attested_not_inferred(self):
        result=behavior.evaluate(self.trial(),self.root)
        self.assertEqual(result['evidence_status'],'PASS')
        self.assertEqual(result['behavioral_status'],'PASS')
        self.assertIn('reviewer',result['limits'])

    def test_pair_requires_same_settings_budget_and_controls_but_different_rule(self):
        a=self.trial('baseline'); b=self.trial()
        self.assertEqual(behavior.compare(a,b,self.root)['status'],'PASS')
        for field,value in [('budget',99),('model','other'),('harness','other'),('settings',{'temperature':1})]:
            changed=copy.deepcopy(b);changed['environment'][field]=value
            self.assertEqual(behavior.compare(a,changed,self.root)['status'],'SKIP')
        same=copy.deepcopy(a);same['condition']='with-rule'
        self.assertEqual(behavior.compare(a,same,self.root)['status'],'SKIP')

    def test_missing_wrong_or_stale_trace_evidence_is_not_pass(self):
        for mutation in ['hash','line','evidence','review']:
            t=self.trial()
            if mutation=='hash':t['transcript']['sha256']='0'*64
            if mutation=='line':t['checkpoints'][0]['evidence'][0]['line']=999
            if mutation=='evidence':t['checkpoints'][0]['evidence']=[]
            if mutation=='review':t['review']['status']='NOT_RUN'
            self.assertNotEqual(behavior.evaluate(t,self.root)['behavioral_status'],'PASS')

    def test_declared_violation_and_invalid_paths_fail(self):
        t=self.trial();t['checkpoints'][0]['status']='FAIL'
        self.assertEqual(behavior.evaluate(t,self.root)['behavioral_status'],'FAIL')
        t=self.trial();t['rule']['path']='../outside'
        self.assertEqual(behavior.evaluate(t,self.root)['evidence_status'],'FAIL')

    def test_invalid_pair_evidence_is_failure_in_report_and_cli(self):
        for side in ['baseline', 'with_rule']:
            for mutation in ['hash', 'path', 'schema']:
                with self.subTest(side=side, mutation=mutation):
                    trials = dict(baseline=self.trial('baseline'), with_rule=self.trial())
                    invalid = trials[side]
                    if mutation == 'hash': invalid['transcript']['sha256'] = '0'*64
                    if mutation == 'path': invalid['rule']['path'] = '../outside'
                    if mutation == 'schema': invalid['unexpected'] = 'PRIVATE_CANARY'
                    report = behavior.compare(trials['baseline'], trials['with_rule'], self.root)
                    self.assertEqual(report['status'], 'FAIL')
                    self.assertEqual(report['evidence_status'], 'FAIL')
                    self.assertEqual(report[side]['behavioral_status'], 'SKIP')
                    self.assertFalse(report['comparable'])
                    self.assertFalse(report['improvement_observed'])
                    for name, trial in trials.items():
                        (self.root/(name+'.json')).write_text(json.dumps(trial), encoding='utf-8')
                    cli = subprocess.run([sys.executable, str(Path(behavior.__file__)), 'compare',
                        str(self.root/'baseline.json'), str(self.root/'with_rule.json'), '--root', str(self.root)],
                        capture_output=True, text=True)
                    self.assertEqual(cli.returncode, 2, cli.stderr)
                    self.assertEqual(json.loads(cli.stdout)['evidence_status'], 'FAIL')
                    self.assertNotIn('PRIVATE_CANARY', cli.stdout+cli.stderr)

    def test_reviewed_partial_failure_survives_incomplete_run(self):
        trial = self.trial()
        trial['checkpoints'][0]['status'] = 'FAIL'
        trial['checkpoints'][-1].update(status='NOT_RUN', evidence=[])
        result = behavior.evaluate(trial, self.root)
        self.assertEqual(result['evidence_status'], 'SKIP')
        self.assertEqual(result['behavioral_status'], 'FAIL')
        (self.root/'partial.json').write_text(json.dumps(trial), encoding='utf-8')
        cli = subprocess.run([sys.executable, str(Path(behavior.__file__)), 'review',
            str(self.root/'partial.json'), '--root', str(self.root)], capture_output=True, text=True)
        self.assertEqual(cli.returncode, 2, cli.stderr)
        for mutation in ['offline', 'unreviewed', 'no_evidence', 'invalid_line', 'unknown_environment']:
            with self.subTest(mutation=mutation):
                other = copy.deepcopy(trial)
                if mutation == 'offline': other['run_kind'] = 'offline'
                if mutation == 'unreviewed': other['review']['status'] = 'NOT_RUN'
                if mutation == 'no_evidence': other['checkpoints'][0]['evidence'] = []
                if mutation == 'invalid_line': other['checkpoints'][0]['evidence'][0]['line'] = 999
                if mutation == 'unknown_environment': other['environment']['model'] = None
                self.assertEqual(behavior.evaluate(other, self.root)['behavioral_status'], 'SKIP')

    def test_valid_noncomparable_pair_still_exits_zero(self):
        a, b = self.trial('baseline'), self.trial()
        b['environment']['model'] = 'different-model'
        for name, trial in [('baseline', a), ('with_rule', b)]:
            (self.root/(name+'.json')).write_text(json.dumps(trial), encoding='utf-8')
        cli = subprocess.run([sys.executable, str(Path(behavior.__file__)), 'compare',
            str(self.root/'baseline.json'), str(self.root/'with_rule.json'), '--root', str(self.root)],
            capture_output=True, text=True)
        self.assertEqual(cli.returncode, 0, cli.stderr)
        self.assertEqual(json.loads(cli.stdout)['status'], 'SKIP')

    def test_scenario_ids_are_unique_and_pressure_has_observables(self):
        data=behavior.scenarios();all_ids=[r['id'] for rows in data.values() for r in rows]
        self.assertEqual(len(all_ids),len(set(all_ids)))
        self.assertGreaterEqual(len(data['pressure']),2)


if __name__=='__main__': unittest.main()
