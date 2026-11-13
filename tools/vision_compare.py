"""Bounded silhouette diagnostics; geometric agreement is not artistic acceptance."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import zlib

from qa_freshness import png_integrity
from validation_core import existing, read_json, Violation

MAX_SIDE = 1024


def require(ok, message):
    if not ok: raise ValueError(message)


def shape(mask):
    require(isinstance(mask,list) and mask and isinstance(mask[0],list) and mask[0], 'Empty mask')
    w,h=len(mask[0]),len(mask)
    require(max(w,h)<=MAX_SIDE and all(isinstance(row,list) and len(row)==w and
            all(type(v) is bool for v in row) for row in mask), 'Invalid bounded binary mask')
    return w,h


def contour(mask):
    w,h=shape(mask)
    return [(x,y) for y,row in enumerate(mask) for x,on in enumerate(row) if on and
            (x==0 or y==0 or x==w-1 or y==h-1 or
             not all(mask[yy][xx] for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1))))]


def _edt_line(f):
    """Squared Euclidean distance transform of one finite sampled function."""
    n=len(f);v=[0]*n;z=[-math.inf]+[math.inf]*n;k=0
    for q in range(1,n):
        s=((f[q]+q*q)-(f[v[k]]+v[k]*v[k]))/(2*(q-v[k]))
        while s<=z[k]:
            k-=1
            s=((f[q]+q*q)-(f[v[k]]+v[k]*v[k]))/(2*(q-v[k]))
        k+=1;v[k]=q;z[k]=s;z[k+1]=math.inf
    out=[];k=0
    for q in range(n):
        while z[k+1]<q:k+=1
        out.append((q-v[k])**2+f[v[k]])
    return out


def _distances(points, target, w, h):
    far=float((w*w+h*h)*4)
    grid=[[far]*w for _ in range(h)]
    for x,y in target:grid[y][x]=0
    grid=[_edt_line(row) for row in grid]
    for x in range(w):
        column=_edt_line([grid[y][x] for y in range(h)])
        for y in range(h):grid[y][x]=column[y]
    return [math.sqrt(grid[y][x]) for x,y in points]


def compare_masks(reference, candidate):
    w,h=shape(reference)
    require(shape(candidate)==(w,h),'Mask dimensions differ; do not silently resize')
    a,b=contour(reference),contour(candidate)
    require(a and b,'Empty foreground has no comparable contour')
    intersection=union=different=0;low=[w,h];high=[0,0]
    for y in range(h):
        for x in range(w):
            r,c=reference[y][x],candidate[y][x]
            intersection+=r and c;union+=r or c
            if r!=c:
                different+=1;low=[min(low[0],x),min(low[1],y)];high=[max(high[0],x+1),max(high[1],y+1)]
    distances=sorted(_distances(a,b,w,h)+_distances(b,a,w,h))
    percentile=lambda p:distances[max(0,math.ceil(p*len(distances))-1)]
    bounds=low+high if different else None
    return dict(resolution=[w,h],iou=intersection/union,different_pixels=different,
                difference_bbox=bounds,reference_pixels=sum(map(sum,reference)),
                candidate_pixels=sum(map(sum,candidate)),
                contour_distance_px=dict(mean=sum(distances)/len(distances),median=percentile(.5),
                                         p95=percentile(.95),maximum=distances[-1]),
                contour_p95_normalized=percentile(.95)/math.hypot(w,h))


def write_png(path, rows):
    w,h=len(rows[0]),len(rows)
    def chunk(kind,payload):
        return struct.pack('>I',len(payload))+kind+payload+struct.pack('>I',zlib.crc32(kind+payload)&0xffffffff)
    raw=b''.join(b'\0'+bytes(c for pixel in row for c in pixel) for row in rows)
    data=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))
    Path(path).write_bytes(data+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))


def read_mask(path, mode):
    """Decode explicit 8-bit PNG masks; never infer segmentation from an RGB photo."""
    png_integrity(path)
    data=Path(path).read_bytes();w,h,depth,color=struct.unpack('>IIBB',data[16:26])
    require(max(w,h)<=MAX_SIDE and depth==8 and color in (0,2,4,6),'Use a bounded 8-bit gray/RGB/RGBA mask')
    require(mode in ('alpha','luminance'),'Explicit alpha or luminance mask mode required')
    channels={0:1,2:3,4:2,6:4}[color]
    require(mode!='alpha' or color in (4,6),'Alpha mask requires an alpha channel')
    compressed=bytearray();pos=8
    while pos<len(data):
        size=struct.unpack('>I',data[pos:pos+4])[0];kind=data[pos+4:pos+8]
        if kind==b'IDAT':compressed.extend(data[pos+8:pos+8+size])
        pos+=size+12
    raw=zlib.decompress(compressed);stride=w*channels;previous=bytearray(stride);rows=[]
    def paeth(a,b,c):
        p=a+b-c;values=[abs(p-a),abs(p-b),abs(p-c)]
        return (a,b,c)[values.index(min(values))]
    for y in range(h):
        start=y*(stride+1);kind=raw[start];row=bytearray(raw[start+1:start+1+stride])
        for i in range(stride):
            a=row[i-channels] if i>=channels else 0;b=previous[i];c=previous[i-channels] if i>=channels else 0
            row[i]=(row[i]+(0,a,b,(a+b)//2,paeth(a,b,c))[kind])&255
        mask=[]
        for x in range(w):
            pixel=row[x*channels:(x+1)*channels]
            if mode=='alpha':value=pixel[-1]
            else:
                require(channels<3 or pixel[0]==pixel[1]==pixel[2], 'Luminance reference must be an explicit monochrome mask')
                value=pixel[0]
            mask.append(value>=128)
        rows.append(mask);previous=row
    return rows


def overlay(reference,candidate):
    require(shape(reference)==shape(candidate),'Mask dimensions differ')
    return [[(220,220,220,255) if r and c else (30,220,100,255) if r else
             (240,60,140,255) if c else (24,24,24,255) for r,c in zip(a,b)]
            for a,b in zip(reference,candidate)]


def assess(metrics,alignment,candidate_setup,authority,thresholds):
    require(authority in ('ORIGINAL','LOCKED_HERO','GENERATED_AUXILIARY'),'Unknown reference authority')
    require(alignment.get('mode') in ('CALIBRATED','APPROXIMATE'),'Explicit alignment mode required')
    require(set(thresholds)<= {'iou_min','contour_p95_max_px'},'Unknown metric threshold')
    for key,value in thresholds.items():
        require(type(value) in (int,float) and math.isfinite(value) and value>=0 and
                (key!='iou_min' or value<=1),'Invalid finite threshold')
    status='REVIEW_REQUIRED';reason='Approximate or auxiliary evidence; metrics are diagnostics'
    if alignment['mode']=='CALIBRATED':
        required={'projection','camera_matrix','resolution','ortho_scale','lens','shift','sensor','pixel_aspect','frame'}
        reference=alignment.get('reference_setup')
        require(isinstance(reference,dict) and set(reference)==required and set(candidate_setup)==required,
                'Complete declared reference and actual candidate camera setup required')
        for setup in (reference,candidate_setup):
            require(setup['projection'] in ('ORTHO','PERSP') and isinstance(setup['camera_matrix'],list) and
                    len(setup['camera_matrix'])==16 and all(type(v) in (int,float) and math.isfinite(v) for v in setup['camera_matrix']),
                    'Invalid camera projection/matrix')
            require(isinstance(setup['resolution'],list) and len(setup['resolution'])==2 and
                    all(type(v) is int and 0<v<=MAX_SIDE for v in setup['resolution']),'Invalid comparison resolution')
            require(all(type(setup[k]) in (int,float) and math.isfinite(setup[k]) and setup[k]>0 for k in ('ortho_scale','lens')),
                    'Invalid camera scale/lens')
            require(type(setup['frame']) in (int,float) and math.isfinite(setup['frame']),'Invalid comparison frame')
        if not alignment.get('reviewed') or not alignment.get('pose_confirmed') or reference!=candidate_setup:
            status,reason='NOT_COMPARABLE','Camera, pose or reviewed registration does not match'
        elif authority!='GENERATED_AUXILIARY' and thresholds:
            passed=metrics['iou']>=thresholds.get('iou_min',0) and metrics['contour_distance_px']['p95']<=thresholds.get('contour_p95_max_px',math.inf)
            status,reason=('PASS' if passed else 'FAIL'),'Declared calibrated silhouette thresholds only'
    return dict(status=status,reason=reason,calibration='DECLARED_BY_REVIEWER',artistic_status='NOT_EVALUATED')


def camera_setup(metadata):
    keys=('projection','camera_matrix','resolution','ortho_scale','lens','shift','sensor','pixel_aspect','frame')
    require(all(k in metadata for k in keys),'Candidate capture lacks complete camera metadata')
    return {k:metadata[k] for k in keys}


def measure_landmarks(rows,resolution):
    require(isinstance(rows,list) and len(rows)<=256,'At most 256 explicit landmarks')
    out=[];seen=set();w,h=resolution
    for row in rows:
        require(isinstance(row,dict) and set(row)=={'id','reference','candidate','visibility'} and
                isinstance(row['id'],str) and row['id'].strip() and row['id'] not in seen,'Invalid/duplicate landmark')
        seen.add(row['id'])
        require(row['visibility'] in ('VISIBLE','PARTIAL','OCCLUDED'),'Unknown landmark visibility')
        if row['visibility']!='VISIBLE':
            out.append(dict(id=row['id'],status='UNKNOWN',distance_px=None));continue
        for point in (row['reference'],row['candidate']):
            require(isinstance(point,list) and len(point)==2 and all(type(x) in (int,float) and math.isfinite(x) for x in point)
                    and 0<=point[0]<w and 0<=point[1]<h,'Landmark falls outside the registered image')
        delta=[b-a for a,b in zip(row['reference'],row['candidate'])]
        out.append(dict(id=row['id'],status='MEASURED',delta_px=delta,distance_px=math.hypot(*delta)))
    return out


def analyze_job(job_path):
    job_path=Path(job_path).resolve(strict=True);root=job_path.parent;job=read_json(job_path)
    require(job_path.stat().st_size<=1024*1024,'Comparison job exceeds 1 MiB')
    required={'schema_version','reference','candidate','alignment','thresholds'}
    require(isinstance(job,dict) and required<=job.keys() and set(job)<=required|{'landmarks'} and type(job['schema_version']) is int and job['schema_version']==1,'Invalid comparison job')
    def artifact(row):
        require(set(row)=={'path','sha256'},'Artifact needs path/hash')
        path=existing(root,row['path'])
        require(path.stat().st_size<=32*1024*1024 and hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'],'Artifact is oversized or stale')
        return path
    ref,can=job['reference'],job['candidate']
    require(set(ref)=={'mask','mode','source','authority'} and set(can)=={'mask','capture'},'Invalid reference/candidate')
    artifact(ref['source'])
    rm=read_mask(artifact(ref['mask']),ref['mode']);cm=read_mask(artifact(can['mask']),'alpha')
    metadata=read_json(artifact(can['capture']))
    require(metadata.get('channel')=='silhouette' and metadata['sha256']==can['mask']['sha256'], 'Candidate is not its declared silhouette capture')
    metrics=compare_masks(rm,cm)
    metrics['landmarks']=measure_landmarks(job.get('landmarks',[]),metrics['resolution'])
    require(metrics['resolution']==metadata['resolution'],'Candidate mask/capture dimensions differ')
    result=dict(schema_version=1,**assess(metrics,job['alignment'],camera_setup(metadata),ref['authority'],job['thresholds']),
                metrics=metrics,job_sha256=hashlib.sha256(job_path.read_bytes()).hexdigest(),
                sources=dict(reference=ref,candidate=can),
                job=dict(path=job_path.name,sha256=hashlib.sha256(job_path.read_bytes()).hexdigest()),
                legend=dict(reference_only='green',candidate_only='magenta',overlap='gray'),
                limits='Mask/registration provenance is declared, not independently proven. No hidden-depth, topology or artistic acceptance.')
    result['findings']=[]
    if result['status']=='NOT_COMPARABLE':
        result['findings'].append(dict(code='REFERENCE_VIEW_UNCERTAIN',action='Resolve camera/pose registration before a geometry conclusion'))
    elif metrics['different_pixels']:
        result['findings'].append(dict(code='SILHOUETTE_DIFFERENCE',objects=metadata.get('objects',[]),view=metadata.get('view'),
            bbox_px=metrics['difference_bbox'],observed=dict(iou=metrics['iou'],contour_p95_px=metrics['contour_distance_px']['p95']),
            confidence='DECLARED_COMPARABLE' if result['status'] in ('PASS','FAIL') else 'DIAGNOSTIC_ONLY',
            action='Inspect the contour overlay against the authoritative source; route confirmed form defects to the existing domain owner'))
    return result,rm,cm


def verify_comparison(path,root):
    """Recompute the existing report against current input hashes before QA reuse."""
    report=read_json(Path(path));job=existing(Path(root),report['job']['path'])
    require(hashlib.sha256(job.read_bytes()).hexdigest()==report['job']['sha256'],'Comparison job is stale')
    current,_,_=analyze_job(job)
    require(current==report,'Comparison metrics or inputs changed; recompute the report')
    return report


def compare_job(job_path,output):
    root=Path(job_path).resolve(strict=True).parent
    result,rm,cm=analyze_job(job_path)
    output=Path(output).resolve()
    require(root in output.parents and not output.exists(),'Use a new contained output directory')
    output.mkdir(parents=True)
    write_png(output/'difference.png',overlay(rm,cm))
    a,b=set(contour(rm)),set(contour(cm));common=a&b;w,h=shape(rm)
    lines=[[(245,245,245,255) if (x,y) in common else (30,220,100,255) if (x,y) in a else
            (240,60,140,255) if (x,y) in b else (24,24,24,255) for x in range(w)] for y in range(h)]
    write_png(output/'contours.png',lines)
    (output/'comparison.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('job',type=Path);parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    try:
        result=compare_job(args.job,args.output);print(json.dumps(result,indent=2))
        raise SystemExit(2 if result['status']=='FAIL' else 0)
    except (ValueError,Violation,OSError,KeyError,TypeError) as exc:
        print(json.dumps(dict(status='ERROR',error=str(exc))));raise SystemExit(1)
