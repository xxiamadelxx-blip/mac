# Deliverables и критерии содержания

Этот документ задаёт минимальный состав результата. Не создавай файл только ради отметки. Каждый deliverable должен содержать наблюдаемое поведение, ownership, ограничения и способ проверки.

## FIRST_RUN_FLOW.md

Должен содержать:

- end-to-end flow от boot до возврата в меню;
- actor/user intent, trigger, preconditions, result;
- экраны/состояния, loading, error, empty и edge cases;
- ветки death, victory, chest eligible/fallback, pause, exit, resume;
- отдельное описание того, какие данные видит игрок;
- явные ссылки на канонические источники;
- distinction между текущим prototype и target architecture.

## FIRST_RUN_STATE_MACHINE.md

Должен содержать:

- список состояний с owner;
- переходы с trigger, guard, side effects и failure/recovery path;
- state diagram, предпочтительно в Mermaid, с короткими названиями;
- terminal states и правила их повторного открытия;
- pause/background overlay как отдельные переходы или явно обоснованная модель;
- idempotent handling для boss reward, chest claim, result claim и save restore;
- таблицу переходов, если диаграмма недостаточна.

## FIRST_RUN_ARCHITECTURE.md

Должен содержать:

- proposed module boundaries;
- source of truth и направление зависимостей;
- menu/run bridge;
- run simulation, wave director, combat/progression, content registry;
- inventory/build/evolution/synergy evaluator;
- chest/reward ledger;
- HUD/read model;
- persistence/checkpoint/recovery;
- aftermath/XP separation;
- diagnostics/fallback;
- Android pause/resume;
- iteration layering и tradeoffs;
- explicit non-goals и будущие seams.

Документ не должен превращаться в список классов без ownership и data flow.

## FIRST_RUN_DATA_CONTRACT.json

Требования:

- валидный JSON без комментариев и trailing comma;
- schema/version/status;
- stable IDs для run, hero, weapon, passive, synergy, artifact, wave band, boss, chest offer, reward ledger entry;
- RunSession и versioned SaveSnapshot;
- current state, elapsed time, checkpoint, selected hero, build, stats, counters;
- event envelope и idempotency key;
- reward ledger contract;
- synergy eligibility и fallback outcome;
- aftermath и XP как разные типы;
- значения, отсутствующие в каноне, помечены PENDING_B1 или PENDING_PRODUCT_DECISION;
- schema не должна содержать скрытых magic numbers, не указанных источниками.

## FIRST_RUN_EVENT_CATALOG.md

Для каждого события укажи:

- event name и version;
- producer;
- consumer;
- payload;
- ordering/causality;
- retry and duplicate behavior;
- persistence/telemetry relevance;
- failure and recovery;
- whether event is authoritative command, domain event or UI projection.

Минимально покрой boot, menu, hero selection, run start, wave change, level up, offer chosen, weapon/passive upgraded, synergy eligible/claimed, boss spawned/defeated, checkpoint reward, chest opened/claimed, artifact obtained, pause/resume, save/restore, death, victory, result finalized и return to menu.

## FIRST_RUN_ACCEPTANCE_MATRIX.md

Сделай traceability matrix:

Requirement | Source | Observable behavior | Evidence/check | Status | Owner/next slice

Включи:

- весь пользовательский flow;
- wave/boss timing;
- XP/aftermath separation;
- upgrade and synergy logic;
- chest fallback;
- pause/resume;
- stats/HUD;
- death/victory;
- ledger idempotency;
- persistence/recovery;
- Android/performance risk;
- no unapproved asset/runtime assumptions.

Статусы должны быть честными: SPECIFIED, PENDING, BLOCKED, NOT_IMPLEMENTED, VERIFIED_BY_DOC_CHECK. Не используй DONE для нереализованного runtime.

## Общая планка

Каждый deliverable должен отвечать на вопросы:

- кто владеет состоянием;
- кто его изменяет;
- какое событие это вызывает;
- что видит пользователь;
- что произойдёт при повторной доставке;
- что произойдёт при ошибке;
- как следующий агент проверит результат.

Если ответа нет, это не повод заполнять пробел выдумкой: запиши pending и указание на владельца решения.
