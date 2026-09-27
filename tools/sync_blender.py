"""Generate compatibility routers or a self-contained, noncanonical offline package."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from check import ROOT, Violation, catalog, inside, read_json, require
from read_blender_skill import render, router


def generate(target, adopt=False, bundle=False, _collect=False):
    central = catalog(ROOT)
    skills = target if bundle else target / "skills"
    if bundle:
        require(not target.exists(), "Bundle output must be a NEW directory", "E_SYNC")
    previous = skills / "PIPELINE_MANIFEST.json"
    require(inside(target, previous) and not previous.is_symlink(), "Manifest escapes target", "E_SYNC")
    old = read_json(previous) if previous.exists() else {}
    folders = [item["folder"] for item in old.get("skills", [])]
    require(len(folders) == len(set(folders)), "Duplicate generated manifest entries", "E_SYNC")
    require(set(folders) <= set(central["blender_aliases"]), "Stale generated manifest entries; review before retiring", "E_SYNC")
    actual = {p.relative_to(skills).as_posix() for p in skills.rglob("SKILL.md")} if skills.exists() else set()
    expected = {alias + "/SKILL.md" for alias in central["blender_aliases"]}
    require(actual <= expected, "Unlisted/stale generated skill files; review before sync", "E_SYNC")
    approved = {item["folder"]: item["sha256"] for item in old.get("skills", [])}
    outputs, rows = {}, []
    for alias, item in central["blender_aliases"].items():
        path = skills / alias / "SKILL.md"
        require(inside(target, path), f"Output escapes target: {path}", "E_SYNC")
        require(not path.is_symlink() and not path.parent.is_symlink(), f"Symlink output: {path}", "E_SYNC")
        if path.exists():
            raw = path.read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            original = adopt and digest == item["source_sha256"]
            managed = b"<!-- tools-c-router -->" in raw and digest == approved.get(alias)
            require(original or managed, f"User edits in {path}; no overwrite", "E_SYNC")
        content = ("<!-- tools-c-generated: do not edit; regenerate from Tools_C -->\n" + render(ROOT, alias)
                   if bundle else router(ROOT, alias)).encode("utf-8")
        outputs[path] = content
        rows.append(dict(folder=alias, file="SKILL.md", bytes=len(content),
                         lines=len(content.splitlines()), sha256=hashlib.sha256(content).hexdigest()))
    data = dict(schema_version=1, name="Tools_C Blender compatibility", version=central["version"], canonical=False, skills=rows)
    outputs[previous] = (json.dumps(data, indent=2) + "\n").encode()
    # Existing legacy server has two lookup locations: SKILLS_DIR and __file__/skills.
    # Mirror only generated routers, never independently editable knowledge.
    if not bundle and (target / "mcp-server/blender_mcp_server.py").is_file():
        outputs.update(generate(target / "mcp-server", _collect=True))
    if _collect:
        return outputs
    # No recursive deletion; only explicitly enumerated, verified files are written.
    for path, raw in outputs.items():
        if path.is_file() and path.read_bytes() == raw:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    print(f"PASS SYNC: {len(rows)} {'generated contexts' if bundle else 'compatibility routers'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--project", type=Path)
    group.add_argument("--bundle", type=Path)
    parser.add_argument("--adopt", action="store_true", help="Migrate only exact audited original skill hashes")
    args = parser.parse_args()
    try:
        generate((args.bundle or args.project).resolve(), args.adopt, args.bundle is not None)
    except (Violation, OSError, UnicodeError) as exc:
        print(f"FAIL {getattr(exc, 'code', 'E_IO')}: {exc}")
        sys.exit(1)
