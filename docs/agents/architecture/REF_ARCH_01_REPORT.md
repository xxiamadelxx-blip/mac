# REF-ARCH-01 — архитектурный отчёт по reference-репозиториям

## Handoff

- TASK-ID: REF-ARCH-01
- Repository: xxiamadelxx-blip/mac
- Branch: main
- Parent HEAD: d23019af2f98463bf5d72026a9e5deeff54beb18
- Resulting HEAD: a9e49743bac4740af061cbbcb0ac2ee63dcc5216
- Changed files: docs/agents/architecture/REF_ARCH_01_REPORT.md
- Status: VERIFIED_RESEARCH
- Scope: read-only исследование пяти внешних репозиториев и архитектурные рекомендации для MAC; runtime-код, сцены MAC, баланс, mockups и assets не изменялись.
- Canonical engine: Godot 4.x, native 2D, GDScript. Unity/C# и Godot/C# ниже являются только сравнительными источниками паттернов; миграция MAC на Unity не предлагается.

Статус VERIFIED_RESEARCH означает, что источники, пути файлов, применимость и ограничения проверены по опубликованным деревьям и содержимому файлов. Он не означает, что runtime, APK, баланс или visual production MAC готовы.

## 1. Метод и границы

Исследование выполнено по default branch main каждого указанного публичного репозитория. Для каждого источника:

1. проверено рекурсивное дерево репозитория;
2. прочитаны выбранные исходники менеджеров, планировщиков, ресурсов, прогрессии, input и сцен/asset-описаний;
3. отдельно проверено наличие или отсутствие object-pooling и dedicated mobile-input seams;
4. архитектурное решение сформулировано как переносимый принцип, без копирования кода, имён, персонажей, ассетов, чисел или визуального дизайна.

Источники MAC, прочитанные до исследования:

- AGENTS.md;
- docs/AGENT_SYNC_STATE.md;
- README.md, GAME_MANIFEST.md, AGENT_CONTEXT.md, ROADMAP.md;
- docs/BALANCE_ECONOMY_SPEC.md;
- docs/architecture/first-run/README.md, AGENT_TASK.md, DELIVERABLES.md, REPO_CONTEXT.md;
- FIRST_RUN_ARCHITECTURE.md, FIRST_RUN_STATE_MACHINE.md, FIRST_RUN_FLOW.md, FIRST_RUN_DATA_CONTRACT.json, FIRST_RUN_DATA_CONTRACT.template.json, FIRST_RUN_EVENT_CATALOG.md, FIRST_RUN_ACCEPTANCE_MATRIX.md и ARCHITECTURE_AUDIT.md;
- scripts/runtime/content_registry.gd, simulation_clock.gd, wave_director.gd, boss_director.gd, run_session.gd и run_coordinator.gd;
- docs/agents/content-design/CONTENT_HANDOFF.md и docs/agents/balance-economy/BALANCE_MODEL.json.

Актуальный coordination baseline требует 30:00 / 1800 секунд, 6 main-boss slots, 5 mini-boss slots, MAIN_BOSS freeze и MINI_BOSS continuation. В существующих first-run документах остаются несовпадающие исторические/working-assumption формулировки; это отмечено в блокерах и не замаскировано этим research report.

## 2. Карта исследованных репозиториев

| Репозиторий | Движок и язык | Дерево | Главный найденный паттерн | Применимость к MAC | Что не переносить | Приоритет | Зависимости |
|---|---|---:|---|---|---|---|---|
| [murparreira/vampire-survivors-clone-godot-4](https://github.com/murparreira/vampire-survivors-clone-godot-4) | Godot 4.x / GDScript | 404 записей | Node-менеджеры, Timer, WeightedTable, PackedScene и Resource/.tres | P1 как Godot reference для typed resources, scene wiring и простого XP/upgrade seam | Не переносить монолитный timer-driven manager, hard-coded difficulty steps, прямой instantiate в hot path и sample content | P1 | Runtime, Content Registry, Balance |
| [sh-cho/godot-survivor-tutorial](https://github.com/sh-cho/godot-survivor-tutorial) | Godot 4.x / GDScript | 201 запись | Минимальный tutorial seam: EnemyManager, ExperienceManager, UpgradeManager, Ability Resource и InputMap | P1 для раннего vertical slice и Godot-подхода к Resource/PackedScene | Не переносить debug-параметры, tutorial-level numbers, отсутствие pool и отсутствие screen-touch adapter | P1 | Runtime, Content, UI |
| [matthiasbroske/VampireSurvivorsClone](https://github.com/matthiasbroske/VampireSurvivorsClone) | Unity / C# | 1112 записей | Пулы по типам сущностей, LevelBlueprint, keyframe spawn table, AbilityManager и touch joystick | P0 для pool lifecycle и разделения entity registry; P1 для progression/input seams | Не переносить Unity API, C# классы, случайный unseeded RNG, монолитный LevelManager и chest-ссылку на final boss | P0/P1 | Runtime, Balance, Content, QA |
| [sentry-demos/unity](https://github.com/sentry-demos/unity) | Unity / C# | 1058 записей | Чистый SpawnDirector без Unity objects, отдельные таймеры и тесты; чистые LevelProgression и distinct upgrade draw | P0 для тестируемого scheduling contract и P1 для progression/mobile adapter | Не переносить Unity Input System, Instantiate-based spawner, Time.timeScale как источник истины и sample telemetry/config | P0/P1 | Runtime, Balance, CI/QA |
| [DarkRewar/SurvivorsStarterKit](https://github.com/DarkRewar/SurvivorsStarterKit) | Godot 4 / C# | 1093 записи | Godot scenes/.tres с C# manager; resource-driven powerups и prefab composition | P1 только как evidence Godot scene/resource wiring и явного asset linkage | Не переносить C# runtime, manager-as-whole-game, per-frame spawn/XP UI coupling, внешние sample assets | P1 | Runtime, Content, Visual Lab |

## 3. Findings по каждому источнику

### 3.1 murparreira — Godot/GDScript

| Конкретный путь источника | Найденный паттерн | Применимость к MAC | Что нельзя переносить | Приоритет / зависимости |
|---|---|---|---|---|
| [scenes/managers/enemy_manager.gd](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/main/scenes/managers/enemy_manager.gd) | EnemyManager получает PackedScene-ссылки, выбирает сцену через WeightedTable, использует Timer и создаёт врага в entity layer; spawn position проверяется относительно игрока и геометрии. Отдельного SpawnDirector в дереве не найдено. | Использовать только идею отдельного spawn adapter: выбор записи и вычисление позиции могут быть разными слоями; MAC должен оставлять schedule policy в SpawnDirector/WaveDirector и instantiation в adapter/pool. | Не объединять schedule, difficulty, boss event, despawn и end-screen в одном manager; не использовать hard-coded набор сцен и sample IDs. | P1; Runtime + Content Registry + Balance |
| [scenes/managers/arena_time_manager.gd](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/main/scenes/managers/arena_time_manager.gd) | Таймер времени эмитит difficulty increase и boss event; difficulty меняется дискретно через интервалы. | Сигнал boundary полезен как event seam, но MAC должен получать boundaries из versioned schedule registry и SimulationClock. | Не переносить фиксированный интервал и не делать Timer владельцем authoritative run time. | P1; Runtime + Balance |
| [scripts/weighted_table.gd](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/main/scripts/weighted_table.gd) | Небольшой weighted selection с исключениями и удалением элемента. | Подходит как локальная стратегия выбора состава/offer после добавления seeded RNG и проверки пустого пула. | Не использовать его как замену ContentRegistry, deterministic event envelope или reward ledger. | P1; Runtime + Content |
| [scenes/managers/experience_manager.gd](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/main/scenes/managers/experience_manager.gd) | XP manager держит текущий XP/target, эмитит experience_updated и level_up. | Сигнал + чистый progression command годятся для HUD projection и паузы на offer; authoritative XP остаётся в RunSession. | Не переносить встроенную growth constant и не отдавать UI право менять XP. | P1; Runtime + Balance |
| [scenes/managers/upgrade_manager.gd](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/main/scenes/managers/upgrade_manager.gd) | Upgrade pool строится из ресурсов, выбор исключает уже выбранные карты, max_quantity убирает завершённый upgrade. | Согласуется с MAC offer из трёх карточек, max-level guard и data-driven content. | Не переносить preload-список, sample names, веса и словарь состояния без versioned IDs/idempotency. | P1; Content + Balance + UI |
| [resources/upgrades/abilty_upgrade.gd](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/main/resources/upgrades/abilty_upgrade.gd) и [resources/upgrades/ability.gd](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/main/resources/upgrades/ability.gd) | Resource отделяет данные upgrade от ability controller scene и icon resource. | Принять как направление: MAC content records описывают identity/limits/effect refs, а runtime node реализует поведение. | Не переносить класс/поля/тексты и не считать Resource сам по себе балансным источником. | P1; Content Registry + Runtime |
| [resources/upgrades/longsword.tres](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/main/resources/upgrades/longsword.tres) и [scenes/managers/enemy_manager.tscn](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/main/scenes/managers/enemy_manager.tscn) | .tres и .tscn содержат реальные PackedScene, Script и Texture2D references; wiring выполняется asset-файлом, не рисованием в коде. | Для MAC это образец linkage: approved/accepted asset manifest → scene/resource reference → runtime consumer; отсутствующий ресурс должен давать diagnostic. | Не копировать texture, scene, names или visual composition; не подменять missing asset процедурным рисованием без маркированного fallback. | P1; Visual Lab + Runtime |

Итог по источнику: это полезный Godot-паттерн для первого среза, но не масштабируемая модель 30-минутного расписания. В нём нет обнаруженного object pool и нет отдельного mobile touch controller; дерево содержит ресурсы и input actions, но не готовый screen-touch seam.

### 3.2 sh-cho — Godot/GDScript tutorial

| Конкретный путь источника | Найденный паттерн | Применимость к MAC | Что нельзя переносить | Приоритет / зависимости |
|---|---|---|---|---|
| [scenes/manager/enemy_manager.gd](https://github.com/sh-cho/godot-survivor-tutorial/blob/main/scenes/manager/enemy_manager.gd) | EnemyManager использует Timer, WeightedTable, PackedScene и spawn outside view; при difficulty event в pool добавляется новый enemy scene. | Полезен для раннего adapter-теста spawn outside camera и для separation между scene reference и spawn policy. | Не переносить timer как schedule source, постепенное изменение числа врагов в manager и hard-coded difficulty thresholds. | P1; Runtime + Balance |
| [scenes/manager/enemy_manager.tscn](https://github.com/sh-cho/godot-survivor-tutorial/blob/main/scenes/manager/enemy_manager.tscn) | Сцена явно связывает script и enemy PackedScene refs, а Timer является отдельным child node. | Подтверждает Godot scene composition для небольших adapters; в MAC refs должны приходить через registry/factory boundary. | Не превращать scene wiring в скрытый content registry и не копировать sample scenes. | P1; Runtime + Content |
| [scenes/manager/experience_manager.gd](https://github.com/sh-cho/godot-survivor-tutorial/blob/main/scenes/manager/experience_manager.gd) | XP update и level_up идут через signals; level event является точкой открытия upgrade screen. | Можно применить как UI notification seam поверх RunSession command/result, сохранив XP и level authoritative в domain. | Не переносить debug target и growth number; сигнал не заменяет persisted state/replay guard. | P1; Runtime + UI |
| [scenes/manager/upgrade_manager.gd](https://github.com/sh-cho/godot-survivor-tutorial/blob/main/scenes/manager/upgrade_manager.gd) | Weighted pool, выбор без повторов, удаление maxed item и добавление unlockable upgrade после выбранного пути. | Подходит для deterministic offer generator и отдельной проверки pool exhaustion. | Не копировать progression order, sample weights, IDs или tutorial behavior; MAC offer boundary задаётся собственным контрактом. | P1; Content + Balance |
| [resources/upgrades/ability_upgrade.gd](https://github.com/sh-cho/godot-survivor-tutorial/blob/main/resources/upgrades/ability_upgrade.gd), [resources/upgrades/ability.gd](https://github.com/sh-cho/godot-survivor-tutorial/blob/main/resources/upgrades/ability.gd), [resources/upgrades/axe.tres](https://github.com/sh-cho/godot-survivor-tutorial/blob/main/resources/upgrades/axe.tres) | Ability resource наследуется от общего upgrade resource, хранит ID/limit/copy и ссылается на controller PackedScene. | Паттерн соответствует MAC separation: content identity и controller seam раздельны. | Не переносить tutorial class hierarchy, names, descriptions, limits и visual assets. | P1; Content + Runtime + Visual Lab |
| [project.godot](https://github.com/sh-cho/godot-survivor-tutorial/blob/main/project.godot) | InputMap содержит movement/pause actions; main scene/theme/icon заданы через res:// paths; emulate_touch_from_mouse не является touch gameplay implementation. | Использовать action-based input contract: keyboard/gamepad/touch adapter публикуют один movement vector и pause command. | Не считать emulate-touch настройку доказательством реального Android touch acceptance. | P1; Runtime + CI/QA |

Итог по источнику: хороший минимальный Godot seam для R1, но tree scan не выявил pool и dedicated mobile/joystick script. Его можно использовать как форму wiring, но не как target performance architecture.

### 3.3 matthiasbroske — Unity/C# comparative source

| Конкретный путь источника | Найденный паттерн | Применимость к MAC | Что нельзя переносить | Приоритет / зависимости |
|---|---|---|---|---|
| [Assets/Scripts/Gameplay/Pools/Pool.cs](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Scripts/Gameplay/Pools/Pool.cs) и [Assets/Scripts/Gameplay/Pools/MonsterPool.cs](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Scripts/Gameplay/Pools/MonsterPool.cs) | Базовый pool получает entity dependencies и prefab; MonsterPool разделяет create, take, return и destroy callbacks, включая activation/deactivation. | Это главный P0 pattern для MAC: PoolRegistry по stable content ID, явные acquire/release, reset перед повторным использованием, controlled max size и diagnostics при exhaustion. | Не переносить UnityEngine.Pool, MonoBehaviour lifecycle, prefab names или capacity numbers; MAC implementation должна быть Godot/GDScript. | P0; Runtime + QA + Balance |
| [Assets/Scripts/Monsters/EntityManager.cs](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Scripts/Monsters/EntityManager.cs) | EntityManager поднимает отдельные pools для monsters, projectiles, throwables, boomerangs, XP gems, coins, chests и damage text; использует living collections и spatial hash. | Применимо как граница entity services и как performance checklist: enemies, projectiles, XP, aftermath и chest не должны иметь одинаковый lifecycle. | Не делать один global god manager; не переносить spatial/hash implementation или sample collectables без MAC contract. | P0; Runtime + Performance QA |
| [Assets/Scripts/Monsters/MonsterSpawnTable.cs](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Scripts/Monsters/MonsterSpawnTable.cs) | Spawn rate, composition chance и HP multiplier задаются keyframes и интерполируются по времени. | Паттерн подходит для data-driven WaveDirector: phase records дают pressure curve, composition и stat refs; вычисление должно быть pure и seeded. | В источнике выбор использует engine Random.Range и не является MAC deterministic evidence; не переносить keyframe values. | P0; Balance + Runtime |
| [Assets/Scripts/Gameplay/LevelManager.cs](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Scripts/Gameplay/LevelManager.cs) | Один manager ведёт level time, ordinary spawn, mini/final boss gates, chest timer, game over и level passed. | Использовать как negative architecture evidence: schedule, combat lifecycle, result и chest нужно разделить в MAC RunCoordinator/domain owners. | Не переносить монолитный ownership, прямые PlayerPrefs reward writes, booleans для одного босса и отдельный final path без ledger. | P0; Runtime + Architecture |
| [Assets/Scripts/Character/Abilities/AbilityManager.cs](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Scripts/Character/Abilities/AbilityManager.cs) | Owned/new abilities разделены, выбор взвешен, доступность проверяется, upgradeable values регистрируются отдельно от UI. | Применимо к BuildInventory и OfferGenerator: owned/new pools, requirements, effect registration и возвращение невыбранных карт должны быть domain operations. | Не переносить class names, chance formulas, Luck behavior и random selection без MAC seed/state_revision. | P1; Runtime + Content + Balance |
| [Assets/Scripts/Character/TouchJoystick.cs](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Scripts/Character/TouchJoystick.cs) | Touch UI имеет permanent/dynamic mode, pointer down/up, radius clamp и callback movement vector; input control отделён от ability logic. | P1 reference для Godot InputAdapter: screen touch state → normalized vector → action bus/RunSession movement command, с reset в zero на release. | Не переносить Unity EventSystem/InputSystem or pointer coordinates; не связывать touch component напрямую с damage/wave/reward. | P1; Runtime + UI + QA |
| [Assets/Scripts/Monsters/BossMonster.cs](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Scripts/Monsters/BossMonster.cs) | Boss component выбирает ability по score и после defeat может вызвать loot/chest. | Использовать только разделение boss behavior/encounter effect; MAC boss defeat обязан идти через BossDirector, checkpoint и RewardLedger. | Не переносить случайный ability loop и главное: sample Final Boss.asset содержит chestBlueprint; это прямо конфликтует с MAC final-boss-no-chest и не принимается. | P0; Runtime + Architecture |
| [Assets/Blueprints/Monsters/Boss/Final Boss.asset](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Blueprints/Monsters/Boss/Final%20Boss.asset), [Assets/Blueprints/Monsters/Boss/Mini Boss.asset](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Blueprints/Monsters/Boss/Mini%20Boss.asset) | Boss blueprint хранит combat stats, ability prefab refs, sprite sequence и loot/chest blueprint reference. | Применимо как data-shape idea: boss record связывает behavior refs, telegraph, rewards и visual manifest через IDs. | Не переносить names, numbers, GUIDs, sprite sequence и chest policy; final boss MAC никогда не получает chest source. | P1; Content + Balance + Visual Lab |
| [Assets/Scenes/Game/Level 1.unity](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Scenes/Game/Level%201.unity) и [Assets/Prefabs/Monsters/Default Boss Monster.prefab](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Prefabs/Monsters/Default%20Boss%20Monster.prefab) | Scene/prefab содержат serialized component hierarchy, render/animation/particle refs и scene wiring; визуал не рисуется в manager code. | Подтверждает MAC rule: runtime consumes real imported scene/asset references через manifest/factory; visual and technical approval remain separate. | Не переносить Unity prefab format, GUIDs, particle look, hierarchy or any source visual design. | P1; Visual Lab + Runtime |

Итог по источнику: наиболее ценен pool/entity boundary и отделение ability selection от UI. LevelManager и final chest reference — полезные negative examples для MAC ownership и final-boss invariant.

### 3.4 sentry-demos — Unity/C# comparative source

| Конкретный путь источника | Найденный паттерн | Применимость к MAC | Что нельзя переносить | Приоритет / зависимости |
|---|---|---|---|---|
| [Assets/Scripts/SceneManagers/SpawnDirector.cs](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/SceneManagers/SpawnDirector.cs) | Чистый scheduling object решает only when: отдельные независимые таймеры для enemy, wave, pickup, spawn ramp и HP ramp; объект не владеет Unity objects и не instantiates. Locked wave не consume timer до открытия gate. | Это основной P0 reference для GDScript RefCounted SpawnDirector: принимает simulation time и registry policy, возвращает admission/ramp decisions, а spawner/pool выполняет side effects. Для MAC добавить schedule cursor, main freeze и mini continuation. | Не переносить C# Timer/Unity classes, sample rates, Time.time source и независимые правила без MAC registry/seed. | P0; Runtime + Balance |
| [Assets/Tests/EditMode/SpawnDirectorTests.cs](https://github.com/sentry-demos/unity/blob/main/Assets/Tests/EditMode/SpawnDirectorTests.cs) | Прямые тесты проверяют interval, re-arm, non-positive rate, locked wave timer, on-screen cap, независимость таймеров и rebase. | P0 test shape для MAC: unit tests без scene/Node, deterministic clock, cap-first behavior и no timer consumption while blocked. | Не переносить test names, values или Unity test framework. | P0; Runtime + CI/QA |
| [Assets/Scripts/SceneManagers/EnemySpawner.cs](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/SceneManagers/EnemySpawner.cs) | Spawner получает DifficultyCurve/WaveFormation, выбирает тип/размер волны, использует serialized prefab refs и SpawnArea, а manager управляет ordering. | Применимо как adapter split: WaveDirector принимает решение, EnemySpawner/PoolAdapter размещает нужный content ID и получает XP parent/config. | В источнике прямой Instantiate и childCount включает объекты во время death animation; это не pool/performance proof для MAC. | P0/P1; Runtime + QA |
| [Assets/Scripts/SceneManagers/LevelProgression.cs](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/SceneManagers/LevelProgression.cs) | Plain class без Unity/frame loop: AddXp, milestone window, TryLevelUp, max level и clamped progress; multi-level grant можно обработать циклом. | P0 reference для pure XP/level module поверх MAC RunSession; UI открывается только после реального transition. | Не переносить milestone array, starting values или implicit level semantics; цифры принадлежат B1. | P0; Runtime + Balance |
| [Assets/Scripts/Upgrades/UpgradeManager.cs](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/Upgrades/UpgradeManager.cs) и [Assets/Scripts/Upgrades/UpgradePathBase.cs](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/Upgrades/UpgradePathBase.cs) | Upgrade paths собираются из scene children, distinct draw выполняется без replacement, max-level path удаляется, presentation fields отделены от stable type identity. | P1 reference для триады: registry record → offer projection → one command; maxed record недоступен; analytics использует stable ID, не display copy. | Не переносить MonoBehaviour child discovery, MAX_LEVEL и display/type names, не смешивать artifact offer с weapon/passive offer. | P1; Content + UI + Balance |
| [Assets/Scripts/UI/FloatingOnScreenStick.cs](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/UI/FloatingOnScreenStick.cs) и [Assets/Scripts/UI/MobileControls.cs](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/UI/MobileControls.cs) | Touch stick clamp-ит drag в radius, публикует normalized Vector2, обнуляет значение на release; mobile controls включаются только на целевой платформе или при force flag. | P1 reference для Godot control adapter, platform gating и touch-target QA на 390x844; authoritative movement остаётся в simulation. | Не переносить Unity OnScreenControl, platform API, UI layout или sample range. | P1; Runtime + UI + Android QA |
| [Assets/Scripts/Weapons/WeaponBase.cs](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/Weapons/WeaponBase.cs) и [Assets/Scripts/Weapons/WeaponManager.cs](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/Weapons/WeaponManager.cs) | Weapon component имеет base cooldown/damage, manager держит run-local modifiers; scaled delta используется для freeze weapon cooldown во время pause. | Применимо как separation base content / derived run stats / weapon runtime. В MAC источником freeze будет SimulationClock, а не global time scale. | Не переносить static Player singleton, Unity Update и Time.deltaTime semantics в domain contract. | P1; Runtime + Balance |
| [Assets/Scripts/SceneManagers/BattleSceneManager.cs](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/SceneManagers/BattleSceneManager.cs) и [Assets/Resources/DemoConfig.asset](https://github.com/sentry-demos/unity/blob/main/Assets/Resources/DemoConfig.asset) | Scene manager связывает tuning asset, progression, SpawnDirector, spawners, HUD и audio; serialized asset references описывают battle configuration. | Полезно как wiring/read-model evidence: data asset → domain services → presentation adapters. Для MAC orchestration остаётся RunCoordinator, а tuning читается из Content Registry/B1. | Не переносить Sentry config, telemetry, crash hooks, Unity scene singleton и arbitrary tuning values. | P1; Runtime + CI/QA |

Итог по источнику: SpawnDirector и его tests — лучший reference для тестируемого scheduling boundary. Spawner сам делает Instantiate, поэтому это не рекомендация по allocation strategy.

### 3.5 DarkRewar — Godot 4/C# comparative source

| Конкретный путь источника | Найденный паттерн | Применимость к MAC | Что нельзя переносить | Приоритет / зависимости |
|---|---|---|---|---|
| [Scripts/Enemies/EnemyManager.cs](https://github.com/DarkRewar/SurvivorsStarterKit/blob/main/Scripts/Enemies/EnemyManager.cs) | Godot EnemyManager хранит enum→PackedScene mapping, active enemy list, spawn rate, boss spawn и stat upgrades; сцены загружаются через res://. Pool не найден. | Использовать только идею явного content ID→scene reference mapping и диагностируемого missing key. В MAC mapping должен быть в ContentRegistry/scene factory, не в manager. | Не переносить C# и dictionary enum, direct Instantiate на каждый spawn, coupling upgrade→spawn→reward. | P1; Runtime + Content |
| [Scripts/GameManager.cs](https://github.com/DarkRewar/SurvivorsStarterKit/blob/main/Scripts/GameManager.cs) | Один GameManager ведёт game time, spawn loop, XP, level, HUD и upgrade vote; enemy cap проверяется рядом с process logic. | Negative reference: MAC должен разделить RunSession, SimulationClock, SpawnDirector, Progression и projections; active cap обязан быть частью registry/policy. | Не переносить god-manager, per-frame XP UI mutation, embedded formula/number или vote logic. | P0; Runtime + Architecture |
| [Scripts/UI/UpgradeView.cs](https://github.com/DarkRewar/SurvivorsStarterKit/blob/main/Scripts/UI/UpgradeView.cs) | UI загружает реальную PackedScene карточки из res://, инстанцирует panel и связывает labels. | Применимо как presentation adapter: offer projection → UI card scene; UI не решает eligibility и не начисляет effect. | Не переносить C# node paths, UI copy или prefab layout. | P1; UI + Visual Lab + Runtime |
| [Powerups/Enemy/EnemySpawnRate.tres](https://github.com/DarkRewar/SurvivorsStarterKit/blob/main/Powerups/Enemy/EnemySpawnRate.tres) и [Powerups/Enemy/EnemyBossSpawn.tres](https://github.com/DarkRewar/SurvivorsStarterKit/blob/main/Powerups/Enemy/EnemyBossSpawn.tres) | .tres records ссылаются на scripts и хранят serialised description/stack data. | Подтверждает value of real resource references и schema-level metadata; MAC numbers остаются B1-owned. | Не переносить C# script class, descriptions, stack values или enemy powerup model. | P1; Content + Balance |
| [Prefabs/Enemies/enemy_minion.tscn](https://github.com/DarkRewar/SurvivorsStarterKit/blob/main/Prefabs/Enemies/enemy_minion.tscn), [Prefabs/Enemies/enemy_boss.tscn](https://github.com/DarkRewar/SurvivorsStarterKit/blob/main/Prefabs/Enemies/enemy_boss.tscn) и [Scenes/main_scene.tscn](https://github.com/DarkRewar/SurvivorsStarterKit/blob/main/Scenes/main_scene.tscn) | Godot scene files имеют ext_resource refs на scripts, PackedScene, particles, animation and collision subresources. | Паттерн реального asset linkage применим к MAC scene factory/manifest; runtime проверяет наличие approved resource и не рисует production visual в code. | Не переносить KayKit assets, scene hierarchy, particle design, C# script refs и sample names. | P1; Visual Lab + Runtime |

Итог по источнику: несмотря на Godot, этот kit не является GDScript reference. Он полезен для проверки res:// composition, но C# и manager coupling исключены из MAC.

## 4. Сводка по проверенным областям

| Область | Evidence | Решение для MAC | Приоритет | Зависимости |
|---|---|---|---|---|
| Enemy manager / spawn director | murparreira/sh-cho EnemyManager; Sentry SpawnDirector + EnemySpawner; Matthias EntityManager/MonsterSpawnTable | Разделить pure schedule/admission, data resolver, spatial placement и pool acquire. RunCoordinator оркестрирует; ни один manager не владеет всей игрой. | P0 | Runtime + Balance + Content |
| Object pooling | Matthias Pool/MonsterPool и EntityManager; recursive trees у murparreira, sh-cho, Sentry и DarkRewar не выявили comparable pool implementation | Ввести общий lifecycle для enemy/projectile/XP/aftermath/chest: acquire → setup → active → release → reset; active cap и pool exhaustion видимы в diagnostics. | P0 | Runtime + QA + performance |
| Weapon/ability resources | Godot Ability/AbilityUpgrade/.tres; Matthias AbilityManager/prefab families; Sentry WeaponBase/WeaponManager | Content record/Resource хранит stable ID, level/limit/effect ref и visual ref; runtime behavior — отдельный controller; UI получает projection. | P1 | Content + Balance + Visual Lab |
| Upgrade system | Godot WeightedTable/UpgradeManager; Sentry PickDistinct/UpgradePathBase; Matthias owned/new abilities | Offer generator выбирает допустимые records без повторов, maxed record исключается, command применяется ровно один раз. Artifact offer отдельный и всегда три карточки. | P0/P1 | Runtime + Content + Balance + UI |
| XP / level-up | Godot ExperienceManager signals; Sentry pure LevelProgression; DarkRewar GameManager coupling | Pure progression command меняет RunSession, emits/read-model event, pause-ит simulation на offer; duplicate XP pickup имеет idempotency key. | P0 | Runtime + Balance |
| Boss / wave progression | Matthias keyframe table/LevelManager; Sentry independent spawn/ramp timers; Godot arena time managers | Versioned schedule registry + WaveDirector + BossDirector. MAIN_BOSS freezes visible clock/wave/XP/ordinary spawn; MINI_BOSS continues; post-boss relief → ramp → peak. | P0 | Architecture + Content + Balance + Runtime |
| Mobile input | Matthias TouchJoystick; Sentry FloatingOnScreenStick/MobileControls; Godot sources only InputMap/emulate-touch | Godot InputAdapter maps touch down/drag/up to normalized action vector and zero release; no domain mutation from Control node; test 390x844 and background/resume. | P1 | Runtime + UI + Android QA |
| Scene/component structure | Godot .tscn/.tres ext_resource; Unity .prefab/.asset/.unity serialized refs; DarkRewar res:// refs | Use real PackedScene/Texture2D/Audio/Resource references from approved/accepted manifests; missing refs produce diagnostics/fallback, not procedural visual replacement. | P1 | Visual Lab + Runtime + CI |
| Boss chest / final rule | Matthias boss assets demonstrate chestBlueprint even on Final Boss; MAC sync-state requires final boss no chest | Keep chest source as explicit encounter record; final slot has no chest offer/generic defeat chest. This is a MAC invariant, not inherited from references. | P0 | Architecture + Content + Balance + Runtime |
| Determinism / telemetry | Sentry injected tests; Matthias engine random; Godot WeightedTable | Seed all selection, include wave_cycle_id/variant_id/selection_revision, preserve reward boundary independent of variant. | P0 | Runtime + QA + Balance |

## 5. Architecture decision for MAC

### 5.1 Target ownership

- ContentRegistry is the source for stable IDs, schedule records, asset refs and status/provenance.
- Balance model supplies wave budgets, active caps, XP/reward formulas and tuning status; no reference-repository number becomes MAC balance.
- SimulationClock is the authoritative gameplay clock. It is not wall time, UI Timer or Android lifecycle time.
- SpawnDirector is a pure policy object. It decides whether a spawn/ramp boundary is eligible and why.
- WaveDirector resolves phase, roster, pressure and active-cap admission from registry records.
- EnemyVariantResolver maps base_enemy_id + seed + wave_cycle_id + selection_revision to one variant record. A variant changes presentation/behavior data but does not silently create a second reward boundary.
- PoolRegistry owns allocation/reuse for high-churn entities. A pool item is reset before release/reacquire; XP and aftermath are distinct stores.
- Build/Progression owns XP, level, weapon/passive state and offer eligibility. It emits projections, not UI mutations.
- ArtifactOfferSystem is a separate source/outcome path. It presents exactly three cards, has no pre-run loadout and does not consume weapon/passive slots.
- BossDirector owns encounter identity and lifecycle; RewardLedger owns checkpoint/result mutation. Final boss defeat settles directly to victory without a boss chest.
- InputAdapter publishes normalized movement/pause intent; it does not call combat or reward code.
- SceneFactory/asset adapter resolves real PackedScene/resource references and reports missing/stale records. It never draws production visual shapes to conceal a missing asset.

### 5.2 Data flow

Content record → Registry validation → pure policy decision → domain command → pool/scene adapter side effect → authoritative RunSession mutation → event/read model → UI/persistence/telemetry.

The direction is one-way for mutation. UI and scene nodes may submit commands, but cannot set elapsed time, XP, build, reward wallet or boss outcome directly.

### 5.3 MAC-specific invariants retained during implementation

- 30:00 target run and 6 main-boss slots remain coordination targets.
- 5 mini-boss slots are the active runtime target; missing records remain a content/registry blocker.
- MAIN_BOSS freezes visible run clock, wave clock, XP and ordinary spawning from intro through settlement; a separate encounter clock can continue.
- MINI_BOSS does not freeze run clock, waves, XP or ordinary spawning.
- Boss chest is non-final and separate from artifact offer.
- Final main boss creates no boss chest and no generic defeat chest.
- Artifact offer has exactly three candidate cards, one choice, no pre-run artifact loadout and no weapon/passive slot consumption.
- A chest window can be offered/claimed once under an idempotency key; chest-window cap is independent from synergy claim cap.
- Unknown content blocks the authoritative dependent spawn with diagnostics; it does not silently substitute an unrelated enemy/boss.
- Numeric values absent from B1 remain PENDING_B1 or PENDING_PRODUCT_DECISION.

## 6. Что исследование не разрешает считать доказанным

- Ни один внешний repository не доказывает готовность MAC runtime, Android APK, 30-minute run, current content registry или R2/R3.
- Tutorial/Godot sample code does not prove pooling, deterministic replay or save/restore.
- Unity source cannot be used as a Unity migration proposal; only boundaries and test shapes are retained.
- Presence of .tscn/.tres/.prefab/.asset/.unity or PNG references proves linkage in the source repository, not artistic approval or production status in MAC.
- Direct Instantiate examples are not a performance guarantee. MAC needs pooling and fresh Android evidence.
- A boss asset with chest reference is not an authority over MAC final-boss policy.
- Source-repository numbers, names, descriptions, character identities and visual assets were not copied into MAC.
- No PNG, SVG, Base64 or ZIP was created or added.

## 7. Concrete runtime task candidates for MAC

These are implementation-sized tasks, not claims that the corresponding runtime already exists.

| ID | Runtime task | MAC area | Observable acceptance | Dependencies | Priority |
|---|---|---|---|---|---|
| R-REF-01 | Реализовать pure SpawnDirector и phase-aware WaveDirector adapter | scripts/runtime/ | Unit tests show independent enemy/wave/ramp timers, no consume while locked, active-cap admission, MAIN_BOSS freeze and MINI_BOSS continuation against current registry. | Architecture clock decision + Balance extension + Content registry | P0 |
| R-REF-02 | Ввести PoolRegistry/Poolable lifecycle для массовых entities | scripts/runtime/ и approved scene adapters | Repeated spawn/release reuses nodes after reset; enemy/projectile/XP/aftermath/chest counters stay bounded; no duplicate XP/reward event on reuse; diagnostics on exhaustion. | Runtime + QA + scene/resource refs | P0 |
| R-REF-03 | Реализовать deterministic EnemyVariantResolver | scripts/runtime/ | Same seed/revision returns same base/variant/wave selection; three Ink Beetle variant records are selected by data and remain one reward boundary; missing record blocks with diagnostic. | Content IDs + B1 tuning + Visual Lab marker records | P0 |
| R-REF-04 | Подключить XP/level/progression и three-card upgrade offer | scripts/runtime/ | XP pickup is idempotent, level transition opens one offer, choices are distinct, maxed records leave pool, weapon/passive mutation is one command, artifact offer remains separate with exactly three cards. | Content + Balance + UI projection | P1 |
| R-REF-05 | Собрать Godot vertical slice с mobile InputAdapter и fresh R2/R3 evidence | scripts/runtime/, scenes/adapters/ только в runtime-задаче | Movement touch down/drag/up maps to action vector; schedule → wave → XP → level → offer → boss/checkpoint/chest/final-no-chest → result path runs; Godot stdout, exit code and artifact are attached for Android/CI validation. | R-REF-01…04 + Content/Balance reconciliation + CI/QA + Visual asset intake | P0 |

## 8. Dependencies между агентами

| Агент | Required input для реализации | Граница ответственности |
|---|---|---|
| Architecture | One reconciled registry shape, 6 main + 5 mini, main freeze/mini continue, 15-window taxonomy, final no-chest invariant | Не меняет runtime код в рамках этого отчёта |
| Content | Stable IDs/records for pending main/mini/enemy/variant entries and asset manifest linkage | Names/mechanics/visual identity, not numeric lock |
| Balance | Parseable 30-minute waves, spawn budgets, active caps, ramp profiles, XP/reward/chest values and status labels | Numbers/formulas and simulation evidence, not runtime implementation |
| Runtime | Godot/GDScript implementation of pure policies, pools, registry consumers, RunSession commands and adapters | Code, tests and runtime behavior; no silent content invention |
| Visual Lab / asset pipeline | Real accepted/approved references and technical import evidence where required | Visual approval/asset provenance; not combat or reward rules |
| CI/QA | Godot stdout/exit code, artifact and Android performance evidence | Verification only; simulation output is not runtime proof |

## 9. Evidence

### 9.1 External source evidence

- Recursive GitHub trees were checked for all five repositories, including engine/language and presence/absence of pool, touch, scene, resource and test paths.
- 61 selected source paths were fetched for inspection across the five repositories: 12 murparreira, 12 sh-cho, 13 matthiasbroske, 14 sentry-demos and 10 DarkRewar.
- Source paths in sections 3.1–3.5 are direct GitHub links to the concrete files. The selected Sentry BattleScene path was confirmed in the repository tree; the connector did not return usable UTF-8 body for that large Unity scene, and no conclusion in this report depends on its body.
- Negative pool/mobile findings for the Godot tutorial sources and DarkRewar are based on recursive tree scans plus the selected manager files, not on an assumption that every file was opened.

### 9.2 MAC evidence

- Live repository identity: xxiamadelxx-blip/mac, branch main.
- Parent HEAD was read from the live main immediately before publication.
- Current sync-state explicitly records the active 30-minute/6-main/5-mini target, MAIN_BOSS freeze, MINI_BOSS continuation, final no-chest and R2/R3 evidence gap.
- Current runtime seams were read from ContentRegistry, SimulationClock, WaveDirector, BossDirector, RunSession and RunCoordinator. They already expose the intended separation points, but content reconciliation and fresh runtime evidence remain outside this report.
- No local checkout was available in the execution environment, so local git status, git branch, git diff --check and Godot/Android execution were not available. Publication and scope verification use GitHub tree/commit API fallback.

### 9.3 Checks performed for this report

- Source URL/path check: PASS for every linked concrete source path used in the report; missing/non-text source body noted above.
- Scope check before publication: one new Markdown file under docs/agents/architecture; no runtime, balance, content-design, architecture/first-run, mockup, scene, project or asset path included.
- Copy/design check: PASS; no source code block, binary, source asset, source character, source name or source tuning value was adopted as MAC content.
- Status check: PASS; research is labelled VERIFIED_RESEARCH, while runtime/APK/balance/visual approval are explicitly not claimed.
- Handoff completeness: PASS; required metadata fields are present, including exactly one final handoff action.

## 10. Blockers

These blockers belong to the MAC integration track and are intentionally not changed by REF-ARCH-01:

1. Registry reconciliation: active sync-state targets 5 mini-boss records, while current first-run documents and the live balance model still expose inconsistent mini-boss shapes/counts; current content proposals remain PROPOSED.
2. Clock contract drift: active sync-state and runtime BossDirector/RunCoordinator implement MAIN_BOSS freeze plus MINI_BOSS continuation, while current FIRST_RUN_DATA_CONTRACT and parts of the architecture audit still describe clock advancement through every boss.
3. Balance model status is PARTIAL: B1 is a 20-minute design baseline and the 30-minute extension remains proposed/simulation-only; values absent from B1 cannot be invented here.
4. R2/R3 runtime evidence is absent: no fresh Godot stdout, exit code and artifact prove the full schedule, pool, boss/chest, save/restore or Android path.
5. Visual/binary gates remain external: source references and mockups are not artistic approval, and current MAC asset intake/technical import evidence is incomplete.
6. The report’s comparative sources include direct-instantiation and final-boss-chest patterns that conflict with MAC invariants; they are recorded as negative evidence, not implementation dependencies.

No blocker was silently closed by this report.

## 11. Result interpretation

Designed by this report: a reference-informed boundary map and five implementation-sized runtime task candidates.

Implemented by this report: documentation only, in the allowed architecture report path.

Verified by this report: source-path evidence, engine classification, pattern applicability, non-transfer rules, priorities, dependency owners, MAC boundary mapping and publication scope.

Not implemented or verified here: Godot runtime, pooling code, scene wiring, Android input acceptance, full 30-minute run, balance lock, visual approval, APK, R2/R3 evidence and production assets.

## Handoff

- Parent HEAD: d23019af2f98463bf5d72026a9e5deeff54beb18
- Resulting HEAD: a9e49743bac4740af061cbbcb0ac2ee63dcc5216
- Changed files: docs/agents/architecture/REF_ARCH_01_REPORT.md
- Status: VERIFIED_RESEARCH
- Evidence: five repository trees, 61 selected source paths, current MAC sync/runtime documents, scope and report-content checks.
- Blockers: registry/clock reconciliation, PARTIAL B1, absent Godot/Android R2/R3 evidence and external visual/binary gates remain open.
- Next action: Core Gameplay Runtime Agent takes R-REF-01 and implements the pure Godot/GDScript SpawnDirector/WaveDirector test slice against the reconciled registry, without changing the reference report.
