
# FIRST_RUN_EVENT_CATALOG — события и команды

Статус: **SPECIFIED_WITH_PENDING_DECISIONS**  
Формат envelope для domain events описан в FIRST_RUN_DATA_CONTRACT.json. Для одного run события упорядочиваются по revision; retries сохраняют event_id и idempotency_key.

## 1. Общие правила

Каждый envelope содержит event_id, event_name, event_version, occurred_at, run_id, revision, causation_id, correlation_id, idempotency_key и payload.

- AUTHORITATIVE_COMMAND — намерение пользователя или платформы; command handler может отклонить его.
- DOMAIN_EVENT — подтверждённое изменение authoritative state; его можно replay/read-model rebuild.
- UI_PROJECTION — производное сообщение для экрана; оно не меняет RunState и может быть восстановлено.
- Повтор domain event с совместимым payload возвращает ранее применённый результат.
- Повтор с несовместимым payload создаёт diagnostic conflict и не делает второй side effect.
- Persistence отмечается только для события, нужного для snapshot, ledger replay, result или диагностики.
- Telemetry не является source of truth и не должна быть условием награды.

## 2. Каталог

| Event name / version | Kind | Producer → consumer | Payload | Ordering / causality | Retry / duplicate | Persistence / telemetry | Failure / recovery |
|---|---|---|---|---|---|---|---|
| app.boot.v1 | DOMAIN_EVENT | BootLoader → AppFlowCoordinator, Diagnostics | app_version, schema_version | process start, no run | same process boot is no-op | diagnostic telemetry | missing registry → RESOURCE_ERROR/retry |
| menu.ready.v1 | UI_PROJECTION | AppFlowCoordinator → menu UI | profile summary, available sections, diagnostics | after registry validation | rebuild projection | no authority; optional telemetry | stale projection rebuild |
| menu.settings.opened.v1 | UI_PROJECTION | AppFlowCoordinator → settings UI | return_owner | caused by open settings | repeated open reuses owner | no persistence | read failure → default + diagnostic |
| characters.opened.v1 | UI_PROJECTION | AppFlowCoordinator → characters UI | hero card IDs, unlock state | after hero registry read | rebuild cards | no authority | missing card disabled |
| hero.selected.v1 | DOMAIN_EVENT | HeroSelection handler → menu/run setup | hero_id, selection_revision | after validation of hero | same hero/revision no-op | profile selection optional | invalid/missing hero → reject + diagnostic |
| run.start_requested.v1 | AUTHORITATIVE_COMMAND | menu UI → RunFacade | command_id, hero_id, artifact_ids, seed_policy | requires no conflicting active run | same command_id returns result | command log optional | invalid selection → RUN_SETUP |
| run.session_created.v1 | DOMAIN_EVENT | RunFacade → SaveRepository, RunLoader | run_id, seed, hero_id, content_version | causation run.start_requested | run_id collision → conflict | snapshot boundary optional | cannot initialize → error, no half-run |
| run.loading_failed.v1 | DOMAIN_EVENT | RunLoader → AppFlowCoordinator, Diagnostics | run_id, path/id, reason_code | after session creation before start | same request replays diagnostic | persist diagnostic | retry or return setup |
| run.started.v1 | DOMAIN_EVENT | RunLoader → RunSession, HUD projection | run_id, revision, initial band | after arena/content validation | same run/revision no-op | snapshot optional | invalid spawn/content → RESOURCE_ERROR |
| wave.changed.v1 | DOMAIN_EVENT | WaveDirector → RunSession, HUD, SpawnService | previous_band_id, current_band_id, multipliers | revision-ordered by clock | same band/revision no-op | snapshot at checkpoint only | unknown band → block spawn + diagnostic |
| boss.telegraph_started.v1 | DOMAIN_EVENT | WaveDirector → arena/HUD, CombatResolver | boss_id, checkpoint_id, telegraph_id, reaction_window | caused by checkpoint crossing | same telegraph_id no-op | event log for result/telemetry | missing boss → RESOURCE_ERROR |
| boss.spawned.v1 | DOMAIN_EVENT | WaveDirector → CombatResolver, SpawnService, HUD | boss_instance_id, boss_id, checkpoint_id | after telegraph guard | duplicate instance ignored | snapshot reference | spawn failure keeps telegraph/error |
| enemy.defeated.v1 | DOMAIN_EVENT | CombatResolver → DropService, Progression, stats | enemy_instance_id, enemy_id, cause, position | one event per instance | duplicate enemy ID no-op | counters/result input | missing content uses diagnostic drop fallback |
| drop.xp_created.v1 | DOMAIN_EVENT | DropService → RunSession, HUD | drop_id, value, source_enemy_id | caused by enemy.defeated | same drop_id no-op | snapshot only if pending | cap pressure → merge, never silent delete |
| aftermath.created.v1 | DOMAIN_EVENT | DropService → aftermath layer, RunSession | aftermath_id, source_enemy_id, visual_kind | caused by enemy.defeated, separate from XP | duplicate aftermath ID no-op | visual state may be clustered | budget pressure → cluster/degrade |
| drop.xp_collected.v1 | DOMAIN_EVENT | PickupSystem → Progression, HUD | drop_id, value, collector_id | after collision/magnet validation | same drop_id cannot add XP twice | counters/result input | invalid/through-wall pickup rejected |
| level.up.v1 | DOMAIN_EVENT | ProgressionService → RunSession, UI | old_level, new_level, xp_remaining | after XP commit | same revision no-op | snapshot if choice pauses | threshold inconsistency → diagnostic |
| upgrade.offer_generated.v1 | UI_PROJECTION | ProgressionService → upgrade UI | offer_id, generation_seed, three offers | caused by level.up; clock frozen | rebuild uses same seed/offer ID | no authority | no legal offer → pending/diagnostic |
| upgrade.offer_chosen.v1 | AUTHORITATIVE_COMMAND | upgrade UI → ProgressionService | offer_id, target_id, command_id | only in UPGRADE_CHOICE | same offer ID returns applied result | build snapshot input | stale/illegal offer → reject and keep choice |
| weapon.upgraded.v1 | DOMAIN_EVENT | BuildInventory → RunSession, HUD, SynergyEvaluator | weapon_id, old_level, new_level | caused by accepted offer | same offer idempotent | build/result snapshot | full/missing weapon → reject |
| passive.upgraded.v1 | DOMAIN_EVENT | BuildInventory → RunSession, HUD, SynergyEvaluator | passive_id, old_level, new_level | caused by accepted offer | same offer idempotent | build/result snapshot | full/missing passive → reject |
| synergy.eligibility_evaluated.v1 | DOMAIN_EVENT | SynergyEvaluator → ChestResolver, HUD | chest_id, eligible_ids, blocked_reasons | after build change or chest open | same build/chest revision rebuilds | chest snapshot input | unresolved content → fallback pending |
| chest.opened.v1 | AUTHORITATIVE_COMMAND | chest UI → ChestResolver | chest_id, offer_id, command_id | only CHEST_PENDING | same offer opens same projection | no claim side effect | unknown/closed chest → read-only/error |
| synergy.claimed.v1 | DOMAIN_EVENT | ChestResolver → BuildInventory, RewardLedger, HUD | synergy_id, chest_id, weapon/passive IDs | after eligibility and user choice | key synergy:run_id:synergy_id | build + ledger reference | duplicate returns prior outcome |
| chest.claimed.v1 | DOMAIN_EVENT | ChestResolver → RewardLedger, RunSession | chest_id, outcome_kind, outcome_id | after one valid outcome | key chest:run_id:chest_id | durable ledger/snapshot | incompatible replay → conflict |
| artifact.obtained.v1 | DOMAIN_EVENT | ChestResolver → BuildInventory, RewardLedger, HUD | artifact_id, chest_id, level/pending effect | caused by chest outcome | same chest/outcome no-op | build + ledger | artifact cap/full → pending fallback |
| boss.defeated.v1 | DOMAIN_EVENT | CombatResolver → RewardCalculator, ChestResolver, RunSession | boss_instance_id, boss_id, checkpoint_id | after authoritative HP zero | duplicate boss instance no-op | checkpoint/result snapshot | inconsistent boss state → diagnostic |
| checkpoint.reward_recorded.v1 | DOMAIN_EVENT | RewardCalculator → RewardLedger, ResultReadModel | entry_id, idempotency_key, amounts, formula_version | caused by boss.defeated | existing key returns receipt | durable ledger required | conflict blocks grant and shows recovery |
| pause.entered.v1 | AUTHORITATIVE_COMMAND | player/OS → RunFacade | reason, captured_phase, command_id | first action freezes clock | repeat is no-op | optional snapshot request | terminal run returns result |
| resume.completed.v1 | DOMAIN_EVENT | RunFacade → RunSession, HUD | captured_phase, revision | after validation of paused session | same revision no-op | telemetry optional | invalid revision → recovery/error |
| save.snapshot_written.v1 | DOMAIN_EVENT | SaveRepository → Diagnostics, recovery UI | snapshot_id, revision, reason, checksum | after atomic write | same snapshot/revision replay | durable record | write failure keeps in-memory run |
| save.restore_succeeded.v1 | DOMAIN_EVENT | SaveRepository → RunFacade, HUD | snapshot_id, revision, migrated_from | after validation/migration | same restore key returns same state | restore audit | no reward claim during restore |
| save.restore_failed.v1 | DOMAIN_EVENT | SaveRepository → Diagnostics, menu | snapshot_id, reason_code, recoverability | after validation failure | same bytes same diagnostic | durable diagnostic | older valid snapshot or fresh menu |
| run.death.v1 | DOMAIN_EVENT | CombatResolver → ResultAssembler, RewardLedger | run_id, terminal_time, reason, checkpoint history | first terminal event wins | result:run_id:defeat replay | immutable result + ledger | duplicate death read-only |
| run.victory.v1 | DOMAIN_EVENT | CombatResolver/RunSession → ResultAssembler, RewardLedger | final_boss_id, terminal_time, victory_guard | after final boss and final check | result:run_id:victory replay | immutable result + ledger | missing guard keeps run pending |
| result.finalized.v1 | DOMAIN_EVENT | ResultAssembler → result UI, RewardLedger | result_id, outcome, stats, ledger refs | after death/victory | same result_id returns snapshot | durable result snapshot | rebuild from RunSession/snapshot |
| result.claimed.v1 | DOMAIN_EVENT | RewardLedger → profile/meta, result UI | result_id, receipt_ids, claim_revision | after user claim/replay | existing receipt returned | durable receipt | failed adapter → retry, no false success |
| diagnostic.reported.v1 | DOMAIN_EVENT | any boundary → Diagnostics/UI | reason_code, operation, affected_id, recovery | causation preserves failed event | same diagnostic can aggregate | durable for recovery/telemetry | never hides original error |
| menu.returned.v1 | UI_PROJECTION | AppFlowCoordinator → menu UI | source_result_id, recovery_summary | after result claim/abandon choice | repeated route is no-op | no domain grant | route retry; active run requires confirmation |

## 3. Causality and ordering rules

1. A domain event is emitted only after the owning state mutation succeeds.
2. One RunSession revision may produce multiple projections, but only one authoritative mutation for the same idempotency key.
3. Boss order is time/checkpoint ordered; a later boss event is invalid while an earlier checkpoint is unresolved.
4. XP collection precedes level.up; level.up precedes offer generation; offer choice precedes build mutation.
5. boss.defeated precedes checkpoint.reward_recorded and chest offer; chest closure never substitutes for claim.
6. run.death or run.victory closes simulation before result.finalized.
7. result.finalized precedes result.claimed; result reopening reads stored result and ledger.
8. Save restore emits no reward event merely because bytes were valid.

## 4. Persistence and duplicate policy

Authoritative persisted items:

- RunSession snapshot at accepted save boundaries;
- RewardLedger entries and receipts;
- immutable ResultSnapshot;
- diagnostics needed for recovery.

Rebuildable items:

- HUD/read model;
- menu projections;
- generated visual aftermath presentation;
- telemetry aggregates.

For a duplicate event, the consumer looks up idempotency_key before applying side effects. A duplicate with matching payload returns REPLAYED. A duplicate with incompatible payload returns CONFLICT and does not mutate state.

## 5. Failure contract

Every failed command/event path emits diagnostic.reported.v1 with reason_code, current state, revision, affected stable ID and recovery action. The UI must distinguish:

- retryable loading/save failure;
- user-correctable invalid choice;
- pending product/content decision;
- terminal run result;
- unrecoverable snapshot requiring fresh menu.

