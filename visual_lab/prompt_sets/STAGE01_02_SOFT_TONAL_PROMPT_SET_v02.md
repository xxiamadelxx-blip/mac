# Moonveil — Soft Tonal Visual Prompt Set v02

Статус: USER REVIEW  
Маршрут: MOCKUP с secondary UI_ART и ART  
Дата: 2026-09-09

## Цель

Перевести меню и арену в одну визуальную семью на основе двух пользовательских референсов Линь Юэ и Соён Хан. Референсы задают мягкую, спокойную, премиальную тональность. Поздняя стадия забега может усиливать давление количеством врагов, следом боя и тенями, но не должна переходить в неон, кислотные цвета или токсичный horror-grade.

## Общий prompt law

- Премиальная 2D mobile fantasy с мягкой painterly anime-подачей, ink-wash и gouache-текстурами.
- Одна материальная система: matte deep blue-gray panels, smoky teal environment, warm ivory typography, thin muted-brass borders.
- Основной цвет роли Линь Юэ — mist jade; цвет роли Соён — restrained desaturated garnet.
- Jade и garnet являются акцентами, а не источниками неонового свечения.
- Мягкий diffused moonlight, controlled contrast, low bloom, читаемые тени.
- Никакого hard HDR, chromatic aberration, cyberpunk-оранжевого, hot magenta, fluorescent cyan или pure saturated red.
- Русский UI; категорийное слово — ПЕРСОНАЖИ, не ГЕРОИНИ.
- Generated composite — candidate/reference; настоящий интерактивный UI должен оставаться отдельным Godot-слоем.

## Palette

| Роль | Направление |
| --- | --- |
| Deep blue-gray | основа воды, ночи и панелей |
| Smoky desaturated teal | среда и вторичные тени |
| Mist jade | мягкий highlight, Линь Юэ, XP и спокойные VFX |
| Warm ivory | луна, текст и светлые ткани |
| Muted brass | рамки, разделители и selected-state |
| Restrained desaturated garnet | лента Соён, редкий combat accent |

## Menu delta

Вертикальный viewport 390×844. Спокойный затопленный сад Лунного лотоса, большие читаемые панели, safe area минимум 16 px по бокам и 24 px сверху/снизу, визуально крупные touch targets минимум 48×48 dp. Детализированные персонажи допустимы в меню, но сохраняют ту же воду, луну, дымчатый teal и matte-панели.

Обязательные строки:

- ПЕРСОНАЖИ
- ВЫБРАТЬ ПЕРСОНАЖА
- НАЧАТЬ ЗАБЕГ
- ОРУЖИЕ
- СПОСОБНОСТЬ
- АРТЕФАКТЫ
- ЗАГРУЗКА
- ПОБЕДА
- ПОРАЖЕНИЕ

## Arena delta

Вертикальный gameplay frame 390×844 — окно камеры большого мира, не вся карта. Арена должна выглядеть как playable top-down 2D field:

- компактный боевой спрайт героя около 40–55 px apparent height в целевом frame;
- обычные враги около 18–30 px;
- 65–75% свободного движения в обычных кадрах;
- 20:00 усиливает давление количеством и следом боя, но сохраняет читаемый центральный маршрут;
- декор и лотосы остаются по краям;
- XP — отдельные мягкие pale-jade точки;
- HUD — минимальный и отдельный от фона;
- никакой full-body splash-иллюстрации на арене и никаких wall-to-wall enemies.

## State deltas

| State | Изменение относительно master |
| --- | --- |
| 0:00 | чистое поле, несколько ориентиров и спокойная рябь |
| 5:00 | небольшие группы у внешнего кольца, редкий XP |
| 10:00 | умеренная волна по краям и боковым lanes, центр открыт |
| 15:00 | высокая плотность по периферии, несколько элитных силуэтов, центр остаётся маршрутом |
| 20:00 | максимальная плотность и накопленный след боя; один крупный силуэт допустим только у дальней границы |

## Tool and post-processing

Инструмент: built-in image_gen. Версия модели, seed и workflow: UNVERIFIED — встроенный инструмент их не предоставил.  
Post-processing: ImageMagick resize to exact 390×844, strip metadata, sRGB output.  
Technical status: размеры и цветовой режим проверены; Godot import, runtime capture и Android performance остаются PENDING.
