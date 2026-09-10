# REF-VISUAL-CONTRACT-01 — аудит визуального контракта

TASK-ID: REF-VISUAL-CONTRACT-01
Репозиторий: xxiamadelxx-blip/mac
Родительский HEAD перед записью: 59d2c3054991696eb9ddd842eb85ff71321e982e
Граница работы: только визуальные документы и каталоги контрактов; исходный код клонов не изучался и не переносился.

## Итог

Статус: PARTIAL / BLOCKED_FOR_RUNTIME.

В репозитории есть реальные PNG/SVG для арены, референсные листы двух героинь и частичные корневые кадры двух врагов. Ни один из этих наборов не подтверждён как APPROVED GOLDEN или PRODUCTION. Для большинства требуемых визуальных областей файлов нет. Ни одна ссылка runtime не может считаться разрешённой до появления runtime manifest с точным экспортным путём, хэшем, производящим коммитом, provenance и подтверждённым статусом.

Линь Юэ и Соён Хан не изменялись и не перегенерировались.

## 1. Канонические соглашения путей

| Область | Действующее соглашение | Фактическое состояние |
|---|---|---|
| Арена v03 | docs/mockups/02-arena/assets/*.svg; ссылки через STAGE02_ARENA_ASSET_MANIFEST_v03.json | 10 из 10 файлов манифеста существуют; статус USER REVIEW; runtime_manifest отсутствует; consumer не подключён |
| Арена v02/слои | docs/mockups/02-arena/layers/* | Это fallback и review evidence, а не автоматически разрешённый runtime |
| Героини | docs/mockups/03-heroes/{hero_id}/{direction}/{state}.png | 8 направлений × 12 состояний; 96 слотов на героиню; фактических PNG в этих папках нет |
| Враги | docs/mockups/04-enemies/{enemy_id}/{direction}/{state}.png | Шаблон явно закреплён для ink_beetle; фактические кадры лежат в корне папок и не образуют directional pack |
| Новые этапы 05–10 | Точный production path ещё не закреплён отдельными манифестами | Нельзя придумывать имена и пути по одному текстовому брифу |

Общее правило production law: runtime должен получать путь из утверждённого манифеста. Само наличие PNG, SVG, README, review-pack или статического composite не является разрешением на подключение.

## 2. Какие asset slots существуют сейчас

### Арена

В STAGE02_ARENA_ASSET_MANIFEST_v03.json описаны и реально существуют:

- arena.base.moon_lotus.v03 → assets/STAGE02_ARENA_BASE_MOON_LOTUS_v03.svg;
- arena.prop.lotus_pond_edge.v03 → assets/STAGE02_ARENA_PROP_LOTUS_POND_EDGE_MASTER_v03.svg;
- arena.prop.broken_bridge_segment.v03 → assets/STAGE02_ARENA_PROP_BROKEN_BRIDGE_SEGMENT_v03.svg;
- arena.prop.stone_cluster.v03 → assets/STAGE02_ARENA_PROP_STONE_CLUSTER_v03.svg;
- arena.prop.reed_patch.v03 → assets/STAGE02_ARENA_PROP_REED_PATCH_v03.svg;
- arena.prop.root_bank.v03 → assets/STAGE02_ARENA_PROP_ROOT_BANK_v03.svg;
- arena.prop.jade_lantern.v03 → assets/STAGE02_ARENA_PROP_JADE_LANTERN_v03.svg;
- arena.prop.lotus_cluster.v03 → assets/STAGE02_ARENA_PROP_LOTUS_CLUSTER_v03.svg;
- arena.prop.fallen_moon_shrine.v03 → assets/STAGE02_ARENA_PROP_FALLEN_MOON_SHRINE_v03.svg;
- arena.prop.fallen_moss_log.v03 → assets/STAGE02_ARENA_PROP_FALLEN_MOSS_LOG_v03.svg;
- arena.vfx.water_ripple_patch.v03 → assets/STAGE02_ARENA_VFX_WATER_RIPPLE_PATCH_v03.svg.

Три preview-ссылки v03 — STAGE02_ARENA_TOPDOWN_COMPOSITE_v03.svg, STAGE02_ARENA_TOPDOWN_INSPECTION_v03.svg и STAGE02_ARENA_ASSET_BOARD_v03.svg — также существуют. Они являются review material, а не runtime asset.

### Героини

Существуют 10 референсных PNG в layers/: общий экран выбора, пять листов Линь Юэ и четыре листа Соён Хан. Это не 192 runtime-слота.

Контракт требует:

- lin_yue: 8 направлений × 12 состояний = 96 PNG;
- soyeon_han: 8 направлений × 12 состояний = 96 PNG;
- canvas 1024×1024, RGBA, прозрачный фон, pivot bottom_center.

Обе папки содержат hero_manifest.json, но не содержат ни одного файла по шаблону direction/state.png.

### Враги

В наличии 20 корневых PNG:

- ink_beetle: idle.png, move_01.png, move_02.png, move_03.png, attack_01.png, attack_02.png, hit.png, death_01.png, death_02.png, shadow.png;
- lantern_moth: тот же набор из 10 корневых PNG.

Эти файлы являются частичными candidate/reference frames. В ink_beetle/enemy_manifest.json заявлен шаблон 8 направлений × 12 состояний, но directional папок нет. В legacy aliases самого ink_beetle дополнительно не хватает attack_03.png, hit_01.png и hit_02.png. Для lantern_moth манифест прямо называет набор reference frames, а не финальным runtime atlas.

Реестр Stage 04 содержит 10 visual families: ink_beetle, lantern_moth, bone_carp, paper_ghost, jade_toad, mirror_fox, bell_crab, thread_doll, stone_oni и eclipse_serpent. У восьми последних нет ни одного PNG или SVG.

## 3. Какие PNG/SVG отсутствуют

| Область | Подтверждённое отсутствие | Что нельзя заявлять |
|---|---|---|
| Героини | 96 PNG Линь Юэ + 96 PNG Соён Хан по runtime-шаблону | Нельзя считать 10 PNG из layers боевым паком; статус остаётся BINARY_INTAKE_PENDING |
| Враги | Нет directional/state pack; отсутствуют папки для восьми visual families; у ink_beetle отсутствуют attack_03.png, hit_01.png, hit_02.png | Нельзя считать 20 корневых кадров полным набором 8×12 и нельзя объявлять roster production |
| Боссы | В docs/mockups/05-bosses/ нет PNG, SVG и отдельного manifest | Текстовый бриф о встречах не является визуальным ресурсом |
| Оружие | В docs/mockups/06-weapons/ нет PNG, SVG и manifest; описаны 10 content IDs | Имена оружия и синергий не являются asset paths |
| Пассивки | В docs/mockups/07-passives/ нет PNG, SVG и manifest; описаны 10 run-passive IDs | Текстовое описание не является иконкой или runtime visual |
| Артефакты | В docs/mockups/08-artifacts/ и docs/mockups/17-artifact-ui/ нет PNG, SVG и manifest; описаны 10 artifact IDs | Карточки, иконки и feedback VFX отсутствуют |
| Опыт | В docs/mockups/09-xp/ нет PNG, SVG и manifest; заявлены 6 градаций XP | Цветовые или кодовые кружки не заменяют реальные pickup assets |
| HUD | В docs/mockups/10-hud/ нет PNG, SVG, layout manifest или review mockup | Semantic blocks README не являются HUD-визуалом |
| Смерть врагов/боссов | В docs/mockups/14-enemy-death/ и 15-boss-death/ нет PNG/SVG | Останки, фрагменты, следы и наградные эффекты отсутствуют |
| Окна улучшений и синергий | В docs/mockups/16-upgrade-offers/ и 19-synergy-info/ нет PNG/SVG | Текстовые состояния LOCKED/OFFERED/CLAIMED не являются готовыми карточками |

## 4. Runtime links, которые допустимы

1. Арена: потребитель должен брать только записи из будущего runtime manifest, связанного с STAGE02_ARENA_ASSET_MANIFEST_v03.json. Сейчас promotion.runtime_manifest = null, поэтому разрешённой runtime-ссылки нет. Исходные ссылки assets/*.svg можно использовать как канонические исходники кандидата, но не как доказанную production-интеграцию.
2. Героини: допустимая форма ссылки задаётся строго как docs/mockups/03-heroes/{hero_id}/{direction}/{state}.png. Сейчас ни один такой файл не существует. Ссылки на layers/STAGE03_HERO_*.png являются только reference paths.
3. Враги: допустимая форма ссылки для стандартизированного набора задаётся как docs/mockups/04-enemies/{enemy_id}/{direction}/{state}.png. Корневые idle.png, move_*.png и прочие legacy frames нельзя подставлять вместо отсутствующих directional paths без отдельного принятого манифеста.
4. Боссы, оружие, пассивки, артефакты, XP и HUD: production runtime link отсутствует. Код не должен придумывать путь, брать README как ресурс или рисовать замену кодом. Сначала нужен реальный candidate, затем manifest и отдельные технический и художественный gates.

Недопустимые значения, которые выглядят как ссылки, но ссылками на ассеты не являются: runtime/procedural, stage-03-and-stage-04, stage-09 и stage-10. Особенно runtime/procedural нельзя принимать как видимый фон, terrain или foreground: это не PNG/SVG и не разрешение рисовать арену кодом. Data-driven collision может оставаться данными, но видимая арена должна состоять из реальных asset files.

## 5. Файлы, которые нельзя принимать как финальный визуал

- любые *_REVIEW_*.png, *_REVIEW_*.svg, REVIEW_GRID, REVIEW_STRIP, MACRO_LAYOUT, TOPDOWN_COMPOSITE и TOPDOWN_INSPECTION — review evidence;
- любые *_COMPOSITE_*.png — составные контрольные изображения, не набор runtime-слоёв;
- docs/mockups/02-arena/layers/STAGE02_ARENA_OPEN_FIELD_ART_v02.png, AMBIENT_VFX_v01.*, REMAINS_20M_v01.* и v02 composites — fallback/reference material, не автоматическая promotion v03;
- docs/mockups/03-heroes/layers/STAGE03_HEROES_SELECTION_v02.png и все STAGE03_HERO_*.png — референсные листы, не runtime pack;
- docs/mockups/04-enemies/STAGE04_ENEMY_INK_BEETLE_MASTER_v01.svg, STAGE04_ENEMY_INK_BEETLE_GAMEPLAY_REVIEW_v01.svg и STAGE04_ENEMY_ROSTER_SILHOUETTES_v01.svg — master/review evidence;
- корневые PNG ink_beetle и lantern_moth — candidate/reference frames; они имеют NOT_PROMOTED или REFERENCE_PASS_PENDING_RUNTIME;
- любой README, текстовый content brief, provenance JSON, manifest без фактического файла и любой static preview — не финальный визуал;
- старый manifest с более ранним статусом DONE не отменяет более новый runtime manifest со статусом BINARY_INTAKE_PENDING;
- любой визуал без explicit Creative Director approval, exact candidate/hash и runtime manifest — не APPROVED GOLDEN и не PRODUCTION.

## 6. Проверка запрета на рисование арены кодом

В STAGE02_ARENA_LAYER_MAP_v02.json присутствуют виртуальные значения runtime/procedural для gameplay_terrain и foreground. Они не являются asset paths и не могут закрывать визуальный контракт. В том же документе static composites помечены как review evidence only, а collision отделён от SVG и должен быть data-driven. Приёмка возможна только если видимые base, props, ambient VFX, remains и foreground представлены реальными файлами и подключены через утверждённые пути.

## 7. Границы изменений

В рамках этой задачи не изменялись:

- Линь Юэ;
- Соён Хан;
- PNG/SVG и существующие манифесты;
- runtime-код, сцены и код клонов;
- бинарные файлы, Base64 и ZIP.

Создан только этот текстовый отчёт в разрешённом каталоге Visual Lab/asset-contract.

## Handoff

Parent HEAD: 59d2c3054991696eb9ddd842eb85ff71321e982e
Changed path: visual_lab/asset-contract/REF-VISUAL-CONTRACT-01.md
Status: PARTIAL
Evidence: STAGE02_ARENA_ASSET_MANIFEST_v03.json — 13/13 ссылок существуют; Stage 03 — 0/192 runtime PNG; Stage 04 — 20 корневых PNG, 8 visual families без файлов; Stage 05–10 и связанные UI/death stages — 0 PNG/SVG.
Open blockers: отсутствие production runtime manifests и PNG/SVG для большинства visual slots; arena v03 остаётся USER REVIEW; героини остаются BINARY_INTAKE_PENDING; враги остаются CANDIDATE/NOT_PROMOTED.
Next action: выполнить intake реальных PNG/SVG по отсутствующим слотам и после этого повторить этот аудит перед любым runtime-подключением.