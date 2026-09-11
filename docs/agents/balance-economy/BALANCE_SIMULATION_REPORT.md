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

Local candidate evidence used the same files under the temporary names
`current_balance_model.json`, `current_balance_simulator.py` and
`current_balance_validator.py` before publication.

## Independent replay

```text
BALANCE_MODEL_CHECK=PASS
waves=7 main_bosses=6 mini_bosses=5 elite_variants=10
single-seed shape_check=PASS, run_count=6
INDEPENDENT_30M_CHECK=PASS
run_count=30
repeat_hash=071ecb2bc1eb23ea389fab4d1ff331c6beb3711284f2e6abeb08d7d3921dbbde
survived=29
completed=29
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
| fresh / Lin Yue | 4/5 | 4/5 | 37.080 | 52.920 | 51.800 | 400 / 373.600 |
| fresh / Soyeon Han | 5/5 | 5/5 | 79.970 | 30.030 | 45.360 | 400 / 382.000 |
| moderate / Lin Yue | 5/5 | 5/5 | 65.010 | 30.390 | 45.276 | 400 / 382.000 |
| moderate / Soyeon Han | 5/5 | 5/5 | 94.099 | 22.501 | 37.593 | 400 / 382.000 |
| max M1 / Lin Yue | 5/5 | 5/5 | 79.524 | 28.476 | 42.840 | 400 / 382.000 |
| max M1 / Soyeon Han | 5/5 | 5/5 | 105.288 | 26.712 | 43.344 | 400 / 382.000 |

## Boss and reward results

Across the completed seed-101 fresh Lin Yue model run:

- six main bosses and five mini-bosses resolved;
- visible run clock `1800.0s`, wall clock `2261.5s`;
- main TTK sequence `70.00 / 64.00 / 60.75 / 95.75 / 88.75 / 82.25s`;
- mini TTK sequence `46.25 / 41.00 / 38.50 / 36.00 / 32.00s`;
- first-clear ledger `1575 Gold / 520 Lunar Seals / 16 Boss Essence`;
- final boss chest `false`, artifact choice count `3`;
- wallet, chest, elite offer and first-clear idempotency `PASS`.

## Interpretation boundary

`MODEL PASS` means the JSON model and deterministic replay satisfy the stated
mathematical invariants. It does not promote proposed values to canonical and
does not close the Architecture/Runtime/Godot/Android gates.
