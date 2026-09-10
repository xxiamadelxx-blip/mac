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
| C-07 | Артефакты не выбираются и не экипируются до старта забега; фиксированных artifact slots нет | Product decision; Magic Survival reference |
| C-08 | Каждый artifact source показывает три карты; игрок выбирает одну, и эффект активен до конца текущего забега | Product decision |
| C-09 | Boss chest — отдельная нефинальная награда для synergy/evolution/fallback; elite pack и first-clear reward могут открывать отдельные artifact offers; final boss не создаёт boss chest | Product decision; B1 reward boundary |
| C-10 | Game clock продолжает идти через BOSS_INTRO и BOSS_ACTIVE для каждого босса; останавливается только на offer/pause/settlement и terminal/transaction boundaries | Explicit current task decision |

## Вопросы, которые агент обязан проверить

| ID | Вопрос | Почему важен | Начальная обработка |
|---|---|---|---|
| U-01 | Что именно означает «накопление бонуса»: kill streak, meter, временный buff или другое? | Меняет RunSession, HUD и balance contract | Спроектировать расширяемый bonus state; точную формулу оставить PENDING_PRODUCT_DECISION |
| U-02 | Что означает лимит слотов оружия/пассивок и каков exact split? | Меняет build inventory и offer legality | Читать GAME_MANIFEST; если неоднозначно, не угадывать, вынести контрактный параметр |
| U-03 | Какой полный roster оружия, пассивок и exact synergy conditions уже каноничен? | Нельзя реализовать evaluator по выдуманным парам | Использовать stable IDs и schema; отсутствующие пары пометить PENDING_PRODUCT_DECISION |
| U-04 | Что именно даёт boss chest на промежуточных checkpoint при eligible и fallback ветках? | Меняет chest offer, rewards и idempotency; у финального босса сундука нет | Описать outcome types и evaluator для нефинального checkpoint, значения оставить pending |
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


## Live repository audit for this architecture task

Дата проверки: 2026-09-10
Repository: xxiamadelxx-blip/mac
Branch: main
HEAD at inspection: 54b5932605691be0aad3ccdd490710e727a641c8

- Прямой локальный checkout в текущем окружении отсутствует, поэтому git status/branch/дословный локальный diff не выполнялись.
- Atlas Scout capability в текущем окружении не опубликована; использован разрешённый fallback: GitHub tree, точечное чтение живых файлов и repository search.
- Фактически проверены project.godot, menu/arena scenes and controllers, B1, живой stage manifest и архитектурные инструкции.
- В рамках этой финализации изменяется только docs/architecture/first-run/; корневые, балансные, runtime и visual paths остаются read-only. Более ранние внешние коммиты не откатываются и не переписываются.
- AGENT_CONTEXT/ROADMAP/MOCKUP_INDEX имеют drift по status этапа 4; для архитектуры это не блокер, поскольку current task не меняет visual stage и не повышает его статус.

## Архитектурные решения текущего задания

| ID | Status | Решение | Причина и последствия |
|---|---|---|---|
| A-01 | RESOLVED_BY_AGENT | RunSession — authoritative source of truth активного забега | UI и scene nodes не смогут незаметно менять time, build, rewards или state; snapshot остаётся сериализуемым |
| A-02 | RESOLVED_BY_AGENT | RunCoordinator только оркестрирует команды и transitions | Combat, progression, waves и ledger сохраняют собственное ownership; не создаётся god controller |
| A-03 | RESOLVED_BY_AGENT | Content Registry immutable/versioned на протяжении run | Offer, wave, reward и restore не зависят от локализации/текущего UI |
| A-04 | RESOLVED_BY_AGENT | XPDrop и AftermathItem — отдельные entity types/stores | XP не теряется при aggregation останков и не становится частью collision/pathfinding |
| A-05 | RESOLVED_BY_AGENT | Reward Ledger commit атомарен с wallet/unlock revision | Повторные checkpoint/chest/result events не удваивают валюту |
| A-06 | WORKING_ASSUMPTION | Safe save points: checkpoint, explicit pause, terminal/reward boundary | Снижает data-loss risk без обещания произвольного mid-frame resume; требует product confirmation |
| A-07 | WORKING_ASSUMPTION | Stage — logical wave/checkpoint projection внутри одной карты, не обязательная отдельная scene | Позволяет закрыть M1 одним runtime path; отдельная scene остаётся будущим seam |
| A-08 | CONFIRMED | Final victory только после defeat финального босса и final settlement; без финального сундука | Это явно закреплённое текущее product decision; timer alone не выдаёт победу |
| A-09 | RESOLVED_BY_AGENT | Duplicate effects защищаются idempotency key + state revision + owned entity ID | Одинаково покрывает ledger, chest, offer, XP pickup и terminal result |
| A-10 | RESOLVED_BY_AGENT | Events are transport/diagnostic contract, not second source of truth | Offline M1 получает replay protection без full event-sourcing complexity |
| A-11 | CONFIRMED | Game clock advances through BOSS_INTRO and BOSS_ACTIVE for every boss and freezes at offers, pause, settlement and terminal/transaction boundaries | Runtime uses one clock contract for all bosses |

## Уточнённые открытые вопросы

| ID | Status | Вопрос | Source/impact | Temporary handling | Owner | Next action |
|---|---|---|---|---|---|---|
| U-11 | PENDING_B1 | Как округлять 50% Gold при defeat после checkpoint с нечётной наградой? | B1 §7 даёт 50%, но не rounding policy | Не фиксировать округление в JSON/коде | balance owner | Добавить правило в B1 до runtime ledger |
| U-12 | PENDING_PRODUCT_DECISION | Что именно выдаётся при chest fallback_required на нефинальном checkpoint? | AGENT_TASK требует fallback для промежуточного сундука, exact outcome не задан; финальный босс сундук не создаёт | Хранить typed fallback policy/value как pending | product owner | Утвердить fallback table и UI copy |
| U-13 | PENDING_PRODUCT_DECISION | Можно ли продолжать run после background kill с последнего snapshot и насколько старого? | Влияет на loss/exploit/recovery policy | Использовать safe snapshot + RECOVERY_REVIEW, не обещать mid-frame | product/runtime owner | Утвердить recovery window and abandon behavior |
| U-14 | PENDING_PRODUCT_DECISION | Является ли current_stage_id отдельной сценой или только wave/checkpoint band? | Влияет на bridge, loading и save boundary | В архитектуре stage — logical projection; scene seam оставлен | product/runtime owner | Подтвердить до implementation Iteration 2 |
| U-15 | PENDING_PRODUCT_DECISION | Какие optional stats обязательны на HUD/result кроме required fields? | Влияет на projection size и acceptance | Expose required fields plus extensible modifiers_ref | product owner | Утвердить presentation matrix до HUD slice |

| U-16 | PENDING_PRODUCT_DECISION | Что сохраняется между забегами: только артефакт в Codex или также его активный эффект? | Разделяет persistent collection и temporary run state | В текущем контракте artifact instance active only within run; persistent unlock остаётся отдельным вопросом | product owner | Утвердить Codex/meta-progression policy до result slice |

## Scope conclusion

Архитектурный пакет проектирует контракт и не закрывает runtime evidence. Отсутствие Godot/Android acceptance здесь не считается дефектом документа; это обязательный следующий implementation slice.