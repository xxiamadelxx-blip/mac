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
The 20:00–25:00 and 25:00–30:00 pickup budgets are now `22.0` and `27.0`
XP/s. This is the requested late-run increase; the canonical XP threshold
formula and canonical drop denominations were not changed.

Level 40 requires `16,852 XP` under the unchanged B1 formula. Level 40 is the
target, not a mandatory result for every seed; level 38 is the accepted lower
model variance floor. Three synergies require three distinct 10/10 pairs, so
the model uses a proposed paired offer: one player level advances one weapon
and its linked passive together.

## Levels at checkpoints

Columns are 02:00 / 05:00 / 10:00 / 15:00 / 20:00 / 25:00 / 30:00. Each
profile row is stable for both heroes in the deterministic seed set.

| Profile | Levels |
|---|---|
| fresh | 2 / 5 / 9 / 13 / 17 / 30 / 40 |
| moderate | 2 / 6 / 10 / 13 / 17 / 30 / 41 |
| max M1 | 2 / 6 / 10 / 14 / 18 / 33 / 44 |

The first five-minute anchors come from B1 targets; the 20:00–30:00 values are
the proposed extension. These are seed-101 model values, not runtime results.

## Synergy results

| Profile | Seed-101 claims | Distinct IDs | Status |
|---|---:|---:|---|
| fresh / Lin Yue | 3 | 3 | PASS / MODEL |
| fresh / Soyeon Han | 3 | 3 | PASS / MODEL |
| moderate / Lin Yue | 3 | 3 | PASS / MODEL |
| moderate / Soyeon Han | 3 | 3 | PASS / MODEL |
| max M1 / Lin Yue | 3 | 3 | PASS / MODEL |
| max M1 / Soyeon Han | 3 | 3 | PASS / MODEL |

Across the independent five-seed set, every profile/hero run reaches at least
three distinct synergies; the level target remains a target with an accepted
variance floor rather than a forced per-run value.

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

## ELITE_CHEST cadence

| Window | Trigger checkpoint | Offer | Wallet mutation | Model settlement |
|---|---|---:|---|---|
| `elite_window_01` | 07:30 mini | 3 cards | no | finite pack clear |
| `elite_window_02` | 12:30 mini | 3 cards | no | finite pack clear |
| `elite_window_03` | 17:30 mini | 3 cards | no | pack clear or next main boundary |
| `elite_window_04` | 22:30 mini | 3 cards | no | pack clear or next main boundary |
| `elite_window_05` | 27:30 mini | 3 cards | no | pack clear or 30:00 main boundary |

The five window IDs and their checkpoint bindings are read from the model, not
repeated in the simulator. Boundary settlement is a proposed model rule that
keeps the reserved five-window cadence from being lost to the final-boss
transition.

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
`ELITE_CHEST` creates a separate three-card artifact offer and does not mutate
the wallet.

## Idempotency evidence

The model uses deterministic `{run_id}:{scope}:{checkpoint}:{reward_type}` keys
for wallet/checkpoint rewards and `{run_id}:ELITE_CHEST:{window_id}:ARTIFACT_OFFER`
for the five reserved elite windows.
For the five-seed run set:

```text
wallet reward idempotency: PASS
boss/mini chest idempotency: PASS
ELITE_CHEST offer idempotency: PASS
first-clear duplicate settlement: PASS
```

This is replay evidence only. Runtime `RewardLedger`, save/reload and UI offer
evidence remain Runtime-owned blockers.
