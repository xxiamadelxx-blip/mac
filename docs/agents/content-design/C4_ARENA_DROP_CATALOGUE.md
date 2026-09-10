# C4 — Каталог дропов арены

Статус пакета: CONTENT_SPECIFIED

Это content proposal для временных предметов на арене. Он не является runtime implementation, numeric balance lock, save-schema change, Visual Lab approval или production-asset delivery.

## 1. Цель и границы

Arena drop должен дать игроку короткое решение: «Забрать возможность сейчас или сохранить позицию и переждать угрозу?» Семь обязательных семейств закрывают восстановление, Gold, XP-сбор, снятие угроз, окно движения, защиту и harvest.

Дополнительные proposals не добавляются: семь обязательных семейств уже покрывают требуемые решения. Новый эффект без отдельной продуктовой потребности размоет drop table и runtime contract.

В C4 не входят числовые значения, частота, drop-table weights, количество, радиусы, длительности, новые canonical events/schema, изменение оружия/пассивок/артефактов/meta tree, boss chest/synergy/artifact offer, мокапы и production assets.

## 2. Общий контракт

| Поле | Content contract |
|---|---|
| drop_id | один из семи stable IDs раздела 3 |
| drop_instance_id | уникален внутри run; повторный pickup не удваивает effect/reward |
| source_context | approved combat/drop-table source; не назначается молча каждому врагу |
| world_position | доступная точка арены; не блокирует движение и не заменяет aftermath |
| pickup_state | active → collected или rejected/expired по entry rules |
| effect_state | activation/effect/expire/cleanup; schema — PENDING_ARCHITECTURE |
| reward_reference | только для currency/XP projection, без второго ledger |
| visual_lifecycle | spawn → idle → pickup/activation → impact/expire → cleanup |

### Lifecycle и boundaries

1. Balance и Architecture определяют approved source, cadence и instance schema; Content не объявляет выпадение из каждого enemy ID.
2. DropSystem размещает item вне стены, поверх героя и вне зоны, где signal скроет lethal telegraph.
3. PickupResolver проверяет героя, стены и active/rejected state; teleport-through-wall и silent auto-grant запрещены.
4. Resolve атомарен: повторный pickup, reconnect или повторная команда не удваивают effect, XP или currency.
5. После cleanup instance не участвует в collision, target query или визуальном слое.

- XP остаётся в xp_drop и существующем xp_drop_collected.v1; arena drop не выдаёт XP напрямую и не меняет XP formula/grades.
- aftermath_item остаётся отдельным слоем: drop не превращает corpse/decal в pickup и не удаляет последствия боя.
- Coin предлагает Gold через RewardLedger settlement boundary; direct persistent wallet write не разрешён. Moon Seals/Boss Essence не являются alias.
- Boss chest, synergy/evolution, artifact offer и final reward остаются отдельными surfaces. Freeze не останавливает run clock/checkpoint.
- Новые activation/resolve events и поля не названы canonical этим документом; Architecture/Runtime должны версионировать их отдельно.

## 3. Каталог

### 3.1 arena_drop_heal_mote — Нефритовая капля
**Promise:** Подбери каплю и верни себе часть здоровья.
**Player decision / counterplay:** Идти за лечением после урона или удерживать безопасную позицию; при full HP риск за предмет не оправдан.
**Визуальный сигнал**
- Тёплая ivory-капля с soft-jade halo и кольцевым spawn impulse.
- Силуэт капли внутри незамкнутого лепесткового кольца читается формой и idle-пульсацией.
- Pickup bloom и full-HP rejection — разные состояния, без вспышки поверх lethal telegraph.
**Pickup rule**
- Обычный contact pickup героя; при заполненном HP подбор отклоняется, instance остаётся active, игрок получает rejected feedback.
- По умолчанию не входит в harvest whitelist vacuum, чтобы лечение оставалось отдельным маршрутом.
- Не проходит через стены, не блокирует движение и не становится XP/aftermath item.
**Effect intent**
- Запрос в обычный health/healing pipeline с восстановлением current HP до max HP.
- Не создаёт shield, XP, Gold, Moon Seals или Boss Essence.
- Совместимость с meta_vitality_mote_healing и healing artifacts проверяется отдельно; это не weapon/passive buff.
**Feedback**
- Jade bloom на героине, мягкий glass/water sound и flash health bar.
- Показывается фактический heal delta; при нулевом effective heal — rejected feedback.
- Spawn, idle, pickup и cleanup имеют отдельные фазы.
**Limitations**
- Нет overheal, resurrection, permanent max-HP change или автоматического shield.
- Не активируется при full HP и не запускает recursive healing triggers.
- Не выдаёт reward только за факт подбора.
**PENDING_BALANCE**
- approved source tiers, drop-table weight, cadence/frequency и safe-spawn spacing
- healing amount, current/max HP model и item lifetime
- pickup boundary, duplicate/overlap handling и performance cap
- interaction с meta_vitality_mote_healing и artifact healing triggers
**PENDING_ARCHITECTURE**
- canonical health effect payload, rejected-pickup result и idempotency key
- vacuum/harvest whitelist и trigger guard против recursive healing
### 3.2 arena_drop_coin_cache — Лунная монета
**Promise:** Рискни маршрутом и добавь Gold в награду за этот забег.
**Player decision / counterplay:** Выбрать безопасный путь без монеты или обойти плотную волну ради постоянной currency-награды.
**Визуальный сигнал**
- Небольшая muted-brass монета с прорезью-полумесяцем и ivory-кромкой.
- Медленный idle-поворот, brass glint и собирающееся кольцо при pickup; не полагаться только на цвет.
- UI feedback не закрывает арену крупной плашкой.
**Pickup rule**
- Подбор при контакте с pickup boundary.
- Может входить в vacuum whitelist после RewardLedger review.
- Не проходит через стены; обычная смерть каждого врага не получает скрытое правило «всегда монета».
**Effect intent**
- Proposal: добавить Gold в run-earned currency через существующий RewardLedger/settlement boundary.
- Content entry не мутирует persistent wallet и не позволяет тратить Gold в арене.
- Moon Seals и Boss Essence не являются alias этой монеты.
**Feedback**
- Короткий coin chime, tick run currency counter и уход монеты к UI anchor.
- Feedback означает принятую запись, а не уже совершённую persistent save commit.
- Duplicate delivery даёт no-op без второго начисления.
**Limitations**
- Не открывает artifact offer, boss chest или synergy/evolution.
- Не начисляет XP, не меняет уровень и не заменяет checkpoint rewards.
- Не даёт Moon Seals/Boss Essence и не меняет shop price внутри run.
**PENDING_BALANCE**
- currency source tiers, drop-table weight, cadence/frequency и safe-spawn
- Gold quantity/value per instance и item lifetime
- pickup boundary, run-carry cap и reward visibility cadence
- duplicate instances и interaction with vacuum

**PENDING_PRODUCT_DECISION**

- подтвердить Gold как wallet target и label «Gold»/«монета»
- подтвердить момент отображения: run total, settlement preview или оба
**PENDING_ARCHITECTURE**
- currency pickup payload, RewardLedger idempotency key и settlement timing
- запрет silent wallet write из DropSystem
### 3.3 arena_drop_xp_magnet — Лунный магнит опыта
**Promise:** Собери лежащий XP, не заходя в опасную плотность.
**Player decision / counterplay:** Забрать магнит сейчас для безопасного сбора или сохранить его до накопления XP за спиной.
**Визуальный сигнал**
- Jade-линза с двумя ivory-дугами; дуги замыкаются и размыкаются на spawn.
- После активации тонкие arcs ведут к eligible XP items, не проходят через стены и не превращаются в screen wash.
- Shape, sound и motion отличаются от обычного XP crystal и vacuum bloom.
**Pickup rule**
- Герой сначала подбирает сам magnet instance обычным способом.
- Затем attraction query действует на eligible xp_drop; фактический сбор идёт по существующему xp_drop_collected.v1.
- Не притягивает currency, healing, ward, freeze или destruction items; уже collected XP не возвращается в query.
**Effect intent**
- Run-scoped attraction к существующим XP items без изменения XP formula, grade value, level curve или reward ledger.
- Текущий source contract использует XP. UI label «mana» — PENDING_PRODUCT_DECISION.
- Если mana станет отдельным ресурсом, нужен отдельный content ID и Architecture contract.
**Feedback**
- Радиальный pulse, дуги к героине, flash XP bar на фактическом collect и resonant sound.
- После очистки области glow завершается сам.
- Pooling/aggregation XP не теряет суммарное значение.
**Limitations**
- Не создаёт XP и не гарантирует сбор вне effect scope.
- Не проходит сквозь стены, не собирает chest/artifact offer и не применяет settlement.
- Не продлевает забег и не становится permanent meta/passive stat.
**PENDING_BALANCE**
- source tiers, drop-table weight, cadence/frequency и safe-spawn
- attraction radius, duration, travel behavior и concurrent target cap
- eligible XP grades, wall/line-of-sight policy и performance budget
- interaction with existing pickup radius и mana-vs-XP presentation
**PENDING_ARCHITECTURE**
- activation payload/lifecycle schema
- mapping к XP collection path без duplicate collection
- semantics при meta_magnet_mana_gain с runtime resource XP
### 3.4 arena_drop_destruction_seal — Печать разрушения
**Promise:** Сотри отмеченные угрозы, пока волна не сомкнулась.
**Player decision / counterplay:** Сохранить заряд для density spike или расчистить путь к XP и другим pickup раньше.
**Визуальный сигнал**
- Разомкнутая muted-crimson/violet seal с ivory-трещиной и smoky-teal inner ring.
- На spawn трещина раскрывается одним импульсом; pickup wave остаётся в effect scope.
- Signal не toxic-neon и не маскируется под lethal attack telegraph.
**Pickup rule**
- Contact pickup; после успешного collect activation начинается один раз.
- Работает только по target whitelist/effect scope, которые закрепят Balance и Architecture.
- Boss и mini-boss защищены базовым proposal; elite inclusion — отдельное решение.
**Effect intent**
- Запросить в Combat/Wave resolution уничтожение или defeat eligible ordinary threats в объявленной зоне.
- Если enemy defeated, один standard death/reward path; если removed — Runtime/Balance явно определяют reward outcome.
- Не является прямым wallet/XP grant и не обходит boss encounter.
**Feedback**
- Fracture wave в scope, короткий low-impact sound, target markers и cleanup.
- Feedback не перекрывает героя, XP и danger telegraphs.
- No-target result читаем, reward records idempotent.
**Limitations**
- Boss/mini-boss, checkpoint, boss chest, artifact offer и persistent reward не уничтожаются.
- Не меняет run clock, не пропускает stage и не гарантирует defeat elite.
- Не создаёт вторую волну наград и не активируется повторно из одного instance.
**PENDING_BALANCE**
- source tiers, drop-table weight, cadence/frequency и availability window
- effect scope, target count/whitelist и elite interaction
- damage/defeat/removal model, kill credit, XP/aftermath output
- activation timing, cleanup latency, performance cap и reward value
**PENDING_ARCHITECTURE**
- canonical destruction request/resolve schema
- atomic target selection, boss immunity, idempotency и cleanup
- единый результат defeated vs removed без потери/дублирования наград
### 3.5 arena_drop_wave_freeze — Печать остановленной волны
**Promise:** Останови натиск и верни себе окно для движения.
**Player decision / counterplay:** Подобрать перед ordinary pressure spike или сохранить freeze для будущей плотной волны.
**Визуальный сигнал**
- Ivory hourglass внутри smoky-teal ring; частицы визуально зависают, а не вспыхивают.
- Affected ordinary actors получают читаемый freeze contour и suspended motes.
- При expire ring размыкается и звучит отдельный release.
**Pickup rule**
- Contact pickup, activation один раз на instance.
- Default target — ordinary wave actors и ordinary spawn pressure; boss/mini-boss, run clock и checkpoint state не замораживаются.
- XP и currency pickup остаются активными; через стены предмет не проходит.
**Effect intent**
- Временно применить freeze state к eligible ordinary enemies и, после Architecture sync, к ordinary spawn pressure.
- Run clock продолжает идти в RUN_ACTIVE, BOSS_INTRO и BOSS_ACTIVE; checkpoint не переносится.
- Active hostile wind-up/telegraph остаётся читаемым; resume/cancel и projectile/hazard policy требуют sync.
**Feedback**
- Jade/ivory pulse на героине, freeze marker на actor и небольшой HUD state indicator.
- Audio/haptic подтверждают activation/release; screen flash не закрывает telegraphs.
- No-target/no-pressure result понятен игроку.
**Limitations**
- Не замораживает boss/mini-boss encounter, run clock, pause/offer/settlement/terminal state или checkpoint rules.
- Не уничтожает enemies, не выдаёт XP/Gold и не открывает reward surface.
- Не складывается в бесконечный lock; stacking/refresh policy должна быть явной.
**PENDING_BALANCE**
- source tiers, drop-table weight, cadence/frequency и availability window
- freeze duration, target whitelist, spawn-pressure policy и recovery behavior
- stacking/refresh, target cap, performance budget и boss/elite resistance
- active telegraph/projectile/hazard interaction
**PENDING_ARCHITECTURE**
- state transition schema, wind-up pause/resume/cancel и deterministic expiry
- WaveDirector/CombatSystem ownership
- idempotency при повторном activation/reconnect
### 3.6 arena_drop_ward_shard — Осколок оберега
**Promise:** Подбери оберег и переживи одну опасную ошибку.
**Player decision / counterplay:** Идти за защитой заранее или сохранить её для участка с высокой ценой ошибки.
**Визуальный сигнал**
- Warm-ivory/jade shard с контуром bell-seal и muted-brass suspension line.
- После pickup вокруг героя — тонкий orbit; при impact он crack-ится и очищается.
- Это ground item, который становится кратким defensive state, а не passive card/artifact.
**Pickup rule**
- Contact pickup с немедленной активацией.
- Если ward active, default proposal — не собирать второй instance и не делать silent overwrite.
- Не проходит через стены и не входит в vacuum whitelist по умолчанию.
**Effect intent**
- Создать run-scoped ward, который поглощает или снижает eligible incoming damage по mitigation model.
- Не увеличивает max HP и не становится permanent damage-taken passive.
- Срабатывание проходит guarded damage-resolution path; boss/elite behavior задаётся whitelist/resistance.
**Feedback**
- Seal orbit, приглушённый bell hit при impact, crack state и короткий haptic confirmation.
- HUD показывает active/consumed shape/pip без незакреплённых чисел.
- Expire/consume cleanup не путается с enemy telegraph.
**Limitations**
- Не resurrection, unconditional invulnerability или защита от каждого death/arena-boundary outcome.
- Не лечит HP, не даёт XP/Gold и не открывает chest/artifact offer.
- По умолчанию не stack-ится и не refresh-ится; один instance — один guarded effect.
**PENDING_BALANCE**
- source tiers, drop-table weight, cadence/frequency и availability window
- mitigation/absorption, charge behavior, duration и eligible damage types
- boss/mini-boss/elite resistance, stacking/refresh и duplicate handling
- activation/impact timing и performance/VFX budget
**PENDING_ARCHITECTURE**
- ward state schema, guarded damage resolver и consumed/expired idempotency
- damage-type whitelist, lethal-hit boundary и in-run save/reconnect behavior
### 3.7 arena_drop_vacuum_bloom — Цветок сбора
**Promise:** Собери всё подходящее вокруг себя одним точным импульсом.
**Player decision / counterplay:** Дождаться, пока XP/coin накопятся локально, и выбрать момент pulse без нового risk route.
**Визуальный сигнал**
- Jade bud с тёплой ivory-серединой и muted-brass лепестковыми линиями.
- Pickup раскрывает локальный ring; от eligible items идут inward arcs, затем bloom закрывается.
- В отличие от magnet, vacuum делает один bounded harvest pulse, а не ведёт предметы во времени.
**Pickup rule**
- Contact pickup запускает один bounded harvest query.
- Default eligible set — существующие XP drops и arena_drop_coin_cache; healing/ward/freeze/destruction не активируются автоматически.
- Query уважает walls/line-of-sight и не собирает chest, artifact offer, aftermath или предметы вне scope.
**Effect intent**
- Немедленно собрать eligible ground resources, сохраняя обычные XP и RewardLedger semantics.
- Не меняет XP values, Gold quantity, pickup_radius meta rank или reward surfaces.
- Это catch-up tool для cluttered field, а не global auto-loot.
**Feedback**
- Один outward/inward bloom, мягкие XP/coin pickup ticks и HUD pulse по фактическим результатам.
- Пустой pulse получает короткий no-target feedback.
- Cleanup закрывает дугу и не оставляет ложные pickup markers.
**Limitations**
- Не проходит через стены, не увеличивает values и не запускает utility effects чужих drop families.
- Не собирает aftermath, boss chest, artifact offer или final settlement.
- Не повторяется после cleanup; eligible set/radius/target cap не закреплены.
**PENDING_BALANCE**
- source tiers, drop-table weight, cadence/frequency и availability window
- harvest radius, target cap, line-of-sight cost и query timing
- eligible XP grades/currency instances и clustered/pooling interaction
- performance budget и feedback cadence for many targets
**PENDING_ARCHITECTURE**
- bounded harvest query schema и per-target idempotency
- shared resolver XP/Gold без cross-wallet duplication
- explicit target whitelist при возможном будущем healing harvest

## 4. Различие решений игрока

| Drop | Сильный момент | Осознанный риск/отказ |
|---|---|---|
| Heal mote | после урона | крюк через угрозу; full HP снижает ценность |
| Coin cache | безопасное окно для currency route | потеря позиции ради долгосрочной награды |
| XP magnet | XP за спиной или в плотности | сохранить предмет до безопасного сбора |
| Destruction seal | peak density/закрывающийся проход | заряд для будущего pressure spike |
| Wave freeze | перед ordinary telegraph/spawn pressure | раннее спасение против запаса на будущее |
| Ward shard | участок с высокой ценой ошибки | момент защитного pickup и отсутствие stack |
| Vacuum bloom | накопленное локальное поле | дождаться pulse, не войти в новый risk route |

Magnet отличается от vacuum: magnet ведёт eligible XP к герою во времени, vacuum делает один bounded harvest pulse. Heal/ward не являются flat passives, destruction/freeze не являются skip boss кнопками.

## 5. Cross-system handoff

| Owner | Contract | Boundary |
|---|---|---|
| Content Registry | семь stable IDs и effect-family metadata | registry/schema sync — PENDING_ARCHITECTURE |
| DropSystem | source context, safe spawn, instance lifecycle | не генерирует скрытые XP/wallet grants |
| PickupResolver/Input | eligibility, wall rule, rejection, idempotency | новые event names не объявлены |
| CombatSystem | heal, ward, destruction, freeze intent | target/mitigation/kill resolution — PENDING |
| WaveDirector | ordinary spawn-pressure freeze proposal | boss/checkpoint/run-clock ownership не меняется |
| XpDropStore/ProgressionSystem | XP magnet/vacuum collection | сохраняет xp_drop_collected.v1 |
| RewardLedger | coin cache settlement proposal | Gold target/timing требуют sync |
| HUD/Renderer/Audio/Haptics | spawn, idle, active, impact, expire, rejected feedback | masters делает Visual Lab |

Минимальные semantic requirements для Architecture/Runtime: drop_instance_id, drop_id, run_id, source/world position, pickup/effect/cleanup state, target/reward references, per-target idempotency, wall/LOS policy, safe-spawn reference и owner system для health, XP, Gold, combat и wave state. Это не новый canonical JSON schema.

## 6. Visual Lab brief (без мокапов)

- Palette: deep blue-grey, smoky teal, warm ivory, muted brass, soft jade; muted crimson/violet — только role/status accent.
- Silhouette-first: капля, монета, линза, треснувшая seal, hourglass, bell shard и lotus bloom различимы в true 1× combat scale.
- Каждый master показывает spawn, idle, pickup/activation, active/impact, expire/cleanup и rejected/full/active state, если применимо.
- Никакого toxic neon, black-on-black, размера с героя или overlay поверх lethal telegraph.
- Проверка: 390×844 UI/combat, cluttered late-run aftermath/XP layer, telegraph visibility и cleanup.
- Suggested intake: SPRITE + VFX + UI_ART, docs/mockups/02-arena/ и docs/mockups/09-xp/; candidate IDs назначает Visual Lab.
- C4 не создаёт mockups, PNG/SVG или production candidate.

## 7. Незакрытые решения

| Вопрос | Owner | Статус/следующий шаг |
|---|---|---|
| Source tiers, cadence и drop-table ownership | Balance + Product | PENDING_BALANCE/PENDING_PRODUCT_DECISION — bind weights |
| Gold target и settlement presentation | Product + Architecture | PENDING_PRODUCT_DECISION — approve wallet/UI timing |
| XP или mana label/semantics | Product + Architecture | PENDING_PRODUCT_DECISION — resolve before mapping |
| Destruction defeat vs removal reward | Product + Balance + Runtime | PENDING_PRODUCT_DECISION/PENDING_ARCHITECTURE — choose path |
| Freeze actor/projectile/wind-up scope | Architecture + Balance | PENDING_ARCHITECTURE/PENDING_BALANCE — define lifecycle |
| Ward mitigation/lethal boundary/duplicate | Balance + Runtime | PENDING_BALANCE/PENDING_ARCHITECTURE — bind guards |
| Vacuum target whitelist | Product + Balance | PENDING_PRODUCT_DECISION/PENDING_BALANCE — preserve utility distinction |
| Drop schema/events/reconnect | Architecture/Runtime | PENDING_ARCHITECTURE — add canonical contract/tests |

## 8. Acceptance и статус

- [x] Есть ровно семь обязательных arena drop IDs; дополнительные proposals не добавлялись.
- [x] Для каждого ID заполнены visual signal, pickup rule, effect intent, feedback, limitations и PENDING_BALANCE fields.
- [x] У семи entries разные player decisions/counterplay и явные ограничения.
- [x] XP/aftermath, boss chest, artifact offer, synergy и final reward boundaries сохранены.
- [x] Frequency, quantity, duration, radius, target cap и values оставлены Balance Agent.
- [x] New runtime events/schema не объявлены canonical; sync points переданы Architecture/Runtime.
- [x] Visual brief отделён от production asset; mockups/candidate IDs не создавались.
- [x] Planned write scope ограничен docs/agents/content-design/.
- [ ] Balance Agent: numeric/source cadence binding.
- [ ] Architecture/Runtime: Registry, instance/effect schema, event names и idempotency.
- [ ] Visual Lab: masters/mockups по своим gates.

Итоговый статус C4: CONTENT_SPECIFIED, не RUNTIME_READY, не BALANCE_LOCKED, не VISUAL_APPROVED.

## 9. Следующий шаг

После принятия C4 Content Agent выполняет C5: catalog index, dependency matrix, duplicate/conflict review, cross-agent handoff и acceptance evidence. C4 не закрывает решения Balance, Architecture/Runtime или Visual Lab.
