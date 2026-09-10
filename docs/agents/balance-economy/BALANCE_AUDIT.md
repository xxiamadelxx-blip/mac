# Balance Audit

Status: PARTIAL / SIMULATED_MODEL_ONLY

## Audit snapshot

- Repository: xxiamadelxx-blip/mac.
- Live main HEAD after the synchronized post-boss wave slice: 1c426c5a7dba79683990b830dace4c7bfba8771c.
- B1 source: docs/BALANCE_ECONOMY_SPEC.md.
- B1 source revision: 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687.
- Architecture contract revision: 2f889f876f2b8aa286523d234786addf0b9b245e.
- Balance model commit: 89c23c7dc80e29463d3dcc2d283e6c7710a5ac65.
- Simulator commit: 607fb24742f0235e1b048bc4a88f3a4a7f80d3d3.
- Contract validator commit: 8ddffa562ec2bacec235aea4b70eec4299c5d119.
- Simulation report commit: 1c426c5a7dba79683990b830dace4c7bfba8771c.
- Seeds: 101, 202, 303, 404, 505.
- Model runs: 30, covering fresh/moderate/max_m1 × Lin Yue/Soyeon Han.
- Repeated full-matrix SHA-256: 6c1e1ea7df9393bc2bc2fc94c8049086d291784a93acc145f8e518d664f9d7cb.
- Contract validator: PASS; post-boss cycle mapping, reset factor, siege window and ramp window also pass.
- Runtime status: NOT_IMPLEMENTED.
- Final status: model evidence is repeatable; Godot balance remains unverified.

The previous stale claim that no simulator existed is no longer true. The current simulator reads one BALANCE_MODEL.json and executes a deterministic 20-minute model. It does not execute the Godot runtime.

## Current clock rule

The user decision applies to every boss, not only the final boss:

- at 300/600/900/1200 visible run-clock seconds, the run clock stops while the corresponding boss is alive;
- ordinary wave selection, spawning, XP pickup and level progression are frozen;
- the boss and existing active enemies use a separate encounter/wall clock;
- after a non-final boss defeat, the visible clock resumes from the same checkpoint;
- the final boss has no resume step because it resolves the model run.

All 30 runs produced four boss clock events. In every event, run-clock spawn and defeat checkpoints were equal, run_clock_advanced_during_encounter was false, and wave_xp_spawn_clock_advanced_during_encounter was false. This is model evidence only; no runtime trace exists.

## Completed in this slice

1. Replaced the misleading final-only clock field with simulation_model.boss_clock_policy and bound it to all four boss checkpoints.
2. Replaced the final-only post-run simulation branch with a two-clock loop. Wall time continues for combat and TTK; visible run time drives waves, active cap and XP.
3. Added per-boss pause/resume evidence, encounter duration, run-clock defeat time, wall-clock defeat time and final-run outcome fields.
4. Extended the contract validator to require ALL_BOSS_CHECKPOINTS and the exact 300/600/900/1200 list.
5. Synchronized combat, acceptance, decisions, simulation report and audit documents.
6. Repeated the full 30-run output twice and confirmed identical SHA-256.
7. Preserved explicit source/derived/proposed/status provenance. No missing B1 value was silently changed to CANON.
8. Rechecked the live runtime seam after the model slice: the architecture contract is still DRAFT/runtime_implemented=false and arena_controller.gd is still preview-only, so no fake runtime integration was added.

## Findings

### F-01 — Critical — runtime balance seam is still absent

Evidence: the architecture contract remains DRAFT with runtime_implemented=false; no implemented RunSession/WaveDirector/BossDirector/RewardLedger consumer reads BALANCE_MODEL.json.

Impact: model evidence cannot prove that the game applies the same values, event ordering, cap, XP pickup, telegraph, pause or reward behavior.

Confidence: High.

Next owner: Architecture + Runtime implementation.

### F-02 — Critical — proposed absolute combat values are not runtime values

Evidence: enemy/boss stats, weapon/passive/synergy effects, pickup cadence and profile hit probabilities are explicitly PROPOSED or DERIVED because B1 does not define them.

Impact: TTK and incoming-risk results are design evidence, not player-facing balance evidence.

Confidence: High.

Next owner: Balance/Product approval, then Combat Runtime.

### F-03 — Watch — active-cap saturation is a model risk

Evidence: all 30 runs reach active cap 280; cap occupancy is approximately 1105.7–1140.0 visible-clock seconds and suppressed spawn attempts are approximately 19,468–20,276 per profile/hero slice.

Impact: the proposed spawn/combat combination may create a continuously saturated horde and may fail readability or performance.

Confidence: Medium; model-only finding.

Next owner: Balance + Runtime performance.

### F-04 — Watch — boss target windows are not uniform across proposed routes

Evidence: moderate Lin Yue passes all four target windows; max M1 Soyeon passes all four; fresh Lin Yue final is 120.5 s, moderate Soyeon final is 123.5 s, fresh Soyeon final is 134.25 s, and max M1 Lin Yue final is 85.25 s.

Impact: one proposed curve does not satisfy every profile/hero route under the current target interpretation.

Confidence: High.

Next owner: Balance/Product decision on reference profile and target-window policy.

### F-05 — Watch — artifact-offer boundary remains pending

Evidence: 15/30 model runs create a separate three-choice FIRST_CLEAR_REWARD offer after finalization. Effect values, refresh, duplicate/stacking and persistence remain pending.

Impact: result UI, artifact choice persistence and Codex/meta-progression can diverge.

Confidence: High.

Next owner: Product + Architecture.

### F-06 — Watch — performance and spatial readability are unverified

Evidence: no selected Android target, Godot runtime load trace, frame-time capture, collision trace, safe-spawn test or visual telegraph QA run.

Impact: cannot establish 30 FPS, safe boss spawn, readable aftermath or no untelegraphed hit in the real game.

Confidence: High.

Next owner: Runtime + Performance + Visual QA.

## What is now verified at model level

- B1 source revision and architecture revision are recorded.
- BALANCE_MODEL.json parses and carries field-level provenance.
- Simulator reads one model JSON instead of duplicating tuning values in Python.
- Contract validator passes stable IDs, wave IDs, build IDs, final reward policy and all-boss clock policy.
- Five independent seeds and two repeated full runs are deterministic.
- 29/30 runs survive the model; one fresh Lin Yue seed dies at wall 1,398.5 s / visible run clock 1,179.0 s before the final boss; duplicate reward grants are rejected in 30/30 runs.
- Four boss encounters per run are resolved on a separate encounter clock; 120/120 boss pause events satisfy the frozen run/wave/XP/spawn assertions.
- Three post-boss cycles per run are monotonic in the model: entry budgets/caps 8/64, 12/104, 17.6/160; peak/siege budgets/caps 15/130, 22/200, 30/280; the 28-second recovery and 60-second siege boundaries are explicit.
- Results include level checkpoints at 2/5/10/15/20 minutes, ordinary/elite TTK, incoming damage, HP risk, active-cap occupancy, boss outcomes, reward balances, synergy, fallback, artifact offers and idempotency.
- Final boss chest remains absent in all model runs, and first-clear artifact delivery remains a separate three-choice offer.

### F-07 — Watch — post-boss curve is model-complete but numerically proposed

Evidence: `simulation_model.boss_wave_ramp` defines three non-final cycles with a 28-second recovery, 212-second linear ramp and 60-second peak siege. The reset factor is 0.80 and remains PROPOSED because B1 does not specify the exact curve. All 30 model runs pass 3/3 monotonic/peak-siege assertions.

Impact: product/B1 approval is still required before treating 0.80 and 60 seconds as canonical; runtime must consume the same phase data to prove the player sees the intended breathing window.

Confidence: High for the model evidence; low for player-facing/runtime behavior.

Next owner: Balance + Product, then Runtime.

## Remaining blockers

- Godot runtime integration and event trace for the all-boss clock rule plus POST_BOSS_RECOVERY/RAMP/SIEGE density phases.
- Approval/promotion of PROPOSED/DERIVED combat, pickup, profile and build values.
- Spatial movement, contact, telegraphs, safe boss spawn and same-frame ordering.
- Active-cap product/performance decision and approval of the post-boss reset/siege parameters.
- Profile/reference interpretation for boss TTK targets.
- First-clear artifact selection, refresh, duplicate/stacking and persistence.
- Android performance and readability evidence.
- Full build/evolution catalog and real offer UI.

## Exact next implementation slice

Runtime/Architecture must:

1. Load BALANCE_MODEL.json through the versioned Content Registry.
2. Add RunSession visible run-clock state, separate encounter-clock state, current boss checkpoint, pause/resume trace and terminal outcome.
3. Gate wave selection, active-cap accounting, XP drops/pickup and level progression on visible run time; keep combat/event ordering on the encounter clock while every boss is alive.
4. Implement BossDirector interruption/recovery and consume `boss_wave_ramp`: POST_BOSS_RECOVERY → RAMP → SIEGE, contact cooldown, telegraph metadata, safe spawn and no same-frame damage stacking.
5. Emit runtime traces for the three post-boss density cycles and compare their budget/cap/phase boundaries with the model report.
6. Implement weapon/passive/synergy IDs, fallback resolution, reward ledger keys, final NO_CHEST settlement and the separate first-clear three-card offer with replay-safe selection.
7. Emit runtime traces for seeds 101/202/303/404/505 and compare them with the model report.

Until that slice exists, the correct status is PARTIAL / SIMULATED_MODEL_ONLY, not VERIFIED.
