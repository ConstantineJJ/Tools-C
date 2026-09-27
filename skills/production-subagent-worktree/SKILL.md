---
name: production-subagent-worktree
description: Coordinate explicitly requested parallel agent work using isolated Git worktrees, file ownership, review before merge, and sequential runtime validation. Use when delegating independent edits or sharing a live editor.
---

# Production Subagent Worktree

Read the required [foundation contract](../../docs/foundation.md).

## 0. Purpose

Enable parallel work without corrupting project state or creating merge chaos.

This skill governs delegation and integration.
It does not replace specialist implementation skills.

## 1. Core rule

Parallelize only work that is actually independent.

Good candidates:
- separate assets;
- separate levels with data isolation;
- independent research;
- isolated mechanic gyms;
- read-only reviews;
- batch conversions with non-overlapping outputs.

Bad candidates:
- two agents editing the player controller;
- two agents editing project settings;
- dependent mechanic B before mechanic A is stable;
- two agents using the same live Blender or engine editor;
- tiny tasks whose coordination costs exceed the work.

## 2. Shared live-tool rule

One live editor / one mutable scene = one controlling agent.

If Blender MCP, Godot editor MCP, Unity editor automation, or another stateful editor exists only once:

- lead owns the live editor;
- subagents must use headless / CLI / isolated files when possible;
- never let two agents mutate the same live scene concurrently.

## 3. Pre-delegation contract

Every editing subagent receives:

```text
TASK:
BASE COMMIT:
ALLOWED FILES / DIRECTORIES:
FORBIDDEN SHARED FILES:
MUST PRESERVE:
DEPENDENCIES:
VALIDATION:
RETURN CONTRACT:
```

Do not rely on "work on X" as sufficient isolation.

## 4. Worktree rule

For an editing subagent:

1. Commit or intentionally stash the lead's required baseline.
2. Create worktree/branch from the intended committed base.
3. Give the subagent explicit ownership boundaries.
4. The subagent works and validates inside that worktree.
5. The subagent commits its own result.
6. Lead reviews before merge.
7. Merge one branch at a time.
8. Verify after every merge.
9. Remove completed worktree/branch when safe.

Uncommitted lead changes are not a valid dependency.

## 5. Ignored/generated data

A worktree normally lacks ignored caches and untracked local files.

Before work begins, identify required local dependencies:

- engine import caches;
- node_modules / package caches;
- downloaded asset packs;
- local configuration;
- LFS objects;
- generated build tools.

Prefer rebuilding or explicitly copying only what is required.

Never solve this by committing junk or secrets.

## 6. Review-before-merge gate

Before merge inspect:

```text
branch commits
diff stat
changed paths
important code/data diff
worktree status
validation evidence
```

Reject or return the branch when:

- files outside scope changed;
- shared project files were modified without permission;
- unrelated refactors appeared;
- generated junk entered the diff;
- validation is missing;
- the implementation violates locked project rules.

Do not merge because the subagent says "done".

## 7. Sequential merge rule

Merge parallel branches one at a time.

After each merge:

```text
IMPORT / RELOAD if required
STATIC CHECKS
ENGINE/RUNTIME CHECK
FOCUSED REGRESSION CHECK
VISUAL EVIDENCE if relevant
```

Only then merge the next branch.

A clean textual merge does not prove runtime compatibility.

## 8. Conflict rule

A large merge conflict usually means the tasks were not independent enough.

For a small local conflict:
- resolve deliberately;
- rerun validation.

For a broad conflict:
- abort;
- rebase/relaunch from the new baseline;
- reduce overlap.

Do not "solve" conflicts by taking one side wholesale without understanding the semantic loss.

## 9. Read-only agents

Research/review agents do not need worktrees when they cannot mutate project files.

Use them for:

- fresh-eyes QA;
- architecture review;
- reference research;
- performance analysis;
- documentation extraction.

Their findings are proposals/evidence, not automatic project decisions.

## 10. Fresh-eyes review

For high-value milestones, a reviewer should receive:

```text
ARTIFACT:
QUALITY BAR / CONTRACT:
HOW TO RUN / VIEW:
WHAT MUST BE PRESERVED:
```

Do not preload the review with the author's intended explanation.

Return:

```text
STATUS: OK | FIXES | NOT ASSESSED
FINDINGS:
- observable issue + evidence
```

A review never replaces the user's taste decision.

## 11. Return contract

Every editing subagent returns:

```text
BRANCH:
BASE:
COMMITS:
CHANGED FILES:
VALIDATION RUN:
EVIDENCE:
KNOWN ISSUES:
MERGE RISKS:
```

No essay is required.

## 12. Safety

Never permit a subagent to:

- push/publish unless explicitly requested;
- modify secrets;
- change repository remotes casually;
- delete unrelated branches/worktrees;
- use another agent's live editor session;
- silently broaden scope.

## 13. Stop conditions

Stop delegation when:

- coordination overhead exceeds expected gain;
- shared-file overlap becomes dominant;
- runtime verification cannot isolate failures;
- the lead needs interactive user feedback before proceeding.

## Pitfalls / Lessons Learned

Do not use concurrent editing of one live scene as a substitute for isolated ownership.
