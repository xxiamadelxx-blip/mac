# Mockups

Здесь хранятся активные визуальные мокапы игры. Индекс и статусы находятся в `../MOCKUP_INDEX.md`.

Каждый этап получает отдельную папку. Preview, описание поведения и файл привязки должны иметь одинаковый идентификатор и версию.

Нельзя отмечать этап DONE, если создана только папка или текстовое намерение без фактического мокапа и проверки.

## Каноническое хранение бинарных mockup-ассетов

Для ассетов, относящихся к этой папке `docs/mockups/`, решение Supabase откатировано. Каноническое место бинарных mockup-ассетов — GitHub-репозиторий `xxiamadelxx-blip/mac`.

Правила:

1. Каждый отдельный mockup-asset package выпускается ровно из **40 реальных бинарных PNG-файлов**.
2. PNG должны быть настоящими файлами в соответствующей stage-папке GitHub. Base64, data URL, PNG внутри текста, SVG/HTML/canvas-замена и ZIP без распакованных PNG не считаются размещением.
3. Пакет сначала имеет статус `QUEUED`. Статус `PLACED` разрешён только после подтверждения фактического GitHub tree/Contents: найдены все 40 точных путей и соответствующие бинарные blobs.
4. После подтверждения в реестре ниже обязательно записываются точные пути всех размещённых файлов, точные пути файлов в очереди, commit SHA и дата проверки.
5. Наличие объекта в Supabase, старого Release, README, manifest или сообщения агента не считается размещением в GitHub.
6. Размещение PNG в GitHub не означает Visual Lab approval. `PLACED` не равно `CANDIDATE`, `APPROVED GOLDEN` или `PRODUCTION`; provenance, technical QA и художественное решение Creative Director остаются обязательными.
7. Если stage требует несколько пакетов, каждый пакет ведётся отдельной записью по 40 PNG. Количество и имена файлов нельзя додумывать — их добавляют в реестр только по фактическому package manifest.

## Реестр бинарных PNG: размещено и на очереди

Этот раздел обновляется только после реальной проверки GitHub. Нельзя отмечать файл размещённым заранее.

### Фактически размещено в GitHub

Проверка: `main@d495aaa431fa6da481ed258c6ac9ae85233e441c`.

- Подтверждённых PNG в `docs/mockups/`: **0**.
- Точные размещённые файлы: **нет**.
- PNG, находящиеся только в Supabase или упомянутые в stage README, сюда не включаются.

### Пакеты на очереди

| Пакет / stage | Размещено | На очереди | Статус |
|---|---:|---|---|
| `docs/mockups/01-menu/` | 0/40 | 40 PNG; точные пути будут внесены после package manifest | `QUEUED` |
| `docs/mockups/02-arena/` | 0/40 | 40 PNG; точные пути будут внесены после package manifest | `QUEUED` |
| `docs/mockups/03-heroes/` | 0/40 | 40 PNG; точные пути будут внесены после package manifest | `QUEUED` |
| `docs/mockups/04-enemies/` | 0/40 | 40 PNG; точные пути будут внесены после package manifest | `QUEUED` |
| Stage 05–19 | 0 | Пакет открывается отдельной записью только при начале соответствующего этапа | `NOT_OPENED` |

### Формат записи после подтверждения

Для каждого пакета в этот README добавляются:

```text
package_id: <stable package ID>
stage_path: docs/mockups/<stage>/
required_png_count: 40
status: PLACED | QUEUED
placed_files:
  - docs/mockups/<stage>/<exact-file-01>.png
  - ...
queued_files:
  - docs/mockups/<stage>/<exact-file-01>.png
  - ...
github_commit: <commit SHA>
github_tree_or_contents_evidence: <verified path/blob evidence>
checked_at_utc: <timestamp>
```

Файл нельзя переводить из `QUEUED` в `PLACED`, пока список `placed_files` не содержит все 40 фактически подтверждённых PNG.

## Активная визуальная итерация

Этапы 1–2 используют единый soft-tonal candidate pack v02: [меню](./01-menu/README.md) и [арена](./02-arena/README.md). Активные composites, contracts, provenance и review-пакеты находятся только в соответствующих stage-папках.

Первое визуальное семейство v01 вынесено из активных каталогов в [`_archive/family-v01/`](./_archive/family-v01/README.md). Архив не является active candidate, golden или production source.

Статус этапов 1–2 — **IN PROGRESS / USER REVIEW**, пока не пройдены художественное утверждение и необходимые runtime/Android-проверки.
