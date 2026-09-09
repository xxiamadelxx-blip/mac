# Этап 03 — боевые 2D-спрайты героинь v01

Статус этапа: **DONE** — пакет мокапов и evidence закрыт.
Статус Visual Lab: `CANDIDATE`; художественное утверждение: `PENDING`.
Статус runtime: `NOT_PROMOTED`; импорт в Godot/Android: `UNVERIFIED`.

## Решение арены

В бою героиня представлена компактным анимированным 2D-спрайтом, а не 3D-моделью и не full-body иллюстрацией. Меню и выбор используют большие референсы; арена использует отдельные боевые кандидаты.

| Параметр | Контракт |
|---|---|
| Логический экран | 390×844, portrait |
| Направления | 4: `front`, `back`, `left`, `right` |
| Состояния | `idle`, `move`, `basic_attack`, `ability`, `hit`, `death` |
| VFX | отдельный слой, не запечённый в identity sprite |
| Приоритет | читаемость силуэта в массовой волне |

## Кандидаты боевых состояний

| Героиня | Candidate ID | Файл | Размер |
|---|---|---|---:|
| Линь Юэ | `vl-20260909-hero-combat-lin-yue-states-v01` | `layers/STAGE03_HERO_LIN_YUE_COMBAT_STATES_v01.png` | 1024×342 |
| Соён Хан | `vl-20260909-hero-combat-soyeon-han-states-v01` | `layers/STAGE03_HERO_SOYEON_HAN_COMBAT_STATES_v01.png` | 1024×342 |

Порядок кадров на каждой панели: `idle → move → basic_attack → ability → hit → death`. Панели являются state-board preview/evidence, а не готовыми `SpriteFrames2D`.

## Кандидаты четырёх направлений

| Героиня | Candidate ID | Файл | Размер |
|---|---|---|---:|
| Линь Юэ | `vl-20260909-hero-directions-lin-yue-v01` | `layers/STAGE03_HERO_LIN_YUE_DIRECTION_KIT_v01.png` | 1024×377 |
| Соён Хан | `vl-20260909-hero-directions-soyeon-han-v01` | `layers/STAGE03_HERO_SOYEON_HAN_DIRECTION_KIT_v01.png` | 1024×432 |

Каждый direction kit содержит front/back/left/right. Направления зафиксированы как отдельные варианты для последующей сборки анимации; автоматическое зеркалирование не считается финальным runtime-решением.

## Проверка игрового масштаба

- `STAGE03_HEROES_GAMEPLAY_SCALE_REVIEW_v01.jpg` — true 1× preview 390×844.
- `STAGE03_HEROES_GAMEPLAY_SCALE_REVIEW_ENLARGED_v01.jpg` — enlarged context review 853×1844.
- Это составная review-доска, а не захват Godot: Линь Юэ показана в верхней половине, Соён Хан — в нижней.
- В затопленном Lotus Garden обе героини различимы среди массовой волны: нефритовый дальний контроль и печати Линь Юэ отделяются от алого ближнего разреза/рывка Соён; XP, телеграфы и тёмные силуэты врагов не сливаются с героями.
- Review board подтверждает визуальную читаемость направления, но не заменяет Android/Godot runtime-проверку.

## Разделение VFX

Привязки вынесены в `STAGE03_HEROES_VFX_BINDINGS_v01.json`. Веер/печати и алый след клинка являются отдельными effect bindings; герой должен оставаться узнаваемым при отключённом VFX.

## Граница закрытия

Этап 3 закрыт как visual mockup/evidence package. Кандидаты остаются `CANDIDATE`, художественная приёмка — `PENDING`; они не promoted в `APPROVED GOLDEN` или `PRODUCTION`. Runtime `SpriteFrames2D`, сцены Godot, Android import и APK относятся к следующей технической проверке.
