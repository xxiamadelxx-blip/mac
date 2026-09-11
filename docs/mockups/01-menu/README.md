# Stage 01 — Menu

Status: **IN PROGRESS / USER REVIEW**.

Активное визуальное семейство: `moonveil-menu-soft-tonal-v02`.

## Активный пакет v02

Пакет использует мягкую живописную anime-fantasy подачу: глубокий сине-серый фон, дымчатый teal, тёплый ivory, приглушённую brass-фурнитуру и мягкий jade как основной акцент. Категория персонажей в интерфейсе — **ПЕРСОНАЖИ**.

- [STAGE01_MENU_HOME_v02.png](./layers/STAGE01_MENU_HOME_v02.png)
- [STAGE01_MENU_HEROES_v02.png](./layers/STAGE01_MENU_HEROES_v02.png)
- [STAGE01_MENU_RUN_SETUP_v02.png](./layers/STAGE01_MENU_RUN_SETUP_v02.png)
- [STAGE01_MENU_LOADING_v02.png](./layers/STAGE01_MENU_LOADING_v02.png)
- [STAGE01_MENU_RESULT_VICTORY_SOYEON_v02.png](./layers/STAGE01_MENU_RESULT_VICTORY_SOYEON_v02.png)
- [STAGE01_MENU_RESULT_VICTORY_LIN_v02.png](./layers/STAGE01_MENU_RESULT_VICTORY_LIN_v02.png)
- [STAGE01_MENU_RESULT_DEFEAT_LIN_v02.png](./layers/STAGE01_MENU_RESULT_DEFEAT_LIN_v02.png)
- [STAGE01_MENU_RESULT_DEFEAT_SOYEON_v02.png](./layers/STAGE01_MENU_RESULT_DEFEAT_SOYEON_v02.png)
- [STAGE01_MENU_REVIEW_GRID_v02.png](./STAGE01_MENU_REVIEW_GRID_v02.png)
- [STAGE01_MENU_UI_CONTRACT_v02.md](./STAGE01_MENU_UI_CONTRACT_v02.md)
- [STAGE01_MENU_VISUAL_FAMILY_v02.md](./STAGE01_MENU_VISUAL_FAMILY_v02.md)
- [STAGE01_MENU_CANDIDATE_PROVENANCE_v02.json](./STAGE01_MENU_CANDIDATE_PROVENANCE_v02.json)
- [STAGE01_MENU_REVIEW_PACK_v02.md](./STAGE01_MENU_REVIEW_PACK_v02.md)

Все v02 preview — 390×844 sRGB. Они остаются visual candidates/review evidence и не считаются автоматически `APPROVED GOLDEN` или `PRODUCTION`.

## Godot navigation prototype

- [project.godot](../../../project.godot)
- [menu.tscn](../../../scenes/menu/menu.tscn)
- [menu_controller.gd](../../../scripts/menu/menu_controller.gd)

Прототип навигации пока использует часть старых v01 art/UI layers как временные backgrounds. Эти файлы перенесены в [`../_archive/family-v01/01-menu/`](../_archive/family-v01/01-menu/) и помечены как `LEGACY_RUNTIME_DEPENDENCY`; пути в контроллере обновлены на архив. Это не делает v01 активным visual family.

## Архив

Старые направления A/B/C, экраны v01, UI contract v01 и старые ART/UI_RU/COMPOSITE_RU слои больше не лежат в активной stage-папке. Они сохранены в [`_archive/family-v01`](../_archive/family-v01/README.md) только для истории и provenance.

## Критерий DONE

Этап закрывается только после явного утверждения выбранного visual family, проверки всех обязательных состояний, читаемости на телефоне, safe area и навигационного маршрута без тупиков, а также требуемого runtime/Android evidence.


## Candidate package v04 — USER REVIEW

Новая серия экранов и активных UI-ассетов после отклонения v03:

`ГЛАВНОЕ МЕНЮ -> ВЫБОР ЭТАПА -> ВЫБОР ПЕРСОНАЖА -> НАЧАТЬ ЗАБЕГ`

Отдельная ветка: `ГЛАВНОЕ МЕНЮ -> МАГАЗИН` с шестью глобальными пассивными улучшениями:
`ЖИВУЧЕСТЬ`, `СИЛА`, `ПРОВОРСТВО`, `ФОКУС`, `МАГНИТ`, `ЗАЩИТА`.

- [STAGE01_MENU_SYSTEM_REVIEW_PACK_v04.md](./STAGE01_MENU_SYSTEM_REVIEW_PACK_v04.md)
- [STAGE01_MENU_SYSTEM_PROVENANCE_v04.json](./STAGE01_MENU_SYSTEM_PROVENANCE_v04.json)

v04 содержит четыре target-size PNG-экрана, отдельные normal/pressed PNG-кнопки и карточки. Все 50 индивидуальных PNG-объектов доставлены в приватный Supabase bucket `visual-assets` по зеркальному пути `moonevil-eclipse/docs/mockups/01-menu/layers/` и проверены. До явного approval пакет остаётся `USER REVIEW`, не `PRODUCTION`.
