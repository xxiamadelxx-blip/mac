# Balance Combat Model

Status: SPECIFIED / PARTIAL

This document defines the combat equations and safety invariants that implementation and testing must satisfy. It is derived from docs/BALANCE_ECONOMY_SPEC.md at revision 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687. It does not fill missing base stats with guesses.

## Status and units

- CANON values come from B1 and are reproduced in BALANCE_MODEL.json.
- DERIVED values are arithmetic or test projections from complete CANON inputs.
- PENDING_B1 means the contract needs a value that B1/GAME_MANIFEST does not currently provide.
- PENDING_PRODUCT_DECISION means an implementation policy is still open.
- TEST_PLACEHOLDER values may appear only in the simulator/report and are never production balance data.
- Runtime integration is NOT_IMPLEMENTED in the audited repository.

Units: HP for damage, world units per second for speed, seconds for cooldown/time, integer units for XP.

## Hero baseline

| Stat | Base hero | Lin Yue | Soyeon Han | Status |
|---|---:|---:|---:|---|
| Max HP | 100 | 90 | 110 | CANON, B1 section 3 |
| Move speed | 100% | 100% | 112% | CANON, B1 section 3 |
| Damage multiplier | 1.00 | pending ranged/control tuning | pending melee/critical-window tuning | Base is CANON; hero-specific numeric modifiers are PENDING_B1 |
| Weapon cooldown multiplier | 1.00 | pending | pending | Base is CANON; hero-specific value PENDING_B1 |
| Armor | 0 | pending | pending | Base is CANON; hero-specific value PENDING_B1 |
| Pickup radius | 100% | 120% | 100% unless otherwise specified | CANON, B1 section 3 |
| Role rule | baseline | ranged/control, weaker in melee | dash/melee/critical windows, plays near horde | CANON, B1 section 3 |

## Combat pipeline contract

The production hit pipeline must be ordered and instrumented:

1. Create an attack event with source, target, raw damage, timestamp, and deterministic event ID.
2. Apply hero, weapon, passive, synergy, wave, and other approved damage multipliers.
3. Roll critical behavior only when crit chance and crit multiplier are defined. Both are PENDING_B1 in the current contract.
4. Apply target mitigation. The armor formula and rounding policy are PENDING_PRODUCT_DECISION.
5. Apply hit gates: contact damage has a 0.8-second cooldown; same-frame damage stacking is forbidden.
6. Subtract the final integer/float result from target HP using one documented rounding policy.
7. Emit combat diagnostics sufficient to reproduce DPS, TTK, telegraph timing, and rejected duplicate hits.

The compact equation is:

enemy HP = base HP(enemy_id) × durability multiplier(enemy_id) × wave HP multiplier

enemy damage = base damage(enemy_id) × wave damage multiplier

enemy speed = base speed(enemy_id) × wave speed multiplier

final damage = mitigation( raw damage × approved multipliers × critical result )

TTK = effective HP / sustained DPS

The first three equations are the intended contract, but base enemy HP, base enemy damage, base enemy speed, mitigation, and rounding are not available in B1. A TTK value is DERIVED only after those inputs and the attack cadence are present.

## TTK targets

| Encounter class | Target | Status |
|---|---:|---|
| Ordinary enemy | 0.5–2.5 seconds | CANON, B1 section 3 |
| Elite | 10–25 seconds | CANON, B1 section 3 |
| First-slice boss | 45–80 seconds | CANON, B1 section 3 |
| Final boss | 90–120 seconds | CANON, B1 section 3 |

These are encounter targets, not proof that the current repository meets them.

## Enemy archetype contract

| Enemy ID | Role | Durability multiplier | XP | Missing production inputs |
|---|---|---:|---:|---|
| enemy_ink_beetle | rusher | 1.0 | 1–5 | base HP, damage, speed |
| enemy_lantern_moth | ranged | 1.2 | 5 | base HP, damage, speed, projectile cadence |
| enemy_bone_carp | telegraphed dash | 1.4 | 5–15 | base HP, damage, speed, dash hit |
| enemy_paper_ghost | teleport | 1.3 | 5–15 | base HP, damage, speed, teleport cadence |
| enemy_jade_toad | jump and zone | 1.6 | 15 | base HP, damage, speed, zone damage |
| enemy_mirror_fox | decoy/copy | 1.5 | 15 | base HP, damage, speed, decoy rules |
| enemy_bell_crab | front block/rear weakness | 2.4 | 15–40 | base HP, damage, speed, angle/mitigation rule |
| enemy_thread_doll | slow beam | 1.8 | 15–40 | base HP, damage, speed, beam tick/slow |
| elite_stone_oni | slow elite, telegraphed AoE | 7.0 | 40–80 | base HP, damage, speed, AoE |
| elite_eclipse_serpent | fast elite, trail/arcs | 8.0 | 80 | base HP, damage, speed, trail/arcs |

Durability multipliers and XP ranges are CANON, B1 section 5. The missing fields are intentionally null in BALANCE_MODEL.json. Filling them with simulator-only numbers requires a TEST_PLACEHOLDER label and cannot be promoted to production without a B1 follow-up.

## Safety invariants

- Contact hit cooldown: 0.8 seconds, CANON.
- Every dangerous attack needs a readable telegraph, CANON.
- Elite spawn must be safe relative to the player, CANON.
- Same-frame damage stacking is forbidden, CANON.
- No untelegraphed hit may exceed 15% of base hero HP, CANON acceptance target.
- Bosses must not spawn inside the player and must leave a readable reaction window, CANON acceptance target.
- The implementation must expose active-mass and safe-mode diagnostics before Android performance is assessed.

## Required combat evidence

A valid combat result must include the exact source revision, profile definition, hero/build, wave band, enemy ID, HP/damage/speed inputs, mitigation rule, attack cadence, crit rule, event trace or deterministic seed, measured TTK, and rejected-hit count. Without these fields the result is SPECIFIED or SIMULATED_TEST_PLACEHOLDER, not RUNTIME_VERIFIED.
