# Balance Wave Table

Status: SPECIFIED / PARTIAL

This document is the wave-schedule contract derived from B1. It is not runtime data. The source baseline is docs/BALANCE_ECONOMY_SPEC.md at revision 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687. The materialized machine-readable contract is BALANCE_MODEL.json.

## Provenance rules

- CANON: copied from B1 without changing the number.
- DERIVED: arithmetic from CANON values; it is not an additional tuning decision.
- PENDING_B1: a number or rule is required by the balance contract but is absent from B1/GAME_MANIFEST.
- PENDING_PRODUCT_DECISION: behavior must be selected before production implementation.
- NOT_IMPLEMENTED: no runtime consumer was found in the audited repository.
- TEST_PLACEHOLDER: allowed only in the simulator, never in this table as production tuning.

## Wave bands

| Band | Time window | Spawn budget | Active cap | HP multiplier | Damage multiplier | Speed multiplier | Composition | Level target | Theoretical spawn opportunity |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
| wave_00_02 | 0:00–2:00 | 6/s | 40 | 1.00 | 0.70 | 0.90 | Ink beetle | 2 | 720 units |
| wave_02_05 | 2:00–5:00 | 10/s | 80 | 1.10 | 0.85 | 1.00 | Ink beetle, lantern moth, bone carp | 5 | 1,800 units |
| wave_05_10 | 5:00–10:00 | 15/s | 130 | 1.35 | 1.00 | 1.02 | Ink beetle, lantern moth, bone carp, paper ghost, jade toad, mirror fox | 9 | 4,500 units |
| wave_10_15 | 10:00–15:00 | 22/s | 200 | 1.70 | 1.25 | 1.05 | Early roster plus bell crab, thread doll, stone oni, eclipse serpent | 13 | 6,600 units |
| wave_15_20 | 15:00–20:00 | 30/s | 280 | 2.20 | 1.55 | 1.08 | Full roster plus empowered elites | 17–18 | 9,000 units |

All values in the first five columns of the table are CANON, source B1 section 4. The final column is DERIVED as spawn budget per second multiplied by the band duration. It represents nominal spawn opportunity before active-cap limits, boss interruption, death/despawn rules, and any safe-mode policy. It is not an expected enemy-kill count.

The nominal opportunity across all five bands is 22,620 spawn units. This is a DERIVED planning number only.

## Boss interruption

At each boss event:

1. Ordinary spawn is reduced for 8 seconds. The 8-second duration is CANON.
2. A recovery factor starts at 0.70 and returns to 1.00 over 20 seconds. The endpoints and duration are CANON.
3. The interpolation shape, overlap with a subsequent boss, and whether the 8-second reduction is additive or replaces the recovery curve are PENDING_B1 / PENDING_PRODUCT_DECISION.
4. If a single uninterrupted 20-second recovery uses linear interpolation, its average factor is DERIVED as 0.85 and its nominal equivalent is 17 spawn-seconds. The simulator may expose this conditional calculation, but production must not depend on it until overlap semantics are decided.

The boss must not spawn inside the player, and the encounter must expose a readable reaction window. This is an acceptance invariant, not a spawn-rate tuning value.

## Composition and spawn selection

B1 defines which archetypes may appear in each band but does not define exact ratios, weighted selection, duplicate limits, or elite insertion cadence. Therefore:

- Composition membership is CANON.
- Exact composition ratios are PENDING_B1.
- Weighted selection, duplicate limits, and elite cadence are PENDING_PRODUCT_DECISION.
- The simulator must not invent ratios and must report composition as a set of eligible IDs unless an explicit test fixture labels the weights TEST_PLACEHOLDER.

## Active-cap and safe-mode contract

The active cap in each band is CANON. The behavior when the cap is reached is not yet implemented.

Required production behavior to decide:

- Do not exceed the active cap.
- Keep XP accounting tied to actual defeated entities; do not create XP from suppressed spawn attempts.
- Preserve boss telegraphs, contact-hit gating, and readable aftermath.
- A performance safe mode may suppress non-gameplay VFX or defer ordinary spawn requests, but this is a PENDING_PRODUCT_DECISION and must not silently change reward or XP rules.
- The target performance requirement is a minimum of 30 FPS on the selected Android target; the target device and measurement protocol are still PENDING_PRODUCT_DECISION.

## Runtime evidence

The audit found no production wave-data consumer, run-session loop, reward ledger, or deterministic test harness. This document is therefore SPECIFIED, not RUNTIME_VERIFIED.
