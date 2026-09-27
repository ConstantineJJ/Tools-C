"""Explicit bounded engine probes. L1 never launches an engine implicitly."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

from check import ROOT, Violation, existing, require


def windows_blender_candidates():
    """Bounded installed-app discovery; no drive scan or launcher/deployment mutation."""
    import winreg
    base = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Blender Foundation"
    paths = set(base.glob("Blender */blender.exe"))
    key_name = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        for view in (winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY):
            try:
                with winreg.OpenKey(hive, key_name, 0, winreg.KEY_READ | view) as parent:
                    for index in range(winreg.QueryInfoKey(parent)[0]):
                        try:
                            with winreg.OpenKey(parent, winreg.EnumKey(parent, index)) as key:
                                name = winreg.QueryValueEx(key, "DisplayName")[0]
                                if re.fullmatch(r"Blender(?: \d.*)?", name):
                                    location = winreg.QueryValueEx(key, "InstallLocation")[0]
                                    if location:
                                        paths.add(Path(location) / "blender.exe")
                        except OSError:
                            continue
            except OSError:
                continue
    return sorted({p.resolve() for p in paths if p.is_file()}, key=str)


def resolve_engine(engine, requested):
    """Opt-in only. An invalid explicit selection must never fall back silently."""
    if requested is None:
        return None, "Engine not requested"
    configured = requested if requested != "auto" else os.environ.get("TOOLS_C_" + engine.upper())
    if configured:
        path = Path(configured).expanduser().resolve()
        require(path.is_file(), f"Configured {engine} executable missing: {path}", "E_ENGINE")
        return path, "explicit argument" if requested != "auto" else "environment configuration"
    if engine == "blender" and os.name == "nt":
        candidates = []
        for path in windows_blender_candidates():
            info = engine_identity(engine, path, "Windows installed applications")
            version = tuple(map(int, re.match(r"\d+(?:\.\d+)+", info["version"])[0].split('.')))
            candidates.append((version, path))
        if candidates:
            return max(candidates, key=lambda item: item[0])[1], "newest reported version: Windows installed applications"
    for name in (["godot", "godot4"] if engine == "godot" else ["blender"]):
        found = shutil.which(name)
        if found:
            return Path(found).resolve(), "PATH fallback"
    return None, "No executable discovered; supply an explicit path or TOOLS_C_" + engine.upper()


def engine_identity(engine, path, source):
    command = [str(path), "--version"]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace",
                            timeout=15, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    output = result.stdout + "\n" + result.stderr
    pattern = r"(?m)^Blender (\d+\.\d+[^\r\n]*)" if engine == "blender" else r"(?m)^(\d+\.\d+[^\r\n]*)"
    match = re.search(pattern, output)
    require(result.returncode == 0 and match is not None,
            f"Cannot identify {engine} version from {path}: {output[:500]}", "E_ENGINE")
    return dict(executable=str(path), version=match[1], resolution=source)


def evaluate(returncode, output, marker):
    errors = re.findall(r"(?im)^.*(?:SCRIPT ERROR:|\bERROR:|Traceback \(most recent call last\)|Error: Python:).*$", output)
    ok = returncode == 0 and marker in output and not errors
    return ok, errors


def probe(command, marker, log, timeout=120):
    try:
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                                errors="replace", timeout=timeout,
                                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        output = result.stdout + "\n" + result.stderr
        ok, errors = evaluate(result.returncode, output, marker)
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(output, encoding="utf-8")
        return dict(status="PASS" if ok else "FAIL", command=command, exit_code=result.returncode,
                    log=str(log), errors=errors[:20],
                    evidence=[line for line in output.splitlines() if marker in line])
    except subprocess.TimeoutExpired:
        return dict(status="FAIL", reason=f"Probe exceeded {timeout}s; child terminated")
    except OSError as exc:
        return dict(status="FAIL", reason=str(exc))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--godot", nargs="?", const="auto", help="Executable or auto; opt in to headless import")
    parser.add_argument("--blender", nargs="?", const="auto", help="Executable or auto; opt in to factory background probe")
    parser.add_argument("--asset", action="append", default=[], help="Project-relative .glb/.gltf/.blend for Blender")
    parser.add_argument("--runtime-scene", help="Explicit res:// scene-load smoke; no input/visual acceptance")
    parser.add_argument("--logs", type=Path, default=ROOT / ".local/engine")
    args = parser.parse_args()
    root = args.project.resolve()
    rows = []
    try:
        assets = [str(existing(root, path)) for path in args.asset]
        godot, godot_source = resolve_engine("godot", args.godot)
        blender, blender_source = resolve_engine("blender", args.blender)
        if godot:
            identity = engine_identity("godot", godot, godot_source)
            existing(root, "project.godot")
            row = probe([str(godot), "--headless", "--path", str(root), "--editor", "--import"],
                        "Godot Engine v", args.logs / "godot-import.log")
            rows.append(dict(level="L2", engine="godot", **identity, **row))
            if args.runtime_scene and row["status"] == "PASS":
                if not args.runtime_scene.startswith("res://"):
                    raise Violation("E_PATH", "Runtime scene must use res://")
                existing(root, args.runtime_scene[6:])
                rows.append(dict(level="L3", engine="godot", **identity, scope="scene-load smoke only", **probe(
                    [str(godot), "--headless", "--path", str(root), "--script",
                     str(ROOT / "tools/probes/godot_load.gd"), "--", args.runtime_scene],
                    "TOOLS_C_GODOT_RUNTIME ", args.logs / "godot-runtime.log")))
            else:
                rows.append(dict(level="L3", status="SKIP", reason="No runtime scene requested or import failed"))
        else:
            rows += [dict(level="L2", engine="godot", status="SKIP", reason=godot_source),
                     dict(level="L3", status="SKIP", reason=godot_source)]
        if blender:
            identity = engine_identity("blender", blender, blender_source)
            rows.append(dict(level="L2", engine="blender", **identity, **probe(
                [str(blender), "--background", "--factory-startup", "--disable-autoexec",
                 "--python-exit-code", "1", "--python", str(ROOT / "tools/probes/blender_import.py"), "--", *assets],
                "TOOLS_C_BLENDER ", args.logs / "blender-import.log")))
        else:
            rows.append(dict(level="L2", engine="blender", status="SKIP", reason=blender_source))
        rows.append(dict(level="L4", status="SKIP", reason="Headless probes do not provide visual or input/feel acceptance"))
    except (Violation, OSError, subprocess.TimeoutExpired) as exc:
        rows.append(dict(level="L2", status="FAIL", reason=str(exc)))
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return int(any(row["status"] == "FAIL" for row in rows))


if __name__ == "__main__":
    sys.exit(main())
