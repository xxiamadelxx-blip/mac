# Balance Combat Model — 30-minute MAC model

Status: \`PARTIAL / SIMULATED_MODEL_ONLY\`

The model is data-driven and reads combat inputs from \`BALANCE_MODEL.json\`. The reference repositories were used only to confirm separable responsibilities (progression, spawn curve, encounter state, loot path); their numeric values are not MAC inputs.

## Canonical hero and enemy inputs

| Input | MAC value/status | Source |
|---|---|---|
| Base hero HP / speed / damage / cooldown / armor / magnet | 100 / 100% / 1.00 / 1.00 / 0 / 100% — CANON | B1 §3 |
| Lin Yue | 90 HP, 100% speed, 120% magnet — CANON | B1 §3 |
| Soyeon Han | 110 HP, 112% speed — CANON | B1 §3 |
| Contact hit gate | 0.8s, telegraph required, no same-frame infinite stacking — CANON | B1 §5 |
| Enemy HP/ATK/speed bands through 20:00 | B1 table — CANON | B1 §4 |
| 20:00–30:00 HP/ATK/speed bands | 2.70→3.30 / 1.75→2.00 / 1.10→1.12 — PROPOSED | JSON extension fields; B1 has no 30-minute numeric band |

Absolute base HP, base ATK, base speed by enemy ID, exact ranged hit values and crit values are not complete in B1. They remain PENDING_B1 or PENDING_PRODUCT_DECISION; the simulator does not promote them to CANON.

## Formula contract

\`raw_damage = weapon_damage × hero_damage_multiplier × weapon_level_multiplier × passive_multiplier × profile_multiplier × expected_critical_multiplier\`

\`post_armor_damage = raw_damage × (1 − min(mitigation_cap, armor + defense_rank × 0.01))\`

\`weapon_level_multiplier = 1 + weapon_level_damage_per_level × (weapon_level − 1)\`

\`expected_critical_multiplier = 1 + crit_chance × (crit_multiplier − 1)\`

\`TTK = effective_HP ÷ focused_sustained_DPS\`

\`incoming_damage = Σ(landed_hit_damage × wave_ATK_multiplier × (1 − mitigation))\`

The proposed model limits the mean-field engaged attacker set and applies seeded landed-hit probability. This is a diagnostic model, not a substitute for collision, telegraph or player telemetry.

## Weapon, passive, synergy and fallback contract

| Layer | Rule | Status |
|---|---|---|
| Weapon | numeric damage/cadence/target count are read from the model; no controller constants | PROPOSED/PENDING_B1 |
| Passive | rank multipliers are data fields; global meta ranks use B1 costs/effects | B1 CANON + PROPOSED local run inputs |
| Synergy eligibility | matching weapon/passive IDs, weapon level 6, passive rank 5, weapon not already evolved, non-final boss chest | DERIVED from content/architecture; exact full catalog join pending |
| Synergy power | clamp one synergy contribution to ≤40% of total damage | CANON target / model guard |
| Fallback | one non-currency micro-upgrade when no eligible synergy exists; proposed +3% damage once per unresolved non-final chest | PROPOSED_PRODUCT_DECISION |
| Artifact | three-card offer, choose one active run effect, no weapon/passive slot, exact effects/refresh/stacking pending | CONFIRMED surface + PENDING effect contract |

The external projects support this separation: [PlayerController/Player in 20-Minutes-till-dawn](https://github.com/ParsaSabzei/20-Minutes-till-dawn/blob/main/core/src/main/java/ap/project/controller/PlayerController.java) separates XP transition from ability application; [Sentaur UpgradeManager](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/Upgrades/UpgradeManager.cs) keeps upgrade-pool selection out of spawn math. MAC keeps the same boundary while retaining its own B1 IDs and numbers.

## TTK target and model evidence

| Measure | MAC target | Fresh | Moderate | Max M1 | Status |
|---|---:|---:|---:|---:|---|
| Ordinary enemy TTK | 0.5–2.5s | 0.75–1.25s | 0.75–1.25s | 0.50–0.75s | SIMULATED |
| Existing elite TTK | 10–25s | 17.25–27.75s | 18.25–25.25s | 14.00–20.00s | SIMULATED/PARTIAL |
| Elite variant TTK | proposed 5–15s | 7.00–20.25s | 5.75–14.50s | 7.00–15.25s | SIMULATED/PARTIAL |
| Mini-boss TTK | proposed 20–55s | 42.50–54.75s | 39.00–50.25s | 30.25–38.25s | SIMULATED |
| Main 05/10/15 TTK | 45–80s | 63.25–78.00s | 58.25–70.50s | 44.75–54.50s | SIMULATED |
| Main 20/25 TTK | proposed 60–100s | 110.25–123.75s | 100.50–113.25s | 78.00–87.75s | SIMULATED/PARTIAL |
| Final 30 TTK | 90–120s | 117.25–130.50s | 107.25–119.75s | 82.75–92.75s | SIMULATED/PARTIAL |

The late fresh/moderate boss rows and the high-durability elite-variant tail do not pass their proposed targets. They are tuning evidence, not hidden fixes.

## Required runtime proof

Runtime must consume this one JSON source and emit main-boss freeze, mini-boss continuation, wave reset/ramp/siege, active-cap occupancy, XP levels, TTK, incoming damage/death and reward idempotency. No Godot or Android evidence is present; status remains PARTIAL.
