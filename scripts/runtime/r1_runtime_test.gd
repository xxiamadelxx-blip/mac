extends SceneTree

const ContentRegistryType = preload("res://scripts/runtime/content_registry.gd")
const RunCoordinatorType = preload("res://scripts/runtime/run_coordinator.gd")
const RunSessionType = preload("res://scripts/runtime/run_session.gd")
const SimulationClockType = preload("res://scripts/runtime/simulation_clock.gd")

var failures: Array[String] = []


func _init() -> void:
    _run_acceptance_fixture()
    var result := {"ok": failures.is_empty(), "failures": failures}
    print("R1_RUNTIME_TEST " + JSON.stringify(result))
    quit(0 if failures.is_empty() else 1)


func _run_acceptance_fixture() -> void:
    var coordinator := RunCoordinatorType.new()
    var boot_result: Dictionary = coordinator.boot()
    _check(bool(boot_result.get("ok", false)), "Content Registry boots BALANCE_MODEL.json")
    _check(not coordinator.registry.content_version.is_empty(), "Registry derives a content version")
    _check(coordinator.registry.get_wave_band_for_time(0.0).has("wave_band_id"), "Registry resolves the first wave band")
    _check(coordinator.registry.get_upgrade_choice_count() == coordinator.registry.get_upgrade_choices("hero_lin_yue").size(), "Registry exposes its offer cardinality")

    var start_result: Dictionary = coordinator.start_run("hero_lin_yue", 101, "test-start")
    var duplicate_start: Dictionary = coordinator.start_run("hero_lin_yue", 101, "test-start")
    _check(bool(start_result.get("ok", false)), "RunCoordinator creates one RunSession")
    _check(bool(duplicate_start.get("duplicate", false)), "Duplicate start is idempotent")
    _check(coordinator.session.state == RunSessionType.STATE_RUN_ACTIVE, "RunSession enters RUN_ACTIVE")

    var first_spawn: Dictionary = coordinator.spawn_wave_fixture()
    _check(bool(first_spawn.get("ok", false)), "Wave fixture is loaded from the Registry")
    var first_hit: Dictionary = coordinator.resolve_fixture_attack()
    var duplicate_hit: Dictionary = coordinator.resolve_fixture_attack()
    _check(bool(first_hit.get("ok", false)), "Combat fixture applies Registry weapon damage")
    _check(str(duplicate_hit.get("code", "")) == "HIT_COOLDOWN", "Contact hit cooldown rejects same-frame repeat")

    coordinator.advance(coordinator.registry.get_contact_damage_cooldown())
    var defeat_hit: Dictionary = coordinator.resolve_fixture_attack()
    _check(bool(defeat_hit.get("defeated", false)), "Combat fixture produces a defeat")
    var drop: Dictionary = defeat_hit.get("drop", {})
    var xp_before := int(coordinator.session.stats.get("xp", 0))
    var collect_result: Dictionary = coordinator.collect_xp(str(drop.get("xp_item_id", "")))
    var duplicate_collect: Dictionary = coordinator.collect_xp(str(drop.get("xp_item_id", "")))
    _check(bool(collect_result.get("ok", false)), "XP drop is collected exactly once")
    _check(bool(duplicate_collect.get("duplicate", false)), "Duplicate XP pickup is idempotent")
    _check(int(coordinator.session.stats.get("xp", 0)) == xp_before + int(drop.get("value", 0)), "Duplicate XP pickup does not double the award")

    var loop_count := 0
    while coordinator.session.state == RunSessionType.STATE_RUN_ACTIVE and loop_count < 128:
        loop_count += 1
        coordinator.spawn_wave_fixture()
        var hit_result: Dictionary = coordinator.resolve_fixture_attack()
        if str(hit_result.get("code", "")) == "HIT_COOLDOWN":
            coordinator.advance(coordinator.registry.get_contact_damage_cooldown())
            hit_result = coordinator.resolve_fixture_attack()
        if bool(hit_result.get("defeated", false)):
            var next_drop: Dictionary = hit_result.get("drop", {})
            coordinator.collect_xp(str(next_drop.get("xp_item_id", "")))
        elif bool(hit_result.get("ok", false)):
            coordinator.advance(coordinator.registry.get_contact_damage_cooldown())

    _check(coordinator.session.state == RunSessionType.STATE_UPGRADE_OFFER, "XP pickup opens a blocking level-up offer")
    var offer: Dictionary = coordinator.session.pending_offer.duplicate(true)
    _check(offer.get("choice_ids", []).size() == coordinator.registry.get_upgrade_choice_count(), "Upgrade offer uses Registry-defined choice count")
    var frozen_run_seconds := coordinator.clock.run_seconds
    coordinator.advance(coordinator.registry.get_contact_damage_cooldown())
    _check(is_equal_approx(coordinator.clock.run_seconds, frozen_run_seconds), "Level-up offer freezes the run clock")

    var choice_ids: Array = offer.get("choice_ids", [])
    if not offer.is_empty() and not choice_ids.is_empty():
        var claim_result: Dictionary = coordinator.claim_upgrade(
            str(offer.get("offer_id", "")),
            str(choice_ids[0]),
            int(offer.get("created_at_revision", -1))
        )
        var duplicate_claim: Dictionary = coordinator.claim_upgrade(
            str(offer.get("offer_id", "")),
            str(choice_ids[0]),
            int(offer.get("created_at_revision", -1))
        )
        _check(bool(claim_result.get("ok", false)), "Upgrade claim resumes the run")
        _check(bool(duplicate_claim.get("duplicate", false)), "Duplicate upgrade claim is idempotent")
        _check(coordinator.session.state == RunSessionType.STATE_RUN_ACTIVE, "Claim returns to RUN_ACTIVE")

    var pause_result: Dictionary = coordinator.pause("R1_TEST")
    _check(bool(pause_result.get("ok", false)), "Pause creates a coherent snapshot")
    var paused_seconds := coordinator.clock.run_seconds
    coordinator.advance(coordinator.registry.get_contact_damage_cooldown())
    _check(is_equal_approx(coordinator.clock.run_seconds, paused_seconds), "Paused run clock does not advance")
    var resume_result: Dictionary = coordinator.resume_from_snapshot(pause_result.get("snapshot", {}))
    _check(bool(resume_result.get("ok", false)), "Valid snapshot resumes the run")

    var invalid_pause: Dictionary = coordinator.pause("R1_INVALID_SNAPSHOT_TEST")
    var invalid_snapshot: Dictionary = invalid_pause.get("snapshot", {}).duplicate(true)
    invalid_snapshot["checksum"] = "corrupted"
    var recovery_result: Dictionary = coordinator.resume_from_snapshot(invalid_snapshot)
    _check(str(recovery_result.get("state", "")) == RunSessionType.STATE_RECOVERY_REVIEW, "Invalid snapshot enters recovery review")
    var recovered: Dictionary = coordinator.recover_from_last_snapshot()
    _check(bool(recovered.get("ok", false)), "Last coherent snapshot recovers the run")

    var clock := SimulationClockType.new()
    clock.start_run()
    clock.advance(1.0)
    clock.start_encounter()
    clock.advance(2.0)
    _check(is_equal_approx(clock.run_seconds, 1.0), "Encounter clock does not advance visible run time")
    _check(is_equal_approx(clock.encounter_seconds, 2.0), "Encounter clock advances independently")

    var first_trace := _run_deterministic_trace(101)
    var second_trace := _run_deterministic_trace(101)
    _check(first_trace == second_trace, "Same seed and command trace are deterministic")


func _run_deterministic_trace(seed: int) -> String:
    var coordinator := RunCoordinatorType.new()
    coordinator.boot()
    coordinator.start_run("hero_lin_yue", seed, "determinism-start")
    coordinator.spawn_wave_fixture()
    coordinator.resolve_fixture_attack()
    coordinator.advance(coordinator.registry.get_contact_damage_cooldown())
    coordinator.resolve_fixture_attack()
    return coordinator.trace_signature()


func _check(condition: bool, label: String) -> void:
    if not condition:
        failures.append(label)
