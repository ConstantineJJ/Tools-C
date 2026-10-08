"""Explicit optional stdio SDK metadata/compatibility probe; no scene writes."""
import asyncio
import json
import os
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from check import catalog
from mcp_deployment import unwrap
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

READS={'list_skills','read_skill','find_skills','get_scene_info','get_skill_context','deployment_info'}


async def main(project, output, baseline):
    checks=[]
    def require(condition,label):
        if not condition: raise AssertionError(label)
        checks.append(dict(check=label,status='PASS'))
    parameters=StdioServerParameters(command=sys.executable,args=[str(project/'mcp-server/blender_mcp_server.py')],
        cwd=str(project/'mcp-server'),env=dict(os.environ,BLENDER_MCP_SKILLS_DIR=str(project/'skills')))
    async with stdio_client(parameters) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            tools=(await session.list_tools()).tools
            names={t.name for t in tools}
            old=json.loads(baseline.read_text())['schemas']
            require(names==set(old) and len(names)==17,'all seventeen existing tool names retained')
            require({t.name:t.inputSchema for t in tools}==old,'all existing tool input schemas retained')
            require(all(t.description and t.description.strip() for t in tools),'all public tools describe their actual behavior')
            require(all(t.annotations and all(type(getattr(t.annotations,k)) is bool for k in
                ['readOnlyHint','destructiveHint','openWorldHint','idempotentHint']) for t in tools),'all impact hints are explicit booleans')
            require({t.name for t in tools if t.annotations.readOnlyHint}==READS,'exact six read-only commands; writes remain conservatively annotated')
            by_name={t.name:t for t in tools}
            require(all(by_name[n].annotations.destructiveHint for n in
                ['delete_object','set_object_material','save_blend_file','execute_blender_python','create_camera','blender_operation_status']),
                'delete, overwrite, arbitrary code and cancellation disclose destructive effects')
            require(not by_name['capture_viewport'].annotations.readOnlyHint and not by_name['start_curve_batch'].annotations.readOnlyHint,
                'saved capture artifacts and queued curve jobs are writes')
            async def call(name,args): return unwrap(await session.call_tool(name,args))
            discovery=await call('list_skills',{})
            manifest=catalog(ROOT)
            require(discovery['ok'] and {r['name'] for r in discovery['skills']}==set(manifest['blender_aliases'])
                    and discovery['count']==9,'legacy discovery fields still enumerate nine aliases')
            require({r['name'] for r in discovery['canonical_skills']}=={r['id'] for r in manifest['skills']}
                    and discovery['canonical_count']==25,'all twenty-five canonical owners discoverable without context bodies')
            found=await call('find_skills',dict(query='blender-anime-character-modeling'))
            require(found['ok'] and found['count']==1 and found['results'][0]['name']=='blender-anime-character-modeling',
                    'canonical search returns one focused owner')
            loaded=await call('read_skill',dict(name=found['results'][0]['name']))
            require(loaded['ok'] and 'SOURCE: skills/blender-anime-character-modeling/SKILL.md' in loaded['content'],
                    'search result can be read through the unchanged read_skill interface')
            alias=await call('read_skill',dict(name='Blender_Character_Modeling_SKILL'))
            require(alias['ok'] and 'SOURCE: skills/blender-character-modeling/SKILL.md' in alias['content'],'legacy aliases still read canonical bytes')
            context=await call('get_skill_context',dict(task='Создай арбузный домик. Создай кошкотян.'))
            require(context['ok'] and set(context['routing']['owners'])=={'blender-architecture-environment','blender-anime-character-modeling'},
                    'character and environment routing remains scoped')
            before=await call('get_scene_info',{})
            identity=await call('deployment_info',{})
            require(identity['ok'] and not identity['restart_required'] and bool(identity['tool_metadata_sha256']),
                    'loaded identity reports metadata hash independently of input schemas')
            after=await call('get_scene_info',{})
            if before.get('ok') and after.get('ok'):
                require(before==after,'read-only smoke leaves reported scene data unchanged')
            else:
                checks.append(dict(check='read-only scene comparison',status='SKIP',reason='Blender addon did not return two successful scene snapshots'))
    output.write_text(json.dumps(dict(checks=checks,tools=[dict(name=t.name,description=t.description,
        annotations=t.annotations.model_dump(),inputSchema=t.inputSchema) for t in tools],
        deployment=identity,legacy_count=9,canonical_count=25,read_count=6,write_count=11,
        scope='Disposable stdio MCP process, current Blender addon; external connector metadata separate'),indent=2))
    print(json.dumps(checks))


if __name__=='__main__':
    asyncio.run(asyncio.wait_for(main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3])),60))
