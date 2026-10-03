"""SDK compatibility probe using actual rendered bytes and a stubbed Blender bridge.

No live Blender transport acceptance follows from this probe.
"""
import asyncio
import base64
import hashlib
import json
from pathlib import Path
import runpy
import sys
import uuid


async def main(project, root, capture_json, output):
    if output.exists():
        raise ValueError('New output directory required')
    output.mkdir(parents=True)
    directory = root / '.local/captures' / uuid.uuid4().hex
    directory.mkdir(parents=True)
    metadata = json.loads(capture_json.read_text(encoding='utf-8'))
    raw = Path(metadata['path']).read_bytes()
    image = directory / 'front.png'; image.write_bytes(raw)
    metadata['path'] = str(image)
    (directory / 'capture.json').write_text(json.dumps(metadata), encoding='utf-8')
    namespace = runpy.run_path(str(project / 'mcp-server/blender_mcp_server.py'))
    function = namespace['execute_blender_python']
    tool = namespace['mcp']._tool_manager._tools['execute_blender_python']
    original = function.__globals__['send_to_blender']
    try:
        response = dict(ok=True, data=dict(result=metadata))
        function.__globals__['send_to_blender'] = lambda payload: response
        result = await tool.run(dict(code='_result = {}'), convert_result=True)
        images = [item for item in result.content if item.type == 'image']
        assert len(images) == 1 and base64.b64decode(images[0].data) == raw
        assert result.structuredContent == dict(result=response)
        ordinary = dict(ok=True, data=dict(result=dict(value=42)))
        function.__globals__['send_to_blender'] = lambda payload: ordinary
        plain = await tool.run(dict(code='_result = {"value": 42}'), convert_result=True)
        assert plain[1] == dict(result=ordinary)
        metadata['sha256'] = '0' * 64
        function.__globals__['send_to_blender'] = lambda payload: response
        failure = await tool.run(dict(code='_result = {}'), convert_result=True)
        assert failure[1]['result']['code'] == 'E_CAPTURE_ARTIFACT'
        report = dict(status='PASS', capture_image=True, python_result_schema_preserved=True,
                      image_sha256=hashlib.sha256(raw).hexdigest(), invalid_artifact_rejected=True,
                      live_blender='SKIP: bridge stubbed; no live transport claim')
        (output / 'result.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps(report))
    finally:
        function.__globals__['send_to_blender'] = original


if __name__ == '__main__':
    asyncio.run(main(*(Path(value).resolve() for value in sys.argv[1:])))
