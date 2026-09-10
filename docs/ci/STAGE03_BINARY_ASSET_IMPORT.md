# Stage 03 — binary asset import

Статус: **IMPLEMENTED / BINARY INTAKE PENDING**.

Этот контур принимает уже существующие бинарные PNG только через Supabase
Storage. Он не генерирует изображения, не мутирует героинь и не переносит PNG,
ZIP или Base64 через чат.

Полный storage-контракт находится в
[`SUPABASE_ASSET_STORAGE.md`](SUPABASE_ASSET_STORAGE.md).

## Канонический поток

```text
готовые PNG на диске агента
  -> проверенный ZIP
  -> raw/resumable upload в приватный Supabase Storage
  -> manifest + SHA-256
  -> STAGE03_IMPORT_REQUEST.json со статусом READY
  -> GitHub Actions download + verify
  -> importer
  -> docs/mockups/03-heroes/<hero>/...png
  -> commit в main
```

GitHub Release больше не используется как источник или триггер. Старый Release
asset остаётся историческим резервом до точной загрузки в Storage и сам по себе
не закрывает `BINARY_INTAKE_PENDING`.

## Содержимое ZIP

Для одного героя архив содержит полный набор из 96 файлов:

```text
lin_yue/
  front/idle.png
  front/move_01.png
  ...
  south_west/shadow.png
```

Разрешены два героя в одном архиве, тогда всего 192 PNG:

```text
lin_yue/<direction>/<state>.png
soyeon_han/<direction>/<state>.png
```

Также принимается архив с префиксом `docs/mockups/03-heroes/`. Другие файлы,
включая README и произвольные manifests, не являются частью этого ZIP-контракта
и отклоняются.

Проверяются:

- полное множество одного или двух героев;
- восемь направлений и двенадцать состояний;
- каждый файл — PNG 1024×1024, 8-bit true RGBA;
- отсутствие `..`, абсолютных путей, symlink и дубликатов;
- ZIP CRC;
- запрет перезаписи уже существующего runtime-файла.

Импортёр не меняет `hero_manifest.json`, stage manifest, provenance, artistic
status или runtime code. Импортированные PNG остаются candidate/technical
intake, пока Creative Director отдельно не подтвердит exact candidate.

## Upload из телефона или удалённой среды

1. Получить настоящий ZIP в файловой системе агента. Имя первого пакета:
   `stage03-assets-lin-yue-v01.zip`.
2. Настроить в защищённой среде `SUPABASE_URL`,
   `SUPABASE_STORAGE_API_KEY` и `SUPABASE_STORAGE_AUTH_TOKEN`.
3. Запустить:

   ```bash
   python3 scripts/assets/upload_stage03_to_supabase.py \
     stage03-assets-lin-yue-v01.zip
   ```

4. Сохранить выведенные `SHA256`, `SIZE_BYTES`, bucket/object и два текстовых
   файла manifest/checksum.
5. Обновить `docs/ci/STAGE03_IMPORT_REQUEST.json`: поставить `READY` и указать
   точные Storage object, SHA-256 и размер.
6. Commit request-файла запускает workflow. На телефоне достаточно сделать
   upload и commit текстового request; сам ZIP в чат или GitHub не загружается.

Для ZIP больше 6 MiB скрипт по умолчанию использует TUS resumable upload с
чанками 6 MiB. Это протокольные запросы к Storage; байты архива передаются
потоком и не сериализуются в текст.

## Request-файл

Минимальная форма `READY`:

```json
{
  "schema": "moonveil.stage03.storage_import_request",
  "version": 1,
  "status": "READY",
  "provider": "supabase_storage",
  "asset_name": "stage03-assets-lin-yue-v01.zip",
  "storage": {
    "bucket": "game-assets",
    "object": "releases/stage03-assets-lin-yue-v01.zip"
  },
  "integrity": {
    "sha256": "<64 lowercase hex characters>",
    "size_bytes": 82744571
  },
  "manifest_object": "manifests/stage03-assets-lin-yue-v01.json",
  "checksum_object": "checksums/stage03-assets-lin-yue-v01.sha256"
}
```

Статусы:

- `PENDING_SUPABASE_UPLOAD` — архив ещё не в Storage;
- `READY` — exact bytes и целостность подтверждены, CI может скачать;
- `IMPORTED` — CI реально создал список PNG и commit;
- `BLOCKED_BINARY_ARTIFACT` — отсутствует бинарный канал, secret, runner или
  evidence.

## Приёмка

Успешный импорт означает только следующее:

- Storage object скачан без подмены и его SHA-256/размер совпали;
- все файлы прошли структурную и PNG-проверку;
- PNG появились в правильной hero-папке;
- Actions создал commit в `main`;
- evidence содержит download/import log.

Это не означает artistic approval, `APPROVED GOLDEN` или `PRODUCTION`.

## Причины типичного отказа

- `Asset name must match...` — имя должно начинаться с `stage03-assets-` и
  заканчиваться `.zip`;
- `incomplete` — не хватает одного из 96/192 путей либо есть лишний путь;
- `expected 1024x1024` — экспорт сделан в другом размере;
- `expected 8-bit true RGBA` — PNG палитровый, RGB без alpha или с другим bit
  depth;
- `refusing to overwrite` — путь уже импортирован; создай новый candidate;
- `BLOCKED_BINARY_ARTIFACT` — не имитировать готовность, а исправить именно
  указанный Storage/CI канал.
