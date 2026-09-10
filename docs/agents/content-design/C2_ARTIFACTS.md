# C2 — Артефакты первого забега

Статус пакета: `CONTENT_SPECIFIED`

Это каталог контентных эффектов и handoff для Balance, Runtime и Visual Lab. Артефакт не занимает weapon/passive slot, не является pre-run loadout и не меняет состав десяти оружий или десяти run-пассивок. Все значения cadence, damage, duration, radius, threshold, rarity, refresh и stacking передаются как `PENDING_BALANCE` или `PENDING_PRODUCT_DECISION`.

## 1. Роль артефактов

Артефакт должен давать игроку короткое читаемое правило: «если я делаю X, мир отвечает Y». Он меняет маршрут забега, приоритет цели или геометрию следующего действия, а не просто добавляет ещё один безусловный процент к стату.

| Контракт | Решение для Run 1 |
|---|---|
| Каталог | 10 артефактов |
| Источник в забеге | `ELITE_PACK` — предложение после elite-пика; `FIRST_CLEAR_REWARD` — отдельная награда после первого прохождения, scope ещё требует решения |
| Offer | ровно 3 candidate IDs, выбран ровно 1; refresh и его цена — `PENDING_PRODUCT_DECISION` |
| Слоты | отдельный слой, не расходует 6 weapon slots и 6 passive slots |
| Pre-run loadout | запрещён текущим архитектурным контрактом; артефакт приходит через offer во время забега |
| Capacity | `UNBOUNDED_WITHIN_RUN` до решения о повторном экземпляре/stacking |
| Дубликат | не считать новым эффектом автоматически; conversion/upgrade policy — `PENDING_PRODUCT_DECISION` |
| Обратная связь | карта offer, подтверждение выбора, combat telegraph, запись в pause/stat projection |
| Валюта между забегами | `Boss Essence` может использоваться для Codex unlock; цена и persistent ownership — `PENDING_BALANCE`/`PENDING_PRODUCT_DECISION` |

`FIRST_CLEAR_REWARD` не должен молча становиться активным эффектом в уже завершившемся забеге. Рекомендуемый scope — unlock в Artifact Codex для будущих offers; окончательное решение принадлежит Product/Architecture.

## 2. Каталог десяти артефактов

| artifact_id | Рабочее имя | Effect family | Trigger | Выбор игрока |
|---|---|---|---|---|
| `artifact_jade_compass` | Нефритовый компас | `AURA` | сбор arena drop | забрать drop сейчас и создать поле маршрутизации или обойти риск |
| `artifact_mirror_shard` | Грань зеркала | `TRIGGERED_EFFECT` | критический удар | играть через крит-связку и принять задержанный echo |
| `artifact_phoenix_feather` | Перо феникса | `TRIGGERED_EFFECT` | убийство elite | вести врагов через огненный след возрождения |
| `artifact_frost_bead` | Ледяная бусина | `WEAPON_MODIFIER` | наложение slow/freeze | удерживать контролируемую цель для следующего bloom |
| `artifact_bell_fragment` | Осколок колокола | `TRIGGERED_EFFECT` | защищённый/полученный удар | допустить контролируемый риск ради резонанса |
| `artifact_lotus_seed` | Семя лотоса | `TRIGGERED_EFFECT` | overheal/full-health heal | сохранить здоровье и превратить лечение в защитный ресурс |
| `artifact_moon_crown` | Лунная корона | `TARGET_MODIFIER` | начало boss phase | пережить telegraph и ударить в короткое окно метки |
| `artifact_black_bead` | Чёрная бусина | `WEAPON_MODIFIER` | попадание по elite | менять между pull и burst для последнего оружия |
| `artifact_tideglass` | Приливное стекло | `AURA` | сбор arena drop | прокладывать путь между drop и героем, меняя движение толпы |
| `artifact_silent_lantern` | Безмолвный фонарь | `TARGET_MODIFIER` | выбор elite/high-threat target | видеть угрозу заранее, но самому уклоняться от telegraph |

Имена и IDs сохраняют существующие восемь архитектурных IDs; `artifact_tideglass` и `artifact_silent_lantern` — две новые content proposals, требующие синхронизации Registry.

## 3. Artifact entries

### 3.1 `artifact_jade_compass` — Нефритовый компас

- **Фантазия:** компас не показывает север — он находит безопасную линию через живую толпу.
- **Обещание игроку:** подобранный drop превращает точку подбора в краткую нефритовую зону, которая мягко меняет поток ближайших врагов и подчёркивает путь к следующей награде.
- **Effect family:** `AURA`; scope `RUN`.
- **Trigger:** `on_arena_drop_collected`; один drop создаёт один instance поля.
- **Target:** враги в поле и путь движения вокруг точки подбора; не геройские статы напрямую.
- **Observable effect:** враги слегка смещают маршрут к краю/от безопасного центра по заданному правилу; pickup остаётся видимым и собираемым.
- **Player decision:** идти к drop ради контроля пространства сейчас или сохранить безопасную позицию и отказаться от поля.
- **Trade-off/counterplay:** поле не убивает, не останавливает boss и не проходит сквозь стены; плотный pack может всё равно продавить край зоны.
- **Synergy hooks:** усиливает пространственный рисунок `weapon_lotus_mines`, `weapon_black_eclipse_umbrella` и `weapon_moon_blade`, но не считается их passive или synergy.
- **Text contract:** «Собранный предмет оставляет нефритовый компас: поле меняет путь ближайших врагов.»
- **VFX brief:** нефритовая стрелка, тонкое кольцо направлений, мягкие линии маршрута; deep blue-grey/smoky teal base, muted jade accent, без neon.
- **Audio/haptic:** тихий металлический щелчок направления; короткий мягкий pulse при создании поля.
- **Balance placeholders:** размер поля, время жизни, сила displacement, drop whitelist — `PENDING_BALANCE`.
- **Runtime contract:** `ArtifactEffectSystem` слушает pickup-событие и создаёт tagged aura; effect source должен удаляться по expiry/run end.
- **Status:** `PROPOSAL`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.

### 3.2 `artifact_mirror_shard` — Грань зеркала

- **Naming note:** ID совпадает с `passive_mirror_shard`; это разные namespaces: artifact `artifact_mirror_shard`, run passive `passive_mirror_shard`. UI обязан показывать family badge «Артефакт»/«Пассивка».
- **Фантазия:** осколок запоминает не весь удар, а его отражённую возможность.
- **Обещание игроку:** критический hit создаёт отложенный зеркальный echo последнего допустимого weapon hit по той же зоне.
- **Effect family:** `TRIGGERED_EFFECT`; scope `RUN`.
- **Trigger:** `on_critical_weapon_hit`; один trigger на один eligible hit event.
- **Target:** тот же target или ближайшая valid target zone, если исходная цель исчезла.
- **Observable effect:** echo повторяет форму/направление исходного weapon hit с отдельным таймингом и меньшей силой, пока source ещё читаем.
- **Player decision:** собирать crit и удерживать дистанцию до echo или выбирать обычный стабильный damage path.
- **Trade-off/counterplay:** echo не создаёт новый echo, не копирует synergy финального удара автоматически и не срабатывает от собственного отражения.
- **Synergy hooks:** особенно заметен с `passive_star_compass`, `passive_frost_thread` и `weapon_star_bow`; не должен удваивать весь global crit multiplier.
- **Text contract:** «Критический удар оставляет отложенное зеркальное отражение последнего удара.»
- **VFX brief:** тонкая тёплая ivory-грань, смещённый силуэт projectile, muted violet только как редкий status accent.
- **Audio/haptic:** стеклянный high ping при crit; echo — приглушённый обратный тон.
- **Balance placeholders:** echo delay, coefficient, eligible weapon tags, internal cooldown, boss behavior — `PENDING_BALANCE`.
- **Runtime contract:** нужен `source_event_id`/echo guard, чтобы не допустить recursive trigger и double-apply после replay.
- **Status:** `PROPOSAL`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.

### 3.3 `artifact_phoenix_feather` — Перо феникса

- **Фантазия:** перо вспыхивает не при смерти героя, а при падении сильного врага.
- **Обещание игроку:** убийство elite прокладывает огненный маршрут от места падения через ближайшую плотную группу.
- **Effect family:** `TRIGGERED_EFFECT`; scope `RUN`.
- **Trigger:** `on_elite_defeated`; один phoenix path на один eligible elite defeat.
- **Target:** враги, пересекающие путь; сам elite corpse не должен повторно триггерить эффект.
- **Observable effect:** полоса углей появляется поэтапно, затем коротко горит и закрывается; направление определяется от death point к threat cluster.
- **Player decision:** вести pack вдоль линии, чтобы получить повторные пересечения, или отойти от опасного маршрута.
- **Trade-off/counterplay:** path телеграфируется, не следует за героем бесконечно, не создаётся от обычных minions и не возрождает elite.
- **Synergy hooks:** естественно поддерживает `passive_ember_heart`, `weapon_crimson_flame_fan` и `synergy_phoenix_sky`, но не должен автоматически выдавать их evolution.
- **Text contract:** «После убийства элитного врага из его следа вырывается огненный путь.»
- **VFX brief:** перо как короткий ivory-to-crimson spark; огонь — muted crimson/amber accent внутри smoky base, без токсичного orange glow.
- **Audio/haptic:** сухой взмах пера, затем низкий ember rumble; единый hit pulse на пересечение.
- **Balance placeholders:** path length, width, burn duration, damage, elite cooldown and pack target rule — `PENDING_BALANCE`.
- **Runtime contract:** effect receives `elite_id`, `death_position`, `run_id`; path must be deterministic under replay and clean on run end.
- **Status:** `PROPOSAL`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.

### 3.4 `artifact_frost_bead` — Ледяная бусина

- **Фантазия:** бусина удерживает один момент холода, чтобы следующий удар раскрыл его.
- **Обещание игроку:** после наложения slow/freeze следующий hit по этой цели создаёт frost bloom вокруг impact.
- **Effect family:** `WEAPON_MODIFIER`; scope `RUN`.
- **Trigger:** `on_control_applied` с condition `slow_or_freeze`; состояние хранит одну цель/один pending bloom.
- **Target:** controlled target и соседняя valid area вокруг него.
- **Observable effect:** на цели видна ледяная метка; первый eligible hit consumes mark и создаёт ring, после чего метка исчезает.
- **Player decision:** не спешить с первым ударом, чтобы собрать более выгодный control-to-bloom момент.
- **Trade-off/counterplay:** метка истекает, не складывается бесконечно, не превращает boss в permanently frozen target; immunity/resistance должен быть видим.
- **Synergy hooks:** связывает `weapon_frost_pearl`, `passive_frost_thread`, `weapon_thunder_needles` через target-control, но не меняет synergy eligibility.
- **Text contract:** «Замедленный враг получает ледяную метку. Следующий удар раскрывает морозное кольцо.»
- **VFX brief:** одна холодная bead outline, radial frost ring и короткие cracks; smoky teal/ivory, холодный jade-blue accent.
- **Audio/haptic:** bead tick при control, мягкий crystalline burst при consume.
- **Balance placeholders:** mark duration, bloom radius/coefficient, eligible hit tags, boss resistance, internal cooldown — `PENDING_BALANCE`.
- **Runtime contract:** control source and consuming hit must be separate events; consume is idempotent by target state revision.
- **Status:** `PROPOSAL`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.

### 3.5 `artifact_bell_fragment` — Осколок колокола

- **Фантазия:** треснувший колокол звучит сильнее, когда удар проходит рядом.
- **Обещание игроку:** полученный или успешно смягчённый hit накапливает resonance и выпускает защитный pulse.
- **Effect family:** `TRIGGERED_EFFECT`; scope `RUN`.
- **Trigger:** `on_damage_taken_or_guarded_hit`; exact guard/damage boundary — `PENDING_ARCHITECTURE`.
- **Target:** nearby enemies and incoming threat field; hero receives only the artifact’s bounded response.
- **Observable effect:** resonance ring visibly fills; threshold event emits knockback/interruption pulse and resets/consumes charge.
- **Player decision:** принять небольшой контролируемый hit или играть идеально ради более редкого, но сильного резонанса.
- **Trade-off/counterplay:** pulse не даёт бессмертия, не отменяет уже landed damage, не бесконечен и не должен permanently lock boss.
- **Synergy hooks:** поддерживает `passive_iron_bell`, `weapon_spirit_bell`, `synergy_guardian_bell`; не дублирует их exact shield values.
- **Text contract:** «Смягчённый удар наполняет осколок. Полный звон отбрасывает врагов вокруг.»
- **VFX brief:** broken bell silhouette, segmented warm ivory resonance ring, muted brass impact; no large opaque shield mockup.
- **Audio/haptic:** один dry chime per charge, lower bell hit on pulse; damage feedback remains distinct.
- **Balance placeholders:** charge threshold, mitigation definition, pulse radius, knockback/interruption, boss rules — `PENDING_BALANCE`.
- **Runtime contract:** consumes post-mitigation damage/guard result, never listens to raw contact twice; needs stable trigger dedupe key.
- **Status:** `PROPOSAL`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.

### 3.6 `artifact_lotus_seed` — Семя лотоса

- **Фантазия:** семя раскрывается только там, где жизнь уже не нужна для срочного лечения.
- **Обещание игроку:** healing while at full health или approved overheal создаёт маленький petal ward на следующую опасную атаку.
- **Effect family:** `TRIGGERED_EFFECT`; scope `RUN`.
- **Trigger:** `on_full_health_heal` or `on_overheal`; exact source whitelist — `PENDING_PRODUCT_DECISION`.
- **Target:** hero and next clearly telegraphed incoming hit; no enemy damage by default.
- **Observable effect:** petal charge appears near the hero; it is consumed by the next eligible hit and softens/shortens its consequence.
- **Player decision:** собирать healing mote в момент полного здоровья или игнорировать его ради позиции.
- **Trade-off/counterplay:** ward не должен стать скрытой второй полосой HP; не поглощает every-hit hazard/instant death without explicit decision; expires between runs and by time limit.
- **Synergy hooks:** supports `passive_lotus_heart`, `weapon_lotus_mines`, `synergy_lotus_sanctuary`, plus healing/pickup tree nodes.
- **Text contract:** «Лечение при полном здоровье раскрывает лепестковый оберег для следующего telegraph.»
- **VFX brief:** one lotus petal halo, soft ivory/jade, readable at 390×844 without hiding enemy telegraphs.
- **Audio/haptic:** muted petal chime on arm, soft damped impact on consume.
- **Balance placeholders:** ward strength, duration, source whitelist, hazard whitelist, full-health epsilon — `PENDING_BALANCE`.
- **Runtime contract:** receives healing result after actual health cap; must not trigger from its own mitigation or from passive preview values.
- **Status:** `PROPOSAL`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.

### 3.7 `artifact_moon_crown` — Лунная корона

- **Фантазия:** корона отмечает не босса целиком, а его следующий перелом ритма.
- **Обещание игроку:** начало boss phase создаёт lunar seal; после пережитого telegraph следующая valid damage window по boss становится усиленной/более читаемой.
- **Effect family:** `TARGET_MODIFIER`; scope `RUN`.
- **Trigger:** `on_boss_phase_started`; once per eligible phase, with final behavior pending.
- **Target:** current boss phase target only.
- **Observable effect:** crown mark attaches to phase indicator; it changes state after the phase telegraph resolves, not immediately on spawn.
- **Player decision:** сначала прочитать и пережить pattern, затем вложить cooldown/crit/evolution в окно метки.
- **Trade-off/counterplay:** корона не пропускает phase, не отключает boss mechanics, не даёт пассивного урона вне окна; missed window expires visibly.
- **Synergy hooks:** rewards deliberate timing for `weapon_star_bow`, `weapon_jade_talismans`, `synergy_heavenly_judgment`, `synergy_constellation_rain`.
- **Text contract:** «В начале фазы отмечает следующее безопасное окно для удара по боссу.»
- **VFX brief:** restrained lunar crown arc over boss phase marker; warm ivory line + smoky teal shadow, no full-screen flash.
- **Audio/haptic:** low two-note phase cue, brighter resolve note when window opens.
- **Balance placeholders:** phase whitelist, window duration, effect coefficient, missed-window rule, final boss behavior — `PENDING_BALANCE`.
- **Runtime contract:** binds to `boss_id` + `phase_id`; must consume only after phase/telegraph state is authoritative and replay-safe.
- **Status:** `PROPOSAL`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.

### 3.8 `artifact_black_bead` — Чёрная бусина

- **Фантазия:** бусина вращает полярность последнего сильного удара.
- **Обещание игроку:** после hit по elite последнее оружие получает чередующийся режим: pull для сборки pack или burst для его разрыва.
- **Effect family:** `WEAPON_MODIFIER`; scope `RUN`.
- **Trigger:** `on_elite_weapon_hit`; mode alternates only on a valid elite interaction.
- **Target:** elite target, nearby enemies and the weapon source that produced the hit.
- **Observable effect:** small black bead orbit changes orientation; next eligible weapon event shows `PULL`/`BURST` state before resolution.
- **Player decision:** сознательно оставить elite рядом для pull или дождаться burst, выбирая порядок оружейных hits.
- **Trade-off/counterplay:** только последнее valid weapon source, без глобального переключения всех weapons; no wall pull, no recursive proc, boss immunity/resistance visible.
- **Synergy hooks:** creates a timing layer around `weapon_black_eclipse_umbrella`, `weapon_fox_mirage`, `weapon_lotus_mines`; never counts as a synergy claim.
- **Text contract:** «Удар по элитному врагу чередует полярность последнего оружия: притянуть, затем разорвать строй.»
- **VFX brief:** matte black bead with a thin muted brass orbit; pull is inward line, burst is outward ring; no black-on-black loss.
- **Audio/haptic:** inward low tick for pull, dry outward click for burst.
- **Balance placeholders:** mode coefficient, alternation reset, valid source tags, radius, boss rules, elite immunity — `PENDING_BALANCE`.
- **Runtime contract:** stores `last_eligible_weapon_id` per artifact instance; effect must be deterministic and not alter `SynergyEvaluator`.
- **Status:** `PROPOSAL`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.

### 3.9 `artifact_tideglass` — Приливное стекло

- **Registry status:** новая content proposal; не добавлять в runtime Registry до согласования Architecture/Balance.
- **Фантазия:** стекло запоминает путь между добычей и героем, как маленький прилив.
- **Обещание игроку:** pickup создаёт короткую tide path от точки drop к текущей позиции героя; враги, пересекающие путь, смещаются/замедляются.
- **Effect family:** `AURA`; scope `RUN`.
- **Trigger:** `on_arena_drop_collected`; path is a snapshot, not a permanent tether.
- **Target:** enemies crossing the path; hero and XP/drop values remain unchanged.
- **Observable effect:** path draws in two beats from drop point to hero, then fades; crossing enemies receive one visible displacement/slow response.
- **Player decision:** выбирать pickup route, чтобы пересечь и разрезать pack, или забрать drop с безопасной стороны.
- **Trade-off/counterplay:** path не тянет предметы, не проходит сквозь стены, не меняет XP amount и не становится permanent arena wall.
- **Synergy hooks:** geometrically supports `weapon_moon_blade`, `weapon_lotus_mines`, `weapon_black_eclipse_umbrella` without granting their damage or evolution.
- **Text contract:** «Подбор предмета оставляет приливный путь от него к герою.»
- **VFX brief:** translucent smoky teal ribbon with warm ivory edges and a glass glint; subtle enough not to compete with spell telegraphs.
- **Audio/haptic:** soft water-glass sweep; one tactile pulse on first enemy crossing, no looped rumble.
- **Balance placeholders:** path duration, width, displacement/slow, drop whitelist, wall interaction — `PENDING_BALANCE`.
- **Runtime contract:** new artifact ID must be added to Registry only with schema and effect mapping; path uses run seed/state revision for replay.
- **Status:** `PROPOSAL`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.

### 3.10 `artifact_silent_lantern` — Безмолвный фонарь

- **Registry status:** новая content proposal; не добавлять в runtime Registry до согласования Architecture/Balance.
- **Фантазия:** фонарь освещает не врага, а момент, в который он собирается стать угрозой.
- **Обещание игроку:** при выборе elite/high-threat target отмечает самого опасного врага и раскрывает его следующий telegraph.
- **Effect family:** `TARGET_MODIFIER`; scope `RUN`.
- **Trigger:** `on_elite_or_high_threat_target_selected`; target selector and threat score contract — `PENDING_ARCHITECTURE`.
- **Target:** one current highest-threat enemy; tie-break must be deterministic.
- **Observable effect:** lantern mark displays target and a compact preview of its next attack timing/shape; it does not cancel or weaken telegraph by default.
- **Player decision:** использовать информацию, чтобы строить позицию/каст, или продолжить damage race и принять раскрытый риск.
- **Trade-off/counterplay:** только один target одновременно, preview не видит за стенами, не останавливает projectile и не превращает boss into harmless dummy.
- **Synergy hooks:** improves decision quality for `weapon_jade_talismans`, `weapon_star_bow`, `synergy_heavenly_seals`, `synergy_constellation_rain`; no direct synergy eligibility.
- **Text contract:** «Безмолвный фонарь отмечает главную угрозу и показывает её следующий telegraph.»
- **VFX brief:** small warm-ivory lantern glyph, restrained line preview in smoky teal; no full HUD mockup and no false precision.
- **Audio/haptic:** almost silent click on target change; distinct soft cue only when preview becomes available.
- **Balance placeholders:** threat selector, preview lead time, preview fidelity, elite/boss eligibility, refresh timing — `PENDING_BALANCE`/`PENDING_ARCHITECTURE`.
- **Runtime contract:** consumes authoritative telegraph projection, never predicts from client-only animation; target changes must be replay-safe and observable.
- **Status:** `PROPOSAL`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.

## 4. Offer, stacking и readable failure states

### 4.1 Offer contract

Каждый offer отображает три distinct candidate IDs, family tag, trigger, player-facing promise, trade-off и источник получения. `artifact_offer_created.v1` должен сохранить ровно три candidate IDs; `artifact_chosen.v1` — один выбранный ID. Refresh не должен создавать четвёртую скрытую карту или менять уже выбранный artifact.

### 4.2 Stacking contract

До отдельного решения нельзя считать одинаковые artifacts бесконечно складывающимися. Для каждого ID Balance/Product выбирает один из режимов:

- `UNIQUE`: второй экземпляр превращается в approved fallback;
- `STACKABLE`: повтор усиливает один заранее названный parameter;
- `UPGRADE`: повтор повышает ранг Codex/run effect по отдельной шкале.

Текущий контентный proposal по умолчанию — `UNIQUE`, кроме случаев, где Product явно выберет другой режим. Артефакты не должны молча складываться с одноимёнными run passives: одинаковая тема не означает общий stack bucket.

### 4.3 Readable failure states

UI copy должен использовать понятные состояния: `Уже получен`, `Недоступно в этом источнике`, `Выберите один артефакт`, `Обновление недоступно`, `Эффект проявится в забеге`. Preview не должен показывать точные числа до того, как Balance закрепит их в Registry.

## 4.4 Content-owned default policy

Ниже зафиксированы только семантические defaults Content Agent. Они не задают цену, частоту, коэффициенты, schema implementation или save format.

| Rule | Content default for Run 1 |
|---|---|
| Refresh | Разрешён только до выбора карты; каждый refresh снова показывает ровно 3 distinct candidate IDs; refresh не создаёт скрытую четвёртую карту и не меняет уже выбранный artifact |
| Duplicate | Все 10 артефактов по умолчанию UNIQUE; повторный ID не активирует второй instance |
| Duplicate outcome | Повтор получает outcome key artifact_duplicate_fallback и передаётся в approved fallback pool; тип ресурса и количество задаёт Balance/Product |
| Cross-theme stacking | Одинаковая тема с run-passive или weapon не означает общий stack bucket; artifact не меняет synergy eligibility |
| Effect scope | Каждый artifact effect имеет один authoritative trigger, target whitelist, cleanup boundary и source event; recursive self-trigger запрещён |
| Offer selection | Один offer выбирает максимум один artifact; preview/refresh не считаются obtained |
| First-clear | FIRST_CLEAR_REWARD по умолчанию открывает artifact в Codex для будущих offers; активный run effect без отдельного offer запрещён |

### 4.5 Canonical semantic effect keys

Эти keys закрывают content-часть typed effect mapping. Architecture всё ещё должна создать runtime definitions и guards, а Balance — привязать численные параметры.

| artifact_id | semantic effect key | Trigger / target boundary |
|---|---|---|
| artifact_jade_compass | aura.drop_route_compass | arena drop collected / nearby enemies and route |
| artifact_mirror_shard | trigger.critical_echo | critical weapon hit / source hit zone |
| artifact_phoenix_feather | trigger.elite_ember_path | elite defeated / enemies crossing path |
| artifact_frost_bead | modifier.control_bloom | slow or freeze applied / controlled target and nearby area |
| artifact_bell_fragment | trigger.guard_resonance | post-mitigation guarded hit / nearby threats |
| artifact_lotus_seed | trigger.overheal_ward | full-health heal or overheal / next eligible incoming hit |
| artifact_moon_crown | target.boss_phase_window | boss phase started / current boss phase |
| artifact_black_bead | modifier.elite_polarity | eligible elite weapon hit / last eligible weapon source |
| artifact_tideglass | aura.drop_tide_path | arena drop collected / enemies crossing snapshot path |
| artifact_silent_lantern | target.threat_telegraph | elite/high-threat target selected / one current threat |

Для каждого key обязательны source event, target whitelist, cleanup/expiry, recursion guard и replay identity. Exact coefficients, cooldowns, durations, radii, rarity, source cadence и performance budgets остаются PENDING_BALANCE/PENDING_ARCHITECTURE.

## 5. Visual Lab handoff — brief only

Мокапы, PNG/SVG, production icons и final VFX **не создаются этим пакетом**.

| Поле | Значение |
|---|---|
| route | `SPRITE` для icon/origin, `VFX` для trigger response, `UI_ART` для offer card/state |
| stage_path | `docs/mockups/08-artifacts/` для artifact identity, `docs/mockups/17-artifact-ui/` для offer/codex UI |
| asset_id / family_id / candidate_id | `null` до Visual Lab intake; IDs не выдумываются content agent |
| status | `PROPOSAL` |
| technical_status | `NOT_RUN` |
| artistic_status | `PENDING` |
| manifest / consumer | `NOT_PROMOTED`; consumer — Content Registry / ArtifactEffectSystem / UI projection |
| visual code | deep blue-grey, smoky teal, warm ivory, muted brass, soft jade; crimson/violet only role/status accent |
| acceptance cue | effect readable by silhouette, trigger icon and telegraph timing at 390×844; no toxic/neon glow |

Visual Lab получает artifact brief после того, как Architecture подтвердит два новых IDs и effect family schema. До этого candidate IDs остаются пустыми.

## 6. Open decisions

- значения effect coefficient, cooldown, duration, radius и threshold для всех десяти IDs — `PENDING_BALANCE`;
- source cadence/composition для `ELITE_PACK`, rarity и повторный offer — `PENDING_BALANCE`/`PENDING_PRODUCT_DECISION`;
- refresh cost/limit и fallback value для `artifact_duplicate_fallback` — `PENDING_PRODUCT_DECISION`/`PENDING_BALANCE`; content defaults уже зафиксированы в разделе 4.4;
- scope `FIRST_CLEAR_REWARD`: Codex unlock или активный effect до следующего забега — `PENDING_ARCHITECTURE`;
- canonical runtime schema для десяти semantic effect keys и trigger guards — `PENDING_ARCHITECTURE`; content mapping зафиксирован в разделе 4.5;
- status/preview для boss phase у `artifact_moon_crown` — `PENDING_BALANCE`;
- точная граница `on_damage_taken_or_guarded_hit` у `artifact_bell_fragment` — `PENDING_ARCHITECTURE`;
- threat selector и source telegraph projection для `artifact_silent_lantern` — `PENDING_ARCHITECTURE`.

