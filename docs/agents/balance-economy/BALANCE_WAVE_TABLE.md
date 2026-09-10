# Balance Wave Table

Status: SIMULATED_MODEL_ONLY / PARTIAL

Source baseline: docs/BALANCE_ECONOMY_SPEC.md, revision 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687.
Current model: BALANCE_MODEL.json, simulation_model version 0.3.
Publication HEAD for this slice is recorded in BALANCE_AUDIT.md after the synchronized updates.

## Canonical wave bands

| Band | Time window | Spawn budget | Active cap | HP multiplier | Damage multiplier | Speed multiplier | B1 composition target |
|---|---:|---:|---:|---:|---:|---:|---|
| wave_warmup_0_2 | 0:00–2:00 | 6/s | 40 | 1.00 | 0.70 | 0.90 | Ink beetle; level 2 |
| wave_pressure_2_5 | 2:00–5:00 | 10/s | 80 | 1.10 | 0.85 | 1.00 | Beetle, moth, carp; level 5 |
| wave_threat_5_10 | 5:00–10:00 | 15/s | 130 | 1.35 | 1.00 | 1.02 | Extended roster; level 9 |
| wave_elite_10_15 | 10:00–15:00 | 22/s | 200 | 1.70 | 1.25 | 1.05 | Elites enter; level 13 |
| wave_eclipse_15_20 | 15:00–20:00 | 30/s | 280 | 2.20 | 1.55 | 1.08 | Full roster; level 17–18 |

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

The latest five-seed matrix reached the cap of 280 in every profile/hero slice. Mean cap occupancy time was 1,117.45–1,157.20 seconds of the 1,200-second visible wave clock across the six profile/hero aggregates. One fresh Lin Yue seed died before the final boss; this is a risk result, not a hidden pass. This remains a model-only sustained-cap stress case and is not runtime proof of acceptable feel or performance.

## Post-boss recovery → ramp → siege

The user-facing pressure rule is now explicit in `simulation_model.boss_wave_ramp`:

| Post-boss cycle | Quiet entry after boss | Linear ramp | Peak/siege before next boss | Phase lengths |
|---|---:|---:|---:|---|
| 5:00 → 10:00 | 8/s, cap 64 (80% of the preceding 10/s, cap 80 peak) | 8/s → 15/s, cap 64 → 130 | 15/s, cap 130 | 28 s recovery + 212 s ramp + 60 s siege |
| 10:00 → 15:00 | 12/s, cap 104 (80% of the preceding 15/s, cap 130 peak) | 12/s → 22/s, cap 104 → 200 | 22/s, cap 200 | 28 s recovery + 212 s ramp + 60 s siege |
| 15:00 → 20:00 | 17.6/s, cap 160 (80% of the preceding 22/s, cap 200 peak) | 17.6/s → 30/s, cap 160 → 280 | 30/s, cap 280 | 28 s recovery + 212 s ramp + 60 s siege |

Formula: `entry = preceding_peak × 0.80`; the 8-second zero-spawn suppression and 20-second 0.70→1.00 recovery complete first; the remaining 212 seconds use linear interpolation; the final 60 seconds hold the next canonical peak. Composition weights are blended from the entry band to the peak band. The first 0:00→5:00 segment keeps the canonical warmup→pressure bands.

The reset factor 0.80 and siege duration 60 seconds are PROPOSED because B1 specifies the bands and boss checkpoints but not this post-boss curve. The cycle mapping, interpolation and phase boundaries are DERIVED from the canonical band anchors, 300-second checkpoint spacing, the existing 8+20-second interruption window and the user’s low-to-peak/siege rule. The simulator emits samples for post-boss start, suppression end, recovery end, ramp peak and siege-before-boss.

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
