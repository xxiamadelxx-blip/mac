# Этап 02 — Арена

Статус: **IN PROGRESS / USER REVIEW**.

Активное визуальное семейство для нового art-review: `moonveil-lotus-garden-environment-soft-tonal-v03`. Runtime fallback v02 сохраняется до approval.

Цель этапа — большой связанный Затопленный сад Лунного лотоса, а не тесный вертикальный фон. Камера 390×844 показывает только сектор мира минимум 1560×2532.

## Действующие технические контракты

- `STAGE02_ARENA_MACRO_LAYOUT_v01.svg` + PNG-preview — макро-масштаб 4×3 viewport;
- `STAGE02_ARENA_COMPOSITION_v01.md` — композиционный контракт;
- `STAGE02_ARENA_SCALE_GATE_v01.md` — ворота масштаба;
- `layers/STAGE02_ARENA_OPEN_FIELD_ART_v02.png` — активный открытый игровой кадр;
- `layers/STAGE02_ARENA_AMBIENT_VFX_v01.*` — действующий независимый ambient layer;
- `layers/STAGE02_ARENA_REMAINS_20M_v01.*` — действующий слой стилизованных останков;
- `STAGE02_ARENA_LAYER_MAP_v02.json` — актуальная карта слоёв/зон;
- `STAGE02_ARENA_VERIFICATION_v02.md` — актуальная static verification.

Номер `v01` сам по себе не означает устаревший файл: технические контракты без superseding-замены остаются активными.

## Активный soft-tonal пакет v02

- [STAGE02_ARENA_COMPOSITE_0M_v02.png](./layers/STAGE02_ARENA_COMPOSITE_0M_v02.png)
- [STAGE02_ARENA_COMPOSITE_5M_v02.png](./layers/STAGE02_ARENA_COMPOSITE_5M_v02.png)
- [STAGE02_ARENA_COMPOSITE_10M_v02.png](./layers/STAGE02_ARENA_COMPOSITE_10M_v02.png)
- [STAGE02_ARENA_COMPOSITE_15M_v02.png](./layers/STAGE02_ARENA_COMPOSITE_15M_v02.png)
- [STAGE02_ARENA_COMPOSITE_20M_v02.png](./layers/STAGE02_ARENA_COMPOSITE_20M_v02.png)
- [STAGE02_ARENA_REVIEW_STRIP_v02.png](./STAGE02_ARENA_REVIEW_STRIP_v02.png)
- [STAGE02_ARENA_VISUAL_FAMILY_v02.md](./STAGE02_ARENA_VISUAL_FAMILY_v02.md)
- [STAGE02_ARENA_CANDIDATE_PROVENANCE_v02.json](./STAGE02_ARENA_CANDIDATE_PROVENANCE_v02.json)
- [STAGE02_ARENA_LAYER_MAP_v02.json](./STAGE02_ARENA_LAYER_MAP_v02.json)
- [STAGE02_ARENA_VERIFICATION_v02.md](./STAGE02_ARENA_VERIFICATION_v02.md)
- [STAGE02_ARENA_REVIEW_PACK_v02.md](./STAGE02_ARENA_REVIEW_PACK_v02.md)

Все v02 composite PNG — 390×844 sRGB. Художественный статус остаётся `PENDING`; runtime/Android acceptance отдельно не закрыта.

## Новый top-down environment package v03

v03 — USER REVIEW candidate для приглушённого top-down визуального кода.

- Top-down composite: ./STAGE02_ARENA_TOPDOWN_COMPOSITE_v03.svg
- Enlarged inspection: ./STAGE02_ARENA_TOPDOWN_INSPECTION_v03.svg
- Asset board: ./STAGE02_ARENA_ASSET_BOARD_v03.svg
- Asset manifest: ./STAGE02_ARENA_ASSET_MANIFEST_v03.json
- Placement map: ./STAGE02_ARENA_PLACEMENT_MAP_v03.json
- Visual family: ./STAGE02_ARENA_VISUAL_FAMILY_v03.md
- Review pack: ./STAGE02_ARENA_REVIEW_PACK_v03.md
- Separate base/landscape SVG assets: ./assets/

Правило v03: подложка арены не содержит декоративных объектов; каждый объект размещается отдельным asset_id поверх неё. Runtime fallback v02 не изменён, пока exact candidate не получит artistic approval.

## Архив

Старый vertical art v01, пять superseded combat-density composite v01 и версии layer-map/verification, имеющие v02-замены, вынесены в [`../_archive/family-v01/02-arena/`](../_archive/family-v01/02-arena/).

Архив не является active visual candidate и не должен использоваться новым art/design агентом как текущее направление.

## Runtime-preview

`scenes/arena/arena.tscn` и `scripts/arena/arena_controller.gd` используют активный `STAGE02_ARENA_OPEN_FIELD_ART_v02.png`; действующий ambient v01 оставлен на месте, потому что он не superseded и остаётся техническим слоем.

## Что ещё нужно для DONE

- открыть сцену в Godot 4.x;
- проверить все пять состояний и касание минимум в трёх местах;
- подключить настоящую героиню, врагов и отдельный слой XP;
- повторить проверку на Android и подтвердить performance budget;
- получить необходимое художественное approval.
