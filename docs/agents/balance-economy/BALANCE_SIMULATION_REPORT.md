# Balance Simulation Report — deterministic 30-minute model

Status: `PARTIAL / SIMULATED_MODEL_ONLY`.

The model is now complete enough to calculate the full content catalog, but it
is not the Godot runtime. It cannot prove FPS, collision, telegraph readability
or player behavior.

## Reproduction

```text
python3 -m json.tool BALANCE_MODEL.json
python3 -m py_compile balance_simulator.py balance_contract_validator.py verify_balance_30m.py
python3 balance_contract_validator.py --model BALANCE_MODEL.json
python3 verify_balance_30m.py --model BALANCE_MODEL.json --simulator balance_simulator.py
```

The model keeps the B1 XP threshold formula and drop denominations. The late
pickup budgets are proposed at `22.0 XP/s` for 20:00–25:00 and `27.0 XP/s` for
25:00–30:00. Level 40 requires `16,852 XP`; level 38 is the accepted lower
variance floor, not a forced failure.

## Independent replay

```text
BALANCE_MODEL_CHECK=PASS
waves=7 main_bosses=6 mini_bosses=5 elite_variants=10
single-seed shape_check=PASS, run_count=6
INDEPENDENT_30M_CHECK=PASS
run_count=30
repeat_hash=c741b3d238fd8df29bc20caf36e89a9522204796e92d00efd0f0fe834ae4174c
survived=30
completed=30
runtime_claim=NOT_IMPLEMENTED
```

Seeds: `101, 202, 303, 404, 505`. Profiles: `fresh`, `moderate`, `max_m1`.
Heroes: `hero_lin_yue`, `hero_seoyeon_han`.

## Deterministic acceptance checks

| Check | Observed | Status |
|---|---|---|
| Full catalog coverage | 10/10/10/10/10/10/6/5 | PASS / MODEL |
| Visible run duration | 1800 seconds | PASS / MODEL |
| Main checkpoints | 6 at 300-second cadence | PASS / MODEL |
| Mini checkpoints | 5 at midpoint windows | PASS / MODEL |
| Main clock | frozen through intro/active/settlement | PASS / MODEL |
| Mini clock | visible run/wave/XP/spawn continues | PASS / MODEL |
| Wave envelope | 7 contiguous bands, 0–1800 | PASS / MODEL |
| Active cap | no occupancy above selected cap | PASS / MODEL |
| Post-boss ramp | five monotonic relief-to-siege cycles | PASS / MODEL |
| Main/mini TTK | concrete values in combat report | PARTIAL / PROPOSED |
| Incoming single-hit bound | worst sample 14/90 = 15.56% | PARTIAL / WATCH |
| Final boss chest | no boss chest | PASS / MODEL |
| Reward idempotency | wallet/chest/elite/first-clear duplicate-safe | PASS / MODEL |
| Godot invocation | not run | BLOCKED |
| Android FPS/occupancy | not measured | BLOCKED |

## Profile outcomes

| Profile / hero | Survived | Completed | Min HP mean | Incoming mean | Peak mean | Cap max / p95 |
|---|---:|---:|---:|---:|---:|---:|
| fresh / Lin Yue | 5/5 | 5/5 | 39.880 | 50.120 | 45.080 | 400 / 382.000 |
| fresh / Soyeon Han | 5/5 | 5/5 | 61.770 | 48.230 | 49.280 | 400 / 382.000 |
| moderate / Lin Yue | 5/5 | 5/5 | 57.739 | 37.661 | 46.099 | 400 / 382.000 |
| moderate / Soyeon Han | 5/5 | 5/5 | 77.292 | 39.308 | 46.648 | 400 / 382.000 |
| max M1 / Lin Yue | 5/5 | 5/5 | 86.265 | 21.735 | 34.272 | 400 / 382.000 |
| max M1 / Soyeon Han | 5/5 | 5/5 | 113.730 | 18.270 | 41.328 | 400 / 382.000 |

## Boss and reward results

Across the completed seed-101 fresh Lin Yue model run:

- six main bosses and five mini-bosses resolved;
- visible run clock `1800.0s`, wall clock `2261.5s`;
- main TTK sequence `62.25 / 54.75 / 48.50 / 89.25 / 81.50 / 81.75s`;
- mini TTK sequence `39.00 / 36.00 / 33.25 / 36.00 / 35.25s`;
- level sequence `2 / 5 / 9 / 13 / 17 / 30 / 40` at 02:00/05:00/10:00/15:00/20:00/25:00/30:00;
- distinct synergies `3`: `synergy_heavenly_seals`, `synergy_winter_palace`, `synergy_nine_reflections`;
- first-clear ledger `1575 Gold / 520 Lunar Seals / 16 Boss Essence`;
- final boss chest `false`, artifact choice count `3`;
- wallet, chest, elite offer and first-clear idempotency `PASS`.

## Interpretation boundary

`MODEL PASS` means the JSON model and deterministic replay satisfy the stated
mathematical invariants. It does not promote proposed values to canonical and
does not close the Architecture/Runtime/Godot/Android gates.
