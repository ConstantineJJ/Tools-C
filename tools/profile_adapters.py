"""Profile-selected L1 adapters; no engine operations in the universal core."""
import hashlib
import re

from check import existing, fields, identifier, local_path, read_json, require, strings


def check_adapter(root, tools_root, adapter):
    require(isinstance(adapter, dict), "Adapter must be object")
    kind = adapter.get("kind")
    if kind == "godot":
        fields(adapter, ["kind", "resources"])
        strings(adapter["resources"])
        existing(root, "project.godot")
        pending = [existing(root, ref) for ref in adapter["resources"]]
        visited = set()
        while pending:
            path = pending.pop()
            if path in visited:
                continue
            visited.add(path)
            if path.suffix not in (".tscn", ".tres"):
                continue
            # Only literal ext_resource path values; not a Godot parser or script scanner.
            text = path.read_text(encoding="utf-8-sig")
            for ref in re.findall(r'(?m)^\[ext_resource[^\n]*\bpath="res://([^"\n]+)"', text):
                pending.append(existing(root, ref))
    elif kind == "blender":
        fields(adapter, ["kind", "manifest"], ["mirrors"])
        from read_blender_skill import router
        data = read_json(existing(root, adapter["manifest"]))
        fields(data, ["schema_version", "name", "version", "canonical", "skills"])
        require(type(data["schema_version"]) is int and data["schema_version"] == 1, "Unknown compatibility manifest version")
        require(data["canonical"] is False, "Blender compatibility copy cannot be canonical", "E_CATALOG")
        require(isinstance(data["skills"], list) and data["skills"], "Empty compatibility manifest")
        central = read_json(existing(tools_root, "manifest.json"))["blender_aliases"]
        seen = set()
        for item in data["skills"]:
            fields(item, ["folder", "file", "bytes", "lines", "sha256"])
            identifier(item["folder"])
            require(item["folder"] not in seen, "Duplicate Blender alias", "E_ID")
            seen.add(item["folder"])
            require(item["folder"] in central and item["file"] == "SKILL.md", "Unknown Blender entry")
            path = existing(root, "skills/" + item["folder"] + "/" + item["file"])
            raw = path.read_bytes()
            require(raw.decode("utf-8") == router(tools_root, item["folder"]),
                    f"Router drift: {path}; regenerate from Tools_C", "E_CATALOG")
            require(type(item["bytes"]) is int and type(item["lines"]) is int, "Invalid manifest counts")
            require(len(raw) == item["bytes"] and len(raw.splitlines()) == item["lines"]
                    and hashlib.sha256(raw).hexdigest() == item["sha256"],
                    f"Manifest checksum mismatch: {path}", "E_HASH")
        require(seen == set(central), "Blender alias coverage differs from canonical manifest", "E_CATALOG")
        actual = {p.parent.name for p in local_path(root, "skills").rglob("SKILL.md")}
        require(actual == seen, "Unlisted Blender skill copy", "E_CATALOG")
        for mirror in strings(adapter.get("mirrors", []), False):
            check_adapter(local_path(root, mirror), tools_root,
                          dict(kind="blender", manifest="skills/PIPELINE_MANIFEST.json"))
    else:
        require(False, f"Unknown profile adapter: {kind!r}")
