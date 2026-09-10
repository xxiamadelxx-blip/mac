extends Node
class_name R1RuntimeEntry

const RunCoordinatorType = preload("res://scripts/runtime/run_coordinator.gd")
const RunSessionType = preload("res://scripts/runtime/run_session.gd")

## Minimal scene-facing entry point for the R1 domain slice.
##
## The arena remains a visual preview, while this node proves that an actual
## scene can boot the domain, run one deterministic fixture and emit a trace.

@export var run_diagnostic_on_ready := true
@export var selected_hero_id := "hero_lin_yue"
@export var diagnostic_seed := 101

var coordinator: RunCoordinator


func _ready() -> void:
    if not run_diagnostic_on_ready:
        return
    var report := run_diagnostic_fixture()
    print("R1_RUNTIME_TRACE " + JSON.stringify(report))


func run_diagnostic_fixture() -> Dictionary:
    coordinator = RunCoordinatorType.new()
    var boot_result := coordinator.boot()
    if not bool(boot_result.get("ok", false)):
        return {"ok": false, "phase": "boot", "report": coordinator.trace_report()}

    var start_result := coordinator.start_run(selected_hero_id, diagnostic_seed, "arena-r1-start")
    var duplicate_start := coordinator.start_run(selected_hero_id, diagnostic_seed, "arena-r1-start")
    if not bool(start_result.get("ok", false)):
        return {
            "ok": false,
            "phase": "start",
            "start": start_result,
            "duplicate_start": duplicate_start,
            "report": coordinator.trace_report()
        }

    var loop_count := 0
    while coordinator.session.state == RunSessionType.STATE_RUN_ACTIVE and loop_count < 128:
        loop_count += 1
        if coordinator.session.active_enemy.is_empty():
            coordinator.spawn_wave_fixture()

        var attack_result := coordinator.resolve_fixture_attack()
        if str(attack_result.get("code", "")) == "HIT_COOLDOWN":
            coordinator.advance(coordinator.registry.get_contact_damage_cooldown())
        elif bool(attack_result.get("defeated", false)):
            var drop: Dictionary = attack_result.get("drop", {})
            coordinator.collect_xp(str(drop.get("xp_item_id", "")))
        elif bool(attack_result.get("ok", false)):
            coordinator.advance(coordinator.registry.get_contact_damage_cooldown())
        else:
            break

    var offer: Dictionary = coordinator.session.pending_offer.duplicate(true)
    var claim_result: Dictionary = {}
    var duplicate_claim: Dictionary = {}
    if not offer.is_empty():
        var choice_ids: Array = offer.get("choice_ids", [])
        if not choice_ids.is_empty():
            claim_result = coordinator.claim_upgrade(
                str(offer.get("offer_id", "")),
                str(choice_ids[0]),
                int(offer.get("created_at_revision", -1))
            )
            duplicate_claim = coordinator.claim_upgrade(
                str(offer.get("offer_id", "")),
                str(choice_ids[0]),
                int(offer.get("created_at_revision", -1))
            )

    return {
        "ok": not offer.is_empty() and bool(claim_result.get("ok", false)),
        "start": start_result,
        "duplicate_start": duplicate_start,
        "offer": offer,
        "claim": claim_result,
        "duplicate_claim": duplicate_claim,
        "loop_count": loop_count,
        "report": coordinator.trace_report()
    }
