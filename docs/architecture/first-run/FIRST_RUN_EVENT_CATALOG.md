# FIRST_RUN_EVENT_CATALOG — события и команды первого забега

Статус: DRAFT ARCHITECTURE SPECIFICATION
Runtime implemented: NO

## 1. Event contract

Every command/domain event uses the envelope shape in [FIRST_RUN_DATA_CONTRACT.json](./FIRST_RUN_DATA_CONTRACT.json):

- event_id — immutable identifier for the emitted message;
- event_name and event_version — stable semantic name plus schema version;
- event_kind — COMMAND, DOMAIN_EVENT or UI_PROJECTION;
- occurred_at — wall-clock metadata for diagnostics only;
- run_id — nullable for boot/menu events;
- state_revision — monotonic RunSession revision when a run exists;
- correlation_id — links one user intent to derived events;
- idempotency_key — required for repeatable effects;
- payload — typed data, never a UI node reference.

RunSession state is authoritative. Events are not a hidden second database. Persist only what is required for recovery, ledger replay protection and diagnostics.

## 2. Ordering and duplicate policy

1. A command enters through MenuFlow, PauseFlow or input adapter.
2. RunCoordinator validates current state, content version and expected state_revision.
3. Domain owner applies the transition.
4. State revision increments.
5. Domain event is emitted.
6. Projection builders derive UI read models.
7. PersistenceGateway snapshots only at an allowed boundary.
8. Reward events are emitted after the atomic ledger/wallet commit.

For commands with side effects, the idempotency key is checked before mutation. A duplicate returns the existing outcome. A stale state_revision is rejected as STALE_COMMAND and never replayed against newer state.

## 3. Event catalog

| Name/version | Kind | Producer | Consumers | Required payload | Ordering/causality | Retry/duplicate | Persistence/telemetry |
|---|---|---|---|---|---|---|---|
| app_boot.v1 | COMMAND | AppShell | ContentLoader | app_version, device_context | first app command | new attempt only | diagnostics |
| content_load_requested.v1 | COMMAND | AppShell | ContentLoader | content_version, save_schema_version | after boot | safe to retry | diagnostics |
| content_loaded.v1 | DOMAIN_EVENT | ContentLoader | AppShell, MenuFlow, RunCoordinator | content_version, registry_hash | before menu/run | duplicate replaces same load attempt | load telemetry |
| content_load_failed.v1 | DOMAIN_EVENT | ContentLoader | AppShell, Diagnostics | code, path, required, recovery_action | terminal for attempt | retry with new attempt id | diagnostic |
| menu_opened.v1 | UI_PROJECTION | MenuFlow | UI | wallets, unlocks, diagnostic_badges | after content_loaded | projection can rebuild | no durable state |
| settings_opened.v1 | UI_PROJECTION | SettingsFlow | UI | settings_projection | from menu/pause | rebuild | no durable state |
| character_select_requested.v1 | COMMAND | MenuFlow | RunCoordinator | character_id | in CHARACTER_SELECT | duplicate no-op | optional navigation telemetry |
| character_selected.v1 | DOMAIN_EVENT | RunCoordinator | RunSetup, MenuFlow | character_id, content_version | before run creation | same selection no-op | active setup only |
| run_start_requested.v1 | COMMAND | MenuFlow | RunCoordinator | character_id, artifact_ids, client_request_id | after setup validation | idempotent by client_request_id before RunSession creation | diagnostics |
| run_created.v1 | DOMAIN_EVENT | RunCoordinator | Persistence, Simulation, HUD | run_id, seed, content_version, selected_hero_id | before arena ready | duplicate returns same run_id | snapshot boundary |
| arena_ready.v1 | DOMAIN_EVENT | Arena adapter | RunCoordinator, HUD | run_id, required_resource_status | after run_created | duplicate no-op | diagnostics |
| wave_band_changed.v1 | DOMAIN_EVENT | WaveDirector | HUD, Spawner, Diagnostics | wave_band_id, from_seconds, to_seconds, multipliers_ref | monotonic elapsed boundary | same band/checkpoint ignored | run metrics |
| level_up.v1 | DOMAIN_EVENT | ProgressionSystem | OfferGenerator, HUD, Persistence | level, xp_total, offer_sequence | after XP commit | duplicate by state_revision ignored | run metrics |
| upgrade_offer_created.v1 | DOMAIN_EVENT | OfferGenerator | Upgrade UI, RunSession | offer_id, three offer records, expires_policy | after level_up | same offer_id reused | snapshot if policy requires |
| offer_chosen.v1 | COMMAND | Upgrade UI | RunCoordinator/BuildInventory | offer_id, choice_id, state_revision | while UPGRADE_OFFER | duplicate returns chosen outcome | run metrics |
| upgrade_applied.v1 | DOMAIN_EVENT | BuildInventory | Stats, HUD, Persistence | content_id, old_level, new_level, modifiers_ref | after valid choice | keyed by offer_id | snapshot at boundary |
| synergy_eligibility_evaluated.v1 | DOMAIN_EVENT | SynergyEvaluator | Chest UI, RunSession | chest_offer_id, outcome, synergy_id | after boss/chest context | same inputs produce same outcome | diagnostics/metrics |
| synergy_claimed.v1 | COMMAND | Chest UI | RunCoordinator/BuildInventory | chest_offer_id, synergy_id, state_revision | after eligible result | idempotent by chest_offer_id | snapshot/metrics |
| artifact_obtained.v1 | DOMAIN_EVENT | ChestSystem | RunSession, HUD, Persistence | chest_offer_id, artifact_id | after valid claim | duplicate claim returns same artifact | snapshot/metrics |
| checkpoint_reached.v1 | DOMAIN_EVENT | SimulationClock/WaveDirector | BossDirector, HUD | checkpoint_id, elapsed_seconds | once per checkpoint | keyed by checkpoint_id | run metrics |
| boss_spawned.v1 | DOMAIN_EVENT | BossDirector | Combat, HUD, WaveDirector | boss_encounter_id, boss_id, checkpoint_id, safe_spawn_ref | after checkpoint | encounter ID dedupe | run metrics |
| boss_defeated.v1 | DOMAIN_EVENT | Combat/BossDirector | RunCoordinator, RewardBoundary | boss_encounter_id, boss_id, checkpoint_id, stats_ref | after authoritative defeat | encounter ID dedupe | snapshot/metrics |
| checkpoint_reward_requested.v1 | COMMAND | RunCoordinator | RewardCalculator/Ledger | run_id, checkpoint_id, reward_bundle_id, idempotency_key | after boss_defeated | ledger key dedupe | pending transaction |
| checkpoint_reward_committed.v1 | DOMAIN_EVENT | RewardLedger | MetaProgression, HUD, Result | ledger_entry_ids, wallet_revision, bundle_id | after atomic commit | existing commit returned | durable ledger + metrics |
| chest_opened.v1 | DOMAIN_EVENT | ChestSystem | SynergyEvaluator, Chest UI | chest_offer_id, checkpoint_id, offer_seed | after reward commit | same offer remains open | snapshot |
| chest_claimed.v1 | COMMAND | Chest UI | ChestSystem, BuildInventory, Ledger if needed | chest_offer_id, outcome_id, state_revision | while CHEST_OFFER | idempotent by chest_offer_id | snapshot/metrics |
| stage_advanced.v1 | DOMAIN_EVENT | RunCoordinator | WaveDirector, HUD, Persistence | from_stage_id, to_stage_id, checkpoint_id | after chest/settlement | same checkpoint no-op | snapshot |
| xp_drop_spawned.v1 | DOMAIN_EVENT | Combat/DropSystem | XpDropStore, HUD | xp_item_id, grade_id, value, source_enemy_id | after enemy death | unique drop id | run metrics |
| xp_drop_collected.v1 | COMMAND | Magnet/Input adapter | ProgressionSystem, XpDropStore | xp_item_id, run_id, collection_context | once per drop | collected flag makes duplicate no-op | metrics |
| aftermath_spawned.v1 | DOMAIN_EVENT | Combat/AftermathSystem | AftermathStore, renderer | aftermath_item_id, enemy_id, kind, aggregation_tier | after death, separate from XP | unique aftermath id | density metrics |
| run_paused.v1 | DOMAIN_EVENT | RunCoordinator | Clock, HUD, Persistence | run_id, pause_reason, paused_from_state, snapshot_revision | before any resume | same pause revision no-op | snapshot/diagnostics |
| run_resumed.v1 | DOMAIN_EVENT | Recovery/PauseFlow | Clock, HUD, Simulation | run_id, restored_revision, resume_state | after validation | duplicate resume no-op | diagnostics |
| save_written.v1 | DOMAIN_EVENT | PersistenceGateway | Recovery, Diagnostics | snapshot_id, revision, checksum, reason | after atomic promotion | same revision no-op | durable metadata |
| save_restore_failed.v1 | DOMAIN_EVENT | PersistenceGateway | RecoveryReview, Diagnostics | snapshot_id, code, recovery_options | before active resume | retry migration/read only | diagnostic |
| run_defeated.v1 | DOMAIN_EVENT | Combat/RunCoordinator | RewardCalculator, ResultProjection | run_id, reason, stats_ref, checkpoint_id | once terminal | run terminal dedupe | terminal snapshot |
| run_victory.v1 | DOMAIN_EVENT | BossDirector/RunCoordinator | RewardCalculator, ResultProjection | run_id, final_boss_id, final_checkpoint_id, stats_ref | after final boss defeat only | final encounter dedupe | terminal snapshot |
| result_finalized.v1 | DOMAIN_EVENT | RewardBoundary | ResultProjection, MenuFlow | run_id, result_id, ledger_entries, wallet_revision | after reward commit | result idempotency key | durable result |
| return_to_menu.v1 | COMMAND | Result/Pause UI | MenuFlow | run_id, return_reason | after commit/abandon | duplicate navigation no-op | optional telemetry |

## 4. Payload and failure rules by critical event

### run_created

Must contain run_id, seed, content_version, schema_version, selected_hero_id and initial state. If persistence cannot record a coherent initial session, the command fails before arena start.

### level_up and offer_chosen

Offer IDs are deterministic within a content version and run seed. The chosen offer must belong to the current open offer and expected state revision. Applying a choice updates build/stats exactly once.

### boss_defeated and checkpoint_reward_committed

boss_defeated is a domain fact, not a wallet mutation. The reward command uses checkpoint-specific idempotency. Ledger commit must be atomic with wallet revision; a crash before commit leaves a retryable pending transaction.

### chest_opened and chest_claimed

The open offer remains stable across close/reopen/recovery. Eligibility may produce fallback_required, but exact fallback value is not invented by this architecture. Claiming the same chest twice returns the stored outcome.

### run_defeated and run_victory

Only one terminal event is accepted for a run_id. Result projection is immutable after finalization except for diagnostic metadata. Reward claim is a separate idempotent boundary.

### run_paused and run_resumed

Pause freezes simulation before snapshot. Resume validates schema, checksum, content version, state revision and ledger cursor. Invalid restore enters RECOVERY_REVIEW and does not generate rewards.

## 5. Event classes and ownership

- Commands express intent and can be rejected.
- Domain events express accepted state changes and are emitted by the owning subsystem.
- UI projections are disposable derived views and never become persistence truth.
- Telemetry can consume events but cannot mutate RunSession or the ledger.
- Persistence events report committed snapshots; they do not prove Android acceptance.

## 6. Required verification

The next runtime slice must prove:

1. duplicate xp_drop_collected does not double XP;
2. duplicate offer_chosen does not double-upgrade;
3. duplicate boss_defeated/checkpoint_reward_requested does not double wallet;
4. duplicate chest_claimed does not double artifact/evolution;
5. duplicate result claim does not double first-clear/repeat rewards;
6. stale state_revision is rejected;
7. corrupted/old snapshot enters recovery without silent data loss.