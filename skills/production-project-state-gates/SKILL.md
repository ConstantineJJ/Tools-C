---
name: production-project-state-gates
description: Maintain lightweight project decisions, gates, guarded corrective tasks and session handoffs. Use for multi-session state where context loss could repeat work or cause regression.
---

# Production Project State Gates

Read the required [foundation contract](../../docs/foundation.md).

## 0. Purpose

Keep project truth outside transient model context.

This skill is intentionally lightweight.

It should answer five questions quickly:

1. Where are we?
2. What is currently being changed?
3. What is already decided?
4. What is locked / must not regress?
5. What evidence proves the current state works?

Do not build a documentation bureaucracy.

## 1. Source-of-truth model

Use the existing project structure when available.

Recommended logical records:

```text
PROJECT_PULSE.md or equivalent  -> current status / next actions
DECISIONS.md                    -> durable decisions and why
GATES.md / milestone section    -> pass/open/blocked conditions
evidence/ or report references  -> proof
```

These may be sections in existing files instead of separate files.

Prefer fewer authoritative files over duplicate summaries.

## 2. Session start

At the beginning of a meaningful project session, read:

```text
CURRENT STATE
OPEN TASK / SCOPE
LOCKED DECISIONS
ACTIVE BLOCKERS
LATEST VERIFIED BASELINE
NEXT STEP
```

Do not reconstruct project history from memory when project records exist.

## 3. Session scope

Record internally:

```text
TASK:
BASELINE:
ALLOWED CHANGES:
MUST PRESERVE:
EXPECTED OUTPUT:
VALIDATION:
```

For narrow tasks, do not expand the project-management footprint.

## 4. Decision record

Record only decisions that future work could otherwise misunderstand.

Format:

```text
DATE / ID:
DECISION:
WHY:
ALTERNATIVES REJECTED:
SCOPE:
REOPEN TRIGGER:
```

Do not log routine implementation details.

A decision is not immutable. If changed, preserve the old rationale and record the superseding decision.

## 5. Gates

A gate represents a condition that must be true before downstream work may rely on a result.

Gate kinds:

### STATIC
File/schema/contract/lint checks.

### ENGINE
Import, compile, engine probe, scene load.

### RUNTIME
Behavior under execution.

### VISUAL / ENGINEERING EVIDENCE
Screenshot, video, measured state, artifact inspection.

A successful command exit is evidence only for what that command actually proves.

## 6. Gate states

Use:

```text
OPEN
PASS
BLOCKED
SKIP
REGRESSED
```

Rules:

- PASS requires evidence.
- BLOCKED includes the blocker.
- SKIP includes why the capability/check is irrelevant or unavailable.
- Missing capability is not FAIL by default.
- REGRESSED means a previously passing condition no longer passes.

## 7. Evidence record

A gate result should point to compact evidence:

```text
GATE:
STATUS:
CHECK:
RESULT:
ARTIFACT / CAPTURE:
BASELINE / COMMIT:
NOTES:
```

Do not paste giant logs into project status files.
Link or reference them.

## 8. Regression gates

Critical previously passed gates may be rechecked after risky changes.

Examples:

- GLB still imports;
- expected animations still exist;
- no root-motion surprise;
- controllers still map correctly;
- save schema still loads;
- target scene still runs;
- locked visual baseline still matches.

Do not rerun the entire project QA suite for every tiny change.
Select regressions based on affected invariants.

## 9. Project Pulse update

After meaningful work, update the authoritative pulse with only:

```text
DONE:
CURRENT:
NEXT:
BLOCKERS:
REGRESSIONS / RISKS:
VERIFIED BASELINE:
```

Keep it short enough that the next agent will actually read it.

## 10. Handoff

When using scoped corrective tasks, read
[project review interfaces](../../docs/project-review.md). Analysis is read-only;
`apply-tasks` is a separate explicit write to an existing owned todo with its old
hash and exclusive writer interval. Preserve IDs, completed history and unrelated
sections; no automatic implementation or task completion. `--previous` retains
observations, not engine resume authority. Keep Pulse/plan/todo authoritative;
a separate Ledger/workflow executor remains deferred for this integration.

Before ending a substantial session:

```text
WHAT CHANGED:
WHAT PASSED:
WHAT REMAINS:
WHAT MUST NOT BE REDONE:
KNOWN RISKS:
NEXT ACTION:
```

The next agent should be able to resume without asking the user to repeat already-settled facts.

## 11. Anti-bureaucracy rule

Stop adding process when process starts consuming more effort than the work it protects.

Avoid:

- duplicate status files;
- prose diaries;
- docs that restate code;
- mandatory research documents for familiar trivial work;
- gates with no downstream consequence;
- recording every small choice.

The project exists to produce working systems/artifacts, not status paperwork.

## 12. Conflict handling

When records disagree, use:

1. user's latest explicit decision;
2. newer superseding project decision;
3. verified current artifact behavior;
4. older project record;
5. model memory.

Flag stale records rather than silently following them.

## 13. Integration with specialist skills

Specialist skills may emit:

```text
CHANGED
PRESERVED
EVIDENCE
OPEN DEFECTS
NEXT
```

This project-state skill decides what must be persisted.

It must not replace Blender/Godot/asset-specific QA.

## 14. Stop conditions

The state update is complete when the next session can correctly answer:

```text
What should I do next?
What should I not break?
How do I know the current baseline works?
```

## Pitfalls / Lessons Learned

Only persist decisions and gates that can change downstream work; avoid duplicate status authorities.
