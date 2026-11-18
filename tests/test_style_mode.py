import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/visual-reference-reconstruction/scripts'))
import validate_style as vs  # noqa: E402

HASH = 'a' * 64
PACKET = {
    "schema": "style-1", "mode": "STYLE", "task": "Redesign laser after style ref",
    "sources": [{"path": "style.png", "sha256": HASH, "role": "style"},
                {"path": "before.blend", "sha256": HASH, "role": "existing_asset"}],
    "baseline": {"source": "before.blend"},
    "adopt": [{"trait": "ring fins", "source": "style.png"}],
    "reject": [{"trait": "large pedestal base", "reason": "user exclusion"}],
    "user_deltas": [{"requirement": "emitter body purple", "status": "REQUIRED"}],
    "invariants": ["SocketReceiver position"], "gate": "READY"}


class StyleModeTests(unittest.TestCase):
    def packet(self, **changes):
        data = copy.deepcopy(PACKET)
        data.update(changes)
        return data

    def test_valid_packet_passes(self):
        self.assertEqual(vs.validate(self.packet())['status'], 'PASS')

    def test_rejections(self):
        bad = [
            self.packet(dimensions={"length": 1}),                       # geometry claim
            self.packet(sources=[PACKET['sources'][1]], adopt=[{"trait": "x", "source": "before.blend"}]),
            self.packet(adopt=[{"trait": "ring fins", "source": "before.blend"}]),  # cites non-style
            self.packet(reject=[{"trait": "Ring Fins", "reason": "conflict"}]),     # adopted and rejected
            self.packet(baseline=None),                                             # redesign without baseline
            self.packet(invariants=[]),
            self.packet(gate="BLOCKED"),                                            # BLOCKED without notes
            self.packet(user_deltas=[{"requirement": "x", "status": "MAYBE"}]),
        ]
        for packet in bad:
            with self.assertRaises(vs.StyleError, msg=json.dumps(packet)[:120]):
                vs.validate(packet)

    def test_verify_files_checks_hashes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'style.png').write_bytes(b'style')
            (root / 'before.blend').write_bytes(b'blend')
            packet = self.packet()
            packet['sources'][0]['sha256'] = hashlib.sha256(b'style').hexdigest()
            packet['sources'][1]['sha256'] = hashlib.sha256(b'blend').hexdigest()
            self.assertEqual(vs.validate(packet, root, True)['status'], 'PASS')
            (root / 'style.png').write_bytes(b'changed')
            with self.assertRaises(vs.StyleError):
                vs.validate(packet, root, True)
            path = root / 'packet.json'
            path.write_text(json.dumps(packet), encoding='utf-8')
            self.assertEqual(vs.main([str(path), '--verify-files']), 1)


if __name__ == '__main__':
    unittest.main()
