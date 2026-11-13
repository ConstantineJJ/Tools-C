"""Read-only L1 contracts. Python 3.10+, standard library only."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PureWindowsPath
import re
import sys
from urllib.parse import unquote, urlsplit

if __name__ == "__main__":
    sys.modules["check"] = sys.modules[__name__]

# Re-export stable public helpers for existing clients.
from validation_core import (
    ROOT, ID, Violation, require, fields,
    strings, identifier, read_json, inside, local_path,
    existing, Report, markdown_links, json_subset, catalog_manifest,
    catalog, RULE_FIELDS, validate_contract, check_rule
)


def load_profile(root, tools_root, config_path=".tooling/config.json"):
    config = read_json(existing(root, config_path))
    fields(config, ["schema_version", "tools_root", "profile"])
    require(type(config["schema_version"]) is int and config["schema_version"] == 1, "Unknown config version")
    require(isinstance(config["tools_root"], str) and config["tools_root"], "Invalid tools_root")
    # This is the only explicit cross-root pointer. Project file paths stay confined.
    configured = os.environ.get("TOOLS_C_ROOT") or config["tools_root"]
    require((root / configured).resolve() == tools_root.resolve(),
            "Configured Tools_C differs from checker location; set TOOLS_C_ROOT or repair config", "E_TOOLS_ROOT")
    profile = read_json(existing(root, config["profile"]))
    fields(profile, ["schema_version", "id", "skills", "contracts", "references"],
           ["adapter", "local_skill_roots", "review_state"])
    if "review_state" in profile:
        require(profile["review_state"] in ("generated_unreviewed", "reviewed"), "Unknown review_state")
    require(type(profile["schema_version"]) is int and profile["schema_version"] == 1, "Unknown profile version")
    identifier(profile["id"])
    for key in ("skills", "contracts", "references"):
        strings(profile[key])
        require(len(profile[key]) == len(set(profile[key])), f"Duplicate {key}", "E_ID")
    for ref in profile["references"]:
        existing(root, ref)
    for directory in strings(profile.get("local_skill_roots", []), False):
        require(local_path(root, directory).is_dir(), f"Missing local skill directory: {directory}", "E_FILE")
    return profile


def run(root, tools_root=ROOT):
    report = Report()
    state = {}
    report.attempt(lambda: state.update(manifest=catalog(tools_root)), "TOOLS-CATALOG")
    report.attempt(lambda: state.update(profile=load_profile(root, tools_root)), "PROJECT-PROFILE")
    if report.failed:
        return report
    profile = state["profile"]
    if profile.get("review_state") != "reviewed":
        report.add("WARN", "W_UNREVIEWED", "Profile/contracts review not confirmed; inspect and specialize "
                   "them, then explicitly set review_state to reviewed", "PROJECT-REVIEW")
    known = {s["id"] for s in state["manifest"]["skills"]}
    report.attempt(lambda: require(set(profile["skills"]) <= known, "Profile references unknown skills", "E_CATALOG"), "PROJECT-ROUTES")
    local_names = set()
    def local_skills():
        for directory in profile.get("local_skill_roots", []):
            for path in local_path(root, directory).rglob("SKILL.md"):
                require(inside(root, path), f"Escaped local skill: {path}", "E_PATH")
                text = path.read_text(encoding="utf-8-sig")
                if "<!-- tools-c-router -->" in text:
                    continue  # Exact generated router integrity is verified by the Blender adapter.
                match = re.search(r"(?m)^name: (.+)$", text)
                require(match, f"Missing skill name: {path}", "E_CATALOG")
                name = match[1].strip()
                require(name not in known | local_names, f"Duplicate canonical skill: {name}", "E_CATALOG")
                local_names.add(name)
    report.attempt(local_skills, "PROJECT-SKILLS")
    contracts, seen = [], set()
    for value in profile["contracts"]:
        def load(value=value):
            data = read_json(existing(root, value))
            validate_contract(data, seen)
            # Validate all paths before executing any contract rule.
            for rule in data["rules"]:
                for path in rule["paths"]:
                    local_path(root, path)
                for target in rule.get('required_targets', ()):
                    local_path(root, target)
            contracts.append(data)
        report.attempt(load, value)
    if not report.failed:
        for contract in contracts:
            for rule in contract["rules"]:
                report.attempt(lambda r=rule: check_rule(root, r), rule["id"], rule.get("severity", "FAIL"))
    if "adapter" in profile:
        from profile_adapters import check_adapter
        report.attempt(lambda: check_adapter(root, tools_root, profile["adapter"]), "PROJECT-ADAPTER")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=ROOT)
    parser.add_argument("--self", action="store_true", help="Check Tools_C itself")
    parser.add_argument("--json", action="store_true", help="Print machine-readable results")
    args = parser.parse_args()
    report = run(ROOT if args.self else args.project.resolve())
    for level, reason in [("L2", "Use tools/engine_check.py; no engine executed by L1"),
                          ("L3", "Runtime/bridge/input behavior requires an explicit task probe"),
                          ("L4", "Visual and engineering review requires recorded evidence")]:
        report.add("SKIP", "NOT_RUN", reason, level=level)
    if args.json:
        print(json.dumps(report.results, ensure_ascii=False, indent=2))
    else:
        for item in report.results:
            print(f"{item['level']} {item['status']} {item['code']} [{item['rule']}] {item['message']}")
        print("SUMMARY " + " ".join(f"{s}={sum(x['status'] == s for x in report.results)}"
                                    for s in ("PASS", "WARN", "FAIL", "SKIP")))
    return int(report.failed)


if __name__ == "__main__":
    sys.exit(main())
