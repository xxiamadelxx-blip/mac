# Visual Lab — UI / Art / Sprite / Mockup Workflow

Статус: MANDATORY ROUTING для задач UI, UI-art, art, sprite и mockup.

Этот файл — операционный маршрут поверх Visual Lab production law. Он настраивает порядок работы агента и формат handoff; он не является генератором, авторинг-инструментом или runtime-зависимостью Godot.

## 1. Выбери основной маршрут

Перед началом зафиксируй один primary route. Дополнительный route допустим только как явно отмеченный secondary route.

| Route | Когда использовать | Канонический результат |
| --- | --- | --- |
| `UI_ART` | экран, панель, карточка, кнопка, иконка, портрет, UI-слой или UI state | `docs/mockups/<stage>/` + экранный contract/layers; runtime только через approved manifest |
| `SPRITE` | reusable hero/enemy/boss/weapon combat sprite, direction или animation state | stage `layers/` + stage manifest/contract + true 1x scene preview |
| `ART` | окружение, фон, VFX, telegraph, death effect или другая world/battle visual family | stage-папка + enlarged/1x + representative scene/map context |
| `MOCKUP` | идея, composition, direction, composite, screenshot или визуальный референс | `docs/mockups/<stage>/` как proposal/candidate/review evidence; не runtime по умолчанию |

Правило выбора: `UI_ART` имеет приоритет над общим `ART` для интерфейсной задачи; `SPRITE` — над `ART` для reusable боевого объекта; `MOCKUP` означает, что запрос остановлен на visual review, пока пользователь явно не запросит дальнейшую интеграцию.

## 2. Обязательный вход

1. Прочитай корневой `AGENTS.md`, весь пакет `visual_lab/` в установленном порядке и этот workflow.
2. Прочитай канонические документы Moonveil и README/contract/manifest целевой stage-папки.
3. Проверь текущий статус stage и конкретного asset/family. Папка, PNG или красивый preview не являются доказательством готовности.
4. Раздели зафиксированный канон, открытые creative decisions и технические ограничения.
5. Если stage или consumer не определён, остановись и запроси уточнение; не создавай новую папку или naming convention по догадке.

## 3. Маршрутизация по текущим stage-папкам

| Задача | Читать в первую очередь |
| --- | --- |
| Menu, Home, Heroes selection, Run Setup, Loading, Result | `docs/mockups/01-menu/` |
| Arena, world background, map-context art | `docs/mockups/02-arena/` |
| Hero portraits, full-body, combat sprites и состояния | `docs/mockups/03-heroes/` |
| Enemy, boss, weapon, passive, artifact, XP assets | `docs/mockups/04-enemies/`, `05-bosses/`, `06-weapons/`, `07-passives/`, `08-artifacts/`, `09-xp/` |
| Run HUD | `docs/mockups/10-hud/` |
| Enemy/boss death visuals | `docs/mockups/14-enemy-death/`, `15-boss-death/` |
| Upgrade offers, artifact UI, synergy information | `docs/mockups/16-upgrade-offers/`, `17-artifact-ui/`, `19-synergy-info/` |

Сначала прочитай локальный README и существующий contract/manifest. Если stage `PLANNED`, создай только явно запрошенный proposal/candidate package и не называй его production.

## 4. Исполнение Visual Lab

### 4.1 Source/canon audit и creative boundary

- Зафиксируй source refs, текущий status, consumer и незакрытые решения.
- При изменении лица, причёски, силуэта, пропорций, композиции, палитры, крупного UI-flow или identity family остановись и запроси выбор Creative Director.
- Уже принятое направление не переоткрывай без конкретного конфликта с каноном или проверяемого дефекта.

### 4.2 Family и один master

- Для новой reusable family сначала подготовь один representative hero master: один canonical screen/master для UI, один representative character/object для sprite, один representative environment/VFX sample для art.
- Сначала проверь identity, role, silhouette, readability, proportions, palette, pivot/anchors и target scale; batch вариантов, направлений и анимаций до этого не запускай.
- Повторяющийся дефект исправляй в family/template/pipeline, а не серией локальных patch-ей.

### 4.3 Candidate и provenance

- Для каждого конкретного результата создай immutable `candidate_id` по шаблону `vl-YYYYMMDD-family-asset-vNN` или существующему канону stage.
- Обязательно задай `asset_id`, `family_id` и `asset_kind`; заполни `visual_lab/CANDIDATE_PROVENANCE_TEMPLATE.json`.
- Укажи source/reference IDs или hashes, request/project revision, tool/model/version/workflow/seed если применимо, editable source и hash, post-processing, runtime export, dimensions/scale/pivot/anchors, gameplay preview и producing commit.
- Неизвестное значение помечай явно как `null`, `UNVERIFIED` или `PENDING`; не заполняй provenance выдуманными данными.

### 4.4 Review pack

Каждый review pack показывает exact candidate, `candidate_id`, producing commit и отдельные technical/artistic statuses.

Для `UI_ART` обязательно показать:

- реальный viewport `390x844`, safe area (минимум 16 dp по бокам и 24 dp сверху/снизу, если применимо);
- normal/pressed/disabled/locked/loading states, если они предусмотрены contract;
- русский текст из localization/contract, без доверия к тексту, запечённому в сгенерированное изображение;
- touch target не меньше `48x48 dp`, и отсутствие overlap, clipping, unsafe input interception и overflow.

Для `SPRITE` и `ART` обязательно показать:

- enlarged inspection и true `1x` gameplay-scale при камере `390x844`;
- representative arena/map/scene context;
- силуэт, голову/корпус, оружие, направление, effect/telegraph, pivot, anchors, footprint и прозрачность;
- соответствующие contract states и frame/direction semantics без индивидуального масштабирования, которое ломает family.

Для `MOCKUP` обязательно показать:

- source/canon relation, exact candidate и открытые вопросы;
- enlarged preview и target-size preview, если визуал предназначен для телефона;
- явную пометку `PROPOSAL`, `CANDIDATE` или `USER REVIEW`.

## 5. Approval и promotion

Technical PASS — только результат технических проверок. Он не равен artistic approval.

- `APPROVED GOLDEN` допустим только после явного решения Creative Director для exact candidate и сохранения output/hash/decision record.
- Только после этого создавай или обновляй runtime manifest, подключай consumer scene/UI и переводишь asset в `PRODUCTION`.
- Автоматический capture, Godot import, lint, тест, Playwright или мнение модели не могут создать artistic approval или golden baseline.
- `REJECTED` candidate сохраняй как non-promotable; не удаляй его молча и не возвращай автоматически в runtime.
- Если пользователь просит только UI/art/sprite/mockup, default handoff останавливается на `PROPOSAL`/`CANDIDATE`/`USER REVIEW`; runtime code/export не меняется без явного запроса и approval.

Допустимые итоговые statuses: `PROPOSAL`, `CANDIDATE`, `TECHNICAL PASS`, `USER REVIEW`, `APPROVED GOLDEN`, `PRODUCTION`, `REJECTED NON-PROMOTABLE`.

## 6. Обязательный handoff агента

В финале каждой такой задачи укажи:

| Поле | Что записать |
| --- | --- |
| `route` | `UI_ART`, `SPRITE`, `ART` или `MOCKUP` (+ secondary route при наличии) |
| `stage_path` | точная canonical stage-папка |
| `asset_kind` | screen/master/variant/state/sprite/VFX/mockup и т. п. |
| `asset_id` / `family_id` | стабильные semantic IDs |
| `candidate_id` | immutable ID или `null` для чистой идеи |
| `status` | одно значение из Visual Lab checklist |
| `technical_status` | evidence и результат технической проверки |
| `artistic_status` | `PENDING`, решение Creative Director или `REJECTED` |
| `manifest/consumer` | путь manifest и scene/UI consumer, либо `not promoted` |
| `open_decisions` | что требует выбора пользователя |
| `next_action` | один проверяемый следующий шаг |

Если поле отсутствует, handoff неполный и работа не может быть обозначена как `DONE`.

## 7. Стоп-условия

Остановись и задай вопрос пользователю/Creative Director, если:

- есть незакрытая creative decision или конфликт между stage contract и новым предложением;
- отсутствуют source refs, provenance, editable source или runtime hash, необходимые для заявленного статуса;
- пытаются запустить batch без утверждённого representative master;
- просят считать PNG/mockup/capture финальным артом только из-за технического прохода;
- runtime должен зависеть от `visual_lab/` или authoring/QA-инструмента;
- задача требует gameplay/data решения, которого нет в visual contract.

## 8. Definition of Done

Visual задача завершена только когда exact candidate, stage/family path, stable IDs, provenance, подходящие previews/checks, отдельные technical/artistic statuses и следующий handoff зафиксированы. `APPROVED GOLDEN` и `PRODUCTION` требуют explicit Creative Director approval и manifest linkage; отсутствие evidence означает, что работа остаётся незавершённой.