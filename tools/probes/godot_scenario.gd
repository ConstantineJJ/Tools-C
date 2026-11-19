extends SceneTree
## Scripted runtime scenario (L3). Loads one scene, advances physics frames, injects
## input actions at given frames and evaluates property assertions. Scenario is JSON.
## It proves only what its assertions state; it never judges feel or visuals.
##
## godot --headless --path P --script tools/probes/godot_scenario.gd -- --scenario=res://x.json
##   (a file path outside res:// also works)
##
## Scenario schema:
##   scene: res:// scene path          frames: total physics frames to run
##   steps: [{frame, action: press|release|tap|call, name, strength?, node?, method?, args?}]
##   assertions: [{at_frame, node, exists?, property?, op?, value?, tolerance?}]
##   node is a path relative to the scene root, "." is the root.
##   ops: == != < <= > >= approx. Arrays of 2/3 numbers match Vector2/Vector3.

var _scene: Node
var _steps: Array = []
var _assertions: Array = []
var _results: Array = []
var _applied := 0


func _initialize() -> void:
	call_deferred("_probe")


func _fail_fast(message: String) -> void:
	push_error("TOOLS_C_SCENARIO " + message)
	quit(1)


func _probe() -> void:
	var path := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--scenario="):
			path = arg.substr(11)
	if path == "" or not FileAccess.file_exists(path):
		_fail_fast("scenario file missing: " + path)
		return
	var data = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(data) != TYPE_DICTIONARY or not data.has("scene") or not data.has("frames"):
		_fail_fast("scenario must be an object with scene and frames")
		return
	var packed := load(String(data["scene"])) as PackedScene
	if packed == null:
		_fail_fast("scene did not load: " + String(data["scene"]))
		return
	_steps = data.get("steps", [])
	_assertions = data.get("assertions", [])
	_scene = packed.instantiate()
	root.add_child(_scene)
	current_scene = _scene
	var frames := int(data["frames"])
	for frame in range(frames):
		await physics_frame
		_apply_steps(frame)
		_check(frame)
	var passed := true
	for item in _results:
		if not item["passed"]:
			passed = false
	var unfired := 0
	for a in _assertions:
		if int(a.get("at_frame", 0)) >= frames:
			unfired += 1
			passed = false
	print("TOOLS_C_GODOT_SCENARIO ", JSON.stringify({
		"scene": data["scene"], "frames": frames, "steps_applied": _applied,
		"steps_declared": _steps.size(), "assertions": _results,
		"assertions_never_reached": unfired, "passed": passed,
		"version": Engine.get_version_info().string,
	}))
	_scene.queue_free()
	await process_frame
	quit(0 if passed else 1)


func _apply_steps(frame: int) -> void:
	for step in _steps:
		if int(step.get("frame", -1)) != frame:
			continue
		var kind := String(step.get("action", ""))
		var action_name := StringName(String(step.get("name", "")))
		match kind:
			"press", "tap":
				_send_action(action_name, true, float(step.get("strength", 1.0)))
				if kind == "tap":
					_send_action(action_name, false, 0.0)
			"release":
				_send_action(action_name, false, 0.0)
			"call":
				var node := _find(String(step.get("node", ".")))
				if node != null and node.has_method(String(step.get("method", ""))):
					node.callv(String(step["method"]), step.get("args", []))
				else:
					push_error("TOOLS_C_SCENARIO call target missing: " + str(step))
					continue
			_:
				push_error("TOOLS_C_SCENARIO unknown step action: " + kind)
				continue
		_applied += 1


func _send_action(action_name: StringName, pressed: bool, strength: float) -> void:
	if not InputMap.has_action(action_name):
		push_error("TOOLS_C_SCENARIO unknown input action: " + String(action_name))
		return
	var event := InputEventAction.new()
	event.action = action_name
	event.pressed = pressed
	event.strength = strength
	Input.parse_input_event(event)


func _find(path: String) -> Node:
	if path == "." or path == "":
		return _scene
	return _scene.get_node_or_null(NodePath(path))


func _check(frame: int) -> void:
	for a in _assertions:
		if int(a.get("at_frame", 0)) != frame:
			continue
		var node := _find(String(a.get("node", ".")))
		var row := {"at_frame": frame, "node": a.get("node", "."), "passed": false}
		if a.has("exists"):
			row["expect_exists"] = bool(a["exists"])
			row["passed"] = (node != null) == bool(a["exists"])
		elif node == null:
			row["reason"] = "node not found"
		else:
			var prop := String(a.get("property", ""))
			var actual = node.get_indexed(NodePath(prop))
			var expected = _coerce(actual, a.get("value"))
			var op := String(a.get("op", "=="))
			row["property"] = prop
			row["op"] = op
			row["expected"] = str(expected)
			row["actual"] = str(actual)
			row["passed"] = _compare(actual, expected, op, float(a.get("tolerance", 0.0001)))
		_results.append(row)


func _coerce(actual, expected):
	if expected is Array:
		if actual is Vector3 and expected.size() == 3:
			return Vector3(expected[0], expected[1], expected[2])
		if actual is Vector2 and expected.size() == 2:
			return Vector2(expected[0], expected[1])
	return expected


func _compare(actual, expected, op: String, tolerance: float) -> bool:
	match op:
		"==":
			return actual == expected
		"!=":
			return actual != expected
		"<":
			return actual < expected
		"<=":
			return actual <= expected
		">":
			return actual > expected
		">=":
			return actual >= expected
		"approx":
			if actual is Vector3 or actual is Vector2:
				return (actual - expected).length() <= tolerance
			return absf(float(actual) - float(expected)) <= tolerance
	return false
