"""Owner delivery and vehicle metadata acceptance across the existing public helpers."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
import mcp_runtime
import project_review as review
import skill_catalog
import qa_gate
import test_qa_gate as receipt_examples

FIXTURE = ROOT/'tests/fixtures/project_review_vehicle'
INTERFACE = 'docs/project-review.md'
OWNERS = ('project-audit', 'contracts-lint', 'verification', 'production-project-state-gates')


class ReviewIntegrationTest(unittest.TestCase):
    def test_review_purposes_discover_existing_owners(self):
        for query, owner in [('cross-artifact', 'project-audit'), ('traceability', 'contracts-lint'), ('convergence', 'verification')]:
            with self.subTest(query=query):
                result = skill_catalog.search(ROOT, query, 3)
                self.assertEqual(result['results'][0]['name'], owner)
                self.assertIn('metadata', result['results'][0]['matched_in'])

    def test_each_existing_owner_delivers_review_route_without_forcing_full_interface(self):
        for owner in OWNERS:
            with self.subTest(owner=owner):
                result = mcp_runtime.context(ROOT, owner, max_chars=200000)
                self.assertTrue(result['ok'])
                content = '\n'.join(s['content'] for s in result['skills'])
                self.assertIn(INTERFACE, content)
                self.assertNotIn(INTERFACE, [r['path'] for r in result['documents']])

    def test_interface_is_fetchable_with_existing_receipts_and_scope_guards(self):
        initial = mcp_runtime.context(ROOT, 'project-audit', max_chars=200000)
        fetched = mcp_runtime.context(ROOT, 'project-audit', max_chars=200000,
            known_documents=initial['receipts'], requested_documents=[INTERFACE])
        self.assertTrue(fetched['ok'])
        row = next(r for r in fetched['documents'] if r['path']==INTERFACE)
        self.assertEqual(row['status'], 'delivered')
        self.assertEqual(row['sha256'], hashlib.sha256((ROOT/INTERFACE).read_text(encoding='utf-8').encode()).hexdigest())
        retained = mcp_runtime.context(ROOT, 'project-audit', max_chars=200000,
            known_documents=fetched['receipts'], requested_documents=[INTERFACE])
        self.assertEqual(next(r['status'] for r in retained['documents'] if r['path']==INTERFACE), 'retained')
        with self.assertRaises(ValueError):
            mcp_runtime.context(ROOT, 'project-audit', requested_documents=['../outside.md'])

    def test_vehicle_metadata_pass_cannot_close_visual_or_formal_pass0(self):
        result = review.review(FIXTURE, 'review.json', operation='converge')
        requirements = {r['id']:r['status'] for r in result['requirements']}
        self.assertEqual(requirements['VEHICLE-001'], 'PASS')
        self.assertEqual(requirements['VEHICLE-002'], 'OPEN')
        self.assertEqual(requirements['VEHICLE-003'], 'OPEN')
        self.assertEqual(result['acceptance_status'], 'OPEN')
        self.assertEqual(result['visual_status'], 'NOT_EVALUATED')
        self.assertEqual(result['proposed_tasks'], [])

    def test_vehicle_example_cli_preserves_all_fixture_bytes(self):
        before = {p.name:p.read_bytes() for p in FIXTURE.iterdir() if p.is_file()}
        result = subprocess.run([sys.executable, str(ROOT/'tools/project_review.py'), 'converge', 'review.json',
            '--project', str(FIXTURE)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['acceptance_status'], 'OPEN')
        self.assertEqual(before, {p.name:p.read_bytes() for p in FIXTURE.iterdir() if p.is_file()})

    def test_existing_asset_receipt_blocks_uninspected_vehicle_views(self):
        packet = receipt_examples.fixture(profile='ASSET_FINAL', changed=False)
        packet['asset'] = 'synthetic-vehicle-metadata-only'
        for capture in packet['captures']:
            capture.update(status='REVIEW_REQUIRED', reviewer='', observations='Not inspected; synthetic metadata only')
        packet['capabilities']['STATIC_VISUAL'].update(status='REVIEW_REQUIRED', reviewer='',
            observations='No visual review performed', evidence=[])
        result = qa_gate.validate(packet)
        self.assertEqual(result['structure'], 'PASS')
        self.assertNotEqual(result['gate'], 'PASS')

if __name__ == '__main__':
    unittest.main()
