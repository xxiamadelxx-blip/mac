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
        clock_policy.get("applies_to") == "ALL_BOSS_CHECKPOINTS",
        "boss clock policy must apply to all boss checkpoints",
    )
    record_error(
        errors,
        clock_policy.get("checkpoint_seconds") == [300, 600, 900, 1200],
        "boss clock policy must bind to 5/10/15/20 minute checkpoints",
    )
    record_error(
        errors,
        clock_policy.get("run_clock_stops_at_boss_checkpoint") is True
        and clock_policy.get("wave_xp_spawn_clock_advances_during_encounter") is False,
        "boss clock policy must freeze the run/wave/XP/spawn clock",
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

    wave_by_range = {
        (int(row["from_seconds"]), int(row["to_seconds"])): str(row["id"])
        for row in registry.get("wave_bands", [])
    }
    model_waves = model.get("wave_bands", [])
    model_wave_ids = {str(row.get("wave_band_id")) for row in model_waves}
    declared_wave_ids = {
        str(row.get("wave_band_id"))
        for row in join_policy.get("wave_band_mapping", [])
    }
    for wave in model_waves:
        key = (int(wave["start_seconds"]), int(wave["end_seconds"]))
        expected_id = wave_by_range.get(key)
        record_error(errors, wave.get("wave_band_id") == expected_id, f"wave range {key} has wrong stable ID")
    record_error(errors, model_wave_ids == set(wave_by_range.values()), "model wave IDs do not cover architecture wave IDs")
    record_error(errors, declared_wave_ids == set(wave_by_range.values()), "handoff wave mapping is incomplete")

    record_error(
        errors,
        model.get("architecture_contract", {}).get("final_boss_policy") == final_boss_policy(architecture),
        "final-boss policy differs between balance and architecture contracts",
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
