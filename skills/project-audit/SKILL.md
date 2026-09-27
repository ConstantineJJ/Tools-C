---
name: project-audit
description: Audit or scope work in a local project, or connect it to Tools_C while preserving instructions and worktree changes. Use for project orientation and integration, not asset authoring.
---

# Project audit

Read the required [foundation contract](../../docs/foundation.md).

## Instruction Priority

Follow the user's audit/integration scope and applicable project instructions before this universal skill. Current files, consumers and observed status outrank historical plans; a remote branch does not authorize replacing local work.

## Domain constraints

- Protected: existing instructions, tracked and untracked user work, project-specific authority and unrelated configuration.
- Owned edits: only explicitly requested integration files or narrowly authorized corrections.
- Acceptance: current state, owners, constraints and evidence are recorded; any requested integration is validated without unrelated drift.

## Workflow

Inspect the primary and additional roots, nested instructions, branch/HEAD, remotes, staged/unstaged/untracked paths, installed runtimes, local routers, skill indexes, manifests, architecture and relevant project status. Read actual consumers before treating an old design or milestone as current. Separate observed implementation, planned work and unknowns. Scope only the applicable skills; a whole integration audit may require all discovered local skills.

For an integration request, follow [project integration](references/integration.md): inspect existing configuration, connect through the managed bootstrap path, then review and specialize the generated profile/contracts. A generated profile is unreviewed until its project choices are checked; L1 passing does not make its assumptions true.

## Anti-degradation and stop

Before edits, record the affected paths and preserve user-owned bytes. Afterward inspect diff, status and project checks; stage only requested own files if a commit was authorized. Stop when the requested inventory or integration is evidenced, with open unknowns distinguished from verified facts. Do not silently expand an audit into an implementation.

## Pitfalls / Lessons Learned

### AUD-001
- Symptom: an old skeleton or stale milestone dictates a new task.
- Cause: a historical handoff was treated as current implementation.
- Rule: verify active scene/profile consumers; keep replaceable choices local.
- Automated check: declared paths through L1; semantic currency needs review.
- Verification: compare profile, current code and dated status.
- Added from / context: Tools_C migration; historical asset instructions differed from current consumers; project identities remain local.
- Version: 0.1.0, 2026-09-21.
