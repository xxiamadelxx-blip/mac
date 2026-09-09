# Moonveil: Eclipse — Visual Lab Production Law

Статус: CANONICAL VISUAL PRODUCTION LAW.
Репозиторий: xxiamadelxx-blip/mac.
Decision authority: Creative Director проекта.
Дата переноса пакета: 2026-09-09.

## 1. Purpose

Visual Lab — production gate вокруг генераторов, editable source, экспортов, технической QA и человеческого художественного approval. Это не синоним image generator.

Канонический принцип:

TECHNICAL PASS != ARTISTIC PASS.

Asset может пройти размеры, pivot, anchors, hash и автоматические тесты и всё равно быть визуально неверным.

## 2. Canonical production flow

Для персонажей, врагов, боссов, окружения, UI и reusable visual families используется:

SOURCE/CANON AUDIT -> VISUAL FAMILY -> ONE HERO MASTER FRAME -> CANDIDATE ID + PROVENANCE -> USER ART-DIRECTION REVIEW -> EDITABLE MASTER -> DERIVED DIRECTIONS/VARIANTS -> RUNTIME EXPORT -> TECHNICAL CHECKS -> TRUE GAMEPLAY-SCALE/MAP-CONTEXT PREVIEW -> CANDIDATE CAPTURE -> USER FINAL VISUAL APPROVAL -> APPROVED GOLDEN BASELINE -> RUNTIME MANIFEST -> PRODUCTION PROMOTION

Нельзя перескакивать от генерации сразу к массовому набору направлений или анимаций, если identity и silhouette не прошли master-gate.

## 3. Hero-master-first gate

До массового производства создаётся один representative hero master в целевом tactical camera angle.

Он должен доказать:

- identity и принадлежность к нужной визуальной family;
- body proportions, mass и silhouette;
- head, hair и ключевую анатомию;
- outfit/armor/material language;
- main equipment и визуальную роль;
- palette и value separation;
- ground contact;
- соответствие target gameplay scale;
- читаемость на representative arena/map или UI-context.

Creative Director отдельно утверждает identity hero master до расширения в directions, equipment family, locomotion, combat animation или batch variants.

Старый технически корректный spritesheet не обходит этот gate.

## 4. Cell size следует за качеством

Размер ячейки — технический параметр, а не священное ограничение.

Сначала доказывается читаемость утверждённого визуала в игре, затем фиксируется shared pixel-density и template cell size. Если 64x64 делает тело, оружие или силуэт нечитаемыми, рассматриваются 80x80, 96x96 или другой обоснованный размер для всей family.

Нельзя независимо раздувать или уменьшать отдельные assets только ради одного screenshot.

## 5. Derived-family rule

После утверждения master все directions и variants выводятся как одна family.

Они сохраняют:

- body proportions и apparent height;
- hair volume и identity traits;
- outfit/equipment design;
- palette/material language;
- ground-contact convention;
- pivot и semantic anchors;
- world-facing direction semantics;
- единый pixel-density и scale law.

Слепое зеркалирование запрещено там, где оно ломает асимметрию, руку, оружие или читаемую ориентацию. Если variant требует изменения identity-bearing traits, проблема решается на уровне master/template.

## 6. Editable source

Для reusable production family сохраняется editable source, если инструмент его поддерживает.

Pixelorama 1.2 может использоваться как bounded TRIAL для editable pixel-art source/export. Это authoring слой, не Godot runtime dependency. Результат trial должен доказать сохранение проекта, воспроизводимый pixel-safe export, стабильные frame/layer semantics и отсутствие uncontrolled filename/manifest drift.

## 7. Provenance contract

Каждый model-assisted или generated candidate, насколько возможно, хранит:

- immutable candidate ID;
- semantic asset ID и family ID;
- source/reference input IDs или hashes;
- prompt или authored request revision;
- generator/tool;
- model/checkpoint и его version;
- workflow artifact/JSON, если поддерживается;
- seed, если поддерживается;
- custom-node/plugin versions;
- editable source path и hash;
- post-processing steps/version;
- runtime export path и hash;
- producing repository commit;
- parent approved master candidate ID для variant.

Фиксированный seed сам по себе не доказывает воспроизводимость после смены модели, nodes, инструмента, hardware или провайдера.

## 8. Три независимых слоя

### Identity layer

Что это за персонаж, объект, enemy, UI family или environment family: identity, silhouette, proportions, face/hair, outfit, palette, equipment и другие признаки.

### Reproducibility layer

Как exact candidate был создан: candidate ID, tool/model/version, workflow, seed, inputs, source, post-processing и hashes.

### Production-QA layer

Работает ли именно этот identity в игре: dimensions, pivot, anchors, export semantics, true 1x gameplay preview, representative map/context, capture, manifest и promotion state.

Passing one layer never implies passing another.

## 9. Review presentation

Каждый world/battle candidate для Creative Director review получает:

1. enlarged inspection view;
2. true 1x gameplay-scale view;
3. representative scene/map context;
4. scale comparison, если она помогает оценке;
5. candidate ID и точный repository commit;
6. отсутствие broken external/relative dependencies;
7. краткую отметку технического статуса и открытых художественных вопросов.

UI candidate дополнительно показывает реальный viewport, safe area, touch target и состояние normal/pressed/disabled/locked, если они входят в задачу.

Review artifact, который не показывает exact candidate в целевом контексте, недействителен как approval evidence.

## 10. Candidate capture и golden baseline

Автоматический capture в игре, браузере или Godot preview — наблюдатель repository-owned presentation.

До approval он называется candidate capture и используется для сравнения/regression diagnostics. Он не является authoritative golden.

Только после явного Creative Director APPROVE exact output/capture/hash может быть promoted в approved golden baseline. Детерминированные условия capture должны фиксировать viewport, DPR/scale, state/fixture, animation frame, fonts и asset versions, когда это возможно.

## 11. Promotion law

MODEL/ARTIST MAY PROPOSE -> LAB CONSTRAINS -> PIPELINE VALIDATES -> USER REVIEWS -> USER APPROVES -> GOLDEN/MANIFEST PROMOTE -> REPOSITORY PRODUCTION

Ни модель, ни агент, ни export tool, ни автоматический тест, ни Visual Lab preflight не может выдать финальное художественное approval.

Rejected candidates сохраняются как immutable non-promotable evidence. Они могут использоваться для диагностики, но не могут молча воскресать в production.

## 12. Tool status

- Pixelorama 1.2: TRIAL как editable source/export layer.
- Tiled: WATCH для будущего authoring layout/scene; не обязательный runtime format.
- ComfyUI execution: HOLD до появления подходящего approved compute; provenance principle принят уже сейчас.
- Versioned workflow provenance: ADOPT.
- Playwright или эквивалентный in-game visual QA: ADOPT как observer, с approved-golden rule.

## 13. Текущее применение к Moonveil

Существующие assets этапов 1, 2 и 3 в docs/mockups являются рабочими visual evidence со статусами их stage-документов. Перенос Visual Lab не объявляет их approved автоматически.

Для следующего нового или перерабатываемого visual family порядок обязателен:

1. canon/source audit по README.md, GAME_MANIFEST.md, AGENT_CONTEXT.md и соответствующему stage;
2. один hero master;
3. candidate ID, provenance и review pack;
4. user identity/art-direction approval;
5. derived family, runtime export и техническая проверка;
6. true gameplay-scale preview;
7. final user approval;
8. manifest и production promotion.

Existing menu, arena, Lin Yue и Seoyeon Han visuals нельзя использовать как бесконтрольный template для всех будущих assets, если это не закреплено в отдельном approved family document.

## 14. Relationship to project law

Этот документ работает вместе с:

- README.md;
- GAME_MANIFEST.md;
- AGENT_CONTEXT.md;
- ROADMAP.md;
- docs/MOCKUP_INDEX.md;
- соответствующими stage README, layer maps, contracts и manifests.

Если старый локальный workflow разрешает массовую генерацию до hero-master review, эта Visual Lab law имеет приоритет для новых и перерабатываемых visual families.

## 15. Short form

ONE GREAT MASTER FIRST -> APPROVE IDENTITY -> RETAIN EDITABLE SOURCE + PROVENANCE -> DERIVE FAMILY -> TEST AT REAL SCALE -> USER APPROVE -> GOLDEN -> MANIFEST -> PRODUCTION.
