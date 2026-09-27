"""Connect a project to Tools_C without copying canonical knowledge."""
import argparse
import json
import os
import hashlib
import re
from pathlib import Path
import sys

from check import ROOT, Violation, inside, require

START = "<!-- tools-c:begin -->"
END = "<!-- tools-c:end -->"


def block():
    return f'''{START}
## Central tools

Read `.tooling/config.json`: resolve tools_root relative to this project root, or
use TOOLS_C_ROOT. Explicitly read that folder's AGENTS.md and matching skills.
Read `.tooling/profile.md` and `.tooling/profile.json` for local choices/contracts.
Current code and dated project status override historical asset descriptions.
Universal skills stay in Tools_C; local project skills supplement them.
Run the central `check.bat --project "<this project root>"` before completion.
{END}
'''


def merge_agents(original):
    text = original.decode("utf-8-sig")
    require(text.count(START) == text.count(END) and text.count(START) <= 1,
            "Ambiguous AGENTS managed markers; inspect before merging", "E_BOOTSTRAP")
    if START in text:
        require(text.index(START) < text.index(END), "Reversed AGENTS markers", "E_BOOTSTRAP")
        # Preserve all bytes outside the one managed block, including CRLF/BOM.
        start, end = original.index(START.encode()), original.index(END.encode()) + len(END)
        return original[:start] + block().rstrip().encode() + original[end:]
    separator = b"" if not original else (b"\n" if original.endswith(b"\n") else b"\n\n")
    return original + separator + block().encode()


def install(root, kind):
    require(root.is_dir(), f"Project root does not exist: {root}", "E_BOOTSTRAP")
    try:
        relative = os.path.relpath(ROOT, root).replace("\\", "/")
    except ValueError:
        relative = ROOT.as_posix()
    config = dict(schema_version=1, tools_root=relative, profile=".tooling/profile.json")
    slug = re.sub(r"[^a-z0-9]+", "-", root.name.lower()).strip("-")
    slug = slug or hashlib.sha256(root.name.encode()).hexdigest()[:12]
    profile = dict(schema_version=1, id="project-" + slug, review_state="generated_unreviewed",
                   skills=["project-audit", "verification"], contracts=[".tooling/contracts.json"],
                   references=["AGENTS.md", ".tooling/profile.md"])
    required = ["AGENTS.md", ".tooling/config.json", ".tooling/profile.json", ".tooling/profile.md"]
    if kind == "godot":
        require((root / "project.godot").is_file(), "Godot project.godot not found", "E_BOOTSTRAP")
        profile["skills"].append("godot-project")
        profile["adapter"] = {"kind": "godot", "resources": ["project.godot"]}
        required.append("project.godot")
    elif kind == "blender":
        profile["skills"].append("blender-pipeline")
        profile["skills"].append("blender-character-modeling")
    contracts = dict(schema_version=1, id="bootstrap-contract", rules=[
        dict(id="BOOT-FILES", kind="files", paths=required)])
    def encoded(value):
        return (json.dumps(value, indent=2) + "\n").encode()
    files = {".tooling/config.json": encoded(config), ".tooling/profile.json": encoded(profile),
             ".tooling/contracts.json": encoded(contracts),
             ".tooling/profile.md": (f"# {root.name} — replaceable profile\n\n"
                 "Describe current owners, target engine, scope and acceptance evidence here.\n"
                 "Bootstrap protects only declared files; specialize contracts after audit.\n").encode()}
    agents = root / "AGENTS.md"
    original = agents.read_bytes() if agents.exists() else b""
    merged = merge_agents(original)
    # Preflight every output before writing any. Existing profiles remain user-owned.
    for name in files:
        path = root / name
        require(inside(root, path), f"Output escapes project: {path}", "E_BOOTSTRAP")
        require(not path.is_symlink() and not path.parent.is_symlink(), f"Symlink output: {path}", "E_BOOTSTRAP")
        if path.exists():
            require(path.is_file(), f"Output is not a file: {path}", "E_BOOTSTRAP")
    require(not agents.is_symlink(), "AGENTS is a symlink", "E_BOOTSTRAP")
    require(inside(root, agents), "AGENTS escapes project", "E_BOOTSTRAP")
    for name, data in files.items():
        path = root / name
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    if original != merged:
        agents.write_bytes(merged)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--kind", choices=["generic", "godot", "blender"], default="generic")
    args = parser.parse_args()
    try:
        install(args.project.resolve(), args.kind)
        print("PASS BOOTSTRAP: existing profile/contracts preserved; router connected")
    except (Violation, OSError, UnicodeError) as exc:
        print(f"FAIL {getattr(exc, 'code', 'E_IO')}: {exc}")
        sys.exit(1)
