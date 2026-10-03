# Blender Iterative Refinement

Use when an existing asset has a measured defect or repeated correction attempts. For a single known change, use its specialist procedure directly.

## Instruction Priority

Follow the user's defect and protected regions, approved reference/project decisions, then [pipeline core](core.md). Do not turn a narrow correction into general polish.

## Domain constraints

- Protected: approved regions, scene data, baseline Actions, rig and target behavior outside the change.
- Owned edits: the diagnosed error class and minimum dependencies.
- Acceptance: the defect improves in comparable evidence with no material regression.

## Loop

Freeze a recoverable candidate and record the relevant fixed views, poses or asset data. Classify the actual defect (reference, silhouette, proportion, form, topology, weights, rig, animation, material or export) and route to its owning procedure. Rank by user priority, visible impact and downstream risk. Open and inspect the actual BEFORE images before choosing the correction. Change one root cause at a time, recapture with the BEFORE target/frame/framing/resolution/mode, open and inspect the AFTER images and decide KEEP, CORRECT or REVERT. Record the visible observation and image paths/hashes for each decision; a successful render call alone does not complete this loop.

If repeated attempts with one method fail, diagnose why and change method or representation. Do not continue blind retries. Read [refinement diagnostics](techniques/refinement-diagnostics.md) for examples of method switches and useful iteration notes.

## Anti-degradation and stop

Explicitly compare the requested feature, another view, silhouette, topology, deformation and task-specific protected data. Stop when the requested defect passes its acceptance gate, further work is outside scope, the source lacks needed art direction, or no safe improvement remains with current evidence. Report retained improvement, relevant rejected attempt, QA level and open blocker.
