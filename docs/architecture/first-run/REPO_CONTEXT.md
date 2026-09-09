# Контекст репозитория для агента архитектуры первого забега

Снимок подготовлен для репозитория xxiamadelxx-blip/mac.
HEAD main на момент подготовки: 9590ad3739ec77295f453fe09ffd2e5e7f153fba
Последний пользовательский коммит на момент подготовки: art: add lantern moth PNG state mockups

Если текущий HEAD отличается, агент обязан использовать фактический HEAD и записать отличие в отчёте.

## Технологический контракт

- Godot 4.x, native 2D, GDScript.
- Целевая платформа M1: Android APK; AAB для релиза.
- Офлайн-first, локальное версионируемое сохранение.
- Контрольный viewport: 390x844, вертикальный 9:16.
- Цель: 60 FPS, безопасный режим не ниже 30 FPS на Android среднего класса.
- Данные оружия, врагов, боссов, пассивок, синергий и артефактов должны быть data-driven.
- Массовые объекты и VFX должны иметь controlled spawn/pooling.
- Ошибка ресурса не должна превращаться в белый экран.

## Что заявлено каноном первого среза

- Один полный 20-минутный забег.
- Два стартовых персонажа.
- Одна большая арена Затопленного сада Лунного лотоса.
- Десять противников.
- Четыре босса на 5, 10, 15 и 20 минутах.
- Оружие, пассивные умения, синергии/эволюции, артефакты и XP.
- HUD, выбор улучшений, пауза, смерть, победа, сохранение.
- Checkpoint rewards, три валюты и идемпотентный reward ledger.
- XP-drop отделён от corpses/aftermath.
- Останки не имеют collision, не участвуют в pathfinding, не наносят урон и не заменяют XP.

Точные цифры, формулы, таблицы волн, XP и rewards брать из docs/BALANCE_ECONOMY_SPEC.md. Не дублировать их в архитектурных документах как независимый источник истины.

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
- нет полноценного героя, movement simulation, enemies, XP, HUD, waves, bosses, drops, persistence или 0→20 acceptance run;
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

- Прочитано — не означает принято как истина, если документ противоречит более высокому источнику.
- Спроектировано — не означает реализовано.
- Реализовано — не означает проверено на Android.
- Technical PASS — не означает artistic approval.
- Candidate/mockup/preview — не означает production.
- Созданная папка или красивый markdown — не означает закрытие M1.
