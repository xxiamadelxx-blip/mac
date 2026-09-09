
# FIRST_RUN_FLOW — целевой путь первого забега

Статус: **SPECIFIED_WITH_PENDING_DECISIONS**  
Область: один 20-минутный забег Moonveil: Eclipse, от boot до возврата в меню.  
Тип документа: логическая спецификация, не runtime-реализация.

## 1. Границы и источники

Авторитетное состояние забега живёт в **RunSession**. Экран и Godot-контроллеры получают только read model и отправляют команды.

Источники с приоритетом:

- docs/architecture/first-run/AGENT_TASK.md — обязательная цепочка и границы;
- GAME_MANIFEST.md — продуктовый цикл, content roster, 20 минут, слоты и герои;
- AGENT_CONTEXT.md — RunState, Android/offline-first и разделение XP/aftermath;
- docs/BALANCE_ECONOMY_SPEC.md — временные полосы, XP, награды и ограничения;
- scripts/menu/menu_controller.gd и scripts/arena/arena_controller.gd — evidence текущего prototype, не target behavior.

Рабочая трактовка: «следующая стадия» — логический checkpoint/wave band внутри одной большой арены. Отдельная сцена не требуется для M1; это WORKING_ASSUMPTION, а окончательная семантика остаётся U-05 / PENDING_PRODUCT_DECISION.

## 2. Участники и ownership

| Участник | Владеет | Не владеет |
|---|---|---|
| Игрок | Ввод, выбор героя, улучшений, пауза, подтверждение выхода, claim результата | Не меняет authoritative state напрямую |
| AppFlowCoordinator | Boot, маршрутизация экранов, menu/run bridge | Не считает урон, XP или награды |
| RunSession | Время, фаза, герой, build, stats, counters, drops, checkpoint | Не рисует UI и не пишет файл сам |
| RunSimulation | Движение, combat tick, wave director, boss lifecycle | Не выдаёт permanent/meta rewards |
| ProgressionService | XP, level-up offers, upgrade application, synergy eligibility | Не решает навигацию |
| RewardLedger | Reward entries и idempotency | Не принимает балансировочное решение |
| SaveRepository | Versioned snapshot, migration, validation | Не является source of truth во время тика |
| RunReadModel | Стабильная проекция HUD, pause и result | Не принимает domain commands |
| Diagnostics | Ошибки загрузки/сохранения/content version и recovery hints | Не маскирует ошибку пустым успехом |

## 3. End-to-end карта

~~~mermaid
flowchart TD
    A["Boot"] --> B["Menu"]
    B --> C["Characters / setup"]
    C --> D["Run loading"]
    D --> E["RunSession: waves, XP, build"]
    E --> F["Boss → chest / checkpoint"]
    F --> G["Next band or result"]
    G --> H["Rewards → menu"]
~~~

## 4. Запуск и меню

### 4.1 Boot, loading и ошибка ресурса

**Trigger:** процесс стартует.

**Порядок:**

1. AppFlowCoordinator создаёт Diagnostics и загружает content registry.
2. Валидируются schema version, обязательные stable IDs, boss/wave references и local save schema.
3. При успехе открывается MENU_HOME.
4. При отсутствии или устаревании ресурса открывается диагностическое состояние с кодом, path, версией и действиями retry/safe mode.
5. Если обязательный gameplay-контент невалиден, запуск забега блокируется; UI не подменяет проблему фальшивым успехом.

**Result:** menu read model содержит доступные разделы и diagnostic banner при наличии.

### 4.2 Главное меню

Игрок может открыть ПЕРСОНАЖИ, настройки, новый забег или validated recovery snapshot.

Если нет валидного selected hero, «Начать забег» ведёт в ПЕРСОНАЖИ. Если есть незавершённый snapshot, меню показывает отдельное восстановление. До решений U-06/U-07 нельзя обещать полный mid-run resume; label должен говорить о проверенном checkpoint, а не о гарантированном продолжении.

### 4.3 Настройки

Настройки открываются из меню и из pause overlay. Они не изменяют RunSession. После закрытия возвращается предыдущий owner screen: MENU_HOME или PAUSED. Ошибка чтения настройки не сбрасывает забег и попадает в Diagnostics.

### 4.4 ПЕРСОНАЖИ

Карточка показывает stable hero ID, имя, стартовые свойства, стартовое оружие, unlock state и selected state. Канонические IDs: lin_yue и soyeon_han.

Если hero record отсутствует, карточка disabled и создаётся CONTENT_MISSING. Другой герой не подставляется молча.

## 5. Создание нового забега

### 5.1 Run setup

**Trigger:** игрок нажимает «Начать забег».

**Guards:**

- выбранный герой существует и разблокирован;
- выбранные артефакты находятся в диапазоне 0–3;
- IDs разрешены registry;
- нет другого активного RunSession, либо игрок подтвердил policy выхода.

**Side effects:**

1. Создаются run_id и seed.
2. elapsed_seconds = 0, current_wave_band_id = wave_0_2m, checkpoint_id = null.
3. Build получает максимум 6 weapon slots, 6 passive slots и 3 artifact slots.
4. RewardLedger пуст; setup не начисляет награды.
5. Создаётся loading request с content version.

**Result:** RUN_LOADING.

### 5.2 Loading арены

При успехе проверяются spawn position, content refs и готовность RunReadModel, затем отправляется run.started. При ошибке RunSession не считается начатым: Diagnostics предлагает retry или возврат в setup. Частично загруженный run не показывается как успешный.

## 6. Активный забег

После run.started RunSession — source of truth, а RunSimulation обрабатывает movement, auto attacks, enemy lifecycle, drops и wave budget.

Игрок видит:

- HP и состояние героя;
- attack, critical chance, critical multiplier, movement speed, cooldown;
- weapon/passive slots, уровни и эффекты;
- artifacts, eligible и claimed synergies;
- level и XP;
- elapsed time и текущую wave/stage;
- kills;
- bonus/series projection, если правило будет подтверждено;
- checkpoint rewards и уже начисленные ledger entries;
- pause action и diagnostics banner.

Набор полей обязателен, точная раскладка остаётся U-08 / PENDING_PRODUCT_DECISION.

### 6.1 Время и волны

Game clock движется только в RUN_ACTIVE/BOSS_ACTIVE. В PAUSED, UPGRADE_CHOICE и BACKGROUND_SUSPENDED он заморожен.

| Время | ID | Spawn budget | Active cap | HP | Damage | Speed |
|---|---|---:|---:|---:|---:|---:|
| 0–2 мин | wave_0_2m | 6/s | 40 | ×1.00 | ×0.70 | ×0.90 |
| 2–5 мин | wave_2_5m | 10/s | 80 | ×1.10 | ×0.85 | ×1.00 |
| 5–10 мин | wave_5_10m | 15/s | 130 | ×1.35 | ×1.00 | ×1.02 |
| 10–15 мин | wave_10_15m | 22/s | 200 | ×1.70 | ×1.25 | ×1.05 |
| 15–20 мин | wave_15_20m | 30/s | 280 | ×2.20 | ×1.55 | ×1.08 |

Это B1 baseline, а не абсолютные base HP/damage/speed. Абсолютные значения остаются PENDING_B1. При boss spawn обычный spawn budget уменьшается на 8 секунд, затем восстанавливается с 70% до 100% за 20 секунд. Active cap обязателен.

### 6.2 XP и aftermath

- XPItem — collectable drop; меняет XP и может вызвать level-up.
- AftermathItem — визуальный след смерти; не collectible, не collision, не XP и не reward.
- У них разные IDs, слои, pooling и лимиты.
- При переполнении XP items объединяются по value, не удаляются; aftermath деградирует в cluster/decal.
- Kills увеличиваются один раз на authoritative enemy.defeated.

### 6.3 Level-up

При пересечении XP threshold:

1. Simulation clock фиксируется.
2. ProgressionService строит три legal offers, если это подтверждено GAME_MANIFEST.
3. Offer legality проверяет slots, max levels, owned IDs и pending synergy rules.
4. UI показывает offer set, но build меняется только после upgrade.offer_chosen.
5. Invalid/expired offer отклоняется diagnostic code и может быть deterministic regenerated.

Max weapon/passive только делает synergy eligible; evolution применяется через chest.

## 7. Босс, checkpoint и сундук

Боссы появляются на 300, 600, 900 и 1200 seconds:

| Checkpoint | Boss ID |
|---|---|
| 5 мин | hua_lin |
| 10 мин | miyon |
| 15 мин | seika |
| 20 мин | black_moon_empress |

Перед появлением существует telegraph и окно реакции. Boss не появляется внутри player model и не наносит instant damage без telegraph.

После authoritative boss defeat:

1. фиксируется boss.defeated;
2. Reward calculator считает deterministic outcome;
3. RewardLedger записывает checkpoint entry с key checkpoint:{run_id}:{checkpoint_id};
4. повтор того же event возвращает существующий entry;
5. создаётся один ChestOffer;
6. SynergyEvaluator возвращает eligible IDs или fallback;
7. после claim run переходит к следующей logical band.

B1 checkpoint rewards:

| Checkpoint | Gold | Lunar Seals | Boss Essence |
|---|---:|---:|---:|
| 5 мин | 50 | 15 | 1 |
| 10 мин | 75 | 20 | 1 |
| 15 мин | 100 | 25 | 1 |
| 20 мин | 200 | 60 | 2 |
| first clear bonus | 300 | 180 | 1 |

При defeat после checkpoint действует B1 правило: 50% gold checkpoint, 100% уже заработанной Essence, Lunar Seals только за defeated boss. Округление дробного gold и точный fallback outcome не заданы и остаются PENDING_B1/PENDING_PRODUCT_DECISION. Ledger хранит formula/version/resolution status, а не скрытое округление.

Eligibility synergy:

- weapon level = 6;
- related passive level = 5;
- synergy ещё не claimed;
- chest не claimed;
- pair подтверждён registry.

Если eligible candidates есть, игрок выбирает из deterministic list. Иначе создаётся fallback_reward с явным PENDING_PRODUCT_DECISION outcome kind. Закрытие и повторное открытие используют тот же chest_id и outcome.

## 8. Пауза, настройки и Android background

Pause command сначала останавливает clock, затем открывает overlay. Continue возобновляет clock. Settings открываются поверх PAUSED и возвращают в PAUSED. Повторная pause command — idempotent no-op.

На Android background:

1. немедленно freeze simulation;
2. запросить snapshot с reason ANDROID_BACKGROUND;
3. при успехе записать revision/checksum;
4. при ошибке сохранить in-memory session и показать recoverability в Diagnostics;
5. на resume валидировать in-memory session, затем вернуть RUN_ACTIVE/PAUSED.

Если процесс был убит, restore разрешён только для валидного snapshot и принятой policy. Полный mid-run resume не обещается до решений U-06/U-07. Background/resume сам по себе не claim-ит reward.

Выход в меню требует подтверждения:

- остаться: PAUSED → RUN_ACTIVE;
- abandon: закрыть active run без terminal reward claim;
- восстановить checkpoint: только при валидном snapshot и принятой policy.

## 9. Смерть и победа

### 9.1 Defeat

При authoritative HP ≤ 0 clock останавливается, строится immutable ResultSnapshot, начисляются только допустимые partial rewards, state становится terminal DEFEAT. Незавершённый chest не claim-ится автоматически.

Partial rule: already earned Essence, seals только за defeated boss, gold по B1 checkpoint formula. Duplicate run.death возвращает первый result и не повторяет grants.

### 9.2 Victory

Финальный boss defeat и final victory check переводят run в VICTORY. Записываются 20m checkpoint reward и отдельный first-clear bonus, если это первый полный clear. ResultSnapshot immutable. Победа не объявляется одним таймером без финального boss, пока canonical contract не изменён.

### 9.3 Result

Result screen показывает outcome, elapsed time, checkpoints, kills, build, levels, stats summary, XP/level, earned/claimed rewards, chest/synergy/artifact outcome и diagnostics. Точная презентация stats остаётся U-08.

«Забрать награды» вызывает ledger claim/replay. Повторный claim возвращает исходную receipt, а не создаёт новую выдачу. Повторное открытие result — read-only. После claim доступен возврат в меню и новый run.

## 10. Prototype и target

| Текущий evidence | Подтверждает | Не подтверждает |
|---|---|---|
| scripts/menu/menu_controller.gd | menu routes, loading delay, placeholder result routes | selected hero, RunSession, save, rewards |
| scripts/arena/arena_controller.gd | visual arena preview, 390×844, accelerated 20-minute preview | movement, combat, waves, XP, HUD, bosses, persistence |
| project.godot | Godot project, main menu, 390×844 viewport | runtime readiness |
| archived/mockups | visual candidate/evidence | approved runtime assets |

Этот пакет не импортирует и не создаёт PNG/SVG/TSCN/GDScript. Runtime-агент сначала использует stubs и neutral controls.

## 11. Flow checks

Следующий агент должен доказать:

1. Каждый transition имеет command/event и owner.
2. Повтор checkpoint/chest/result event не меняет balance.
3. XP pickup не создаёт aftermath, aftermath не повышает XP.
4. Pause/background не продвигают elapsed time.
5. Invalid content/save попадает в Diagnostics, а не в белый экран.
6. До отдельного approval assets используются только как stubs/placeholders.
