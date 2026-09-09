
# FIRST_RUN_ARCHITECTURE — логическая архитектура

Статус: **SPECIFIED_WITH_PENDING_DECISIONS**
Назначение: контракт для следующего runtime-агента.
Запрещённая интерпретация: этот документ не означает, что M1, APK или production runtime уже реализованы.

## 1. Архитектурное решение

Выбран лёгкий domain-first runtime вокруг одной authoritative RunSession:

- AppFlowCoordinator оркестрирует маршруты и команды между menu и run;
- RunSession владеет изменяемым состоянием одного забега;
- domain services меняют только принадлежащие им части RunState через явные команды;
- RunReadModel является производной проекцией для HUD/pause/result;
- ContentRegistry владеет data-driven definitions;
- RewardLedger владеет внешним side effect наград и idempotency;
- SaveRepository владеет versioned snapshots, но не заменяет in-memory source of truth;
- Diagnostics сохраняет причины отказов и recovery path.

Архитектура намеренно не вводит общий GodController, event bus «на всякий случай» или интерфейсы без реального boundary pressure.

## 2. Границы и направление зависимостей

~~~mermaid
flowchart TD
    UI["Menu / HUD / Pause / Result"] --> FLOW["AppFlowCoordinator"]
    FLOW --> FACADE["RunFacade + commands"]
    FACADE --> SESSION["RunSession / RunState"]
    SESSION --> DOMAIN["Simulation · Progression · Chest"]
    DOMAIN --> READ["RunReadModel"]
    DOMAIN --> LEDGER["RewardLedger"]
    DOMAIN --> SAVE["SaveRepository"]
    CONTENT["ContentRegistry"] --> DOMAIN
    DIAG["Diagnostics"] --> FLOW
    SAVE --> DIAG
~~~

Правило зависимостей:

- UI зависит только от read models и command interfaces;
- coordinator зависит от domain façades и adapters, но не реализует combat;
- domain services зависят от stable content contracts, не от Node2D/Control;
- ledger/save adapters не вызываются напрямую экраном;
- persistence и diagnostics не импортируют UI;
- visual assets и mockups не являются dependency для логического контракта.

## 3. Source of truth

| Данные | Source of truth | Кто изменяет | Кто читает | Почему |
|---|---|---|---|---|
| Hero/weapon/passive/boss/wave definitions | ContentRegistry | content pipeline | services, UI projections | data-driven и versioned |
| Текущее время/phase/checkpoint | RunSession.RunState | RunClock/WaveDirector | all run domains, HUD | один authoritative clock |
| HP/combat counters/drops | RunSession.RunState | CombatResolver/DropService | read model, result | атомарное domain update |
| Weapon/passive/artifact build | BuildState внутри RunSession | BuildInventory/ProgressionService/ChestResolver | HUD, synergy evaluator | slot/max/evolution rules вне UI |
| Eligible/claimed synergy | SynergyState внутри BuildState | SynergyEvaluator/ChestResolver | chest/HUD/result | защита от повторной выдачи |
| Checkpoint/meta rewards | RewardLedger | RewardService/Ledger adapter | result/profile | durable idempotent side effect |
| Save bytes/revision/checksum | SaveRepository | snapshot writer/migrator | restore flow/diagnostics | безопасное восстановление |
| HUD/pause/result fields | RunReadModel / ResultSnapshot | projection builder | UI only | UI не пересчитывает domain |
| Errors/fallbacks | Diagnostics | adapters/services | UI, logs, acceptance | failure observable |

## 4. Module boundaries

| Module | Ownership | Input | Output | Не делает |
|---|---|---|---|---|
| BootLoader | process init и registry loading | app start, schema version | boot result/diagnostic | не стартует run сам |
| AppFlowCoordinator | screen route, request lifecycle | UI commands, domain events | screen state, command result | не считает damage/rewards |
| ContentRegistry | immutable definitions и IDs | versioned content data | resolved records | не хранит mutable run state |
| RunFacade | public boundary run operations | Start/Pause/Resume/Choice/Exit | accepted/rejected command + events | не прячет ownership |
| RunSession | lifecycle одного run | validated commands | RunState revisions | не рисует и не пишет raw file |
| RunClock | game time and freeze | tick/pause/resume | elapsed_seconds, clock events | не делает OS time authoritative |
| WaveDirector | band selection, spawn budget, boss gates | elapsed time, active counts | wave/boss commands | не резолвит attack damage |
| CombatResolver | damage, enemy death, telegraph guard | simulation entities, content | combat events/counters | не выдаёт meta currency |
| DropService | XP item and aftermath creation | enemy defeat, cap | typed drops | не смешивает XP и aftermath |
| ProgressionService | XP threshold, offers, upgrades | XP/build/content | offer set, build mutations | не открывает screen |
| BuildInventory | slots, levels, artifact collection | validated upgrade/claim | BuildState revision | не выбирает random offers |
| SynergyEvaluator | pair eligibility | build/content/chest context | eligible/fallback projection | не claim-ит reward |
| ChestResolver | offer lifecycle and outcome | boss defeat, eligibility | chest offer/claim event | не начисляет checkpoint currency |
| RewardCalculator | deterministic reward formula | outcome/checkpoint/profile flags | reward plan | не persists directly |
| RewardLedger | idempotent reward side effects | reward plan + key | entry/receipt | не меняет combat state |
| RunReadModelBuilder | UI projections | RunState/events/diagnostics | HUD/pause/chest/result model | не принимает commands |
| ResultAssembler | immutable terminal snapshot | RunState/ledger | ResultSnapshot | не re-runs simulation |
| SaveRepository | snapshot write/read/migrate/validate | serializable state | validated snapshot/recovery result | не решает product policy |
| Diagnostics | error code/path/version/recovery | failures | diagnostic record | не скрывает broken contract |

## 5. Menu/run bridge

### 5.1 Commands from menu

Каждая команда имеет command_id, profile_id, content_version и deterministic timestamp source:

- OpenCharacters;
- SelectHero(hero_id);
- ConfigureArtifacts(artifact_ids);
- StartRun(hero_id, artifact_ids, seed_policy);
- RequestRecovery(snapshot_id);
- OpenSettings(return_owner);
- ConfirmAbandon(run_id);
- ReturnToMenu(result_id).

Coordinator проверяет routing/permission, затем передаёт domain command. UI не получает доступ к mutable RunState.

### 5.2 Accepted result

StartRunAccepted содержит run_id, seed, selected hero, content_version и initial revision. После arena validation публикуется run.started. До этого menu может показывать loading/error, но не active HUD.

### 5.3 Return contract

Result screen возвращает ResultSnapshot и ledger receipt summary. ReturnToMenu закрывает presentation, но profile/meta writes считаются завершёнными только после ledger receipt. Если ledger adapter недоступен, экран показывает retry/recovery, а не сообщает «награды получены».

## 6. ContentRegistry и stable IDs

Content data отделены от runtime logic. Registry records имеют:

- stable ID, canonical display name и content schema version;
- source status: CANONICAL или PENDING_*;
- allowed references;
- numeric values только из подтверждённого B1 или с pending token;
- deterministic ordering для offer/chest candidates;
- compatibility/migration policy.

Канонический roster первого среза:

- heroes: lin_yue, soyeon_han;
- weapons/passives: 10 прямых пар из GAME_MANIFEST;
- bosses: hua_lin, miyon, seika, black_moon_empress;
- wave bands: 0–2, 2–5, 5–10, 10–15, 15–20 minutes;
- artifacts: максимум 3 одновременно, exact runtime effect values are content data.

Stable slug IDs в JSON-контракте являются предложенной registry naming convention. Пока runtime registry не создан, они не являются доказательством импортированных assets.

## 7. RunSession и simulation

RunSession содержит serializable RunState:

- run_id, seed, schema/content version;
- phase, elapsed_seconds, current wave band, checkpoint;
- selected hero and artifacts;
- BuildState;
- combat stats and health;
- XP/level/kills;
- typed drop collections;
- bonus_state extension point;
- pending offers/chest;
- reward ledger references;
- diagnostics summary;
- revision.

### 7.1 Clock

RunClock — единственный источник elapsed game time:

- tick только в active simulation phase;
- pause/upgrade/background выставляют frozen=true до UI transition;
- OS wall clock не двигает run;
- resume продолжает с revision, а не пересчитывает время по wall-clock;
- final victory/death фиксирует terminal_time.

### 7.2 WaveDirector

WaveDirector получает elapsed_seconds и возвращает immutable WaveBandConfig:

| Band | Budget | Cap | HP modifier | Damage modifier | Speed modifier |
|---|---:|---:|---:|---:|---:|
| wave_0_2m | 6/s | 40 | ×1.00 | ×0.70 | ×0.90 |
| wave_2_5m | 10/s | 80 | ×1.10 | ×0.85 | ×1.00 |
| wave_5_10m | 15/s | 130 | ×1.35 | ×1.00 | ×1.02 |
| wave_10_15m | 22/s | 200 | ×1.70 | ×1.25 | ×1.05 |
| wave_15_20m | 30/s | 280 | ×2.20 | ×1.55 | ×1.08 |

Spawn budget — среднее число новых сущностей в секунду; active cap — safety ceiling, а не цель постоянно держать заполненной. На boss spawn ordinary budget уменьшается на 8 seconds, затем линейно возвращается 70% → 100% за 20 seconds.

Absolute enemy base HP/damage/speed не заданы B1 и должны оставаться PENDING_B1 в registry.

## 8. Combat, drops и performance boundary

CombatResolver:

- применяет damage и contact cooldown;
- требует telegraph до опасной зоны;
- подтверждает enemy death ровно один раз;
- обновляет kills;
- передаёт DropService enemy_id и drop policy;
- не создаёт persistent meta reward.

DropService создаёт два разных типа:

1. XPItem: value, source enemy, collectible=true, collision policy, merge key.
2. AftermathItem: visual_id, source enemy, collectible=false, collision=false, xp_value=0, decay/cluster policy.

Они не должны иметь общий polymorphic «drop» с неявным поведением. Если общее envelope нужно для транспорта, type discriminator обязателен и domain handlers разделены.

Object pooling применяется к enemies, projectiles, XP items, telegraphs и aftermath clusters. Target budgets из balance docs (например, до 400 low-detail aftermath и до 80 clusters/decals) являются performance baseline, а не разрешением нарушать читаемость.

## 9. Progression, build и evolution

### 9.1 Slots and levels

- максимум 6 weapons;
- максимум 6 passives;
- максимум 3 artifacts;
- weapon level range 1–6;
- passive level range 1–5.

Slot legality принадлежит BuildInventory. UI может показывать disabled offer, но не решает slot count.

### 9.2 Offers

ProgressionService строит OfferSet из трёх canonical candidates, если соответствующий rule подтверждён. Offer содержит offer_id, generation seed, content version, kind, target ID, current level, next level, legality и reason.

Выбор применяется один раз через offer idempotency key. При stale offer возвращается rejection с regenerate path.

### 9.3 Synergy

SynergyEvaluator — чистая проверка:

- weapon/passive pair;
- max levels;
- not claimed;
- chest context;
- content version.

ChestResolver применяет подтверждённую synergy. Если pair не eligible, формируется explicit fallback outcome с pending marker. Ни UI, ни random fallback не могут молча изменить build.

## 10. Chest и reward ledger

### 10.1 Разделение ответственности

- boss defeat создаёт checkpoint reward plan и chest offer;
- ChestResolver определяет offer/eligibility/fallback;
- RewardCalculator считает B1 currency plan;
- RewardLedger делает durable idempotent grant;
- ResultAssembler только читает ledger receipt.

### 10.2 Ledger key policy

- checkpoint:run_id:checkpoint_id;
- chest:run_id:chest_id;
- synergy:run_id:synergy_id;
- result:run_id:defeat;
- result:run_id:victory;
- result:run_id:first_clear.

Операция должна быть atomic для одного key: first write получает status GRANTED/PENDING, повторная доставка возвращает исходную entry. Несовместимый payload с существующим key — diagnostic conflict, а не новая запись.

### 10.3 B1 rewards

| Event | Gold | Lunar Seals | Boss Essence |
|---|---:|---:|---:|
| boss 1 / 5m | 50 | 15 | 1 |
| boss 2 / 10m | 75 | 20 | 1 |
| boss 3 / 15m | 100 | 25 | 1 |
| final boss / 20m | 200 | 60 | 2 |
| first full clear bonus | 300 | 180 | 1 |

Defeat after checkpoint: 50% checkpoint gold, earned Essence, seals only for defeated bosses. Exact rounding of half gold remains pending. No normal enemy gold is introduced.

## 11. Persistence, checkpoint и recovery

SaveRepository stores versioned SaveSnapshot, not arbitrary Node tree:

- schema_version and content_version;
- revision;
- save reason;
- serialized RunSession;
- ledger references/entries necessary for replay;
- checksum/integrity marker;
- created_at from persistence metadata;
- migration path.

Write triggers:

- before/after validated checkpoint reward;
- terminal result before claim;
- Android background;
- explicit recovery boundary, if product policy enables it.

Exact incomplete-run save timing is U-06. Until product decision, architecture supports a seam and safe validated checkpoint recovery, but does not promise continuous mid-run save.

Restore algorithm:

1. read bytes;
2. validate checksum and schema;
3. migrate only known versions;
4. resolve content IDs;
5. verify ledger key/payload consistency;
6. rebuild RunReadModel;
7. enter recovery prompt or error if any step fails.

Never grant reward during validation alone. Reward claim requires the ledger operation.

## 12. HUD, pause и result read models

RunReadModel is rebuilt from RunState and domain events. Minimum fields:

- hero HP/max HP and alive/terminal;
- attack, critical chance, critical multiplier, movement speed, cooldown and active passives;
- weapon/passive/artifact records with levels;
- eligible/claimed synergies;
- level, current XP, next XP threshold;
- elapsed time, wave band, stage/checkpoint;
- kills and bonus_state projection;
- current pending offer/chest;
- earned/claimed reward summary;
- diagnostics and recoverability.

ResultSnapshot freezes relevant fields and adds outcome, terminal reason, stats summary, checkpoint history and ledger receipts. UI never recomputes amounts, timers, eligibility or XP.

## 13. Diagnostics and fallback

Every recoverable failure has:

- stable reason_code;
- operation and command/event ID;
- affected stable ID/path;
- content/save version;
- current state/revision;
- user-facing recovery action;
- safe fallback marker.

Required cases:

- missing content → disable affected card/offer, block unsafe run, show retry;
- stale content → migrate or block with version mismatch;
- invalid snapshot → retain no untrusted state, offer validated older snapshot or fresh menu;
- ledger conflict → show receipt/conflict, never double grant;
- missing chest fallback definition → keep CHEST_PENDING and mark PENDING_PRODUCT_DECISION;
- renderer/asset issue → neutral placeholder only, no hidden production asset dependency.

## 14. Android and performance

Android pause/resume is part of lifecycle, not a UI afterthought:

- freeze simulation before platform callback returns;
- snapshot asynchronously without changing authoritative state;
- resume only validated revision;
- keep controls and HUD read models lightweight;
- pool high-churn entities;
- cap active enemies and drops;
- degrade aftermath to clusters before deleting its semantic evidence;
- test 60 FPS target and 30 FPS safety target on a real device.

Current repository has CI Godot image barichello/godot-ci:4.7.2, but this architecture document does not pin a runtime build or claim Android verification.

## 15. Iteration layering

### Slice 0 — contract harness

Stub content, RunSession serializer, state transitions, diagnostics, fake clock, deterministic ledger. No assets.

### Slice 1 — playable core

Neutral hero marker, movement, one enemy stub, one XP type, one level-up offer, HUD read model, pause/resume. Prove XP/aftermath separation with test doubles.

### Slice 2 — wave/checkpoint

Data-driven five wave bands, one boss stub at 5 minutes, telegraph placeholder, checkpoint ledger, chest fallback placeholder.

### Slice 3 — build loop

Six/six slot enforcement, weapon/passive max levels, three-offer flow, synergy evaluator, one deterministic evolution, artifact stub.

### Slice 4 — full first run

All four bosses, full roster, result/death branches, recovery policy, result claim, Android background/resume and performance evidence.

### Slice 5 — approved content integration

Replace stubs only with separately approved assets/manifests. This architecture task does not perform that work.

## 16. Tradeoffs and non-goals

Tradeoffs:

- RunSession + explicit services is more code than one controller, but ownership and replay/idempotency are testable.
- Read model adds projection work, but prevents HUD from becoming a second rules engine.
- Ledger persistence adds schema/recovery work, but protects checkpoint rewards from duplicate delivery.
- Logical stage inside one arena is simpler for M1; separate scene loading remains a seam if product later requires it.
- Safe fallback can pause progress on missing content; this is preferable to silently changing rewards/build.

Non-goals:

- no combat balance beyond sourced B1 values;
- no absolute enemy base stats until B1;
- no new hero/weapon/artifact content;
- no networking, accounts, multiplayer, ads, shop or gacha;
- no visual asset import or approval;
- no runtime code, scenes, project settings or export changes;
- no claim that current prototype is production-ready.

## 17. Current prototype seam

The current menu controller proves navigation placeholders and uses archived v01 references; the arena controller proves only a visual preview with accelerated time and ambient reactions. The first runtime slice should wrap or replace these controllers behind AppFlowCoordinator/RunFacade, not let them become owners of RunState.

