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

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"[A-Za-z][A-Za-z0-9_.-]*\Z")


class Violation(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def require(ok, message, code="E_SCHEMA"):
    if not ok:
        raise Violation(code, message)


def fields(value, required, optional=()):
    require(isinstance(value, dict), "Expected an object")
    require(set(required) <= value.keys(), f"Missing fields: {set(required) - value.keys()}")
    require(value.keys() <= set(required) | set(optional),
            f"Unknown fields: {value.keys() - set(required) - set(optional)}")


def strings(value, nonempty=True):
    require(isinstance(value, list) and (bool(value) or not nonempty), "Expected an array of strings")
    require(all(isinstance(x, str) and x.strip() for x in value), "Expected nonempty strings")
    return value


def identifier(value):
    require(isinstance(value, str) and ID.fullmatch(value), f"Invalid ID: {value!r}")


def read_json(path):
    def pairs(items):
        obj = {}
        for key, value in items:
            require(key not in obj, f"Duplicate JSON key {key!r} in {path}", "E_JSON")
            obj[key] = value
        return obj

    def constant(value):
        raise Violation("E_JSON", f"Non-finite JSON constant {value} in {path}")

    def finite_float(value):
        number = float(value)
        require(math.isfinite(number), f"Non-finite JSON number {value} in {path}", "E_JSON")
        return number

    try:
        return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=pairs,
                          parse_constant=constant, parse_float=finite_float)
    except (ValueError, OSError, UnicodeError) as exc:
        raise Violation("E_JSON", f"{path}: {exc}") from exc


def inside(root, path):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def local_path(root, value, base=None):
    require(isinstance(value, str) and value.strip(), "Path must be a nonempty string")
    # Reject Windows drives, UNC, ADS and ambiguous backslashes on all platforms.
    require(not PureWindowsPath(value).drive and not value.startswith(("/", "\\"))
            and ":" not in value and "\\" not in value and "\0" not in value,
            f"Use a relative forward-slash path: {value}", "E_PATH")
    path = ((base or root) / value).resolve()
    require(inside(root, path), f"Path escapes allowed root: {value}", "E_PATH")
    return path


def existing(root, value):
    path = local_path(root, value)
    require(path.is_file(), f"Required file missing: {value}", "E_FILE")
    return path


class Report:
    def __init__(self):
        self.results = []

    def add(self, status, code, message, rule="system", level="L1"):
        self.results.append(dict(level=level, status=status, code=code, rule=rule, message=message))

    @property
    def failed(self):
        return any(x["status"] == "FAIL" for x in self.results)

    def attempt(self, function, rule="system", severity="FAIL"):
        try:
            function()
        except Violation as exc:
            # Invalid structure/path boundaries always fail, even for advisory rules.
            status = "FAIL" if exc.code in {"E_SCHEMA", "E_PATH", "E_ID", "E_JSON"} else severity
            self.add(status, exc.code, str(exc), rule)
        except (OSError, UnicodeError) as exc:
            self.add("FAIL", "E_IO", str(exc), rule)
        else:
            self.add("PASS", "OK", "Declared check satisfied", rule)


def markdown_links(root, path, required_targets=()):
    """Deliberately bounded Markdown subset; no code spans, anchors or web checks."""
    text = re.sub(r"(?ms)^(`{3,}|~{3,}).*?^\1[^\n]*$", "", path.read_text(encoding="utf-8-sig"))
    text = re.sub(r"`[^`\n]*`", "", text)
    text = re.sub(r"(?s)<!--.*?-->", "", text)
    targets = [(match.group(1), match.start() > 0 and text[match.start()-1] == '!')
               for match in re.finditer(r"\[[^\]\n]*\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)", text)]
    targets += [(target, False) for target in re.findall(r"(?m)^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)", text)]
    routed = set()
    for target, image in targets:
        target = target.strip("<>")
        if target.startswith("#"):
            continue
        uri = urlsplit(target)
        if uri.scheme:
            require(uri.scheme.lower() in {"http", "https", "mailto", "app", "codex", "plugin"},
                    f"{path}: unsupported or absolute local link {target}", "E_PATH")
            continue
        require(not uri.netloc, f"{path}: network path escapes root: {target}", "E_PATH")
        rel = unquote(uri.path)
        if not rel:
            continue
        resolved = local_path(root, rel, path.parent)
        require(resolved.exists(), f"{path.relative_to(root)}: broken local link {target}", "E_LINK")
        if not image:
            routed.add(resolved)
    for target in required_targets:
        resolved = existing(root, target)
        require(resolved in routed, f"{path.relative_to(root)}: missing required local route to {target}", "E_ROUTE")


def json_subset(actual, expected, location='$'):
    """Declarative subset only: mappings recurse; arrays require matching members."""
    require(type(actual) is type(expected), f"{location}: expected {type(expected).__name__}", "E_JSON_VALUE")
    if isinstance(expected, dict):
        for key, value in expected.items():
            require(key in actual, f"{location}: missing required key {key!r}", "E_JSON_VALUE")
            json_subset(actual[key], value, location + '/' + key.replace('~', '~0').replace('/', '~1'))
    elif isinstance(expected, list):
        for member in expected:
            for candidate in actual:
                try:
                    json_subset(candidate, member, location + '/[]')
                except Violation:
                    continue
                break
            else:
                raise Violation('E_JSON_VALUE', f"{location}: missing required member {json.dumps(member, ensure_ascii=False)}")
    else:
        require(actual == expected, f"{location}: expected {expected!r}, got {actual!r}", "E_JSON_VALUE")


def catalog(root):
    manifest = read_json(existing(root, "manifest.json"))
    fields(manifest, ["schema_version", "version", "skills", "blender_aliases"])
    require(type(manifest["schema_version"]) is int and manifest["schema_version"] == 1, "Unknown catalog version")
    require(isinstance(manifest["version"], str) and manifest["version"], "Missing version")
    require(isinstance(manifest["skills"], list) and manifest["skills"], "Empty skills catalog")
    seen, paths = set(), set()
    for item in manifest["skills"]:
        fields(item, ["id", "path"])
        identifier(item["id"])
        require(item["id"] not in seen, f"Duplicate skill ID: {item['id']}", "E_ID")
        seen.add(item["id"])
        path = existing(root, item["path"])
        require(path not in paths, f"Two canonical aliases for {path}", "E_ID")
        paths.add(path)
        text = path.read_text(encoding="utf-8")
        require(text.startswith("---\n"), f"Missing frontmatter: {path}")
        front = text.split("---", 2)[1]
        require(re.search(r"(?m)^name: " + re.escape(item["id"]) + "$", front), f"Skill name differs: {path}")
        require(re.search(r"(?m)^description: \S.+$", front), f"Missing description: {path}")
        require("## Pitfalls / Lessons Learned" in text, f"Missing lessons: {path}")
        if manifest["version"].startswith("4."):
            require("../../docs/foundation.md" in text, f"Missing shared foundation reference: {path}", "E_CATALOG")
            existing(root, "docs/foundation.md")
        require(item["path"] in existing(root, "docs/skills.md").read_text(encoding="utf-8"), f"Unrouted skill: {path}")
    actual = {p.resolve() for p in (root / "skills").rglob("SKILL.md")}
    require(actual == paths, "Unlisted or duplicated canonical SKILL.md in skills tree", "E_CATALOG")
    require(isinstance(manifest["blender_aliases"], dict), "Invalid Blender aliases")
    for alias, item in manifest["blender_aliases"].items():
        identifier(alias)
        fields(item, ["reference", "source_sha256", "source_version"])
        existing(root, item["reference"])
        require(re.fullmatch(r"[0-9a-f]{64}", str(item["source_sha256"])), "Invalid source hash")
        require(isinstance(item["source_version"], str), "Invalid source version")
    lessons = set()
    for path in (root / "skills").rglob("*.md"):
        require(inside(root, path), f"Escaped skill: {path}", "E_PATH")
        text = path.read_text(encoding="utf-8")
        for rule in re.findall(r"(?m)^### ([A-Z][A-Z0-9]*-\d+)\s*$", text):
            require(rule not in lessons, f"Duplicate lesson ID: {rule}", "E_ID")
            lessons.add(rule)
        markdown_links(root, path)
    return manifest


RULE_FIELDS = {
    "files": ([], []), "json": ([], []), "markdown": ([], ["required_targets"]),
    "json_subset": (["expected"], []),
    "text": (["required", "forbidden"], []),
    "sha256": (["expected"], []),
}


def validate_contract(data, seen):
    fields(data, ["schema_version", "id", "rules"])
    require(type(data["schema_version"]) is int and data["schema_version"] == 1, "Unknown contract version")
    identifier(data["id"])
    require(data["id"] not in seen, f"Duplicate contract ID {data['id']}", "E_ID")
    seen.add(data["id"])
    require(isinstance(data["rules"], list) and data["rules"], "Contract rules must not be empty")
    for rule in data["rules"]:
        require(isinstance(rule, dict), "Rule must be object")
        kind = rule.get("kind")
        require(isinstance(kind, str) and kind in RULE_FIELDS, f"Unknown rule kind: {kind!r}")
        extra, optional = RULE_FIELDS[kind]
        fields(rule, ["id", "kind", "paths", *extra], ["severity", *optional])
        identifier(rule["id"])
        require(rule["id"] not in seen, f"Duplicate rule ID {rule['id']}", "E_ID")
        seen.add(rule["id"])
        strings(rule["paths"])
        require(rule.get("severity", "FAIL") in ("FAIL", "WARN"), "Severity must be FAIL or WARN")
        if kind == 'markdown' and 'required_targets' in rule:
            strings(rule['required_targets'])
        if kind == 'json_subset':
            require(len(rule['paths']) == 1 and isinstance(rule['expected'], dict) and rule['expected'],
                    'json_subset needs one path and a nonempty expected object')
            try:
                json.dumps(rule['expected'], allow_nan=False)
            except (TypeError, ValueError):
                raise Violation('E_SCHEMA', 'json_subset expected must contain finite JSON values')
        if kind == "text":
            strings(rule["required"], False)
            strings(rule["forbidden"], False)
            require(rule["required"] or rule["forbidden"], "Empty text check")
        if kind == "sha256":
            require(len(rule["paths"]) == 1 and isinstance(rule["expected"], str)
                    and re.fullmatch(r"[0-9a-f]{64}", rule["expected"]), "sha256 needs one path and lowercase hash")


def check_rule(root, rule):
    for value in rule["paths"]:
        path = existing(root, value)
        kind = rule["kind"]
        if kind == "json":
            read_json(path)
        elif kind == 'json_subset':
            json_subset(read_json(path), rule['expected'], value + '#')
        elif kind == "markdown":
            markdown_links(root, path, rule.get('required_targets', ()))
        elif kind == "text":
            content = path.read_text(encoding="utf-8-sig")
            for token in rule["required"]:
                require(token in content, f"{value}: missing literal {token!r}", "E_TEXT")
            for token in rule["forbidden"]:
                require(token not in content, f"{value}: forbidden literal {token!r}", "E_TEXT")
        elif kind == "sha256":
            require(hashlib.sha256(path.read_bytes()).hexdigest() == rule["expected"],
                    f"{value}: protected content changed", "E_HASH")


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
