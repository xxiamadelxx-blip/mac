# Balance Combat Model — 30-minute model evidence

Status: `PARTIAL / MODEL_ONLY`. All absolute enemy/boss/mini/elite values not
present in B1 are `PROPOSED` or `PENDING_B1`; they are not canonical runtime
stats.

## Model equations

```text
post_armor_damage = raw_damage × (1 − damage_reduction_fraction)
expected_crit = 1 + crit_chance × (crit_multiplier − 1)
weapon_level_multiplier = 1 + 0.10 × (weapon_level − 1)
TTK = effective_HP / focused_DPS
```

The simulator reads these records from `BALANCE_MODEL.json`. It contains no
copied B1 tuning constants. The proposed enemy records expose HP, ATK, speed,
attack interval, contact delay and XP; elite records apply the linked overlay
formula `base × multiplier` and remain finite event content.

## Profile risk over five seeds

`min HP` is the lowest simulated player HP; `incoming total` is the mean total
landed incoming damage; `peak DPS` is the largest per-step incoming rate;
`max hit` is the largest landed hit.

| Profile / hero | Completed | Min HP | Incoming total | Peak DPS | Max hit |
|---|---:|---:|---:|---:|---:|
| fresh / Lin Yue | 5/5 | 19.65 | 45.920 | 49.000 | 12.250 |
| fresh / Soyeon Han | 5/5 | 41.05 | 35.280 | 49.000 | 12.250 |
| moderate / Lin Yue | 5/5 | 56.641 | 22.295 | 42.532 | 10.633 |
| moderate / Soyeon Han | 5/5 | 49.372 | 41.023 | 48.020 | 12.005 |
| max M1 / Lin Yue | 5/5 | 88.155 | 15.498 | 44.100 | 11.025 |
| max M1 / Soyeon Han | 5/5 | 96.090 | 23.562 | 50.400 | 12.600 |

The B1 single-hit bound is 15% of base HP. The worst model hit is 12.25% for
the 90-HP profile, so the model bound passes; this is not collision evidence.

## Main-boss TTK, seconds

Columns are 05:00 / 10:00 / 15:00 / 20:00 / 25:00 / 30:00.

| Profile / hero | TTK sequence |
|---|---|
| fresh / Lin Yue | 70.00 / 64.00 / 60.75 / 95.75 / 88.75 / 82.25 |
| fresh / Soyeon Han | 75.00 / 69.00 / 67.50 / 110.25 / 103.50 / 94.50 |
| moderate / Lin Yue | 59.50 / 55.00 / 55.50 / 87.75 / 81.00 / 75.00 |
| moderate / Soyeon Han | 64.50 / 60.25 / 62.25 / 100.75 / 95.25 / 87.00 |
| max M1 / Lin Yue | 46.00 / 42.50 / 41.50 / 65.75 / 54.25 / 58.00 |
| max M1 / Soyeon Han | 50.00 / 47.00 / 46.75 / 76.75 / 62.75 / 67.25 |

The first three columns are compared with the B1 first-slice target; 20:00–
30:00 values use the proposed late-main extension and must not be called a
balance lock. The fresh Soyeon late-main result is above the proposed 60–100s
window and is an explicit tuning watch, not silently corrected by a multiplier.

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

Mini-bosses continue the visible/wave/XP clock in the model. Their numeric
records are proposed from the short-encounter target because B1 has no absolute
mini-boss stats.

## Ordinary and elite TTK

Ordinary target is approximately 0.5–2.5s. Model means are 0.50–1.25s; role
outlier p95 values reach 5.75s in fresh Lin Yue and 3.75s in fresh Soyeon. Elite
variant means are generally 3.75–12.00s, with p95 outliers up to 23.25s. The
elite mean target is proposed at 5–15s, so the outliers remain a balance-watch
and require runtime/telegraph validation.

## Remaining combat blockers

- B1 does not provide absolute new-family base stats or elite overlays.
- B1 does not define hit probability, ranged cadence, crit pipeline or exact
  mini/elite cadence; proposed values are labelled in the model.
- No runtime collision, telegraph, movement or Android occupancy evidence is
  available.
