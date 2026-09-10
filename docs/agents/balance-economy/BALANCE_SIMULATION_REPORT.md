# Balance Simulation Report

Status: SIMULATED_MODEL_ONLY / PARTIAL

## Run snapshot

- Live main HEAD immediately before this report refresh: a55c50c2f12a77141dff958b9e22ed732d0ed06b.
- B1 source revision: 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687.
- Architecture contract revision: 2f889f876f2b8aa286523d234786addf0b9b245e.
- Balance model commit: 3a40341a71b910f12bea1834c0758a74b6059bdc.
- Simulator commit: 34d62768787b39191151d6e9f62b957db0e9c1e8.
- Contract validator commit: 83df99e44c40839724b57563fee90b3032eed87f.
- Seeds: 101, 202, 303, 404, 505.
- Runs: 30 (fresh/moderate/max_m1 × Lin Yue/Soyeon Han × 5 seeds).
- Runtime executed: false. No Godot runtime claim is made.
- Contract validator: PASS.
- Two full current-model outputs: equal SHA-256 52b32ebff019e312a23d2153439ec0ebbfb7fdf3b48acb568efb16e922a78242.
- Clock policy: at 300/600/900/1200 seconds the visible run clock stops; wave selection, ordinary spawn, XP pickup and level progression remain frozen; each boss resolves on a separate encounter clock.

The simulator reads one BALANCE_MODEL.json. It does not duplicate tuning values in Python. The result is evidence for the proposed deterministic model only, not proof that the Godot game applies those values.

## Provenance of values that B1 does not define

No missing input was silently promoted to CANON. The full field-level source, derived formula, proposed value and status remain in BALANCE_MODEL.json. The important decision surface is:

| Input | Source | Derived formula | Proposed value used | Why this supports a B1 check | Status |
|---|---|---|---|---|---|
| Visible boss-clock rule | User product decision captured 2026-09-10 | run clock is constant during each boss encounter; separate encounter clock resolves TTK | checkpoints 300/600/900/1200; no wave/XP/spawn advancement | makes the 20-minute pacing and every boss interruption observable without lengthening the wave clock | CANON |
| Simulation step | Simulation method; absent from B1 | fixed step below the 0.8 s contact gate and shortest proposed attack interval | 0.25 s | deterministic spawn, attack, pickup and checkpoint boundaries | PROPOSED |
| Enemy base HP/damage/speed | PENDING_B1 / GAME_MANIFEST | HP = proposed base HP × durability × wave HP multiplier; damage = base damage × wave damage multiplier | per-enemy rows in simulation_model.enemy_stats | makes ordinary/elite TTK and incoming risk calculable while awaiting absolute combat values | PROPOSED |
| Boss base HP/damage/speed | PENDING_B1; B1 gives TTK windows | target midpoint × reference DPS for HP; telegraphed cadence and damage budget for pressure | boss HP 3600/4500/5200/9600; damage 12/15/18/22; speed 24/28/30/34 | produces measurable first-slice and final TTK windows without hiding the assumptions | PROPOSED |
| Profile hit probability | PENDING_PRODUCT_DECISION | landed-hit probability under movement and telegraphing | fresh 0.002; moderate 0.0015; max_m1 0.001 | exposes incoming-risk sensitivity for the three requested account states | PROPOSED |
| Pickup capacity and delay | PENDING_B1; B1 gives level targets but not cadence | collected XP budget = capacity × dt × magnet multiplier; drops unlock after delay | explicit per-wave capacities, first-level window, 1 s drop delay in model | makes first-level and 2/5/10/15/20-minute XP checkpoints testable | PROPOSED / CANON_TARGET_BOUND |
| Weapon/passive/synergy effects | B1 and architecture provide IDs/requirements, not numeric effects | weapon cadence × level bonus × passive × profile × expected crit, with synergy share clamp | explicit build_catalog values and 40% attribution cap in model | lets the model compare Lin Yue and Soyeon routes while keeping tuning approval visible | PROPOSED |
| Artifact effects and refresh | Product/architecture boundary, exact catalog absent | typed offer lifecycle; effect exists only after one-of-three selection | three-card first-clear offer; effect values/refresh/stacking remain null | prevents an artifact from being granted silently as a boss chest | PENDING_PRODUCT_DECISION |

These proposed values are model inputs, not canonical game data. Product/B1 owners must approve or replace them before a runtime balance claim.

## Concrete profile inputs and progression

| Profile / hero | Meta ranks | Damage | Cooldown | Hit probability | First level (s) | Level at 2/5/10/15/20 min | Final |
|---|---|---:|---:|---:|---:|---|---:|
| fresh / Lin Yue | all 0 | 1.00 | 1.00 | 0.002 | 39.75 | 2 / 5 / 9 / 13 / 17 | 17 |
| fresh / Soyeon Han | all 0 | 1.00 | 1.00 | 0.002 | 39.75 | 2 / 5 / 9 / 13 / 17 | 17 |
| moderate / Lin Yue | V3/P3/A2/F2/M2/D2 | 1.06 | 0.97 | 0.0015 | 38.25 | 2 / 6 / 10 / 13 / 17 | 17 |
| moderate / Soyeon Han | V3/P3/A2/F2/M2/D2 | 1.06 | 0.97 | 0.0015 | 38.25 | 2 / 6 / 10 / 13 / 17 | 17 |
| max_m1 / Lin Yue | all 10 | 1.20 | 0.85 | 0.001 | 33.25 | 2 / 6 / 10 / 14 / 18 | 18 |
| max_m1 / Soyeon Han | all 10 | 1.20 | 0.85 | 0.001 | 33.25 | 2 / 6 / 10 / 14 / 18 | 18 |

The level values are run-clock checkpoints. They do not advance while a boss encounter is resolving.

## TTK and incoming risk

Means and p95 values are across the five fixed seeds for the profile/hero row. Focused TTK begins at the first damage event; spawn-to-kill queue delay is reported separately by the simulator.

| Profile / hero | Ordinary mean / p95 (s) | Elite mean / p95 (s) | Mean incoming damage | Mean minimum HP | Deaths / 5 |
|---|---:|---:|---:|---:|---:|
| fresh / Lin Yue | 1.25 / 3.45 | 25.25 / 59.65 | 66.220 | 23.780 | 0 |
| fresh / Soyeon Han | 0.75 / 2.85 | 18.00 / 51.00 | 72.320 | 37.680 | 0 |
| moderate / Lin Yue | 1.25 / 2.90 | 22.95 / 53.75 | 49.451 | 45.949 | 0 |
| moderate / Soyeon Han | 0.75 / 2.15 | 16.95 / 46.40 | 41.121 | 75.479 | 0 |
| max_m1 / Lin Yue | 0.75 / 1.80 | 18.15 / 34.65 | 29.430 | 78.570 | 0 |
| max_m1 / Soyeon Han | 0.50 / 1.50 | 13.90 / 27.50 | 25.092 | 106.908 | 0 |

The conservative single-hit bound passed in all 30 runs. Spatial collision, telegraph timing and same-frame ordering were not executed.

## Active-cap occupancy

Occupancy is sampled on the visible run clock and excludes the time spent inside boss encounters. This prevents a paused boss from inflating 20-minute cap occupancy.

| Profile / hero | Max cap | Mean cap seconds | Suppressed spawn attempts | Sample clock |
|---|---:|---:|---:|---|
| fresh / Lin Yue | 280 | 1112.25 | 19928.0 | 1199.25 s run clock |
| fresh / Soyeon Han | 280 | 1140.00 | 20276.4 | 1199.25 s run clock |
| moderate / Lin Yue | 280 | 1111.20 | 19847.2 | 1199.25 s run clock |
| moderate / Soyeon Han | 280 | 1129.40 | 20118.2 | 1199.25 s run clock |
| max_m1 / Lin Yue | 280 | 1105.70 | 19468.4 | 1199.25 s run clock |
| max_m1 / Soyeon Han | 280 | 1117.00 | 19656.8 | 1199.25 s run clock |

Every slice reaches cap 280. This remains a balance/performance watch item, not a runtime acceptance pass.

## Boss results

Each cell is mean TTK in seconds with target-window passes out of five seeds. First-slice target is 45–80 seconds; final target is 90–120 seconds.

| Profile / hero | 5:00 boss | 10:00 boss | 15:00 boss | 20:00 final boss |
|---|---|---|---|---|
| fresh / Lin Yue | 70.00; 5/5 | 72.50; 5/5 | 77.00; 5/5 | 120.50; 0/5, POST_RUN_WINDOW_EXCEEDED |
| fresh / Soyeon Han | 75.00; 5/5 | 80.25; 0/5 | 87.00; 0/5 | 134.25; 0/5, POST_RUN_WINDOW_EXCEEDED |
| moderate / Lin Yue | 59.50; 5/5 | 64.50; 5/5 | 70.00; 5/5 | 110.50; 5/5 |
| moderate / Soyeon Han | 64.50; 5/5 | 72.50; 5/5 | 79.75; 5/5 | 123.50; 0/5, POST_RUN_WINDOW_EXCEEDED |
| max_m1 / Lin Yue | 46.00; 5/5 | 49.75; 5/5 | 54.00; 5/5 | 85.25; 0/5, below lower target |
| max_m1 / Soyeon Han | 50.00; 5/5 | 56.50; 5/5 | 62.00; 5/5 | 95.25; 5/5 |

Boss encounter pause duration, summed over all four bosses, was 340.00 s, 376.50 s, 304.50 s, 340.25 s, 235.00 s and 263.75 s for the rows above respectively. In every run each boss result has the same run-clock spawn and defeat checkpoint (300, 600, 900 or 1200); only wall/encounter time advances between them.

## Rewards, builds, fallback and idempotency

| Profile / hero | Ledger balance | Synergy | Fallback bonus | First-clear offers |
|---|---|---|---:|---:|
| fresh / Lin Yue | 225 gold / 60 Moon Seals / 3 Boss Essence | synergy_heavenly_seals | 0.06 | 0/5 |
| fresh / Soyeon Han | 225 / 60 / 3 | synergy_moon_dance | 0.06 | 0/5 |
| moderate / Lin Yue | 725 / 300 / 6 | synergy_heavenly_seals | 0.06 | 5/5 |
| moderate / Soyeon Han | 225 / 60 / 3 | synergy_moon_dance | 0.06 | 0/5 |
| max_m1 / Lin Yue | 725 / 300 / 6 | synergy_heavenly_seals | 0.06 | 5/5 |
| max_m1 / Soyeon Han | 725 / 300 / 6 | synergy_moon_dance | 0.06 | 5/5 |

- Duplicate reward attempts were rejected in 30/30 runs; idempotency PASS.
- Final boss chest offer was created in 0/30 runs.
- First-clear artifact offers were created in 15/30 runs, each with exactly 3 choices and status OFFER_CREATED_PENDING_SELECTION. The 15/30 count follows the proposed 120-second final encounter window; effect values, refresh, duplicate and persistence rules remain pending.
- Non-final build resolution is deterministic: two fallback upgrades followed by the eligible synergy for both architecture-compatible routes.

## Changed files in this slice

- docs/agents/balance-economy/BALANCE_MODEL.json — renamed the clock rule to boss_clock_policy, applied it to all four checkpoints, and refreshed repository evidence.
- docs/agents/balance-economy/balance_simulator.py — replaced the final-only post-run special case with a two-clock loop for every boss; added pause traces, encounter wall time, and model-only outcome fields.
- docs/agents/balance-economy/balance_contract_validator.py — validates all four boss checkpoints and the all-boss clock policy.
- docs/agents/balance-economy/BALANCE_COMBAT_MODEL.md — documented all-boss pause semantics.
- docs/agents/balance-economy/BALANCE_ACCEPTANCE_MATRIX.md — synchronized checks, results and deterministic hash.
- docs/agents/balance-economy/DECISIONS_AND_UNKNOWNS.md — recorded C-11 for every boss.
- docs/agents/balance-economy/BALANCE_SIMULATION_REPORT.md — this report refresh.
- docs/agents/balance-economy/BALANCE_AUDIT.md — must be refreshed after this commit with the final live HEAD.

## Remaining blockers

1. Godot runtime still does not consume BALANCE_MODEL.json; no RunSession/WaveDirector/BossDirector/RewardLedger trace exists.
2. Absolute enemy, boss, weapon, passive, synergy, profile and pickup numbers are PROPOSED/DERIVED, not approved CANON.
3. Active-cap saturation is severe in the model and requires a product decision plus runtime performance test.
4. Fresh/moderate Soyeon miss the proposed final-boss window; max_m1 Lin Yue is below the proposed final-boss lower bound.
5. Spatial movement, safe boss spawn, telegraphs, same-frame ordering, XP presentation and Android 30 FPS are unverified.
6. First-clear artifact selection, refresh, duplicate/stacking and persistence are still pending product/architecture decisions.

## Exact next implementation slice

Runtime/Architecture must load the single balance model through the versioned Content Registry and implement a RunSession with:

1. visible run clock and a separate encounter clock that pauses at 300/600/900/1200 for every boss;
2. wave selection, active cap and XP pickup gates keyed only to visible run time while a boss is active;
3. boss interruption/recovery state, combat event ordering, contact cooldown, telegraph metadata, safe spawn and deterministic five-seed traces;
4. the canonical weapon/passive/synergy IDs, fallback resolver and three-card first-clear artifact-offer boundary;
5. reward ledger keys, final NO_CHEST settlement, offer selection persistence and replay-safe commands.

Then rerun the same 30 traces against Godot. Until that runtime slice exists, the balance is verified only as a model and the repository status remains PARTIAL, not VERIFIED.
