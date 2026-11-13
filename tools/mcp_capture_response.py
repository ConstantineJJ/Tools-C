"""Verify managed capture artifacts for the existing Python tool's image fallback."""
import hashlib
import json
import os
from pathlib import Path
import struct


def work_directory(root, category):
    """Resolve bounded artifacts outside the canonical source tree."""
    if category not in ('captures', 'operations'):
        raise ValueError('Unknown work artifact category')
    canonical = Path(root).resolve()
    work = Path(os.environ.get('TOOLS_C_WORK_ROOT') or canonical.parent / 'Work_Utility')
    if not work.is_absolute():
        raise ValueError('TOOLS_C_WORK_ROOT must be an absolute path')
    directory = (work / category).resolve()
    if directory == canonical or canonical in directory.parents:
        raise ValueError('Work output must stay outside canonical Tools_C')
    return directory


def capture_directory(root):
    """Resolve the external work area shared by capture and image delivery."""
    return work_directory(root, 'captures')


def capture_image(root, response):
    """Return verified PNG bytes, or None for ordinary Python responses."""
    metadata = response.get('data', {}).get('result')
    if not response.get('ok') or not isinstance(metadata, dict):
        return None
    kind=metadata.get('capture_kind')
    if kind not in ('viewport-oriented evidence render','silhouette comparison diagnostic'):
        return None
    diagnostic=kind=='silhouette comparison diagnostic'
    if metadata.get('ok') is not True or metadata.get('status') != 'VISUAL REVIEW REQUIRED':
        raise ValueError('Capture did not return an unreviewed successful image')
    directory = capture_directory(root)
    image = Path(metadata['path']).resolve(strict=True)
    if image.parent.parent != directory or image.suffix.lower() != '.png':
        raise ValueError('Image fallback requires a managed Work_Utility captures/<new-directory> PNG')
    manifest = image.parent / ('comparison-image.json' if diagnostic else 'capture.json')
    if manifest.resolve(strict=True).parent != image.parent:
        raise ValueError('Capture manifest escaped artifact directory')
    if json.loads(manifest.read_text(encoding='utf-8')) != metadata:
        raise ValueError('Python result differs from capture manifest')
    if not (67 if diagnostic else 100) <= image.stat().st_size <= 32 * 1024 * 1024:
        raise ValueError('Capture PNG is empty or exceeds bounded image size')
    raw = image.read_bytes()
    if raw[:8] != b'\x89PNG\r\n\x1a\n' or raw[12:16] != b'IHDR':
        raise ValueError('Capture is not a PNG image')
    dimensions = list(struct.unpack('>II', raw[16:24]))
    minimum,maximum=(1,1024) if diagnostic else (64,2048)
    if dimensions != metadata['resolution'] or not all(minimum <= value <= maximum for value in dimensions):
        raise ValueError('Capture PNG dimensions differ from bounded metadata')
    if hashlib.sha256(raw).hexdigest() != metadata['sha256']:
        raise ValueError('Capture artifact hash mismatch')
    if diagnostic:
        from qa_freshness import png_integrity
        from vision_compare import verify_comparison
        job_root=Path(metadata['job_root']).resolve(strict=True)
        if not job_root.is_relative_to(directory.parent):
            raise ValueError('Comparison job must stay in managed Work_Utility')
        report=Path(metadata['comparison_report']['path']).resolve(strict=True)
        if report.parent!=image.parent or report.name!='comparison.json' or image.name not in ('contours.png','difference.png'):
            raise ValueError('Comparison image/report escaped managed output')
        if hashlib.sha256(report.read_bytes()).hexdigest()!=metadata['comparison_report']['sha256']:
            raise ValueError('Comparison report hash mismatch')
        result=verify_comparison(report,job_root)
        if result['status']!=metadata['comparison_status'] or result['metrics']!=metadata['metrics']:
            raise ValueError('Comparison delivery differs from verified report')
        png_integrity(image)
    return raw
