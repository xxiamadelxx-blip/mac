extends RefCounted
class_name WaveDirector

## Data-driven wave projection used by R2.
##
## This class never owns balance numbers. It projects the current band and
## reports whether ordinary wave time is allowed to progress for the active
## boss policy. Spawn admission is also derived from the same registry record,
## so active-cap enforcement cannot drift into a controller constant.

const SpawnDirectorType = preload("res://scripts/runtime/spawn_director.gd")

var registry: Object
var spawn_director: Object


func _init(p_registry: Object) -> void:
    registry = p_registry
    spawn_director = SpawnDirectorType.new(registry)


func reset() -> void:
    spawn_director.reset()


func begin_post_boss_cycle(from_checkpoint_id: String, to_checkpoint_id: String) -> Dictionary:
    var from_record := _find_main_checkpoint(from_checkpoint_id)
    var to_record := _find_main_checkpoint(to_checkpoint_id)
    if from_record.is_empty() or to_record.is_empty():
        return {
            "ok": false,
            "code": "WAVE_CYCLE_CHECKPOINT_NOT_FOUND",
            "from_checkpoint_id": from_checkpoint_id,
            "to_checkpoint_id": to_checkpoint_id
        }

    var cycle_mapping := _find_cycle_mapping(from_checkpoint_id, to_checkpoint_id)
    if cycle_mapping.is_empty():
        return {
            "ok": false,
            "code": "WAVE_CYCLE_MAPPING_MISSING",
            "from_checkpoint_id": from_checkpoint_id,
            "to_checkpoint_id": to_checkpoint_id
        }

    var start_seconds := _checkpoint_seconds(from_record)
    var end_seconds := _checkpoint_seconds(to_record)
    if start_seconds < 0.0 or end_seconds <= start_seconds:
        return {
            "ok": false,
            "code": "WAVE_CYCLE_BOUNDARY_INVALID",
            "from_checkpoint_id": from_checkpoint_id,
            "to_checkpoint_id": to_checkpoint_id
        }

    var cycle := cycle_mapping.duplicate(true)
    cycle["cycle_id"] = str(cycle.get("cycle_id", "%s_to_%s" % [from_checkpoint_id, to_checkpoint_id]))
    cycle["from_checkpoint_id"] = from_checkpoint_id
    cycle["to_checkpoint_id"] = to_checkpoint_id
    cycle["start_seconds"] = start_seconds
    cycle["end_seconds"] = end_seconds
    return spawn_director.begin_post_boss_cycle(cycle)


func resolve(run_seconds: float, boss_kind: String = "") -> Dictionary:
    var phase: String = spawn_director.phase_for(run_seconds, boss_kind)
    if boss_kind == "MAIN_BOSS":
        return {
            "ok": true,
            "paused": true,
            "phase": phase,
            "run_seconds": run_seconds,
            "source": "RUNTIME_CONTEXT"
        }

    var band: Dictionary = registry.get_wave_band_for_time(run_seconds)
    if band.is_empty():
        return {
            "ok": false,
            "code": "WAVE_BAND_NOT_FOUND",
            "run_seconds": run_seconds,
            "content_status": registry.get_r2_content_status()
        }

    return {
        "ok": true,
        "paused": phase == "WAVE_LOCKED",
        "phase": phase,
        "run_seconds": run_seconds,
        "wave_band_id": str(band.get("wave_band_id", "")),
        "spawn_budget_per_second": _record_value(band.get("spawn_budget_per_second", {}), 0.0),
        "active_cap": _record_value(band.get("active_cap", {}), 0),
        "composition": band.get("composition", {}),
        "band": band.duplicate(true),
        "registry_source": "BALANCE_MODEL.json.wave_bands"
    }


func advance(
        run_seconds: float,
        delta_seconds: float,
        boss_kind: String = "",
        active_count: int = 0,
        requested_count: int = 1
    ) -> Dictionary:
    var decision: Dictionary = spawn_director.advance(
        run_seconds,
        delta_seconds,
        boss_kind,
        active_count,
        requested_count
    )
    if not bool(decision.get("ok", false)):
        return decision

    var pressure := resolve(run_seconds, boss_kind)
    if not bool(pressure.get("ok", false)):
        return pressure
    for key in [
        "paused",
        "phase",
        "run_seconds",
        "wave_band_id",
        "spawn_budget_per_second",
        "active_cap",
        "composition",
        "band",
        "registry_source"
    ]:
        if pressure.has(key):
            decision[key] = pressure[key]
    decision["pressure"] = pressure
    return decision


func get_timer_snapshot() -> Dictionary:
    return spawn_director.snapshot()


func evaluate_spawn(
        run_seconds: float,
        boss_kind: String,
        active_count: int,
        requested_count: int = 1
    ) -> Dictionary:
    if active_count < 0 or requested_count <= 0:
        return {
            "ok": false,
            "code": "SPAWN_REQUEST_INVALID",
            "active_count": active_count,
            "requested_count": requested_count
        }

    var pressure := resolve(run_seconds, boss_kind)
    if not bool(pressure.get("ok", false)):
        return pressure
    if bool(pressure.get("paused", false)):
        pressure["admitted"] = false
        pressure["code"] = "WAVE_PROGRESSION_BLOCKED"
        return pressure

    var active_cap := int(pressure.get("active_cap", 0))
    if active_count + requested_count > active_cap:
        return {
            "ok": false,
            "admitted": false,
            "code": "ACTIVE_CAP_REACHED",
            "active_count": active_count,
            "requested_count": requested_count,
            "active_cap": active_cap,
            "wave_band_id": pressure.get("wave_band_id", ""),
            "registry_source": pressure.get("registry_source", "")
        }

    pressure["admitted"] = true
    pressure["active_count"] = active_count
    pressure["requested_count"] = requested_count
    return pressure


func _find_main_checkpoint(checkpoint_id: String) -> Dictionary:
    for record in registry.get_main_bosses():
        if str(record.get("checkpoint_id", "")) == checkpoint_id:
            return record.duplicate(true)
    return {}


func _find_cycle_mapping(from_checkpoint_id: String, to_checkpoint_id: String) -> Dictionary:
    var mappings: Variant = registry.get_model_field([
        "simulation_model",
        "boss_wave_ramp",
        "cycle_band_mapping"
    ], [])
    if not (mappings is Array):
        return {}
    for mapping in mappings:
        if not (mapping is Dictionary):
            continue
        if str(mapping.get("from_checkpoint_id", "")) == from_checkpoint_id and str(mapping.get("to_checkpoint_id", "")) == to_checkpoint_id:
            return mapping.duplicate(true)
    return {}


func _checkpoint_seconds(record: Dictionary) -> float:
    for key in ["time_seconds", "target_seconds", "boundary_seconds"]:
        if record.has(key):
            return float(record.get(key, -1.0))
    return -1.0


func _record_value(record: Variant, fallback: Variant) -> Variant:
    if record is Dictionary:
        return record.get("value", fallback)
    return record if record != null else fallback
