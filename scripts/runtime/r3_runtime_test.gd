extends SceneTree

const RunCoordinatorType = preload("res://scripts/runtime/run_coordinator.gd")
const RunSessionType = preload("res://scripts/runtime/run_session.gd")

var failures: Array[String] = []
var seed_traces: Array[Dictionary] = []
var main_boss_registry_count := -1
var mini_boss_registry_count := -1


func _init() -> void:
    _test_artifact_contract_and_idempotency()
    _test_main_boss_freeze_and_final_settlement()
    _test_first_clear_offer_is_separate()
    _test_seed_set()
    var result := {
        "ok": failures.is_empty(),
        "failures": failures,
        "seed_traces": seed_traces,
        "r2_content": {
            "main_boss_count": main_boss_registry_count,
            "mini_boss_count": mini_boss_registry_count,
            "mini_boss_status": "PENDING_CONTENT_SYNC" if mini_boss_registry_count == 0 else "AVAILABLE"
        }
    }
    print("R3_RUNTIME_TEST " + JSON.stringify(result))
    print("R3_RUNTIME_TRACE " + JSON.stringify({"ok": failures.is_empty(), "seed_traces": seed_traces, "main_boss_count": main_boss_registry_count, "mini_boss_count": mini_boss_registry_count}))
    quit(0 if failures.is_empty() else 1)


func _test_artifact_contract_and_idempotency() -> void:
    var coordinator: Variant = RunCoordinatorType.new()
    _check(bool(coordinator.boot().get("ok", false)), "R3 registry boots")
    var rejected: Dictionary = coordinator.start_run("hero_lin_yue", 101, "pre-run-artifact", ["artifact_aura"])
    _check(str(rejected.get("code", "")) == "PRE_RUN_ARTIFACT_LOADOUT_REJECTED", "Pre-run artifact loadout is rejected")

    var started: Dictionary = coordinator.start_run("hero_lin_yue", 101, "r3-start")
    _check(bool(started.get("ok", false)), "R3 run starts")
    var sources: Array = coordinator.registry.get_artifact_offer_model().get("sources", [])
    _check(sources.has("ELITE_PACK"), "ELITE_PACK is a registry-defined artifact source")
    _check(sources.has("FIRST_CLEAR_REWARD"), "FIRST_CLEAR_REWARD is a registry-defined artifact source")
    _check(coordinator.registry.get_artifact_offer_model().get("choice_count", 0) == 3, "Artifact source has exactly three cards")

    var before_weapon_slots := int(coordinator.session.build.get("weapon_slots", -1))
    var before_passive_slots := int(coordinator.session.build.get("passive_slots", -1))
    var opened: Dictionary = coordinator.open_artifact_offer("ELITE_PACK", "elite-open")
    _check(bool(opened.get("ok", false)), "ELITE_PACK opens ARTIFACT_OFFER")
    var offer: Dictionary = opened.get("offer", {})
    _check(coordinator.session.state == RunSessionType.STATE_ARTIFACT_OFFER, "Artifact offer blocks the run")
    _check(offer.get("choice_ids", []).size() == 3, "Artifact offer contains three choices")
    var typed_candidates := true
    for candidate in offer.get("candidates", []):
        if not candidate.get("effect", {}).has("type"):
            typed_candidates = false
    _check(typed_candidates, "Artifact effects remain typed")

    var stale_revision := int(offer.get("created_at_revision", -1))
    var refreshed: Dictionary = coordinator.refresh_artifact_offer(str(offer.get("offer_id", "")), "refresh-1", stale_revision)
    _check(bool(refreshed.get("ok", false)), "Artifact refresh succeeds")
    var duplicate_refresh: Dictionary = coordinator.refresh_artifact_offer(str(offer.get("offer_id", "")), "refresh-1", stale_revision)
    _check(bool(duplicate_refresh.get("duplicate", false)), "Artifact refresh is idempotent")
    var refreshed_offer: Dictionary = refreshed.get("offer", {})
    _check(int(refreshed_offer.get("refresh_count", 0)) == 1, "Refresh increments the offer revision")

    var stale_claim: Dictionary = coordinator.claim_artifact(
        str(offer.get("offer_id", "")),
        str(refreshed_offer.get("choice_ids", [""])[0]),
        stale_revision
    )
    _check(str(stale_claim.get("code", "")) == "STALE_COMMAND", "Stale artifact choice is rejected")
    var chosen_id := str(refreshed_offer.get("choice_ids", [""])[0])
    var claim: Dictionary = coordinator.claim_artifact(str(offer.get("offer_id", "")), chosen_id, int(refreshed_offer.get("created_at_revision", -1)))
    var duplicate_claim: Dictionary = coordinator.claim_artifact(str(offer.get("offer_id", "")), chosen_id, int(refreshed_offer.get("created_at_revision", -1)))
    _check(bool(claim.get("ok", false)), "One artifact choice creates one instance")
    _check(bool(duplicate_claim.get("duplicate", false)), "Artifact choice is idempotent")
    _check(coordinator.session.stats.get("artifacts", []).size() == 1, "Artifact is stored in the run, not a build slot")
    _check(int(coordinator.session.build.get("weapon_slots", -1)) == before_weapon_slots, "Artifact does not change weapon slots")
    _check(int(coordinator.session.build.get("passive_slots", -1)) == before_passive_slots, "Artifact does not change passive slots")
    _check(str(claim.get("artifact", {}).get("capacity", "")) == "UNBOUNDED_WITHIN_RUN", "Artifact capacity is unbounded within run")


func _test_first_clear_offer_is_separate() -> void:
    var coordinator: Variant = RunCoordinatorType.new()
    _check(bool(coordinator.boot().get("ok", false)), "First-clear registry boots")
    _check(bool(coordinator.start_run("hero_lin_yue", 202, "first-clear-start").get("ok", false)), "First-clear run starts")
    var main_bosses: Array[Dictionary] = coordinator.registry.get_main_bosses()
    var final_checkpoint := str(main_bosses.back().get("checkpoint_id", "")) if not main_bosses.is_empty() else ""
    var boss: Dictionary = coordinator.start_main_boss(final_checkpoint)
    if not bool(boss.get("ok", false)):
        _check(false, "Final boss content is available for the first-clear path")
        return
    var final_result: Dictionary = coordinator.defeat_active_boss()
    _check(bool(final_result.get("final", false)), "Final boss settles the run")
    _check(coordinator.session.state == RunSessionType.STATE_RUN_VICTORY, "Final settlement reaches RUN_VICTORY")
    _check(coordinator.session.pending_chest_offer.is_empty(), "Final boss creates no boss chest")
    var opened: Dictionary = coordinator.open_artifact_offer("FIRST_CLEAR_REWARD", "first-clear-offer")
    _check(bool(opened.get("ok", false)), "FIRST_CLEAR_REWARD opens after result finalization")
    var offer: Dictionary = opened.get("offer", {})
    _check(offer.get("choice_ids", []).size() == 3, "First-clear offer contains three cards")
    _check(str(offer.get("source", "")) == "FIRST_CLEAR_REWARD", "First-clear source stays separate from boss chest")
    var choice_id := str(offer.get("choice_ids", [""])[0])
    var claim: Dictionary = coordinator.claim_artifact(str(offer.get("offer_id", "")), choice_id, int(offer.get("created_at_revision", -1)))
    _check(bool(claim.get("ok", false)), "First-clear artifact choice succeeds")
    _check(coordinator.session.state == RunSessionType.STATE_RUN_VICTORY, "First-clear claim does not reopen the run")


func _test_main_boss_freeze_and_final_settlement() -> void:
    var coordinator: Variant = RunCoordinatorType.new()
    _check(bool(coordinator.boot().get("ok", false)), "Main-boss registry boots")
    main_boss_registry_count = coordinator.registry.get_main_bosses().size()
    mini_boss_registry_count = coordinator.registry.get_mini_bosses().size()
    _check(bool(coordinator.start_run("hero_lin_yue", 303, "main-boss-start").get("ok", false)), "Main-boss run starts")
    coordinator.advance(1.0)
    var main_bosses: Array[Dictionary] = coordinator.registry.get_main_bosses()
    var final_checkpoint := str(main_bosses.back().get("checkpoint_id", "")) if not main_bosses.is_empty() else ""
    var started: Dictionary = coordinator.start_main_boss(final_checkpoint)
    _check(bool(started.get("ok", false)), "Main boss starts from registry checkpoint")
    var frozen_run := coordinator.clock.run_seconds
    coordinator.advance(2.0)
    _check(is_equal_approx(coordinator.clock.run_seconds, frozen_run), "Main boss freezes visible run clock")
    _check(is_equal_approx(coordinator.clock.encounter_seconds, 2.0), "Main boss advances separate encounter clock")
    _check(str(coordinator.spawn_wave_fixture().get("code", "")) == "WAVE_PROGRESSION_BLOCKED", "Main boss blocks ordinary wave progression")
    var settled: Dictionary = coordinator.defeat_active_boss()
    _check(bool(settled.get("final", false)), "Main boss creates final settlement")
    _check(coordinator.session.pending_chest_offer.is_empty(), "Final main boss has no boss chest")

    if mini_boss_registry_count == 0:
        return
    var mini: Variant = RunCoordinatorType.new()
    _check(bool(mini.boot().get("ok", false)), "Mini-boss registry boots")
    _check(bool(mini.start_run("hero_lin_yue", 404, "mini-boss-start").get("ok", false)), "Mini-boss run starts")
    var mini_id := str(mini.registry.get_mini_bosses()[0].get("boss_id", mini.registry.get_mini_bosses()[0].get("mini_boss_id", "")))
    var mini_started: Dictionary = mini.start_mini_boss(mini_id)
    _check(bool(mini_started.get("ok", false)), "Mini boss starts from registry content")
    var mini_run_before := mini.clock.run_seconds
    mini.advance(2.0)
    _check(mini.clock.run_seconds > mini_run_before, "Mini boss keeps visible run clock moving")
    _check(mini.clock.encounter_seconds > 0.0, "Mini boss advances encounter clock")
    _check(bool(mini.spawn_wave_fixture().get("ok", false)), "Mini boss keeps ordinary waves available")
    var mini_settlement: Dictionary = mini.defeat_active_boss()
    _check(str(mini_settlement.get("offer", {}).get("offer_type", "")) == "MINI_BOSS_CHEST", "Mini boss creates a separate chest")
    var mini_offer: Dictionary = mini_settlement.get("offer", {})
    var mini_claim: Dictionary = mini.claim_chest(str(mini_offer.get("offer_id", "")), int(mini_offer.get("created_at_revision", -1)))
    _check(bool(mini_claim.get("ok", false)), "Mini-boss chest claim resumes the run")


func _test_seed_set() -> void:
    var seeds := [101, 202, 303, 404, 505]
    for seed in seeds:
        var first: Variant = RunCoordinatorType.new()
        var second: Variant = RunCoordinatorType.new()
        _check(bool(first.boot().get("ok", false)), "Seed %d first boot" % seed)
        _check(bool(second.boot().get("ok", false)), "Seed %d second boot" % seed)
        _check(bool(first.start_run("hero_lin_yue", seed, "seed-start").get("ok", false)), "Seed %d first start" % seed)
        _check(bool(second.start_run("hero_lin_yue", seed, "seed-start").get("ok", false)), "Seed %d second start" % seed)
        var first_offer: Dictionary = first.open_artifact_offer("ELITE_PACK", "seed-offer").get("offer", {})
        var second_offer: Dictionary = second.open_artifact_offer("ELITE_PACK", "seed-offer").get("offer", {})
        var first_signature := JSON.stringify(first_offer.get("choice_ids", []))
        var second_signature := JSON.stringify(second_offer.get("choice_ids", []))
        _check(first_signature == second_signature, "Seed %d produces a stable artifact offer" % seed)
        var effect_types: Array[String] = []
        for candidate in first_offer.get("candidates", []):
            effect_types.append(str(candidate.get("effect", {}).get("type", "")))
        seed_traces.append({
            "seed": seed,
            "content_version": first.session.content_version,
            "source": first_offer.get("source", ""),
            "choice_ids": first_offer.get("choice_ids", []),
            "effect_types": effect_types
        })


func _check(condition: bool, label: String) -> void:
    if not condition:
        failures.append(label)
