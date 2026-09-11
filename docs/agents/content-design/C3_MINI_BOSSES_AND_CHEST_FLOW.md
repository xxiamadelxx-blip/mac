# C3 — Будущие противники, боссы и поток checkpoint-наград

Статус пакета: `CONTENT_SPECIFIED`

Это content-only proposal для расширения первого забега до 30 минут. Пять mini-boss ID, два main-boss extension ID, четыре future enemy ID и дополнительные поля encounter/chest требуют синхронизации Architecture/Runtime. Мокапы, sprites, VFX assets и production manifests этим документом не создаются.

Existing first-run roster остаётся каноническим и не заменяется. Четыре regular enemy proposals не добавляются в Run 1 автоматически; пять mini-boss proposals и два main-boss extension proposals описаны как content layer. Десять нефинальных boss encounters получают BOSS_CHEST; ещё пять зарезервированных ELITE_CHEST windows предназначены для bounded elite variants. Их cadence и numeric budget остаются PENDING_BALANCE/PENDING_ARCHITECTURE.

### Existing first-run IDs — protected boundary

The following records are canonical for Run 1 and are not replaced by this C3 proposal:

| Type | Stable IDs |
|---|---|
| Активные обычные | enemy_ink_beetle, enemy_lantern_moth, enemy_bone_carp, enemy_paper_ghost, enemy_jade_toad, enemy_mirror_fox, enemy_bell_crab, enemy_thread_doll, enemy_lotus_usher, enemy_moonroot_burrower |
| Совместимость | enemy_stone_oni, enemy_eclipse_serpent (не входят в 10 активных) |
| Только будущее | enemy_silver_reed_seer, enemy_moontrail_stalker (не входят в Run 1) |
| Boss | boss_hua_lin, boss_miyeon, boss_seika, boss_black_moon_empress |

The four future enemy IDs, five mini-boss IDs and two main-boss extension IDs in this file are content proposals. They remain outside the runtime Registry until Architecture/Balance approve their registry shape and stage placement.


## 1. Ритм первого забега

Content target первого забега — 30 минут / 1800 секунд. Шесть main-boss checkpoints идут каждые пять минут; checkpoint на 30:00 — финальный босс без boss chest. Пять mini-boss encounters стоят между main-boss checkpoints и продолжают run clock, волны, XP и ordinary spawn. Точные encounter timers являются content cadence proposal для Balance/Architecture и не заменяют их контракт молча.

| Время | Encounter | Chest | Synergy opportunity |
|---:|---|---|---|
| 05:00 | Main Boss 1 | BOSS_CHEST | да, если есть eligible pair и cap не достигнут |
| 07:30 | Mini-boss A — Чернильный Нефритовый Страж | BOSS_CHEST, encounter_kind: MINI_BOSS | да |
| 10:00 | Main Boss 2 | BOSS_CHEST | да |
| 12:30 | Mini-boss B — Жнец Завесы | BOSS_CHEST, encounter_kind: MINI_BOSS | да |
| 15:00 | Main Boss 3 | BOSS_CHEST | да |
| 17:30 | Mini-boss C — Хранительница Лотосового Обряда | BOSS_CHEST, encounter_kind: MINI_BOSS | да |
| 20:00 | Main Boss 4 — Регент Чёрного Прилива | BOSS_CHEST | да |
| 22:30 | Mini-boss D — Колокольный аскет | BOSS_CHEST, encounter_kind: MINI_BOSS | да |
| 25:00 | Main Boss 5 — Архивариус Лунных Знаков | BOSS_CHEST | да |
| 27:30 | Mini-boss E — Луннокорневой перевозчик | BOSS_CHEST, encounter_kind: MINI_BOSS | да |
| 30:00 | Final Boss — Чёрная Лунная Императрица | chest не создаётся | нет |

Таким образом, content proposal содержит десять нефинальных BOSS_CHEST windows, способных разрешить synergy или fallback. Лимит остаётся пятью claims за забег: наличие десяти eligible windows не гарантирует получение пяти синергий. Пять дополнительных ELITE_CHEST windows из bounded elite variants не увеличивают synergy cap и по умолчанию ведут в artifact/upgrade/fallback flow.

## 1.1 Main-boss extension proposals

Эти два main-boss ID закрывают content-часть пользовательского расширения с четырёх до шести checkpoints. Они сопоставлены архитектурным slots 04/05 как proposals; этот документ не изменяет Architecture Registry.

| Architecture slot | Content ID | Рабочее имя | Checkpoint |
|---|---|---|---:|
| boss_extension_slot_04 | boss_tideglass_regent | Регент Чёрного Прилива | 20:00 |
| boss_extension_slot_05 | boss_omen_paper_archivist | Архивариус Лунных Знаков | 25:00 |

### boss_tideglass_regent — Регент Чёрного Прилива

- Silhouette brief: высокая фигура в плаще из тёмных полупрозрачных пластин, три приливных кольца вокруг корпуса и один тёплый ivory crest; силуэт должен читаться как управляющий потоками.
- Role/signature: flow director; создаёт видимые дуги прилива, которые временно разделяют безопасный проход и pressure route.
- Readable telegraph: сначала возникает источник прилива, затем дуга заполняется smoky teal и только после этого разрешается.
- Arena interaction: дуги меняют маршрут, но не становятся невидимыми стенами; XP и pickups остаются читаемыми.
- Player counter-decision: перейти в безопасный коридор и потерять часть damage uptime или переждать convergence ради окна уязвимости.
- Phase/spawn behavior: safe external spawn; следующая фаза меняет направление/порядок дуг, а не добавляет нечитабельный damage class.
- VFX/audio/haptic hooks: tide source, ivory edge, muted jade resolve, полный cleanup; стеклянный низкий sweep и один короткий pulse на resolve.
- Drop/reward boundary: один non-final BOSS_CHEST, synergy/fallback only; artifact offer и wallet mutation запрещены.
- Balance questions: current spacing, warning lead, corridor width, phase threshold, recovery, damage, boss resistance и performance cap — PENDING_BALANCE/PENDING_B1.

### boss_omen_paper_archivist — Архивариус Лунных Знаков

- Silhouette brief: тонкая фигура с веером бумажных талисманов, прямоугольной лунной маской и тремя подвесными печатями; силуэт не должен сливаться с paper ghost.
- Role/signature: pattern sequencer; раскладывает ограниченную последовательность знаков и разрешает её в заранее читаемом порядке.
- Readable telegraph: знак появляется как warm ivory outline, порядок активации показывается короткой линией связи, resolve имеет отдельный muted brass edge.
- Arena interaction: активные знаки создают временные зоны угрозы, но не блокируют движение и не скрывают обычные telegraphs.
- Player counter-decision: быстро уничтожить активный знак, сохранить cooldown для окна boss vulnerability или сменить позицию по известному порядку.
- Phase/spawn behavior: safe external spawn; phase transition меняет порядок/ритм знаков, сохраняя ту же grammar telegraph.
- VFX/audio/haptic hooks: paper fold on trigger, ivory seal, smoky teal resolve, clean retract on expiry; сухой шелест и двойной щелчок на phase shift.
- Drop/reward boundary: один non-final BOSS_CHEST; final-boss no-chest rule не меняется.
- Balance questions: active mark count, warning lead, sequence length, zone duration, vulnerability window, phase threshold, damage and add budget — PENDING_BALANCE/PENDING_B1.

## 2. Mini-boss A — `miniboss_ink_jade_warden`

Рабочее имя: **Чернильный Нефритовый Страж**.

Статус ID: `PROPOSED`, `REGISTRY_SYNC_PENDING`.

### Роль и skill-check

Первый минибосс проверяет, умеет ли игрок читать ground telegraph и менять маршрут. Он не должен быть просто «обычным врагом с большим HP»: его опасность — в складывающихся линиях, закрывающих пространство.

- **Arena role:** space controller; short encounter, pressure grows through geometry, not raw stat inflation.
- **Signature:** чернильные нефритовые печати появляются до удара и соединяются в линии.
- **Player question:** где будет следующий безопасный проход и когда выгодно остановиться для каста?
- **Counters:** movement speed, evasion timing, spell size used deliberately, controlled area damage and patience between telegraphs.
- **Failure mode:** overlapping lines leave a narrow but readable gap; no invisible damage and no unavoidable full-arena hit.

### Pattern kit

1. **Чернильная печать:** несколько ground markers раскрываются с задержкой; после warning line становится dangerous и затем исчезает.
2. **Складка завесы:** две линии медленно сходятся, оставляя один moving safe lane; safe lane is visible before movement.
3. **Нефритовый разлом:** Страж проводит направленный sweep через arena; после sweep остаётся короткое окно для damage.
4. **Переход фазы:** при approved health threshold Страж меняет rotation/spacing, но не добавляет новый нечитабельный damage class.

Точные HP, duration, warning time, damage, immunity, phase threshold и add composition — `PENDING_BALANCE`. Нельзя компенсировать плохой telegraph большим количеством здоровья.

### Reward intent

После defeat создаётся один `BOSS_CHEST` с `encounter_kind: MINI_BOSS` и `checkpoint_id` этого encounter. При наличии eligible pair игрок получает шанс выбрать synergy/evolution. Если пары нет, срабатывает общий fallback из раздела 4.

### Visual Lab brief

- `route`: `SPRITE` + `VFX` + `UI_ART`.
- `stage_path`: `docs/mockups/05-bosses/`; это brief, не запись в stage.
- `asset_id`, `family_id`, `candidate_id`: `null` до Visual Lab intake.
- `status`: `PROPOSED`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.
- `visual code`: smoky teal/soft jade body language, warm ivory telegraph, muted brass edge; no toxic neon ink.

## 3. Mini-boss B — `miniboss_veil_harvester`

Рабочее имя: **Жнец Завесы**.

Статус ID: `PROPOSED`, `REGISTRY_SYNC_PENDING`.

### Роль и skill-check

Второй минибосс проверяет target priority, чтение delayed projectile и дисциплину маршрута. Он приходит после второго main boss и должен создавать другую задачу, а не повторять пространственные линии Стража.

- **Arena role:** priority hunter; pressure follows target selection and delayed threats.
- **Signature:** Жнец оставляет безмолвные shadow markers, а затем атакует по ним с задержкой.
- **Player question:** продолжать damage по Жнецу или сначала очистить безопасный маршрут от отложенных угроз?
- **Counters:** target focus, repositioning, pickup discipline and identifying the real body among bounded decoy shadows.
- **Failure mode:** decoys confuse target priority but never hide the actual attack telegraph; damage source must remain attributable.

### Pattern kit

1. **Тихая метка:** на земле появляется shadow marker; через warning interval в него приходит направленный strike.
2. **Двойной след:** Жнец оставляет два delayed paths, один из которых является safe decoy; оба показываются заранее, настоящий порядок разрешения видим.
3. **Сборщик долгов:** временно помечает highest-threat/nearest route target; если игрок продолжает стоять на линии, marker resolves в узкий burst.
4. **Переход фазы:** после approved health threshold Жнец сокращает delay или меняет target priority, но сохраняет читаемую форму telegraph.

Точные HP, delay, marker count, decoy rule, target selector, damage, phase threshold и boss immunity — `PENDING_BALANCE`/`PENDING_ARCHITECTURE`.

### Reward intent

После defeat создаётся ровно один chest, привязанный к `encounter_id`. Успешный synergy claim расходует один из пяти run claims; fallback не расходует cap и не считается synergy.

### Visual Lab brief

- `route`: `SPRITE` + `VFX` + `UI_ART`.
- `stage_path`: `docs/mockups/05-bosses/`; production assets остаются у Visual Lab.
- `asset_id`, `family_id`, `candidate_id`: `null` до Visual Lab intake.
- `status`: `PROPOSED`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.
- `visual code`: deep blue-grey silhouette, warm ivory target marker, restrained violet only for status distinction; no black-on-black telegraph.


## 3.4 Mandatory field coverage for the five mini-bosses

The five mini-boss entries above define role, signature, player question, counters, patterns, reward intent and visual direction. To close the canonical C3 field set, the following explicit fields apply to each entry:

### miniboss_ink_jade_warden

- Silhouette brief: broad shoulders, smoky jade mask, heavy shoulder guard and two ink ribbons that fold into geometric lines; the body must read as a space controller, not a large rusher.
- Arena interaction: folding lines alter the route but never become collision walls; safe lanes remain visible and XP stays readable.
- Phase/spawn behavior: safe external spawn; an approved health threshold changes rotation/spacing only; add composition, phase threshold and interruption rules remain pending.
- VFX/audio/haptic hooks: seal trigger, ivory line warning, jade/brass resolve flash, visible recovery and full cleanup; low ink stroke plus one brass fracture note; one light haptic tap on resolve and one stronger tap on phase change.
- Drop/reward boundary: authoritative defeat enters checkpoint reward, then one non-final BOSS_CHEST proposal; no artifact offer and no direct wallet mutation.
- Balance questions: HP, damage, speed, warning lead time, line geometry, safe-lane width, phase threshold, add composition, recovery and reward weight are PENDING_BALANCE/PENDING_B1.

### miniboss_veil_harvester

- Silhouette brief: tall blue-grey hooded figure with crescent mask and dense body shape that is distinct from the shadow markers; violet is a restrained status accent only.
- Arena interaction: delayed shadow paths change the route temporarily but do not block movement or hide other telegraphs; resolution order is visible.
- Phase/spawn behavior: safe external spawn after the second main boss checkpoint; an approved health threshold may shorten delay or change target priority without changing telegraph grammar; all selector and immunity rules remain pending.
- VFX/audio/haptic hooks: ivory marker trigger, smoky teal path, restrained violet/silver strike, inward fold on expiry and full cleanup; muted click, dry slice and low phase double-note; one short haptic tap per first marker state.
- Drop/reward boundary: defeat creates one checkpoint-owned BOSS_CHEST; a selected synergy consumes one of five run claims, fallback consumes zero; final boss remains no-chest.
- Balance questions: HP, damage, speed, marker delay, marker geometry, target priority, phase threshold, recovery, resistance, VFX cap and reward weight are PENDING_BALANCE/PENDING_B1.

## 3.1 Mini-boss C — miniboss_lotus_ritekeeper

Рабочее имя: **Хранительница Лотосового Обряда**.

Статус ID: PROPOSED, REGISTRY_SYNC_PENDING.

### Роль и skill-check

Хранительница проверяет target priority и умение прерывать защитный ритуал, не теряя контроль над ордой. Её задача отличается от линий Стража и delayed markers Жнеца: игрок выбирает между прямым damage по mini-boss и разрушением опорных печатей.

- Arena role: support ritual controller.
- Signature: три lotus anchors связывают ближайшую группу и дают ей читаемое состояние защиты; связь видна до любого усиления.
- Player question: сломать anchor сейчас или использовать окно и добить саму Хранительницу?
- Counters: target switching, burst timing, area control and reading the exposed anchor.
- Failure mode: если anchors пересекаются, между ними остаётся проход; ritual не превращается в невидимый full-arena lock.

### Pattern kit

1. **Лотосовая печать:** anchor раскрывается с ivory outline, затем создаёт видимую связь с выбранной целью.
2. **Процессия лепестков:** anchors медленно перемещаются по дуге, оставляя один читаемый gap для прохода.
3. **Незавершённый обряд:** при активной связи Хранительница получает защитное состояние; уничтожение anchor открывает короткое окно уязвимости.
4. **Переход фазы:** меняется порядок anchor и направление дуги, но не grammar telegraph.

Точные HP, anchor count, link duration, protection rule, warning lead, phase threshold, damage и support composition — PENDING_BALANCE/PENDING_B1.

### Reward intent

После authoritative defeat создаётся один BOSS_CHEST с encounter_kind MINI_BOSS. Eligible synergy может быть выбрана в рамках общего cap 5; при отсутствии pair используется fallback из раздела 4.

### Visual Lab brief

- route: SPRITE + VFX + UI_ART.
- stage_path: docs/mockups/05-bosses/; asset_id/family_id/candidate_id остаются null до Visual Lab intake.
- visual code: soft jade lotus crown, warm ivory anchors, smoky teal links, muted crimson только для phase/status accent.
- technical_status: NOT_RUN; artistic_status: PENDING.

## 3.2 Mini-boss D — miniboss_bell_rhythm_ascetic

Рабочее имя: **Колокольный аскет**.

Статус ID: PROPOSED, REGISTRY_SYNC_PENDING.

### Роль и skill-check

Аскет проверяет ритм движения и чтение expanding rings. Урон не должен зависеть только от звука: каждая фаза звонка имеет видимый внешний и внутренний контур.

- Arena role: timing and rhythm controller.
- Signature: колокол создаёт чередующиеся резонансные кольца с gap, который можно прочитать и пересечь.
- Player question: перейти через gap, удержать позицию для damage или отступить и потерять tempo?
- Counters: movement timing, dash/evasion discipline and damage during the recovery beat.
- Failure mode: визуальный контур появляется раньше resolve; audio/haptic только усиливают, но не заменяют сигнал.

### Pattern kit

1. **Первый звон:** внешний ivory ring расширяется с видимым safe gap.
2. **Тишина между ударами:** кольцо замирает, gap смещается и остаётся читаемым до resolve.
3. **Возвратный тон:** после паузы идёт более узкий inner ring; оба контура не сливаются.
4. **Переход фазы:** меняется порядок колец и recovery window, но сохраняется одна понятная beat grammar.

Точные HP, ring speed, gap width, warning lead, damage, phase threshold, interruption и boss resistance — PENDING_BALANCE/PENDING_B1.

### Reward intent

После defeat создаётся один BOSS_CHEST с encounter_kind MINI_BOSS. Успешный synergy claim расходует один из пяти claims; fallback не расходует cap.

### Visual Lab brief

- route: SPRITE + VFX + UI_ART.
- stage_path: docs/mockups/05-bosses/; candidate_id null до intake.
- visual code: restrained brass bell, warm ivory rings, deep blue-grey body, muted teal recovery pulse; без black-on-black.
- technical_status: NOT_RUN; artistic_status: PENDING.

## 3.3 Mini-boss E — miniboss_moonroot_ferryman

Рабочее имя: **Луннокорневой перевозчик**.

Статус ID: PROPOSED, REGISTRY_SYNC_PENDING.

### Роль и skill-check

Перевозчик проверяет решение о маршруте и приоритет угрозы: он ведёт видимый convoy врагов к краю арены, а игрок решает, когда перехватить его. Он не крадёт Gold, XP или pickups и не создаёт фальшивые предметы.

- Arena role: convoy pressure and route commitment.
- Signature: moonroot barge/line движется по заранее показанному маршруту и временно тянет отмеченных врагов в одну сторону.
- Player question: продолжать damage по мини-боссу или перерезать convoy, пока он не занял выгодную для орды позицию?
- Counters: route reading, focus fire, controlled movement and choosing an interception point.
- Failure mode: маршрут и endpoint всегда видны; convoy не телепортируется и не превращается в permanent collision wall.

### Pattern kit

1. **Лунный маршрут:** корневая линия появляется от края к endpoint, затем перевозчик начинает движение.
2. **Корневые ворота:** два видимых gate markers сужают проход на время, оставляя минимум один читаемый обход.
3. **Смена прилива:** convoy меняет направление после warning pulse, но не меняет endpoint скрытно.
4. **Переход фазы:** растёт сложность маршрута и target priority, а не raw stat inflation.

Точные HP, route duration, convoy size, pull/drag rule, gate geometry, warning lead, phase threshold и recovery — PENDING_BALANCE/PENDING_B1.

### Reward intent

После authoritative defeat создаётся один BOSS_CHEST с encounter_kind MINI_BOSS. Boss chest не выдаёт artifact offer; при отсутствии eligible pair применяется fallback.

### Visual Lab brief

- route: SPRITE + VFX + UI_ART.
- stage_path: docs/mockups/05-bosses/; candidate_id null до Visual Lab intake.
- visual code: moonroot deep teal, ivory route line, muted jade root joints and restrained brass endpoint mark.
- technical_status: NOT_RUN; artistic_status: PENDING.

### miniboss_lotus_ritekeeper

- Silhouette brief: folded lotus crown, three hanging anchor seals and a compact ritual stance; the body must read as support controller.
- Arena interaction: anchors alter enemy protection and route pressure but never become collision walls; XP remains readable.
- Phase/spawn behavior: safe external spawn; phase changes anchor order/spacing; selector, interrupt and support pack rules remain pending.
- VFX/audio/haptic hooks: ivory anchor outline, smoky teal link, jade resolve and full cleanup; petal click and one soft phase note; short haptic on anchor resolve.
- Drop/reward boundary: one non-final MINI_BOSS BOSS_CHEST; no artifact offer and no wallet mutation.
- Balance questions: HP, anchor count, duration, protection, warning lead, damage, phase threshold, support composition and reward weight are PENDING_BALANCE/PENDING_B1.

### miniboss_bell_rhythm_ascetic

- Silhouette brief: narrow ascetic body, restrained brass bell and visible ring-emitter posture; readable without audio.
- Arena interaction: rings alter safe movement only; every gap is visible before resolve and no ring permanently blocks the arena.
- Phase/spawn behavior: safe external spawn; phase changes ring ordering and recovery; speed, gap, interruption and resistance remain pending.
- VFX/audio/haptic hooks: ivory outer/inner contours, brass resolve, teal recovery fade and full cleanup; audio/haptic reinforce but never replace the telegraph.
- Drop/reward boundary: one non-final MINI_BOSS BOSS_CHEST; synergy claim or fallback only.
- Balance questions: ring speed, gap width, warning lead, damage, phase threshold, recovery and VFX cap are PENDING_BALANCE/PENDING_B1.

### miniboss_moonroot_ferryman

- Silhouette brief: low root-barge body with a crescent lantern and visible route harness; distinct from Burrower and existing Bell Crab.
- Arena interaction: convoy route shifts enemy formation but does not steal pickups, mutate wallet or create collision walls.
- Phase/spawn behavior: safe edge spawn; phase changes route direction/priority; convoy size, endpoint, drag and interruption remain pending.
- VFX/audio/haptic hooks: ivory route line, teal root joints, jade endpoint pulse and complete route cleanup; low wood scrape plus one route-change tap.
- Drop/reward boundary: one non-final MINI_BOSS BOSS_CHEST; no artifact offer and no direct wallet mutation.
- Balance questions: HP, route duration, convoy size, drag rule, gate geometry, warning lead, recovery, phase threshold and reward weight are PENDING_BALANCE/PENDING_B1.

## 3.5 Future enemy proposal batch

These four entries are future-stage proposals only. They do not enter the first-run registry, do not change the 30-minute content target and do not replace any of the ten canonical enemy IDs.

### enemy_lotus_usher — Лотосовый распорядитель

Status: PROPOSED, REGISTRY_SYNC_PENDING.

- Silhouette brief: narrow tall figure with a lotus collar, two hanging binding ribbons and a small bell knot on the back; vertical silhouette and visible links are the primary recognition cues.
- Role/signature: support tether. The Usher selects two enemy targets and joins them with a lotus knot. While the link is active, the pair receives one shared guard/resonance state; formula and strength belong to Balance.
- Readable telegraphs: paired lotus mark appears first, a visible thread connects the targets second, and the knot gives a short ivory pulse before any guard refresh.
- Arena interaction: the thread is a route marker without collision; it must not hide ground telegraphs. Defeating the Usher or applying the approved break rule changes the linked pair state.
- Player counter-decision: remove the support enemy to weaken the pack or continue pressure on the priority target while accepting temporary protection. The linked targets and consequence must be visible.
- Phase/spawn behavior: future support packs only, external safe spawn, deterministic target selector from seed/state revision. Pack size, active link cap and spawn budget are PENDING_BALANCE/PENDING_B1.
- VFX/audio/haptic hooks: trigger is the lotus mark; active phase is a thin smoky teal thread with an ivory knot; resolve is a jade/brass pulse; expiry retracts the thread and clears it. Audio is one soft knot click on create and one dry bell on break. Haptic is one short pulse on link-state change.
- Drop/reward boundary: normal XP and aftermath after authoritative defeat; no Gold, boss chest, artifact offer or direct wallet mutation. Special drops require a separate C4/Balance contract.
- Balance questions: guard rule, duration, link range, refresh, break condition, target selector, spawn budget, XP grade/value, elite interaction and performance cap are PENDING_BALANCE/PENDING_ARCHITECTURE.

### enemy_moonroot_burrower — Луннокорневой землерой

Status: PROPOSED, REGISTRY_SYNC_PENDING.

- Silhouette brief: low root-backed body with a rounded moon bud on the head, short digging limbs and a visible soil line under the body; horizontal profile and emergence trail distinguish it from the existing crab.
- Role/signature: ambush route shaper. The Burrower previews a path below the arena, emerges at an endpoint and leaves a temporary root patch that changes the safe route.
- Readable telegraphs: a segmented moving soil ridge precedes the emergence, a root circle opens at the endpoint and only after the warning window does the zone resolve. Burrowing is not invisible movement.
- Arena interaction: root patch changes movement by an approved hazard category without becoming a collision wall. Water and ground may have different surface reactions, but danger remains one readable rule.
- Player counter-decision: leave the endpoint and preserve a route or stay close to punish the emergence and recovery window.
- Phase/spawn behavior: future ambush bands with external safe spawn and safe-spawn validation; emergence timing, patch lifetime, interruptibility and hazard overlap are PENDING_BALANCE/PENDING_ARCHITECTURE.
- VFX/audio/haptic hooks: ripple trail on trigger, two-stage ivory root circle in warning, jade endpoint burst on resolve and roots retracting on expiry. Audio is a muted scrape followed by one low impact. Haptic is one weak pulse on zone creation, never a loop.
- Drop/reward boundary: normal XP and aftermath only; root cleanup does not create XP, Gold, a chest or an artifact offer.
- Balance questions: trail lead time, endpoint selector, patch geometry, slow/lock category, interrupt rule, recovery window, spawn budget, XP grade/value and pool cost are PENDING_BALANCE/PENDING_B1.

### enemy_silver_reed_seer — Серебряный камышовый провидец

Status: PROPOSED, REGISTRY_SYNC_PENDING.

- Silhouette brief: thin reed-built figure with a long petal sleeve and an elongated silver mask; the sharp upright profile and opening sleeve identify it in a dense pack.
- Role/signature: lane sniper. The Seer selects a straight corridor and fires one long moonline after preparation; it is not a homing projectile.
- Readable telegraphs: the mask turns toward the selected line, a warm ivory guide appears on the ground and the sleeve opens before the line resolves.
- Arena interaction: the line crosses water, bridge or open ground without becoming an invisible wall; after one resolution the Seer enters recovery.
- Player counter-decision: cross before resolution, route around the line while dealing with the pack, or focus the distant threat first.
- Phase/spawn behavior: future ranged-pressure packs with external safe spawn and visible aim lock. Active line count, priority selector and interrupt rule are PENDING_BALANCE/PENDING_ARCHITECTURE.
- VFX/audio/haptic hooks: mask-turn trigger, thin ivory line with smoky teal shadow during aim, short silver flash on resolve and fade from source to endpoint on expiry. Audio is a dry breath then a short firing tone. Haptic is one directional pulse on resolve.
- Drop/reward boundary: standard XP and aftermath; no special currency, boss chest, artifact offer or wallet mutation.
- Balance questions: lead time, width class, damage category, interrupt rule, recovery, target selector, spawn budget, XP grade/value and telegraph overlap budget are PENDING_BALANCE/PENDING_B1.

### enemy_moontrail_stalker — Лунный следопыт

Status: PROPOSED, REGISTRY_SYNC_PENDING.

- Silhouette brief: four-legged smoky figure with a crescent muzzle and a narrow trail that repeats the last movement direction; it has no fox-like shard tail and no clone flash.
- Role/signature: predictive flanker. The Stalker records a short recent route, fixes an endpoint and attacks along a shown crescent instead of teleporting behind the player.
- Readable telegraphs: smoky teal trail appears first, an ivory crescent opens at the endpoint and the body locks briefly before the dash.
- Arena interaction: the trail marks a route segment but does not block it or persist as a permanent hazard. Changing direction before resolution reduces the threat value.
- Player counter-decision: change direction, leave the crescent or spend damage during the lock window; standing on the marked route is a clear, avoidable risk.
- Phase/spawn behavior: future flank bands after support/ranged pressure is introduced; safe edge spawn and an available escape zone are required. Prediction horizon, dash recovery, pairing and active cap are PENDING_BALANCE/PENDING_ARCHITECTURE.
- VFX/audio/haptic hooks: trail-record trigger, crescent fill during lock, short silver/jade arc on resolve and backward trail dissolve on expiry. Audio is a dry rustle and low dash snap. Haptic is one directional tap on lock.
- Drop/reward boundary: ordinary XP and aftermath; no Gold, boss chest, artifact offer or synergy-counter change.
- Balance questions: prediction horizon, arc geometry, lead time, dash damage category, recovery, safe-spawn distance, active cap, XP grade/value and overlap with existing teleport/dash patterns are PENDING_BALANCE/PENDING_B1.


## 3.6 Content-only reward-window map

Это контентная раскладка для сверки с 15 архитектурными chest windows. Она не переписывает Architecture Registry и не фиксирует numeric cadence элитных вариантов.

| Content window group | Source kind | Windows | Outcome policy | Synergy |
|---|---|---|---|---|
| C01–C05 | MAIN_BOSS_NON_FINAL | 300, 600, 900, 1200, 1500 | BOSS_CHEST: eligible synergy, иначе upgrade/fallback | allowed, общий cap 5 |
| C06–C10 | INTERMEDIATE_BOSS | 450, 750, 1050, 1350, 1650 | BOSS_CHEST: eligible synergy, иначе upgrade/fallback | allowed, общий cap 5 |
| C11–C15 | ELITE_VARIANT | Balance-selected bounded elite peaks | ELITE_CHEST: artifact offer из 3 карт или upgrade/fallback | запрещена по умолчанию |

Content invariant: C01–C10 дают десять отдельных non-final boss chest opportunities, но один chest claim выбирает максимум одну synergy, а run counter никогда не превышает 5. C11–C15 не расходуют synergy counter и не превращаются в boss chest. Final boss на 1800 секунд не создаёт chest.

Для каждой строки нужны source_id, encounter_id/drop_id, state_revision, outcome policy и idempotency semantics на стороне Architecture/Runtime. До их подтверждения эта таблица имеет статус CONTENT_PROPOSAL_FOR_RECONCILIATION.

## 4. Единый chest resolver

### 4.1 Проверка при defeat

После authoritative defeat `BossChestSystem`/`RewardLedger` оценивают encounter один раз:

```text
if encounter already rewarded:
    return idempotent_noop

eligible_pairs = pairs where
    weapon_level == 10
    passive_rank == 10
    weapon_not_evolved
    matching weapon/passive pair
    claimed_synergy_count < 5

if eligible_pairs is not empty:
    create synergy-capable BOSS_CHEST
else if any weapon/passive has legal upgrade:
    create regular upgrade fallback
else:
    create approved reward fallback
```

`eligible_pairs` оцениваются одинаково для Main Boss и Mini-boss. Mini-boss не получает скрытый отдельный synergy rule и не может выдать шестой claim.

### 4.2 Что получает игрок

| Состояние билда | Chest result | Влияние на cap |
|---|---|---|
| Есть одна или несколько eligible pairs, claims < 5 | synergy/evolution offer по существующему Boss Chest flow | выбранная synergy: `+1`; отказ/невыбор — `+0` |
| Pair пока не собрана, есть legal weapon/passive upgrade | regular upgrade fallback | `+0` |
| Pair не собрана, upgrade offer невозможен | approved reward fallback из RewardLedger | `+0` |
| Уже 5 claims | regular upgrade/reward fallback, без synergy card | `+0` |
| Final Boss | chest не создаётся | `+0` |

Fallback должен быть полезным, но не должен маскироваться под evolution. Рекомендуемый reward pool для третьего случая: существующий разрешённый `RewardLedger` outcome — Gold, Boss Essence, Lunar Seal или recovery/resource reward в зависимости от текущего run contract. Exact choice, amount and rarity — `PENDING_BALANCE`/`PENDING_PRODUCT_DECISION`.

### 4.3 Если eligible pair несколько

Content фиксирует только безопасность выбора:

- все eligible IDs должны быть получены из authoritative build snapshot;
- один chest не может claim больше одной synergy;
- выбранная карта превращает weapon в evolved state и расходует один claim;
- невыбранные карты не должны автоматически считаться claimed;
- deterministic ordering/priority и количество synergy cards в chest — `PENDING_PRODUCT_DECISION`;
- если offer construction не может показать eligible pair, используется fallback, а не пустой экран.

## 5. Run cap и anti-exploit contract

```yaml
synergy_run_policy:
  max_claimed_per_run: 5
  weapon_level_required: 10
  passive_rank_required: 10
  eligible_encounter_kinds: [MAIN_BOSS, MINI_BOSS]
  eligible_checkpoint_seconds: [300, 450, 600, 750, 900, 1050, 1200, 1350, 1500, 1650]
  mini_boss_checkpoints_seconds: [450, 750, 1050, 1350, 1650]
  main_boss_non_final_checkpoints_seconds: [300, 600, 900, 1200, 1500]
  final_boss_checkpoint_seconds: 1800
  final_boss_chest: forbidden
  fallback_after_missing_requirements: required
  duplicate_reward_for_same_encounter: idempotent_noop
```

- Counter увеличивается только на подтверждённый `synergy_claimed.v1`, не на появление chest и не на preview.
- Повторная доставка defeat/reward для одного `encounter_id` — idempotent no-op.
- После пятого claim resolver не создаёт скрытых evolution cards.
- Mini-boss chest не выдаёт artifact offer вместо Boss Chest; artifact offer остаётся отдельным `ArtifactOfferSystem` contract.
- Reward fallback не изменяет weapon/passive slot capacity и не обходит max weapon level/passive rank.
- Replay/snapshot должны хранить encounter state, chest outcome, selected synergy ID и `claimed_synergy_count`.

## 6. Architecture/Balance handoff

### Architecture

- Добавить/подтвердить пять mini-boss encounter IDs и два main-boss extension IDs в Content Registry; сохранить `encounter_kind: MINI_BOSS` для промежуточных боёв.
- Решить, достаточно ли существующего `BOSS_CHEST` source с encounter kind или нужен новый canonical source; content не объявляет новый event.
- Закрепить checkpoint ownership, pause/clock semantics, defeat idempotency и snapshot fields.
- Сохранить раздельность Boss Chest и Artifact Offer.

### Balance

- Закрепить main/mini cadence, HP budget, phase threshold, telegraph lead time, damage, resistances, add composition и reward weights.
- Проверить, что десять BOSS_CHEST windows не гарантируют чрезмерный power spike при удачном билде, а пять ELITE_CHEST windows остаются отдельным artifact/upgrade потоком.
- Протестировать три состояния fallback: недособранная pair, заполненный build, cap reached.

## 7. Visual Lab handoff

Мокапы и ассеты отсутствуют намеренно. Visual Lab получает пять mini-boss briefs и два main-boss extension briefs с `candidate_id: null`, `status: PROPOSED`, `technical_status: NOT_RUN`, `artistic_status: PENDING`. Нужно отдельно проверить силуэты, warning readability at 390×844, true 1× combat scale, cleanup и отсутствие токсичных/neon цветов.

## 8. Живая граница C3

Родительский main для этой сверки: ec30c239aa22aa1d9c8ad1faab25d99633f4cb29. Архитектурная карта 0b8cb1bb96d4ab2d0bd14bd7a21b042e53d8c5e8 разделяет активный набор и совместимость.

| Группа | Записи | Статус в контенте |
|---|---|---|
| Активные обычные | 8 существующих записей + enemy_lotus_usher + enemy_moonroot_burrower | CONTENT_SCOPE_CLOSED; новые записи остаются PROPOSED |
| Совместимость | enemy_stone_oni, enemy_eclipse_serpent (не входят в 10) | LEGACY_PRESERVED |
| Только будущее | enemy_silver_reed_seer, enemy_moontrail_stalker (не входят в Run 1) | PROPOSED |

Пять мини-боссов и два расширения главных боссов имеют stable semantic IDs, encounter kind, checkpoint и зависимости. Их контентные записи не являются runtime, balance или artistic approval.

Для всех новых записей действует PROPOSED_ONLY: нельзя считать их финальными именами, production-ассетами или зафиксированными числовыми профилями.
