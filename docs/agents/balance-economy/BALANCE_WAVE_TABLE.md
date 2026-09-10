# Balance Wave Table — 30-minute extension

Status: `PARTIAL / SIMULATED_MODEL_ONLY`

The requested 30-minute run is represented in `BALANCE_MODEL.json`. The legacy B1/architecture inputs still declare 1200 seconds, so extension values are explicitly `PROPOSED/PENDING`, not runtime canon.

Sources: user decision (30-minute run, two additional main bosses, five mini-bosses, finite elite variations); B1 revision `6aa4ec96afc8a8c9e6a35c164c99e7d62910a687`; architecture revision `2f889f876f2b8aa286523d234786addf0b9b245e`.

## Wave bands

| Run clock | Band | Spawn/s | Active cap | HP mult | Damage mult | Status |
|---:|---|---:|---:|---:|---:|---|
| 00:00–02:00 | warmup | 6 | 40 | 1.00 | 0.70 | CANON B1 |
| 02:00–05:00 | first pressure | 10 | 80 | 1.10 | 0.85 | CANON B1 |
| 05:00–10:00 | threat expansion | 15 | 130 | 1.35 | 1.00 | CANON B1 |
| 10:00–15:00 | elite band | 22 | 200 | 1.70 | 1.25 | CANON B1 |
| 15:00–20:00 | eclipse | 30 | 280 | 2.20 | 1.55 | CANON B1 |
| 20:00–25:00 | cataclysm extension | 38 | 340 | 2.70 | 1.75 | PROPOSED |
| 25:00–30:00 | apocalypse extension | 48 | 400 | 3.30 | 2.00 | PROPOSED |

Every extension value has `source`, `derived_formula`, `rationale` and `status` in the JSON. The 20:00–30:00 composition reuses the canonical roster; elite variants are not permanent wave members.

## Encounter schedule

| Time | Encounter | Clock rule | ID status |
|---:|---|---|---|
| 05:00 | Main boss 1 | visible run/wave/XP/spawn clock freezes | existing canonical |
| 07:30 | Mini-boss 1 | timer, waves and XP continue | C3 proposal: `miniboss_ink_jade_warden` |
| 10:00 | Main boss 2 | freezes | existing canonical |
| 12:30 | Mini-boss 2 | continues | C3 proposal: `miniboss_veil_harvester` |
| 15:00 | Main boss 3 | freezes | existing canonical |
| 17:30 | Mini-boss 3 | continues | content ID pending |
| 20:00 | Main boss 4 | freezes; old final role needs reclassification | existing ID, architecture sync pending |
| 22:30 | Mini-boss 4 | continues | content ID pending |
| 25:00 | Main boss 5 | freezes | new ID pending |
| 27:30 | Mini-boss 5 | continues | content ID pending |
| 30:00 | Main final boss | freezes; no final boss chest | new ID pending |

Mini-boss times are a proposed midpoint cadence; the runtime contract must add `MINI_BOSS` encounter semantics.

## Post-main-boss ramp

Each interval is: 8s zero-spawn suppression → 20s recovery factor 0.70→1.00 → linear low-to-peak ramp → 60s peak siege. Proposed reset factor: 0.80.

| From | To | Entry band | Peak band | Status |
|---|---|---|---|---|
| 05:00 | 10:00 | first pressure | threat expansion | DERIVED |
| 10:00 | 15:00 | threat expansion | elite band | DERIVED |
| 15:00 | 20:00 | elite band | eclipse | DERIVED |
| 20:00 | 25:00 | eclipse | cataclysm | PROPOSED |
| 25:00 | 30:00 | cataclysm | apocalypse | PROPOSED |

## Elite variations

Elite variations are finite post-mini pressure/reward events:

- maximum five events per run, one after each mini-boss;
- three members: one seeded elite overlay and two current-wave escorts;
- overlay: HP ×8, damage ×1.25, speed ×1.05, XP ×2;
- reward: one three-card `ARTIFACT_OFFER`, no wallet mutation;
- duplicate resolution returns the stored offer by idempotency key.

All overlay/cadence values are `PROPOSED`; B1 and the content registry do not yet provide variant stats.

The active cap counts ordinary and elite entities, discards overflow spawn attempts and accumulates no spawn debt. The maximum proposed cap is 400; Android FPS and runtime readability remain unverified.
