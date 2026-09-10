# Balance XP and Rewards

Status: SIMULATED_MODEL_ONLY / PARTIAL

Source baseline: B1 revision 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687. The simulator reads BALANCE_MODEL.json; it does not duplicate the XP, wave, reward, or profile numbers in Python.

## Canonical XP formula

For level L:

    XP_to_next(L) = round(30 + 12 × (L − 1) + 3 × (L − 1)^1.35)

The formula and drop vocabulary [1, 5, 15, 40, 80, 250] are CANON. The simulator materializes the four formula parameters in the model and uses half-up rounding to avoid language-runtime rounding drift.

## Proposed pickup model

B1 does not define pickup latency or collection capacity. The model exposes each proposed value:

| Input | Value | Status | Purpose |
|---|---:|---|---|
| Drop delay | 1.0 s | PROPOSED | separates defeat from aftermath pickup |
| First-level window | 45 s | CANON target bound | explicit early-progression calibration window |
| First-window capacity | 0.75 XP/s | PROPOSED | places first level-up in the 30–45 s target |
| wave_00_02 capacity | 0.35 XP/s | PROPOSED | conservative warmup |
| wave_02_05 capacity | 1.35 XP/s | PROPOSED | level-5 target |
| wave_05_10 capacity | 1.90 XP/s | PROPOSED | level-9 target |
| wave_10_15 capacity | 2.50 XP/s | PROPOSED | level-13 target |
| wave_15_20 capacity | 3.80 XP/s | PROPOSED | level-17–18 target |
| magnet capacity per rank | +2% | PROPOSED | small pickup benefit; B1 canonically defines radius, not rate |
| boss XP | excluded from main level curve | PROPOSED | prevents an unconfirmed 250-XP boss grant from invalidating B1 timing targets |

## Five-seed level result

| Profile / hero | First level | Level at 2 / 5 / 10 / 15 / 20 min | Final level |
|---|---:|---|---:|
| fresh | hero_lin_yue | 39.75 | 2 / 5 / 9 / 13 / 17 | 17 | 0 | 39.38 | 50.62 | 1.15 / 2.85 | 24.5 / 38.05 |
| fresh | hero_seoyeon_han | 39.75 | 2 / 5 / 9 / 13 / 17 | 17 | 0 | 63.04 | 46.96 | 0.75 / 2.4 | 18 / 33.3 |
| max_m1 | hero_lin_yue | 33.25 | 2 / 6 / 10 / 14 / 18 | 18 | 0 | 84.474 | 23.526 | 0.75 / 1.75 | 17.65 / 23.85 |
| max_m1 | hero_seoyeon_han | 33.25 | 2 / 6 / 10 / 14 / 18 | 18 | 0 | 115.116 | 16.884 | 0.5 / 1.25 | 12.35 / 18 |
| moderate | hero_lin_yue | 38.25 | 2 / 6 / 10 / 13 / 17 | 17 | 0 | 61.159 | 34.241 | 1.25 / 2.6 | 22.3 / 39.1 |
| moderate | hero_seoyeon_han | 38.25 | 2 / 6 / 10 / 13 / 17 | 17 | 0 | 83.868 | 32.732 | 0.75 / 1.75 | 15.1 / 27 |

Fresh reaches its first level-up at 39.75 s in both hero routes. Moderate reaches it at 38.25 s; max M1 at 33.25 s. Fresh matches the B1 2/5/9/13/17–18 cadence in this model. Moderate and max M1 are intentionally faster at later checkpoints and should be treated as stress profiles, not canonical timing proof.

## Rewards, boss chest, artifact offer, and fallback

B1 checkpoint totals remain CANON. The architecture contract adds the live settlement policy:

- reward ledger key: {run_id}:{reward_scope}:{checkpoint_id}:{reward_type};
- duplicate commit returns the existing entry without applying currency again;
- non-final checkpoints may create a **boss chest** for synergy/evolution or fallback;
- final boss creates no boss chest;
- the B1 first-clear artifact value is represented by a separate post-result `FIRST_CLEAR_REWARD` artifact offer with exactly three choices; it is not a final boss chest and is not automatically granted before the player chooses;
- special elite packs between bosses may create the same three-card artifact offer; cadence and composition remain PENDING until B1/product defines them;
- when a non-final synergy is not eligible, the model applies one proposed +3% fallback damage upgrade.

| Profile / hero | Ledger balance | Idempotency | Final boss chest | Boss-chest outcome | Fallback bonus |
|---|---|---|---|---|---|
| fresh/hero_lin_yue | {"boss_essence": 6, "gold": 725, "moon_seals": 300} | PASS | false | synergy_heavenly_seals | 0.06 |
| fresh/hero_seoyeon_han | {"boss_essence": 3, "gold": 225, "moon_seals": 60} | PASS | false | synergy_moon_dance | 0.06 |
| max_m1/hero_lin_yue | {"boss_essence": 6, "gold": 725, "moon_seals": 300} | PASS | false | synergy_heavenly_seals | 0.06 |
| max_m1/hero_seoyeon_han | {"boss_essence": 6, "gold": 725, "moon_seals": 300} | PASS | false | synergy_moon_dance | 0.06 |
| moderate/hero_lin_yue | {"boss_essence": 6, "gold": 725, "moon_seals": 300} | PASS | false | synergy_heavenly_seals | 0.06 |
| moderate/hero_seoyeon_han | {"boss_essence": 3, "gold": 225, "moon_seals": 60} | PASS | false | synergy_moon_dance | 0.06 |

The B1 first-clear totals are 725 gold / 300 Moon Seals / 6 boss essence. The repeat-clear totals are 425 / 120 / 5. They remain arithmetic CANON values. The first-clear artifact offer is a separate three-card post-result boundary; exact artifact effect, refresh, duplicate/stacking and Codex persistence rules remain pending.

## Evidence boundary

This is a deterministic model result, not a wallet, save/reconnect, UI, or runtime XP proof.
