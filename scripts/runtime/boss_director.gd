extends RefCounted
class_name BossDirector

## Boss encounter boundary. Boss identity and cadence come from ContentRegistry.

const KIND_MAIN := "MAIN_BOSS"
const KIND_MINI := "MINI_BOSS"

var registry: Object
var sequence := 0
var active_encounter: Dictionary = {}
var completed_encounters: Dictionary = {}


func _init(p_registry: Object) -> void:
    registry = p_registry


func begin(kind: String, checkpoint_id: String = "", boss_id: String = "", run_seconds: float = 0.0) -> Dictionary:
    if not active_encounter.is_empty():
        return {"ok": false, "code": "BOSS_ALREADY_ACTIVE", "encounter": active_encounter.duplicate(true)}
    if kind != KIND_MAIN and kind != KIND_MINI:
        return {"ok": false, "code": "BOSS_KIND_INVALID"}

    var record := _find_record(kind, checkpoint_id, boss_id)
    if record.is_empty():
        return {
            "ok": false,
            "code": "MINI_BOSS_CONTENT_PENDING" if kind == KIND_MINI else "BOSS_CONTENT_NOT_FOUND",
            "boss_kind": kind,
            "checkpoint_id": checkpoint_id,
            "boss_id": boss_id
        }

    sequence += 1
    var resolved_boss_id := str(record.get("boss_id", record.get("mini_boss_id", record.get("id", boss_id))))
    var resolved_checkpoint := str(record.get("checkpoint_id", checkpoint_id))
    active_encounter = {
        "encounter_id": "%s:%d" % [resolved_boss_id, sequence],
        "boss_kind": kind,
        "boss_id": resolved_boss_id,
        "checkpoint_id": resolved_checkpoint,
        "started_at_run_seconds": run_seconds,
        "freeze_run_clock": kind == KIND_MAIN,
        "freeze_wave_xp_spawn": kind == KIND_MAIN,
        "encounter_clock": 0.0,
        "telegraph": record.get("telegraph", {"status": "CONTRACT_PENDING"}),
        "safe_spawn": record.get("safe_spawn", {"status": "CONTRACT_PENDING"}),
        "source_path": record.get("source_path", record.get("source", record.get("boss_source", "BALANCE_MODEL.json"))),
        "source_status": record.get("content_status", record.get("boss_status", record.get("status", "PENDING_CONTENT_SYNC")))
    }
    return {"ok": true, "encounter": active_encounter.duplicate(true)}


func defeat(encounter_id: String) -> Dictionary:
    if active_encounter.is_empty():
        if completed_encounters.has(encounter_id):
            var duplicate: Dictionary = completed_encounters[encounter_id].duplicate(true)
            duplicate["duplicate"] = true
            return duplicate
        return {"ok": false, "code": "NO_ACTIVE_BOSS"}
    if str(active_encounter.get("encounter_id", "")) != encounter_id:
        return {"ok": false, "code": "STALE_BOSS_ENCOUNTER", "encounter_id": encounter_id}
    var defeated := active_encounter.duplicate(true)
    active_encounter = {}
    var outcome := {"ok": true, "duplicate": false, "defeated": defeated}
    completed_encounters[encounter_id] = outcome.duplicate(true)
    return outcome


func has_active() -> bool:
    return not active_encounter.is_empty()


func _find_record(kind: String, checkpoint_id: String, boss_id: String) -> Dictionary:
    var records: Array[Dictionary] = registry.get_main_bosses() if kind == KIND_MAIN else registry.get_mini_bosses()
    for record in records:
        var record_checkpoint := str(record.get("checkpoint_id", ""))
        var record_id := str(record.get("boss_id", record.get("mini_boss_id", record.get("id", ""))))
        if not checkpoint_id.is_empty() and record_checkpoint == checkpoint_id:
            return record.duplicate(true)
        if not boss_id.is_empty() and record_id == boss_id:
            return record.duplicate(true)
    return {}
