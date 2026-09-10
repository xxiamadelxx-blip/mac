# XP, Level and Reward Model — 30-minute slice

Status: `PARTIAL / MODEL_ONLY`.

## XP curve

The model evaluates the B1 formula directly from JSON:

```text
XP_to_next(L) = round(30 + 12 × (L − 1) + 3 × (L − 1)^1.35)
```

XP drops use the model's explicit ordinary/elite/boss records and the pickup
capacity policy; the simulator does not contain a second XP curve.

## Levels at visible run checkpoints

Columns are level at 02:00 / 05:00 / 10:00 / 15:00 / 20:00 / 25:00 / 30:00.
Each row is the deterministic five-seed aggregate; the level sequence is
identical for both heroes within a profile.

| Profile | Levels |
|---|---|
| fresh | 2 / 5 / 9 / 13 / 17 / 20 / 24 |
| moderate | 2 / 6 / 10 / 13 / 17 / 21 / 24 |
| max M1 | 2 / 6 / 10 / 14 / 18 / 22 / 26 |

The 25:00 and 30:00 anchors are continuation targets because B1 stops at the
20-minute baseline. They remain `PROPOSED` in the model.

## Checkpoint rewards

| Checkpoint | Gold | Lunar Seals | Boss Essence | Status |
|---|---:|---:|---:|---|
| 05:00 main | 50 | 15 | 1 | `CANON` B1 |
| 07:30 mini | 40 | 10 | 1 | `PROPOSED` |
| 10:00 main | 75 | 20 | 1 | `CANON` B1 |
| 12:30 mini | 50 | 12 | 1 | `PROPOSED` |
| 15:00 main | 100 | 25 | 1 | `CANON` B1 |
| 17:30 mini | 60 | 14 | 1 | `PROPOSED` |
| 20:00 main | 200 | 60 | 2 | `CANON` B1 |
| 22:30 mini | 70 | 16 | 1 | `PROPOSED` |
| 25:00 main | 250 | 70 | 2 | `PROPOSED` extension |
| 27:30 mini | 80 | 18 | 1 | `PROPOSED` |
| 30:00 final | 300 | 80 | 3 | `PROPOSED` extension |

Formulas and source/status records live in `BALANCE_MODEL.json`:

```text
first clear = sum(all checkpoint rows) + first_clear_bonus
repeat clear = sum(all checkpoint rows)
defeat after checkpoint = round(checkpoint_gold × 0.50),
                         plus only the defeated checkpoint's seals/essence
```

The model output for a completed 30-minute run is:

| Scenario | Gold | Lunar Seals | Boss Essence | Artifact offer |
|---|---:|---:|---:|---|
| First clear | 1575 | 520 | 16 | separate exactly-three-card offer |
| Repeat clear | 1275 | 340 | 15 | no first-clear offer |

The final boss has no boss chest. Non-final main/mini checkpoints resolve a
separate chest path; a missing eligible synergy resolves the model fallback.
Elite packs are a separate three-card artifact-offer source and do not mutate
wallets.

## Idempotency evidence

Every wallet, chest, elite offer and first-clear result uses a deterministic
scope/checkpoint key. The independent checker observed:

```text
wallet reward idempotency: PASS
boss/mini chest idempotency: PASS
elite-pack offer idempotency: PASS
first-clear duplicate settlement: PASS
```

This is model evidence only. Runtime `RewardLedger` traces and save/reload
replay remain Runtime-owned blockers.
