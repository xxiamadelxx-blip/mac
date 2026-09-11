<!-- LIVE-AGENT-SYNC: this is a target/reference document, not binary or runtime proof -->
> **Status correction:** read [`docs/AGENT_SYNC_STATE.md`](../../AGENT_SYNC_STATE.md). This file does not prove that runtime PNGs, Godot import, artistic approval, or Android evidence exist.

# Этап 03 — героини

Статус: **CANDIDATE** — добавлен прозрачный runtime-oriented пакет v02 поверх исторических Visual Lab boards v02.

## Новый runtime-пакет

Для обеих героинь добавлены отдельные папки с одинаковым контрактом:

```
docs/mockups/03-heroes/{hero_id}/{direction}/{state}.png
```

Каждая папка содержит 8 направлений:

`front`, `back`, `left`, `right`, `north_west`, `north_east`, `south_east`, `south_west`.

И 12 состояний:

`idle`, `move_01`, `move_02`, `move_03`, `attack_01`, `attack_02`, `attack_03`, `hit_01`, `hit_02`, `death_01`, `death_02`, `shadow`.

## Технический стандарт

- PNG RGBA с настоящей прозрачностью;
- 1024×1024 px;
- pivot bottom-center;
- одинаковая схема имён и папок для обеих героинь;
- `shadow.png` — отдельный силуэтный слой.

Фронтальные базовые состояния и direction masters вырезаны из чистых листов. Недостающие кадры закрыты контролируемыми производными; художественная покадровая approval и импорт в движок остаются следующими gate.

## Документы

- `STAGE03_HEROES_RUNTIME_ASSET_MANIFEST_v02.json` — новый общий runtime manifest.
- `TRANSPARENT_ASSET_CONTRACT_v02.md` — контракт каталогов, состояний и alpha.
- `lin_yue/hero_manifest.json` — manifest Линь Юэ.
- `soyeon_han/hero_manifest.json` — manifest Соён Хан.
- `STAGE03_HEROES_MANIFEST_v01.json` — историческая карта исходных boards.
- `STAGE03_HEROES_VFX_BINDINGS_v01.json` — существующие VFX bindings.


## Binary transport

Каждый PNG размещается отдельным файлом в GitHub repository `xxiamadelxx-blip/mac` по пути `docs/mockups/03-heroes/<hero>/<direction>/<state>.png`.

Stage 03 содержит 192 ожидаемых PNG: 96 для Линь Юэ и 96 для Соён Хан. Порядок размещения — пять отдельных запусков: `40`, `40`, `40`, `40`, `32`.

После каждой партии создаётся `docs/asset_batches/03-heroes/batch-<NNN>.json` с фактическими GitHub paths/blobs, размером и SHA-256. Следующая партия не начинается в том же запуске.

Пока evidence не подтверждает каждый конкретный PNG в GitHub, статус остаётся `PENDING_GITHUB_UPLOAD`; наличие manifest или папки не является binary evidence.

GitHub Release assets, ZIP, архивы, PNG/Base64 в чат и кодовая отрисовка вместо реальных файлов запрещены. Линь Юэ и Соён Хан не перегенерируются и не мутируются.
