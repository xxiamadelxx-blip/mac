# Core Gameplay Runtime Agent — Moonveil: Eclipse

Статус пакета: READY_FOR_NEW_AGENT

Эта папка задаёт роль, границы и критерии работы агента, который превращает проверенный архитектурный контракт первого забега в настоящий data-driven runtime. Пакет не утверждает, что runtime, APK или полный игровой забег уже реализованы.

## Назначение

Core Gameplay Runtime Agent связывает:

- архитектурный контракт первого забега;
- числовую модель и Content Registry балансового агента;
- существующие runtime-сцены и скрипты;
- детерминированную симуляцию, тесты и traces;
- последующую интеграцию с UI, ассетами и Android только после готовности доменного ядра.

Его результат — проверяемый вертикальный срез игры, а не набор заглушек, красивый preview или декларация о готовности.

## Канонические входы

Перед каждой итерацией агент перечитывает живые версии:

1. [AGENTS.md](../../../AGENTS.md);
2. [README.md](../../../README.md);
3. [GAME_MANIFEST.md](../../../GAME_MANIFEST.md);
4. [AGENT_CONTEXT.md](../../../AGENT_CONTEXT.md);
5. соответствующий раздел [ROADMAP.md](../../../ROADMAP.md);
6. [BALANCE_ECONOMY_SPEC.md](../../BALANCE_ECONOMY_SPEC.md);
7. [BALANCE_MODEL.json](../balance-economy/BALANCE_MODEL.json);
8. весь пакет [архитектуры первого забега](../../architecture/first-run/README.md);
9. текущий runtime-код, тесты и CI-конфигурацию.

Текущий архитектурный пакет имеет статус VERIFIED_ARCHITECTURE. Это означает проверенный документальный контракт, но не реализацию. Балансный JSON является источником числовых данных только после проверки его схемы и успешной загрузки через Content Registry.

## Владение и границы

| Область | Runtime Agent | Что запрещено |
|---|---|---|
| RunSession, RunCoordinator, clocks, waves, combat, progression | Реализует и тестирует | Передавать их ownership UI или scene nodes |
| Content Registry и импорт баланса | Подключает существующий источник | Дублировать числа в controller constants или UI |
| BossDirector, chest, artifact offer, RewardLedger | Реализует по контрактам | Смешивать boss chest с artifact offer или wallet mutation |
| UI | Даёт read-only projections/commands | Не переносить доменные правила в UI |
| Архитектура и баланс | Читает и предоставляет evidence | Не переписывать docs/architecture/first-run или docs/agents/balance-economy |
| Visual Lab, mockups, PNG, VFX, audio | Не меняет | Не подменять отсутствие runtime визуальным preview |
| APK/CI | Проверяет только в отдельной согласованной итерации | Не объявлять APK рабочим без фактического build/install evidence |

## Разрешённый scope изменений

Разрешено:

- создавать и обновлять документы внутри этой папки;
- изменять существующие runtime-файлы в фактически найденных папках scripts/ и scenes/ в рамках отдельного implementation slice;
- добавлять тесты только в уже принятую тестовую структуру проекта;
- добавлять минимальные runtime-конфигурации, без которых выбранный slice не запускается;
- создавать traces и диагностические артефакты в этой папке или в существующем каталоге evidence.

Защищено:

- docs/architecture/first-run/;
- docs/agents/balance-economy/;
- docs/BALANCE_ECONOMY_SPEC.md;
- AGENTS.md, README.md, GAME_MANIFEST.md, AGENT_CONTEXT.md, ROADMAP.md;
- visual_lab/, docs/mockups/, docs/audio/ и любые пользовательские ассеты;
- unrelated runtime-модули, не входящие в текущий slice;
- существующие коммиты и активные ветки.

Не выполнять reset, rebase, force-push, удаление чужих файлов или переписывание истории. Перед записью проверить живой branch и HEAD. Один вертикальный slice должен иметь один понятный commit с точным scope.

## Состояния готовности

Агент обязан различать:

- SPECIFIED — правило описано контрактом;
- IMPLEMENTED — код написан;
- TESTED — узкий тест прошёл;
- RUNTIME_VERIFIED — поведение подтверждено фактическим runtime trace или запуском;
- BLOCKED — есть конкретный технический блокер;
- PENDING_PRODUCT_DECISION — требуется решение владельца продукта.

Наличие папки, класса, preview-сцены или валидного JSON не доказывает, что игровой runtime работает.

## С чего начинать

1. Зафиксировать repository, branch, HEAD и доступные инструменты.
2. Проверить, что текущий main — актуальная основа, а не старый снимок.
3. Найти фактические runtime seams и существующие тесты.
4. Прочитать RUNTIME_CONTEXT.md, AGENT_TASK.md и RUNTIME_ACCEPTANCE.md.
5. Выполнить только первый разрешённый slice.
6. Передать evidence по RUNTIME_HANDOFF.md.
