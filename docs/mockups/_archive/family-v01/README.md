# Архив визуального семейства v01

Статус: **ARCHIVED / SUPERSEDED**.

Эта папка хранит визуальные материалы первой итерации, вытесненные актуальной soft-tonal family v02. Архив создан 2026-09-09 по решению Creative Director, чтобы старые кандидаты не смешивались с активными stage-пакетами.

## Правила

- содержимое архива не считается активным visual candidate и не должно использоваться как источник нового art direction;
- файлы не являются `APPROVED GOLDEN` или `PRODUCTION`;
- восстановление любого файла в активную stage-папку требует явного решения и нового review;
- технические v01-файлы, которые всё ещё являются действующими контрактами или не имеют замены, сюда не переносились только из-за номера версии;
- история Git и исходные blob SHA сохранены.

## Stage 01 — menu

Архивированы старые направления A/B/C, экраны v01, UI contract v01 и весь старый набор `ART / UI_RU / COMPOSITE_RU` вместе с его README.

Текущая замена: `docs/mockups/01-menu/` + `moonveil-menu-soft-tonal-v02`.

Важно: текущий Godot navigation prototype всё ещё использует часть старых слоёв как временные backgrounds. Его пути перенаправлены в этот архив, поэтому архивирование не должно ломать прототип. Это явно помеченная `LEGACY_RUNTIME_DEPENDENCY`, а не возврат v01 в активный visual family.

## Stage 02 — arena

Архивированы старый vertical art v01, пять старых combat-density composites v01, `STAGE02_ARENA_LAYER_MAP_v01.json` и `STAGE02_ARENA_VERIFICATION_v01.md`, поскольку для последних существуют v02-замены.

Текущая замена: `docs/mockups/02-arena/` + `moonveil-arena-soft-tonal-v02`.

`MACRO_LAYOUT_v01`, `COMPOSITION_v01`, `SCALE_GATE_v01`, ambient/remains и другие технические v01-файлы оставлены активными, если они всё ещё являются действующими контрактами и не были superseded.
