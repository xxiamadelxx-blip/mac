# Balance Combat Model

Status: SIMULATED_MODEL_ONLY / PARTIAL

This document separates B1 CANON targets from the explicit PROPOSED inputs used by the deterministic model. The complete proposed input set is in BALANCE_MODEL.json under simulation_model.enemy_stats, boss_stats, combat_math, heroes_and_profiles, and build_catalog.

## Canonical targets and invariants

| Requirement | B1 value | Status |
|---|---:|---|
| Ordinary TTK | 0.5–2.5 s | CANON target |
| Elite TTK | 10–25 s | CANON target |
| First-slice boss TTK | 45–80 s | CANON target |
| Final boss TTK | 90–120 s | CANON target |
| Contact damage cooldown | 0.8 s | CANON |
| No same-frame damage stacking | forbidden | CANON |
| No untelegraphed hit above base HP × 15% | 15% | CANON acceptance target |
| Boss safe spawn and readable reaction window | required | CANON acceptance target |

B1 does not define absolute enemy HP/damage/speed, boss stats, armor mitigation, crit values, weapon cadence, exact composition ratios, or profile definitions. Those values are now visible as PROPOSED or DERIVED entries in the model; they have not been promoted to CANON.

## Model formulas

- enemy HP = proposed base HP × B1 durability multiplier × canonical wave HP multiplier;
- enemy damage = proposed base damage × canonical wave damage multiplier;
- outgoing damage = raw hit × hero multiplier × weapon-level multiplier × passive multiplier × profile multiplier × expected critical multiplier;
- mitigation = raw incoming damage × (1 − proposed damage-reduction fraction);
- weapon-level multiplier = 1 + proposed 0.10 × (weapon level − 1);
- focused TTK = effective HP ÷ focused sustained DPS;
- incoming damage = landed attack damage × wave damage multiplier × (1 − mitigation).

The simulator reports focused TTK from the first damage event, separately from spawn-to-kill delay. This prevents queueing behind an active horde from being misreported as enemy durability.

## All-boss clock policy

At every boss checkpoint (300/600/900/1200 seconds, or 5/10/15/20 minutes), the visible run clock freezes. Wave selection, ordinary spawning, XP pickup and level progression do not advance while that boss is alive. The boss and existing active enemies continue on a separate encounter/wall clock; once a non-final boss is defeated, the visible clock resumes from the same checkpoint. The final boss has no resume step because it ends the model run.

- Source: user product decision captured 2026-09-10.
- Status: CANON product behavior in the model; runtime implementation is NOT_IMPLEMENTED.
- Model key: simulation_model.boss_clock_policy.
- Evidence: every one of the 30 deterministic model runs emits four pause events with run_clock_stop_seconds equal to defeat_time_run_clock_seconds; runtime trace is still absent.

## Profile/build inputs

| Profile | Meta ranks | Damage multiplier | Cooldown multiplier | Landed-hit probability | Build status |
|---|---|---:|---:|---:|---|
| fresh | all 0 | 1.00 | 1.00 | 0.002 | PROPOSED model profile |
| moderate | V3/P3/A2/F2/M2/D2 | 1.06 | 0.97 | 0.0015 | PROPOSED model profile |
| max_m1 | all 10 | 1.20 | 0.85 | 0.001 | PROPOSED model profile |

Lin Yue uses architecture IDs hero_lin_yue + weapon_jade_talismans + passive_jade_focus + synergy_heavenly_seals. Soyeon Han uses hero_seoyeon_han + weapon_moon_blade + passive_wind_of_travel + synergy_moon_dance. Weapon/passive numeric values, crit pipeline, and synergy damage multipliers are PROPOSED because B1/architecture provide IDs and requirements but not tuning values.

## Model-only result summary

The five-seed result is in BALANCE_SIMULATION_REPORT.md. Ordinary and elite rows are not blanket passes: mean focused TTK is usually inside the target, while some p95 values and hero/profile combinations remain outside it. Boss results are reported per checkpoint and per profile. This is evidence about the proposed equations and inputs only, not runtime combat.

## Remaining combat blockers

- absolute values need Product/Balance approval;
- contact/telegraph positions are not simulated spatially;
- incoming hit probability is a mean-field proposal, not collision evidence;
- synergy attribution is computed by formula but not by runtime event trace;
- Android performance and same-frame event ordering are unverified.
