extends SceneTree
## Explicit scene-load smoke only; does not certify gameplay/input or visuals.

func _initialize() -> void:
	call_deferred("_probe")

func _probe() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() != 1:
		push_error("Expected exactly one res:// scene path")
		quit(1)
		return
	var packed := load(args[0]) as PackedScene
	if packed == null:
		push_error("Scene resource did not load")
		quit(1)
		return
	var scene := packed.instantiate()
	root.add_child(scene)
	current_scene = scene
	for frame in range(30):
		await physics_frame
	print("TOOLS_C_GODOT_RUNTIME ", JSON.stringify({
		"scene": args[0], "class": scene.get_class(),
		"nodes": scene.find_children("*", "", true, false).size(),
		"physics_frames": 30, "version": Engine.get_version_info().string
	}))
	scene.queue_free()
	await process_frame
	quit(0)
