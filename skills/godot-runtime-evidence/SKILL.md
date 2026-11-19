---
name: godot-runtime-evidence
description: Produce and judge Godot evidence beyond import - whole-project parse gate, scripted input/assert scenarios, frame capture, project test runners, export and Godot MCP use. Use to prove a Godot change works; it grants no permission to edit gameplay or assets. Acceptance of appearance or feel also loads verification.
---

# Godot runtime evidence

Read the required [foundation contract](../../docs/foundation.md) and [engine probes](../../docs/engines.md).
This skill decides which Godot check proves which claim, runs it, and reports what it did not prove.
Gameplay edits belong to [godot-gameplay-implementation](../godot-gameplay-implementation/SKILL.md);
scene ownership to [godot-project](../godot-project/SKILL.md); import to
[godot-asset-integration](../godot-asset-integration/SKILL.md); level wording to
[verification](../verification/SKILL.md).

## Instruction priority

User request, then project instructions and the project's own test setup, then this skill.
Use the engine executable and version the project declares; never infer them from another project.

## Choose the check by the claim

| Claim | Check | Level | Not proven |
| --- | --- | --- | --- |
| Project imports | `engine_check --godot` | L2 | any script outside the import path |
| No file in the project is broken, including unused ones | `--parse-gate` | L2 | shaders, C#, GDExtension, behavior |
| A scene loads and ticks | `--runtime-scene` | L3 smoke | input, gameplay, visuals |
| Input causes the stated state change | `--scenario` with assertions | L3 | feel, timing quality, visuals |
| It looks right | `--scenario --capture`, then reviewed frames | L4 input | acceptance is a reviewer's or user's call |
| The project's own tests pass | its runner, see [procedures](references/procedures.md) | L3 | what the tests do not assert |
| The build exports | export preset run | L2 | that the exported build runs correctly |

Run a check that can fail for the claim. A load smoke does not support an input claim.
`--parse-gate` is the check for "nothing is broken": on Godot 4.7.2 import and the
scene-load smoke both stay PASS when an unreferenced script has a parse error.

## Workflow

1. Read project.godot, `config/features` (engine version), the InputMap, physics layer names
   and any existing tests or scenario folder. Record the executable and its reported version.
2. Import first (`--godot`), then `--parse-gate`, then the scenario. A failed earlier step stops
   the later ones; report them as SKIP with the reason, never as PASS.
3. Write a scenario that asserts the changed behavior and one unchanged neighbor
   (see [scenario format](references/scenario-format.md)). Keep scenario files in the project.
4. Judge by the log, not the exit code. Godot returns 0 with `SCRIPT ERROR:` / `ERROR:` lines;
   any such line fails the probe unless the user has accepted a named, pre-existing one.
5. For capture, a real renderer and display are required. Read the sampled frames yourself
   with the image reader, state what is visible, and still mark L4 as needing the user when the
   claim is about feel, readability or art direction. Identical frames mean nothing changed.
6. Restore temporary diagnostic state. Do not save editor or gameplay state in read-only QA.

## Editor and Godot MCP

An open editor can own a fixed MCP port and make a second headless instance log an error; report
that conflict separately and do not stop the user's editor or filter the error. When a Godot MCP
bridge is connected, use the tool names and descriptions it actually lists; do not assume any.
A transport answer (health endpoint, tunnel, 404) is not engine evidence. See
[MCP and editor rules](references/mcp-and-editor.md).

## Reporting

For each check give: level, exact command, engine path and version, exit code, marker line,
error lines, and what the check cannot see. Use PASS, WARN, FAIL or SKIP honestly. Capture alone
is WARN with "VISUAL REVIEW REQUIRED".

## Pitfalls / Lessons Learned

### GRE-001
- Symptom: import and a scene-load smoke pass while a script in the project is broken.
- Cause: the broken file is not referenced by the imported or loaded scene; Godot exits 0.
- Rule: use the whole-project parse gate for any "project is clean" claim, and read log lines.
- Automated check: `engine_check --parse-gate`; tests/test_godot_runtime.py for the builders.
- Verification: orphan lab project reported L2 FAIL for the unreferenced script and scene.
- Added from / context: Godot skills pass 2026-11; observed on Godot 4.7.2.
