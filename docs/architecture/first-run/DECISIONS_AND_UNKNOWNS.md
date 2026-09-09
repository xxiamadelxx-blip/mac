# Решения и открытые вопросы

Статусы: CONFIRMED, WORKING_ASSUMPTION, PENDING_PRODUCT_DECISION, PENDING_B1, BLOCKED, RESOLVED_BY_AGENT.

Правило: агент не закрывает вопрос молча. Для каждого вопроса указываются source, impact, temporary handling, owner и next action.

## Подтверждённый минимум

| ID | Решение | Источник |
|---|---|---|
| C-01 | Первый срез включает один полный 20-минутный забег | GAME_MANIFEST.md, AGENT_CONTEXT.md |
| C-02 | Боссы происходят на 5, 10, 15 и 20 минутах | GAME_MANIFEST.md, docs/BALANCE_ECONOMY_SPEC.md |
| C-03 | XP-дропы и останки/aftermath — отдельные сущности и слои | AGENT_CONTEXT.md, docs/BALANCE_ECONOMY_SPEC.md |
| C-04 | Награды checkpoint должны быть идемпотентными | GAME_MANIFEST.md, docs/BALANCE_ECONOMY_SPEC.md |
| C-05 | Игра — Godot 4.x native 2D, Android, offline-first | README.md, AGENT_CONTEXT.md |
| C-06 | Нейтральный раздел меню называется ПЕРСОНАЖИ | AGENT_CONTEXT.md, stage-01 docs |

## Вопросы, которые агент обязан проверить

| ID | Вопрос | Почему важен | Начальная обработка |
|---|---|---|---|
| U-01 | Что именно означает «накопление бонуса»: kill streak, meter, временный buff или другое? | Меняет RunSession, HUD и balance contract | Спроектировать расширяемый bonus state; точную формулу оставить PENDING_PRODUCT_DECISION |
| U-02 | Что означает лимит слотов оружия/пассивок и каков exact split? | Меняет build inventory и offer legality | Читать GAME_MANIFEST; если неоднозначно, не угадывать, вынести контрактный параметр |
| U-03 | Какой полный roster оружия, пассивок и exact synergy conditions уже каноничен? | Нельзя реализовать evaluator по выдуманным парам | Использовать stable IDs и schema; отсутствующие пары пометить PENDING_PRODUCT_DECISION |
| U-04 | Что именно даёт boss chest при eligible и fallback ветках? | Меняет chest offer, rewards и idempotency | Описать outcome types и evaluator, значения оставить pending |
| U-05 | Является ли «следующая стадия» отдельной сценой, wave band или checkpoint внутри одной карты? | Меняет state machine и save boundary | Связать stage с wave/checkpoint, но явно отметить implementation decision |
| U-06 | В какие моменты можно сохранить незавершённый run? | Меняет recovery и exploit surface | Описать snapshot seam и policy placeholder; не обещать mid-run resume без подтверждения |
| U-07 | Что происходит при выходе в меню, background kill или ошибке restore? | Риск потери прогресса и дубля reward | Разделить abandon, recoverable checkpoint и terminal result |
| U-08 | Какие поля stats обязательны в HUD и в result screen? | Меняет read model и acceptance matrix | Включить запрошенные attack/crit/multiplier/speed, kill count, XP и build; exact presentation pending |
| U-09 | Какие unlocks разрешены после победы и какова семантика повторного прохождения? | Меняет meta save и reward ledger | Сослаться на B1/GAME_MANIFEST; не изобретать новые валюты или unlock rules |
| U-10 | Какая часть текущего menu/arena prototype станет seam для runtime? | Меняет implementation order и migration risk | Зафиксировать prototype как evidence, предложить adapter/replace boundary, не менять код |

## Known drift

- AGENT_CONTEXT.md и docs/MOCKUP_INDEX.md говорят, что этап 4 уже начат; ROADMAP.md может сохранять PLANNED.
- Menu prototype использует архивные v01 ресурсы и не доказывает полный navigation/runtime contract.
- Arena controller доказывает visual preview, но не movement, combat, waves, bosses, XP, HUD или save.
- Stage assets имеют candidate/pending statuses; архитектурный агент не должен повышать их статус.

После аудита агент обновляет таблицы, добавляет обнаруженные конфликты и указывает, какие вопросы можно закрыть только пользователем, B1 или runtime-тестом.


## Результат аудита первого забега (2026-09-09)

| ID | Статус после аудита | Что подтверждено | Что остаётся открытым | Evidence |
|---|---|---|---|---|
| U-01 | PENDING_PRODUCT_DECISION | RunSession/HUD extension point обязателен | exact meaning/formula of bonus or series | GAME_MANIFEST.md, AGENT_TASK.md |
| U-02 | PARTIALLY_RESOLVED | GAME_MANIFEST фиксирует 6 weapon slots и 6 passive slots; уровни 6/5 | replacement/offer legality при заполненном слоте | GAME_MANIFEST.md §4/§6 |
| U-03 | PARTIALLY_RESOLVED | проверены 10 прямых weapon/passive pairs и условия max weapon/passive + chest | exact effect data, evaluator details и fallback | GAME_MANIFEST.md §6 |
| U-04 | PENDING_PRODUCT_DECISION | chest outcome и idempotent chest_id зафиксированы в архитектуре | exact fallback reward при отсутствии eligible synergy | AGENT_TASK.md, FIRST_RUN_DATA_CONTRACT.json |
| U-05 | WORKING_ASSUMPTION | для M1 stage трактуется как logical wave/checkpoint band внутри одной арены | нужна ли отдельная scene/stage boundary | GAME_MANIFEST.md §4, FIRST_RUN_FLOW.md |
| U-06 | PENDING_PRODUCT_DECISION | snapshot seam описан для checkpoint/background/terminal | разрешённые точки incomplete-run save | GAME_MANIFEST.md, AGENT_TASK.md |
| U-07 | PENDING_PRODUCT_DECISION | exit требует confirmation; invalid snapshot не восстанавливается молча | abandon/process-kill UX и retention | AGENT_TASK.md, FIRST_RUN_STATE_MACHINE.md |
| U-08 | PENDING_PRODUCT_DECISION | обязательный набор HUD/result fields перечислен | exact presentation/layout | AGENT_TASK.md |
| U-09 | PENDING_PRODUCT_DECISION | first-clear/repeat ledger keys предусмотрены | unlock/replay semantics и новые meta rules | GAME_MANIFEST.md, BALANCE_ECONOMY_SPEC.md |
| U-10 | WORKING_ASSUMPTION | current menu/arena остаются prototype evidence; seam — AppFlowCoordinator/RunFacade | конкретная migration strategy runtime agent | scripts/menu/menu_controller.gd, scripts/arena/arena_controller.gd |

### Зафиксированный document drift

- AGENT_CONTEXT.md и ROADMAP.md расходятся в статусе этапа 4; архитектура не объявляет этап завершённым и оставляет это внешним release/product решением.
- menu prototype использует архивные v01 пути и старый пользовательский label; каноническая архитектура использует нейтральный раздел ПЕРСОНАЖИ, не исправляя runtime в рамках этого задания.
- arena controller ускоряет 20 минут до 60 секунд и рисует visual preview; это не доказательство runtime simulation.
- visual assets и mockups имеют candidate/evidence статус; архитектурный пакет не повышает их статус и не добавляет ссылки на них как runtime dependencies.

### Решения агента, применённые только к контракту

- reward ledger key и duplicate policy определены как обязательный boundary, даже если adapter ещё не написан;
- fallback chest outcome оставлен явным pending вместо выдуманной награды;
- абсолютные enemy base HP/damage/speed не добавлены; B1 multipliers сохранены;
- JSON использует stable slug IDs для уже названного canonical roster; это naming convention для будущего registry, а не утверждение о готовом runtime content.
