"""Read-only bounded process adapter to the canonical L1 checker; no shell API."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def registered_projects(root,integration):
    """Private machine allowlist, separate from project-authored contracts."""
    roots=[Path(root).resolve(),Path(integration).resolve()]
    config=roots[0]/'.local/mcp-projects.json'
    if config.exists():
        if config.stat().st_size>65536:raise ValueError('Project allowlist is oversized')
        data=json.loads(config.read_text(encoding='utf-8'))
        if not isinstance(data,dict) or set(data)!={'projects'} or not isinstance(data['projects'],list) or len(data['projects'])>64:
            raise ValueError('Expected private projects array')
        for p in data['projects']:
            if not isinstance(p,str) or not Path(p).is_absolute():raise ValueError('Registered project needs an absolute path')
            roots.append(Path(p).resolve(strict=True))
    return sorted(set(roots),key=str)


def run_checks(root,project=None,*,allowed_projects=()):
    root=Path(root).resolve();project=Path(project or root).resolve()
    allowed={Path(p).resolve() for p in allowed_projects}|{root}
    if project not in allowed or not project.is_dir():
        return dict(ok=False,code='E_PROJECT_ACCESS',error='Project is not explicitly registered for MCP checks')
    command=[sys.executable,str(root/'tools/check.py'),'--project',str(project),'--json']
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TOOLS_C_ROOT=str(root))
    try:
        # Output stays in a temporary file so subprocess output cannot grow RAM without bound.
        with tempfile.TemporaryFile() as log:
            process=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=30,env=env,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            log.seek(0);raw=log.read(1024*1024+1)
        if len(raw)>1024*1024:raise ValueError('Checker output exceeds 1 MiB')
        rows=json.loads(raw)
        if not isinstance(rows,list) or not all(isinstance(x,dict) and x.get('status') in ('PASS','WARN','FAIL','SKIP') for x in rows):
            raise ValueError('Checker did not return its result array')
        return dict(ok=process.returncode==0,scope='L1_READ_ONLY',project=str(project),results=rows,
                    runtime_status='NOT_EVALUATED',visual_status='NOT_EVALUATED')
    except subprocess.TimeoutExpired:
        return dict(ok=False,code='E_CHECK_TIMEOUT',error='L1 checker exceeded 30 seconds',scope='L1_READ_ONLY')
    except (ValueError,OSError) as exc:
        return dict(ok=False,code='E_CHECK_RESULT',error=str(exc),scope='L1_READ_ONLY')
