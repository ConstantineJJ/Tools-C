"""Explicit optional SDK/live-addon probe; no tunnel restart or source asset edits."""
import asyncio
import json
import os
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from mcp_deployment import unwrap
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main(project,output):
    checks=[]
    def require(condition,label):
        if not condition: raise AssertionError(label)
        checks.append(dict(check=label,status='PASS'))
    params=StdioServerParameters(command=sys.executable,args=[str(project/'mcp-server/blender_mcp_server.py')],
                                cwd=str(project/'mcp-server'),env=dict(os.environ,BLENDER_MCP_SKILLS_DIR=str(project/'skills')))
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            async def call(name,args): return unwrap(await session.call_tool(name,args))
            schemas={t.name:t.inputSchema for t in (await session.list_tools()).tools}
            require({'known_documents','requested_documents'}<=set(schemas['get_skill_context']['properties']), 'context continuation fields registered in actual MCP schema')
            task='Создай аниме кошкодевушку, арбузный домик, скамью, забор, дерево и реквизит.'
            first=await call('get_skill_context',dict(task=task,max_chars=12000))
            require(not first['ok'] and bool(first['missing_documents']), 'tight budget returns required missing documents')
            second=await call('get_skill_context',dict(task=task,known_documents=first['receipts'],requested_documents=first['missing_documents']))
            require(second['ok'] and len(second['routing']['owners'])==5, 'continuation completes five Russian domain owners')
            retained=await call('get_skill_context',dict(task=task,known_documents=second['receipts']))
            require(retained['ok'] and not any(s['content'] for s in retained['skills']), 'retained context emits no duplicate bodies')
            forbidden=await call('get_skill_context',dict(task=task,requested_documents=['../private.md']))
            require(not forbidden['ok'], 'context path traversal is rejected')
            operation='form-mcp-probe-'+str(time.time_ns())
            collection='ToolsC_MCP_FormSmoke_'+str(time.time_ns())
            name=collection+'_Curve'
            started=await call('start_curve_batch',dict(operation_id=operation,collection_name=collection,
                 batches=[dict(name=name,paths=[[[0,0,0],[0,0,0.1]]])]))
            require(started['ok'] and started['data']['result']['operation_id']==operation, 'typed MCP operation returns queued receipt')
            try:
                for _ in range(40):
                    await asyncio.sleep(0.05)
                    status=await call('blender_operation_status',dict(operation_id=operation))
                    if status['data']['result']['status'] not in ('queued','running'): break
                require(status['ok'] and status['data']['result']['status']=='completed', 'typed MCP status observes actual Blender timer completion')
            finally:
                code=("import bpy\n"+"obj=bpy.data.objects.get("+repr(name)+")\n"+
                    "if obj is not None:\n    data=obj.data\n    bpy.data.objects.remove(obj,do_unlink=True)\n    if data.users==0: bpy.data.curves.remove(data)\n"+
                    "collection=bpy.data.collections.get("+repr(collection)+")\n"+
                    "if collection is not None: bpy.data.collections.remove(collection)\n_result={'cleaned':True}\n")
                cleaned=await call('execute_blender_python',dict(code=code))
                require(cleaned['ok'] and cleaned['data']['result']['cleaned'], 'typed smoke output cleaned up')
            async with stdio_client(params) as (fresh_read,fresh_write):
                async with ClientSession(fresh_read,fresh_write) as fresh_session:
                    await fresh_session.initialize()
                    historical=unwrap(await fresh_session.call_tool('blender_operation_status',dict(operation_id=operation)))
            require(historical['data']['result']['completed_batches']==1 and historical['data']['result']['status']=='completed',
                    'operation state survives a new MCP server process')
            partial_collection='ToolsC_MCP_Partial_'+str(time.time_ns())
            failed_operation='form-mcp-partial-'+str(time.time_ns())
            code=("import bpy,runpy\n"+"jobs=runpy.run_path("+repr(str(ROOT/'tools/blender_jobs.py'))+")\n"+
                  "batches="+repr([dict(name=partial_collection+'_First',paths=[[[0,0,0],[0,0,0.1]]]),dict(name=partial_collection+'_Second',paths=[[[0,0,0],[0,0,0.1]]])])+"\n"+
                  "jobs['start_curve_batch']("+repr(failed_operation)+","+repr(partial_collection)+",batches)\n"+
                  "collision=bpy.data.objects.new("+repr(partial_collection+'_Second')+",None)\n"+
                  "bpy.data.collections["+repr(partial_collection)+"].objects.link(collision)\n_result={'started':True}\n")
            require((await call('execute_blender_python',dict(code=code)))['ok'],'partial-failure fixture submitted')
            try:
                for _ in range(40):
                    await asyncio.sleep(0.05)
                    partial=await call('blender_operation_status',dict(operation_id=failed_operation))
                    if partial['data']['result']['status'] not in ('queued','running'): break
                require(partial['data']['result']['status']=='failed' and partial['data']['result']['completed_batches']==1,
                        'failed operation retains first completed batch and its identity')
            finally:
                cleanup=("import bpy\ncollection=bpy.data.collections["+repr(partial_collection)+"]\n"+
                  "for obj in list(collection.objects):\n    data=obj.data\n    bpy.data.objects.remove(obj,do_unlink=True)\n    if isinstance(data,bpy.types.Curve) and data.users==0: bpy.data.curves.remove(data)\n"+
                  "bpy.data.collections.remove(collection)\n_result={'cleaned':True}\n")
                require((await call('execute_blender_python',dict(code=cleanup)))['ok'],'partial-failure fixture cleaned')
    output.write_text(json.dumps(dict(checks=checks,schemas=schemas,first_context=dict(owners=first['routing']['owners'],missing=first['missing_documents']),
               operation=status['data']['result'],scope='Disposable stdio MCP server to current Blender addon; existing connector catalog is separate'),indent=2))
    print(json.dumps(checks))

if __name__=='__main__':
    asyncio.run(asyncio.wait_for(main(Path(sys.argv[1]),Path(sys.argv[2])),60))
