# Balance Wave Table — 30-minute model

Status: `PARTIAL / MODEL_ONLY`. `CANON` below means the value is present in
the live B1 baseline; it does not mean the current Godot runtime consumes it.
The 20:00–30:00 rows are `PROPOSED` extensions.

## Wave envelope

| Band | Time | Spawn budget/s | Active cap | HP mult | ATK mult | Speed mult | Provenance |
|---|---:|---:|---:|---:|---:|---:|---|
| `wave_warmup_0_2` | 0–120 | 6 | 40 | 1.00 | 0.70 | 0.90 | B1 §4 / `CANON` |
| `wave_pressure_2_5` | 120–300 | 10 | 80 | 1.10 | 0.85 | 1.00 | B1 §4 / `CANON` |
| `wave_threat_5_10` | 300–600 | 15 | 130 | 1.35 | 1.00 | 1.02 | B1 §4 / `CANON` |
| `wave_elite_10_15` | 600–900 | 22 | 200 | 1.70 | 1.25 | 1.05 | B1 §4 / `CANON` |
| `wave_eclipse_15_20` | 900–1200 | 30 | 280 | 2.20 | 1.55 | 1.08 | B1 §4 / `CANON` |
| `wave_cataclysm_20_25` | 1200–1500 | 38 | 340 | 2.70 | 1.75 | 1.10 | continuation formula / `PROPOSED` |
| `wave_apocalypse_25_30` | 1500–1800 | 48 | 400 | 3.30 | 2.00 | 1.12 | continuation formula / `PROPOSED` |

Every numeric row is stored as a model record with source and status. The
extension formulas are explicit in `BALANCE_MODEL.json`; they are not copied
into Python.

## Encounter envelope

Main bosses occur at `300, 600, 900, 1200, 1500, 1800` seconds. Mini-bosses
occur at `450, 750, 1050, 1350, 1650` seconds. Main-boss encounters freeze
the visible run/wave/XP/ordinary-spawn clock; mini-boss encounters continue
those clocks. This is the active coordination lock, while the first-run
architecture document still needs reconciliation.

For every non-final main-boss cycle:

```text
post-boss relief → low entry → linear ramp → peak-density siege → next boss
```

The model uses `post_boss_reset_factor = 0.80`, an 8-second zero-spawn
interruption, a 20-second 0.70→1.00 recovery, and a 60-second peak siege.
These four tuning inputs are `PROPOSED` where B1 does not supply the exact
value. The independent checker confirmed monotonic density and a final siege
sample at factor `1.0` for all five cycles.

Elite variants are finite packs after mini-boss defeat: one anchor variant plus
two ordinary escorts, one offer of three cards after the pack is resolved, and
no permanent roster mutation. The full catalog has ten IDs; the model's
run-scoped selected set is bounded to five.

## Cap rule

Ordinary and elite entities count toward the band cap. Overflow spawn attempts
are discarded rather than queued as spawn debt. The boss occupies a reserved
slot in the model. The simulator reports occupancy per fixed 0.25-second step;
it never exceeds the selected band cap. Runtime/Android occupancy is still
unmeasured.

## Acceptance status

Wave shape, ramp order, clock policy and cap behavior: `MODEL PASS`.
Numeric extension lock, runtime trace and Android performance: `PENDING` or
`BLOCKED` as documented in `BALANCE_AUDIT.md`.
