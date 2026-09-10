# C3 — Два промежуточных минибосса и поток сундуков

Статус пакета: `CONTENT_SPECIFIED`

Это content proposal для расширения первого забега. Новые mini-boss IDs и дополнительные поля encounter/chest требуют синхронизации Architecture/Runtime. Мокапы, sprites, VFX assets и production manifests этим документом не создаются.

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

