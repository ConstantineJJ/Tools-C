# Clean stylized surfaces

Use for baseline color, directional texture and soft highlights without a wear,
damage or emission brief. [Surfaces](../surfaces.md) owns UV/channel/binding and
baseline shader correctness; [polishing](../../../blender-posteffects-polishing/SKILL.md)
owns a requested refinement of an existing finish.

First prove [primary forms](form-development.md) in neutral light. Choose broad color
regions and roughness that describe the material at target scale. Add restrained
directional maps only where they improve the image. Keep numeric maps in their
intended data space and inspect UV seams/flow. Do not turn every hair lock into
uniform engraved grooves or every wooden board into high-contrast noise.

Compare an actual-renderer close view and production-distance view. Preserve calm
areas, readable large groups and the approved palette. Make a local material copy
when only selected users may change. Stop once the requested clean finish reads;
wear, damage, glow, a compositor pass and bake are conditional, not prerequisites.
