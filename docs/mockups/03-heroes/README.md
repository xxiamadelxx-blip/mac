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

Каждый PNG доставляется отдельным объектом private Supabase Storage по
docs/ci/SUPABASE_ASSET_STORAGE.md. GitHub хранит только request/manifest/инструкции,
а CI скачивает и проверяет файлы в build workspace. Это build-time transport,
не runtime network dependency и не художественное approval. Пока request имеет
PENDING_SUPABASE_UPLOAD, папки runtime остаются без доказанного binary intake.
