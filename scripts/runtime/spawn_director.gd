extends RefCounted
class_name SpawnDirector

## Pure, data-driven spawn scheduling for the runtime boundary.
##
## The director owns no Godot nodes and performs no scene instantiation. It
## advances independent timer state only when progression is unlocked, derives
## the ordinary spawn interval and active cap from ContentRegistry, and
## leaves admission side effects to a scene/pool adapter.

const MAIN_BOSS := "MAIN_BOSS"
const MINI_BOSS := "MINI_BOSS"

const PHASE_CANONICAL := "CANONICAL_WAVE_BANDS"
const PHASE_MAIN_BOSS_FREEZE := "MAIN_BOSS_FREEZE"
const PHASE_MINI_BOSS_PRESSURE := "MINI_BOSS_PRESSURE"
const PHASE_WAVE_LOCKED := "WAVE_LOCKED"
const PHASE_POST_BOSS_RECOVERY := "POST_BOSS_RECOVERY"
const PHASE_RAMP := "RAMP"
const PHASE_SIEGE := "SIEGE"

var registry: Object
var progression_locked := false
var current_wave_band_id := ""
var enemy_timer_seconds := 0.0
var wave_timer_seconds := 0.0
var ramp_timer_seconds := 0.0
var ramp_context: Dictionary = {}
var diagnostics: Array[Dictionary] = []


func _init(p_registry: Object) -> void:
    registry = p_registry


func reset() -> void:
    progression_locked = false
    current_wave_band_id = ""
    enemy_timer_seconds = 0.0
    wave_timer_seconds = 0.0
    ramp_timer_seconds = 0.0
    ramp_context = {}
    diagnostics.clear()


func set_progression_locked(locked: bool) -> void:
    progression_locked = locked


func begin_post_boss_cycle(cycle: Dictionary) -> Dictionary:
    var cycle_id := str(cycle.get("cycle_id", ""))
    var start_seconds := float(cycle.get("start_seconds", -1.0))
    var end_seconds := float(cycle.get("end_seconds", -1.0))
    if cycle_id.is_empty() or not _valid_time(start_seconds) or not _valid_time(end_seconds) or end_seconds <= start_seconds:
        _add_diagnostic("WAVE_CYCLE_INVALID", "Post-boss cycle requires a stable ID and ordered registry boundaries.", {"cycle": cycle})
        return {"ok": false, "code": "WAVE_CYCLE_INVALID", "cycle": cycle.duplicate(true)}

    ramp_context = cycle.duplicate(true)
    ramp_context["cycle_id"] = cycle_id
    ramp_context["start_seconds"] = start_seconds
    ramp_context["end_seconds"] = end_seconds
    ramp_timer_seconds = 0.0
    return {
        "ok": true,
        "cycle": ramp_context.duplicate(true),
        "phase": phase_for(start_seconds)
    }


func advance(
        simulation_seconds: float,
        delta_seconds: float,
        boss_kind: String = "",
        active_count: int = 0,
        requested_count: int = 1
    ) -> Dictionary:
    if not _valid_time(simulation_seconds) or not _valid_delta(delta_seconds):
        _add_diagnostic("SPAWN_TIME_INVALID", "SpawnDirector time inputs must be finite and bounded.", {
            "simulation_seconds": simulation_seconds,
            "delta_seconds": delta_seconds
        })
        return {"ok": false, "code": "SPAWN_TIME_INVALID"}
    if active_count < 0 or requested_count <= 0:
        return {
            "ok": false,
            "code": "SPAWN_REQUEST_INVALID",
            "active_count": active_count,
            "requested_count": requested_count
        }
    if registry == null:
        return {"ok": false, "code": "CONTENT_REGISTRY_MISSING"}

    var band: Dictionary = registry.get_wave_band_for_time(simulation_seconds)
    if band.is_empty():
        return {
            "ok": false,
            "code": "WAVE_BAND_NOT_FOUND",
            "simulation_seconds": simulation_seconds,
            "content_status": registry.get_r2_content_status()
        }

    var spawn_interval := _spawn_interval_seconds(band)
    if spawn_interval <= 0.0:
        _add_diagnostic("SPAWN_RATE_INVALID", "The current registry band has no positive spawn budget.", {
            "wave_band_id": band.get("wave_band_id", "")
        })
        return {
            "ok": false,
            "code": "SPAWN_RATE_INVALID",
            "wave_band_id": band.get("wave_band_id", "")
        }

    var before := snapshot()
    var locked := progression_locked or boss_kind == MAIN_BOSS
    var band_id := str(band.get("wave_band_id", ""))
    var band_changed := band_id != current_wave_band_id

    # Main-boss freeze and an explicit locked-wave gate both hold every timer.
    # The encounter clock is owned by SimulationClock, not by this director.
    if not locked:
        if band_changed:
            current_wave_band_id = band_id
            wave_timer_seconds = 0.0
        else:
            wave_timer_seconds += delta_seconds
        enemy_timer_seconds += delta_seconds
        if not ramp_context.is_empty():
            ramp_timer_seconds += delta_seconds

    var active_cap := int(_record_number(band.get("active_cap", 0), 0.0))
    var required_time := spawn_interval * float(requested_count)
    var spawn_due := not locked and enemy_timer_seconds >= required_time
    var result := {
        "ok": true,
        "admitted": false,
        "code": "",
        "locked": locked,
        "paused": locked,
        "phase": phase_for(simulation_seconds, boss_kind),
        "simulation_seconds": simulation_seconds,
        "wave_band_id": band_id,
        "spawn_interval_seconds": spawn_interval,
        "spawn_due": spawn_due,
        "active_count": active_count,
        "requested_count": requested_count,
        "active_cap": active_cap,
        "wave_changed": band_changed and not locked,
        "registry_source": "BALANCE_MODEL.json.wave_bands",
        "timers_before": before.get("timers", {}).duplicate(true),
        "timers_after": snapshot().get("timers", {}).duplicate(true),
        "timer_consumed_seconds": 0.0,
        "band": band.duplicate(true)
    }

    if locked:
        result["code"] = "WAVE_PROGRESSION_BLOCKED"
        result["would_be_due"] = enemy_timer_seconds >= required_time
        result["timers_after"] = snapshot().get("timers", {}).duplicate(true)
        return result

    if not spawn_due:
        result["code"] = "SPAWN_TIMER_NOT_READY"
        result["timers_after"] = snapshot().get("timers", {}).duplicate(true)
        return result

    if active_count + requested_count > active_cap:
        # Cap-first admission: retain one bounded due interval, never queue
        # unbounded spawn debt while the adapter cannot admit another entity.
        enemy_timer_seconds = min(enemy_timer_seconds, required_time)
        result["code"] = "ACTIVE_CAP_REACHED"
        result["timers_after"] = snapshot().get("timers", {}).duplicate(true)
        return result

    enemy_timer_seconds -= required_time
    result["admitted"] = true
    result["code"] = "SPAWN_ADMITTED"
    result["timer_consumed_seconds"] = required_time
    result["timers_after"] = snapshot().get("timers", {}).duplicate(true)
    return result


func phase_for(simulation_seconds: float, boss_kind: String = "") -> String:
    if boss_kind == MAIN_BOSS:
        return PHASE_MAIN_BOSS_FREEZE
    if boss_kind == MINI_BOSS:
        return PHASE_MINI_BOSS_PRESSURE
    if progression_locked:
        return PHASE_WAVE_LOCKED
    if ramp_context.is_empty():
        return PHASE_CANONICAL

    var start_seconds := float(ramp_context.get("start_seconds", -1.0))
    var end_seconds := float(ramp_context.get("end_seconds", -1.0))
    if not _valid_time(start_seconds) or not _valid_time(end_seconds) or end_seconds <= start_seconds:
        return PHASE_CANONICAL

    var cycle_duration := end_seconds - start_seconds
    var elapsed: float = clampf(simulation_seconds - start_seconds, 0.0, cycle_duration)
    var suppression_seconds := _model_seconds([
        "simulation_model",
        "boss_interruption",
        "suppression_seconds"
    ])
    var recovery_seconds := _model_seconds([
        "simulation_model",
        "boss_interruption",
        "recovery_duration_seconds"
    ])
    var siege_seconds := _model_seconds([
        "simulation_model",
        "boss_wave_ramp",
        "siege_duration_seconds"
    ])
    if suppression_seconds < 0.0 or recovery_seconds < 0.0 or siege_seconds < 0.0:
        return PHASE_CANONICAL

    var recovery_end: float = minf(cycle_duration, suppression_seconds + recovery_seconds)
    var siege_start: float = maxf(0.0, cycle_duration - siege_seconds)
    if elapsed < recovery_end:
        return PHASE_POST_BOSS_RECOVERY
    if elapsed >= siege_start:
        return PHASE_SIEGE
    return PHASE_RAMP


func snapshot() -> Dictionary:
    return {
        "progression_locked": progression_locked,
        "current_wave_band_id": current_wave_band_id,
        "timers": {
            "enemy_seconds": enemy_timer_seconds,
            "wave_seconds": wave_timer_seconds,
            "ramp_seconds": ramp_timer_seconds
        },
        "ramp_context": ramp_context.duplicate(true)
    }


func _spawn_interval_seconds(band: Dictionary) -> float:
    var rate := _record_number(band.get("spawn_budget_per_second", 0), 0.0)
    if rate <= 0.0:
        return -1.0
    return 1.0 / rate


func _model_seconds(path: Array[String]) -> float:
    if registry == null:
        return -1.0
    var record: Variant = registry.get_model_field(path, null)
    return _record_number(record, -1.0)


func _record_number(record: Variant, fallback: float) -> float:
    if record is Dictionary:
        var value: Variant = record.get("value", null)
        if typeof(value) == TYPE_INT or typeof(value) == TYPE_FLOAT:
            return float(value)
        return fallback
    if typeof(record) == TYPE_INT or typeof(record) == TYPE_FLOAT:
        return float(record)
    return fallback


func _valid_time(value: float) -> bool:
    return value >= 0.0 and value == value and value < 8640000.0


func _valid_delta(value: float) -> bool:
    return value >= 0.0 and value == value and value < 3600.0


func _add_diagnostic(code: String, message: String, details: Dictionary = {}) -> void:
    var item := {"code": code, "message": message}
    for key in details:
        item[key] = details[key]
    diagnostics.append(item)
