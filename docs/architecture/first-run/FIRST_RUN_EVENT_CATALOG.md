# FIRST_RUN_EVENT_CATALOG — события и команды первого забега

Статус: VERIFIED ARCHITECTURE SPECIFICATION

> Revision 2: event catalog now includes schedule slots, wave relief/ramp phases, enemy variants and generic chest windows. Runtime implemented: NO.
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

The game clock advances in RUN_ACTIVE, BOSS_INTRO and BOSS_ACTIVE for every boss. It freezes in UPGRADE_OFFER, CHEST_OFFER, ARTIFACT_OFFER, RUN_PAUSED, CHECKPOINT_SETTLEMENT and terminal/transaction states; BOSS_INTRO is not a pause boundary.

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
| run_start_requested.v1 | COMMAND | MenuFlow | RunCoordinator | character_id, client_request_id | after setup validation; no artifact is selected before the run | idempotent by client_request_id before RunSession creation | diagnostics |
| run_created.v1 | DOMAIN_EVENT | RunCoordinator | Persistence, Simulation, HUD | run_id, seed, content_version, selected_hero_id | before arena ready | duplicate returns same run_id | snapshot boundary |
| arena_ready.v1 | DOMAIN_EVENT | Arena adapter | RunCoordinator, HUD | run_id, required_resource_status | after run_created | duplicate no-op | diagnostics |
| wave_band_changed.v1 | DOMAIN_EVENT | WaveDirector | HUD, Spawner, Diagnostics | wave_band_id, from_seconds, to_seconds, multipliers_ref | monotonic elapsed boundary | same band/checkpoint ignored | run metrics |
| level_up.v1 | DOMAIN_EVENT | ProgressionSystem | OfferGenerator, HUD, Persistence | level, xp_total, offer_sequence | after XP commit | duplicate by state_revision ignored | run metrics |
| upgrade_offer_created.v1 | DOMAIN_EVENT | OfferGenerator | Upgrade UI, RunSession | offer_id, three offer records, expires_policy | after level_up | same offer_id reused | snapshot if policy requires |
| offer_chosen.v1 | COMMAND | Upgrade UI | RunCoordinator/BuildInventory | offer_id, choice_id, state_revision | while UPGRADE_OFFER | duplicate returns chosen outcome | run metrics |
| upgrade_applied.v1 | DOMAIN_EVENT | BuildInventory | Stats, HUD, Persistence | content_id, old_level, new_level, modifiers_ref | after valid choice | keyed by offer_id | snapshot at boundary |
| synergy_eligibility_evaluated.v1 | DOMAIN_EVENT | SynergyEvaluator | Boss Chest UI, RunSession | chest_offer_id, outcome, synergy_id | after non-final boss-chest context | same inputs produce same outcome | diagnostics/metrics |
| synergy_claimed.v1 | COMMAND | Boss Chest UI | RunCoordinator/BuildInventory | chest_offer_id, synergy_id, state_revision | after eligible result | idempotent by chest_offer_id | snapshot/metrics |
| first_clear_artifact_offer_requested.v1 | COMMAND | Result UI | ArtifactOfferSystem | run_id, result_id, idempotency_key | after result_finalized and first-clear eligibility | idempotent by result_id | pending transaction/metrics |
| artifact_offer_created.v1 | DOMAIN_EVENT | ArtifactOfferSystem | Artifact Offer UI, RunSession | artifact_offer_id, source_kind, source_id, choice_artifact_ids[3], offer_seed | after elite pack or first-clear reward boundary | same offer_id reused | snapshot/metrics |
| artifact_offer_refresh_requested.v1 | COMMAND | Artifact Offer UI | ArtifactOfferSystem | artifact_offer_id, state_revision, idempotency_key | while ARTIFACT_OFFER and refresh policy allows | duplicate returns existing refresh outcome | pending transaction/metrics |
| artifact_offer_refreshed.v1 | DOMAIN_EVENT | ArtifactOfferSystem | Artifact Offer UI, RunSession | artifact_offer_id, choice_artifact_ids[3], refresh_count | after valid refresh | keyed by artifact_offer_id + idempotency key | snapshot/metrics |
| artifact_chosen.v1 | COMMAND | Artifact Offer UI | RunCoordinator/ArtifactEffectSystem | artifact_offer_id, artifact_id, state_revision, idempotency_key | while ARTIFACT_OFFER | duplicate returns chosen outcome | snapshot/metrics |
| artifact_obtained.v1 | DOMAIN_EVENT | ArtifactEffectSystem | RunSession, HUD, Persistence | artifact_offer_id, artifact_instance_id, artifact_id, source_kind, effect_contract_ref | after valid artifact choice | duplicate choice returns same instance | snapshot/metrics |
| elite_pack_defeated.v1 | DOMAIN_EVENT | Combat/ElitePackDirector | ArtifactOfferSystem, HUD | elite_pack_id, encounter_id, stage_id | after authoritative elite-pack defeat | encounter ID dedupe | run metrics |
| boss_chest_outcome_applied.v1 | DOMAIN_EVENT | BossChestSystem | BuildInventory, SynergyEvaluator, RunSession, HUD | chest_offer_id, outcome_id, outcome_type | after valid boss-chest claim | duplicate claim returns same outcome | snapshot/metrics |
| checkpoint_reached.v1 | DOMAIN_EVENT | SimulationClock/WaveDirector | BossDirector, HUD | checkpoint_id, elapsed_seconds | once per checkpoint | keyed by checkpoint_id | run metrics |
| boss_spawned.v1 | DOMAIN_EVENT | BossDirector | Combat, HUD, WaveDirector | boss_encounter_id, boss_id, checkpoint_id, safe_spawn_ref | after checkpoint | encounter ID dedupe | run metrics |
| boss_defeated.v1 | DOMAIN_EVENT | Combat/BossDirector | RunCoordinator, RewardBoundary | boss_encounter_id, boss_id, checkpoint_id, stats_ref | after authoritative defeat | encounter ID dedupe | snapshot/metrics |
| checkpoint_reward_requested.v1 | COMMAND | RunCoordinator | RewardCalculator/Ledger | run_id, checkpoint_id, reward_bundle_id, idempotency_key | after boss_defeated | ledger key dedupe | pending transaction |
| checkpoint_reward_committed.v1 | DOMAIN_EVENT | RewardLedger | MetaProgression, HUD, Result | ledger_entry_ids, wallet_revision, bundle_id | after atomic commit | existing commit returned | durable ledger + metrics |
| final_settlement_committed.v1 | DOMAIN_EVENT | RewardLedger | RunCoordinator, ResultProjection | run_id, final_boss_id, checkpoint_id, ledger_entry_ids, wallet_revision | after final checkpoint reward commit and before RUN_VICTORY | final checkpoint ledger key returns existing settlement | durable ledger + metrics |
| boss_chest_opened.v1 | DOMAIN_EVENT | BossChestSystem | SynergyEvaluator, Boss Chest UI | chest_offer_id, checkpoint_id, offer_seed | after non-final checkpoint reward commit | same offer remains open | snapshot |
| boss_chest_claimed.v1 | COMMAND | Boss Chest UI | BossChestSystem, BuildInventory, Ledger if needed | chest_offer_id, outcome_id, state_revision | while CHEST_OFFER for non-final checkpoint | idempotent by chest_offer_id | snapshot/metrics |
| stage_advanced.v1 | DOMAIN_EVENT | RunCoordinator | WaveDirector, HUD, Persistence | from_stage_id, to_stage_id, checkpoint_id | after non-final boss-chest claim/settlement | same checkpoint no-op | snapshot |
| xp_drop_spawned.v1 | DOMAIN_EVENT | Combat/DropSystem | XpDropStore, HUD | xp_item_id, grade_id, value, source_enemy_id | after enemy death | unique drop id | run metrics |
| xp_drop_collected.v1 | COMMAND | Magnet/Input adapter | ProgressionSystem, XpDropStore | xp_item_id, run_id, collection_context | once per drop | collected flag makes duplicate no-op | metrics |
| aftermath_spawned.v1 | DOMAIN_EVENT | Combat/AftermathSystem | AftermathStore, renderer | aftermath_item_id, enemy_id, kind, aggregation_tier | after death, separate from XP | unique aftermath id | density metrics |
| run_paused.v1 | DOMAIN_EVENT | RunCoordinator | Clock, HUD, Persistence | run_id, pause_reason, paused_from_state, snapshot_revision | before any resume | same pause revision no-op | snapshot/diagnostics |
| run_resumed.v1 | DOMAIN_EVENT | Recovery/PauseFlow | Clock, HUD, Simulation | run_id, restored_revision, resume_state | after validation | duplicate resume no-op | diagnostics |
| save_written.v1 | DOMAIN_EVENT | PersistenceGateway | Recovery, Diagnostics | snapshot_id, revision, checksum, reason | after atomic promotion | same revision no-op | durable metadata |
| save_restore_failed.v1 | DOMAIN_EVENT | PersistenceGateway | RecoveryReview, Diagnostics | snapshot_id, code, recovery_options | before active resume | retry migration/read only | diagnostic |
| run_defeated.v1 | DOMAIN_EVENT | Combat/RunCoordinator | RewardCalculator, ResultProjection | run_id, reason, stats_ref, checkpoint_id | once terminal | run terminal dedupe | terminal snapshot |
| run_victory.v1 | DOMAIN_EVENT | RunCoordinator | RewardCalculator, ResultProjection | run_id, final_boss_id, final_checkpoint_id, stats_ref | after final_settlement_committed; no boss chest required | final checkpoint/result key returns existing victory | terminal snapshot |
| result_finalized.v1 | DOMAIN_EVENT | RewardBoundary | ResultProjection, MenuFlow | run_id, result_id, ledger_entries, wallet_revision | after reward commit | result idempotency key | durable result |
| return_to_menu.v1 | COMMAND | Result/Pause UI | MenuFlow | run_id, return_reason | after commit/abandon | duplicate navigation no-op | optional telemetry |
## 3.1 Extension event additions

The existing boss_* events remain valid for a scheduled encounter. These events add the registry-level trace for the 30-minute/cycle/chest extension:

| Name/version | Kind | Producer | Consumers | Required payload | Ordering/causality | Retry/duplicate | Persistence/telemetry |
|---|---|---|---|---|---|---|---|
| encounter_schedule_slot_reached.v1 | DOMAIN_EVENT | SimulationClock/WaveDirector | BossDirector, WaveCycleDirector, HUD | schedule_index, encounter_id, encounter_kind, checkpoint_id, is_final, target_boundary_ref | before boss_spawned.v1 | schedule index + checkpoint ID dedupe | run snapshot/metrics |
| wave_cycle_started.v1 | DOMAIN_EVENT | WaveCycleDirector | WaveDirector, Spawner, HUD | wave_cycle_id, from_encounter_id, phase_id, phase_revision | after run start or non-final chest claim | same cycle/revision no-op | snapshot/pressure telemetry |
| wave_phase_changed.v1 | DOMAIN_EVENT | WaveCycleDirector | Spawner, HUD, Diagnostics | wave_cycle_id, from_phase_id, to_phase_id, profile_ref, state_revision | monotonic phase transition | same target phase/revision no-op | wave metrics |
| enemy_variant_selected.v1 | DOMAIN_EVENT | EnemyVariantResolver | Spawner, Combat, ResultProjection, Telemetry | base_enemy_id, variant_id, wave_cycle_id, selection_revision, balance_profile_ref | before enemy entity spawn | same selection key returns same variant | spawn/variant metrics |
| chest_window_triggered.v1 | DOMAIN_EVENT | ChestWindowRegistry/RunCoordinator | ChestResolver, HUD | chest_window_id, source_kind, source_id, checkpoint_id, eligibility_ref | after authoritative source trigger | window ID prevents second offer | snapshot/metrics |
| chest_offer_created.v1 | DOMAIN_EVENT | ChestResolver | Chest UI, RunSession, Persistence | chest_offer_id, chest_window_id, source_kind, source_id, outcome_policy_ref | after window validation | same window/source returns existing offer | snapshot/metrics |
| chest_claimed.v1 | COMMAND | Chest UI | RunCoordinator/ChestResolver | chest_offer_id, chest_window_id, outcome_id, state_revision, idempotency_key | while CHEST_OFFER | same offer returns stored outcome | snapshot/metrics |
| chest_outcome_applied.v1 | DOMAIN_EVENT | ChestResolver/BossChestSystem | BuildInventory, SynergyEvaluator, RewardLedger, HUD | chest_offer_id, source_kind, outcome_type, outcome_id, ledger_entry_ids | after valid claim | offer ID + outcome key dedupe | snapshot/metrics |
| post_boss_relief_started.v1 | DOMAIN_EVENT | WaveCycleDirector | WaveDirector, HUD, PerformanceTelemetry | from_encounter_id, next_wave_cycle_id, relief_profile_ref, state_revision | after non-final settlement/claim | same source encounter no-op | wave/performance metrics |

boss_chest_opened.v1 and boss_chest_claimed.v1 remain source-specific projections for a BOSS_CHEST offer. They must carry chest_window_id; they do not apply to reserved non-boss windows or the final boss.


## 4. Payload and failure rules by critical event

### run_created

Must contain run_id, seed, content_version, schema_version, selected_hero_id and initial state. If persistence cannot record a coherent initial session, the command fails before arena start.

### level_up and offer_chosen

Offer IDs are deterministic within a content version and run seed. The chosen offer must belong to the current open offer and expected state revision. Applying a choice updates build/stats exactly once.

### boss_defeated and checkpoint_reward_committed

boss_defeated is a domain fact, not a wallet mutation. The reward command uses checkpoint-specific idempotency. Ledger commit must be atomic with wallet revision; a crash before commit leaves a retryable pending transaction.

### boss_chest_opened and boss_chest_claimed

These events belong only to the non-final boss chest. The offer remains stable across close/reopen/recovery. Eligibility may produce fallback_required, but exact fallback value is not invented by this architecture. The final boss has no boss-chest offer. Claiming the same boss chest twice returns the stored synergy/evolution/fallback outcome.

### artifact_offer_created, artifact_offer_refresh_requested, artifact_chosen

Artifacts are not a pre-run loadout and do not use weapon/passive slots. An elite pack may open an `ARTIFACT_OFFER`; the first-clear reward opens a separate post-result offer. Each offer exposes exactly three artifact cards. `Get` accepts one card and creates one active run effect; `Refresh` rerolls the three cards only when the separately pending refresh policy permits it. Exact cost, limit, duplicate/stacking behavior, elite-pack cadence and effect values remain pending. A boss chest never becomes an artifact offer.

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
4. duplicate boss_chest_claimed does not double boss-chest synergy/evolution/fallback;
5. duplicate artifact_chosen does not create a second artifact instance or effect;
6. duplicate artifact_offer_refresh_requested does not charge or reroll twice;
7. duplicate result claim does not double first-clear/repeat rewards;
8. stale state_revision is rejected;
9. corrupted/old snapshot enters recovery without silent data loss.
10. The same schedule revision selects the same enemy variant and cannot double-spawn a variant-bound reward.
11. A configured chest window creates at most one offer; 15-window capacity never implies more than one outcome per window.
12. Post-boss relief is observable before the next ramp; no direct post-boss jump to a peak profile is accepted without an explicit B1 rule.
