<!-- LIVE-AGENT-SYNC: read docs/AGENT_SYNC_STATE.md at current main before using this file -->
> **Live coordination pointer:** continuation work is routed through [`docs/AGENT_SYNC_STATE.md`](../../AGENT_SYNC_STATE.md). Legacy 20-minute/4-boss passages below are historical until reconciled.

# Balance Audit

Status: `PARTIAL / SIMULATED_MODEL_ONLY`

## Audit snapshot

- Repository: `xxiamadelxx-blip/mac`.
- Live main HEAD immediately before this audit write: `4ce6122ac19bf1f8e3bc84bf8afb192a55145ba9`.
- Live architecture contract revision: `bd1d4d44f9c0a525b26ac136d98ace3cf76a3d00`.
- Architecture state: `VERIFIED_ARCHITECTURE`, duration 1800s, six main checkpoint records, three intermediate records, three stable enemy-variant IDs; runtime is still not implemented.
- Balance model: `docs/agents/balance-economy/BALANCE_MODEL.json`, status `PARTIAL`; simulation status `PROPOSED_MODEL_ONLY`.
- Runtime status: `NOT_IMPLEMENTED`.
- Architecture/content registries were read but not modified by this balance slice.

This slice continues from the prior balance work. It updates the existing model, simulator, validator and reports for the requested 30-minute run, new main/mini encounters and finite elite variations. It does not recreate a second tuning source.

## What is implemented in this slice

- A single JSON authority for 1800 visible-run seconds, six main bosses and five model mini-boss slots.
- Current architecture IDs are synchronized: `boss_extension_slot_04`, `boss_extension_slot_05`, `boss_black_moon_empress`, `miniboss_extension_slot_03`, and the three architecture variant IDs.
- Main-boss model clock freeze and mini-boss model clock advance are explicit and emitted per encounter.
- Two proposed 20:00–30:00 wave bands with source/formula/status provenance.
- Five main-boss low→peak→siege ramp cycles; the architecture rule for intermediate/mini relief is recorded as an unresolved alignment item.
- Finite elite-variation packs after model mini-bosses; variants are selected from JSON registry IDs, not hardcoded in Python.
- Main/mini TTK, incoming damage/risk, active occupancy, XP/levels, rewards, boss chests, artifact offers and idempotency are emitted by the deterministic simulator.
- Validator passes against the fresh live architecture contract and the independent checker runs two identical 30-run batches.

## Model-only evidence

Seed set: 101, 202, 303, 404, 505; two heroes; fresh/moderate/max M1 profiles; 30 runs.

- Repeat hash: `2d901903a59cc88926b4413c5caa71cb92e2321cd3b446e93e6ee14db5f43d92`.
- Survived: 24/30.
- Completed inside the final-boss target window: 21/30.
- Fresh: 5/10 survived, 2/10 completed.
- Moderate: 9/10 survived and completed.
- Max M1: 10/10 survived and completed.
- Independent check: `INDEPENDENT_30M_CHECK=PASS`.
- Validator: `BALANCE_CONTRACT_CHECK=PASS` against architecture revision `bd1d4d44…`.
- Wallet, boss-chest and elite-offer duplicate attempts: PASS in the model.
- Runtime execution: none; Android FPS/collision/telegraph evidence: none.

Full levels, TTK, incoming damage, occupancy and reward values are in `BALANCE_SIMULATION_REPORT.md`; wave semantics and stable-ID mapping are in `BALANCE_WAVE_TABLE.md`; acceptance statuses are in `BALANCE_ACCEPTANCE_MATRIX.md`.

## Provenance boundary

Existing B1 values remain CANON. The following are not silently promoted:

- B1 extension duration/XP/wave/reward numbers beyond the currently synced architecture duration;
- two new main-boss numeric kits and all five mini-boss numeric kits;
- the five-vs-three mini schedule reconciliation;
- elite overlay multipliers, pack size/cadence and artifact-offer effects;
- extension wallet rewards and fallback/stacking behavior;
- main-boss freeze versus the live architecture clock contract.

Each proposed input is stored in `BALANCE_MODEL.json` with `source`, `derived_formula`, `rationale` and `status`.

## Current blockers

1. Clock contract conflict: live architecture says elapsed time advances through every boss; the balance/product rule requires main-boss visible/wave/XP/spawn freeze.
2. Schedule conflict: the model has five mini-bosses, while the live architecture registry currently has three intermediate slots at 450/750/1350. The extra 1050/1650 slots and their content records are pending.
3. Content join is incomplete for new main bosses, pending intermediate/minis and variant numeric/visual records.
4. B1/Product must approve or replace proposed 20:00–30:00 wave anchors, XP capacities, boss/mini/elite combat values and extension rewards.
5. Runtime must consume this model, implement the selected clock/schedule policy and emit timer, wave, XP, combat, reward and idempotency traces.
6. Android occupancy/FPS must be profiled at the proposed cap of 400.
7. Product must set the fresh-profile completion target; the current model completes 2/10 fresh runs.

## Next implementation slice

Architecture/Runtime: resolve the main-boss clock conflict and choose/register the five-mini schedule (or explicitly change the product target to three intermediate slots). Then wire `RunSession`, `WaveDirector/BossDirector`, `CombatSystem`, `ProgressionSystem`, `RewardLedger` and `ArtifactOfferSystem` to `BALANCE_MODEL.json`. Re-run the exact seed set with runtime traces and Android profiling. Do not mark `DONE` or `VERIFIED` until those traces exist.