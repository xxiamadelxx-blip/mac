# GitHub PNG batch upload contract

Статус: **CANONICAL BINARY TRANSPORT**.

Для MAC реальные PNG хранятся прямо в репозитории `xxiamadelxx-blip/mac` в отдельных файлах. GitHub Releases, внешние Storage-провайдеры и чат не являются хранилищем ассетов.

## Жёсткое правило партии

- Одна задача/один запуск агента = одна партия.
- Если осталось 40 или больше PNG — выкладываются ровно 40.
- Если осталось меньше 40 — выкладывается ровно оставшийся объём.
- После проверки текущей партии агент останавливается. Следующая партия начинается отдельным запуском после перечитывания живого `main`.
- Для Stage 03 из 192 PNG это пять партий: `40 + 40 + 40 + 40 + 32`.

Партия — это рабочая граница для чата, а не архив: каждый PNG остаётся отдельным файлом с отдельным GitHub path и Git blob.

## Канонический путь

xxiamadelxx-blip/mac@main
  docs/mockups/<stage>/<asset>.png
  docs/asset_batches/<stage>/batch-001.json

В batch evidence записываются только метаданные: `github_path`, `size_bytes`, `sha256`, `git_blob_sha`, batch index и commit SHA. Бинарные байты туда не копируются.

## Запуск

Нужны реальные PNG в файловой системе агента и входной manifest:

```json
{
  "stage": "03-heroes",
  "asset_root": "docs/mockups/03-heroes",
  "assets": [
    {
      "local_path": "/workspace/assets/lin_yue/front/idle.png",
      "github_path": "docs/mockups/03-heroes/lin_yue/front/idle.png"
    }
  ]
}
```

Запуск одной партии:

```bash
export GITHUB_TOKEN='<secure repository token>'
python3 scripts/assets/upload_png_batch_to_github.py \
  --repository xxiamadelxx-blip/mac \
  --branch main \
  --source-manifest /workspace/assets/stage03-manifest.json \
  --batch-index 1 \
  --report-output /workspace/assets/stage03-batch-001-report.json
```

Скрипт выбирает одну партию, проверяет PNG, создаёт отдельные Git blobs, коммит, проверяет удалённые blobs, записывает evidence `PLACED` и завершает работу. Следующий batch автоматически не запускается.

Внутреннее Base64-кодирование GitHub API не попадает в чат, отчёты или репозиторий. Агент не должен вручную готовить, вставлять или печатать Base64.

## Статусы

- `PENDING_GITHUB_UPLOAD` — бинарные файлы ещё не размещены;
- `PARTIAL_GITHUB_BATCH` — commit создан частично, но evidence полной проверки ещё нет;
- `PLACED` — все файлы именно этой партии реально лежат в GitHub и проверены;
- `BLOCKED_BINARY_ARTIFACT` — нет локального файла, GitHub write-доступа или проверки;
- `USER_REVIEW` — художественное решение ещё не принято; `PLACED` не означает artistic approval.

## Запрещено

- ZIP и любые архивы;
- PNG/Base64 в чат, issue, comment или README;
- GitHub Release как замена файлам в репозитории;
- SVG/HTML/data URL или draw-код вместо PNG;
- запуск второй партии в том же агентском запуске;
- изменение или перегенерация героинь ради транспортировки.
