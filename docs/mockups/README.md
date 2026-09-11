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
- размер партии определяется фактическим manifest и безопасным лимитом чата/транспорта;
- 40 файлов — только ориентир для больших наборов, не обязательный размер; если набор меньше, выкладывается весь набор;
- один агентский запуск обрабатывает только одну партию и после evidence останавливается;
- следующая партия начинается только отдельным запуском после перечитывания живого `main` и проверки evidence предыдущей;
- `PLACED` ставится только после проверки всех фактических GitHub paths/blobs и SHA-256;
- ZIP, архивы, PNG/Base64 в чат, data URL, SVG/HTML-замены и кодовая отрисовка финального визуала запрещены;
- runtime-код только ссылается на локальные asset paths и не рисует финальный визуал кодом.

Исторические внешние объекты и старые Release-записи не являются доказательством размещения в текущем GitHub tree.

### Restart Stage 01 — текущее состояние

Текущий утверждённый hero master:

- `docs/mockups/01-menu/candidates/STAGE01_MENU_HOME_CANDIDATE_v02.png` — 390×844, `APPROVED GOLDEN`;
- candidate ID: `vl-20260911-menu-home-master-v02`;
- commit с бинарным PNG: `ad897f13686865292f88f087fc45a444b5a89ade`;
- blob: `0d46c417c7d56ce4886df36692c3dd2c675f35a8`;
- прямой preview: [STAGE01_MENU_HOME_CANDIDATE_v02.png](./01-menu/candidates/STAGE01_MENU_HOME_CANDIDATE_v02.png).

Кандидат v01 сохранён как историческая версия до удаления слогана и не является текущим approval target. v02 утверждён только как визуальный home master; это не означает автоматическое утверждение остальных экранов и не переводит ассет в `PRODUCTION`.

### Scope Stage 01 — внутренняя menu/navigation system

Канонический pre-run маршрут: `ГЛАВНОЕ МЕНЮ → НАЧАТЬ ЗАБЕГ → ВЫБОР ПЕРСОНАЖА → ВЫБОР ЭТАПА → ПОДТВЕРЖДЕНИЕ → ЗАГРУЗКА`.

В Stage 01 относятся все экраны и UI-состояния до, между и сразу после запуска забега:

- главный экран меню;
- выбор этапа;
- выбор персонажа;
- run setup / подтверждение запуска;
- loading;
- экран результата победы/поражения;
- настройки;
- мета-магазин и экран покупки глобальных пассивных улучшений.

Разделение ответственности:

- визуальный экран магазина относится к Stage 01;
- сами пассивные способности, их иконки и data-описания относятся к Stage 07;
- портреты и боевые ассеты героинь относятся к Stage 03;
- внутриигровой HUD относится к Stage 10;
- внутриигровые предложения оружия/пассивок относятся к Stage 16;
- внутриигровой интерфейс артефактов относится к Stage 17;
- отображение информации о синергиях относится к Stage 19.

Stage 01 restart package v01 уже создан: 11 новых PNG размещены в GitHub; 10 точных визуальных кандидатов утверждены пользователем как `APPROVED GOLDEN`, review grid остаётся evidence-only. Старые v02/v04 screen mockups в новый пакет не включены.

### Handoff для следующей партии

```yaml
package_id: stage01-menu-internal-screens-next
stage_path: docs/mockups/01-menu/
manifest_png_count: null
batch_size_policy: adaptive
status: QUEUED
placed_files:
  - docs/mockups/01-menu/candidates/STAGE01_MENU_HOME_CANDIDATE_v02.png
queued_files: []
workspace_files: []
github_commit: ad897f13686865292f88f087fc45a444b5a89ade
github_tree_or_contents_evidence: blob:0d46c417c7d56ce4886df36692c3dd2c675f35a8
checked_at_utc: 2026-09-11
```

## Активная визуальная итерация





Этапы 1–2 используют единый soft-tonal candidate pack v02: [меню](./01-menu/README.md) и [арена](./02-arena/README.md). Активные composites, contracts, provenance и review-пакеты находятся только в соответствующих stage-папках.

Первое визуальное семейство v01 вынесено из активных каталогов в [`_archive/family-v01/`](./_archive/family-v01/README.md). Архив не является active candidate, golden или production source.

Stage 01 home master и restart package v01 — **APPROVED GOLDEN**; вся внутренняя menu/navigation system Stage 01 остаётся **IN PROGRESS** до нужных runtime/Android-проверок и отдельного production promotion. Stage 02 остаётся **USER REVIEW**.


### Stage 01 restart package v01 — handoff

- package: `stage01-menu-restart-v01`;
- candidate status: `USER REVIEW`;
- binary delivery: `PLACED`, 11/11 PNG;
- approved MAIN MENU v02: unchanged;
- placed files: все 11 путей перечислены в [batch-001.json](./../asset_batches/01-menu/batch-001.json);
- queued files: `[]`;
- old mockups used: `[]`;
- review pack: [STAGE01_MENU_SYSTEM_RESTART_v01_REVIEW_PACK.md](./01-menu/candidates/STAGE01_MENU_SYSTEM_RESTART_v01_REVIEW_PACK.md);
- next action: Creative Director возвращает APPROVE, REVISION или REJECT; следующая партия в этом запуске не начинается.


#### Follow-up: Soyeon Han result variants

Запрошены два новых варианта `ПОБЕДА` и `ПОРАЖЕНИЕ` для СОЁН ХАН. Они пока не сгенерированы и не размещены: built-in imagegen вернул `429 usage_limit_reached`. Старые мокапы и мутация существующих PNG запрещены; `batch-002` не создавался до появления новых бинарных файлов.
