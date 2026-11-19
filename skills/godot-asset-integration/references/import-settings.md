# Godot import settings for delivered 3D assets

Read before changing import settings, import hints or the wrapper of a delivered GLB/glTF/.blend.
Facts are from the Godot 3D-import documentation (model export considerations, import configuration, node type
customization). Option names move between 4.x releases: confirm them in the project's own Import dock.

## Conventions to check first

- Godot is right-handed, Y-up; a camera looks along -Z. An oriented asset (character, vehicle) is expected
  to face +Z (glTF convention), so it faces a default camera. In Blender that is -Y front, +Y rear.
  When rotating an asset with `look_at`, use `use_model_front` and the `Vector3.MODEL_*` constants.
- Triangulate before export when possible (Blender: Triangulate modifier with Apply Modifiers on). Importer
  triangulation of N-gons can be wrong.
- Apply object transforms before export; export meshes in rest pose, not deformed by bones.
- Light and cameras from the source are usually better rebuilt in Godot; imported light strength differs.
- Tangents: let the exporter write them when normal or height maps are used. **Ensure Tangents** generates
  them with Mikktspace only when missing.

## Import dock options that change behavior

| Option | Effect to verify in the target scene |
| --- | --- |
| Root Type / Root Name | node class and name of the scene root; prefer a Node3D-derived type |
| Apply Root Scale / Root Scale | baked into meshes and animation, or multiplies the root node scale; changes child positions |
| Ensure Tangents, Generate LODs, Create Shadow Meshes | file size, import time, shadow and distance rendering |
| Light Baking | Static Lightmaps sets GI mode and generates UV2 |
| Use Named Skins | skin binds by bone name; check retargeting and shared skeletons |
| Animation: Import, FPS, Trimming, Remove Immutable Tracks | clip content and size; FPS should match the source baseline |
| Import Script | an `EditorScenePostImport` script runs after import and must return the scene |
| glTF / FBX Embedded Texture Handling | discard, extract, or embed textures; extract for editable texture import settings |
| FBX Importer | ufbx reads FBX natively; FBX2glTF converts to glTF, needs extra setup and is not recommended without a reason |
| .blend: Visible, Active Collection Only, Modifiers, Skins, Materials Export, Animation Limit Playback / Always Sample / Group Tracks | what Blender data reaches Godot; Limit Playback can silently drop frames |

Animation Library import mode produces an `AnimationLibrary` instead of a scene, for sharing clips across characters.

## Import hints (name suffixes set in the source)

`-noimp` removes a node or animation, `-loop` marks a looping animation, `-col` / `-convcol` add a trimesh or
convex collision to a mesh, `-colonly` / `-convcolonly` replace the mesh with collision, `-occ` / `-occonly`
occluders, `-navmesh`, `-rigid` (RigidBody3D), `-vehicle` / `-wheel`, and material suffixes `-alpha`, `-vcol`.
A suffix works with `-`, `$` or `_`. Hints are a source-side contract: record them in the handoff, and check
the resulting node types rather than assuming them.

## What to compare in the target scene

Scale and orientation against a known-good asset in the same scene; material response under the project's
lighting; skeleton bone names against the profile; clip names, lengths, loop flags and root motion; collision
node types and layers (set layers from the project's named layers). A clean import is structure only.

## Where the settings live

Import options are saved next to the source as `<asset>.import` (and `.godot/imported/` holds generated
data). Commit the `.import` file with the asset; do not edit `.godot/`. After changing options, reimport
(`--import`) and re-run the parse gate and the playback scenario.
