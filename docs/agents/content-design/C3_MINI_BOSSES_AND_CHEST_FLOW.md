# C3 — Будущие противники, боссы и поток checkpoint-наград

Статус пакета: `CONTENT_SPECIFIED`

Это content-only proposal для будущего контента и расширения checkpoint flow первого забега. Два mini-boss ID, четыре future enemy ID и дополнительные поля encounter/chest требуют синхронизации Architecture/Runtime. Мокапы, sprites, VFX assets и production manifests этим документом не создаются.

Existing first-run roster остаётся каноническим и не заменяется. Четыре regular enemy proposals ниже не добавляются в Run 1 автоматически; два mini-boss proposal используют пять нефинальных chest windows только после Architecture/Balance sync.
### Existing first-run IDs — protected boundary

The following records are canonical for Run 1 and are not replaced by this C3 proposal:

| Type | Stable IDs |
|---|---|
| Enemy | enemy_ink_beetle, enemy_lantern_moth, enemy_bone_carp, enemy_paper_ghost, enemy_jade_toad, enemy_mirror_fox, enemy_bell_crab, enemy_thread_doll, enemy_stone_oni, enemy_eclipse_serpent |
| Boss | boss_hua_lin, boss_miyeon, boss_seika, boss_black_moon_empress |

The four future enemy IDs and two mini-boss IDs in this file remain proposal-only until Architecture/Balance approve their Registry and stage placement.


## 1. Ритм первого забега

В забеге 20 минут остаются четыре основных boss checkpoints из текущего first-run контракта. Между ними добавляются два самостоятельных mini-boss encounter. Таким образом, до финала игрок получает ровно пять возможностей открыть chest с synergy offer.

| Время | Encounter | Chest | Synergy opportunity |
|---:|---|---|---|
| 05:00 | Main Boss 1 | `BOSS_CHEST` | да, если есть eligible pair и cap не достигнут |
| 07:30 | Mini-boss A — Чернильный Нефритовый Страж | `BOSS_CHEST`, `encounter_kind: MINI_BOSS` | да |
| 10:00 | Main Boss 2 | `BOSS_CHEST` | да |
| 12:30 | Mini-boss B — Жнец Завесы | `BOSS_CHEST`, `encounter_kind: MINI_BOSS` | да |
| 15:00 | Main Boss 3 | `BOSS_CHEST` | да |
| 20:00 | Final Boss | chest не создаётся | нет |

Времена 07:30 и 12:30 — target cadence для Balance/Architecture. Они не заменяют main bosses и не расширяют длительность забега. Если владелец таймера выберет другую cadence, должны сохраниться два mini-boss encounter и пять нефинальных chest windows.

## 2. Mini-boss A — `miniboss_ink_jade_warden`

Рабочее имя: **Чернильный Нефритовый Страж**.

Статус ID: `PROPOSAL`, `REGISTRY_SYNC_PENDING`.

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
- `status`: `PROPOSAL`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.
- `visual code`: smoky teal/soft jade body language, warm ivory telegraph, muted brass edge; no toxic neon ink.

## 3. Mini-boss B — `miniboss_veil_harvester`

Рабочее имя: **Жнец Завесы**.

Статус ID: `PROPOSAL`, `REGISTRY_SYNC_PENDING`.

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
- `status`: `PROPOSAL`; `technical_status: NOT_RUN`; `artistic_status: PENDING`.
- `visual code`: deep blue-grey silhouette, warm ivory target marker, restrained violet only for status distinction; no black-on-black telegraph.


## 3.3 Mandatory field coverage for the two mini-bosses

The existing mini-boss entries above already define role, signature, player question, counters, patterns, reward intent and visual direction. To close the canonical C3 field set, the following explicit fields apply to each entry:

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

## 3.4 Future enemy proposal batch

These four entries are future-stage proposals only. They do not enter the first-run registry, do not change the 20-minute schedule and do not replace any of the ten canonical enemy IDs.

### enemy_lotus_usher — Лотосовый распорядитель

Status: PROPOSAL, REGISTRY_SYNC_PENDING.

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

Status: PROPOSAL, REGISTRY_SYNC_PENDING.

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

Status: PROPOSAL, REGISTRY_SYNC_PENDING.

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

Status: PROPOSAL, REGISTRY_SYNC_PENDING.

- Silhouette brief: four-legged smoky figure with a crescent muzzle and a narrow trail that repeats the last movement direction; it has no fox-like shard tail and no clone flash.
- Role/signature: predictive flanker. The Stalker records a short recent route, fixes an endpoint and attacks along a shown crescent instead of teleporting behind the player.
- Readable telegraphs: smoky teal trail appears first, an ivory crescent opens at the endpoint and the body locks briefly before the dash.
- Arena interaction: the trail marks a route segment but does not block it or persist as a permanent hazard. Changing direction before resolution reduces the threat value.
- Player counter-decision: change direction, leave the crescent or spend damage during the lock window; standing on the marked route is a clear, avoidable risk.
- Phase/spawn behavior: future flank bands after support/ranged pressure is introduced; safe edge spawn and an available escape zone are required. Prediction horizon, dash recovery, pairing and active cap are PENDING_BALANCE/PENDING_ARCHITECTURE.
- VFX/audio/haptic hooks: trail-record trigger, crescent fill during lock, short silver/jade arc on resolve and backward trail dissolve on expiry. Audio is a dry rustle and low dash snap. Haptic is one directional tap on lock.
- Drop/reward boundary: ordinary XP and aftermath; no Gold, boss chest, artifact offer or synergy-counter change.
- Balance questions: prediction horizon, arc geometry, lead time, dash damage category, recovery, safe-spawn distance, active cap, XP grade/value and overlap with existing teleport/dash patterns are PENDING_BALANCE/PENDING_B1.


## 4. Единый chest resolver

### 4.1 Проверка при defeat

После authoritative defeat `BossChestSystem`/`RewardLedger` оценивают encounter один раз:

```text
if encounter already rewarded:
    return idempotent_noop

eligible_pairs = pairs where
    weapon_level == 6
    passive_rank == 5
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
  eligible_encounter_kinds: [MAIN_BOSS, MINI_BOSS]
  eligible_checkpoint_seconds: [300, 450, 600, 750, 900]
  mini_boss_checkpoints_seconds: [450, 750]
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

- Добавить/подтвердить два encounter IDs и `encounter_kind: MINI_BOSS` в Content Registry.
- Решить, достаточно ли существующего `BOSS_CHEST` source с encounter kind или нужен новый canonical source; content не объявляет новый event.
- Закрепить checkpoint ownership, pause/clock semantics, defeat idempotency и snapshot fields.
- Сохранить раздельность Boss Chest и Artifact Offer.

### Balance

- Закрепить main/mini cadence, HP budget, phase threshold, telegraph lead time, damage, resistances, add composition и reward weights.
- Проверить, что пять chest windows не гарантируют чрезмерный power spike при удачном билде.
- Протестировать три состояния fallback: недособранная pair, заполненный build, cap reached.

## 7. Visual Lab handoff

Мокапы и ассеты отсутствуют намеренно. Visual Lab получает два brief-а с `candidate_id: null`, `status: PROPOSAL`, `technical_status: NOT_RUN`, `artistic_status: PENDING`. Нужно отдельно проверить силуэты, warning readability at 390×844, true 1× combat scale, cleanup и отсутствие токсичных/neon цветов.

