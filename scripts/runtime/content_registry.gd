extends RefCounted
class_name ContentRegistry

## R1 content boundary.
##
## BALANCE_MODEL.json is loaded at runtime and remains the only source for
## balance values. This class validates shape, provenance and wave boundaries;
## it does not copy tuning numbers into GDScript.

const DEFAULT_PATH := "res://docs/agents/balance-economy/BALANCE_MODEL.json"
const TARGET_RUN_DURATION_SECONDS := 1800.0
const TARGET_MAIN_BOSS_COUNT := 6
const TARGET_MINI_BOSS_COUNT := 5
const REQUIRED_TOP_LEVEL_KEYS := [
    "schema_version",
    "status",
    "model_id",
    "source_of_truth",
    "hero_stats",
    "wave_bands",
    "combat_rules",
    "progression",
    "run_stats_contract",
    "runtime_integration"
]

var data: Dictionary = {}
var diagnostics: Array[Dictionary] = []
var content_version := ""
var loaded_path := ""


func load_and_validate(path: String = DEFAULT_PATH) -> Dictionary:
    data = {}
    diagnostics.clear()
    content_version = ""
    loaded_path = path

    if not FileAccess.file_exists(path):
        _add_diagnostic("CONTENT_FILE_MISSING", "Required balance model does not exist.", {"path": path})
        return _failure()

    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        _add_diagnostic("CONTENT_FILE_OPEN_FAILED", "Required balance model could not be opened.", {"path": path})
        return _failure()

    var parsed: Variant = JSON.parse_string(file.get_as_text())
    if not (parsed is Dictionary):
        _add_diagnostic("CONTENT_JSON_INVALID", "Balance model is not a JSON object.", {"path": path})
        return _failure()

    data = parsed
    _validate_top_level_shape()
    _validate_source_of_truth()
    _validate_wave_bands()
    _validate_hero_stats()
    _validate_combat_rules()
    _validate_progression()

    if not diagnostics.is_empty():
        return _failure()

    content_version = _derive_content_version()
    return {
        "ok": true,
        "content_version": content_version,
        "model_id": str(data.get("model_id", "")),
        "model_status": str(data.get("status", "")),
        "source_path": loaded_path,
        "diagnostics": diagnostics.duplicate(true)
    }


func is_loaded() -> bool:
    return not data.is_empty() and not content_version.is_empty() and diagnostics.is_empty()


func get_wave_band_for_time(seconds: float) -> Dictionary:
    var bands: Array = data.get("wave_bands", [])
    if bands.is_empty() or seconds < 0.0:
        return {}

    for band in bands:
        var start := float(band.get("start_seconds", -1.0))
        var end := float(band.get("end_seconds", -1.0))
        if seconds >= start and seconds < end:
            return band.duplicate(true)

    # Never extend the last source band beyond its declared end. A missing
    # 30-minute band is a content-sync blocker, not permission to reuse tuning.
    return {}


func get_runtime_hero_profile(hero_id: String) -> Dictionary:
    var simulation_model: Dictionary = data.get("simulation_model", {})
    var heroes_and_profiles: Dictionary = simulation_model.get("heroes_and_profiles", {})
    var model_heroes: Dictionary = heroes_and_profiles.get("heroes", {})
    if model_heroes.has(hero_id):
        var profile: Dictionary = model_heroes[hero_id].duplicate(true)
        profile["stats_source_path"] = "simulation_model.heroes_and_profiles.heroes.%s" % hero_id
        profile["stats_source_status"] = "PROPOSED_MODEL_ONLY"
        return profile

    var hero_stats: Dictionary = data.get("hero_stats", {})
    var canonical_heroes: Array = hero_stats.get("heroes", [])
    for hero in canonical_heroes:
        if str(hero.get("hero_id", "")) == hero_id:
            var canonical_profile: Dictionary = hero.duplicate(true)
            canonical_profile["stats_source_path"] = "hero_stats.heroes[%s]" % hero_id
            canonical_profile["stats_source_status"] = "CANON"
            return canonical_profile

    return {}


func get_enemy_fixture(enemy_id: String) -> Dictionary:
    var simulation_model: Dictionary = data.get("simulation_model", {})
    var enemy_stats: Dictionary = simulation_model.get("enemy_stats", {})
    if not enemy_stats.has(enemy_id):
        return {}

    var fixture: Dictionary = enemy_stats[enemy_id].duplicate(true)
    fixture["enemy_id"] = enemy_id
    fixture["source_path"] = "simulation_model.enemy_stats.%s" % enemy_id
    fixture["source_status"] = "PROPOSED_MODEL_ONLY"
    return fixture


func get_weapon_fixture(weapon_id: String) -> Dictionary:
    var simulation_model: Dictionary = data.get("simulation_model", {})
    var build_catalog: Dictionary = simulation_model.get("build_catalog", {})
    var weapons: Dictionary = build_catalog.get("weapons", {})
    if not weapons.has(weapon_id):
        return {}
    var fixture: Dictionary = weapons[weapon_id].duplicate(true)
    fixture["weapon_id"] = weapon_id
    fixture["source_path"] = "simulation_model.build_catalog.weapons.%s" % weapon_id
    fixture["source_status"] = "PROPOSED_MODEL_ONLY"
    return fixture


func get_upgrade_choices(hero_id: String) -> Array[Dictionary]:
    var profile := get_runtime_hero_profile(hero_id)
    var starting_weapon := str(profile.get("starting_weapon_id", ""))
    var starting_passive := str(profile.get("starting_passive_id", ""))
    var simulation_model: Dictionary = data.get("simulation_model", {})
    var build_catalog: Dictionary = simulation_model.get("build_catalog", {})
    var offer_model: Dictionary = build_catalog.get("offer_model", {})
    var fallback: Dictionary = offer_model.get("fallback", {})
    var fallback_id := str(fallback.get("id", ""))

    var choices: Array[Dictionary] = []
    if not starting_weapon.is_empty() and not get_weapon_fixture(starting_weapon).is_empty():
        choices.append({
            "choice_id": starting_weapon,
            "kind": "WEAPON_UPGRADE",
            "source_path": "simulation_model.build_catalog.weapons.%s" % starting_weapon,
            "source_status": "PROPOSED_MODEL_ONLY"
        })
    if not starting_passive.is_empty():
        choices.append({
            "choice_id": starting_passive,
            "kind": "PASSIVE_UPGRADE",
            "source_path": "simulation_model.heroes_and_profiles.heroes.%s" % hero_id,
            "source_status": "PROPOSED_MODEL_ONLY"
        })
    if not fallback_id.is_empty():
        choices.append({
            "choice_id": fallback_id,
            "kind": _record_value(fallback.get("type", "PENDING_UPGRADE"), "PENDING_UPGRADE"),
            "source_path": "simulation_model.build_catalog.offer_model.fallback",
            "source_status": _record_status(fallback.get("type", {}), "PROPOSED")
        })
    return choices


func get_upgrade_choice_count() -> int:
    var simulation_model: Dictionary = data.get("simulation_model", {})
    var build_catalog: Dictionary = simulation_model.get("build_catalog", {})
    var offer_model: Dictionary = build_catalog.get("offer_model", {})
    return int(_record_value(offer_model.get("choice_count", 0), 0))


func get_xp_drop_values() -> Array:
    var progression: Dictionary = data.get("progression", {})
    var record: Dictionary = progression.get("xp_drop_values", {})
    return record.get("value", [])


func get_xp_to_next(level: int) -> int:
    var progression: Dictionary = data.get("progression", {})
    var formula_record: Dictionary = progression.get("xp_to_next_formula", {})
    var formula := str(formula_record.get("value", ""))
    if formula.is_empty():
        _add_diagnostic("XP_FORMULA_MISSING", "The registry has no level-up formula.")
        return -1

    # B1 writes exponentiation as '^'. GDScript Expression uses '**'.
    var expression := Expression.new()
    var parse_error := expression.parse(formula.replace("^", "**"), PackedStringArray(["L"]))
    if parse_error != OK:
        _add_diagnostic("XP_FORMULA_INVALID", "The registry level-up formula could not be parsed.", {"formula": formula})
        return -1

    var result: Variant = expression.execute([level])
    if expression.has_execute_failed():
        _add_diagnostic("XP_FORMULA_EXECUTION_FAILED", "The registry level-up formula failed during evaluation.", {"level": level})
        return -1
    return int(round(float(result)))


func get_contact_damage_cooldown() -> float:
    var combat_rules: Dictionary = data.get("combat_rules", {})
    var record: Dictionary = combat_rules.get("contact_damage_cooldown_seconds", {})
    return float(record.get("value", -1.0))


func get_main_bosses() -> Array[Dictionary]:
    var result: Array[Dictionary] = []
    var records: Variant = data.get("main_bosses", data.get("boss_checkpoints", []))
    if records is Array:
        for record in records:
            if record is Dictionary and str(record.get("encounter_kind", "MAIN_BOSS")) != "MINI_BOSS":
                _append_unique_record(result, _normalize_encounter_record(record, "MAIN_BOSS"))
    return result


func get_mini_bosses() -> Array[Dictionary]:
    var result: Array[Dictionary] = []
    var sources: Array = [data.get("mini_bosses", [])]
    var simulation_model: Dictionary = data.get("simulation_model", {})
    sources.append(simulation_model.get("mini_bosses", []))
    for source_key in ["boss_checkpoints", "main_bosses"]:
        var checkpoint_records: Variant = data.get(source_key, [])
        if checkpoint_records is Array:
            var checkpoint_minis: Array[Dictionary] = []
            for record in checkpoint_records:
                if record is Dictionary and str(record.get("encounter_kind", "")) == "MINI_BOSS":
                    checkpoint_minis.append(record.duplicate(true))
            sources.append(checkpoint_minis)
    for source in sources:
        if not (source is Array):
            continue
        for record in source:
            if record is Dictionary:
                _append_unique_record(result, _normalize_encounter_record(record, "MINI_BOSS"))
    return result


func get_checkpoint_reward(checkpoint_id: String) -> Dictionary:
    var rewards: Dictionary = data.get("rewards", {})
    var records: Variant = rewards.get("checkpoint_rewards", [])
    if records is Array:
        for record in records:
            if record is Dictionary and str(record.get("checkpoint_id", "")) == checkpoint_id:
                return record.duplicate(true)
    return {}


func is_final_checkpoint(checkpoint_id: String) -> bool:
    var records := get_main_bosses()
    if records.is_empty():
        return false
    return str(records.back().get("checkpoint_id", "")) == checkpoint_id


func get_boss_wave_ramp() -> Dictionary:
    var simulation_model: Dictionary = data.get("simulation_model", {})
    var ramp: Variant = simulation_model.get("boss_wave_ramp", {})
    return ramp.duplicate(true) if ramp is Dictionary else {}


func get_artifact_offer_model() -> Dictionary:
    var simulation_model: Dictionary = data.get("simulation_model", {})
    var build_catalog: Dictionary = simulation_model.get("build_catalog", {})
    var offer_model: Dictionary = build_catalog.get("offer_model", {})
    var artifact_offer: Variant = offer_model.get("artifact_offer", {})
    if artifact_offer is Dictionary and not artifact_offer.is_empty():
        return artifact_offer.duplicate(true)
    var artifact_model: Variant = simulation_model.get("artifact_offer_model", {})
    if artifact_model is Dictionary:
        return artifact_model.duplicate(true)
    return {}


func get_artifact_effect_types() -> Array:
    var model := get_artifact_offer_model()
    var effect_types: Variant = model.get("effect_types", [])
    return effect_types.duplicate(true) if effect_types is Array else []


func get_run_duration_seconds() -> float:
    var simulation_model: Dictionary = data.get("simulation_model", {})
    var record: Variant = simulation_model.get("main_run_duration_seconds", {})
    return float(_record_value(record, 0.0))


func get_elite_variants() -> Array[Dictionary]:
    var result: Array[Dictionary] = []
    var sources: Array = [data.get("elite_variants", [])]
    var simulation_model: Dictionary = data.get("simulation_model", {})
    sources.append(simulation_model.get("elite_variants", []))
    for source in sources:
        if not (source is Array):
            continue
        for record in source:
            if record is Dictionary:
                _append_unique_record(result, _normalize_elite_variant(record))
    return result


func get_wave_envelope_status() -> Dictionary:
    var bands: Variant = data.get("wave_bands", [])
    var coverage_end := 0.0
    var contiguous := true
    var expected_start := 0.0
    if bands is Array:
        for index in range(bands.size()):
            var band: Variant = bands[index]
            if not (band is Dictionary):
                contiguous = false
                continue
            var start := float(band.get("start_seconds", -1.0))
            var end := float(band.get("end_seconds", -1.0))
            if index == 0 and not is_equal_approx(start, 0.0):
                contiguous = false
            if not is_equal_approx(start, expected_start) or end <= start:
                contiguous = false
            expected_start = end
            coverage_end = max(coverage_end, end)
    return {
        "source_path": "BALANCE_MODEL.json.wave_bands",
        "declared_duration_seconds": get_run_duration_seconds(),
        "coverage_end_seconds": coverage_end,
        "target_duration_seconds": TARGET_RUN_DURATION_SECONDS,
        "contiguous": contiguous,
        "ready_for_target": contiguous and coverage_end >= TARGET_RUN_DURATION_SECONDS
    }


func get_r2_content_status() -> Dictionary:
    var main_bosses := get_main_bosses()
    var mini_bosses := get_mini_bosses()
    var elite_variants := get_elite_variants()
    var wave_status := get_wave_envelope_status()
    var blockers: Array[String] = []
    var main_count := _count_stable_records(main_bosses, "boss_id")
    var mini_count := _count_stable_records(mini_bosses, "boss_id")
    var elite_count := _count_stable_records(elite_variants, "variant_id")

    if main_count != TARGET_MAIN_BOSS_COUNT:
        blockers.append("MAIN_BOSS_ROSTER_COUNT")
    if mini_count != TARGET_MINI_BOSS_COUNT:
        blockers.append("MINI_BOSS_ROSTER_COUNT")
    if elite_count == 0:
        blockers.append("ELITE_VARIANT_CONTENT")
    if float(wave_status.get("declared_duration_seconds", 0.0)) < TARGET_RUN_DURATION_SECONDS:
        blockers.append("RUN_DURATION_CONTENT")
    if not bool(wave_status.get("ready_for_target", false)):
        blockers.append("WAVE_ENVELOPE_CONTENT")

    return {
        "status": "READY" if blockers.is_empty() else "PENDING_CONTENT_SYNC",
        "source_path": "BALANCE_MODEL.json",
        "target_duration_seconds": TARGET_RUN_DURATION_SECONDS,
        "declared_duration_seconds": wave_status.get("declared_duration_seconds", 0.0),
        "wave_coverage_end_seconds": wave_status.get("coverage_end_seconds", 0.0),
        "target_main_boss_count": TARGET_MAIN_BOSS_COUNT,
        "available_main_boss_count": main_count,
        "target_mini_boss_count": TARGET_MINI_BOSS_COUNT,
        "available_mini_boss_count": mini_count,
        "available_elite_variant_count": elite_count,
        "blockers": blockers
    }


func get_chest_eligibility(offer_type: String) -> Dictionary:
    var simulation_model: Dictionary = data.get("simulation_model", {})
    var build_catalog: Dictionary = simulation_model.get("build_catalog", {})
    var offer_model: Dictionary = build_catalog.get("offer_model", {})
    var key := "boss_chest"
    if offer_type == "MINI_BOSS_CHEST":
        key = "mini_boss_chest"
    elif offer_type == "ELITE_CHEST":
        key = "elite_chest"
    var eligibility: Variant = offer_model.get(key, {})
    if eligibility is Dictionary and not eligibility.is_empty():
        return eligibility.duplicate(true)
    return {
        "status": "PENDING_CONTENT_SYNC",
        "source_path": "simulation_model.build_catalog.offer_model.%s" % key
    }


func get_model_field(path: Array[String], fallback: Variant = null) -> Variant:
    var current: Variant = data
    for segment in path:
        if not (current is Dictionary) or not current.has(segment):
            return fallback
        current = current[segment]
    return current


func _normalize_encounter_record(record: Dictionary, kind: String) -> Dictionary:
    var normalized := record.duplicate(true)
    var record_id := str(record.get("boss_id", record.get("mini_boss_id", record.get("id", ""))))
    if not record_id.is_empty():
        normalized["boss_id"] = record_id
        if kind == "MINI_BOSS":
            normalized["mini_boss_id"] = record_id
    normalized["encounter_kind"] = kind
    normalized["source_path"] = str(record.get("source_path", record.get("source", record.get("boss_source", "BALANCE_MODEL.json"))))
    normalized["content_status"] = str(record.get("content_status", record.get("boss_status", record.get("status", "PENDING_CONTENT_SYNC"))))
    return normalized


func _normalize_elite_variant(record: Dictionary) -> Dictionary:
    var normalized := record.duplicate(true)
    var variant_id := str(record.get("variant_id", record.get("elite_variant_id", record.get("id", ""))))
    if not variant_id.is_empty():
        normalized["variant_id"] = variant_id
    normalized["source_path"] = str(record.get("source_path", record.get("source", "BALANCE_MODEL.json")))
    normalized["content_status"] = str(record.get("content_status", record.get("status", "PENDING_CONTENT_SYNC")))
    return normalized


func _append_unique_record(target: Array[Dictionary], record: Dictionary) -> void:
    var identity := _record_identity(record)
    if identity.is_empty():
        target.append(record)
        return
    for existing in target:
        if _record_identity(existing) == identity:
            return
    target.append(record)


func _record_identity(record: Dictionary) -> String:
    var encounter_kind := str(record.get("encounter_kind", ""))
    var record_id := str(record.get("boss_id", record.get("mini_boss_id", record.get("variant_id", record.get("elite_variant_id", record.get("id", ""))))))
    if record_id.is_empty():
        return ""
    var checkpoint_id := str(record.get("checkpoint_id", record.get("window_id", "")))
    return "%s:%s:%s" % [encounter_kind, record_id, checkpoint_id]


func _count_stable_records(records: Array[Dictionary], id_key: String) -> int:
    var count := 0
    for record in records:
        if not str(record.get(id_key, "")).is_empty():
            count += 1
    return count


func _validate_top_level_shape() -> void:
    for key in REQUIRED_TOP_LEVEL_KEYS:
        if not data.has(key):
            _add_diagnostic("CONTENT_KEY_MISSING", "Balance model is missing a required top-level key.", {"key": key})


func _validate_source_of_truth() -> void:
    var source: Variant = data.get("source_of_truth", null)
    if not (source is Dictionary):
        _add_diagnostic("CONTENT_SOURCE_INVALID", "source_of_truth must be an object.")
        return
    for key in ["path", "version", "source_revision"]:
        if not source.has(key) or str(source.get(key, "")).is_empty():
            _add_diagnostic("CONTENT_SOURCE_FIELD_MISSING", "source_of_truth is missing provenance.", {"key": key})


func _validate_wave_bands() -> void:
    var bands: Variant = data.get("wave_bands", null)
    if not (bands is Array) or bands.is_empty():
        _add_diagnostic("WAVE_BANDS_INVALID", "wave_bands must be a non-empty array.")
        return

    var previous_end := 0.0
    for index in range(bands.size()):
        var band: Variant = bands[index]
        if not (band is Dictionary):
            _add_diagnostic("WAVE_BAND_INVALID", "Every wave band must be an object.", {"index": index})
            continue
        for key in ["wave_band_id", "start_seconds", "end_seconds", "spawn_budget_per_second", "active_cap", "composition"]:
            if not band.has(key):
                _add_diagnostic("WAVE_BAND_FIELD_MISSING", "Wave band is missing a required field.", {"index": index, "key": key})
        var start := float(band.get("start_seconds", -1.0))
        var end := float(band.get("end_seconds", -1.0))
        if index == 0 and not is_equal_approx(start, 0.0):
            _add_diagnostic("WAVE_BAND_START_INVALID", "The first wave band must start at zero.")
        if not is_equal_approx(start, previous_end):
            _add_diagnostic("WAVE_BAND_GAP", "Wave bands must be contiguous.", {"index": index, "expected_start": previous_end, "actual_start": start})
        if end <= start:
            _add_diagnostic("WAVE_BAND_RANGE_INVALID", "Wave band end must be greater than start.", {"index": index})
        previous_end = end
        _validate_numeric_record(band.get("spawn_budget_per_second", null), "WAVE_BAND_SPAWN_BUDGET", index)
        _validate_numeric_record(band.get("active_cap", null), "WAVE_BAND_ACTIVE_CAP", index)


func _validate_hero_stats() -> void:
    var hero_stats: Variant = data.get("hero_stats", null)
    if not (hero_stats is Dictionary):
        _add_diagnostic("HERO_STATS_INVALID", "hero_stats must be an object.")
        return
    var heroes: Variant = hero_stats.get("heroes", null)
    if not (heroes is Array) or heroes.is_empty():
        _add_diagnostic("HERO_STATS_EMPTY", "hero_stats.heroes must be a non-empty array.")
        return
    for index in range(heroes.size()):
        var hero: Variant = heroes[index]
        if not (hero is Dictionary):
            _add_diagnostic("HERO_RECORD_INVALID", "Every hero record must be an object.", {"index": index})
            continue
        if str(hero.get("hero_id", "")).is_empty():
            _add_diagnostic("HERO_ID_MISSING", "Hero record has no stable ID.", {"index": index})
        _validate_numeric_record(hero.get("hp", null), "HERO_HP", index)
        _validate_numeric_record(hero.get("move_speed_percent", null), "HERO_SPEED", index)


func _validate_combat_rules() -> void:
    var combat_rules: Variant = data.get("combat_rules", null)
    if not (combat_rules is Dictionary):
        _add_diagnostic("COMBAT_RULES_INVALID", "combat_rules must be an object.")
        return
    _validate_numeric_record(combat_rules.get("contact_damage_cooldown_seconds", null), "CONTACT_COOLDOWN", -1)


func _validate_progression() -> void:
    var progression: Variant = data.get("progression", null)
    if not (progression is Dictionary):
        _add_diagnostic("PROGRESSION_INVALID", "progression must be an object.")
        return
    var drops: Variant = progression.get("xp_drop_values", null)
    if not (drops is Dictionary) or not (drops.get("value", []) is Array) or drops.get("value", []).is_empty():
        _add_diagnostic("XP_DROPS_INVALID", "progression.xp_drop_values.value must be a non-empty array.")
    var formula_record: Variant = progression.get("xp_to_next_formula", null)
    if not (formula_record is Dictionary):
        _add_diagnostic("XP_FORMULA_MISSING", "progression.xp_to_next_formula.value is required.")
    elif str(formula_record.get("value", "")).is_empty():
        _add_diagnostic("XP_FORMULA_MISSING", "progression.xp_to_next_formula.value is required.")


func _record_value(record: Variant, fallback: Variant = null) -> Variant:
    if record is Dictionary:
        return record.get("value", fallback)
    return record if record != null else fallback


func _record_status(record: Variant, fallback: String) -> String:
    if record is Dictionary:
        return str(record.get("status", fallback))
    return fallback


func _validate_numeric_record(record: Variant, code: String, index: int) -> void:
    if not (record is Dictionary):
        _add_diagnostic("%s_RECORD_INVALID" % code, "Expected a numeric provenance record.", {"index": index})
        return
    var value: Variant = record.get("value", null)
    if typeof(value) != TYPE_INT and typeof(value) != TYPE_FLOAT:
        _add_diagnostic("%s_VALUE_INVALID" % code, "Numeric provenance record has no numeric value.", {"index": index})


func _derive_content_version() -> String:
    var source: Dictionary = data.get("source_of_truth", {})
    return "%s:%s@%s" % [str(data.get("model_id", "")), str(data.get("schema_version", "")), str(source.get("source_revision", ""))]


func _failure() -> Dictionary:
    return {
        "ok": false,
        "content_version": "",
        "source_path": loaded_path,
        "diagnostics": diagnostics.duplicate(true)
    }


func _add_diagnostic(code: String, message: String, details: Dictionary = {}) -> void:
    var item := {"code": code, "message": message}
    for key in details:
        item[key] = details[key]
    diagnostics.append(item)
