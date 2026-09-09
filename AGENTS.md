# Agent Instructions — Moonveil: Eclipse

Этот файл обязателен для любого агента, работающего в репозитории xxiamadelxx-blip/mac.

## 1. Обязательный старт

Перед существенной работой:

1. Проверь идентичность репозитория: xxiamadelxx-blip/mac.
2. Прочитай README.md, GAME_MANIFEST.md, AGENT_CONTEXT.md и актуальный раздел ROADMAP.md.
3. Проверь текущую ветку, HEAD и состояние дерева перед изменением.
4. Если задача касается visual, design, art, asset, UI-visual, animation, VFX, environment, character, enemy, boss, weapon, icon, portrait или mockup, обязательно прочитай в указанном порядке:
   - visual_lab/README.md;
   - visual_lab/VISUAL_POLICY_RULE.md;
   - visual_lab/VISUAL_LAB_PRODUCTION_LAW.md;
   - visual_lab/ASSET_PIPELINE_CODE.md;
   - visual_lab/REVIEW_CHECKLIST.md;
   - соответствующий документ и папку из docs/mockups, docs/manifests или docs/audio.
5. Если решение меняет ещё не зафиксированное лицо, силуэт, композицию, цветовую систему, крупный UI-поток или другую существенную пользовательскую часть, остановись на границе творческого решения и запроси выбор Creative Director до production-реализации.
6. Для готового утверждённого направления используй стабильные asset/family IDs, provenance и runtime manifest. Не создавай одноразовые визуальные файлы без связи с ними.

## 2. Обязательная маршрутизация Visual Lab

Visual Lab — обязательный вход для всех visual/design/art задач. Нельзя:

- сразу отправлять результат генерации в production;
- считать PNG, SVG, мокап, скриншот или технически корректный экспорт утверждённым артом;
- запускать batch из направлений или анимаций до проверки одного hero master;
- исправлять повторяющийся дефект вручную на каждом персонаже, если его можно исправить в family/template/pipeline;
- объявлять artistic approval от имени модели, агента, теста, Playwright или preflight;
- превращать candidate capture в golden baseline без явного approval Creative Director.

Обязательная цепочка:

SOURCE/CANON AUDIT -> VISUAL FAMILY -> HERO MASTER -> CANDIDATE + PROVENANCE -> USER REVIEW -> EDITABLE MASTER -> VARIANTS -> RUNTIME EXPORT -> TECHNICAL QA -> TRUE GAMEPLAY-SCALE PREVIEW -> USER FINAL APPROVAL -> GOLDEN/MANIFEST -> PRODUCTION.

Technical PASS и artistic approval — разные состояния. Прохождение размеров, pivot, anchors, hashes, lint или тестов не разрешает производственное продвижение.

## 3. Состояния визуального результата

Каждый новый или существенно изменённый визуальный результат должен иметь одно состояние:

- PROPOSAL — идея или направление;
- CANDIDATE — конкретный результат с candidate ID и provenance;
- TECHNICAL PASS — техническая проверка пройдена, художественное approval не выдано;
- USER REVIEW — материал передан Creative Director;
- APPROVED GOLDEN — именно этот визуал явно утверждён пользователем и закреплён с хэшем;
- PRODUCTION — подключён к runtime manifest и используется игрой.

Отсутствие явного статуса означает, что результат не разрешено считать production art.

## 4. Границы доменов

- Visual/design/art агенты владеют визуальной системой, кандидатами, источниками, вариантами, review-pack и manifest-привязками; они не меняют игровую механику молча.
- Animation/VFX агенты представляют уже рассчитанные игровые события; они не определяют hit, damage, legality, timing rules или результат атаки.
- UI агенты объясняют существующее состояние и правила; они не прячут причинность механики и не выдают технический pass за художественное approval.
- Code/runtime агенты потребляют approved manifests и не перерисовывают визуальный контракт по своему усмотрению.
- Gameplay- и data-агенты не могут заменить visual family случайным placeholder без явного маркированного fallback.

## 5. Правила текущего проекта

- Канонические визуальные решения Moonveil находятся в README.md, GAME_MANIFEST.md, AGENT_CONTEXT.md и stage-документах; Visual Lab управляет производственным процессом и воротами.
- Existing assets в docs/mockups остаются в статусах, записанных в их документах. Перенос Visual Lab не утверждает их задним числом.
- visual_lab/ — process package, а не Godot runtime dependency. Игра не должна требовать Pixelorama, Tiled, ComfyUI, Playwright или другой authoring/QA-инструмент для запуска.
- Все кандидатные изображения, исходники, экспорты и review captures должны быть воспроизводимыми настолько, насколько это поддерживает используемый инструмент.
- Не удаляй и не заменяй пользовательскую работу без явного основания. Не смешивай этот репозиторий с браузером, VPN, оркестратором, dice roller или Out of the Abyss runtime.

## 6. Definition of Done для визуальной работы

Работа считается завершённой только если:

- результат лежит в правильной stage/family папке;
- есть стабильный ID, provenance и связь с нужным manifest/документом;
- пройдены подходящие технические проверки;
- есть enlarged и true 1x gameplay-scale preview, а для world/battle asset — map/scene context;
- отдельно зафиксированы technical status и user artistic status;
- явное approval Creative Director существует для перехода в APPROVED GOLDEN;
- нет незаявленного placeholder, broken dependency или незакрытой заглушки в границах задачи;
- следующий агент может продолжить без догадок.

План, имя файла, созданная папка или красивый preview сами по себе не являются evidence готовности.
## 7. Специализированный маршрут UI / art / sprite / mockup

Для задач UI, UI-art, art, sprite и mockup после `visual_lab/REVIEW_CHECKLIST.md` обязательно прочитай `visual_lab/UI_ART_SPRITE_MOCKUP_WORKFLOW.md` и следуй его маршруту.

- Выбери один primary route: `UI_ART`, `SPRITE`, `ART` или `MOCKUP`; укажи точную stage-папку, `asset_id`, `family_id`, `candidate_id` и статус.
- Для UI проверяй реальный `390x844`, safe area, localization, touch-target и состояния; для sprite/art — enlarged, true `1x` и representative scene/map context.
- Mockup, PNG, screenshot и технический pass остаются proposal/candidate/evidence, пока Creative Director явно не утвердил exact candidate.
- Default handoff для запроса только на визуал останавливается на `USER REVIEW`; runtime integration требует отдельного явного запроса, approval и manifest linkage.
- Если creative decision не зафиксировано, batch не начинай: вынеси открытые варианты и запроси выбор пользователя/Creative Director.

Обязательный handoff содержит: `route`, `stage_path`, `asset_kind`, `asset_id`, `family_id`, `candidate_id`, `status`, `technical_status`, `artistic_status`, `manifest/consumer`, `open_decisions` и `next_action`.
