"""Builder and validation fixtures only; real-engine behavior is covered by manual lab runs."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import godot_runtime as rt
from check import Violation

GOOD = {"scene": "res://main.tscn", "frames": 30,
        "steps": [{"frame": 1, "action": "press", "name": "go"}],
        "assertions": [{"at_frame": 29, "node": "Box", "property": "position:x", "op": ">", "value": 0}]}


class ScenarioValidationTest(unittest.TestCase):
    def write(self, folder, data):
        path = Path(folder) / "scenario.json"
        path.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
        return path

    def test_valid_scenario_passes(self):
        with tempfile.TemporaryDirectory() as folder:
            path, data = rt.validate_scenario(Path(folder), str(self.write(folder, GOOD)))
            self.assertEqual(data["frames"], 30)
            self.assertTrue(path.is_file())

    def test_scenarios_that_would_prove_nothing_are_rejected(self):
        bad = [
            dict(GOOD, assertions=[]),
            dict(GOOD, frames=0),
            dict(GOOD, scene="main.tscn"),
            dict(GOOD, assertions=[{"at_frame": 30, "node": "Box", "exists": True}]),
            dict(GOOD, assertions=[{"at_frame": 1, "node": "Box", "propery": "x"}]),
            "{not json",
        ]
        with tempfile.TemporaryDirectory() as folder:
            for case in bad:
                with self.assertRaises(Violation, msg=str(case)):
                    rt.validate_scenario(Path(folder), str(self.write(folder, case)))

    def test_input_action_binding_assertion_is_accepted(self):
        data = dict(GOOD, assertions=[{"at_frame": 1, "input_action": "jump"}])
        with tempfile.TemporaryDirectory() as folder:
            _, loaded = rt.validate_scenario(Path(folder), str(self.write(folder, data)))
            self.assertEqual(loaded["assertions"][0]["input_action"], "jump")

    def test_missing_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(Violation):
                rt.validate_scenario(Path(folder), str(Path(folder) / "none.json"))


class CommandTest(unittest.TestCase):
    def test_parse_gate_command_is_headless_and_forwards_options(self):
        cmd = rt.parse_gate_command("godot", "P", ["res://addons/x/"], True)
        self.assertIn("--headless", cmd)
        self.assertEqual(cmd[cmd.index("--") + 1:], ["--skip=res://addons/x/", "--include-imported"])
        self.assertNotIn("--", rt.parse_gate_command("godot", "P"))

    def test_scenario_command_headless_versus_capture(self):
        headless = rt.scenario_command("godot", "P", "s.json")
        self.assertIn("--headless", headless)
        self.assertNotIn("--write-movie", headless)
        with tempfile.TemporaryDirectory() as folder:
            cap = rt.scenario_command("godot", "P", "s.json", Path(folder) / "out", 24)
            self.assertNotIn("--headless", cap)
            self.assertEqual(cap[cap.index("--fixed-fps") + 1], "24")
            self.assertTrue(cap[cap.index("--write-movie") + 1].endswith("frame.png"))
            self.assertTrue((Path(folder) / "out").is_dir())


class CaptureSummaryTest(unittest.TestCase):
    def test_counts_distinct_frames_and_flags_static_sequences(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)
            self.assertEqual(rt.capture_summary(out)["frames"], 0)
            for index in range(4):
                (out / f"frame{index:08d}.png").write_bytes(b"same")
            summary = rt.capture_summary(out)
            self.assertEqual((summary["frames"], summary["distinct"]), (4, 1))
            self.assertTrue(summary["first_equals_last"])
            (out / "frame00000003.png").write_bytes(b"other")
            summary = rt.capture_summary(out)
            self.assertEqual(summary["distinct"], 2)
            self.assertFalse(summary["first_equals_last"])
            self.assertEqual(len(summary["samples"]), 3)


if __name__ == "__main__":
    unittest.main()
