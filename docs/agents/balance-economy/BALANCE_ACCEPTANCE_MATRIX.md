# Balance Acceptance Matrix

Status: SIMULATED_MODEL_ONLY / PARTIAL

B1 source revision: 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687.
Architecture source revision: 2f889f876f2b8aa286523d234786addf0b9b245e.
Model run: 30 runs, 3 profiles × 2 heroes × 5 seeds.

| Requirement | Source | Model/runtime behavior | Check | Observed | Status | Next owner |
|---|---|---|---|---|---|---|
| One auditable balance model | B1 + architecture contract | BALANCE_MODEL.json contains CANON, DERIVED, PROPOSED, PENDING fields | JSON parse and provenance inspection | Valid model; simulator reads this file | SIMULATED_MODEL_ONLY | Balance + Architecture |
| Balance↔architecture stable IDs | Architecture contract revision 2f889f876f2b8aa286523d234786addf0b9b245e | Boss, wave-band, enemy and build references join by semantic ID; numeric tuning is not duplicated | balance_contract_validator.py | PASS: 4 boss IDs, 5 wave IDs, build references, all-boss clock policy and final policy | SIMULATED_MODEL_ONLY | Runtime + Architecture |
| Five wave bands and caps | B1 section 4 | Canonical rates/caps plus proposed weighted composition | 30 deterministic runs | All bands traversed; cap reached in every slice | SIMULATED_MODEL_ONLY | Runtime |
| Exact composition ratios | B1 section 4 | Ratios exposed in model, not hidden in Python | Compare model weights to output | Ratios are PROPOSED; Product decision pending | PROPOSED | Product + Balance |
| Boss interruption/recovery | B1 section 4 + user clock decision | 8 s, 0.70→1.00/20 s; all four boss encounters pause the visible run clock and suppress ordinary wave/XP/spawn time | Fixed checkpoint factors and clock-event assertions | 4/4 boss events per run; encounter clock advanced while run clock stayed fixed; recovery factor reproduced | SIMULATED_MODEL_ONLY | Runtime |
| Active cap | B1 section 4/10 | Cap 40/80/130/200/280, excess discarded | Occupancy and suppressed-spawn trace | Cap 280 reached in all 30 runs; cap occupancy 1105.7–1140.0 s and 19,468–20,276 suppressed attempts by slice | SIMULATED_MODEL_ONLY / WATCH | Balance + Runtime |
| First level 30–45 s | B1 section 6 | Proposed pickup window/capacity | Five-seed checkpoint trace | 33.25–39.75 s across profiles | SIMULATED_MODEL_ONLY | Runtime |
| Levels 2/5/9/13/17–18 | B1 section 4/6 | XP formula + proposed pickup model; XP clock is paused during all bosses | Levels at 120/300/600/900/1200 s | Fresh: 2/5/9/13/17; moderate: 2/6/10/13/17; max M1: 2/6/10/14/18 | SIMULATED_MODEL_ONLY | Balance |
| Ordinary TTK 0.5–2.5 s | B1 section 3 | Focused TTK from first damage event | Per-enemy/profile trace | Means mostly inside; some p95 values exceed 2.5 s | PARTIAL | Balance + Combat Runtime |
| Elite TTK 10–25 s | B1 section 3 | Proposed absolute stats and focused DPS | Elite trace | Means mostly inside; p95 can exceed target | PARTIAL | Balance + Combat Runtime |
| Boss TTK 45–80/90–120 s | B1 section 3 | Four proposed boss stat blocks resolved on separate encounter clocks | Per-checkpoint trace | 30 runs: fresh Lin 3/4, fresh Soyeon 1/4, moderate Lin 4/4, moderate Soyeon 3/4, max Lin 3/4, max Soyeon 4/4 target windows; final Lin max is below lower bound and fresh/moderate Soyeon exceed upper bound | PARTIAL / BLOCKED | Balance + Boss Runtime |
| Incoming damage/risk | B1 section 10 | Deterministic landed-hit model and mitigation | HP/damage trace | All 30 runs survive; conservative single-hit bound passes; spatial collision unverified | SIMULATED_MODEL_ONLY | Combat Runtime + QA |
| No same-frame stacking/contact gate | B1 section 5 | Contract documented; simulator is not event-runtime | Runtime event trace | Not exercised in Godot | BLOCKED | Combat Runtime |
| Boss safe spawn/reaction window | B1 section 10 | Boss timing only; no positions/telegraphs | Runtime property test | Not implemented | BLOCKED | Boss Runtime + QA |
| Weapon/passive/synergy IDs | Architecture contract | Canonical IDs and proposed numeric effects | Build/evolution trace | Both proposed routes resolve boss-chest synergy; final checkpoint creates no boss chest | SIMULATED_MODEL_ONLY | Runtime + Product |
| Artifact offer boundary | Architecture contract; product decision | Elite pack/first-clear source opens exactly three cards; one chosen effect is active in-run and consumes no weapon/passive slot | Offer lifecycle/idempotency trace | Contract specified; elite cadence and exact effects pending | SIMULATED_MODEL_ONLY / PENDING | Balance + Runtime + Product |
| Artifact effect power/types | GAME_MANIFEST; architecture contract | Typed aura/derived-stat/target/weapon/triggered/cooldown effects are modeled separately from passive modifiers | Effect attribution and stacking trace | Contract boundary specified; definitions pending | PENDING | Balance + Product |
| Synergy ≤40% total damage | B1 section 10 | Formula clamps attribution share | Damage attribution output | Model cap is enforced; no runtime attribution | SIMULATED_MODEL_ONLY | Combat Runtime |
| Boss-chest fallback offer | Architecture contract open question | Proposed +3% fallback on unresolved non-final boss chest | Boss-chest resolver trace | Fallback is deterministic and visible | PROPOSED | Product |
| Artifact refresh/choice idempotency | Architecture contract; product decision | Refresh and Get commands are replay-safe; one of three cards creates one active effect | Duplicate command trace | Not implemented in runtime; simulator models first-clear offer creation | PENDING | Runtime + Product |
| Checkpoint rewards | B1 section 7 | Canonical values read from model | Ledger sum | Full first clear 725/300/6; repeat 425/120/5 arithmetic preserved | SIMULATED_MODEL_ONLY | Reward Runtime |
| Reward idempotency | Architecture contract | Canonical key format and duplicate rejection | Duplicate grant attempts | PASS in all 30 model runs | SIMULATED_MODEL_ONLY | Reward Runtime |
| Final boss chest policy | Architecture latest HEAD | NO_CHEST final policy; first-clear artifact is a separate post-result three-card offer | Assert final boss chest=false and artifact offer source=FIRST_CLEAR_REWARD | PASS in model; offer selection/persistence remains pending | SPECIFIED / PENDING | Architecture + Product |
| Boss encounter run clock | User product decision 2026-09-10 | At 300/600/900/1200s the main run clock stops; wave/XP/spawn clock remains frozen; each boss resolves on a separate encounter clock | Assert model clock_policy and runtime trace | PASS in model: 4/4 pause events in all 30 runs; runtime trace absent | SIMULATED_MODEL_ONLY / BLOCKED | Runtime + QA |
| Post-clear progression pacing | B1 sections 7–9 | Reward totals exist; summon/catalog pacing absent | Full economy replay | Not runtime-verified | BLOCKED | Economy + Product |
| Minimum 30 FPS Android | B1 section 10 | No device/frame-time model | Device profiling | Target device and Godot runtime absent | BLOCKED | Performance + Runtime |
| Readability of telegraphs/XP/aftermath | B1 sections 4/6/10 | No scene execution | Visual/runtime QA | Not measured | BLOCKED | Runtime + Visual QA |
| Deterministic replay | Engineering guardrails | Fixed model input and seed set | Two full runs + hash | PASS; hashes equal: 52b32ebff019e312a23d2153439ec0ebbfb7fdf3b48acb568efb16e922a78242 | SIMULATED_MODEL_ONLY | QA + Runtime |
