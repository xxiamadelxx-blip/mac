# Balance Audit

Status: `PARTIAL / SIMULATED_MODEL_ONLY`

## Audit snapshot

- Repository: `xxiamadelxx-blip/mac`.
- Live main HEAD at audit write: `52e2ec4d42b5c64eb303d0501a37f8fdd7d284ec`.
- Balance model: `docs/agents/balance-economy/BALANCE_MODEL.json`.
- Model status: `PARTIAL`; simulation status: `PROPOSED_MODEL_ONLY`.
- Runtime status: `NOT_IMPLEMENTED`.
- Runtime/architecture and content registries were read but not modified by this balance slice.

This slice continues from the previous balance work. It does not recreate the old documents: it extends the single data model and the existing simulator to the requested 30-minute schedule.

## What is implemented in this slice

- 1800-second model schedule with six main-boss slots at 05:00/10:00/15:00/20:00/25:00/30:00.
- Five mini-boss slots at 07:30/12:30/17:30/22:30/27:30.
- Separate clock policies: main bosses freeze visible run/wave/XP/spawn clocks; mini-bosses keep them advancing.
- Two proposed 20:00–30:00 wave bands with explicit source/formula/status fields.
- Five post-main-boss low→peak→siege ramp cycles.
- Finite elite-variation packs after mini-bosses; no permanent elite composition.
- Main/mini encounter TTK, incoming damage/risk, active occupancy, XP/levels, rewards, boss chests, elite offers and idempotency are emitted by the deterministic simulator.
- Validator accepts canonical legacy IDs plus explicitly proposed extension bands/schedule.
- Independent checker runs the simulator twice and validates the public result contract.

## Model-only evidence

Seed set: 101, 202, 303, 404, 505; two heroes; fresh/moderate/max M1 profiles; 30 runs.

- Repeat hash: `a2d4b1258c869da4f22a852e46a73166d419e6b59ed8bb33771971cbaa9f505a`.
- Survived: 24/30.
- Completed inside the final-boss target window: 20/30.
- Fresh: 5/10 survived, 1/10 completed.
- Moderate: 9/10 survived and completed.
- Max M1: 10/10 survived and completed.
- Independent check: `INDEPENDENT_30M_CHECK=PASS`.
- Wallet, boss-chest and elite-offer duplicate attempts: PASS in the model.
- Runtime execution: none; Android FPS/collision/telegraph evidence: none.

The full ranges and level/XP checkpoints are in `BALANCE_SIMULATION_REPORT.md`. Wave values and clock semantics are in `BALANCE_WAVE_TABLE.md`; acceptance statuses are in `BALANCE_ACCEPTANCE_MATRIX.md`.

## Provenance boundary

Existing B1 values remain CANON. The following are not silently promoted:

- 30-minute duration and 25:00/30:00 boss IDs;
- 20:00 reclassification of the old final-boss ID;
- three missing mini-boss IDs and all mini-boss absolute stats;
- 20:00–30:00 wave anchors and XP pickup rates;
- elite overlay multipliers, pack size/cadence and artifact-offer effects;
- extension wallet rewards and fallback/stacking behavior.

Each proposed input is stored in `BALANCE_MODEL.json` with `source`, `derived_formula`, `rationale` and `status`.

## Current blockers

1. Architecture still declares 1200 seconds, four main bosses and a different legacy clock contract; it must own the 1800-second `RunSession`/encounter update.
2. Content/Architecture must register the two new main bosses and three additional mini-bosses, including phase/telegraph/ID data.
3. B1/Product must approve the proposed 20–30 wave/XP/combat/reward values and define the fresh-profile completion target.
4. Runtime must consume this JSON, emit timer/wave/XP/combat/reward traces and prove idempotency.
5. Android occupancy/FPS must be profiled at the proposed cap of 400.

## Next implementation slice

Architecture/Runtime: sync the 30-minute schedule, `MAIN_BOSS` vs `MINI_BOSS` clock policy, five mini-boss slots, elite event state and idempotency fields into the runtime contract/registry. Then Balance reruns the same model against the new revisions. Do not mark `DONE` or `VERIFIED` until runtime evidence exists.
