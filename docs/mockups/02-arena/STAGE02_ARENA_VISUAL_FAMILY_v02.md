# Stage 02 — Soft Tonal Arena Family v02

Статус: USER REVIEW  
Primary route: ART  
Secondary route: MOCKUP  
Family ID: moonveil-arena-soft-tonal-v02

## Главный исправленный принцип

Арена больше не подаётся как вертикальный character poster. Это широкое окно камеры большого связанного мира Moon Lotus Garden. Главный игровой якорь — маленький читаемый боевой спрайт; не фон, не гигантская атака и не декоративная толпа.

## Scale law

- Target frame: 390×844 portrait.
- Hero apparent height: примерно 40–55 px в target frame.
- Normal enemy apparent height: примерно 18–30 px.
- 0:00–10:00: ориентир 65–75% свободного проходимого поля.
- 15:00: центральный маршрут остаётся читаемым, ориентир 55–65% свободного пространства.
- 20:00: давление растёт по количеству и следу боя; центральная зона вокруг героя сохраняет движение, ориентир 50–60%.
- Декор, мост, камыш, фонари и лотосы — краевые ориентиры, не ковёр и не лабиринт.
- XP не смешивается с останками.
- HUD остаётся компактным и не маскирует поле.

## Tonal law

Все пять состояний сохраняют один и тот же blue-gray/teal/ivory/mist-jade/garnet язык. Поздние кадры не получают отдельный красный или зелёный color grade. Тревога читается плотностью, направлением волны, телеграфом и накопленным материальным следом.

## Candidates

| State | Candidate ID | Файл |
| --- | --- | --- |
| 0:00 master | vl-20260909-arena-0m-v02 | STAGE02_ARENA_COMPOSITE_0M_v02.png |
| 5:00 | vl-20260909-arena-5m-v02 | STAGE02_ARENA_COMPOSITE_5M_v02.png |
| 10:00 | vl-20260909-arena-10m-v02 | STAGE02_ARENA_COMPOSITE_10M_v02.png |
| 15:00 | vl-20260909-arena-15m-v02 | STAGE02_ARENA_COMPOSITE_15M_v02.png |
| 20:00 | vl-20260909-arena-20m-v02 | STAGE02_ARENA_COMPOSITE_20M_v02.png |

Все preview имеют размер 390×844, sRGB. Arena strip показывает одну камеру и непрерывное увеличение давления; это не доказательство runtime, collision, spawn logic или Android FPS.

## Review result

Технически: TECHNICAL PASS для размера, sRGB, целевого масштаба и static map-context preview.  
Художественно: PENDING — нужен выбор Creative Director для exact candidate family.  
Godot/runtime: не изменялись; реальный gameplay-scale capture и Android performance остаются отдельным этапом.
