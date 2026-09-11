# Balance Wave Table — 30-minute model

Status: `PARTIAL / MODEL_ONLY`.

`CANON` means the value is explicit in live B1. The 20:00–30:00 extension and
post-boss numeric ramp are `PROPOSED`; they are not silently treated as B1.

## Wave envelope

| Band | Time | Spawn budget/s | Active cap | HP× | ATK× | Speed× | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| `wave_warmup_0_2` | 0–120 | 6 | 40 | 1.00 | 0.70 | 0.90 | CANON B1 §4 |
| `wave_pressure_2_5` | 120–300 | 10 | 80 | 1.10 | 0.85 | 1.00 | CANON B1 §4 |
| `wave_threat_5_10` | 300–600 | 15 | 130 | 1.35 | 1.00 | 1.02 | CANON B1 §4 |
| `wave_elite_10_15` | 600–900 | 22 | 200 | 1.70 | 1.25 | 1.05 | CANON B1 §4 |
| `wave_eclipse_15_20` | 900–1200 | 30 | 280 | 2.20 | 1.55 | 1.08 | CANON B1 §4 |
| `wave_cataclysm_20_25` | 1200–1500 | 38 | 340 | 2.70 | 1.75 | 1.10 | PROPOSED extension |
| `wave_apocalypse_25_30` | 1500–1800 | 48 | 400 | 3.30 | 2.00 | 1.12 | PROPOSED extension |

Each JSON field has source, formula, rationale and status. Overflow attempts are
discarded rather than queued as spawn debt; ordinary and elite entities count
toward the selected cap.

XP progression is intentionally a target envelope, not an exact per-run
contract. The B1 threshold formula and early pickup denominations remain
unchanged; the proposed late pickup capacities are `22.0 XP/s` for 20:00–25:00
and `27.0 XP/s` for 25:00–30:00. This produces a 25:00 target of levels 29–31
and a 30:00 target of level 40, with level 38 accepted as normal variance. The
paired-offer model makes three distinct 10/10 synergy paths reachable within
the 40-level target; it does not force every seed to land on exactly level 40.

## Boss cadence and clock

- Main bosses: 300/600/900/1200/1500/1800 seconds.
- Mini-bosses: 450/750/1050/1350/1650 seconds.
- MAIN: visible run, wave, XP and ordinary-spawn clocks freeze from intro to
  settlement; encounter time is separate.
- MINI: visible run, wave, XP and ordinary-spawn clocks continue.
- Final 30:00 main boss has no boss chest.

## Post-boss density shape

For every non-final main checkpoint the model follows:

```text
peak-density siege → boss interruption → relief → low entry → monotonic ramp → peak siege
```

The proposed numeric policy is reset factor `0.80`, zero-spawn suppression for
8 seconds, recovery from `0.70` to `1.00` over 20 seconds, and a 60-second
final siege. These inputs are in `simulation_model.boss_wave_ramp`.

| Cycle after | Entry budget/cap | Peak budget/cap | Last phase |
|---|---:|---:|---|
| 05:00 → 10:00 | 8 / 64 | 15 / 130 | SIEGE at 1.00 |
| 10:00 → 15:00 | 12 / 104 | 22 / 200 | SIEGE at 1.00 |
| 15:00 → 20:00 | 17.6 / 160 | 30 / 280 | SIEGE at 1.00 |
| 20:00 → 25:00 | 24 / 224 | 38 / 340 | SIEGE at 1.00 |
| 25:00 → 30:00 | 30.4 / 272 | 48 / 400 | SIEGE at 1.00 |

The independent shape checker confirms all five cycles are monotonic and end in
the peak-density siege. It does not prove that Godot uses the same cadence.

## Occupancy evidence

Across the fixed seed/profile set, the model never exceeds the selected cap.
The representative seed `101` run reaches a final cap of `400`, with p95
occupancy `382`; this is a target envelope, not Android performance evidence.

| Check | Model result | Status |
|---|---|---|
| Seven contiguous bands | 0–1800 seconds | PASS / MODEL |
| Cap overflow | no occupancy above selected cap | PASS / MODEL |
| Post-boss ramp | relief → monotonic ramp → siege, five cycles | PASS / MODEL |
| Elite roster | 10 catalog IDs, at most 5 selected for a run | PASS / MODEL |
| Runtime occupancy/FPS | no Godot/device trace | BLOCKED |
