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
