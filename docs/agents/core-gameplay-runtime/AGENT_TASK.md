# Задание Core Gameplay Runtime Agent

## 1. Роль

Ты — владелец реализации первого data-driven игрового runtime-среза Moonveil: Eclipse.

Архитектурный агент уже подготовил и проверил логический контракт первого забега. Балансовый агент подготовил числовую модель и не может подтвердить её в игре, пока не появится настоящий потребитель. Твоя задача — реализовать минимальный runtime seam и предоставить проверяемые traces, не переписывая документы этих агентов.

## 2. Главная цель

Довести первый vertical slice от создания забега до проверяемого игрового цикла:

- загрузить баланс через Content Registry;
- создать RunSession и RunCoordinator;
- запустить run-clock и encounter-clock;
- провести детерминированную волну;
- обработать combat, HP, XP и level-up offer;
пережить разделённую main-boss/mini-boss clock policy;
- провести checkpoint/chest/fallback или final victory;
- записать результат через RewardLedger;
- доказать повторное воспроизведение и idempotency.

Не требуется закрывать сразу все ассеты, UI, полный roster, визуальные эффекты или APK. Не разрешается объявлять полный первый забег готовым после одного preview.

## 3. Обязательный старт

Перед первым изменением:

1. Проверь repository, branch, HEAD и рабочее дерево доступным способом.
2. Сверь HEAD с актуальным main и зафиксируй SHA.
3. Прочитай AGENTS.md, README.md, GAME_MANIFEST.md, AGENT_CONTEXT.md и ROADMAP.md.
4. Прочитай docs/architecture/first-run/README.md, FIRST_RUN_ARCHITECTURE.md, FIRST_RUN_STATE_MACHINE.md, FIRST_RUN_DATA_CONTRACT.json и FIRST_RUN_EVENT_CATALOG.md.
5. Прочитай docs/BALANCE_ECONOMY_SPEC.md, docs/agents/balance-economy/README.md и BALANCE_MODEL.json.
6. Найди фактические runtime entry points, preview-only code, existing tests и CI commands.
7. Составь короткий collision/scope report. Если найдено чужое незакоммиченное изменение в зоне будущего edit, остановись и зафиксируй конфликт.

## 4. Вертикальные срезы

### R1 — Core run loop

Реализуй:

- ContentLoader/Content Registry с schema/content-version validation;
- RunSession с selected character, run_id, seed, state, revision, stage, clocks, build, stats и diagnostics;
- RunCoordinator с command validation и transitions;
- SimulationClock с run-clock и encounter-clock;
- один минимальный data-driven wave fixture из B1;
- базовый combat путь с HP, damage, hit cooldown и defeat fact;
- XPDrop collection, XP threshold и blocking level-up offer;
- pause/resume и recoverable diagnostic error;
- тесты на duplicate start, duplicate pickup, offer claim и clock freeze.

R1 считается проверенным только если фактический test/trace показывает работающий state progression. Создание классов без вызова из реального entry point не считается реализацией.

### R2 — Основные/мини-боссы, 30-минутные волны и settlement

После зелёного R1 добавь:

- WaveDirector с data-driven bands на 30-минутном envelope, spawn budget и active cap;
- BossDirector с безопасным spawn, telegraph, encounter ID и defeat event для основных и мини-боссов;
- 6 основных боссов (текущие 4 плюс 2 новых) и 5 мини-боссов; имена, состав и cadence приходят из синхронизированных architecture/content/B1-источников;
- единое состояние времени для MAIN_BOSS: с MAIN_BOSS_INTRO останавливаются run clock и обычные wave/XP/spawn clocks, а encounter clock идёт только в MAIN_BOSS_ACTIVE;
- отдельное состояние давления для MINI_BOSS: run clock, волны, XP и обычные spawn продолжаются в MINI_BOSS_INTRO/MINI_BOSS_ACTIVE; mini-boss encounter clock идёт во время активного боя;
- checkpoint settlement через RewardCalculator/RewardLedger;
- нефинальный main-boss chest с eligibility/fallback outcome contract; defeat мини-босса может создать отдельный MINI_BOSS_CHEST, но он не смешивается с BOSS_CHEST или artifact offer;
- final main boss at 30:00 → RUN_VICTORY без boss chest;
- elite-варианты обычных противников как условный bounded слой, а не постоянный roster: ограниченные spawn budget/active cap/eligibility/expiry; defeat/eligibility может дать отдельный ELITE_CHEST для дополнительного сундука и давления орды;
- повторную доставку defeat/checkpoint/chest claim без повторной выдачи.

Если B1 сохраняет пятиминутный baseline, ожидаемые main-boss boundaries — 5, 10, 15, 20, 25 и 30 минут. Пока architecture/B1 не синхронизированы, runtime хранит это как contract boundary, а не как локально выдуманные числовые настройки.

### R3 — Artifact offer и traces

После зелёного R2 добавь:

- ARTIFACT_OFFER как отдельное blocking state;
- source ELITE_PACK для artifact offer между боссами и source FIRST_CLEAR_REWARD после result; отдельный ELITE_CHEST от условных elite-вариантов не считается artifact offer без явного product/B1 mapping;
- ровно три candidate cards и выбор ровно одной;
- typed artifact effect, отдельный от BuildInventory и обычных passive slots;
- artifact refresh как отдельную idempotent command с pending policy, если cost/limit не заданы;
- отсутствие fixed artifact capacity и pre-run artifact selection;
- traces для seed 101, 202, 303, 404 и 505.

В R3 не изобретай отсутствующие effect values, cadence, duplicate или stacking rules. Выводи PENDING_PRODUCT_DECISION и сохраняй typed seam.

### R4 — Runtime scale and Android evidence

Только после domain proof:

- подключи реальные scene adapters;
- проведи Android/CI build;
- проверь performance и object caps на целевом устройстве или доступном эквиваленте;
- добавь UI projections, pause/background recovery и diagnostics;
- выдай отдельный build/install evidence.

R4 не смешивается с R1. Если Godot или Android runner недоступен, честно оставь блокировку и не подменяй её фиктивным APK.

## 5. Правила реализации

- Не переносить числовые параметры в UI или произвольные controllers.
- Не превращать RunCoordinator в god controller.
- Не давать UI, scene node или telemetry право менять RunSession напрямую.
- Не использовать preview arena как доказательство полноценного run loop.
- Не смешивать XP, chest, artifact, corpse/aftermath и wallet entries.
- Не создавать artifact slots, pre-run artifact loadout или boss chest для final main boss. Не превращать bounded elite-варианты в постоянный roster.
- Не менять архитектурные и балансовые исходники для устранения runtime-проблемы.
- При недостающем контракте создать диагностируемый pending/blocker, а не придумать значение.
- Один slice — один ограниченный commit. Не менять существующие коммиты и не выполнять force-push.

## 6. Обязательный отчёт после slice

Отчёт должен содержать:

- repository, branch, точный HEAD и parent;
- статус R1/R2/R3/R4: IMPLEMENTED, TESTED, RUNTIME_VERIFIED, BLOCKED или PARTIAL;
- список изменённых файлов и проверку scope;
- источник каждого подключённого data field;
- команды и exit status;
- test output и детерминированные traces;
- проверку duplicate/idempotency;
- что фактически работает, а что только спроектировано;
- риски, pending decisions и точный следующий slice.

Не использовать слова DONE, PLAYABLE, APK READY или VERIFIED без соответствующего evidence.
