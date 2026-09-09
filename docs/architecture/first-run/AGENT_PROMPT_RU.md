# Готовый prompt для нового чата агента

Ты — ведущий системный архитектор первого полного забега Moonveil: Eclipse.

Рабочий репозиторий: xxiamadelxx-blip/mac
Рабочая папка: docs/architecture/first-run/

REPO_CONTEXT.md — исторический baseline, а не live HEAD. Перед началом самостоятельно проверь текущие repository, branch и HEAD. Расхождение с prepared_from_main_sha не является ошибкой и не требует переписывать context packet.

Твоя задача — не написать общий список идей и не сделать вид, что runtime уже существует. Твоя задача — на основании текущего репозитория спроектировать логическую архитектуру первого 20-минутного забега так, чтобы следующий coding-агент мог реализовать её по проверяемому контракту.

## Сначала

1. Проверь, что это именно репозиторий xxiamadelxx-blip/mac.
2. Прочитай AGENTS.md.
3. Прочитай README.md, GAME_MANIFEST.md, AGENT_CONTEXT.md и актуальный раздел ROADMAP.md.
4. Прочитай docs/BALANCE_ECONOMY_SPEC.md. Это единственный baseline для чисел, формул, XP, волн и rewards.
5. Прочитай docs/architecture/first-run/README.md, AGENT_TASK.md, REPO_CONTEXT.md, SKILLS_AND_INSTRUCTIONS.md и DECISIONS_AND_UNKNOWNS.md.
6. Проверь branch, HEAD и состояние дерева до изменений.
7. Не доверяй заявлениям о готовности без файлов, diff, проверок или другого evidence.

## Навыки

Перед существенной работой загрузи доступные системные навыки:

- atlas-scout:atlas-scout-code-navigation — для структурного понимания кода и связей;
- keystone:project-audit — для read-only проверки состояния репозитория и drift между документами и реальностью;
- keystone:product-planning — для формализации пользовательского потока, состояний, правил и технических границ;
- keystone:task-creation — для разложения архитектуры на последовательные вертикальные срезы;
- codex-engineering-guardrails:code-verification — для независимой проверки документов, JSON, ссылок и acceptance matrix.

Навыки нужно прочитать полностью до использования. Если конкретный skill недоступен, зафиксируй это в отчёте одной строкой и используй безопасный fallback. Для Atlas Scout GitHub tree/точечное чтение/rg — штатная замена, не блокер и не причина останавливать работу. Code-work не нужен: в этой задаче запрещена реализация runtime. Visual Lab нужен только если ты решишь менять visual/art assets, а это запрещено.

## Что нужно описать

Опиши полный маршрут:

включение → splash/loading → главное меню → настройки → ПЕРСОНАЖИ → выбор персонажа → подготовка забега → арена → волны → XP и уровень → выбор оружия/пассивки → максимизация → проверка синергии → босс → checkpoint → сундук → синергия или fallback-награда → следующая стадия → пауза/настройки/возврат к игре → смерть или победа → итоговая статистика → rewards/unlocks → главное меню → новый забег или продолжение.

Обязательно включи:

- боссы на 5, 10, 15 и 20 минутах;
- временные диапазоны волн и active cap из канона;
- XP отдельно от тел, останков и следа боя;
- оружие, пассивные умения, артефакты и синергии;
- характеристики атаки, критического шанса, критического множителя, скорости, cooldown и другие поля, необходимые HUD/информации;
- список текущего оружия, пассивок, синергий, артефактов и счётчик убийств;
- pause/resume, выход в меню, Android background/resume;
- death/victory и checkpoint reward;
- reward ledger с idempotency;
- локальное версионируемое сохранение;
- диагностируемые ошибки без белого экрана;
- тонкий vertical slice и дальнейшее расширение.

## Что создать

Изменяй только docs/architecture/first-run/.

Создай:

- FIRST_RUN_FLOW.md — end-to-end user flow и observable states;
- FIRST_RUN_STATE_MACHINE.md — state machine с переходами, ownership и edge paths;
- FIRST_RUN_ARCHITECTURE.md — модули, boundaries, data flow, persistence, UI projection и tradeoffs;
- FIRST_RUN_DATA_CONTRACT.json — валидный machine-readable contract сущностей, run snapshot, events, rewards и invariants;
- FIRST_RUN_EVENT_CATALOG.md — события, payload, producer/consumer, idempotency и failure handling;
- FIRST_RUN_ACCEPTANCE_MATRIX.md — requirement → behavior → evidence → status.

Не создавай пустые файлы и не добавляй папки «на будущее» без содержания.

## Правила принятия решений

- Не выдумывай числовые значения, имена контента, цены, длительности и условия.
- Канонические числовые значения бери только из docs/BALANCE_ECONOMY_SPEC.md.
- Если в документах конфликт, не скрывай его: запиши конфликт, временное решение, confidence и владельца следующего решения.
- Если термин «накопление бонуса» не определён, смоделируй расширяемый bonus/series state и пометь точную механику PENDING_PRODUCT_DECISION.
- Если exact synergy roster или chest fallback rules отсутствуют, проектируй интерфейс данных и eligibility evaluator, но не придумывай конкретные комбинации.
- Делай технический выбор самостоятельно в рамках канона и фиксируй tradeoff. Не задавай серию мелких вопросов; выноси вопрос только если он действительно блокирует контракт.
- Не называй architecture ready-to-ship, runtime implemented или M1 complete. Документирование и реализация — разные статусы.

## Границы

Не изменяй:

- scripts/, scenes/, project.godot, export_presets.cfg;
- README.md, GAME_MANIFEST.md, AGENT_CONTEXT.md, ROADMAP.md;
- docs/BALANCE_ECONOMY_SPEC.md;
- docs/mockups/, docs/manifests/, docs/audio/;
- любые PNG, SVG, TSCN, GDScript или другие runtime/art files.

## Синхронизация перед работой

Если чат стартовал на старой ветке или commit, сначала сравни его с актуальным main и используй живые канонические документы. Не выдавай обнаруженное отличие HEAD за неисправность репозитория. Не force-push и не изменяй чужую активную ветку.

## Проверка

Перед финалом:

1. Проверь, что все шесть обязательных файлов существуют.
2. Проверь FIRST_RUN_DATA_CONTRACT.json командой валидатора JSON.
3. Проверь внутренние ссылки на существующие repo paths.
4. Выполни git diff --check, если доступен Git.
5. Сверь acceptance matrix с каждым требованием AGENT_TASK.md.
6. Проверь, что PENDING/TBD значения перечислены в DECISIONS_AND_UNKNOWNS.md.
7. Проверь diff на случайные изменения вне рабочей папки.
8. Не считай summary агента доказательством: сам прочитай итоговые файлы и результаты проверок.

## Финальный ответ

Используй REPORT_TEMPLATE.md. Обязательно укажи:

- VERIFIED, PARTIAL или BLOCKED;
- точный список файлов;
- branch и HEAD;
- реальные команды, exit status и результаты;
- принятые решения и pending;
- ограничения и что не сделано;
- следующий рекомендуемый vertical slice.

Если исходные документы недоступны, не восполняй их воображением: сообщи, какой именно источник недоступен и какие части поэтому inconclusive.
