# PASS 0 STYLE MODE

Use when the user supplies an image as a **style example** ("примерно как на
референсе", "not one-to-one") for a new or redesigned asset. The image informs
shape language, palette, material families, detail density and mood. It is not
geometry authority: no measured proportions, counts or CONFIRMED certainty come
from it. If the user later says "match it exactly", switch to REFERENCE MODE.

## Packet (`schema: style-1`)

```json
{
  "schema": "style-1", "mode": "STYLE",
  "task": "Redesign RockMind laser module after the reference style",
  "sources": [
    {"path": "refs/laser_style.png", "sha256": "<64 hex>", "role": "style"},
    {"path": "baseline/Laser_before.blend", "sha256": "<64 hex>", "role": "existing_asset"}
  ],
  "baseline": {"source": "baseline/Laser_before.blend"},
  "adopt": [
    {"trait": "stacked ring cooling fins along the barrel", "source": "refs/laser_style.png"},
    {"trait": "chunky machined receiver with bevelled plates", "source": "refs/laser_style.png"}
  ],
  "reject": [{"trait": "large pedestal base", "reason": "user: no big base; module mounts on a socket"}],
  "user_deltas": [
    {"requirement": "emitter body purple", "status": "REQUIRED"},
    {"requirement": "emitter yellow; few yellow/purple accents on hull", "status": "REQUIRED"}
  ],
  "invariants": ["SocketReceiver position", "forward -X", "muzzle at the front"],
  "gate": "READY"
}
```

## Rules

- **Adopt** names traits and cites the style source; **reject** names what is not
  borrowed and why (user exclusions first). A trait cannot be both.
- **User deltas** override the reference. Mark them DONE only after evidence.
- A **redesign** keeps a recoverable baseline and lists invariants (interface,
  axes, markers) before mutation.
- Check sameness by style traits at review views, not by silhouette IoU against
  the style image.

Validate: `python skills/visual-reference-reconstruction/scripts/validate_style.py PACKET.json --verify-files`.
