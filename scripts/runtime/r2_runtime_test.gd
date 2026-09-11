extends SceneTree

const RunCoordinatorType = preload("res://scripts/runtime/run_coordinator.gd")

var failures: Array[String] = []
var blockers: Array[String] = []
var policy_trace: Array[Dictionary] = []
var content_status: Dictionary = {}


func _init() -> void:
    var coordinator: Variant = RunCoordinatorType.new()
    var boot := coordinator.boot()
    _check(bool(boot.get("ok", false)), "R2 registry boots")
    if not bool(boot.get("ok", false)):
        _finish("BLOCKED")
        return

    content_status = coordinator.registry.get_r2_content_status()
    _check(str(content_status.get("status", "")) in ["READY", "PENDING_CONTENT_SYNC"], "R2 content status is explicit")
    _require_contract(content_status, "target_main_boss_count", 6)
    _require_contract(content_status, "target_mini_boss_count", 5)
    _require_contract(content_status, "target_duration_seconds", 1800.0)
    _require_contract(content_status, "available_main_boss_count", 6)
    _require_contract(content_status, "available_mini_boss_count", 5)
    _require_contract(content_status, "available_elite_variant_count", 10)

    if str(content_status.get("status", "")) != "READY":
        for blocker in content_status.get("blockers", []):
            blockers.append(str(blocker))

    _test_wave_admission(coordinator)
    _test_main_boss_freeze_and_duplicate(coordinator)
    _test_mini_boss_missing_is_explicit(coordinator)
    _test_elite_resolution()
    _finish("BLOCKED" if not blockers.is_empty() else "TESTED")


func _test_wave_admission(coordinator: Variant) -> void:
    var started: Dictionary = coordinator.start_run("hero_lin_yue", 101, "r2-wave")
    _check(bool(started.get("ok", false)), "R2 fixture run starts")
    if not bool(started.get("ok", false)):
        return
    var admission: Dictionary = coordinator.wave_director.evaluate_spawn(0.0, "", 0, 1)
    _check(bool(admission.get("ok", false)) and bool(admission.get("admitted", false)), "Wave admission uses registry band and active cap")
    _check(not str(admission.get("wave_band_id", "")).is_empty(), "Wave admission returns source band ID")
    policy_trace.append({
        "policy": "ordinary_wave",
        "run_seconds": 0.0,
        "wave_band_id": admission.get("wave_band_id", ""),
        "active_cap": admission.get("active_cap", null),
        "spawn_budget_per_second": admission.get("spawn_budget_per_second", null),
        "admitted": admission.get("admitted", false)
    })
    var cap: int = int(admission.get("active_cap", 0))
    var rejected: Dictionary = coordinator.wave_director.evaluate_spawn(0.0, "", cap, 1)
    _check(str(rejected.get("code", "")) == "ACTIVE_CAP_REACHED", "Wave admission rejects an occupied active cap")


func _test_main_boss_freeze_and_duplicate(coordinator: Variant) -> void:
    var mains: Array[Dictionary] = coordinator.registry.get_main_bosses()
    _check(mains.size() > 0, "At least one main-boss record is available")
    if mains.is_empty():
        return
    var checkpoint_id := str(mains.back().get("checkpoint_id", ""))
    if checkpoint_id.is_empty():
        _check(false, "Main-boss record exposes a checkpoint ID")
        return
    var started: Dictionary = coordinator.start_main_boss(checkpoint_id)
    _check(bool(started.get("ok", false)), "Main boss starts from registry content")
    if not bool(started.get("ok", false)):
        return
    var run_before := coordinator.clock.run_seconds
    coordinator.advance(2.0)
    _check(is_equal_approx(coordinator.clock.run_seconds, run_before), "Main boss freezes run clock")
    _check(is_equal_approx(coordinator.clock.encounter_seconds, 2.0), "Main boss advances encounter clock")
    var outcome: Dictionary = coordinator.defeat_active_boss()
    _check(bool(outcome.get("ok", false)), "Main boss defeat settles through the ledger")
    var duplicate: Dictionary = coordinator.defeat_active_boss()
    _check(bool(duplicate.get("duplicate", false)), "Repeated boss defeat returns stored outcome")
    var settlement_duplicate: Dictionary = coordinator.settle_checkpoint()
    _check(bool(settlement_duplicate.get("duplicate", false)), "Repeated checkpoint settlement returns stored outcome")
    policy_trace.append({
        "policy": "main_boss",
        "run_before": run_before,
        "run_after": coordinator.clock.run_seconds,
        "encounter_after": coordinator.clock.encounter_seconds,
        "outcome_type": outcome.get("offer", {}).get("offer_type", "FINAL_SETTLEMENT"),
        "duplicate": duplicate.get("duplicate", false),
        "settlement_duplicate": settlement_duplicate.get("duplicate", false)
    })

    if mains.size() < 2:
        return
    var chest_coordinator: Variant = RunCoordinatorType.new()
    _check(bool(chest_coordinator.boot().get("ok", false)), "Non-final chest registry boots")
    _check(bool(chest_coordinator.start_run("hero_lin_yue", 202, "r2-chest").get("ok", false)), "Non-final chest run starts")
    var non_final_checkpoint := str(mains[0].get("checkpoint_id", ""))
    var non_final_start: Dictionary = chest_coordinator.start_main_boss(non_final_checkpoint)
    _check(bool(non_final_start.get("ok", false)), "Non-final main boss starts")
    if not bool(non_final_start.get("ok", false)):
        return
    var chest_result: Dictionary = chest_coordinator.defeat_active_boss()
    var chest_offer: Dictionary = chest_result.get("offer", {})
    _check(str(chest_offer.get("offer_type", "")) == "BOSS_CHEST", "Non-final main boss creates a boss chest")
    _check(str(chest_offer.get("source_kind", "")) == "MAIN_BOSS", "Main boss chest keeps its source kind")
    var chest_claim: Dictionary = chest_coordinator.claim_chest(
        str(chest_offer.get("offer_id", "")),
        int(chest_offer.get("created_at_revision", -1))
    )
    _check(bool(chest_claim.get("ok", false)), "Non-final boss chest claim succeeds")
    var duplicate_chest_claim: Dictionary = chest_coordinator.claim_chest(
        str(chest_offer.get("offer_id", "")),
        int(chest_offer.get("created_at_revision", -1))
    )
    _check(bool(duplicate_chest_claim.get("duplicate", false)), "Chest claim is idempotent")


func _test_mini_boss_missing_is_explicit(coordinator: Variant) -> void:
    var minis: Array[Dictionary] = coordinator.registry.get_mini_bosses()
    if minis.is_empty():
        var result: Dictionary = coordinator.start_mini_boss("pending-mini-boss")
        _check(str(result.get("code", "")) == "MINI_BOSS_CONTENT_PENDING", "Missing mini-boss roster is explicit and does not invent an encounter")
        return

    var mini_coordinator: Variant = RunCoordinatorType.new()
    _check(bool(mini_coordinator.boot().get("ok", false)), "Mini-boss registry boots")
    _check(bool(mini_coordinator.start_run("hero_lin_yue", 303, "r2-mini").get("ok", false)), "Mini-boss run starts")
    var mini_id := str(minis[0].get("boss_id", minis[0].get("mini_boss_id", minis[0].get("id", ""))))
    var mini_started: Dictionary = mini_coordinator.start_mini_boss(mini_id)
    if not bool(coordinator.registry.is_runtime_record_ready(minis[0])):
        _check(
            str(mini_started.get("code", "")) == "MINI_BOSS_CONTENT_PENDING",
            "Pending mini-boss record is visible but cannot start"
        )
        return
    _check(bool(mini_started.get("ok", false)), "Mini boss starts from registry content")
    if not bool(mini_started.get("ok", false)):
        return
    var run_before := mini_coordinator.clock.run_seconds
    mini_coordinator.advance(2.0)
    _check(mini_coordinator.clock.run_seconds > run_before, "Mini boss keeps run clock moving")
    _check(mini_coordinator.clock.encounter_seconds > 0.0, "Mini boss advances encounter clock")
    var mini_wave: Dictionary = mini_coordinator.wave_director.resolve(mini_coordinator.clock.run_seconds, "MINI_BOSS")
    _check(bool(mini_wave.get("ok", false)) and str(mini_wave.get("phase", "")) == "MINI_BOSS_PRESSURE", "Mini boss keeps ordinary wave pressure active")
    var mini_result: Dictionary = mini_coordinator.defeat_active_boss()
    var mini_offer: Dictionary = mini_result.get("offer", {})
    _check(str(mini_offer.get("offer_type", "")) == "MINI_BOSS_CHEST", "Mini boss creates a separate chest")
    var mini_claim: Dictionary = mini_coordinator.claim_chest(
        str(mini_offer.get("offer_id", "")),
        int(mini_offer.get("created_at_revision", -1))
    )
    _check(bool(mini_claim.get("ok", false)), "Mini-boss chest claim resumes the run")


func _test_elite_resolution() -> void:
    var coordinator: Variant = RunCoordinatorType.new()
    var boot: Dictionary = coordinator.boot()
    if not bool(boot.get("ok", false)):
        return
    var started: Dictionary = coordinator.start_run("hero_lin_yue", 505, "r2-elite")
    _check(bool(started.get("ok", false)), "Elite resolver fixture run starts")
    if not bool(started.get("ok", false)):
        return

    var first: Dictionary = coordinator.resolve_elite_variant_event()
    var second: Dictionary = coordinator.resolve_elite_variant_event(
        str(coordinator.session.current_wave_band_id),
        coordinator.session.state_revision
    )
    policy_trace.append({
        "policy": "finite_elite_pressure",
        "first": first,
        "second": second
    })
    if not bool(first.get("ok", false)):
        _check(
            str(first.get("code", "")) == "ELITE_VARIANT_CONTENT_PENDING",
            "Pending elite records remain an explicit resolver blocker"
        )
        return

    var first_ids: Array[String] = []
    var second_ids: Array[String] = []
    for variant in first.get("variants", []):
        first_ids.append(str(variant.get("variant_id", "")))
    for variant in second.get("variants", []):
        second_ids.append(str(variant.get("variant_id", "")))
    _check(first_ids == second_ids, "Elite resolution is deterministic for the same seed and revision")
    _check(first_ids.size() <= 5, "Elite selection stays within the maximum five")
    _check(
        not bool(first.get("automatic_artifact_offer", true)),
        "Elite resolution does not open an artifact offer"
    )
    _check(
        not bool(first.get("persistent_roster_mutation", true)),
        "Elite resolution does not mutate a permanent roster"
    )


func _require_contract(value: Dictionary, key: String, expected: Variant) -> void:
    _check(value.has(key), "R2 content status exposes %s" % key)
    if value.has(key):
        _check(value.get(key) == expected, "R2 content status keeps %s canonical" % key)


func _finish(status: String) -> void:
    var result := {
        "ok": failures.is_empty() and blockers.is_empty(),
        "status": status,
        "failures": failures,
        "blockers": blockers,
        "content_status": content_status,
        "policy_trace": policy_trace
    }
    print("R2_RUNTIME_TEST " + JSON.stringify(result))
    quit(0 if result["ok"] else 1)


func _check(condition: bool, label: String) -> void:
    if not condition:
        failures.append(label)
