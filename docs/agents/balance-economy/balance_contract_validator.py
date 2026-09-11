#!/usr/bin/env python3
"""Validate the Balance-owned 30-minute model without hiding join blockers.

This check validates the data shape owned by Balance. It deliberately does
not turn a stale Architecture/Content contract into a false model failure:
those mismatches are reported as an explicit architecture_join warning. A
PASS here is a model/registry-shape pass, never Godot evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def unwrap(value: Any) -> Any:
    if isinstance(value, dict) and "value" in value:
        return value["value"]
    return value


def number(value: Any) -> float:
    return float(unwrap(value))


def error(errors: List[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def check_provenance(errors: List[str], value: Any, label: str) -> None:
    """Require an explicit numeric provenance object for content tuning."""
    if not isinstance(value, dict) or "value" not in value:
        error(errors, False, f"{label} is not an explicit value/provenance record")
        return
    for field in ("source", "derived_formula", "rationale", "status"):
        error(errors, field in value and bool(value[field]), f"{label} lacks {field}")
    error(
        errors,
        value.get("status") in {"CANON", "DERIVED", "PROPOSED", "PENDING_B1", "PENDING_PRODUCT_DECISION", "BLOCKED"},
        f"{label} has unsupported status {value.get('status')!r}",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    here = Path(__file__).resolve().parent
    parser.add_argument("--model", type=Path, default=here / "BALANCE_MODEL.json")
    parser.add_argument(
        "--architecture",
        type=Path,
        default=here / "../../architecture/first-run/FIRST_RUN_DATA_CONTRACT.json",
        help="Optional legacy/architecture contract used only to report join drift.",
    )
    parser.add_argument(
        "--variant-map",
        type=Path,
        default=here / "../architecture/REGISTRY_VARIANT_MAP.json",
        help="Optional REF-ARCH-02 map used only to report ID reconciliation.",
    )
    args = parser.parse_args()

    try:
        model = load_json(args.model)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BALANCE_MODEL_CHECK=ERROR: {exc}", file=sys.stderr)
        return 2

    errors: List[str] = []
    join_warnings: List[str] = []
    simulation = model.get("simulation_model", {})
    schedule = simulation.get("run_schedule", {})
    main_schedule = schedule.get("main_boss_checkpoints", [])
    mini_schedule = schedule.get("mini_boss_checkpoints", [])
    waves = model.get("wave_bands", [])
    roster = simulation.get("content_roster", {})
    elite_policy = simulation.get("elite_variation_policy", {})

    error(errors, model.get("status") == "PARTIAL", "model status must remain PARTIAL")
    error(errors, simulation.get("status") == "PROPOSED_MODEL_ONLY", "simulation_model must remain PROPOSED_MODEL_ONLY")
    allowed_runtime_statuses = {
        "NOT_IMPLEMENTED",
        "R2_STRUCTURAL_ONLY_PENDING_FRESH_TRACE",
    }
    error(errors, model.get("runtime_status") in allowed_runtime_statuses, "runtime_status is not an allowed evidence state")
    error(errors, simulation.get("runtime_status") in allowed_runtime_statuses, "simulation runtime_status is not an allowed evidence state")
    error(errors, isinstance(model.get("source_of_truth", {}).get("source_revision"), str), "B1 source revision is missing")
    error(errors, number(simulation.get("main_run_duration_seconds", -1)) == 1800, "model duration must be 1800 seconds")
    error(errors, number(schedule.get("duration_seconds", -1)) == 1800, "schedule duration must be 1800 seconds")
    error(errors, number(schedule.get("duration_seconds", -1)) == number(simulation.get("main_run_duration_seconds", -2)), "schedule duration must match main run duration")

    error(errors, len(waves) == 7, "30-minute model must expose seven wave bands")
    expected_start = 0.0
    for index, band in enumerate(waves):
        start = number(band.get("start_seconds", -1))
        end = number(band.get("end_seconds", -1))
        error(errors, start == expected_start, f"wave band {index} is not contiguous")
        error(errors, end > start, f"wave band {index} has invalid range")
        for field in ("spawn_budget_per_second", "active_cap", "composition"):
            field_value = band.get(field, {})
            error(errors, isinstance(field_value, dict) and "source" in field_value and "status" in field_value, f"wave band {index} field {field} lacks provenance")
        expected_start = end
    error(errors, expected_start == 1800, "wave envelope must end at 1800 seconds")

    error(errors, len(main_schedule) == 6, "schedule must expose six main checkpoints")
    error(errors, len(mini_schedule) == 5, "schedule must expose five mini checkpoints")
    main_times = [int(number(row.get("time_seconds", -1))) for row in main_schedule]
    mini_times = [int(number(row.get("time_seconds", -1))) for row in mini_schedule]
    error(errors, main_times == [300, 600, 900, 1200, 1500, 1800], "main checkpoint schedule drifted")
    error(errors, mini_times == [450, 750, 1050, 1350, 1650], "mini-boss schedule drifted")
    error(errors, not set(main_times).intersection(mini_times), "main and mini checkpoints overlap")
    error(errors, simulation.get("boss_clock_policy", {}).get("checkpoint_seconds") == main_times, "main clock policy is not bound to all main checkpoints")
    error(errors, simulation.get("mini_boss_clock_policy", {}).get("checkpoint_seconds") == mini_times, "mini clock policy is not bound to all mini checkpoints")
    error(errors, simulation.get("boss_clock_policy", {}).get("run_clock_stops_at_boss_checkpoint") is True, "main-boss freeze policy is missing")
    error(errors, simulation.get("mini_boss_clock_policy", {}).get("run_clock_stops_at_checkpoint") is False, "mini-boss continuation policy is missing")

    main_registry = model.get("main_bosses", [])
    mini_registry = model.get("mini_bosses", [])
    elite_registry = model.get("elite_variants", [])
    error(errors, len(main_registry) == 6, "top-level main_bosses must contain six records for ContentRegistry")
    error(errors, len(mini_registry) == 5, "top-level mini_bosses must contain five records for ContentRegistry")
    error(errors, len(elite_registry) == 10, "top-level elite_variants must contain ten mapped records for ContentRegistry")

    schedule_main_by_id = {str(row.get("checkpoint_id")): row for row in main_schedule}
    for record in main_registry:
        checkpoint_id = str(record.get("checkpoint_id", ""))
        scheduled = schedule_main_by_id.get(checkpoint_id)
        error(errors, scheduled is not None, f"main registry references unknown checkpoint {checkpoint_id}")
        if scheduled is not None:
            error(errors, record.get("boss_id") == scheduled.get("boss_id"), f"main registry boss drift at {checkpoint_id}")
            error(errors, int(record.get("time_seconds", -1)) == int(scheduled.get("time_seconds", -2)), f"main registry time drift at {checkpoint_id}")
        error(errors, bool(record.get("stats_ref")), f"main registry has no stats_ref at {checkpoint_id}")

    schedule_mini_by_id = {str(row.get("checkpoint_id")): row for row in mini_schedule}
    for record in mini_registry:
        checkpoint_id = str(record.get("checkpoint_id", ""))
        scheduled = schedule_mini_by_id.get(checkpoint_id)
        error(errors, scheduled is not None, f"mini registry references unknown checkpoint {checkpoint_id}")
        if scheduled is not None:
            error(errors, record.get("boss_id") == scheduled.get("boss_id"), f"mini registry boss drift at {checkpoint_id}")
            error(errors, int(record.get("time_seconds", -1)) == int(scheduled.get("time_seconds", -2)), f"mini registry time drift at {checkpoint_id}")
        error(errors, bool(record.get("stats_ref")), f"mini registry has no stats_ref at {checkpoint_id}")

    ordinary_ids = list(unwrap(roster.get("ordinary_enemy_ids", [])))
    proposed_variant_ids = list(unwrap(roster.get("elite_variant_ids", [])))
    selected_variant_ids = list(unwrap(elite_policy.get("variant_ids", [])))
    registered_cap = int(number(roster.get("registered_variant_cap", 0)))
    ordinary_registry = model.get("ordinary_enemies", [])
    error(errors, len(ordinary_ids) == 10 and len(set(ordinary_ids)) == 10, "ordinary content roster must contain ten unique IDs")
    error(errors, {str(row.get("enemy_id")) for row in ordinary_registry} == set(ordinary_ids), "ordinary registry does not match the ten mapped content IDs")
    error(errors, all(str(row.get("stats_ref", "")).startswith("simulation_model.enemy_stats.") for row in ordinary_registry), "ordinary registry is missing numeric stats references")
    error(errors, len(proposed_variant_ids) == 10 and len(set(proposed_variant_ids)) == 10, "elite content roster must contain ten unique IDs")
    error(errors, len(selected_variant_ids) == 10 and len(set(selected_variant_ids)) == 10, "elite policy must retain the complete ten-ID catalog")
    active_selection = elite_policy.get("active_selection", {})
    active_cap = int(number(active_selection.get("max_active_records", 0))) if active_selection.get("max_active_records") else 0
    error(errors, 0 < active_cap <= registered_cap <= 5, "active elite projection exceeds the maximum-five cap")
    error(errors, active_selection.get("selection_inputs") == ["content_version", "run_seed", "wave_cycle_id", "state_revision"], "active elite selection inputs drifted")
    error(errors, bool(active_selection.get("selection_key_template")), "active elite selection key template is missing")
    registry_variant_ids = {str(row.get("variant_id", "")) for row in elite_registry}
    error(errors, registry_variant_ids == set(proposed_variant_ids), "elite registry does not match the ten mapped content IDs")
    error(errors, set(selected_variant_ids) == registry_variant_ids, "elite policy references IDs outside the mapped registry")
    overlay_records = elite_policy.get("variant_overrides", {}).get("records", {})
    overlay_provenance = elite_policy.get("variant_overrides", {}).get("record_provenance", {})
    error(errors, set(proposed_variant_ids).issubset(overlay_records), "one or more mapped elite variants lacks a numeric overlay")
    error(errors, set(proposed_variant_ids).issubset(set(overlay_provenance.get("record_ids", []))), "elite overlay provenance does not cover all mapped variants")
    error(errors, overlay_provenance.get("status") == "PROPOSED" and len(overlay_provenance.get("fields", [])) == 4, "elite overlay provenance is incomplete")
    for variant_id in proposed_variant_ids:
        record = overlay_records.get(variant_id, {})
        error(errors, bool(record.get("base_enemy_id")), f"elite overlay has no base_enemy_id: {variant_id}")
        for stat_path in ("hp_multiplier", "damage_multiplier", "speed_multiplier", "xp_multiplier"):
            check_provenance(errors, record.get(stat_path), f"{variant_id}.{stat_path}")
        for stat_path in ("hp", "atk", "speed"):
            check_provenance(errors, record.get("resolved_base_stats", {}).get(stat_path), f"{variant_id}.resolved_base_stats.{stat_path}")
        for stat_path in ("hp", "atk", "speed"):
            check_provenance(errors, record.get("late_run_effective_stats", {}).get(stat_path), f"{variant_id}.late_run_effective_stats.{stat_path}")
    enemy_stats = simulation.get("enemy_stats", {})
    error(errors, all(enemy_id in enemy_stats for enemy_id in ordinary_ids), "one or more ordinary content IDs lacks numeric stats")
    error(errors, simulation.get("boss_stats", {}).keys() >= {str(row.get("checkpoint_id")) for row in main_schedule}, "one or more main checkpoints lacks stats")
    error(errors, simulation.get("mini_boss_stats", {}).keys() >= {str(row.get("boss_id")) for row in mini_schedule}, "one or more mini-boss checkpoints lacks stats")

    # Full content binding is Balance-owned.  The model must expose every
    # content record in one JSON source; the simulator must not have to invent
    # the remaining eight weapons/passives/synergies or any artifact effects.
    catalog = simulation.get("build_catalog", {})
    check_provenance(errors, catalog.get("weapon_max_level"), "build_catalog.weapon_max_level")
    check_provenance(errors, catalog.get("passive_max_rank"), "build_catalog.passive_max_rank")
    expected_weapons = {
        "weapon_moon_blade", "weapon_jade_talismans", "weapon_crimson_flame_fan",
        "weapon_frost_pearl", "weapon_thunder_needles", "weapon_spirit_bell",
        "weapon_fox_mirage", "weapon_lotus_mines", "weapon_star_bow",
        "weapon_black_eclipse_umbrella",
    }
    expected_passives = {
        "passive_wind_of_travel", "passive_jade_focus", "passive_ember_heart",
        "passive_frost_thread", "passive_heavenly_seal", "passive_iron_bell",
        "passive_mirror_shard", "passive_lotus_heart", "passive_star_compass",
        "passive_spirit_lens",
    }
    expected_synergies = {
        "synergy_moon_dance", "synergy_heavenly_seals", "synergy_phoenix_sky",
        "synergy_winter_palace", "synergy_heavenly_judgment", "synergy_guardian_bell",
        "synergy_nine_reflections", "synergy_lotus_sanctuary", "synergy_constellation_rain",
        "synergy_eclipse_vortex",
    }
    expected_artifacts = {
        "artifact_jade_compass", "artifact_mirror_shard", "artifact_phoenix_feather",
        "artifact_frost_bead", "artifact_bell_fragment", "artifact_lotus_seed",
        "artifact_moon_crown", "artifact_black_bead", "artifact_tideglass",
        "artifact_silent_lantern",
    }
    for field, expected in (("weapons", expected_weapons), ("passives", expected_passives), ("synergies", expected_synergies), ("artifacts", expected_artifacts)):
        actual = set(catalog.get(field, {}))
        error(errors, actual == expected, f"full content catalog {field} is incomplete or has drifted IDs")
        for content_id in expected:
            record = catalog.get(field, {}).get(content_id, {})
            error(errors, bool(record.get("content_description")), f"{field}.{content_id} lacks content description")
            error(errors, record.get("balance_status") == "PROPOSED", f"{field}.{content_id} must remain explicitly PROPOSED")
            if field == "weapons":
                for numeric_field in ("base_damage", "attack_interval_seconds", "targets_per_attack", "range_world_units", "area_radius_world_units", "projectile_speed_world_units_per_second", "lifetime_seconds", "pierce_or_chain_limit", "knockback_world_units", "status_duration_seconds"):
                    check_provenance(errors, record.get(numeric_field), f"{field}.{content_id}.{numeric_field}")
                for numeric_field in ("damage_multiplier", "attack_interval_multiplier", "area_multiplier", "extra_targets", "effect_duration_seconds"):
                    check_provenance(errors, record.get("evolution", {}).get(numeric_field), f"{field}.{content_id}.evolution.{numeric_field}")
            elif field == "passives":
                for numeric_field in ("damage_per_rank", "defense_per_rank", "primary_value_per_rank", "trigger_cooldown_seconds", "effect_duration_seconds", "stack_cap"):
                    check_provenance(errors, record.get(numeric_field), f"{field}.{content_id}.{numeric_field}")
            elif field == "synergies":
                for numeric_field in ("damage_multiplier", "attack_interval_multiplier", "area_multiplier", "extra_targets", "effect_duration_seconds", "requires_weapon_level", "requires_passive_rank"):
                    check_provenance(errors, record.get(numeric_field), f"{field}.{content_id}.{numeric_field}")
            else:
                for numeric_field in record.get("effect_parameters", {}):
                    check_provenance(errors, record["effect_parameters"].get(numeric_field), f"{field}.{content_id}.effect_parameters.{numeric_field}")

    error(errors, len(model.get("content_balance_binding", {}).get("source_documents", {})) >= 8, "content balance binding lacks source document evidence")
    error(errors, model.get("content_balance_binding", {}).get("status") == "PROPOSED_MODEL_ONLY", "content balance binding status is missing")
    error(errors, not any("extension_slot" in str(row.get("boss_id", "")) for row in main_schedule), "main schedule still contains placeholder boss IDs")
    error(errors, not any("pending_" in str(row.get("boss_id", "")) or "extension_slot" in str(row.get("boss_id", "")) for row in mini_schedule), "mini schedule still contains placeholder boss IDs")
    for enemy_id in ordinary_ids:
        record = enemy_stats.get(enemy_id, {})
        error(errors, bool(record.get("content_description")), f"ordinary enemy lacks content description: {enemy_id}")
        for stat_path in ("hp", "atk", "speed"):
            check_provenance(errors, record.get("resolved_base_stats", {}).get(stat_path), f"{enemy_id}.resolved_base_stats.{stat_path}")
            check_provenance(errors, record.get("late_run_effective_stats", {}).get(stat_path), f"{enemy_id}.late_run_effective_stats.{stat_path}")
    for checkpoint_id, record in simulation.get("boss_stats", {}).items():
        if checkpoint_id in {str(row.get("checkpoint_id")) for row in main_schedule}:
            error(errors, bool(record.get("content_description")), f"main boss lacks content description: {checkpoint_id}")
            error(errors, record.get("balance_status") == "PROPOSED", f"main boss numeric binding must remain PROPOSED: {checkpoint_id}")
            for stat_path in ("base_hp", "base_damage", "base_speed", "attack_interval_seconds", "telegraph_seconds"):
                check_provenance(errors, record.get(stat_path), f"{checkpoint_id}.{stat_path}")
    for boss_id in {str(row.get("boss_id")) for row in mini_schedule}:
        record = simulation.get("mini_boss_stats", {}).get(boss_id, {})
        error(errors, bool(record.get("content_description")), f"mini boss lacks content description: {boss_id}")
        error(errors, record.get("balance_status") == "PROPOSED", f"mini boss numeric binding must remain PROPOSED: {boss_id}")
        for stat_path in ("base_hp", "base_damage", "base_speed", "attack_interval_seconds", "telegraph_seconds", "xp_value"):
            check_provenance(errors, record.get(stat_path), f"{boss_id}.{stat_path}")

    ramp = simulation.get("boss_wave_ramp", {})
    error(errors, ramp.get("status") == "PROPOSED", "post-boss ramp must remain explicitly PROPOSED")
    error(errors, ramp.get("ramp_curve", {}).get("value") == "LINEAR", "post-boss ramp must be linear")
    error(errors, len(ramp.get("cycle_band_mapping", [])) == 5, "post-boss ramp must cover five non-final cycles")
    error(errors, 0 < number(ramp.get("post_boss_reset_factor", 0)) < 1, "post-boss reset factor must be bounded")
    error(errors, number(ramp.get("siege_duration_seconds", 0)) > 0, "post-boss siege duration must be positive")

    reward_ids = {str(row.get("checkpoint_id")) for row in model.get("rewards", {}).get("checkpoint_rewards", [])}
    error(errors, reward_ids >= {str(row.get("checkpoint_id")) for row in main_schedule + mini_schedule}, "checkpoint rewards do not cover all 30-minute encounters")
    error(errors, number(simulation.get("build_catalog", {}).get("offer_model", {}).get("choice_count", 0)) == 3, "upgrade offer must expose three choices")
    elite_chest = catalog.get("offer_model", {}).get("elite_chest", {})
    elite_windows = elite_chest.get("windows", [])
    error(errors, elite_chest.get("source_kind") == "ELITE_CHEST", "elite offer source kind must be ELITE_CHEST")
    error(errors, int(elite_chest.get("window_count", 0)) == 5 and len(elite_windows) == 5, "ELITE_CHEST must expose five windows")
    error(errors, int(elite_chest.get("choice_count", 0)) == 3, "ELITE_CHEST must expose three choices")
    error(errors, elite_chest.get("wallet_mutation") is False, "ELITE_CHEST must not mutate the wallet")
    error(errors, [int(number(row.get("run_clock_seconds", -1))) for row in elite_windows] == mini_times, "ELITE_CHEST cadence must bind to all five mini-boss times")
    error(errors, {str(row.get("after_checkpoint_id")) for row in elite_windows} == {str(row.get("checkpoint_id")) for row in mini_schedule}, "ELITE_CHEST cadence must bind one-for-one to mini checkpoints")
    error(errors, len({str(row.get("window_id")) for row in elite_windows}) == 5, "ELITE_CHEST windows must have unique IDs")
    error(errors, all(row.get("source_kind") == "ELITE_CHEST" and row.get("one_claim_per_window") is True for row in elite_windows), "ELITE_CHEST window records are incomplete")
    error(errors, model.get("architecture_contract", {}).get("final_boss_policy") == "CHECKPOINT_REWARD_THEN_RUN_VICTORY_NO_BOSS_CHEST", "final boss policy must forbid a boss chest")

    if args.variant_map.exists():
        try:
            variant_map = load_json(args.variant_map)
            mapped_ordinary = {str(row.get("record_id")) for row in variant_map.get("ordinary_roster", {}).get("records", [])}
            mapped_elite = {str(row.get("variant_id")) for row in variant_map.get("elite_variant_catalog", {}).get("records", [])}
            if mapped_ordinary and mapped_ordinary != set(ordinary_ids):
                join_warnings.append("REF-ARCH-02 ordinary roster differs from model")
            if mapped_elite and mapped_elite != registry_variant_ids:
                join_warnings.append("REF-ARCH-02 elite roster differs from model")
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            join_warnings.append(f"variant map could not be read: {exc}")
    else:
        join_warnings.append("REF-ARCH-02 variant map is not available in this checkout")

    if args.architecture.exists():
        try:
            architecture = load_json(args.architecture)
            canonical = architecture.get("canonical", {})
            if int(unwrap(canonical.get("duration_seconds", -1))) != 1800:
                join_warnings.append("live architecture contract still declares a legacy duration")
            if [int(value) for value in canonical.get("boss_checkpoint_seconds", [])] != main_times:
                join_warnings.append("live architecture contract still declares a legacy boss schedule")
            if len(architecture.get("content_registry", {}).get("intermediate_bosses", [])) != 5:
                join_warnings.append("live architecture contract does not yet expose five mini-boss records")
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            join_warnings.append(f"architecture contract could not be read: {exc}")
    else:
        join_warnings.append("architecture contract is not available in this checkout")

    if errors:
        print("BALANCE_MODEL_CHECK=FAIL")
        for item in errors:
            print(f"- {item}")
        return 1

    print("BALANCE_MODEL_CHECK=PASS")
    print(f"model={args.model}")
    print(f"waves={len(waves)} main_bosses={len(main_registry)} mini_bosses={len(mini_registry)} elite_variants={len(elite_registry)}")
    print(f"runtime_claim={model.get('runtime_status', 'NOT_IMPLEMENTED')}")
    if join_warnings:
        print("ARCHITECTURE_JOIN=BLOCKED")
        for item in join_warnings:
            print(f"- {item}")
    else:
        print("ARCHITECTURE_JOIN=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
