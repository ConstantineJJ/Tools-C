extends SceneTree
## Whole-project load gate (L2). Loads every script, scene and resource under res://,
## including files that nothing references, so a broken orphan file cannot hide behind
## a clean import. Run it after an import so the global class cache exists.
## It does not run gameplay and does not certify behavior, shaders or visuals.
##
## godot --headless --path P --script tools/probes/godot_parse_gate.gd -- [--skip=res://addons/x/] [--include-imported]

const SKIP_DIRS: PackedStringArray = [".godot", ".git", ".tooling", ".local"]


func _initialize() -> void:
	call_deferred("_probe")


func _probe() -> void:
	await process_frame
	var skips: PackedStringArray = []
	var include_imported := false
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--skip="):
			skips.append(arg.substr(7))
		elif arg == "--include-imported":
			include_imported = true
	var files: PackedStringArray = []
	_collect("res://", files, skips, include_imported)
	files.sort()
	var failures: Array = []
	var counts := {"script": 0, "scene": 0, "resource": 0, "imported": 0}
	for path in files:
		var kind := _kind(path)
		counts[kind] += 1
		var loaded: Resource = ResourceLoader.load(path, "", ResourceLoader.CACHE_MODE_REUSE)
		var reason := ""
		if loaded == null:
			reason = "load returned null"
		elif loaded is GDScript:
			# A script with a parse error still loads as a non-null GDScript. Only
			# reload() reports it; can_instantiate() alone also fails for abstract classes.
			var script := loaded as GDScript
			if not script.can_instantiate():
				var err := script.reload(true)
				if err != OK:
					reason = "script reload failed: " + error_string(err)
		elif loaded is PackedScene and not (loaded as PackedScene).can_instantiate():
			reason = "scene cannot instantiate"
		if reason == "" and (kind == "scene" or kind == "resource"):
			# A scene with a missing script/scene/texture dependency still loads non-null.
			reason = _missing_dependency(path)
		if reason != "":
			failures.append({"path": path, "kind": kind, "reason": reason})
	var report := {
		"checked": files.size(),
		"failed": failures.size(),
		"counts": counts,
		"failures": failures.slice(0, 50),
		"skipped": skips,
		"include_imported": include_imported,
		"not_checked": ["gdshader", "cs", "gdextension binaries", "runtime behavior"],
		"version": Engine.get_version_info().string,
	}
	print("TOOLS_C_GODOT_PARSE_GATE ", JSON.stringify(report))
	quit(1 if failures.size() > 0 else 0)


func _kind(path: String) -> String:
	match path.get_extension().to_lower():
		"gd":
			return "script"
		"tscn", "scn":
			return "scene"
		"tres", "res":
			return "resource"
	return "imported"


func _missing_dependency(path: String) -> String:
	for dep in ResourceLoader.get_dependencies(path):
		var parts: PackedStringArray = dep.split("::")
		var target: String = parts[parts.size() - 1]
		if target.begins_with("res://"):
			if not FileAccess.file_exists(target) and not ResourceLoader.exists(target):
				return "missing dependency: " + target
		elif parts[0].begins_with("uid://"):
			var id := ResourceUID.text_to_id(parts[0])
			if not ResourceUID.has_id(id):
				return "unresolved uid: " + parts[0]
	return ""


func _is_skipped(path: String, skips: PackedStringArray) -> bool:
	for prefix in skips:
		if path.begins_with(prefix):
			return true
	return false


func _collect(dir_path: String, out: PackedStringArray, skips: PackedStringArray, include_imported: bool) -> void:
	var dir := DirAccess.open(dir_path)
	if dir == null:
		push_error("parse gate cannot open " + dir_path)
		return
	for name in dir.get_files():
		var path := dir_path.path_join(name)
		if _is_skipped(path, skips):
			continue
		match name.get_extension().to_lower():
			"gd", "tscn", "scn", "tres", "res":
				out.append(path)
			_:
				if include_imported and FileAccess.file_exists(path + ".import"):
					out.append(path)
	for name in dir.get_directories():
		if name in SKIP_DIRS:
			continue
		var path := dir_path.path_join(name)
		if _is_skipped(path + "/", skips):
			continue
		_collect(path, out, skips, include_imported)
