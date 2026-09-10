# Context для Balance & Economy Agent

Этот файл — статический ориентир, а не live HEAD. Перед каждой работой агент обязан самостоятельно проверить repository, branch, HEAD и состояние дерева.

## Репозиторий

- Repository: xxiamadelxx-blip/mac.
- Primary branch: main.
- Engine: Godot 4.x, native 2D, GDScript.
- Target: Android APK/AAB.
- Viewport: 390x844, вертикальный 9:16.
- Runtime: offline-first, локальное версионируемое сохранение.
- Target performance: 60 FPS, безопасный режим не ниже 30 FPS на Android среднего класса.

## Фактическое состояние, которое нужно перепроверять

На момент подготовки этого пакета:

- B1 существует как design baseline и прямо говорит, что числовые параметры ещё не подключены к коду.
- Главное меню — навигационный prototype с переходами и preview-экранами.
- Arena controller — визуальный preview арены с ландшафтом/частицами/aftermath; полноценные movement, combat, enemies, XP, HUD, waves, bosses и persistence не доказаны.
- В репозитории уже есть отдельный архитектурный пакет первого забега: docs/architecture/first-run/.
- Канонические visual assets находятся под статусами Visual Lab и не являются разрешённым материалом для этого доменного агента.
- AGENT_CONTEXT.md отмечает, что absolute base HP/damage/speed по enemy_id должны быть подтверждены в B1 до закрытия соответствующего этапа; их нельзя выдумывать внутри visual manifest.

Этот список — evidence baseline, а не обещание текущего состояния. Если live-код изменился, обнови аудит и не переписывай контекст только ради совпадения.

## Что является входом

- B1: числовой baseline волн, enemy durability/XP, XP curve, checkpoint rewards, meta costs и acceptance.
- GAME_MANIFEST.md: объём M1, roster и продуктовые границы.
- AGENT_CONTEXT.md: канон проекта, текущие статусы и границы.
- docs/architecture/first-run/: контракты run state, wave, progression, chest, stats и ledger, если пакет уже заполнен.
- runtime-код: только evidence фактически работающего поведения.

## Что не следует предполагать

- Что меню уже запускает настоящий забег.
- Что visual mockup является production asset.
- Что данные B1 автоматически загружаются Godot.
- Что точные weapon/passive/synergy IDs и условия существуют только потому, что упомянуты в brief.
- Что «20 минут» сами по себе доказывают победу.
- Что логика должна жить в одном controller.

## Обязательное разделение

Каждый результат должен иметь один из статусов:

- CANON — прямо задан источником;
- DERIVED — вычислен из CANON по явной формуле;
- PENDING_B1 — значения нет или оно требует уточнения именно в B1;
- PENDING_PRODUCT_DECISION — нужна продуктовая/дизайнерская воля;
- IMPLEMENTED — подтверждено runtime/test evidence;
- NOT_IMPLEMENTED — описано, но не подключено;
- BLOCKED — нельзя безопасно продолжить без внешнего решения.

Не смешивай эти статусы в одной строке без пояснения.
