# Deliverables Balance & Economy Agent

Все обязательные документы этого списка создаются в docs/agents/balance-economy/. Не создавай пустые файлы ради отметки: каждый должен содержать source, owner, rule, evidence и статус.

## Обязательные результаты

### 1. BALANCE_AUDIT.md

Живой аудит:

- repository, branch, HEAD и состояние дерева;
- прочитанные источники;
- что реально реализовано;
- B1 source/derived/pending matrix;
- числовой drift и его влияние;
- существующие runtime seams;
- блокеры и безопасные следующие шаги.

### 2. BALANCE_MODEL.json

Валидный JSON на основе BALANCE_MODEL.template.json:

- schema/version/status;
- source revision и status каждого значимого поля;
- hero stats;
- enemy archetypes и base values;
- wave bands;
- damage/HP/crit/cooldown model;
- XP/progression;
- chest/synergy/fallback;
- checkpoint/reward ledger;
- fresh/moderate/max profiles;
- invariants и acceptance references.

Нельзя заменять отсутствующие значения молча выбранными числами.

### 3. BALANCE_WAVE_TABLE.md

Для каждой полосы:

- time range;
- spawn budget;
- active cap;
- multipliers;
- composition/role intent;
- boss interruption;
- safe-mode behavior;
- expected XP/load;
- evidence and status.

### 4. BALANCE_COMBAT_MODEL.md

Опиши:

- hero/enemy stats;
- damage pipeline;
- armor and mitigation;
- crit;
- cooldown and hit cadence;
- contact/ranged/telegraphed damage;
- time-to-kill;
- boss windows;
- safety bounds;
- unresolved base values.

### 5. BALANCE_XP_REWARDS.md

Опиши:

- XP drops and sources;
- XP merge/magnet;
- XP curve;
- level cadence;
- weapon/passive offers;
- synergy eligibility and fallback;
- chest flow;
- checkpoint rewards;
- first-clear/repeat/defeat;
- idempotency and wallets.

### 6. BALANCE_SIMULATION_REPORT.md

Должен быть воспроизводимым:

- command;
- environment;
- input and seeds;
- profile definition;
- expected values;
- observed values;
- pass/fail/partial;
- artifacts;
- known limitations.

### 7. BALANCE_ACCEPTANCE_MATRIX.md

Таблица:

Requirement | Source | Model/runtime behavior | Check | Observed | Status | Next owner

Минимум включи все B1 acceptance targets, три профиля, wave/boss timing, XP cadence, TTK, synergy power, reward idempotency, active cap и performance risk.

### 8. Код и data integration

Если текущий runtime имеет безопасный seam:

- добавь минимальные data/domain/test файлы;
- не добавляй визуальные ассеты;
- перечисли каждый внешний изменённый файл;
- свяжи data source с model и test;
- покажи runtime evidence.

Если seam отсутствует, создай handoff с точными путями/контрактами, а не фиктивную интеграцию.

## Definition of Done

Статус пакета может быть VERIFIED только если:

- B1 был прочитан из живой ветки;
- source/derived/pending разделены;
- JSON валиден;
- симуляция повторяется;
- три профиля проверены;
- acceptance matrix заполнена честно;
- runtime claims подкреплены runtime evidence;
- открытые решения и ограничения явно указаны;
- ни один документ не выдаёт design baseline за готовую игру.
