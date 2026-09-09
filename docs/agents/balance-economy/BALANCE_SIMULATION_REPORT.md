# Balance Simulation Report

Status: SIMULATED_TEST_PLACEHOLDER

This report records a deterministic contract simulation, not a playable-run result. The source baseline is docs/BALANCE_ECONOMY_SPEC.md at revision 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687. The simulator is docs/agents/balance-economy/balance_simulator.py. The simulator commit used for this report is 77a6f75417bc3531c743aa648ecd74998ad76652.

## What was executed

Command:

    python3 docs/agents/balance-economy/balance_simulator.py --seed 20260909 --json

The command exits with code 0 after self-checks. Two identical runs with seed 20260909 produced the same SHA-256:

    95c09b1e184f297e3de5cb295e4e2a0b63c15056ef54c6536ee21016e68caae9

The run status is SIMULATED_TEST_PLACEHOLDER. All test fixture values below are marked TEST_PLACEHOLDER by the simulator and are not production inputs.

## Canonical arithmetic checks

### Wave schedule

| Band | Duration (s) | Spawn budget/s | Theoretical spawn opportunity |
|---|---:|---:|---:|
| wave_00_02 | 120 | 6 | 720 |
| wave_02_05 | 180 | 10 | 1800 |
| wave_05_10 | 300 | 15 | 4500 |
| wave_10_15 | 300 | 22 | 6600 |
| wave_15_20 | 300 | 30 | 9000 ||

Total nominal spawn opportunity: 22620. This is DERIVED arithmetic before active-cap limits, boss interruption, actual defeat/despawn behavior, and safe mode. It is not a kill-count prediction.

The conditional single-recovery projection is:

- reduction window: 8 seconds;
- start factor: 0.70;
- end factor: 1.00;
- recovery duration: 20 seconds;
- linear average: 0.85;
- equivalent nominal spawn-seconds: 17.

The interpolation and overlap policy remain pending.

### XP formula

The simulator evaluates the CANON formula:

    XP_to_next(L) = round(30 + 12 × (L - 1) + 3 × (L - 1)^1.35)

The first twelve derived thresholds are:

| Current level | XP to next | Cumulative XP |
|---:|---:|---:|
| 1 | 30 | 30 |
| 2 | 45 | 75 |
| 3 | 62 | 137 |
| 4 | 79 | 216 |
| 5 | 97 | 313 |
| 6 | 116 | 429 |
| 7 | 136 | 565 |
| 8 | 155 | 720 |
| 9 | 176 | 896 |
| 10 | 196 | 1092 |
| 11 | 217 | 1309 |
| 12 | 238 | 1547 ||

The XP drop set checked is: 1, 5, 15, 40, 80, 250.

### Reward totals

| Scenario | Gold | Moon Seals | Boss Essence |
|---|---:|---:|---:|
| Checkpoint sum | 425 | 120 | 5 |
| Full first clear | 725 | 300 | 6 |
| Repeat clear | 425 | 120 | 5 |

These match the CANON totals in B1 section 7.

### Meta rank costs

The simulator evaluates cost(r) = round(100 × 1.45^r). Costs for current ranks 0–9 are:

100, 145, 210, 305, 442, 641, 929, 1,348, 1,954, 2,833.

These are DERIVED from the CANON formula, not a new economy decision.

## Test-placeholder profile projection

B1 does not define fresh, moderate, or max_m1 numeric upgrade profiles. The following rows only exercise the report and profile plumbing with explicit TEST_PLACEHOLDER XP rates.

| Profile | XP/s | First level (s) | Level at 10 min | XP at 10 min | Status |
|---|---:|---:|---:|---:|---|
| fresh | 1 | 30 | 8 | 600 | TEST_PLACEHOLDER |
| max_m1 | 1.4 | 21.429 | 9 | 840 | TEST_PLACEHOLDER |
| moderate | 1.2 | 25 | 9 | 720 | TEST_PLACEHOLDER ||

Do not interpret these rows as progression evidence. The production profile definitions remain PENDING_PRODUCT_DECISION and the level timing target remains NOT_IMPLEMENTED in runtime.

## TTK equation harness

B1 defines target ranges but does not provide absolute enemy base HP, base damage, base speed, weapon cadence, mitigation, or crit rules. The simulator therefore uses a deliberately isolated TEST_PLACEHOLDER fixture to check the equation and range guard only.

| Encounter | Effective HP | Sustained DPS | Fixture TTK (s) | Target range | Guard |
|---|---:|---:|---:|---:|---|
| ordinary | 100 | 60 | 1.667 | 0.5–2.5 | PASS (fixture only) |
| elite | 1000 | 50 | 20 | 10–25 | PASS (fixture only) |
| first_slice_boss | 3000 | 50 | 60 | 45–80 | PASS (fixture only) |
| final_boss | 5250 | 50 | 105 | 90–120 | PASS (fixture only) ||

Every guard passes for the fixture. This is not evidence that any enemy, hero, boss, or build meets the target in runtime.

## Reward idempotency harness

The harness sends two checkpoint grants twice with the same test key shape:

- attempted grants: 4;
- accepted grants: 2;
- stored grants: 2;
- duplicate attempts rejected: true.

The key shape is a test fixture: run ID, checkpoint ID, outcome, and source-table revision. The production ledger transaction/idempotency schema is still PENDING_PRODUCT_DECISION and NOT_IMPLEMENTED.

## Evidence boundary

Verified by this report:

- the B1 wave arithmetic is reproducible;
- the B1 XP formula and derived thresholds are reproducible;
- the B1 checkpoint/clear totals are reproducible;
- the meta-cost formula is reproducible;
- the isolated duplicate-grant harness rejects duplicate attempts;
- the simulator output is deterministic for a fixed seed.

Not verified:

- production wave spawning or active-cap behavior;
- ordinary/elite/boss TTK;
- hero/build routes or synergy power ceiling;
- boss telegraph and reaction timing;
- reward wallet persistence or reconnect/replay behavior;
- Android performance or 30 FPS target;
- readability of combat, XP, aftermath, or results;
- playability or overall balance.

