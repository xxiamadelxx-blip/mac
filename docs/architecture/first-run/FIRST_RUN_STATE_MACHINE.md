
# FIRST_RUN_STATE_MACHINE — состояния и переходы

Статус: **SPECIFIED_WITH_PENDING_DECISIONS**  
Модель: экранные состояния оркестрирует AppFlowCoordinator, доменные состояния принадлежат RunSession, side effects с идемпотентностью принадлежат RewardLedger и SaveRepository.

## 1. Ownership model

| State family | Owner | Authoritative data |
|---|---|---|
| Boot/loading/menu/settings/characters | AppFlowCoordinator | AppReadModel, Diagnostics |
| Run active/wave/boss/upgrade/chest | RunSession + domain services | RunState, BuildState, RunClock |
| Pause/background | RunSession freezes clock; coordinator owns overlay | PauseContext, validated snapshot |
| Defeat/victory/result | ResultAssembler + RewardLedger | immutable ResultSnapshot, ledger entries |
| Persistence/recovery | SaveRepository | versioned SaveSnapshot |
| UI | screen controllers/read models | no authoritative mutation |

UI может отражать domain state, но не является source of truth.

## 2. State inventory

| ID | Owner | Meaning | Terminal? | Reopen rule |
|---|---|---|---|---|
| BOOT | AppFlowCoordinator | process started, diagnostics initialized | no | one entry per process |
| LOADING_MENU | AppFlowCoordinator | registry/profile/save validation | no | retry same request or safe error |
| MENU_HOME | AppFlowCoordinator | main menu ready | no | idempotent navigation |
| MENU_SETTINGS | AppFlowCoordinator | settings projection | no | return to captured owner |
| MENU_CHARACTERS | AppFlowCoordinator | hero list/selection | no | selection stays in menu model |
| RUN_SETUP | AppFlowCoordinator | hero/artifact validation | no | invalid command returns here |
| RUN_LOADING | AppFlowCoordinator + RunLoader | arena/content loading | no | retry or setup; no half-run |
| RUN_ACTIVE | RunSession | simulation ticking | no | resume after guard |
| UPGRADE_CHOICE | ProgressionService | clock frozen, offer pending | no | same offer set until decision |
| BOSS_TELEGRAPH | WaveDirector/CombatResolver | boss warning/reaction | no | duplicate spawn event no-op |
| BOSS_ACTIVE | RunSimulation | boss encounter | no | same boss instance/event identity |
| CHEST_PENDING | ChestResolver | boss chest unresolved | no | same chest/offer reopens |
| CHECKPOINT_RESOLVED | RunSession + RewardLedger | checkpoint side effects committed | no | replay returns entry |
| PAUSED | RunSession + AppFlowCoordinator | run frozen under overlay | no | repeated pause no-op |
| BACKGROUND_SUSPENDED | RunSession + SaveRepository | OS freeze/snapshot request | no | restore only after validation |
| DEFEAT | ResultAssembler | run ended by death | yes for simulation | result read-only reopen |
| VICTORY | ResultAssembler | final boss/victory passed | yes for simulation | result read-only reopen |
| RESULTS_PENDING | ResultAssembler + RewardLedger | result built, claims pending | no for result flow | reconstruct by result_id |
| RESULTS_CLAIMED | RewardLedger | result entries acknowledged | terminal result flow | replay returns receipt |
| RESOURCE_ERROR | Diagnostics + AppFlowCoordinator | cannot proceed safely | no | retry/safe mode/menu |
| RETURN_TO_MENU | AppFlowCoordinator | route after result/abandon | no | one route per request |

## 3. State diagram

~~~mermaid
stateDiagram-v2
    [*] --> BOOT
    BOOT --> LOADING_MENU
    LOADING_MENU --> MENU_HOME
    LOADING_MENU --> RESOURCE_ERROR
    RESOURCE_ERROR --> LOADING_MENU: retry
    MENU_HOME --> MENU_CHARACTERS
    MENU_HOME --> MENU_SETTINGS
    MENU_HOME --> RUN_SETUP
    MENU_SETTINGS --> MENU_HOME
    MENU_CHARACTERS --> RUN_SETUP
    RUN_SETUP --> RUN_LOADING: valid start
    RUN_SETUP --> MENU_CHARACTERS: missing hero
    RUN_LOADING --> RUN_ACTIVE
    RUN_LOADING --> RESOURCE_ERROR
    RUN_ACTIVE --> UPGRADE_CHOICE: level up
    UPGRADE_CHOICE --> RUN_ACTIVE: offer chosen
    RUN_ACTIVE --> BOSS_TELEGRAPH: checkpoint
    BOSS_TELEGRAPH --> BOSS_ACTIVE
    BOSS_ACTIVE --> CHEST_PENDING: boss defeated
    CHEST_PENDING --> CHECKPOINT_RESOLVED: claim/fallback
    CHECKPOINT_RESOLVED --> RUN_ACTIVE: next band
    RUN_ACTIVE --> PAUSED: pause
    PAUSED --> RUN_ACTIVE: resume
    RUN_ACTIVE --> BACKGROUND_SUSPENDED: app background
    BACKGROUND_SUSPENDED --> RUN_ACTIVE: validated resume
    RUN_ACTIVE --> DEFEAT: HP zero
    BOSS_ACTIVE --> DEFEAT: HP zero
    BOSS_ACTIVE --> VICTORY: final boss defeated
    DEFEAT --> RESULTS_PENDING
    VICTORY --> RESULTS_PENDING
    RESULTS_PENDING --> RESULTS_CLAIMED: claim/replay
    RESULTS_CLAIMED --> RETURN_TO_MENU
    RETURN_TO_MENU --> MENU_HOME
~~~

Duplicate-event self-loops omitted from the diagram are explicit below and never create a second grant.

## 4. Transition contract

| ID | From → To | Trigger | Guard | Owner/side effect | Failure/recovery |
|---|---|---|---|---|---|
| T-01 | BOOT → LOADING_MENU | process ready | coordinator exists | load registry/profile | fatal init → RESOURCE_ERROR |
| T-02 | LOADING_MENU → MENU_HOME | validation success | schema/content compatible | publish menu model | retry preserves diagnostic |
| T-03 | LOADING_MENU → RESOURCE_ERROR | missing/stale resource | required data unavailable | record code/path/version | retry/safe mode/menu |
| T-04 | MENU_HOME → MENU_CHARACTERS | open characters | hero registry readable | project hero cards | missing card disabled |
| T-05 | MENU_HOME → MENU_SETTINGS | open settings | none | capture return owner | safe default on read failure |
| T-06 | MENU_CHARACTERS → RUN_SETUP | choose hero | hero unlocked/valid | persist menu selection | invalid selection stays |
| T-07 | RUN_SETUP → RUN_LOADING | start run | valid hero/artifacts, no conflict | create run_id/seed/zero clock | reject without session |
| T-08 | RUN_LOADING → RUN_ACTIVE | arena loaded | spawn/content/read model valid | emit run.started, start clock | retry/setup; no half-run |
| T-09 | RUN_ACTIVE → UPGRADE_CHOICE | XP threshold | legal offer set exists | freeze clock, expose offer | deterministic regenerate/diagnostic |
| T-10 | UPGRADE_CHOICE → RUN_ACTIVE | choose offer | offer version/ownership valid | apply one upgrade | duplicate returns applied result |
| T-11 | RUN_ACTIVE → BOSS_TELEGRAPH | checkpoint time | boss not already spawned | gate normal spawn, telegraph | duplicate checkpoint ignored |
| T-12 | BOSS_TELEGRAPH → BOSS_ACTIVE | telegraph elapsed | boss instance valid | create boss, budget reduction | missing boss → RESOURCE_ERROR |
| T-13 | BOSS_ACTIVE → CHEST_PENDING | boss HP zero | authoritative defeat | record defeat, checkpoint reward, chest | replay uses same IDs |
| T-14 | CHEST_PENDING → CHECKPOINT_RESOLVED | claim/fallback | offer open and legal | claim one outcome | close/reopen keeps offer |
| T-15 | CHECKPOINT_RESOLVED → RUN_ACTIVE | checkpoint committed | next band exists | set band/stage | final checkpoint → victory guard |
| T-16 | RUN_ACTIVE → PAUSED | pause command | not terminal | freeze clock, overlay | repeat is no-op |
| T-17 | PAUSED → RUN_ACTIVE | resume | run not terminal | close overlay, clock resumes | stale run → recovery/result |
| T-18 | RUN_ACTIVE → BACKGROUND_SUSPENDED | Android pause | not terminal | freeze first, snapshot request | write error recorded |
| T-19 | BACKGROUND_SUSPENDED → RUN_ACTIVE | app resume | in-memory/session valid | publish same revision | bad snapshot → error/prompt |
| T-20 | RUN_ACTIVE/BOSS_ACTIVE → DEFEAT | HP ≤ 0 | death not finalized | immutable result, partial reward | duplicate returns result |
| T-21 | BOSS_ACTIVE → VICTORY | final boss defeated | final checkpoint/victory guard | terminal result, final rewards | missing condition stays pending |
| T-22 | DEFEAT/VICTORY → RESULTS_PENDING | result finalized | result_id stable | publish immutable result | rebuild from snapshot |
| T-23 | RESULTS_PENDING → RESULTS_CLAIMED | claim/replay | ledger entries valid | apply receipts | duplicate key returns receipt |
| T-24 | RESULTS_CLAIMED → RETURN_TO_MENU | menu action | claim complete or explicit pending choice | close run presentation | route retry safe |

## 5. Pause/background as explicit transition

Pause is a domain freeze, not a second simulation owner:

- RunSession phase сохраняет RUN_ACTIVE/BOSS_ACTIVE/UPGRADE context;
- clock.is_running = false;
- combat/build mutation commands rejected while paused;
- settings store return_state = PAUSED;
- Android background uses BACKGROUND_SUSPENDED for persistence, then returns to captured phase after validation;
- while frozen, no time, spawn, damage, XP, chest or reward side effect is legal.

## 6. Idempotency

| Operation | Idempotency key | Duplicate behavior |
|---|---|---|
| Boss checkpoint reward | checkpoint:{run_id}:{checkpoint_id} | return existing ledger entry |
| Chest claim | chest:{run_id}:{chest_id} | return prior outcome |
| Synergy claim | synergy:{run_id}:{synergy_id} | existing claimed synergy is no-op |
| Defeat result | result:{run_id}:defeat | return immutable snapshot |
| Victory result | result:{run_id}:victory | return immutable snapshot |
| First-clear bonus | result:{run_id}:first_clear | grant once per profile/map policy |
| Save restore | restore:{snapshot_id}:{revision} | same validated revision restores once |
| Offer choice | offer:{run_id}:{offer_id} | same applied choice returned |

DEFEAT and VICTORY are terminal for simulation. Their result screens may reopen read-only until claim receipt is shown. Reopen reads immutable result plus ledger and never recalculates rewards.

## 7. Illegal transitions and diagnostics

A command is rejected without partial side effects when:

- owner state does not match command;
- stable ID is missing/stale;
- clock is frozen but command requires active simulation;
- checkpoint/chest/result key is already resolved with incompatible payload;
- snapshot fails integrity validation;
- content version cannot resolve an item.

Every rejection emits reason_code, current state, command_id and recoverability. UI shows a recovery action, not a silent jump.

## 8. Verification checklist

- [ ] Every state has owner and observable entry/exit behavior.
- [ ] Every transition has trigger, guard, owner, side effect and recovery.
- [ ] Pause/background never advances the clock.
- [ ] Replayed boss/chest/result/save operations never duplicate grants.
- [ ] Terminal result reopens without simulation.
- [ ] RESOURCE_ERROR is recoverable without a white screen.
