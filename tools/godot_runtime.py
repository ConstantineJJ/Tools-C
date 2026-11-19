"""Command builders and evidence summaries for the Godot L2/L3/L4 probes.

Pure helpers: they build argument lists and read output folders. They never launch an
engine themselves; engine_check.probe() does, so every run shares one log/marker rule.
"""
import hashlib
import json
from pathlib import Path

from check import ROOT, Violation, existing

PROBES = ROOT / "tools/probes"
SCENARIO_ASSERT_KEYS = {"at_frame", "node", "exists", "property", "op", "value", "tolerance"}


def parse_gate_command(godot, root, skips=(), include_imported=False):
    extra = [f"--skip={s}" for s in skips] + (["--include-imported"] if include_imported else [])
    return [str(godot), "--headless", "--path", str(root), "--script",
            str(PROBES / "godot_parse_gate.gd"), *(["--", *extra] if extra else [])]


def validate_scenario(root, scenario):
    """Static check so a typo cannot make a scenario silently assert nothing."""
    path = existing(root, scenario) if not Path(scenario).is_absolute() else Path(scenario)
    if not path.is_file():
        raise Violation("E_PATH", f"Scenario file missing: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise Violation("E_SCENARIO", f"Scenario is not valid JSON: {exc}")
    if not isinstance(data, dict) or not str(data.get("scene", "")).startswith("res://"):
        raise Violation("E_SCENARIO", "Scenario needs a res:// scene")
    if int(data.get("frames", 0)) < 1:
        raise Violation("E_SCENARIO", "Scenario needs frames >= 1")
    assertions = data.get("assertions", [])
    if not assertions:
        raise Violation("E_SCENARIO", "Scenario has no assertions; it would prove only that the scene loads")
    for item in assertions:
        unknown = set(item) - SCENARIO_ASSERT_KEYS
        if unknown:
            raise Violation("E_SCENARIO", f"Unknown assertion keys {sorted(unknown)}")
        if int(item.get("at_frame", 0)) >= int(data["frames"]):
            raise Violation("E_SCENARIO", f"Assertion at_frame {item.get('at_frame')} is never reached")
    return path, data


def scenario_command(godot, root, scenario_path, capture_dir=None, fps=30):
    """Headless scenario run, or a rendered run that also writes a PNG sequence.

    Capture needs a real renderer, so it is not --headless. The movie is a PNG sequence
    (no encoder dependency). Frame count follows the scenario length at fixed fps.
    """
    base = [str(godot)]
    if capture_dir is None:
        base.append("--headless")
    else:
        capture_dir.mkdir(parents=True, exist_ok=True)
        base += ["--write-movie", str(capture_dir / "frame.png"), "--fixed-fps", str(fps)]
    return base + ["--path", str(root), "--script", str(PROBES / "godot_scenario.gd"),
                   "--", f"--scenario={scenario_path}"]


def capture_summary(capture_dir):
    """Honest facts about a frame sequence. It cannot judge whether the picture is right."""
    frames = sorted(capture_dir.glob("frame*.png"))
    if not frames:
        return dict(frames=0, distinct=0, samples=[])
    hashes = [hashlib.sha256(f.read_bytes()).hexdigest() for f in frames]
    picks = sorted({0, len(frames) // 2, len(frames) - 1})
    return dict(frames=len(frames), distinct=len(set(hashes)),
                first_equals_last=hashes[0] == hashes[-1],
                samples=[str(frames[i]) for i in picks])
