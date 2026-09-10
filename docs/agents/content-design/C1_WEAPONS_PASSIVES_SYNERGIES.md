# C1 — Оружие, пассивки и синергии первого забега

Статус пакета: `CONTENT_SPECIFIED`

Это контентный контракт, а не баланс и не runtime implementation. Все значения урона, cadence, cooldown, дальности, размера, длительности, вероятности и лимитов передаются Balance Agent как `PENDING_BALANCE`.

## 1. Общий контракт первого забега

| Правило | Контракт |
|---|---|
| Пул | 10 weapons + 10 run passives |
| Одновременно в билде | максимум 6 weapon slots и 6 passive slots |
| Weapon progression | максимум уровня 6 по архитектурному контракту |
| Passive progression | максимум ранга 5 по архитектурному контракту |
| Upgrade offer | три карточки; New/Upgrade/Evolution — разные outcome types |
| Evolution gate | weapon max level + paired passive max rank + non-final boss chest + weapon not evolved |
| Synergy catalogue | 10 стабильных direct pairs |
| Synergy claims per run | **не более 3**; это пользовательское product decision для Run 1 |
| Synergy windows | рекомендуются нефинальные boss chest на 5/10/15 минутах |
| Final boss | не создаёт boss chest и не выдаёт четвёртую synergy |
| Если подходящей пары нет | существующий fallback contract, значение назначает Balance/Product |

### Разделение сущностей

- **Run passive** — временный элемент билда, занимает один из шести passive slots и улучшается внутри забега.
- **Synergy/evolution** — преобразует конкретное оружие после выполнения gate; не добавляет новый slot.
- **Meta tree node** — постоянное улучшение за Gold, описано отдельно в `META_PASSIVE_TREE.md`; не является run passive.
- **Artifact** — отдельный run modifier без slot capacity; описан в `C2_ARTIFACTS.md`.

## 2. Карта десяти пар

| weapon_id | Оружие | passive_id | Пассивка | synergy_id | Результат эволюции | Build decision |
|---|---|---|---|---|---|---|
| `weapon_moon_blade` | Лунный клинок | `passive_wind_of_travel` | Ветер странствий | `synergy_moon_dance` | Танец Луны | держать ближнюю дистанцию и менять направление |
| `weapon_jade_talismans` | Нефритовые талисманы | `passive_jade_focus` | Нефритовый фокус | `synergy_heavenly_seals` | Небесные печати | помечать цели и выбирать момент цепной детонации |
| `weapon_crimson_flame_fan` | Веер багрового пламени | `passive_ember_heart` | Сердце углей | `synergy_phoenix_sky` | Феникс алого неба | поддерживать горящие зоны и направлять проход птицы |
| `weapon_frost_pearl` | Ледяная жемчужина | `passive_frost_thread` | Морозная нить | `synergy_winter_palace` | Дворец вечной зимы | замедлять поток и удерживать врагов в выгодных точках |
| `weapon_thunder_needles` | Иглы грома | `passive_heavenly_seal` | Небесная печать | `synergy_heavenly_judgment` | Приговор небес | создавать плотность целей для цепи, не теряя телеграфы |
| `weapon_spirit_bell` | Колокол духов | `passive_iron_bell` | Железный колокол | `synergy_guardian_bell` | Звон защитницы | выбирать момент защиты от снарядов вместо постоянного урона |
| `weapon_fox_mirage` | Лисий мираж | `passive_mirror_shard` | Осколок зеркала | `synergy_nine_reflections` | Девять отражений | направлять атаки в коридоры и фланги, а не только в ближайшую цель |
| `weapon_lotus_mines` | Лотосовые мины | `passive_lotus_heart` | Сердце лотоса | `synergy_lotus_sanctuary` | Святилище лотоса | заранее занимать безопасные зоны и заманивать туда волну |
| `weapon_star_bow` | Звёздный лук | `passive_star_compass` | Звёздный компас | `synergy_constellation_rain` | Дождь созвездий | работать по дальним приоритетным целям и связывать точки арены |
| `weapon_black_eclipse_umbrella` | Чёрный зонт затмения | `passive_spirit_lens` | Духовная линза | `synergy_eclipse_vortex` | Воронка затмения | решать, когда стянуть врагов и предметы, не создавая опасную кучу |

---

## 3. Weapon entries

### 3.1 `weapon_moon_blade` — Лунный клинок

- **Fantasy / promise:** парные лунные лезвия сами прорезают ближнюю дугу, а движение игрока меняет, где появится следующий разрез.
- **Role:** `mobility / close_area`.
- **Targeting:** `nearest_cluster`; qualitative range `close`; geometry `cone + returning_arc`.
- **Core loop:** автоматический взмах создаёт пересекающиеся серповидные трассы; после прохода игрока через новую позицию следующая атака получает направленную ось. Это награждает движение по касательной к орде, а не стояние в центре.
- **Hit behavior:** `direct`, `pierce` по линии дуги, короткий `persist` след; один враг не должен многократно получать урон от одного прохода без отдельного balance rule.
- **Strength:** чистит плотную ближнюю группу и оставляет окно для рывка.
- **Weakness / counterplay:** плохо достаёт дальних врагов и рассеивается против разных направлений; игрок должен заранее выбирать сторону выхода.
- **VFX lifecycle:** cast — серебряный crescent flash у руки; travel — короткий jade-white smear по дуге; hit — тонкий разрез и искры; persistent — слабый след на земле; expire — затухание без остаточного collision.
- **Audio/haptic:** короткий металлический свист на cast, мягкий двойной удар на hit, тактильный импульс только на подтверждённом контакте; готовность cooldown — высокий, но не резкий тон.
- **Synergy tag:** `movement_changes_attack_lane`, `close_commitment`, `moon_arc`.
- **PENDING_BALANCE:** base damage, cadence, cooldown, arc width, exact range, pierce limit, trail duration, evolution power budget.
- **Runtime contract:** `upgrade_applied.v1` меняет weapon level; CombatSystem читает `targeting`, `geometry`, `hit/persist`; эволюция вызывается только через `synergy_claimed.v1`; persistent trail отправляет cleanup event.
- **Visual Lab brief:** route `SPRITE` + secondary `ART`; stage `docs/mockups/06-weapons/`; asset family `family.weapon.moonveil-soft-tonal.v01`; нужны icon, combat origin, crescent trail и ground trace; `candidate_id: null`, status `PROPOSAL`, artistic `PENDING`.

### 3.2 `weapon_jade_talismans` — Нефритовые талисманы

- **Fantasy / promise:** талисманы находят угрозы, прикрепляются к целям и превращают последовательные попадания в управляемую сеть меток.
- **Role:** `control / ranged_sustain`.
- **Targeting:** сначала ближайшая непомеченная цель, затем marked/high-threat target; qualitative range `long`; geometry `homing_projectile + mark`.
- **Core loop:** первый талисман ставит метку; повторный контакт обновляет/активирует её по data rule. Игроку важно, чтобы атаки не все ушли в одну мелкую цель, если рядом есть элитная угроза.
- **Hit behavior:** `homing`, `mark`, `delayed_resolve`; метка имеет наблюдаемый icon/state и не может бесконечно продлевать сама себя.
- **Strength:** стабильно достаёт опасных врагов сквозь рыхлую волну и даёт Lin Yue безопасный дальний контроль.
- **Weakness / counterplay:** одиночная цель получает меньше пользы от цепных эффектов; телепорт/зеркальная копия могут сорвать target lock.
- **VFX lifecycle:** cast — бумажная печать раскрывается; travel — jade thread показывает путь; hit — знак закрепляется над целью; persist — метка пульсирует, но не закрывает силуэт; expire/detonate — печать сгорает и удаляет mark state.
- **Audio/haptic:** бумажный щелчок на cast, стеклянный jade ping на mark, более глубокий аккорд на resolve; haptic только при активации метки, не на каждом homing tick.
- **Synergy tag:** `mark_network`, `homing_control`, `chain_resolution`.
- **PENDING_BALANCE:** base damage, projectile cadence/count, homing turn rate, range, mark lifetime, resolve threshold, chain count, evolution power budget.
- **Runtime contract:** MarkStore/CombatSystem хранят mark state; `upgrade_applied.v1` меняет данные; `synergy_eligibility_evaluated.v1` проверяет пару; chain resolver должен иметь visited-set и cleanup.
- **Visual Lab brief:** route `SPRITE` + `VFX`; stage `docs/mockups/06-weapons/`; asset family `family.weapon.jade-seal.v01`; отличать талисман от XP-кристалла формой бумаги и ореолом, а не только цветом.

### 3.3 `weapon_crimson_flame_fan` — Веер багрового пламени

- **Fantasy / promise:** веер срезает пространство конусом огня и оставляет очаги, вокруг которых враги начинают двигаться иначе.
- **Role:** `area / status_burn`.
- **Targeting:** ближайшая плотная группа или направление максимальной угрозы; qualitative range `mid`; geometry `alternating_cone + zone`.
- **Core loop:** cast чередует широкие огненные веера; попадания оставляют горящие участки. Игрок выбирает, закрыть путь перед собой или отрезать боковой фланг.
- **Hit behavior:** cone hit, `burn`, `persist_zone`; зона не должна превращаться в невидимую стену — её граница и время жизни читаются.
- **Strength:** контролирует коридор и хорошо наказывает плотные группы.
- **Weakness / counterplay:** разреженная волна и быстрые элиты обходят очаг; игроку приходится заранее смотреть на траектории, а не просто держать атаку.
- **VFX lifecycle:** cast — веер раскрывается из crimson ribbon; travel — приглушённое пламя с ivory edge; hit — вспышка углей; persist — низкий слой горения, не закрывающий enemy telegraph; expire — угли гаснут и очищают zone.
- **Audio/haptic:** шелест ткани и короткий flame rush, отдельный crackle при постановке зоны, низкий haptic на burn application; не использовать постоянную вибрацию.
- **Synergy tag:** `burn_zone`, `lane_control`, `phoenix_trigger`.
- **PENDING_BALANCE:** damage, cast cadence, cone width/length, burn damage, zone duration/area, target cap, evolution power budget.
- **Runtime contract:** StatusSystem хранит burn; ZoneStore отвечает за lifetime; `synergy_claimed.v1` заменяет attack data на evolution profile; cleanup обязан удалять визуал и status source.
- **Visual Lab brief:** route `ART` + `SPRITE`; muted crimson — только внутри огня и warning edge, основа остаётся smoky teal/ivory; status `PROPOSAL`.

### 3.4 `weapon_frost_pearl` — Ледяная жемчужина

- **Fantasy / promise:** жемчужина летит в цель и раскрывает вокруг неё морозный импульс, замедляя поток, но не превращая бой в полностью безопасную паузу.
- **Role:** `control / mid_area`.
- **Targeting:** ближайшая группа с приоритетом на врага, который входит в опасный коридор; qualitative range `mid`; geometry `projectile + impact_burst`.
- **Core loop:** direct projectile создаёт точку замедления; следующие удары выгоднее направлять в уже slowed cluster, но одиночный дальний target не должен блокировать весь пул.
- **Hit behavior:** `direct`, `slow`, `burst`, optional `freeze_candidate` только при отдельном balance rule.
- **Strength:** создаёт время для чтения телеграфов и спасает от плотного rush.
- **Weakness / counterplay:** быстро движущиеся цели могут покинуть burst; постоянное удержание одной зоны уменьшает покрытие другой стороны.
- **VFX lifecycle:** cast — pearl charge; travel — тонкий cold trail; hit — шестилепестковый frost ring; persist — ледяная рябь с ясным краем; expire — крошение, после которого не остаётся замедляющего collider.
- **Audio/haptic:** crystal chime на launch, приглушённый crack на impact, отдельный low pulse на freeze/strong status; haptic только при переходе status в новый tier.
- **Synergy tag:** `slow_field`, `controlled_cluster`, `winter_lattice`.
- **PENDING_BALANCE:** projectile damage, cadence, range, burst radius, slow strength/duration, freeze eligibility, evolution power budget.
- **Runtime contract:** StatusSystem и ZoneStore должны различать slow source и frost visual; no hidden permanent freeze; evolution adds lattice entity with deterministic cleanup.
- **Visual Lab brief:** route `ART`; stage `docs/mockups/06-weapons/`; pale ivory/jade ice silhouette, без кислотного cyan; telegraph edge должен быть виден на воде и останках.

### 3.5 `weapon_thunder_needles` — Иглы грома

- **Fantasy / promise:** иглы перескакивают между ближайшими угрозами и создают короткие электрические маршруты по волне.
- **Role:** `burst / chain`.
- **Targeting:** nearest unhit target with high-threat tie-break; qualitative range `mid`; geometry `chain`.
- **Core loop:** первый удар выбирает узел, затем цепь ищет соседний допустимый target. Игроку выгодно держать врагов в читаемой плотности, но опасно позволять цепи скрывать telegraph.
- **Hit behavior:** `chain`, `mark/conductive`; visited targets не получают повторный прыжок от того же cast без explicit rule.
- **Strength:** эффективен против компактной смешанной орды и быстро снимает приоритетные цели.
- **Weakness / counterplay:** слабее против одиночного удалённого врага и рассредоточенной волны; chain path не должен проходить сквозь стену/невалидную геометрию.
- **VFX lifecycle:** cast — needle glyph; travel — тонкая lightning line с пустым пространством вокруг; hit — compact flash; persist — короткий conductive mark; expire — line dissolves from first to last node.
- **Audio/haptic:** сухой click на target acquire, rising tone по цепи, отдельный удар на final node; haptic pulse ограничен финальным подтверждённым hit.
- **Synergy tag:** `conductive_chain`, `priority_burst`, `sky_judgment`.
- **PENDING_BALANCE:** hit damage, chain reach, chain count, cadence, mark duration, target priority weights, evolution power budget.
- **Runtime contract:** ChainResolver receives immutable target snapshot and visited-set; combat facts identify source weapon and chain index for attribution; cleanup removes conductive tags.
- **Visual Lab brief:** route `VFX`; stage `docs/mockups/06-weapons/`; muted violet/ivory lightning with strong silhouette gaps; no full-screen white flash.

### 3.6 `weapon_spirit_bell` — Колокол духов

- **Fantasy / promise:** колокол выпускает радиальные звуковые волны, которые отодвигают угрозы и могут сбить читаемые снаряды в правильный момент.
- **Role:** `defense / area_control`.
- **Targeting:** self-centered radial; qualitative range `close_to_mid`; geometry `radial_pulse`.
- **Core loop:** автоматический pulse создаёт безопасное окно вокруг героини. Игрок не получает постоянную неуязвимость: сила оружия — в моменте выхода из окружения и снятии projectile pressure.
- **Hit behavior:** `knockback`; optional `projectile_interruption` только для projectile classes, обозначенных Runtime/Balance.
- **Strength:** стабилизирует ближний бой и помогает пережить волну с нескольких сторон.
- **Weakness / counterplay:** не закрывает дальние зоны и не заменяет движение; крупные элиты могут пережить impulse и продолжить паттерн.
- **VFX lifecycle:** cast — bell halo; travel — expanding translucent ring; hit — short ripple on enemy; persist — fading resonance line; expire — ring disappears before next pulse.
- **Audio/haptic:** deep bell with readable onset, soft body resonance, different short tick for projectile deflection; haptic onset once per pulse, not per enemy.
- **Synergy tag:** `radial_ward`, `projectile_window`, `guardian_bell`.
- **PENDING_BALANCE:** pulse damage, cadence, radius, knockback, interruption classes, immunity/repeat-hit policy, evolution power budget.
- **Runtime contract:** CombatSystem tags pulse source; projectile interaction must be explicit and deterministic; ArtifactEffectSystem may observe guard events but cannot mutate Bell state directly.
- **Visual Lab brief:** route `ART` + `VFX`; stage `docs/mockups/06-weapons/`; muted brass bell core, ivory resonance ring, no screen-covering bloom.

### 3.7 `weapon_fox_mirage` — Лисий мираж

- **Fantasy / promise:** призрачная лиса прокладывает собственную линию через орду и возвращается, превращая фланги в часть зоны поражения.
- **Role:** `mobility / summon_line`.
- **Targeting:** nearest high-density lane; qualitative range `mid`; geometry `dash_linked_summon`.
- **Core loop:** fox selects a line, dashes through targets, leaves a delayed mirror route and returns/vanishes by its lifecycle. Игроку важно вести волну так, чтобы маршрут лисы пересекал следующий поток.
- **Hit behavior:** `pierce`, `mark`, delayed echo; summoned entity has source owner and cannot become an independent enemy.
- **Strength:** бьёт коридоры и фланги, полезен против окружения и decoy-поведения.
- **Weakness / counterplay:** плохо работает по цели, которая постоянно меняет направление; неправильная линия уводит урон от ближайшей опасности.
- **VFX lifecycle:** cast — mirror shard opens; travel — fox silhouette with silver afterimage; hit — paper-glass split; persist — route marker with low opacity; expire — reflections fold back into the fox.
- **Audio/haptic:** light fox chime on summon, two directional swishes on dash/return, haptic only on summon or evolution event.
- **Synergy tag:** `summoned_route`, `flank_coverage`, `mirror_echo`.
- **PENDING_BALANCE:** summon cadence, route length, hit damage, echo delay/damage, active summon cap, target rules, evolution power budget.
- **Runtime contract:** ControlledSpawner/pool owns summon lifecycle; `summon_id` and `source_weapon_id` are required; no orphaned route or damage after expire.
- **Visual Lab brief:** route `SPRITE` + `ART`; stage `docs/mockups/06-weapons/`; fox must remain readable at true 1x and not merge with mirror_fox enemy.

### 3.8 `weapon_lotus_mines` — Лотосовые мины

- **Fantasy / promise:** закрытые бутоны заранее занимают точки, раскрываясь под врагом и превращая путь волны в карту решений.
- **Role:** `area / delayed_control`.
- **Targeting:** projected enemy path or nearest unoccupied threat lane; qualitative range `mid`; geometry `delayed_zone`.
- **Core loop:** mine is placed, telegraphed, armed, triggered by an enemy or expires. Игрок выбирает движение так, чтобы не оставить все бутоны далеко от следующего потока.
- **Hit behavior:** `delayed`, `area_burst`, optional `petal_mark`; trigger is once per mine instance.
- **Strength:** удерживает choke point, помогает Соён Хан безопасно менять маршрут и заранее готовит арену.
- **Weakness / counterplay:** задержка делает оружие слабее при хаотичном rush; уже поставленная мина не должна бесконечно следовать за целью.
- **VFX lifecycle:** cast — closed lotus marker; arm — petals slowly open; warning — ground ring; hit — petal burst and soil ripple; expire — petals close and dissolve; cleanup removes zone.
- **Audio/haptic:** soft wood/petal click on arm, bass bloom on trigger, muted haptic on first detonation only.
- **Synergy tag:** `delayed_zone`, `route_prediction`, `lotus_sanctuary`.
- **PENDING_BALANCE:** mine cadence, placement distance, arm delay, area, damage, trigger rules, active mine cap, evolution power budget.
- **Runtime contract:** ZoneStore distinguishes `ARMED`, `TRIGGERED`, `EXPIRED`; placement uses world coordinates and deterministic target snapshot; no collision for visual petals after expiration.
- **Visual Lab brief:** route `ART`; stage `docs/mockups/06-weapons/`; lotus silhouette must be distinct from arena plants and XP crystal; muted jade/ivory with crimson only on danger rim.

### 3.9 `weapon_star_bow` — Звёздный лук

- **Fantasy / promise:** лук отмечает дальние угрозы и проводит через них пробивающие звездные линии, сохраняя свободный центр для движения.
- **Role:** `ranged / pierce / priority`.
- **Targeting:** farthest high-threat or first ranged/elite target; qualitative range `long`; geometry `line_projectile + anchor`.
- **Core loop:** shot travels through a chosen line and creates a star anchor at a meaningful target/location. Следующий выстрел может соединить anchors, если они валидны, поэтому игроку выгодно не полностью слипаться с ордой.
- **Hit behavior:** `direct`, `pierce`, `mark/anchor`; anchor is a read-only targeting datum until a later shot consumes it.
- **Strength:** достаёт backline moths, elites и опасные цели за первой линией.
- **Weakness / counterplay:** близкий swarm может перегрузить приоритет; неверный дальний target оставляет ближайшую опасность без ответа.
- **VFX lifecycle:** cast — bow constellation; travel — narrow ivory projectile; hit — star pin; persist — tiny anchor with line hint; expire — anchor dims and clears; no permanent arena geometry.
- **Audio/haptic:** string snap, clean star ping, low chord on line connection; haptic on anchor consumption only.
- **Synergy tag:** `long_priority`, `pierce_line`, `constellation_anchor`.
- **PENDING_BALANCE:** damage, cadence, exact range, pierce, target priority, anchor lifetime/count, line effect, evolution power budget.
- **Runtime contract:** TargetingSystem supplies immutable candidates; anchor state is scoped to weapon instance; combat attribution must separate direct arrow and constellation effect.
- **Visual Lab brief:** route `SPRITE` + `VFX`; stage `docs/mockups/06-weapons/`; ivory arrow, smoky jade constellation lines, no starfield that hides XP or boss telegraphs.

### 3.10 `weapon_black_eclipse_umbrella` — Чёрный зонт затмения

- **Fantasy / promise:** зонт вращается вокруг героини, перехватывает часть projectile pressure и раскрывается, когда нужно стянуть опасную группу.
- **Role:** `defense / utility / pull`.
- **Targeting:** incoming projectiles for guard mode; nearest dense group for open mode; qualitative range `close_to_mid`; geometry `orbit + cone/vortex`.
- **Core loop:** umbrella alternates between closed guard orbit and open eclipse sweep. Игрок использует момент раскрытия для управления пространством, но не получает постоянный screen clear.
- **Hit behavior:** `intercept/deflect` for eligible projectiles, `pull`, then optional burst; hostile projectile classes require explicit registry tags.
- **Strength:** сочетает защиту и control, особенно когда нужно собрать волну в заранее подготовленную зону.
- **Weakness / counterplay:** pull может собрать врагов или опасные зоны слишком близко; игрок должен выбрать безопасный угол и не раскрывать зонт поверх telegraph.
- **VFX lifecycle:** orbit — matte black silhouette with silver edge; open — eclipse iris; pull — visible curved streams; burst — contained crimson-violet ring; expire — iris closes and all temporary fields clean up.
- **Audio/haptic:** cloth snap on open, low eclipse hum during pull, deep impact on burst; one haptic onset per mode switch.
- **Synergy tag:** `projectile_guard`, `controlled_pull`, `eclipse_field`.
- **PENDING_BALANCE:** orbit cadence, interception classes, guard capacity, pull strength/radius, open duration, burst damage, evolution power budget.
- **Runtime contract:** projectile tags are data-driven; CombatSystem emits `projectile_intercepted`; pull affects enemy positioning but not boss-safe-spawn rules; all temporary fields have owner/effect IDs.
- **Visual Lab brief:** route `SPRITE` + `ART` + `VFX`; stage `docs/mockups/06-weapons/`; keep black object distinct from dark arena by silver rim and jade contact shadow.

## 4. Passive entries

### 4.1 `passive_wind_of_travel` — Ветер странствий

- **Fantasy / promise:** постоянное движение делает героиню легче и помогает превращать смену позиции в часть атаки.
- **Axis:** `mobility`.
- **Activation:** `always_on` for movement baseline; `on_move` for a temporary momentum hook if approved.
- **Affected systems:** movement speed, dash/active-ability recovery hook, close-weapon directional state.
- **Mechanic:** усиливает mobility axis и может открывать momentum window после смены направления; window должен быть наблюдаемым и не превращаться в скрытый DPS multiplier.
- **Decision/trade-off:** выгоден на открытой арене и для Moon Blade, но не заменяет защиту и не даёт пользы, если игрок зажат в углу.
- **Stacking intent:** repeated offers upgrade same entry; duplicate application is no-op; exact cap `PENDING_BALANCE` beyond canonical passive max rank 5.
- **Compatible content:** `weapon_moon_blade`, `synergy_moon_dance`; secondary mobility artifacts only after stacking review.
- **UI copy:** short — «Двигайся легче»; detail — «Усиливает мобильность и поддерживает атаки, зависящие от смены позиции.»
- **VFX brief:** thin jade wind ribbon at feet only while movement hook is active; no permanent aura that hides floor telegraphs.
- **PENDING_BALANCE:** movement modifier, momentum window, dash recovery, conditional attack hook, rank curve.
- **Runtime contract:** StatsCalculator reads persistent modifier; MovementSystem may emit `movement_started/direction_changed`; no UI mutation of RunSession.

### 4.2 `passive_jade_focus` — Нефритовый фокус

- **Fantasy / promise:** концентрация удерживает талисманы и дальние заклинания на выбранной угрозе.
- **Axis:** `offense / status / targeting`.
- **Activation:** `always_on` for projectile-control axis; `on_mark` for a conditional mark hook.
- **Affected systems:** homing stability, mark retention, long-range targeting priority, projectile travel behavior.
- **Mechanic:** improves consistency of marked-target loop and rewards finishing meaningful targets instead of randomizing every shot.
- **Decision/trade-off:** stronger single-target control can reduce coverage of scattered enemies; TargetingSystem must expose why a target was chosen.
- **Stacking intent:** same passive upgrades; no separate hidden mark stack outside the weapon's mark contract.
- **Compatible content:** `weapon_jade_talismans`, `weapon_star_bow`, `synergy_heavenly_seals`.
- **UI copy:** short — «Удерживай цель»; detail — «Улучшает контроль дальних атак и делает метки талисманов стабильнее.»
- **VFX brief:** icon uses a jade eye/anchor motif; feedback is a small ring around a valid marked target, not a full-screen glow.
- **PENDING_BALANCE:** homing correction, mark lifetime, target priority weight, projectile behavior, rank curve.
- **Runtime contract:** Content Registry supplies modifier tags; Combat/Targeting consume them; emitted mark events remain idempotent per hit/event ID.

### 4.3 `passive_ember_heart` — Сердце углей

- **Fantasy / promise:** каждый очаг дышит дольше и помогает строить огненный маршрут.
- **Axis:** `status / area`.
- **Activation:** `always_on` for burn axis; `on_hit`/`on_zone_created` for ember hook.
- **Affected systems:** burn lifecycle, fire-zone persistence, spread eligibility.
- **Mechanic:** extends the burn identity and gives the Flame Fan a choice between broad coverage and sustained lanes; no unnamed global damage bonus.
- **Decision/trade-off:** выгоден, если игрок планирует маршрут через очаги; слабее против целей, которые обходят zones.
- **Stacking intent:** rank upgrades burn-related fields; multiple independent burn sources retain source IDs and do not refresh forever.
- **Compatible content:** `weapon_crimson_flame_fan`, `synergy_phoenix_sky`, fire-tagged artifacts.
- **UI copy:** short — «Раздувай очаг»; detail — «Усиливает поведение горения и делает огненные зоны частью маршрута.»
- **VFX brief:** ember icon with a contained core; feedback adds small rising sparks only during a valid burn event.
- **PENDING_BALANCE:** burn duration, zone persistence, spread rule, status intensity, rank curve.
- **Runtime contract:** StatusSystem owns burn; ZoneStore owns zones; passive cannot directly spawn VFX or mutate HP.

### 4.4 `passive_frost_thread` — Морозная нить

- **Fantasy / promise:** замедленные враги связываются в удобный для прицела холодный узор.
- **Axis:** `status / crit_conditional`.
- **Activation:** `on_hit` when slow/freeze is applied; `timed_window` for conditional follow-up.
- **Affected systems:** slow effectiveness, controlled-target damage tag, conditional critical interaction.
- **Mechanic:** makes a slowed target a deliberate follow-up target; the benefit is conditional and visible, not universal crit power.
- **Decision/trade-off:** focus fire improves control but may allow another lane to approach; player chooses between finishing frozen pack and repositioning.
- **Stacking intent:** one controlled-target window per source event; duplicate passive ranks improve the same axis, not create nested infinite windows.
- **Compatible content:** `weapon_frost_pearl`, `weapon_thunder_needles`, `synergy_winter_palace`.
- **UI copy:** short — «Свяжи холодом»; detail — «Усиливает замедление и открывает выгодное продолжение атаки по подконтрольным целям.»
- **VFX brief:** thin frost thread between controlled targets; must not mimic arena water ripples.
- **PENDING_BALANCE:** slow modifier, conditional critical modifier, window duration, target linkage, rank curve.
- **Runtime contract:** consumes status events, never infers status from sprite color; CombatSystem validates target/source and clears window on expiry.

### 4.5 `passive_heavenly_seal` — Небесная печать

- **Fantasy / promise:** удар по одной цели оставляет проводящий знак для следующей молнии.
- **Axis:** `chain / status`.
- **Activation:** `on_hit` and `on_chain`.
- **Affected systems:** conductive mark, chain target selection, chain resolution feedback.
- **Mechanic:** makes Thunder Needles better at building a chain rhythm; the mark expires or resolves deterministically, so the player can read why a jump happened.
- **Decision/trade-off:** dense packs are valuable, but spreading the first hit too widely can lose the priority target.
- **Stacking intent:** marks from the same source obey a cap and refresh policy owned by Balance; no duplicate passive entry.
- **Compatible content:** `weapon_thunder_needles`, `weapon_jade_talismans`, `synergy_heavenly_judgment`.
- **UI copy:** short — «Замкни цепь»; detail — «Поддерживает проводящие метки и цепную логику электрических атак.»
- **VFX brief:** small geometric seal at the target; chain lines remain thin and leave telegraphs visible.
- **PENDING_BALANCE:** mark duration, chain reach, target cap, proc rule, rank curve.
- **Runtime contract:** ChainResolver consumes typed mark state; passive never chooses wallet/reward outcome.

### 4.6 `passive_iron_bell` — Железный колокол

- **Fantasy / promise:** защита становится слышимой: удар отбрасывает угрозу и даёт место для ответа.
- **Axis:** `defense / knockback`.
- **Activation:** `always_on` for defensive axis; `on_guard`/`on_pulse` for bell hook.
- **Affected systems:** damage reduction/guard tags, knockback, projectile interruption eligibility.
- **Mechanic:** strengthens the defensive identity of Spirit Bell and allows a pulse to create a readable reset of nearby pressure.
- **Decision/trade-off:** defensive control is strongest near the hero but does not kill distant ranged threats; movement remains necessary.
- **Stacking intent:** rank upgrades one defensive lane; guard and knockback cannot be independently multiplied by duplicate hidden stacks.
- **Compatible content:** `weapon_spirit_bell`, `synergy_guardian_bell`, defense-oriented artifacts.
- **UI copy:** short — «Отзови удар»; detail — «Усиливает защитный импульс, отбрасывание и работу с угрожающими снарядами.»
- **VFX brief:** brass ring with ivory center; feedback appears at pulse onset, not as a permanent shield bubble.
- **PENDING_BALANCE:** damage taken modifier, knockback, interruption rule, pulse interaction, rank curve.
- **Runtime contract:** CombatSystem emits guard/deflect facts; StatsCalculator and projectile tags remain separate owners.

### 4.7 `passive_mirror_shard` — Осколок зеркала

- **Fantasy / promise:** удачный удар может оставить за собой короткий отражённый след.
- **Axis:** `replication / crit`.
- **Activation:** `on_crit` or `on_hit` according to Balance binding; exact trigger pending.
- **Affected systems:** echo creation, source attack replay, target selection for the echo.
- **Mechanic:** creates a bounded echo of an eligible attack with its own event ID; echo cannot recursively create another echo without an explicit rule.
- **Decision/trade-off:** replication rewards accurate high-value hits, but offers less reliable coverage than a flat area passive.
- **Stacking intent:** duplicate ranks improve bounded echo behavior; recursion forbidden by default.
- **Compatible content:** `weapon_fox_mirage`, `weapon_star_bow`, `synergy_nine_reflections`.
- **UI copy:** short — «Оставь отражение»; detail — «Некоторые удачные попадания могут повторить часть атаки зеркальным эхом.»
- **VFX brief:** translucent ivory/jade afterimage with a clear source-to-echo relationship.
- **PENDING_BALANCE:** trigger chance, echo power, delay, eligible attack tags, echo cap, rank curve.
- **Runtime contract:** CombatSystem creates an `echo_instance_id`; recursion guard and cleanup are mandatory; no duplicate reward/XP path.

### 4.8 `passive_lotus_heart` — Сердце лотоса

- **Fantasy / promise:** запас здоровья и осознанный подбор лечения позволяют пережить ошибку без бессмертия.
- **Axis:** `defense / healing`.
- **Activation:** `always_on` for max HP; `on_pickup`/`on_heal` for recovery hook.
- **Affected systems:** max HP, healing intake, overheal/temporary-ward boundary if approved.
- **Mechanic:** strengthens survival and gives Lotus Mines a recovery identity; healing remains limited by actual pickup/effect rules.
- **Decision/trade-off:** safer route supports close play, but investing in recovery reduces opportunity for offensive passives in six slots.
- **Stacking intent:** one authoritative heal pipeline; passive must not create a second hidden heal from XP.
- **Compatible content:** `weapon_lotus_mines`, `synergy_lotus_sanctuary`, `artifact_lotus_seed`.
- **UI copy:** short — «Сохрани жизнь»; detail — «Усиливает запас здоровья и ценность разрешённых источников лечения.»
- **VFX brief:** lotus heart icon; heal feedback is a restrained petal pulse around the hero, not a permanent aura.
- **PENDING_BALANCE:** max HP, healing modifier, overheal policy, recovery cap, rank curve.
- **Runtime contract:** HealthSystem owns HP/heal; passive consumes `heal_applied` fact; XPDrop remains separate from heal pickup.

### 4.9 `passive_star_compass` — Звёздный компас

- **Fantasy / promise:** фокус удерживает дальнюю цель и сокращает паузу между значимыми выстрелами.
- **Axis:** `cooldown / targeting`.
- **Activation:** `always_on`; optional `on_long_hit` targeting hook.
- **Affected systems:** weapon cooldown, long-range priority, anchor selection.
- **Mechanic:** gives Star Bow a clear long-range identity and can support other weapons that deliberately choose high-threat targets; it does not globally accelerate every unrelated system by hidden logic.
- **Decision/trade-off:** prioritizing a distant elite can leave a close rusher alive; player accepts target-selection risk.
- **Stacking intent:** cooldown is calculated once by StatsCalculator; no separate per-weapon hidden multiplier.
- **Compatible content:** `weapon_star_bow`, `weapon_jade_talismans`, `synergy_constellation_rain`.
- **UI copy:** short — «Выбери звезду»; detail — «Сокращает паузу оружия и помогает удерживать дальнюю приоритетную цель.»
- **VFX brief:** compass needle icon, a small target reticle for selected high-threat target.
- **PENDING_BALANCE:** cooldown modifier, targeting priority, anchor behavior, rank curve.
- **Runtime contract:** StatsCalculator returns derived cooldown; TargetingSystem receives explicit priority tags; no UI timer as source of truth.

### 4.10 `passive_spirit_lens` — Духовная линза

- **Fantasy / promise:** линза показывает ценность предметов и расширяет управляемую зону подбора/воздействия.
- **Axis:** `pickup / area / utility`.
- **Activation:** `always_on` for acquisition radius; `on_pickup` for feedback hook.
- **Affected systems:** XP/item pickup radius, selected field readability, umbrella utility interactions.
- **Mechanic:** increases useful awareness and acquisition area; it does not automatically collect through walls and does not convert XP into Gold.
- **Decision/trade-off:** wider pickup encourages routes through drops, but chasing distant items can pull the player into danger.
- **Stacking intent:** one derived pickup radius from StatsCalculator; artifact auras remain separate modifiers with source attribution.
- **Compatible content:** `weapon_black_eclipse_umbrella`, `synergy_eclipse_vortex`, `weapon_lotus_mines`.
- **UI copy:** short — «Увидь поток»; detail — «Расширяет радиус подбора опыта и предметов, сохраняя правила стен и опасных зон.»
- **VFX brief:** lens ring with a dark center and jade rim; no large radial overlay on gameplay.
- **PENDING_BALANCE:** pickup radius, XP/item distinction, wall/LOS rule, field interaction, rank curve.
- **Runtime contract:** Magnet/Progression owns collection validation; passive provides derived modifier; `xp_drop_collected.v1` remains idempotent.

## 5. Synergy/evolution entries

Все десять entries используют один gate: `weapon_level = 6`, `passive_rank = 5`, matching `synergy_id`, weapon not evolved, non-final `BOSS_CHEST`, `claimed_synergy_count < 3`. Точные значения и priority при нескольких eligible pairs — `PENDING_BALANCE/PRODUCT`.

### 5.1 `synergy_moon_dance` — Танец Луны

- **Requires:** `weapon_moon_blade` + `passive_wind_of_travel`.
- **New weapon behavior:** парные crescent traces начинают двигаться по орбитальному рисунку вокруг текущей траектории героя; движение создаёт чередующиеся режущие дорожки, а остановка оставляет только ближнюю защитную дугу.
- **Player decision:** проходить через край волны и прокладывать lane или удерживать позицию ради плотного radial coverage.
- **Counterplay/trade-off:** scattered ranged enemies остаются слабым match-up; эволюция не должна превращать движение в постоянную неуязвимость.
- **VFX/audio:** moon trails, short silver dance chord, cleanup after each lane.
- **PENDING_BALANCE:** evolved damage, cadence, lane duration, orbit reach, hit repeat policy, power share.

### 5.2 `synergy_heavenly_seals` — Небесные печати

- **Requires:** `weapon_jade_talismans` + `passive_jade_focus`.
- **New weapon behavior:** activated marks break into a controlled chain of jade seals; a resolved mark can seed the next target but cannot revisit the same node in the same resolve.
- **Player decision:** spread marks across a pack or spend resolution on elite/priority target.
- **Counterplay/trade-off:** teleports, decoys and isolated targets break chain value; visual chain must never cover danger zones.
- **VFX/audio:** seal-to-seal path, clear final detonation, no recursive particles.
- **PENDING_BALANCE:** chain target cap, resolve cadence, damage share, mark lifetime, power share.

### 5.3 `synergy_phoenix_sky` — Феникс алого неба

- **Requires:** `weapon_crimson_flame_fan` + `passive_ember_heart`.
- **New weapon behavior:** burning zones feed a phoenix flight path; the bird crosses eligible embers, ignites a readable lane and then exits the arena instead of remaining as a permanent summon.
- **Player decision:** place/maintain fire where the next flight can cross the threat lane.
- **Counterplay/trade-off:** no active ember means no full flight; scattered enemies reduce value and force repositioning.
- **VFX/audio:** contained crimson bird silhouette, ember trail with visible expire, rising call on launch.
- **PENDING_BALANCE:** flight cadence, path length, damage, ember consumption, zone interaction, power share.

### 5.4 `synergy_winter_palace` — Дворец вечной зимы

- **Requires:** `weapon_frost_pearl` + `passive_frost_thread`.
- **New weapon behavior:** controlled targets form frost links; enough valid links produce a temporary lattice/field that slows incoming lanes and leaves a readable safe route.
- **Player decision:** build a compact control palace or abandon it to move before a new telegraph arrives.
- **Counterplay/trade-off:** the lattice is location-bound and expires; bosses/immune targets must not be silently frozen.
- **VFX/audio:** ice lines grow from source to source, lattice collapses visibly, low crystal chord on completion.
- **PENDING_BALANCE:** link threshold, field size/duration, slow/freeze rules, boss immunity, power share.

### 5.5 `synergy_heavenly_judgment` — Приговор небес

- **Requires:** `weapon_thunder_needles` + `passive_heavenly_seal`.
- **New weapon behavior:** conductive marks call a visible overhead judgment; the first strike resolves the chosen node, while secondary arcs follow valid marked targets.
- **Player decision:** prioritize marked elite or allow the judgment to thin a dense wave.
- **Counterplay/trade-off:** no marked targets means no judgment; isolated enemies and fast teleports lower chain efficiency.
- **VFX/audio:** pre-strike vertical warning, ivory-violet impact, compact arc trails; no untelegraphed damage.
- **PENDING_BALANCE:** judgment cadence, target selection, arc count, damage, mark consumption, power share.

### 5.6 `synergy_guardian_bell` — Звон защитницы

- **Requires:** `weapon_spirit_bell` + `passive_iron_bell`.
- **New weapon behavior:** a successful radial pulse leaves a moving ward rim; the rim can deflect eligible telegraphed projectiles and push close threats before fading.
- **Player decision:** stay near the rim for protection or leave it to pursue XP/priority targets.
- **Counterplay/trade-off:** ward has an explicit lifecycle and cannot block all damage; ground zones and distant attacks remain threats.
- **VFX/audio:** brass/ivory ring, projectile deflect tick, fade to zero before cleanup.
- **PENDING_BALANCE:** ward lifetime, radius, deflect classes/capacity, knockback, damage, power share.

### 5.7 `synergy_nine_reflections` — Девять отражений

- **Requires:** `weapon_fox_mirage` + `passive_mirror_shard`.
- **New weapon behavior:** the fox's route leaves a series of mirror echoes that execute with staggered timing; the name is fantasy identity, not permission to hardcode an unbalanced count.
- **Player decision:** lay a corridor through a dense pack or aim cross-lane echoes at a dangerous flank.
- **Counterplay/trade-off:** delayed echoes can miss a moving target; mirrors must be distinguishable from `mirror_fox` enemy decoys.
- **VFX/audio:** low-opacity afterimages with source arrows, staggered chimes, deterministic cleanup per echo instance.
- **PENDING_BALANCE:** echo count, delay, damage, route lifetime, active cap, power share.

### 5.8 `synergy_lotus_sanctuary` — Святилище лотоса

- **Requires:** `weapon_lotus_mines` + `passive_lotus_heart`.
- **New weapon behavior:** triggered mines link into a temporary lotus sanctuary; the field controls enemies and exposes a bounded recovery interaction only if the approved healing contract allows it.
- **Player decision:** fight around the sanctuary or abandon it before a boss/elite telegraph makes the location unsafe.
- **Counterplay/trade-off:** static field is powerful only where placed; it does not block collision or make the player immune.
- **VFX/audio:** layered lotus petals, safe/unsafe edge distinction, bloom chord, full cleanup at expiry.
- **PENDING_BALANCE:** link rule, field lifetime/area, damage/control, healing interaction, power share.

### 5.9 `synergy_constellation_rain` — Дождь созвездий

- **Requires:** `weapon_star_bow` + `passive_star_compass`.
- **New weapon behavior:** star anchors connect into a constellation; arrows descend along its readable segments and collapse the oldest anchor after resolve.
- **Player decision:** aim across the arena at ranged threats or create a local constellation for a dense group.
- **Counterplay/trade-off:** the system requires valid anchors and line of sight; it does not fire through walls or generate invisible off-screen damage.
- **VFX/audio:** thin constellation lines, clear falling-arrow warnings, bright but controlled impact; anchors expire visibly.
- **PENDING_BALANCE:** anchor count/lifetime, rain cadence, line geometry, damage, target rules, power share.

### 5.10 `synergy_eclipse_vortex` — Воронка затмения

- **Requires:** `weapon_black_eclipse_umbrella` + `passive_spirit_lens`.
- **New weapon behavior:** the umbrella opens a bounded vortex that pulls eligible enemies and nearby pickups toward a visible center, then collapses into a contained burst.
- **Player decision:** use the vortex to harvest/cluster or preserve it for an incoming elite; clustering hazards is a real risk.
- **Counterplay/trade-off:** bosses, dangerous zones and immune entities require explicit tags; vortex cannot pull through walls or erase all projectiles for free.
- **VFX/audio:** black iris with silver edge, jade pickup streams, audible wind-up, burst and full collapse; no opaque screen overlay.
- **PENDING_BALANCE:** pull radius/strength, charge/cooldown, duration, eligible target classes, burst power, power share.

## 6. Synergy resolver contract

### Eligibility

`SynergyEvaluator` возвращает только `ELIGIBLE`, `NOT_ELIGIBLE`, `ALREADY_CLAIMED`, `UNAVAILABLE_CONTEXT` или `FALLBACK_REQUIRED`. Он не изобретает новую пару.

### Run-1 cap

```yaml
synergy_run_policy:
  catalog_size: 10
  max_claimed_per_run: 3
  eligible_sources: [BOSS_CHEST]
  eligible_checkpoints_seconds: [300, 600, 900]
  final_boss_chest: forbidden
  after_cap: FALLBACK_REQUIRED
  duplicate_claim: idempotent_noop
```

Если у игрока одновременно несколько eligible pairs, порядок выбора должен быть deterministic и видимым в projection; конкретная priority policy остаётся `PENDING_PRODUCT_DECISION`. Четвёртый claim запрещён даже после финального босса.

### Required runtime facts

- `weapon_id`, `passive_id`, `synergy_id`, `weapon_level`, `passive_rank`;
- `chest_offer_id`, `checkpoint_id`, `run_id`, `state_revision`;
- `claimed_synergy_ids`, `claimed_synergy_count`;
- `evolved` до claim и `evolution_id` после claim;
- source tags для damage attribution и VFX cleanup;
- fallback outcome, если gate не проходит.

## 7. Общий Visual Lab handoff

Это не production asset request.

- `route`: `SPRITE` для combat icon/origin, `ART`/`VFX` для attacks/evolutions;
- `stage_path`: `docs/mockups/06-weapons/` для оружия, `docs/mockups/07-passives/` для passive icons/cards, `docs/mockups/19-synergy-info/` для explanatory relation;
- `asset_id`, `family_id`, `candidate_id` назначаются Visual Lab перед production;
- current status: `PROPOSAL`; `technical_status: NOT_RUN`; `artistic_status: PENDING`; `manifest/consumer: NOT_PROMOTED`;
- soft tonal code: deep blue-grey, smoky teal, warm ivory, muted brass, jade; crimson/violet только как role/status accent;
- icon identity должна читаться по форме, silhouette и interaction, а не только по цвету;
- Visual Lab отдельно проверяет 390×844 UI scale, true 1× combat scale, telegraph visibility и no-asset-drift.
