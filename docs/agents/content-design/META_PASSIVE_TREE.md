# META — Полное постоянное дерево пассивок магазина

Статус пакета: `CONTENT_SPECIFIED`

Это дизайн магазина между забегами. Узлы дерева постоянны, покупаются за Gold и применяются со следующего забега. Они не занимают шесть временных passive slots, не появляются в upgrade offer и не должны смешиваться с десятью `passive_*` из `C1_WEAPONS_PASSIVES_SYNERGIES.md`.

## 1. Цель и границы

Дерево переводит все характеристики, видимые на pause/stat screen, в понятную долгосрочную прогрессию. Каждый узел отвечает за один stat axis, имеет собственный tooltip и принадлежит одной из шести тематических ветвей.

| Слой | Назначение | Lifetime | Валюта |
|---|---|---|---|
| Run passive | тактический модификатор билда | один забег | XP/upgrade offer |
| Meta tree node | постоянное изменение базовой характеристики | между забегами | Gold |
| Artifact Codex | открытие/состояние artifact catalogue | между забегами; точный scope pending | Boss Essence |

Визуальный пример пользователя использован как reference для списка характеристик, но этот документ не создаёт и не заменяет экран, мокап, иконку или финальный asset.

## 2. Макроархитектура дерева

Текущий B1 balance contract задаёт шесть макро-ветвей по 10 branch ranks и формулу цены следующего rank `round(100 × 1.45^rank)`, где первый rank стоит 100 Gold. Сохраняем эту экономическую оболочку и раскладываем её на 17 видимых stat nodes. Как именно распределяется 10-rank budget ветви между дочерними узлами, закрепляет Balance Agent; content не подменяет его числами.

| branch_id | Ветка | Основная фантазия | Дочерний путь |
|---|---|---|---|
| `meta_vitality` | Живучесть | пережить ещё одну ошибку и восстановиться | max HP → regen → healing mote |
| `meta_force` | Сила | сделать каждый spell/weapon hit весомее | attack power → attack multiplier → magic damage |
| `meta_agility` | Проворство | управлять расстоянием и окном критического удара | move speed → evasion → crit chance → crit power |
| `meta_focus` | Фокус | получать больше времени и формы из одного каста | cooldown → duration → size |
| `meta_magnet` | Магнит | не терять ресурс из-за опасного маршрута | pickup radius → mana/XP gain |
| `meta_defense` | Защита | смягчать контакт и снижать давление толпы | damage taken → enemy max HP |

### Прогрессия ветвей

- `branch_rank` — агрегированный прогресс ветви, максимум 10 покупок по B1 contract.
- `node_rank` — прогресс конкретного stat node; рабочее предложение — до 5 ступеней на node, но это `PENDING_BALANCE`.
- Покупка дочернего узла требует предыдущий узел пути и минимальный branch rank; точные пороги — `PENDING_PRODUCT_DECISION`.
- При открытых нескольких путях игрок выбирает, куда направить следующий branch budget. Дерево не должно автоматически покупать соседний узел.
- Значения, проценты, округление и порядок применения идут из единого Balance/StatsCalculator источника; здесь зафиксированы только оси, зависимости и семантика.

## 3. Полный список 17 stat nodes

### 3.1 Ветка `meta_vitality` — Живучесть

#### `meta_vitality_max_hp` — Здоровье

- **Stat key:** `max_hp`.
- **Player promise:** увеличивает максимальное здоровье героя и размер health bar.
- **Path role:** root node; открывает восстановление.
- **Affects:** hero max HP, starting/current HP normalization between runs — правило текущего HP после покупки требует Runtime confirmation.
- **Does not affect:** damage, healing rate, temporary ward/artifact shields.
- **UI copy:** «Увеличивает максимальное здоровье.»
- **Dependency:** branch root `meta_vitality`; cost from branch rank formula.
- **Balance:** amount per node rank and branch budget `PENDING_BALANCE`.

#### `meta_vitality_regen` — Исцеление в сек

- **Stat key:** `regen_per_second`.
- **Player promise:** восстанавливает здоровье постепенно в течение забега.
- **Path role:** second node after `meta_vitality_max_hp`.
- **Affects:** continuous hero healing tick; must clamp at max HP.
- **Does not affect:** healing mote value, artifact ward strength, revive.
- **UI copy:** «Увеличивает постоянное исцеление в секунду.»
- **Dependency:** max HP node + branch gate; exact gate `PENDING_PRODUCT_DECISION`.
- **Balance:** base unit, tick cadence and amount per rank `PENDING_BALANCE`.

#### `meta_vitality_mote_healing` — Исцеление от крупицы

- **Stat key:** `healing_mote_value`.
- **Player promise:** отдельная healing mote восстанавливает больше здоровья при подборе.
- **Path role:** capstone utility node of vitality route.
- **Affects:** only a pickup tagged `HEALING_MOTE`; does not silently change XP/mana.
- **Does not affect:** normal arena drops, passive regen, lotus artifact’s ward.
- **UI copy:** «Увеличивает исцеление от крупицы.»
- **Dependency:** `meta_vitality_regen` plus pickup/magnet root cross-gate; gate semantics `PENDING_PRODUCT_DECISION`.
- **Balance:** mote value, source tag and pickup cap `PENDING_BALANCE`.

### 3.2 Ветка `meta_force` — Сила

#### `meta_force_attack_power` — Сила атаки

- **Stat key:** `attack_power`.
- **Player promise:** добавляет базовую силу попадания оружия.
- **Path role:** root damage node.
- **Affects:** sources tagged `ATTACK_POWER`; flat contribution is resolved before multipliers.
- **Does not affect:** pickup, cooldown, enemy HP or pure UI preview.
- **UI copy:** «Увеличивает базовую силу атаки.»
- **Dependency:** branch root `meta_force`.
- **Balance:** flat unit and tagged source list `PENDING_BALANCE`.

#### `meta_force_attack_multiplier` — Приумножение атаки

- **Stat key:** `attack_multiplier`.
- **Player promise:** умножает итоговую силу eligible weapon/attack source после flat power.
- **Path role:** second node; communicates the difference between flat strength and multiplicative scaling.
- **Affects:** tagged attack damage after additive contributions.
- **Does not affect:** spell duration/size, critical power, artifact trigger coefficient unless explicitly tagged.
- **UI copy:** «Умножает силу атаки после базового усиления.»
- **Dependency:** `meta_force_attack_power` + branch gate.
- **Balance:** stacking order, cap and amount per rank `PENDING_BALANCE`.

#### `meta_force_magic_damage` — Весь магический урон

- **Stat key:** `all_magic_damage`.
- **Player promise:** усиливает все damage sources, помеченные `MAGIC`, включая spell/projectile effects, но не physical-only effects.
- **Path role:** magic specialization/capstone.
- **Affects:** MAGIC tagged weapon, synergy and eligible artifact damage; tag ownership must be explicit.
- **Does not affect:** knockback, pull, healing, pickup yield, enemy max HP.
- **UI copy:** «Увеличивает весь магический урон.»
- **Dependency:** `meta_force_attack_multiplier` + `meta_focus` root cross-gate.
- **Balance:** tag list, order with attack multiplier and cap `PENDING_BALANCE`.

### 3.3 Ветка `meta_agility` — Проворство

#### `meta_agility_move_speed` — Скорость движения

- **Stat key:** `move_speed`.
- **Player promise:** герой быстрее меняет позицию и проходит между telegraphs.
- **Path role:** root mobility node.
- **Affects:** hero locomotion only; does not accelerate enemy or projectile simulation.
- **Does not affect:** cooldown, attack cadence, pickup magnet speed.
- **UI copy:** «Увеличивает скорость движения.»
- **Dependency:** branch root `meta_agility`.
- **Balance:** additive/multiplicative order and movement cap `PENDING_BALANCE`.

#### `meta_agility_evasion` — Уклонение

- **Stat key:** `evasion_chance`.
- **Player promise:** часть eligible incoming hits может быть полностью избежана по правилам combat.
- **Path role:** defensive mobility node after move speed.
- **Affects:** eligible direct damage hits only; result must be visible and deterministic.
- **Does not affect:** unavoidable hazard, telegraph information, healing or shield.
- **UI copy:** «Даёт шанс уклониться от допустимого попадания.»
- **Dependency:** `meta_agility_move_speed` + branch gate.
- **Balance:** eligible hit list, roll timing, cap and feedback `PENDING_BALANCE`.

#### `meta_agility_crit_chance` — Шанс крит. удара

- **Stat key:** `crit_chance`.
- **Player promise:** eligible weapon hit иногда становится критическим и включает crit feedback.
- **Path role:** offensive precision node.
- **Affects:** sources tagged `CAN_CRIT`; one hit rolls once, not per secondary target unless source says so.
- **Does not affect:** healing, displacement or artifact trigger frequency by itself.
- **UI copy:** «Увеличивает шанс критического удара.»
- **Dependency:** `meta_agility_evasion` + `meta_force_attack_power` cross-gate.
- **Balance:** roll scope, cap and source tags `PENDING_BALANCE`.

#### `meta_agility_crit_power` — Усиление крит. удара

- **Stat key:** `crit_power`.
- **Player promise:** критический hit заметно сильнее обычного hit.
- **Path role:** final precision node.
- **Affects:** critical damage multiplier only; must preserve base damage semantics.
- **Does not affect:** crit chance, echo count or all magic damage unless the source is also MAGIC and ordering is explicit.
- **UI copy:** «Усиливает урон критического удара.»
- **Dependency:** `meta_agility_crit_chance` + `meta_force_attack_power`/branch gate.
- **Balance:** base multiplier, cap and interaction with `passive_star_compass`/mirror echo `PENDING_BALANCE`.

### 3.4 Ветка `meta_focus` — Фокус

#### `meta_focus_cooldown` — Перезарядка заклинаний

- **Stat key:** `spell_cooldown`.
- **Player promise:** оружие/заклинание возвращается к готовности быстрее.
- **Path role:** root tempo node.
- **Affects:** weapon/spell cooldowns that opt into `COOLDOWN_REDUCIBLE`.
- **Does not affect:** animation speed, effect duration, trigger frequency of unrelated artifacts.
- **UI copy:** «Сокращает перезарядку заклинаний.»
- **Dependency:** branch root `meta_focus`.
- **Balance:** additive vs multiplicative order, floor and source tags `PENDING_BALANCE`.

#### `meta_focus_duration` — Длительность заклинаний

- **Stat key:** `spell_duration`.
- **Player promise:** persistent field, orbit or status remains active longer.
- **Path role:** persistence node after cooldown.
- **Affects:** effects tagged `DURATION_SCALABLE`; should not extend telegraph warning unless explicitly paired.
- **Does not affect:** projectile travel time, damage over time tick count, artifact offer timer by default.
- **UI copy:** «Увеличивает длительность активных заклинаний.»
- **Dependency:** `meta_focus_cooldown` + branch gate.
- **Balance:** tag list, tick behavior and cap `PENDING_BALANCE`.

#### `meta_focus_size` — Размер заклинаний

- **Stat key:** `spell_size`.
- **Player promise:** зона воздействия и shape readablely grow together.
- **Path role:** geometry capstone.
- **Affects:** radius/width/length of tagged spell geometry and its telegraph.
- **Does not affect:** target count, damage multiplier or screen-space UI icons.
- **UI copy:** «Увеличивает размер зон и форм заклинаний.»
- **Dependency:** `meta_focus_duration` + `meta_force_magic_damage` cross-gate.
- **Balance:** geometry whitelist, telegraph scaling, cap and collision safety `PENDING_BALANCE`.

### 3.5 Ветка `meta_magnet` — Магнит

#### `meta_magnet_pickup_radius` — Радиус сбора предметов

- **Stat key:** `pickup_radius`.
- **Player promise:** arena drops легче подбирать, когда рядом опасная толпа.
- **Path role:** root collection node.
- **Affects:** eligible pickups within line-of-effect; radius must not pull through walls unless level contract explicitly allows it.
- **Does not affect:** drop spawn rate, XP/mana value, artifact rarity or enemy aggro.
- **UI copy:** «Увеличивает радиус сбора предметов.»
- **Dependency:** branch root `meta_magnet`.
- **Balance:** drop whitelist, wall/occlusion rule and cap `PENDING_BALANCE`.

#### `meta_magnet_mana_gain` — Получение маны / опыта

- **Stat key:** `pickup_yield_multiplier` (working internal name).
- **Player promise:** выбранный progression pickup даёт больше ресурса при фактическом сборе.
- **Path role:** resource node after pickup radius.
- **Naming note:** screenshot labels this stat «Получение маны», while current first-run architecture uses XP. Recommended UI decision is to name the player-facing resource consistently after Product confirms whether mana and XP are the same economy.
- **Affects:** only an explicitly tagged progression pickup; does not alter healing mote amount or gold.
- **Does not affect:** pickup radius, XP threshold table, artifact offer chance, enemy drop rate.
- **UI copy:** «Увеличивает получение маны/опыта с подобранного ресурса.»
- **Dependency:** `meta_magnet_pickup_radius`; semantic label and source tag `PENDING_PRODUCT_DECISION`.
- **Balance:** yield multiplier, rounding and XP/mana mapping `PENDING_BALANCE`.

### 3.6 Ветка `meta_defense` — Защита

#### `meta_defense_damage_taken` — Получаемый урон

- **Stat key:** `damage_taken_multiplier`.
- **Player promise:** eligible incoming damage is reduced before health is changed.
- **Path role:** root mitigation node.
- **Affects:** combat damage after hit validity and before healing/health delta; displayed as a negative modifier in stat screen.
- **Does not affect:** unavoidable instant-death policy, evasion rolls, artifact ward or enemy damage output.
- **UI copy:** «Снижает получаемый урон.»
- **Dependency:** branch root `meta_defense`.
- **Balance:** cap, damage categories and order with armor/internal mitigation `PENDING_BALANCE`.

#### `meta_defense_enemy_hp` — Макс. HP врага / Ослабление врагов

- **Stat key:** `enemy_max_hp_multiplier`.
- **Player promise:** reduces maximum HP of eligible enemies so that pressure falls without secretly increasing hero damage.
- **Path role:** offensive defense capstone.
- **Affects:** enemy health initialization for eligible non-boss/approved boss classes; health bar and death threshold update together.
- **Does not affect:** enemy speed, damage, spawn rate, elite rarity or boss mechanics unless approved.
- **UI copy:** recommended «Ослабление врагов»; screenshot-compatible secondary label «Макс. HP врага» with a negative modifier.
- **Dependency:** `meta_defense_damage_taken` + `meta_force_attack_power` cross-gate.
- **Balance:** sign, floor, enemy whitelist and boss policy `PENDING_BALANCE`/`PENDING_PRODUCT_DECISION`.

## 4. Dependency map

### Основные пути

```text
Живучесть:  max_hp → regen → healing_mote
Сила:       attack_power → attack_multiplier → magic_damage
Проворство: move_speed → evasion → crit_chance → crit_power
Фокус:      cooldown → duration → size
Магнит:     pickup_radius → mana/XP_gain
Защита:     damage_taken → enemy_max_hp
```

### Cross-gates

| Открываемый узел | Дополнительная связь | Зачем игроку |
|---|---|---|
| `meta_vitality_mote_healing` | `meta_magnet_pickup_radius` | healing mote — это pickup-решение, а не скрытая regen-пассивка |
| `meta_force_magic_damage` | `meta_focus_cooldown` или focus root | магический урон раскрывается через темп заклинаний |
| `meta_agility_crit_chance` | `meta_force_attack_power` | точность требует базовой силы, иначе crit не меняет понятный outcome |
| `meta_agility_crit_power` | `meta_force_attack_power` | критический multiplier не открывается без damage foundation |
| `meta_focus_size` | `meta_force_magic_damage` | большая зона должна быть осознанным magic build choice |
| `meta_defense_enemy_hp` | `meta_force_attack_power` | ослабление врагов не должно быть единственным damage route |

Пороги branch rank, минимальный node rank и выбор `cooldown`-или-`focus root` для magic gate — `PENDING_PRODUCT_DECISION`; таблица фиксирует topology, не готовую числовую экономику.

## 5. Семантика StatsCalculator

Один вычислительный слой должен собрать persistent node ranks, базовые характеристики героя и run modifiers. Content Agent фиксирует следующие границы:

- `max_hp`, `regen_per_second`, `healing_mote_value` — разные источники и разные этапы health pipeline.
- `attack_power` — additive/flat axis; `attack_multiplier` — multiplicative axis. Нельзя показывать их одной строкой.
- `all_magic_damage` действует только на источники с explicit `MAGIC` tag.
- `move_speed` не меняет enemy/projectile simulation speed.
- `evasion_chance` бросается на hit resolution, а не при появлении telegraph.
- `crit_chance` делает один roll на определённый source event; `crit_power` меняет только crit outcome.
- `spell_cooldown`, `spell_duration`, `spell_size` — разные axes; size увеличивает geometry и её telegraph согласованно.
- `pickup_radius` не проходит через walls/occlusion без отдельного level rule.
- `mana_gain`/`XP gain` не меняет XP threshold table и не превращает healing mote в progression resource.
- `damage_taken_multiplier` применяется до health delta; внутренний `armor`, если runtime сохраняет его, маппится сюда или остаётся непубличным, чтобы не создавать второй UI node.
- `enemy_max_hp_multiplier` применяется при создании/инициализации enemy health с явным floor; sign и boss whitelist должны быть едины в UI, runtime и balance data.

## 6. Магазин и состояния

### Purchase flow

1. Игрок находится в hub/shop между забегами.
2. Выбирает node и видит текущий rank, следующий rank, стоимость, dependency и итоговую строку stat.
3. Нажимает «Улучшить» и подтверждает покупку.
4. MetaProgression атомарно проверяет Gold, node rank, branch budget и snapshot revision.
5. Wallet и meta snapshot сохраняются одной операцией; UI показывает «Изменения применятся в следующем забеге».

UI не меняет Gold или rank локально без подтверждённого результата persistence. Повтор запроса с той же revision должен быть idempotent.

### Required states and copy

| Состояние | Copy |
|---|---|
| доступно | «Улучшить» |
| max rank | «Максимальный ранг» |
| закрыто | «Недоступно» + причина зависимости |
| мало Gold | «Не хватает золота» |
| нет branch budget | «Ветка исчерпана» |
| сохранение | «Сохраняем прогресс…» |
| success | «Изменения применятся в следующем забеге» |
| save failure | «Не удалось сохранить. Покупка не применена.» |
| reset proposal | «Сбросить ветку»; refund/price `PENDING_PRODUCT_DECISION` |

Магазин не должен открывать upgrade offer во время pause/run. Run result и reward ledger — отдельная граница; Gold reward не следует вычислять UI.

## 7. Visual Lab handoff — brief only

Мокапы и final art не создаются этим пакетом.

| Поле | Значение |
|---|---|
| route | `UI_ART` для shop/tree/cards; `SPRITE` только для будущих node icons |
| stage_path | `docs/mockups/07-passives/` для visual language, `docs/mockups/16-upgrade-offers/` для upgrade card patterns |
| asset_id / family_id / candidate_id | `null` до Visual Lab intake |
| status | `PROPOSAL` |
| technical_status | `NOT_RUN` |
| artistic_status | `PENDING` |
| manifest / consumer | `NOT_PROMOTED`; consumer — MetaProgression/StatsCalculator/UI projection |
| visual code | deep blue-grey, smoky teal, warm ivory, muted brass, soft jade; ветви различаются формой/линией и мягким accent, не только цветом |
| acceptance cue | node state/rank/lock/cost читаются на 390×844; high-contrast negative modifier и dependency remain visible |

Визуальная задача следующего агента — создать master tree/shop language и mockups по этим semantic IDs. Content Agent не назначает candidate IDs и не объявляет visual approval.

## 8. Open decisions

- как именно 10 branch ranks распределяются между 17 node ranks и какие node caps подтверждаются Balance;
- точные значения и порядок сложения/умножения по всем 17 осям;
- `Получение маны` и текущая XP-экономика: одно ли это значение и какое имя является canonical;
- источник и тег healing mote;
- sign, floor и enemy whitelist для `meta_defense_enemy_hp`;
- отображать ли internal armor как часть `Получаемый урон` без отдельного публичного node;
- применяются ли покупки с начала следующего run или после hub reload;
- reset/refund policy и offline/save-failure behavior;
- canonical event/schema для meta purchase — не изобретать в content docs до Architecture sync.

## Актуальная граница дерева постоянных улучшений

Сверка выполнена от main ec30c239aa22aa1d9c8ad1faab25d99633f4cb29. Сохранено 6 ветвей и 17 узлов; улучшения применяются к следующему забегу.

Стоимость, кривые рангов, кошелёк и сохранение принадлежат Balance/Runtime. Контент фиксирует только смысловые оси, зависимости и порядок узлов.

Статус: CONTENT_SCOPE_CLOSED; balance lock и runtime proof не заявлены.
