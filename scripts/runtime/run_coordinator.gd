extends RefCounted
class_name RunCoordinator

const ContentRegistryType = preload("res://scripts/runtime/content_registry.gd")
const RunSessionType = preload("res://scripts/runtime/run_session.gd")
const SimulationClockType = preload("res://scripts/runtime/simulation_clock.gd")

## R1 orchestration boundary.
##
## Commands enter here, domain state is changed on RunSession, and every
## accepted mutation emits a deterministic trace event. The combat path is a
## deliberately small fixture backed by BALANCE_MODEL.json's explicit
## simulation_model records; the trace keeps that proposed status visible.

var registry: ContentRegistry
var session: RunSession
var clock: SimulationClock
var trace: Array[Dictionary] = []
var diagnostics: Array[Dictionary] = []
var start_outcomes: Dictionary = {}
var completed_offer_outcomes: Dictionary = {}
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
    _emit("content_loaded", {
        "content_version": registry.content_version,
        "model_id": result.get("model_id", ""),
        "model_status": result.get("model_status", ""),
        "source_path": content_path
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
        "artifacts": [],
        "level": 1,
        "xp": 0,
        "elapsed_time": 0.0,
        "current_wave_band": str(initial_wave.get("wave_band_id", "")),
        "enemies_defeated": 0,
        "active_enemy_count": 0,
        "bonus_state": {},
        "checkpoint_rewards": [],
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
    if session.state == RunSession.STATE_RUN_ACTIVE and result.get("advanced", false):
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
    if not _is_active():
        return _fail("RUN_NOT_ACTIVE", "Wave fixture requires RUN_ACTIVE.", true)
    if not session.active_enemy.is_empty():
        return {
            "ok": true,
            "duplicate": true,
            "enemy_id": session.active_enemy.get("enemy_id", ""),
            "active_enemy": session.active_enemy.duplicate(true)
        }

    var band := registry.get_wave_band_for_time(clock.run_seconds)
    if band.is_empty():
        return _fail("WAVE_BAND_NOT_FOUND", "No wave band matches the current run clock.", true)
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
    if not _is_active():
        return _fail("RUN_NOT_ACTIVE", "Combat fixture requires RUN_ACTIVE.", true)
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

    if session.state != RunSession.STATE_RUN_ACTIVE:
        return _fail("XP_COLLECTION_BLOCKED", "XP collection is blocked outside RUN_ACTIVE.", true)

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
