extends RefCounted
class_name RunCoordinator

const ContentRegistryType = preload("res://scripts/runtime/content_registry.gd")
const RunSessionType = preload("res://scripts/runtime/run_session.gd")
const SimulationClockType = preload("res://scripts/runtime/simulation_clock.gd")
const WaveDirectorType = preload("res://scripts/runtime/wave_director.gd")
const BossDirectorType = preload("res://scripts/runtime/boss_director.gd")
const RewardLedgerType = preload("res://scripts/runtime/reward_ledger.gd")
const ArtifactOfferSystemType = preload("res://scripts/runtime/artifact_offer_system.gd")

## R1 orchestration boundary.
##
## Commands enter here, domain state is changed on RunSession, and every
## accepted mutation emits a deterministic trace event. The combat path is a
## deliberately small fixture backed by BALANCE_MODEL.json's explicit
## simulation_model records; the trace keeps that proposed status visible.

var registry: ContentRegistry
var session: RunSession
var clock: SimulationClock
var wave_director: WaveDirector
var boss_director: BossDirector
var reward_ledger: RewardLedger
var artifact_offer_system: ArtifactOfferSystem
var trace: Array[Dictionary] = []
var diagnostics: Array[Dictionary] = []
var start_outcomes: Dictionary = {}
var completed_offer_outcomes: Dictionary = {}
var completed_chest_outcomes: Dictionary = {}
var completed_artifact_outcomes: Dictionary = {}
var artifact_refresh_outcomes: Dictionary = {}
var artifact_open_outcomes: Dictionary = {}
var last_coherent_snapshot: Dictionary = {}
var run_sequence := 0
var booted := false


func boot(content_path: String = ContentRegistry.DEFAULT_PATH) -> Dictionary:
    registry = ContentRegistryType.new()
    var result: Dictionary = registry.load_and_validate(content_path)
    if not bool(result.get("ok", false)):
        booted = false
        diagnostics = result.get("diagnostics", []).duplicate(true)
        _emit("content_load_failed", {"diagnostics": diagnostics, "source_path": content_path})
        return result

    booted = true
    wave_director = WaveDirectorType.new(registry)
    boss_director = BossDirectorType.new(registry)
    reward_ledger = RewardLedgerType.new()
    artifact_offer_system = ArtifactOfferSystemType.new(registry)
    _emit("content_loaded", {
        "content_version": registry.content_version,
        "model_id": result.get("model_id", ""),
        "model_status": result.get("model_status", ""),
        "source_path": content_path,
        "r2_content_status": registry.get_r2_content_status()
    })
    return result


func start_run(
        character_id: String,
        seed: int,
        client_request_id: String,
        pre_run_artifact_ids: Array = []
    ) -> Dictionary:
    if not booted or registry == null or not registry.is_loaded():
        return _fail("CONTENT_NOT_READY", "Cannot start a run before content is loaded.", true)

    if not pre_run_artifact_ids.is_empty():
        return _fail("PRE_RUN_ARTIFACT_LOADOUT_REJECTED", "R1 does not accept pre-run artifact selection.", false)

    if not client_request_id.is_empty() and start_outcomes.has(client_request_id):
        var stored: Dictionary = start_outcomes[client_request_id].duplicate(true)
        stored["duplicate"] = true
        _emit("run_start_duplicate", {"client_request_id": client_request_id, "run_id": stored.get("run_id", "")})
        return stored

    if session != null:
        var existing: Dictionary = {
            "ok": true,
            "duplicate": true,
            "code": "RUN_ALREADY_ACTIVE",
            "run_id": session.run_id,
            "state": session.state,
            "state_revision": session.state_revision,
            "content_version": session.content_version
        }
        _remember_start(client_request_id, existing)
        _emit("run_start_duplicate", {"client_request_id": client_request_id, "run_id": session.run_id})
        return existing

    var hero_profile := registry.get_runtime_hero_profile(character_id)
    if hero_profile.is_empty():
        return _fail("UNKNOWN_CHARACTER", "Character is not present in the loaded Content Registry.", false, {"character_id": character_id})

    var starting_weapon := str(hero_profile.get("starting_weapon_id", ""))
    var starting_passive := str(hero_profile.get("starting_passive_id", ""))
    var weapon_fixture := registry.get_weapon_fixture(starting_weapon)
    if weapon_fixture.is_empty():
        return _fail("STARTING_WEAPON_MISSING", "Starting weapon is missing from the loaded Content Registry.", false, {"weapon_id": starting_weapon})

    var initial_wave := registry.get_wave_band_for_time(0.0)
    if initial_wave.is_empty():
        return _fail("WAVE_CONTENT_MISSING", "No initial wave band is available in the Content Registry.", false)

    run_sequence += 1
    var run_id := "run-%d-%d" % [seed, run_sequence]
    var hero_hp := _hero_hp(hero_profile)
    var move_speed := _hero_move_speed(hero_profile)
    var damage_multiplier := _base_numeric_value(["hero_stats", "base", "damage_multiplier"], 1.0)
    var cooldown_multiplier := _base_numeric_value(["hero_stats", "base", "weapon_cooldown_multiplier"], 1.0)

    var build := {
        "weapon_slots": 6,
        "passive_slots": 6,
        "weapons": {starting_weapon: {"level": 1, "source_status": weapon_fixture.get("source_status", "UNKNOWN")}},
        "passives": {starting_passive: {"rank": 0, "source_status": "PROPOSED_MODEL_ONLY"}},
        "claimed_synergy_ids": []
    }
    var stats := {
        "current_hp": hero_hp,
        "max_hp": hero_hp,
        "attack": float(weapon_fixture.get("base_damage", {}).get("value", 0.0)),
        "damage_multiplier": damage_multiplier,
        "crit_chance": _nested_numeric(hero_profile.get("crit_chance", {}), 0.0),
        "crit_multiplier": _nested_numeric(hero_profile.get("crit_multiplier", {}), 1.0),
        "move_speed": move_speed,
        "weapon_cooldown": cooldown_multiplier,
        "weapon_levels": {starting_weapon: 1},
        "passive_levels": {starting_passive: 0},
        "active_synergies": [],
        "level": 1,
        "xp": 0,
        "elapsed_time": 0.0,
        "current_wave_band": str(initial_wave.get("wave_band_id", "")),
        "enemies_defeated": 0,
        "active_enemy_count": 0,
        "bonus_state": {},
        "checkpoint_rewards": [],
        "wallet": {"gold": 0, "moon_seals": 0, "boss_essence": 0},
        "artifacts": [],
        "artifact_capacity": "UNBOUNDED_WITHIN_RUN",
        "diagnostics": [],
        "source_status": "BALANCE_MODEL_AND_SIMULATION_FIXTURE"
    }

    session = RunSessionType.new(
        run_id,
        seed,
        registry.content_version,
        character_id,
        build,
        stats,
        str(initial_wave.get("wave_band_id", ""))
    )
    session.state = RunSession.STATE_RUN_ACTIVE
    session.bump_revision()

    clock = SimulationClockType.new()
    clock.start_run()
    session.stats["elapsed_time"] = clock.run_seconds
    _remember_start(client_request_id, {
        "ok": true,
        "duplicate": false,
        "run_id": run_id,
        "state": session.state,
        "state_revision": session.state_revision,
        "content_version": session.content_version
    })
    _emit("run_created", {
        "run_id": run_id,
        "seed": seed,
        "content_version": session.content_version,
        "selected_hero_id": character_id,
        "state": session.state,
        "source_status": "BALANCE_MODEL_AND_SIMULATION_FIXTURE"
    })
    _emit("arena_ready", {"run_id": run_id, "required_resource_status": "R1_DOMAIN_ENTRY_READY"})
    return start_outcomes.get(client_request_id, {
        "ok": true,
        "duplicate": false,
        "run_id": run_id,
        "state": session.state,
        "state_revision": session.state_revision,
        "content_version": session.content_version
    }).duplicate(true)


func advance(delta_seconds: float) -> Dictionary:
    if session == null or clock == null:
        return _fail("RUN_NOT_STARTED", "No RunSession exists.", true)
    var result := clock.advance(delta_seconds)
    if not bool(result.get("ok", false)):
        _record_diagnostic("CLOCK_ADVANCE_FAILED", "Simulation clock rejected the delta.", true, {"delta": delta_seconds})
        return result

    session.stats["elapsed_time"] = clock.run_seconds
    if _is_wave_progression_active() and result.get("advanced", false):
        var pressure := wave_director.resolve(clock.run_seconds, _active_boss_kind())
        _emit("wave_pressure_sample", pressure)
        var band := registry.get_wave_band_for_time(clock.run_seconds)
        if not band.is_empty():
            var next_band_id := str(band.get("wave_band_id", ""))
            if next_band_id != session.current_wave_band_id:
                var previous_band_id := session.current_wave_band_id
                session.current_wave_band_id = next_band_id
                session.stats["current_wave_band"] = next_band_id
                session.bump_revision()
                _emit("wave_band_changed", {
                    "from_wave_band_id": previous_band_id,
                    "wave_band_id": next_band_id,
                    "elapsed_seconds": clock.run_seconds,
                    "registry_source": "BALANCE_MODEL.json.wave_bands"
                })
    return result


func spawn_wave_fixture() -> Dictionary:
    if not _is_wave_progression_active():
        return _fail("WAVE_PROGRESSION_BLOCKED", "Wave fixture is blocked during a main-boss encounter or offer.", true)
    if not session.active_enemy.is_empty():
        return {
            "ok": true,
            "duplicate": true,
            "enemy_id": session.active_enemy.get("enemy_id", ""),
            "active_enemy": session.active_enemy.duplicate(true)
        }

    var admission := wave_director.evaluate_spawn(
        clock.run_seconds,
        _active_boss_kind(),
        int(session.stats.get("active_enemy_count", 0)),
        1
    )
    if not bool(admission.get("ok", false)):
        return _fail(
            str(admission.get("code", "WAVE_SPAWN_REJECTED")),
            "Wave spawn was rejected by the data-driven wave policy.",
            true,
            admission
        )
    var band: Dictionary = admission.get("band", {})
    var composition: Variant = band.get("composition", {}).get("value", [])
    var enemy_id := ""
    if composition is Array and not composition.is_empty():
        var spawn_index := int(session.stats.get("fixture_spawn_count", 0)) % composition.size()
        enemy_id = str(composition[spawn_index])
    elif typeof(composition) == TYPE_STRING:
        var enemy_stats: Dictionary = registry.get_model_field(["simulation_model", "enemy_stats"], {})
        if not enemy_stats.is_empty():
            enemy_id = str(enemy_stats.keys()[0])
    if enemy_id.is_empty():
        return _fail("WAVE_COMPOSITION_EMPTY", "Wave band has no usable fixture composition.", true)

    var enemy := registry.get_enemy_fixture(enemy_id)
    var hp_record: Dictionary = enemy.get("base_hp", {})
    var damage_record: Dictionary = enemy.get("base_damage", {})
    var speed_record: Dictionary = enemy.get("base_speed", {})
    var xp_record: Dictionary = enemy.get("xp_value", {})
    if enemy.is_empty() or not hp_record.has("value") or not damage_record.has("value") or not speed_record.has("value") or not xp_record.has("value"):
        return _fail("COMBAT_FIXTURE_DATA_PENDING", "The selected fixture has no complete data record.", true, {"enemy_id": enemy_id})

    var hp_multiplier := float(band.get("enemy_hp_multiplier", {}).get("value", 1.0))
    var damage_multiplier := float(band.get("enemy_damage_multiplier", {}).get("value", 1.0))
    session.active_enemy = {
        "enemy_id": enemy_id,
        "hp_current": float(hp_record.get("value", 0.0)) * hp_multiplier,
        "hp_max": float(hp_record.get("value", 0.0)) * hp_multiplier,
        "damage": float(damage_record.get("value", 0.0)) * damage_multiplier,
        "speed": float(speed_record.get("value", 0.0)),
        "xp_value": int(xp_record.get("value", 0)),
        "source_path": enemy.get("source_path", ""),
        "source_status": enemy.get("source_status", "UNKNOWN"),
        "wave_band_id": band.get("wave_band_id", ""),
        "active_cap": band.get("active_cap", {}).get("value", null),
        "active_count_after_spawn": 1
    }
    session.stats["active_enemy_count"] = 1
    session.stats["fixture_spawn_count"] = int(session.stats.get("fixture_spawn_count", 0)) + 1
    session.bump_revision()
    _emit("wave_fixture_spawned", {
        "enemy_id": enemy_id,
        "wave_band_id": band.get("wave_band_id", ""),
        "active_count": 1,
        "active_cap": band.get("active_cap", {}).get("value", null),
        "spawn_budget_per_second": band.get("spawn_budget_per_second", {}).get("value", null),
        "hp": session.active_enemy["hp_current"],
        "damage": session.active_enemy["damage"],
        "xp_value": session.active_enemy["xp_value"],
        "source_path": enemy.get("source_path", ""),
        "source_status": enemy.get("source_status", "UNKNOWN")
    })
    return {"ok": true, "duplicate": false, "active_enemy": session.active_enemy.duplicate(true)}


func resolve_fixture_attack() -> Dictionary:
    if not _is_wave_progression_active():
        return _fail("COMBAT_BLOCKED", "Combat fixture is blocked outside an active wave state.", true)
    if session.active_enemy.is_empty():
        return _fail("NO_ACTIVE_ENEMY", "Combat fixture has no active enemy.", true)

    var contact_cooldown := registry.get_contact_damage_cooldown()
    if clock.run_seconds - session.last_hit_at < contact_cooldown:
        _emit("combat_hit_rejected", {
            "reason": "HIT_COOLDOWN",
            "required_seconds": contact_cooldown,
            "remaining_seconds": contact_cooldown - (clock.run_seconds - session.last_hit_at)
        })
        return {"ok": false, "duplicate": true, "code": "HIT_COOLDOWN"}

    var weapon_ids: Array = session.build.get("weapons", {}).keys()
    if weapon_ids.is_empty():
        return _fail("BUILD_WEAPON_MISSING", "Combat fixture has no weapon in the build.", false)
    var weapon_id := str(weapon_ids[0])
    var weapon := registry.get_weapon_fixture(weapon_id)
    var base_damage := float(weapon.get("base_damage", {}).get("value", 0.0))
    var damage_multiplier := float(session.stats.get("damage_multiplier", 1.0))
    var damage := base_damage * damage_multiplier
    var before_hp := float(session.active_enemy.get("hp_current", 0.0))
    var after_hp := max(0.0, before_hp - damage)
    session.active_enemy["hp_current"] = after_hp
    session.last_hit_at = clock.run_seconds
    session.bump_revision()

    if after_hp <= 0.0:
        var defeated_enemy_id := str(session.active_enemy.get("enemy_id", ""))
        var xp_value := int(session.active_enemy.get("xp_value", 0))
        var drop := session.create_xp_drop(defeated_enemy_id, "fixture_xp", xp_value)
        session.active_enemy = {}
        session.stats["active_enemy_count"] = 0
        session.stats["enemies_defeated"] = int(session.stats.get("enemies_defeated", 0)) + 1
        session.bump_revision()
        _emit("combat_defeat", {
            "enemy_id": defeated_enemy_id,
            "damage": damage,
            "hp_before": before_hp,
            "xp_drop_id": drop.get("xp_item_id", ""),
            "xp_value": xp_value,
            "source_status": "PROPOSED_MODEL_ONLY"
        })
        return {"ok": true, "defeated": true, "drop": drop, "damage": damage}

    _emit("combat_damage", {
        "enemy_id": session.active_enemy.get("enemy_id", ""),
        "damage": damage,
        "hp_before": before_hp,
        "hp_after": after_hp,
        "contact_cooldown_seconds": contact_cooldown,
        "weapon_source_path": weapon.get("source_path", ""),
        "weapon_source_status": weapon.get("source_status", "UNKNOWN")
    })
    return {"ok": true, "defeated": false, "damage": damage, "hp_after": after_hp}


func collect_xp(xp_item_id: String) -> Dictionary:
    if session == null:
        return _fail("RUN_NOT_STARTED", "No RunSession exists.", true)
    if not session.xp_drops.has(xp_item_id):
        return _fail("XP_DROP_NOT_FOUND", "XP drop does not belong to this run.", true, {"xp_item_id": xp_item_id})

    var drop: Dictionary = session.xp_drops[xp_item_id]
    if bool(drop.get("collected", false)):
        var duplicate_outcome := {
            "ok": true,
            "duplicate": true,
            "xp_item_id": xp_item_id,
            "xp_after": session.stats.get("xp", 0),
            "state": session.state
        }
        _emit("xp_drop_duplicate", duplicate_outcome)
        return duplicate_outcome

    if not _is_wave_progression_active():
        return _fail("XP_COLLECTION_BLOCKED", "XP collection is blocked while ordinary wave progression is paused.", true)

    drop["collected"] = true
    drop["pool_state"] = "COLLECTED"
    session.xp_drops[xp_item_id] = drop
    session.stats["xp"] = int(session.stats.get("xp", 0)) + int(drop.get("value", 0))
    session.bump_revision()
    _emit("xp_drop_collected", {
        "xp_item_id": xp_item_id,
        "value": drop.get("value", 0),
        "xp_after": session.stats["xp"],
        "source_enemy_id": drop.get("source_enemy_id", "")
    })

    var level_up := _maybe_open_level_up_offer()
    return {
        "ok": true,
        "duplicate": false,
        "xp_item_id": xp_item_id,
        "xp_after": session.stats["xp"],
        "level_up": level_up
    }


func claim_upgrade(offer_id: String, choice_id: String, expected_revision: int) -> Dictionary:
    if completed_offer_outcomes.has(offer_id):
        var completed: Dictionary = completed_offer_outcomes[offer_id].duplicate(true)
        completed["duplicate"] = true
        _emit("offer_claim_duplicate", {"offer_id": offer_id, "choice_id": choice_id})
        return completed

    if session == null or session.state != RunSession.STATE_UPGRADE_OFFER:
        return _fail("OFFER_NOT_OPEN", "No blocking upgrade offer is open.", true, {"offer_id": offer_id})
    if str(session.pending_offer.get("offer_id", "")) != offer_id:
        return _fail("STALE_OFFER", "Offer ID does not match the open offer.", true, {"offer_id": offer_id})
    if expected_revision != int(session.pending_offer.get("created_at_revision", -1)):
        return _fail("STALE_COMMAND", "Offer revision is stale.", true, {"expected_revision": expected_revision, "offer_revision": session.pending_offer.get("created_at_revision", -1)})
    var choice_ids: Array = session.pending_offer.get("choice_ids", [])
    if not choice_ids.has(choice_id):
        return _fail("INVALID_OFFER_CHOICE", "Choice is not one of the three cards in the open offer.", false, {"choice_id": choice_id})

    var outcome := {
        "ok": true,
        "duplicate": false,
        "offer_id": offer_id,
        "choice_id": choice_id,
        "mutation": ""
    }
    var choices: Array = session.pending_offer.get("choice_records", [])
    var selected: Dictionary = {}
    for choice in choices:
        if str(choice.get("choice_id", "")) == choice_id:
            selected = choice
            break

    var kind := str(selected.get("kind", ""))
    if kind == "WEAPON_UPGRADE" and session.build.get("weapons", {}).has(choice_id):
        var weapon_entry: Dictionary = session.build["weapons"][choice_id]
        weapon_entry["level"] = int(weapon_entry.get("level", 0)) + 1
        session.build["weapons"][choice_id] = weapon_entry
        session.stats["weapon_levels"][choice_id] = weapon_entry["level"]
        outcome["mutation"] = "WEAPON_LEVEL_INCREASED"
    elif kind == "PASSIVE_UPGRADE" and session.build.get("passives", {}).has(choice_id):
        var passive_entry: Dictionary = session.build["passives"][choice_id]
        passive_entry["rank"] = int(passive_entry.get("rank", 0)) + 1
        session.build["passives"][choice_id] = passive_entry
        session.stats["passive_levels"][choice_id] = passive_entry["rank"]
        outcome["mutation"] = "PASSIVE_RANK_INCREASED"
    else:
        session.stats["bonus_state"]["fixture_upgrade_id"] = choice_id
        session.stats["bonus_state"]["fixture_upgrade_status"] = "EFFECT_PENDING_PRODUCT_DECISION"
        outcome["mutation"] = "TYPED_PENDING_FIXTURE_UPGRADE"

    session.pending_offer["claimed"] = true
    session.pending_offer["outcome"] = outcome.duplicate(true)
    session.completed_offer_outcomes[offer_id] = outcome.duplicate(true)
    completed_offer_outcomes[offer_id] = outcome.duplicate(true)
    session.pending_offer = {}
    session.state = RunSession.STATE_RUN_ACTIVE
    clock.resume()
    session.bump_revision()
    _emit("upgrade_applied", outcome)
    return outcome


func start_main_boss(checkpoint_id: String) -> Dictionary:
    if session == null or session.state != RunSession.STATE_RUN_ACTIVE:
        return _fail("MAIN_BOSS_NOT_ALLOWED", "Main boss requires RUN_ACTIVE.", true)
    var started := boss_director.begin(BossDirectorType.KIND_MAIN, checkpoint_id, "", clock.run_seconds)
    if not bool(started.get("ok", false)):
        return _fail(str(started.get("code", "BOSS_START_FAILED")), "Main boss could not start.", false, started)

    session.resume_state = RunSession.STATE_RUN_ACTIVE
    session.active_boss_encounter = started.get("encounter", {}).duplicate(true)
    session.checkpoint_id = checkpoint_id
    session.state = RunSession.STATE_MAIN_BOSS_INTRO
    session.bump_revision()
    _emit("main_boss_intro", session.active_boss_encounter)

    clock.start_encounter()
    session.state = RunSession.STATE_MAIN_BOSS_ACTIVE
    session.bump_revision()
    _emit("main_boss_active", {
        "encounter_id": session.active_boss_encounter.get("encounter_id", ""),
        "run_seconds": clock.run_seconds,
        "encounter_seconds": clock.encounter_seconds,
        "run_clock_frozen": true,
        "wave_xp_spawn_frozen": true
    })
    return {"ok": true, "state": session.state, "encounter": session.active_boss_encounter.duplicate(true)}


func start_mini_boss(boss_id: String) -> Dictionary:
    if session == null or session.state != RunSession.STATE_RUN_ACTIVE:
        return _fail("MINI_BOSS_NOT_ALLOWED", "Mini boss requires RUN_ACTIVE.", true)
    var started := boss_director.begin(BossDirectorType.KIND_MINI, "", boss_id, clock.run_seconds)
    if not bool(started.get("ok", false)):
        return _fail(str(started.get("code", "MINI_BOSS_START_FAILED")), "Mini boss content is not available in the loaded registry.", true, started)

    session.resume_state = RunSession.STATE_RUN_ACTIVE
    session.active_boss_encounter = started.get("encounter", {}).duplicate(true)
    session.checkpoint_id = str(session.active_boss_encounter.get("checkpoint_id", ""))
    session.state = RunSession.STATE_MINI_BOSS_INTRO
    session.bump_revision()
    _emit("mini_boss_intro", session.active_boss_encounter)

    clock.start_mini_boss()
    session.state = RunSession.STATE_MINI_BOSS_ACTIVE
    session.bump_revision()
    _emit("mini_boss_active", {
        "encounter_id": session.active_boss_encounter.get("encounter_id", ""),
        "run_seconds": clock.run_seconds,
        "encounter_seconds": clock.encounter_seconds,
        "run_clock_frozen": false,
        "wave_xp_spawn_frozen": false
    })
    return {"ok": true, "state": session.state, "encounter": session.active_boss_encounter.duplicate(true)}


func defeat_active_boss() -> Dictionary:
    if session == null:
        return _fail("NO_ACTIVE_BOSS", "There is no active boss encounter.", true)
    if not [RunSession.STATE_MAIN_BOSS_ACTIVE, RunSession.STATE_MINI_BOSS_ACTIVE].has(session.state):
        if not session.last_boss_encounter_id.is_empty() and session.boss_defeat_outcomes.has(session.last_boss_encounter_id):
            var duplicate: Dictionary = session.boss_defeat_outcomes[session.last_boss_encounter_id].duplicate(true)
            duplicate["duplicate"] = true
            _emit("boss_defeat_duplicate", {"encounter_id": session.last_boss_encounter_id})
            return duplicate
        return _fail("NO_ACTIVE_BOSS", "There is no active boss encounter.", true)
    var encounter_id := str(session.active_boss_encounter.get("encounter_id", ""))
    var defeated := boss_director.defeat(encounter_id)
    if not bool(defeated.get("ok", false)):
        return _fail(str(defeated.get("code", "BOSS_DEFEAT_FAILED")), "Boss defeat was stale or missing.", false, defeated)

    var encounter: Dictionary = defeated.get("defeated", {}).duplicate(true)
    encounter_id = str(encounter.get("encounter_id", ""))
    session.last_boss_encounter_id = encounter_id
    session.active_boss_encounter = encounter
    clock.freeze()
    if str(encounter.get("boss_kind", "")) == BossDirectorType.KIND_MAIN:
        session.state = RunSession.STATE_CHECKPOINT_SETTLEMENT
        session.bump_revision()
        _emit("main_boss_defeated", {"encounter": encounter, "encounter_seconds": clock.encounter_seconds})
        var main_result := settle_checkpoint()
        session.boss_defeat_outcomes[encounter_id] = main_result.duplicate(true)
        return main_result

    session.state = RunSession.STATE_RUN_ACTIVE
    session.bump_revision()
    _emit("mini_boss_defeated", {"encounter": encounter, "encounter_seconds": clock.encounter_seconds})
    var mini_settlement := reward_ledger.settle(
        session.run_id,
        "MINI_BOSS",
        str(encounter.get("boss_id", "")),
        "MINI_BOSS_CHEST",
        {"source_status": encounter.get("source_status", "PENDING_CONTENT_SYNC")}
    )
    session.reward_ledger_entries[mini_settlement.get("ledger_key", "")] = mini_settlement.duplicate(true)
    session.active_boss_encounter = {}
    var mini_result := _create_chest_offer("MINI_BOSS_CHEST", str(encounter.get("boss_id", "")), mini_settlement)
    session.boss_defeat_outcomes[encounter_id] = mini_result.duplicate(true)
    return mini_result


func settle_checkpoint() -> Dictionary:
    if session == null:
        return _fail("CHECKPOINT_SETTLEMENT_NOT_ALLOWED", "No RunSession exists.", true)
    var checkpoint_id := str(session.active_boss_encounter.get("checkpoint_id", session.checkpoint_id))
    if session.state != RunSession.STATE_CHECKPOINT_SETTLEMENT:
        if session.checkpoint_settlement_outcomes.has(checkpoint_id):
            var duplicate: Dictionary = session.checkpoint_settlement_outcomes[checkpoint_id].duplicate(true)
            duplicate["duplicate"] = true
            _emit("checkpoint_settlement_duplicate", {"checkpoint_id": checkpoint_id})
            return duplicate
        return _fail("CHECKPOINT_SETTLEMENT_NOT_ALLOWED", "Checkpoint settlement requires CHECKPOINT_SETTLEMENT.", true)
    var is_final := registry.is_final_checkpoint(checkpoint_id)
    var reward := registry.get_checkpoint_reward(checkpoint_id)
    var reward_type := "FINAL_SETTLEMENT" if is_final else "CHECKPOINT_REWARD"
    var settlement := reward_ledger.settle(session.run_id, "MAIN_BOSS", checkpoint_id, reward_type, reward)
    session.reward_ledger_entries[settlement.get("ledger_key", "")] = settlement.duplicate(true)
    if not bool(settlement.get("duplicate", false)):
        _apply_wallet_reward(reward)
        session.stats["checkpoint_rewards"].append(reward.duplicate(true))
    _emit("checkpoint_settled", {
        "checkpoint_id": checkpoint_id,
        "final": is_final,
        "ledger_key": settlement.get("ledger_key", ""),
        "reward": reward,
        "duplicate": settlement.get("duplicate", false)
    })

    if is_final:
        session.state = RunSession.STATE_RUN_VICTORY
        session.active_boss_encounter = {}
        session.bump_revision()
        clock.freeze()
        _emit("run_victory", {
            "checkpoint_id": checkpoint_id,
            "final_settlement": true,
            "boss_chest": false,
            "run_seconds": clock.run_seconds
        })
        var final_result := {"ok": true, "final": true, "state": session.state, "settlement": settlement}
        session.checkpoint_settlement_outcomes[checkpoint_id] = final_result.duplicate(true)
        return final_result

    var chest_result := _create_chest_offer("BOSS_CHEST", checkpoint_id, settlement)
    session.checkpoint_settlement_outcomes[checkpoint_id] = chest_result.duplicate(true)
    return chest_result


func claim_chest(offer_id: String, expected_revision: int) -> Dictionary:
    if completed_chest_outcomes.has(offer_id):
        var duplicate: Dictionary = completed_chest_outcomes[offer_id].duplicate(true)
        duplicate["duplicate"] = true
        _emit("chest_claim_duplicate", {"offer_id": offer_id})
        return duplicate
    if session == null or session.state != RunSession.STATE_BOSS_CHEST:
        return _fail("CHEST_NOT_OPEN", "No chest offer is open.", true, {"offer_id": offer_id})
    if str(session.pending_chest_offer.get("offer_id", "")) != offer_id:
        return _fail("STALE_CHEST", "Chest offer ID does not match.", true, {"offer_id": offer_id})
    if expected_revision != int(session.pending_chest_offer.get("created_at_revision", -1)):
        return _fail("STALE_COMMAND", "Chest offer revision is stale.", true, {"expected_revision": expected_revision})

    var outcome := {
        "ok": true,
        "duplicate": false,
        "offer_id": offer_id,
        "offer_type": session.pending_chest_offer.get("offer_type", ""),
        "source_kind": session.pending_chest_offer.get("source_kind", ""),
        "source_id": session.pending_chest_offer.get("source_id", ""),
        "checkpoint_id": session.pending_chest_offer.get("checkpoint_id", ""),
        "mutation": "SYNERGY_OR_FALLBACK_CONTRACT"
    }
    completed_chest_outcomes[offer_id] = outcome.duplicate(true)
    session.completed_chest_outcomes[offer_id] = outcome.duplicate(true)
    session.pending_chest_offer = {}
    session.active_boss_encounter = {}
    session.state = RunSession.STATE_RUN_ACTIVE
    session.bump_revision()
    clock.start_run()
    _emit("chest_claimed", outcome)
    return outcome


func open_artifact_offer(source: String, client_request_id: String = "") -> Dictionary:
    if session == null:
        return _fail("RUN_NOT_STARTED", "No RunSession exists.", true)
    if not client_request_id.is_empty() and artifact_open_outcomes.has(client_request_id):
        var duplicate: Dictionary = artifact_open_outcomes[client_request_id].duplicate(true)
        duplicate["duplicate"] = true
        return duplicate
    if source == "FIRST_CLEAR_REWARD" and session.state != RunSession.STATE_RUN_VICTORY:
        return _fail("FIRST_CLEAR_OFFER_NOT_ALLOWED", "First-clear offer requires a finalized victory.", false)
    if source == "ELITE_PACK" and session.state != RunSession.STATE_RUN_ACTIVE:
        return _fail("ELITE_PACK_OFFER_NOT_ALLOWED", "Elite-pack offer requires an active run.", false)

    session.artifact_sequence += 1
    var offer := artifact_offer_system.create_offer(session.run_id, session.seed, source, session.artifact_sequence, session.state_revision)
    if not bool(offer.get("ok", false)):
        session.artifact_sequence -= 1
        return _fail(str(offer.get("code", "ARTIFACT_OFFER_FAILED")), "Artifact offer contract is unavailable.", false, offer)
    session.resume_state = session.state
    session.pending_artifact_offer = offer.duplicate(true)
    session.state = RunSession.STATE_ARTIFACT_OFFER
    session.bump_revision()
    if source == "FIRST_CLEAR_REWARD":
        clock.freeze()
    else:
        clock.pause()
    var result := {"ok": true, "duplicate": false, "offer": session.pending_artifact_offer.duplicate(true), "state": session.state}
    if not client_request_id.is_empty():
        artifact_open_outcomes[client_request_id] = result.duplicate(true)
    _emit("artifact_offer_created", session.pending_artifact_offer)
    return result


func refresh_artifact_offer(offer_id: String, request_id: String, expected_revision: int) -> Dictionary:
    if artifact_refresh_outcomes.has(request_id):
        var duplicate: Dictionary = artifact_refresh_outcomes[request_id].duplicate(true)
        duplicate["duplicate"] = true
        return duplicate
    if session == null or session.state != RunSession.STATE_ARTIFACT_OFFER:
        return _fail("ARTIFACT_OFFER_NOT_OPEN", "No artifact offer is open.", true)
    if str(session.pending_artifact_offer.get("offer_id", "")) != offer_id:
        return _fail("STALE_ARTIFACT_OFFER", "Artifact offer ID does not match.", true)
    if expected_revision != int(session.pending_artifact_offer.get("created_at_revision", -1)):
        return _fail("STALE_COMMAND", "Artifact offer revision is stale.", true)
    var refreshed := artifact_offer_system.refresh_offer(session.pending_artifact_offer, session.seed + session.artifact_sequence)
    session.bump_revision()
    refreshed["created_at_revision"] = session.state_revision
    session.pending_artifact_offer = refreshed
    var result := {"ok": true, "duplicate": false, "offer": refreshed.duplicate(true), "request_id": request_id}
    artifact_refresh_outcomes[request_id] = result.duplicate(true)
    session.artifact_refresh_outcomes[request_id] = result.duplicate(true)
    _emit("artifact_offer_refreshed", {"offer_id": offer_id, "refresh_count": refreshed.get("refresh_count", 0), "choice_ids": refreshed.get("choice_ids", [])})
    return result


func claim_artifact(offer_id: String, choice_id: String, expected_revision: int) -> Dictionary:
    if completed_artifact_outcomes.has(offer_id):
        var duplicate: Dictionary = completed_artifact_outcomes[offer_id].duplicate(true)
        duplicate["duplicate"] = true
        _emit("artifact_claim_duplicate", {"offer_id": offer_id, "choice_id": choice_id})
        return duplicate
    if session == null or session.state != RunSession.STATE_ARTIFACT_OFFER:
        return _fail("ARTIFACT_OFFER_NOT_OPEN", "No artifact offer is open.", true)
    if str(session.pending_artifact_offer.get("offer_id", "")) != offer_id:
        return _fail("STALE_ARTIFACT_OFFER", "Artifact offer ID does not match.", true)
    if expected_revision != int(session.pending_artifact_offer.get("created_at_revision", -1)):
        return _fail("STALE_COMMAND", "Artifact choice revision is stale.", true)
    var selected := artifact_offer_system.select(session.pending_artifact_offer, choice_id)
    if not bool(selected.get("ok", false)):
        return _fail(str(selected.get("code", "INVALID_ARTIFACT_CHOICE")), "Artifact choice is not in the open offer.", false)

    var candidate: Dictionary = selected.get("selected", {}).duplicate(true)
    var instance_id := "%s:artifact-instance:%d" % [session.run_id, session.artifact_sequence]
    var instance := {
        "artifact_instance_id": instance_id,
        "artifact_id": candidate.get("artifact_id", ""),
        "source": candidate.get("source", ""),
        "effect": candidate.get("effect", {}).duplicate(true),
        "capacity": "UNBOUNDED_WITHIN_RUN",
        "build_slot_mutation": false
    }
    session.stats["artifacts"].append(instance.duplicate(true))
    var outcome := {
        "ok": true,
        "duplicate": false,
        "offer_id": offer_id,
        "choice_id": choice_id,
        "artifact_instance_id": instance_id,
        "artifact": instance.duplicate(true)
    }
    completed_artifact_outcomes[offer_id] = outcome.duplicate(true)
    session.completed_artifact_outcomes[offer_id] = outcome.duplicate(true)
    var resume_state := session.resume_state
    session.pending_artifact_offer = {}
    session.state = resume_state if not resume_state.is_empty() else RunSession.STATE_RUN_ACTIVE
    session.bump_revision()
    if session.state == RunSession.STATE_RUN_VICTORY:
        clock.freeze()
    else:
        clock.start_run()
    _emit("artifact_claimed", outcome)
    return outcome


func pause(reason: String = "MANUAL") -> Dictionary:
    if session == null or session.state != RunSession.STATE_RUN_ACTIVE:
        return _fail("PAUSE_NOT_ALLOWED", "Pause requires RUN_ACTIVE.", true)
    session.resume_state = session.state
    session.pause_reason = reason
    last_coherent_snapshot = session.to_snapshot(clock.snapshot())
    last_coherent_snapshot["checksum"] = _snapshot_checksum(last_coherent_snapshot)
    clock.pause()
    session.state = RunSession.STATE_RUN_PAUSED
    session.bump_revision()
    _emit("run_paused", {
        "pause_reason": reason,
        "snapshot_revision": last_coherent_snapshot.get("state_revision", -1),
        "run_seconds": clock.run_seconds,
        "encounter_seconds": clock.encounter_seconds
    })
    return {"ok": true, "state": session.state, "snapshot": last_coherent_snapshot.duplicate(true)}


func resume_from_snapshot(snapshot: Dictionary = {}) -> Dictionary:
    if session == null or (session.state != RunSession.STATE_RUN_PAUSED and session.state != RunSession.STATE_RECOVERY_REVIEW):
        return _fail("RESUME_NOT_ALLOWED", "Resume requires RUN_PAUSED or RECOVERY_REVIEW.", true)
    var candidate := snapshot.duplicate(true) if not snapshot.is_empty() else last_coherent_snapshot.duplicate(true)
    if candidate.is_empty() or not candidate.has("checksum") or str(candidate.get("checksum", "")) != _snapshot_checksum(candidate):
        return _enter_recovery("SAVE_RESTORE_FAILED", "Snapshot checksum or shape is invalid.", {"snapshot_id": candidate.get("run_id", "")})
    var clock_snapshot: Dictionary = candidate.get("clock", {})
    if not session.restore_snapshot(candidate) or not clock.restore(clock_snapshot):
        return _enter_recovery("SAVE_RESTORE_FAILED", "Snapshot could not be restored into the active domain state.", {"snapshot_id": candidate.get("run_id", "")})
    session.state = RunSession.STATE_RUN_ACTIVE
    completed_offer_outcomes = session.completed_offer_outcomes.duplicate(true)
    completed_chest_outcomes = session.completed_chest_outcomes.duplicate(true)
    completed_artifact_outcomes = session.completed_artifact_outcomes.duplicate(true)
    artifact_refresh_outcomes = session.artifact_refresh_outcomes.duplicate(true)
    if reward_ledger != null:
        reward_ledger.entries = session.reward_ledger_entries.duplicate(true)
    session.clear_recoverable_diagnostics()
    clock.start_run()
    session.bump_revision()
    _emit("run_resumed", {"restored_revision": candidate.get("state_revision", -1), "run_seconds": clock.run_seconds})
    return {"ok": true, "state": session.state, "run_seconds": clock.run_seconds}


func recover_from_last_snapshot() -> Dictionary:
    if last_coherent_snapshot.is_empty():
        return _fail("RECOVERY_SNAPSHOT_MISSING", "No last coherent snapshot is available.", false)
    var result := resume_from_snapshot(last_coherent_snapshot)
    if bool(result.get("ok", false)):
        _emit("diagnostic_recovered", {"run_id": session.run_id, "state": session.state})
    return result


func get_clock_snapshot() -> Dictionary:
    if clock == null:
        return {}
    return clock.snapshot()


func trace_signature() -> String:
    return JSON.stringify(trace)


func trace_report() -> Dictionary:
    var state_sequence: Array[String] = []
    for event in trace:
        state_sequence.append(str(event.get("event_name", "")))
    return {
        "seed": session.seed if session != null else null,
        "content_version": session.content_version if session != null else "",
        "character": session.selected_hero_id if session != null else "",
        "state_sequence": state_sequence,
        "trace": trace.duplicate(true),
        "final_state": session.state if session != null else "NO_SESSION",
        "final_revision": session.state_revision if session != null else 0,
        "clock": get_clock_snapshot(),
        "active_boss_encounter": session.active_boss_encounter.duplicate(true) if session != null else {},
        "artifacts": session.stats.get("artifacts", []).duplicate(true) if session != null else [],
        "reward_ledger": session.reward_ledger_entries.duplicate(true) if session != null else {},
        "diagnostics": diagnostics.duplicate(true) + (session.diagnostics.duplicate(true) if session != null else [])
    }


func _maybe_open_level_up_offer() -> Dictionary:
    if session.state != RunSession.STATE_RUN_ACTIVE:
        return {"opened": false, "reason": "STATE_BLOCKED"}
    var level := int(session.stats.get("level", 1))
    var threshold := registry.get_xp_to_next(level)
    if threshold < 0:
        _record_diagnostic("LEVEL_FORMULA_UNAVAILABLE", "The registry could not evaluate the level threshold.", true, {"level": level})
        return {"opened": false, "reason": "FORMULA_ERROR"}
    if int(session.stats.get("xp", 0)) < threshold:
        return {"opened": false, "threshold": threshold}

    var choices := registry.get_upgrade_choices(session.selected_hero_id)
    var expected_choice_count := registry.get_upgrade_choice_count()
    if expected_choice_count <= 0 or choices.size() != expected_choice_count:
        _record_diagnostic("UPGRADE_OFFER_INVALID", "R1 requires the registry-defined number of data-backed choices.", true, {"choice_count": choices.size(), "expected_choice_count": expected_choice_count})
        return {"opened": false, "reason": "CHOICE_COUNT_INVALID"}

    session.stats["level"] = level + 1
    session.bump_revision()
    session.state = RunSession.STATE_UPGRADE_OFFER
    session.create_offer(choices)
    clock.pause()
    _emit("level_up", {"level": session.stats["level"], "xp_total": session.stats["xp"], "threshold": threshold})
    _emit("upgrade_offer_created", {
        "offer_id": session.pending_offer.get("offer_id", ""),
        "choice_ids": session.pending_offer.get("choice_ids", []),
        "state_revision": session.state_revision,
        "clock": clock.snapshot(),
        "source": "BALANCE_MODEL.json.simulation_model.build_catalog"
    })
    return {"opened": true, "offer": session.pending_offer.duplicate(true), "threshold": threshold}


func _is_active() -> bool:
    return session != null and session.state == RunSession.STATE_RUN_ACTIVE and clock != null


func _is_wave_progression_active() -> bool:
    return session != null and clock != null and session.state in [RunSession.STATE_RUN_ACTIVE, RunSession.STATE_MINI_BOSS_ACTIVE]


func _active_boss_kind() -> String:
    if session == null:
        return ""
    if session.state in [RunSession.STATE_MAIN_BOSS_INTRO, RunSession.STATE_MAIN_BOSS_ACTIVE, RunSession.STATE_CHECKPOINT_SETTLEMENT]:
        return BossDirectorType.KIND_MAIN
    if session.state in [RunSession.STATE_MINI_BOSS_INTRO, RunSession.STATE_MINI_BOSS_ACTIVE]:
        return BossDirectorType.KIND_MINI
    return ""


func _create_chest_offer(offer_type: String, source_id: String, settlement: Dictionary) -> Dictionary:
    if not (offer_type in ["BOSS_CHEST", "MINI_BOSS_CHEST", "ELITE_CHEST"]):
        return _fail("CHEST_TYPE_INVALID", "Chest source is not part of the runtime chest contract.", false, {"offer_type": offer_type})

    session.offer_sequence += 1
    var source_kind := _chest_source_kind(offer_type)
    session.pending_chest_offer = {
        "offer_id": "%s:chest:%d" % [session.run_id, session.offer_sequence],
        "offer_type": offer_type,
        "source_kind": source_kind,
        "source_id": source_id,
        "chest_window_id": source_id,
        "checkpoint_id": source_id,
        "created_at_revision": session.state_revision,
        "eligibility": registry.get_chest_eligibility(offer_type),
        "settlement": settlement.duplicate(true),
        "claimed": false
    }
    session.state = RunSession.STATE_BOSS_CHEST
    session.resume_state = RunSession.STATE_RUN_ACTIVE
    session.bump_revision()
    clock.pause()
    _emit("chest_offer_created", session.pending_chest_offer)
    return {"ok": true, "state": session.state, "offer": session.pending_chest_offer.duplicate(true)}


func _chest_source_kind(offer_type: String) -> String:
    if offer_type == "BOSS_CHEST":
        return "MAIN_BOSS"
    if offer_type == "MINI_BOSS_CHEST":
        return "MINI_BOSS"
    if offer_type == "ELITE_CHEST":
        return "ELITE_VARIANT"
    return "UNKNOWN"


func _apply_wallet_reward(reward: Dictionary) -> void:
    var wallet: Dictionary = session.stats.get("wallet", {})
    for wallet_id in ["gold", "moon_seals", "boss_essence"]:
        var value: Variant = reward.get(wallet_id, 0)
        if typeof(value) == TYPE_INT or typeof(value) == TYPE_FLOAT:
            wallet[wallet_id] = int(wallet.get(wallet_id, 0)) + int(value)
    session.stats["wallet"] = wallet


func _hero_hp(profile: Dictionary) -> float:
    if profile.has("canonical_hp"):
        return float(profile.get("canonical_hp", 0.0))
    return _nested_numeric(profile.get("hp", {}), 0.0)


func _hero_move_speed(profile: Dictionary) -> float:
    if profile.has("canonical_move_speed_percent"):
        return float(profile.get("canonical_move_speed_percent", 0.0))
    return _nested_numeric(profile.get("move_speed_percent", {}), 0.0)


func _nested_numeric(value: Variant, fallback: float) -> float:
    if value is Dictionary:
        var nested: Variant = value.get("value", fallback)
        if typeof(nested) == TYPE_INT or typeof(nested) == TYPE_FLOAT:
            return float(nested)
    if typeof(value) == TYPE_INT or typeof(value) == TYPE_FLOAT:
        return float(value)
    return fallback


func _base_numeric_value(path: Array[String], fallback: float) -> float:
    return _nested_numeric(registry.get_model_field(path, {}), fallback)


func _snapshot_checksum(snapshot: Dictionary) -> String:
    return "%s|%s|%s|%d|%.3f|%.3f" % [
        str(snapshot.get("run_id", "")),
        str(snapshot.get("content_version", "")),
        str(snapshot.get("state", "")),
        int(snapshot.get("state_revision", -1)),
        float(snapshot.get("clock", {}).get("run_seconds", -1.0)),
        float(snapshot.get("clock", {}).get("encounter_seconds", -1.0))
    ]


func _enter_recovery(code: String, message: String, details: Dictionary) -> Dictionary:
    session.state = RunSession.STATE_RECOVERY_REVIEW
    session.record_diagnostic(code, message, true, details)
    clock.pause()
    _emit("save_restore_failed", {"code": code, "message": message, "details": details})
    return {"ok": false, "code": code, "state": session.state, "recoverable": true}


func _record_diagnostic(code: String, message: String, recoverable: bool, details: Dictionary = {}) -> void:
    var diagnostic := {"code": code, "message": message, "recoverable": recoverable, "details": details.duplicate(true)}
    diagnostics.append(diagnostic)
    if session != null:
        session.record_diagnostic(code, message, recoverable, details)
    _emit("diagnostic", diagnostic)


func _fail(code: String, message: String, recoverable: bool, details: Dictionary = {}) -> Dictionary:
    _record_diagnostic(code, message, recoverable, details)
    return {"ok": false, "code": code, "message": message, "recoverable": recoverable, "details": details}


func _remember_start(client_request_id: String, outcome: Dictionary) -> void:
    if not client_request_id.is_empty():
        start_outcomes[client_request_id] = outcome.duplicate(true)


func _emit(event_name: String, payload: Dictionary = {}) -> void:
    var event := {
        "event_name": event_name,
        "event_version": 1,
        "run_id": session.run_id if session != null else "",
        "state_revision": session.state_revision if session != null else 0,
        "payload": payload.duplicate(true)
    }
    trace.append(event)
