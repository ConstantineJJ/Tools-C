# Topology and deformation notes for animals / anthropomorphic characters

This reference supplements the central retopology and rigging skills. It does not replace them.

## Where topology earns its cost

Add resolution where it materially improves:
1. silhouette,
2. deformation,
3. facial expression/readability,
4. shading of important curved forms.

Reduce it on flat, hidden or rigid regions when the production target benefits from a lower budget.

## Deformation regions

Typical high-attention regions:
- shoulder/scapula transition;
- hip/groin;
- elbow;
- knee/stifle;
- wrist/carpus and ankle/hock;
- neck base;
- tail base;
- mouth corners, muzzle and jaw;
- eyelids;
- wing roots or other major appendage joints.

Edge loops should support the expected fold/compression direction and be denser in areas that deform more. Avoid abrupt topology-density changes directly across a flexing joint.

## Quadruped warning

A topology layout copied from a human does not automatically suit a quadruped:
- shoulder mechanics and scapular motion differ visibly;
- hindlimb proportions and contact pattern depend on plantigrade/digitigrade/unguligrade posture;
- the torso must accommodate spine flexion and limb swing;
- paws/hooves need enough geometry for the intended contact/deformation, not necessarily for every anatomical detail.

## Anthropomorphic face

Topology depends on the required acting range:
- simple mascot with no lip-sync: prioritize clean silhouette and eye/mouth readability;
- expressive face: build loops for eyelids, mouth corners, muzzle/cheek compression and jaw opening;
- speech/lip-sync: topology and rig must support the required phoneme shapes; do not promise this from static mouth geometry alone.

## Pose test before approval

For animation-bound characters, inspect representative deformations rather than only wireframe aesthetics.

Minimum useful test set (adapt to the character):
- neutral;
- deep elbow/knee bend;
- shoulder/hip extremes;
- neck turn/bend;
- tail S-curve;
- mouth open / blink when applicable;
- walk/run or equivalent locomotion cycle for quadrupeds.

A community best-practice recommendation is to rig and run a cycle specifically to expose topology weaknesses that are not visible in static inspection.
