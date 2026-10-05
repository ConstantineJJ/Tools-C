"""Small deterministic Blender stage snapshot schema and comparison (stdlib)."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re

from check import fields, read_json, require, strings


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def names(value):
    strings(value, False)
    require(value == sorted(set(value)), "Names must be unique and sorted")


def validate(data):
    fields(data, ["schema_version", "stage", "blender_version", "frame", "fps", "objects",
                  "actions", "protected_objects", "blockers", "verification"], ['data_categories'])
    categories=data.get('data_categories',[])
    names(categories)
    require(set(categories)<={'uvs','normals','shape_keys','weights','modifiers','curves','material_graphs'}, 'Unknown protected-data category')
    require(type(data["schema_version"]) is int and data["schema_version"] == 1, "Unknown snapshot schema")
    for key in ("stage", "blender_version"):
        require(isinstance(data[key], str) and bool(data[key].strip()), f"Empty {key}")
    require(number(data["frame"]) and number(data["fps"]) and data["fps"] > 0, "Invalid time base")
    require(isinstance(data["objects"], list), "Objects must be an array")
    object_names = []
    for obj in data["objects"]:
        fields(obj, ["name", "type", "parent", "parent_bone", "matrix_world", "geometry", "bones", "materials"], ['data_fingerprints'])
        fingerprints=obj.get('data_fingerprints',{})
        require(isinstance(fingerprints,dict) and set(fingerprints)==set(categories), 'Declared fingerprints missing or undeclared')
        require(all(isinstance(v,str) and re.fullmatch(r'[0-9a-f]{64}',v) for v in fingerprints.values()), 'Invalid data fingerprint')
        strings([obj["name"], obj["type"]])
        require(obj["parent"] is None or isinstance(obj["parent"], str), "Invalid parent")
        require(isinstance(obj["parent_bone"], str), "Invalid parent bone")
        object_names.append(obj["name"])
        require(isinstance(obj["matrix_world"], list) and len(obj["matrix_world"]) == 16
                and all(number(n) for n in obj["matrix_world"]), "Invalid finite world transform")
        names(obj["materials"])
        geo = obj["geometry"]
        if geo is not None:
            fields(geo, ["vertices", "edges", "polygons", "triangles", "sha256"])
            for key in ("vertices", "edges", "polygons", "triangles"):
                require(type(geo[key]) is int and geo[key] >= 0, "Invalid geometry count")
            require(isinstance(geo["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", geo["sha256"]), "Invalid geometry digest")
        require(isinstance(obj["bones"], list), "Invalid bones")
        bone_names = []
        for bone in obj["bones"]:
            fields(bone, ["name", "parent"])
            strings([bone["name"]]); bone_names.append(bone["name"])
            require(bone["parent"] is None or isinstance(bone["parent"], str), "Invalid bone parent")
        names(bone_names)
        for bone in obj["bones"]:
            require(bone["parent"] is None or bone["parent"] in bone_names, "Missing bone parent")
    names(object_names)
    names(data["protected_objects"])
    require(set(data["protected_objects"]) <= set(object_names), "Protected objects missing from scope")
    strings(data["blockers"], False)
    require(isinstance(data["actions"], list), "Actions must be an array")
    action_names = []
    for action in data["actions"]:
        fields(action, ["name", "range"])
        strings([action["name"]]); action_names.append(action["name"])
        r = action["range"]
        require(isinstance(r, list) and len(r) == 2 and all(number(x) for x in r) and r[0] <= r[1], "Invalid frame range")
    names(action_names)
    verification = data["verification"]
    fields(verification, ["structural", "visual", "evidence", "reason"])
    require(verification["structural"] in ("PASS", "FAIL", "SKIP"), "Invalid structural state")
    require(verification["visual"] in ("PASS", "FAIL", "SKIP", "REVIEW REQUIRED"), "Invalid visual state")
    strings(verification["evidence"], False)
    require(isinstance(verification["reason"], str) and verification["reason"].strip(), "Evidence reason required")
    if verification["visual"] in ("PASS", "FAIL", "REVIEW REQUIRED"):
        require(bool(verification["evidence"]), "Visual judgment needs image evidence references")
    return data


def canonical_bytes(data):
    validate(data)
    return (json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def compare(before, after):
    validate(before); validate(after)
    old = {o["name"]: o for o in before["objects"]}
    new = {o["name"]: o for o in after["objects"]}
    changed = sorted(k for k in old.keys() | new.keys() if old.get(k) != new.get(k))
    protected = sorted(set(changed) & set(before["protected_objects"]))
    return {"changed_objects": changed, "protected_regressions": protected,
            "actions_changed": before["actions"] != after["actions"],
            "comparable_time": before["frame"] == after["frame"] and before["fps"] == after["fps"],
            "data_categories_changed": before.get('data_categories',[])!=after.get('data_categories',[]),
            "limits": "Declared source identity only; omitted categories/resources, export equivalence and visual acceptance are not certified"}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("snapshot", type=Path); p.add_argument("--compare", type=Path)
    args = p.parse_args()
    try:
        data = validate(read_json(args.snapshot))
        result = compare(data, read_json(args.compare)) if args.compare else {"schema": "PASS", "sha256": hashlib.sha256(canonical_bytes(data)).hexdigest()}
        print(json.dumps(result, indent=2))
        raise SystemExit(1 if result.get("protected_regressions") or result.get("comparable_time") is False else 0)
    except Exception as exc:
        print(f"FAIL SNAPSHOT: {exc}"); raise SystemExit(1)
