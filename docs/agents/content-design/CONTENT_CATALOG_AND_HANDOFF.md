# Content Design — каталог и межагентский handoff

Статус пакета: `CONTENT_SPECIFIED`  
C5 status: `HANDOFF_READY_WITH_OPEN_RECONCILIATIONS`

Пакет фиксирует контент первого забега на 30 минут, постоянное дерево магазина, пять mini-bosses, два main-boss extension proposals, future encounter proposals, семь временных drops арены и C5 cross-system handoff. Он не является runtime implementation, balance lock, visual approval или production-asset delivery.

## 1. Состав среза

| Файл | Назначение | Состояние |
|---|---|---|
| `C0_CONTENT_AUDIT.md` | C0 source-of-truth audit, protected scope и gaps | `READ_ONLY_AUDIT_COMPLETE` |
| `C1_WEAPONS_PASSIVES_SYNERGIES.md` | 10 оружий, 10 run-пассивок, 10 direct pairs/evolutions | `CONTENT_SPECIFIED` |
| `C2_ARTIFACTS.md` | 10 артефактов, trigger/effect/counterplay и offer contract | `CONTENT_SPECIFIED` |
| `C3_MINI_BOSSES_AND_CHEST_FLOW.md` | 4 future enemy proposals, 5 mini-bosses, 2 main-boss extension proposals, 15 content reward windows и fallback resolver | `CONTENT_SPECIFIED` |
| `C4_ARENA_DROP_CATALOGUE.md` | 7 arena drops: heal, Gold, XP magnet, destruction, freeze, ward, vacuum | `CONTENT_SPECIFIED` |
| `C5_CROSS_SYSTEM_HANDOFF.md` | cross-system index, dependency matrix, conflict review and owner handoff | `HANDOFF_READY_WITH_OPEN_RECONCILIATIONS` |
| `META_PASSIVE_TREE.md` | 6 ветвей, 17 stat nodes и shop/persistence contract | `CONTENT_SPECIFIED` |
| `CONTENT_CATALOG_INDEX.json` | машинно читаемый roster/count/limit index | `CONTENT_SPECIFIED` |

## 2. Зафиксированные числа и границы

- 10 weapon IDs и 10 passive IDs из текущего стабильного roster сохранены без переименования.
- 10 synergy IDs сопоставлены с десятью direct pairs; каждая evolution создаёт новое evolved behavior/weapon state, а не новый slot.
- Все 10 run-passives дают общий эффект eligible build; их weapon ID — только synergy anchor для проверки evolution gate, не отдельный weapon buff.
- В одном Run 1 разрешено **максимум 5 synergy claims**. Шестая synergy не появляется даже после финального босса.
- Content target первого забега — 30 минут / 1800 секунд: пять main-boss non-final windows на 300/600/900/1200/1500 и пять mini-boss windows на 450/750/1050/1350/1650 секунд. Все десять BOSS_CHEST windows могут проверить synergy eligibility, но общий cap — 5; при отсутствии eligible content используется fallback.
- C3 добавляет четыре future enemy proposals, пять mini-boss content IDs и два main-boss extension proposals; future enemies остаются вне Run 1 до отдельного stage/Registry decision, а существующие 10 enemy IDs не заменяются.
- Build ограничен 6 weapon slots и 6 passive slots. Для синергии weapon должен достичь 10-го уровня, а связанная passive — 10-го ранга; это content target, пока не синхронизированный с текущей architecture/legacy manifest.
- Артефактов 10; offer содержит ровно 3 candidate IDs, игрок выбирает 1. Content defaults: UNIQUE duplicate, refresh только до выбора, один выбранный ID, отдельный run layer без slot capacity.
- Дерево магазина содержит 6 macro branches и 17 stat nodes, покрывающих характеристики из пользовательского stat-screen reference.
- Покупки meta tree выполняются только в hub/shop за Gold и применяются со следующего забега.
- C4 содержит 7 arena drop IDs. Их source cadence, quantity, effect duration/radius, frequency и target caps не зафиксированы content-агентом; drops не заменяют XP/aftermath, chest, artifact offer или checkpoint reward.
- Content proposal для 15 chest windows: C01–C05 MAIN_BOSS_NON_FINAL, C06–C10 INTERMEDIATE_BOSS, C11–C15 ELITE_VARIANT; ELITE_CHEST не расходует synergy cap и не становится boss chest.
- C3 content cadence является предложением для сверки с Architecture/Balance; он не изменяет их registry, event schema, numeric balance или runtime state.

## 3. Handoff для Balance Agent

Balance Agent должен привязать значения к одному источнику данных и не создавать вторую таблицу чисел поверх content docs.

### Weapons, passives, synergies

Нужно закрепить для каждого ID: base damage, cadence, cooldown, target/geometry limits, duration, radius, scaling tags, level/rank curve, damage category, boss/elite behavior, VFX-safe telegraph budget и evolution coefficients. В C1 намеренно оставлены `PENDING_BALANCE` поля.

Отдельный gate синергии: weapon level 10 + passive rank 10 + matching `synergy_id` + weapon не evolved + нефинальный `BOSS_CHEST`; числовые эффекты и стоимость прокачки остаются `PENDING_BALANCE`.

Отдельно подтвердить:

- цена opportunity cost пяти synergy claims и fallback outcome;
- deterministic priority, если в одной boss chest одновременно eligible несколько pairs;
- поведение upgrade offer после evolved weapon;
- exact max 5 enforcement и duplicate idempotency;
- баланс двух mini-bosses: telegraph, HP budget, cadence, фаз и состава support pack;
- balance future enemy batch: support tether, route shaping, lane sniper, predictive flanker и их safe-spawn/active-cap rules.

### Artifacts

Нужно закрепить для десяти IDs: rarity/source cadence, trigger cooldown, radius, duration, coefficient, target whitelist, boss/elite resistance, duplicate mode (`UNIQUE`/`STACKABLE`/`UPGRADE`), refresh price/limit и first-clear scope. Пока это `PENDING_BALANCE`/`PENDING_PRODUCT_DECISION`.

`artifact_tideglass` и `artifact_silent_lantern` нельзя считать runtime-ready до Registry/Architecture sync.

### Meta tree

Нужно решить, как 10 branch ranks распределяются между 17 node ranks, затем закрепить значения, caps, stacking order и floor. Обязательные semantic checks:

- `attack_power` и `attack_multiplier` — разные axes;
- `all_magic_damage` — только explicit `MAGIC` tags;
- `spell_size` меняет geometry вместе с telegraph, а `spell_duration` не продлевает telegraph без решения;
- `pickup_radius` не проходит через walls;
- healing mote отделена от XP/mana pickup;
- `enemy_max_hp` имеет явный sign/floor/whitelist;
- internal armor не становится дублирующим публичным node.

### Arena drops

Для семи IDs нужно закрепить:

- approved source tiers, drop-table weights, cadence/frequency и safe-spawn rules;
- quantity/value for Gold/healing and resource ownership for XP;
- pickup boundary, effect radius, duration, concurrent target cap и performance budget;
- destruction target whitelist, kill credit и reward/aftermath outcome;
- freeze target whitelist, ordinary spawn-pressure policy, active telegraph resume/cancel и resistance;
- ward mitigation/absorption model, lethal boundary, charge and duplicate/refresh policy;
- vacuum eligible set, line-of-sight/wall cost и collection cap;
- interaction с `meta_vitality_mote_healing`, `meta_magnet_pickup_radius`, `meta_magnet_mana_gain` и artifact triggers только после explicit semantic review.

В C4 нет numeric binding. Balance Agent должен оставить XP formula/grade vocabulary и current reward ledger authority в их канонических источниках.
## 4. Handoff для Architecture/Runtime

### Existing contracts to preserve

- stable semantic IDs и Content Registry data-driven resolution;
- `BuildInventory`: 6 weapon + 6 passive slots;
- `SynergyEvaluator`/`BossChestSystem`: weapon/passive gate, non-final boss chest, fallback;
- `ArtifactOfferSystem`: 3 cards, 1 selection, separate from build slots;
- `ArtifactEffectSystem`: run-scoped trigger/effect/cleanup;
- `StatsCalculator`: aggregate persistent meta node ranks with base stats and run modifiers;
- `MetaProgression`, `SaveSnapshot`, `RewardLedger`: authoritative purchase, save and reward boundaries.

### Events already named by architecture

Content consumes/provides projections around the existing `upgrade_applied.v1`, `synergy_eligibility_evaluated.v1`, `synergy_claimed.v1`, `artifact_offer_created.v1`, `artifact_offer_refresh_requested.v1`, `artifact_chosen.v1`, `artifact_obtained.v1` and `first_clear_artifact_offer_requested.v1`. New event names for meta purchases не объявляются canonical этим пакетом; Architecture должен закрепить их отдельно.

### Arena-drop sync decisions

- зарегистрировать семь drop IDs и общий transient instance lifecycle через Content Registry;
- закрепить drop instance/effect/cleanup schema, wall/safe-spawn policy и per-instance/per-target idempotency;
- определить owner systems для health, Gold, XP attraction/harvest, destruction, freeze и ward;
- назвать новые activation/resolve events отдельно; C4 не является event catalog;
- связать XP magnet/vacuum с существующим XP collection path без duplicate XP;
- связать coin cache с RewardLedger без silent wallet mutation;
- определить destruction defeated-vs-removed resolution, чтобы не терять и не дублировать XP/aftermath;
- сохранить boss/mini-boss immunity, checkpoint and final-boss no-chest boundary;
- определить reconnect/restore policy для uncollected transient drops.
### Required sync decisions

- добавить `artifact_tideglass` и `artifact_silent_lantern` в Registry только после schema/effect mapping review;
- добавить canonical `max_synergy_claims_per_run: 5` и authoritative run counter;
- синхронизировать пять mini-boss encounter proposals и два main-boss extension proposals; content map содержит десять BOSS_CHEST windows и пять ELITE_CHEST windows, но Architecture сохраняет за собой canonical schedule/source mapping;
- зарегистрировать четыре future enemy proposals только после отдельного stage decision; до этого держать их вне Run 1 registry и save restore.
- сохранить checkpoint source и final-boss prohibition;
- определить persistence scope first-clear artifact reward;
- определить trigger guards для echo/pulse/ward effects, включая replay/idempotency;
- определить meta tree schema: branch budget, node rank, dependency and purchase result;
- устранить stale clock-policy conflict в architecture source отдельно, не изменяя его этим content slice.

## 5. Handoff для Visual Lab

Этот пакет передаёт briefs, но не создаёт мокапы.

| Content family | Route | Stage path | Candidate/manifest status |
|---|---|---|---|
| weapon origin/combat identity | `SPRITE` + `VFX` | `docs/mockups/06-weapons/` | `candidate_id: null`, `PROPOSAL`, `NOT_PROMOTED` |
| passive identity/card | `SPRITE` + `UI_ART` | `docs/mockups/07-passives/` | `candidate_id: null`, `PROPOSAL`, `NOT_PROMOTED` |
| artifact identity/offer | `SPRITE` + `VFX` + `UI_ART` | `docs/mockups/08-artifacts/`, `docs/mockups/17-artifact-ui/` | `candidate_id: null`, `PROPOSAL`, `NOT_PROMOTED` |
| synergy explanation/evolution | `VFX` + `UI_ART` | `docs/mockups/19-synergy-info/` | `candidate_id: null`, `PROPOSAL`, `NOT_PROMOTED` |
| mini-boss encounter identity | `SPRITE` + `VFX` + `UI_ART` | `docs/mockups/05-bosses/` | `candidate_id: null`, `PROPOSAL`, `NOT_PROMOTED` |
| future enemy identity | `SPRITE` + `VFX` + `UI_ART` | `docs/mockups/04-enemies/` или отдельная будущая stage-папка после решения | `candidate_id: null`, `PROPOSAL`, `NOT_PROMOTED` |
| arena drops / pickup identity | `SPRITE` + `VFX` + `UI_ART` | `docs/mockups/02-arena/`, `docs/mockups/09-xp/` | `candidate_id: null`, `PROPOSAL`, `NOT_PROMOTED` |
| passive meta tree/shop | `UI_ART` | `docs/mockups/07-passives/`, `docs/mockups/16-upgrade-offers/` | `candidate_id: null`, `PROPOSAL`, `NOT_PROMOTED` |

Visual code: deep blue-grey, smoky teal, warm ivory, muted brass, soft jade; muted crimson/violet только для role/status accent. Identity должна читаться по silhouette, shape grammar и interaction, а не только цветом. Нужны проверки 390×844 UI scale, true 1× combat scale, telegraph visibility и no-asset-drift.

## 6. Product decisions still open

| Вопрос | Почему блокирует следующий этап |
|---|---|
| B1 flat six branches vs 17 visible stat nodes | нужно выбрать единую economic/progression модель |
| `mana` vs `XP` label/semantics | иначе `meta_magnet_mana_gain` будет неоднозначен в UI и data |
| healing mote source | влияет на vitality node, Lotus Seed и pickup contract |
| enemy max HP sign/floor/boss scope | влияет на баланс, UI и enemy initialization |
| artifact first-clear scope | Codex unlock или активный run effect |
| artifact refresh and duplicate policy | влияет на offer economy и save schema |
| elite pack cadence | определяет реальную частоту десяти artifact effects |
| simultaneous eligible synergies | нужен deterministic priority/offer rule |
| mini-boss schedule and chest source | нужно подтвердить 7:30/12:30/17:30/22:30/27:30, encounter kind и fallback outcome |
| arena-drop source cadence and target semantics | нужно определить risk/reward economy, Gold/XP label и target whitelist |
| future enemy stage insertion | нужно определить будущую wave/stage band, safe-spawn и не добавлять proposals в Run 1 молча |
| meta purchase event and reset/refund | нужен authoritative persistence boundary |
| boss clock conflict | architecture source contains stale key; must be resolved by owner |

## 7. Acceptance checks for this content slice

- [x] C0 audit выполнен по live main и protected scope.
- [x] Сохранены все существующие weapon/passive/synergy IDs.
- [x] Roster содержит ровно 10 оружий, 10 run-пассивок, 10 synergy/evolutions и 10 artifacts.
- [x] Все run-passives описаны как общие эффекты; weapon связи оставлены только как synergy anchors.
- [x] Synergy rule «не более 5 за забег», обязательный максимум weapon level 10 + passive rank 10 для пары, пять mini-boss encounters и десять content BOSS_CHEST windows явно повторены в C1, C3 и index.
- [x] Каждый mini-boss имеет distinct skill-check, telegraph contract и fallback path.
- [x] Четыре future enemy proposals имеют silhouette, role/signature, telegraph, arena interaction, counter-decision, spawn behavior, hooks, reward boundary и balance questions.
- [x] Полное дерево содержит 6 ветвей и 17 stat nodes из stat-screen reference.
- [x] Все числовые значения, которые ещё не принадлежат content ownership, помечены `PENDING_BALANCE`/`PENDING_PRODUCT_DECISION`.
- [x] Briefs для Visual Lab есть; mockups, PNG/SVG и candidate IDs не создавались.
- [x] C4 catalog содержит семь arena drops с signal/pickup/intent/feedback/limitations и PENDING_BALANCE fields.
- [x] Arena drops отделены от XP/aftermath, boss chest, artifact offer и final reward settlement.
- [ ] Balance Agent должен выполнить numeric binding.
- [ ] Architecture/Runtime должны синхронизировать Registry/schema/events.
- [ ] Visual Lab должен отдельно принять briefs и создать свои mockups по master gates.

Локальная проверка JSON, ID uniqueness, required fields и remote path scope выполняется перед commit; production/playable/APPROVED статус этому пакету не присваивается.

## 8. Historical C4 handoff order

1. Balance Agent: reconcile six B1 branch budgets with 17-node topology and bind numbers.
2. Architecture/Runtime: sync two artifact proposals, ten semantic artifact effect keys, five mini-boss proposals, two main-boss extension proposals, synergy cap, chest source, artifact effect schema and meta purchase boundary.
3. Visual Lab: create master tree/shop and artifact/synergy/weapon visual briefs/mockups in its protected stages.
4. QA/Integration: validate offer counts, five-synergy cap, stats aggregation and persistence after the preceding decisions are locked.

## 9. C4 short handoff

- Status: CONTENT_SPECIFIED; seven new IDs remain PROPOSAL / REGISTRY_SYNC_PENDING.
- Balance owns source cadence, quantities, values, radii, durations, target caps, mitigation and performance budgets.
- Architecture/Runtime owns instance/effect schema, new event names, idempotency, reward ownership, wall policy and reconnect behavior.
- Visual Lab receives briefs only; no mockups or candidate IDs were created.
- C5 is now documented in `C5_CROSS_SYSTEM_HANDOFF.md`; its open reconciliation items are explicit and are not hidden as content decisions.


## 10. C5 cross-system reconciliation

C5 сверяет каталог с live Architecture, Runtime и Balance contracts на baseline `6d7c2a361944ada398622e77c2436a79a47baf46`. Полная dependency matrix, P1/P2 findings, Balance/Runtime/Visual Lab handoff и acceptance evidence находятся в `C5_CROSS_SYSTEM_HANDOFF.md`.

Ключевые открытые reconciliation items:

- Architecture: единая clock policy для MAIN_BOSS freeze и MINI_BOSS continuation;
- Product/Content: C3 content roster = 5 mini-bosses, data contract = 3, runtime acceptance = 5, live B1 Registry = 0; content identities are supplied, registry sync remains external;
- Architecture: синхронизация 2 недостающих артефактов и typed effect definitions;
- Product/Balance: 20-minute legacy vs 30-minute architecture envelope; `BALANCE_MODEL.json` содержит только proposed/model-only extension;
- Product/Architecture: content map C01–C15 разделяет десять boss chest windows, пять elite chest windows и synergy claims от artifact offers;
- Product/Architecture: content gate weapon level 10 + passive rank 10 не совпадает с legacy architecture cap 6/5 и требует отдельной синхронизации;
- Runtime: typed arena-drop instance/events поверх существующих XP/aftermath records;
- Visual Lab: briefs переданы, mockups и production assets C5 не создаёт.

C5 package status: `HANDOFF_READY_WITH_OPEN_RECONCILIATIONS`; до закрытия P1 findings нельзя ставить `APPROVED`, `IMPLEMENTED`, `VERIFIED`, `PLAYABLE` или `PRODUCTION`.
