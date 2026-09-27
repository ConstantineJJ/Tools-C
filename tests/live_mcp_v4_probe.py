"""Explicit live Blender capture probe through a disposable stdio MCP server.

Read-only asset inspection plus new evidence files. Does not save the live .blend.
"""
import asyncio
import base64
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from mcp_deployment import unwrap


async def main(project,output):
    from mcp import ClientSession,StdioServerParameters
    from mcp.client.stdio import stdio_client
    if output.exists(): raise ValueError('New output directory required')
    output.mkdir(parents=True)
    params=StdioServerParameters(command=sys.executable,args=[str(project/'mcp-server/blender_mcp_server.py')])
    code=("import runpy\n"+
          "capture_snapshot=runpy.run_path("+repr(str(ROOT/'tools/blender_snapshot.py'))+")[\"snapshot\"]\n"+
          "_result={'snapshot':capture_snapshot('live-capture', [o.name for o in bpy.context.scene.objects], action_names=[a.name for a in bpy.data.actions]), 'selected':[o.name for o in bpy.context.selected_objects], 'active':bpy.context.active_object.name if bpy.context.active_object else None, 'camera':bpy.context.scene.camera.name if bpy.context.scene.camera else None, 'scene':bpy.context.scene.name, 'filepath':bpy.data.filepath}\n")
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            before=unwrap(await session.call_tool('execute_blender_python',dict(code=code)))
            if not before.get('ok'): raise ValueError(before)
            before=before['data']['result']; frame=int(before['snapshot']['frame'])
            (output/'before.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
            framing=None; captures=[]
            for view in ('front','side','back','three_quarter','current'):
                args=dict(view=view,target='scene',mode='solid',frame=frame,resolution=512)
                if framing and view!='current': args['framing']=framing
                result=await session.call_tool('capture_viewport',args)
                metadata=json.loads(next(c.text for c in result.content if c.type=='text'))
                if not metadata.get('ok'): raise ValueError(metadata)
                images=[c for c in result.content if c.type=='image']
                if len(images)!=1: raise ValueError('MCP capture must return one image')
                raw=base64.b64decode(images[0].data)
                if hashlib.sha256(raw).hexdigest()!=metadata['sha256']: raise ValueError('Image hash differs')
                (output/(view+'.png')).write_bytes(raw)
                (output/(view+'.json')).write_text(json.dumps(metadata,indent=2),encoding='utf-8')
                captures.append(metadata); framing=framing or metadata['framing']
            after=unwrap(await session.call_tool('execute_blender_python',dict(code=code)))['data']['result']
            (output/'after.json').write_text(json.dumps(after,indent=2),encoding='utf-8')
            if before!=after: raise ValueError('Live capture changed declared asset/UI state')
            result=dict(status='PASS',transport='MCP SDK stdio to real running Blender bridge',
                        source_preserved=True,frame=frame,captures=captures,
                        connector='SKIP: separate connector catalog refresh required')
            (output/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
            print('TOOLS_C_LIVE_CAPTURE '+json.dumps(dict(status='PASS',views=[c['view'] for c in captures],frame=frame,source_preserved=True)))


if __name__=='__main__':
    asyncio.run(asyncio.wait_for(main(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve()),300))
