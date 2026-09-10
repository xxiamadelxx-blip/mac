extends RefCounted
class_name WaveDirector

## Data-driven wave projection used by R2.
##
## This class never owns balance numbers. It projects the current band and
## reports whether ordinary wave time is allowed to progress for the active
## boss policy.

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
        return {"ok": false, "code": "WAVE_BAND_NOT_FOUND", "run_seconds": run_seconds}

    return {
        "ok": true,
        "paused": false,
        "phase": "MINI_BOSS_PRESSURE" if boss_kind == "MINI_BOSS" else "CANONICAL_WAVE_BANDS",
        "run_seconds": run_seconds,
        "wave_band_id": str(band.get("wave_band_id", "")),
        "spawn_budget_per_second": _record_value(band.get("spawn_budget_per_second", {}), 0.0),
        "active_cap": _record_value(band.get("active_cap", {}), 0),
        "composition": band.get("composition", {}),
        "registry_source": "BALANCE_MODEL.json.wave_bands"
    }


func _record_value(record: Variant, fallback: Variant) -> Variant:
    if record is Dictionary:
        return record.get("value", fallback)
    return record if record != null else fallback
