# FIRST_RUN_EVENT_CATALOG — события и команды первого забега

> Revision 3. Events are a versioned transport and diagnostics contract. RunSession and RewardLedger remain authoritative.

Sources: [state machine](./FIRST_RUN_STATE_MACHINE.md) and [data contract](./FIRST_RUN_DATA_CONTRACT.json).

## 1. Event contract

Every event envelope has event ID, name/version, run ID, state revision, correlation ID, idempotency key, occurred time and payload. Extension payloads include encounter kind, encounter ID, checkpoint seconds, registry map reference, variant class, chest source kind and separate encounter-clock value when applicable.

## 2. Event catalog

| Event | Producer | Consumers | Payload | Ordering | Retry / duplicate policy |
| --- | --- | --- | --- | --- | --- |
| run_created.v1 | RunCoordinator | SaveSnapshot, UI | run_id, seed, hero_id, content_version, state_revision | after content_loaded | same run ID returns existing record |
| content_loaded.v1 | ContentLoader | RunCoordinator, diagnostics | schema_version, content_version, registry_map_ref, required_ids | before run_created | duplicate load is read-only |
| run_started.v1 | RunCoordinator | RunSession, UI | run_id, schedule_cursor, encounter_kind:null | after run_created | start key prevents second session |
| wave_phase_changed.v1 | WaveCycleDirector | HUD, diagnostics | wave_cycle_id, phase_id, boundary, state_revision | ordered by schedule clock | same boundary is no-op |
| xp_collected.v1 | ProgressionSystem | RunSession, HUD | xp_item_id, value, source_enemy_id, state_revision | after authoritative pickup | item ID prevents duplicate XP |
| level_up.v1 | ProgressionSystem | OfferSystem, HUD | run_id, new_level, offer_revision | after XP commit | level revision prevents duplicate offer |
| upgrade_offer_created.v1 | OfferSystem | Upgrade UI, RunSession | offer_id, three cards, state_revision | after level_up | same offer ID is read-only |
| upgrade_chosen.v1 | BuildInventory | RunSession, HUD | offer_id, chosen_content_id, slot_kind, new_rank | after valid choice | choice key commits once |
| checkpoint_reached.v1 | EncounterSchedule | BossDirector, WaveCycleDirector | schedule_index, checkpoint_id, encounter_kind, encounter_id, checkpoint_seconds, is_final | ordered by encounter schedule | same checkpoint is ignored |
| boss_intro_started.v1 | BossDirector | HUD, CombatSystem | boss_encounter_id, encounter_kind, telegraph_ref, encounter_clock_start | after checkpoint_reached | encounter ID prevents duplicate intro |
| boss_defeated.v1 | BossDirector | RunCoordinator, RewardLedger | boss_encounter_id, encounter_kind, checkpoint_id, defeat_revision | after authoritative HP-zero | defeat key commits once |
| checkpoint_reward_committed.v1 | RewardLedger | RunSession, HUD | checkpoint_id, reward_bundle_ref, ledger_entry_id, idempotency_key | after boss_defeated | ledger entry is replay-safe |
| boss_chest_opened.v1 | ChestWindowSystem | Chest UI, RunSession | chest_window_id, source_kind:BOSS_CHEST, source_id, offer_id | after settlement | one window opens once |
| boss_chest_claimed.v1 | ChestResolver | BuildInventory, RewardLedger | offer_id, outcome_type, outcome_id, claim_key | after valid offer | claim key prevents second outcome |
| elite_variant_selected.v1 | EnemyVariantResolver | Spawner, diagnostics | base_enemy_id, variant_id, variant_class, registry_map_ref, selection_revision | before elite spawn | selection revision is deterministic |
| elite_chest_opened.v1 | EliteChestResolver | Elite UI, RunSession | chest_window_id, source_kind:ELITE_CHEST, selected_variant_id, offer_id | after allowed elite source | reserved window opens once |
| artifact_offer_created.v1 | ArtifactOfferSystem | Artifact UI, RunSession | offer_id, source_kind, exactly_three_artifact_ids, offer_seed | after elite or first-clear source | offer ID prevents duplicate cards |
| artifact_chosen.v1 | ArtifactOfferSystem | RunSession, Result UI | offer_id, selected_artifact_id, effect_ref, state_revision | after valid choice | choice key prevents duplicate effect |
| run_paused.v1 | RunSession | SaveSnapshot, Pause UI | run_id, state_revision, reason, snapshot_ref | at safe boundary | one pause revision |
| run_resumed.v1 | RunSession | SimulationClock, HUD | run_id, restored_state_revision, restore_ref | after validation | restore token prevents double resume |
| run_defeated.v1 | RunCoordinator | ResultBuilder, RewardLedger | run_id, death_reason, state_revision | after authoritative death | death key prevents duplicate settlement |
| run_victory.v1 | RunCoordinator | ResultBuilder, RewardLedger | run_id, final_boss_id, final_settlement_id, no_chest:true | after final ledger commit | victory key prevents duplicate terminal state |
| result_finalized.v1 | ResultBuilder | RewardLedger, Result UI | result_id, outcome, stats_ref, build_ref, state_revision | after defeat or victory projection | read-only reopen |
| reward_ledger_committed.v1 | RewardLedger | MenuFlow, SaveSnapshot | run_id, ledger_revision, committed_entry_ids | after atomic commit | entry IDs prevent duplicate wallet mutation |

## 3. Ordering and duplicate policy

Content load precedes run creation. XP commit precedes level-up offer. Schedule checkpoint precedes boss intro. Authoritative defeat precedes settlement. Non-final settlement precedes BOSS_CHEST. Terminal settlement precedes victory. Defeat or victory precedes result finalization, which precedes wallet commit. A replayed event is acknowledged against its idempotency key and does not repeat XP, aftermath, chest, artifact effect or wallet mutation.

## 4. Conditional clock event semantics

MAIN_BOSS intro and active events keep the visible run, wave, XP and ordinary-spawn clocks frozen through settlement; the encounter clock advances. MINI_BOSS intro and active events keep all visible simulation clocks and ordinary spawn advancing; its encounter clock also advances. Offer, pause, settlement and result events freeze visible clocks.

## 5. Critical payload rules

- checkpoint_reached.v1 must carry one schedule index, stable encounter ID, encounter kind, checkpoint ID, checkpoint seconds and is_final.
- boss_defeated.v1 must carry one boss encounter ID and one defeat revision.
- checkpoint_reward_committed.v1 must carry one ledger entry and one idempotency key.
- boss_chest_opened.v1 is valid only for non-final BOSS_CHEST windows.
- elite_chest_opened.v1 is valid only for reserved ELITE_CHEST windows and an allowed elite projection.
- artifact_offer_created.v1 must carry exactly three candidate IDs. It cannot consume a weapon/passive slot.
- run_victory.v1 requires final settlement and declares no chest.
- XP and aftermath are separate records and cannot share a completion key.

## 6. Ownership and failure

Producers validate local preconditions. Consumers reject unknown IDs, stale state revisions and invalid source kinds. Failures create diagnostics and a recoverable state; they do not fabricate rewards. Retry reuses the same idempotency key.

## 7. Verification target

Static verification checks names, producers, consumers, payload fields, ordering, source-kind guards and duplicate policy against FIRST_RUN_STATE_MACHINE.md and FIRST_RUN_DATA_CONTRACT.json. Godot stdout and exit code are Runtime evidence and remain outside this package.
