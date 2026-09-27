---
name: contracts-lint
description: Maintain Tools_C contracts, checker rules and reusable lessons when a repeatable invariant or skill rule needs to change. Use for tooling maintenance, not ordinary project QA.
---

# Contracts and lessons

Read the required [foundation contract](../../docs/foundation.md).

## Instruction Priority

Follow the user's requested rule scope, active project contracts and observed defect evidence, then this skill. Project-specific asset choices stay in the project profile; a general rule must not silently override them.

## Domain constraints

- Protected: unrelated rules, stable IDs and diagnostics, existing project data, and documented validation boundaries.
- Owned edits: the owning rule/skill, its checker and consumers, and focused positive/negative tests.
- Acceptance: the intended invariant is enforced or retired consistently; affected projects and self-checks pass with useful diagnostics.

## Workflow

Read the [contract format](../../docs/contracts.md), relevant checker, current tests and actual consumers. Establish the defect and cause before adding a rule. Use a declarative contract only for a property the checker can prove; use a lesson in the owning skill for judgment that cannot be reliably automated. Do not execute arbitrary contract text or infer semantics from word counts and loose keyword matches.

For a rule change, update the active definition and affected tests/consumers together. Exercise a valid fixture and a violating fixture, including malformed input and path escape when relevant. Retire superseded active text rather than keeping two authorities. Follow the [rule and lesson lifecycle](references/rule-lifecycle.md) for IDs, provenance and replacement details.

## Anti-degradation and stop

Compare diagnostics, exit behavior, unaffected rules and each affected project profile before and after. Stop when the scoped invariant and negative case are demonstrated, no unintended rule drift remains, and any unrun engine/runtime level is reported as SKIP. Do not claim a textual check proves gameplay, asset quality or user intent.

## Pitfalls / Lessons Learned

### LINT-001
- Symptom: checks succeed after a misspelled rule kind or an escaped path.
- Cause: permissive parsing, ignored fields or string-prefix containment.
- Rule: reject unknown fields/kinds, duplicate JSON keys/IDs, and resolve paths before containment.
- Automated check: E_SCHEMA, E_JSON, E_ID, E_PATH; negative fixtures.
- Verification: run tests including symlink/junction escape where supported.
- Added from / context: V1 contract design threat cases, not a claimed production incident.
- Version: 0.1.0, 2026-09-21.
