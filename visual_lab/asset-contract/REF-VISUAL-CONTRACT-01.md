# REF-VISUAL-CONTRACT-01 — аудит визуального контракта

TASK-ID: REF-VISUAL-CONTRACT-01
Репозиторий: xxiamadelxx-blip/mac
Родительский HEAD перед исправлением: 44ab69b70135b4bd2a1f2e98512c52c17ca08a6b
Граница работы: только визуальный контракт, манифесты и проверка бинарного хранилища. Исходный код клонов не изучался и не переносился.

## Исправление предыдущей версии

Предыдущая версия отчёта ошибочно трактовала отсутствие PNG/SVG в дереве GitHub как отсутствие самих бинарных ассетов. Это неверно после перехода на Supabase.

Теперь разделяются три независимых факта:

1. объект существует в Supabase;
2. объект связан с семантическим asset ID и манифестом;
3. объект импортирован в Godot/runtime, технически проверен и художественно утверждён.

## Итог

Статус: PARTIAL / STORAGE_VERIFIED / NOT_RUNTIME_PROMOTED.

Фактическое бинарное хранилище проверено в Supabase project ylhbihgrchtqzaphuxvy, bucket visual-assets.

Под каноническим префиксом moonevil-eclipse/docs/mockups/ найдено:

| Область | Всего объектов | PNG | SVG | Толкование |
|---|---:|---:|---:|---|
| Именованный пакет Moonveil | 114 | 88 | 26 | Фактически перенесённые объекты |
| Активные каталоги, без _archive | 76 | 56 | 20 | Доступные текущие визуальные объекты |
| _archive | 38 | 32 | 6 | Исторические объекты, не production |
| 02-arena/generated-v01 | 7 | 7 | 0 | Новая арена и отдельные PNG, ещё не привязанные к манифесту |

Дополнительно в bucket есть 26 PNG под безымянным UUID-префиксом. Они не включены в канонический инвентарь: у них нет семантического пути, asset ID или связи с манифестом.

Линь Юэ и Соён Хан не изменялись и не перегенерировались.

## 1. Каноническая модель хранения

| Слой | Где находится | Что считается доказательством |
|---|---|---|
| Документация и манифесты | GitHub | Соглашения путей, asset ID, статусы, потребители и правила |
| Исходные визуальные PNG/SVG | Supabase Storage, bucket visual-assets | Реальный объект с именованным путём, размером и MIME-типом |
| Сборочный бинарный intake | Supabase Storage → CI → импорт в репозиторий | Проверенный размер, SHA-256, импортёр и evidence |
| Godot runtime | Импортированные файлы из репозитория | Ссылка на runtime export path из утверждённого манифеста; сеть Supabase во время игры не нужна |

Наличие объекта в Supabase не означает APPROVED GOLDEN, PRODUCTION или готовность runtime.

## 2. Существующие слоты и фактическое состояние

### Арена

В Supabase существуют все 13 ссылок, перечисленные в STAGE02_ARENA_ASSET_MANIFEST_v03.json:

- 10 SVG в docs/mockups/02-arena/assets/;
- STAGE02_ARENA_TOPDOWN_COMPOSITE_v03.svg;
- STAGE02_ARENA_TOPDOWN_INSPECTION_v03.svg;
- STAGE02_ARENA_ASSET_BOARD_v03.svg.

Манифест остаётся USER REVIEW: runtime_manifest = null, consumer не подключён.

Отдельно перенесён новый пакет арены:

- moonevil-eclipse/docs/mockups/02-arena/generated-v01/arena-mockup-v01.png;
- generated-v01/assets/interior/fallen-moon-shrine.png;
- generated-v01/assets/interior/jade-lantern.png;
- generated-v01/assets/interior/moon-guardian-statue.png;
- generated-v01/assets/landscape/broken-bridge-segment.png;
- generated-v01/assets/landscape/lotus-pond-edge.png;
- generated-v01/assets/landscape/reed-root-bank.png.

Эти 7 PNG существуют в Supabase, но пока не имеют записи в действующем runtime manifest и не должны подключаться кодом как финальный runtime-визуал.

### Героини

В Supabase существуют 10 референсных PNG из layers/: экран выбора, листы Линь Юэ и Соён Хан.

Runtime-контракт по-прежнему требует:

- lin_yue: 8 направлений × 12 состояний = 96 PNG;
- soyeon_han: 8 направлений × 12 состояний = 96 PNG;
- canvas 1024×1024, RGBA, прозрачный фон, pivot bottom_center.

В каноническом префиксе Supabase нет 192 объектов по шаблону docs/mockups/03-heroes/{hero_id}/{direction}/{state}.png. Поэтому корректная формулировка: референсные PNG перенесены, runtime-пакет не подтверждён и остаётся BINARY_INTAKE_PENDING.

### Враги

В Supabase существуют:

- 20 корневых PNG: по 10 для ink_beetle и lantern_moth;
- 3 SVG: master, gameplay review и roster silhouettes Stage 04.

Полного directional/state pack 8×12 нет. Восемь остальных visual families Stage 04 не имеют объектов в каноническом Supabase-префиксе. У ink_beetle также отсутствуют заявленные legacy-файлы attack_03.png, hit_01.png и hit_02.png.

Корректный статус: PARTIAL / NOT_PROMOTED, а не «бинарные файлы отсутствуют».

### Боссы, оружие, пассивки, артефакты, XP, HUD и UI

В каноническом префиксе Supabase пока нет объектов для Stage 05–10, 14–19. Это означает, что соответствующие визуальные пакеты ещё не перенесены или ещё не созданы. Текстовые README и контентные записи не считаются PNG/SVG.

## 3. Допустимые runtime links

1. Арена v03: runtime должен ссылаться на записи утверждённого манифеста, а не напрямую на URL Supabase. Текущий манифест не содержит runtime_manifest.
2. Новая арена v01: текущие пути generated-v01 — это пути исходных кандидатов в Supabase. До решения Creative Director и записи semantic asset IDs они не являются runtime links.
3. Героини: ожидаемая форма — docs/mockups/03-heroes/{hero_id}/{direction}/{state}.png после реального intake и импорта. Существующие layers/*.png — reference paths.
4. Враги: ожидаемая форма — docs/mockups/04-enemies/{enemy_id}/{direction}/{state}.png после полного directional/state intake. Корневые PNG нельзя молча объявлять этим набором.
5. Боссы, оружие, пассивки, артефакты, XP и HUD: runtime links ещё не существуют; нельзя придумывать их по названиям контента.

Godot не должен загружать Supabase во время игры. Схема: Supabase → проверка CI → импортированный файл → runtime manifest → Godot.

## 4. Что нельзя принимать как финальный визуал

- PNG/SVG из Supabase без semantic asset ID, provenance, технической проверки и художественного approval;
- все 7 объектов 02-arena/generated-v01 до отдельного review и привязки к манифесту;
- review, composite, inspection, board, macro-layout и silhouette-файлы;
- объекты из _archive;
- 26 UUID-объектов без семантического пути и манифестной связи;
- reference-листы героинь вместо runtime-паков;
- 20 корневых кадров врагов вместо полного directional/state pack;
- README, content brief, provenance JSON и manifest без связанного бинарного объекта;
- любой ассет без explicit Creative Director approval как APPROVED GOLDEN;
- любой визуал, который заменяется draw_* или runtime/procedural вместо реального файла.

## 5. Запрет визуала арены через код

В STAGE02_ARENA_LAYER_MAP_v02.json значения runtime/procedural для gameplay_terrain и foreground остаются недопустимыми как видимый визуал. Теперь для арены уже есть реальные PNG/SVG в Supabase, включая отдельные PNG интерьера и ландшафта. Следующий корректный шаг — связать выбранные файлы с манифестом и импортировать их в runtime. Рисование арены кодом не допускается.

Data-driven collision может оставаться данными; видимые base, props, landscape, interior, ambient VFX, remains и foreground должны быть реальными ассетами.

## 6. Границы изменений

В рамках этой задачи не изменялись:

- Линь Юэ и Соён Хан;
- PNG/SVG и объекты Supabase;
- существующие stage-манифесты;
- runtime-код и сцены;
- бинарные данные, Base64 и ZIP.

Изменён только этот текстовый отчёт в visual_lab/asset-contract/.

## Handoff

Parent HEAD: 44ab69b70135b4bd2a1f2e98512c52c17ca08a6b
Changed path: visual_lab/asset-contract/REF-VISUAL-CONTRACT-01.md
Status: PARTIAL / STORAGE_VERIFIED / NOT_RUNTIME_PROMOTED
Evidence: Supabase project ylhbihgrchtqzaphuxvy, bucket visual-assets, SQL inventory storage.objects: 114 именованных объектов под moonevil-eclipse/docs/mockups/; 88 PNG, 26 SVG; 7 новых PNG в 02-arena/generated-v01; 26 UUID-объектов исключены из канонического инвентаря.
Open blockers: новые PNG арены не связаны с manifest; runtime import и checksum evidence не подтверждены; героини не имеют подтверждённого 192-файлового runtime-пака; Stage 04 остаётся частичным; Stage 05–10 и UI/death-пакеты не представлены в canonical Supabase path.
Next action: провести отдельный Visual Lab review 02-arena/generated-v01 и после одобрения привязать выбранные PNG к asset IDs и манифесту.