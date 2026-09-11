# Balance Content Binding — 30-minute model

Status: `PARTIAL / PROPOSED_MODEL_ONLY`

This is the numeric balance overlay for the content described by the mockup and
content documents. The one source of numeric truth is
`BALANCE_MODEL.json`; the simulator reads it and does not repeat these values
in Python.

## Provenance boundary

| Field | Value |
|---|---|
| Parent main read before this slice | `7a8112e9bb3175d6c86030b14e680ce01b4e1254` |
| B1 | `docs/BALANCE_ECONOMY_SPEC.md`, `6aa4ec96afc8a8c9e6a35c164c99e7d62910a687` |
| Architecture contract | `e9a50971f61f204cbbda39edaad2c48a08e2228b` |
| Registry map | `0b8cb1bb96d4ab2d0bd14bd7a21b042e53d8c5e8` |
| Model | `BALANCE_MODEL.json`, version `0.8-registry-ids-elite-chest` |
| Numeric status rule | B1 exact values are `CANON`; formulas from explicit records are `DERIVED`; absent B1 absolute values are `PROPOSED` and never silently promoted |
| Runtime boundary | R2 structurally consumes the registry shape; this model's numeric values remain `PROPOSED`/`DERIVED` until a fresh post-publication trace |
| Late-run rule | 20:00–30:00 effective stats are derived from the proposed base records and proposed wave multipliers |

Every numeric record in the JSON has `value`, `source`, `derived_formula`,
`rationale` and `status`. The tables below are the resolved values for review;
the JSON remains authoritative for the full provenance text.

## XP target and synergy progression

The B1 XP threshold formula remains canonical. The proposed late pickup budgets are 22.0 XP/s for 20:00–25:00 and 27.0 XP/s for 25:00–30:00. Level 40 requires 16,852 XP; level 38 is an accepted lower variance floor.

To make three distinct 10/10 synergies testable in a 40-level run, the model uses a proposed paired offer: one player level advances one selected weapon and its linked passive. Three pairs consume 30 paired offers; remaining levels continue the build. This is a balance-model rule, not runtime approval.

## Weapons — 10

Base columns: damage per cast, interval, targets, range, area radius, projectile
speed, lifetime, pierce/chain limit, knockback, status duration. Evolution
columns are multiplier/extra-target/effect-duration overlays.

| ID | Base damage | Interval | Targets | Range | Area | Projectile | Life | Pierce | KB | Status s | Evolution D/Int/Area | +Targets | Effect s | Balance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| `weapon_moon_blade` | 18 | 0.75 | 2 | 82 | 34 | 180 | 0.35 | 3 | 10 | 0 | 0.20/0.92/1.25 | 2 | 1.5 | PROPOSED |
| `weapon_jade_talismans` | 12 | 0.65 | 3 | 240 | 12 | 170 | 1.30 | 1 | 2 | 1.5 | 0.18/0.90/1.20 | 2 | 1.8 | PROPOSED |
| `weapon_crimson_flame_fan` | 16 | 0.90 | 3 | 140 | 46 | 0 | 1.00 | 1 | 4 | 2.0 | 0.18/0.93/1.30 | 2 | 2.5 | PROPOSED |
| `weapon_frost_pearl` | 14 | 1.05 | 2 | 180 | 30 | 160 | 0.80 | 1 | 0 | 1.8 | 0.16/0.90/1.35 | 2 | 2.5 | PROPOSED |
| `weapon_thunder_needles` | 15 | 1.20 | 3 | 175 | 12 | 220 | 0.55 | 3 | 3 | 0.8 | 0.18/0.92/1.20 | 2 | 1.0 | PROPOSED |
| `weapon_spirit_bell` | 11 | 1.10 | 6 | 62 | 48 | 0 | 0.30 | 0 | 22 | 0.6 | 0.15/0.94/1.15 | 3 | 1.2 | PROPOSED |
| `weapon_fox_mirage` | 17 | 1.35 | 3 | 190 | 18 | 180 | 1.20 | 4 | 8 | 0.9 | 0.17/0.91/1.25 | 2 | 1.5 | PROPOSED |
| `weapon_lotus_mines` | 20 | 1.65 | 4 | 130 | 32 | 0 | 3.00 | 1 | 14 | 1.5 | 0.16/0.92/1.30 | 2 | 3.0 | PROPOSED |
| `weapon_star_bow` | 28 | 1.45 | 1 | 280 | 8 | 260 | 1.40 | 5 | 4 | 0 | 0.18/0.90/1.20 | 2 | 1.8 | PROPOSED |
| `weapon_black_eclipse_umbrella` | 10 | 1.00 | 5 | 100 | 42 | 0 | 1.80 | 0 | 12 | 1.0 | 0.14/0.95/1.30 | 2 | 1.5 | PROPOSED |

Reference DPS audit: base values are `19.31–60.00` against the proposed
ordinary anchor; evolved values are `68.74–125.22`. The synergy share guard is
40%, and all ten model checks pass it.

## Passives — 10

`damage/rank` and `defense/rank` are fractional modifiers. `primary` uses the
unit of the described effect (for example radius, seconds or flat utility),
and is not silently treated as universal damage.

| ID | Damage/rank | Defense/rank | Primary/rank | Trigger CD | Effect duration | Stack cap | Balance |
|---|---:|---:|---:|---:|---:|---:|---|
| `passive_wind_of_travel` | 0.020 | 0.003 | 0.012 | 4.0 | 2.0 | 1 | PROPOSED |
| `passive_jade_focus` | 0.030 | 0.002 | 0.150 | 2.5 | 1.5 | 1 | PROPOSED |
| `passive_ember_heart` | 0.022 | 0.001 | 0.250 | 1.5 | 2.0 | 1 | PROPOSED |
| `passive_frost_thread` | 0.018 | 0.002 | 0.080 | 2.0 | 1.5 | 1 | PROPOSED |
| `passive_heavenly_seal` | 0.025 | 0.001 | 0.080 | 1.5 | 1.25 | 1 | PROPOSED |
| `passive_iron_bell` | 0.012 | 0.004 | 0.040 | 4.0 | 1.0 | 1 | PROPOSED |
| `passive_mirror_shard` | 0.018 | 0.001 | 0.350 | 3.0 | 0.25 | 1 | PROPOSED |
| `passive_lotus_heart` | 0.010 | 0.004 | 0.020 | 5.0 | 5.0 | 1 | PROPOSED |
| `passive_star_compass` | 0.020 | 0.0015 | 6.000 | 3.5 | 2.5 | 1 | PROPOSED |
| `passive_spirit_lens` | 0.010 | 0.001 | 0.040 | 2.5 | 1.5 | 1 | PROPOSED |

## Synergies — 10

The model currently uses the C1 10/10 gate: weapon level 10 and passive rank 10.
Stage 06/07 mockups still say 6/5, so that gate is explicitly
`PENDING_PRODUCT_DECISION`, not a hidden lock.

| Synergy | Weapon → passive | Damage | Interval | Area | +Targets | Effect s | Family | Balance |
|---|---|---:|---:|---:|---:|---:|---|---|
| `synergy_moon_dance` | moon_blade → wind_of_travel | 0.20 | 0.92 | 1.25 | 2 | 1.5 | movement_route | PROPOSED |
| `synergy_heavenly_seals` | jade_talismans → jade_focus | 0.18 | 0.90 | 1.20 | 2 | 1.8 | mark_chain | PROPOSED |
| `synergy_phoenix_sky` | crimson_flame_fan → ember_heart | 0.18 | 0.93 | 1.30 | 2 | 2.5 | burn_route | PROPOSED |
| `synergy_winter_palace` | frost_pearl → frost_thread | 0.16 | 0.90 | 1.35 | 2 | 2.5 | control_lattice | PROPOSED |
| `synergy_heavenly_judgment` | thunder_needles → heavenly_seal | 0.18 | 0.92 | 1.20 | 2 | 1.0 | telegraphed_chain_burst | PROPOSED |
| `synergy_guardian_bell` | spirit_bell → iron_bell | 0.15 | 0.94 | 1.15 | 3 | 1.2 | projectile_ward | PROPOSED |
| `synergy_nine_reflections` | fox_mirage → mirror_shard | 0.17 | 0.91 | 1.25 | 2 | 1.5 | delayed_route_echo | PROPOSED |
| `synergy_lotus_sanctuary` | lotus_mines → lotus_heart | 0.16 | 0.92 | 1.30 | 2 | 3.0 | sanctuary_zone | PROPOSED |
| `synergy_constellation_rain` | star_bow → star_compass | 0.18 | 0.90 | 1.20 | 2 | 1.8 | anchor_constellation | PROPOSED |
| `synergy_eclipse_vortex` | black_eclipse_umbrella → spirit_lens | 0.14 | 0.95 | 1.30 | 2 | 1.5 | bounded_pull_burst | PROPOSED |

## Artifacts — 10

Artifacts do not consume weapon/passive build slots. They are offered from the
`ELITE_CHEST` and first-clear channels, exactly three cards per offer. Numeric
parameters below are proposed model inputs with their complete provenance in
the JSON.

| ID | Effect key | Trigger/target | Numeric parameters | Balance |
|---|---|---|---|---|
| `artifact_jade_compass` | `aura.drop_route_compass` | arena drop → route field | radius 42; duration 3.0; displacement 0.18; CD 2.0 | PROPOSED |
| `artifact_mirror_shard` | `trigger.critical_echo` | critical hit → source zone | echo 0.35; delay 0.25; CD 2.5 | PROPOSED |
| `artifact_phoenix_feather` | `trigger.elite_ember_path` | elite defeat → crossing path | length 80; width 10; burn 2.5; damage/tick 8; CD 3.5 | PROPOSED |
| `artifact_frost_bead` | `modifier.control_bloom` | control applied → target/area | mark 2.0; radius 28; damage 12; CD 1.5 | PROPOSED |
| `artifact_bell_fragment` | `trigger.guard_resonance` | damage/guarded hit → nearby | threshold 3; radius 42; knockback 20; CD 4.0 | PROPOSED |
| `artifact_lotus_seed` | `trigger.overheal_ward` | full-health heal → next hit | mitigation 0.25; ward 5.0; epsilon 0.01; CD 5.0 | PROPOSED |
| `artifact_moon_crown` | `target.boss_phase_window` | phase start → current boss | window 2.5; damage 0.25; CD 12.0 | PROPOSED |
| `artifact_black_bead` | `modifier.elite_polarity` | elite weapon hit → pack | pull radius 36; burst radius 30; effect 0.18; CD 2.0 | PROPOSED |
| `artifact_tideglass` | `aura.drop_tide_path` | arena drop → saved path | duration 2.2; width 9; slow 0.25; displacement 14; CD 2.0 | PROPOSED |
| `artifact_silent_lantern` | `target.threat_telegraph` | threat select → highest target | lead 1.0; mark 4.0; target count 1; refresh 3.0 | PROPOSED |

## Ordinary enemies — 10

`Base` is pre-wave HP/ATK/speed. `Late` is the derived effective value in the
25:00–30:00 `wave_apocalypse_25_30` band: HP ×3.30, ATK ×2.00, speed ×1.12.

| ID | Role | Base HP/ATK/speed | Attack CD | Late HP/ATK/speed | Balance |
|---|---|---|---:|---|---|
| `enemy_ink_beetle` | rusher | 24 / 3 / 70 | 0.8 | 79.20 / 6 / 78.40 | PROPOSED |
| `enemy_lantern_moth` | ranged | 30 / 4 / 42 | 1.6 | 118.80 / 8 / 47.04 | PROPOSED |
| `enemy_bone_carp` | telegraphed dash | 36 / 7 / 58 | 2.4 | 166.32 / 14 / 64.96 | PROPOSED |
| `enemy_paper_ghost` | teleport | 34 / 7 / 48 | 2.0 | 145.86 / 14 / 53.76 | PROPOSED |
| `enemy_jade_toad` | telegraphed zone | 36 / 7 / 36 | 3.0 | 190.08 / 14 / 40.32 | PROPOSED |
| `enemy_mirror_fox` | decoy | 38 / 7 / 46 | 2.5 | 188.10 / 14 / 51.52 | PROPOSED |
| `enemy_bell_crab` | blocker/rear weakness | 35 / 7 / 28 | 1.8 | 277.20 / 14 / 31.36 | PROPOSED |
| `enemy_thread_doll` | slow beam | 20 / 6 / 30 | 1.2 | 118.80 / 12 / 33.60 | PROPOSED |
| `enemy_lotus_usher` | telegraphed zone route | 42 / 7 / 34 | 2.7 | 235.62 / 14 / 38.08 | PROPOSED |
| `enemy_moonroot_burrower` | burrow ambush | 46 / 7 / 50 | 2.6 | 288.42 / 14 / 56.00 | PROPOSED |

Legacy `enemy_stone_oni` and `enemy_eclipse_serpent` remain outside the target
10-ID ordinary roster; they are not silently counted as the two new ordinary
families.

## Elite variants — 10

Elite overlays are finite event content; a run selects at most five registered
variants. `Resolved` is the derived base overlay; `Late` applies the same final
wave multipliers as the ordinary table.

| Variant | Base ID | HP×/ATK×/speed×/XP× | Resolved HP/ATK/speed | Late HP/ATK/speed | Balance |
|---|---|---|---|---|---|
| `elite_variant_ink_beetle_ironcarapace` | ink_beetle | 6.0/1.10/1.00/2.0 | 144 / 3.30 / 70.00 | 475.20 / 6.60 / 78.40 | PROPOSED |
| `elite_variant_lantern_moth_prismwing` | lantern_moth | 6.5/1.25/1.05/2.0 | 234 / 5.00 / 44.10 | 772.20 / 10.00 / 49.392 | PROPOSED |
| `elite_variant_bone_carp_tidepiercer` | bone_carp | 7.0/1.30/1.08/2.0 | 352.8 / 9.10 / 62.64 | 1164.24 / 18.20 / 70.157 | PROPOSED |
| `elite_variant_paper_ghost_sealbreaker` | paper_ghost | 6.5/1.20/1.05/2.0 | 287.3 / 8.40 / 50.40 | 948.09 / 16.80 / 56.448 | PROPOSED |
| `elite_variant_jade_toad_mudcrown` | jade_toad | 7.0/1.25/1.00/2.0 | 403.2 / 8.75 / 36.00 | 1330.56 / 17.50 / 40.32 | PROPOSED |
| `elite_variant_mirror_fox_falsepath` | mirror_fox | 6.5/1.20/1.10/2.0 | 370.5 / 8.40 / 50.60 | 1222.65 / 16.80 / 56.672 | PROPOSED |
| `elite_variant_bell_crab_resonant_shell` | bell_crab | 7.0/1.30/1.00/2.0 | 588 / 9.10 / 28.00 | 1940.40 / 18.20 / 31.36 | PROPOSED |
| `elite_variant_thread_doll_cutline` | thread_doll | 7.0/1.25/1.02/2.0 | 252 / 7.50 / 30.60 | 831.60 / 15.00 / 34.272 | PROPOSED |
| `elite_variant_lotus_usher_bloomguard` | lotus_usher | 7.0/1.25/1.00/2.0 | 499.8 / 8.75 / 34.00 | 1649.34 / 17.50 / 38.08 | PROPOSED |
| `elite_variant_moonroot_burrower_gravewake` | moonroot_burrower | 7.5/1.30/1.08/2.0 | 655.5 / 9.10 / 54.00 | 2163.15 / 18.20 / 60.48 | PROPOSED |

## Bosses and mini-bosses

The ID status and numeric balance status are separate. Existing boss IDs may be
canonical content IDs, but every absolute number below is `PROPOSED` because B1
does not contain the requested per-ID absolute stats.

### Main bosses

| Checkpoint | ID | HP / ATK / speed | Attack CD | Telegraph | XP | Numeric status |
|---|---|---|---:|---:|---:|---|
| 05:00 | `boss_hua_lin` | 3600 / 12 / 24 | 3.2 | 0.90 | 250 | PROPOSED |
| 10:00 | `boss_miyeon` | 4500 / 15 / 28 | 3.0 | 0.85 | 250 | PROPOSED |
| 15:00 | `boss_seika` | 5200 / 18 / 30 | 2.8 | 0.80 | 250 | PROPOSED |
| 20:00 | `boss_tideglass_regent` | 9600 / 22 / 34 | 2.6 | 0.80 | 250 | PROPOSED |
| 25:00 | `boss_omen_paper_archivist` | 10000 / 26 / 36 | 2.5 | 0.80 | 250 | PROPOSED |
| 30:00 | `boss_black_moon_empress` | 11200 / 30 / 38 | 2.4 | 0.80 | 250 | PROPOSED |

Each main boss has two proposed readable phases, a 110-unit pressure radius and
a four-threat summon cap. MAIN encounters freeze visible run/wave/XP/ordinary
spawns; only the encounter clock advances.

### Mini-bosses

| Checkpoint | ID | HP / ATK / speed | Attack CD | Telegraph | XP | Numeric status |
|---|---|---|---:|---:|---:|---|
| 07:30 | `miniboss_ink_jade_warden` | 3000 / 14 / 22 | 2.8 | 0.90 | 80 | PROPOSED |
| 12:30 | `miniboss_veil_harvester` | 3300 / 16 / 24 | 2.6 | 0.85 | 80 | PROPOSED |
| 17:30 | `miniboss_lotus_ritekeeper` | 3600 / 18 / 26 | 2.5 | 0.80 | 80 | PROPOSED |
| 22:30 | `miniboss_bell_rhythm_ascetic` | 3900 / 20 / 28 | 2.4 | 0.80 | 80 | PROPOSED |
| 27:30 | `miniboss_moonroot_ferryman` | 4300 / 22 / 30 | 2.3 | 0.80 | 80 | PROPOSED |

Each mini has one proposed primary phase, an 80-unit pressure radius and a
two-threat summon cap. MINI encounters continue run/wave/XP/ordinary spawning.

## Dependencies and fallback

`weapon → passive → synergy` pairs are one-to-one in the catalog. A boss chest
resolves an eligible synergy or the bounded `fallback_damage_resonance` (+3%
once per unresolved non-final chest). Five `ELITE_CHEST` windows follow the
five mini-boss checkpoints; their finite pressure packs use the ten-ID elite
catalog with a maximum-five active projection, and each three-card offer does
not mutate the wallet. Final 30:00 has no boss chest; first-clear artifact
offer remains separate and idempotent.

## Open decisions

1. Promote or revise the proposed absolute stat table in B1; until then these
   values are model inputs, not a balance lock.
2. Resolve the C1 10/10 progression gate versus Stage 06/07 mockup 6/5 gate.
3. Architecture/Runtime must consume this JSON and prove the 30-minute Godot
   trace; model evidence cannot close runtime, collision, or Android gates.
