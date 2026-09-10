# Balance Simulation Report — 30-minute extension

Status: `PARTIAL / SIMULATED_MODEL_ONLY`

## Inputs

- model: `docs/agents/balance-economy/BALANCE_MODEL.json`;
- live architecture revision: `bd1d4d44f9c0a525b26ac136d98ace3cf76a3d00`;
- duration: 1800 visible-run seconds;
- main bosses: six checkpoints at 300-second cadence;
- mini-bosses: five model checkpoints at 450/750/1050/1350/1650 seconds;
- profiles: `fresh`, `moderate`, `max_m1`;
- heroes: `hero_lin_yue`, `hero_seoyeon_han`;
- seeds: 101, 202, 303, 404, 505;
- total runs: 30;
- runtime: not executed.

Independent checker: `INDEPENDENT_30M_CHECK=PASS`. Repeat hash: `2d901903a59cc88926b4413c5caa71cb92e2321cd3b446e93e6ee14db5f43d92`.

## Profile results

| Profile | Survived | Completed in final window | Level 02:00 | 05:00 | 10:00 | 15:00 | 20:00 | 25:00 | 30:00 | Total incoming damage mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fresh | 5/10 | 2/10 | 2 | 5 | 9 | 13 | 17 | 20 | 24 | 86.110 |
| moderate | 9/10 | 9/10 | 2 | 6 | 10 | 13 | 17 | 21 | 24 | 68.468 |
| max_m1 | 10/10 | 10/10 | 2 | 6 | 10 | 14 | 18 | 22 | 26 | 52.488 |

Levels are reached values on runs that reach the checkpoint; `None` means the run died earlier. They are simulated progression, not runtime telemetry. Total incoming damage ranges were fresh 50.80–116.90, moderate 48.755–96.530, max M1 28.440–81.090.

## TTK

Main-boss TTK ranges across both heroes and five seeds:

| Checkpoint | fresh | moderate | max M1 | Model target |
|---|---:|---:|---:|---:|
| 05:00 | 70.0–75.0s | 59.5–64.5s | 46.0–50.0s | 45–80s |
| 10:00 | 70.5–78.0s | 62.5–70.5s | 48.0–54.5s | 45–80s |
| 15:00 | 63.25–70.5s | 58.25–65.0s | 44.75–50.0s | 45–80s |
| 20:00 | 110.75–123.75s | 101.5–113.25s | 78.5–87.75s | proposed late 60–100s |
| 25:00 | 110.25–122.25s | 100.5–112.5s | 78.0–86.75s | proposed late 60–100s |
| 30:00 final | 117.25–130.5s | 107.25–119.75s | 82.75–92.75s | 90–120s |

Mini-boss TTK ranges: fresh 42.5–54.75s, moderate 39.0–50.25s, max M1 30.25–38.25s; proposed target 20–55s.

Ordinary TTK medians remain in [0.5, 2.5] seconds. Existing elite TTK medians are reported against [10, 25] seconds. Elite-variant mean ranges are fresh 7.0–20.25s, moderate 5.75–14.5s and max M1 7.0–15.25s against the proposed [5, 15] target; fresh/high-durability anchors need tuning.

## Incoming damage and occupancy

- Mean peak incoming DPS ranges by profile: fresh 40.0–56.0, moderate 48.608–54.880, max M1 36.0–63.0.
- Maximum proposed active occupancy: 400; per-profile maximum ranges are fresh 340–400, moderate 330–400 and max M1 400.
- Per-profile p95 occupancy ranges are fresh 324–382, moderate 291–382 and max M1 382.
- Occupancy cap behavior discards overflow attempts; there is no hidden spawn debt.
- Single-hit telegraph-bound checks and reward idempotency passed in all model runs.

## Boss and reward behavior

- Main bosses freeze visible run/wave/XP/spawn clocks in the model; mini-bosses keep them moving.
- A completed moderate sample (`hero_lin_yue`, seed 101) resolves all six main and five mini encounters; main TTKs are 59.5/62.5/58.25/101.5/100.5/107.25s and mini TTKs are 45.5/43.5/39.0/39.75/42.25s.
- Completed model runs receive the proposed ledger total `gold 1575 / moon_seals 520 / boss_essence 16`; failed runs retain only rewards already settled before death.
- Elite packs are finite post-mini events, use only the three architecture variant IDs and create a three-card artifact offer without wallet mutation.
- Duplicate wallet, boss-chest and elite-offer attempts are idempotent in all 30 runs.
- The 30:00 final boss creates no boss chest; the first-clear artifact offer is a separate post-result flow.
- Runtime execution, Godot collision/telegraph traces and Android FPS are not evidenced.

## Decision-required blockers

1. Reconcile the live architecture clock rule (currently advances through bosses) with the balance freeze rule for all main bosses.
2. Reconcile the five-mini balance schedule with the architecture registry, which currently has three intermediate slots at 450/750/1350; register the two extra slots or approve three instead of five.
3. Content/Architecture must provide names, mechanics and stable records for pending main/mini content; B1 must approve variant numeric overrides.
4. B1/Product must approve or replace the proposed 20–30 wave anchors, XP curve, combat values and extension rewards.
5. Runtime must consume this single model and emit timer, wave, XP, combat and idempotency traces.
6. Product must define the fresh-profile completion target; current model completion is 2/10 fresh.

Next implementation slice: resolve the clock and five-vs-three mini schedule decisions in the architecture/content contract, then wire runtime consumers to this model and rerun the same seed set without changing Python constants.