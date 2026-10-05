---
name: production-lookdev-gate
description: Establish a representative visual slice and evaluate it before mass asset production. Use before building environments, buildings, vehicles, vegetation, props, UI, lighting, or effects at scale, and after art direction changes.
---

# Production Lookdev Gate

Read the required [foundation contract](../../docs/foundation.md).

## 0. Purpose

Prove the visual target on a small representative scene before producing large amounts of content.

The gate answers:

> If we build the whole project this way, will it look right?

Do not use mass production to discover the art direction.

## 1. Inputs

Use the strongest available visual contract:

- approved references;
- art bible;
- palette;
- material language;
- lighting target;
- camera/framing rules;
- shape language;
- detail density;
- performance/platform constraints.

Record the delivery target: Blender-only image/scene, exported asset or target-engine
use. A Blender-only slice uses the intended Blender renderer and camera; engine
import/gameplay checks apply only when delivery includes them. Do not require an
engine or manufacture runtime requirements for a static diorama.

If no formal art bible exists, derive only the minimum needed for the look-dev pass.

## 2. Representative slice

Build a small scene containing enough variety to expose visual incompatibilities.

Typical 3D slice:

- one hero/focal asset;
- one environment/module sample;
- one small prop;
- representative materials;
- lighting/post-processing;
- camera;
- scale reference;
- optional character;
- minimal UI/HUD if UI materially affects the composition.

Do not produce a whole level.

## 3. Quality questions

Evaluate:

### Shape
- silhouette;
- proportion language;
- bevel/edge treatment;
- thickness;
- geometric detail density.

### Materials
- roughness/metalness discipline;
- texture density;
- normal intensity;
- emission discipline;
- palette consistency.

### Lighting
- contrast;
- key/fill balance;
- readability;
- mood;
- exposure.

### Camera
- gameplay distance;
- FOV/orthographic scale;
- framing;
- expected asset screen size.

### Cohesion
- do assets look like they belong to the same game?
- does one category visually overpower another?
- does the result still match the references?

### Runtime when delivery includes a target engine
- target engine import;
- shader/material compatibility;
- expected performance budget;
- readability during actual gameplay.

## 4. Evidence

Prefer fixed-view comparisons.

Capture:

```text
PRODUCTION VIEW (gameplay view when applicable)
HERO DETAIL VIEW
WIDE ENVIRONMENT VIEW
OPTIONAL MATERIAL/LIGHTING DEBUG VIEW
```

Keep comparison camera, lighting, and resolution stable between iterations whenever the goal is before/after evaluation.

## 5. Gate result

Possible status:

```text
OPEN
PASS
PASS WITH RECORDED LIMITATIONS
REWORK
BLOCKED
```

PASS requires:

- the representative slice matches the intended direction closely enough for production;
- major asset categories can share the same visual language;
- when engine delivery is requested, engine import does not destroy the intended look;
- known limitations are recorded;
- no unresolved primary-form or lighting contradiction remains.

## 6. Production lock

When the gate passes, record a compact production contract:

```text
LOOKDEV VERSION:
REFERENCE SET:
PALETTE:
SHAPE RULES:
MATERIAL RULES:
LIGHTING RULES:
CAMERA RULES:
DETAIL DENSITY:
RUNTIME LIMITS:
NEVER / AVOID:
APPROVED CAPTURES:
```

Downstream asset skills should consume this contract.

It is a baseline, not an excuse to block all evolution.

## 7. Reopen triggers

Reopen look-dev when:

- art direction materially changes;
- camera changes enough to alter asset requirements;
- rendering pipeline changes;
- the target platform changes visual/performance constraints;
- new asset categories clearly do not fit;
- repeated local fixes indicate the baseline itself is wrong.

Do not reopen it for every small prop.

## 8. Anti-regression

Before changing the look-dev baseline:

```text
REQUESTED IMPROVEMENT:
MUST PRESERVE:
KNOWN GOOD CAPTURES:
```

Afterwards:

```text
Did the intended visual problem improve?
Did readability worsen?
Did another view worsen?
Did material consistency worsen?
Did runtime cost materially worsen?
Did the scene drift from the reference contract?
```

Keep only net-positive changes.

## 9. Handoff to production

Output:

```text
STATUS:
APPROVED VISUAL BASELINE:
PRODUCTION RULES:
RUNTIME RULES:
KNOWN LIMITATIONS:
ASSET CATEGORIES CLEARED FOR MASS PRODUCTION:
CATEGORIES STILL REQUIRING THEIR OWN TEST:
```

## 10. Stop conditions

Stop when the visual baseline is strong enough to guide production.

Do not continue polishing the look-dev scene into a final level unless explicitly requested.

## Pitfalls / Lessons Learned

Keep fixed views and target engine settings comparable when evaluating a visual baseline.
