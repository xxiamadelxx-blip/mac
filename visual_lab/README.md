# Visual Lab — Moonveil: Eclipse

Статус: ADOPTED. Обязательный production-gate для visual, design, art, asset, UI-visual, animation и VFX работы.

Visual Lab — это отдельный процессный пакет репозитория. Он не является генератором изображений и не является runtime-зависимостью Godot. Его задача — не дать кандидату, техническому экспорту или случайному PNG незаметно стать производственным визуалом.

## Точка входа

Любой visual/design/art агент сначала читает:

1. корневой AGENTS.md;
2. этот README;
3. VISUAL_POLICY_RULE.md;
4. VISUAL_LAB_PRODUCTION_LAW.md;
5. ASSET_PIPELINE_CODE.md;
6. REVIEW_CHECKLIST.md;
7. для задач UI, UI-art, art, sprite и mockup — `UI_ART_SPRITE_MOCKUP_WORKFLOW.md`;
8. канонические документы Moonveil и локальную stage-папку.

Если задача создаёт новую существенную пользовательскую визуальную единицу, агент сначала выявляет открытые решения и получает выбор Creative Director. Уже утверждённые решения не переоткрываются без реального конфликта.

## Что входит в пакет

| Файл | Назначение |
| --- | --- |
| VISUAL_POLICY_RULE.md | Короткий обязательный входной gate |
| VISUAL_LAB_PRODUCTION_LAW.md | Канонический порядок master, provenance, QA, review и promotion |
| ASSET_PIPELINE_CODE.md | Производство от full-game census до runtime manifest |
| REVIEW_CHECKLIST.md | Практический пакет проверки кандидата и условия promotion |
| UI_ART_SPRITE_MOCKUP_WORKFLOW.md | Обязательная маршрутизация агента для UI, art, sprite и mockup задач |
| CANDIDATE_PROVENANCE_TEMPLATE.json | Машиночитаемый шаблон provenance |
| SOURCE_TRANSFER.md | Происхождение и адаптация перенесённого пакета |

## Обязательный production flow

SOURCE/CANON AUDIT
-> VISUAL FAMILY
-> ONE HERO MASTER
-> CANDIDATE ID + PROVENANCE
-> USER ART-DIRECTION REVIEW
-> EDITABLE MASTER
-> DERIVED VARIANTS
-> RUNTIME EXPORT
-> TECHNICAL CHECKS
-> TRUE 1X GAMEPLAY-SCALE / MAP-CONTEXT PREVIEW
-> USER FINAL VISUAL APPROVAL
-> APPROVED GOLDEN BASELINE
-> RUNTIME MANIFEST
-> PRODUCTION PROMOTION

Technical PASS никогда не равен artistic PASS.

## Область применения

Пакет применяется к:

- меню, экрану выбора героини, результатам и другим UI-визуалам;
- арене, воде, растениям, свету, частицам и следам боя;
- Линь Юэ, Соён Хан, обычным врагам, элитам и боссам;
- оружию, пассивкам, артефактам, XP и иконкам;
- animation/VFX состояниям и телеграфам;
- любым новым картам, персонажам, визуальным семействам и runtime asset manifests.

## Правила хранения

- visual_lab/ хранит закон, шаблоны и ворота процесса, а не случайную коллекцию production PNG.
- Фактические candidates и approved assets лежат в соответствующей docs/mockups, docs/manifests или runtime-папке и имеют стабильные IDs.
- Отклонённые candidates не удаляются молча и не могут автоматически вернуться в production.
- Existing stage assets не получают approval только потому, что в репозитории появился Visual Lab.
- Инструменты авторинга и QA могут быть заменены; provenance и разделение технического pass/художественного approval сохраняются.

## Главное правило

ONE GREAT MASTER FIRST -> APPROVE IDENTITY -> RETAIN EDITABLE SOURCE + PROVENANCE -> DERIVE FAMILY -> TEST AT REAL SCALE -> USER APPROVE -> GOLDEN -> MANIFEST -> PRODUCTION.
