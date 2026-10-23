# MPFB: choose a human base deliberately

MPFB is a Blender human-character generator. Consider it for a **new** human body,
human proportion variants, a fitting mannequin or the human-dominant regions of
an approved anthropomorphic design. Prefer it when the supplied topology/targets
are compatible with the silhouette, editability and downstream needs. If it fits
the task, use the available installed generator and adjust against the reference
rather than constructing an equivalent generic human base unnecessarily.

For a quadruped, species-specific skull/limbs, wings or an animal-dominant body,
use the animal owner's anatomy and construction workflow. A human base is not an
animal solution merely because MPFB is installed. A highly stylized/chibi body
may also be cheaper to build directly. This selection is Tools_C synthesis from
MPFB's human-base scope, not a restriction claimed by the addon authors.

## Inspect and choose

1. Confirm the actual Blender version, enabled MPFB module/extension, reported
   version and available assets. An extension-panel screenshot does not prove
   that another running Blender has it enabled. Do not auto-install, upgrade or
   download unrelated asset packs as a prerequisite to ordinary modeling.
2. Choose a generator base, an existing project base, direct modeling or sculpting
   from the current task. Record the material reason for choosing/skipping MPFB
   briefly; no separate operator report is required.
3. If using MPFB, create in the task's collection without replacing existing assets.
   Set proportions from the reference; inspect front/profile/three-quarter and
   measure against the actual target. Generator output is a starting mesh, not
   proof of likeness, final deformation, export or engine acceptance.

## Preserve parametric editing

The documented basemesh has stable vertex/face identity; targets encode vertex
displacements/shape keys. Hidden helper geometry includes fitting helpers and
joint markers. Do not delete it as apparent debris from the editable source.
Inspect what a mask modifier hides before export or a destructive operation.

Preserve a recoverable parametric source when making a baked/derived sculpt or
export copy. Do not remesh, reorder/delete vertices or apply topology-changing
operations to the parametric source and assume targets, fitting, rig references
or presets will still work. Inspect the installed version's bake/export-copy
workflow and actual data before committing a derived copy; no operator/API name
is assumed across versions.

When body targets change, use MPFB's refit-assets operation or supported auto-refit
for fitted clothes/rigs as appropriate, then inspect their actual result. Custom
groom, whiskers and separately authored accessories may need their own rebind.
Do not replace an existing approved character with MPFB for a narrow correction.
Rig/weights, animation and export retain their current specialist owners.

## Sources, checked 2026-10-21

- [MPFB overview](https://static.makehumancommunity.org/mpfb.html): human generator.
- [Basemesh and helpers](https://static.makehumancommunity.org/mpfb/docs/assets/concept_basemesh_and_helpers.html): stable mesh identity and helper roles.
- [Targets](https://static.makehumancommunity.org/mpfb/docs/assets/concept_targets.html): vertex displacements and shape keys.
- [Modeling and refitting](https://static.makehumancommunity.org/mpfb/docs/characters/modeling.html): targets, optional symmetry, one-shot/automatic asset refitting.

Use the installed extension's reported version; documentation landing pages may
lag individual release pages. This guidance does not require a particular MPFB version.
