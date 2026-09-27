# Rule and lesson lifecycle

Read when creating, replacing or retiring a contract/checker rule or a durable lesson.

Start from a reproducible defect and its owner. Decide whether a machine can prove the intended invariant with the declared data. A one-off typo or a judgment about appearance is not by itself a universal contract. Keep character dimensions, clip lists, supplier quirks and other replaceable choices in the project profile or project contract.

For a machine rule, choose a unique stable ID, use the existing [contract format](../../../docs/contracts.md), and test both a satisfying fixture and a violating fixture. Include malformed inputs and path containment cases when the parser or filesystem boundary changes. Preserve diagnostic code, location and repair guidance unless the requested change explicitly revises them.

Core L1 checks remain read-only and dependency-free; engine checks belong in profile-selected adapters. Lesson IDs are unique across the canonical skill tree.

For a judgment lesson, add it to the owning skill's Pitfalls / Lessons Learned section with a stable ID, Symptom, Cause, Rule, Automated check or limitation, Verification, provenance and date/version. Do not present a design threat or anecdote as a production incident.

When replacing a rule, change active consumers and tests together. Remove obsolete active text so there is one authority. Explain the transition in Git history rather than keeping parallel archived copies. Run the Tools_C self-check, unit tests and affected project profiles; engine and visual checks remain separate.
