# REF-CONTENT-01 — Оригинальная матрица контента MAC

Статус пакета: `PARTIAL / CONTENT_SPECIFIED`
Идентификатор задачи: `REF-CONTENT-01`
Parent HEAD: `a83dfc7886bc32ae55b87bc96136c992a41c0bd3`
Разрешённый каталог: `docs/agents/content-design/`

Этот документ фиксирует результат разработки контента и границы передачи. Он не является разрешением на исполнение, баланс или производство графики.

- Runtime approval: `NOT_REQUESTED`
- Balance lock: `NOT_GRANTED`
- Artistic approval: `PENDING`
- Runtime implementation: `NOT_CHANGED`
- PNG/SVG и мокапы: `NOT_CREATED`
- Новые ID в рамках этой ревизии: 10 элитных вариаций; все имеют только статус `PROPOSED`, без runtime/architecture approval

## 1. Цель, пользователь и критерии успеха

**Цель:** дать агенту баланса, архитектуре/исполнению и Visual Lab одну самостоятельную матрицу оригинального контента MAC с понятными ролями, тегами, зависимостями, точками предложения/появления и границами ответственности.

**Пользователь результата:** игрок должен за короткое описание понять, зачем нужен предмет, какую опасность он создаёт и какое решение предлагает; следующий агент должен получить стабильный ID и проверяемый контракт без догадок.

**Режим работы:** продуктовая спецификация контента, проверка зависимостей, подготовка межагентской передачи.

Критерии успеха:

1. Матрица содержит 10 оружий-способностей, 10 общих пассивок забега, 10 прямых синергий, 10 артефактов, 10 базовых/обычных записей противников, 10 отдельных предложенных элитных вариаций и 4 базовые записи боссов.
2. Каждая пассивка забега даёт общую выгоду билду; связанное оружие используется только как `synergy_anchor` для проверки эволюции.
3. У каждой связи указаны роль, теги, точка предложения/появления, потребители и незакрытые числовые поля.
4. Указаны два предложенных расширения главных боссов и пять предложенных мини-боссов действующего конверта 30 минут; они не выдаются за утверждённые записи исполнения.
5. Ни один внешний проект не является источником названий, персонажей, описаний, чисел, изображений, шансов выпадения или ассетов.

## 2. Правило оригинальности и граница источников

Четыре разрешённых репозитория использовались только для анализа общих способов разделить игровые обязанности: сбор опыта и переход уровня, отдельное предложение улучшений, таблица состава волн, специальная встреча, жизненный цикл снаряда/зоны и отдельный путь награды. Все названия, фантазии, роли, теги и поведение ниже написаны для Moonveil: Eclipse.

Из внешних проектов не перенесены значения параметров, имена, герои, противники, боссы, тексты, изображения, таблицы добычи и пути ассетов.

### Доказательства по разрешённым репозиториям

| Репозиторий и зафиксированная ревизия | Проверенные файлы | Наблюдение общего уровня | Граница применения в MAC |
|---|---|---|---|
| [murparreira/vampire-survivors-clone-godot-4, `ea00bccf518b4a6084870e313e10aaad99746540`](https://github.com/murparreira/vampire-survivors-clone-godot-4/tree/ea00bccf518b4a6084870e313e10aaad99746540) | [`experience_manager.gd`](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/ea00bccf518b4a6084870e313e10aaad99746540/scenes/managers/experience_manager.gd), [`upgrade_manager.gd`](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/ea00bccf518b4a6084870e313e10aaad99746540/scenes/managers/upgrade_manager.gd), [`enemy_manager.gd`](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/ea00bccf518b4a6084870e313e10aaad99746540/scenes/managers/enemy_manager.gd), [`experience_vial.gd`](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/ea00bccf518b4a6084870e313e10aaad99746540/scenes/game_objects/experience_vial/experience_vial.gd) | Опыт, улучшения, состав врагов, особая встреча и жизненный цикл подбираемого опыта разведены по отдельным узлам. | В MAC сохраняются отдельные `ProgressionSystem`, `UpgradeOfferSystem`, `WaveDirector`, `BossDirector` и `XPDrop`; чужие значения не используются. |
| [ParsaSabzei/20-Minutes-till-dawn, `fe437437a369b620e4c32c36ce2826a14f911230`](https://github.com/ParsaSabzei/20-Minutes-till-dawn/tree/fe437437a369b620e4c32c36ce2826a14f911230) | [`PlayerController.java`](https://github.com/ParsaSabzei/20-Minutes-till-dawn/blob/fe437437a369b620e4c32c36ce2826a14f911230/core/src/main/java/ap/project/controller/PlayerController.java), [`AbilityController.java`](https://github.com/ParsaSabzei/20-Minutes-till-dawn/blob/fe437437a369b620e4c32c36ce2826a14f911230/core/src/main/java/ap/project/controller/AbilityController.java), [`MonsterController.java`](https://github.com/ParsaSabzei/20-Minutes-till-dawn/blob/fe437437a369b620e4c32c36ce2826a14f911230/core/src/main/java/ap/project/controller/MonsterController.java), [`GameView.java`](https://github.com/ParsaSabzei/20-Minutes-till-dawn/blob/fe437437a369b620e4c32c36ce2826a14f911230/core/src/main/java/ap/project/view/GameView.java) | Подбор опыта переводит игру в выбор способности; обычный спавн и особая встреча идут разными путями; состояние выбора отделено от обычной игры. | В MAC закреплены три карточки предложения, отдельные encounter-записи и отдельные каналы сундука босса и артефакта. Чужие таймеры, тексты и названия не используются. |
| [Blaze-master/Magic_Survival_Clone, `27a3d9e9aeb06f0ffc590fd18fc37fa83367bfaa`](https://github.com/Blaze-master/Magic_Survival_Clone/tree/27a3d9e9aeb06f0ffc590fd18fc37fa83367bfaa) | [`enemies.py`](https://github.com/Blaze-master/Magic_Survival_Clone/blob/27a3d9e9aeb06f0ffc590fd18fc37fa83367bfaa/enemies.py), [`magic.py`](https://github.com/Blaze-master/Magic_Survival_Clone/blob/27a3d9e9aeb06f0ffc590fd18fc37fa83367bfaa/magic.py), [`objects.py`](https://github.com/Blaze-master/Magic_Survival_Clone/blob/27a3d9e9aeb06f0ffc590fd18fc37fa83367bfaa/objects.py), [`artifacts.py`](https://github.com/Blaze-master/Magic_Survival_Clone/blob/27a3d9e9aeb06f0ffc590fd18fc37fa83367bfaa/artifacts.py) | Состав врагов и временные группы спавна отделены от объектов поведения; в данных оружия различаются свойства снаряда, линии и зоны. | MAC использует собственную семантику оружия, зон и телеграфов; пустой внешний модуль артефактов не стал основанием для содержания MAC. |
| [syncXL/Magic_Survival_Clone, `87f460c5385f93f785ec4310edbaa9039f078863`](https://github.com/syncXL/Magic_Survival_Clone/tree/87f460c5385f93f785ec4310edbaa9039f078863) | [`gamedata.py`](https://github.com/syncXL/Magic_Survival_Clone/blob/87f460c5385f93f785ec4310edbaa9039f078863/gamedata.py), [`magic.py`](https://github.com/syncXL/Magic_Survival_Clone/blob/87f460c5385f93f785ec4310edbaa9039f078863/magic.py), [`objects.py`](https://github.com/syncXL/Magic_Survival_Clone/blob/87f460c5385f93f785ec4310edbaa9039f078863/objects.py), [`artifacts.py`](https://github.com/syncXL/Magic_Survival_Clone/blob/87f460c5385f93f785ec4310edbaa9039f078863/artifacts.py) | Глобальные данные, определения атак, объекты поля, границы спавна и сундуки имеют разные области ответственности. | В MAC это применено как единый data-driven реестр с раздельными `XP`, `BOSS_CHEST`, `ELITE_CHEST` и `ArtifactOfferSystem`; код внешней копии не переносится. |

## 3. Матрица: оружие-способность → общая пассивка → синергия

Под «способностью» здесь понимается автоматически применяемое оружие забега. Начальные значения урона, частоты, дальности, размера, длительности и ограничения производительности принадлежат агенту баланса и в этот документ не входят.

| Оружие / способность | Роль и решение игрока | Общая пассивка | Синергия и новое поведение | Теги | Зависимости | Точка предложения / статус |
|---|---|---|---|---|---|---|
| `weapon_moon_blade` — Лунный клинок | Ближняя дуга; вести толпу по касательной или менять направление, чтобы не застрять в контакте | `passive_wind_of_travel` — улучшает качество перемещения и выбор линии для всего билда | `synergy_moon_dance` — орбитальные дорожки меняют ценность движения и оставляют читаемый безопасный ритм | `close`, `arc`, `movement`, `lane` | `BuildInventory`, `CombatSystem`, `SynergyResolver`, `TelegraphResolver` | `STARTING_LOADOUT`/`UPGRADE_OFFER`; `EXISTING_CONTENT_SPECIFIED` |
| `weapon_jade_talismans` — Нефритовые талисманы | Дальний контроль; распределять метки по группе или удерживать приоритетную цель | `passive_jade_focus` — повышает стабильность выбора и разрешения меток у всех подходящих источников | `synergy_heavenly_seals` — цепь печатей проходит по ещё не посещённым узлам и не зацикливается | `ranged`, `mark`, `homing`, `chain` | `MarkStore`, `CombatSystem`, `UpgradeOfferSystem`, `SynergyResolver` | `STARTING_LOADOUT`/`UPGRADE_OFFER`; `EXISTING_CONTENT_SPECIFIED` |
| `weapon_crimson_flame_fan` — Веер багрового пламени | Конус и очаги; закрыть опасный коридор или оставить проход для движения | `passive_ember_heart` — поддерживает осмысленность состояний и зон для всех допустимых источников | `synergy_phoenix_sky` — огненный след проходит через разрешённые очаги и связывает разрозненные зоны | `cone`, `burn`, `zone`, `lane` | `StatusSystem`, `ZoneStore`, `TelegraphResolver`, `SynergyResolver` | `UPGRADE_OFFER`; `EXISTING_CONTENT_SPECIFIED` |
| `weapon_frost_pearl` — Ледяная жемчужина | Контроль группы; удержать кластер в выгодной точке или уйти до нового телеграфа | `passive_frost_thread` — связывает контрольные эффекты всего билда, не выключая предупреждения | `synergy_winter_palace` — создаёт временную морозную решётку с видимым безопасным маршрутом | `slow`, `burst`, `lattice`, `control` | `StatusSystem`, `ZoneStore`, `CombatSystem`, `BossImmunityPolicy` | `UPGRADE_OFFER`; `EXISTING_CONTENT_SPECIFIED` |
| `weapon_thunder_needles` — Иглы грома | Всплеск и цепь; собрать допустимую плотность целей, сохраняя чтение угроз | `passive_heavenly_seal` — выстраивает общий порядок точных попаданий и уязвимостей | `synergy_heavenly_judgment` — видимый удар сверху проходит по отмеченным узлам без скрытого урона за экраном | `chain`, `conductive`, `burst`, `priority` | `CombatSystem`, `MarkStore`, `TelegraphResolver`, `SynergyResolver` | `UPGRADE_OFFER`; `EXISTING_CONTENT_SPECIFIED` |
| `weapon_spirit_bell` — Колокол духов | Защита и толчок; остаться у оберега или выйти за опытом и приоритетной целью | `passive_iron_bell` — даёт всему билду читаемое окно защиты и стойкости | `synergy_guardian_bell` — движущийся край оберега отталкивает допустимые угрозы и закрывается после окна | `ward`, `guard`, `pulse`, `displacement` | `HealthSystem`, `ProjectileResolver`, `CombatSystem`, `CleanupRegistry` | `UPGRADE_OFFER`; `EXISTING_CONTENT_SPECIFIED` |
| `weapon_fox_mirage` — Лисий мираж | Манёвр и линия; прокладывать атаки в коридор или во фланг, а не всегда в ближайшую цель | `passive_mirror_shard` — разрешает ограниченное повторение подходящих попаданий с защитой от рекурсии | `synergy_nine_reflections` — оставляет отложенные отражения с указанием источника и самостоятельным завершением | `mirror`, `echo`, `corridor`, `delayed` | `CombatSystem`, `EchoGuard`, `VFXCleanup`, `SynergyResolver` | `UPGRADE_OFFER`; `EXISTING_CONTENT_SPECIFIED` |
| `weapon_lotus_mines` — Лотосовые мины | Отложенная зона; заранее занять место или отказаться от него перед опасным телеграфом | `passive_lotus_heart` — связывает здоровье и разрешённое лечение как общий выбор выживания | `synergy_lotus_sanctuary` — мины объединяются во временное поле контроля с ограниченным восстановлением | `mine`, `zone`, `sanctuary`, `healing` | `ZoneStore`, `HealthSystem`, `HealingSource`, `SynergyResolver` | `UPGRADE_OFFER`; `EXISTING_CONTENT_SPECIFIED` |
| `weapon_star_bow` — Звёздный лук | Приоритетная дальняя цель; соединять дальние точки или собрать плотную группу | `passive_star_compass` — задаёт общий ритм точных ударов для всех источников, допускающих крит | `synergy_constellation_rain` — якоря соединяются, затем по линиям проходит видимый дождь стрел | `ranged`, `anchor`, `line`, `precision` | `TargetingSystem`, `TelegraphResolver`, `CombatSystem`, `SynergyResolver` | `UPGRADE_OFFER`; `EXISTING_CONTENT_SPECIFIED` |
| `weapon_black_eclipse_umbrella` — Чёрный зонт затмения | Стягивание и сбор; объединить допустимую угрозу или сохранить притяжение для элиты | `passive_spirit_lens` — улучшает чтение и сбор подходящих ресурсов без прохода сквозь стены | `synergy_eclipse_vortex` — ограниченная воронка стягивает разрешённых врагов и предметы, затем схлопывается | `pull`, `pickup`, `vortex`, `utility` | `MagnetSystem`, `TargetFilter`, `CombatSystem`, `SynergyResolver` | `UPGRADE_OFFER`; `EXISTING_CONTENT_SPECIFIED` |

### Правило общих пассивок

Все 10 `passive_*` занимают временные слоты пассивок, но их эффект относится к общему билду и к явно разрешённым источникам, а не только к парному оружию. Связь с одним оружием хранится как `synergy_anchor` и нужна для проверки конкретной эволюции. Она не создаёт скрытого множителя только для этого оружия.

Общее условие эволюции: оружие достигло уровня 6, пассивка достигла ранга 5, оружие ещё не эволюционировано, пара совпадает по `synergy_id`, источник — нефинальный `BOSS_CHEST`, `encounter_kind` равен `MAIN_BOSS` или `MINI_BOSS`, а число подтверждённых синергий в забеге меньше 5. Числовой вклад и кривую рангов закрепляет агент баланса.

## 4. Матрица десяти артефактов

Артефакт — временный модификатор текущего забега. Он не занимает слот оружия или пассивки, не образует предзабеговый набор и не меняет кошелёк напрямую. Каждый источник показывает ровно три различные карточки и принимает один выбор.

| Артефакт | Класс и событие | Решение игрока | Теги цели / границы | Зависимости | Источник / статус |
|---|---|---|---|---|---|
| `artifact_jade_compass` — Нефритовый компас | `AURA`; сбор дропа арены | пройти через поле маршрута ради ресурса или обойти риск | допустимые дропы и ближайшие угрозы; не сквозь стену | `ArtifactEffectSystem`, `PickupFilter`, `ArenaDropRegistry` | `ELITE_PACK`/`FIRST_CLEAR_REWARD`; `EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING` |
| `artifact_mirror_shard` — Грань зеркала | `TRIGGERED_EFFECT`; критическое попадание оружия | принять отложенное эхо ради окна давления | зона исходного попадания, один источник события, без самозапуска | `ArtifactEffectSystem`, `CombatSystem`, `SourceEventDedupe` | `ELITE_PACK`/`FIRST_CLEAR_REWARD`; `EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING` |
| `artifact_phoenix_feather` — Перо феникса | `TRIGGERED_EFFECT`; поражение элиты | провести следующий поток через короткий огненный след | враги, пересекающие след; путь очищается самостоятельно | `ArtifactEffectSystem`, `EliteEvent`, `ZoneStore` | `ELITE_PACK`/`FIRST_CLEAR_REWARD`; `EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING` |
| `artifact_frost_bead` — Ледяная бусина | `WEAPON_MODIFIER`; наложение контроля | удержать отмеченную цель до следующего раскрытия зоны | контролируемая цель и соседняя область; защита босса явна | `ArtifactEffectSystem`, `StatusSystem`, `TargetFilter` | `ELITE_PACK`/`FIRST_CLEAR_REWARD`; `EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING` |
| `artifact_bell_fragment` — Осколок колокола | `TRIGGERED_EFFECT`; защищённое попадание после проверки урона | допустить ограниченный риск ради резонанса | ближайшие угрозы; одно событие урона, без двойного начисления | `HealthSystem`, `CombatSystem`, `DamageFactLedger` | `ELITE_PACK`/`FIRST_CLEAR_REWARD`; `EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING` |
| `artifact_lotus_seed` — Семя лотоса | `TRIGGERED_EFFECT`; лечение при полном здоровье или излишек лечения | сохранить восстановление как будущий оберег | следующее разрешённое входящее попадание; список источников лечения | `HealthSystem`, `HealingSource`, `ArtifactTriggerDedupe` | `ELITE_PACK`/`FIRST_CLEAR_REWARD`; `EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING` |
| `artifact_moon_crown` — Лунная корона | `TARGET_MODIFIER`; начало фазы босса | пережить телеграф и использовать короткое окно уязвимости | только текущая разрешённая фаза босса | `BossDirector`, `TelegraphResolver`, `ArtifactEffectSystem` | `ELITE_PACK`/`FIRST_CLEAR_REWARD`; `EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING` |
| `artifact_black_bead` — Чёрная бусина | `WEAPON_MODIFIER`; попадание по допустимой элите | менять режим притяжения и всплеска под текущую угрозу | последний допустимый источник оружия и список иммунитетов | `CombatSystem`, `TargetFilter`, `ArtifactEffectSystem` | `ELITE_PACK`/`FIRST_CLEAR_REWARD`; `EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING` |
| `artifact_tideglass` — Приливное стекло | `AURA`; сбор дропа арены | провести путь от ресурса к герою, меняя маршрут толпы | снимок пути, пересекающие его враги; без кражи награды | `ArenaDropRegistry`, `ZoneStore`, `ReplayState` | `ELITE_PACK`/`FIRST_CLEAR_REWARD`; `PROPOSED / REGISTRY_SYNC_PENDING` |
| `artifact_silent_lantern` — Безмолвный фонарь | `TARGET_MODIFIER`; выбор элиты или цели высокого риска | увидеть следующую угрозу заранее, но всё равно выполнить уклонение | одна текущая телеграфируемая угроза; не отменяет её | `TargetSelector`, `TelegraphResolver`, `ArtifactEffectSystem` | `ELITE_PACK`/`FIRST_CLEAR_REWARD`; `PROPOSED / REGISTRY_SYNC_PENDING` |

Для каждого артефакта обязательны один источник события, список допустимых целей, граница очистки/окончания, защита от рекурсии и идентификатор повтора. Значения, частота, редкость, режим повтора и числовой эффект — `PENDING_BALANCE` или `PENDING_ARCHITECTURE`.

## 5. Полное дерево постоянных пассивок магазина

Полная запись с описанием каждого узла находится в [`META_PASSIVE_TREE.md`](META_PASSIVE_TREE.md). Это отдельный слой между забегами: узлы покупаются за Gold, не занимают шесть временных passive slots и не попадают в обычное предложение улучшений.

| Ветка | Полный путь узлов | Дополнительные зависимости |
|---|---|---|
| `meta_vitality` — Живучесть | `meta_vitality_max_hp` → `meta_vitality_regen` → `meta_vitality_mote_healing` | последний узел требует `meta_magnet_pickup_radius` |
| `meta_force` — Сила | `meta_force_attack_power` → `meta_force_attack_multiplier` → `meta_force_magic_damage` | магический финал требует корень `meta_focus` или `meta_focus_cooldown` |
| `meta_agility` — Проворство | `meta_agility_move_speed` → `meta_agility_evasion` → `meta_agility_crit_chance` → `meta_agility_crit_power` | шанс и сила крита требуют `meta_force_attack_power` |
| `meta_focus` — Фокус | `meta_focus_cooldown` → `meta_focus_duration` → `meta_focus_size` | размер требует `meta_force_magic_damage` |
| `meta_magnet` — Магнит | `meta_magnet_pickup_radius` → `meta_magnet_mana_gain` | имя «мана/опыт» и единый источник ресурса требуют продуктового решения |
| `meta_defense` — Защита | `meta_defense_damage_taken` → `meta_defense_enemy_hp` | ослабление врагов требует `meta_force_attack_power` |

Итого зафиксировано 17 `meta_*` узлов. Распределение десяти покупок ветви между дочерними узлами, цены, величины, порядок сложения и сохранение — `PENDING_BALANCE`/`PENDING_PRODUCT_DECISION`. Дерево не смешивает постоянные узлы, run-пассивки и артефакты.

## 6. Матрица десяти базовых/обычных записей противников первого забега

Эта десятка уже принадлежит защищённому пакету Stage 04 и не заменяется этим документом. Для данного среза она является `base_enemy_roster`: десять базовых/обычных записей, поверх которых описываются отдельные элитные вариации. Все записи являются противниками пула, а не мини-боссами или главными боссами. `enemy_stone_oni` и `enemy_eclipse_serpent` уже помечены `ELITE_FAMILY`; это усиленные базовые записи, а не боссы. Поэтому термин «10 обычных» здесь означает десять базовых enemy ID, а вопрос о подкатегории двух Stage 04 записей остаётся явно открытым — тихая переклассификация запрещена.

| ID | Роль и подпись поведения | Теги | Первая точка появления | Контр-решение игрока | Зависимости | Статус |
|---|---|---|---|---|---|---|
| `enemy_ink_beetle` — Чернильный жук | Прямой натиск с короткой линией контакта | `rusher`, `contact`, `low_durability` | 0–2 мин; затем продолжается | двигаться по касательной или очистить ближайшую линию | `WaveDirector`, `CombatSystem`, `XPDrop`, visual manifest Stage 04 | `EXISTING_CONTENT_SPECIFIED` |
| `enemy_lantern_moth` — Фонарная моль | Дальний преследователь с предупреждаемым снарядом | `ranged`, `projectile`, `spacing` | 2–5 мин; первый слой дальнего давления | сократить дистанцию или сохранить маршрут | `TargetingSystem`, `ProjectileResolver`, `TelegraphResolver` | `EXISTING_CONTENT_SPECIFIED` |
| `enemy_bone_carp` — Костяной карп | Рывок по зафиксированной линии с восстановлением | `line_dash`, `telegraph`, `recovery` | 2–5 мин; вместе с первым давлением | выйти из отмеченной линии и наказать восстановление | `TelegraphResolver`, `MovementSystem`, `CombatSystem` | `EXISTING_CONTENT_SPECIFIED` |
| `enemy_paper_ghost` — Бумажный призрак | Перемещение с видимым мерцанием до повторного появления | `teleporter`, `reposition`, `contact` | 5–10 мин; расширение угроз | читать окно возвращения, а не преследовать исчезновение | `EncounterState`, `TelegraphResolver`, `TargetingSystem` | `EXISTING_CONTENT_SPECIFIED` |
| `enemy_jade_toad` — Нефритовая жаба | Прыжок в отмеченную область и временная зона отравления | `leap`, `zone`, `area_denial` | 5–10 мин; пространственное давление | покинуть метку приземления и вернуться после восстановления | `ZoneStore`, `TelegraphResolver`, `StatusSystem` | `EXISTING_CONTENT_SPECIFIED` |
| `enemy_mirror_fox` — Зеркальная лиса | Ложная копия и фланговый манёвр | `decoy`, `flank`, `mirror`, `target_confusion` | 5–10 мин; проверка выбора цели | найти источник и не идти в ложный коридор | `TargetFilter`, `DecoyResolver`, `CombatSystem` | `EXISTING_CONTENT_SPECIFIED` |
| `enemy_bell_crab` — Колокольный краб | Лобовая защита; уязвимое место читается сзади | `guard`, `tank`, `directional`, `contact` | 10–15 мин; усиленный рядовой слой | обойти и не обмениваться ударами в защиту | `DirectionalHitResolver`, `CombatSystem`, `TelegraphResolver` | `EXISTING_CONTENT_SPECIFIED` |
| `enemy_thread_doll` — Нитяная кукла | Луч замедления; разрыв дистанции ломает связь | `controller`, `beam`, `slow`, `spacing` | 10–15 мин; контроль маршрута | разорвать линию до фиксации замедления | `ProjectileResolver`, `StatusSystem`, `TelegraphResolver` | `EXISTING_CONTENT_SPECIFIED` |
| `enemy_stone_oni` — Каменный они | Усиленный удар по земле с длинным предупреждением и восстановлением | `elite`, `slam`, `zone`, `heavy` | 10–15 мин; вход усиленного семейства | покинуть крупный телеграф и атаковать восстановление | `EliteDirector`, `TelegraphResolver`, `ZoneStore`, `XPDrop` | `EXISTING_CONTENT_SPECIFIED / ELITE_FAMILY` |
| `enemy_eclipse_serpent` — Змей затмения | Усиленный рывок по дуге с оставляемым следом | `elite`, `dash`, `trail`, `arc` | 15–20 мин; поздний слой давления | пересечь путь после поворота и не входить в след | `EliteDirector`, `TelegraphResolver`, `ZoneStore`, `XPDrop` | `EXISTING_CONTENT_SPECIFIED / ELITE_FAMILY` |

Точные HP, урон, скорость, веса состава, активный лимит, ступень XP, элитный ритм и продолжение после 20 минут принадлежат агенту баланса и `ContentRegistry`; здесь они не задаются.

## 6A. Десять предложенных элитных вариаций

Эти десять записей — отдельные варианты поверх десяти базовых записей пула, по одному варианту на каждую базовую семью. Они не заменяют базовые ID, не становятся мини-боссами, не добавляются в постоянный roster и не дают автоматический артефакт. Все ID ниже впервые вводятся в этой ревизии и имеют только статус `PROPOSED`; их числовые параметры и точные окна появления принадлежат B1.

| Вариант ID | Базовая запись | Уникальная проверка и контр-решение | Теги | Окно появления | Зависимости | Статус |
|---|---|---|---|---|---|---|
| `elite_variant_ink_beetle_ironcarapace` — Железнопанцирный чернильный жук | `enemy_ink_beetle` | Короткий направленный разгон с читаемым панцирным окном; уйти по касательной и наказать паузу восстановления | `elite`, `rusher`, `guard`, `recovery` | полоса базовой записи; точное elite-окно `PENDING_BALANCE` | `EliteDirector`, `TelegraphResolver`, `CombatSystem`, `XPDrop`, `EnemyRegistry` | `PROPOSED / PENDING_BALANCE / PENDING_ARCHITECTURE` |
| `elite_variant_lantern_moth_prismwing` — Призмокрылая фонарная моль | `enemy_lantern_moth` | Три сходящиеся линии с одним читаемым зазором; пройти через зазор или сократить дистанцию до следующего залпа | `elite`, `ranged`, `fan`, `spacing` | полоса базовой записи; точное elite-окно `PENDING_BALANCE` | `EliteDirector`, `ProjectileResolver`, `TelegraphResolver`, `TargetingSystem` | `PROPOSED / PENDING_BALANCE / PENDING_ARCHITECTURE` |
| `elite_variant_bone_carp_tidepiercer` — Приливный костяной карп | `enemy_bone_carp` | Ложная линия перед задержанным настоящим рывком; не реагировать на первый сигнал и ударить после восстановления | `elite`, `line_dash`, `feint`, `recovery` | полоса базовой записи; точное elite-окно `PENDING_BALANCE` | `EliteDirector`, `TelegraphResolver`, `MovementSystem`, `CombatSystem` | `PROPOSED / PENDING_BALANCE / PENDING_ARCHITECTURE` |
| `elite_variant_paper_ghost_sealbreaker` — Призрак-разрушитель печатей | `enemy_paper_ghost` | Оставляет печать ухода и возвращается к отдельной отмеченной точке; сломать печать или сменить маршрут | `elite`, `teleporter`, `mark`, `reposition`, `choice` | полоса базовой записи; точное elite-окно `PENDING_BALANCE` | `EliteDirector`, `EncounterState`, `TelegraphResolver`, `TargetingSystem` | `PROPOSED / PENDING_BALANCE / PENDING_ARCHITECTURE` |
| `elite_variant_jade_toad_mudcrown` — Жабий грязевой венец | `enemy_jade_toad` | После основного прыжка появляется задержанное кольцо меньшей зоны; покинуть первую метку и не вернуться до второго сигнала | `elite`, `leap`, `nested_zone`, `timing`, `area_denial` | полоса базовой записи; точное elite-окно `PENDING_BALANCE` | `EliteDirector`, `ZoneStore`, `TelegraphResolver`, `StatusSystem` | `PROPOSED / PENDING_BALANCE / PENDING_ARCHITECTURE` |
| `elite_variant_mirror_fox_falsepath` — Лиса ложного пути | `enemy_mirror_fox` | Ложный коридор перехватывает приоритет цели, пока настоящая лиса обходит фланг; проверить источник и сохранить линию отхода | `elite`, `decoy`, `flank`, `targeting` | полоса базовой записи; точное elite-окно `PENDING_BALANCE` | `EliteDirector`, `TargetFilter`, `DecoyResolver`, `CombatSystem` | `PROPOSED / PENDING_BALANCE / PENDING_ARCHITECTURE` |
| `elite_variant_bell_crab_resonant_shell` — Краб резонансного панциря | `enemy_bell_crab` | После звона фронтальная защита создаёт конус и поворачивает слабую сторону; обойти импульс и ударить в смену ориентации | `elite`, `guard`, `pulse`, `directional`, `rotation` | полоса базовой записи; точное elite-окно `PENDING_BALANCE` | `EliteDirector`, `DirectionalHitResolver`, `TelegraphResolver`, `CombatSystem` | `PROPOSED / PENDING_BALANCE / PENDING_ARCHITECTURE` |
| `elite_variant_thread_doll_cutline` — Кукла режущей нити | `enemy_thread_doll` | Луч после предупреждения разделяется на две короткие линии, оставляя центральный проход; пересечь проход до фиксации | `elite`, `beam`, `split`, `spacing`, `control` | полоса базовой записи; точное elite-окно `PENDING_BALANCE` | `EliteDirector`, `ProjectileResolver`, `StatusSystem`, `TelegraphResolver` | `PROPOSED / PENDING_BALANCE / PENDING_ARCHITECTURE` |
| `elite_variant_stone_oni_faultline` — Каменный они разлома | `enemy_stone_oni` | После удара по земле проходит одна видимая трещина; сохранить окно восстановления и не пересечь линию вторично | `elite`, `slam`, `faultline`, `heavy`, `recovery` | полоса базовой записи; точное elite-окно `PENDING_BALANCE` | `EliteDirector`, `TelegraphResolver`, `ZoneStore`, `CombatSystem` | `PROPOSED / PENDING_BALANCE / PENDING_ARCHITECTURE` |
| `elite_variant_eclipse_serpent_moonwake` — Змей лунного следа | `enemy_eclipse_serpent` | Дуговой рывок оставляет два коротких следа, которые гаснут последовательно; пересечь путь после первого затухания | `elite`, `dash`, `trail`, `arc`, `route` | полоса базовой записи; точное elite-окно `PENDING_BALANCE` | `EliteDirector`, `TelegraphResolver`, `ZoneStore`, `CombatSystem` | `PROPOSED / PENDING_BALANCE / PENDING_ARCHITECTURE` |

Правило выбора: каждый запуск может выбирать ограниченное подмножество из этого пула; вариант не создаёт второй XP-дроп, сундук или прямую награду поверх базовой смерти. Текущий `AGENT_SYNC_STATE` ограничивает реестр максимум пятью зарегистрированными элитными вариантами, поэтому пул из десяти является контентным предложением и требует отдельного решения Architecture/Product до registry/runtime sync. `EliteDirector` также обязан сохранить конечный выбор и отсутствие постоянной мутации roster.

## 7. Матрица четырёх базовых боссов

Ниже сохранены четыре защищённые идентичности из исходного MAC-контракта. Действующий целевой контракт первого забега уже расширен до 30 минут: две дополнительные записи стоят в отдельных предложенных слотах, а финальная идентичность переносится на финальную контрольную точку. Исторический текст 20 минут/4 босса не используется как единственный действующий контракт.

| ID | Точка появления | Роль, фазы и телеграф | Теги | Граница награды и зависимости | Статус |
|---|---|---|---|---|---|
| `boss_hua_lin` — Хуа Линь | 300 с; первая главная контрольная точка | Проверка маршрута: огненные круги, веер фонарей и перенос безопасной зоны; перед каждой опасностью есть сигнал | `main_boss`, `fire`, `lantern`, `teleport`, `zone` | `BossDirector` → `TelegraphResolver` → факт победы → нефинальный `BOSS_CHEST`; расчёт в `RewardLedger` | `EXISTING_PROTECTED_CONTENT` |
| `boss_miyeon` — Миён | 600 с; вторая главная контрольная точка | Проверка выбора цели: истинное тело, копии, отражение снарядов и временные стены; раскрытие источника — окно чтения | `main_boss`, `mirror`, `decoy`, `wall`, `redirect` | `BossDirector` → `DecoyResolver` → `ChestResolver`; копия не создаёт второй XP/сундук/награду | `EXISTING_PROTECTED_CONTENT` |
| `boss_seika` — Сэйка | 900 с; третья главная контрольная точка | Проверка пространства: дуги клинка, нефритовые столбы и отмеченный удар по земле; снятие защиты открывает вторую фазу | `main_boss`, `guard`, `melee`, `column`, `phase_break` | `BossDirector` → `DirectionalHitResolver` → состояние фазы → нефинальный `BOSS_CHEST` | `EXISTING_PROTECTED_CONTENT` |
| `boss_black_moon_empress` — Императрица Чёрной Луны | 1800 с; финальная точка действующего целевого контракта; исторически 1200 с | Финальная проверка билда: вращающиеся лезвия, диагональные лучи, призванные элиты и читаемое окно снятия печатей | `final_boss`, `darkness`, `seal`, `elite_summon`, `final_settlement` | `BossDirector` → финальная победа → итог забега; финальный `BOSS_CHEST` запрещён, артефактное предложение отдельно | `EXISTING_PROTECTED_CONTENT / RETIMING_PENDING` |

Параметры HP, фазовых порогов, времени предупреждения, урона, призывов, сопротивлений и целевого времени убийства — `PENDING_BALANCE`. Художественный образ и производство принадлежат Visual Lab.

### Два предложения расширения главных боссов

| Слот | ID | Рабочее имя | Точка появления | Роль и теги | Статус |
|---|---|---|---:|---|---|
| `boss_extension_slot_04` | `boss_tideglass_regent` | Регент Чёрного Прилива | 1200 с | Управляет видимыми дугами потока и временными коридорами; `flow`, `arc`, `route`, `phase` | `PROPOSED / REGISTRY_SYNC_PENDING` |
| `boss_extension_slot_05` | `boss_omen_paper_archivist` | Архивариус Лунных Знаков | 1500 с | Раскладывает читаемую последовательность знаков и временных зон; `sequence`, `seal`, `zone`, `vulnerability` | `PROPOSED / REGISTRY_SYNC_PENDING` |

Оба расширения создают один нефинальный `BOSS_CHEST` с синергией или резервным результатом; артефактное предложение и прямое изменение кошелька запрещены.

### Пять предложенных мини-боссов

| ID | Точка появления | Роль и проверяемый навык | Теги | Зависимости | Награда / статус |
|---|---:|---|---|---|---|
| `miniboss_ink_jade_warden` — Чернильный Нефритовый Страж | 450 с | Читать сходящиеся линии печатей и менять маршрут | `mini_boss`, `line`, `zone`, `route` | `BossDirector`, `TelegraphResolver`, `ZoneStore`, `RewardLedger` | один `BOSS_CHEST`; `PROPOSED / REGISTRY_SYNC_PENDING` |
| `miniboss_veil_harvester` — Жнец Завесы | 750 с | Переждать срез завесы и выбрать безопасное окно атаки | `mini_boss`, `sweep`, `veil`, `recovery` | `BossDirector`, `TelegraphResolver`, `MovementSystem`, `ChestResolver` | один `BOSS_CHEST`; `PROPOSED / REGISTRY_SYNC_PENDING` |
| `miniboss_lotus_ritekeeper` — Хранительница Лотосового Обряда | 1050 с | Разобрать якоря защиты и не потерять проход | `mini_boss`, `anchor`, `support`, `zone` | `BossDirector`, `TargetFilter`, `TelegraphResolver`, `RewardLedger` | один `BOSS_CHEST`; `PROPOSED / REGISTRY_SYNC_PENDING` |
| `miniboss_bell_rhythm_ascetic` — Колокольный аскет | 1350 с | Читать ритм колец и перемещаться через заранее видимый зазор | `mini_boss`, `ring`, `rhythm`, `movement` | `BossDirector`, `TelegraphResolver`, `ProjectileResolver`, `CleanupRegistry` | один `BOSS_CHEST`; `PROPOSED / REGISTRY_SYNC_PENDING` |
| `miniboss_moonroot_ferryman` — Луннокорневой перевозчик | 1650 с | Пересекать меняющийся маршрут конвоя и не терять приоритетную цель | `mini_boss`, `convoy`, `route`, `drag` | `BossDirector`, `MovementSystem`, `TargetFilter`, `RewardLedger` | один `BOSS_CHEST`; `PROPOSED / REGISTRY_SYNC_PENDING` |

Мини-босс продолжает `run_elapsed_seconds`, волны, XP и обычный спавн. Главный босс по текущему sync-контракту замораживает видимые часы забега, часы волн, XP и обычный спавн от вступления до `settlement`; часы встречи отделены. Это поле требует подтверждения архитектуры/исполнения, а не нового контента.

## 8. Синергии, сундуки и зависимости забега

В действующем конверте 30 минут предусмотрены 10 нефинальных окон `BOSS_CHEST`: главные боссы на 300, 600, 900, 1200 и 1500 с, мини-боссы на 450, 750, 1050, 1350 и 1650 с. Они могут открыть синергию или полезный резервный результат. Максимум подтверждённых синергий — 5; наличие десяти окон не гарантирует пять полученных синергий.

Пять отдельных окон `ELITE_CHEST` предназначены для артефактного/обычного улучшения и не расходуют лимит синергий. Пул из десяти предложенных элитных вариаций не означает одновременную регистрацию десяти вариантов: текущий sync-контракт ограничивает реестр пятью, а точный selection policy принадлежит Architecture/Runtime. Финальный босс на 1800 с не создаёт сундук босса.

Проверка `SynergyResolver`:

```yaml
synergy_run_policy:
  catalog_size: 10
  max_claimed_per_run: 5
  eligible_encounter_kinds: [MAIN_BOSS, MINI_BOSS]
  weapon_level: 6
  passive_rank: 5
  weapon_not_evolved: true
  final_boss_chest: forbidden
  after_cap: FALLBACK_REQUIRED
  duplicate_claim: idempotent_noop
```

Один сундук подтверждает не больше одной синергии. Невыбранная карта не считается полученной. Если пара не собрана или лимит достигнут, сундук выдаёт обычное улучшение либо результат `RewardLedger`; пустой экран и скрытая шестая синергия запрещены.

## 9. Карта зависимостей и границы владельцев

| Контентная поверхность | Обязательные потребители | Что эта поверхность не должна владеть |
|---|---|---|
| Оружие и пассивки забега | `ContentRegistry`, `BuildInventory`, `UpgradeOfferSystem`, `StatsCalculator` | окончательные числа, кошелёк, право управления интерфейсом |
| Синергии/эволюции | `SynergyEvaluator`, `BossChestSystem`, `EvolutionState`, `VFXCleanup` | артефактное предложение, финальный сундук, скрытая замена пассивки |
| Артефакты | `ArtifactOfferSystem`, `ArtifactEffectSystem`, типизированные правила trigger/target/stack, проекция HUD | слоты оружия/пассивок, `BOSS_CHEST`, прямое изменение постоянного кошелька |
| Противники | `WaveDirector`, `EnemyRegistry`, `TelegraphResolver`, `CombatSystem`, `XPDrop` | награды контрольных точек и постоянная мутация состава |
| Боссы и мини-боссы | `BossDirector`, часы встречи, `TelegraphResolver`, `ChestResolver`, `RewardLedger` | баланс HP/урона, художественное approval, прямое начисление кошелька |
| Дерево магазина | `MetaProgression`, `StatsCalculator`, `Wallet`, проекция UI | временные пассивки забега, эффект артефакта и предложение улучшения во время забега |
| Визуальные задания | маршрут семейств/шаблонов/манифестов Visual Lab | PNG/SVG, утверждение candidate, golden и перевод в production |
| Числовая передача | B1 / `BALANCE_MODEL` и профильная симуляция | второй источник чисел и скрытые тестовые коэффициенты |

## 10. Спорные места для баланса, экономики и архитектуры

| Вопрос | Текущая граница | Статус |
|---|---|---|
| Четыре базовых босса против действующего конверта 6 главных + 5 мини | Сохраняем четыре защищённые идентичности, два расширения и пять мини как отдельные предложения; финальное сопоставление реестра не выполняем молча | `PENDING_ARCHITECTURE / PENDING_PRODUCT_DECISION` |
| Десять базовых/обычных записей плюс десять элитных вариаций | Базовый пул содержит 10 записей; две из них уже имеют `ELITE_FAMILY`, а новые 10 вариантов описаны отдельными `PROPOSED` IDs | `PENDING_PRODUCT_DECISION / PENDING_ARCHITECTURE` |
| Артефакты 10 против 8 записей в архитектурном реестре | Два ID сохраняются как `PROPOSED`; нужны типизированные определения, правила повторов, обновления и дубликата | `REGISTRY_SYNC_PENDING` |
| Часы главного босса | `AGENT_SYNC_STATE` требует заморозки видимых часов, но старые документы содержат противоположное правило | `PENDING_ARCHITECTURE` |
| Поздний состав волн и усиленные типы | Точки первой появления указаны, но веса, активный лимит, ритм и продолжение после 20 минут не заданы | `PENDING_BALANCE` |
| HP, урон, скорость, длительность, частота, дальность, стоимость и целевое время убийства | Все значения должны прийти из одного B1/`BALANCE_MODEL` источника | `PENDING_BALANCE` |
| Распределение десяти покупок по 17 узлам магазина | Топология и поперечные зависимости описаны, цены и ранги не закрыты | `PENDING_BALANCE / PENDING_PRODUCT_DECISION` |
| Сундук босса и артефактное предложение | Каналы разделены; конкретные награды, резервный результат и ритм требуют единого реестра | `PENDING_BALANCE / PENDING_ARCHITECTURE` |
| Визуальные силуэты и эффекты | Этот пакет даёт краткие задания; Visual Lab должен пройти собственные ворота и получить пользовательское approval | `ARTISTIC_PENDING` |

## 11. Область исключений и приёмка

- Матрица содержит 10 связок оружие-пассивка-синергия, 10 общих пассивок забега, 10 артефактов, 10 базовых/обычных записей противников, 10 отдельных элитных вариаций и 4 базовых босса.
- Полное дерево магазина содержит 17 узлов в `META_PASSIVE_TREE.md` и не смешивается с десятью временными пассивками.
- Два `boss_extension_slot_*` и пять `miniboss_*` имеют явно обозначенный статус `PROPOSED / REGISTRY_SYNC_PENDING`; они не объявлены утверждёнными итоговыми ID.
- Десять новых `elite_variant_*` ID добавлены только как `PROPOSED`; ни один не повышен до `APPROVED`, `PRODUCTION` или runtime-ready.
- Не изменялись `AGENTS.md`, корневые документы, баланс, архитектура, runtime, Visual Lab и `docs/mockups/`.
- В `docs/agents/content-design/` нет пустого текстового/JSON мокап-файла, который требовал бы заполнения; PNG/SVG не создавались.
- Матрица и ссылки на исходные ревизии являются документальным доказательством, а не доказательством исполнения, Godot/Android, баланса или художественной приёмки.

## 12. Блокеры

1. Архитектура и владелец продукта должны выпустить одно непротиворечивое сопоставление четырёх защищённых базовых боссов с действующим конвертом 6 главных боссов и 5 мини-боссов.
2. Архитектура и исполнительный агент должны добавить в потребляемый реестр два предложенных главных босса, пять мини-боссов и два недостающих типизированных описания артефактов, не меняя ID молча.
3. Агент баланса должен закрепить одну числовую таблицу для десяти оружий, десяти пассивок, десяти артефактов, десяти базовых противников, десяти элитных вариаций, боссов, волн, сундуков, резервных результатов и дерева магазина.
4. Architecture/Product должны решить конфликт между контентным пулом из 10 элитных вариаций и текущим лимитом реестра максимум 5 зарегистрированных вариантов; без этого новые ID остаются `PROPOSED` и не поступают в runtime.
5. Visual Lab должен отдельно принять или отклонить краткие визуальные задания; этот документ не создаёт и не утверждает графику.

## 13. Следующее действие

Владелец продукта и Architecture owner публикуют одно решение: принять пул из 10 элитных вариаций с bounded runtime selection либо сопоставить его с текущим лимитом 5 зарегистрированных вариантов; до этой публикации Balance и Runtime используют только статус `PROPOSED`.
