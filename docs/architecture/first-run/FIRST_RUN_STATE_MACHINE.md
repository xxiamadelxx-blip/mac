# FIRST_RUN_STATE_MACHINE — состояния и переходы первого забега

> Revision 3. State machine is target architecture. Runtime implementation and Godot execution evidence are external.

Source: [data contract](./FIRST_RUN_DATA_CONTRACT.json).

## 1. Ownership model

AppShell owns lifecycle signals and mobile background notifications. RunCoordinator orchestrates transitions. RunSession owns authoritative state. ContentLoader owns immutable versioned data. SimulationClock owns elapsed time policy. BossDirector and WaveCycleDirector own encounter and pressure state. RewardLedger owns persistent rewards.

## 2. State list

BOOT, MAIN_MENU, CHARACTER_SELECT, RUN_SETUP, RUN_LOADING, RUN_ACTIVE, UPGRADE_OFFER, BOSS_INTRO, BOSS_ACTIVE, CHECKPOINT_SETTLEMENT, CHEST_OFFER, RUN_PAUSED, SETTINGS, RECOVERY_REVIEW, RUN_DEFEAT, RUN_VICTORY, RESULT_REVIEW and REWARD_COMMITTING.

BOSS_INTRO and BOSS_ACTIVE carry encounter_kind. For MAIN_BOSS they freeze visible run, wave, XP and ordinary spawn clocks. For MINI_BOSS those clocks continue. The separate encounter clock advances in both variants.

## 3. State graph

BOOT → MAIN_MENU → CHARACTER_SELECT → RUN_SETUP → RUN_LOADING → RUN_ACTIVE.
RUN_ACTIVE may open UPGRADE_OFFER, BOSS_INTRO or RUN_PAUSED. A non-final boss goes through BOSS_ACTIVE → CHECKPOINT_SETTLEMENT → CHEST_OFFER → RUN_ACTIVE. The terminal boss goes through BOSS_ACTIVE → CHECKPOINT_SETTLEMENT → RUN_VICTORY → RESULT_REVIEW. Defeat goes through RUN_DEFEAT → RESULT_REVIEW. Result goes through REWARD_COMMITTING → MAIN_MENU.

## 3.1 Encounter schedule and wave-cycle state

| Order | Time | Seconds | Kind | ID | Outcome |
| --- | --- | --- | --- | --- | --- |
| 1 | 05:00 | 300 | MAIN_BOSS | boss_hua_lin | reward then BOSS_CHEST |
| 2 | 07:30 | 450 | MINI_BOSS | miniboss_ink_jade_warden | reward then BOSS_CHEST |
| 3 | 10:00 | 600 | MAIN_BOSS | boss_miyeon | reward then BOSS_CHEST |
| 4 | 12:30 | 750 | MINI_BOSS | miniboss_veil_harvester | reward then BOSS_CHEST |
| 5 | 15:00 | 900 | MAIN_BOSS | boss_seika | reward then BOSS_CHEST |
| 6 | 17:30 | 1050 | MINI_BOSS | miniboss_lotus_ritekeeper | reward then BOSS_CHEST |
| 7 | 20:00 | 1200 | MAIN_BOSS | boss_tideglass_regent | reward then BOSS_CHEST |
| 8 | 22:30 | 1350 | MINI_BOSS | miniboss_bell_rhythm_ascetic | reward then BOSS_CHEST |
| 9 | 25:00 | 1500 | MAIN_BOSS | boss_omen_paper_archivist | reward then BOSS_CHEST |
| 10 | 27:30 | 1650 | MINI_BOSS | miniboss_moonroot_ferryman | reward then BOSS_CHEST |
| 11 | 30:00 | 1800 | MAIN_BOSS | boss_black_moon_empress | victory after settlement |

Wave cycle is OPENING → RAMP → PRE_BOSS_PEAK. Every non-final defeat enters POST_BOSS_RELIEF before the next RAMP. Exact budgets and caps are B1-owned values.

## 3.2 Clock policy

| State and kind | Visible run clock | Wave/XP/spawn | Encounter clock |
|---|---|---|---|
| BOSS_INTRO MAIN_BOSS | freeze | freeze | advance |
| BOSS_ACTIVE MAIN_BOSS | freeze | freeze | advance |
| BOSS_INTRO MINI_BOSS | advance | advance | advance |
| BOSS_ACTIVE MINI_BOSS | advance | advance | advance |
| offer, pause, settlement, result | freeze | freeze | no tick |

## 4. Transition contract

Every row has trigger, preconditions/guard, owner, side effects, failure path, recovery path and duplicate/idempotency behavior.

| ID | Transition | Trigger | Preconditions / guard | Owner | Side effects | Failure path | Recovery path | Duplicate / idempotency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-01 | BOOT → MAIN_MENU | Boot process completed and shell is available | shell and diagnostics context are available | AppShell | Create menu projection and diagnostics context | Missing shell resource shows recoverable diagnostic | Retry load or open safe error screen | Repeated boot token returns existing menu projection |
| T-02 | MAIN_MENU → CHARACTER_SELECT | Start run command is accepted | menu is loaded and no active setup is open | MenuFlow | Open character registry projection | Invalid command is rejected without session | Return to menu and refresh content | Same command ID is no-op |
| T-03 | CHARACTER_SELECT → RUN_SETUP | Selected hero ID exists in loaded registry | character registry is loaded and selection is not committed | RunSetupModel | Store hero ID and expose setup confirmation | Unknown hero is quarantined | Reload registry or return to selection | Same hero selection replaces only uncommitted selection |
| T-04 | RUN_SETUP → RUN_LOADING | Hero, seed and content version are present | hero, seed and content version are non-null | RunCoordinator | Create run ID and loading request | Missing required field blocks load | Return to setup with diagnostic | Existing run ID cannot be created twice |
| T-05 | RUN_LOADING → RUN_ACTIVE | Arena, schedule and registry map validate | required arena resources and registry map validate | ContentLoader | Create RunSession and start active clocks | Missing resource blocks run start | Safe menu return or retry load | Repeated start of same run ID does not create second session |
| T-06 | RUN_ACTIVE → UPGRADE_OFFER | Authoritative XP crosses level threshold | XP revision is newer than the last level-up revision | ProgressionSystem | Freeze simulation and create one offer revision | Invalid offer pool leaves XP at committed boundary | Rebuild offer from same state revision | Same XP pickup or level event is ignored by idempotency key |
| T-07 | UPGRADE_OFFER → RUN_ACTIVE | Player chooses one valid card | offer is open and chosen card belongs to that offer | BuildInventory | Apply weapon/passive change and resume clocks | Stale or illegal card is rejected | Keep offer open or create diagnostic | Choice ID can commit only once |
| T-08 | RUN_ACTIVE → BOSS_INTRO | Schedule cursor reaches non-final MAIN_BOSS checkpoint | schedule cursor points to a configured non-final main record | EncounterSchedule | Freeze visible clocks and spawn intro telegraph | Missing boss record blocks encounter and records diagnostic | Retry deterministic spawn before advancing cursor | Same checkpoint ID cannot start twice |
| T-09 | BOSS_INTRO → BOSS_ACTIVE | Main intro telegraph and spawn are valid | main telegraph and safe spawn position validate | BossDirector | Create encounter clock and active boss state | Invalid spawn cancels intro safely | Retry safe spawn using same encounter ID | Duplicate intro event returns existing encounter |
| T-10 | RUN_ACTIVE → BOSS_INTRO | Schedule cursor reaches MINI_BOSS checkpoint | schedule cursor points to a configured mini record | EncounterSchedule | Keep visible clocks and ordinary spawn advancing; open mini intro | Missing mini record blocks encounter and records diagnostic | Retry deterministic spawn before cursor advance | Same mini checkpoint ID cannot start twice |
| T-11 | BOSS_INTRO → BOSS_ACTIVE | Mini intro telegraph and spawn are valid | mini telegraph and safe spawn position validate | BossDirector | Create mini encounter clock and active state | Invalid spawn cancels intro safely | Retry safe spawn using same encounter ID | Duplicate intro event returns existing encounter |
| T-12 | BOSS_ACTIVE → CHECKPOINT_SETTLEMENT | Non-final MAIN_BOSS authoritative HP reaches zero | active encounter is a non-final main record | BossDirector + RunCoordinator | Close encounter, freeze main visible clocks, create settlement | Duplicate or malformed defeat is rejected | Restore active encounter or recovery review | Defeat key and checkpoint ID commit once |
| T-13 | BOSS_ACTIVE → CHECKPOINT_SETTLEMENT | MINI_BOSS authoritative HP reaches zero | active encounter is a mini record | BossDirector + RunCoordinator | Close mini encounter while visible clocks continue, create settlement | Malformed defeat is rejected | Restore active encounter or recovery review | Defeat key and checkpoint ID commit once |
| T-14 | CHECKPOINT_SETTLEMENT → CHEST_OFFER | Non-final main reward ledger commit succeeds | settlement belongs to a non-final main checkpoint | RewardLedger + ChestWindowSystem | Commit reward and open matching BOSS_CHEST | Ledger failure leaves settlement recoverable | Retry ledger with same key | Committed checkpoint cannot open second window |
| T-15 | CHECKPOINT_SETTLEMENT → CHEST_OFFER | Mini reward ledger commit succeeds | settlement belongs to a mini checkpoint | RewardLedger + ChestWindowSystem | Commit reward and open matching BOSS_CHEST | Ledger failure leaves settlement recoverable | Retry ledger with same key | Committed checkpoint cannot open second window |
| T-16 | CHECKPOINT_SETTLEMENT → RUN_VICTORY | Terminal boss defeat and final settlement are committed | settlement belongs to the terminal record and no chest source is attached | RunCoordinator + RewardLedger | Create victory result boundary with no chest | Missing final settlement blocks victory | Recover settlement and retry commit | Terminal checkpoint key commits once |
| T-17 | CHEST_OFFER → RUN_ACTIVE | Non-final BOSS_CHEST claim resolves | offer belongs to a configured non-final window | ChestResolver | Apply synergy/evolution or fallback and advance stage | Unknown outcome stays pending and no reward is granted | Reopen same offer or recovery review | Chest offer ID and claim key are idempotent |
| T-18 | RUN_ACTIVE → RUN_PAUSED | User pause command is accepted | run is resumable and no offer transaction is mid-commit | RunSession | Freeze simulation and request safe snapshot | Snapshot failure leaves pause UI with diagnostic | Retry save or offer recovery choice | Same pause command returns existing pause revision |
| T-19 | RUN_PAUSED → RUN_ACTIVE | Continue command and snapshot validation pass | snapshot checksum, schema and content versions validate | RunSession + SaveSnapshot | Restore state revision and resume allowed clocks | Checksum or version failure goes to recovery | Open RECOVERY_REVIEW | Same resume token cannot double-resume |
| T-20 | RUN_PAUSED → SETTINGS | Settings command is accepted | run remains paused and settings projection is available | PauseShell | Open settings without mutating RunSession | Settings resource failure returns to pause | Retry settings load | Repeated open is read-only |
| T-21 | SETTINGS → RUN_PAUSED | Back or close settings command | settings projection is open and run snapshot is retained | PauseShell | Restore pause projection | Projection failure keeps safe pause | Recreate projection from snapshot | Close command is no-op when already paused |
| T-22 | RUN_PAUSED → MAIN_MENU | Exit confirmation is accepted | pause state exists and explicit exit confirmation is true | RunCoordinator | Commit abandon marker or recoverable snapshot per policy | Save/abandon failure keeps run in recovery | Retry commit or reopen pause | Same exit command cannot grant rewards |
| T-23 | RUN_ACTIVE → RUN_PAUSED | Android background notification or OS pause | run is active and OS lifecycle signal is authoritative | AppShell + RunSession | Freeze clocks and persist last safe snapshot | Snapshot failure marks recovery required | Resume from last valid revision or abandon | Repeated background signal does not create snapshots per frame |
| T-24 | RUN_PAUSED → RECOVERY_REVIEW | Foreground detects invalid, missing or stale snapshot | foreground signal exists and snapshot validation failed | SaveSnapshot + RunCoordinator | Show recovery choices and block simulation | Recovery metadata failure keeps safe error state | Use last valid snapshot or explicit abandon | Same snapshot revision is evaluated once |
| T-25 | RECOVERY_REVIEW → RUN_ACTIVE | User chooses valid last snapshot and checks pass | selected snapshot matches run ID and ledger revision | SaveSnapshot + RunSession | Restore without time jump and resume allowed clocks | Restore conflict returns to recovery | Choose another valid snapshot or abandon | Restore token and state revision are idempotent |
| T-26 | RECOVERY_REVIEW → MAIN_MENU | User abandons unrecoverable run | user explicitly selected abandon | RunCoordinator | Record abandon without unearned reward | Abandon write failure remains recoverable | Retry write or retain recovery screen | Abandon key commits once |
| T-27 | RUN_ACTIVE → RUN_DEFEAT | Authoritative player HP reaches zero | run is active and death boundary is not committed | CombatSystem + RunCoordinator | Freeze run and create defeat settlement input | Duplicate death or invalid HP source is rejected | Restore last safe active state or settle once | Death event key is idempotent |
| T-28 | RUN_DEFEAT → RESULT_REVIEW | Defeat result projection is complete | defeat settlement input is committed | ResultBuilder | Create partial result read model | Missing stats leaves result recoverable | Rebuild from RunSession snapshot | Result ID cannot be created twice |
| T-29 | RUN_VICTORY → RESULT_REVIEW | Victory settlement is complete | victory settlement and final ledger entry are committed | ResultBuilder | Create full result read model | Missing final stats blocks result claim | Rebuild from committed ledger | Victory result ID is idempotent |
| T-30 | RESULT_REVIEW → REWARD_COMMITTING | Player claims result rewards | result is immutable and claim has not committed | RewardLedger | Validate immutable result and prepare commit | Validation failure keeps read-only result | Retry claim with same key | Result claim key prevents duplicate wallet mutation |
| T-31 | REWARD_COMMITTING → MAIN_MENU | Ledger commit and save revision succeed | ledger transaction is prepared and save revision is writable | RewardLedger + MenuFlow | Persist wallet/unlocks and return menu | Save failure keeps committed result recoverable | Retry persistence without recalculation | Committed ledger entry is never applied twice |
| T-32 | MAIN_MENU → RUN_LOADING | Player starts a fresh run after result or abandon | previous session is closed or explicitly abandoned | MenuFlow + RunCoordinator | Allocate fresh run ID and seed | Old session reference blocks start | Clear stale projection and retry | Fresh run never reuses prior run ID |
| T-33 | CHEST_OFFER → RECOVERY_REVIEW | Chest offer load or claim fails validation | offer is open and source kind is valid | ChestWindowSystem + RunCoordinator | Freeze offer and persist diagnostic | Diagnostic persistence failure keeps safe pause | Retry same offer or recover snapshot | Offer ID and state revision prevent duplicate aftermath |

## 5. Pause, background and restore

Android background is equivalent to a pause request at a safe boundary. It does not advance elapsed clocks while paused and cannot grant rewards. SaveSnapshot stores content version, schema version 3, run ID, state revision, ledger revision, schedule cursor, encounter kind and checksum. Foreground resumes only a valid snapshot. Otherwise RECOVERY_REVIEW offers restore or abandon.

## 6. Terminal behavior

The final encounter is boss_black_moon_empress at 1800 seconds. It has no chest window. Victory requires authoritative defeat and final ledger settlement. A timer tick alone cannot produce victory. First-clear artifact offer is post-result and separate.

## 7. Invariants

- One RunSession and one authoritative reward boundary per run.
- XP pickup, aftermath, chest claim, artifact choice and result claim each have separate idempotency keys.
- No transition may invent a missing registry record or B1 number.
- State revision increments once per committed transition.
