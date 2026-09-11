# CI Execution Runbook

## Decision

- **Код и инструкции:** GitHub repository `xxiamadelxx-blip/mac`, branch `main`.
- **Бинарные ассеты:** приватный Supabase project `ylhbihgrchtqzaphuxvy`, bucket `visual-assets`.
- **Asset intake executor:** `.github/workflows/import-stage03-release-assets.yml`.
- **Godot environment:** `barichello/godot-ci:4.7.2` для существующих Godot jobs.
- **GitLab:** downstream mirror, не источник бинарных ассетов.
- **CircleCI:** legacy и не acceptance source, пока внешний проект не переподключён.

GitHub Actions получает только текстовый request, скачивает каждый Storage object
по защищённым secrets, проверяет байты и готовит их в build workspace. Бинарные
файлы не коммитятся обратно в GitHub.

## Required CI secrets

В настройках репозитория должны быть заданы:

- `SUPABASE_URL` — URL проекта;
- `SUPABASE_STORAGE_API_KEY` — ключ Storage API;
- `SUPABASE_STORAGE_AUTH_TOKEN` — защищённый token/service secret для приватного bucket.

Ни один секрет не записывается в репозиторий, request-файл, issue, URL или
workflow output. Runtime APK эти secrets не получает.

## Stage 03 acceptance

1. `docs/ci/STAGE03_IMPORT_REQUEST.json` имеет статус `READY`.
2. Request перечисляет каждый PNG отдельной записью с bucket/object,
   `local_path`, `content_type`, `sha256` и `size_bytes`.
3. Workflow скачивает объекты по одному и проверяет hash/size до importer-а.
4. `.github/scripts/import_stage03_assets.py` сообщает фактические `STAGED`
   paths, count, dimensions и RGBA.
5. Build workspace содержит файлы для Godot; GitHub tree не получает бинарный commit.
6. Evidence содержит download/import logs, object list и exit code.

Manifest без байтов, старый Release, список ожидаемых путей или сообщение агента
не являются acceptance evidence.

## Проверка runtime отдельно

После intake runtime-проверка остаётся независимой:

1. дождаться реального job conclusion `success`;
2. проверить runtime trace и отсутствие `SCRIPT ERROR`/`Parse Error`;
3. для Android требуется отдельное install/launch evidence;
4. проверить GitLab mirror только как синхронизацию SHA.

Не объявлять CI зелёным, если runner не стартовал.

## Failure contract

- Storage/secret/object unavailable → `BLOCKED_BINARY_ARTIFACT` с конкретной причиной;
- hash/size mismatch → job fail до Godot/import;
- invalid PNG → importer fail, без binary commit;
- runner unavailable → `BLOCKED` в handoff, без имитации evidence;
- artistic review pending → technical pass не переводит asset в `APPROVED GOLDEN` или `PRODUCTION`.
