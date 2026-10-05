# DESCRIPTION MODE — text to a locked visual plan

Use for a new complex 3D asset when no authoritative image is supplied. Supplied
photos/concept art choose REFERENCE; do not replace them with a preferred new design.
Text requirements outrank every generated pixel. Keep the asset domain/provider
replaceable. Concept design stays here; 3D implementation stays with its domain owner.

## PASS0.1 — Design constraints extraction

Save the user's actual brief verbatim, hash it, and preserve quoted clauses/locations.
Extract stable REQUIRED constraint IDs: quantities, body plan, shapes, function,
style, proportions, palette, prohibited features, and output/use constraints when
specified. Separate hard requirements, soft preferences and open design decisions.
Do not turn an agent-added color, pod, radiator or backstory into REQUIRED.
Conflicting requirements or a necessary unresolved user choice block dependent work.
Only ask for decisions needed for the requested outcome; otherwise design autonomously
within the brief and record the choice. Do not infer real-world dimensions from pixels.

For "light reconnaissance biped mech, spherical torso, two energy guns, long legs":
biped/two guns/spherical torso/long legs/reconnaissance intent are REQUIRED.
The particular shoulder mount and palette may become CANONICAL after lock.
Rear cooling internals remain SPECULATIVE unless separately designed and reviewed;
seeing an invented rear radiator in a derived sheet does not settle its construction.

## PASS0.2 — Canonical Concept / Hero View

Generate individual concept images, each depicting one whole object in a readable
3/4 hero view. This phase may explore different designs under the **same brief**;
it does not generate independent technical views. Prefer neutral lighting, unobscured
joints, clear negative spaces and little wear so the candidate can be reconstructed.
Save each exact prompt, brief input lineage and image hash.

Use one candidate for a well-determined design or a bounded/low-cost task. For open
exploration, prefer three candidates if available within the task budget. Record the
candidate count/strategy/reason; three is a useful option, not a universal cost requirement.
If none obeys hard requirements, reject all. Default to at most two targeted repair
attempts for an identified defect, then report the failure rather than relaxing the brief.

Inspect actual pixels. For each candidate record every REQUIRED constraint as
PASS / FAIL / UNKNOWN with observations, plus 0–5 quality scores and reasoning for:
brief fit, silhouette readability, mechanical/design plausibility, suitability for
3D reconstruction and low design noise. Use domain-appropriate plausibility: a
building is not required to articulate. A high artistic score cannot compensate
for a failed or unreviewed hard constraint. UNKNOWN is ineligible for lock.

## PASS0.3 — Candidate selection and Identity Lock

In autonomous work, select the strongest eligible candidate, documenting tradeoffs
and quality scores. In an explicitly interactive selection, show the actual candidates
and wait for the user's choice before locking. Ordinary work does not require approval;
do not manufacture a selection pause. User preference for an ineligible concept requires
fixing its violation or an explicit recorded brief revision, never silently dropping it.

Freeze the chosen image bytes/hash and record selector/rationale/image lock version.
Immediately seal the single [Model Contract](model-contract.md) in `pass0.json`:
stable component IDs/counts, adopted shape decisions, relative envelopes/anchors,
handedness, hierarchy/symmetry, critical attachment relationships and pose. Constraint
strength (hard/proportion/soft) is independent of REQUIRED/CANONICAL/SPECULATIVE.
New schema 3 does not write a duplicate identity-lock.json manifest.
Rejected candidates remain review evidence, never downstream geometry authority.

- REQUIRED: explicitly instructed in the saved user brief, linked to its clause.
- CANONICAL: a visible design choice adopted from the selected, reviewed hero image
  and included in the lock. This is design authority, not confirmation of hidden geometry
  or engineering validity; perspective-derived ranges are adopted estimates.
- SPECULATIVE: uncommitted alternatives, hidden mechanisms and unresolved construction.

Classify properties separately; one component can contain all three labels. Required
functional intent does not prove feasible actuators. Record that feasibility separately.
The hero is immutable after lock. Refining materials or lighting must not quietly
change its geometry. A new user requirement or material design defect needs an explicit
new packet/brief/lock revision, reason and predecessor IDs/hashes. Re-review candidates;
invalidate previous multiviews and affected 3D work. Never overwrite an old lock in place.

## PASS0.4 — Multiview reconstruction FROM THAT IMAGE

Read [generation and consistency](generation-and-consistency.md). Supply the frozen
hero image, required constraints and Model Contract to the generator. Generate a
shared front / object-right side / rear / 3/4 sheet; add top/close-up sheets only for
needed interfaces. Use the same lock version and scale/pose correspondence in every file.
The generator now reconstructs the chosen concept; it no longer explores alternatives.
Do not re-prompt views from the brief alone, use a losing candidate, or chain a failed
auxiliary sheet as new authority. Unseen rear/underside forms use marked minimal proxies.

## PASS0.5 — Consistency QA and common handoff

Compare every view against the canonical image, REQUIRED constraints and Model
Contract (including VIEW COMPLETENESS), then
compare views with each other. Record the six existing consistency criteria, region
observations, violations, permitted uses and lock lineage. Conflicting counts or primary
silhouette never become new CANONICAL decisions. Restrict/reject defective images;
if usable source-only geometry remains, hand off READY_WITH_LIMITS from the frozen hero.
Never model a failed region from its generated panel. Unresolved major design/identity
or required articulation contradictions block dependent construction.

Deliver the common `pass0.json` and readable analysis, brief/constraints, candidate
reviews/prompts, frozen canonical image, persistent Model Contract, certainty map and reviewed auxiliaries.
Validate files and stage limits before Blender. The domain agent consumes this package
without recreating concept selection or converting design authority into observed fact.

If image generation is unavailable or every candidate fails, still save the extracted
brief and honest BLOCKED packet with PENDING lock and no canonical image. Do not label
a text list or a procedural placeholder as a successful hero/multiview pass. An explicit
user-authorized source-free/proxy workflow can be a separate scope, not a silent bypass.
