# Balance Audit

Status: PARTIAL / SIMULATED_MODEL_ONLY

## Audit snapshot

- Repository: xxiamadelxx-blip/mac.
- Live main HEAD verified immediately before this audit refresh: 03d40129d4e31126b1707c6aac3eb51f735dae51.
- B1 source: docs/BALANCE_ECONOMY_SPEC.md.
- B1 source revision: 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687.
- Architecture contract revision: 2f889f876f2b8aa286523d234786addf0b9b245e.
- Balance model commit: 3a40341a71b910f12bea1834c0758a74b6059bdc.
- Simulator commit: 34d62768787b39191151d6e9f62b957db0e9c1e8.
- Contract validator commit: 83df99e44c40839724b57563fee90b3032eed87f.
- Simulation report commit: 03d40129d4e31126b1707c6aac3eb51f735dae51.
- Seeds: 101, 202, 303, 404, 505.
- Model runs: 30, covering fresh/moderate/max_m1 × Lin Yue/Soyeon Han.
- Repeated full-run SHA-256: 52b32ebff019e312a23d2153439ec0ebbfb7fdf3b48acb568efb16e922a78242.
- Contract validator: PASS.
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
- 30/30 runs survive the model, and duplicate reward grants are rejected.
- Four boss encounters per run are resolved on a separate encounter clock; 120/120 boss pause events satisfy the frozen run/wave/XP/spawn assertions.
- Results include level checkpoints at 2/5/10/15/20 minutes, ordinary/elite TTK, incoming damage, HP risk, active-cap occupancy, boss outcomes, reward balances, synergy, fallback, artifact offers and idempotency.
- Final boss chest remains absent in all model runs, and first-clear artifact delivery remains a separate three-choice offer.

## Remaining blockers

- Godot runtime integration and event trace for the all-boss clock rule.
- Approval/promotion of PROPOSED/DERIVED combat, pickup, profile and build values.
- Spatial movement, contact, telegraphs, safe boss spawn and same-frame ordering.
- Active-cap product/performance decision.
- Profile/reference interpretation for boss TTK targets.
- First-clear artifact selection, refresh, duplicate/stacking and persistence.
- Android performance and readability evidence.
- Full build/evolution catalog and real offer UI.

## Exact next implementation slice

Runtime/Architecture must:

1. Load BALANCE_MODEL.json through the versioned Content Registry.
2. Add RunSession visible run-clock state, separate encounter-clock state, current boss checkpoint, pause/resume trace and terminal outcome.
3. Gate wave selection, active-cap accounting, XP drops/pickup and level progression on visible run time; keep combat/event ordering on the encounter clock while every boss is alive.
4. Implement BossDirector interruption/recovery, contact cooldown, telegraph metadata, safe spawn and no same-frame damage stacking.
5. Implement weapon/passive/synergy IDs, fallback resolution, reward ledger keys, final NO_CHEST settlement and the separate first-clear three-card offer with replay-safe selection.
6. Emit runtime traces for seeds 101/202/303/404/505 and compare them with the model report.

Until that slice exists, the correct status is PARTIAL / SIMULATED_MODEL_ONLY, not VERIFIED.
