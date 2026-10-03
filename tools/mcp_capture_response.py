"""Verify managed capture artifacts for the existing Python tool's image fallback."""
import hashlib
import json
from pathlib import Path
import struct


def capture_image(root, response):
    """Return verified PNG bytes, or None for ordinary Python responses."""
    metadata = response.get('data', {}).get('result')
    if not response.get('ok') or not isinstance(metadata, dict):
        return None
    if metadata.get('capture_kind') != 'viewport-oriented evidence render':
        return None
    if metadata.get('ok') is not True or metadata.get('status') != 'VISUAL REVIEW REQUIRED':
        raise ValueError('Capture did not return an unreviewed successful image')
    directory = (Path(root) / '.local/captures').resolve()
    image = Path(metadata['path']).resolve(strict=True)
    if image.parent.parent != directory or image.suffix.lower() != '.png':
        raise ValueError('Image fallback requires a managed Tools_C .local/captures/<new-directory> PNG')
    manifest = image.parent / 'capture.json'
    if manifest.resolve(strict=True).parent != image.parent:
        raise ValueError('Capture manifest escaped artifact directory')
    if json.loads(manifest.read_text(encoding='utf-8')) != metadata:
        raise ValueError('Python result differs from capture manifest')
    if not 100 <= image.stat().st_size <= 32 * 1024 * 1024:
        raise ValueError('Capture PNG is empty or exceeds bounded image size')
    raw = image.read_bytes()
    if raw[:8] != b'\x89PNG\r\n\x1a\n' or raw[12:16] != b'IHDR':
        raise ValueError('Capture is not a PNG image')
    dimensions = list(struct.unpack('>II', raw[16:24]))
    if dimensions != metadata['resolution'] or not all(64 <= value <= 2048 for value in dimensions):
        raise ValueError('Capture PNG dimensions differ from bounded metadata')
    if hashlib.sha256(raw).hexdigest() != metadata['sha256']:
        raise ValueError('Capture artifact hash mismatch')
    return raw
