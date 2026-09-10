extends RefCounted
class_name SimulationClock

## Deterministic clocks for the domain layer.
##
## RUN_ACTIVE advances only the visible run clock. ENCOUNTER_ACTIVE advances
## only the encounter clock, which gives R2 a separate boss-time seam without
## allowing ordinary wave time to advance during an encounter.

const MODE_STOPPED := "STOPPED"
const MODE_RUN_ACTIVE := "RUN_ACTIVE"
const MODE_ENCOUNTER_ACTIVE := "ENCOUNTER_ACTIVE"
const MODE_PAUSED := "PAUSED"
const MODE_FROZEN := "FROZEN"

var run_seconds := 0.0
var encounter_seconds := 0.0
var mode := MODE_STOPPED
var paused_from_mode := MODE_STOPPED
var diagnostics: Array[Dictionary] = []


func start_run() -> void:
    mode = MODE_RUN_ACTIVE
    paused_from_mode = MODE_RUN_ACTIVE


func start_encounter() -> void:
    mode = MODE_ENCOUNTER_ACTIVE
    paused_from_mode = MODE_ENCOUNTER_ACTIVE


func freeze() -> void:
    mode = MODE_FROZEN


func pause() -> void:
    if mode != MODE_PAUSED:
        paused_from_mode = mode
    mode = MODE_PAUSED


func resume() -> bool:
    if paused_from_mode == MODE_STOPPED:
        _add_diagnostic("CLOCK_RESUME_WITHOUT_SOURCE", "Clock cannot resume without a previous active mode.")
        return false
    mode = paused_from_mode
    return true


func advance(delta_seconds: float) -> Dictionary:
    if delta_seconds < 0.0 or delta_seconds != delta_seconds or delta_seconds > 3600.0:
        _add_diagnostic("CLOCK_DELTA_INVALID", "Simulation delta must be finite, non-negative and bounded.", {"delta": delta_seconds})
        return {"ok": false, "advanced": false, "mode": mode}

    var before := snapshot()
    match mode:
        MODE_RUN_ACTIVE:
            run_seconds += delta_seconds
        MODE_ENCOUNTER_ACTIVE:
            encounter_seconds += delta_seconds
        MODE_PAUSED, MODE_FROZEN, MODE_STOPPED:
            pass
        _:
            _add_diagnostic("CLOCK_MODE_INVALID", "Unknown simulation clock mode.", {"mode": mode})
            return {"ok": false, "advanced": false, "mode": mode}

    return {
        "ok": true,
        "advanced": not is_equal_approx(before["run_seconds"], run_seconds) or not is_equal_approx(before["encounter_seconds"], encounter_seconds),
        "before": before,
        "after": snapshot(),
        "mode": mode
    }


func snapshot() -> Dictionary:
    return {
        "run_seconds": run_seconds,
        "encounter_seconds": encounter_seconds,
        "mode": mode,
        "paused_from_mode": paused_from_mode
    }


func restore(value: Dictionary) -> bool:
    if not value.has("run_seconds") or not value.has("encounter_seconds") or not value.has("mode"):
        _add_diagnostic("CLOCK_SNAPSHOT_INVALID", "Clock snapshot is missing required fields.")
        return false
    var restored_run := float(value.get("run_seconds", -1.0))
    var restored_encounter := float(value.get("encounter_seconds", -1.0))
    var restored_mode := str(value.get("mode", ""))
    if restored_run < 0.0 or restored_encounter < 0.0 or not _is_known_mode(restored_mode):
        _add_diagnostic("CLOCK_SNAPSHOT_INVALID", "Clock snapshot contains invalid values.", {"snapshot": value})
        return false
    run_seconds = restored_run
    encounter_seconds = restored_encounter
    mode = restored_mode
    paused_from_mode = str(value.get("paused_from_mode", restored_mode))
    return true


func clear_diagnostics() -> void:
    diagnostics.clear()


func _is_known_mode(value: String) -> bool:
    return value in [MODE_STOPPED, MODE_RUN_ACTIVE, MODE_ENCOUNTER_ACTIVE, MODE_PAUSED, MODE_FROZEN]


func _add_diagnostic(code: String, message: String, details: Dictionary = {}) -> void:
    var item := {"code": code, "message": message}
    for key in details:
        item[key] = details[key]
    diagnostics.append(item)
