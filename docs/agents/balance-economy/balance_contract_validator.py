#!/usr/bin/env python3
"""Validate balance-model IDs against the first-run architecture contract.

This is a contract check, not a Godot runtime test.  It deliberately reads
the balance model and the architecture contract as two different authorities:
the balance model owns numeric tuning, while the architecture contract owns
stable IDs, state shapes, and final-boss policy.
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


def ids(rows: Iterable[Dict[str, Any]]) -> set[str]:
    return {str(row["id"]) for row in rows if "id" in row}


def scalar(value: Any) -> Any:
    if isinstance(value, dict) and "value" in value:
        return value["value"]
    return value


def record_error(errors: List[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def final_boss_policy(contract: Dict[str, Any]) -> Any:
    if "final_boss_policy" in contract:
        return contract["final_boss_policy"]
    canonical = contract.get("canonical")
    if isinstance(canonical, dict):
        if "final_boss_policy" in canonical:
            return canonical["final_boss_policy"]
        outcome_policy = canonical.get("checkpoint_outcome_policy")
        if isinstance(outcome_policy, dict):
            return outcome_policy.get("final_boss")
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    here = Path(__file__).resolve().parent
    parser.add_argument("--model", type=Path, default=here / "BALANCE_MODEL.json")
    parser.add_argument(
        "--architecture",
        type=Path,
        default=here / "../../architecture/first-run/FIRST_RUN_DATA_CONTRACT.json",
    )
    args = parser.parse_args()

    try:
        model = load_json(args.model)
        architecture = load_json(args.architecture.resolve())
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BALANCE_CONTRACT_CHECK=ERROR: {exc}", file=sys.stderr)
        return 2

    errors: List[str] = []
    registry = architecture.get("content_registry", {})
    simulation = model.get("simulation_model", {})
    integration = model.get("runtime_integration", {})
    join_policy = integration.get("join_policy", {})
    clock_policy = simulation.get("boss_clock_policy", {})
    mini_clock_policy = simulation.get("mini_boss_clock_policy", {})
    wave_ramp = simulation.get("boss_wave_ramp", {})
    schedule = simulation.get("run_schedule", {})
    schedule_main = schedule.get("main_boss_checkpoints", [])
    schedule_mini = schedule.get("mini_boss_checkpoints", [])

    record_error(errors, model.get("status") == "PARTIAL", "model status must remain PARTIAL")
    record_error(
        errors,
        simulation.get("status") == "PROPOSED_MODEL_ONLY",
        "simulation_model must remain explicitly model-only",
    )
    record_error(
        errors,
        clock_policy.get("status") == "CANON",
        "boss clock policy must be explicit CANON product behavior",
    )
    record_error(
        errors,
        clock_policy.get("applies_to") == "MAIN_BOSS_CHECKPOINTS",
        "main-boss clock policy must apply to all main checkpoints",
    )
    record_error(
        errors,
        clock_policy.get("checkpoint_seconds") == [int(row["time_seconds"]) for row in schedule_main],
        "main-boss clock policy must bind to every 30-minute main checkpoint",
    )
    record_error(
        errors,
        clock_policy.get("run_clock_stops_at_boss_checkpoint") is True
        and clock_policy.get("wave_xp_spawn_clock_advances_during_encounter") is False,
        "boss clock policy must freeze the run/wave/XP/spawn clock",
    )
    record_error(
        errors,
        mini_clock_policy.get("applies_to") == "MINI_BOSS_CHECKPOINTS"
        and mini_clock_policy.get("run_clock_stops_at_checkpoint") is False
        and mini_clock_policy.get("wave_xp_spawn_clock_advances_during_encounter") is True
        and mini_clock_policy.get("checkpoint_seconds") == [int(row["time_seconds"]) for row in schedule_mini],
        "mini-boss clock policy must advance the visible/wave/XP clock at all five mini checkpoints",
    )
    record_error(
        errors,
        wave_ramp.get("status") == "PROPOSED"
        and wave_ramp.get("applies_to") == "POST_BOSS_CYCLES_BEFORE_EVERY_NEXT_BOSS"
        and wave_ramp.get("ramp_curve", {}).get("value") == "LINEAR",
        "post-boss wave ramp must be explicit PROPOSED linear recovery/ramp/siege behavior",
    )
    record_error(
        errors,
        integration.get("status") == "NOT_IMPLEMENTED",
        "runtime_integration must not claim runtime implementation",
    )
    record_error(
        errors,
        join_policy.get("no_duplicate_tuning_values") is True,
        "integration policy must forbid duplicated tuning values",
    )
    record_error(
        errors,
        model.get("architecture_contract", {}).get("source_revision")
        == integration.get("architecture_contract_revision"),
        "model and runtime handoff must name the same architecture revision",
    )
    record_error(
        errors,
        int(scalar(architecture.get("canonical", {}).get("duration_seconds", -1))) == int(scalar(schedule.get("duration_seconds", -2))),
        "balance schedule duration must match the live architecture duration",
    )
    record_error(
        errors,
        [int(row.get("time_seconds")) for row in schedule_main]
        == [int(value) for value in architecture.get("canonical", {}).get("boss_checkpoint_seconds", [])],
        "main-boss schedule must use the live architecture checkpoint seconds",
    )

    character_ids = ids(registry.get("characters", []))
    weapon_ids = ids(registry.get("weapons", []))
    passive_ids = ids(registry.get("passives", []))
    synergy_ids = ids(registry.get("synergies", []))
    enemy_ids = ids(registry.get("enemies", []))
    boss_rows = registry.get("bosses", [])
    boss_ids = ids(boss_rows)
    boss_by_checkpoint = {
        int(row["checkpoint_seconds"]): str(row["id"])
        for row in boss_rows
        if "checkpoint_seconds" in row and "id" in row
    }
    canonical = architecture.get("canonical", {})
    architecture_intermediate_rows = registry.get("intermediate_bosses", [])
    architecture_intermediate_by_checkpoint = {
        int(row["checkpoint_seconds"]): str(row["id"])
        for row in architecture_intermediate_rows
        if "checkpoint_seconds" in row and "id" in row
    }
    architecture_variant_ids = {
        str(row["variant_id"])
        for row in canonical.get("enemy_variant_policy", {}).get("variant_ids", [])
        if isinstance(row, dict) and "variant_id" in row
    }
    if not architecture_variant_ids:
        architecture_variant_ids = {
            str(value)
            for value in canonical.get("enemy_variant_policy", {}).get("variant_ids", [])
            if isinstance(value, str)
        }

    heroes = simulation.get("heroes_and_profiles", {}).get("heroes", {})
    build = simulation.get("build_catalog", {})
    weapons = build.get("weapons", {})
    passives = build.get("passives", {})
    synergies = build.get("synergies", {})

    for hero_id, hero in heroes.items():
        record_error(errors, hero_id in character_ids, f"unknown architecture hero ID: {hero_id}")
        weapon_id = hero.get("starting_weapon_id")
        passive_id = hero.get("starting_passive_id")
        record_error(errors, weapon_id in weapon_ids, f"unknown architecture weapon ID: {weapon_id}")
        record_error(errors, passive_id in passive_ids, f"unknown architecture passive ID: {passive_id}")
        if weapon_id in weapons:
            synergy_id = weapons[weapon_id].get("synergy_id")
            record_error(errors, synergy_id in synergy_ids, f"unknown architecture synergy ID: {synergy_id}")
            if synergy_id in synergies:
                record_error(
                    errors,
                    synergies[synergy_id].get("weapon_id") == weapon_id,
                    f"synergy {synergy_id} does not point back to weapon {weapon_id}",
                )

    for enemy_id in model.get("enemy_archetypes", []):
        record_error(errors, enemy_id.get("enemy_id") in enemy_ids, f"unknown architecture enemy ID: {enemy_id.get('enemy_id')}")

    model_checkpoints = {
        int(row["time_seconds"]): row
        for row in model.get("boss_checkpoints", [])
        if "time_seconds" in row
    }
    model_stats = simulation.get("boss_stats", {})
    checkpoint_time_by_id = {
        str(row["checkpoint_id"]): int(row["time_seconds"])
        for row in model.get("boss_checkpoints", [])
        if "checkpoint_id" in row and "time_seconds" in row
    }
    declared_mapping = {
        checkpoint_time_by_id.get(str(row.get("checkpoint_id")), -1): row.get("boss_id")
        for row in join_policy.get("checkpoint_boss_mapping", [])
    }
    for checkpoint_seconds, expected_boss_id in boss_by_checkpoint.items():
        checkpoint = model_checkpoints.get(checkpoint_seconds, {})
        checkpoint_id = checkpoint.get("checkpoint_id")
        record_error(errors, checkpoint.get("boss_id") == expected_boss_id, f"checkpoint {checkpoint_seconds} has wrong boss ID")
        stats = model_stats.get(checkpoint_id, {})
        record_error(errors, stats.get("boss_id") == expected_boss_id, f"stats {checkpoint_id} has wrong boss ID")
        record_error(errors, stats.get("boss_id") in boss_ids, f"stats {checkpoint_id} uses unknown boss ID")
        record_error(errors, declared_mapping.get(checkpoint_seconds) == expected_boss_id, f"handoff mapping {checkpoint_seconds} is stale")

    schedule_main_ids = {str(row.get("checkpoint_id")) for row in schedule_main}
    record_error(errors, len(schedule_main) == 6, "30-minute extension must expose six main-boss checkpoints")
    record_error(errors, len(schedule_mini) == 5, "30-minute extension must expose five mini-boss checkpoints")
    for row in schedule_main:
        checkpoint_id = str(row.get("checkpoint_id"))
        stats = model_stats.get(checkpoint_id, {})
        record_error(errors, stats.get("boss_id") == row.get("boss_id"), f"30m stats {checkpoint_id} has wrong boss ID")
        if row.get("id_status") == "CANON_ARCHITECTURE":
            record_error(errors, row.get("boss_id") in boss_ids, f"30m canonical boss {checkpoint_id} is not in architecture registry")
        else:
            record_error(errors, stats.get("boss_id_status") == "PENDING_CONTENT_REGISTRY" or row.get("id_status") != "CANON_ARCHITECTURE", f"30m extension boss {checkpoint_id} must remain pending")
    mini_stats = simulation.get("mini_boss_stats", {})
    for row in schedule_mini:
        record_error(errors, str(row.get("boss_id")) in mini_stats, f"mini-boss stats missing for {row.get('boss_id')}")
    for checkpoint_seconds, expected_mini_id in architecture_intermediate_by_checkpoint.items():
        model_mini = next((row for row in schedule_mini if int(row.get("time_seconds", -1)) == checkpoint_seconds), {})
        record_error(
            errors,
            model_mini.get("boss_id") == expected_mini_id,
            f"architecture intermediate slot {checkpoint_seconds} is not represented by the balance schedule",
        )
    for row in schedule_mini:
        checkpoint_seconds = int(row.get("time_seconds", -1))
        if checkpoint_seconds not in architecture_intermediate_by_checkpoint:
            record_error(
                errors,
                row.get("id_status") == "PENDING_CONTENT_REGISTRY",
                f"proposed extra mini-boss at {checkpoint_seconds} must remain pending",
            )
    record_error(errors, simulation.get("elite_variation_policy", {}).get("persistent") is False, "elite variants must not be persistent wave members")
    model_variant_ids = set(simulation.get("elite_variation_policy", {}).get("variant_ids", {}).get("value", []))
    record_error(errors, model_variant_ids == architecture_variant_ids, "elite variation IDs must match the architecture registry")

    model_waves = model.get("wave_bands", [])
    model_wave_ids = {str(row.get("wave_band_id")) for row in model_waves}
    declared_wave_ids = {
        str(row.get("wave_band_id"))
        for row in join_policy.get("wave_band_mapping", [])
    }
    architecture_wave_rows = registry.get("wave_bands", [])
    legacy_wave_by_range = {
        (int(row["from_seconds"]), int(row["to_seconds"])): str(row["id"])
        for row in architecture_wave_rows
        if "from_seconds" in row and "to_seconds" in row
    }
    if legacy_wave_by_range:
        for wave in model_waves:
            key = (int(wave["start_seconds"]), int(wave["end_seconds"]))
            expected_id = legacy_wave_by_range.get(key)
            if expected_id is not None:
                record_error(errors, wave.get("wave_band_id") == expected_id, f"wave range {key} has wrong stable ID")
            else:
                record_error(errors, str(wave.get("wave_band_id")) in model_wave_ids - set(legacy_wave_by_range.values()), f"unregistered extension wave {wave.get('wave_band_id')}")
        architecture_wave_ids = set(legacy_wave_by_range.values())
        record_error(errors, architecture_wave_ids.issubset(model_wave_ids), "model wave IDs do not cover architecture wave IDs")
        record_error(errors, architecture_wave_ids.issubset(declared_wave_ids), "handoff wave mapping is incomplete for architecture waves")
        for extension_id in model_wave_ids - architecture_wave_ids:
            record_error(
                errors,
                any(row.get("wave_band_id") == extension_id and row.get("status") == "PROPOSED_EXTENSION" for row in join_policy.get("wave_band_mapping", [])),
                f"extension wave {extension_id} must remain explicitly PROPOSED_EXTENSION",
            )
    else:
        architecture_wave_ids = ids(architecture_wave_rows)
        architecture_wave_mapping = join_policy.get("architecture_wave_cycle_mapping", [])
        mapped_architecture_wave_ids = {str(row.get("architecture_wave_band_id")) for row in architecture_wave_mapping}
        mapped_model_wave_ids = {str(row.get("model_wave_band_id")) for row in architecture_wave_mapping}
        record_error(errors, architecture_wave_ids.issubset(mapped_architecture_wave_ids), "architecture wave-cycle handoff is incomplete")
        record_error(errors, model_wave_ids.issubset(mapped_model_wave_ids), "every model wave band needs an architecture cycle alias")
        record_error(errors, mapped_model_wave_ids.issubset(model_wave_ids), "wave-cycle handoff references an unknown model wave band")

    ramp_cycles = wave_ramp.get("cycle_band_mapping", [])
    checkpoint_ids = [str(row.get("checkpoint_id")) for row in schedule_main]
    checkpoint_times = {
        str(row.get("checkpoint_id")): int(row.get("time_seconds"))
        for row in schedule_main
    }
    record_error(
        errors,
        len(ramp_cycles) == max(0, len(checkpoint_ids) - 1),
        "post-boss wave ramp must cover every non-final boss interval",
    )
    for index, cycle in enumerate(ramp_cycles):
        from_id = str(cycle.get("from_checkpoint_id"))
        to_id = str(cycle.get("to_checkpoint_id"))
        entry_id = str(cycle.get("entry_band_id"))
        peak_id = str(cycle.get("peak_band_id"))
        record_error(errors, index + 1 < len(checkpoint_ids) and from_id == checkpoint_ids[index], f"wave ramp cycle {index} has wrong source checkpoint")
        record_error(errors, index + 2 <= len(checkpoint_ids) and to_id == checkpoint_ids[index + 1], f"wave ramp cycle {index} has wrong target checkpoint")
        record_error(errors, from_id in checkpoint_times and to_id in checkpoint_times and checkpoint_times[to_id] > checkpoint_times[from_id], f"wave ramp cycle {index} has invalid checkpoint order")
        record_error(errors, entry_id in model_wave_ids, f"wave ramp cycle {index} uses unknown entry wave ID")
        record_error(errors, peak_id in model_wave_ids, f"wave ramp cycle {index} uses unknown peak wave ID")
    suppression = simulation.get("boss_interruption", {}).get("suppression_seconds", 0)
    recovery = simulation.get("boss_interruption", {}).get("recovery_duration_seconds", 0)
    siege = wave_ramp.get("siege_duration_seconds", 0)
    try:
        suppression_value = float(suppression.get("value", suppression))
        recovery_value = float(recovery.get("value", recovery))
        siege_value = float(siege.get("value", siege))
        reset_value = float(wave_ramp.get("post_boss_reset_factor", {}).get("value", 0))
    except (TypeError, ValueError):
        suppression_value = recovery_value = siege_value = -1
        reset_value = 0
    record_error(errors, siege_value > 0, "wave ramp siege duration must be positive")
    record_error(errors, 0 < reset_value < 1, "wave ramp reset factor must be between zero and one")
    for from_id, to_id in zip(checkpoint_ids[:-1], checkpoint_ids[1:]):
        record_error(
            errors,
            checkpoint_times[to_id] - checkpoint_times[from_id] > suppression_value + recovery_value + siege_value,
            f"wave ramp leaves no positive linear-ramp window between {from_id} and {to_id}",
        )

    record_error(
        errors,
        model.get("architecture_contract", {}).get("final_boss_policy") == final_boss_policy(architecture),
        "legacy final-boss policy differs between balance and architecture contracts",
    )

    if errors:
        print("BALANCE_CONTRACT_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("BALANCE_CONTRACT_CHECK=PASS")
    print(f"model={args.model}")
    print(f"architecture={args.architecture.resolve()}")
    print(f"boss_ids={len(boss_ids)} wave_ids={len(model_wave_ids)}")
    print("runtime_claim=NOT_IMPLEMENTED")
    print("extension_status=BLOCKED_PENDING_ARCHITECTURE_AND_CONTENT_REGISTRY_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

