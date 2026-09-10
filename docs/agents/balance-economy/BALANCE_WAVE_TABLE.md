# Balance Wave Table — 30-minute MAC model

Status: \`PARTIAL / SIMULATED_MODEL_ONLY\`

This table is the agreed 30-minute balance shape, not a runtime claim. The numeric source of truth remains \`docs/BALANCE_ECONOMY_SPEC.md\` (B1 revision \`6aa4ec96afc8a8c9e6a35c164c99e7d62910a687\`). The 20:00–30:00 anchors, five-mini schedule and elite overlay remain explicitly proposed/pending where the JSON says so.

Parent HEAD for REF-BALANCE-REF-01: \`488c5bbd6b0ad412f0c1647eb99e17d31a6953a0\`.
Model consumer: \`docs/agents/balance-economy/BALANCE_MODEL.json\`.

## Shared reference pattern

The three requested repositories show the same useful shape: time/level keyed spawn data, progression separated from spawn control, special encounters as explicit events, and rewards resolved through a distinct loot/offer path. They are reference-only; no foreign number or content ID is imported.

- [VampireSurvivorsClone spawn table](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Scripts/Monsters/MonsterSpawnTable.cs): time-keyed rate/composition/HP selection.
- [20-Minutes-till-dawn monster controller](https://github.com/ParsaSabzei/20-Minutes-till-dawn/blob/main/core/src/main/java/ap/project/controller/MonsterController.java): elapsed-progress gates for pressure and special encounters.
- [Sentaur difficulty curve and spawn director](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/SceneManagers/DifficultyCurve.cs): separate unlock, wave-size, HP and spawn-rate concerns.

## Wave bands

| Run clock | Model band | Spawn budget/s | Active cap | HP mult | ATK mult | Speed mult | Level target | Status |
|---:|---|---:|---:|---:|---:|---:|---|---|
| 00:00–02:00 | warmup | 6 | 40 | 1.00 | 0.70 | 0.90 | 2 | CANON B1 |
| 02:00–05:00 | first pressure | 10 | 80 | 1.10 | 0.85 | 1.00 | 5 | CANON B1 |
| 05:00–10:00 | threat expansion | 15 | 130 | 1.35 | 1.00 | 1.02 | 9 | CANON B1 |
| 10:00–15:00 | elite band | 22 | 200 | 1.70 | 1.25 | 1.05 | 13 | CANON B1 |
| 15:00–20:00 | eclipse | 30 | 280 | 2.20 | 1.55 | 1.08 | 17–18 | CANON B1 |
| 20:00–25:00 | cataclysm extension | 38 | 340 | 2.70 | 1.75 | 1.10 | 21–22 | PROPOSED |
| 25:00–30:00 | apocalypse extension | 48 | 400 | 3.30 | 2.00 | 1.12 | 25–26 | PROPOSED |

Composition follows the B1 roster order through 20:00. The two extension bands reuse the roster and add only finite elite events; no new enemy ID is invented. Spawn overflow is discarded at the active cap with no spawn debt. A runtime safe-mode fallback is required if device occupancy/FPS exceeds the target, but the fallback value is not yet canonical.

## Main-boss shape: low → peak → siege

At each main checkpoint, the visible run/wave/XP/ordinary-spawn clocks freeze and a separate encounter clock resolves the boss. After settlement, the next interval is deliberately not a hard jump:

1. 8 seconds of ordinary-spawn suppression;
2. recovery from 70% to 100% of the current budget over 20 seconds;
3. enter at 80% of the preceding peak budget/cap;
4. linearly ramp to the next band peak;
5. hold the peak for the final 60-second siege before the next main checkpoint.

The 0.80 reset, 8-second suppression, 20-second recovery, linear curve and 60-second siege are DERIVED/PROPOSED model inputs, not external-game numbers. The formula is stored in \`simulation_model.boss_wave_ramp\`.

| Cycle | From → to | Entry band → peak band | Density behavior | Status |
|---|---|---|---|---|
| 1 | 05:00 → 10:00 | first pressure → threat | recovery, linear ramp, siege | DERIVED |
| 2 | 10:00 → 15:00 | threat → elite | recovery, linear ramp, siege | DERIVED |
| 3 | 15:00 → 20:00 | elite → eclipse | recovery, linear ramp, siege | DERIVED |
| 4 | 20:00 → 25:00 | eclipse → cataclysm | recovery, linear ramp, siege | PROPOSED |
| 5 | 25:00 → 30:00 | cataclysm → apocalypse | recovery, linear ramp, siege | PROPOSED |

## Mini-boss and elite windows

Mini-bosses are pressure beats inside the wave cadence, not additional main checkpoints:

| Time | Event | Clock | Ordinary wave | Post-event elite window | Status |
|---:|---|---|---|---|---|
| 07:30 | \`miniboss_ink_jade_warden\` | continues | continues | finite pack after defeat | PENDING_CONTENT_REGISTRY |
| 12:30 | \`miniboss_veil_harvester\` | continues | continues | finite pack after defeat | PENDING_CONTENT_REGISTRY |
| 17:30 | \`miniboss_pending_03\` | continues | continues | finite pack after defeat | PENDING_CONTENT_REGISTRY |
| 22:30 | \`miniboss_extension_slot_03\` | continues | continues | finite pack after defeat | PENDING_CONTENT_REGISTRY |
| 27:30 | \`miniboss_pending_05\` | continues | continues | finite pack after defeat | PENDING_CONTENT_REGISTRY |

The mini-boss does not reset the main ramp or create an immediate density spike. One finite pack may follow each mini defeat: one seeded variant anchor plus two current-wave escorts. The pack counts against active cap, selection is seeded, and the roster returns to ordinary composition afterward. The model allows at most five events/run; numeric overlays and the two missing mini records remain PROPOSED/PENDING.

## Provenance and non-import rule

- B1 bands, XP vocabulary, checkpoint/reward rules and acceptance bounds: CANON.
- 20:00–30:00 bands, reset/ramp values, mini kits, elite overlay and extension rewards: PROPOSED or DERIVED as recorded in JSON.
- External repositories: REFERENCE_ONLY structural evidence; no numbers, IDs, assets or loot odds copied.
- Runtime Godot/Android proof: NOT_IMPLEMENTED.
