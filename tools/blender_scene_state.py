"""Read-only Blender session/scene state for intake and baseline decisions.

Run inside Blender (for example through execute_blender_python with runpy) and
assign the return value to `_result`; current adapters return `_result`, not `result`.
Nothing is saved, selected, hidden or evaluated beyond reading object state.
"""


def scene_state(object_names=None):
    import bpy  # noqa: F401 - available only inside Blender
    scene = bpy.context.scene
    names = set(object_names) if object_names else None
    objects = []
    for obj in scene.objects:
        if names is not None and obj.name not in names:
            continue
        objects.append(dict(
            name=obj.name, type=obj.type, parent=obj.parent.name if obj.parent else None,
            collections=sorted(c.name for c in obj.users_collection),
            hidden=obj.hide_get(), hide_viewport=obj.hide_viewport, hide_render=obj.hide_render,
            selected=obj.select_get()))
    if names is not None:
        missing = sorted(names - {o['name'] for o in objects})
    else:
        missing = []
    return summarize(dict(
        file=bpy.data.filepath or None, is_dirty=bool(bpy.data.is_dirty),
        blender=bpy.app.version_string, scene=scene.name, frame=scene.frame_current,
        mode=bpy.context.mode, active=getattr(bpy.context.view_layer.objects.active, 'name', None),
        collections=_collection_tree(scene.collection), objects=objects, missing=missing))


def _collection_tree(collection):
    return dict(name=collection.name, objects=len(collection.objects),
                hide_render=getattr(collection, 'hide_render', False),
                children=[_collection_tree(c) for c in collection.children])


def summarize(state):
    """Pure post-processing shared with tests: baseline guidance and hidden counts."""
    hidden = [o['name'] for o in state['objects'] if o['hidden'] or o['hide_viewport']]
    unsaved = state['file'] is None
    state = dict(state, hidden_objects=hidden, unsaved_session=unsaved)
    if unsaved:
        state['baseline'] = ('Session has no file: save a copy (save_as_mainfile(copy=True)) '
                             'outside the project as the recoverable baseline before mutation.')
    elif state['is_dirty']:
        state['baseline'] = ('File has unsaved changes: save a copy before mutation; '
                             'do not overwrite the author file without permission.')
    else:
        state['baseline'] = 'Saved file is the baseline; record its path and hash.'
    return state
