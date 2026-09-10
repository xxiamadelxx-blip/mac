# Balance Acceptance Matrix — 30-minute extension

Status: `PARTIAL`; the model and independent checker pass, but this is not runtime verification.

| Acceptance item | Evidence in this slice | Status | Remaining blocker |
|---|---|---|---|
| 30:00 run duration | `simulation_model.main_run_duration_seconds = 1800`; live architecture revision `bd1d4d44…` also declares 1800 | MODEL PASS | B1 still has no approved extension numeric profiles |
| Six main checkpoints | 05/10/15/20/25/30 schedule; architecture registry contains six records, with slots 04/05 pending content | MODEL PASS / PARTIAL JOIN | content registry and runtime join for new slots |
| Five mini-bosses | 07:30/12:30/17:30/22:30/27:30 model schedule; 22:30 uses architecture ID `miniboss_extension_slot_03` | MODEL PASS / ARCH BLOCKED | architecture currently registers only three intermediate slots; two extra IDs/kits are pending |
| Main-boss timer freeze | six model main events report no visible/wave/XP/spawn advancement | MODEL PASS / CONTRACT CONFLICT | live architecture clock policy currently says elapsed time advances through bosses |
| Mini-boss timer advance | five model mini events report visible timer/wave/XP advancement | MODEL PASS | runtime policy is not defined for all five slots |
| Low→peak→siege waves | five main-boss cycles: recovery, linear ramp, then peak siege; independent checker verified monotonic density | MODEL PASS FOR MAIN CYCLES | architecture rule covers intermediate encounters too; mini-boss relief is not runtime-proven |
| Elite variations | three stable architecture variant IDs, finite one-pack-per-mini policy, no permanent wave member | MODEL PASS / NUMBERS PENDING | B1 numeric overrides, cadence and visual records |
| XP and levels | 30 deterministic runs report levels at 02/05/10/15/20/25/30 | MODEL PASS | 20–30 XP pickup capacities remain proposed |
| Ordinary/elite TTK | ordinary, existing elite and elite-variant TTK are emitted | MODEL PARTIAL | elite overlay is proposed; no gameplay trace |
| Main/mini boss TTK | all resolved main and mini encounters emit TTK and target pass | MODEL PARTIAL | new boss stats and mini kits are not canon |
| Incoming damage/risk | total damage, peak DPS, min HP and single-hit bound are emitted | MODEL PASS | hit probability/telegraph assumptions need runtime evidence |
| Rewards | main/mini wallet rows, boss chest, elite offer and final no-chest path are modelled | MODEL PARTIAL | extension rewards, fallback and artifact stacking remain proposed |
| Idempotency | wallet, chest and elite-offer duplicate attempts pass in all 30 model runs | MODEL PASS | RewardLedger/ArtifactOffer runtime is not implemented |
| Determinism | independent checker repeat hash `2d901903a59cc88926b4413c5caa71cb92e2321cd3b446e93e6ee14db5f43d92` | PASS | model only |
| Runtime 30-minute run | no Godot runtime execution in this slice | BLOCKED | runtime implementation and trace required |
| Android occupancy/FPS | model cap is 400; occupancy reaches the cap in late profiles | BLOCKED | device profiling and active-cap decision required |

Across seeds 101/202/303/404/505 and both heroes: fresh 5/10 survived and 2/10 completed; moderate 9/10 survived and 9/10 completed; max M1 10/10 survived and 10/10 completed. These are model-only tuning results, not a VERIFIED claim.