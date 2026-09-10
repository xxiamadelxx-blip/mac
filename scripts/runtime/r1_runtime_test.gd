extends SceneTree

const ContentRegistryType = preload("res://scripts/runtime/content_registry.gd")
const RunCoordinatorType = preload("res://scripts/runtime/run_coordinator.gd")
const RunSessionType = preload("res://scripts/runtime/run_session.gd")
const SimulationClockType = preload("res://scripts/runtime/simulation_clock.gd")
const WaveDirectorType = preload("res://scripts/runtime/wave_director.gd")

var failures: Array[String] = []


func _init() -> void:
    _run_acceptance_fixture()
    var r_ref_01_report := _run_ref_r01()
    for failure in r_ref_01_report.get("failures", []):
        failures.append("R-REF-01: %s" % str(failure))
    var result := {
        "ok": failures.is_empty(),
        "failures": failures,
        "r_ref_01": r_ref_01_report
    }
    print("R1_RUNTIME_TEST " + JSON.stringify(result))
    quit(0 if failures.is_empty() else 1)


func _run_acceptance_fixture() -> void:
    var coordinator: Variant = RunCoordinatorType.new()
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
    var frozen_run_seconds: float = float(coordinator.clock.run_seconds)
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
    var paused_seconds: float = float(coordinator.clock.run_seconds)
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
    var coordinator: Variant = RunCoordinatorType.new()
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


func _run_ref_r01() -> Dictionary:
    var ref_failures: Array[String] = []
    var report := {
        "task_id": "REF-RUNTIME-01",
        "slice": "R-REF-01",
        "registry_source": "res://docs/agents/balance-economy/BALANCE_MODEL.json",
        "failures": ref_failures
    }
    var registry: Variant = ContentRegistryType.new()
    var boot: Dictionary = registry.load_and_validate()
    _ref_check(ref_failures, bool(boot.get("ok", false)), "Content Registry loads for R-REF-01")
    if not bool(boot.get("ok", false)):
        report["ok"] = false
        return report

    var wave_bands: Variant = registry.get_model_field(["wave_bands"], [])
    var main_bosses: Array[Dictionary] = registry.get_main_bosses()
    report["registry"] = {
        "wave_band_count": wave_bands.size() if wave_bands is Array else 0,
        "main_boss_count": main_bosses.size(),
        "r2_content_status": registry.get_r2_content_status()
    }
    _ref_check(ref_failures, wave_bands is Array and wave_bands.size() > 0, "Current registry exposes wave bands")
    _ref_check(ref_failures, main_bosses.size() >= 2, "Current registry exposes two ordered main checkpoints")
    if main_bosses.size() < 2:
        report["ok"] = false
        return report

    var from_checkpoint_id := str(main_bosses[0].get("checkpoint_id", ""))
    var to_checkpoint_id := str(main_bosses[1].get("checkpoint_id", ""))
    var wave: Variant = WaveDirectorType.new(registry)
    var cycle: Dictionary = wave.begin_post_boss_cycle(from_checkpoint_id, to_checkpoint_id)
    _ref_check(ref_failures, bool(cycle.get("ok", false)), "WaveDirector binds the registry cycle mapping")
    if not bool(cycle.get("ok", false)):
        report["ok"] = false
        return report

    var cycle_start := float(cycle.get("cycle", {}).get("start_seconds", -1.0))
    var current_band: Dictionary = registry.get_wave_band_for_time(cycle_start)
    var spawn_rate := _ref_number(current_band.get("spawn_budget_per_second", 0), 0.0)
    var active_cap := int(_ref_number(current_band.get("active_cap", 0), 0.0))
    _ref_check(ref_failures, not current_band.is_empty(), "Cycle start resolves a current registry band")
    _ref_check(ref_failures, spawn_rate > 0.0, "Spawn interval comes from the current registry budget")
    _ref_check(ref_failures, active_cap > 0, "Active cap comes from the current registry band")
    if current_band.is_empty() or spawn_rate <= 0.0 or active_cap <= 0:
        report["ok"] = false
        return report

    var interval := 1.0 / spawn_rate
    var half_interval := interval / 2.0
    var first_tick: Dictionary = wave.advance(cycle_start, half_interval, "", 0, 1)
    var second_tick: Dictionary = wave.advance(cycle_start + half_interval, half_interval, "", 0, 1)
    _ref_check(ref_failures, str(first_tick.get("code", "")) == "SPAWN_TIMER_NOT_READY", "Enemy timer has its own not-ready boundary")
    _ref_check(ref_failures, bool(second_tick.get("admitted", false)), "Enemy timer admits after its registry-derived interval")
    _ref_check(
        ref_failures,
        float(first_tick.get("timers_after", {}).get("enemy_seconds", -1.0)) > 0.0
            and is_equal_approx(float(first_tick.get("timers_after", {}).get("wave_seconds", -1.0)), 0.0)
            and float(first_tick.get("timers_after", {}).get("ramp_seconds", -1.0)) > 0.0,
        "Enemy, wave and ramp timers remain independent"
    )
    _ref_check(
        ref_failures,
        float(second_tick.get("timer_consumed_seconds", 0.0)) > 0.0
            and float(second_tick.get("timers_after", {}).get("wave_seconds", -1.0)) > 0.0
            and float(second_tick.get("timers_after", {}).get("ramp_seconds", -1.0)) > 0.0,
        "Spawn admission consumes only the enemy timer"
    )

    var timers_before_main: Dictionary = wave.get_timer_snapshot().get("timers", {}).duplicate(true)
    var main_tick: Dictionary = wave.advance(cycle_start + half_interval, 2.0, "MAIN_BOSS", 0, 1)
    var timers_after_main: Dictionary = wave.get_timer_snapshot().get("timers", {}).duplicate(true)
    _ref_check(ref_failures, str(main_tick.get("phase", "")) == "MAIN_BOSS_FREEZE", "MAIN_BOSS selects the freeze phase")
    _ref_check(ref_failures, str(main_tick.get("code", "")) == "WAVE_PROGRESSION_BLOCKED", "MAIN_BOSS blocks ordinary admission")
    _ref_check(ref_failures, _ref_timers_equal(timers_before_main, timers_after_main), "MAIN_BOSS does not consume ordinary timers")

    var cap_tick: Dictionary = wave.advance(cycle_start + half_interval, interval, "", active_cap, 1)
    _ref_check(ref_failures, str(cap_tick.get("code", "")) == "ACTIVE_CAP_REACHED", "Active cap rejects a due ordinary spawn")
    _ref_check(ref_failures, is_equal_approx(float(cap_tick.get("timer_consumed_seconds", 0.0)), 0.0), "Cap rejection does not consume the enemy timer")

    var mini_before: Dictionary = wave.get_timer_snapshot().get("timers", {}).duplicate(true)
    var mini_tick: Dictionary = wave.advance(cycle_start + interval, half_interval, "MINI_BOSS", 0, 1)
    var mini_after: Dictionary = wave.get_timer_snapshot().get("timers", {}).duplicate(true)
    _ref_check(ref_failures, str(mini_tick.get("phase", "")) == "MINI_BOSS_PRESSURE", "MINI_BOSS selects the pressure phase")
    _ref_check(ref_failures, not bool(mini_tick.get("paused", true)), "MINI_BOSS leaves ordinary pressure unpaused")
    _ref_check(
        ref_failures,
        float(mini_after.get("wave_seconds", -1.0)) > float(mini_before.get("wave_seconds", -1.0))
            and float(mini_after.get("ramp_seconds", -1.0)) > float(mini_before.get("ramp_seconds", -1.0)),
        "MINI_BOSS advances wave and ramp timers"
    )

    var main_policy := wave.resolve(cycle_start, "MAIN_BOSS")
    var mini_policy := wave.resolve(cycle_start, "MINI_BOSS")
    _ref_check(ref_failures, bool(main_policy.get("paused", false)), "Wave policy freezes under MAIN_BOSS")
    _ref_check(ref_failures, not bool(mini_policy.get("paused", true)), "Wave policy continues under MINI_BOSS")

    var clock := SimulationClockType.new()
    clock.start_run()
    clock.advance(1.0)
    var run_before_main := clock.run_seconds
    clock.start_encounter()
    clock.advance(2.0)
    _ref_check(ref_failures, is_equal_approx(clock.run_seconds, run_before_main), "SimulationClock freezes run time for MAIN_BOSS")
    _ref_check(ref_failures, is_equal_approx(clock.encounter_seconds, 2.0), "SimulationClock advances the encounter clock")

    clock.start_run()
    clock.advance(1.0)
    var run_before_mini := clock.run_seconds
    clock.start_mini_boss()
    clock.advance(2.0)
    _ref_check(ref_failures, clock.run_seconds > run_before_mini, "SimulationClock continues run time for MINI_BOSS")
    _ref_check(ref_failures, clock.encounter_seconds > 0.0, "SimulationClock advances MINI_BOSS encounter time")

    var arena_scene_path := "res://scenes/arena/arena.tscn"
    var arena_scene: Variant = ResourceLoader.load(arena_scene_path)
    _ref_check(ref_failures, ResourceLoader.exists(arena_scene_path), "Arena scene path resolves")
    _ref_check(ref_failures, arena_scene is PackedScene, "Arena scene loads as PackedScene")
    if arena_scene is PackedScene:
        var instance: Node = arena_scene.instantiate()
        _ref_check(ref_failures, instance != null, "Arena scene instantiates")
        if instance != null:
            instance.free()

    var asset_paths: Array[String] = [
        "res://docs/mockups/02-arena/layers/STAGE02_ARENA_OPEN_FIELD_ART_v02.png",
        "res://docs/mockups/02-arena/layers/STAGE02_ARENA_AMBIENT_VFX_v01.png"
    ]
    for path in asset_paths:
        _ref_check(ref_failures, ResourceLoader.exists(path), "Asset path resolves: %s" % path)
        var resource: Variant = ResourceLoader.load(path)
        _ref_check(ref_failures, resource != null, "Asset resource loads: %s" % path)

    report["evidence"] = {
        "cycle": cycle.get("cycle", {}),
        "first_tick": first_tick,
        "second_tick": second_tick,
        "main_tick": main_tick,
        "cap_tick": cap_tick,
        "mini_tick": mini_tick,
        "main_policy": main_policy,
        "mini_policy": mini_policy,
        "asset_paths": asset_paths
    }
    report["ok"] = ref_failures.is_empty()
    return report


func _ref_check(ref_failures: Array[String], condition: bool, label: String) -> void:
    if not condition:
        ref_failures.append(label)


func _ref_number(record: Variant, fallback: float) -> float:
    if record is Dictionary:
        var value: Variant = record.get("value", null)
        if typeof(value) == TYPE_INT or typeof(value) == TYPE_FLOAT:
            return float(value)
        return fallback
    if typeof(record) == TYPE_INT or typeof(record) == TYPE_FLOAT:
        return float(record)
    return fallback


func _ref_timers_equal(left: Dictionary, right: Dictionary) -> bool:
    for key in ["enemy_seconds", "wave_seconds", "ramp_seconds"]:
        if not is_equal_approx(float(left.get(key, -1.0)), float(right.get(key, -1.0))):
            return false
    return true
