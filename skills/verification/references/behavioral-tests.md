# Behavioral Skill tests

Read when maintaining a rule or testing agent compliance. This protocol extends
Verification; it does not replace asset QA, the existing activation cases or
Project Pulse. Offline tests, agent trials and visual acceptance are separate.

## Small controlled trial

1. Select one scenario and the changed rule. Archive baseline and with-rule text
   with hashes. Keep the same model, harness, settings, tool schemas, fixture data
   and budget. Use isolated workspaces; do not remove any production safeguard.
2. Run baseline without the *new* rule, then with-rule on the same task. Record
   actual full Skill reads, significant actions/checks and the final response.
   Command text alone does not prove a successful read or execution.
3. Include at least two pressure cases: unreviewed image → requested VISUAL PASS;
   Action preservation versus shortcut weight repair; failed FACE gate versus
   pressure to detail hair. Use prepared metadata, never mutate a production asset.
4. Repeat under the same conditions when practical; retain every run. One pair,
   or baseline already passing, does not establish reliable improvement.
5. Review the actual trace and named observations. Do not infer geometry quality
   from string matches. Use current source/captures and the existing QA receipt
   for visual/deformation/engine claims; unavailable review stays SKIP/OPEN.

## Evidence utility and manual harness

`tools/skill_behavior.py` launches no model or engine. Its default output is a
NOT_RUN manifest. Prepare baseline and with-rule manifests in an explicit evidence
root, using the isolated archived rule path for each:

```powershell
python tools/skill_behavior.py prepare unreviewed-image --condition baseline --skill-id verification --rule baseline-rule.md --root PATH
python tools/skill_behavior.py prepare unreviewed-image --condition with-rule --skill-id verification --rule with-rule.md --root PATH
python tools/skill_behavior.py review PATH/trial.json --root PATH
python tools/skill_behavior.py compare PATH/baseline.json PATH/with-rule.json --root PATH
```

Redirect JSON yourself to a new chosen file when desired. For a manual trial,
give the agent the scenario goal and its condition's rule, without expected
checkpoint answers. Save its real tool trace. Set `run_kind: agent` only for an
actual run. Fill model/harness/settings/budget and fingerprints of protected
conditions; declare the budget unit in `environment.settings.budget_unit`.
Use fixture/tool fingerprints in `controls`. Fingerprints document the coordinator's controls;
the utility does not prove all external conditions were identical.

Manifest fields are schema_version 1, scenario_id, condition, run_kind, rule,
environment, controls, transcript, review and ordered checkpoints. `rule` has
id/path/sha256; transcript has path/sha256. Checkpoint evidence references the
same transcript path/hash and an existing 1-based line. Rule paths may differ
between archived conditions but their skill ID must match. The transcript is
bounded to 16 MiB and the manifest to 1 MiB; paths resolve inside the declared root.
No raw transcript text is printed by review/compare.

`review.status: REVIEWED` requires a named reviewer who actually inspected the
trace. Checkpoint PASS/FAIL remains a reviewer attestation. File validation proves
its binding, not the truth of opinions. Offline input can never produce behavioral
PASS. Missing/unreviewed/noncomparable runs return SKIP. Explicit reviewed failures
remain FAIL. Only a comparable baseline FAIL → with-rule PASS pair reports observed
improvement; it is not a statistical guarantee. Exit: 0 for prepare/PASS/SKIP,
2 for evidence or observed behavioral FAIL, 1 for invalid CLI input.

## Report and handoff

Record scenario/repeat ID, rule version/hash, environment, protected controls,
commands, exact observations/path:line, PASS/FAIL/WARN/SKIP and limitations.
Time/tokens/cost are reported only from actual measurements. No model price
estimates or automatic paid/long-running CI jobs. Never label unit fixtures as
real agent trials. B may later reference these passive reports; A creates no
requirement registry, new Ledger or workflow engine.
