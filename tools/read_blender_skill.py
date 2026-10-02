"""Render canonical procedural context for a legacy Blender skill name."""
import argparse
import hashlib
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check import ROOT, catalog, existing


# Keep legacy names stable; these descriptions decide discovery at the old entrypoints.
ROUTE_DESCRIPTIONS = {
    "Blender_Character_Pipeline_Core": "Route a Blender character task to the relevant canonical procedure and scope its acceptance checks. Use for multi-stage work or an unclear Blender workflow.",
    "Blender_Reference_Reconstruction_SKILL": "Match or repair a Blender character against supplied images, orthographic views or measured silhouettes. Use when reference fidelity is the task.",
    "Blender_Organic_Sculpting_SKILL": "Route organic or hard-surface sculpting, bounded form corrections and sculpted damage to canonical blender-sculpting. Use for sculpt execution, not final retopology or weight repair.",
    "Blender_Retopology_Deformation_SKILL": "Retopologize a Blender mesh or repair edge flow for required deformation. Use when topology is the diagnosed owner.",
    "Blender_Character_QA_SKILL": "Review a Blender character's geometry, reference match, deformation, animation or export with evidence. Use for validation, not unrequested edits.",
    "Blender_Animal_Anthropomorphic_Modeling_SKILL": "Model or substantially revise animals, creatures, quadrupeds, stylized pets or anthropomorphic animal characters when body-plan anatomy and animal/human feature integration are central.",
    "Blender_Iterative_Refinement_SKILL": "Iterate on a measured defect in an existing Blender asset using comparable before and after evidence. Use for repeated correction, not routine creation.",
    "Blender_Character_Rigging_Animation_Godot_SKILL": "Route legacy requests to separate rigging-skinning, animation, export-validation and Godot-asset-integration owners. Load only the stage relevant to the task.",
}

ROUTE_TECHNIQUES = {
    "Blender_Reference_Reconstruction_SKILL": "reference-registration.md",
    "Blender_Organic_Sculpting_SKILL": "sculpt-operations.md",
    "Blender_Retopology_Deformation_SKILL": "deformation-checks.md",
    "Blender_Character_QA_SKILL": "qa-evidence.md",
    "Blender_Iterative_Refinement_SKILL": "refinement-diagnostics.md",
    "Blender_Character_Rigging_Animation_Godot_SKILL": "animation-export.md",
}

SPECIALISTS = ("blender-rigging-skinning", "blender-animation",
               "blender-export-validation", "godot-asset-integration")


def render(root, alias):
    manifest = catalog(root)
    canonical = {s["id"]: s["path"] for s in manifest["skills"]}
    if alias not in manifest["blender_aliases"] and alias not in canonical:
        raise ValueError(f"Unknown Blender skill alias: {alias}")
    paths = ["docs/foundation.md", "skills/blender-pipeline/SKILL.md",
             "skills/blender-pipeline/references/core.md",
             canonical[alias] if alias in canonical else manifest["blender_aliases"][alias]["reference"],
             "skills/verification/SKILL.md"]
    if alias == "Blender_Character_Rigging_Animation_Godot_SKILL":
        paths.extend(canonical[s] for s in SPECIALISTS)
        paths.append("skills/blender-animation/references/motion.md")
    elif alias == "blender-animation":
        paths.append("skills/blender-animation/references/motion.md")
    if alias in ROUTE_TECHNIQUES:
        paths.append("skills/blender-pipeline/references/techniques/" + ROUTE_TECHNIQUES[alias])
    return "\n\n".join(f"SOURCE: {p}\n\n{existing(root, p).read_text(encoding='utf-8')}"
                        for p in dict.fromkeys(paths))


def router(root, alias):
    if alias == "Blender_Character_Modeling_SKILL":
        frontmatter = existing(root, "skills/blender-character-modeling/SKILL.md").read_text(
            encoding="utf-8").split("---", 2)[1]
        description = next(line.removeprefix("description: ") for line in frontmatter.splitlines()
                           if line.startswith("description: "))
    else:
        description = ROUTE_DESCRIPTIONS.get(
            alias, f"Compatibility route to the canonical Tools_C Blender procedures for {alias}.")
    return f'''---
name: {alias.lower().replace('_', '-')}
description: {description}
---
<!-- tools-c-router -->
<!-- tools-c-context-sha256: {hashlib.sha256(render(root, alias).encode()).hexdigest()} -->
# Tools_C compatibility entrypoint

This file contains no canonical production rules. Read the complete central context
before editing. Local agents: run `python "{root.as_posix()}/tools/read_blender_skill.py" {alias}`.
The default path is generated from installation configuration; TOOLS_C_ROOT overrides it.

For an MCP-only client, run this read-only snippet through Blender execute_python:

```python
import os, runpy
from pathlib import Path
tools_c = Path(os.environ.get("TOOLS_C_ROOT", {str(root)!r})).resolve()
reader = runpy.run_path(str(tools_c / "tools/read_blender_skill.py"))
context = reader["render"](tools_c, {alias!r})
print(context)
_result = {{"skill": {alias!r}, "content": context}}
```

If the central folder is unavailable, report SKIP with its missing path. Do not use
an obsolete project profile as a fallback. Load the active project's profile explicitly.
For an isolated machine, generate a materialized package with Tools_C
`tools/sync_blender.py --bundle NEW_DIRECTORY`; generated copies are not editable sources.
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("alias")
    args = parser.parse_args()
    print(render(ROOT, args.alias))
