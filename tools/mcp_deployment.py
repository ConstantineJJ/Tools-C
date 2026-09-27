"""Read-only disk audit and opt-in disposable stdio MCP probe; no tunnel restarts."""
import argparse
import ast
import asyncio
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.request import urlopen

from check import catalog, read_json
from mcp_runtime import resolve_root, fingerprints
from profile_adapters import check_adapter
from read_blender_skill import render

REQUIRED = {'list_skills','read_skill','find_skills','get_skill_context','execute_blender_python',
            'capture_viewport','deployment_info'}


def compare_catalog(expected, observed):
    missing=sorted(set(expected)-set(observed)); extra=sorted(set(observed)-set(expected))
    return dict(status='WARN' if missing or extra else 'PASS',missing=missing,extra=extra,
                meaning='Observed connector catalog only; missing tools can require server restart or connector refresh')


def tunnel_probe(profile, project):
    # Read only the two non-secret scalars needed for identity. Reject ambiguity.
    text=Path(profile).read_text(encoding='utf-8-sig')
    def scalar(key):
        values=re.findall(r'^\s*'+key+r':\s*[\"\']?([^\"\'\r\n#]+)',text,re.M)
        if len(values)!=1: raise ValueError('Ambiguous/missing tunnel '+key)
        return values[0].strip()
    address=scalar('listen_addr'); command=scalar('command')
    if not re.fullmatch(r'127\.0\.0\.1:\d+',address): raise ValueError('Expected fixed loopback health address')
    expected=(Path(project)/'mcp-server/run_blender_mcp_server.cmd').resolve()
    if Path(command).resolve()!=expected: raise ValueError('Tunnel profile points at another deployment target')
    with urlopen('http://'+address+'/api/status',timeout=3) as response: status=json.load(response)
    with urlopen('http://'+address+'/readyz',timeout=3) as response: ready=response.status==200
    channels=status.get('channels',[])
    commands=[d.get('value') for c in channels if c.get('name')=='main' for d in c.get('details',[]) if d.get('key')=='command']
    if status.get('health_listen_addr')!=address or len(commands)!=1 or Path(commands[0]).resolve()!=expected or not ready:
        raise ValueError('Live tunnel target/readiness mismatch')
    return dict(status='PASS',profile=str(Path(profile).resolve()),health=address,command=str(expected),
                limits='Target and ready status only; actual connector calls remain separate')


def tool_names(server):
    tree=ast.parse(server.read_text(encoding='utf-8-sig'))
    return {n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))
            and any(isinstance(d,ast.Call) and isinstance(d.func,ast.Attribute) and d.func.attr=='tool' for d in n.decorator_list)}


def disk_audit(project):
    project=Path(project).resolve(strict=True); root=resolve_root(project)
    server=project/'mcp-server/blender_mcp_server.py'
    if not server.is_file(): raise ValueError('Deployment server missing')
    check_adapter(project,root,dict(kind='blender',manifest='skills/PIPELINE_MANIFEST.json',mirrors=['mcp-server']))
    names=tool_names(server)
    if not REQUIRED<=names: raise ValueError('Missing source tools: '+str(sorted(REQUIRED-names)))
    wrapper=project/'mcp-server/run_blender_mcp_server.cmd'
    if not wrapper.is_file(): raise ValueError('Deployment wrapper missing')
    return dict(disk='PASS',project=str(project),server=str(server),wrapper=str(wrapper),
                server_sha256=hashlib.sha256(server.read_bytes()).hexdigest(),source_tools=sorted(names),
                **fingerprints(root),live='SKIP',tunnel='SKIP',connector='SKIP')


def unwrap(result):
    if getattr(result,'isError',False): raise ValueError(str(result))
    structured=getattr(result,'structuredContent',None)
    if structured:
        return structured.get('result',structured)
    for item in result.content:
        if item.type=='text': return json.loads(item.text)
    raise ValueError('MCP returned no JSON result')


async def stdio_probe(project, python):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    disk=disk_audit(project); root=Path(disk['canonical_root'])
    env=dict(os.environ, BLENDER_MCP_SKILLS_DIR=str(Path(project)/'skills'))
    params=StdioServerParameters(command=str(python),args=[disk['server']],cwd=str(Path(project)/'mcp-server'),env=env)
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            listed=await session.list_tools(); names={t.name for t in listed.tools}
            if names!=set(disk['source_tools']): raise ValueError('Runtime/source tool catalog mismatch')
            discovery=unwrap(await session.call_tool('list_skills',{}))
            aliases=set(catalog(root)['blender_aliases'])
            if {x['name'] for x in discovery['skills']} != aliases: raise ValueError('Live router availability mismatch')
            checked=[]
            for alias in sorted(aliases):
                result=unwrap(await session.call_tool('read_skill',{'name':alias}))
                if not result.get('ok') or result.get('content') != render(root,alias): raise ValueError('Canonical context mismatch: '+alias)
                checked.append(alias)
            for task in ('blender-rigging-skinning','blender-animation','blender-export-validation','godot-asset-integration'):
                result=unwrap(await session.call_tool('get_skill_context',{'task':task}))
                if not result.get('ok') or [x['name'] for x in result['skills']] != [task]: raise ValueError('Stage routing mismatch: '+task)
            bad=unwrap(await session.call_tool('execute_blender_python',{'code':'if :\n pass'}))
            if bad.get('code') != 'E_PYTHON_SYNTAX': raise ValueError('Runtime preflight did not reject invalid Python')
            identity=unwrap(await session.call_tool('deployment_info',{}))
            if not identity.get('ok') or identity.get('restart_required') or identity.get('loaded_server_sha256') != disk['server_sha256']:
                raise ValueError('Loaded server identity differs from audited disk')
            schemas={t.name:t.inputSchema for t in listed.tools}
            return dict(**{k:v for k,v in disk.items() if k!='live'},live='PASS',
                        live_scope='Disposable stdio server; not already-running tunnel/connector',
                        aliases_checked=checked,schemas=schemas,
                        tool_schema_sha256=hashlib.sha256(json.dumps(schemas,sort_keys=True).encode()).hexdigest(),
                        deployment=identity,preflight=bad)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,required=True)
    parser.add_argument('--stdio',action='store_true'); parser.add_argument('--python',type=Path,default=Path(sys.executable))
    parser.add_argument('--output',type=Path)
    parser.add_argument('--tunnel-profile',type=Path)
    parser.add_argument('--connector-tools',type=Path,help='JSON array of observed unprefixed tool names')
    args=parser.parse_args()
    try:
        result=asyncio.run(asyncio.wait_for(stdio_probe(args.project,args.python),60)) if args.stdio else disk_audit(args.project)
        if args.tunnel_profile: result['tunnel']=tunnel_probe(args.tunnel_profile,args.project)
        if args.connector_tools: result['connector']=compare_catalog(result['source_tools'],read_json(args.connector_tools))
        text=json.dumps(result,indent=2)
        if args.output: args.output.write_text(text,encoding='utf-8')
        print(text)
    except Exception as exc:
        print(json.dumps(dict(status='FAIL',reason=str(exc)))); raise SystemExit(1)
