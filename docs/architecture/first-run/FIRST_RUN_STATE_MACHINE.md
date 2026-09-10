# FIRST_RUN_STATE_MACHINE — состояния и переходы первого забега

Статус: VERIFIED ARCHITECTURE SPECIFICATION
Runtime implemented: NO
Источник истины переходов: RunSession + RunCoordinator; UI не владеет переходами.

> Revision 2: state transitions consume a versioned encounter schedule and generic chest-window source. Runtime implemented: NO.

## 1. Ownership model

| State/модель | Владелец | Разрешённая ответственность | Не владеет |
|---|---|---|---|
| App state | AppShell | Boot, content loading, menu/settings/error | Run combat, rewards |
| Menu flow | MenuFlow | Команды навигации и read models меню | Authoritative run state |
| Run lifecycle | RunCoordinator | Оркестрация команд и переходов | Формулы урона, wallet mutation |
| RunSession | RunSession aggregate | Clock, state, stage, build, stats, drops, pending offers, counters | UI nodes, textures, persistence I/O |
| Content Registry | ContentLoader/Registry | Версионированные immutable data records | Live run mutation |
| Simulation | SimulationClock, WaveDirector, CombatSystem, ProgressionSystem | Time, waves, combat, XP and level rules | Menu navigation, meta wallet |
| Build | BuildInventory + BossChestEvaluator | Six weapon/six passive slots, levels, evolution eligibility/claim | Rendering |
| Artifact effects | ArtifactOfferSystem + ArtifactEffectSystem | Three-card source offers, active run effects, refresh/duplicate guards | Boss chest, ordinary passive slots |
| Rewards | RewardCalculator + RewardLedger | Deterministic bundles, idempotency, wallet settlement | UI-only reward text |
| Persistence | PersistenceGateway | Versioned snapshots, atomic write/read, migration | Gameplay decisions |
| UI read model | HudProjection/ResultProjection | Derived display model and diagnostics presentation | Domain mutations |
| Diagnostics | DiagnosticReporter | Error codes, fallback visibility, evidence | Silent repair of invalid state |

## 2. State list

| State | Kind | Entry trigger | Exit condition | Simulation clock |
|---|---|---|---|---|
| APP_BOOT | app | Process starts | AppShell ready | N/A |
| CONTENT_LOADING | app | Boot accepted | Required content validated | N/A |
| CONTENT_ERROR | app terminal-for-attempt | Required resource/schema failure | Retry succeeds or user returns | N/A |
| MAIN_MENU | app | Content loaded / result returned | Navigation command | N/A |
| SETTINGS | app overlay/screen | Settings command | Back/close | N/A |
| CHARACTER_SELECT | app screen | ПЕРСОНАЖИ command | Character chosen/back | N/A |
| RUN_SETUP | app screen | Start flow | Confirm/cancel | N/A |
| RUN_LOADING | run lifecycle | Confirm start | Arena and session ready | Not started |
| RUN_ACTIVE | simulation | Session ready/resume | Level-up, boss checkpoint, pause, death | Running |
| UPGRADE_OFFER | blocking run state | Level-up | Offer chosen/cancel policy | Frozen |
| BOSS_INTRO | boss presentation state | Boss checkpoint reached | Intro complete | Running |
| BOSS_ACTIVE | simulation | Boss intro complete | Boss defeated/death/pause | Running |
| CHECKPOINT_SETTLEMENT | transaction state | Boss defeated | Ledger committed; final branch or non-final chest selected | Frozen |
| CHEST_OFFER | blocking run state | Configured non-final chest-window offer committed | Typed chest outcome claimed/closed by policy; no victory transition | Frozen |
| ARTIFACT_OFFER | blocking run state | Elite pack or first-clear artifact source committed | One of three cards chosen, or refresh under policy | Frozen |
| RUN_PAUSED | overlay state | User pause/background | Resume, settings, exit | Frozen |
| RECOVERY_REVIEW | recovery state | Invalid/available snapshot | Restore accepted, abandon, diagnostic | Frozen |
| RUN_DEFEAT | terminal run state | HP reaches zero | Result opened/finalized | Frozen |
| RUN_VICTORY | terminal run state | Final settlement committed after final boss defeat | Result opened/finalized | Frozen |
| RESULT_REVIEW | terminal read state | Defeat/victory | Claim/return | Frozen |
| REWARD_COMMITTING | transaction state | Claim result/reward | Commit success/failure | Frozen |
| MAIN_MENU_RETURN | transition | Commit/abandon complete | MAIN_MENU | N/A |

## 3. State graph

~~~mermaid
stateDiagram-v2
    [*] --> APP_BOOT
    APP_BOOT --> CONTENT_LOADING
    CONTENT_LOADING --> MAIN_MENU
    CONTENT_LOADING --> CONTENT_ERROR
    CONTENT_ERROR --> CONTENT_LOADING
    MAIN_MENU --> SETTINGS
    SETTINGS --> MAIN_MENU
    MAIN_MENU --> CHARACTER_SELECT
    CHARACTER_SELECT --> RUN_SETUP
    RUN_SETUP --> RUN_LOADING
    RUN_LOADING --> RUN_ACTIVE
    RUN_ACTIVE --> UPGRADE_OFFER
    UPGRADE_OFFER --> RUN_ACTIVE
    RUN_ACTIVE --> BOSS_INTRO
    BOSS_INTRO --> BOSS_ACTIVE
    BOSS_ACTIVE --> CHECKPOINT_SETTLEMENT
    CHECKPOINT_SETTLEMENT --> CHEST_OFFER
    RUN_ACTIVE --> CHEST_OFFER
    CHECKPOINT_SETTLEMENT --> RUN_VICTORY
    RUN_ACTIVE --> ARTIFACT_OFFER
    RESULT_REVIEW --> ARTIFACT_OFFER
    ARTIFACT_OFFER --> RUN_ACTIVE
    ARTIFACT_OFFER --> RESULT_REVIEW
    CHEST_OFFER --> RUN_ACTIVE
    RUN_ACTIVE --> RUN_PAUSED
    BOSS_ACTIVE --> RUN_PAUSED
    RUN_PAUSED --> RUN_ACTIVE
    RUN_PAUSED --> BOSS_ACTIVE
    RUN_PAUSED --> SETTINGS
    RUN_PAUSED --> MAIN_MENU_RETURN
    RUN_PAUSED --> RECOVERY_REVIEW
    RECOVERY_REVIEW --> RUN_ACTIVE
    RECOVERY_REVIEW --> MAIN_MENU_RETURN
    RUN_ACTIVE --> RUN_DEFEAT
    BOSS_ACTIVE --> RUN_DEFEAT
    RUN_DEFEAT --> RESULT_REVIEW
    RUN_VICTORY --> RESULT_REVIEW
    RESULT_REVIEW --> REWARD_COMMITTING
    REWARD_COMMITTING --> MAIN_MENU_RETURN
    MAIN_MENU_RETURN --> MAIN_MENU
~~~

The final boss enters BOSS_INTRO/BOSS_ACTIVE at the terminal 1800-second target slot. Its defeat goes through CHECKPOINT_SETTLEMENT and final ledger settlement directly to RUN_VICTORY; no CHEST_OFFER is created for the final boss. The final boss never creates a boss chest or generic defeat chest. Timer expiry alone is not victory. The schedule also contains five non-final main-boss slots and three intermediate-boss slots; exact new content IDs/tuning remain pending.
## 3.1 Encounter schedule and wave-cycle state

The target registry has six main-boss records and three intermediate-boss records. It resolves the following order without hard-coded UI branches:

1. 05:00 main boss;
2. 07:30 intermediate boss from C3;
3. 10:00 main boss;
4. 12:30 intermediate boss from C3;
5. 15:00 main boss;
6. 20:00 new main-boss slot;
7. 22:30 new intermediate slot (target placement pending approval);
8. 25:00 new main-boss slot;
9. 30:00 existing final boss identity.

The final slot alone has is_final=true. The five-minute main cadence and 22:30 slot are working architecture targets and can be changed in the registry after Product/B1 approval.

## 3.2 State invariants for wave pressure and variants

- WaveDirector resolves all main/intermediate encounters through encounter_schedule; state transitions do not branch on hard-coded boss names.
- Every non-final encounter ends in a relief/rebuild phase before the next ramp. BOSS_INTRO and BOSS_ACTIVE continue the clock; settlement/chest/offer states freeze it.
- EnemyVariantResolver is deterministic and records base_enemy_id, variant_id, wave_cycle_id and selection_revision; the same input revision cannot spawn a different variant.
- A variant inherits XP/aftermath/reward boundaries from its base enemy unless an explicit B1 record says otherwise. A color change alone is not an accessibility-complete distinction.
- A missing new boss/enemy/variant record blocks only the dependent authoritative spawn and emits diagnostics; it never silently falls back to an unrelated enemy or boss.


## 4. Transition contract

Каждый transition выполняется через RunCoordinator, который вызывает доменный owner. Таблица использует stable transition IDs и отдельно фиксирует trigger, guard, owner, side effects, failure path, recovery path и duplicate/idempotency behavior.

| ID | From → To | Trigger | Preconditions/guard | Owner | Side effects | Failure path | Recovery path | Duplicate/idempotency behavior |
|---|---|---|---|---|---|---|---|---|
| T-01 | APP_BOOT → CONTENT_LOADING | boot_ready | AppShell initialized | AppShell / ContentLoader | ContentLoader starts versioned load | Diagnostic boot error; retry has new load attempt | Recover from owning boundary: Diagnostic boot error; retry has new load attempt | Duplicate boot creates no second load or RunSession |
| T-02 | CONTENT_LOADING → MAIN_MENU | content_loaded | Required records valid; save migrated or absent | ContentLoader / AppShell | Build menu read model | Invalid optional record is quarantined; required failure → T-03 | Retry from last coherent state or enter diagnostic recovery | Same load attempt returns existing menu projection |
| T-03 | CONTENT_LOADING → CONTENT_ERROR | content_load_failed | Required content/schema missing | ContentLoader / DiagnosticReporter | DiagnosticReporter records code/path/version | Retry or return; no RunSession | Recover from owning boundary: Retry or return; no RunSession | Duplicate failure for one load attempt is a no-op |
| T-04 | MAIN_MENU ↔ SETTINGS | open/back settings | Menu context valid | SettingsFlow | SettingsFlow reads/writes validated settings | Invalid value rejected; previous valid value remains | Retry from last coherent state or enter diagnostic recovery | Repeated settings navigation rebuilds projection without mutation |
| T-05 | MAIN_MENU → CHARACTER_SELECT | open characters | Registry has selectable records | MenuFlow | Character read model | Missing card shown as non-selectable diagnostic | Recover from owning boundary: Missing card shown as non-selectable diagnostic | Repeated navigation is a no-op |
| T-06 | CHARACTER_SELECT → RUN_SETUP | select_character | character_id exists and unlocked | RunSetupModel / RunCoordinator | RunSetupModel stores selection | Unknown/stale ID is no-op with error | Recover from owning boundary: Unknown/stale ID is no-op with error | Same character selection is a no-op |
| T-07 | RUN_SETUP → RUN_LOADING | confirm_start | Character, no pre-run artifact selection, and content version valid | RunCoordinator | RunCoordinator creates run_id/seed and provisional RunSession | Any artifact_ids/pre-run loadout is rejected; validation failure returns to setup | Recover from owning boundary: Any artifact_ids/pre-run loadout is rejected; validation failure returns to setup | client_request_id returns existing start; no second RunSession |
| T-08 | RUN_LOADING → RUN_ACTIVE | arena_ready | Session schema and required gameplay content validated | RunCoordinator / Arena adapter | Clock starts; first wave band derived | Resource failure → recoverable run error; no false reward | Retry from last coherent state or enter diagnostic recovery | Repeated arena_ready is a no-op |
| T-09 | RUN_ACTIVE → UPGRADE_OFFER | level_up | Offer generator can produce valid projection | ProgressionSystem / OfferGenerator | Freeze clock; persist pending offer if policy requires | Invalid pool → deterministic fallback or diagnostic, never illegal card | Recover from owning boundary: Invalid pool → deterministic fallback or diagnostic, never illegal card | offer_id plus state_revision returns same offer |
| T-10 | UPGRADE_OFFER → RUN_ACTIVE | offer_chosen | offer_id belongs to open offer and not claimed | RunCoordinator / BuildInventory | Apply BuildInventory/Stats mutation; clear offer | Duplicate/stale choice is rejected/no-op | Recover from owning boundary: Duplicate/stale choice is rejected/no-op | Repeated choice returns stored outcome; no second mutation |
| T-11 | RUN_ACTIVE → BOSS_INTRO | checkpoint_reached | checkpoint_id matches next unhandled encounter_schedule slot (main or intermediate) | WaveDirector / BossDirector | Enter scheduled encounter, select cycle phase and create one encounter | Missing/pending required record blocks spawn with diagnostic; duplicate boundary ignored | Retry after registry/B1 is valid or enter recovery; no reward is created | checkpoint_id/encounter_id creates one encounter only |
| T-12 | BOSS_INTRO → BOSS_ACTIVE | intro_complete | Boss record and safe spawn available | BossDirector | Start boss pattern/telegraph contract | Safe spawn retry; failure → paused diagnostic | Recover from owning boundary: Safe spawn retry; failure → paused diagnostic | Existing encounter ID returns existing intro |
| T-13 | BOSS_ACTIVE → CHECKPOINT_SETTLEMENT | boss_defeated | Non-final encounter active; final boss uses T-17 | Combat / BossDirector / RunCoordinator | Freeze; create checkpoint settlement command | Duplicate defeat ignored by encounter id | Retry from last coherent state or enter diagnostic recovery | boss_encounter_id prevents second settlement |
| T-14 | CHECKPOINT_SETTLEMENT → CHEST_OFFER | checkpoint_settled | Non-final scheduled encounter; ledger commit succeeded; matching chest window is configured | RewardLedger / ChestWindowSystem / RunCoordinator | Record checkpoint and create one typed chest offer | Persistence or missing window configuration keeps transaction retryable/pending; no silent chest | Retry settlement/window resolution from same revision; do not create a second offer | checkpoint_id + chest_window_id + ledger key returns existing settlement/offer |
| T-14F | CHECKPOINT_SETTLEMENT → RUN_VICTORY | final_settlement_committed | is_final=true terminal schedule slot; ledger commit succeeded; no chest pending | RewardLedger / RunCoordinator | Mark terminal victory and build result projection; first-clear artifact offer opens only after result finalization | Persistence failure keeps settlement retryable | Recover from owning boundary: Persistence failure keeps settlement retryable | Final encounter/checkpoint plus ledger key returns existing final settlement |
| T-15 | CHEST_OFFER → RUN_ACTIVE | chest_claimed | Offer belongs to a configured non-final window; outcome valid and not already claimed | ChestWindowSystem / RunCoordinator | Apply typed synergy/evolution/fallback/approved chest outcome; mark window claimed; advance stage if required | Duplicate/stale claim returns existing outcome or diagnostic; final-source guard rejects | Retry same offer from persisted revision; no new outcome | chest_offer_id + window_id returns stored outcome |
| T-15C | RUN_ACTIVE → CHEST_OFFER | chest_window_triggered | Non-boss reserved window is configured, source trigger is authoritative, and no open offer exists | ChestWindowSystem / RunCoordinator | Create one source-bound chest offer and freeze clock | Unconfigured/pending source becomes diagnostic/pending without offer; duplicate trigger ignored | Retry after source registry is valid from same cycle/revision | chest_window_id + source_id dedupes offer creation |
| T-15E | RUN_ACTIVE → ARTIFACT_OFFER | elite_pack_defeated | Elite-pack source is authoritative and offer policy allows it | ArtifactOfferSystem | ArtifactOfferSystem creates exactly three candidate cards and freezes clock | Duplicate elite encounter does not create a second offer | Retry from last coherent state or enter diagnostic recovery | Encounter/offer identity prevents second artifact offer |
| T-15R | ARTIFACT_OFFER → ARTIFACT_OFFER | artifact_offer_refresh_requested | Refresh policy allows it; expected revision/idempotency key valid | ArtifactOfferSystem | Reroll three cards and increment refresh count; no artifact instance yet | Duplicate refresh returns the stored offer without a second charge/reroll | Recover from owning boundary: Duplicate refresh returns the stored offer without a second charge/reroll | artifact_offer_id plus idempotency key returns stored refresh |
| T-15A | ARTIFACT_OFFER → RUN_ACTIVE | artifact_chosen | Selected ID belongs to the three-card offer; choice not claimed | ArtifactEffectSystem / RunCoordinator | ArtifactEffectSystem creates one active run effect/instance; close offer | Duplicate choice returns the same artifact instance | Recover from owning boundary: Duplicate choice returns the same artifact instance | Repeated choice returns same artifact instance |
| T-15F | RESULT_REVIEW → ARTIFACT_OFFER | first_clear_artifact_offer_requested | Result finalized and first-clear reward is eligible | RewardBoundary / ArtifactOfferSystem | Create separate post-result three-card artifact offer; no boss chest is involved | Repeat clear does not create first-clear offer | Retry from last coherent state or enter diagnostic recovery | result_id plus first-clear key prevents repeated offer |
| T-15FR | ARTIFACT_OFFER → RESULT_REVIEW | artifact_chosen after first-clear result | Offer source is FIRST_CLEAR_REWARD; selected ID belongs to offer | ArtifactEffectSystem / RewardBoundary | Commit one first-clear artifact effect/instance and close offer | Duplicate choice returns same instance | Recover from owning boundary: Duplicate choice returns same instance | artifact_offer_id returns same first-clear instance |
| T-16 | BOSS_ACTIVE → RUN_DEFEAT | player_death | Death not settled | Combat / RunCoordinator | Freeze and create defeat result | Duplicate death ignored | Retry from last coherent state or enter diagnostic recovery | Terminal run_id accepts one defeat only |
| T-17 | BOSS_ACTIVE → CHECKPOINT_SETTLEMENT | final_boss_defeated | Scheduled encounter has is_final=true and authoritative defeat | BossDirector / RunCoordinator | Create final settlement command; do not create chest offer; victory waits for T-14F | Invalid final result returns to checkpoint recovery | Recover from owning boundary: Invalid final result returns to checkpoint recovery | Final encounter ID prevents second final settlement |
| T-18 | RUN_ACTIVE/BOSS_ACTIVE → RUN_PAUSED | pause_requested/background | Current state resumable | RunCoordinator / PersistenceGateway | Freeze clock; write allowed snapshot | Snapshot failure leaves in-memory paused state with diagnostic | Recover from owning boundary: Snapshot failure leaves in-memory paused state with diagnostic | Pause revision prevents second snapshot |
| T-19 | RUN_PAUSED → RUN_ACTIVE/BOSS_ACTIVE | resume_requested | Snapshot/content/checksum valid | Recovery / PauseFlow | Restore resume_state and continue clock | Invalid snapshot → RECOVERY_REVIEW | Recover from owning boundary: Invalid snapshot → RECOVERY_REVIEW | restored_revision makes resume idempotent |
| T-20 | RUN_PAUSED → SETTINGS | settings_requested | Pause context is valid | SettingsFlow | Open settings while preserving paused_from_state | Settings failure returns to pause with diagnostic | Recover from owning boundary: Settings failure returns to pause with diagnostic | Repeated settings requests do not mutate run |
| T-21 | RUN_PAUSED → RECOVERY_REVIEW | restore_needed | Background kill or invalid live state | PersistenceGateway / Recovery | Show last coherent revision and choices | No valid revision → abandon without rewards | Retry from last coherent state or enter diagnostic recovery | snapshot_id plus revision returns same recovery review |
| T-22 | RUN_PAUSED/RECOVERY_REVIEW → MAIN_MENU_RETURN | exit_confirmed/abandon_confirmed | User confirms abandon or recovery policy | PauseFlow / Recovery | Mark session abandoned; do not settle unearned rewards | Cancel returns to originating state | Recover from owning boundary: Cancel returns to originating state | Abandoned session returns without second settlement |
| T-23 | RUN_DEFEAT/RUN_VICTORY → RESULT_REVIEW | result_opened | Terminal result exists | ResultProjection / RunCoordinator | Build immutable result projection | Missing result → retry from snapshot | Recover from owning boundary: Missing result → retry from snapshot | result_id reopens same read-only projection |
| T-24 | RESULT_REVIEW → REWARD_COMMITTING | claim_result | Result not committed or ledger has pending entries | RewardBoundary / RewardLedger | Start one atomic reward transaction | Retry same idempotency keys | Recover from owning boundary: Retry same idempotency keys | result_id plus idempotency key cannot start second reward transaction |
| T-25 | REWARD_COMMITTING → MAIN_MENU_RETURN | reward_commit_succeeded | Ledger and meta save committed | RewardLedger / PersistenceGateway | Mark result claimed | Save failure retains retryable transaction | Recover from owning boundary: Save failure retains retryable transaction | Ledger key returns existing committed result |
| T-26 | MAIN_MENU_RETURN → MAIN_MENU | return_complete | No pending commit | MenuFlow | Refresh wallets/unlocks | If refresh fails, keep committed values and show diagnostic | Recover from owning boundary: If refresh fails, keep committed values and show diagnostic | Repeated return command is a no-op |

## 5. Pause/background model

RUN_PAUSED содержит:

- paused_from_state;
- pause_reason: MANUAL, ANDROID_BACKGROUND, RECOVERY;
- last_coherent_snapshot_revision;
- whether a pending upgrade, boss-chest or artifact offer exists;
- diagnostic code, если snapshot/content mismatch.

UPGRADE_OFFER, CHEST_OFFER и ARTIFACT_OFFER сами замораживают simulation; BOSS_INTRO остаётся непаузным presentation state и не останавливает clock. Вход в Settings из offer или RUN_PAUSED возвращается в тот же blocking/resume context. В RUN_PAUSED Settings открывается отдельным transition без возобновления clock; выход ведёт в подтверждение/MAIN_MENU_RETURN. Android background не считается победой, поражением или выходом из забега.

Working assumption: snapshot делается на checkpoint, при явной паузе и в terminal/reward boundary. Полный произвольный mid-frame resume не обещается до отдельного product decision.

## 6. Terminal states and repeat behavior

- RUN_DEFEAT и RUN_VICTORY terminal для конкретного run_id.
- RESULT_REVIEW можно открывать повторно; это read-only projection.
- REWARD_COMMITTING повторяется только с теми же idempotency keys.
- После committed result старый run нельзя возобновить как active.
- Повторный event для boss defeat, boss-chest claim, checkpoint reward, artifact choice/refresh или result claim возвращает уже сохранённый outcome.
- Новый забег всегда получает новый run_id и новый deterministic seed.

## 7. Invariants

1. Final boss defeat cannot bypass CHECKPOINT_SETTLEMENT or RewardLedger; final settlement transitions directly to RUN_VICTORY without CHEST_OFFER or any boss chest.
2. UI не меняет authoritative state напрямую.
3. Clock advances in RUN_ACTIVE, BOSS_INTRO and BOSS_ACTIVE for every boss; it freezes in offer, pause, settlement and terminal/transaction states.
4. XPDrop не превращается в AftermathItem и наоборот.
5. Checkpoint reward не применяется без ledger idempotency key.
6. Final victory невозможна без final boss defeat и финального settlement; final boss не создаёт boss chest, а first-clear artifact offer создаётся отдельной post-result boundary.
7. Unknown/stale content не превращается в silent default.
8. Ошибка persistence не подтверждает reward commit.
9. Повторная доставка одного effect command не меняет итог.
10. Все неизвестные числовые/продуктовые решения отмечены в data contract и decisions file.
11. Artifact offer всегда содержит ровно три кандидата; один выбор создаёт один active run effect без фиксированного capacity и без weapon/passive slot consumption.
12. Boss chest и artifact offer имеют разные state IDs, event IDs, idempotency keys и outcome contracts.
13. The configured chest-window cap is 15; a window can create at most one offer and the cap is independent from the five-claim synergy cap.
14. The final schedule slot is the only final boss slot; it creates no boss chest or generic defeat chest.
15. Three enemy_ink_beetle variants share one base reward boundary and are selected by deterministic data, not UI logic.
16. New boss/enemy slots remain explicit pending registry records until Content/B1 owners provide names, mechanics and tuning.
