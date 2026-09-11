extends SceneTree

const RunCoordinatorType = preload("res://scripts/runtime/run_coordinator.gd")

var failures: Array[String] = []
var blockers: Array[String] = []
var policy_trace: Array[Dictionary] = []
var seed_traces: Array[Dictionary] = []
var content_status: Dictionary = {}


func _init() -> void:
    var registry_coordinator: Variant = RunCoordinatorType.new()
    var boot := registry_coordinator.boot()
    _check(bool(boot.get("ok", false)), "R2 registry boots from BALANCE_MODEL.json")
    if not bool(boot.get("ok", false)):
        _finish("BLOCKED")
        return

    content_status = registry_coordinator.registry.get_r2_content_status()
    _check(str(content_status.get("status", "")) == "READY", "R2 content and live registry join are ready")
    _require_contract(content_status, "target_main_boss_count", 6)
    _require_contract(content_status, "target_mini_boss_count", 5)
    _require_contract(content_status, "target_duration_seconds", 1800.0)
    if str(content_status.get("status", "")) != "READY":
        for blocker in content_status.get("blockers", []):
            blockers.append(str(blocker))

    var join_status: Dictionary = content_status.get("live_registry_join", {})
    _check(str(join_status.get("status", "")) == "READY", "Balance model joins the live architecture registry")
    _test_registry_join(registry_coordinator, join_status)
    _test_wave_admission()
    _test_main_boss_freeze_and_duplicate()
    _test_all_mini_bosses()
    _test_elite_projection(registry_coordinator)
    _finish("BLOCKED" if not blockers.is_empty() else "TESTED")


func _test_registry_join(coordinator: Variant, join_status: Dictionary) -> void:
    var counts: Dictionary = join_status.get("counts", {})
    _check(int(counts.get("main_bosses", -1)) == 6, "Live join exposes six main bosses")
    _check(int(counts.get("mini_bosses", -1)) == 5, "Live join exposes five mini bosses")
    _check(int(counts.get("ordinary", -1)) == 10, "Live join exposes ten ordinary enemies")
    _check(int(counts.get("elite", -1)) == 10, "Live join exposes ten elite catalog records")
    _check(int(counts.get("legacy", -1)) == 2, "Live join keeps two legacy records separate")
    _check(int(counts.get("chest_windows", -1)) == 15, "Live join exposes fifteen typed chest windows")
    _check(int(counts.get("boss_chest_windows", -1)) == 10, "Live join exposes ten non-final boss chest windows")
    _check(int(counts.get("elite_chest_windows", -1)) == 5, "Live join exposes five reserved elite chest windows")

    var clock_policy: Dictionary = join_status.get("clock_policy", {})
    _check(bool(clock_policy.get("main_boss_freezes", false)), "Live architecture policy freezes main-boss visible time")
    _check(bool(clock_policy.get("mini_boss_continues", false)), "Live architecture policy keeps mini-boss time moving")

    var ordinary_ids: Array = join_status.get("ids", {}).get("ordinary", [])
    var elite_ids: Array = join_status.get("ids", {}).get("elite", [])
    var legacy_ids: Array = join_status.get("ids", {}).get("legacy", [])
    _check(ordinary_ids.size() == 10, "Ordinary registry IDs are complete")
    _check(elite_ids.size() == 10, "Elite registry IDs are complete")
    _check(legacy_ids.size() == 2, "Legacy IDs are quarantined, not counted as ordinary")

    var main_records: Array[Dictionary] = coordinator.registry.get_main_bosses()
    var mini_records: Array[Dictionary] = coordinator.registry.get_mini_bosses()
    _check(main_records.size() == 6, "ContentRegistry returns six joined main records")
    _check(mini_records.size() == 5, "ContentRegistry returns five joined mini records")
    _check(coordinator.registry.get_elite_variants().size() == 10, "ContentRegistry returns ten joined elite records")
    _check(coordinator.registry.get_active_elite_limit() == 5, "Elite runtime projection limit is five")
    _check(not coordinator.registry.get_chest_eligibility("ELITE_CHEST").is_empty(), "ELITE_CHEST remains a typed registry outcome")


func _test_wave_admission() -> void:
    var coordinator: Variant = RunCoordinatorType.new()
    _check(bool(coordinator.boot().get("ok", false)), "Wave registry boots")
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


func _test_main_boss_freeze_and_duplicate() -> void:
    var coordinator: Variant = RunCoordinatorType.new()
    _check(bool(coordinator.boot().get("ok", false)), "Main-boss registry boots")
    _check(bool(coordinator.start_run("hero_lin_yue", 202, "r2-final").get("ok", false)), "Final-boss run starts")
    var mains: Array[Dictionary] = coordinator.registry.get_main_bosses()
    _check(mains.size() == 6, "Final-boss path sees the six-record main roster")
    if mains.is_empty():
        return

    var checkpoint_id := str(mains.back().get("checkpoint_id", ""))
    var started: Dictionary = coordinator.start_main_boss(checkpoint_id)
    _check(bool(started.get("ok", false)), "Final main boss starts from joined registry content")
    if not bool(started.get("ok", false)):
        return

    var run_before := coordinator.clock.run_seconds
    coordinator.advance(2.0)
    _check(is_equal_approx(coordinator.clock.run_seconds, run_before), "Main boss freezes visible run clock")
    _check(is_equal_approx(coordinator.clock.encounter_seconds, 2.0), "Main boss advances separate encounter clock")
    _check(str(coordinator.spawn_wave_fixture().get("code", "")) == "WAVE_PROGRESSION_BLOCKED", "Main boss blocks ordinary wave progression")

    var outcome: Dictionary = coordinator.defeat_active_boss()
    _check(bool(outcome.get("final", false)), "Final main boss settles through the ledger")
    _check(coordinator.session.state == "RUN_VICTORY", "Final main boss reaches victory")
    _check(coordinator.session.pending_chest_offer.is_empty(), "Final main boss creates no boss chest")
    var duplicate: Dictionary = coordinator.defeat_active_boss()
    _check(bool(duplicate.get("duplicate", false)), "Repeated final boss defeat returns stored outcome")
    var settlement_duplicate: Dictionary = coordinator.settle_checkpoint()
    _check(bool(settlement_duplicate.get("duplicate", false)), "Repeated final settlement returns stored outcome")
    policy_trace.append({
        "policy": "main_boss_final",
        "boss_id": mains.back().get("boss_id", ""),
        "run_before": run_before,
        "run_after": coordinator.clock.run_seconds,
        "encounter_after": coordinator.clock.encounter_seconds,
        "final": outcome.get("final", false),
        "boss_chest": not coordinator.session.pending_chest_offer.is_empty(),
        "duplicate": duplicate.get("duplicate", false),
        "settlement_duplicate": settlement_duplicate.get("duplicate", false)
    })

    var chest_coordinator: Variant = RunCoordinatorType.new()
    _check(bool(chest_coordinator.boot().get("ok", false)), "Non-final chest registry boots")
    _check(bool(chest_coordinator.start_run("hero_lin_yue", 303, "r2-chest").get("ok", false)), "Non-final chest run starts")
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


func _test_all_mini_bosses() -> void:
    var probe: Variant = RunCoordinatorType.new()
    _check(bool(probe.boot().get("ok", false)), "Mini-boss registry boots")
    var minis: Array[Dictionary] = probe.registry.get_mini_bosses()
    _check(minis.size() == 5, "All five mini-boss records are consumable")
    for index in range(minis.size()):
        var coordinator: Variant = RunCoordinatorType.new()
        var boss_id := str(minis[index].get("boss_id", minis[index].get("mini_boss_id", "")))
        _check(bool(coordinator.boot().get("ok", false)), "Mini-boss %s registry boots" % boss_id)
        var started_run: Dictionary = coordinator.start_run("hero_lin_yue", 400 + index, "r2-mini-%d" % index)
        _check(bool(started_run.get("ok", false)), "Mini-boss %s run starts" % boss_id)
        if not bool(started_run.get("ok", false)):
            continue

        var mini_started: Dictionary = coordinator.start_mini_boss(boss_id)
        _check(bool(mini_started.get("ok", false)), "Mini-boss %s starts from joined content" % boss_id)
        if not bool(mini_started.get("ok", false)):
            continue

        var run_before := coordinator.clock.run_seconds
        coordinator.advance(2.0)
        _check(coordinator.clock.run_seconds > run_before, "Mini-boss %s keeps visible run clock moving" % boss_id)
        _check(coordinator.clock.encounter_seconds > 0.0, "Mini-boss %s advances encounter clock" % boss_id)
        _check(bool(coordinator.spawn_wave_fixture().get("ok", false)), "Mini-boss %s keeps ordinary wave pressure" % boss_id)

        var mini_result: Dictionary = coordinator.defeat_active_boss()
        var mini_offer: Dictionary = mini_result.get("offer", {})
        _check(str(mini_offer.get("offer_type", "")) == "MINI_BOSS_CHEST", "Mini-boss %s creates a separate chest" % boss_id)
        var mini_claim: Dictionary = coordinator.claim_chest(
            str(mini_offer.get("offer_id", "")),
            int(mini_offer.get("created_at_revision", -1))
        )
        _check(bool(mini_claim.get("ok", false)), "Mini-boss %s chest claim resumes the run" % boss_id)
        policy_trace.append({
            "policy": "mini_boss",
            "boss_id": boss_id,
            "run_before": run_before,
            "run_after": coordinator.clock.run_seconds,
            "encounter_after": coordinator.clock.encounter_seconds,
            "chest_type": mini_offer.get("offer_type", ""),
            "resumed": mini_claim.get("state", "")
        })


func _test_elite_projection(coordinator: Variant) -> void:
    var all_variants: Array[Dictionary] = coordinator.registry.get_elite_variants()
    _check(all_variants.size() == 10, "Elite catalog contains ten variants")
    var limit := coordinator.registry.get_active_elite_limit()
    _check(limit == 5, "Elite active projection limit is five")
    var selected_first: Array[Dictionary] = coordinator.registry.select_active_elite_variants(505)
    var selected_second: Array[Dictionary] = coordinator.registry.select_active_elite_variants(505)
    _check(selected_first.size() == limit, "Elite projection is bounded by the registry limit")
    _check(JSON.stringify(_variant_ids(selected_first)) == JSON.stringify(_variant_ids(selected_second)), "Elite projection is deterministic for a seed")
    var unique_ids: Array = _variant_ids(selected_first)
    _check(unique_ids.size() == _unique_count(unique_ids), "Elite projection has no duplicate records")
    seed_traces.append({
        "seed": 505,
        "selected_elite_variant_ids": unique_ids,
        "limit": limit,
        "catalog_size": all_variants.size()
    })


func _variant_ids(records: Array[Dictionary]) -> Array:
    var ids: Array = []
    for record in records:
        ids.append(str(record.get("variant_id", "")))
    return ids


func _unique_count(values: Array) -> int:
    var unique: Array = []
    for value in values:
        if not unique.has(value):
            unique.append(value)
    return unique.size()


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
        "policy_trace": policy_trace,
        "seed_traces": seed_traces
    }
    print("R2_RUNTIME_TEST " + JSON.stringify(result))
    print("R2_RUNTIME_TRACE " + JSON.stringify({
        "ok": result["ok"],
        "status": status,
        "content_version": content_status.get("content_version", ""),
        "live_registry_join": content_status.get("live_registry_join", {}),
        "policy_trace": policy_trace,
        "seed_traces": seed_traces
    }))
    quit(0 if result["ok"] else 1)


func _check(condition: bool, label: String) -> void:
    if not condition:
        failures.append(label)
