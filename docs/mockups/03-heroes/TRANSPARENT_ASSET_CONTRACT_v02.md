# Stage 03 transparent asset contract v02

Статус: **CANDIDATE**. Этот пакет добавляет runtime-ориентированные прозрачные PNG для двух героинь. Исторические v01 boards остаются в `layers/` как visual references.

## Каталог

```
docs/mockups/03-heroes/{hero_id}/{direction}/{state}.png
```

Героини:

- `lin_yue/`
- `soyeon_han/`

Направления:

- `front`, `back`, `left`, `right`
- `north_west`, `north_east`, `south_east`, `south_west`

Состояния:

- `idle`
- `move_01`, `move_02`, `move_03`
- `attack_01`, `attack_02`, `attack_03`
- `hit_01`, `hit_02`
- `death_01`, `death_02`
- `shadow`

## Технический стандарт

- canvas: **1024×1024 px**;
- PNG с настоящим RGBA alpha, без checkerboard/серого/зелёного фона;
- центрирование по общей боевой сетке, pivot: **bottom-center**;
- силуэт и ключевые цвета сохраняются между направлениями и состояниями;
- `shadow.png` — отдельный однотонный силуэтный слой;
- все имена — lowercase snake_case, одинаковые во всех папках.

## Производственный статус

Фронтальные листы состояний и восемь direction masters вырезаны в прозрачные PNG. Состояния, которых не было в исходном state-sheet, собраны как контролируемые производные; это позволяет закрыть runtime-контракт Stage 3, но не заменяет финальную покадровую художественную ревизию. Перед promotion в игру нужно проверить pivot, hitbox, VFX separation и импорт в Godot/Android.

Манифест пакета: `STAGE03_HEROES_RUNTIME_ASSET_MANIFEST_v02.json`.
Манифест каждой героини лежит в её папке как `hero_manifest.json`.
