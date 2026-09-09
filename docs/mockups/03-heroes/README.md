# Этап 03 — героини

Статус: **DONE** — пакет visual mockup/evidence закрыт.

Этап разрешён до технического прогона этапа 2 по явному решению пользователя. Godot/Android-проверка арены остаётся отдельной технической задачей; её отсутствие не отменяет закрытие визуального пакета этапа 3.

## Канон двух героинь

| Героиня | Роль | Главное ощущение | Цветовой код |
|---|---|---|---|
| Линь Юэ — Нефритовая ведьма | дальний бой и контроль | спокойная точность, печати, замедление | нефрит / мятный / лунное серебро |
| Соён Хан — Алый клинок | ближний бой и критические рывки | скорость, риск, резкий вход в толпу | багровый / угольный / приглушённое золото |

## Закрытые deliverables

- full-body референсы, портреты и русский мокап выбора 390×844;
- manifest ролей, цветов, силуэтов, состояний и candidate IDs;
- боевой контракт `idle/move/basic_attack/ability/hit/death`;
- state-board кандидаты для всех шести состояний каждой героини;
- direction kit кандидаты `front/back/left/right` для каждой героини;
- true 1× и enlarged gameplay-scale review в массовой волне;
- отдельные VFX bindings и provenance-пакет Visual Lab.

## Файлы закрытия

| Файл | Назначение |
|---|---|
| `STAGE03_HEROES_COMBAT_SPRITE_SPEC_v01.md` | контракт 2D-спрайта, масштаба и handoff |
| `STAGE03_HEROES_VFX_BINDINGS_v01.json` | отдельные VFX для атак, способностей, hit/death |
| `STAGE03_HEROES_PROVENANCE_v01.json` | candidate IDs, источники, хэши и статусы |
| `layers/STAGE03_HERO_LIN_YUE_COMBAT_STATES_v01.png` | шесть боевых состояний Линь Юэ |
| `layers/STAGE03_HERO_SOYEON_HAN_COMBAT_STATES_v01.png` | шесть боевых состояний Соён Хан |
| `layers/STAGE03_HERO_LIN_YUE_DIRECTION_KIT_v01.png` | четыре направления Линь Юэ |
| `layers/STAGE03_HERO_SOYEON_HAN_DIRECTION_KIT_v01.png` | четыре направления Соён Хан |
| `layers/STAGE03_HEROES_GAMEPLAY_SCALE_REVIEW_v01.jpg` | exact 390×844 true 1× review |
| `layers/STAGE03_HEROES_GAMEPLAY_SCALE_REVIEW_ENLARGED_v01.jpg` | enlarged 853×1844 context review |

## Инварианты образа

- Линь Юэ сохраняет длинные чёрные волосы с нефритовым оттенком, лунное украшение, светлое многослойное одеяние и веер-печать.
- Соён Хан сохраняет высокий хвост с красной лентой, чёрно-багровый костюм, красный пояс и короткий алый клинок.
- Лицо, причёска, костюм и основной силуэт не меняются между портретом, full-body, боевым спрайтом и UI.
- На арене идентичность должна читаться без текста и без обязательного VFX.

## Evidence и границы

- Проверены наличие файлов, JSON-валидность, размеры PNG/JPEG и сохранение RGBA у state/direction candidates.
- На review board героини различаются среди массовой волны по силуэту, цветовой роли и механическому телеграфу.
- Кандидаты имеют статус `CANDIDATE`; художественная приёмка — `PENDING`. Они не являются `APPROVED GOLDEN` или `PRODUCTION`.
- State boards не являются готовыми Godot `SpriteFrames2D`; Android, runtime import, touch и APK остаются вне этого visual closure.

## Handoff

Следующий содержательный этап — **4. Мокапы противников**. Перед runtime-продакшеном этапы 6/11 должны привязать оружие и VFX через IDs из manifest и отдельного VFX binding-файла.
