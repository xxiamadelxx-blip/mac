# FIRST_RUN_STATE_MACHINE — состояния и переходы первого забега

Статус: DRAFT ARCHITECTURE SPECIFICATION  
Runtime implemented: NO  
Источник истины переходов: RunSession + RunCoordinator; UI не владеет переходами.

## 1. Ownership model

| State/модель | Владелец | Разрешённая ответственность | Не владеет |
|---|---|---|---|
| App state | AppShell | Boot, content loading, menu/settings/error | Run combat, rewards |
| Menu flow | MenuFlow | Команды навигации и read models меню | Authoritative run state |
| Run lifecycle | RunCoordinator | Оркестрация команд и переходов | Формулы урона, wallet mutation |
| RunSession | RunSession aggregate | Clock, state, stage, build, stats, drops, pending offers, counters | UI nodes, textures, persistence I/O |
| Content Registry | ContentLoader/Registry | Версионированные immutable data records | Live run mutation |
| Simulation | SimulationClock, WaveDirector, CombatSystem, ProgressionSystem | Time, waves, combat, XP and level rules | Menu navigation, meta wallet |
| Build | BuildInventory + SynergyEvaluator | Slots, levels, evolution eligibility/claim | Rendering |
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
| BOSS_INTRO | blocking run state | Boss checkpoint reached | Intro complete | Frozen |
| BOSS_ACTIVE | simulation | Boss intro complete | Boss defeated/death/pause | Running |
| CHECKPOINT_SETTLEMENT | transaction state | Boss defeated | Ledger committed | Frozen |
| CHEST_OFFER | blocking run state | Settlement committed | Chest claimed/closed by policy | Frozen |
| RUN_PAUSED | overlay state | User pause/background | Resume, settings, exit | Frozen |
| RECOVERY_REVIEW | recovery state | Invalid/available snapshot | Restore accepted, abandon, diagnostic | Frozen |
| RUN_DEFEAT | terminal run state | HP reaches zero | Result opened/finalized | Frozen |
| RUN_VICTORY | terminal run state | Final boss defeated | Result opened/finalized | Frozen |
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
    CHEST_OFFER --> RUN_ACTIVE
    RUN_ACTIVE --> RUN_PAUSED
    BOSS_ACTIVE --> RUN_PAUSED
    RUN_PAUSED --> RUN_ACTIVE
    RUN_PAUSED --> RECOVERY_REVIEW
    RECOVERY_REVIEW --> RUN_ACTIVE
    RUN_ACTIVE --> RUN_DEFEAT
    BOSS_ACTIVE --> RUN_DEFEAT
    BOSS_ACTIVE --> RUN_VICTORY
    RUN_DEFEAT --> RESULT_REVIEW
    RUN_VICTORY --> RESULT_REVIEW
    RESULT_REVIEW --> REWARD_COMMITTING
    REWARD_COMMITTING --> MAIN_MENU_RETURN
    MAIN_MENU_RETURN --> MAIN_MENU
~~~

Final boss checkpoint enters BOSS_INTRO/BOSS_ACTIVE at the canonical 1200-second boundary. RUN_VICTORY is allowed only after the final boss defeat; timer expiry alone is not victory.

## 4. Transition contract

Каждый transition выполняется через RunCoordinator, который вызывает доменный owner. Таблица использует stable transition IDs.

| ID | From → To | Trigger | Guard | Owner/side effects | Failure/recovery |
|---|---|---|---|---|---|
| T-01 | APP_BOOT → CONTENT_LOADING | boot_ready | AppShell initialized | ContentLoader starts versioned load | Diagnostic boot error; retry has new load attempt |
| T-02 | CONTENT_LOADING → MAIN_MENU | content_loaded | Required records valid; save migrated or absent | Build menu read model | Invalid optional record is quarantined; required failure → T-03 |
| T-03 | CONTENT_LOADING → CONTENT_ERROR | content_load_failed | Required content/schema missing | DiagnosticReporter records code/path/version | Retry or return; no RunSession |
| T-04 | MAIN_MENU ↔ SETTINGS | open/back settings | Menu context valid | SettingsFlow reads/writes validated settings | Invalid value rejected; previous valid value remains |
| T-05 | MAIN_MENU → CHARACTER_SELECT | open characters | Registry has selectable records | Character read model | Missing card shown as non-selectable diagnostic |
| T-06 | CHARACTER_SELECT → RUN_SETUP | select_character | character_id exists and unlocked | RunSetupModel stores selection | Unknown/stale ID is no-op with error |
| T-07 | RUN_SETUP → RUN_LOADING | confirm_start | Character, artifact selection and content version valid | RunCoordinator creates run_id/seed and provisional RunSession | Validation failure returns to setup |
| T-08 | RUN_LOADING → RUN_ACTIVE | arena_ready | Session schema and required gameplay content validated | Clock starts; first wave band derived | Resource failure → recoverable run error; no false reward |
| T-09 | RUN_ACTIVE → UPGRADE_OFFER | level_up | Offer generator can produce valid projection | Freeze clock; persist pending offer if policy requires | Invalid pool → deterministic fallback or diagnostic, never illegal card |
| T-10 | UPGRADE_OFFER → RUN_ACTIVE | offer_chosen | offer_id belongs to open offer and not claimed | Apply BuildInventory/Stats mutation; clear offer | Duplicate/stale choice is rejected/no-op |
| T-11 | RUN_ACTIVE → BOSS_INTRO | checkpoint_reached | checkpoint_id matches next unhandled B1 boundary | Freeze normal spawn, create boss encounter | Duplicate boundary ignored |
| T-12 | BOSS_INTRO → BOSS_ACTIVE | intro_complete | Boss record and safe spawn available | Start boss pattern/telegraph contract | Safe spawn retry; failure → paused diagnostic |
| T-13 | BOSS_ACTIVE → CHECKPOINT_SETTLEMENT | boss_defeated | Encounter active; defeat not settled | Freeze; create settlement command | Duplicate defeat ignored by encounter id |
| T-14 | CHECKPOINT_SETTLEMENT → CHEST_OFFER | checkpoint_settled | Ledger commit succeeded | Record checkpoint; create chest offer | Persistence failure keeps transaction retryable |
| T-15 | CHEST_OFFER → RUN_ACTIVE | chest_claimed | offer valid; evaluator outcome not already claimed | Apply synergy/artifact/fallback; mark offer claimed | Duplicate claim returns existing outcome |
| T-16 | BOSS_ACTIVE → RUN_DEFEAT | player_death | death not settled | Freeze and create defeat result | Duplicate death ignored |
| T-17 | BOSS_ACTIVE → RUN_VICTORY | final_boss_defeated | checkpoint is final; final boss defeated | Create victory result; no timer-only shortcut | Invalid final result returns to checkpoint recovery |
| T-18 | RUN_ACTIVE/BOSS_ACTIVE → RUN_PAUSED | pause_requested/background | Current state resumable | Freeze clock; write allowed snapshot | Snapshot failure leaves in-memory paused state with diagnostic |
| T-19 | RUN_PAUSED → RUN_ACTIVE/BOSS_ACTIVE | resume_requested | snapshot/content/checksum valid | Restore resume_state and continue clock | Invalid snapshot → RECOVERY_REVIEW |
| T-20 | RUN_PAUSED → RECOVERY_REVIEW | restore_needed | Background kill or invalid live state | Show last coherent revision and choices | No valid revision → abandon without rewards |
| T-21 | RUN_PAUSED → MAIN_MENU_RETURN | exit_confirmed | User confirms abandon or recover policy | Mark session abandoned; do not settle unearned rewards | Cancel returns to RUN_PAUSED |
| T-22 | RUN_DEFEAT/RUN_VICTORY → RESULT_REVIEW | result_opened | terminal result exists | Build immutable result projection | Missing result → retry from snapshot |
| T-23 | RESULT_REVIEW → REWARD_COMMITTING | claim_result | result not committed or ledger has pending entries | Start one atomic reward transaction | Retry same idempotency keys |
| T-24 | REWARD_COMMITTING → MAIN_MENU_RETURN | reward_commit_succeeded | Ledger and meta save committed | Mark result claimed | Save failure retains retryable transaction |
| T-25 | MAIN_MENU_RETURN → MAIN_MENU | return_complete | No pending commit | Refresh wallets/unlocks | If refresh fails, keep committed values and show diagnostic |

## 5. Pause/background model

RUN_PAUSED содержит:

- paused_from_state;
- pause_reason: MANUAL, ANDROID_BACKGROUND, RECOVERY;
- last_coherent_snapshot_revision;
- whether a pending offer/chest exists;
- diagnostic code, если snapshot/content mismatch.

UPGRADE_OFFER и CHEST_OFFER сами замораживают simulation; вход в Settings из них возвращается в тот же blocking state. Android background не считается победой, поражением или выходом из забега.

Working assumption: snapshot делается на checkpoint, при явной паузе и в terminal/reward boundary. Полный произвольный mid-frame resume не обещается до отдельного product decision.

## 6. Terminal states and repeat behavior

- RUN_DEFEAT и RUN_VICTORY terminal для конкретного run_id.
- RESULT_REVIEW можно открывать повторно; это read-only projection.
- REWARD_COMMITTING повторяется только с теми же idempotency keys.
- После committed result старый run нельзя возобновить как active.
- Повторный event для boss defeat, chest claim, checkpoint reward или result claim возвращает уже сохранённый outcome.
- Новый забег всегда получает новый run_id и новый deterministic seed.

## 7. Invariants

1. UI не меняет authoritative state напрямую.
2. Clock не идёт в paused/blocking states.
3. XPDrop не превращается в AftermathItem и наоборот.
4. Checkpoint reward не применяется без ledger idempotency key.
5. Final victory невозможна без final boss defeat.
6. Unknown/stale content не превращается в silent default.
7. Ошибка persistence не подтверждает reward commit.
8. Повторная доставка одного effect command не меняет итог.
9. Все неизвестные числовые/продуктовые решения отмечены в data contract и decisions file.