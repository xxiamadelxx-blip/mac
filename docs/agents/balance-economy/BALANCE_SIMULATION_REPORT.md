# Balance Simulation Report — 30-minute extension

Status: `PARTIAL / SIMULATED_MODEL_ONLY`

## Inputs

- model: `docs/agents/balance-economy/BALANCE_MODEL.json`;
- duration: 1800 visible-run seconds;
- main bosses: six checkpoints at 300-second cadence;
- mini-bosses: five proposed checkpoints at 450/750/1050/1350/1650 seconds;
- profiles: `fresh`, `moderate`, `max_m1`;
- heroes: `hero_lin_yue`, `hero_seoyeon_han`;
- seeds: 101, 202, 303, 404, 505;
- total runs: 30;
- runtime: not executed.

Independent checker result: `INDEPENDENT_30M_CHECK=PASS`. Repeat hash: `a2d4b1258c869da4f22a852e46a73166d419e6b59ed8bb33771971cbaa9f505a`.

## Profile results

| Profile | Survived | Completed in final window | Level 02:00 | 05:00 | 10:00 | 15:00 | 20:00 | 25:00 | 30:00 | Total incoming damage mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fresh | 5/10 | 1/10 | 2 | 5 | 9 | 13 | 17 | 20 | 24 | 93.75 |
| moderate | 9/10 | 9/10 | 2 | 6 | 10 | 13 | 17 | 21 | 24 | 73.05 |
| max_m1 | 10/10 | 10/10 | 2 | 6 | 10 | 14 | 18 | 22 | 26 | 45.55 |

Levels are identical across the five seeds within each profile in this model. They are simulated progression targets, not runtime telemetry.

## TTK

Main-boss TTK range across both heroes and five seeds:

| Checkpoint | fresh | moderate | max M1 | Model target |
|---|---:|---:|---:|---:|
| 05:00 | 70.0–75.0s | 59.5–64.5s | 46.0–50.0s | 45–80s |
| 10:00 | 70.5–78.0s | 62.5–70.5s | 48.0–54.5s | 45–80s |
| 15:00 | 63.25–70.5s | 58.25–65.0s | 44.75–50.0s | 45–80s |
| 20:00 | 110.75–123.75s | 101.5–113.25s | 78.5–87.75s | proposed late 60–100s |
| 25:00 | 110.25–122.25s | 100.5–112.5s | 78.0–86.75s | proposed late 60–100s |
| 30:00 final | 117.25–130.5s | 107.25–119.75s | 82.75–92.75s | 90–120s |

Mini-boss TTK ranges: fresh 42.5–54.75s, moderate 39.0–50.25s, max M1 30.25–38.25s; proposed target 20–55s.

Ordinary TTK medians remain in the model target band [0.5, 2.5] seconds. Existing elite archetypes use [10, 25] seconds. Elite-variant overlay means across runs range from 5.0 to 36.0 seconds against the proposed [5, 15] target; this is a tuning warning for high-durability anchors and remains PROPOSED, not canon.

## Incoming damage and occupancy

- Total incoming damage mean: fresh 93.75, moderate 73.05, max M1 45.55.
- Maximum observed total incoming damage: fresh 110.10, moderate 102.02, max M1 59.85.
- Maximum proposed active occupancy: 400; p95 occupancy is 361.1 fresh and 382.0 for moderate/max.
- Occupancy cap behavior discards overflow attempts; there is no hidden spawn debt.
- Single-hit telegraph-bound checks and reward idempotency passed in all model runs.

## Boss/reward behavior

- Main bosses freeze visible run/wave/XP/spawn clocks.
- Mini-bosses keep all four clocks moving.
- Five mini-boss defeats create five proposed boss-chest opportunities when the run reaches them.
- Elite packs are finite post-mini events and create an artifact offer without wallet mutation.
- Duplicate wallet, boss-chest and elite-offer attempts are idempotent in the model.
- The 30:00 final boss creates no boss chest; first-clear artifact offer remains a separate post-result flow.
- Runtime execution, Godot collision/telegraph traces and Android FPS are not evidenced.

## Decision-required blockers

1. Architecture must replace the 1200-second contract with the 1800-second schedule and add `MINI_BOSS` clock semantics.
2. Content/Architecture must provide IDs and skill kits for the two new main bosses and three additional mini-bosses.
3. B1 must approve or replace the proposed 20–30 wave anchors, mini stats, elite overlay and reward rows.
4. Runtime must consume this single model and emit timer, wave, XP, combat and idempotency traces.
5. Product must define the fresh-profile completion target; the current proposed model intentionally exposes fresh attrition rather than silently labelling it acceptable.

Next implementation slice: architecture/runtime registry sync for the 30-minute schedule, then rerun this same model without changing the Python constants.
