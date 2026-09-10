# Binary asset transport — Supabase Storage

Статус: **CANONICAL BUILD-TIME CONTRACT**.

GitHub хранит код, сцены, JSON, manifests, инструкции и доказательства CI.
PNG, ZIP и другие бинарные пакеты не являются содержимым GitHub-репозитория и
не передаются через чат. Канонический транспорт бинарных ассетов — приватный
bucket Supabase Storage.

## Разделение ответственности

| Слой | Ответственность |
|---|---|
| GitHub | код, Godot-сцены, JSON, manifest, request-файл, CI-скрипты и документация |
| Supabase Storage | оригинальный ZIP, manifest ZIP и checksum-файл |
| CI | скачать ZIP, проверить размер/SHA-256, прогнать технический importer, commit-нуть только проверенные PNG |
| Godot runtime | потреблять импортированные файлы из репозитория; сеть и Storage во время игры не требуются |

Visual Lab по-прежнему решает provenance, technical status и artistic approval.
Загрузка в Storage не утверждает арт и не переводит candidate в `PRODUCTION`.

## Canonical object layout

Используется приватный bucket `game-assets`:

```text
game-assets/
  releases/stage03-assets-lin-yue-v01.zip
  manifests/stage03-assets-lin-yue-v01.json
  checksums/stage03-assets-lin-yue-v01.sha256
```

Пути версионируются. Не перезаписывай уже опубликованный объект: для нового
кандидата используй новое имя. `x-upsert: true` допускается только как явно
указанное аварийное действие владельца хранилища.

## Request contract

CI импортирует только request-файл со статусом `READY` и всеми полями ниже:

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

Пока точные байты не загружены, request обязан оставаться
`PENDING_SUPABASE_UPLOAD`. Нельзя выставлять `READY` по одному имени файла,
старому Release, manifest или сообщению агента.

## Upload protocol

Из каталога, где находится настоящий ZIP:

```bash
export SUPABASE_URL='https://<project-ref>.supabase.co'
export SUPABASE_STORAGE_API_KEY='<secure-key>'
export SUPABASE_STORAGE_AUTH_TOKEN='<secure-token>'

python3 scripts/assets/upload_stage03_to_supabase.py \
  stage03-assets-lin-yue-v01.zip
```

Скрипт перед upload проверяет имя, полный набор 96 или 192 путей, PNG IHDR
1024×1024 RGBA, traversal/symlink/duplicate entries, ZIP CRC, размер и SHA-256.
Архив отправляется потоково как настоящие байты. Для пакета больше 6 MiB по
умолчанию используется TUS resumable upload с чанками 6 MiB и direct storage
hostname; маленькие текстовые manifest/checksum отправляются обычным raw
HTTP upload. Ни PNG, ни ZIP не превращаются в строку и не попадают в чат.

Нужны только метаданные: имя объекта, размер, SHA-256 и два текстовых файла.
Протокольное кодирование TUS metadata, если оно используется библиотекой,
содержит только bucket/path/content-type; оно никогда не содержит байты PNG или
ZIP.

`SUPABASE_STORAGE_AUTH_TOKEN` и service/secret key разрешены только в CI или
локальном защищённом окружении. Их нельзя записывать в GitHub-файл, issue,
чат, URL или публичный клиент. Bucket по умолчанию приватный; anonymous upload
не включается.

## CI import

`.github/workflows/import-stage03-release-assets.yml` запускается push-ом
request-файла или вручную. Он:

1. читает только `READY` request;
2. скачивает `storage.object` через `.github/scripts/download_supabase_asset.py`;
3. сверяет `size_bytes` и SHA-256 до распаковки;
4. запускает существующий Stage 03 importer;
5. commit-ит фактически импортированные PNG в `docs/mockups/03-heroes/`;
6. сохраняет `import.log`, checksum и request metadata как evidence.

Событие GitHub Release больше не является триггером или источником. Старый
Release asset сохраняется только как исторический источник для одноразовой
перезагрузки точных байтов и не может закрыть binary intake сам по себе.

## Failure contract

Если Storage project, secret, объект, размер, SHA-256 или CI runner недоступны,
результат — `BLOCKED_BINARY_ARTIFACT` с конкретной причиной. Нельзя создавать
фиктивный ZIP, вставлять Base64, объявлять manifest бинарным содержимым или
ставить `IMPORTED` без реального списка файлов и exit code.

## Official Storage references

- [Standard uploads](https://supabase.com/docs/guides/storage/uploads/standard-uploads)
- [Resumable uploads](https://supabase.com/docs/guides/storage/uploads/resumable-uploads)
- [Storage access control](https://supabase.com/docs/guides/storage/security/access-control)
