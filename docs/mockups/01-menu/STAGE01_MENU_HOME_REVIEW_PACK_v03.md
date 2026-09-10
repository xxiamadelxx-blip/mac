# STAGE01_MENU_HOME_REVIEW_PACK_v03

TASK-ID: MOCKUP-01-MENU-HOME-01
Parent HEAD: fa7a32828d17d79a1af9f204df43f2412bbcd4f1
Route: MOCKUP
Secondary route: UI_ART
Stage path: docs/mockups/01-menu/
Asset kind: hero_master / screen
Asset ID: menu.home.soft_tonal.v03
Family ID: moonveil-menu-soft-tonal-v02
Candidate ID: vl-20260910-moonveil-menu-home-v03
Status: USER REVIEW
Technical status: PARTIAL / STATIC_IMAGE_PASS
Artistic status: PENDING
Storage status: BLOCKED_UPLOAD

## Что создано

Один representative master главного экрана вертикального меню как готовая PNG-картинка. Визуальная основа — оригинальная иллюстрация затопленного лунного сада; поверх неё собрана растровая UI-композиция мягкой tonal family Stage 01.

В GitHub не оставлен код визуала. Временный внутренний слой компоновки не является deliverable и не хранится в репозитории.

## Exact candidate

Формат: PNG, 390×844, sRGB  
SHA-256: be328b1802aa2c5e46e8ddf2a126df852bc16d330879f99e6951171cb07181b0  
Размер: 387921 bytes

Канонический путь для Supabase Storage:

- bucket: visual-assets
- object: moonevil-eclipse/docs/mockups/01-menu/layers/STAGE01_MENU_HOME_CANDIDATE_v03.png

Фактический статус на момент handoff: объект ещё не появился в Supabase. Прямой upload из текущего окружения завершился сетевым timeout; RLS-политики не изменялись и не ослаблялись.

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

- Итоговый файл — PNG 390×844, 8-bit RGB, sRGB.
- Обязательные labels присутствуют в растровой композиции и визуально проверены.
- Интерактивные области расположены внутри безопасной композиции; primary и secondary targets соответствуют размерам из README.
- Визуал существует как бинарный image asset, не как GDScript/HTML/canvas-отрисовка.
- PNG SHA-256 и размер зафиксированы выше.

## Evidence gaps

- Supabase Storage upload не завершён из текущего окружения; object path зарезервирован, но existence не подтверждён.
- Godot import не прогонялся: локальный Godot runner не заявлен.
- Android screenshot и touch test не прогонялись.
- Реальные font metrics/safe-area device inset не проверялись на устройстве.
- Это не APPROVED GOLDEN и не PRODUCTION.

## Creative Director decision

PENDING. Нужен выбор exact candidate:

- APPROVE — закрепить эту identity как basis для остальных menu states;
- REVISION — указать точечные правки;
- REJECT — пометить candidate non-promotable.

## Next action

Сначала доставить этот PNG в указанный Supabase object path и подтвердить его размер/SHA-256. После явного APPROVE создать остальные menu states тем же family contract; до этого batch и runtime integration не начинать.
