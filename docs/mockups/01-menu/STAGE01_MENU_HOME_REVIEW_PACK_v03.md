# STAGE01_MENU_HOME_REVIEW_PACK_v03

TASK-ID: MOCKUP-01-MENU-HOME-01
Parent HEAD: 259d7ab2ae299c9d6db00ff102f9334a37aaef80
Route: MOCKUP
Secondary route: UI_ART
Stage path: docs/mockups/01-menu/
Asset kind: hero_master / screen
Asset ID: menu.home.soft_tonal.v03
Family ID: moonveil-menu-soft-tonal-v02
Candidate ID: vl-20260910-moonveil-menu-home-v03
Status: USER REVIEW
Technical status: PARTIAL / STATIC_CONTRACT_CHECKED
Artistic status: PENDING

## Что создано

Один representative master главного экрана вертикального меню как authored SVG-asset. Кандидат наследует существующую мягкую tonal family Stage 01 и не создаёт новую identity героинь.

Файл exact candidate:

- layers/STAGE01_MENU_HOME_CANDIDATE_v03.svg

## Source / canon audit

- Корневой визуальный контракт: глубокий сине-серый фон, smoky teal, warm ivory, muted brass, mist jade.
- Stage 01 README: главный экран, рабочее название, Start/Heroes/Arsenal/Artifacts/Settings, viewport 390×844.
- Visual Lab workflow: один master до batch; UI review в реальном viewport; technical status отдельно от artistic approval.
- Русская категория сохранена как ПЕРСОНАЖИ; слово ГЕРОИНИ не используется.
- Героини Линь Юэ и Соён Хан не изменялись и не перегенерировались.

## Состав экрана

- viewport 390×844, вертикальная композиция;
- верхний бренд MOONVEIL / ECLIPSE и русское название;
- лунный lotus emblem как самостоятельный UI identity mark;
- primary action НАЧАТЬ ЗАБЕГ;
- secondary actions ПЕРСОНАЖИ, ОРУЖИЕ, АРТЕФАКТЫ, НАСТРОЙКИ;
- безопасная зона: внешние поля не менее 30 px; верхний контент начинается ниже 24 px;
- touch targets: primary 274×58 px; secondary 130×52 px;
- отдельная нижняя служебная строка, не являющаяся интерактивной кнопкой.

## Static checks performed

- SVG имеет viewBox 0 0 390 844 и width/height 390×844.
- Все интерактивные области находятся внутри x=58..332 и y=430..620.
- На экране присутствуют обязательные русские labels exact text.
- Кандидат не содержит Base64, data URL, runtime draw calls или внешних URL.
- Визуал размещён как файл-ассет, а не строка GDScript/HTML/canvas.

## Evidence gaps

- Godot import не прогонялся: локальный Godot runner не заявлен.
- Android screenshot и touch test не прогонялись.
- Реальные font metrics/safe-area device inset не проверялись на устройстве.
- SHA-256 binary evidence не зафиксирован; это text SVG candidate, не Supabase production binary.
- Это не APPROVED GOLDEN и не PRODUCTION.

## Creative Director decision

PENDING. Нужен выбор exact candidate:

- APPROVE — закрепить эту identity как basis для остальных menu states;
- REVISION — указать точечные правки;
- REJECT — пометить candidate non-promotable.

## Next action

После явного APPROVE создать остальные menu states тем же family contract; до этого batch и runtime integration не начинать.
