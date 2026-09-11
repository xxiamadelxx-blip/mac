# CI Execution Runbook

## Decision

- Код, сцены, JSON, инструкции и реальные PNG хранятся в GitHub repository `xxiamadelxx-blip/mac`, branch `main`.
- PNG лежат отдельными файлами в правильной stage-папке, например `docs/mockups/03-heroes/...`; GitHub Release assets не используются.
- Максимум одной партии — 40 PNG. При остатке меньше 40 выкладывается только остаток. Один запуск агента обрабатывает одну партию и останавливается.
- Канонический upload/verification contract: [`GITHUB_PNG_BATCH_UPLOAD.md`](GITHUB_PNG_BATCH_UPLOAD.md).
- Проверяющий workflow: `.github/workflows/verify-github-png-batches.yml`.

## Для одной партии

1. Прочитать живой `main`, `AGENTS.md`, `docs/AGENT_SYNC_STATE.md` и предыдущие `docs/asset_batches/<stage>/batch-*.json`.
2. Выбрать один `batch_index`; при 40+ оставшихся файлов — ровно 40.
3. Загрузить PNG как отдельные GitHub repository files через `upload_png_batch_to_github.py`.
4. Проверить фактические GitHub paths/blobs, размер и SHA-256 каждого файла.
5. Создать evidence JSON со статусом `PLACED`, commit SHA и списком файлов.
6. Завершить запуск. Следующий агент/запуск перечитает evidence и начнёт следующую партию.

## Не является доказательством

- папка без PNG;
- список ожидаемых имён;
- manifest без связанного GitHub blob;
- GitHub Release page;
- скриншот или сообщение другого агента;
- Base64, data URL, SVG/HTML или кодовая отрисовка;
- запущенная, но не завершившаяся CI job.

Если реальный файл, GitHub write-доступ или проверка недоступны: `BLOCKED_BINARY_ARTIFACT`, точная причина и одно следующее действие. Никаких имитаций.
