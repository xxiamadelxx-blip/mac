# Individual binary asset transport — Supabase Storage

Статус: **CANONICAL BUILD-TIME CONTRACT**.

GitHub хранит код, Godot-сцены, JSON, manifests, инструкции и доказательства
CI. Реальные PNG/SVG и другие утверждённые бинарные файлы хранятся в приватном
Supabase Storage project `ylhbihgrchtqzaphuxvy`, bucket `visual-assets`.

Каждый визуальный файл передаётся отдельным Storage object. Бинарные байты не
передаются через чат и не кодируются в Base64. Storage используется как
транспорт до удалённой сборки; APK получает файлы в build workspace и работает
офлайн.

## Разделение ответственности

| Слой | Ответственность |
|---|---|
| GitHub | код, сцены, JSON, manifests, request-файлы, CI и документация |
| Supabase Storage | отдельные PNG/SVG и другие принятые бинарные объекты |
| CI | скачать каждый объект, проверить размер/SHA-256, положить его в build workspace |
| Godot runtime | ссылаться на локальные build paths и approved manifests; не рисовать финальный визуал кодом |
| Visual Lab | provenance, технический статус, художественный review и promotion gates |

## Canonical object layout

Структура Storage повторяет канонические asset paths проекта:

```text
visual-assets/
  moonevil-eclipse/docs/mockups/01-menu/<asset>.png
  moonevil-eclipse/docs/mockups/02-arena/<asset>.png
  moonevil-eclipse/docs/mockups/03-heroes/<hero>/<direction>/<state>.png
  moonevil-eclipse/docs/mockups/04-enemies/<enemy>/<state>.png
```

Путь объекта версионируется именем candidate/family. Уже опубликованный объект
не перезаписывается без явного `--allow-overwrite` владельца хранилища.

## Manifest contract

Request хранится в GitHub и перечисляет каждый бинарный объект отдельно:

```json
{
  "schema": "moonveil.stage03.storage_import_request",
  "version": 2,
  "status": "READY",
  "provider": "supabase_storage",
  "storage": {
    "project_ref": "ylhbihgrchtqzaphuxvy",
    "bucket": "visual-assets",
    "prefix": "moonevil-eclipse/docs/mockups/03-heroes"
  },
  "assets": [
    {
      "asset_id": "stage03.lin_yue.front.idle",
      "local_path": "lin_yue/front/idle.png",
      "object": "moonevil-eclipse/docs/mockups/03-heroes/lin_yue/front/idle.png",
      "content_type": "image/png",
      "size_bytes": 123456,
      "sha256": "<64 lowercase hex characters>",
      "technical_status": "PASS",
      "artistic_status": "USER_REVIEW"
    }
  ]
}
```

`READY` разрешён только после того, как каждый перечисленный object реально
существует и для него подтверждены размер и SHA-256. Один список имён или
manifest без байтов не является evidence.

## Upload protocol

Из каталога с реальными PNG/SVG:

```bash
export SUPABASE_URL='https://ylhbihgrchtqzaphuxvy.supabase.co'
export SUPABASE_STORAGE_API_KEY='<secure-key>'
export SUPABASE_STORAGE_AUTH_TOKEN='<secure-token>'

python3 scripts/assets/upload_assets_to_supabase.py \
  --manifest path/to/upload-manifest.json \
  --report-output path/to/upload-report.json
```

Скрипт проверяет существование, тип, размер и SHA-256 каждого локального файла,
передаёт его напрямую в Storage и после записи повторно скачивает объект для
побайтной проверки. Manifest/report содержат только метаданные; сами PNG/SVG
через них не проходят.

`SUPABASE_STORAGE_AUTH_TOKEN` и service/secret key разрешены только в защищённой
среде CI или агента. Публичный ключ не превращает приватный bucket в канал
записи. Не ослаблять RLS: отсутствие Storage write-token — отдельный blocker.

## CI import

`.github/workflows/import-stage03-release-assets.yml`:

1. читает request со статусом `READY`;
2. проверяет bucket, object paths и наличие SHA-256/размера у каждого файла;
3. скачивает объекты по одному через `.github/scripts/download_supabase_asset.py`;
4. сверяет байты до передачи в importer;
5. проверяет PNG-контракт и помещает файлы только в build workspace;
6. не коммитит бинарные файлы обратно в GitHub.

Godot-код получает только локальный build path/manifest. Сеть и Storage
credentials в APK не попадают.

## Failure contract

Если не хватает проекта, Storage API write-token, объекта, размера, SHA-256 или
runner, результат — `BLOCKED_BINARY_ARTIFACT` с конкретной причиной. Нельзя
имитировать загрузку, подменять файл сообщением, использовать старый Release или
объявлять `READY` без проверки каждого объекта.

## Official references

- [Standard uploads](https://supabase.com/docs/guides/storage/uploads/standard-uploads)
- [Resumable uploads](https://supabase.com/docs/guides/storage/uploads/resumable-uploads)
- [Storage access control](https://supabase.com/docs/guides/storage/security/access-control)
