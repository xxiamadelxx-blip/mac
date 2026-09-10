<!-- LIVE-AGENT-SYNC: read docs/AGENT_SYNC_STATE.md at current main before using this file -->
> **Live coordination pointer:** continuation work is routed through [`docs/AGENT_SYNC_STATE.md`](../../AGENT_SYNC_STATE.md). Legacy 20-minute/4-boss passages below are historical until reconciled.

# Рабочая папка агента: архитектура первого забега

Статус пакета: VERIFIED_ARCHITECTURE

> Revision 2 / 2026-09-10: архитектурная target-модель расширена до 30 минут. Старые 20-минутные значения в корневых GAME_MANIFEST.md, AGENT_CONTEXT.md и B1 остаются read-only legacy baseline; конфликт и порядок синхронизации зафиксированы в DECISIONS_AND_UNKNOWNS.md.

Текущая target revision: 30-минутный run, 6 main-boss slots, 3 intermediate-boss slots, до 15 chest windows и data-driven enemy variants. Root 20-minute/B1 records остаются внешним legacy baseline до отдельной синхронизации владельцами продукта и баланса.

REPO_CONTEXT.md содержит исторический baseline с метаданными подготовки. Текущий branch/HEAD всегда проверяется агентом непосредственно перед работой; расхождение SHA само по себе не является дефектом пакета.

Эта папка содержит проверенный логический контракт первого полного игрового забега Moonveil: Eclipse. Статус VERIFIED означает согласованность архитектурных документов и выполненные документальные проверки; он не означает готовность runtime, APK или production.

## С чего начинать

1. Прочитать корневой AGENTS.md.
2. Прочитать README.md, GAME_MANIFEST.md, AGENT_CONTEXT.md и актуальный раздел ROADMAP.md.
3. Прочитать docs/BALANCE_ECONOMY_SPEC.md как единственный числовой baseline.
4. Прочитать REPO_CONTEXT.md и DECISIONS_AND_UNKNOWNS.md из этой папки.
5. Прочитать AGENT_TASK.md.
6. Перед началом работы загрузить навыки, перечисленные в SKILLS_AND_INSTRUCTIONS.md.
7. Использовать AGENT_PROMPT_RU.md как готовое задание для нового чата.

## Границы

Агент проектирует поведение, состояния, границы модулей, данные, события, сохранение и проверяемые критерии. В этой задаче агент не пишет gameplay-код, не создаёт визуальные ассеты и не продвигает кандидаты в production.

Все результаты этого задания должны оставаться внутри docs/architecture/first-run/. Корневые канонические документы и runtime-файлы не изменяются.

## Состав проверенного пакета

- FIRST_RUN_FLOW.md
- FIRST_RUN_STATE_MACHINE.md
- FIRST_RUN_ARCHITECTURE.md
- FIRST_RUN_DATA_CONTRACT.json
- FIRST_RUN_EVENT_CATALOG.md
- FIRST_RUN_ACCEPTANCE_MATRIX.md
- ARCHITECTURE_AUDIT.md

Все обязательные deliverables и финальный аудит присутствуют; пакет готов как архитектурный контракт для следующего runtime-агента.

## Проверка перед передачей

Агент обязан показать:

- точный список изменённых файлов;
- ветку и HEAD, на которых работал;
- сопоставление требований с разделами документов;
- результат проверки валидности JSON;
- результат проверки Markdown-ссылок и git diff --check, если доступен локальный Git;
- список нерешённых вопросов и явно отложенных решений;
- честное разделение между спроектировано, реализовано и проверено.
