"""Read-only in-Blender MCP bridge health receipt (stdlib + bpy).

Invoke through execute_blender_python AFTER opening/resetting a blend, then call
get_scene_info independently. A TCP listener or Hub status alone is not evidence
that the main-thread queue can execute requests.
"""
import os
import sys


def _same_file(a, b):
    return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))


def probe(expected_file=None, expected_scene=None):
    try:
        import bpy
    except ImportError:
        return {"status": "FAIL", "error": "Blender bpy unavailable", "checks": {}}
    addon = sys.modules.get("chatgpt_blender_mcp")
    timer = getattr(addon, "process_queue", None)
    state = getattr(addon, "_state", {})
    scene = getattr(bpy.context, "scene", None)
    actual_file = getattr(bpy.data, "filepath", "")
    tests = {
        "addon_loaded": addon is not None,
        "bridge_running": bool(state.get("running")),
        "queue_registered": bool(timer is not None and bpy.app.timers.is_registered(timer)),
        "scene_available": scene is not None,
    }
    if expected_file is not None:
        tests["file_matches"] = bool(actual_file and _same_file(actual_file, expected_file))
    if expected_scene is not None:
        tests["scene_matches"] = bool(scene and scene.name == expected_scene)
    handler = getattr(addon, "on_blend_load", None)
    if handler is not None:
        tests["load_handler_registered"] = handler in bpy.app.handlers.load_post
    return {
        "status": "PASS" if all(tests.values()) else "FAIL",
        "checks": tests,
        "scene": getattr(scene, "name", None),
        "filepath": actual_file,
        "queued_requests": state.get("queue").qsize() if state.get("queue") is not None else None,
        "limits": "Proves this RPC reached the active Blender interpreter, not external tunnel reconnection or zero in-progress jobs. Independently call get_scene_info after file loading."
    }


if __name__ == "__main__":
    import json
    print(json.dumps(probe(),ensure_ascii=False,indent=2))
