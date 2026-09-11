# Skills и рабочие инструкции Runtime Agent

Эта папка не копирует системные skill-файлы. Она задаёт маршрутизацию. Каждый skill нужно прочитать полностью перед применением, если он доступен в текущем окружении.

## Обязательные навыки

| Skill | Когда использовать | Evidence |
|---|---|---|
| atlas-scout:atlas-scout-code-navigation | Структурно найти Godot entry points, symbols, callers и seams | Проверенные paths, symbols и фактические связи |
| keystone:project-audit | До первой записи: live repository, drift, dirty state и scope | HEAD, branch, status, findings и confidence |
| keystone:implementation | Любой runtime behavior change | Red/green или обоснованный fallback, diff и checks |
| codex-engineering-guardrails:code-work | Контролируемая реализация с protected scope | Точный список разрешённых и запрещённых paths |
| codex-engineering-guardrails:code-verification | Независимая проверка результата и требований | Команды, exit status, traces, contract checks |
| keystone:change-review | После нетривиального implementation slice | Scope review, regressions, unresolved risks |
| keystone:root-cause-analysis | Только при непонятном падении или противоречивом evidence | Доказанная причина до исправления |

Если task-creation недоступен или не нужен, не создавай новый planning package: используй уже проверенный порядок R1 → R2 → R3 → R4 из AGENT_TASK.md.

## Fallback без Atlas Scout

Atlas Scout — опциональный навигационный инструмент. Если capability не опубликована:

- используй GitHub tree/file reads и точечный поиск;
- при наличии checkout используй rg;
- не называй fallback локальным structural index;
- запиши ограничение одной строкой и продолжай.

Отсутствие Atlas Scout не оправдывает выдуманные entry points или недоказанный runtime.

## Обязательный протокол

1. Прочитать root instructions и этот пакет.
2. Зафиксировать live HEAD и collision matrix.
3. Найти реальный seam и его callers.
4. Для behavior change установить узкий red signal: failing test, reproduction или чётко зафиксированное отсутствие поведения.
5. Сделать минимальное изменение.
6. Запустить focused check.
7. Запустить regression/contract check.
8. Проверить diff на scope и архитектурные smells.
9. Создать handoff по RUNTIME_HANDOFF.md.
10. Перед финальным утверждением пройти change-review или явно указать pending review.

## Запрещённые подмены доказательства

Не считать proof:

- наличие нового класса без вызова;
- валидный JSON без фактической загрузки;
- preview-сцену без RunSession;
- ручной «удачный» забег;
- тест, который проверяет только вызов mock;
- сообщение агента без файла, diff и output;
- APK build без install/launch evidence;
- traces, сгенерированные не тем runtime, который будет потреблять игру.

## Маршрутизация Visual Lab

Visual Lab не нужен для доменного R1–R3. Если работа начинает менять sprite, portrait, UI-art, VFX, environment, animation или audio:

1. остановись на границе runtime consumer;
2. не изменяй визуальные файлы;
3. передай потребность через manifest/consumer contract;
4. направь визуальную задачу в Visual Lab согласно AGENTS.md.

Runtime Agent потребляет утверждённые manifests и не принимает художественные решения.


## Binary asset transport boundary

Runtime Agent не запрашивает бинарные файлы через чат и не принимает manifest за бинарное содержимое. Если runtime нужен новый visual asset, он создаёт только consumer/manifest contract и передаёт intake Binary Asset Transport Agent.
Runtime потребляет фактически проверенные файлы из build workspace; Storage credentials и сеть во время офлайн-игры не нужны. Никакой мутации или перегенерации героинь в рамках runtime task.



## Технические правила

- Балансные числа только через Content Registry.
- Domain rules отдельно от UI, persistence и framework glue.
- Stable IDs, revision и idempotency на повторных событиях.
- Никаких sleep, magic timing или special cases вместо модели clock.
- Не расширять slice после достижения его acceptance.
- Не исправлять unrelated drift.
- Не выполнять destructive git commands.
