# Stage 01 — Menu

Status: **IN PROGRESS** — три визуальных направления главного меню созданы; Direction B рекомендовано как база для следующей итерации.

## Текущие deliverables

- [STAGE01_MENU_DIRECTION_A_v01.png](./STAGE01_MENU_DIRECTION_A_v01.png) — лунный сад, кинематографичная подача;
- [STAGE01_MENU_DIRECTION_B_v01.png](./STAGE01_MENU_DIRECTION_B_v01.png) — основной кандидат с валютами, START RUN и нижней навигацией;
- [STAGE01_MENU_DIRECTION_C_v01.png](./STAGE01_MENU_DIRECTION_C_v01.png) — чернильно-фонарная тёмная подача;
- [STAGE01_MENU_DIRECTION_SELECTION_v01.md](./STAGE01_MENU_DIRECTION_SELECTION_v01.md) — сравнение вариантов и критерии утверждения.
- [STAGE01_MENU_HEROES_v01.png](./STAGE01_MENU_HEROES_v01.png) — экран выбора героини;
- [STAGE01_MENU_RUN_SETUP_v01.png](./STAGE01_MENU_RUN_SETUP_v01.png) — экран подготовки забега;
- [STAGE01_MENU_LOADING_v01.png](./STAGE01_MENU_LOADING_v01.png) — loading перед ареной;
- [STAGE01_MENU_RESULT_VICTORY_v01.png](./STAGE01_MENU_RESULT_VICTORY_v01.png) — успешное завершение;
- [STAGE01_MENU_RESULT_DEFEAT_v01.png](./STAGE01_MENU_RESULT_DEFEAT_v01.png) — поражение и сохранённая контрольная точка.
- [STAGE01_MENU_UI_CONTRACT_v01.md](./STAGE01_MENU_UI_CONTRACT_v01.md) — экранный маршрут, string keys, button states и критерии реализации.

Target preview: **390×844**, вертикальный экран.

## Следующая работа

- утвердить или скорректировать базовое направление;
- подготовить готовые к реализации экраны Home, Heroes, Run Setup, Loading и Result;
- заменить весь placeholder-текст на утверждённые строки и локализационные ключи;
- описать normal, pressed, disabled и locked states;
- разложить композицию на слои и зафиксировать переходы Home → Heroes → Run Setup → Arena.

## Прототип навигации

- [project.godot](../../../project.godot) — Godot 4.x, portrait viewport 390×844;
- [menu.tscn](../../../scenes/menu/menu.tscn) — main scene;
- [menu_controller.gd](../../../scripts/menu/menu_controller.gd) — real controls and screen transitions.

Прототип использует PNG как временный art-direction background, но навигационные кнопки являются реальными Godot controls. Arena не подменяется готовой игрой: после Loading показывается честный Stage 02 handoff с preview-only Victory/Run Ended.

## Русские слои UI

- [layers/README.md](./layers/README.md) — схема слоёв и соответствие экранов;
- *_ART_v01.png — неизменённый арт персонажей и окружения;
- *_UI_RU_v01.png — отдельный прозрачный слой с русскими панелями и текстом;
- *_COMPOSITE_RU_v01.png — контрольный русский preview.

Исходные лица, причёски, костюмы и позы не перегенерировались. Генератор больше не используется как источник текста.

PNG в этой папке — визуальный референс, а не финальный интерактивный UI.

## Критерий DONE

Этап закрывается только после утверждения направления, создания всех обязательных экранов и состояний, проверки читаемости на телефоне, проверки безопасную зону и фиксации навигационного маршрута без тупиков.
