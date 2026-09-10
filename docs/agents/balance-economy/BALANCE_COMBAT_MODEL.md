# Balance Combat Model — 30-minute extension

Status: `PARTIAL / SIMULATED_MODEL_ONLY`

## Clock and encounter math

- Main boss: visible run clock stops at checkpoint; wave selection, ordinary spawning and XP pickup stop; a separate wall encounter clock advances.
- Mini-boss: visible run clock, waves, XP pickup and ordinary spawning continue; the mini encounter uses the same wall/run clock.
- Elite variation: finite overlay entity; it counts against the ordinary/elite active cap and never becomes a permanent composition member.

## Data-driven formulas

`post_armor_damage = raw_damage × (1 − min(mitigation_cap, armor + defense_rank × 0.01))`

`weapon_level_multiplier = 1 + weapon_level_damage_per_level × (weapon_level − 1)`

`focused_TTK = effective_HP ÷ (player_attack_damage × boss_focus_fraction)`

`effective_spawn_budget = density_ramp_budget × boss_interruption_factor`

For every post-main-boss cycle:

- entry budget/cap = 0.80 × preceding/entry anchor;
- 8s suppression;
- 20s recovery factor 0.70→1.00;
- linear ramp;
- final 60s at the peak siege.

All non-B1 numbers are stored in the JSON model with `source`, `derived_formula`, `rationale` and `status`.

## Targets and observed model ranges

| Measure | Proposed target | Observed model result |
|---|---|---|
| Ordinary TTK | 0.5–2.5s | medians remain in band |
| Existing elite TTK | 10–25s | reported per archetype; model-only |
| Elite-variant TTK | 5–15s | 5.0–36.0s means across profiles; high-durability anchors need tuning |
| Mini-boss TTK | 20–55s | fresh 42.5–54.75s; moderate 39.0–50.25s; max 30.25–38.25s |
| Main boss 05/10/15 | 45–80s | reported per profile/seed |
| Late main boss 20/25 | 60–100s | fresh/moderate exceed proposed target; max is inside |
| Final 30 | 90–120s | moderate/max mostly inside; fresh is a stress case |

Incoming damage is computed from up to the data-model engaged-attacker limit and the landed-hit probability in each profile. The single-hit check is measured against the 15% base-HP telegraph bound. These are deterministic model assumptions, not player telemetry.

## Required runtime proof

Runtime must consume `BALANCE_MODEL.json` and produce traces for:

- visible timer freeze for all main bosses;
- visible timer continuation for all five mini-bosses;
- wave density reset/ramp/siege;
- active-cap occupancy and overflow;
- XP/levels at 02/05/10/15/20/25/30;
- ordinary, existing elite, elite-variant, mini and main TTK;
- incoming damage/death;
- reward/chest/elite-offer idempotency.

No runtime or Android evidence is present in this slice.
