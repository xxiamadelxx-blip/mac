# Runtime Handoff — шаблон результата

Этот файл заполняется агентом после каждого вертикального среза. Он предназначен для архитектурного и балансового агентов, но не заменяет их документы и не даёт им права редактировать runtime.

## 1. Идентичность работы

- Repository:
- Branch:
- HEAD:
- Parent:
- Slice: R1 / R2 / R3 / R4
- Status: IMPLEMENTED / TESTED / RUNTIME_VERIFIED / PARTIAL / BLOCKED
- Content version:
- Seed(s):

## 2. Scope

### Изменённые файлы

- path — зачем изменён и какой contract закрывает.

### Проверка границ

- Изменены только разрешённые runtime/test/evidence paths: PASS/FAIL.
- docs/architecture/first-run не изменялась: PASS/FAIL.
- docs/agents/balance-economy и B1 не изменялись: PASS/FAIL.
- visual_lab, mockups, assets, audio не изменялись: PASS/FAIL.
- destructive history operation не выполнялась: PASS/FAIL.

## 3. Contract evidence

| Contract | Source | Implementation path | Check | Observed | Status |
|---|---|---|---|---|---|
| Content Registry | B1/model |  |  |  |  |
| RunSession | architecture data contract |  |  |  |  |
| RunCoordinator | architecture/state machine |  |  |  |  |
| SimulationClock | architecture/runtime context |  |  |  |  |
| Wave/Boss | B1 and event catalog |  |  |  |  |
| Chest/Artifact | architecture artifact/chest contract |  |  |  |  |
| RewardLedger | architecture reward contract |  |  |  |  |
| Persistence | architecture recovery contract |  |  |  |  |

## 4. Проверки

Для каждой команды укажи реальную команду, exit status и существенный output:

- focused unit/integration check:
- contract/schema validation:
- deterministic replay:
- duplicate/idempotency check:
- regression check:
- build/install/launch check, если это R4:

Если команда недоступна, укажи точную ошибку. Не заменяй её фразой «проверено визуально».

## 5. Runtime traces

Для каждого trace укажи:

- seed;
- content_version;
- character;
- input/policy;
- state sequence;
- clock values before/after pause and boss;
- wave band, spawn budget, active cap;
- XP, level, kills;
- boss encounter and settlement;
- chest/artifact offer IDs and candidates;
- selected outcome;
- ledger key, wallet revision and terminal result;
- replay result/hash.

Минимальные seeds для R3: 101, 202, 303, 404, 505.

## 6. Условия и остатки

### Доказано

-

### Только реализовано, но не runtime-verified

-

### Blocked

- Причина:
- Точная граница блокировки:
- Что нужно для продолжения:

### Pending product decisions

-

## 7. Handoff

- Что должен проверить балансный агент:
- Что должен проверить архитектурный агент:
- Какой следующий slice:
- Первая проверка следующего агента:

Не переписывать исходные документы других агентов ради обновления статуса. Передача выполняется через evidence и ссылку на commit.
