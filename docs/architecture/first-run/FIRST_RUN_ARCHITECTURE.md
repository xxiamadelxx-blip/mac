# FIRST_RUN_ARCHITECTURE — логические границы и data flow

Статус: DRAFT ARCHITECTURE SPECIFICATION
Runtime implemented: NO
Цель: контракт для следующего runtime-агента, а не список классов и не доказательство APK.

## 1. Цель и ограничения

Архитектура должна провести один offline-first 20-минутный Android-забег от меню до result screen, не смешивая UI, симуляцию, content data, persistence и reward mutation.

Защищённый scope этого задания:

- основной scope — docs/architecture/first-run/; явно синхронизируются только документы, затронутые утверждённым artifact-offer product decision;
- scripts, scenes, project.godot, B1, visual assets и runtime manifests не изменяются;
- точные числа берутся из [BALANCE_ECONOMY_SPEC.md](../../../docs/BALANCE_ECONOMY_SPEC.md);
- текущие menu/arena scripts — evidence прототипа, не готовый runtime.

## 2. Source of truth

| Данные | Source of truth | Кто читает | Кто меняет |
|---|---|---|---|
| Run state | RunSession aggregate | Simulation, progression, projections, persistence adapter | RunCoordinator через domain owners |
| Content definitions | Versioned Content Registry | All runtime systems | Data/content pipeline, не UI |
| Wave numbers | B1 source document → imported wave records | WaveDirector | Только владелец B1/content import |
| Derived combat stats | Stats calculator from base/profile/build | Combat, HUD projection | Build/progression commands |
| Build inventory | BuildInventory inside RunSession | Progression, synergy, HUD | Upgrade/evolution commands |
| XP drops | XpDropStore inside RunSession/world subsystem | Magnet/Progression/HUD | Spawn/collect commands |
| Aftermath | AftermathStore, separate from XP | Rendering/performance diagnostics | Death/aggregation subsystem |
| UI state | Versioned read models | Menu/HUD/result/settings | Projection builders |
| Local persistence | Versioned SaveSnapshot | AppShell/Recovery/PersistenceGateway | Atomic snapshot writer |
| Wallet/unlocks | MetaProgression inside SaveSnapshot | Menu/result/registry | RewardLedger transaction only |
| Rewards | RewardLedger | Result/analytics/recovery | Reward service at one persistence boundary |
| Errors | DiagnosticReporter + diagnostic entries | UI and logs | Owning subsystem on failure |

The event catalog is not a second source of truth. Events carry decisions and effects; current authoritative state lives in RunSession, SaveSnapshot and RewardLedger.

## 3. Module boundaries

~~~mermaid
flowchart TD
    AppShell --> MenuFlow
    MenuFlow --> RunCoordinator
    RunCoordinator --> RunSession
    RunCoordinator --> Simulation
    Simulation --> Projections
    RunSession --> Persistence
    RunCoordinator --> RewardBoundary
    RewardBoundary --> SaveSnapshot
    ContentRegistry --> Simulation
    ContentRegistry --> MenuFlow
~~~

### AppShell and ContentLoader

Responsibilities:

- initialize Godot process boundary;
- load versioned content and migration rules;
- load or create local SaveSnapshot;
- expose MAIN_MENU, SETTINGS and CONTENT_ERROR;
- install Android pause/resume hooks.

Must not own damage, waves, XP, build mutation or wallet arithmetic.

### MenuFlow and RunSetupModel

Responsibilities:

- render main menu, ПЕРСОНАЖИ, settings and run setup;
- validate character_id/unlock state; do not accept pre-run artifact selection or artifact loadout;
- send commands to RunCoordinator;
- derive menu read models from SaveSnapshot and Content Registry.

Must not create rewards, set HP, advance clock or change RunSession directly.

The existing scripts/menu/menu_controller.gd is a navigation prototype. Its screen transitions and preview buttons are migration evidence only; it currently jumps to the arena scene without a real RunSession.

### RunCoordinator

Responsibilities:

- accept intent-level commands;
- route them to the owning domain subsystem;
- enforce legal state transitions from FIRST_RUN_STATE_MACHINE;
- correlate run_id, state_revision and event sequence;
- request persistence at defined boundaries;
- publish projection refresh requests.

RunCoordinator is orchestration only. It does not calculate damage, choose reward amounts, render UI, or become a god controller.

### RunSession aggregate

Responsibilities:

- hold authoritative live state for one run;
- expose validated commands for clock, movement/combat result, XP collection, upgrade choice, boss/checkpoint and pause;
- own state_revision and transition guards;
- contain selected hero, stage/checkpoint, build, active artifact instances/effects, stats, counters, drops, pending upgrade/boss-chest/artifact offers and diagnostics references.

RunSession does not reference Godot UI nodes, textures, scene paths or network services. It may contain stable IDs and plain serializable data.

### Simulation layer

#### SimulationClock

- consumes delta only while RUN_ACTIVE or BOSS_ACTIVE;
- derives elapsed_seconds;
- emits boundary candidate, never settles reward itself;
- freezes on pause, upgrade offer, boss-chest offer, artifact offer and terminal states;
- uses a monotonic run clock, not wall-clock time, for gameplay.

#### WaveDirector

- reads elapsed_seconds and B1 wave records;
- selects current wave_band_id;
- produces spawn budget, active cap, roster and boss interruption commands;
- enforces no silent per-second HP growth;
- resumes post-boss spawn from imported B1 rule;
- delegates actual entity creation to controlled spawner/pool.

#### CombatSystem

- resolves movement contacts, attacks, projectiles, status and death;
- reads content and derived stats;
- applies contact cooldown and telegraph prerequisites from B1;
- emits combat facts; it does not directly edit wallet or UI.

#### ProgressionSystem

- consumes XP collection facts;
- computes level boundary using B1 formula;
- freezes simulation and asks OfferGenerator for three offers;
- applies validated offer through BuildInventory;
- emits level/upgrade events and updates read model.

#### ControlledSpawner and pools

- enforce active cap and object lifecycle;
- separate enemy/projectile/XP/VFX/aftermath pools;
- expose diagnostics when a pool is exhausted;
- never silently delete XP; merge XP items by defined value policy.

## 4. Content and build modules

### Content Registry

Records are data-driven and versioned. At minimum:

- characters: two M1 characters and their starting properties;
- weapons, passives and ten direct synergy pairs from GAME_MANIFEST;
- ten enemy records and four boss records;
- five B1 wave bands;
- artifact definitions and typed artifact-effect contracts, XP grades and reward bundles;
- telegraph metadata, fallback references and schema version.

Registry load validates IDs, references, numeric source refs and required consumers before a run starts. Missing optional decorative content can use a diagnostic fallback; missing gameplay content blocks run creation.

### BuildInventory

Owns:

- six weapon slots and six passive slots;
- weapon level and passive rank;
- evolved flags and claimed synergy IDs;
- BuildInventory owns no artifact capacity; active artifact effects are owned by ArtifactEffectSystem;
- legal New/Upgrade outcomes.

Limits come from GAME_MANIFEST/B1-derived data, not UI. Full slots remove illegal New offers from the pool. If no legal offer exists, the offer contract returns fallback_required; fallback value is pending product decision.

### SynergyEvaluator

Input:

- weapon_id and passive_id;
- max levels/ranks;
- matching synergy_id;
- evolved flag;
- chest context;
- claimed_synergy set.

Output is one of eligible, not_eligible, already_claimed, unavailable_context or fallback_required. It never invents a pair. The ten current direct pairs come from GAME_MANIFEST; exact future cross-synergy schema remains extensible.

### Boss chest subsystem

BossChestSystem owns offer lifecycle for non-final boss checkpoints, not reward wallet mutation. It creates a stable `chest_offer_id` linked to a non-final boss encounter/checkpoint and run seed. SynergyEvaluator determines synergy/evolution eligibility and fallback only in this boss-chest context. The final boss checkpoint never creates a boss chest; after final settlement it transitions to victory. RewardLedger settles only the explicitly defined checkpoint/meta bundle.

### Artifact offer and effect subsystem

ArtifactOfferSystem is separate from BossChestSystem and BuildInventory. It accepts two sources: `ELITE_PACK` between bosses when the pending cadence/composition policy allows it, and `FIRST_CLEAR_REWARD` after result finalization. Each source creates an `artifact_offer_id` with exactly three candidate cards. There is no pre-run artifact loadout and no fixed active-artifact capacity (`UNBOUNDED_WITHIN_RUN`); the chosen artifact does not consume a weapon/passive slot. `Get` selects one card and creates one `artifact_instance_id` owned by the current run. `Refresh` is a separate idempotent command whose cost, limit and reroll policy remain pending.

ArtifactEffectSystem evaluates typed effects such as AURA, DERIVED_STAT, TARGET_MODIFIER, WEAPON_MODIFIER, TRIGGERED_EFFECT and COOLDOWN_MODIFIER. It owns trigger/target/parameter/stacking evaluation and exposes active effects to Stats/HUD. Artifact effects are not flattened into ordinary passive modifiers without preserving their effect contract. The first-clear artifact offer is a separate post-result reward boundary, never the final boss chest.

## 5. Reward boundary and idempotency

RewardCalculator maps a terminal/checkpoint reason to a deterministic reward bundle from B1.

RewardLedger transaction:

1. validate run_id, state_revision, checkpoint/result scope and content version;
2. build idempotency key;
3. if key already committed, return stored outcome without wallet mutation;
4. otherwise append immutable ledger entry;
5. update the appropriate wallet/unlock projection;
6. persist both entry and wallet revision atomically;
7. emit reward_committed;
8. make result read model available.

Recommended key shape:

run_id : reward_scope : checkpoint_id : reward_type

Examples are shape examples, not additional business rules. First-clear/repeat-clear and defeat-after-checkpoint remain separate scopes. 50% Gold defeat rounding is PENDING_B1 because B1 does not specify a rounding rule for odd values.

No ordinary enemy gold drop is implemented by this architecture; enemies primarily yield XP. Currency separation is enforced at the reward boundary.

## 6. Persistence and recovery

### SaveSnapshot

SaveSnapshot is a versioned document containing:

- schema_version and content_version;
- revision, checksum and saved_at;
- meta progression and wallet balances;
- active RunSession if policy permits;
- pending upgrade/boss-chest/artifact offers and active artifact instances;
- reward ledger cursor/entries needed for replay protection;
- migration and diagnostic metadata.

Writes use an atomic persistence boundary: validate → serialize → write temporary revision → verify checksum → promote current revision. A failed write never marks a reward committed.

Working default:

- checkpoint, explicit pause and terminal/reward boundaries are safe snapshot points;
- no promise of arbitrary-frame save;
- Android background forces pause and attempts a safe snapshot;
- background kill offers the last coherent revision, or an abandon path if no valid revision exists;
- restore validates schema, checksum, content version and idempotency state before RUN_ACTIVE.

This default is a safety policy, not a confirmed product decision. It remains pending until user/product owner confirms the exact resume promise.

### Migration and stale content

- newer snapshot schema → diagnostic, no destructive downgrade;
- older schema with migration → migrate into a new revision before resume;
- content version mismatch → compatibility map or RECOVERY_REVIEW; never silently reinterpret IDs;
- unknown ID in a nonessential collection → quarantine record and show diagnostic;
- unknown ID in selected character, active weapon, wave, boss or reward entry → block run resume and request recovery.

## 7. Drops, aftermath and diagnostics

### XPDrop

XPDrop has its own id, grade, value, source enemy, world position, collected state and pool state. Magnet rules are checked by Progression/Magnet subsystem and XP is credited once.

### AftermathItem

AftermathItem has its own id, enemy_id, aftermath kind, visual family reference, world position, aggregation tier, collision=false and xp_reference=null. It never contributes XP and does not block pathfinding.

At B1 scale, aftermath aggregation may collapse old items into low-detail clusters/decals; this is a rendering/performance concern, not a combat state change.

### Diagnostics and fallback

Every fallback has:

- stable diagnostic_code;
- source path/id;
- severity;
- user-safe message;
- developer detail;
- recovery action;
- whether run start is blocked.

A missing decorative asset can use a marked fallback. Missing authoritative gameplay data blocks the dependent action. No resource error is rendered as a blank screen.

## 8. UI projection contracts

Projection builders consume immutable snapshots and expose plain data:

- MenuProjection: characters, unlocks, wallets, available sections and diagnostic badges.
- CharacterProjection: selected character, role, start weapon, active ability and locked/unlocked state.
- HudProjection: HP, attack, critical chance/multiplier, speed, cooldown, build, active artifact effects, XP, level, kills, time, stage, boss, rewards and diagnostics.
- PauseProjection: resume state, snapshot revision, settings availability, exit policy.
- ChestProjection: boss-chest offer_id, eligibility, exact available synergy/evolution/fallback outcomes, claim state; emitted only for non-final checkpoints.
- ArtifactOfferProjection: artifact_offer_id, source, exactly three candidate cards, effect previews, selected/refresh state and pending policy; emitted for elite-pack or first-clear sources.
- ResultProjection: terminal reason, stats, build, checkpoints, committed/pending rewards, wallet revision and unlocks.

A projection is disposable. UI re-requests it after every authoritative state revision and never serializes node references.

## 9. Data and event flow

1. User intent enters MenuFlow or PauseFlow.
2. RunCoordinator validates command against RunSession and Content Registry.
3. Domain owner mutates RunSession or starts RewardBoundary transaction.
4. Domain event is emitted with run_id, revision and idempotency key where required.
5. Projection builder derives UI state from the new authoritative snapshot.
6. PersistenceGateway snapshots at approved boundary.
7. Diagnostics are attached to projection without replacing authoritative errors with silent defaults.

Event names and payload requirements are in [FIRST_RUN_EVENT_CATALOG.md](./FIRST_RUN_EVENT_CATALOG.md). The machine-readable shape is in [FIRST_RUN_DATA_CONTRACT.json](./FIRST_RUN_DATA_CONTRACT.json).

## 10. Vertical delivery slices

### Iteration 1 — one safe end-to-end combat path

Outcome: a selected character starts a new session, moves/attacks one enemy, receives one XP drop, levels once, pauses/resumes and reaches a test defeat/result path with a valid snapshot.

Include:

- Content Registry schema for one character/weapon/enemy;
- RunSession, RunCoordinator and SimulationClock;
- one controlled enemy/projectile path;
- XPDrop separate from aftermath;
- one offer and BuildInventory mutation;
- pause, diagnostic fallback and local snapshot;
- deterministic tests for state transitions and idempotency shape.

Defer: full roster, bosses, all UI art, final balancing and Android performance proof.

### Iteration 2 — complete M1 rules and failure paths

Outcome: all B1 wave bands, ten enemies, four bosses, six-weapon/six-passive build, XP curve, upgrade offers, separate non-final boss-chest eligible/fallback path, elite-pack/first-clear artifact-offer path, checkpoint ledger, death/victory results and recovery run through one contract.

Include:

- WaveDirector and BossDirector;
- full content registry references;
- RewardLedger and atomic meta save;
- three-profile simulation logs;
- repeated event/restart tests.

Defer: production visual promotion, final audio and polish.

### Iteration 3 — Android hardening and scale evidence

Outcome: target Android APK completes the full 0→20-minute scenario with no critical failure and recorded performance/evidence.

Include:

- controlled pools and aftermath aggregation;
- Android pause/resume and background-kill checks;
- 0/5/10/15/20 evidence;
- real HUD, approved runtime assets and audio only after their own gates;
- performance at full active cap.

## 11. Tradeoffs

- Aggregate RunSession is simpler to serialize and test than distributing authority across scene nodes; scene composition becomes an adapter concern.
- A coordinator plus domain owners avoids one god controller, at the cost of command/event plumbing.
- Snapshot plus durable ledger is simpler than full event sourcing for an offline M1; replay is limited to idempotency and recovery boundaries.
- Deterministic offer generation improves reproducibility, but exact content availability still depends on versioned registry.
- Keeping artifact-effect evaluation outside BuildInventory preserves the difference between ordinary passive slots and expressive run-modifier mechanics, at the cost of a separate offer/effect projection and pending stacking policy.
- Safe pause snapshots reduce data-loss risk, but arbitrary mid-frame resume is not promised.
- Read models make UI replaceable and testable, but require projection refresh after every state revision.
- Controlled pools protect mobile performance, but pool exhaustion must surface a diagnostic rather than silently drop XP or rewards.

## 12. Explicit non-goals

- No runtime code, Godot scene rewrite or APK claim in this package.
- No visual asset creation, approval or production promotion.
- No B1 number changes.
- No network, account, multiplayer, shop or paid gacha.
- No full event-sourced backend.
- No claim that current preview scripts satisfy the target architecture.
- No hidden fallback values for unresolved product/B1 decisions.

## 13. Next implementation handoff

Next primary module: implementation/runtime slice for Iteration 1. Before it starts, the coding agent must read the six documents in this folder, implement only the thin path, and return fresh tests/evidence. Iteration 2 must add the separate artifact-offer path after boss-chest synergy is stable. Runtime changes must be performed outside this architecture scope by the authorized runtime agent.