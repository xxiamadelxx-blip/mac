# Balance Simulation Report — 30-minute deterministic model

Status: `PARTIAL / SIMULATED_MODEL_ONLY`.

The simulator reads one `BALANCE_MODEL.json`; tuning values are not repeated in
Python. The model is not the Godot runtime and cannot prove FPS, collision,
telegraph readability or player behavior.

## Reproduction

```text
python3 -m json.tool current_balance_model.json
python3 -m py_compile current_balance_simulator.py current_balance_validator.py verify_balance_30m.py
python3 current_balance_validator.py --model current_balance_model.json --architecture current_architecture_contract.json
python3 verify_balance_30m.py --model current_balance_model.json --simulator current_balance_simulator.py
```

Independent output:

```text
BALANCE_MODEL_CHECK=PASS
waves=7 main_bosses=6 mini_bosses=5 elite_variants=10
ARCHITECTURE_JOIN=BLOCKED
INDEPENDENT_30M_CHECK=PASS
run_count=30
repeat_hash=e3fea44d1bda986bfae372d83ee7efabf9549e212ad63f2e61fa0242c22b758c
survived=30
completed=30
runtime_claim=NOT_IMPLEMENTED
```

Seeds: `101, 202, 303, 404, 505`. Profiles: `fresh`, `moderate`, `max_m1`.
Heroes: `hero_lin_yue`, `hero_seoyeon_han`.

## Deterministic model checks

| Check | Observed | Status |
|---|---|---|
| 30-minute visible run | 1800 seconds | PASS / MODEL |
| Main checkpoints | 6 at 300-second cadence | PASS / MODEL |
| Mini checkpoints | 5 at midpoint windows | PASS / MODEL |
| Main clock | frozen during intro/active/settlement | PASS / MODEL |
| Mini clock | visible run/wave/XP/spawn continue | PASS / MODEL |
| Wave envelope | 7 contiguous bands, 0–1800 | PASS / MODEL |
| Active cap | occupancy never exceeds selected band cap | PASS / MODEL |
| Post-boss ramp | relief → monotonic ramp → peak siege in 5 cycles | PASS / MODEL |
| Final chest | no boss chest at 30:00 | PASS / MODEL |
| Reward idempotency | wallet/chest/elite/first-clear duplicate-safe | PASS / MODEL |
| Godot invocation | not run | NOT_IMPLEMENTED |
| Android occupancy/FPS | not measured | BLOCKED |

## Ramp evidence, seed 101 / fresh Lin Yue

The five non-final cycles reset below the next peak and climb monotonically:

| Cycle | Entry budget/cap | Peak budget/cap | Interruption |
|---|---:|---:|---|
| after 05:00 | 8 / 64 | 15 / 130 | 0 → 0.70 in 8+20s |
| after 10:00 | 12 / 104 | 22 / 200 | 0 → 0.70 in 8+20s |
| after 15:00 | 17.6 / 160 | 30 / 280 | 0 → 0.70 in 8+20s |
| after 20:00 | 24 / 224 | 38 / 340 | 0 → 0.70 in 8+20s |
| after 25:00 | 30.4 / 272 | 48 / 400 | 0 → 0.70 in 8+20s |

The last sample of each cycle is `SIEGE` at density factor `1.0`. This is the
requested low-to-peak behavior; it is still a proposed model policy until the
Architecture/Runtime clock contract is reconciled.

## Reward and outcome evidence

Seed 101 fresh Lin Yue completed with visible clock `1800.0`, wall clock
`2261.5`, six main events and five mini events. Its first-clear ledger was
`1575 Gold / 520 Lunar Seals / 16 Boss Essence`; final boss chest was false;
artifact offer choice count was `3`; maximum single incoming hit was `12.25`
on a 90-HP base, below the model's 15% bound.

## Interpretation boundary

`MODEL PASS` means the JSON model and deterministic replay satisfy the stated
mathematical invariants. It does not promote proposed values to canonical, does
not resolve the architecture's legacy schedule, and does not close runtime or
Android evidence gates.
