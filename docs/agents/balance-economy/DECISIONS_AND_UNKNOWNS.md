# Решения и открытые вопросы Balance & Economy

Статусы: CONFIRMED, CANON, DERIVED, PENDING_B1, PENDING_PRODUCT_DECISION, BLOCKED, RESOLVED_BY_AGENT.

Агент не закрывает вопрос молча. Для каждого пункта нужны source, impact, temporary handling, owner и next action.

## Подтверждено

| ID | Решение | Источник |
|---|---|---|
| C-01 | Первый целевой забег длится 20 минут и имеет босса на 5/10/15/20 минутах | GAME_MANIFEST.md, AGENT_CONTEXT.md, B1 |
| C-02 | B1 — единственный текущий числовой baseline для waves, XP, rewards и meta costs | AGENT_CONTEXT.md, B1 |
| C-03 | B1 — design baseline; числа ещё не подключены к коду | B1 |
| C-04 | Сложность должна расти через состав, плотность, паттерны и давление на пространство, а не только через HP | B1 |
| C-05 | XP, aftermath, chest, artifact и reward ledger — разные типы состояния | B1, AGENT_CONTEXT.md |
| C-06 | Gold, Moon Seals и Boss Essence — разные кошельки | B1 |
| C-07 | Баланс проверяется fresh, moderate и max M1 профилями | B1 |
| C-08 | Визуальные ассеты не входят в работу Balance Agent | AGENTS.md, область этого задания |
| C-09 | Артефакты — run offers из трёх карт, без pre-run loadout и фиксированных слотов; активный эффект отделён от обычных passive modifiers | Product decision; architecture contract |
| C-10 | Boss chest и artifact offer — разные потоки: boss chest даёт synergy/evolution/fallback, elite pack/first-clear могут дать artifact offer, final boss не создаёт boss chest | Product decision; B1 reward boundary |
| C-11 | На каждом боссе в 5/10/15/20 минут основной таймер забега замирает; волны, XP и spawn clock не продвигаются, бой идёт на отдельном encounter-clock, после чего нефинальный таймер возобновляется с той же отметки | Product decision captured 2026-09-10; model boss_clock_policy |

## Обязательные вопросы

| ID | Вопрос | Влияние | Временная обработка | Владелец/следующий шаг |
|---|---|---|---|---|
| U-01 | Заданы ли абсолютные base HP/damage/speed для каждого enemy_id? | Без них нельзя доказать TTK и входящий урон | Не выдумывать; использовать PENDING_B1 или TEST_PLACEHOLDER вне production | Product/B1 owner; уточнить B1 |
| U-02 | Каковы exact weapon/passive/synergy IDs и условия eligible? | Без этого нельзя доказать offer legality и power budget | Схема evaluator с pending conditions | Product/gameplay owner |
| U-03 | Что означает «накопление бонуса»: streak, meter, buff или иной state? | Меняет reward/XP/DPS и HUD contract | Расширяемый bonus state без формулы | Product owner |
| U-04 | Каков точный split слотов оружия и пассивок, reroll/banish и offer rules? | Меняет вероятность сборки и баланс выбора | Не фиксировать числом без источника | Gameplay/architecture owner |
| U-05 | Как распределяется composition внутри каждой 5-minute band? | Меняет фактическую нагрузку и XP | Использовать role-level table; точные доли pending | Balance agent предложит derived table |
| U-06 | Каковы boss identities, skills и arena constraints? | Меняет boss duration, telegraph и victory proof | Проверить GAME_MANIFEST; неизвестное блокирует boss TTK, но не wave model | Content/gameplay owner |
| U-07 | Какой success-rate считать «проходимо» для fresh profile? | Нужен для математического pass/fail, а B1 говорит только «шанс после попыток» | Показывать reach/kill/death proxies и запросить decision | Product owner |
| U-08 | Какой runtime seam станет владельцем balance data? | Определяет, где числа будут жить | Контракт и simulator в этой папке; integration handoff | Architecture/coding agent |
| U-09 | На каком Android-устройстве подтверждать 30 FPS? | Без device baseline performance только risk | Отдельно пометить performance unverified | QA/technical owner |
| U-10 | Разрешено ли менять B1 при обнаружении противоречия? | Предотвращает незаметный drift канона | Только decision request, не silent edit | Project owner |
| U-11 | Какова политика artifact refresh: cost, currency, max count and reroll scope? | Меняет offer frequency and economy | Expose three-card refresh command with pending policy; no numeric cost invented | Product owner | Approve refresh contract |
| U-12 | Разрешены ли дубликаты артефактов и как они stack? | Меняет power curve and active-effect attribution | Keep stacking_policy pending per artifact effect | Product/gameplay owner | Approve duplicate/stacking matrix |
| U-13 | Какова cadence/size/composition special elite packs between bosses? | Меняет artifact-offer frequency and wave budget | Model source as allowed pending elite event; do not inject spawn count | B1/balance owner | Add elite-pack schedule to B1 |
| U-14 | Какие exact artifact effects, triggers, targets and values входят в first slice? | Меняет DPS/survivability/weapon interactions and test fixtures | Use typed effect contract and examples only; numbers remain pending | Product/balance owner | Approve effect catalog |

## Правило обновления

После каждой итерации:

- закрытые вопросы получают evidence и дату/ревизию источника;
- новые вопросы добавляются, а не прячутся в prose;
- derived values не переводятся в CANON автоматически;
- если вопрос блокирует только часть, независимая работа продолжается.
