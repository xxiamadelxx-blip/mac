# Skills и рабочие инструкции агента

Эта папка не копирует системные skill-файлы. Она задаёт обязательную маршрутизацию: новый агент должен загрузить доступные навыки в своём окружении и применить их инструкции. Если skill недоступен, агент фиксирует это как ограничение и использует описанный fallback.

## Обязательные skills

| Skill | Зачем нужен | Что должно попасть в evidence |
|---|---|---|
| atlas-scout:atlas-scout-code-navigation | Понять структуру Godot-кода, symbols, callers и текущие seams | Список проверенных entry points и фактически найденных связей |
| keystone:project-audit | Провести read-only snapshot и обнаружить docs-vs-reality drift | Краткие findings со ссылкой на файл и confidence |
| keystone:product-planning | Перевести пользовательский brief в точные состояния, правила, UX edge cases и архитектурные boundaries | Goal, audience, behavior, tradeoffs, acceptance criteria |
| keystone:task-creation | Разложить будущую реализацию на вертикальные срезы и verification gates | Iteration 1/2/3, dependencies, slice order, checks |
| codex-engineering-guardrails:code-verification | Проверить JSON, ссылки, traceability и границы diff независимо от авторского summary | Команды, exit status, result и непроверенные участки |

## Условные skills

- codex-engineering-guardrails:code-work — не загружать для реализации; использовать только если отдельным решением позже будет разрешено менять runtime.
- canonical-memory-verifier:verify-canonical-memory — применять только если в чат явно передан отдельный memory bundle; текущие repo-документы сами по себе не являются таким bundle.
- Visual Lab instructions — читать только при visual/design/art/asset/sprite/mockup изменениях. В текущем задании такие изменения запрещены.

## Обязательный старт без инструмента Atlas

Если structural navigation tool недоступен, используй read-only проверки:

1. git status --short
2. git branch --show-current
3. git rev-parse HEAD
4. rg --files
5. rg -n по ключевым символам и путям
6. чтение целевых файлов целиком или нужными диапазонами

Не утверждай, что сделал локальную проверку, если у тебя нет локального checkout. В таком случае используй доступный GitHub/repository connector и укажи источник evidence.

## Порядок планирования

1. Сначала инвентаризация и источники.
2. Затем продуктовый flow и состояния.
3. Затем границы модулей и ownership.
4. Затем данные и события.
5. Затем вертикальные срезы.
6. Затем acceptance matrix и независимая проверка.

Не начинай с написания красивой диаграммы. Диаграмма должна быть следствием зафиксированных состояний и правил.

## Правила контекстной целостности

- Не меняй источник истины в обход владельца.
- Не переноси числовые значения в отдельный контракт без ссылки на B1.
- Не называй unknown ошибкой, если он только не проверен.
- Отделяй confirmed, inferred, pending и blocked.
- Любой конфликт между документами записывай в DECISIONS_AND_UNKNOWNS.md.
- Любое событие, которое может быть доставлено повторно, должно иметь idempotency strategy или явное объяснение, почему повтор невозможен.
- Любое state transition должно иметь trigger, guard, owner, side effects, failure path и recovery path.

## Scope lock

Изменения разрешены только в docs/architecture/first-run/. Если обнаружена необходимость менять код, B1, root docs или visual package, создай запись pending/blocker и не меняй внешний файл.

## Перед финалом

- проверить наличие всех обязательных deliverables;
- валидировать JSON;
- проверить внутренние пути;
- выполнить git diff --check;
- перечитать свои документы;
- сравнить каждый пункт AGENT_TASK.md с acceptance matrix;
- проверить diff на выход за scope;
- заполнить REPORT_TEMPLATE.md в финальном сообщении, не обязательно создавая отдельный файл.
