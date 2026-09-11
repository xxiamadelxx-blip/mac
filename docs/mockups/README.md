# Mockups

Здесь хранятся активные визуальные мокапы игры. Индекс и статусы находятся в `../MOCKUP_INDEX.md`.

Каждый этап получает отдельную папку. Preview, описание поведения и файл привязки должны иметь одинаковый идентификатор и версию.

Нельзя отмечать этап DONE, если создана только папка или текстовое намерение без фактического мокапа и проверки.

## Каноническое хранение бинарных mockup-ассетов

Для `docs/mockups/**` действует отдельное решение от 2026-09-11: каноническое хранилище mockup-ассетов — GitHub, ветка `main`. Supabase не используется как источник истины для mockup-ассетов.

Правила транспортировки:

- Размер партии не фиксирован: если файлов немного, загружается весь набор; если файлов много (например, развёртка движения героини), набор делится на последовательные партии по текущему лимиту чата и транспорта. Число 40 — только практический пример, не обязательное условие.
- Base64 применяется только как транспортная кодировка при создании GitHub blob. В репозитории хранится декодированный бинарный PNG, а не текст Base64.
- Папки, README, manifest, старый Supabase object, Release или сообщение агента не доказывают размещение бинарника.
- Каждая партия получает статус `PLACED` только после проверки всех её точных GitHub paths, blob SHA и фактического PNG content.
- До approval допускается отдельный `USER REVIEW` preview-кандидат. Он нужен для проверки внешнего вида, не считается завершённой asset-партией и не переводится в `PLACED`.
- После каждой партии фиксируются exact placed files, exact queued/workspace files, commit SHA, blob/tree evidence и UTC-время проверки.
- `APPROVED GOLDEN` и `PRODUCTION` возможны только после отдельного художественного approval Creative Director и manifest linkage.

### Restart Stage 01 — текущее состояние

Review-кандидат размещён в GitHub:

- `docs/mockups/01-menu/candidates/STAGE01_MENU_HOME_CANDIDATE_v01.png` — 390×844, `USER REVIEW`;
- commit: `4cf3caeb7f930cef6f17f245e360b6d3fa369571`;
- blob: `14f5f06742bb9dbffeb06c5cb6ddf9f0aa4943cd`;
- прямой preview: [STAGE01_MENU_HOME_CANDIDATE_v01.png](./01-menu/candidates/STAGE01_MENU_HOME_CANDIDATE_v01.png).

Пакет Stage 01 пока не открыт к загрузке: его exact manifest и размер первой партии будут определены после approval этого кандидата. Нельзя считать исторические Supabase objects v02/v04 размещёнными в GitHub.

### Handoff-формат для каждой партии

```yaml
package_id: stage01-menu-home-batch-01
stage_path: docs/mockups/01-menu/
manifest_png_count: null
batch_size_policy: adaptive
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
