# Balance Acceptance Matrix — 30-minute extension

Status: `PARTIAL`; model-only evidence is not runtime verification.

| Acceptance item | Evidence in this slice | Status | Remaining blocker |
|---|---|---|---|
| 30:00 run duration | `simulation_model.main_run_duration_seconds = 1800` with formula `30×60` | MODEL PASS | B1/architecture still say 1200 |
| Six main checkpoints | 05/10/15/20/25/30 schedule in one model | PROPOSED | two new boss IDs and 20:00 reclassification need registry sync |
| Five mini-bosses | 07:30/12:30/17:30/22:30/27:30 schedule | MODEL PASS | only two content IDs exist; three IDs/skills are pending |
| Main-boss timer freeze | six main clock events report no visible/wave/XP advancement | MODEL PASS | runtime `BossDirector/RunSession` not connected |
| Mini-boss timer advance | five mini events report visible timer/wave/XP advancement | MODEL PASS | architecture lacks `MINI_BOSS` clock contract |
| Low→peak→siege waves | five linear ramp cycles; independent checker verified monotonic density and peak siege | MODEL PASS | runtime wave director not connected |
| Elite variations are finite | five post-mini packs, no permanent composition weight | MODEL PASS | B1 cadence, variant IDs/stats and artifact semantics pending |
| XP and levels | 30 deterministic runs report levels at 02/05/10/15/20/25/30 | MODEL PASS | 20–30 XP pickup capacities are proposed |
| Ordinary/elite TTK | model reports ordinary, existing elite and elite-variant TTK | MODEL PARTIAL | elite variant range is proposed; no gameplay trace |
| Main/mini boss TTK | model reports every resolved encounter | MODEL PARTIAL | new boss stats and mini skill kits are proposed |
| Incoming damage/risk | total damage, peak incoming DPS, min HP and single-hit bound are reported | MODEL PASS | hit probability and telegraph assumptions need runtime evidence |
| Rewards | main/mini wallet rows, boss chest, elite offer and final no-chest path are modelled | MODEL PARTIAL | proposed reward values and content chest contract pending |
| Idempotency | wallet, chest and elite-offer duplicate attempts pass for all 30 model runs | MODEL PASS | RewardLedger/ArtifactOffer runtime not implemented |
| Determinism | independent checker: repeat hash `a2d4b1258c869da4f22a852e46a73166d419e6b59ed8bb33771971cbaa9f505a` | PASS | model only |
| Runtime 30-minute run | no Godot execution in this slice | BLOCKED | runtime implementation and trace required |
| Android occupancy/FPS | max proposed occupancy reaches 400 | BLOCKED | device profiling and active-cap decision required |

Profile outcome across seeds 101/202/303/404/505 and both heroes: fresh 5/10 survived and 1/10 completed in the target final-boss window; moderate 9/10 survived and completed; max M1 10/10 survived and completed. These are tuning evidence, not a VERIFIED claim.
