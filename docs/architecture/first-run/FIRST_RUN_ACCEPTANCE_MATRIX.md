# FIRST_RUN_ACCEPTANCE_MATRIX — traceability первого забега

Статус: VERIFIED ARCHITECTURE SPECIFICATION
Runtime implemented: NO
Правило: VERIFIED_BY_DOC_CHECK означает проверку архитектурного артефакта/ссылки, а не работу Godot runtime или Android APK.

> Revision 2: acceptance rows include the 30-minute schedule, three intermediate encounters, 15-window chest registry, relief/ramp waves and beetle variants. Runtime implemented: NO.

## 1. Матрица требований

| Requirement | Source | Observable behavior / contract | Evidence/check | Status | Owner/next slice |
|---|---|---|---|---|---|
| Boot и splash/loading | AGENT_TASK §2; GAME_MANIFEST | AppShell загружает registry/save и показывает error без blank screen | FIRST_RUN_FLOW §§3, 10; event catalog content_load_* | SPECIFIED | Runtime Iteration 1: AppShell/ContentLoader |
| Главный экран | AGENT_TASK §2 | MAIN_MENU имеет навигацию и read model | FLOW step 3; STATE T-04/T-05 | SPECIFIED | Runtime Iteration 1 |
| Settings и возврат | AGENT_TASK §2 | Settings доступен из menu и pause, invalid values не меняют valid state | FLOW steps 4, 7, 25–27; STATE T-04/T-18/T-20 | SPECIFIED | Runtime Iteration 2 |
| ПЕРСОНАЖИ | AGENT_CONTEXT; AGENT_TASK | Нейтральный label, карточки character и selected state | FLOW step 5/6; DATA content_registry.characters | SPECIFIED | Runtime Iteration 1 |
| Создание RunSession | AGENT_TASK §2 | Confirm start создаёт новый run_id, seed, content version и revision | FLOW step 8; STATE T-07/T-08; DATA run_session | SPECIFIED | Runtime Iteration 1 |
| Menu/run bridge | AGENT_TASK §3 | MenuFlow отправляет command, RunCoordinator создаёт session; UI не владеет state | ARCHITECTURE §§2–3 | SPECIFIED | Runtime Iteration 1 |
| Arena loading | GAME_MANIFEST; live prototype evidence | Сессия стартует только после validation обязательных gameplay resources | FLOW step 9; ARCHITECTURE ContentLoader | SPECIFIED | Runtime Iteration 1 |
| Movement/combat | GAME_MANIFEST; AGENT_TASK | Simulation consumes clock and emits combat facts, not wallet/UI mutation | ARCHITECTURE Simulation; EVENT combat boundary | SPECIFIED | Runtime Iteration 1 |
| Wave cycles and pressure | B1 §§4–5; user extension brief | WaveDirector uses opening/relief/ramp/peak phases and does not jump from boss defeat directly to max pressure | DATA wave_bands/wave_policy; FLOW §3.2; EVENT wave_phase_changed/post_boss_relief | SPECIFIED/PENDING_B1 | Runtime Iteration 2 after B1 extension |
| Boss schedule 5/10/15/20/25/30 + 3 intermediate slots | User extension brief; C3; legacy GAME_MANIFEST/B1 | Registry emits six main slots and three intermediate encounters; final identity is terminal at 30:00 | STATE T-11/T-12; DATA encounter schedule; FLOW §3.1 | SPECIFIED/PENDING_CONTENT | Runtime Iteration 2 after Content/B1 sync |
| Next stage semantics | AGENT_TASK; DECISIONS U-05 | После нефинального settlement/chest меняется stage projection; финальный босс заканчивает забег без следующей стадии | FLOW §§6, 11; STATE T-15 | PENDING | Product/runtime owner confirms U-05 |
| XP formula and grades | B1 §§6; GAME_MANIFEST | XPDrop collection credits value once and opens level offer at threshold | DATA xp_grades; EVENT xp_* / level_up | SPECIFIED | Runtime Iteration 2 |
| XP versus aftermath | GAME_MANIFEST; B1 §4 | XPDrop и AftermathItem имеют разные IDs, stores, layers и lifecycle | DATA entity_shapes; ARCHITECTURE §7 | SPECIFIED | Runtime Iteration 1 then 2 |
| Kills and stats | AGENT_TASK §2/§4 | RunSession counts kills and projects required combat/progression stats | FLOW §9; DATA run_session.stats | SPECIFIED | Runtime Iteration 1/2 |
| Bonus/series | AGENT_TASK; DECISIONS U-01 | Extensible bonus_state exists; no unconfirmed formula is invented | DATA stats.bonus_state | PENDING | Product owner confirms U-01 |
| Level-up freeze | GAME_MANIFEST; AGENT_TASK | Clock stops, exactly three valid offer projections are shown | STATE T-09/T-10; EVENT level_up/offer_* | SPECIFIED | Runtime Iteration 1/2 |
| Weapon acquisition/upgrade | GAME_MANIFEST | BuildInventory validates New/Upgrade and emits one mutation per offer | DATA weapons/build_entry; EVENT upgrade_applied | SPECIFIED | Runtime Iteration 1/2 |
| Passive acquisition/upgrade | GAME_MANIFEST | Passive slots/ranks and modifiers are data-driven | DATA passives/build_entry | SPECIFIED | Runtime Iteration 2 |
| Slot limits | GAME_MANIFEST; AGENT_TASK | Six weapon and six passive slots; artifacts have no fixed slot capacity and do not consume either build slot type | DATA canonical/build; ARCHITECTURE BuildInventory | SPECIFIED | Runtime Iteration 2 |
| Artifact offer choice | GAME_MANIFEST; product decision | An elite-pack or first-clear source opens an offer with exactly three cards; `Get` selects one effect | DATA artifact_offer; EVENT artifact_offer_created/artifact_chosen | SPECIFIED | Runtime Iteration 2 |
| Artifact refresh | Product decision | `Refresh` is a separate idempotent command; cost, limit and reroll policy remain explicit pending fields | DATA artifact_offer.refresh_policy; EVENT artifact_offer_refresh_* | PENDING | Product owner |
| Artifact effect boundary | GAME_MANIFEST; AGENT_TASK | Active artifact effects are typed run modifiers (aura, derived stat, target, weapon or triggered effect), separate from ordinary passive modifiers | DATA content_registry.artifact_effects; ARCHITECTURE ArtifactEffectSystem | PENDING | Product owner defines typed effects; runtime validates contract |
| Artifact sources | Product decision; B1 first-clear reward | Elite packs may create offers between bosses; first-clear creates a separate post-result offer; boss chest remains synergy/fallback only | FLOW; STATE; EVENT elite_pack_defeated/artifact_offer_created | PENDING | Product owner + balance owner define cadence and pool before runtime Iteration 2 |
| Synergy eligibility | GAME_MANIFEST; AGENT_TASK | Matching pair, max weapon/passive, non-evolved, non-final boss-chest context and claim guard are checked | DATA synergy_evaluator; FLOW §5 | SPECIFIED | Runtime Iteration 2 |
| Synergy/evolution duplicate guard | AGENT_TASK | Repeated claim returns existing outcome; no second evolution | STATE T-15; EVENT synergy_claimed | SPECIFIED | Runtime Iteration 2 |
| Chest eligible path | GAME_MANIFEST; AGENT_TASK; user extension brief | Up to 15 registry windows are independently identified; only non-final boss/mini-boss source may create BOSS_CHEST; eligible outcome/fallback claims once; final boss creates no chest | FLOW §§3.1/6.1; STATE T-14/T-15/T-15C; EVENT chest_window_* / boss_chest_* | SPECIFIED/PENDING_PRODUCT | Runtime Iteration 2 after reserved-source approval |
| Chest fallback path | AGENT_TASK; DECISIONS U-04 | Для нефинального chest fallback_required is representable but exact value is not fabricated; final boss has no fallback chest | DATA chest_offer.fallback_policy | PENDING | Product owner confirms U-04 |
| HUD/read model | AGENT_TASK §4 | UI can show HP, attack, crit, speed, cooldown, build, active artifact effects, pending three-card offer, XP, time, stage, kills, rewards | FLOW §9; ARCHITECTURE §8 | SPECIFIED | Runtime Iteration 2 |
| Pause | AGENT_TASK §4 | Manual pause freezes clock and preserves resume_state | STATE RUN_PAUSED/T-18/T-19; EVENT run_paused | SPECIFIED | Runtime Iteration 1 |
| Settings from pause | AGENT_TASK | Settings returns to exact blocking/resume context | FLOW §7; STATE pause model | SPECIFIED | Runtime Iteration 2 |
| Exit to menu | AGENT_TASK | Confirmation distinguishes cancel from abandon; no unearned rewards | FLOW §7; STATE T-22 | SPECIFIED | Runtime Iteration 2 |
| Android background/resume | GAME_MANIFEST; AGENT_TASK | Background forces pause; restore validates snapshot/checksum/content | ARCHITECTURE §6; EVENT run_resumed | SPECIFIED | Runtime Iteration 3 |
| Save boundary | GAME_MANIFEST; DECISIONS U-06/U-07 | Checkpoint/explicit pause/terminal snapshots are versioned and atomic; arbitrary frame not promised | DATA save_snapshot; ARCHITECTURE §6 | PENDING | Product/runtime owner confirms recovery policy |
| Death | GAME_MANIFEST; B1 | HP zero yields one terminal defeat result and allowed partial rewards | FLOW §8; STATE T-16; EVENT run_defeated | SPECIFIED | Runtime Iteration 2 |
| Victory | GAME_MANIFEST | Final victory requires final boss defeat and final settlement, not timer alone; final boss has no boss chest and first-clear artifact is separate | FLOW §8; STATE T-17/T-14F; invariant 6 | SPECIFIED | Runtime Iteration 2 |
| Result stats | AGENT_TASK | Result projection contains build, kills, XP, stats, checkpoints and reward status | FLOW §9; ARCHITECTURE §8 | SPECIFIED | Runtime Iteration 2 |
| Reward bundles | B1 §§7–9 | RewardCalculator reads deterministic bundles and separate wallets | DATA reward_bundles; ARCHITECTURE §5 | SPECIFIED | Runtime Iteration 2 |
| Checkpoint ledger | GAME_MANIFEST; B1 extension required | Every configured main/intermediate checkpoint settles once; final 30:00 settlement has no chest | STATE T-14/T-14F; EVENT checkpoint_reward_* / final_settlement_committed | SPECIFIED/PENDING_B1 | Runtime Iteration 2 after reward table sync |
| First clear/repeat/defeat | B1 §7 | Scopes are separate; defeat after checkpoint uses allowed partial path | FLOW §8; DATA reward ledger | SPECIFIED | Runtime Iteration 2 |
| Ledger idempotency | AGENT_TASK; GAME_MANIFEST | Duplicate checkpoint/boss-chest/artifact-offer/result commands return existing outcome without wallet mutation or duplicate effect | ARCHITECTURE §5; EVENT §2/§4 | SPECIFIED | Runtime Iteration 1 test then 2 |
| Save restore idempotency | AGENT_TASK | Restore cannot replay settled ledger entries | STATE T-19/T-21; DATA reward_ledger_ref | SPECIFIED | Runtime Iteration 2 |
| Diagnostics/fallback | GAME_MANIFEST; AGENT_CONTEXT | Missing resources produce code/path/severity/recovery, never blank screen | ARCHITECTURE §7; EVENT content_load_failed | SPECIFIED | Runtime Iteration 1 |
| Data-driven content | GAME_MANIFEST; AGENT_TASK | Registry owns content and version; UI does not encode invariants | ARCHITECTURE §4; DATA registry | SPECIFIED | Runtime Iteration 1/2 |
| Controlled spawn/pooling | GAME_MANIFEST; B1 | Enemy/projectile/XP/aftermath pools enforce cap and do not drop XP silently | ARCHITECTURE Simulation; DATA entity shapes | SPECIFIED | Runtime Iteration 2/3 |
| Performance | B1 §10; GAME_MANIFEST | Full wave has target/safe FPS evidence on Android | B1 acceptance targets; future runtime profiling | NOT_IMPLEMENTED | Runtime Iteration 3 |
| No unapproved assets | AGENTS; Visual Lab law | Architecture references IDs/manifests only; no asset promotion or runtime dependency added | Scope inspection and explicit non-goals | VERIFIED_BY_DOC_CHECK | Separate visual/runtime owners |
| Current prototype distinction | REPO_CONTEXT; live code | Menu/arena prototypes are adapters/evidence, not target runtime | ARCHITECTURE §3 and FLOW §10 | VERIFIED_BY_DOC_CHECK | Runtime migration review |
| JSON schema validity | DELIVERABLES; AGENT_TASK | Contract parses without comments/trailing comma | json validator after commit | VERIFIED_BY_DOC_CHECK | Architecture verification |
| Internal path validity | README; AGENT_TASK | Links point to existing repository paths or same-folder deliverables | repository path audit after commit | VERIFIED_BY_DOC_CHECK | Architecture verification |
| Scope boundary | README; AGENT_TASK; explicit product decision | This finalization commit changes only docs/architecture/first-run; pre-existing external commits are reported but not modified | changed-path inspection against parent HEAD | VERIFIED_BY_DOC_CHECK | Architecture verification |
| No pre-run artifact loadout | GAME_MANIFEST; AGENT_TASK | Run setup rejects artifact selection before run; artifact capacity is unbounded only after a source offer | FLOW step 7; STATE T-07; DATA canonical/artifact_offer | SPECIFIED | Runtime Iteration 1/2 |
| Boss telegraph/reaction | AGENT_TASK; GAME_MANIFEST; B1 | Boss shows telegraph and reaction window before damage and spawns safely outside the player model | FLOW steps 16/17; STATE T-12; EVENT boss_spawned.v1 | SPECIFIED | Runtime Iteration 2 |
| Run clock during every boss | Explicit current task decision; AGENT_TASK; B1 boundary | Elapsed time continues in BOSS_INTRO/BOSS_ACTIVE for all bosses and freezes only at offer, pause or settlement boundaries | FLOW clock; STATE BOSS_INTRO/BOSS_ACTIVE; DATA clock_policy | SPECIFIED | Runtime Iteration 2 |
| Ownership and dependency direction | AGENT_TASK §3 | Coordinator orchestrates, domain owners mutate, UI/projections remain read-only | ARCHITECTURE §§2–3; STATE ownership | VERIFIED_BY_DOC_CHECK | Architecture verification |
| Unfinished run continuation/new run | AGENT_TASK | Cancel returns to pause; abandon gives no unearned rewards; later start creates a new run_id and follows recovery policy | FLOW steps 26–32; STATE T-19/T-22/T-26 | SPECIFIED | Runtime Iteration 2 |
| Transition/event/data traceability | AGENT_TASK §§2–3 | Every transition has trigger, guard, owner, side effects, failure/recovery and duplicate policy; event names map to state/data contracts | STATE table; EVENT catalog; DATA envelope | VERIFIED_BY_DOC_CHECK | Architecture verification |
## 1.1 Extension delta traceability

| Requirement | Source | Observable behavior / contract | Evidence/check | Status | Owner/next slice |
|---|---|---|---|---|---|
| 30-minute run | User extension brief; legacy root conflict recorded in decisions | duration_seconds=1800; terminal encounter uses final slot; old 20-minute snapshots do not silently resume | DATA canonical; FLOW §3.1; DECISIONS U-17/U-21 | SPECIFIED/PENDING_B1 | Balance + Runtime migration gate |
| Two added main bosses | User extension brief | boss_extension_slot_04 and boss_extension_slot_05 are stable pending records at target 20:00/25:00 slots | DATA content_registry.bosses; STATE schedule | SPECIFIED/PENDING_CONTENT | Content Registry owner |
| Final boss remains at end | Product continuity assumption | boss_black_moon_empress is final at 30:00; final settlement → victory; no chest | DATA/STATE/FLOW final branch | SPECIFIED | Product confirms target schedule |
| Three intermediate bosses | C3 plus user extension brief | two C3 IDs plus one new intermediate slot; each uses BOSS_INTRO/BOSS_ACTIVE and non-final chest flow | DATA intermediate_bosses; FLOW §3.1 | SPECIFIED/PENDING_CONTENT | Content owner + B1 |
| Chest capacity >7 / target 15 | User extension brief | 15 registry slots/cap, 8 configured boss/mini windows, 7 reserved source windows; one offer per window | DATA chest_windows/chest_offer; EVENT chest_window_*; STATE T-15C | SPECIFIED/PENDING_PRODUCT | Product/B1 configure 7 sources |
| Synergy count remains separate | C3 content contract; product decision | Chest count does not increase synergy claim cap; fallback does not consume synergy claim | DATA canonical/synergy_evaluator; FLOW §6.1 | SPECIFIED | Runtime Iteration 2 |
| Three beetle variants | User extension brief; AGENT_TASK | deterministic variant selection with base/variant telemetry and non-color marker; no duplicate reward | DATA enemy_variants; EVENT enemy_variant_selected; ARCHITECTURE EnemyVariantResolver | SPECIFIED/PENDING_B1 | Content/B1 + Runtime Iteration 2 |
| Three new enemies | User extension brief | three explicit pending registry slots; no invented names/stats/assets | DATA enemy_extension_slots; scope inspection | SPECIFIED/PENDING_CONTENT | Content owner |
| Post-boss wave recovery | User extension brief; B1 principle | after every non-final encounter relief precedes gradual ramp; no immediate peak jump | FLOW §3.2; STATE §3.2; EVENT post_boss_relief_started | SPECIFIED/PENDING_B1 | Balance + Runtime Iteration 2 |
| Legacy contract migration | Architecture safety invariant | schema v2 rejects/isolates v1 20-minute snapshots unless explicit adapter exists | DATA migration_policy; DECISIONS U-21 | SPECIFIED/BLOCKED_EXTERNAL_SYNC | Runtime owner before save shipping |


## 1.2 AGENT_TASK §3 traceability

Каждый из 18 нумерованных пунктов раздела 3 AGENT_TASK.md имеет отдельную строку ниже. Статус означает готовность архитектурного контракта; runtime proof остаётся задачей соответствующего runtime-среза.

| ID | AGENT_TASK §3 point | Evidence | Status |
|---|---|---|---|
| AT-01 | Source of truth для run state, content, UI projection, persistence и ledger | ARCHITECTURE §§2–4; DATA top-level contracts | VERIFIED_BY_DOC_CHECK |
| AT-02 | Границы модулей и направление зависимостей | ARCHITECTURE §§2–3 | VERIFIED_BY_DOC_CHECK |
| AT-03 | Контракт menu ↔ run | FLOW §§3–4; STATE T-04/T-07/T-08 | SPECIFIED |
| AT-04 | Контракт simulation ↔ progression ↔ UI ↔ save | ARCHITECTURE §§3, 6, 8; DATA run_session/save_snapshot | SPECIFIED |
| AT-05 | Контракт времени, pause, background, checkpoint и victory | FLOW §3; STATE clock/pause transitions; DATA clock_policy | SPECIFIED |
| AT-06 | Контракт волн, budgets, caps, boss interruption и recovery | FLOW §3.2; DATA wave_policy/wave_bands; EVENT wave_* | SPECIFIED/PENDING_B1 |
| AT-07 | Разделение XP, chest, artifact и aftermath | ARCHITECTURE §7; DATA entity_shapes/drops; EVENT drop boundaries | VERIFIED_BY_DOC_CHECK |
| AT-08 | Контракт выбора, synergy eligibility и fallback | FLOW §5–6; STATE offer transitions; DATA artifact_offer/chest_offer/synergy_evaluator | SPECIFIED/PENDING_PRODUCT |
| AT-09 | Контракт статистики run и result | FLOW §9; ARCHITECTURE §8; DATA stats/result fields | SPECIFIED |
| AT-10 | Deterministic rewards, checkpoint ledger и idempotency | ARCHITECTURE §5; DATA reward_ledger; EVENT reward/checkpoint events | VERIFIED_BY_DOC_CHECK |
| AT-11 | Snapshot version и безопасное восстановление | ARCHITECTURE §6; STATE T-18/T-19/T-21; DATA schema_migration | SPECIFIED/BLOCKED_EXTERNAL_SYNC |
| AT-12 | Диагностика отсутствующего/устаревшего контента | ARCHITECTURE §7; STATE failure/recovery columns; EVENT content_load_failed | SPECIFIED |
| AT-13 | Data-driven части и UI-независимые invariants | ARCHITECTURE §4; DATA content_registry/invariants | VERIFIED_BY_DOC_CHECK |
| AT-14 | Тонкий vertical slice и расширение до M1 | ARCHITECTURE §10; AUDIT handoff | SPECIFIED |
| AT-15 | Schedule registry для main/intermediate/final/chest source | FLOW §3.1; DATA schedule_policy/chest_windows; STATE T-11/T-12 | SPECIFIED/PENDING_CONTENT |
| AT-16 | Post-boss relief и gradual ramp | FLOW §3.2; DATA wave_policy; EVENT post_boss_relief_started | SPECIFIED/PENDING_B1 |
| AT-17 | Детерминированный EnemyVariantResolver и telemetry/reward invariants | ARCHITECTURE EnemyVariantResolver; DATA enemy_variants; EVENT enemy_variant_selected | SPECIFIED/PENDING_B1 |
| AT-18 | Миграция/блокировка legacy 20-minute snapshots | DATA schema_migration; DECISIONS U-21; STATE restore guard | SPECIFIED/BLOCKED_EXTERNAL_SYNC |

## 2. Status interpretation

- SPECIFIED — logical behavior and owner are described; runtime proof is not implied.
- VERIFIED_BY_DOC_CHECK — repository/document check directly verified the artifact or boundary.
- PENDING — exact product/B1 decision is intentionally open.
- NOT_IMPLEMENTED — runtime/Android evidence is absent and must be produced by a later slice.
- BLOCKED — use only for a concrete blocker that prevents the specified contract; no current row is marked BLOCKED solely because runtime is not yet implemented.

## 3. Required implementation gates

Before a runtime slice may claim completion:

1. read all six architecture deliverables;
2. implement only the slice scope;
3. add deterministic checks for duplicate effects and stale revisions;
4. run JSON/content validation against the contract;
5. record fresh evidence for the observable rows;
6. do not change pending decisions silently;
7. keep runtime changes outside this architecture folder and review them separately.