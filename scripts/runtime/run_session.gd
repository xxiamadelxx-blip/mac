extends RefCounted
class_name RunSession

## Authoritative state for one active run.
##
## No UI nodes, textures, scene paths or network objects are stored here. The
## coordinator is the only owner allowed to move this aggregate between
## states in the R1 slice.

const STATE_RUN_LOADING := "RUN_LOADING"
const STATE_RUN_ACTIVE := "RUN_ACTIVE"
const STATE_UPGRADE_OFFER := "UPGRADE_OFFER"
const STATE_RUN_PAUSED := "RUN_PAUSED"
const STATE_RECOVERY_REVIEW := "RECOVERY_REVIEW"
const STATE_CONTENT_ERROR := "CONTENT_ERROR"

var schema_version := 1
var run_id := ""
var seed := 0
var content_version := ""
var selected_hero_id := ""
var state := STATE_RUN_LOADING
var resume_state := ""
var state_revision := 0
var stage_id := "first_run"
var checkpoint_id := ""
var current_wave_band_id := ""

var build: Dictionary = {}
var stats: Dictionary = {}
var xp_drops: Dictionary = {}
var aftermath_items: Dictionary = {}
var pending_offer: Dictionary = {}
var completed_offer_outcomes: Dictionary = {}
var active_enemy: Dictionary = {}
var diagnostics: Array[Dictionary] = []

var drop_sequence := 0
var offer_sequence := 0
var last_hit_at := -999999.0
var pause_reason := ""


func _init(
        p_run_id: String,
        p_seed: int,
        p_content_version: String,
        p_selected_hero_id: String,
        initial_build: Dictionary,
        initial_stats: Dictionary,
        initial_wave_band_id: String
    ) -> void:
    run_id = p_run_id
    seed = p_seed
    content_version = p_content_version
    selected_hero_id = p_selected_hero_id
    build = initial_build.duplicate(true)
    stats = initial_stats.duplicate(true)
    current_wave_band_id = initial_wave_band_id


func bump_revision() -> int:
    state_revision += 1
    return state_revision


func create_xp_drop(source_enemy_id: String, grade_id: String, value: int) -> Dictionary:
    drop_sequence += 1
    var xp_item_id := "%s:xp:%d" % [run_id, drop_sequence]
    var drop := {
        "xp_item_id": xp_item_id,
        "grade_id": grade_id,
        "value": value,
        "source_enemy_id": source_enemy_id,
        "collected": false,
        "pool_state": "ACTIVE",
        "aftermath_reference": ""
    }
    xp_drops[xp_item_id] = drop
    return drop.duplicate(true)


func create_offer(choice_records: Array[Dictionary]) -> Dictionary:
    offer_sequence += 1
    var offer_id := "%s:upgrade:%d" % [run_id, offer_sequence]
    var choice_ids: Array[String] = []
    for record in choice_records:
        choice_ids.append(str(record.get("choice_id", "")))
    pending_offer = {
        "offer_id": offer_id,
        "offer_type": "UPGRADE_OFFER",
        "choice_records": choice_records.duplicate(true),
        "choice_ids": choice_ids,
        "created_at_revision": state_revision,
        "claimed": false,
        "outcome": {}
    }
    return pending_offer.duplicate(true)


func record_diagnostic(code: String, message: String, recoverable: bool, details: Dictionary = {}) -> Dictionary:
    var diagnostic := {
        "code": code,
        "message": message,
        "recoverable": recoverable,
        "state_revision": state_revision,
        "details": details.duplicate(true)
    }
    diagnostics.append(diagnostic)
    return diagnostic


func clear_recoverable_diagnostics() -> void:
    var remaining: Array[Dictionary] = []
    for diagnostic in diagnostics:
        if not bool(diagnostic.get("recoverable", false)):
            remaining.append(diagnostic)
    diagnostics = remaining


func to_snapshot(clock_snapshot: Dictionary) -> Dictionary:
    return {
        "schema_version": schema_version,
        "run_id": run_id,
        "seed": seed,
        "content_version": content_version,
        "selected_hero_id": selected_hero_id,
        "state": state,
        "resume_state": resume_state,
        "state_revision": state_revision,
        "stage_id": stage_id,
        "checkpoint_id": checkpoint_id,
        "current_wave_band_id": current_wave_band_id,
        "build": build.duplicate(true),
        "stats": stats.duplicate(true),
        "xp_drops": xp_drops.duplicate(true),
        "aftermath_items": aftermath_items.duplicate(true),
        "pending_offer": pending_offer.duplicate(true),
        "completed_offer_outcomes": completed_offer_outcomes.duplicate(true),
        "active_enemy": active_enemy.duplicate(true),
        "drop_sequence": drop_sequence,
        "offer_sequence": offer_sequence,
        "last_hit_at": last_hit_at,
        "clock": clock_snapshot.duplicate(true),
        "pause_reason": pause_reason
    }


func restore_snapshot(snapshot: Dictionary) -> bool:
    var required := [
        "schema_version", "run_id", "seed", "content_version", "selected_hero_id",
        "state", "state_revision", "build", "stats", "xp_drops", "clock"
    ]
    for key in required:
        if not snapshot.has(key):
            return false
    if int(snapshot.get("schema_version", -1)) != schema_version:
        return false
    if str(snapshot.get("run_id", "")) != run_id:
        return false
    if str(snapshot.get("content_version", "")) != content_version:
        return false

    seed = int(snapshot.get("seed", seed))
    selected_hero_id = str(snapshot.get("selected_hero_id", selected_hero_id))
    state = str(snapshot.get("state", STATE_RUN_PAUSED))
    resume_state = str(snapshot.get("resume_state", ""))
    state_revision = int(snapshot.get("state_revision", state_revision))
    stage_id = str(snapshot.get("stage_id", stage_id))
    checkpoint_id = str(snapshot.get("checkpoint_id", checkpoint_id))
    current_wave_band_id = str(snapshot.get("current_wave_band_id", current_wave_band_id))
    build = snapshot.get("build", {}).duplicate(true)
    stats = snapshot.get("stats", {}).duplicate(true)
    xp_drops = snapshot.get("xp_drops", {}).duplicate(true)
    aftermath_items = snapshot.get("aftermath_items", {}).duplicate(true)
    pending_offer = snapshot.get("pending_offer", {}).duplicate(true)
    completed_offer_outcomes = snapshot.get("completed_offer_outcomes", {}).duplicate(true)
    active_enemy = snapshot.get("active_enemy", {}).duplicate(true)
    drop_sequence = int(snapshot.get("drop_sequence", drop_sequence))
    offer_sequence = int(snapshot.get("offer_sequence", offer_sequence))
    last_hit_at = float(snapshot.get("last_hit_at", last_hit_at))
    pause_reason = str(snapshot.get("pause_reason", ""))
    return true
