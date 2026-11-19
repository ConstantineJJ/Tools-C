import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import mcp_runtime  # noqa: E402

ASSET = "godot-asset-integration"
GAME = "godot-gameplay-implementation"
EVID = "godot-runtime-evidence"

CASES = {
    "Import the delivered GLB and verify its skeleton in Godot.": ["blender-export-validation", ASSET],
    "Validate the character in Godot.": [ASSET],
    "Add a dash ability to the player in Godot: new input action and script.": [GAME],
    "Write the player controller script in GDScript.": [GAME],
    "Wire a pickup signal and update the score in Godot.": [GAME],
    "Prove with a headless run in Godot that the move action changes position.": [EVID],
    "Capture frames of the door in Godot.": [EVID],
    "Implement the jump in Godot and run a headless scenario.": [GAME, EVID],
    "Добавь действие прыжка в Godot и проверь сценарием.": ["verification", GAME, EVID],
    "Импортируй GLB в Godot и проверь скелет.": ["verification", "blender-export-validation", ASSET],
}


class GodotRoutingTests(unittest.TestCase):
    def test_godot_routes(self):
        for task, expected in CASES.items():
            with self.subTest(task=task):
                self.assertEqual(mcp_runtime.route_task(task), expected)

    def test_pure_gameplay_does_not_load_blender_owners(self):
        routes = mcp_runtime.route_task("Add a ramp and a controller input action to the Godot player script.")
        self.assertEqual([r for r in routes if r.startswith("blender-")], [])

    def test_parse_review_keeps_verification_and_evidence(self):
        routes = mcp_runtime.route_task("Review this Godot project: run the parse gate and a headless scenario.")
        self.assertEqual(routes, ["verification", EVID])

    def test_review_of_godot_import_stays_verification(self):
        self.assertEqual(mcp_runtime.route_task("Review the imported asset in Godot."), ["verification"])

    def test_explicit_names_still_win(self):
        self.assertEqual(mcp_runtime.route_task("Use godot-runtime-evidence for this."), [EVID])

    def test_blender_plus_godot_keeps_both(self):
        routes = mcp_runtime.route_task("Export the unchanged character as GLB and validate it in Godot.")
        self.assertEqual(routes, ["blender-export-validation", ASSET])


if __name__ == "__main__":
    unittest.main()
