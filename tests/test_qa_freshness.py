"""Freshness MVP decision tests, with real PNG/snapshot bytes in temporary folders."""
import copy
import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import qa_freshness as freshness
import qa_gate as qa


def png(rgba=b'\xff\0\0\xff'):
    def chunk(name, body):
        return struct.pack('>I', len(body)) + name + body + struct.pack('>I', zlib.crc32(name + body) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 1,1,8,6,0,0,0))
            + chunk(b'IDAT', zlib.compress(b'\0'+rgba)) + chunk(b'IEND', b''))


def artifact(root, name, data):
    path = root/name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return dict(path=name, sha256=hashlib.sha256(data).hexdigest())


def snapshot(root, name, *, revision=12, changed=()):
    rows = [dict(name=r, geometry=dict(sha256=hashlib.sha256((r+str(r in changed)).encode()).hexdigest()),
                 data_fingerprints=dict(material_graphs='declared material hash')) for r in ('hair','face','torso','legs')]
    data = dict(schema_version=1, frame=1, fps=24, objects=rows, data_categories=['material_graphs'])
    return dict(revision=revision, verified=True,
                snapshot=artifact(root, name, json.dumps(data).encode()),
                regions={r:[r] for r in ('hair','face','torso','legs')})


def fixture(root):
    images = {'front':dict(id='front', image=artifact(root,'front.png',png()), view='front', phase='AFTER', status='PASS')}
    state = snapshot(root, 'r12.json')
    binding = dict(id='front', capture_series='series-A', captured_at='2026-10-08T10:00:00Z', state='r12',
                   dependencies=dict(hair=[], face=['hair'], torso=[], legs=[]))
    return dict(states={'r12':state}, current='r12', captures=[binding]), images


class FreshnessTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.record, self.images = fixture(self.root)

    def assess(self):
        return freshness.assess(self.record, self.images, root=self.root, verify_artifact=qa.verify_artifact)

    def advance(self, changed=('hair',)):
        self.record['states']['r13'] = snapshot(self.root,'r13.json',revision=13,changed=changed)
        self.record['current'] = 'r13'

    def test_confirmed_current_revision(self):
        self.assertEqual(self.assess()['front']['status'], 'CURRENT')

    def test_region_change_visibility_and_unaffected_reuse(self):
        self.advance()
        result = self.assess()['front']
        self.assertEqual(result['regions'], dict(hair='STALE', face='PARTIAL', torso='CURRENT', legs='CURRENT'))
        self.assertEqual(result['status'], 'PARTIAL')

    def test_fully_stale(self):
        self.advance(('hair','face','torso','legs'))
        self.assertEqual(self.assess()['front']['status'], 'STALE')

    def test_unknown_dependencies_do_not_mean_current(self):
        self.record['captures'][0]['dependencies']['face'] = None
        self.assertEqual(self.assess()['front']['regions']['face'], 'UNKNOWN')

    def test_uncontrolled_changes_require_new_verified_probe(self):
        self.record['states']['r12']['verified'] = False
        self.assertEqual(self.assess()['front']['status'], 'UNKNOWN')

    def test_multiple_views_one_series(self):
        self.images['side'] = dict(self.images['front'], id='side', view='side', image=artifact(self.root,'side.png',png()))
        binding = copy.deepcopy(self.record['captures'][0]); binding['id'] = 'side'
        self.record['captures'].append(binding)
        self.assertEqual([x['status'] for x in self.assess().values()], ['CURRENT','CURRENT'])

    def test_mixed_revisions_in_one_series(self):
        self.advance()
        self.images['side'] = dict(self.images['front'], id='side', view='side', image=artifact(self.root,'side.png',png()))
        binding = copy.deepcopy(self.record['captures'][0]); binding.update(id='side', state='r13')
        self.record['captures'].append(binding)
        result = self.assess()
        self.assertEqual(result['front']['status'], 'PARTIAL')
        self.assertEqual(result['side']['status'], 'CURRENT')

    def test_missing_png(self):
        (self.root/'front.png').unlink()
        self.assertEqual(self.assess()['front']['status'], 'UNKNOWN')

    def test_corrupt_png_even_with_matching_hash(self):
        self.images['front']['image'] = artifact(self.root,'front.png',png()[:-7])
        self.assertEqual(self.assess()['front']['image_integrity'], 'FAIL')

    def test_modified_png_hash(self):
        (self.root/'front.png').write_bytes(png()+b'corrupt')
        self.assertEqual(self.assess()['front']['status'], 'UNKNOWN')

    def test_current_front_does_not_prove_back(self):
        coverage = freshness.sufficient({'hair':dict(views=['back'],criterion='back of head')},self.images,self.assess())
        self.assertEqual(coverage['status'], 'INSUFFICIENT')
        self.assertEqual(coverage['requests'], [dict(region='hair',view='back',action='REQUEST_CAPTURE')])

    def test_timestamp_alone_never_confirms_state(self):
        self.advance()
        self.record['captures'][0]['captured_at'] = '2099-01-01T00:00:00Z'
        self.assertEqual(self.assess()['front']['regions']['hair'], 'STALE')

    def test_same_revision_conflicting_snapshot_is_unknown(self):
        self.advance()
        self.record['states']['r13']['revision'] = 12
        self.assertEqual(self.assess()['front']['status'], 'UNKNOWN')

    def test_snapshot_hash_and_membership_fail_closed(self):
        (self.root/'r12.json').write_text('{}',encoding='utf-8')
        self.assertEqual(self.assess()['front']['status'], 'UNKNOWN')

    def test_no_root_never_current(self):
        result = freshness.assess(self.record,self.images,verify_artifact=qa.verify_artifact)
        self.assertEqual(result['front']['status'], 'UNKNOWN')

    def test_missing_current_region(self):
        self.advance(())
        del self.record['states']['r13']['regions']['face']
        self.assertEqual(self.assess()['front']['regions']['face'], 'UNKNOWN')

    def test_immutable_inputs(self):
        before = copy.deepcopy(self.record)
        self.assess()
        self.assertEqual(before, self.record)


if __name__ == '__main__':
    unittest.main()
