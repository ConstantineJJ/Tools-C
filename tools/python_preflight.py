"""Non-executing Blender Python preflight; not a sandbox or Blender API validator."""
import argparse
import ast
import json
from pathlib import Path


def preflight(code):
    if not isinstance(code, str):
        return {"ok": False, "code": "E_PYTHON_TYPE", "error": "code must be a string"}
    try:
        tree = ast.parse(code, filename="<blender-mcp>", mode="exec")
        # AST alone permits return/break outside a function/loop. Compile, never execute.
        compile(tree, "<blender-mcp>", "exec")
    except (SyntaxError, ValueError, TypeError, RecursionError) as exc:
        return {"ok": False, "code": "E_PYTHON_SYNTAX", "error": str(exc),
                "line": getattr(exc, "lineno", None), "column": getattr(exc, "offset", None)}
    warnings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = ast.unparse(node.func)
            if name in {"bpy.ops.object.delete", "bpy.ops.wm.open_mainfile", "bpy.ops.wm.read_factory_settings"}:
                warnings.append({"line": node.lineno, "code": "W_STATE_CHANGE", "call": name,
                                 "message": "Confirm named scope and recovery; existing safety gate still applies"})
    return {"ok": True, "code": "PYTHON_PARSE_PASS", "warnings": warnings,
            "limits": "No execution, API-signature proof, ownership proof or safety approval"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path)
    args = parser.parse_args()
    result = preflight(args.script.read_text(encoding="utf-8-sig"))
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["ok"] else 1)
