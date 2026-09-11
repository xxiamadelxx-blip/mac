# Balance Combat Model — 30-minute evidence

Status: `PARTIAL / MODEL_ONLY`. The JSON contains explicit proposed absolute
values for every content record; none of the values absent from B1 is presented
as canonical.

## Equations and authority

```text
post_armor_damage = raw_damage × (1 − damage_reduction_fraction)
expected_crit = 1 + crit_chance × (crit_multiplier − 1)
weapon_level_multiplier = 1 + 0.10 × (weapon_level − 1)
TTK = effective_HP / focused_DPS
late_stats = proposed_base_stats × proposed_wave_multiplier
```

`balance_simulator.py` reads the single `BALANCE_MODEL.json`; it contains no
second copy of weapon, enemy, elite, boss or reward tuning.

## Risk results — five seeds per profile/hero

`min HP` is the lowest simulated HP; incoming is total landed damage; peak is
the largest step DPS; max hit is the largest landed event. A death may produce a
negative final sample because the simulator records the post-hit state.

| Profile / hero | Survived | Completed | Min HP mean / min | Incoming mean | Peak mean | Max hit mean / max |
|---|---:|---:|---:|---:|---:|---:|
| fresh / Lin Yue | 4/5 | 4/5 | 37.080 / -0.300 | 52.920 | 51.800 | 12.950 / 14.000 |
| fresh / Soyeon Han | 5/5 | 5/5 | 79.970 / 56.800 | 30.030 | 45.360 | 11.340 / 14.000 |
| moderate / Lin Yue | 5/5 | 5/5 | 65.010 / 59.042 | 30.390 | 45.276 | 11.319 / 13.720 |
| moderate / Soyeon Han | 5/5 | 5/5 | 94.099 / 73.039 | 22.501 | 37.593 | 9.398 / 12.005 |
| max M1 / Lin Yue | 5/5 | 5/5 | 79.524 / 69.255 | 28.476 | 42.840 | 10.710 / 12.600 |
| max M1 / Soyeon Han | 5/5 | 5/5 | 105.288 / 92.310 | 26.712 | 43.344 | 10.836 / 12.600 |

The largest model hit is 14.0 HP, or 15.56% of the 90-HP Lin Yue base. The
independent acceptance bound is 15%; this is a model watch requiring either a
hit-rate/telegraph correction or B1 decision, not a hidden status change.

## Main-boss TTK, seconds

Values are deterministic for the fixed build path. Columns are 05:00 / 10:00 /
15:00 / 20:00 / 25:00 / 30:00.

| Profile / hero | TTK sequence |
|---|---|
| fresh / Lin Yue | 70.00 / 64.00 / 60.75 / 95.75 / 88.75 / 82.25 |
| fresh / Soyeon Han | 75.00 / 69.00 / 67.50 / 110.25 / 103.50 / 94.50 |
| moderate / Lin Yue | 59.50 / 55.00 / 55.50 / 87.75 / 81.00 / 75.00 |
| moderate / Soyeon Han | 64.50 / 60.25 / 62.25 / 100.75 / 95.25 / 87.00 |
| max M1 / Lin Yue | 46.00 / 42.50 / 41.50 / 65.75 / 54.25 / 58.00 |
| max M1 / Soyeon Han | 50.00 / 47.00 / 46.75 / 76.75 / 62.75 / 67.25 |

The 05:00–15:00 results sit in the B1 45–80 second first-slice window. The
20:00–30:00 records are proposed late-run extensions. Fresh Soyeon at 20:00
and the fresh Lin Yue final result are explicit watch points against the
proposed late/final targets.

## Mini-boss TTK, seconds

Columns are 07:30 / 12:30 / 17:30 / 22:30 / 27:30.

| Profile / hero | TTK sequence |
|---|---|
| fresh / Lin Yue | 46.25 / 41.00 / 38.50 / 36.00 / 32.00 |
| fresh / Soyeon Han | 50.25 / 45.00 / 43.50 / 42.00 / 36.75 |
| moderate / Lin Yue | 42.25 / 37.25 / 35.50 / 33.00 / 29.00 |
| moderate / Soyeon Han | 45.75 / 41.25 / 40.50 / 38.50 / 34.00 |
| max M1 / Lin Yue | 31.25 / 28.50 / 26.75 / 25.25 / 22.75 |
| max M1 / Soyeon Han | 33.75 / 31.50 / 30.25 / 29.75 / 26.50 |

Mini numeric records are proposed because B1 does not define them. Their 20–55
second target is represented in the model and remains pending product/B1 lock.

## Ordinary and elite TTK

Representative seed `101` outputs from the full ten-content model:

| Profile / hero | Ordinary mean / p95 | Elite-variant mean / p95 |
|---|---:|---:|
| fresh / Lin Yue | 1.25 / 5.25 | 9.00 / 15.50 |
| fresh / Soyeon Han | 0.75 / 4.50 | 3.75 / 4.50 |
| moderate / Lin Yue | 1.25 / 4.25 | 9.00 / 12.00 |
| moderate / Soyeon Han | 0.75 / 3.50 | 3.75 / 9.50 |
| max M1 / Lin Yue | 0.75 / 2.75 | 3.75 / 10.50 |
| max M1 / Soyeon Han | 0.50 / 2.00 | 4.50 / 7.50 |

Ordinary means meet the 0.5–2.5 target. Elite variants use a proposed 5–15
second reference; lower outliers on high-damage Soyeon builds and role p95
values are intentionally exposed as tuning watches.

## Remaining combat blockers

- B1 lacks absolute new-family and late-run stats, exact elite cadence and a
  hit-probability/crit pipeline.
- The largest landed-hit sample is slightly over the strict 15% bound in one
  proposed run; runtime telegraphs and hit-rate evidence are required before
  changing the number.
- No Godot collision, telegraph, movement, save/reload or Android performance
  evidence exists.
