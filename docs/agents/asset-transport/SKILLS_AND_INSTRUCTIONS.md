# Skills и инструкции Binary Asset Transport Agent

Этот агент отвечает только за доставку уже существующих бинарных ассетов в
сборочный контур. Он не генерирует, не мутирует, не перерисовывает и не
утверждает героинь, арену или любой другой арт.

## Обязательное чтение

Перед работой прочитать с текущего `main`:

1. `AGENTS.md`;
2. `docs/AGENT_SYNC_STATE.md`;
3. `docs/ci/SUPABASE_ASSET_STORAGE.md`;
4. `docs/ci/STAGE03_BINARY_ASSET_IMPORT.md` для Stage 03;
5. relevant Visual Lab law и asset manifest, если меняется путь или статус ассета.

Для технической реализации применяются `codex-engineering-guardrails:code-work`
и `codex-engineering-guardrails:code-verification`. Для Storage-интеграции
используется Supabase skill и актуальный Storage API.

## Канонический протокол

```text
отдельные реальные PNG/SVG на диске агента
  -> локальная проверка каждого файла
  -> отдельные raw/resumable uploads в visual-assets
  -> manifest с object/size/SHA-256
  -> текстовый request READY в GitHub
  -> CI download + verify каждого файла
  -> build workspace / Godot export
```

GitHub используется для текста и управления request-файлом. Бинарные байты нельзя
помещать в commit, issue, comment или чат. GitHub Release не закрывает intake.

## Проверка подключения

Сначала проверь Supabase project `ylhbihgrchtqzaphuxvy` и bucket
`visual-assets`. Management/SQL-коннектор подтверждает проект и metadata, но
для передачи байтов нужен авторизованный Storage API/CLI/CI write-token. Не
называй Supabase «отключённым», если management connection отвечает; укажи
точно, какого бинарного метода или секрета не хватает.

## Статусы

- `PENDING_SUPABASE_UPLOAD` — хотя бы один отдельный файл не загружен или не проверен;
- `READY` — у каждого объекта есть bucket/path, размер и SHA-256, подтверждённые Storage;
- `IMPORTED` — CI реально скачал и проверил перечисленные файлы в build workspace;
- `BLOCKED_BINARY_ARTIFACT` — отсутствует файл, Storage write-token, runner или evidence.

`READY` и `IMPORTED` нельзя ставить вручную без соответствующего evidence.

## Границы записи

Разрешено менять только transport scripts, storage contract, CI workflow, request
metadata и handoff-документы. Нельзя менять визуальные файлы, hero manifests,
artistic status, runtime mechanics или делать массовую регенерацию. CI не
коммитит бинарные файлы в GitHub.

## Секреты и безопасность

Используй только защищённые переменные:

- `SUPABASE_URL`;
- `SUPABASE_STORAGE_API_KEY`;
- `SUPABASE_STORAGE_AUTH_TOKEN`.

Секреты не пишутся в репозиторий, лог, URL, request или handoff. Bucket остаётся
приватным; runtime игры не получает Storage credentials. RLS не изменять для
обхода отсутствующего write-token.

## Handoff

```text
TASK-ID: ASSET-03
Parent HEAD: <SHA>
Changed paths: <exact list>
Status: READY | PARTIAL | BLOCKED | VERIFIED
Storage bucket/objects: <metadata only, one row per file>
SHA-256 / size: <values>
Evidence: <command, exit code, CI run, object verification>
Open blockers: <concrete list>
Next action: <exactly one>
```

Если отдельные файлы или авторизованный Storage write-channel отсутствуют, оставайся
на `BLOCKED_BINARY_ARTIFACT` и укажи ровно, что требуется для продолжения.
