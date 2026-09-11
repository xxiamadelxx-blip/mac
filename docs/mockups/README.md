# Mockups

Здесь хранятся активные визуальные мокапы игры. Индекс и статусы находятся в `../MOCKUP_INDEX.md`.

Каждый этап получает отдельную папку. Preview, описание поведения и файл привязки должны иметь одинаковый идентификатор и версию.

Нельзя отмечать этап DONE, если создана только папка или текстовое намерение без фактического мокапа и проверки.

## Каноническое хранение бинарных mockup-ассетов

Каноническое бинарное хранилище mockup-ассетов — GitHub repository `xxiamadelxx-blip/mac`, ветка `main`.

- Реальные PNG лежат отдельными файлами под `docs/mockups/<stage>/`.
- Batch evidence лежит под `docs/asset_batches/<stage>/batch-<NNN>.json`.
- GitHub Release assets не являются файлами репозитория и не используются.

Правила транспортировки:

- отдельный `USER REVIEW` preview можно разместить для одобрения внешнего вида до пакетной выкладки;
- если осталось 40 или больше PNG, одна партия содержит ровно 40;
- если осталось меньше 40, последняя партия содержит ровно оставшийся объём;
- один агентский запуск обрабатывает только одну партию и после evidence останавливается;
- следующая партия начинается только отдельным запуском после перечитывания живого `main` и проверки evidence предыдущей;
- `PLACED` ставится только после проверки всех фактических GitHub paths/blobs и SHA-256;
- ZIP, архивы, PNG/Base64 в чат, data URL, SVG/HTML-замены и кодовая отрисовка финального визуала запрещены;
- runtime-код только ссылается на локальные asset paths и не рисует финальный визуал кодом.

Исторические внешние объекты и старые Release-записи не являются доказательством размещения в текущем GitHub tree.

### Restart Stage 01 — текущее состояние

Review-кандидат размещён в GitHub:

- `docs/mockups/01-menu/candidates/STAGE01_MENU_HOME_CANDIDATE_v01.png` — 390×844, `USER REVIEW`;
- commit: `4cf3caeb7f930cef6f17f245e360b6d3fa369571`;
- blob: `14f5f06742bb9dbffeb06c5cb6ddf9f0aa4943cd`;
- прямой preview: [STAGE01_MENU_HOME_CANDIDATE_v01.png](./01-menu/candidates/STAGE01_MENU_HOME_CANDIDATE_v01.png).

Пакет Stage 01 пока не открыт к загрузке: его exact manifest и размер первой партии будут определены после approval этого кандидата. Нельзя считать исторические внешние objects v02/v04 размещёнными в GitHub.

### Handoff-формат для каждой партии

```yaml
package_id: stage01-menu-home-batch-01
stage_path: docs/mockups/01-menu/
manifest_png_count: null
batch_size_policy: exact-40-or-final-remainder
status: QUEUED
placed_files: []
queued_files: []
workspace_files: []
github_commit: null
github_tree_or_contents_evidence: null
checked_at_utc: null
```

## Активная визуальная итерация



Этапы 1–2 используют единый soft-tonal candidate pack v02: [меню](./01-menu/README.md) и [арена](./02-arena/README.md). Активные composites, contracts, provenance и review-пакеты находятся только в соответствующих stage-папках.

Первое визуальное семейство v01 вынесено из активных каталогов в [`_archive/family-v01/`](./_archive/family-v01/README.md). Архив не является active candidate, golden или production source.

Статус этапов 1–2 — **IN PROGRESS / USER REVIEW**, пока не пройдены художественное утверждение и необходимые runtime/Android-проверки.
