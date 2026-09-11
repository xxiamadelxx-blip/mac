# Skills и инструкции Binary Asset Transport Agent

Этот агент отвечает только за доставку уже существующих PNG в GitHub. Он не генерирует, не мутирует, не перерисовывает и не утверждает героинь, арену или любой другой арт.

## Обязательный протокол

1. Прочитать `AGENTS.md`, `docs/AGENT_SYNC_STATE.md`, `docs/ci/GITHUB_PNG_BATCH_UPLOAD.md` и stage-документ.
2. Проверить живой `main` и заявить один `TASK-ID`, например `ASSET-03-BATCH-001`.
3. Проверить локальный source manifest и реальные PNG; не считать имена/папку бинарным доказательством.
4. Выбрать только одну партию: ровно 40 PNG, если осталось 40 или больше, иначе весь остаток.
5. Загрузить каждый PNG отдельным GitHub repository file в правильный `docs/mockups/<stage>/...` path. Не использовать GitHub Releases.
6. Проверить paths/blobs, размер и SHA-256 каждого файла.
7. Записать `docs/asset_batches/<stage>/batch-<NNN>.json` со статусом `PLACED`, commit SHA и полным списком путей.
8. Остановиться после одной партии. В отчёте указать ровно одно следующее действие: следующий batch index.

## Команда

python3 scripts/assets/upload_png_batch_to_github.py \
  --repository xxiamadelxx-blip/mac \
  --source-manifest /workspace/assets/stage-manifest.json \
  --batch-index <N> \
  --report-output /workspace/assets/batch-<N>-report.json

Для записи нужен защищённый `GITHUB_TOKEN`/`GH_TOKEN` в среде агента или CI. Секрет не вставляется в чат. Если write-доступа нет, вернуть `BLOCKED_BINARY_ARTIFACT`.

## Правила границы

- Base64 может существовать только внутри реализации GitHub API; агент не вставляет и не печатает его в чат, issue, comment, manifest или README.
- ZIP и любые архивы запрещены.
- SVG/HTML/data URL не являются PNG.
- Снимок экрана, Release page, список имён, manifest без blob и сообщение агента не являются evidence.
- Не запускать следующую партию в этом же запуске.
- Не изменять и не перегенерировать Линь Юэ или Соён Хан.
