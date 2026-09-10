# Контекст репозитория для агента архитектуры первого забега

Снимок подготовлен для репозитория xxiamadelxx-blip/mac.

## Семантика снимка

Этот файл — статический context packet, а не live-указатель на ветку. В нём сохранены исторические параметры, на которых пакет был собран:

- prepared_baseline: snapshot of the repository before the latest documentation/art follow-up commits;
- prepared_baseline_commit: art: add lantern moth PNG state mockups;
- prepared_at: 2026-09-09.

Эти значения нужны только для происхождения контекста и не являются текущим состоянием ветки. Перед каждой работой агент обязан самостоятельно определить фактические repository, branch и HEAD. Отличие live HEAD от этого исторического baseline само по себе не является ошибкой, drift или блокером и не требует переписывать этот файл. В отчёте достаточно указать фактический HEAD и существенные изменения, влияющие на задачу.

## Технологический контракт

- Godot 4.x, native 2D, GDScript.
- Целевая платформа M1: Android APK; AAB для релиза.
- Офлайн-first, локальное версионируемое сохранение.
- Контрольный viewport: 390x844, вертикальный 9:16.
- Цель: 60 FPS, безопасный режим не ниже 30 FPS на Android среднего класса.
- Данные оружия, врагов, боссов, пассивок, синергий и артефактов должны быть data-driven.
- Массовые объекты и VFX должны иметь controlled spawn/pooling.
- Ошибка ресурса не должна превращаться в белый экран.

## Что заявлено в текущей архитектурной revision

- Один полный 30-минутный target run для этого architecture package.
- Два стартовых персонажа.
- Одна большая арена Затопленного сада Лунного лотоса.
- Десять существующих enemy families плюс три новые registry slots; варианты одного base enemy являются data records, а не отдельными reward systems.
- Шесть main-boss slots: 5/10/15/20/25/30 минут как target cadence; существующий финальный boss identity перенесён на 30:00.
- Три intermediate-boss slots: два сохранены из C3, один добавлен этой revision.
- До 15 chest windows: 8 configured non-final boss/mini-boss windows и 7 reserved non-boss windows; final boss никогда не создаёт boss chest.
- Оружие, пассивные умения, синергии/эволюции, артефакты и XP.
- HUD, выбор улучшений, пауза, смерть, победа, сохранение и идемпотентный reward ledger.
- XP-drop отделён от corpses/aftermath.
- Останки не имеют collision, не участвуют в pathfinding, не наносят урон и не заменяют XP.

Exact wave profiles, spawn budgets, active caps, enemy variant tuning, new-content names and extension reward values are not invented here. They remain PENDING_B1, PENDING_PRODUCT_DECISION or PENDING_CONTENT_REGISTRY as indicated by the contract.

Корневые GAME_MANIFEST.md, AGENT_CONTEXT.md, ROADMAP.md и docs/BALANCE_ECONOMY_SPEC.md пока содержат legacy 20-minute wording. They are read-only in this task; the conflict is recorded below and does not silently make the root docs look synchronized.

## Канонический визуальный и продуктовый язык

- Название: Moonveil: Eclipse / «Падение Лунного сада».
- Стиль: мягкая premium East Asian fantasy tonal family.
- Основные цвета: deep blue-gray, smoky teal, warm ivory, muted brass, jade; restrained crimson для identity/опасности.
- Нейтральный label меню: ПЕРСОНАЖИ.
- Арена — большое открытое пространство, окно камеры 390x844, а не размер мира.
- Landscape должен оставаться читаемым и взаимодействующим: вода, дорожки, корни, мостики, камни, растения.
- Боевой aftermath — отдельный накопительный визуальный слой.

Архитектурный агент не меняет визуальные assets и не делает выводов о production status из наличия PNG/SVG/mockup.

## Что реально есть в runtime на момент подготовки

### Меню

Сцена scenes/menu/menu.tscn и скрипт scripts/menu/menu_controller.gd образуют navigation prototype.

Фактически:

- создаются preview-слои и кнопки поверх подготовленного UI;
- часть экранов использует архивные v01 background paths;
- есть preview-переходы home, characters, run setup, loading, arena preview, victory/defeat;
- настройки, арсенал и артефакты остаются placeholders;
- реального выбранного персонажа, RunSession, reward ledger и save contract нет;
- в prototype встречается label ГЕРОИНИ, хотя актуальный контракт требует ПЕРСОНАЖИ;
- loading после короткой задержки переводит в arena scene, а не создаёт полноценный run lifecycle.

### Арена

Сцена scenes/arena/arena.tscn и scripts/arena/arena_controller.gd — proof-of-concept визуального preview.

Фактически:

- объявлены размеры мира и камеры;
- рендерится статическое поле с ambient-слоем;
- есть preview-mode и временные visual markers;
- нет полноценного героя, movement simulation, enemies, XP, HUD, waves, bosses, drops, persistence или 0→30 acceptance run;
- это evidence существующего preview, не готовая игровая архитектура.

## Текущий статус документации и stages

- Этап 1 menu: IN PROGRESS.
- Этап 2 arena: IN PROGRESS.
- Этап 3 heroes: DONE только как visual mockup/evidence package; art candidate, не production.
- Этап 4 enemies: IN PROGRESS.
- ROADMAP может содержать устаревший статус относительно AGENT_CONTEXT.md и docs/MOCKUP_INDEX.md. Конфликт фиксировать, не замалчивать.
- Visual Lab обязателен для visual/art/sprite/mockup задач; текущая архитектурная задача не должна входить в visual route.

## Источники для чтения runtime и канона

- AGENTS.md
- README.md
- GAME_MANIFEST.md
- AGENT_CONTEXT.md
- ROADMAP.md
- docs/BALANCE_ECONOMY_SPEC.md
- docs/MOCKUP_INDEX.md
- scripts/menu/menu_controller.gd
- scenes/menu/menu.tscn
- scripts/arena/arena_controller.gd
- scenes/arena/arena.tscn
- docs/mockups/04-enemies/STAGE04_ENEMIES_MANIFEST_v01.json

## Важное разделение статусов

## Extension sync boundary

Architecture owns the shape of the extension. Balance owns exact 30-minute wave/reward numbers; Content owns names, mechanics and registry records for the two new main bosses, the third intermediate boss and three new enemies; Runtime owns implementation and Android evidence. Until those owners publish compatible revisions, this package can be verified as a target contract but not as an implemented 30-minute run.


- Прочитано — не означает принято как истина, если документ противоречит более высокому источнику.
- Спроектировано — не означает реализовано.
- Реализовано — не означает проверено на Android.
- Technical PASS — не означает artistic approval.
- Candidate/mockup/preview — не означает production.
- Созданная папка или красивый markdown — не означает закрытие M1.
