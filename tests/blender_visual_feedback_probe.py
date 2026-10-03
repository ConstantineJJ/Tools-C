"""Opt-in visual feedback fixture; isolated background Blender only."""
import json
from pathlib import Path
import sys

import bpy


def main(action, source, destination):
    if not bpy.app.background:
        raise RuntimeError('Disposable background process required')
    if destination.exists():
        raise ValueError('New candidate path required')
    destination.parent.mkdir(parents=True, exist_ok=True)
    if action == 'build':
        bpy.ops.wm.read_factory_settings(use_empty=True)
        specs = [('Body', (0, 0, 1.55), (.45, .3, .55)),
                 ('Head', (.85, 0, 2.5), (.35, .3, .35)),
                 ('LeftLeg', (-.26, 0, .5), (.16, .22, .5)),
                 ('RightLeg', (.26, 0, .5), (.16, .22, .5)),
                 ('LeftArm', (-.64, 0, 1.6), (.14, .22, .5)),
                 ('RightArm', (.64, 0, 1.6), (.14, .22, .5))]
        mat = bpy.data.materials.new('ProbeBlue'); mat.diffuse_color = (.12, .42, .72, 1)
        for name, location, scale in specs:
            bpy.ops.mesh.primitive_cube_add(size=2, location=location)
            obj = bpy.context.object; obj.name = name; obj.scale = scale
            obj.data.materials.append(mat)
        bpy.context.scene.frame_set(1)
    elif action == 'correct':
        bpy.ops.wm.open_mainfile(filepath=str(source), use_scripts=False)
        before = {obj.name: [list(row) for row in obj.matrix_world] for obj in bpy.context.scene.objects}
        head = bpy.data.objects['Head']
        head.location.x = 0
        bpy.context.view_layer.update()
        after = {obj.name: [list(row) for row in obj.matrix_world] for obj in bpy.context.scene.objects}
        changed = [name for name in before if before[name] != after[name]]
        if changed != ['Head']:
            raise AssertionError(f'Unexpected changed scope: {changed}')
        destination.with_suffix('.json').write_text(json.dumps(dict(changed=changed, before=before, after=after)), encoding='utf-8')
    else:
        raise ValueError(action)
    bpy.ops.wm.save_as_mainfile(filepath=str(destination))
    print('TOOLS_C_VISUAL_FIXTURE ' + json.dumps(dict(ok=True, action=action, path=str(destination))))


if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:]
    main(args[0], Path(args[1]), Path(args[2]))
