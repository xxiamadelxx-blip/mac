# Слои меню v01

Все файлы рассчитаны на вертикальный экран **390×844**.

Для каждого состояния меню используются три слоя:

- *_ART_v01.png — исходный арт без перерисовки персонажей;
- *_UI_RU_v01.png — прозрачный PNG-слой с масками, панелями и русским интерфейсом;
- *_COMPOSITE_RU_v01.png — контрольный preview: арт + русский UI.

Исходный арт намеренно не изменяется. Это сохраняет лица, причёски, костюмы и позы без новых мутаций. Английские подписи закрываются непрозрачными UI-панелями, а русский текст лежит отдельным слоем.

## Набор экранов

| Состояние | Арт | UI-слой | Preview |
|---|---|---|---|
| Главная | STAGE01_HOME_ART_v01.png | STAGE01_HOME_UI_RU_v01.png | STAGE01_HOME_COMPOSITE_RU_v01.png |
| Героини | STAGE01_HEROES_ART_v01.png | STAGE01_HEROES_UI_RU_v01.png | STAGE01_HEROES_COMPOSITE_RU_v01.png |
| Подготовка забега | STAGE01_RUN_SETUP_ART_v01.png | STAGE01_RUN_SETUP_UI_RU_v01.png | STAGE01_RUN_SETUP_COMPOSITE_RU_v01.png |
| Загрузка | STAGE01_LOADING_ART_v01.png | STAGE01_LOADING_UI_RU_v01.png | STAGE01_LOADING_COMPOSITE_RU_v01.png |
| Победа | STAGE01_VICTORY_ART_v01.png | STAGE01_VICTORY_UI_RU_v01.png | STAGE01_VICTORY_COMPOSITE_RU_v01.png |
| Забег завершён | STAGE01_DEFEAT_ART_v01.png | STAGE01_DEFEAT_UI_RU_v01.png | STAGE01_DEFEAT_COMPOSITE_RU_v01.png |

SVG-файлы рядом — редактируемые исходники UI-слоёв. PNG используются Godot-прототипом и подходят для проверки на телефоне.

## Ограничения v01

- это визуальный слой и navigation prototype, а не окончательный интерактивный интерфейс;
- точные кнопки, локализация, safe area и reward ledger дополнительно проверяются в Godot;
- текст больше не берётся из генератора изображений;
- переход к реальной арене остаётся заглушкой до этапа 2.
