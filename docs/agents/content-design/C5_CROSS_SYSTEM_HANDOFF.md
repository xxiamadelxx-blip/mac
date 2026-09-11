# C5 — Cross-system handoff контентного среза

Статус: `HANDOFF_READY_WITH_OPEN_RECONCILIATIONS`

Repository: `xxiamadelxx-blip/mac`  
Проверенный baseline перед записью: `6d7c2a361944ada398622e77c2436a79a47baf46`  
Срез: C5  
Дата: 2026-09-10

Этот документ закрывает C5 из `AGENT_TASK.md`: сводит C1–C4, META passive tree и живые контракты Architecture / Balance / Runtime / Visual Lab. Он не является runtime implementation, numeric balance lock, product approval, visual approval или production-asset delivery.

## 1. Результат и аудитория

Цель C5 — дать следующим агентам один проверяемый handoff: какие стабильные ID уже описаны, какие поля должны связаться между системами, где есть дубли или конфликтующие источники и какой следующий владелец снимает каждый блокер.

Критерий успеха:

- C1–C4 и `META_PASSIVE_TREE.md` доступны через каталог и не получают новых скрытых чисел;
- каждый контентный поток имеет source, status, consumer и next owner;
- boss chest, artifact offer, arena drop, XP, aftermath и wallet не смешаны;
- пять синергий остаются верхним лимитом claims первого забега, но это не означает принудительное получение пяти синергий;
- главный босс и мини-босс явно разделены по clock policy;
- все несовпадения live-репозитория записаны как решения с владельцем, а не исправлены догадкой;
- C5 не создаёт mockup, sprite, texture, scene или runtime-код.

## 2. Сводка контента и состояния registry

| Поток | Content design сейчас | Live Architecture registry сейчас | Статус handoff |
|---|---|---|---|
| Weapons | 10 stable IDs, слоты 6, max level 10 для synergy gate | 10 records; architecture progression cap требует сверки | `CONTENT_SPECIFIED / PROGRESSION_RECONCILIATION_PENDING` |
| Run passives | 10 stable IDs, слоты 6, max rank 10 для synergy gate; каждая passive даёт общую выгоду и лишь имеет weapon binding для eligibility синергии | 10 records; architecture progression cap требует сверки | `CONTENT_SPECIFIED / PROGRESSION_RECONCILIATION_PENDING` |
| Synergies / evolutions | 10 direct weapon + passive pairs, max 5 claims per run | 10 records; evaluator contract есть | `CONTENT_SPECIFIED`, numeric binding pending |
| Run artifacts | 10 IDs, отдельный от passive slot поток, offer ровно 3 карты; C2 теперь задаёт 10 semantic effect keys и content defaults для refresh/duplicate | 8 records; `artifact_tideglass` и `artifact_silent_lantern` не синхронизированы; runtime `artifact_effects.definitions` пуст | `CONTENT_SPECIFIED`, `REGISTRY_SYNC_PENDING` |
| Future enemies | 4 proposals: `enemy_lotus_usher`, `enemy_moonroot_burrower`, `enemy_silver_reed_seer`, `enemy_moontrail_stalker` | 10 base enemies; extension slots присутствуют как null records | `CONTENT_SPECIFIED`, balance/registry pending |
| Mini-bosses | C3 теперь описывает 5: `miniboss_ink_jade_warden`, `miniboss_veil_harvester`, `miniboss_lotus_ritekeeper`, `miniboss_bell_rhythm_ascetic`, `miniboss_moonroot_ferryman` | Architecture содержит 5 intermediate records, третий — `miniboss_extension_slot_03` без identity; live B1 Registry, по R3 handoff, пока содержит 0 mini-boss records | `CONTENT_SPECIFIED`, registry sync conflict |
| Main bosses | C3 добавляет content proposals `boss_tideglass_regent` и `boss_omen_paper_archivist` для slots 04/05 | 6 records, из них `boss_extension_slot_04` и `boss_extension_slot_05` пока без synchronized identity | `CONTENT_SPECIFIED`, registry sync pending |
| Arena drops | C4 описывает 7 IDs и effect intent | `RunSession.drops` содержит только XP и aftermath; typed arena-drop registry/event contract отсутствует | `CONTENT_SPECIFIED`, runtime/architecture pending |
| Meta passive tree | 6 branches, 17 stat nodes, branch cap 10, node cap 5, currency Gold, applies next run | отдельный C5 join с Shop/Meta persistence ещё не подтверждён | `CONTENT_SPECIFIED`, balance/runtime pending |

Артефактные и passive ID с похожими названиями не являются collision: `artifact_mirror_shard` и `passive_mirror_shard` находятся в разных типизированных scope. В UI и telemetry используются scope-qualified IDs, а не только display name.

## 3. Reconciliation текущего run target

Ниже не новая игровая идея, а результат сравнения live-файлов. Пока владелец не подтвердит строку, Content Agent не переименовывает extension slots и не добавляет отсутствующие записи.

| Тема | Что найдено | Рабочая передача C5 | Владелец решения |
|---|---|---|---|
| Envelope | `FIRST_RUN_DATA_CONTRACT.json` задаёт 1800 секунд и main checkpoints 300/600/900/1200/1500/1800; `BALANCE_MODEL.json` содержит 30-minute model-only extension; `GAME_MANIFEST.md` и B1 wave table/acceptance сохраняют legacy 20 минут | Для новых consumer contracts использовать 1800-секундный target с пометкой `PENDING_B1/PRODUCT`; не переписывать legacy source в C5 | Product + Architecture + Balance |
| Main-boss clock | Runtime acceptance/context фиксируют: MAIN_BOSS freeze run-clock и обычных wave/XP/spawn clocks от intro до settlement, отдельно идёт encounter clock. Data contract одновременно говорит, что clock advances в `BOSS_INTRO/BOSS_ACTIVE` для каждого boss | Runtime handoff следует принятому freeze/continuation поведению из runtime acceptance; data contract требует reconciliation до implementation | Architecture + Runtime |
| Mini-boss clock | Runtime acceptance/context: MINI_BOSS не останавливает run clock, wave, XP и ordinary spawn | Сохранить continuation policy; chest claim не должен задним числом замораживать elapsed time | Runtime + Architecture |
| Mini-boss count | C3 content теперь описывает канонический content target 5; data contract содержит 5 intermediate records; runtime acceptance требует 5; R3 handoff reports 0 records in the live B1 Registry | Schedule, chest capacity, Visual Lab intake and Balance cadence still cannot join by ID | High: counts and named IDs are inspectable | Architecture/Runtime sync the five stable IDs; Content не добавляет шестой ID без нового решения |
| Main-boss roster | Architecture/runtime acceptance требуют 6 records; два extension slots не имеют synchronized identity; legacy manifest говорит о 4 bosses | Content proposals для slots 04/05 готовы; Architecture/Runtime должны сопоставить их с versioned records после envelope reconciliation | Content → Architecture/Runtime |
| Chest capacity | Data contract: максимум 15 windows = 8 configured non-final boss windows + 7 reserved additional windows; C3 content proposal теперь раскладывает 10 BOSS_CHEST windows + 5 ELITE_CHEST windows | Сопоставить content window groups C01–C15 с canonical source_kind; ELITE_CHEST не расходует synergy cap | Product + Architecture + Balance |
| Final source | Non-final boss chest: synergy/evolution/fallback; final boss at 1800: victory без boss chest | `boss_black_moon_empress` остаётся `NO_CHEST`; first-clear artifact offer отдельна от final boss chest | Architecture + Runtime |
| Elite variants | Runtime acceptance разрешает bounded elite-tagged ordinary enemy с отдельным `ELITE_CHEST`; data contract оставляет profiles pending | Вариант не становится permanent roster и не открывает artifact offer автоматически; cadence/budget/visual marker остаются pending | Balance + Runtime + Visual Lab |
| Progression gate | C1 content требует weapon level 10 + passive rank 10; текущая architecture/legacy manifest всё ещё содержит 6/5 | Сохранить 10/10 как content target и вынести сверку cap в отдельный consumer contract; не менять root/architecture в content-задаче | Product + Architecture + Balance |

### 3.1 Иерархия решений

При конфликте применяется порядок из `CONTENT_CONTEXT.md`: явное решение владельца → project context → architecture → balance → Visual Lab policy → фактический runtime → старые proposals. Ниже перечисленные конфликты не разрешаются молча, потому что они меняют расписание, reward count или restore semantics.

## 4. Dependency matrix

| Контракт / пакет | Что передаётся | Главные consumers | Что доказано сейчас | Следующий шаг / evidence |
|---|---|---|---|---|
| C1 weapon catalog | stable `weapon_id`, attack decision, lifecycle, trade-off, balance fields | `ContentRegistry`, `WeaponSystem`, `SynergyEvaluator`, HUD, Visual Lab | 10 entries + 10 direct synergy links | Balance binds numbers; Runtime resolves IDs; Visual Lab делает brief/asset intake |
| C1 passive catalog | stable `passive_id`, global stat/behavior axis, trigger, stacking intent, weapon eligibility binding | `BuildInventory`, `StatsAggregator`, `SynergyEvaluator`, HUD | 10 entries; passive не является улучшением только одного weapon | Проверить duplicate/stacking и объединение статов без weapon-specific side effect |
| C1 synergy catalog | `synergy_id`, required weapon/passive pair, evolution output, claim guard | `SynergyEvaluator`, `BossChestSystem`, `RunSession.build`, ResultProjection | 10 records, cap 5, final boss chest forbidden | Runtime trace: one claim per chest/outcome; Balance route simulation |
| C2 artifact catalog | `artifact_id`, semantic effect key, typed effect intent, trigger/target/scope, stacking/counterplay | `ArtifactOfferSystem`, `StatsAggregator`, HUD, ResultProjection | 10 content entries, 10 semantic effect keys; offer contract exactly 3 cards; no passive slot usage | Architecture syncs 2 missing records and runtime definitions; Balance binds values |
| META passive tree | branch/node IDs, rank loop, Gold wallet, next-run application | Shop UI, `MetaProgression`, persistence, wallet ledger | 6 branches/17 nodes in content doc/index | Balance binds costs/ranks; Runtime proves purchase, save and next-run application |
| C3 future enemies | role, silhouette brief, telegraph, counter-decision, XP/drop boundary | `ContentRegistry`, `WaveDirector`, Combat, Visual Lab | 4 proposals, no runtime roster replacement | Balance supplies profiles; Runtime consumes versioned records only after approval |
| C3 boss/miniboss flow | 5 mini-boss IDs, 2 main-boss extension proposals, phases, telegraph, defeat, chest/fallback boundary | `BossDirector`, `SimulationClock`, `ChestWindowRegistry`, `RewardLedger` | 5 named mini-boss proposals and 2 main-boss content proposals; registry sync remains pending | Architecture/Runtime add versioned records and schedule/settlement trace |
| C4 arena drops | drop ID, pickup, effect intent, limitation, feedback, pending numeric fields | `DropResolver`, `RunSession`, `WaveDirector`, Combat, HUD, RewardLedger only where typed | 7 content entries; XP/aftermath separation preserved | Architecture defines typed instance + spawn/collect events; Balance binds cadence/quantity |
| First-run data contract | immutable versioned registry, session/build/offer/ledger shapes | all run systems, save/replay, diagnostics | schema v2 and stable ID policy exist; some registry arrays contain null placeholders | Reconcile clock/roster/artifact/drop fields before implementation |
| Event catalog | command/event ownership, source IDs, idempotency | Runtime, persistence, telemetry, UI projection | generic chest/window and variant events are specified | Add/approve arena-drop event contract and replay cases |
| Balance B1 | wave budgets, caps, XP, reward values, costs and performance limits | Wave/Combat/Progression/Reward systems | `BALANCE_MODEL.json` has a 30-minute proposed model; B1 wave table/acceptance remain a 20-minute baseline and runtime integration is not implemented | Product/B1 must promote or revise the model; no numbers copied into content docs |
| Visual Lab | visual brief, readable signal, provenance and production handoff | art pipeline, UI/HUD, VFX/SFX, QA | C1–C4 briefs exist; no mockups/assets created by Content | Intake existing briefs; create only approved extension/variant records |

### 4.1 Ownership boundary

- Content owns semantic identity, fantasy, readable behavior, eligibility, counterplay and text contract.
- Balance owns damage, HP, speed, cooldown, range, frequency, quantity, duration, radius, caps, costs and performance budgets.
- Architecture/Runtime owns schemas, state transitions, event versioning, persistence, replay, idempotency and actual effect application.
- Visual Lab owns production-ready visual briefs, candidates, masters, provenance and review gates.
- Product owner resolves time envelope, roster count, reward taxonomy and unknown effect policies.

## 5. Duplicate, conflict и stale-source review

### P1 — блокирует финальный cross-system acceptance

| ID | Finding → evidence | Impact | Confidence | Next action |
|---|---|---|---|---|
| C5-P1-01 | Clock conflict: `FIRST_RUN_DATA_CONTRACT.json` says boss clock advances for every boss; `RUNTIME_CONTEXT.md` and `RUNTIME_ACCEPTANCE.md` say main freezes while mini continues | Replay, wave timing, XP and boss settlement will diverge between Architecture and Runtime | High: both statements are explicit live text | Architecture publishes one canonical `clock_policy`; Runtime updates trace contract; C5 index stays flagged until then |
| C5-P1-02 | Mini roster mismatch: C3 content now has 5 named records, живой архитектурный контракт имеет 5 mini-boss records, runtime acceptance has target 5, while текущая B1 model содержит 5 mini-boss records, а runtime proof отсутствует | Schedule, chest capacity, Visual Lab intake and Balance cadence cannot join by ID until registry is synchronized | High: counts and named IDs are inspectable | Architecture/Runtime sync the five content IDs into approved slots; no sixth ID is introduced by Content |
| C5-P1-03 | Artifact gap: content/index = 10 and C2 now provides 10 semantic effect keys, while architecture `content_registry.artifacts` = 8 and runtime `artifact_effects.definitions` is empty | Two cards cannot load from a single immutable registry; runtime effect projection still has no typed definitions | High | Architecture syncs the two IDs and runtime effect definitions; Balance binds numeric parameters; Content does not edit Architecture schema |
| C5-P1-04 | Time-source drift: Architecture target = 30:00; `GAME_MANIFEST.md`, B1 wave table and Balance acceptance retain 20:00/old four-boss or five-band assumptions | Wave/reward values and final checkpoint are unsafe to bind; balance evidence cannot be called final | High | Product/Architecture/B1 publish source-of-truth update; keep old files marked legacy until changed by their owners |
| C5-P1-05 | Chest taxonomy drift: data contract has 15 total windows with 10+5 source split; C3 content now maps C01–C10 to boss chests and C11–C15 to elite chests | A reserved chest may be accidentally counted as synergy, artifact or extra claim | High | Architecture maps C01–C15 to canonical `source_kind` and outcome policy; Product confirms whether content proposal replaces 8+7 split |
| C5-P1-06 | Content synergy gate is 10/10 while current architecture/legacy sources still expose 6/5 | Eligibility and upgrade cards cannot be joined without one canonical progression cap | High | Architecture/Runtime/Balance publish the 10/10 consumer contract; Content keeps the gate PROPOSED until reconciliation |

### P2 — must be resolved before implementation handoff

| ID | Finding → evidence | Impact | Confidence | Next action |
|---|---|---|---|---|
| C5-P2-01 | C4 arena drops are not present as typed `RunSession` drop records; current session lists only XP and aftermath | Drop pickup cannot be replay-safe or projected consistently | High | Architecture adds typed drop instance/event contract; Content remains effect-intent owner |
| C5-P2-02 | `enemy_extension_slots` and `enemy_variants` are present as null records; variant numeric/visual profiles are pending | Spawner cannot safely resolve a null record; Visual Lab lacks a concrete brief target | High | Balance supplies profile refs; Content/Visual Lab names only approved records; Runtime quarantines null IDs |
| C5-P2-03 | Artifact refresh, duplicate and stacking policies remain pending in data contract | A three-card offer can produce non-deterministic power or save behavior | High | Product approves policy, then Balance binds values and Runtime adds idempotency tests |
| C5-P2-04 | `artifact_mirror_shard` and `passive_mirror_shard`, plus `passive_heavenly_seal` and `synergy_heavenly_seals`, are close display names | Player-facing cards can look duplicated even though stable IDs are scoped | Medium | UI uses type badge + scope-qualified copy; Creative review may rename display labels without changing IDs |
| C5-P2-05 | C4 resource semantics keep XP vs mana label pending, and `arena_drop_coin_cache` proposes Gold while wallet ownership belongs to ledger | Pickup feedback and economy attribution can be wrong | High | Product resolves label and wallet event; Runtime applies through typed resolver/ledger, never from content text |

Нет P0 finding: текущий scope — documentation handoff, а не запуск незавершённого runtime. Но P1 findings блокируют `APPROVED`/`IMPLEMENTED` статус каталога.

## 6. Balance handoff

### 6.1 C1–C2 build content

Balance получает 10 weapon profiles, 10 общих run-passives и 10 direct evolutions. Для каждого weapon нужны numeric bindings для damage, cooldown, count, range/area, targeting, projectile lifetime и performance budget. Для каждой passive нужны axis, rank curve, affected stat/system, trigger и stacking rule.

Ключевое ограничение после пользовательской переработки: passive может быть привязана к weapon только в поле eligibility для соответствующей synergy. Её базовая выгода должна действовать на общий build/stat system и не превращаться в скрытый modifier одного weapon. Balance должен отдельно проверить:

1. baseline passive без соответствующего weapon;
2. passive + weapon как обычный build;
3. weapon level 10 + passive rank 10 как synergy eligibility;
4. пять claims в одном run без forced fifth claim;
5. duplicate offer и уже claimed synergy.

### 6.2 C3 encounters and chests

Balance должен привязать TTK, pressure, post-boss relief/ramp, XP, checkpoint rewards, chest source cadence и fallback value после решения roster. Main/mini clock behavior берётся из согласованного runtime contract. Final boss reward не создаёт boss chest. `ELITE_CHEST` и `MINI_BOSS_CHEST` остаются отдельными источниками от artifact offer.

До reconciliation 20→30 нельзя считать старые five-band values из B1 wave table доказательством полного 30-minute run. Новые 30-minute bands в `BALANCE_MODEL.json` имеют proposed/model-only provenance и не являются runtime или product lock. Старые числа остаются legacy evidence.

### 6.3 C4 arena drops

Balance получает семь IDs:

| ID | Что балансирует | Нельзя менять в numeric binding |
|---|---|---|
| `arena_drop_heal_mote` | frequency, heal amount, pickup radius | не превращать в XP или persistent wallet |
| `arena_drop_coin_cache` | frequency, Gold quantity, source attribution | не начислять Gold напрямую из UI/content description |
| `arena_drop_xp_magnet` | frequency, radius, duration, target whitelist | не смешивать с aftermath; XP/mana label pending |
| `arena_drop_destruction_seal` | frequency, eligible target, removal/destroy resolution, cap | не создавать повторный XP/reward без idempotency rule |
| `arena_drop_wave_freeze` | frequency, duration, scope, resume behavior | не останавливать main run clock автоматически |
| `arena_drop_ward_shard` | frequency, mitigation, stack/lethal rule | не менять permanent defense без approved scope |
| `arena_drop_vacuum_bloom` | frequency, radius, duration, target whitelist | не притягивать запрещённые сущности или wallet без policy |

Ожидаемое Balance evidence: seeded source table, per-band cadence, quantity/radius/duration/cap values, economy attribution и performance bound. Content Agent не дублирует эти значения в каталоге.

## 7. Runtime / Architecture handoff

### 7.1 Registry and session

1. `ContentRegistry` должен загрузить ровно одну versioned запись для каждого approved ID. Null extension record не считается playable content и должен быть rejected/quarantined.
2. Синхронизировать два артефакта и десять content semantic effect keys с typed `artifact_effects.definitions` до включения их в offer pool.
3. После решения roster заменить placeholder slots только stable semantic IDs; display labels и visual asset paths не используются как keys.
4. Для C4 нужен отдельный typed `ArenaDropInstance`/эквивалент в `RunSession.drops`; он не объединяется с `xp_items` или `aftermath_items`.
5. Drop effect application принадлежит Runtime resolver. Content entry не мутирует `RewardLedger`, wallet или `RunSession` напрямую.

### 7.2 Events and idempotency

Уже существующие generic boundaries, которые нужно использовать:

- `chest_window_triggered.v1` → `chest_offer_created.v1` → `chest_claimed.v1` → `chest_outcome_applied.v1`;
- `boss_chest_opened.v1` / `boss_chest_claimed.v1` только как source-specific projection для `BOSS_CHEST`;
- `enemy_variant_selected.v1` для deterministic variant selection;
- `post_boss_relief_started.v1` перед следующим ramp.

Для C4 Architecture/Runtime должен утвердить отдельные versioned events, например `arena_drop_spawned.v1` и `arena_drop_collected.v1`, с `run_id`, `content_version`, `drop_instance_id`, `drop_id`, `source_id`, `state_revision` и `idempotency_key`. Это handoff gap, а не заявление, что события уже реализованы.

Обязательные guards:

- duplicate pickup не повторяет heal, Gold, XP, effect или removal;
- duplicate chest claim не повторяет synergy/evolution/fallback;
- final boss не создаёт chest offer;
- artifact offer всегда имеет 3 candidates, одна выбранная карта создаёт один active effect и не занимает weapon/passive slot;
- mini-boss outcome не замораживает run clock задним числом;
- main-boss freeze и resume дают наблюдаемую пару before/after values;
- save/reconnect сохраняют content version, offer IDs, claimed window IDs и ledger cursor.

### 7.3 Clock and chest boundary

До исправления data contract Runtime должен не кодировать обе взаимоисключающие политики. При reconciliation требуются отдельные observable values:

- `run_elapsed_seconds`;
- `encounter_elapsed_seconds`;
- `wave_progress_seconds`;
- `xp_spawn/collection` cursor;
- `chest_window_id`, `source_kind`, `outcome_type`;
- `synergy_claimed_count`.

`arena_drop_wave_freeze` имеет scope только на разрешённую simulation/wave subsystem. Он не меняет `run_elapsed_seconds`, checkpoint identity или reward ledger, если Product отдельно не утвердит иное.

## 8. Visual Lab brief handoff

Content передаёт briefs, но не mockups и не production assets.

| Intake | Brief source | Обязательный визуальный сигнал |
|---|---|---|
| 10 weapons + 10 passives + 10 synergies | `C1_WEAPONS_PASSIVES_SYNERGIES.md` | weapon/passive/synergy должны различаться формой, silhouette и role; pair readable в offer UI |
| 10 artifacts | `C2_ARTIFACTS.md` | отдельный artifact language; не копировать passive-slot iconography; три-card offer readable |
| 5 named mini-bosses + 2 main-boss extension proposals + 4 future enemies | `C3_MINI_BOSSES_AND_CHEST_FLOW.md` | silhouette, signature, telegraph, reaction window, counter-decision; corpse/XP boundary | `candidate_id: null`, `PROPOSAL`, `NOT_PROMOTED` |
| 7 arena drops | `C4_ARENA_DROP_CATALOGUE.md` | pickup silhouette + world feedback; heal/Gold/XP/control/defense/vacuum signals не должны сливаться |
| Beetle variants | Architecture enemy variant policy | detail/marker beyond hue; variant не должен быть только recolor |
| Main/miniboss extension slots | C5 reconciliation | не производить assets до решения roster и stable identity |

Visual Lab проверяет briefs по своему `visual_lab/README.md` и review checklist. В C5 не добавляются candidate IDs, image files, sprites, mockups или ссылки на несуществующие assets.

## 9. Open product decisions

| Decision ID | Вопрос | Что блокирует | Владелец |
|---|---|---|---|
| C5-D01 | Финальный envelope первого забега — 20 минут legacy или 30 минут current target? | checkpoint schedule, B1 bands, manifest, reward values | Product + Architecture + Balance |
| C5-D02 | Какая единая clock policy для MAIN_BOSS: freeze или advance? | wave/XP/spawn replay, runtime acceptance | Architecture + Runtime |
| C5-D03 | Как синхронизировать канонический content roster из 5 mini-bosses с data contract (3 records) и live B1 Registry (0 records)? | stable roster, cadence, chest windows, Visual Lab scope | Architecture + Runtime; Product только при изменении канонического решения |
| C5-D04 | Как сопоставить готовые content proposals `boss_tideglass_regent`, `boss_omen_paper_archivist` и пять mini-boss IDs с versioned Registry records? | registry, balance profile, telegraph, schedule | Architecture + Runtime; Content поддерживает semantic fields |
| C5-D05 | Как именно разложить 15 chest windows: 8 configured boss windows + 7 additional sources? | synergy eligibility, fallback, reward ledger | Product + Architecture + Balance |
| C5-D06 | Какие дополнительные источники дают chest, а какие дают artifact offer? | UI state, offer source, idempotency | Product + Runtime |
| C5-D07 | Синхронизировать ли сразу `artifact_tideglass`/`artifact_silent_lantern` и какие typed effects им разрешены? | ContentRegistry, offer pool, Balance | Product + Architecture + Balance |
| C5-D08 | Refresh, duplicate и stacking policy для artifacts | power curve, save/replay, UI copy | Product + Balance + Runtime |
| C5-D09 | Cadence, budget, expiry и size bounded elite variants | ELITE_CHEST frequency, wave pressure, VFX | Balance + Runtime + Visual Lab |
| C5-D10 | XP или mana — player-facing label для collection/magnet systems? | HUD, C4 XP magnet, meta magnet | Product + Architecture |
| C5-D11 | Destruction seal: remove, destroy, or reward-producing defeat? | XP, aftermath, ledger and replay | Product + Balance + Runtime |
| C5-D12 | Какие arena drops сохраняются только в run, а какие входят в aftermath/result? | RunSession, save, RewardLedger | Product + Architecture |

Пока решения не приняты, unresolved fields остаются `PENDING_*`; C5 не подменяет их числами или новыми ID.

## 10. Acceptance evidence

### Проверено перед C5

- live `main` fetched at `ec30c239aa22aa1d9c8ad1faab25d99633f4cb29`;
- `FIRST_RUN_DATA_CONTRACT.json` parseable, содержит schema v2, 10 weapons, 10 passives, 10 synergies, 6 main-boss records, 5 intermediate records, 15 chest-window records и 8 artifact records; content target remains 10;
- Content Catalog index содержит 10 weapons, 10 passives, 10 synergies, 10 artifacts, 5 named mini-bosses, 2 main-boss extension proposals, 7 arena drops и 17 meta nodes;
- `RUNTIME_ACCEPTANCE.md` остаётся `NOT_IMPLEMENTED` для полного R2/R3 acceptance, а `R3_RUNTIME_HANDOFF.md` имеет статус `RUNTIME_VERIFICATION_BLOCKED`: runner не выделил steps, поэтому C5 не объявляет run playable;
- `R1_RUNTIME_HANDOFF.md` не используется как доказательство boss/chest/artifact implementation: сам документ оставляет их более поздними slices;
- `BALANCE_ACCEPTANCE_MATRIX.md` маркирует модель как `SIMULATED_MODEL_ONLY / PARTIAL`, а 30-minute extension не считается numeric lock;
- Visual Lab brief boundary сохранена: никаких mockup/asset changes.

### Гейт C5

| Gate | Expected evidence | C5 result |
|---|---|---|
| Catalog index | JSON parse, stable IDs, source refs, statuses, gaps | `READY_WITH_OPEN_RECONCILIATIONS` |
| Dependency matrix | C1–C4/META → Registry/Runtime/Balance/Visual consumers | `SPECIFIED` |
| Duplicate review | no unqualified ID collision; display-name collisions noted | `PASS_WITH_UI_NOTE` |
| Conflict review | each P1/P2 has evidence, impact, confidence, owner and next action | `PASS_WITH_P1_BLOCKERS` |
| Balance handoff | no new numeric values; pending fields named | `READY_FOR_B1` |
| Runtime handoff | state/event/idempotency boundaries named; missing drop events explicit | `READY_FOR_ARCHITECTURE_RECONCILIATION` |
| Visual handoff | briefs referenced; no mocks/assets | `BRIEF_ONLY` |
| Scope | docs-only content-design files; no architecture/balance/runtime/visual policy edits | `REQUIRED` |

Итоговый статус C5: `HANDOFF_READY_WITH_OPEN_RECONCILIATIONS`. Это не `APPROVED`, `IMPLEMENTED`, `VERIFIED`, `PLAYABLE` или `PRODUCTION`.

## 11. Следующий модуль и граница scope

1. Product/Architecture закрывают C5-P1-01, C5-P1-04 и C5-P1-05; roster из пяти mini-bosses и два main-boss proposals уже зафиксированы Content Agent.
2. Balance Agent делает numeric binding только после решения envelope/roster/chest taxonomy и добавляет 30-minute evidence.
3. Runtime Agent синхронизирует registry с пятью mini-boss IDs и двумя main-boss proposals, typed artifact/drop contracts, event idempotency и clock traces.
4. Visual Lab принимает готовые briefs и работает в своих protected stages.
5. Content Agent не расширяет C5 новыми предметами. Новая механика, weapon, passive, artifact, boss, enemy или drop оформляется отдельным proposal с новым scope.

## 12. Актуальная сверка C5

Родительский main: ec30c239aa22aa1d9c8ad1faab25d99633f4cb29. Этот раздел заменяет старые числовые снимки C5, если они расходятся с живыми источниками.

| Область | Живое состояние | Контентный вывод |
|---|---|---|
| Расписание | архитектура: 0 главных записей и 5 мини-боссов; 1800 секунд | контентная сетка 6 + 5 совпадает структурно |
| Окна наград | 10 BOSS_CHEST и 5 ELITE_CHEST; финальный босс без сундука | схема C01–C15 закрыта на уровне контента |
| Баланс | модель PARTIAL; 5 мини-боссов и 10 вариантов элит опубликованы | числа и cadence не заблокированы |
| Синергии | 10-й уровень оружия + 10-й ранг пассивки; максимум 5 | условие остаётся content target до единого consumer cap |
| Артефакты | контент 10; архитектура 8; определения эффектов 0 | два ID и typed effects требуют внешней синхронизации |

Структурно закрыты: clock policy, пятёрка мини-боссов, два расширения главных боссов, 30-минутная сетка и разделение 10+5 окон. Открыты только внешние стыки и доказательства.

Нет изменений в Architecture, Balance, Runtime, Visual Lab, мокапах или бинарных ассетах.
