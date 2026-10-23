"""Region freshness for existing QA images/snapshots. No scene mutation or image store."""
import hashlib
import json
import struct
import zlib
from datetime import datetime
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def exact(row, fields, label):
    require(isinstance(row, dict) and set(row) == set(fields), label + ': missing/unknown fields')


def digest(row):
    return hashlib.sha256(json.dumps(row, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()


def png_integrity(path):
    """CRC + bounded decoded scanlines; noninterlaced capture PNGs, not pixel QA."""
    data = Path(path).read_bytes()
    require(len(data) <= 64 * 1024 * 1024 and data[:8] == b'\x89PNG\r\n\x1a\n', 'invalid PNG signature/size')
    pos, chunks, compressed, header, ended = 8, [], bytearray(), None, False
    while pos < len(data):
        require(pos + 12 <= len(data), 'truncated PNG chunk')
        size = struct.unpack('>I', data[pos:pos+4])[0]
        kind = data[pos+4:pos+8]
        end = pos + 12 + size
        require(end <= len(data), 'truncated PNG data')
        payload = data[pos+8:end-4]
        require(zlib.crc32(kind + payload) & 0xffffffff == struct.unpack('>I', data[end-4:end])[0], 'PNG CRC mismatch')
        if not chunks:
            require(kind == b'IHDR' and size == 13, 'PNG needs first IHDR')
            header = struct.unpack('>IIBBBBB', payload)
        elif kind == b'IHDR':
            raise ValueError('duplicate PNG header')
        if kind == b'IDAT':
            compressed.extend(payload)
        if kind == b'IEND':
            require(size == 0 and end == len(data), 'invalid PNG end')
            ended = True
        chunks.append(kind)
        pos = end
    require(header is not None and ended and compressed, 'incomplete PNG')
    w, h, depth, color, compression, filtering, interlace = header
    channels = {0:1, 2:3, 3:1, 4:2, 6:4}
    depths = {0:{1,2,4,8,16}, 2:{8,16}, 3:{1,2,4,8}, 4:{8,16}, 6:{8,16}}
    require(0 < w <= 4096 and 0 < h <= 4096 and color in channels and depth in depths[color]
            and compression == filtering == interlace == 0, 'unsupported PNG dimensions/encoding')
    require(color != 3 or b'PLTE' in chunks[:chunks.index(b'IDAT')], 'indexed PNG missing palette')
    row_size = (w * channels[color] * depth + 7) // 8 + 1
    expected = row_size * h
    require(expected <= 64 * 1024 * 1024, 'PNG decoded size exceeds bound')
    decoder = zlib.decompressobj()
    try:
        pixels = decoder.decompress(bytes(compressed), expected + 1)
    except zlib.error as error:
        raise ValueError('corrupt PNG compressed data') from error
    require(decoder.eof and not decoder.unused_data and len(pixels) == expected
            and all(pixels[i] <= 4 for i in range(0, expected, row_size)), 'invalid PNG scanlines')
    return {'width':w, 'height':h}


def snapshot_regions(snapshot, regions):
    """Hash explicit existing snapshot rows, including requested data fingerprints."""
    require(isinstance(snapshot, dict) and snapshot.get('schema_version') == 1
            and isinstance(snapshot.get('objects'), list), 'invalid Blender snapshot')
    objects = {r['name']:r for r in snapshot['objects']}
    require(len(objects) == len(snapshot['objects']), 'duplicate snapshot objects')
    require(isinstance(regions, dict) and regions, 'explicit region/object map required')
    out = {}
    for name, names in regions.items():
        require(isinstance(name, str) and name.strip() and isinstance(names, list) and names
                and all(isinstance(x, str) and x in objects for x in names)
                and len(names) == len(set(names)), 'invalid region/object membership')
        out[name] = digest({'objects':[objects[x] for x in sorted(names)],
                            'frame':snapshot['frame'], 'fps':snapshot['fps'],
                            'categories':snapshot.get('data_categories', [])})
    return out


def assess(record, images, *, root=None, verify_artifact=None):
    """Compute dynamic status without touching immutable capture.json/snapshot files.

    verified attests a synchronous state probe and adequate declared fingerprint
    coverage. File/hash validation checks that declaration's evidence, not honesty
    or subsequent live changes. Uncontrolled/unprobed state must set it false.
    """
    exact(record, ('states', 'current', 'captures'), 'freshness')
    states = record['states']
    require(isinstance(states, dict) and states and record['current'] in states, 'missing current state')
    loaded, errors = {}, {}
    for key, row in states.items():
        exact(row, ('revision', 'snapshot', 'regions', 'verified'), 'freshness state')
        require(isinstance(key, str) and key.strip() and type(row['revision']) is int
                and row['revision'] >= 0 and type(row['verified']) is bool, 'invalid state revision/probe')
        require(isinstance(row['regions'], dict) and row['regions'], 'state regions required')
        require(callable(verify_artifact), 'existing artifact verifier required')
        verify_artifact(row['snapshot'], 'snapshot', png_only=False)
        try:
            if root is None:
                raise ValueError('files not verified')
            verify_artifact(row['snapshot'], 'snapshot', root, png_only=False)
            loaded[key] = snapshot_regions(json.loads((Path(root)/row['snapshot']['path']).read_text(encoding='utf-8-sig')), row['regions'])
        except (OSError, ValueError, KeyError, TypeError) as error:
            errors[key] = str(error)
    current_key = record['current']
    current = states[current_key]
    require(isinstance(record['captures'], list), 'capture bindings required')
    result = {}
    for binding in record['captures']:
        exact(binding, ('id', 'capture_series', 'captured_at', 'state', 'dependencies'), 'capture binding')
        cid, source_key = binding['id'], binding['state']
        require(isinstance(cid, str) and cid in images and cid not in result and source_key in states,
                'unknown/duplicate capture binding or state')
        require(isinstance(binding['capture_series'], str) and binding['capture_series'].strip(), 'capture series required')
        require(isinstance(binding['captured_at'],str) and binding['captured_at'].strip(), 'capture timestamp required')
        timestamp = datetime.fromisoformat(binding['captured_at'].replace('Z', '+00:00'))
        require(timestamp.tzinfo is not None, 'capture timestamp needs timezone')
        deps = binding['dependencies']
        require(isinstance(deps, dict) and deps and set(deps) <= set(states[source_key]['regions']), 'invalid checked regions')
        for region, dependencies in deps.items():
            require(dependencies is None or isinstance(dependencies, list)
                    and all(isinstance(x, str) and x in states[source_key]['regions'] for x in dependencies)
                    and len(dependencies) == len(set(dependencies)), 'invalid region dependencies')
        image_error = None
        try:
            if root is None or images[cid].get('image') is None:
                raise ValueError('image not file-verified')
            verify_artifact(images[cid]['image'], cid, root)
            png_integrity(Path(root)/images[cid]['image']['path'])
        except (OSError, ValueError, TypeError, KeyError) as error:
            image_error = str(error)
        reasons, statuses, changed = {}, {}, []
        known = source_key in loaded and current_key in loaded and states[source_key]['verified'] and current['verified']
        if known:
            changed = sorted(r for r, h in loaded[source_key].items() if h != loaded[current_key].get(r))
        for region, dependencies in deps.items():
            if image_error or not known or dependencies is None or current['revision'] < states[source_key]['revision']:
                status, reason = 'UNKNOWN', image_error or errors.get(source_key) or errors.get(current_key) or 'unverified state/dependency history'
            elif (region not in loaded[current_key] or states[source_key]['regions'][region] != current['regions'].get(region)):
                status, reason = 'UNKNOWN', 'region membership changed or missing'
            elif current['revision'] == states[source_key]['revision'] and changed:
                status, reason = 'UNKNOWN', 'conflicting fingerprints for the same revision'
            elif region in changed:
                status, reason = 'STALE', 'region fingerprint changed'
            elif any(d not in loaded[current_key] for d in dependencies):
                status, reason = 'UNKNOWN', 'missing visibility dependency'
            elif any(d in changed for d in dependencies):
                status, reason = 'PARTIAL', 'visibility dependency changed; recapture this region'
            else:
                status, reason = 'CURRENT', 'verified scoped fingerprints match'
            statuses[region], reasons[region] = status, reason
        values = set(statuses.values())
        overall = ('UNKNOWN' if 'UNKNOWN' in values else 'CURRENT' if values == {'CURRENT'}
                   else 'STALE' if values == {'STALE'} else 'PARTIAL')
        result[cid] = dict(status=overall, regions=statuses, reasons=reasons,
                           changed_regions=changed, image_integrity='FAIL' if image_error else 'PASS',
                           capture_series=binding['capture_series'], revision=states[source_key]['revision'])
    return result


def sufficient(requirements, images, freshness):
    """CURRENT and view coverage are separate; reuse only suitable AFTER evidence."""
    require(isinstance(requirements, dict) and requirements, 'review requirements required')
    selected, missing = {}, []
    for region, row in requirements.items():
        exact(row, ('views', 'criterion'), 'review requirement')
        require(isinstance(row['views'], list) and row['views'] and len(row['views']) == len(set(row['views']))
                and all(isinstance(x, str) and x.strip() for x in row['views'])
                and isinstance(row['criterion'], str) and row['criterion'].strip(), 'invalid review requirement')
        selected[region] = []
        for view in row['views']:
            candidates = [cid for cid, image in images.items() if image.get('phase') == 'AFTER'
                          and image.get('view', 'closeup') == view and image.get('status') != 'SKIP'
                          and freshness.get(cid, {}).get('regions', {}).get(region) == 'CURRENT']
            if not candidates:
                missing.append(dict(region=region, view=view, action='REQUEST_CAPTURE'))
            else:
                selected[region].append(sorted(candidates)[-1])
    return dict(status='SUFFICIENT' if not missing else 'INSUFFICIENT', selected=selected, requests=missing)
