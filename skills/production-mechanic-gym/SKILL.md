---
name: production-mechanic-gym
description: Build and tune one gameplay mechanic in an isolated playable gym. Use for new mechanics, combat or movement feel, timing, interaction, regression reproduction, and runtime playtest evidence.
---

# Production Mechanic Gym

Read the required [foundation contract](../../docs/foundation.md).

## 0. Purpose

Develop one mechanic in a controlled playable environment before integrating it into the main game.

This skill does not replace:
- engine-specific implementation skills;
- project-specific gameplay rules;
- QA / verification skills.

It defines the production loop around the mechanic.

## 1. Authority

Conflict order:

1. User's current explicit request.
2. Project-specific rules and locked design decisions.
3. Existing mechanic contract and invariants.
4. This skill.
5. Generic engine conventions.

Do not redesign unrelated systems just because the gym exposes weaknesses elsewhere.

## 2. Scope contract

Before implementation record internally:

```text
MECHANIC:
PLAYER INTENT:
INPUTS:
DEPENDENCIES:
TUNABLE PARAMETERS:
MUST PRESERVE:
OUT OF SCOPE:
ACCEPTANCE EVIDENCE:
```

The gym must test the smallest useful slice of the mechanic.

## 3. When a gym is required

Create or reuse a gym when at least one applies:

- a mechanic is new;
- game feel is being tuned;
- timings/windows/ranges matter;
- physics behavior is uncertain;
- a combat interaction must be validated;
- a regression is difficult to reproduce in the full game;
- multiple variants need A/B comparison;
- a mechanic is about to be declared stable/locked.

Do not create a new gym for a trivial cosmetic-only change.

## 4. Gym structure

A gym should contain only what is necessary to exercise the mechanic repeatedly.

Typical examples:

- melee: target dummy, blocking dummy, attacking dummy, range markers;
- movement: measured gaps, slopes, walls, speed markers;
- vehicle: straight, turn, ramp, surface changes, collision target;
- shooting: targets at known ranges, moving targets, TTK/damage readout;
- UI interaction: injected states, navigation paths, input-device switching.

Required controls when practical:

```text
Restart
Toggle debug/tuning UI
Pause / slow motion
Preset A / Preset B
Capture or log current tuning values
```

Use project-native controls when they already exist; do not invent a second debug framework unnecessarily.

## 5. Tunable parameters

Important feel parameters should be externalized from gameplay code whenever practical.

Examples:

- startup / active / recovery;
- cooldown;
- acceleration / braking;
- jump impulse / gravity scale;
- camera lag / shake;
- hit-stop;
- damage / knockback;
- aim assist;
- steering / grip;
- spawn cadence.

Numbers are evidence, not truth.

Translate vague feedback into measurable parameters where useful, but do not force every perceptual judgment into a number. A mechanic can pass numeric targets and still feel bad.

## 6. Live tuning

Prefer changing high-value tuning parameters without rebuilding or restarting the whole game.

The implementation may use:
- Godot Resources / exported debug controls;
- config/data files;
- engine debug inspectors;
- a small custom tuning panel;
- console commands.

Requirements:

- the mechanic reads the current value, not a stale startup copy;
- debug tuning must not leak into release behavior unintentionally;
- saved values must be reviewable as a diff;
- production values remain the source of truth.

## 7. Evidence loop

Default loop:

```text
IMPLEMENT
↓
RUN GYM
↓
OBSERVE / CAPTURE
↓
COMPARE AGAINST ACCEPTANCE
↓
TUNE
↓
RE-RUN
↓
KEEP / CORRECT / REVERT
```

Evidence can include:

- video or screenshots;
- timings / frame counts;
- measured distances;
- debug overlays;
- logs;
- test input traces;
- runtime state;
- user playtest feedback.

Exit code alone is never sufficient evidence of mechanic quality.

## 8. Playtest contract

When the user plays, provide a small set of concrete things to try.

Record:

```text
BUILD / COMMIT:
MECHANIC VERSION:
WHAT WAS TRIED:
USER FEEDBACK:
OBSERVED FAILURE:
TUNING CHANGED:
RESULT:
```

Preserve user wording for subjective feel when useful.

Do not mix feedback from several unrelated mechanics into one tuning pass.

## 9. Lock gate

A mechanic may be marked LOCKED only when:

- its explicit acceptance criteria pass;
- no known blocker remains for its intended scope;
- regression checks pass;
- relevant runtime evidence exists;
- the user has accepted subjective feel when user judgment is required.

Lock means:
- stable baseline;
- future changes must state why the lock is being reopened;
- downstream systems may depend on it.

Lock does not mean the mechanic can never change.

## 10. Regression rule

Before a meaningful change record:

```text
BASELINE:
EXPECTED IMPROVEMENT:
MUST PRESERVE:
```

After the change ask:

```text
Did the requested mechanic improve?
Did responsiveness worsen?
Did another interaction regress?
Did performance materially worsen?
Did input behavior change unexpectedly?
```

Decision:

```text
improvement + no material regression -> KEEP
improvement + local regression -> CORRECT
no meaningful improvement -> REVERT
net result worse -> REVERT
```

## 11. Stop conditions

Stop the gym pass when:

- the requested mechanic is locked for the current scope;
- a blocker belongs to another system and is clearly handed off;
- further tuning would be blind repetition;
- the user chooses to cut or redesign the mechanic.

Do not polish the whole game from inside the gym.

## 12. Handoff

```text
MECHANIC:
STATUS: idea | prototype | tuning | locked | blocked | cut
CHANGED:
FINAL PARAMETERS:
EVIDENCE:
REGRESSIONS CHECKED:
OPEN ISSUES:
NEXT DEPENDENCY:
```

## Pitfalls / Lessons Learned

Keep the gym scoped to a single behavior; compare playable evidence before locking tuning.
