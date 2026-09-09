
# FIRST_RUN_ACCEPTANCE_MATRIX — трассировка требований

Статус документа: **SPECIFIED_WITH_PENDING_DECISIONS**  
Статусы строк:

- SPECIFIED — логика и ownership определены, runtime ещё не доказан;
- VERIFIED_BY_DOC_CHECK — подтверждено статической проверкой этого пакета;
- PENDING — требуется product/B1/runtime решение;
- NOT_IMPLEMENTED — текущий runtime этого ещё не делает;
- BLOCKED — невозможно закрыть в разрешённой папке.

| ID | Requirement | Source | Observable behavior | Evidence/check | Status | Owner / next slice |
|---|---|---|---|---|---|---|
| A-01 | Boot → menu и resource error | AGENT_TASK.md §2; GAME_MANIFEST.md §2 | Registry validates; success opens menu; missing/stale data opens diagnostic, not white screen | Read FIRST_RUN_FLOW §4; event app.boot/menu.ready/diagnostic | SPECIFIED | Runtime BootLoader + Diagnostics |
| A-02 | Settings from menu and pause | AGENT_TASK.md §2; U-08 | Settings returns to captured owner and does not mutate RunSession | FLOW §4, §8; state transitions T-05/T-17 | SPECIFIED | Runtime AppFlowCoordinator |
| A-03 | PЕРСОНАЖИ and hero selection | AGENT_CONTEXT.md; GAME_MANIFEST.md §5 | lin_yue/soyeon_han cards expose canonical start data; invalid card is disabled | FLOW §4; JSON content_catalog.heroes | VERIFIED_BY_DOC_CHECK | Runtime menu/read model |
| A-04 | New run creates RunSession | AGENT_TASK.md §2; GAME_MANIFEST.md §4 | New run gets run_id, seed, zero clock, hero/build/checkpoint | FLOW §5; JSON run_session_contract | SPECIFIED | Runtime RunFacade |
| A-05 | Menu/run bridge ownership | AGENT_TASK.md §3 | UI sends commands; coordinator routes; UI never owns authoritative state | ARCHITECTURE §2/§5; STATE_MACHINE ownership | VERIFIED_BY_DOC_CHECK | Runtime bridge slice |
| A-06 | 20-minute game clock | GAME_MANIFEST.md §4; BALANCE §4 | elapsed time advances only in active phase and reaches 1200 seconds | JSON canonical_values; pause tests specified | SPECIFIED | Runtime RunClock |
| A-07 | Wave bands and active caps | BALANCE_ECONOMY_SPEC.md §4 | Exact five B1 bands, budgets, caps and modifiers are data-driven | FLOW §6; ARCHITECTURE §7; JSON wave_bands | VERIFIED_BY_DOC_CHECK | Runtime WaveDirector |
| A-08 | Boss at 5/10/15/20 minutes | GAME_MANIFEST.md §4/§8; BALANCE §4 | boss IDs spawn at 300/600/900/1200 with telegraph and reaction window | FLOW §7; JSON content_catalog.bosses | VERIFIED_BY_DOC_CHECK | Runtime boss stub, then content |
| A-09 | Boss spawn recovery budget | BALANCE_ECONOMY_SPEC.md §4 | Normal spawn reduced 8 seconds, then 70%→100% over 20 seconds | FLOW §6; JSON boss_spawn_policy | VERIFIED_BY_DOC_CHECK | Runtime WaveDirector test |
| A-10 | XP and aftermath separation | AGENT_CONTEXT.md; GAME_MANIFEST.md §4; BALANCE §6 | XP is collectible and raises XP; aftermath is visual, non-collision, zero XP | FLOW §6.2; EVENT catalog; JSON drops | VERIFIED_BY_DOC_CHECK | Runtime DropService |
| A-11 | XP formula and level-up choice | BALANCE_ECONOMY_SPEC.md §6; GAME_MANIFEST.md §4 | XP threshold triggers frozen clock and three legal offers | FLOW §6.3; events level.up/offer | SPECIFIED | Runtime ProgressionService |
| A-12 | Weapon/passive slots and max levels | GAME_MANIFEST.md §4/§6 | 6 weapon, 6 passive, 3 artifact capacity; levels 6/5; full slot rejects new item | ARCHITECTURE §9; JSON build contract | VERIFIED_BY_DOC_CHECK | Runtime BuildInventory |
| A-13 | Synergy eligibility/evolution | GAME_MANIFEST.md §6; U-03 | Pair requires max components, chest and unclaimed state; apply once | FLOW §7; JSON synergy_resolution | SPECIFIED | B1 registry + SynergyEvaluator |
| A-14 | Chest close/reopen/fallback | AGENT_TASK.md §2; U-04 | Same chest_id/offer_id reopens same outcome; no eligible pair produces explicit pending fallback | FLOW §7; STATE_MACHINE T-14; event chest | SPECIFIED | Product decision + ChestResolver |
| A-15 | Checkpoint reward amounts | BALANCE_ECONOMY_SPEC.md §7 | Ledger plans B1 gold/seals/essence for each defeated boss | FLOW §7 table; JSON reward_policy | VERIFIED_BY_DOC_CHECK | Runtime RewardCalculator |
| A-16 | Defeat partial rewards | BALANCE_ECONOMY_SPEC.md §7 | Defeat after checkpoint uses 50% gold formula, earned essence, defeated-boss seals only | FLOW §9; JSON reward_policy | PENDING | B1: define half-gold rounding |
| A-17 | Reward ledger idempotency | GAME_MANIFEST.md §2; BALANCE §7; AGENT_TASK.md §3 | Duplicate checkpoint/chest/result event returns existing receipt, never double grants | STATE_MACHINE §6; ARCHITECTURE §10; JSON ledger | VERIFIED_BY_DOC_CHECK | Runtime Ledger adapter tests |
| A-18 | Pause/upgrade freeze | AGENT_TASK.md §2; GAME_MANIFEST.md §2 | Clock, spawn, damage, XP and reward side effects stop while frozen | STATE_MACHINE §5; event pause/resume | SPECIFIED | Runtime RunClock integration test |
| A-19 | Android background/resume | GAME_MANIFEST.md §2; U-06/U-07 | App pause freezes first; validated snapshot/revision restores; failure is visible | FLOW §8; ARCHITECTURE §14; events save | SPECIFIED | Android runtime slice |
| A-20 | Versioned save and recovery | GAME_MANIFEST.md §2; AGENT_TASK.md §3 | Snapshot validates checksum/schema/content/ledger; invalid bytes never grant rewards | ARCHITECTURE §11; JSON save_snapshot_contract | SPECIFIED | SaveRepository + migration test |
| A-21 | HUD/read model | AGENT_TASK.md §2; U-08 | HUD exposes HP, attack, crit, multiplier, speed, cooldown, build, XP, time, kills, rewards and diagnostics | FLOW §6; ARCHITECTURE §12 | SPECIFIED | Runtime RunReadModel |
| A-22 | Result stats and terminal reopen | AGENT_TASK.md §2 | Death/victory creates immutable ResultSnapshot; reopening is read-only | FLOW §9; STATE_MACHINE terminal rules | SPECIFIED | ResultAssembler |
| A-23 | Victory gate and first-clear bonus | GAME_MANIFEST.md §4; BALANCE §7 | Final boss + final check produce victory; first-clear bonus has separate key | FLOW §9; JSON reward_policy/ledger keys | SPECIFIED | Runtime result/ledger integration |
| A-24 | Return to menu/new run | AGENT_TASK.md §2 | Claim/replay result then returns menu; active run exit requires confirmation | FLOW §8/§9; state T-24 | SPECIFIED | Runtime AppFlowCoordinator |
| A-25 | Missing/stale content diagnostics | AGENT_TASK.md §3; GAME_MANIFEST.md §2 | Missing stable ID blocks unsafe action and exposes code/path/version/recovery | ARCHITECTURE §13; event diagnostic | VERIFIED_BY_DOC_CHECK | Runtime Diagnostics |
| A-26 | No hidden absolute enemy stats | AGENT_TASK.md §4; BALANCE §4 | Architecture stores B1 multipliers only; absolute base HP/damage/speed remain pending | FLOW §6; ARCHITECTURE §7; JSON PENDING_B1 | VERIFIED_BY_DOC_CHECK | B1 balance owner |
| A-27 | Stage semantic | U-05; AGENT_TASK.md §2 | Current architecture treats stage as logical band/checkpoint within one arena | FLOW §1; JSON pending_decisions U-05 | PENDING | Product/runtime decision |
| A-28 | Bonus/series | U-01; AGENT_TASK.md §2 | State extension and HUD projection exist without invented formula | FLOW §6; JSON stats.bonus_state | PENDING | Product/B1 decision |
| A-29 | Unlock/replay semantics | U-09; AGENT_TASK.md §2 | Ledger supports first-clear/repeat keys; no new unlock economy invented | JSON pending_decisions U-09 | PENDING | Meta progression owner |
| A-30 | Current prototype boundary | DECISIONS_AND_UNKNOWNS.md U-10; code evidence | Menu/arena prototypes are evidence only; no runtime claims | FLOW §10; ARCHITECTURE §17 | NOT_IMPLEMENTED | Runtime agent wraps/replaces prototype |
| A-31 | Stub-only implementation scope | User brief; AGENT_TASK.md §5 | No PNG/SVG/TSCN/GDScript/assets added or promoted by this package | GitHub diff path check; FLOW §10; ARCHITECTURE §16 | VERIFIED_BY_DOC_CHECK | Runtime/content agents later |
| A-32 | Contract JSON validity | DELIVERABLES.md; AGENT_TASK.md §7 | FIRST_RUN_DATA_CONTRACT.json parses without comments/trailing commas | JSON.parse / Python json.load; path check | VERIFIED_BY_DOC_CHECK | Maintainer reruns on edits |
| A-33 | Traceability and event coverage | DELIVERABLES.md; AGENT_TASK.md §7 | Required flow and events map to docs, owners, payloads and checks | Event catalog minimum list + this matrix | VERIFIED_BY_DOC_CHECK | Change review before runtime |
| A-34 | Android performance risk | GAME_MANIFEST.md §2; BALANCE §4/§6 | Pooling, active caps, aftermath budget and 60/30 FPS target are explicit; no performance claim yet | ARCHITECTURE §8/§14; runtime profiling required | NOT_IMPLEMENTED | Android slice + real-device evidence |

## 1. Pending decisions

The following are intentionally not marked as closed:

- U-01: exact bonus/series meaning and formula;
- U-02: exact slot replacement/offer semantics, although capacity 6+6 is canonical;
- U-03: evaluator details and exact effects for the ten direct pairs;
- U-04: chest fallback reward;
- U-05: separate scene versus logical stage;
- U-06: incomplete-run save points;
- U-07: abandon/process-kill/recovery policy;
- U-08: final HUD/result presentation;
- U-09: unlock and replay semantics.

These are represented in FIRST_RUN_DATA_CONTRACT.json and must not be silently resolved in runtime.

## 2. Scope proof

Allowed mutation set for this task: docs/architecture/first-run/.

Intentionally not changed:

- scripts/;
- scenes/;
- project.godot;
- export_presets.cfg;
- GAME_MANIFEST.md;
- AGENT_CONTEXT.md;
- ROADMAP.md;
- README.md;
- docs/BALANCE_ECONOMY_SPEC.md;
- visual_lab/ and all PNG/SVG/TSCN/GDScript/assets.

A runtime agent may consume this package, but this matrix does not mark runtime implementation as complete.
