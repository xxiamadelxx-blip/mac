# XP, levels and rewards — 30-minute model

Status: `PARTIAL / MODEL_ONLY`.

## XP authority

The simulator reads the B1 formula from JSON:

```text
XP_to_next(L) = round(30 + 12 × (L − 1) + 3 × (L − 1)^1.35)
```

Canonical drop vocabulary is `1 / 5 / 15 / 40 / 80 / 250` XP. The mapping of
new IDs to those drops, late-run pickup capacity and all proposed mini-boss
values are explicit in the model and remain non-canonical where B1 is silent.

## Levels at checkpoints

Columns are 02:00 / 05:00 / 10:00 / 15:00 / 20:00 / 25:00 / 30:00. Each
profile row is stable for both heroes in the deterministic seed set.

| Profile | Levels |
|---|---|
| fresh | 2 / 5 / 9 / 13 / 17 / 20 / 24 |
| moderate | 2 / 6 / 10 / 13 / 17 / 21 / 24 |
| max M1 | 2 / 6 / 10 / 14 / 18 / 22 / 26 |

The first five-minute anchors come from B1 targets; 25:00/30:00 progression is
the proposed extension and needs B1/Product promotion.

## Checkpoint reward rows

| Checkpoint | Gold | Lunar Seals | Boss Essence | Status |
|---|---:|---:|---:|---|
| 05:00 main | 50 | 15 | 1 | CANON B1 |
| 07:30 mini | 40 | 10 | 1 | PROPOSED |
| 10:00 main | 75 | 20 | 1 | CANON B1 |
| 12:30 mini | 50 | 12 | 1 | PROPOSED |
| 15:00 main | 100 | 25 | 1 | CANON B1 |
| 17:30 mini | 60 | 14 | 1 | PROPOSED |
| 20:00 main | 200 | 60 | 2 | CANON B1 |
| 22:30 mini | 70 | 16 | 1 | PROPOSED |
| 25:00 main | 250 | 70 | 2 | PROPOSED extension |
| 27:30 mini | 80 | 18 | 1 | PROPOSED |
| 30:00 final | 300 | 80 | 3 | PROPOSED extension |

Model formulas:

```text
first clear = all checkpoint rows + first_clear_bonus
repeat clear = all checkpoint rows
defeat after checkpoint = round(checkpoint_gold × 0.50)
                       + the defeated checkpoint's seals/essence
```

## Reward results

| Scenario | Gold | Lunar Seals | Boss Essence | Artifact offer |
|---|---:|---:|---:|---|
| First clear | 1575 | 520 | 16 | separate exactly-three-card offer |
| Repeat clear | 1275 | 340 | 15 | no first-clear bonus offer |

The final boss has no boss chest. Non-final main/mini checkpoints use the
separate chest path; missing eligible synergy resolves the bounded fallback.
Elite packs create a separate three-card artifact offer and do not mutate the
wallet.

## Idempotency evidence

The model uses deterministic `{run_id}:{scope}:{checkpoint}:{reward_type}` keys.
For the five-seed run set:

```text
wallet reward idempotency: PASS
boss/mini chest idempotency: PASS
elite-pack offer idempotency: PASS
first-clear duplicate settlement: PASS
```

This is replay evidence only. Runtime `RewardLedger`, save/reload and UI offer
evidence remain Runtime-owned blockers.
