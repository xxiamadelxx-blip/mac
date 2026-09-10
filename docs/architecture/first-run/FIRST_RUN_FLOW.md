# FIRST_RUN_FLOW — логический пользовательский маршрут первого забега

Статус: VERIFIED ARCHITECTURE SPECIFICATION
Runtime implemented: NO
Android acceptance: NOT_PERFORMED

> Revision 2: этот flow теперь описывает 30-минутный target run, schedule-driven encounters, до 15 chest windows и cycle-based wave pressure. Runtime implemented: NO.

Документ описывает наблюдаемое поведение от включения игры до возврата в меню. Он не утверждает, что описанные состояния уже реализованы в Godot.

## 1. Границы и источники

Цель — дать runtime-агенту последовательный контракт первого 30-минутного забега:

включение → загрузка → меню → ПЕРСОНАЖИ → подготовка → арена → волны → XP/уровни → улучшения → промежуточные боссы → checkpoint/сундук → следующая полоса; финальный босс → финальная награда → победа или поражение → результат → rewards → меню.

Канонические источники:

- [AGENT_TASK.md](./AGENT_TASK.md) — обязательный scope и критерии.
- [GAME_MANIFEST.md](../../../GAME_MANIFEST.md) — пользовательский цикл, roster и M1.
- [AGENT_CONTEXT.md](../../../AGENT_CONTEXT.md) — текущий контекст и границы.
- [BALANCE_ECONOMY_SPEC.md](../../../docs/BALANCE_ECONOMY_SPEC.md) — единственный источник чисел.
- [FIRST_RUN_DATA_CONTRACT.json](./FIRST_RUN_DATA_CONTRACT.json) — machine-readable форма этого контракта.
- [FIRST_RUN_STATE_MACHINE.md](./FIRST_RUN_STATE_MACHINE.md) — формальные переходы.
- [FIRST_RUN_EVENT_CATALOG.md](./FIRST_RUN_EVENT_CATALOG.md) — события и повторная доставка.

## 2. Термины и authority

- ПЕРСОНАЖИ — пользовательский label меню; доменные идентификаторы персонажей могут называться hero_id.
- RunSession — единственный источник истины незавершённого забега.
- UI — только read model и отправитель команд; UI не меняет RunSession напрямую.
- Content Registry — версия неизменяемых данных персонажей, оружия, пассивок, синергий, врагов, боссов, волн и наград.
- Reward Ledger — долговечный журнал применённых наград; запись ledger и изменение кошелька выполняются одной транзакционной операцией persistence boundary.
- XPDrop и AftermathItem — разные сущности и разные визуальные/жизненные циклы.
- «Спроектировано» ниже не означает «реализовано».

## 3. Сквозной flow

| Шаг | Actor/trigger | Preconditions | Целевое состояние и owner | Что видит пользователь | Ошибка и recovery |
|---|---|---|---|---|---|
| 1. Boot | Запуск приложения | Доступен AppShell | APP_BOOT, AppShell | Splash/loading без игровых обещаний | Ошибка оболочки → диагностический экран; повторная загрузка не создаёт RunSession |
| 2. Content loading | AppShell запрашивает Content Registry и SaveSnapshot | Версия схемы известна | CONTENT_LOADING, ContentLoader | Индикатор загрузки | Отсутствующий обязательный content → CONTENT_ERROR; показана причина и доступно возвращение в меню без запуска |
| 3. Main menu | Content loaded или безопасный fallback | Меню и локализация доступны | MAIN_MENU, MenuFlow | Старт, ПЕРСОНАЖИ, Арсенал, Артефакты, Настройки | Недоступный раздел получает disabled/diagnostic состояние, но не белый экран |
| 4. Settings | Пользователь открывает Настройки | MAIN_MENU или pause context | SETTINGS, SettingsFlow | Звук, доступность и прочие реально доступные настройки | Неизвестная настройка игнорируется с diagnostic entry; возврат сохраняет только валидированные значения |
| 5. Characters | Пользователь открывает ПЕРСОНАЖИ | Registry содержит selectable character | CHARACTER_SELECT, MenuFlow | Имя, portrait/full-body reference, стартовое оружие, активная способность, role и ограничения | Повреждённая карточка → placeholder с идентификатором ошибки; выбор такого персонажа запрещён |
| 6. Character selection | Нажатие на карточку | character_id существует и unlocked | CHARACTER_SELECT, RunSetupModel | Выбранная карточка и её стартовые свойства | Повторное нажатие идемпотентно; неизвестный ID отклоняется |
| 7. Run setup | Пользователь нажимает «Начать забег» | Персонаж выбран; artifact pre-run selection отсутствует | RUN_SETUP → RUN_LOADING, RunCoordinator | Selected character и подтверждение старта; артефакты не экипируются заранее | Любая попытка передать artifact_ids отклоняется; RunSession ещё не создаётся |
| 8. Run creation | Confirm start command | Content version и save revision согласованы | RUN_LOADING, RunCoordinator создаёт RunSession | Loading screen | Ошибка создания/seed → CONTENT_ERROR или MAIN_MENU; частичный RunSession не считается начатым |
| 9. Arena load | RunCoordinator загружает карту | RunSession создана, arena contract найден | RUN_ACTIVE, Arena/Simulation adapters | Героиня в стартовой точке, HUD и открытое поле | Ошибка visual/runtime resource → fallback + diagnostic; запуск запрещён только при отсутствии обязательного gameplay resource |
| 10. Active simulation | Clock tick | Не paused, RunSession active | RUN_ACTIVE, RunSession + SimulationClock | Движение, автоматическое оружие, враги, HUD, XP и aftermath | Ошибка одного декоративного ресурса не останавливает simulation; ошибка authoritative state переводит в recoverable pause |
| 11. Wave cycle/phase | Elapsed time или encounter boundary пересекает registry boundary | RunSession active | RUN_ACTIVE, WaveDirector | После boss — relief, затем постепенный ramp к следующему peak; состав/варианты/pressure читаются из data | Повторный tick той же boundary не создаёт вторую фазу; missing extension profile → diagnostic/pending gate |
| 12. XP and level | XPDrop collected | Drop ещё не collected; magnet/line-of-sight разрешены | RUN_ACTIVE или UPGRADE_OFFER, ProgressionSystem | XP bar, level-up и readable pickup | Повторная доставка pickup не увеличивает XP; потерянный drop остаётся отдельной диагностируемой записью |
| 13. Upgrade offer | Level-up command | Simulation can freeze; content offer pool valid | UPGRADE_OFFER, ProgressionSystem | Ровно три offer projection, current/new values и slot state | Невалидная карта отклоняется; offer сохраняется до выбора/отмены по policy |
| 14. Upgrade chosen | Пользователь выбирает карточку | Offer open, choice belongs to offer | RUN_ACTIVE или UPGRADE_OFFER | Изменившийся build и stats | Повторный выбор того же offer → duplicate/no-op; stale offer требует открыть новый valid projection |
| 15. Weapon/passive slot | Chosen offer adds content | Slot available or upgrade target exists | RUN_ACTIVE, BuildInventory | Weapon/passive level и доступные слоты | Полный слот исключает illegal new-item offer; если pool исчерпан, fallback outcome помечен в offer contract |
| 16. Encounter checkpoint | Clock достигает scheduled main/intermediate checkpoint | Нужная encounter record и cycle phase loaded; boss state не останавливает elapsed time | BOSS_INTRO → BOSS_ACTIVE, BossDirector | Main boss или intermediate boss, health bar, telegraph и controlled ordinary spawn | Encounter не может появиться внутри персонажа; invalid spawn → deterministic safe spawn retry и diagnostic |
| 17. Boss combat | Boss pattern event | Boss active; elapsed time continues for every boss | BOSS_ACTIVE, Combat/BossDirector | Wind-up, telegraph, reaction window, damage | Повторный boss spawn с тем же checkpoint_id ignored; отсутствие telegraph — contract failure |
| 18. Boss defeated | Authoritative defeat | Boss active и HP <= zero | CHECKPOINT_SETTLEMENT, RunCoordinator | Death beat; settlement промежуточного или финального босса | Повторный defeat event не повторяет rewards; повреждённое result → recoverable checkpoint state |
| 19. Checkpoint reward | Settlement command | checkpoint_id not settled | CHECKPOINT_SETTLEMENT, RewardLedger | Gold, Lunar Seals, Boss Essence и ledger status | Для финального босса это последняя награда перед victory; idempotency key не допускает повтор |
| 20. Chest window | Non-final settlement or configured non-boss source trigger | chest_window_id is enabled and not consumed; final boss guard passes | CHEST_OFFER, ChestWindowSystem | Source, offer type, eligibility/fallback and claim state; boss chest remains a typed non-final source | Final boss cannot create a boss chest or generic defeat chest; unconfigured reserved window stays pending; close/reopen preserves offer |
| 21. Boss-chest outcome | Claim non-final boss-chest offer | Offer valid, evaluator result known | RUN_ACTIVE, BossChestSystem | Synergy/evolution или fallback reward согласно offer | Применяется только к нефинальному boss chest; exact fallback values остаются PENDING_PRODUCT_DECISION |
| 22. Elite-pack artifact source | Special elite pack defeated between bosses | Elite encounter is authoritative; cadence/composition policy allows source | ARTIFACT_OFFER, ArtifactOfferSystem | Three-card artifact offer | Elite-pack cadence and card pool remain explicit pending fields |
| 23. Artifact offer choice/refresh | Artifact source opens offer | Exactly three cards; offer owned by current run | ARTIFACT_OFFER → RUN_ACTIVE or RESULT_REVIEW | `Get` selects one card; `Refresh` rerolls the offer only under pending policy | One choice creates one active run effect; no weapon/passive slot is consumed; duplicate commands are idempotent |
| 24. Next stage | Non-final boss-chest claim complete | Reward and boss-chest claim committed | RUN_ACTIVE, RunCoordinator | Следующая wave band и updated HUD | Финальный checkpoint не открывает следующую стадию; повторный command — no-op |
| 25. Pause | User taps pause or Android background | RunSession is resumable | RUN_PAUSED, RunSession | Pause overlay, Continue, Settings, Exit | SimulationClock = paused; save snapshot создаётся только по defined policy |
| 26. Resume | Continue / Android foreground | Snapshot and content version valid | Previous resumable state | Simulation continues without time jump | Invalid snapshot → RECOVERY_REVIEW/diagnostic; rewards не начисляются автоматически |
| 27. Exit attempt | User chooses menu from pause | Confirmation required for active run | Exit confirmation overlay | Ясно указано: abandon или recoverable save policy | Cancel returns to pause; confirm follows abandon policy and не выдаёт незаработанные rewards |
| 28. Death | HP reaches zero | Run active; death not already settled | RUN_DEFEAT → RESULT_REVIEW | Причина смерти, stats, partial rewards | Repeated death event ignored; partial rewards считаются один раз |
| 29. Final boss defeat | Final boss defeated at the terminal 30-minute schedule slot | Final boss result valid and final settlement committed | CHECKPOINT_SETTLEMENT → RUN_VICTORY → RESULT_REVIEW | Финальная награда, victory state, full-run summary | Timer alone не объявляет победу; final boss creates no boss chest; first-clear artifact offer remains post-result and separate |
| 30. Result finalization | User opens/claims result | RUN_DEFEAT or RUN_VICTORY | RESULT_REVIEW → REWARD_COMMITTING | Stats, build, kills, XP, checkpoints, rewards; result_finalized.v1 marks the immutable result boundary | Повторное открытие read-only; claim использует ledger idempotency |
| 31. Return to menu | Result claim or explicit menu action | Result settlement committed or abandon confirmed | MAIN_MENU, MenuFlow | Updated wallets/unlocks and start options | Неудача save → result остаётся recoverable; возврат не теряет committed ledger |
| 32. New run | User starts another run | Previous result committed/abandoned | New RUN_LOADING | New run_id и fresh session | Старый RunSession не переиспользуется |
## 3.1 Revision 2: encounter schedule

The schedule is registry data, not a set of UI branches. checkpoint_reached.v1 carries encounter_kind, encounter_id, checkpoint_id and is_final.

| Order | Target time | Kind | Stable ID | Defeat outcome | Status |
|---:|---:|---|---|---|---|
| 1 | 300 s / 05:00 | MAIN_BOSS | boss_hua_lin | checkpoint reward → chest window | existing |
| 2 | 450 s / 07:30 | INTERMEDIATE_BOSS | miniboss_ink_jade_warden | checkpoint reward → chest window | C3 target |
| 3 | 600 s / 10:00 | MAIN_BOSS | boss_miyeon | checkpoint reward → chest window | existing |
| 4 | 750 s / 12:30 | INTERMEDIATE_BOSS | miniboss_veil_harvester | checkpoint reward → chest window | C3 target |
| 5 | 900 s / 15:00 | MAIN_BOSS | boss_seika | checkpoint reward → chest window | existing |
| 6 | 1200 s / 20:00 | MAIN_BOSS | boss_extension_slot_04 | checkpoint reward → chest window | new content slot; pending registry/B1 |
| 7 | 1350 s / 22:30 | INTERMEDIATE_BOSS | miniboss_extension_slot_03 | checkpoint reward → chest window | new slot; target placement pending approval |
| 8 | 1500 s / 25:00 | MAIN_BOSS | boss_extension_slot_05 | checkpoint reward → chest window | new content slot; pending registry/B1 |
| 9 | 1800 s / 30:00 | MAIN_BOSS / FINAL | boss_black_moon_empress | final settlement → victory; no boss chest | existing identity retimed to terminal slot |

The five-minute main cadence and the 22:30 intermediate placement are working architecture targets derived from the existing cadence and C3 ordering; Product/B1 may replace the seconds through the registry without changing state ownership. There are six main-boss records and three intermediate records, but only eight non-final boss/mini-boss chest windows because the terminal record has no boss chest.

## 3.2 Revision 2: wave cycles and enemy variants

Each main-boss interval is a wave cycle. Every cycle after the first begins with a post-boss relief phase, then rebuilds pressure gradually and reaches a pre-boss peak. BOSS_INTRO and BOSS_ACTIVE consume the same run clock; after settlement/claim the next cycle starts at relief. A boss or mini-boss must never be followed by an immediate jump to the previous peak profile.

| Phase | Owner | Observable rule | Numeric source |
|---|---|---|---|
| OPENING | WaveDirector | readable onboarding pressure before the first scheduled encounter | B1 extension |
| POST_BOSS_RELIEF | WaveDirector | lower pressure after any non-final encounter and chest settlement | B1 extension |
| RAMP | WaveDirector | pressure, composition and allowed variants grow in steps toward the next peak | B1 extension |
| PRE_BOSS_PEAK | WaveDirector | target pressure before the next main/intermediate encounter | B1 extension |
| BOSS_ACTIVE | BossDirector + WaveDirector | controlled ordinary spawn; boss telegraphs remain readable; clock continues | B1 extension |

EnemyVariantResolver selects a variant from content_version, run_seed, wave_cycle_id, base_enemy_id and state_revision and records variant_id in telemetry and the run snapshot. enemy_ink_beetle has three reserved variants. Each variant inherits the base role, XP/drop boundary and aftermath separation unless B1 explicitly overrides a field; it must have a non-color marker/detail and may not silently create a new reward source. Three new enemy slots are registry placeholders only, with names/roles/tuning pending Content/B1.


## 4. Что считается активным забегом

RunSession создаётся только на шаге 8 после подтверждения запуска. В нём фиксируются:

- run_id, seed, content_version и schema_version;
- selected hero_id;
- elapsed_seconds, current wave_band_id, current_stage_id и checkpoint_id;
- current state и resume_state;
- build, stats, XP, level, kills и расширяемый bonus_state;
- pending upgrade, boss-chest and artifact offers;
- XP drops, aftermath items и их pooling/aggregation status;
- reward ledger reference и diagnostics.

Game clock движется в RUN_ACTIVE, BOSS_INTRO и BOSS_ACTIVE для каждого босса. Он останавливается только на UPGRADE_OFFER, CHEST_OFFER, ARTIFACT_OFFER, RUN_PAUSED и CHECKPOINT_SETTLEMENT; после terminal/transaction states остаётся frozen. BOSS_INTRO не останавливает elapsed time. Exact pause/background save policy описана как working assumption и вынесена в pending decisions.

Временные полосы, spawn budget, active cap, boss interruption и восстановление после boss берутся только из B1. Архитектура не дублирует их как второй источник чисел.

## 5. Развитие билда

- В момент level-up authoritative simulation замораживается.
- Offer generator выдаёт три детерминированных offer_id, связанных с run_id, level/choice sequence, seed и content version.
- Offer может быть New weapon, Weapon upgrade, New passive, Passive upgrade или fallback, если это разрешено registry.
- Шесть weapon slots и шесть passive slots — канонический M1 limit; artifact effects не входят в BuildInventory slots.
- Weapon max level = 6, passive max rank = 5.
- Boss-chest evaluator проверяет matching synergy_id, weapon max, passive max, weapon не evolved, boss-chest context и offer не claimed.
- ArtifactOfferSystem отдельно проверяет source, ровно три карты, choice/refresh state и pending refresh policy; ArtifactEffectSystem применяет выбранный typed run effect.
- BuildInventory применяет только weapon/passive/evolution изменения; UI только показывает projection.
- Повторная доставка offer chosen, synergy claimed, boss chest claimed, artifact chosen или artifact refresh не меняет итог второй раз.

Точная семантика bonus/series state и некоторые fallback outcomes не выдумываются; они отмечены в DECISIONS_AND_UNKNOWNS.md и data contract.

## 6. Босс, checkpoint и сундук

На target schedule 300, 600, 900, 1200, 1500 и 1800 секундах WaveDirector создаёт main-boss checkpoints; intermediate slots находятся на 450, 750 и target 1350 секундах. Новые slot IDs и exact cadence/tuning помечены pending. На входе:

1. обычный spawn временно уменьшается по B1;
2. BossDirector выбирает безопасную позицию;
3. BOSS_INTRO показывает identity и telegraph contract;
4. BOSS_ACTIVE принимает только boss-owned combat transitions;
5. после defeat создаётся один settlement command;
6. RewardLedger применяет checkpoint bundle по idempotency key;
7. Только для нефинального checkpoint BossChestSystem создаёт persistent `CHEST_OFFER`; финальный checkpoint boss chest не создаёт;
8. SynergyEvaluator возвращает eligible, already_claimed или fallback_required для boss chest;
9. ElitePackDirector может после special elite pack (`source_kind=ELITE_PACK`) открыть отдельный `ARTIFACT_OFFER` из трёх карт; cadence/composition остаются pending;
10. First-clear reward после result finalization открывает отдельный `FIRST_CLEAR_REWARD` artifact offer, а не boss chest;
11. после claim нефинального boss chest открывается следующий wave band; после финального settlement начинается result flow без boss chest.

Точное содержимое fallback-награды и правила округления 50% Gold при defeat после checkpoint отсутствуют в B1 и не заполняются агентом.
### 6.1 Chest-window registry

The chest system is a source registry plus one idempotent offer lifecycle:

- max_openable_windows_per_run = 15 is an architecture cap/target, independent from synergy claims and artifact capacity.
- Eight windows are configured for non-final encounters: five main-boss windows (05:00, 10:00, 15:00, 20:00, 25:00) and three intermediate-boss windows.
- Seven additional windows are reserved for non-boss sources. Their triggers, cadence and exact outcome are PENDING_PRODUCT_DECISION/PENDING_B1; a reserved slot is not a guaranteed drop until configured.
- Each window may create at most one chest_offer_id. Closing, reopening, retrying or restoring it returns the same offer and cannot duplicate the outcome.
- BOSS_CHEST can be created only for a non-final main/intermediate encounter and resolves synergy/evolution or an approved fallback. It never becomes an artifact offer.
- FIRST_CLEAR_REWARD artifact offer remains a separate post-result three-card source and is not counted as a boss chest or as a pre-run loadout.
- The final boss at 30:00 creates no boss chest and no generic chest as part of defeat; it goes through final settlement and victory.

Chest-window count is not a guarantee that all 15 windows are active in the first balance pass. The registry has the capacity now; Balance/Product must configure the seven reserved sources before runtime claims a 15-window run.


## 7. Pause, settings, background и выход

Pause не удаляет RunSession и не сбрасывает elapsed time.

- Ручная пауза переводит simulation в RUN_PAUSED.
- Android background обрабатывается как forced pause до проверки resume.
- Settings из pause работают как дочерний UI-контекст; authoritative simulation остаётся paused.
- Continue возвращает state из resume_state, если content version и snapshot valid.
- Exit требует подтверждения. До отдельного product decision безопасный default — не выдавать незаработанные rewards и не обещать восстановление произвольного кадра.
- Checkpoint/explicit pause/terminal snapshots должны иметь revision, checksum и content version.
- При background kill valid last snapshot может быть предложен к recovery; snapshot старше допустимой policy либо несовместимый с content переводит пользователя в diagnostic recovery path.
- Restore не вызывает checkpoint settlement повторно: ledger проверяет idempotency key.

## 8. Смерть, победа и результат

Death:

- CombatSystem публикует один run_defeated command/event.
- RunSession замораживает simulation.
- RewardCalculator считает только разрешённые B1 partial rewards.
- Gold/Lunar Seals/Boss Essence проходят через RewardLedger.
- Result screen отображает уже committed и pending rewards раздельно.
- Повторное открытие result — read-only.

Victory:

- 30 минут сами по себе не дают victory.
- Нужен defeat final boss и commit final settlement для authoritative victory; final boss chest не создаётся.
- Final checkpoint bundle и first-clear/repeat-clear outcome проходят одну ledger transaction; final boss chest не создаётся.
- После commit доступен result screen и возврат в меню.
- Разблокировки читаются из committed meta save; UI не создаёт unlock сам.

## 9. Read model для игрока

Одна UI projection должна получать минимум:

| Область | Поля |
|---|---|
| Character | character_id, name, HP current/max, state, selected ability |
| Combat stats | attack, critical_chance, critical_multiplier, movement_speed, cooldown, armor и derived modifiers |
| Build | six weapon slots, six passive slots, levels/ranks, evolved flags |
| Active artifact effects | unbounded run instances, source/trigger/target/effect contract; no weapon/passive slot consumption |
| Pending artifact offer | source, three candidate cards, selected card/refresh state, policy status |
| Progression | level, xp_current, xp_to_next, kills, bonus_state |
| Run | elapsed time, current wave band/stage, boss state, checkpoint |
| Drops | XP visible count/value, aftermath density/status |
| Rewards | current earned, settled checkpoints, ledger keys/status |
| Diagnostics | resource fallback, restore result, content version mismatch |

Проекция должна быть derived и versioned. Она не содержит callable references к UI, scenes или texture objects.

## 10. Prototype versus target architecture

| Область | Что реально есть сейчас | Что требует target architecture |
|---|---|---|
| Menu | scripts/menu/menu_controller.gd меняет экраны и ведёт в arena scene | MenuFlow + Character/RunSetup commands + real RunSession |
| Arena | scripts/arena/arena_controller.gd рисует visual preview и временный timer | SimulationClock, player, combat, waves, XP, bosses, HUD, persistence |
| Loading | задержка и переход в preview scene | content validation, RunSession creation и recoverable errors |
| Victory/defeat | preview buttons возвращают в menu | result finalization, ledger, stats, meta save |
| Settings | placeholder section | validated settings model and pause integration |
| Assets | candidate/mockup references | runtime consumers после отдельного visual approval |
| Balance | B1 design baseline | data-driven runtime implementation and three-profile playtests |

## 11. Open decisions carried forward

Следующие вопросы не замаскированы архитектурными defaults:

- exact bonus/kill-series semantics;
- exact boss-chest fallback reward and selection;
- artifact effect definitions, elite-pack cadence, refresh cost/limit, duplicate/stacking and Codex persistence;
- rounding rule for 50% Gold after defeat;
- whether “next stage” is only a wave/checkpoint band or a future scene boundary;
- precise safe-save/recovery window for background kill;
- exact HUD presentation and optional stat fields.

Они перечислены с owner и next action в [DECISIONS_AND_UNKNOWNS.md](./DECISIONS_AND_UNKNOWNS.md).