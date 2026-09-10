# Balance Audit

Status: PARTIAL / SIMULATED_MODEL_ONLY

## Audit snapshot

- Repository: xxiamadelxx-blip/mac
- Live main HEAD verified immediately before this final clock/provenance refresh: ca093f9ccae18d4bd33aa7c5ffb28d435ae0d8e1
- Historical audit baseline before this implementation slice: ffc2e8d2f02d7a4d5c169151b2d59e5307ae5f2d
- B1 source: docs/BALANCE_ECONOMY_SPEC.md
- B1 source revision: 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687
- Architecture contract revision: 2f889f876f2b8aa286523d234786addf0b9b245e
- Balance model commit used for current v0.3 evidence: 0f9bbc72d2ceb77d5d1c51f5da74f0845705e2b7
- Historical model commit used for prior v0.2 evidence: 42966b44650ec63aead33d04cbe34ae1e9d57489
- Balance model repository-evidence refresh commit: 0536f182c1ae8876b9213e0c2fb761793e503a66
- Simulator commit used for current v0.3 evidence: 7fa90fce9f70c71ede3da54dc52c52a2fee5c5a6
- Current simulator path: docs/agents/balance-economy/balance_simulator.py
- Contract validator commit used for current v0.3 evidence: 87730846c35d74087c727cfaf0518c5914ec19d1
- Simulation status: SIMULATED_MODEL_ONLY
- Runtime status: NOT_IMPLEMENTED
- Final-boss clock policy: CANON model rule; main run clock freezes at 1200 seconds and boss resolves on a separate encounter clock

This update supersedes the previous stale statement that no simulator existed. The simulator now reads BALANCE_MODEL.json and runs a deterministic model, but it still does not execute Godot runtime behavior.

## Completed since the previous audit

1. Added explicit simulation_model input data to BALANCE_MODEL.json.
2. Added provenance for missing enemy/boss stats, composition weights, pickup cadence, combat formulas, profiles, builds, synergies, fallback, artifact-offer cadence/effects and first-clear artifact delivery.
3. Replaced the placeholder simulator with a 20-minute model covering waves, cap, XP, levels, damage, TTK, incoming risk, bosses, rewards, idempotency, builds, synergies, and fallback.
4. Ran 30 model runs across fresh, moderate, max_m1 × Lin Yue/Soyeon × seeds 101/202/303/404/505.
5. Repeated the current v0.3 full run twice; both JSON outputs produced SHA-256 6ace894187a6ca540561268123b3ec6abfc993570350a3aeef83686cf300bbce.
6. Synchronized the wave, combat, XP/reward, and acceptance documents with the model-only evidence and the current final-boss NO_CHEST architecture policy.
7. Reconciled model boss, wave-band and elite enemy IDs with the architecture registry; added a contract validator and confirmed PASS without changing tuning numbers.
8. Resolved the architecture SHA placeholder, added the final-boss clock freeze policy to the current v0.3 model/simulator, and confirmed the policy across 30 runs.

## Findings

### F-01 — Critical — runtime balance seam is still absent

Evidence: repository audit found no implemented RunSession/wave director/reward ledger consumer for this model. The architecture contract remains DRAFT with runtime_implemented=false.

Impact: the model cannot prove that the game applies the same values, event ordering, caps, telegraphs, XP pickup, or reward transactions.

Confidence: High.

Next owner: Architecture + Runtime implementation.

### F-02 — Critical — proposed absolute combat values are not runtime values

Evidence: BALANCE_MODEL.json records base enemy/boss stats and combat formulas as PROPOSED because B1 does not define them. The simulator exercises them, but Godot has no verified consumer.

Impact: TTK, incoming risk, and boss windows remain design evidence, not player-facing balance evidence.

Confidence: High.

Next owner: Balance/Product approval, then Combat Runtime.

### F-03 — Watch — model regression exists; runtime regression does not

Evidence: 30 deterministic runs pass shape checks, reward idempotency checks, and repeatability. No Godot event trace or runtime test suite exists.

Impact: changes to the game can diverge from the model without detection.

Confidence: High.

Next owner: Runtime + QA.

### F-04 — Watch — active-cap saturation is a model risk

Evidence: every profile/hero slice reaches cap 280; cap occupancy averages approximately 1,118–1,150 seconds; approximately 19,600–20,500 spawn attempts are suppressed.

Impact: the proposed spawn/combat combination may create a continuously saturated horde and may fail readability/performance even though the model remains deterministic.

Confidence: Medium; this is a model finding, not runtime evidence.

Next owner: Balance + Runtime performance.

### F-05 — Watch — some profile/hero boss targets still fail

Evidence: fresh and moderate Soyeon final-boss model TTK are above 120 seconds; max M1 Lin Yue final-boss TTK is below 90 seconds. Fresh/moderate Soyeon boss 3 can also exceed the first-slice upper bound.

Impact: the proposed model does not yet demonstrate a single boss curve that satisfies every profile/hero route.

Confidence: High.

Next owner: Balance/Product decision on whether target ranges apply to fresh, moderate, max, or a reference build.

### F-06 — Watch — first-clear artifact offer boundary requires product confirmation

Evidence: B1 defines a first-clear artifact reward value, while the architecture contract requires final checkpoint reward → run victory → no final boss chest. The corrected model represents this as a separate post-result `FIRST_CLEAR_REWARD` artifact offer with three choices, not as a boss chest or automatic artifact award attached directly to the result.

Impact: result UI, artifact choice persistence and Codex/meta-progression can diverge until the post-result offer, refresh, duplicate and persistence policies are approved.

Confidence: High.

Next owner: Product + Architecture.

### F-07 — Watch — performance and readability are unverified

Evidence: no selected Android target, no Godot runtime load trace, no frame-time capture, and no visual/telegraph QA run.

Impact: cannot establish 30 FPS, safe boss spawn, readable aftermath, or no untelegraphed hit in the real game.

Confidence: High.

Next owner: Runtime + Performance + Visual QA.

## What is now verified

- B1 source revision and live architecture revision are recorded.
- BALANCE_MODEL.json parses and contains explicit provenance.
- Simulator reads one model JSON instead of duplicating balance numbers in Python.
- Five independent seeds and two repeated full runs are deterministic.
- Canonical XP formula, wave arithmetic, reward totals, and idempotency key behavior are exercised.
- Model results include levels at 2/5/10/15/20, TTK, incoming damage, HP risk, occupancy, boss outcomes, reward balances, synergies, fallback outcomes, and artifact offers.
- The final-boss clock policy is emitted in every run result and passed independently by the contract validator.

## What remains blocked

- Godot runtime integration, event trace and final-boss clock enforcement.
- Approval/promotion of PROPOSED values to CANON.
- Spatial movement, contact, telegraphs, safe boss spawn, and same-frame ordering.
- Final boss profile target policy.
- First-clear artifact-offer presentation, refresh, selection and persistence policy.
- Android performance and readability evidence.
- Full build/evolution catalog and real offer UI.

## Next implementation slice

The next slice is not another document pass. Runtime/Architecture should:

1. Load the single balance model and architecture content registry through a versioned Content Registry.
2. Create RunSession fields for elapsed time, seeded wave selection, active cap, boss checkpoint state, XP drops/pickup queue, final-boss clock freeze and diagnostics.
3. Implement the combat event pipeline with contact cooldown, telegraph metadata, mitigation, crit attribution, and no same-frame stacking.
4. Implement the XP pickup queue and level-up offer resolver using the weapon/passive/synergy IDs and explicit fallback outcome.
5. Implement the reward ledger key format and final-boss NO_CHEST settlement, then open the separate post-result first-clear artifact offer and persist its choice idempotently.
6. Emit deterministic runtime traces for the same five seeds so the model can be compared against actual behavior.

Until that slice exists, the correct status remains PARTIAL, not VERIFIED.
