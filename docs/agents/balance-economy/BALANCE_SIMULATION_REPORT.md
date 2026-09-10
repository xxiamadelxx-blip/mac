# Balance Simulation Report

Status: SIMULATED_MODEL_ONLY / PARTIAL

## Run snapshot

- Model source: docs/BALANCE_ECONOMY_SPEC.md revision 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687.
- Architecture source: docs/architecture/first-run/FIRST_RUN_DATA_CONTRACT.json revision 5a9697ef9d28a825726f42b2e63b6ffce8f66ba0.
- Historical live main HEAD observed at the start of the original implementation slice: ffc2e8d2f02d7a4d5c169151b2d59e5307ae5f2d.
- Balance model commit used: 42966b44650ec63aead33d04cbe34ae1e9d57489.
- Simulator commit used: 3dbe3f375b7d9cbd201d11943e79fa1c9582e86c.
- Historical main HEAD observed immediately before the original report update: 42966b44650ec63aead33d04cbe34ae1e9d57489.
- Latest verified main HEAD before this report refresh: 0536f182c1ae8876b9213e0c2fb761793e503a66.
- Seeds: 101, 202, 303, 404, 505.
- Runs: 30 (6 profile/hero slices × 5 seeds).
- Runtime executed: false.
- Balance↔architecture contract validator: PASS (boss, wave, build and policy IDs).
- Contract validator commit: bff8dae32d049a1d135c6491d62d18dc0be093ce.
- Repeated full-run SHA-256: f456c8a3469ae51e4e41db2f97df69969d245815459c660e52ff40b2045a7f33.

The simulator reads one BALANCE_MODEL.json. Tuning values absent from B1 are explicit PROPOSED/PENDING fields in that model. No balance number below should be read as CANON unless the source column says so. Stable IDs are joined against the architecture registry; the model does not copy architecture tuning values.

## Concrete profile inputs

| Profile | Meta ranks | Damage multiplier | Cooldown multiplier | Landed-hit probability | Status |
|---|---|---:|---:|---:|---|
| fresh | all 0 | 1.00 | 1.00 | 0.002 | PROPOSED |
| moderate | vitality 3, power 3, agility 2, focus 2, magnet 2, defense 2 | 1.06 | 0.97 | 0.0015 | PROPOSED |
| max_m1 | all branches rank 10 | 1.20 | 0.85 | 0.001 | PROPOSED |

Two architecture-compatible build routes were run for every profile:

- Lin Yue: hero_lin_yue / weapon_jade_talismans / passive_jade_focus / synergy_heavenly_seals.
- Soyeon Han: hero_seoyeon_han / weapon_moon_blade / passive_wind_of_travel / synergy_moon_dance.

## XP and levels

| Profile | Hero | First level-up (s) | Level at 2 / 5 / 10 / 15 / 20 min | Final |
|---|---|---:|---|---:|
| fresh | hero_lin_yue | 39.75 | 2 / 5 / 9 / 13 / 17 | 17 | 0 | 39.38 | 50.62 | 1.15 / 2.85 | 24.5 / 38.05 |
| fresh | hero_seoyeon_han | 39.75 | 2 / 5 / 9 / 13 / 17 | 17 | 0 | 63.04 | 46.96 | 0.75 / 2.4 | 18 / 33.3 |
| max_m1 | hero_lin_yue | 33.25 | 2 / 6 / 10 / 14 / 18 | 18 | 0 | 84.474 | 23.526 | 0.75 / 1.75 | 17.65 / 23.85 |
| max_m1 | hero_seoyeon_han | 33.25 | 2 / 6 / 10 / 14 / 18 | 18 | 0 | 115.116 | 16.884 | 0.5 / 1.25 | 12.35 / 18 |
| moderate | hero_lin_yue | 38.25 | 2 / 6 / 10 / 13 / 17 | 17 | 0 | 61.159 | 34.241 | 1.25 / 2.6 | 22.3 / 39.1 |
| moderate | hero_seoyeon_han | 38.25 | 2 / 6 / 10 / 13 / 17 | 17 | 0 | 83.868 | 32.732 | 0.75 / 1.75 | 15.1 / 27 |

B1 target comparison:

- first level: 30–45 seconds; all six slices are 33.25–39.75 seconds;
- level at 2/5/10/15/20 minutes: fresh is 2/5/9/13/17; moderate is 2/6/10/13/17; max M1 is 2/6/10/14/18;
- the moderate/max acceleration is an observed consequence of the proposed meta/pickup model, not a canonical claim.

## Combat and incoming risk

The TTK columns below are focused TTK: time from the first damage event to death. Spawn-to-kill queue delay is tracked separately by the simulator.

| Profile | Hero | Ordinary mean / p95 (s) | Elite mean / p95 (s) | Deaths / 5 | Mean min HP | Mean incoming damage | Conservative single-hit bound |
|---|---|---:|---:|---:|---:|---:|---|
| fresh | hero_lin_yue | 1.15 / 2.85 | 24.5 / 38.05 | 0 | 39.38 | 50.62 | PASS (0.1) |
| fresh | hero_seoyeon_han | 0.75 / 2.4 | 18 / 33.3 | 0 | 63.04 | 46.96 | PASS (0.124) |
| max_m1 | hero_lin_yue | 0.75 / 1.75 | 17.65 / 23.85 | 0 | 84.474 | 23.526 | PASS (0.112) |
| max_m1 | hero_seoyeon_han | 0.5 / 1.25 | 12.35 / 18 | 0 | 115.116 | 16.884 | PASS (0.112) |
| moderate | hero_lin_yue | 1.25 / 2.6 | 22.3 / 39.1 | 0 | 61.159 | 34.241 | PASS (0.122) |
| moderate | hero_seoyeon_han | 0.75 / 1.75 | 15.1 / 27 | 0 | 83.868 | 32.732 | PASS (0.122) |

The conservative bound treats the largest model hit as if it were untelegraphed. It passes the B1 15% bound in all 30 runs. This does not prove spatial telegraph behavior or collision ordering.

## Active-cap occupancy

| Profile / hero | Max occupancy mean | p95 occupancy mean | Seconds at cap mean | Suppressed spawn attempts mean |
|---|---:|---:|---:|---:|
| fresh/hero_lin_yue | 280 | 280 | 1123.75 | 20134 |
| fresh/hero_seoyeon_han | 280 | 280 | 1150.1 | 20470.4 |
| max_m1/hero_lin_yue | 280 | 280 | 1117.5 | 19622.6 |
| max_m1/hero_seoyeon_han | 280 | 280 | 1128.3 | 19804.6 |
| moderate/hero_lin_yue | 280 | 280 | 1122.2 | 20039.4 |
| moderate/hero_seoyeon_han | 280 | 280 | 1139.9 | 20278.2 |

Every slice reaches the 280 cap in the final band. This is a model risk, not a runtime acceptance pass: the proposed spawn/damage combination keeps the arena saturated for most of the run.

## Boss results

Target pass count is out of five seeds.

| Profile / hero | Boss | Mean TTK (s) | TTK range | Target passes | Status |
|---|---|---:|---:|---:|---|
| fresh/hero_lin_yue | boss_01_05 | 65.5 | 65.5–65.5 | 5/5 | DEFEATED |
| fresh/hero_lin_yue | boss_02_10 | 70.25 | 70.25–70.25 | 5/5 | DEFEATED |
| fresh/hero_lin_yue | boss_03_15 | 77 | 77–77 | 5/5 | DEFEATED |
| fresh/hero_lin_yue | boss_final_20 | 119.928 | 119.928–119.928 | 5/5 | PROJECTED_POST_RUN_DEFEAT |
| fresh/hero_seoyeon_han | boss_01_05 | 70.5 | 70.5–70.5 | 5/5 | DEFEATED |
| fresh/hero_seoyeon_han | boss_02_10 | 78.75 | 78.75–78.75 | 5/5 | DEFEATED |
| fresh/hero_seoyeon_han | boss_03_15 | 87 | 87–87 | 0/5 | DEFEATED |
| fresh/hero_seoyeon_han | boss_final_20 | 133.749 | 133.749–133.749 | 0/5 | POST_RUN_WINDOW_EXCEEDED |
| max_m1/hero_lin_yue | boss_01_05 | 45.5 | 45.5–45.5 | 5/5 | DEFEATED |
| max_m1/hero_lin_yue | boss_02_10 | 48.75 | 48.75–48.75 | 5/5 | DEFEATED |
| max_m1/hero_lin_yue | boss_03_15 | 47.75 | 47.75–47.75 | 5/5 | DEFEATED |
| max_m1/hero_lin_yue | boss_final_20 | 85.409 | 85.409–85.409 | 0/5 | PROJECTED_POST_RUN_DEFEAT |
| max_m1/hero_seoyeon_han | boss_01_05 | 49.5 | 49.5–49.5 | 5/5 | DEFEATED |
| max_m1/hero_seoyeon_han | boss_02_10 | 54.75 | 54.75–54.75 | 5/5 | DEFEATED |
| max_m1/hero_seoyeon_han | boss_03_15 | 53.25 | 53.25–53.25 | 5/5 | DEFEATED |
| max_m1/hero_seoyeon_han | boss_final_20 | 94.633 | 94.633–94.633 | 5/5 | PROJECTED_POST_RUN_DEFEAT |
| moderate/hero_lin_yue | boss_01_05 | 59.5 | 59.5–59.5 | 5/5 | DEFEATED |
| moderate/hero_lin_yue | boss_02_10 | 64.75 | 64.75–64.75 | 5/5 | DEFEATED |
| moderate/hero_lin_yue | boss_03_15 | 70.5 | 70.5–70.5 | 5/5 | DEFEATED |
| moderate/hero_lin_yue | boss_final_20 | 109.71 | 109.71–109.71 | 5/5 | PROJECTED_POST_RUN_DEFEAT |
| moderate/hero_seoyeon_han | boss_01_05 | 64.5 | 64.5–64.5 | 5/5 | DEFEATED |
| moderate/hero_seoyeon_han | boss_02_10 | 72.25 | 72.25–72.25 | 5/5 | DEFEATED |
| moderate/hero_seoyeon_han | boss_03_15 | 68.5 | 68.5–68.5 | 5/5 | DEFEATED |
| moderate/hero_seoyeon_han | boss_final_20 | 123.079 | 123.079–123.079 | 0/5 | POST_RUN_WINDOW_EXCEEDED |

Interpretation:

- fresh Lin Yue passes all four model target windows and resolves the first-clear ledger;
- fresh Soyeon passes bosses 1–2 but misses boss 3 and final target windows;
- moderate Lin Yue passes all four;
- moderate Soyeon passes bosses 1–3 but misses the final upper bound by a small margin;
- max M1 Lin Yue defeats the final boss faster than the 90-second lower target;
- max M1 Soyeon passes all four target windows.

These are explicit model findings. They are not hidden by profile-specific scaling.

## Rewards, synergy, fallback, and idempotency

| Profile / hero | Ledger balance | Idempotency | Final chest_offer | Synergy | Fallback damage bonus |
|---|---|---|---|---|---|
| fresh/hero_lin_yue | {"boss_essence": 6, "gold": 725, "moon_seals": 300} | PASS | false | synergy_heavenly_seals | 0.06 |
| fresh/hero_seoyeon_han | {"boss_essence": 3, "gold": 225, "moon_seals": 60} | PASS | false | synergy_moon_dance | 0.06 |
| max_m1/hero_lin_yue | {"boss_essence": 6, "gold": 725, "moon_seals": 300} | PASS | false | synergy_heavenly_seals | 0.06 |
| max_m1/hero_seoyeon_han | {"boss_essence": 6, "gold": 725, "moon_seals": 300} | PASS | false | synergy_moon_dance | 0.06 |
| moderate/hero_lin_yue | {"boss_essence": 6, "gold": 725, "moon_seals": 300} | PASS | false | synergy_heavenly_seals | 0.06 |
| moderate/hero_seoyeon_han | {"boss_essence": 3, "gold": 225, "moon_seals": 60} | PASS | false | synergy_moon_dance | 0.06 |

The canonical arithmetic remains:

- full first clear: 725 gold / 300 Moon Seals / 6 boss essence;
- repeat clear: 425 gold / 120 Moon Seals / 5 boss essence;
- duplicate reward attempts: rejected in all 30 model runs;
- final boss chest_offer: false in all model runs;
- artifact delivery: proposed run-result artifact grant, because the architecture contract currently says final boss NO_CHEST while B1 specifies first-clear artifact value.

## Remaining blockers

1. The Godot runtime does not consume BALANCE_MODEL.json.
2. Absolute combat values and profile definitions are PROPOSED, not approved CANON.
3. Active-cap saturation needs a product decision and runtime performance test.
4. Fresh/moderate Soyeon and max Lin Yue do not share the final-boss target window.
5. Spatial movement, telegraphs, same-frame ordering, XP presentation, and Android 30 FPS are not executed.
6. The result-artifact settlement needs Product/Architecture confirmation.

## Exact next implementation slice

Runtime/Architecture must load this model through the versioned Content Registry, create the RunSession wave/XP/combat/reward fields, implement the event pipeline and final NO_CHEST settlement, then emit the same five-seed traces. Balance can only promote PROPOSED inputs or tune against those traces after that evidence exists.

