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
используется Supabase skill и только актуальный Storage API.

## Канонический протокол

```text
реальный ZIP на диске агента
  -> локальная структурная проверка
  -> raw/resumable upload в приватный Supabase bucket
  -> manifest + SHA-256
  -> текстовый request READY в GitHub
  -> CI download + verify
  -> существующий importer
  -> commit фактически созданных PNG
```

GitHub Release не является источником бинарных байтов. GitHub используется для
текста и управления request-файлом. Бинарные байты нельзя помещать в commit,
issue, comment или чат в виде PNG, ZIP, Base64, data URL или «примерного» файла.

## Статусы

- `PENDING_SUPABASE_UPLOAD` — ZIP ещё не загружен или его точность не доказана;
- `READY` — есть bucket/object, размер, SHA-256 и manifest/checksum object;
- `IMPORTED` — CI реально проверил и импортировал перечисленные PNG;
- `BLOCKED_BINARY_ARTIFACT` — канал, секрет, runner или evidence недоступны.

`READY` и `IMPORTED` нельзя ставить вручную без соответствующего evidence.
Manifest, список путей или старый Release не заменяют архив.

## Границы записи

Разрешено менять только transport scripts, storage contract, CI workflow,
request metadata и handoff-документы. Нельзя менять визуальные файлы, hero
manifests, artistic status, runtime mechanics или делать массовую регенерацию.
Importer может создать PNG только как точную распаковку принятого ZIP; агент не
создаёт заменяющие изображения.

## Секреты и безопасность

Используй только защищённые переменные:

- `SUPABASE_URL`;
- `SUPABASE_STORAGE_API_KEY`;
- `SUPABASE_STORAGE_AUTH_TOKEN`.

Секреты не пишутся в репозиторий, лог, URL, request или handoff. Bucket
остаётся приватным; runtime игры не получает Storage credentials. APK получает
ассеты на этапе CI и может работать офлайн.

## Handoff

```text
TASK-ID: ASSET-03
Parent HEAD: <SHA>
Changed paths: <exact list>
Status: READY | PARTIAL | BLOCKED | VERIFIED
Storage bucket/object: <metadata only>
SHA-256 / size: <values>
Evidence: <command, exit code, CI run, artifact>
Open blockers: <concrete list>
Next action: <exactly one>
```

Если настоящий ZIP или авторизованный Storage project отсутствует, остановись
на `BLOCKED_BINARY_ARTIFACT` и укажи ровно, что требуется для продолжения.
