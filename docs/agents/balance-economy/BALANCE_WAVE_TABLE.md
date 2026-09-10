# Balance Wave Table

Status: SIMULATED_MODEL_ONLY / PARTIAL

Source baseline: docs/BALANCE_ECONOMY_SPEC.md, revision 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687.
Current model: BALANCE_MODEL.json, simulation_model version 0.2.
Live main HEAD verified before this documentation refresh: 0536f182c1ae8876b9213e0c2fb761793e503a66.

## Canonical wave bands

| Band | Time window | Spawn budget | Active cap | HP multiplier | Damage multiplier | Speed multiplier | B1 composition target |
|---|---:|---:|---:|---:|---:|---:|---|
| wave_00_02 | 0:00–2:00 | 6/s | 40 | 1.00 | 0.70 | 0.90 | Ink beetle; level 2 |
| wave_02_05 | 2:00–5:00 | 10/s | 80 | 1.10 | 0.85 | 1.00 | Beetle, moth, carp; level 5 |
| wave_05_10 | 5:00–10:00 | 15/s | 130 | 1.35 | 1.00 | 1.02 | Extended roster; level 9 |
| wave_10_15 | 10:00–15:00 | 22/s | 200 | 1.70 | 1.25 | 1.05 | Elites enter; level 13 |
| wave_15_20 | 15:00–20:00 | 30/s | 280 | 2.20 | 1.55 | 1.08 | Full roster; level 17–18 |

The first five rows are CANON from B1 section 4. Their nominal spawn opportunities are DERIVED as 720, 1,800, 4,500, 6,600, and 9,000 attempts respectively, for 22,620 before cap suppression and boss interruption.

## Model selection and cap behavior

Exact composition ratios were absent from B1. They are now explicit in BALANCE_MODEL.json under simulation_model.wave_selection.composition_weights with status PROPOSED and a provenance block. The simulator performs seeded weighted selection and does not contain a second copy of those ratios.

The model uses:

- ordinary and elite entities count toward the active cap;
- one boss slot is reserved outside that cap;
- excess spawn attempts are discarded rather than accumulated as hidden debt;
- suppressed attempts create no XP;
- occupancy is sampled every 0.25 seconds;
- safe-mode/runtime behavior remains NOT_IMPLEMENTED.

The five-seed model run reached the cap of 280 in every profile/hero slice. Mean cap occupancy time was approximately 1,118–1,150 seconds of the 1,200-second wave clock, with approximately 19,600–20,500 suppressed spawn attempts. This is a material MODEL finding: the proposed spawn/damage/cap combination is a sustained-cap stress case and is not runtime proof of acceptable feel or performance.

## Boss interruption

The canonical B1 values remain:

- ordinary spawn reduction window: 8 seconds;
- recovery starts at factor 0.70;
- recovery ends at factor 1.00;
- recovery duration: 20 seconds.

The exact suppression factor and overlap semantics were absent from B1. The model proposes factor 0.0 for the first 8 seconds and a latest-boss-restarts-recovery policy. These values are PROPOSED, not CANON.

## Architecture synchronization

The current architecture contract uses stable boss checkpoint IDs and reserves chest offers for non-final checkpoints. The final checkpoint is CHECKPOINT_REWARD_THEN_RUN_VICTORY_NO_CHEST. The simulator therefore creates no final chest_offer; the first-clear artifact is represented as a run-result grant, pending product confirmation.

## Evidence boundary

This table and the simulator are SIMULATED_MODEL_ONLY. They do not establish Godot spawn behavior, collision, telegraph readability, Android frame time, or player routing.
