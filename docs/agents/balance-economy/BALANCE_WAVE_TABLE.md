# Balance Wave Table — 30-minute extension

Status: `PARTIAL / SIMULATED_MODEL_ONLY`

The live architecture contract is revision `bd1d4d44f9c0a525b26ac136d98ace3cf76a3d00`: it now declares a 1800-second run, six main checkpoint records and six stable wave-cycle IDs. Numeric extension profiles remain Balance-owned proposed values; runtime is not implemented.

Sources: user decision (30-minute run, two additional main bosses, five mini-bosses, finite elite variations); B1 revision `6aa4ec96afc8a8c9e6a35c164c99e7d62910a687`; live architecture revision above.

## Wave bands

| Run clock | Model band | Spawn/s | Active cap | HP mult | Damage mult | Status |
|---:|---|---:|---:|---:|---:|---|
| 00:00–02:00 | warmup | 6 | 40 | 1.00 | 0.70 | CANON B1 |
| 02:00–05:00 | first pressure | 10 | 80 | 1.10 | 0.85 | CANON B1 |
| 05:00–10:00 | threat expansion | 15 | 130 | 1.35 | 1.00 | CANON B1 |
| 10:00–15:00 | elite band | 22 | 200 | 1.70 | 1.25 | CANON B1 |
| 15:00–20:00 | eclipse | 30 | 280 | 2.20 | 1.55 | CANON B1 |
| 20:00–25:00 | cataclysm extension | 38 | 340 | 2.70 | 1.75 | PROPOSED |
| 25:00–30:00 | apocalypse extension | 48 | 400 | 3.30 | 2.00 | PROPOSED |

Model bands alias to architecture cycles: warmup+first pressure→cycle 01, threat→02, elite→03, eclipse→04, cataclysm→05, apocalypse→06. The 20:00–30:00 composition reuses the canonical roster; elite variants are event-triggered, never permanent wave members.

## Encounter schedule

| Time | Encounter | Clock rule in balance model | Stable-ID/registry status |
|---:|---|---|---|
| 05:00 | Main boss 1 `boss_hua_lin` | freezes | existing architecture record |
| 07:30 | Mini 1 `miniboss_ink_jade_warden` | continues | architecture C3 target |
| 10:00 | Main boss 2 `boss_miyeon` | freezes | existing architecture record |
| 12:30 | Mini 2 `miniboss_veil_harvester` | continues | architecture C3 target |
| 15:00 | Main boss 3 `boss_seika` | freezes | existing architecture record |
| 17:30 | Mini 3 `miniboss_pending_03` | continues | model proposal; registry pending |
| 20:00 | Main boss 4 `boss_extension_slot_04` | freezes | architecture slot ID pending content |
| 22:30 | Mini 4 `miniboss_extension_slot_03` | continues | architecture intermediate ID pending content |
| 25:00 | Main boss 5 `boss_extension_slot_05` | freezes | architecture slot ID pending content |
| 27:30 | Mini 5 `miniboss_pending_05` | continues | model proposal; registry pending |
| 30:00 | Final `boss_black_moon_empress` | freezes; no boss chest | architecture final ID retimed to 1800 |

Architecture currently has only three intermediate slots (450/750/1350); the 1050 and 1650 model slots are explicitly proposed. The live architecture clock policy currently says boss time advances, which conflicts with the balance rule above.

## Post-main-boss ramp

Each main-boss interval is: 8s suppression → 20s recovery factor 0.70→1.00 → linear low-to-peak ramp → 60s peak siege. Proposed reset factor: 0.80.

| From | To | Entry band | Peak band | Status |
|---|---|---|---|---|
| 05:00 | 10:00 | first pressure | threat expansion | DERIVED |
| 10:00 | 15:00 | threat expansion | elite band | DERIVED |
| 15:00 | 20:00 | elite band | eclipse | DERIVED |
| 20:00 | 25:00 | eclipse | cataclysm | PROPOSED |
| 25:00 | 30:00 | cataclysm | apocalypse | PROPOSED |

The architecture wave rule says every non-final main/intermediate encounter enters relief. The current model verifies the five main cycles; mini-boss relief/ramp still needs an explicit decision and runtime implementation.

## Elite variations

Elite variations are finite post-mini pressure/reward events:

- maximum five events per run, one after each model mini-boss;
- three members: one seeded elite overlay and two current-wave escorts;
- stable IDs are `enemy_ink_beetle_variant_01`, `_02`, `_03`, read from the model's registry handoff;
- overlay: HP ×8, damage ×1.25, speed ×1.05, XP ×2;
- reward: one three-card `ARTIFACT_OFFER`, no wallet mutation;
- duplicate resolution returns the stored offer by idempotency key.

Overlay/cadence values are `PROPOSED`; architecture numeric overrides and visual records are pending B1/content work. The active cap counts ordinary and elite entities, discards overflow attempts and accumulates no spawn debt. Maximum proposed cap is 400; Android FPS and runtime readability remain unverified.