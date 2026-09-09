# Balance Acceptance Matrix

Status: PARTIAL

Source baseline: docs/BALANCE_ECONOMY_SPEC.md, revision 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687.

This matrix separates specification, deterministic contract arithmetic, and runtime evidence. A row is not VERIFIED merely because the target is written down. Runtime rows remain NOT_IMPLEMENTED or BLOCKED until an executable run loop, trace, test, or device measurement exists.

| Requirement | Source | Model/runtime behavior | Check | Observed | Status | Next owner |
|---|---|---|---|---|---|---|
| Machine-readable balance contract has source and provenance | B1; BALANCE_MODEL.json | Canonical values carry CANON source; missing values remain null/PENDING_* | Parse JSON; inspect status/source fields | Contract materialized; no runtime consumer found | SPECIFIED | Balance + Architecture |
| Wave bands, multipliers, caps, and level targets | B1 section 4 | Five CANON bands; arithmetic simulator derives 22,620 nominal spawn opportunity | Run balance_simulator.py with fixed seed | Arithmetic self-check passes | SIMULATED | Runtime |
| Exact wave composition ratios and elite cadence | B1 section 4 | Membership is defined; weights/cadence are not invented | Require explicit composition fixture | Ratios, duplicate limits, and cadence absent | BLOCKED | Balance + Product |
| Boss interruption | B1 section 4 | 8-second reduction and 0.70→1.00 over 20 seconds; overlap semantics pending | Run conditional interpolation check; then runtime trace | Conditional 0.85 average/17 nominal spawn-seconds only | SPECIFIED | Balance + Runtime |
| Ordinary TTK 0.5–2.5 s | B1 section 3 | Requires absolute enemy stats and sustained player DPS | Deterministic combat trace per enemy/profile | Base HP/damage/speed and runtime combat loop absent | BLOCKED | Combat Runtime + Balance |
| Elite TTK 10–25 s | B1 section 3 | Same | Deterministic elite trace with telegraph and mitigation | No absolute elite inputs or trace | BLOCKED | Combat Runtime + Balance |
| First-slice boss TTK 45–80 s | B1 section 3 | Boss HP, phases, DPS window, and spawn schedule required | Boss trace with phase timestamps | Boss numeric stats and boss runtime absent | BLOCKED | Boss Runtime + Balance |
| Final boss TTK 90–120 s | B1 section 3 | Same | Full 20-minute trace | Final boss numeric stats and runtime absent | BLOCKED | Boss Runtime + Balance |
| First level in 30–45 s | B1 section 6 | Threshold formula is CANON; actual XP rate is runtime-dependent | Fixed-seed XP pickup trace | Placeholder profiles only; no RunSession/XP loop | BLOCKED | Progression Runtime + Balance |
| Level approximately 9 at 10 minutes | B1 section 6 | Requires kill composition, XP pickup latency, and level-up overflow rules | 10-minute replay per hero/profile | Placeholder projection is not production evidence | BLOCKED | Progression Runtime + Balance |
| First significant decision by 90 s | B1 section 6 | Offer generation and pause/selection flow required | Replay with timestamps and offer IDs | Offer IDs/eligibility/flow not implemented | BLOCKED | Progression Runtime + Product |
| First evolution at 8–12 minutes | B1 section 6 | Requires weapon/passive/synergy catalog and eligibility | Replay with selected build and evolution timestamp | Catalog and evolution rules are pending | BLOCKED | Progression Runtime + Product |
| No untelegraphed hit above 15% base HP | B1 section 10 | Every damage event needs telegraph metadata and post-mitigation amount | Assert event trace against 15% base HP | Contract written; no combat event trace | BLOCKED | Combat Runtime + QA |
| Contact gate, telegraphs, safe elite spawn, no same-frame stacking | B1 section 5 | Contact cooldown 0.8 s; telegraph/safe-spawn invariants | Combat event and spawn-position tests | Rules are specified; runtime tests absent | SPECIFIED | Combat Runtime + QA |
| Boss never spawns inside player and leaves reaction window | B1 section 10 | Spawn validator plus telegraph timestamp required | Property test over deterministic seeds | No boss spawn/runtime trace | BLOCKED | Boss Runtime + QA |
| Synergy contributes no more than 40% total damage | B1 section 10 | Damage attribution must label synergy versus base/weapon/passive | All-build damage attribution suite | Synergy IDs and build catalog absent | BLOCKED | Build Runtime + Balance |
| Two sustainable routes per hero | B1 section 10 | At least two viable Lin Yue and Soyeon Han builds | Profiled route replay with survival/TTK evidence | No build catalog or hero run loop | BLOCKED | Balance + Build Runtime |
| Active mass cap and safe mode | B1 section 4/10 | Must enforce cap and preserve XP/telegraphs/readability | Stress test at each cap and Android target | Caps are specified; consumer and safe mode absent | BLOCKED | Runtime + Performance |
| XP drops and separate aftermath | B1 section 6; AGENT_CONTEXT | XP values are CANON; aftermath must not obscure XP/readability | Scene/replay and pickup trace | Arithmetic is simulated; runtime presentation absent | BLOCKED | Runtime + Visual QA |
| Checkpoint, first-clear, repeat-clear totals | B1 section 7 | Simulator reproduces 425/120/5 repeat and 725/300/6 first-clear totals | Deterministic reward calculation | Totals match B1 | SIMULATED | Reward Runtime |
| Reward ledger idempotency | B1 section 7; GAME_MANIFEST | Retry-safe grant keyed by run/checkpoint/outcome/table version | Duplicate/reconnect/replay transaction test | Test harness rejects duplicates; production key/ledger absent | BLOCKED | Reward Runtime + Architecture |
| Post-clear grants some meta/summons but not whole progression | B1 section 7–9 | Reward pacing must be measured over first clear and repeats | Progression economy replay | Reward table is specified; summon pool and pacing absent | BLOCKED | Economy + Product |
| M1 has no paid gacha | B1 section 9 | No paid-gacha transaction path | Static config and store-flow audit | Rule is specified; store runtime not audited as implemented | SPECIFIED | Product + Economy |
| Minimum 30 FPS on target Android | B1 section 10 | Target device, scene, load, and measurement protocol required | Profiled 20-minute run with frame-time capture | Target device and runtime run absent | BLOCKED | Performance + Runtime |
| Deterministic replay and regression suite | B1/AGENT_CONTEXT; engineering guardrails | Seeded contract simulator is repeatable; runtime replay is still required | Run twice; compare hash; then replay game trace | Simulator hash stable: 95c09b1e…68caae9; no runtime test suite | SIMULATED | QA + Runtime |
| Readability of combat, telegraphs, XP, aftermath, results | B1 section 10; visual package | Requires actual scene capture and review | Visual QA checklist on runtime build | Runtime evidence absent; visual assets are out of scope here | BLOCKED | Visual Lab + Runtime |
