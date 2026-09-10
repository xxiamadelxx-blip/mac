# Balance Acceptance Matrix — REF-BALANCE-REF-01

Status: \`PARTIAL\`. The single-source 30-minute model, deterministic simulation and independent repeat check pass. Godot/Android runtime evidence does not exist.

| Requirement | Source | Model/runtime behavior | Check | Observed | Status | Next owner |
|---|---|---|---|---|---|---|
| Live B1 read | \`docs/BALANCE_ECONOMY_SPEC.md\` | B1 revision stored in JSON | fetch + SHA | \`6aa4ec96afc8a8c9e6a35c164c99e7d62910a687\` | PASS | Balance |
| 30:00 duration | user decision + architecture duration | 1800 visible-run seconds | validator + independent check | PASS | MODEL PASS | Architecture/Runtime |
| 7 wave bands | B1 + 30m extension proposal | one JSON \`wave_bands\` table | validator/simulator | 5 CANON B1 + 2 PROPOSED | MODEL PASS / PARTIAL | B1/Product |
| Main bosses | architecture + user 30m decision | 6 at 05/10/15/20/25/30 | independent check | 6 events | MODEL PASS / JOIN PENDING | Content/Architecture |
| Mini-bosses | sync lock + user decision | 5 at 07:30/12:30/17:30/22:30/27:30 | independent check | 5 events | MODEL PASS / REGISTRY BLOCKED | Content/Architecture |
| Main-boss freeze | user product rule | visible run/wave/XP/spawn clocks stop | independent event assertions | all 6 stop | MODEL PASS / CONTRACT CONFLICT | Architecture/Runtime |
| Mini-boss continuation | sync lock/model rule | visible clock, wave and XP continue | independent event assertions | all 5 continue | MODEL PASS / CONTRACT PENDING | Architecture/Runtime |
| Low→peak→siege after main | B1 interruption + user rule | suppression → recovery → linear ramp → 60s siege | monotonic/ramp assertions | PASS for 5 main cycles | MODEL PASS | Runtime |
| No immediate mini spike | model policy | mini uses current ramp; finite post-defeat pack only | model event output | no permanent roster mutation | DERIVED / MODEL PASS | Runtime |
| Active cap | B1 cap + model policy | discard overflow, no spawn debt | occupancy assertion | max 400, never exceeded | MODEL PASS / FPS BLOCKED | CI/Runtime |
| XP formula | B1 §6 | model reads formula from JSON | JSON/model replay | formula exact | MODEL PASS | Runtime |
| Levels 02/05/10/15/20/25/30 | B1 + proposed extension | model emits checkpoint levels | 30-run aggregation | fresh 2/5/9/13/17/20/24; moderate 2/6/10/13/17/21/24; max 2/6/10/14/18/22/26 | MODEL PASS / LATE PENDING | Balance/Product |
| Ordinary TTK | B1 target | data-driven combat formula | 30-run output | 0.50–1.25s | MODEL PASS | Runtime |
| Elite/boss/mini TTK | B1 target + proposed extension | output per event | 30-run output | ranges in simulation report | MODEL PARTIAL | Balance/Product |
| Incoming damage/risk | B1 15% single-hit bound | seeded landed-hit model | risk assertion | peak DPS and damage output; model bound PASS | SIMULATED | Runtime |
| Weapon/passive/synergy | B1 + content IDs | one model catalog, eligibility and fallback | model contract | no Python constants; ≤40% synergy guard | MODEL PARTIAL | Content/Balance |
| Rewards | B1 + architecture ledger | checkpoint, chest, offer and first-clear channels separate | reward assertions | proposed 1575/520/16 for completed 30m model runs | MODEL PARTIAL | Product/Balance |
| Idempotency | architecture ledger | duplicate wallet/chest/offer returns stored result | independent checker | PASS across 30 runs | MODEL PASS | Runtime |
| Reference pattern use | three requested public repos | structure only, no foreign numeric inputs | provenance audit | links and pattern registry in JSON/docs | DERIVED PASS | Balance |
| Godot 30m run | project runtime | no actual runtime invocation in this slice | no command available | no trace | BLOCKED | Runtime |
| Android occupancy/FPS | B1 ≥30 FPS target | no device profile | no device evidence | not measured | BLOCKED | CI/QA |

## Status boundary

\`SIMULATED\` means deterministic Python model only. \`RUNTIME_VERIFIED\` is intentionally absent. The package cannot move to VERIFIED until runtime traces and Android evidence exist.
