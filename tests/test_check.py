import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import check
import bootstrap
import read_blender_skill
import sync_blender


class ContractsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="tools c fixture ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.addCleanup(patch.stopall)
        patch.dict(os.environ, {"TOOLS_C_ROOT": str(check.ROOT)}).start()
        bootstrap.install(self.root, "generic")

    def write_contract(self, rules):
        data = dict(schema_version=1, id="fixture", rules=rules)
        (self.root / ".tooling/contracts.json").write_text(json.dumps(data), encoding="utf-8")

    def results(self):
        return check.run(self.root)

    def has_code(self, code):
        self.assertIn(code, [item["code"] for item in self.results().results])

    def test_bootstrap_project_passes(self):
        self.assertFalse(self.results().failed)

    def test_review_state_warns_until_explicitly_reviewed(self):
        path = self.root / '.tooling/profile.json'
        profile = check.read_json(path)
        self.assertEqual(profile['review_state'], 'generated_unreviewed')
        for state in ('generated_unreviewed', None, 'reviewed', 'typo', []):
            with self.subTest(state=state):
                if state is None:
                    profile.pop('review_state')
                else:
                    profile['review_state'] = state
                path.write_text(json.dumps(profile))
                result = self.results()
                self.assertEqual(result.failed, state in ('typo', []))
                self.assertEqual(any(r['code'] == 'W_UNREVIEWED' and r['status'] == 'WARN'
                                     for r in result.results), state in ('generated_unreviewed', None))
        profile['review_state'] = 'reviewed'
        path.write_text(json.dumps(profile))
        self.write_contract([dict(id='missing', kind='files', paths=['missing'])])
        self.assertTrue(self.results().failed)  # Review never bypasses actual checks.

    def test_all_bootstrap_kinds_in_unicode_space_paths(self):
        for kind in ('generic', 'godot', 'blender'):
            target = self.root / ('Новый проект ' + kind)
            target.mkdir()
            if kind == 'godot':
                (target / 'project.godot').write_text('config_version=5')
            bootstrap.install(target, kind)
            report = check.run(target)
            self.assertFalse(report.failed)
            self.assertIn('W_UNREVIEWED', [r['code'] for r in report.results])
            if kind == 'blender':
                profile = check.read_json(target / '.tooling/profile.json')
                self.assertIn('blender-character-modeling', profile['skills'])

    def test_bootstrap_rejects_symlink_before_writing(self):
        with tempfile.TemporaryDirectory() as outside:
            target = self.root / 'new project'
            target.mkdir()
            try:
                (target / '.tooling').symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(str(exc))
            with self.assertRaises(check.Violation):
                bootstrap.install(target, 'generic')
            self.assertFalse((target / 'AGENTS.md').exists())
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_missing_file_fails_and_cli_returns_nonzero(self):
        self.write_contract([dict(id="missing", kind="files", paths=["missing.txt"])])
        self.has_code("E_FILE")
        result = subprocess.run([sys.executable, str(check.ROOT / "tools/check.py"),
                                 "--project", str(self.root), "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any(x["status"] == "FAIL" for x in json.loads(result.stdout)))

    @unittest.skipUnless(os.name == 'nt', 'Windows batch launcher')
    def test_batch_launcher_outside_tools_root_preserves_exit_codes(self):
        command = [str(check.ROOT / 'check.bat'), '--project', str(self.root)]
        good = subprocess.run(command, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(good.returncode, 0)
        self.assertIn('W_UNREVIEWED', good.stdout)
        self.write_contract([dict(id='missing', kind='files', paths=['missing'])])
        bad = subprocess.run(command, cwd=self.root, capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)
        self.assertIn('E_FILE', bad.stdout)

    def test_advisory_failure_warns(self):
        self.write_contract([dict(id="advice", kind="files", paths=["missing"], severity="WARN")])
        report = self.results()
        self.assertFalse(report.failed)
        self.assertIn("WARN", [x["status"] for x in report.results])

    def test_rejects_unknown_kind_and_fields(self):
        for rule in [dict(id="bad", kind="fiels", paths=["AGENTS.md"]),
                     dict(id="bad", kind="files", paths=["AGENTS.md"], typo=True)]:
            with self.subTest(rule=rule):
                self.write_contract([rule])
                self.has_code("E_SCHEMA")

    def test_rejects_structural_types(self):
        for value in [None, [], {}, 2, True]:
            with self.subTest(value=value):
                self.write_contract([dict(id="bad", kind=value, paths=["AGENTS.md"])])
                self.has_code("E_SCHEMA")

    def test_duplicate_ids(self):
        rule = dict(id="same", kind="files", paths=["AGENTS.md"])
        self.write_contract([rule, rule])
        self.has_code("E_ID")

    def test_duplicate_json_key_and_nonfinite(self):
        for text in ['{"schema_version":1,"schema_version":1}', '{"x":NaN}', '{"x":Infinity}', '{']:
            (self.root / ".tooling/contracts.json").write_text(text)
            self.has_code("E_JSON")

    def test_escape_and_windows_paths_always_fail(self):
        for value in ["../outside", "C:/Windows", "C:relative", "//server/share", "a:stream", "a\\b"]:
            with self.subTest(value=value):
                self.write_contract([dict(id="escape", kind="files", paths=[value], severity="WARN")])
                self.has_code("E_PATH")
                self.assertTrue(self.results().failed)

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            (Path(outside) / "file").write_text("external")
            try:
                (self.root / "link").symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"OS does not allow symlink creation: {exc}")
            self.write_contract([dict(id="escape", kind="files", paths=["link/file"])])
            self.has_code("E_PATH")

    def test_markdown_relative_encoded_and_reference_links(self):
        (self.root / "a b.md").write_text("target")
        doc = self.root / ".tooling/links.md"
        doc.write_text('[good](../a%20b.md#anchor)\n[label]: <../a b.md>\n'
                       '```text\n[fake](missing)\n```\n`[fake](missing)`\n[web](https://example.com)')
        check.markdown_links(self.root, doc)
        doc.write_text('[broken](missing.md)')
        with self.assertRaises(check.Violation) as error:
            check.markdown_links(self.root, doc)
        self.assertEqual(error.exception.code, "E_LINK")

    def test_markdown_escape_is_rejected(self):
        doc = self.root / "links.md"
        for target in ['../outside', 'C:/Windows', 'file:///C:/Windows', '//server/share']:
            doc.write_text(f'[escape]({target})')
            with self.assertRaises(check.Violation) as error:
                check.markdown_links(self.root, doc)
            self.assertEqual(error.exception.code, "E_PATH")

    def test_literals_and_protected_hash(self):
        path = self.root / "asset.txt"
        path.write_text("current")
        digest = check.hashlib.sha256(path.read_bytes()).hexdigest()
        self.write_contract([dict(id="hash", kind="sha256", paths=["asset.txt"], expected=digest)])
        self.assertFalse(self.results().failed)
        path.write_text("changed")
        self.has_code("E_HASH")
        self.write_contract([dict(id="legacy", kind="text", paths=["asset.txt"], required=[], forbidden=["changed"])])
        self.has_code("E_TEXT")

    def test_unknown_profile_skill_fails(self):
        path = self.root / ".tooling/profile.json"
        profile = check.read_json(path)
        profile["skills"] = ["does-not-exist"]
        path.write_text(json.dumps(profile))
        self.has_code("E_CATALOG")

    def test_wrong_tools_root_fails(self):
        with patch.dict(os.environ, {"TOOLS_C_ROOT": str(self.root)}):
            self.has_code("E_TOOLS_ROOT")

    def test_duplicate_canonical_skill_in_project_fails(self):
        directory = self.root / "skills/clone"
        directory.mkdir(parents=True)
        (directory / "SKILL.md").write_text('---\nname: verification\ndescription: clone\n---\n')
        path = self.root / ".tooling/profile.json"
        profile = check.read_json(path)
        profile["local_skill_roots"] = ["skills"]
        path.write_text(json.dumps(profile))
        self.has_code("E_CATALOG")

    def test_godot_adapter_follows_resources(self):
        from profile_adapters import check_adapter
        (self.root / "project.godot").write_text('config_version=5')
        (self.root / "main.tscn").write_text('[ext_resource type="Resource" path="res://nested.tres" id="1"]')
        adapter = dict(kind="godot", resources=["main.tscn"])
        with self.assertRaises(check.Violation):
            check_adapter(self.root, check.ROOT, adapter)
        (self.root / "nested.tres").write_text('[resource]')
        check_adapter(self.root, check.ROOT, adapter)

    def test_malformed_adapter_cli_reports_failure_without_traceback(self):
        path = self.root / ".tooling/profile.json"
        profile = check.read_json(path)
        profile["adapter"] = {"kind": "unknown"}
        path.write_text(json.dumps(profile))
        p = subprocess.run([sys.executable, str(check.ROOT / "tools/check.py"), "--project", str(self.root)],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertNotIn("Traceback", p.stderr)

    def test_bootstrap_preserves_user_bytes_and_is_idempotent(self):
        raw = b'\xef\xbb\xbf# User instructions\r\nPreserve this text.\r\n'
        (self.root / "AGENTS.md").write_bytes(raw)
        profile = (self.root / ".tooling/profile.json").read_bytes()
        bootstrap.install(self.root, "generic")
        first = (self.root / "AGENTS.md").read_bytes()
        self.assertTrue(first.startswith(raw))
        bootstrap.install(self.root, "generic")
        self.assertEqual(first, (self.root / "AGENTS.md").read_bytes())
        self.assertEqual(profile, (self.root / ".tooling/profile.json").read_bytes())

    def test_bootstrap_ambiguous_markers_fail_before_write(self):
        raw = b'User text\n<!-- tools-c:begin -->\n'
        (self.root / "AGENTS.md").write_bytes(raw)
        with self.assertRaises(check.Violation):
            bootstrap.install(self.root, "generic")
        self.assertEqual(raw, (self.root / "AGENTS.md").read_bytes())

    def test_all_eight_blender_contexts_and_routers(self):
        from profile_adapters import check_adapter
        sync_blender.generate(self.root)
        check_adapter(self.root, check.ROOT, dict(kind="blender", manifest="skills/PIPELINE_MANIFEST.json"))
        for alias in check.catalog(check.ROOT)["blender_aliases"]:
            context = read_blender_skill.render(check.ROOT, alias)
            self.assertIn("Blender-native", context)
            self.assertIn("Pitfalls / Lessons Learned", context)
            self.assertNotIn("Fixed 18-bone", context)
            text = read_blender_skill.router(check.ROOT, alias)
            snippet = text.split('```python\n')[1].split('```')[0]
            env = {}
            with patch('builtins.print'):
                exec(snippet, env)
            self.assertEqual(env['_result']['content'], context)

    def test_blender_activation_cases_cover_revised_routes(self):
        suite = json.loads((check.ROOT / "tests/blender_activation_cases.json").read_text(encoding="utf-8"))
        aliases = set(check.catalog(check.ROOT)["blender_aliases"])
        self.assertEqual({case["alias"] for case in suite["cases"]}, aliases)
        prompts = []
        for case in suite["cases"]:
            self.assertGreaterEqual(len(case["should_trigger"]), 2)
            self.assertGreaterEqual(len(case["should_not_trigger"]), 2)
            self.assertTrue(case["edge"]["prompt"])
            self.assertTrue(case["edge"]["reason"])
            self.assertIn(case["alias"], case["edge"]["expected"])
            self.assertLessEqual(set(case["edge"]["expected"]), aliases)
            prompts.extend(case["should_trigger"] + case["should_not_trigger"] + [case["edge"]["prompt"]])
            router = read_blender_skill.router(check.ROOT, case["alias"])
            self.assertNotIn("description: Compatibility route", router)
            if case["alias"] != "Blender_Character_Modeling_SKILL":
                self.assertIn("description: " + read_blender_skill.ROUTE_DESCRIPTIONS[case["alias"]], router)
        modeling = next(case for case in suite["cases"] if case["alias"] == "Blender_Character_Modeling_SKILL")
        self.assertEqual(len(modeling["diagnostic_edges"]), 3)
        for edge in modeling["diagnostic_edges"]:
            self.assertTrue(edge["prompt"] and edge["reason"])
            self.assertLessEqual(set(edge["expected_initial"]), aliases)
            self.assertNotIn(modeling["alias"], edge["expected_initial"])
            self.assertNotIn(edge["prompt"], prompts)
            prompts.append(edge["prompt"])
        self.assertEqual(len(prompts), len(set(prompts)))
        modeling_router = read_blender_skill.router(check.ROOT, "Blender_Character_Modeling_SKILL")
        front = (check.ROOT / "skills/blender-character-modeling/SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
        self.assertIn("name: blender-character-modeling", front)
        description = next(line for line in front.splitlines() if line.startswith("description: "))
        self.assertIn(description, modeling_router)
        context = read_blender_skill.render(check.ROOT, modeling["alias"])
        self.assertIn("SOURCE: skills/blender-character-modeling/SKILL.md", context)
        self.assertNotIn("SOURCE: skills/blender-pipeline/references/modeling.md", context)
        self.assertNotIn("SOURCE: skills/blender-pipeline/references/surfaces.md", context)
        self.assertNotIn("SOURCE: skills/blender-pipeline/references/external-import.md", context)
        legacy = (check.ROOT / "skills/blender-pipeline/references/modeling.md").read_text(encoding="utf-8")
        self.assertIn("../../blender-character-modeling/SKILL.md", legacy)
        self.assertNotIn("## 0. Scope", legacy)

    def test_core_activation_cases_cover_non_blender_skills(self):
        suite = json.loads((check.ROOT / "tests/core_activation_cases.json").read_text(encoding="utf-8"))
        expected = {"contracts-lint", "godot-project", "project-audit", "verification"}
        self.assertEqual({case["skill"] for case in suite["cases"]}, expected)
        prompts = []
        for case in suite["cases"]:
            self.assertGreaterEqual(len(case["should_trigger"]), 2)
            self.assertGreaterEqual(len(case["should_not_trigger"]), 2)
            self.assertTrue(case["edge"]["prompt"])
            self.assertTrue(case["edge"]["reason"])
            self.assertIn(case["skill"], case["edge"]["expected"])
            self.assertLessEqual(set(case["edge"]["expected"]), expected)
            prompts.extend(case["should_trigger"] + case["should_not_trigger"] + [case["edge"]["prompt"]])
        self.assertEqual(len(prompts), len(set(prompts)))

    def test_sync_refuses_user_drift_before_any_write(self):
        sync_blender.generate(self.root)
        paths = list((self.root / "skills").glob('*/SKILL.md'))
        paths[-1].write_text('user edit')
        before = {p: p.read_bytes() for p in paths}
        with self.assertRaises(check.Violation):
            sync_blender.generate(self.root)
        self.assertEqual(before, {p: p.read_bytes() for p in paths})

    def test_sync_does_not_rewrite_identical_routers(self):
        sync_blender.generate(self.root)
        with patch.object(Path, "write_bytes", side_effect=AssertionError("unexpected rewrite")):
            sync_blender.generate(self.root)

    def test_bundle_is_complete_and_will_not_overwrite(self):
        target = self.root / "offline"
        sync_blender.generate(target, bundle=True)
        self.assertEqual(len(list(target.glob('*/SKILL.md'))), 8)
        for alias, technique in read_blender_skill.ROUTE_TECHNIQUES.items():
            self.assertIn(technique, (target / alias / 'SKILL.md').read_text(encoding='utf-8'))
        with self.assertRaises(check.Violation):
            sync_blender.generate(target, bundle=True)

    def test_bundle_rejects_empty_and_nonempty_existing_dirs_without_mutation(self):
        for populated in (False, True):
            target = self.root / str(populated)
            target.mkdir()
            if populated:
                (target / 'keep.txt').write_bytes(b'user bytes')
            before = {p: p.read_bytes() for p in target.rglob('*') if p.is_file()}
            result = subprocess.run([sys.executable, str(check.ROOT / 'tools/sync_blender.py'),
                                     '--bundle', str(target)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('NEW directory', result.stdout)
            self.assertEqual(before, {p: p.read_bytes() for p in target.rglob('*') if p.is_file()})

    def test_adapter_rejects_router_drift(self):
        from profile_adapters import check_adapter
        sync_blender.generate(self.root)
        path = next((self.root / 'skills').glob('*/SKILL.md'))
        path.write_text('user drift')
        with self.assertRaisesRegex(check.Violation, 'Router drift'):
            check_adapter(self.root, check.ROOT, dict(kind='blender', manifest='skills/PIPELINE_MANIFEST.json'))

    def test_legacy_mirror_drift_blocks_all_sync_writes(self):
        server = self.root / 'mcp-server/blender_mcp_server.py'
        server.parent.mkdir()
        server.write_text('# fixture server presence')
        sync_blender.generate(self.root)
        paths = list((self.root / 'mcp-server/skills').glob('*/SKILL.md'))
        self.assertEqual(len(paths), 8)
        paths[0].write_text('user edit')
        before = {p: p.read_bytes() for p in self.root.rglob('SKILL.md')}
        with self.assertRaises(check.Violation):
            sync_blender.generate(self.root)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('SKILL.md')})

    def test_non_ascii_project_name(self):
        target = self.root / 'Новый проект'
        target.mkdir()
        bootstrap.install(target, 'generic')
        self.assertFalse(check.run(target).failed)

    def test_engine_zero_exit_does_not_hide_script_errors(self):
        from engine_check import evaluate
        self.assertFalse(evaluate(0, 'TOOLS_C_GODOT_RUNTIME {}\nSCRIPT ERROR: failure', 'TOOLS_C_GODOT_RUNTIME')[0])
        self.assertFalse(evaluate(0, 'No assertions', 'TOOLS_C_GODOT_RUNTIME')[0])
        self.assertTrue(evaluate(0, 'TOOLS_C_GODOT_RUNTIME {}', 'TOOLS_C_GODOT_RUNTIME')[0])


if __name__ == '__main__':
    unittest.main()
