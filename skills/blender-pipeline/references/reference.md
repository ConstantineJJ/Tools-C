# Blender Reference Reconstruction

Use for rebuilding an asset from supplied images or diagnosing mismatch with them. Do not use for an ordinary freeform design change without a reference contract.

## Instruction Priority

Apply the user's stated fidelity and corrections, the active project profile and approved reference decisions, then [pipeline core](core.md). Generic anatomy fills missing information only; it does not override intentional stylization.

## Domain constraints

- Protected: approved identity, parts, landmark relationships, locked views and any user-protected geometry.
- Owned edits: only the indicated geometry or reference setup and dependencies needed to match the evidence.
- Acceptance: primary identity, part count, landmarks and front/side silhouettes match to the precision the images support; inferred hidden forms are identified.

## Workflow

Identify the primary view, scale or proportion unit, structural parts, symmetry and uncertainties. For shape-locked work, record the major landmark and proportion relationships before detailed modeling. For orthographic sheets, register shared heights and solve each view in its own axes; do not improve one projection by silently damaging a locked one. See [registration and measurement](techniques/reference-registration.md) when multiple views or perspective distortion make this nontrivial.

Compare fixed silhouettes and feature positions before surface polish. When references conflict, use the designated primary view for recognizability, retain shared landmarks where possible and record the compromise. If an existing asset misses the reference, diagnose global scale, landmarks, silhouette, depth, part count and feature placement; fix the highest-impact class first. Route mesh edits to [modeling](../../blender-character-modeling/SKILL.md), [sculpting](sculpting.md) or [retopology](retopology.md) as the cause requires.

## Anti-degradation and stop

Keep comparison camera, projection, pose and framing fixed. Recheck the previously approved views after each meaningful change. Stop when the visible contract passes and residual uncertainty concerns unseen or unsupported detail. If the source cannot determine a requested hidden form or views conflict in a way that changes the outcome, state the inference or ask for the missing art direction. Hand off locked views, proportions, landmarks, parts and unresolved ambiguity.
