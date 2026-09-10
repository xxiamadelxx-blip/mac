<!-- LIVE-AGENT-SYNC: read docs/AGENT_SYNC_STATE.md at current main before using this file -->
> **Live coordination pointer:** continuation work is routed through [`docs/AGENT_SYNC_STATE.md`](../../AGENT_SYNC_STATE.md). Legacy 20-minute/4-boss passages below are historical until reconciled.

# R3 Runtime Handoff

## Status

`RUNTIME_VERIFICATION_BLOCKED`

R2/R3 runtime seams and the R3 acceptance test are published, but the Godot
runner did not allocate a runner. This handoff is not a runtime-verification
claim and contains no fabricated trace.

## Current source

- Repository: `xxiamadelxx-blip/mac`
- Branch: `main`
- HEAD: `8efdd61e1017748584b6c1bb8775898c6f289cca`
- Previous implementation commit: `6491de629527b541f0a3792aa5fd6a48b62cc62e`
- Godot image requested by workflow: `barichello/godot-ci:4.7.2`

## Implemented runtime scope

- `WaveDirector` projects Registry wave bands and main/mini boss pressure policy.
- `BossDirector` supports Registry-backed main and optional mini-boss encounters.
- `SimulationClock` has separate main-boss freeze and mini-boss advancing modes.
- `RewardLedger` uses replay-safe run/scope/checkpoint/reward keys.
- `ArtifactOfferSystem` creates three typed cards for `ELITE_PACK` and `FIRST_CLEAR_REWARD`.
- Artifact refresh and selection are idempotent; stale revisions are rejected.
- Artifacts are stored as unbounded-within-run effects and do not mutate weapon/passive slots.
- `r3_runtime_test.gd` covers the five required seeds and final/no-boss-chest separation.

## Verification attempted

Workflow: [R3 Runtime Verification](https://github.com/xxiamadelxx-blip/mac/actions/runs/34490450692)

Job: `102915512575`

Observed result:

- conclusion: `failure`;
- status: `completed`;
- runner steps: `null`;
- logs URL: `null`;
- Godot stdout: unavailable;
- Godot exit codes: unavailable;
- `R3_RUNTIME_TEST {"ok":true}`: not observed;
- `R3_RUNTIME_TRACE {"ok":true}`: not observed.

The same push also failed before steps for the existing R1 verification and
GitHub-to-GitLab mirror workflows. The precise observed blocker is failure
before runner/step allocation; there is no Godot failure evidence to classify.

## Content synchronization boundary

The live B1 Registry still reports the pre-sync content boundary: 20-minute
duration, four main checkpoints and no mini-boss records. Runtime reads optional
future main/mini/elite records from the Registry and does not invent the missing
six-main/five-mini roster or numeric cadence.

The next verification attempt must run the workflow after a functional runner
is available and must capture the actual stdout and exit codes. Only then may
this status become `RUNTIME_VERIFIED`.
