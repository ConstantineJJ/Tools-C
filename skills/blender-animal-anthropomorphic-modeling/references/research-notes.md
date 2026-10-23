# Research notes — animal / anthropomorphic modeling

Research snapshot: 2026-09-28.

## Refresh — 2026-10-21 (primary sources)

- [Marshall Vandruff, Introduction to Animal Anatomy, Gnomon Workshop](https://www.thegnomonworkshop.com/workshops/introduction-to-animal-anatomy).
  Public workshop descriptions cover skeleton/muscle volumes, torso, support and
  propulsion, skulls in multiple views and facial construction from simple solids.
  Applied as a lightweight skeletal/mass scaffold, species-specific joints and
  cross-view head reasoning. This does not require fully modeling an internal
  skeleton. Public descriptions were read; the subscription lessons were not viewed.
- [Gaël Kerchenbaum, Lynx pardinus / CGMA lecture](https://gaelkerchenbaum.art/projects/kvGL6).
  The artist's own presentation identifies skull/bone study and écorché as the
  anatomy foundation. Applied as skull/soft-tissue/coat separation and supported
  attachments. No claim is made to have watched the paid course or reproduced
  its software-specific brush procedure.
- [Blender, Attach Hair Curves to Surface](https://docs.blender.org/manual/en/4.4/modeling/geometry_nodes/hair/utility/attach_hair_curves_to_surface.html).
  Surface and surface UV inputs, transform alignment and rest-position handling
  inform groom recovery after shape changes. Root snapping and normal alignment
  do not alone certify the final visible coat. This API/workflow reference is
  versioned; check the installed Blender/node group before use.
- [MPFB basemesh](https://static.makehumancommunity.org/mpfb/docs/assets/concept_basemesh_and_helpers.html).
  The documented base is human. Tools_C therefore evaluates it for human-dominant
  hybrid regions instead of assuming it supplies a species-specific quadruped.

These sources inform [construction and revisions](quadruped-checkpoints.md).
The late-stage geometry revision use case is expressly authorized by the user;
it is not recorded as an agent sequencing failure. Initial construction advice
does not prohibit revisions after fur, texturing or detailing.

This file records the external principles used to design the specialist skill. It is not a claim that every source is an authority; production/community advice is used where it aligns with Blender documentation and is framed as practice rather than invariant law.

## Blender Manual — Mesh Structure (4.5 LTS)

Source:
https://docs.blender.org/manual/en/4.5/modeling/meshes/structure.html

Key points used:
- quadrangles generally deform well and are preferred for animation/subdivision use;
- edge loops are foundational for organic character animation;
- loops can follow natural contours/deformation lines and should be denser where deformation is greater, such as shoulders or knees.

Applied in the skill as deformation-aware topology guidance rather than an absolute all-quads rule.

## Blender Manual — Sculpt Symmetry / Dyntopo / Remesh

Sources:
https://docs.blender.org/manual/en/4.5/sculpt_paint/sculpting/tool_settings/symmetry.html
https://docs.blender.org/manual/en/4.5/sculpt_paint/sculpting/introduction/adaptive.html
https://docs.blender.org/manual/en/4.5/modeling/meshes/retopology.html

Key points used:
- symmetry is useful during broad construction and can be deliberately broken later;
- Dyntopo and remeshing are useful for exploring complex shapes without locking final topology too early;
- remeshing is a sculpting/form tool, not evidence of final deformation-ready topology.

## CG Cookie — Workflow Tips: Creating a Stylized Blender Character

Source:
https://blog.cgcookie.com/posts/workflow-tips-from-pierrick-picaut-creating-a-stylized-blender-character/

Key points used:
- establish the style and gather multiple references;
- proportions and rough shape must work before detail;
- for animated characters, use meaningful loops around joints, mouth and eyes and follow natural muscle/deformation flow.

## CG Cookie — Creature Modeling for Production in Blender

Source:
https://www.cgcookie.com/courses/creature-modeling-for-production/

Key points used:
- production creature work benefits from a staged handoff: base mesh / anatomy and volume exploration / purposeful retopology / presentation;
- topology is driven by the eventual animation/production needs rather than sculpt beauty alone;
- anatomy and broad forms should be solved before polishing details.

## CG Cookie — The Art of Good Topology

Source:
https://blog.cgcookie.com/posts/the-art-of-good-topology-blender/

Key point used:
- good topology is use-case dependent; game assets, subdivision/VFX and animation have different priorities. The target use determines construction and density decisions.

## 80 Level — Sculpting & Grooming a Humanoid Cat Character

Source:
https://80.lv/articles/sculpting-and-grooming-a-humanoid-cat-character-with-zbrush-and-xgen

Key points used:
- the difficult design problem is creating a harmonious mix between human and animal proportions/features;
- compare animal and human anatomy rather than guessing the hybrid;
- lock primary forms early, refine secondary forms before tertiary surface detail;
- where a hybrid contains human-like and animal-like regions, use reference appropriate to each region instead of one universal rule.

## Polycount — Animal Subdivision Topology (2025 discussion)

Source:
https://polycount.com/discussion/237045/animal-subdivision-topology

Key practice used:
- rigging an animal and testing a run cycle is an effective way to expose topology problems and iterate based on actual deformation.

This is community practice, not a Blender specification, so the skill phrases it as a valuable validation test.

## Blender Artists — Quadruped / Anthropomorphic discussions

Sources:
https://blenderartists.org/t/correct-topology-for-quadruped-legs/700312
https://blenderartists.org/t/help-with-modeling-an-anthropomorphic-animal/702074
https://blenderartists.org/t/rigging-for-human-like-quadruped-character/1557547

Key practices used:
- understand actual quadruped shoulder/hip and limb joint placement rather than reading digitigrade legs as "inverted knees";
- topology depends on the articulation and expressions the character must perform;
- animal and human facial topology can share deformation logic where underlying motion/function is similar, but the final structure should be driven by the required character behavior.

These are community sources and are treated as practical warnings, not hard standards.
