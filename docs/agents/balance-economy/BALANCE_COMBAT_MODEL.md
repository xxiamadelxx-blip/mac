# Balance Combat Model — 30-minute evidence

Status: `PARTIAL / MODEL_ONLY`. R2 proves the registry seam, but the JSON contains explicit proposed absolute
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
means over seeds `101, 202, 303, 404, 505`; the model records the post-hit state.

| Profile / hero | Survived | Completed | Min HP mean / min | Incoming mean | Peak mean | Max hit mean / max |
|---|---:|---:|---:|---:|---:|---:|
| fresh / Lin Yue | 5/5 | 5/5 | 49.890 / 28.050 | 40.110 | 43.960 | 10.027 / 12.250 |
| fresh / Soyeon Han | 5/5 | 5/5 | 49.870 / 33.350 | 60.130 | 46.760 | 11.270 / 12.250 |
| moderate / Lin Yue | 5/5 | 5/5 | 57.258 / 43.264 | 38.142 | 46.922 | 9.536 / 12.005 |
| moderate / Soyeon Han | 5/5 | 5/5 | 75.166 / 57.604 | 41.434 | 48.020 | 11.662 / 13.720 |
| max M1 / Lin Yue | 5/5 | 5/5 | 87.525 / 77.760 | 20.475 | 34.524 | 8.377 / 9.765 |
| max M1 / Soyeon Han | 5/5 | 5/5 | 105.288 / 96.090 | 26.712 | 37.800 | 9.765 / 11.025 |

The largest model hit is 13.72 HP, or 13.72% of the 100-HP base hero stat. It
stays below the 15% untelegraphed-hit bound in this replay; runtime telegraph
and hit-rate evidence is still required before treating that as verified.

## Main-boss TTK, seconds

These are representative seed `101` outputs for the fixed build path. Columns
are 05:00 / 10:00 / 15:00 / 20:00 / 25:00 / 30:00; the risk table is based on
the five-seed set.

| Profile / hero | TTK sequence |
|---|---|
| fresh / Lin Yue | 62.25 / 54.75 / 48.50 / 89.25 / 81.50 / 81.75 |
| fresh / Soyeon Han | 69.75 / 63.00 / 55.50 / 102.75 / 93.00 / 93.75 |
| moderate / Lin Yue | 52.00 / 46.00 / 44.25 / 81.50 / 74.50 / 74.50 |
| moderate / Soyeon Han | 58.75 / 54.25 / 51.50 / 94.25 / 85.50 / 86.50 |
| max M1 / Lin Yue | 40.00 / 35.25 / 33.75 / 63.00 / 57.50 / 57.50 |
| max M1 / Soyeon Han | 45.75 / 41.50 / 40.00 / 72.75 / 66.00 / 66.50 |

The 05:00–15:00 results sit in the B1 45–80 second first-slice window. The
20:00–30:00 records are proposed late-run extensions. Fresh Soyeon at 20:00
and the fresh Lin Yue final result are explicit watch points against the
proposed late/final targets.

## Mini-boss TTK, seconds

Columns are 07:30 / 12:30 / 17:30 / 22:30 / 27:30.

| Profile / hero | TTK sequence |
|---|---|
| fresh / Lin Yue | 39.00 / 36.00 / 33.25 / 36.00 / 35.25 |
| fresh / Soyeon Han | 45.00 / 42.00 / 38.25 / 41.25 / 39.75 |
| moderate / Lin Yue | 36.00 / 33.00 / 30.50 / 33.00 / 32.25 |
| moderate / Soyeon Han | 41.25 / 38.50 / 35.50 / 37.75 / 36.25 |
| max M1 / Lin Yue | 26.25 / 25.75 / 23.50 / 25.75 / 22.25 |
| max M1 / Soyeon Han | 30.25 / 29.75 / 27.00 / 29.25 / 26.00 |

Mini numeric records are proposed because B1 does not define them. Their 20–55
second target is represented in the model and remains pending product/B1 lock.

## Ordinary and elite TTK

Representative seed `101` outputs from the full ten-content model:

| Profile / hero | Ordinary mean / p95 | Elite-variant mean / p95 |
|---|---:|---:|
| fresh / Lin Yue | 1.25 / 4.50 | 11.00 / 11.00 |
| fresh / Soyeon Han | 0.75 / 3.75 | 9.75 / 9.75 |
| moderate / Lin Yue | 1.25 / 3.75 | 10.00 / 10.00 |
| moderate / Soyeon Han | 0.75 / 3.00 | 7.25 / 7.25 |
| max M1 / Lin Yue | 0.75 / 2.25 | 6.25 / 6.25 |
| max M1 / Soyeon Han | 0.50 / 2.00 | 5.75 / 5.75 |

Ordinary means meet the 0.5–2.5 target. Elite variants use a proposed 5–15
second reference; lower outliers on high-damage Soyeon builds and role p95
values are intentionally exposed as tuning watches.

## Elite registry and chest cadence

The model binds ten elite IDs to ten ordinary base families, projects at most
five IDs per deterministic window, and keeps the projection separate from the
permanent catalog. Five `ELITE_CHEST` windows are attached to the five mini
bosses. The offer is three cards, has no wallet mutation, and is settled once
per `{run_id}:ELITE_CHEST:{window_id}:ARTIFACT_OFFER`; an explicit duplicate
attempt returns the committed offer. A remaining finite pack is cleared at the
next main checkpoint boundary, which is why the late windows are not silently
lost at 30:00.

## Remaining combat blockers

- B1 lacks absolute new-family and late-run stats, exact elite cadence and a
  hit-probability/crit pipeline.
- The largest landed-hit sample is slightly over the strict 15% bound in one
  proposed run; runtime telegraphs and hit-rate evidence are required before
  changing the number.
- R2 structural evidence predates this numeric publication; no fresh Godot
  combat trace proves the proposed TTK or incoming-damage results.
- No collision, telegraph, movement, save/reload or Android performance
  evidence exists.
