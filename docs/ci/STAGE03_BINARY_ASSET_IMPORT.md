# Stage 03 — individual binary asset import

Статус: **IMPLEMENTED / BINARY INTAKE PENDING**.

Контур принимает уже существующие PNG героинь через приватный Supabase Storage.
Он не генерирует изображения, не мутирует героинь и не передаёт бинарные данные
через чат.

Полный транспортный контракт находится в
[`SUPABASE_ASSET_STORAGE.md`](SUPABASE_ASSET_STORAGE.md).

## Канонический поток

```text
готовые PNG на диске агента
  -> manifest с отдельными файлами и SHA-256
  -> отдельные Storage objects в visual-assets
  -> request со статусом READY
  -> GitHub Actions download + verify каждого объекта
  -> PNG validator
  -> build workspace/docs/mockups/03-heroes/<hero>/...
  -> Godot export
```

GitHub Release не является источником бинарных байтов. Runtime-файлы не
коммитятся обратно в GitHub: они скачиваются в рабочую директорию конкретной
сборки и исчезают после job.

## Требуемая структура Stage 03

Для одного героя требуется полный набор из 96 отдельных PNG:

```text
lin_yue/
  front/idle.png
  front/move_01.png
  ...
  south_west/shadow.png
```

Для двух героинь request перечисляет 192 отдельных объекта:

```text
lin_yue/<direction>/<state>.png
soyeon_han/<direction>/<state>.png
```

Разрешены восемь направлений (`front`, `back`, `left`, `right`, `north_west`,
`north_east`, `south_east`, `south_west`) и двенадцать состояний (`idle`,
`move_01`, `move_02`, `move_03`, `attack_01`, `attack_02`, `attack_03`,
`hit_01`, `hit_02`, `death_01`, `death_02`, `shadow`).

Каждый файл проверяется как PNG 1024×1024, 8-bit true RGBA. Также проверяются
пути без traversal, отсутствие дубликатов и совпадение заявленного размера и
SHA-256.

## Upload из телефона или удалённой среды

1. Получить реальные отдельные PNG в файловой системе агента.
2. Создать manifest с `local_path`, Storage `object`, MIME type, размером и
   SHA-256 для каждого файла.
3. Настроить в защищённой среде `SUPABASE_URL`,
   `SUPABASE_STORAGE_API_KEY` и `SUPABASE_STORAGE_AUTH_TOKEN`.
4. Запустить:

   ```bash
   python3 scripts/assets/upload_assets_to_supabase.py \
     --manifest path/to/upload-manifest.json \
     --report-output path/to/upload-report.json
   ```

5. Убедиться, что отчёт содержит `VERIFIED` для каждого объекта.
6. Перенести проверенные метаданные в `STAGE03_IMPORT_REQUEST.json`, поставить
   `READY` и отправить только текстовый request в GitHub.

Если Storage API write-token недоступен, не менять RLS и не создавать замену:
вернуть `BLOCKED_BINARY_ARTIFACT` с указанием недостающего канала.

## Request statuses

- `PENDING_SUPABASE_UPLOAD` — хотя бы один объект ещё не загружен или не проверен;
- `READY` — все перечисленные объекты имеют подтверждённые байты, размер и SHA-256;
- `IMPORTED` — CI скачал и проверил все файлы в build workspace;
- `BLOCKED_BINARY_ARTIFACT` — отсутствует Storage write-token, object, runner или evidence.

## Приёмка

Успешный intake означает только следующее:

- каждый Storage object скачан без подмены;
- размер и SHA-256 каждого объекта совпали;
- PNG прошли структурную проверку;
- файлы появились в build workspace нужной hero-папки;
- job завершился с exit code 0.

Это не означает artistic approval, `APPROVED GOLDEN` или `PRODUCTION`.
