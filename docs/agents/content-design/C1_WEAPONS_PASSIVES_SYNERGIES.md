# C1 — Оружие, пассивки и синергии первого забега

Статус пакета: `CONTENT_SPECIFIED`

Это контентный контракт, а не баланс и не runtime implementation. Все значения урона, cadence, cooldown, дальности, размера, длительности, вероятности и лимитов передаются Balance Agent как `PENDING_BALANCE`.

## 1. Общий контракт первого забега

| Правило | Контракт |
|---|---|
| Пул | 10 weapons + 10 run passives |
| Одновременно в билде | максимум 6 weapon slots и 6 passive slots |
| Weapon progression | максимум уровня 10; для synergy нужен уровень 10 (content target) |
| Passive progression | максимум ранга 10; для synergy нужен ранг 10 (content target) |
| Upgrade offer | три карточки; New/Upgrade/Evolution — разные outcome types |
| Evolution gate | weapon max level + paired passive max rank + non-final boss/mini-boss chest + weapon not evolved |
| Synergy catalogue | 10 стабильных direct pairs |
| Synergy claims per run | **не более 5**; это пользовательское product decision для Run 1 |
| Synergy windows | десять нефинальных окон сундука: main bosses на 5/10/15/20/25 минутах и mini-bosses на 7:30/12:30/17:30/22:30/27:30 |
| Final boss | не создаёт boss chest и не выдаёт шестую synergy |
| Если подходящей пары нет | существующий fallback contract, значение назначает Balance/Product |

> Важно: число 10 относится к максимальному уровню оружия и рангу пассивки, а не к количеству слотов. В билде остаётся максимум 6 оружий и 6 пассивок; архитектурная сверка нового уровня 10/10 ещё не закрыта.

### Разделение сущностей

- **Run passive** — временный общий элемент билда, занимает один из шести passive slots и улучшает разрешённую глобальную ось, а не конкретное оружие.
- **Synergy anchor** — скрытая content-связь passive с одним weapon ID, используемая только для проверки evolution gate; она не превращает passive в weapon upgrade.
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

- **Fantasy / promise:** движение становится ресурсом выживания и темпа всего билда.
- **Axis:** `mobility / momentum`.
- **Activation:** `always_on` for movement axis; `on_movement_sequence` for a shared momentum state.
- **General effect:** повышает управляемость перемещения; после непрерывного движения любой eligible weapon hit получает общий `MOMENTUM` context до остановки/истечения окна.
- **Affected systems:** hero movement, universal hit context, telegraph navigation; не только close-range attacks.
- **Synergy anchor:** `weapon_moon_blade` — связь используется только для `synergy_moon_dance` eligibility; passive не усиливает Moon Blade отдельно.
- **Decision/trade-off:** игрок выбирает между постоянным маршрутом и остановкой для точного позиционирования; остановка сбрасывает momentum, но не наказывает весь билд.
- **Stacking intent:** ranks усиливают одну mobility/momentum ось; duplicate offer upgrades this entry, hidden per-weapon modifiers forbidden.
- **UI copy:** short — «Сохрани темп»; detail — «Улучшает перемещение и создаёт общий momentum для следующего удачного действия.»
- **VFX brief:** тонкий jade wind ribbon только при активном momentum; не показывать постоянную ауру, скрывающую floor telegraphs.
- **PENDING_BALANCE:** movement modifier, sequence definition, momentum window, eligible hit outcome, rank curve.
- **Runtime contract:** StatsCalculator supplies derived mobility; MovementSystem owns sequence state; passive never reads Moon Blade state and never mutates a single weapon.

### 4.2 `passive_jade_focus` — Нефритовый фокус

- **Fantasy / promise:** фокус не привязан к талисману — он удерживает любую выбранную угрозу в центре решения игрока.
- **Axis:** `targeting / consistency`.
- **Activation:** `always_on` for target-selection quality; `on_target_lock` for a shared focus state.
- **General effect:** auto-targeted weapons and spells дольше сохраняют valid priority target, меньше теряют цель при смене pack; manual aim не перехватывается.
- **Affected systems:** TargetingSystem, homing/retarget rules and priority projection for all eligible weapons.
- **Synergy anchor:** `weapon_jade_talismans` — только condition для `synergy_heavenly_seals`; passive не повышает damage/marks именно талисманов.
- **Decision/trade-off:** удержание elite улучшает single-target pressure, но может оставить ближайшего rush enemy без внимания; причина выбора цели должна быть видимой.
- **Stacking intent:** ranks улучшают общую стабильность выбора; один shared focus state, без отдельных per-weapon lock stacks.
- **UI copy:** short — «Удерживай угрозу»; detail — «Улучшает выбор и удержание приоритетной цели для всех автоматических атак.»
- **VFX brief:** jade eye/anchor motif; маленькое кольцо у выбранной цели, не full-screen glow.
- **PENDING_BALANCE:** target retention, retarget delay, priority weights, valid target classes, rank curve.
- **Runtime contract:** TargetingSystem consumes typed priority/focus tags; passive never checks or upgrades a specific weapon state.

### 4.3 `passive_ember_heart` — Сердце углей

- **Fantasy / promise:** каждый сильный исход оставляет запас тепла, который можно превратить в следующий общий всплеск.
- **Axis:** `overkill / chain tempo`.
- **Activation:** `on_enemy_defeated` or approved overkill result; `on_next_eligible_hit` consumes one ember charge.
- **General effect:** избыточный damage/подтверждённое убийство создаёт ограниченный ember charge; следующий hit любого eligible weapon может выпустить afterspark по соседней valid area.
- **Affected systems:** damage result, defeat attribution, universal follow-up hit and area response; не только fire-tagged sources.
- **Synergy anchor:** `weapon_crimson_flame_fan` — только condition для `synergy_phoenix_sky`; passive не продлевает и не усиливает зоны Flame Fan.
- **Decision/trade-off:** выгодно добивать цели и вести цепочку, но заряд ограничен и теряется при неудачном выборе/истечении; игрок не получает постоянный flat damage.
- **Stacking intent:** charges имеют bounded cap and source IDs; rank improves charge economy, never infinite recursive afterspark.
- **UI copy:** short — «Сохрани жар»; detail — «Удачное добивание оставляет заряд для следующего общего всплеска.»
- **VFX brief:** contained ember core with one rising spark on charge and a compact afterspark on consume.
- **PENDING_BALANCE:** overkill definition, charge cap, expiry, afterspark area/coefficient, eligible hit tags, rank curve.
- **Runtime contract:** Damage/Defeat systems own authoritative result; passive consumes typed result and cannot directly spawn zones or mutate HP.

### 4.4 `passive_frost_thread` — Морозная нить

- **Fantasy / promise:** контроль врага становится временным окном темпа для всего арсенала.
- **Axis:** `control / cooldown-tempo`.
- **Activation:** `on_slow_or_freeze_applied`; `on_controlled_hit` grants a bounded shared tempo response.
- **General effect:** когда любой eligible source накладывает slow/freeze, следующий hit по controlled target даёт ограниченное ускорение готовности всем eligible weapons/abilities, а не только источнику холода.
- **Affected systems:** status pipeline, controlled-target validation and universal cooldown/tempo response.
- **Synergy anchor:** `weapon_frost_pearl` — только condition для `synergy_winter_palace`; passive не усиливает Frost Pearl damage или slow отдельно.
- **Decision/trade-off:** игрок может добить controlled target ради темпа или уйти с линии telegraph; tempo не выдаётся без корректного control event.
- **Stacking intent:** one pending control window per target/source rule; ranks improve the shared window, no nested cooldown loops.
- **UI copy:** short — «Поймай момент»; detail — «Попадание по подконтрольной цели ускоряет следующий общий темп заклинаний.»
- **VFX brief:** thin frost thread between status marker and next hit; it must not mimic arena water ripples.
- **PENDING_BALANCE:** slow/freeze whitelist, window duration, cooldown response, target cap, rank curve.
- **Runtime contract:** consumes authoritative status events, never infers status from sprite color; StatsCalculator/TimerSystem own cooldown mutation.

### 4.5 `passive_heavenly_seal` — Небесная печать

- **Fantasy / promise:** печать отмечает момент, когда любой источник может превратить последовательность ударов в общий burst.
- **Axis:** `damage sequencing / vulnerability`.
- **Activation:** `on_distinct_hit` against the same valid target; `on_next_damage` consumes the seal.
- **General effect:** после заданной последовательности distinct hits любой следующий damage source может consume seal и открыть короткое universal vulnerability window.
- **Affected systems:** hit sequence, target status and damage calculation for all eligible sources.
- **Synergy anchor:** `weapon_thunder_needles` — только condition для `synergy_heavenly_judgment`; passive не добавляет chain/lightning mechanics сам по себе.
- **Decision/trade-off:** фокус по одной цели создаёт сильное окно, но распыление урона сбрасывает ценность последовательности; игрок выбирает target discipline.
- **Stacking intent:** one seal per target with deterministic refresh/consume; ranks improve sequence access, not universal permanent vulnerability.
- **UI copy:** short — «Открой уязвимость»; detail — «Последовательные попадания открывают короткое окно общего усиления урона.»
- **VFX brief:** small geometric seal and one clear state transition on consume; no chain lines unless the weapon itself owns them.
- **PENDING_BALANCE:** hit sequence length, seal lifetime, vulnerability coefficient, eligible damage categories, rank curve.
- **Runtime contract:** CombatSystem owns typed hit sequence and damage tags; passive never chooses a weapon or reward outcome.

### 4.6 `passive_iron_bell` — Железный колокол

- **Fantasy / promise:** один пережитый удар создаёт место для следующего решения, а не бесконечный щит.
- **Axis:** `defense / poise`.
- **Activation:** `always_on` for incoming damage axis; `on_damage_taken` opens a bounded grace/poise state.
- **General effect:** снижает eligible incoming damage и после подтверждённого попадания даёт короткое окно устойчивости к повторному stagger/chain-hit эффекту для героя.
- **Affected systems:** HealthSystem, damage mitigation, hit-stun/poise and universal projectile interaction.
- **Synergy anchor:** `weapon_spirit_bell` — только condition для `synergy_guardian_bell`; passive не создаёт bell pulse и не усиливает его радиус.
- **Decision/trade-off:** защита помогает пережить ошибку, но не отменяет telegraph, ground zone или следующий независимый hit; позиционирование остаётся обязательным.
- **Stacking intent:** one authoritative mitigation and one grace window; duplicate ranks cannot create nested invulnerability.
- **UI copy:** short — «Выдержи удар»; detail — «Снижает получаемый урон и уменьшает цепную цену одной ошибки.»
- **VFX brief:** small brass ring with ivory center at hit resolution; no permanent shield bubble.
- **PENDING_BALANCE:** damage categories, mitigation, poise/grace duration, repeat-hit rules, rank curve.
- **Runtime contract:** CombatSystem emits post-mitigation damage facts; HealthSystem owns HP; passive cannot cancel arbitrary hazards.

### 4.7 `passive_mirror_shard` — Осколок зеркала

- **Fantasy / promise:** любой сильный момент может оставить короткий след, но отражение никогда не становится самостоятельным оружием.
- **Axis:** `bounded replication`.
- **Activation:** `on_eligible_hit` or approved `on_critical_hit`; internal cooldown and source whitelist are Balance-owned.
- **General effect:** периодически повторяет часть последнего eligible hit любого оружия/способности с отдельным event ID; echo не наследует passive trigger.
- **Affected systems:** universal attack replay, source attribution, target/area snapshot and cleanup.
- **Synergy anchor:** `weapon_fox_mirage` — только condition для `synergy_nine_reflections`; passive не выдаёт fox route и не усиливает Mirage отдельно.
- **Decision/trade-off:** точный высокий hit может получить echo, но эффект не так надёжен, как постоянный area bonus; игрок сохраняет цель и позицию.
- **Stacking intent:** ranks улучшают bounded echo; recursion and echo-of-echo forbidden by default.
- **UI copy:** short — «Оставь след»; detail — «Некоторые попадания повторяются коротким зеркальным эхом независимо от оружия.»
- **VFX brief:** translucent ivory/jade afterimage with a clear source-to-echo relationship; no clone swarm.
- **PENDING_BALANCE:** trigger rule, coefficient, delay, eligible source tags, echo cap, internal cooldown, rank curve.
- **Runtime contract:** CombatSystem creates `echo_instance_id`; recursion guard, attribution and cleanup are mandatory; no duplicate reward/XP path.

### 4.8 `passive_lotus_heart` — Сердце лотоса

- **Fantasy / promise:** здоровье — это запас решений, а лечение в правильный момент превращается в устойчивость всего билда.
- **Axis:** `health / healing conversion`.
- **Activation:** `always_on` for max HP; `on_heal_applied` and `on_full_health_heal` for a bounded Petal state.
- **General effect:** увеличивает survival axis и позволяет approved healing source накопить один Petal state, который смягчает следующий eligible hit; это работает независимо от оружия.
- **Affected systems:** HealthSystem, healing intake, max HP and universal incoming-hit response.
- **Synergy anchor:** `weapon_lotus_mines` — только condition для `synergy_lotus_sanctuary`; passive не усиливает mine damage/placement.
- **Decision/trade-off:** игрок может подобрать лечение при полном HP ради Petal или отказаться ради позиции; state не становится второй полосой HP.
- **Stacking intent:** one authoritative heal pipeline and one bounded Petal state; XP pickup never counts as heal.
- **UI copy:** short — «Сохрани жизнь»; detail — «Укрепляет здоровье и превращает разрешённое лечение в краткую защиту.»
- **VFX brief:** lotus-heart icon; heal/Petal feedback is a restrained petal pulse, not a permanent aura.
- **PENDING_BALANCE:** max HP, healing modifier, full-health rule, ward strength/duration, hazard whitelist, rank curve.
- **Runtime contract:** HealthSystem owns HP/heal; passive consumes `heal_applied` fact after cap; XPDrop remains separate.

### 4.9 `passive_star_compass` — Звёздный компас

- **Fantasy / promise:** каждый промах приближает точный момент, который может решить бой.
- **Axis:** `critical rhythm`.
- **Activation:** `on_eligible_hit_result`; non-critical sequence charges a shared precision state, next valid hit consumes it.
- **General effect:** создаёт общий ритм критических ударов для всех eligible weapons/abilities: последовательность обычных hit открывает гарантированный/усиленный precision window по правилам Balance.
- **Affected systems:** crit roll, crit power window, hit sequence and universal source tags.
- **Synergy anchor:** `weapon_star_bow` — только condition для `synergy_constellation_rain`; passive не повышает дальность/anchor count Star Bow.
- **Decision/trade-off:** игрок решает сохранять precision window для elite или тратить его на обычную волну; missed/invalid target не должен скрыто переносить заряд.
- **Stacking intent:** one shared precision meter; ranks improve access/window, not per-weapon crit multipliers.
- **UI copy:** short — «Выбери момент»; detail — «Серия обычных ударов открывает общий точный критический момент.»
- **VFX brief:** compass needle fills a small ring; precision state has one readable accent at the hero, not a permanent starfield.
- **PENDING_BALANCE:** sequence length, crit chance/power response, window duration, eligible sources, reset rule, rank curve.
- **Runtime contract:** CombatSystem owns crit result and meter state; StatsCalculator provides base crit values; passive never reads Star Bow internals.

### 4.10 `passive_spirit_lens` — Духовная линза

- **Fantasy / promise:** линза связывает получение ресурсов, чтение поля и безопасный маршрут, а не одно конкретное заклинание.
- **Axis:** `pickup / information utility`.
- **Activation:** `always_on` for pickup radius; `on_pickup` for a short resource/information pulse.
- **General effect:** расширяет радиус сбора eligible arena drops and XP/mana pickups и кратко выделяет собранный resource path; не превращает pickup в automatic through-wall vacuum.
- **Affected systems:** Magnet/Progression, pickup validation, resource feedback and readable drop priority for the whole run.
- **Synergy anchor:** `weapon_black_eclipse_umbrella` — только condition для `synergy_eclipse_vortex`; passive не меняет pull/burst umbrella behavior.
- **Decision/trade-off:** большой радиус позволяет безопаснее собирать drops, но может заманить игрока к опасной границе; маршрут остаётся выбором.
- **Stacking intent:** one derived pickup radius; artifacts and run passive retain separate source attribution; no XP-to-Gold conversion.
- **UI copy:** short — «Увидь поток»; detail — «Расширяет сбор ресурсов и помогает читать ценность предметов по всему забегу.»
- **VFX brief:** lens ring with dark center and jade rim; no large radial overlay on gameplay.
- **PENDING_BALANCE:** pickup radius, resource whitelist, path pulse duration, wall/LOS rule, rank curve.
- **Runtime contract:** Magnet/Progression owns collection validation; passive provides derived modifier; `xp_drop_collected.v1` remains idempotent.

## 5. Synergy/evolution entries

Все десять entries используют один gate: `weapon_level = 10`, `passive_rank = 10`, matching `synergy_id`, weapon not evolved, non-final `BOSS_CHEST`, `encounter_kind ∈ {MAIN_BOSS, MINI_BOSS}`, `claimed_synergy_count < 5`. Число 10 — обязательный максимум развития для этой пары; оно не меняет вместимость билда 6/6. Связь passive с weapon здесь проверяется только как pair gate; сам passive продолжает работать на общий eligible build. Точные значения и priority при нескольких eligible pairs — `PENDING_BALANCE/PRODUCT`.

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
  max_claimed_per_run: 5
  weapon_level_required: 10
  passive_rank_required: 10
  eligible_sources: [BOSS_CHEST]
  eligible_encounter_kinds: [MAIN_BOSS, MINI_BOSS]
  eligible_checkpoints_seconds: [300, 450, 600, 750, 900, 1050, 1200, 1350, 1500, 1650]
  main_boss_non_final_checkpoints_seconds: [300, 600, 900, 1200, 1500]
  mini_boss_checkpoints_seconds: [450, 750, 1050, 1350, 1650]
  final_boss_checkpoint_seconds: 1800
  final_boss_chest: forbidden
  after_cap: FALLBACK_REQUIRED
  duplicate_claim: idempotent_noop
```

Рекомендуемый ритм: main boss chest на 300/600/900/1200/1500 секундах, mini-boss chest на 450/750/1050/1350/1650 секундах, финальный boss на 1800 секундах без chest. Числа и encounter ownership требуют Architecture/Balance sync; этот документ фиксирует content target: десять возможностей получить synergy chest до финала при общем cap 5.

Если у игрока одновременно несколько eligible pairs, порядок выбора должен быть deterministic и видимым в projection; конкретная priority policy остаётся `PENDING_PRODUCT_DECISION`. Шестой claim запрещён даже после финального босса. Если gate не выполнен, chest выдаёт fallback reward по `C3_MINI_BOSSES_AND_CHEST_FLOW.md`.

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
