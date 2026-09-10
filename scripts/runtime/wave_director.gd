extends RefCounted
class_name WaveDirector

## Data-driven wave projection used by R2.
##
## This class never owns balance numbers. It projects the current band and
## reports whether ordinary wave time is allowed to progress for the active
## boss policy. Spawn admission is also derived from the same registry record,
## so active-cap enforcement cannot drift into a controller constant.

var registry: Object


func _init(p_registry: Object) -> void:
    registry = p_registry


func resolve(run_seconds: float, boss_kind: String = "") -> Dictionary:
    if boss_kind == "MAIN_BOSS":
        return {
            "ok": true,
            "paused": true,
            "phase": "MAIN_BOSS_FREEZE",
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
        "paused": false,
        "phase": "MINI_BOSS_PRESSURE" if boss_kind == "MINI_BOSS" else "CANONICAL_WAVE_BANDS",
        "run_seconds": run_seconds,
        "wave_band_id": str(band.get("wave_band_id", "")),
        "spawn_budget_per_second": _record_value(band.get("spawn_budget_per_second", {}), 0.0),
        "active_cap": _record_value(band.get("active_cap", {}), 0),
        "composition": band.get("composition", {}),
        "band": band.duplicate(true),
        "registry_source": "BALANCE_MODEL.json.wave_bands"
    }


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


func _record_value(record: Variant, fallback: Variant) -> Variant:
    if record is Dictionary:
        return record.get("value", fallback)
    return record if record != null else fallback
