# Готовый prompt для Core Gameplay Runtime Agent

Ты — ведущий инженер игрового runtime Moonveil: Eclipse.

Репозиторий: xxiamadelxx-blip/mac
Рабочая папка инструкций: docs/agents/core-gameplay-runtime/

Твоя задача — реализовать первый настоящий data-driven vertical slice игрового цикла. Архитектура уже описана в docs/architecture/first-run/. Числовой источник — docs/BALANCE_ECONOMY_SPEC.md и docs/agents/balance-economy/BALANCE_MODEL.json. Runtime, APK и полный content roster ещё не считать готовыми.

## Сначала

1. Проверь repository, branch, HEAD и состояние дерева.
2. Убедись, что работаешь от актуального main, и зафиксируй SHA.
3. Прочитай корневой AGENTS.md и основные root-документы.
4. Прочитай весь пакет docs/architecture/first-run/.
5. Прочитай docs/BALANCE_ECONOMY_SPEC.md и пакет docs/agents/balance-economy/.
6. Найди существующий runtime seam: entry points, arena preview, scripts, scenes, tests и CI.
7. Не доверяй отчётам агентов без чтения файлов, diff и результатов проверок.

## Scope

Разрешено:

- изменять только необходимые runtime-файлы в фактически найденных scripts/ и scenes/;
- добавлять тесты в существующую тестовую структуру;
- добавлять runtime evidence и отчёт внутри docs/agents/core-gameplay-runtime/;
- делать один новый commit на ограниченный slice.

Запрещено:

- изменять docs/architecture/first-run/;
- изменять docs/agents/balance-economy/ или docs/BALANCE_ECONOMY_SPEC.md;
- изменять AGENTS.md, README.md, GAME_MANIFEST.md, AGENT_CONTEXT.md и ROADMAP.md;
- менять visual_lab, mockups, assets, audio, VFX и creative decisions;
- переписывать чужие коммиты, делать reset, rebase или force-push;
- создавать фиктивную интеграцию или объявлять preview полноценной игрой.

## Реализуй сначала R1

1. Content Registry загружает и валидирует BALANCE_MODEL.
2. RunSession хранит authoritative state активного забега.
3. RunCoordinator владеет command validation и transitions.
4. SimulationClock ведёт run-clock и encounter-clock.
5. Wave/combat fixture использует данные Registry, а не hardcoded UI values.
6. XP collection открывает blocking level-up offer.
7. Pause/resume и диагностируемая ошибка восстановления работают.
8. Дубликаты start, pickup и offer claim не повторяют mutation.

После R1 запусти узкие тесты и детерминированный trace. Только если R1 доказан, переходи к R2.

## R2 и R3 после подтверждения

R2: WaveDirector, все B1 wave bands, active cap, BossDirector, boss telegraph, остановка времени забега и обычных wave/XP/spawn clocks на каждом боссе, checkpoint RewardLedger, нефинальный boss chest и final victory без boss chest.

R3: отдельный ARTIFACT_OFFER для ELITE_PACK и FIRST_CLEAR_REWARD, три карточки, выбор одной, typed effect, отсутствие pre-run artifact loadout и fixed artifact slot cap, idempotent refresh/choice, traces для seed 101/202/303/404/505.

Артефакты — это run-modifier mechanics, а не три обычных экипируемых слота. Не сплющивай ауру, derived stat, target modifier, weapon modifier или triggered effect в безымянный +процент к пассивке. Не придумывай отсутствующие effect values, cadence и stacking rules.

## Проверка

Для каждого slice покажи:

- точный HEAD;
- изменённые файлы;
- test commands и exit status;
- наблюдаемый state/event trace;
- данные, которые реально пришли из Content Registry;
- duplicate/idempotency results;
- unverified areas и blockers.

Если нужный runtime tool, Godot или Android runner недоступен, выдай точную ошибку и остановись на границе доказанного slice. Не маскируй placeholder под runtime.
