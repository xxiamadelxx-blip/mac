# Stage 01 — Menu

Status: **IN PROGRESS / HOME MASTER APPROVED; RESTART PACKAGE v01 APPROVED GOLDEN; SOYEON RESULT VARIANTS BLOCKED BEFORE GENERATION**.

Активное визуальное семейство: `moonveil-menu-soft-tonal-v02`.

## Исторический пакет v02 — НЕ ИСПОЛЬЗУЕТСЯ В НОВОМ RESTART

Старые screen mockups из этого раздела сохранены только как история. В новый пакет Stage 01 restart v01 они не переносились и не использовались.

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


## Исторический пакет v04 — НЕ ИСПОЛЬЗУЕТСЯ В НОВОМ RESTART

Новая серия экранов и активных UI-ассетов после отклонения v03:

`ГЛАВНОЕ МЕНЮ -> НАЧАТЬ ЗАБЕГ -> ВЫБОР ПЕРСОНАЖА -> ВЫБОР ЭТАПА -> ПОДТВЕРЖДЕНИЕ -> ЗАГРУЗКА`

Отдельная ветка: `ГЛАВНОЕ МЕНЮ -> МАГАЗИН` с шестью глобальными пассивными улучшениями:
`ЖИВУЧЕСТЬ`, `СИЛА`, `ПРОВОРСТВО`, `ФОКУС`, `МАГНИТ`, `ЗАЩИТА`.

- [STAGE01_MENU_SYSTEM_REVIEW_PACK_v04.md](./STAGE01_MENU_SYSTEM_REVIEW_PACK_v04.md)
- [STAGE01_MENU_SYSTEM_PROVENANCE_v04.json](./STAGE01_MENU_SYSTEM_PROVENANCE_v04.json)

v04 содержит четыре target-size PNG-экрана, отдельные normal/pressed PNG-кнопки и карточки. Пакет состоит из 50 отдельных PNG-файлов в `docs/mockups/01-menu/layers/`, но в текущем GitHub tree бинарное размещение не подтверждено: `PENDING_GITHUB_UPLOAD`. Исторический план `40` и `10` отменён: размер будущих партий определяется manifest и лимитом чата/транспорта. До явного approval пакет остаётся `USER REVIEW`, не `PRODUCTION`.


## Restart Stage 01 — candidate v01 — SUPERSEDED BY v02

Кандидат v01 сохранён как история первого review. После твоего замечания о слогане он заменён точечной редакцией v02.

- candidate ID: `vl-20260911-menu-home-master-v01`;
- binary commit: `4cf3caeb7f930cef6f17f245e360b6d3fa369571`;
- preview: [STAGE01_MENU_HOME_CANDIDATE_v01.png](./candidates/STAGE01_MENU_HOME_CANDIDATE_v01.png).

## Revision Stage 01 — candidate v02 — APPROVED GOLDEN

Текущий утверждённый home master:

- route: `UI_ART` + secondary `MOCKUP`;
- stage path: `docs/mockups/01-menu/`;
- asset ID: `menu.home`;
- family ID: `moonveil-menu-soft-tonal-v02`;
- candidate ID: `vl-20260911-menu-home-master-v02`;
- status: `APPROVED GOLDEN`;
- technical status: `STATIC EXPORT CHECKED`;
- artistic status: `APPROVED BY CREATIVE DIRECTOR`.

Preview: [STAGE01_MENU_HOME_CANDIDATE_v02.png](./candidates/STAGE01_MENU_HOME_CANDIDATE_v02.png).

Правка v02: удалён только текст “ТАМ, ГДЕ ЛУНА ТОНЕТ, ПРОБУЖДАЕТСЯ ИСТИНА.”. Текущий candidate утверждён для визуального направления главного меню. Runtime manifest и production promotion ещё не выполнялись.

## Scope Stage 01 — внутренняя menu/navigation system

Канонический pre-run маршрут: `ГЛАВНОЕ МЕНЮ → НАЧАТЬ ЗАБЕГ → ВЫБОР ПЕРСОНАЖА → ВЫБОР ЭТАПА → ПОДТВЕРЖДЕНИЕ → ЗАГРУЗКА`.

К Stage 01 относятся:

- главный экран;
- выбор этапа;
- выбор персонажа;
- run setup и подтверждение запуска;
- loading;
- результаты победы/поражения;
- настройки;
- мета-магазин и покупка глобальных пассивных улучшений.

Не путать экран и содержимое: экран магазина — Stage 01, а сами passive assets/data — Stage 07; портреты и боевые ассеты героинь — Stage 03; внутриигровой HUD — Stage 10; внутриигровые предложения оружия/пассивок — Stage 16; artifact UI — Stage 17; synergy info — Stage 19.

После approval home master следующая работа — создавать остальные внутренние экраны Stage 01. Размер любой партии определяется фактическим manifest и лимитом чата/транспорта; 40 — только пример.

## Stage 01 restart — NEW mockup package v01 — APPROVED GOLDEN

Пакет собран с нуля текущим генератором изображений. Старые Stage 01 v02/v04 mockups не использовались. Утверждённый MAIN MENU v02 не изменён. Пользователь утвердил 10 точных визуальных кандидатов 2026-09-11.

- [STAGE01_MENU_SYSTEM_RESTART_v01_REVIEW_PACK.md](./candidates/STAGE01_MENU_SYSTEM_RESTART_v01_REVIEW_PACK.md)
- [STAGE01_MENU_SYSTEM_RESTART_v01.provenance.json](./candidates/STAGE01_MENU_SYSTEM_RESTART_v01.provenance.json)
- [STAGE01_MENU_NEW_REVIEW_GRID_v01.png](./candidates/STAGE01_MENU_NEW_REVIEW_GRID_v01.png)

Новые candidate PNG:

- [STAGE01_HERO_LIN_YUE_MOCKUP_v01.png](./candidates/STAGE01_HERO_LIN_YUE_MOCKUP_v01.png)
- [STAGE01_HERO_SOYEON_HAN_MOCKUP_v01.png](./candidates/STAGE01_HERO_SOYEON_HAN_MOCKUP_v01.png)
- [STAGE01_MENU_CHARACTER_SELECT_CANDIDATE_v01.png](./candidates/STAGE01_MENU_CHARACTER_SELECT_CANDIDATE_v01.png)
- [STAGE01_MENU_STAGE_SELECT_CANDIDATE_v01.png](./candidates/STAGE01_MENU_STAGE_SELECT_CANDIDATE_v01.png)
- [STAGE01_MENU_RUN_CONFIRM_CANDIDATE_v01.png](./candidates/STAGE01_MENU_RUN_CONFIRM_CANDIDATE_v01.png)
- [STAGE01_MENU_LOADING_CANDIDATE_v01.png](./candidates/STAGE01_MENU_LOADING_CANDIDATE_v01.png)
- [STAGE01_MENU_RESULT_VICTORY_CANDIDATE_v01.png](./candidates/STAGE01_MENU_RESULT_VICTORY_CANDIDATE_v01.png)
- [STAGE01_MENU_RESULT_DEFEAT_CANDIDATE_v01.png](./candidates/STAGE01_MENU_RESULT_DEFEAT_CANDIDATE_v01.png)
- [STAGE01_MENU_SETTINGS_CANDIDATE_v01.png](./candidates/STAGE01_MENU_SETTINGS_CANDIDATE_v01.png)
- [STAGE01_MENU_PASSIVE_SHOP_CANDIDATE_v01.png](./candidates/STAGE01_MENU_PASSIVE_SHOP_CANDIDATE_v01.png)

Delivery: `PLACED`, 11/11 PNG; queued: `[]`. Artistic status: `APPROVED BY CREATIVE DIRECTOR` для 10 визуальных кандидатов; review grid — evidence only. Runtime promotion: not performed.


## Requested addition — Soyeon Han result variants — BLOCKED BEFORE GENERATION

Запрошены два новых независимых варианта для второй героини, СОЁН ХАН:

- `STAGE01_MENU_RESULT_VICTORY_SOYEON_VARIANT_CANDIDATE_v01.png` — победа;
- `STAGE01_MENU_RESULT_DEFEAT_SOYEON_VARIANT_CANDIDATE_v01.png` — поражение.

Оба файла **не созданы и не размещены**: встроенный новый генератор изображений вернул `429 usage_limit_reached` до выдачи результата. Старые мокапы не использовались, существующие PNG не мутировались и не копировались. Для этого запроса `batch-002` не создавался; очередь бинарной выкладки отсутствует, пока нет новых PNG. Следующее действие — отдельная генерация, техническая проверка, GitHub placement и передача ссылок на `USER REVIEW`.
