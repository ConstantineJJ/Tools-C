"""Bounded tests for the read-only Blender bridge RPC health receipt."""
import importlib.util
from pathlib import Path
import queue
import sys
import types
import unittest
from unittest.mock import patch

TOOL = Path(__file__).resolve().parents[1] / "tools" / "blender_bridge_health.py"
spec = importlib.util.spec_from_file_location("blender_bridge_health", TOOL)
health = importlib.util.module_from_spec(spec)
spec.loader.exec_module(health)


def fake_environment(*, timer=True, handler=True, running=True):
    fake = types.ModuleType("bpy")
    function = lambda: None
    hook = lambda arg: None
    state = {"running": running, "queue": queue.Queue()}
    addon = types.SimpleNamespace(process_queue=function, on_blend_load=hook, _state=state)
    fake.context = types.SimpleNamespace(scene=types.SimpleNamespace(name="Agent_Red7"))
    fake.data = types.SimpleNamespace(filepath=r"D:\Desktop\My Labarotory\TESTS\Agent_Red7.blend")
    fake.app = types.SimpleNamespace(timers=types.SimpleNamespace(
        is_registered=lambda callback: timer and callback is function),
        handlers=types.SimpleNamespace(load_post=[hook] if handler else []))
    return fake, addon


class BlenderBridgeHealthTest(unittest.TestCase):
    def test_expected_file_scene_and_queue_pass(self):
        fake, addon = fake_environment()
        with patch.dict(sys.modules, {"bpy": fake, "chatgpt_blender_mcp": addon}):
            result = health.probe(expected_file=fake.data.filepath, expected_scene="Agent_Red7")
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["queued_requests"], 0)

    def test_connection_flag_does_not_hide_dead_timer(self):
        fake, addon = fake_environment(timer=False)
        with patch.dict(sys.modules, {"bpy": fake, "chatgpt_blender_mcp": addon}):
            result = health.probe(expected_file=fake.data.filepath)
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["checks"]["queue_registered"])

    def test_wrong_file_or_scene_fails(self):
        fake, addon = fake_environment()
        with patch.dict(sys.modules, {"bpy": fake, "chatgpt_blender_mcp": addon}):
            self.assertEqual(health.probe(expected_scene="Different")["status"], "FAIL")
            self.assertEqual(health.probe(expected_file=r"D:\fake\other.blend")["status"], "FAIL")

    def test_missing_load_handler_fails_when_reported(self):
        fake, addon = fake_environment(handler=False)
        with patch.dict(sys.modules, {"bpy": fake, "chatgpt_blender_mcp": addon}):
            self.assertFalse(health.probe()["checks"]["load_handler_registered"])


if __name__ == "__main__":
    unittest.main()
