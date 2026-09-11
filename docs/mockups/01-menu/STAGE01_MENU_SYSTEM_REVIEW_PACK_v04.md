# STAGE01_MENU_SYSTEM_REVIEW_PACK_v04

TASK-ID: MOCKUP-01-MENU-SYSTEM-01
Parent HEAD: 0f1695283a7bacdc6e30f87011c11b273b9d6372
Route: MOCKUP
Secondary route: UI_ART
Stage path: docs/mockups/01-menu/
Asset kind: screen-system / UI asset family
Asset ID: menu.system.soft_tonal.v04
Family ID: moonveil-menu-soft-tonal-v02
Candidate ID: vl-20260910-moonveil-menu-system-v04
Status: USER REVIEW
Technical status: PARTIAL / STATIC_IMAGE_PASS
Artistic status: PENDING
Binary delivery status: PENDING_GITHUB_UPLOAD

## Решение по отклонённому v03

Предыдущий candidate `vl-20260910-moonveil-menu-home-v03` сохранён как `REJECTED NON-PROMOTABLE`.

Новая серия учитывает решение Creative Director: нужен не один экран, а связанный набор экранов и самостоятельные PNG-ассеты всех активных элементов.

## Каноничный пользовательский поток

`ГЛАВНОЕ МЕНЮ`
→ нажать `ВЫБОР ЭТАПА`
→ `ВЫБОР ЭТАПА`
→ нажать `ВЫБРАТЬ` / `ДАЛЕЕ`
→ `ВЫБОР ПЕРСОНАЖА`
→ выбрать `ЛИНЬ ЮЭ` или `СОЁН ХАН`
→ нажать `НАЧАТЬ ЗАБЕГ`

Отдельная ветка из главного меню:

`ГЛАВНОЕ МЕНЮ`
→ `МАГАЗИН`
→ экран покупки постоянных пассивных улучшений за Gold.

## Созданные основные экраны

Все target-size screens: 390×844, PNG, sRGB.

- `STAGE01_MENU_HOME_v04.png` — главное меню; primary action `ВЫБОР ЭТАПА`.
- `STAGE01_MENU_STAGE_SELECT_v04.png` — выбор этапа; активен каноничный `ЭТАП 01`.
- `STAGE01_MENU_CHARACTER_SELECT_v04.png` — выбор Линь Юэ / Соён Хан после выбора этапа; использованы существующие character PNG, без перегенерации.
- `STAGE01_MENU_PASSIVE_SHOP_v04.png` — магазин шести глобальных пассивных веток.
- `STAGE01_MENU_SYSTEM_REVIEW_GRID_v04.png` — общий review preview четырёх экранов.

## Активные элементы

Для каждого активного UI-элемента созданы отдельные растровые состояния `NORMAL` и `PRESSED`:

- главная навигация: `ВЫБОР ЭТАПА`, `МАГАЗИН`, `ПЕРСОНАЖИ`, `АРСЕНАЛ`, `АРТЕФАКТЫ`, `НАСТРОЙКИ`;
- выбор этапа: `ВЫБРАТЬ`, `ДАЛЕЕ`, `НАЗАД`;
- выбор персонажа: `ЛИНЬ ЮЭ`, `СОЁН ХАН`, `НАЧАТЬ ЗАБЕГ`;
- магазин: `КУПИТЬ`, `УЛУЧШИТЬ`.

Отдельно созданы stage-node, stage-card, character-card и карточки пассивных улучшений. Кнопки не рисуются runtime-кодом.

## Каноничные пассивные ветки магазина

По `docs/BALANCE_ECONOMY_SPEC.md`:

- `ЖИВУЧЕСТЬ` — +2% максимального HP;
- `СИЛА` — +2% общего урона;
- `ПРОВОРСТВО` — +1.5% скорости движения;
- `ФОКУС` — −1.5% cooldown оружия;
- `МАГНИТ` — +4% радиуса подбора;
- `ЗАЩИТА` — +1% снижения урона.

Историческое ограничение «магазин не входит в M1» остаётся отмеченным в проектных документах; этот screen candidate создан по прямому запросу Creative Director и не подключается в runtime автоматически.

## Existing character source

В character cards использованы существующие PNG-ассеты Stage 03:

- `docs/mockups/03-heroes/layers/STAGE03_HERO_LIN_YUE_PORTRAIT_v02.png`;
- `docs/mockups/03-heroes/layers/STAGE03_HERO_SOYEON_HAN_PORTRAIT_v02.png`.

Линь Юэ и Соён Хан не перегенерировались и не менялись как identity family.

## GitHub PNG batch delivery

Канонический binary destination: `xxiamadelxx-blip/mac@main/docs/mockups/01-menu/layers/<filename>.png`.

Пакет содержит 50 отдельных PNG. В текущем GitHub tree фактическое наличие этих файлов не подтверждено, поэтому статус — `PENDING_GITHUB_UPLOAD`.

Размещение выполняется двумя отдельными запусками: batch 001 = 40 PNG, затем после проверки batch 001 batch 002 = оставшиеся 10 PNG. Каждый batch получает отдельный evidence-файл в `docs/asset_batches/01-menu/`.

ZIP, архивы, PNG/Base64 в чат, GitHub Release assets, SVG/HTML/data URL и кодовая отрисовка запрещены. Доставка не меняет и не перегенерирует Линь Юэ или Соён Хан.

## Static checks

- target-size screens проверены как PNG 390×844, sRGB;
- button PNG имеют отдельные normal/pressed states и touch-oriented размеры не меньше 48×48 для экранных размещений;
- русский текст проверен визуально: `ПЕРСОНАЖИ`, `ВЫБОР ЭТАПА`, `ЛИНЬ ЮЭ`, `СОЁН ХАН`, `КУПИТЬ`;
- character screen использует существующие heroine assets;
- no SVG, no runtime draw visual, no Base64 asset payload;
- exact SHA-256 зафиксированы в provenance.

## Open decisions

- Artistic approval/revision/rejection для v04;
- подтверждение, что магазин входит в нужный продуктовый срез, несмотря на историческую M1-оговорку;
- подтверждение/коррекция художественного решения v04 и последующий runtime promotion после APPROVE.

## Next action

Сделать отдельный запуск для batch 001 из 40 PNG, проверить GitHub paths/blobs и записать evidence. После этого остановиться; batch 002 запускается отдельно.

## Asset inventory

### Screens and backgrounds

- `STAGE01_MENU_CHARACTER_SELECT_v04.png`
- `STAGE01_MENU_HOME_v04.png`
- `STAGE01_MENU_PASSIVE_SHOP_v04.png`
- `STAGE01_MENU_STAGE_SELECT_v04.png`
- `STAGE01_MENU_SYSTEM_REVIEW_GRID_v04.png`
- `STAGE01_MENU_BG_CHARACTER_SELECT_v04.png`
- `STAGE01_MENU_BG_MAIN_v04.png`
- `STAGE01_MENU_BG_PASSIVE_SHOP_v04.png`
- `STAGE01_MENU_BG_STAGE_SELECT_v04.png`

### Buttons

- `BTN_ARSENAL_NORMAL_v04.png`
- `BTN_ARSENAL_PRESSED_v04.png`
- `BTN_ARTIFACTS_NORMAL_v04.png`
- `BTN_ARTIFACTS_PRESSED_v04.png`
- `BTN_BACK_NORMAL_v04.png`
- `BTN_BACK_PRESSED_v04.png`
- `BTN_CHARACTERS_NORMAL_v04.png`
- `BTN_CHARACTERS_PRESSED_v04.png`
- `BTN_CONTINUE_NORMAL_v04.png`
- `BTN_CONTINUE_PRESSED_v04.png`
- `BTN_LIN_SELECT_NORMAL_v04.png`
- `BTN_LIN_SELECT_PRESSED_v04.png`
- `BTN_PASSIVE_PURCHASE_NORMAL_v04.png`
- `BTN_PASSIVE_PURCHASE_PRESSED_v04.png`
- `BTN_PASSIVE_UPGRADE_NORMAL_v04.png`
- `BTN_PASSIVE_UPGRADE_PRESSED_v04.png`
- `BTN_SETTINGS_NORMAL_v04.png`
- `BTN_SETTINGS_PRESSED_v04.png`
- `BTN_SOYEON_SELECT_NORMAL_v04.png`
- `BTN_SOYEON_SELECT_PRESSED_v04.png`
- `BTN_STAGE_CHOOSE_NORMAL_v04.png`
- `BTN_STAGE_CHOOSE_PRESSED_v04.png`
- `BTN_STAGE_SELECT_NORMAL_v04.png`
- `BTN_STAGE_SELECT_PRESSED_v04.png`
- `BTN_START_RUN_NORMAL_v04.png`
- `BTN_START_RUN_PRESSED_v04.png`
- `BTN_STORE_NORMAL_v04.png`
- `BTN_STORE_PRESSED_v04.png`

### Cards and nodes

- `CARD_STAGE_01_ACTIVE_v04.png`
- `STAGE_NODE_ACTIVE_v04.png`
- `STAGE_NODE_LOCKED_v04.png`
- `CARD_CHARACTER_LIN_v04.png`
- `CARD_CHARACTER_SOYEON_v04.png`
- `CARD_PASSIVE_AGILITY_v04.png`
- `CARD_PASSIVE_DEFENSE_v04.png`
- `CARD_PASSIVE_FOCUS_v04.png`
- `CARD_PASSIVE_FORCE_v04.png`
- `CARD_PASSIVE_MAGNET_v04.png`
- `CARD_PASSIVE_VITALITY_v04.png`
- `STAGE01_MENU_CHARACTER_PORTRAIT_LIN_v04.png`
- `STAGE01_MENU_CHARACTER_PORTRAIT_SOYEON_v04.png`
