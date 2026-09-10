# CI Execution Runbook

## Decision

- **Код и инструкции:** GitHub repository `xxiamadelxx-blip/mac`, branch `main`.
- **Бинарные ассеты:** приватный Supabase Storage bucket `game-assets`.
- **Asset intake executor:** `.github/workflows/import-stage03-release-assets.yml`.
- **Godot environment:** `barichello/godot-ci:4.7.2` для существующих Godot jobs.
- **GitLab:** downstream mirror, не источник ассетов.
- **CircleCI:** legacy и не acceptance source, пока внешний проект не
  переподключён.

GitHub Release не является частью canonical binary path. GitHub Actions получает
только текстовый request, скачивает объект Storage по защищённым secrets и
commit-ит результат технического importer-а.

## Required CI secrets

В настройках репозитория должны быть заданы:

- `SUPABASE_URL` — URL проекта;
- `SUPABASE_STORAGE_API_KEY` — ключ для Storage API;
- `SUPABASE_STORAGE_AUTH_TOKEN` — защищённый token/service secret для приватного
  bucket.

Ни один из них не записывается в репозиторий, request-файл, issue, URL или
workflow output. Bucket остаётся приватным; runtime APK эти secrets не получает.

## Stage 03 acceptance

1. `docs/ci/STAGE03_IMPORT_REQUEST.json` имеет статус `READY`.
2. В request указаны exact `storage.bucket`, `storage.object`,
   `integrity.sha256`, `integrity.size_bytes`.
3. Workflow скачивает ZIP потоково и проверяет hash/size до распаковки.
4. `.github/scripts/import_stage03_assets.py` сообщает фактические
   `IMPORTED` paths, count, dimensions и RGBA.
5. Commit содержит только эти PNG и, для push-trigger, удаляет одноразовый
   request-файл.
6. Evidence содержит download/import logs и commit SHA.

`manifest` без байтов, старый Release asset, список ожидаемых путей или
сообщение агента не являются acceptance evidence.

## Проверка runtime отдельно

После binary intake runtime-проверка остаётся независимой:

1. дождаться реального job conclusion `success`;
2. проверить `R1_RUNTIME_TEST` и `R1_RUNTIME_TRACE` с `"ok":true`;
3. убедиться, что нет `SCRIPT ERROR`, `Parse Error` или invalid-call failure;
4. для Android требуется отдельное install/launch evidence;
5. проверить GitLab mirror только как синхронизацию SHA.

Не объявлять CI зелёным, если runner не стартовал. Не генерировать trace,
APK, PNG или ZIP в качестве замены отсутствующего job.

## Failure contract

- Storage/secret/object unavailable → `BLOCKED_BINARY_ARTIFACT` с конкретной
  причиной;
- hash/size mismatch → job fail до importer-а;
- invalid ZIP/PNG → importer fail, без commit;
- runner unavailable → `BLOCKED` в handoff, без имитации evidence;
- artistic review pending → binary technical pass не переводит asset в
  `APPROVED GOLDEN` или `PRODUCTION`.

## Current project note

На момент миграции текущий Stage 03 ZIP всё ещё числится в старом GitHub Release
и не доказан в Supabase Storage. Поэтому request оставлен в
`PENDING_SUPABASE_UPLOAD`; сначала нужно загрузить точные байты в выбранный
Storage project, затем выставить `READY`.
