#!/usr/bin/env python3
"""Data-driven deterministic 30-minute balance model.

The program reads every tuning input from BALANCE_MODEL.json.  It models the
wave clock, cap pressure, XP progression, proposed combat math, incoming risk,
checkpoint bosses, reward settlement, idempotency, boss-chest outcomes, artifact offers, and build offers.  It is a
model-only result: it does not execute the Godot runtime and cannot establish
runtime FPS, collision, telegraph, or player-behavior evidence.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


def unwrap(value: Any) -> Any:
    if isinstance(value, dict) and "value" in value:
        return value["value"]
    return value


def number(value: Any) -> float:
    return float(unwrap(value))


def integer(value: Any) -> int:
    return int(round(number(value)))


def require_status(value: Any, allowed: Iterable[str], label: str) -> None:
    if not isinstance(value, dict):
        return
    status = value.get("status")
    if status is not None and status not in set(allowed):
        raise ValueError(f"{label} has unsupported status {status!r}")


def load_model(path: Path) -> Dict[str, Any]:
    model = json.loads(path.read_text(encoding="utf-8"))
    simulation = model["simulation_model"]
    if simulation["status"] != "PROPOSED_MODEL_ONLY":
        raise ValueError("simulation_model must explicitly be PROPOSED_MODEL_ONLY")
    for key in (
        "main_run_duration_seconds",
        "simulation_step_seconds",
        "boss_clock_policy",
        "mini_boss_clock_policy",
        "boss_wave_ramp",
        "run_schedule",
        "mini_boss_stats",
        "elite_variation_policy",
        "default_seed_set",
    ):
        if key not in simulation:
            raise ValueError(f"simulation_model missing {key}")
    clock_policy = simulation["boss_clock_policy"]
    schedule = simulation["run_schedule"]
    main_checkpoints = schedule["main_boss_checkpoints"]
    mini_checkpoints = schedule["mini_boss_checkpoints"]
    main_registry = model.get("main_bosses", [])
    mini_registry = model.get("mini_bosses", [])
    elite_registry = model.get("elite_variants", [])
    if len(main_registry) != len(main_checkpoints) or len(main_registry) != 6:
        raise ValueError("top-level main_bosses must expose the six scheduled main checkpoints")
    if len(mini_registry) != len(mini_checkpoints) or len(mini_registry) != 5:
        raise ValueError("top-level mini_bosses must expose the five scheduled mini checkpoints")
    if len(elite_registry) != 10:
        raise ValueError("top-level elite_variants must expose the ten mapped variant records")
    scheduled_main = {
        str(row["checkpoint_id"]): row for row in main_checkpoints
    }
    for record in main_registry:
        checkpoint_id = str(record.get("checkpoint_id", ""))
        scheduled = scheduled_main.get(checkpoint_id)
        if scheduled is None or record.get("boss_id") != scheduled.get("boss_id") or int(record.get("time_seconds", -1)) != int(scheduled.get("time_seconds", -2)):
            raise ValueError(f"main_bosses registry diverges from run_schedule at {checkpoint_id}")
        if not str(record.get("stats_ref", "")):
            raise ValueError(f"main_bosses registry has no stats_ref at {checkpoint_id}")
    scheduled_mini = {
        str(row["checkpoint_id"]): row for row in mini_checkpoints
    }
    for record in mini_registry:
        checkpoint_id = str(record.get("checkpoint_id", ""))
        scheduled = scheduled_mini.get(checkpoint_id)
        if scheduled is None or record.get("boss_id") != scheduled.get("boss_id") or int(record.get("time_seconds", -1)) != int(scheduled.get("time_seconds", -2)):
            raise ValueError(f"mini_bosses registry diverges from run_schedule at {checkpoint_id}")
        if not str(record.get("stats_ref", "")):
            raise ValueError(f"mini_bosses registry has no stats_ref at {checkpoint_id}")
    elite_registry_ids = {str(record.get("variant_id", "")) for record in elite_registry}
    if "" in elite_registry_ids or len(elite_registry_ids) != 10:
        raise ValueError("elite_variants registry must expose ten unique variant IDs")
    selected_variant_ids = set(unwrap(simulation["elite_variation_policy"].get("variant_ids", [])))
    if not selected_variant_ids.issubset(elite_registry_ids):
        raise ValueError("selected elite variants must be a bounded subset of the registry")
    if clock_policy.get("applies_to") != "MAIN_BOSS_CHECKPOINTS":
        raise ValueError("main boss clock policy must apply to main checkpoints")
    if clock_policy.get("checkpoint_seconds") != [int(number(row["time_seconds"])) for row in main_checkpoints]:
        raise ValueError("main boss clock policy must bind to every 30-minute main checkpoint")
    if clock_policy.get("run_clock_stops_at_boss_checkpoint") is not True:
        raise ValueError("boss clock policy must stop the main run clock at every boss")
    if clock_policy.get("wave_xp_spawn_clock_advances_during_encounter") is not False:
        raise ValueError("wave/XP/spawn clock must remain frozen during every boss encounter")
    ramp = simulation["boss_wave_ramp"]
    if ramp.get("applies_to") != "POST_BOSS_CYCLES_BEFORE_EVERY_NEXT_BOSS":
        raise ValueError("boss wave ramp must apply to every post-boss cycle")
    if number(ramp["siege_duration_seconds"]) <= 0:
        raise ValueError("boss wave ramp siege duration must be positive")
    if not 0 < number(ramp["post_boss_reset_factor"]) < 1:
        raise ValueError("post-boss reset factor must be between zero and one")
    if ramp.get("ramp_curve", {}).get("value") != "LINEAR":
        raise ValueError("boss wave ramp must use the declared linear curve")
    if len(ramp.get("cycle_band_mapping", [])) != len(main_checkpoints) - 1:
        raise ValueError("boss wave ramp must cover every non-final boss cycle")
    mini_policy = simulation["mini_boss_clock_policy"]
    if mini_policy.get("applies_to") != "MINI_BOSS_CHECKPOINTS":
        raise ValueError("mini-boss clock policy must apply to mini-boss checkpoints")
    if mini_policy.get("run_clock_stops_at_checkpoint") is not False:
        raise ValueError("mini-boss encounters must not stop the visible run clock")
    if mini_policy.get("wave_xp_spawn_clock_advances_during_encounter") is not True:
        raise ValueError("waves, XP, and spawning must continue during mini-boss encounters")
    if mini_policy.get("checkpoint_seconds") != [int(number(row["time_seconds"])) for row in mini_checkpoints]:
        raise ValueError("mini-boss clock policy must bind to every mini-boss checkpoint")
    if len({int(number(row["time_seconds"])) for row in main_checkpoints + mini_checkpoints}) != len(main_checkpoints) + len(mini_checkpoints):
        raise ValueError("main and mini-boss checkpoints may not overlap")
    if number(simulation["main_run_duration_seconds"]) != number(schedule["duration_seconds"]):
        raise ValueError("schedule duration must match main run duration")
    if model["architecture_contract"]["final_boss_policy"] != "CHECKPOINT_REWARD_THEN_RUN_VICTORY_NO_BOSS_CHEST":
        raise ValueError("final-boss chest policy drifted from the live architecture contract")
    variant_ids = unwrap(simulation["elite_variation_policy"].get("variant_ids", []))
    if not variant_ids or len(set(variant_ids)) != len(variant_ids):
        raise ValueError("elite variation policy must expose unique stable variant IDs")
    roster = simulation.get("content_roster", {})
    ordinary_ids = unwrap(roster.get("ordinary_enemy_ids", []))
    if len(ordinary_ids) != 10 or len(set(ordinary_ids)) != 10:
        raise ValueError("content roster must expose ten unique ordinary enemy IDs")
    enemy_stats = simulation.get("enemy_stats", {})
    missing_ordinary = [enemy_id for enemy_id in ordinary_ids if enemy_id not in enemy_stats]
    if missing_ordinary:
        raise ValueError(f"content roster has no numeric enemy stats: {missing_ordinary}")
    proposed_variants = unwrap(roster.get("elite_variant_ids", []))
    records = simulation["elite_variation_policy"].get("variant_overrides", {}).get("records", {})
    if len(proposed_variants) != 10 or any(variant_id not in records for variant_id in proposed_variants):
        raise ValueError("content roster must expose numeric records for all ten elite variants")
    if len(variant_ids) > integer(roster.get("registered_variant_cap", 5)):
        raise ValueError("model variant selection exceeds the registered variant cap")
    progression = simulation["build_catalog"].get("synergy_progression")
    if not progression:
        raise ValueError("build_catalog must expose the data-driven synergy progression contract")
    target_policy = simulation["target_policy"]
    if integer(target_policy.get("target_final_level", 0)) < 40:
        raise ValueError("30-minute XP target must be at least level 40")
    if integer(target_policy.get("minimum_synergy_claims", 0)) < 3:
        raise ValueError("30-minute target must require at least three synergy claims")
    hero_ids = simulation["heroes_and_profiles"]["heroes"].keys()
    pair_orders = progression.get("pair_order_by_hero", {})
    for hero_id in hero_ids:
        path = unwrap(pair_orders.get(hero_id, []))
        if len(path) < integer(progression["minimum_pairs_for_target"]):
            raise ValueError(f"{hero_id} synergy path is too short for the target")
        missing_pairs = [synergy_id for synergy_id in path if synergy_id not in simulation["build_catalog"]["synergies"]]
        if missing_pairs:
            raise ValueError(f"{hero_id} synergy path references unknown pairs: {missing_pairs}")
    return model


def round_half_up(value: float) -> int:
    return int(math.floor(value + 0.5))


def xp_thresholds(model: Dict[str, Any], max_level: int = 64) -> List[int]:
    params = model["simulation_model"]["xp_formula_parameters"]
    base = number(params["base_xp"])
    linear = number(params["linear_per_level"])
    coefficient = number(params["power_coefficient"])
    exponent = number(params["power_exponent"])
    cumulative: List[int] = []
    total = 0
    for level in range(1, max_level + 1):
        next_xp = round_half_up(base + linear * (level - 1) + coefficient * ((level - 1) ** exponent))
        total += next_xp
        cumulative.append(total)
    return cumulative


def level_from_xp(total_xp: float, thresholds: List[int]) -> int:
    level = 1
    for cumulative in thresholds:
        if total_xp >= cumulative:
            level += 1
        else:
            break
    return level


def profile_value(profile: Dict[str, Any], key: str) -> Any:
    return unwrap(profile[key])


def synergy_path_for_hero(model: Dict[str, Any], hero_id: str) -> List[str]:
    progression = model["simulation_model"]["build_catalog"]["synergy_progression"]
    path = unwrap(progression["pair_order_by_hero"][hero_id])
    if not isinstance(path, list) or len(path) < 3:
        raise ValueError(f"synergy path for {hero_id} must expose at least three distinct pairs")
    if len(path) != len(set(path)):
        raise ValueError(f"synergy path for {hero_id} contains duplicate pairs")
    return [str(synergy_id) for synergy_id in path]


def run_schedule(model: Dict[str, Any]) -> Dict[str, Any]:
    return model["simulation_model"]["run_schedule"]


def main_checkpoints(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(run_schedule(model)["main_boss_checkpoints"])


def mini_checkpoints(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(run_schedule(model)["mini_boss_checkpoints"])


def all_encounter_checkpoints(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    return sorted(main_checkpoints(model) + mini_checkpoints(model), key=lambda row: number(row["time_seconds"]))


def progression_checkpoint_seconds(model: Dict[str, Any]) -> List[float]:
    """Read level-report checkpoints from the model target table."""
    target_table = model["simulation_model"]["target_policy"].get("xp_level_targets", {})
    return sorted(float(key) for key in target_table)


def late_main_boss_start_seconds(model: Dict[str, Any]) -> float:
    """Read the late-main classification boundary from model data."""
    boundary = model["simulation_model"]["target_policy"].get("late_main_boss_start_seconds")
    if boundary is None:
        raise ValueError("target_policy is missing late_main_boss_start_seconds")
    return number(boundary)


def checkpoint_is_final(model: Dict[str, Any], checkpoint_id: str) -> bool:
    for row in main_checkpoints(model):
        if str(row["checkpoint_id"]) == checkpoint_id:
            return bool(row.get("is_final", False))
    return False


def checkpoint_kind(model: Dict[str, Any], checkpoint_id: str) -> str:
    for row in all_encounter_checkpoints(model):
        if str(row["checkpoint_id"]) == checkpoint_id:
            return str(row.get("encounter_kind", "MAIN_BOSS"))
    raise KeyError(f"unknown checkpoint: {checkpoint_id}")


def wave_at(model: Dict[str, Any], elapsed: float) -> Dict[str, Any]:
    bands = model["wave_bands"]
    for band in bands:
        start = number(band["start_seconds"])
        end = number(band["end_seconds"])
        if start <= elapsed < end:
            return band
    return bands[-1]


def _lerp(start: float, end: float, fraction: float) -> float:
    fraction = max(0.0, min(1.0, fraction))
    return start + (end - start) * fraction


def _band_map(model: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {str(band["wave_band_id"]): band for band in model["wave_bands"]}


def _checkpoint_time_map(model: Dict[str, Any]) -> Dict[str, float]:
    return {str(row["checkpoint_id"]): number(row["time_seconds"]) for row in main_checkpoints(model)}


def _blend_composition_weights(
    model: Dict[str, Any], entry_band_id: str, peak_band_id: str, fraction: float
) -> Dict[str, float]:
    weights = model["simulation_model"]["wave_selection"]["composition_weights"]
    entry = weights[entry_band_id]
    peak = weights[peak_band_id]
    keys = sorted(set(entry) | set(peak))
    blended = {
        enemy_id: _lerp(number(entry.get(enemy_id, 0.0)), number(peak.get(enemy_id, 0.0)), fraction)
        for enemy_id in keys
    }
    total = sum(blended.values())
    if total <= 0.0:
        raise ValueError("blended composition weights must have positive sum")
    return {enemy_id: value / total for enemy_id, value in blended.items()}


def wave_state_at(model: Dict[str, Any], elapsed: float) -> Dict[str, Any]:
    """Return the canonical band or the post-boss recovery/ramp/siege state.

    Canonical B1 bands remain the authority for the first five minutes.  After
    each non-final boss, the next band starts below the preceding peak, ramps
    linearly to its own peak, and holds that peak for the configured siege
    window.  The separate boss-interruption factor is applied by the caller so
    the 8-second suppression and 20-second recovery remain visible.
    """
    base = wave_at(model, elapsed)
    ramp = model["simulation_model"].get("boss_wave_ramp")
    if not ramp:
        return base
    band_by_id = _band_map(model)
    checkpoint_times = _checkpoint_time_map(model)
    reset_factor = number(ramp["post_boss_reset_factor"])
    siege_duration = number(ramp["siege_duration_seconds"])
    interruption = model["simulation_model"]["boss_interruption"]
    recovery_gate = number(interruption["suppression_seconds"]) + number(interruption["recovery_duration_seconds"])
    for cycle in ramp["cycle_band_mapping"]:
        cycle_start = checkpoint_times[str(cycle["from_checkpoint_id"])]
        cycle_end = checkpoint_times[str(cycle["to_checkpoint_id"])]
        if not (cycle_start <= elapsed < cycle_end):
            continue
        entry = band_by_id[str(cycle["entry_band_id"])]
        peak = band_by_id[str(cycle["peak_band_id"])]
        cycle_duration = cycle_end - cycle_start
        ramp_duration = max(0.0, cycle_duration - recovery_gate - siege_duration)
        since_start = max(0.0, elapsed - cycle_start)
        ramp_elapsed = max(0.0, since_start - recovery_gate)
        fraction = 1.0 if ramp_duration <= 0.0 else min(1.0, ramp_elapsed / ramp_duration)
        entry_budget = number(entry["spawn_budget_per_second"]) * reset_factor
        peak_budget = number(peak["spawn_budget_per_second"])
        entry_cap = number(entry["active_cap"]) * reset_factor
        peak_cap = number(peak["active_cap"])
        state = dict(peak)
        state["spawn_budget_per_second"] = _lerp(entry_budget, peak_budget, fraction)
        state["active_cap"] = max(1, round_half_up(_lerp(entry_cap, peak_cap, fraction)))
        state["composition_weights"] = _blend_composition_weights(
            model, str(entry["wave_band_id"]), str(peak["wave_band_id"]), fraction
        )
        state["ramp_cycle_id"] = cycle["cycle_id"]
        state["ramp_phase"] = (
            "POST_BOSS_RECOVERY"
            if since_start < recovery_gate
            else "SIEGE"
            if since_start >= recovery_gate + ramp_duration
            else "RAMP"
        )
        state["ramp_fraction"] = fraction
        state["entry_band_id"] = entry["wave_band_id"]
        state["peak_band_id"] = peak["wave_band_id"]
        state["cycle_start_seconds"] = cycle_start
        state["cycle_end_seconds"] = cycle_end
        state["ramp_end_seconds"] = cycle_start + recovery_gate + ramp_duration
        state["density_start_budget_per_second"] = entry_budget
        state["density_peak_budget_per_second"] = peak_budget
        state["density_start_active_cap"] = round_half_up(entry_cap)
        state["density_peak_active_cap"] = round_half_up(peak_cap)
        state["density_factor_of_peak"] = state["spawn_budget_per_second"] / peak_budget if peak_budget else 0.0
        return state
    return base


def wave_ramp_samples(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Expose auditable phase checkpoints for independent balance checks."""
    ramp = model["simulation_model"].get("boss_wave_ramp")
    if not ramp:
        return []
    checkpoint_times = _checkpoint_time_map(model)
    suppression = number(model["simulation_model"]["boss_interruption"]["suppression_seconds"])
    recovery = number(model["simulation_model"]["boss_interruption"]["recovery_duration_seconds"])
    siege = number(ramp["siege_duration_seconds"])
    samples: List[Dict[str, Any]] = []
    for cycle in ramp["cycle_band_mapping"]:
        start = checkpoint_times[str(cycle["from_checkpoint_id"])]
        end = checkpoint_times[str(cycle["to_checkpoint_id"])]
        ramp_end = end - siege
        for label, elapsed in (
            ("post_boss_start", start),
            ("suppression_end", start + suppression),
            ("recovery_end", start + suppression + recovery),
            ("ramp_peak", ramp_end),
            ("siege_before_boss", max(ramp_end, end - number(model["simulation_model"]["simulation_step_seconds"]))),
        ):
            state = wave_state_at(model, elapsed)
            interruption_factor = boss_interruption_factor(model, elapsed)
            samples.append({
                "cycle_id": cycle["cycle_id"],
                "sample": label,
                "run_clock_seconds": round(elapsed, 3),
                "phase": state.get("ramp_phase", "CANONICAL"),
                "density_factor_of_peak": round(float(state.get("density_factor_of_peak", 1.0)), 6),
                "density_budget_per_second": round(number(state["spawn_budget_per_second"]), 6),
                "effective_budget_per_second_after_interruption": round(number(state["spawn_budget_per_second"]) * interruption_factor, 6),
                "active_cap": integer(state["active_cap"]),
                "boss_interruption_factor": round(interruption_factor, 6),
            })
    return samples


def weighted_choice(rng: random.Random, weights: Dict[str, Any]) -> str:
    pairs = [(key, number(value)) for key, value in sorted(weights.items())]
    total = sum(weight for _, weight in pairs)
    if total <= 0:
        raise ValueError("composition weights must have positive sum")
    pick = rng.random() * total
    cursor = 0.0
    for key, weight in pairs:
        cursor += weight
        if pick < cursor:
            return key
    return pairs[-1][0]


def stat_map(model: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {row["enemy_id"]: row for row in model["enemy_archetypes"]}


def boss_reward_map(model: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {row["checkpoint_id"]: row for row in model["rewards"]["checkpoint_rewards"]}


def boss_interruption_factor(model: Dict[str, Any], elapsed: float) -> float:
    interruption = model["simulation_model"]["boss_interruption"]
    suppression = number(interruption["suppression_seconds"])
    recovery = number(interruption["recovery_duration_seconds"])
    suppression_factor = number(interruption["suppression_factor"])
    start_factor = number(interruption["recovery_start_factor"])
    end_factor = number(interruption["recovery_end_factor"])
    latest_checkpoint = None
    for checkpoint in main_checkpoints(model):
        checkpoint_time = number(checkpoint["time_seconds"])
        if checkpoint_time <= elapsed:
            latest_checkpoint = checkpoint_time
    if latest_checkpoint is None:
        return 1.0
    since_boss = elapsed - latest_checkpoint
    if since_boss < suppression:
        return suppression_factor
    recovery_elapsed = since_boss - suppression
    if recovery_elapsed < recovery:
        fraction = recovery_elapsed / recovery
        return start_factor + (end_factor - start_factor) * fraction
    return end_factor


def make_entity(
    model: Dict[str, Any],
    enemy_id: str,
    wall_elapsed: float,
    band: Dict[str, Any],
    entity_id: int,
    boss: bool = False,
    boss_key: Optional[str] = None,
    run_elapsed: Optional[float] = None,
    encounter_kind: str = "MAIN_BOSS",
    elite_variant: bool = False,
    variant_id: Optional[str] = None,
) -> Dict[str, Any]:
    if run_elapsed is None:
        run_elapsed = wall_elapsed
    simulation = model["simulation_model"]
    if boss:
        if encounter_kind == "MINI_BOSS":
            source = simulation["mini_boss_stats"][boss_key or ""]
        else:
            source = simulation["boss_stats"][boss_key or ""]
        hp = number(source["base_hp"])
        damage = number(source["base_damage"])
        speed = number(source["base_speed"])
        attack_interval = number(source["attack_interval_seconds"])
        delay = 0.0
        xp = integer(source["xp_value"])
        telegraph = number(source["telegraph_seconds"])
        wave_damage = 1.0
        durability = 1.0
    else:
        source = simulation["enemy_stats"][enemy_id]
        archetype = stat_map(model)[enemy_id]
        durability = number(archetype["durability_multiplier"])
        hp = number(source["base_hp"]) * durability * number(band["enemy_hp_multiplier"])
        damage = number(source["base_damage"])
        speed = number(source["base_speed"])
        attack_interval = number(source["attack_interval_seconds"])
        delay = number(source["contact_delay_seconds"])
        xp = integer(source["xp_value"])
        telegraph = 0.0
        wave_damage = number(band["enemy_damage_multiplier"])
        if elite_variant:
            policy = simulation["elite_variation_policy"]
            overlay = policy.get("variant_overrides", {}).get("records", {}).get(variant_id or "")
            if overlay is None:
                overlay = policy["variant_overlay"]
            hp *= number(overlay["hp_multiplier"])
            damage *= number(overlay["damage_multiplier"])
            speed *= number(overlay["speed_multiplier"])
            xp = round_half_up(xp * number(overlay["xp_multiplier"]))
    return {
        "entity_id": entity_id,
        "enemy_id": enemy_id,
        "boss": boss,
        "boss_key": boss_key,
        "encounter_kind": encounter_kind if boss else "ORDINARY_WAVE",
        "elite_variant": elite_variant,
        "variant_id": variant_id,
        "spawn_time": run_elapsed,
        "spawn_wall_time": wall_elapsed,
        "hp": hp,
        "max_hp": hp,
        "base_damage": damage,
        "base_speed": speed,
        "attack_interval": attack_interval,
        "contact_delay": delay,
        "telegraph_seconds": telegraph,
        "wave_damage": wave_damage,
        "durability": durability,
        "xp": xp,
        "next_attack": wall_elapsed + attack_interval,
        "damage_taken": 0.0,
    }


def calculate_profile_stats(model: Dict[str, Any], profile: Dict[str, Any], hero_id: str) -> Dict[str, float]:
    hero = model["simulation_model"]["heroes_and_profiles"]["heroes"][hero_id]
    meta = profile["meta_ranks"]
    meta_effects = model["simulation_model"]["heroes_and_profiles"]["meta_effect_parameters"]
    combat = model["simulation_model"]["combat_math"]
    hp = number(hero["canonical_hp"]) * (1.0 + number(meta["vitality"]) * number(meta_effects["vitality_hp_per_rank"]))
    defense_per_rank = number(combat["defense_reduction_per_meta_rank"])
    armor = number(model["hero_stats"]["base"]["armor"])
    defense = armor + number(meta["defense"]) * defense_per_rank
    return {
        "max_hp": hp,
        "move_speed": number(hero["canonical_move_speed_percent"]) * (1.0 + number(meta["agility"]) * number(meta_effects["agility_speed_per_rank"])),
        "damage_multiplier": number(profile["damage_multiplier"]),
        "cooldown_multiplier": number(profile["cooldown_multiplier"]),
        "damage_reduction": min(number(combat["mitigation_cap"]), defense),
        "crit_chance": number(hero["crit_chance"]),
        "crit_multiplier": number(hero["crit_multiplier"]),
    }


def apply_level_upgrade(model: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    catalog = model["simulation_model"]["build_catalog"]
    progression = catalog["synergy_progression"]
    weapon_max = integer(catalog["weapon_max_level"])
    passive_max = integer(catalog["passive_max_rank"])
    path = state["synergy_path"]
    pair_index = integer(state["active_pair_index"])
    pair_id = path[pair_index]
    pair = state["pair_progress"][pair_id]
    if pair["weapon_level"] < weapon_max:
        pair["weapon_level"] += 1
    if pair["passive_rank"] < passive_max:
        pair["passive_rank"] += 1
    pair_complete = pair["weapon_level"] >= weapon_max and pair["passive_rank"] >= passive_max
    state["weapon_level"] = pair["weapon_level"]
    state["passive_rank"] = pair["passive_rank"]
    state["active_pair_id"] = pair_id
    event = {
        "type": "paired_weapon_passive_level",
        "pair_id": pair_id,
        "weapon_level": pair["weapon_level"],
        "passive_rank": pair["passive_rank"],
        "pair_complete": pair_complete,
        "level": state["level"],
    }
    if pair_complete and pair_index + 1 < len(path):
        state["active_pair_index"] = pair_index + 1
        state["active_pair_id"] = path[pair_index + 1]
        next_pair = state["pair_progress"][state["active_pair_id"]]
        state["weapon_level"] = next_pair["weapon_level"]
        state["passive_rank"] = next_pair["passive_rank"]
        event["next_pair_id"] = state["active_pair_id"]
    return event


def damage_components(model: Dict[str, Any], profile: Dict[str, Any], hero_id: str, state: Dict[str, Any]) -> Dict[str, float]:
    catalog = model["simulation_model"]["build_catalog"]
    hero = model["simulation_model"]["heroes_and_profiles"]["heroes"][hero_id]
    # The paired progression tracks three independent 10/10 eligibility paths;
    # damage remains anchored to the hero's equipped starter weapon/passive so
    # moving to the next path does not accidentally reset the build's combat
    # power to level 1.
    weapon = catalog["weapons"][hero["starting_weapon_id"]]
    passive = catalog["passives"][hero["starting_passive_id"]]
    combat = model["simulation_model"]["combat_math"]
    weapon_level_bonus = number(combat["weapon_level_damage_per_level"])
    pair_progress = state.get("pair_progress", {})
    completed_weapon_levels = max(
        [integer(pair["weapon_level"]) for pair in pair_progress.values()]
        or [integer(state.get("weapon_level", 1))]
    )
    completed_passive_ranks = max(
        [integer(pair["passive_rank"]) for pair in pair_progress.values()]
        or [integer(state.get("passive_rank", 0))]
    )
    weapon_level_multiplier = 1.0 + weapon_level_bonus * (completed_weapon_levels - 1)
    passive_multiplier = 1.0
    passive_multiplier += number(passive["damage_per_rank"]) * completed_passive_ranks
    crit_expected = 1.0 + number(hero["crit_chance"]) * (number(hero["crit_multiplier"]) - 1.0)
    base_per_target = (
        number(weapon["base_damage"])
        * weapon_level_multiplier
        * passive_multiplier
        * number(profile["damage_multiplier"])
        * crit_expected
        * (1.0 + state["fallback_damage_bonus"])
    )
    targets = integer(weapon["targets_per_attack"])
    base_attack_damage = base_per_target * targets
    synergy_damage = 0.0
    claimed_synergy_ids = state.get("claimed_synergy_ids", [])
    if claimed_synergy_ids:
        proposed_synergy = sum(
            base_attack_damage * number(catalog["synergies"][synergy_id]["damage_multiplier"])
            for synergy_id in claimed_synergy_ids
        )
        share_cap = number(model["simulation_model"]["target_policy"]["synergy_damage_share_max"])
        synergy_damage = min(proposed_synergy, base_attack_damage * share_cap / (1.0 - share_cap))
    return {
        "base_attack_damage": base_attack_damage,
        "synergy_attack_damage": synergy_damage,
        "total_attack_damage": base_attack_damage + synergy_damage,
        "targets_per_attack": targets,
        "attack_interval": number(weapon["attack_interval_seconds"]) * number(profile["cooldown_multiplier"]),
    }


def resolve_chest(
    model: Dict[str, Any],
    state: Dict[str, Any],
    checkpoint_id: str,
    elapsed: float,
    final: bool = False,
    encounter_kind: str = "MAIN_BOSS",
) -> Dict[str, Any]:
    catalog = model["simulation_model"]["build_catalog"]
    if final:
        return {
            "checkpoint_id": checkpoint_id,
            "encounter_kind": encounter_kind,
            "outcome": "NO_CHEST",
            "time": elapsed,
            "status": "CANON_ARCHITECTURE_NO_BOSS_CHEST",
        }
    path = state.get("synergy_path", [])
    eligible_synergy_id = None
    for synergy_id in path:
        pair = state.get("pair_progress", {}).get(synergy_id, {})
        synergy = catalog["synergies"].get(synergy_id)
        if (
            synergy is not None
            and integer(pair.get("weapon_level", 0)) >= integer(synergy["requires_weapon_level"])
            and integer(pair.get("passive_rank", 0)) >= integer(synergy["requires_passive_rank"])
            and synergy_id not in state.get("claimed_synergy_ids", [])
        ):
            eligible_synergy_id = synergy_id
            break
    if eligible_synergy_id is None:
        return {"checkpoint_id": checkpoint_id, "outcome": "FALLBACK_REQUIRED", "time": elapsed, "status": "PROPOSED"}
    max_claims = integer(model["simulation_model"]["build_catalog"]["max_synergy_claims_per_run"])
    if state.get("claimed_synergy_count", 0) < max_claims:
        state["synergy_id"] = eligible_synergy_id
        state.setdefault("claimed_synergy_ids", []).append(eligible_synergy_id)
        state["claimed_synergy_count"] = state.get("claimed_synergy_count", 0) + 1
        outcome = "SYNERGY_GRANTED"
    else:
        fallback = catalog["offer_model"]["fallback"]
        state["fallback_damage_bonus"] += number(fallback["damage_multiplier_additive"])
        outcome = "FALLBACK_UPGRADE"
    return {
        "checkpoint_id": checkpoint_id,
        "encounter_kind": encounter_kind,
        "outcome": outcome,
        "time": elapsed,
        "synergy_id": eligible_synergy_id,
        "claimed_synergy_count": state.get("claimed_synergy_count", 0),
        "claimed_synergy_ids": list(state.get("claimed_synergy_ids", [])),
    }


def grant_once(ledger: Dict[str, Dict[str, Any]], key: str, reward: Dict[str, int]) -> bool:
    if key in ledger:
        return False
    ledger[key] = dict(reward)
    return True


def reward_key(model: Dict[str, Any], run_id: str, scope: str, checkpoint_id: str, reward_type: str) -> str:
    pattern = model["architecture_contract"]["reward_idempotency_key_format"]
    return pattern.format(run_id=run_id, reward_scope=scope, checkpoint_id=checkpoint_id, reward_type=reward_type)


def reward_amount(row: Dict[str, Any]) -> Dict[str, int]:
    return {wallet: integer(row[wallet]) for wallet in ("gold", "moon_seals", "boss_essence") if wallet in row}


def sum_reward_rows(rows: Iterable[Dict[str, Any]], wallets: Iterable[str]) -> Dict[str, int]:
    totals = {wallet: 0 for wallet in wallets}
    for row in rows:
        for wallet in totals:
            totals[wallet] += integer(row.get(wallet, 0))
    return totals


def reward_scenario_audit(model: Dict[str, Any]) -> Dict[str, Any]:
    """Audit first/repeat/defeat reward paths from the model reward rows."""
    rewards = model["rewards"]
    wallets = list(rewards["wallets"])
    checkpoint_rows = list(rewards["checkpoint_rewards"])
    checkpoint_total = sum_reward_rows(checkpoint_rows, wallets)
    first_clear_bonus = reward_amount(rewards["first_clear_bonus"])
    first_clear_total = {
        wallet: checkpoint_total[wallet] + first_clear_bonus.get(wallet, 0)
        for wallet in wallets
    }
    repeat_total = dict(checkpoint_total)
    defeat_policy = rewards["defeat_after_checkpoint"]
    defeat_rows = {}
    idempotency_pass = True
    for row in checkpoint_rows:
        checkpoint_id = str(row["checkpoint_id"])
        payout = {
            wallet: (
                round_half_up(integer(row.get(wallet, 0)) * number(defeat_policy["gold_factor"]))
                if wallet == "gold"
                else integer(row.get(wallet, 0))
            )
            for wallet in wallets
        }
        defeat_rows[checkpoint_id] = payout
        ledger: Dict[str, Dict[str, Any]] = {}
        for wallet, amount in payout.items():
            key = reward_key(model, "scenario_defeat", "CHECKPOINT_OR_RESULT", checkpoint_id, wallet)
            first = grant_once(ledger, key, {wallet: amount})
            duplicate = grant_once(ledger, key, {wallet: amount})
            idempotency_pass = idempotency_pass and first and not duplicate
    for scenario_id, totals in (
        ("first_clear_30m", first_clear_total),
        ("repeat_clear_30m", repeat_total),
    ):
        ledger = {}
        for wallet, amount in totals.items():
            key = reward_key(model, f"scenario_{scenario_id}", "CHECKPOINT_OR_RESULT", "run_result", wallet)
            first = grant_once(ledger, key, {wallet: amount})
            duplicate = grant_once(ledger, key, {wallet: amount})
            idempotency_pass = idempotency_pass and first and not duplicate
    return {
        "status": model["simulation_model"]["reward_scenario_policy"]["status"],
        "source": model["simulation_model"]["reward_scenario_policy"]["source"],
        "first_clear_30m_total": first_clear_total,
        "repeat_clear_30m_total": repeat_total,
        "defeat_after_checkpoint": defeat_rows,
        "idempotency_pass": idempotency_pass,
        "runtime_claim": "NOT_IMPLEMENTED",
    }


def resolve_reward(model: Dict[str, Any], ledger: Dict[str, Dict[str, Any]], run_id: str, checkpoint_id: str, reward: Dict[str, int]) -> Dict[str, Any]:
    attempts = []
    for wallet, amount in sorted(reward.items()):
        key = reward_key(model, run_id, "CHECKPOINT_OR_RESULT", checkpoint_id, wallet)
        accepted = grant_once(ledger, key, {wallet: amount})
        duplicate = grant_once(ledger, key, {wallet: amount})
        attempts.append({"key": key, "wallet": wallet, "amount": amount, "accepted": accepted, "duplicate_accepted": duplicate})
    return {"checkpoint_id": checkpoint_id, "attempts": attempts}


def sum_ledger(ledger: Dict[str, Dict[str, Any]]) -> Dict[str, int]:
    total = {"gold": 0, "moon_seals": 0, "boss_essence": 0}
    for reward in ledger.values():
        for wallet, amount in reward.items():
            if wallet in total:
                total[wallet] += int(amount)
    return total


def percentile(values: List[float], fraction: float) -> Optional[float]:
    if not values:
        return None
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(math.floor((len(ordered) - 1) * fraction)))
    return round(ordered[index], 3)


def content_balance_audit(model: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate measurable budgets for every content record in the model.

    The run loop exercises the two protected starter builds. This independent
    pass proves that the remaining catalog records are populated, linked, and
    numerically inspectable without promoting proposed values to CANON or
    runtime evidence.
    """
    simulation = model["simulation_model"]
    catalog = simulation["build_catalog"]
    anchors = catalog["balance_anchors"]
    reference_hp = number(anchors["reference_ordinary_hp"])
    target_share = number(simulation["target_policy"]["synergy_damage_share_max"])

    weapons: Dict[str, Any] = {}
    for weapon_id, weapon in catalog["weapons"].items():
        base_dps = number(weapon["base_damage"]) * integer(weapon["targets_per_attack"]) / number(weapon["attack_interval_seconds"])
        evolved = weapon["evolution"]
        evolved_targets = integer(weapon["targets_per_attack"]) + integer(evolved["extra_targets"])
        evolved_dps = (
            number(weapon["base_damage"])
            * evolved_targets
            * (1.0 + number(evolved["damage_multiplier"]))
            / (number(weapon["attack_interval_seconds"]) * number(evolved["attack_interval_multiplier"]))
        )
        weapons[weapon_id] = {
            "base_dps_reference": round(base_dps, 3),
            "evolved_dps_reference": round(evolved_dps, 3),
            "base_reference_ttk_seconds": round(reference_hp / max(base_dps, 1e-9), 3),
            "evolved_reference_ttk_seconds": round(reference_hp / max(evolved_dps, 1e-9), 3),
            "status": weapon.get("balance_status", "PROPOSED"),
        }

    passives: Dict[str, Any] = {}
    passive_cap = integer(catalog["passive_max_rank"])
    for passive_id, passive in catalog["passives"].items():
        passives[passive_id] = {
            "max_rank": passive_cap,
            "max_damage_multiplier": round(1.0 + number(passive["damage_per_rank"]) * passive_cap, 4),
            "max_defense_fraction_before_cap": round(number(passive["defense_per_rank"]) * passive_cap, 4),
            "max_primary_value": round(number(passive["primary_value_per_rank"]) * passive_cap, 4),
            "trigger_cooldown_seconds": number(passive["trigger_cooldown_seconds"]),
            "stack_cap": integer(passive["stack_cap"]),
            "status": passive.get("balance_status", "PROPOSED"),
        }

    synergies: Dict[str, Any] = {}
    for synergy_id, synergy in catalog["synergies"].items():
        raw_share = number(synergy["damage_multiplier"]) / (1.0 + number(synergy["damage_multiplier"]))
        synergies[synergy_id] = {
            "damage_share_before_geometry_guard": round(raw_share, 4),
            "damage_share_guard": target_share,
            "guard_pass": raw_share <= target_share + 1e-9,
            "effective_interval_multiplier": number(synergy["attack_interval_multiplier"]),
            "extra_targets": integer(synergy["extra_targets"]),
            "effect_duration_seconds": number(synergy["effect_duration_seconds"]),
            "status": synergy.get("balance_status", "PROPOSED"),
        }

    artifacts: Dict[str, Any] = {}
    for artifact_id, artifact in catalog["artifacts"].items():
        artifacts[artifact_id] = {
            "effect_key": artifact["effect_key"],
            "effect_family": artifact["effect_family"],
            "numeric_parameters": {key: number(value) for key, value in artifact["effect_parameters"].items()},
            "uses_build_slots": bool(artifact["consumes_weapon_or_passive_slot"]),
            "status": artifact.get("balance_status", "PROPOSED"),
        }

    ordinary: Dict[str, Any] = {}
    for enemy_id in unwrap(simulation["content_roster"]["ordinary_enemy_ids"]):
        record = simulation["enemy_stats"][enemy_id]
        ordinary[enemy_id] = {
            "base_stats": {key: number(record["resolved_base_stats"][key]) for key in ("hp", "atk", "speed")},
            "late_run_stats": {key: number(record["late_run_effective_stats"][key]) for key in ("hp", "atk", "speed")},
            "role": record.get("attack_type", "ordinary"),
            "status": record.get("balance_status", "PROPOSED"),
        }

    elite: Dict[str, Any] = {}
    for variant_id in unwrap(simulation["content_roster"]["elite_variant_ids"]):
        record = simulation["elite_variation_policy"]["variant_overrides"]["records"][variant_id]
        elite[variant_id] = {
            "base_enemy_id": record["base_enemy_id"],
            "resolved_base_stats": {key: number(record["resolved_base_stats"][key]) for key in ("hp", "atk", "speed", "xp")},
            "late_run_stats": {key: number(record["late_run_effective_stats"][key]) for key in ("hp", "atk", "speed")},
            "status": record.get("balance_status", "PROPOSED"),
        }

    bosses: Dict[str, Any] = {}
    for checkpoint_id, record in simulation["boss_stats"].items():
        bosses[checkpoint_id] = {
            "boss_id": record["boss_id"],
            "hp": number(record["base_hp"]),
            "atk": number(record["base_damage"]),
            "speed": number(record["base_speed"]),
            "attack_interval_seconds": number(record["attack_interval_seconds"]),
            "telegraph_seconds": number(record["telegraph_seconds"]),
            "status": record.get("balance_status", record.get("boss_id_status", "PROPOSED")),
        }
    minis: Dict[str, Any] = {}
    for boss_id in (row["boss_id"] for row in simulation["run_schedule"]["mini_boss_checkpoints"]):
        record = simulation["mini_boss_stats"][boss_id]
        minis[boss_id] = {
            "hp": number(record["base_hp"]),
            "atk": number(record["base_damage"]),
            "speed": number(record["base_speed"]),
            "attack_interval_seconds": number(record["attack_interval_seconds"]),
            "telegraph_seconds": number(record["telegraph_seconds"]),
            "status": record.get("balance_status", record.get("stat_status", "PROPOSED")),
        }

    return {
        "status": "PROPOSED_MODEL_ONLY",
        "coverage": {
            "weapons": len(weapons),
            "passives": len(passives),
            "synergies": len(synergies),
            "artifacts": len(artifacts),
            "ordinary_enemies": len(ordinary),
            "elite_variants": len(elite),
            "main_bosses": len(bosses),
            "mini_bosses": len(minis),
        },
        "weapons": weapons,
        "passives": passives,
        "synergies": synergies,
        "artifacts": artifacts,
        "ordinary_enemies": ordinary,
        "elite_variants": elite,
        "main_bosses": bosses,
        "mini_bosses": minis,
    }


def simulate_legacy(model: Dict[str, Any], profile_name: str, hero_id: str, seed: int) -> Dict[str, Any]:
    """Run one deterministic model slice with a paused run clock at every boss.

    ``run_elapsed`` is the visible 20-minute clock.  ``wall_elapsed`` is the
    encounter clock used for attacks and focused TTK.  While a boss is alive,
    wall time advances but run time does not; ordinary spawning and XP pickup
    therefore cannot silently progress through a boss encounter.
    """
    simulation = model["simulation_model"]
    profile = simulation["heroes_and_profiles"]["profiles"][profile_name]
    dt = number(simulation["simulation_step_seconds"])
    main_duration = number(simulation["main_run_duration_seconds"])
    clock_policy = simulation["boss_clock_policy"]
    thresholds = xp_thresholds(model)
    rng = random.Random(seed)
    enemy_catalog = simulation["enemy_stats"]
    archetypes = stat_map(model)
    weights = simulation["wave_selection"]["composition_weights"]
    target_policy = simulation["target_policy"]
    combat = simulation["combat_math"]
    profile_stats = calculate_profile_stats(model, profile, hero_id)
    synergy_path = synergy_path_for_hero(model, hero_id)
    state = {
        "hero_id": hero_id,
        "profile": profile_name,
        "level": 1,
        "xp": 0.0,
        "weapon_level": 1,
        "passive_rank": 0,
        "synergy_id": None,
        "claimed_synergy_ids": [],
        "claimed_synergy_count": 0,
        "synergy_path": synergy_path,
        "active_pair_index": 0,
        "active_pair_id": synergy_path[0],
        "pair_progress": {
            synergy_id: {"weapon_level": 1, "passive_rank": 0}
            for synergy_id in synergy_path
        },
        "fallback_damage_bonus": 0.0,
        "pending_xp_drops": [],
        "xp_pickup_budget": 0.0,
        "xp_dropped": 0,
        "xp_collected": 0,
        "final_boss_outcome_valid": True,
    }
    active: List[Dict[str, Any]] = []
    boss: Optional[Dict[str, Any]] = None
    next_checkpoint_index = 0
    next_entity_id = 1
    spawn_accumulator = 0.0
    next_player_attack = 0.0
    player_hp = profile_stats["max_hp"]
    min_hp = player_hp
    total_incoming = 0.0
    peak_incoming_step = 0.0
    max_single_incoming_hit = 0.0
    death_time: Optional[float] = None
    death_run_clock: Optional[float] = None
    cap_samples: List[int] = []
    cap_seconds = 0.0
    suppressed_spawn_attempts = 0
    kills: List[Dict[str, Any]] = []
    boss_results: List[Dict[str, Any]] = []
    clock_events: List[Dict[str, Any]] = []
    level_times: Dict[str, float] = {}
    checkpoint_levels: Dict[str, int] = {}
    upgrade_events: List[Dict[str, Any]] = []
    chest_results: List[Dict[str, Any]] = []
    artifact_offer_results: List[Dict[str, Any]] = []
    reward_results: List[Dict[str, Any]] = []
    ledger: Dict[str, Dict[str, Any]] = {}
    run_id = f"{profile_name}:{hero_id}:{seed}"
    run_elapsed = 0.0
    wall_elapsed = 0.0
    loop_guard = 0
    checkpoints = sorted(model["boss_checkpoints"], key=lambda row: number(row["time_seconds"]))
    xp_pickup = simulation["xp_pickup_model"]
    magnet_per_rank = number(xp_pickup["magnet_capacity_per_rank"])

    def add_xp(amount: int, run_clock: float) -> None:
        state["xp"] += amount
        while state["level"] <= len(thresholds) and state["xp"] >= thresholds[state["level"] - 1]:
            state["level"] += 1
            level_times[str(state["level"])] = round(run_clock, 3)
            upgrade = apply_level_upgrade(model, state)
            upgrade["time"] = round(run_clock, 3)
            upgrade_events.append(upgrade)

    def register_kill(entity: Dict[str, Any], wall_clock: float, run_clock: float) -> None:
        spawn_ttk = wall_clock - entity["spawn_wall_time"]
        focused_start = entity.get("first_damage_time")
        focused_ttk = wall_clock - focused_start if focused_start is not None else spawn_ttk
        enemy_id = entity["enemy_id"]
        role = str(archetypes[enemy_id].get("role", ""))
        kind = "elite" if "elite" in role else "ordinary"
        kills.append({
            "enemy_id": enemy_id,
            "kind": kind,
            "spawn_time": round(entity["spawn_time"], 3),
            "spawn_wall_time": round(entity["spawn_wall_time"], 3),
            "defeat_time_wall": round(wall_clock, 3),
            "defeat_time_run_clock": round(run_clock, 3),
            "spawn_to_kill_seconds": round(spawn_ttk, 3),
            "focused_ttk_seconds": round(focused_ttk, 3),
            "xp": entity["xp"],
        })
        state["pending_xp_drops"].append({
            "available_time": run_clock + number(xp_pickup["drop_delay_seconds"]),
            "value": entity["xp"],
        })
        state["xp_dropped"] += entity["xp"]

    def collect_xp(run_clock: float, band: Dict[str, Any]) -> None:
        if run_clock < number(xp_pickup["first_level_window_seconds"]):
            capacity = number(xp_pickup["first_level_capacity_per_second"])
        else:
            capacity = number(xp_pickup["capacity_per_second_by_wave"][band["wave_band_id"]])
        capacity_multiplier = 1.0 + number(profile["meta_ranks"]["magnet"]) * magnet_per_rank
        state["xp_pickup_budget"] += capacity * capacity_multiplier * dt
        ready = sorted(
            [drop for drop in state["pending_xp_drops"] if drop["available_time"] <= run_clock + 1e-9],
            key=lambda drop: (drop["available_time"], drop["value"]),
        )
        for drop in ready:
            if state["xp_pickup_budget"] + 1e-9 < drop["value"]:
                continue
            state["xp_pickup_budget"] -= drop["value"]
            state["pending_xp_drops"].remove(drop)
            state["xp_collected"] += drop["value"]
            add_xp(drop["value"], run_clock)

    def resolve_boss(boss_entity: Dict[str, Any], wall_clock: float, run_clock: float) -> None:
        checkpoint_id = boss_entity["checkpoint_id"]
        final = checkpoint_is_final(model, checkpoint_id)
        ttk = wall_clock - boss_entity["boss_start_wall_time"]
        target_range = target_policy["final_boss_ttk_seconds"] if final else target_policy["first_slice_boss_ttk_seconds"]
        target_pass = number(target_range[0]) <= ttk <= number(target_range[1])
        within_window = (not final) or ttk <= number(simulation["post_final_boss_window_seconds"])
        status = "DEFEATED" if (not final or within_window) else "POST_RUN_WINDOW_EXCEEDED"
        if final and not within_window:
            state["final_boss_outcome_valid"] = False
        boss_results.append({
            "checkpoint_id": checkpoint_id,
            "boss_id": boss_entity["enemy_id"],
            "status": status,
            "spawn_time": round(boss_entity["boss_start_run_clock"], 3),
            "encounter_start_wall_time": round(boss_entity["boss_start_wall_time"], 3),
            "defeat_time": round(wall_clock, 3),
            "defeat_time_wall_seconds": round(wall_clock, 3),
            "defeat_time_run_clock_seconds": round(run_clock, 3),
            "ttk_seconds": round(ttk, 3),
            "target_range": list(target_range),
            "target_pass": target_pass,
            "within_post_run_window": within_window,
        })
        clock_events.append({
            "checkpoint_id": checkpoint_id,
            "checkpoint_seconds": round(boss_entity["boss_start_run_clock"], 3),
            "run_clock_stop_seconds": round(boss_entity["boss_start_run_clock"], 3),
            "run_clock_resume_seconds": round(run_clock, 3) if not final else None,
            "encounter_duration_seconds": round(ttk, 3),
            "run_clock_advanced_during_encounter": False,
            "wave_xp_spawn_clock_advanced_during_encounter": False,
            "status": status,
        })
        if not final or within_window:
            reward_row = boss_reward_map(model)[checkpoint_id]
            reward_results.append(resolve_reward(model, ledger, run_id, checkpoint_id, reward_amount(reward_row)))
            chest_results.append(resolve_chest(model, state, checkpoint_id, run_clock))
        if final:
            chest_results.append({"checkpoint_id": checkpoint_id, "outcome": "NO_BOSS_CHEST", "status": "CANON_ARCHITECTURE"})
            if within_window:
                first_clear = model["rewards"]["first_clear_bonus"]
                reward_results.append(resolve_reward(model, ledger, run_id, "run_result", reward_amount(first_clear)))
                artifact_model = simulation["artifact_offer_model"]
                artifact_offer_results.append({
                    "offer_id": f"{run_id}:first_clear_artifact",
                    "source_kind": "FIRST_CLEAR_REWARD",
                    "source_id": "reward_first_clear_bonus",
                    "choice_count": integer(artifact_model["choice_count"]),
                    "status": "OFFER_CREATED_PENDING_SELECTION",
                    "effect_status": artifact_model["effect_parameters_status"],
                })

    while True:
        loop_guard += 1
        if loop_guard > 200000:
            raise RuntimeError("simulation loop exceeded deterministic guard")
        if death_time is not None:
            break

        encounter_active = boss is not None
        if not encounter_active and next_checkpoint_index < len(checkpoints):
            checkpoint = checkpoints[next_checkpoint_index]
            checkpoint_seconds = number(checkpoint["time_seconds"])
            if run_elapsed + 1e-9 >= checkpoint_seconds:
                checkpoint_id = str(checkpoint["checkpoint_id"])
                boss = make_entity(
                    model,
                    simulation["boss_stats"][checkpoint_id]["boss_id"],
                    wall_elapsed,
                    wave_at(model, min(run_elapsed, main_duration - dt)),
                    next_entity_id,
                    True,
                    checkpoint_id,
                    run_elapsed=run_elapsed,
                )
                next_entity_id += 1
                boss["checkpoint_id"] = checkpoint_id
                boss["boss_start_run_clock"] = run_elapsed
                boss["boss_start_wall_time"] = wall_elapsed
                next_checkpoint_index += 1
                encounter_active = True

        # Only the visible run clock drives ordinary wave selection, spawning,
        # and XP pickup.  This branch is skipped for the full boss encounter.
        if not encounter_active and run_elapsed < main_duration - 1e-9:
            band = wave_state_at(model, run_elapsed)
            collect_xp(run_elapsed, band)
            spawn_accumulator += number(band["spawn_budget_per_second"]) * dt * boss_interruption_factor(model, run_elapsed)
            while spawn_accumulator >= 1.0:
                spawn_accumulator -= 1.0
                cap = integer(band["active_cap"])
                if len(active) >= cap:
                    suppressed_spawn_attempts += 1
                    continue
                enemy_id = weighted_choice(rng, band.get("composition_weights", weights[band["wave_band_id"]]))
                entity = make_entity(model, enemy_id, wall_elapsed, band, next_entity_id, run_elapsed=run_elapsed)
                next_entity_id += 1
                active.append(entity)

        occupied = len(active)
        if not encounter_active:
            cap_samples.append(occupied)
            band_now = wave_state_at(model, min(run_elapsed, main_duration - dt))
            if occupied >= integer(band_now["active_cap"]):
                cap_seconds += dt

        # Incoming attacks continue on the separate wall/encounter clock.  A
        # boss can therefore threaten the player while the visible timer is
        # paused, which is the intended interruption/recovery model.
        incoming_this_step = 0.0
        candidates = sorted(active, key=lambda entity: (entity["contact_delay"], entity["entity_id"]))
        if boss is not None and boss["hp"] > 0.0:
            candidates.append(boss)
        attacker_limit = integer(combat["engaged_attacker_limit"])
        for entity in candidates[:attacker_limit]:
            if wall_elapsed + dt < entity["spawn_wall_time"] + entity["contact_delay"]:
                continue
            if wall_elapsed + 1e-9 < entity["next_attack"]:
                continue
            interval = entity["attack_interval"]
            while entity["next_attack"] <= wall_elapsed + 1e-9:
                entity["next_attack"] += interval
            if rng.random() > number(profile["hit_probability"]):
                continue
            damage_taken = entity["base_damage"] * entity["wave_damage"] * (1.0 - profile_stats["damage_reduction"])
            incoming_this_step += damage_taken
            max_single_incoming_hit = max(max_single_incoming_hit, damage_taken)
        player_hp -= incoming_this_step
        total_incoming += incoming_this_step
        peak_incoming_step = max(peak_incoming_step, incoming_this_step / dt)
        min_hp = min(min_hp, player_hp)
        if player_hp <= 0.0:
            player_hp = 0.0
            death_time = wall_elapsed
            death_run_clock = run_elapsed
            break

        # Outgoing attacks continue during a boss encounter, but no new
        # ordinary wave/XP clock work is performed until the boss is gone.
        damage = damage_components(model, profile, hero_id, state)
        if wall_elapsed + 1e-9 >= next_player_attack:
            while next_player_attack <= wall_elapsed + 1e-9:
                next_player_attack += damage["attack_interval"]
            total_damage = damage["total_attack_damage"]
            boss_damage = 0.0
            if boss is not None and boss["hp"] > 0.0:
                boss_damage = total_damage * number(combat["boss_focus_fraction"])
                boss["hp"] -= boss_damage
                boss["damage_taken"] += boss_damage
                if boss["hp"] <= 0.0:
                    defeated_boss = boss
                    resolve_boss(defeated_boss, wall_elapsed, run_elapsed)
                    boss = None
            remaining = total_damage - boss_damage
            targets = sorted(active, key=lambda entity: (entity["spawn_wall_time"], entity["entity_id"]))[: damage["targets_per_attack"]]
            if targets:
                per_target = remaining / len(targets)
                for entity in list(targets):
                    hit_damage = per_target
                    if entity["enemy_id"] == "enemy_bell_crab":
                        crab = enemy_catalog[entity["enemy_id"]]
                        if rng.random() < number(crab["rear_hit_probability"]):
                            hit_damage *= number(crab["rear_weakness_multiplier"])
                    entity["hp"] -= hit_damage
                    entity["damage_taken"] += hit_damage
                    if entity.get("first_damage_time") is None:
                        entity["first_damage_time"] = wall_elapsed

        survivors = []
        for entity in active:
            if entity["hp"] <= 0.0:
                register_kill(entity, wall_elapsed, run_elapsed)
            else:
                survivors.append(entity)
        active = survivors

        for checkpoint_time in progression_checkpoint_seconds(model):
            key = f"{int(checkpoint_time)}"
            if run_elapsed + 1e-9 >= checkpoint_time and key not in checkpoint_levels:
                checkpoint_levels[key] = state["level"]

        # A final boss ends the model run at its defeat.  Non-final bosses
        # leave the visible clock at the checkpoint for the next frame, then
        # normal wave time resumes.
        if boss is None and next_checkpoint_index >= len(checkpoints) and run_elapsed >= main_duration - 1e-9:
            break

        wall_elapsed = round(wall_elapsed + dt, 9)
        if boss is None and run_elapsed < main_duration - 1e-9:
            run_elapsed = round(min(main_duration, run_elapsed + dt), 9)

    if boss is not None and death_time is not None:
        encounter_duration = wall_elapsed - boss["boss_start_wall_time"]
        boss_results.append({
            "checkpoint_id": boss["checkpoint_id"],
            "boss_id": boss["enemy_id"],
            "status": "RUN_FAILED_DURING_ENCOUNTER",
            "spawn_time": round(boss["boss_start_run_clock"], 3),
            "encounter_start_wall_time": round(boss["boss_start_wall_time"], 3),
            "defeat_time": None,
            "defeat_time_wall_seconds": None,
            "defeat_time_run_clock_seconds": None,
            "ttk_seconds": None,
            "target_range": list(target_policy["final_boss_ttk_seconds"] if checkpoint_is_final(model, boss["checkpoint_id"]) else target_policy["first_slice_boss_ttk_seconds"]),
            "target_pass": False,
            "within_post_run_window": False,
        })
        clock_events.append({
            "checkpoint_id": boss["checkpoint_id"],
            "checkpoint_seconds": round(boss["boss_start_run_clock"], 3),
            "run_clock_stop_seconds": round(boss["boss_start_run_clock"], 3),
            "run_clock_resume_seconds": None,
            "encounter_duration_seconds": round(encounter_duration, 3),
            "run_clock_advanced_during_encounter": False,
            "wave_xp_spawn_clock_advanced_during_encounter": False,
            "status": "RUN_FAILED_DURING_ENCOUNTER",
        })

    ordinary_ttks = [row["focused_ttk_seconds"] for row in kills if row["kind"] == "ordinary"]
    elite_ttks = [row["focused_ttk_seconds"] for row in kills if row["kind"] == "elite"]
    ttk_by_enemy: Dict[str, List[float]] = {}
    for row in kills:
        ttk_by_enemy.setdefault(row["enemy_id"], []).append(row["focused_ttk_seconds"])
    cap_stats = {
        "max_occupancy": max(cap_samples) if cap_samples else 0,
        "mean_occupancy": round(statistics.mean(cap_samples), 3) if cap_samples else 0.0,
        "p95_occupancy": percentile([float(value) for value in cap_samples], 0.95),
        "cap_seconds": round(cap_seconds, 3),
        "suppressed_spawn_attempts": suppressed_spawn_attempts,
        "sample_clock": "RUN_CLOCK_EXCLUDING_BOSS_ENCOUNTER_PAUSE",
        "sample_seconds": round(sum(dt for _ in cap_samples), 3),
    }
    reward_balance = sum_ledger(ledger)
    survived = death_time is None
    run_completed = survived and boss is None and next_checkpoint_index >= len(checkpoints) and run_elapsed >= main_duration - 1e-9
    return {
        "status": "SIMULATED_MODEL_ONLY",
        "source_revision": model["source_of_truth"]["source_revision"],
        "architecture_revision": model["architecture_contract"]["source_revision"],
        "seed": seed,
        "profile": profile_name,
        "hero_id": hero_id,
        "model_inputs": {
            "profile_meta_ranks": profile["meta_ranks"],
            "profile_stats": {key: round(value, 6) for key, value in profile_stats.items()},
            "build_rules": {
                "weapon_slots": integer(simulation["build_catalog"]["weapon_slot_limit"]),
                "passive_slots": integer(simulation["build_catalog"]["passive_slot_limit"]),
                "weapon_max_level": integer(simulation["build_catalog"]["weapon_max_level"]),
                "passive_max_rank": integer(simulation["build_catalog"]["passive_max_rank"]),
                "max_synergy_claims_per_run": integer(simulation["build_catalog"]["max_synergy_claims_per_run"]),
            },
            "ordinary_roster_size": len(unwrap(simulation["content_roster"]["ordinary_enemy_ids"])),
            "elite_variant_proposal_count": len(unwrap(simulation["content_roster"]["elite_variant_ids"])),
            "elite_variant_registered_cap": integer(simulation["content_roster"]["registered_variant_cap"]),
            "proposed_build": {
                "weapon_id": model["simulation_model"]["heroes_and_profiles"]["heroes"][hero_id]["starting_weapon_id"],
                "passive_id": model["simulation_model"]["heroes_and_profiles"]["heroes"][hero_id]["starting_passive_id"],
            },
        },
        "progression": {
            "final_level_at_20_minutes": state["level"],
            "final_xp_at_20_minutes": round(state["xp"], 3),
            "levels_at_checkpoints": {
                str(int(checkpoint_time)): checkpoint_levels.get(str(int(checkpoint_time)))
                for checkpoint_time in progression_checkpoint_seconds(model)
            },
            "xp_at_20_minutes": round(state["xp"], 3),
            "xp_dropped": state["xp_dropped"],
            "xp_collected": state["xp_collected"],
            "xp_pending_at_end": sum(drop["value"] for drop in state["pending_xp_drops"]),
            "level_up_times": level_times,
            "upgrade_events": upgrade_events,
            "xp_formula_status": "CANON_FORMULA_SIMULATED",
        },
        "combat": {
            "ordinary_kills": len(ordinary_ttks),
            "elite_kills": len(elite_ttks),
            "ordinary_ttk_seconds": {"mean": percentile(ordinary_ttks, 0.5), "p95": percentile(ordinary_ttks, 0.95), "target": list(target_policy["ordinary_ttk_seconds"])},
            "elite_ttk_seconds": {"mean": percentile(elite_ttks, 0.5), "p95": percentile(elite_ttks, 0.95), "target": list(target_policy["elite_ttk_seconds"])},
            "ttk_by_enemy_seconds": {
                enemy_id: {"median": percentile(values, 0.5), "p95": percentile(values, 0.95), "samples": len(values)}
                for enemy_id, values in sorted(ttk_by_enemy.items())
            },
            "boss_results": boss_results,
            "synergy_id": state["synergy_id"],
            "fallback_damage_bonus": round(state["fallback_damage_bonus"], 6),
            "chest_results": chest_results,
            "artifact_offer_results": artifact_offer_results,
        },
        "risk": {
            "survived_main_run": survived,
            "death_time_seconds": death_time,
            "death_time_wall_seconds": death_time,
            "death_time_run_clock_seconds": death_run_clock,
            "min_hp": round(min_hp, 3),
            "max_hp": round(profile_stats["max_hp"], 3),
            "total_incoming_damage": round(total_incoming, 3),
            "peak_incoming_dps": round(peak_incoming_step, 3),
            "max_single_incoming_hit": round(max_single_incoming_hit, 3),
            "max_single_hit_fraction_of_base_hp": round(max_single_incoming_hit / number(model["hero_stats"]["base"]["hp"]), 6),
            "telegraph_bound_target": number(target_policy["incoming_untelegraphed_hit_fraction_of_base_hp"]),
            "conservative_single_hit_bound_pass": max_single_incoming_hit / number(model["hero_stats"]["base"]["hp"]) <= number(target_policy["incoming_untelegraphed_hit_fraction_of_base_hp"]),
        },
        "waves": {
            "active_cap": cap_stats,
            "boss_encounter_wall_seconds": round(sum(event["encounter_duration_seconds"] for event in clock_events), 3),
            "visible_run_clock_final_seconds": round(run_elapsed, 3),
            "wall_clock_final_seconds": round(wall_elapsed, 3),
            "boss_clock_events": clock_events,
            "boss_wave_ramp": {
                "status": simulation["boss_wave_ramp"]["status"],
                "applies_to": simulation["boss_wave_ramp"]["applies_to"],
                "phase_order": simulation["boss_wave_ramp"]["phase_order"],
                "samples": wave_ramp_samples(model),
            },
            "boss_interruption_checkpoints": [
                {"time_seconds": checkpoint, "factor_at_checkpoint": round(boss_interruption_factor(model, checkpoint), 6), "factor_at_plus_8": round(boss_interruption_factor(model, checkpoint + number(simulation["boss_interruption"]["suppression_seconds"])), 6)}
                for checkpoint in (number(row["time_seconds"]) for row in main_checkpoints(model))
            ],
        },
        "rewards": {
            "ledger_balance": reward_balance,
            "reward_events": reward_results,
            "scenario_audit": reward_scenario_audit(model),
            "idempotency_pass": all(not attempt.get("duplicate_accepted", False) for event in reward_results for attempt in event.get("attempts", [])),
            "final_boss_chest_offer_created": False,
            "first_clear_artifact_offer_created": bool(artifact_offer_results),
            "artifact_offer_choice_count": integer(simulation["artifact_offer_model"]["choice_count"]) if artifact_offer_results else 0,
        },
        "run_outcome": {
            "completed_model_run": run_completed,
            "main_run_clock_duration_seconds": round(main_duration, 3),
            "visible_run_clock_final_seconds": round(run_elapsed, 3),
            "wall_clock_duration_seconds": round(wall_elapsed, 3),
            "boss_encounter_pause_seconds": round(sum(event["encounter_duration_seconds"] for event in clock_events), 3),
        },
        "runtime_boundary": {
            "godot_runtime_executed": False,
            "collision_and_telegraph_evidence": "NOT_IMPLEMENTED",
            "android_fps_evidence": "BLOCKED",
            "model_status": "SIMULATED_MODEL_ONLY",
        },
        "clock_policy": {
            "applies_to": clock_policy["applies_to"],
            "checkpoint_seconds": clock_policy["checkpoint_seconds"],
            "run_clock_stops_at_boss_checkpoint": clock_policy["run_clock_stops_at_boss_checkpoint"],
            "wave_xp_spawn_clock_advances_during_encounter": clock_policy["wave_xp_spawn_clock_advances_during_encounter"],
            "resolution_clock": clock_policy["resolution_clock"],
        },
    }


def simulate(model: Dict[str, Any], profile_name: str, hero_id: str, seed: int) -> Dict[str, Any]:
    """Run one 30-minute model slice with separate main/mini clock policies.

    Main bosses pause the visible run clock and the wave/XP/spawn clock.  Mini
    bosses are simultaneous wave events: wall time and visible run time advance,
    ordinary entities keep spawning, and XP keeps collecting.  Elite variants
    are spawned only as finite post-mini-boss packs and never as a permanent
    wave composition member.
    """
    simulation = model["simulation_model"]
    profile = simulation["heroes_and_profiles"]["profiles"][profile_name]
    dt = number(simulation["simulation_step_seconds"])
    main_duration = number(simulation["main_run_duration_seconds"])
    clock_policy = simulation["boss_clock_policy"]
    mini_clock_policy = simulation["mini_boss_clock_policy"]
    thresholds = xp_thresholds(model)
    rng = random.Random(seed)
    enemy_catalog = simulation["enemy_stats"]
    archetypes = stat_map(model)
    weights = simulation["wave_selection"]["composition_weights"]
    target_policy = simulation["target_policy"]
    combat = simulation["combat_math"]
    profile_stats = calculate_profile_stats(model, profile, hero_id)
    schedule = simulation["run_schedule"]
    synergy_path = synergy_path_for_hero(model, hero_id)
    main_schedule = sorted(main_checkpoints(model), key=lambda row: number(row["time_seconds"]))
    mini_schedule = sorted(mini_checkpoints(model), key=lambda row: number(row["time_seconds"]))
    state = {
        "hero_id": hero_id,
        "profile": profile_name,
        "level": 1,
        "xp": 0.0,
        "weapon_level": 1,
        "passive_rank": 0,
        "synergy_id": None,
        "claimed_synergy_ids": [],
        "claimed_synergy_count": 0,
        "synergy_path": synergy_path,
        "active_pair_index": 0,
        "active_pair_id": synergy_path[0],
        "pair_progress": {
            synergy_id: {"weapon_level": 1, "passive_rank": 0}
            for synergy_id in synergy_path
        },
        "fallback_damage_bonus": 0.0,
        "pending_xp_drops": [],
        "xp_pickup_budget": 0.0,
        "xp_dropped": 0,
        "xp_collected": 0,
        "final_boss_outcome_valid": True,
    }
    active: List[Dict[str, Any]] = []
    main_boss: Optional[Dict[str, Any]] = None
    mini_boss: Optional[Dict[str, Any]] = None
    next_main_index = 0
    next_mini_index = 0
    next_entity_id = 1
    spawn_accumulator = 0.0
    next_player_attack = 0.0
    player_hp = profile_stats["max_hp"]
    min_hp = player_hp
    total_incoming = 0.0
    peak_incoming_step = 0.0
    max_single_incoming_hit = 0.0
    death_time: Optional[float] = None
    death_run_clock: Optional[float] = None
    cap_samples: List[int] = []
    cap_seconds = 0.0
    suppressed_spawn_attempts = 0
    kills: List[Dict[str, Any]] = []
    boss_results: List[Dict[str, Any]] = []
    clock_events: List[Dict[str, Any]] = []
    level_times: Dict[str, float] = {}
    checkpoint_levels: Dict[str, int] = {}
    upgrade_events: List[Dict[str, Any]] = []
    chest_results: List[Dict[str, Any]] = []
    artifact_offer_results: List[Dict[str, Any]] = []
    elite_pack_offer_results: List[Dict[str, Any]] = []
    elite_pack_states: Dict[str, Dict[str, Any]] = {}
    chest_ledger: Dict[str, Dict[str, Any]] = {}
    reward_results: List[Dict[str, Any]] = []
    ledger: Dict[str, Dict[str, Any]] = {}
    run_id = f"{profile_name}:{hero_id}:{seed}"
    run_elapsed = 0.0
    wall_elapsed = 0.0
    loop_guard = 0
    xp_pickup = simulation["xp_pickup_model"]
    magnet_per_rank = number(xp_pickup["magnet_capacity_per_rank"])

    def add_xp(amount: int, run_clock: float) -> None:
        state["xp"] += amount
        while state["level"] <= len(thresholds) and state["xp"] >= thresholds[state["level"] - 1]:
            state["level"] += 1
            level_times[str(state["level"])] = round(run_clock, 3)
            upgrade = apply_level_upgrade(model, state)
            upgrade["time"] = round(run_clock, 3)
            upgrade_events.append(upgrade)

    def resolve_elite_pack_offer(event_id: str, run_clock: float) -> None:
        key = f"{run_id}:ELITE_PACK:{event_id}:ARTIFACT_OFFER"
        first = key not in elite_pack_states.get(event_id, {}).get("offer_ledger", {})
        event = elite_pack_states[event_id]
        event.setdefault("offer_ledger", {})
        if first:
            event["offer_ledger"][key] = {"event_id": event_id, "choice_count": 3}
        duplicate = key in event["offer_ledger"]
        elite_pack_offer_results.append({
            "event_id": event_id,
            "source_kind": "ELITE_PACK",
            "reward_type": "ARTIFACT_OFFER",
            "choice_count": integer(simulation["elite_variation_policy"]["reward"]["choice_count"]),
            "offer_created": first,
            "duplicate_attempt_idempotent": duplicate and not first,
            "time": round(run_clock, 3),
            "wallet_mutation": False,
        })

    def spawn_elite_pack(mini_row: Dict[str, Any], run_clock: float, wall_clock: float, band: Dict[str, Any]) -> None:
        nonlocal next_entity_id
        event_id = f"elite_pack_after_{mini_row['checkpoint_id']}"
        if event_id in elite_pack_states:
            return
        policy = simulation["elite_variation_policy"]
        pack_size = integer(policy["pack_size"])
        variant_ids = list(unwrap(policy["variant_ids"]))
        overlay_records = policy.get("variant_overrides", {}).get("records", {})
        # A variant overlays one ordinary family. Select the anchor and
        # variant as a linked pair so an ink-beetle overlay cannot silently be
        # applied to a moth or another family.
        band_weights = band.get("composition_weights", weights[band["wave_band_id"]])
        allowed_pairs = [
            (variant_id, str(overlay_records[variant_id]["base_enemy_id"]))
            for variant_id in variant_ids
            if variant_id in overlay_records and overlay_records[variant_id].get("base_enemy_id") in band_weights
        ]
        if not allowed_pairs:
            allowed_pairs = [
                (variant_id, str(overlay_records[variant_id]["base_enemy_id"]))
                for variant_id in variant_ids
                if variant_id in overlay_records
            ]
        pair_weights = {enemy_id: band_weights.get(enemy_id, 1.0) for _, enemy_id in allowed_pairs}
        anchor_enemy = weighted_choice(rng, pair_weights)
        matching_variants = [variant_id for variant_id, enemy_id in allowed_pairs if enemy_id == anchor_enemy]
        variant_id = matching_variants[rng.randrange(len(matching_variants))]
        pack_size = min(pack_size, max(0, integer(band["active_cap"]) - len(active)))
        elite_pack_states[event_id] = {
            "event_id": event_id,
            "source_checkpoint_id": mini_row["checkpoint_id"],
            "anchor_enemy_id": anchor_enemy,
            "variant_id": variant_id,
            "remaining": pack_size,
            "defeated": 0,
            "offer_ledger": {},
        }
        if pack_size == 0:
            resolve_elite_pack_offer(event_id, run_clock)
            return
        for member_index in range(pack_size):
            enemy_id = anchor_enemy if member_index == 0 else weighted_choice(rng, band.get("composition_weights", weights[band["wave_band_id"]]))
            entity = make_entity(
                model,
                enemy_id,
                wall_clock,
                band,
                next_entity_id,
                run_elapsed=run_clock,
                elite_variant=member_index == 0,
                variant_id=variant_id if member_index == 0 else None,
            )
            entity["elite_pack_event_id"] = event_id
            next_entity_id += 1
            active.append(entity)

    def register_kill(entity: Dict[str, Any], wall_clock: float, run_clock: float) -> None:
        spawn_ttk = wall_clock - entity["spawn_wall_time"]
        focused_start = entity.get("first_damage_time")
        focused_ttk = wall_clock - focused_start if focused_start is not None else spawn_ttk
        enemy_id = entity["enemy_id"]
        role = str(archetypes[enemy_id].get("role", ""))
        if entity.get("elite_variant"):
            kind = "elite_variant"
        else:
            kind = "elite" if "elite" in role else "ordinary"
        kills.append({
            "enemy_id": enemy_id,
            "kind": kind,
            "elite_pack_event_id": entity.get("elite_pack_event_id"),
            "variant_id": entity.get("variant_id"),
            "spawn_time": round(entity["spawn_time"], 3),
            "spawn_wall_time": round(entity["spawn_wall_time"], 3),
            "defeat_time_wall": round(wall_clock, 3),
            "defeat_time_run_clock": round(run_clock, 3),
            "spawn_to_kill_seconds": round(spawn_ttk, 3),
            "focused_ttk_seconds": round(focused_ttk, 3),
            "xp": entity["xp"],
        })
        state["pending_xp_drops"].append({
            "available_time": run_clock + number(xp_pickup["drop_delay_seconds"]),
            "value": entity["xp"],
        })
        state["xp_dropped"] += entity["xp"]
        event_id = entity.get("elite_pack_event_id")
        if event_id is not None and event_id in elite_pack_states:
            event = elite_pack_states[event_id]
            event["remaining"] -= 1
            event["defeated"] += 1
            if event["remaining"] == 0:
                resolve_elite_pack_offer(event_id, run_clock)
                resolve_elite_pack_offer(event_id, run_clock)

    def collect_xp(run_clock: float, band: Dict[str, Any]) -> None:
        if run_clock < number(xp_pickup["first_level_window_seconds"]):
            capacity = number(xp_pickup["first_level_capacity_per_second"])
        else:
            capacity = number(xp_pickup["capacity_per_second_by_wave"][band["wave_band_id"]])
        capacity_multiplier = 1.0 + number(profile["meta_ranks"]["magnet"]) * magnet_per_rank
        state["xp_pickup_budget"] += capacity * capacity_multiplier * dt
        ready = sorted(
            [drop for drop in state["pending_xp_drops"] if drop["available_time"] <= run_clock + 1e-9],
            key=lambda drop: (drop["available_time"], drop["value"]),
        )
        for drop in ready:
            if state["xp_pickup_budget"] + 1e-9 < drop["value"]:
                continue
            state["xp_pickup_budget"] -= drop["value"]
            state["pending_xp_drops"].remove(drop)
            state["xp_collected"] += drop["value"]
            add_xp(drop["value"], run_clock)

    def resolve_chest_once(checkpoint_id: str, elapsed: float, final: bool, encounter_kind: str) -> Dict[str, Any]:
        key = f"{run_id}:BOSS_CHEST:{checkpoint_id}:CHEST"
        if key in chest_ledger:
            return {
                "checkpoint_id": checkpoint_id,
                "encounter_kind": encounter_kind,
                "outcome": "IDEMPOTENT_NOOP",
                "idempotency_key": key,
                "duplicate": True,
                "time": elapsed,
            }
        result = resolve_chest(model, state, checkpoint_id, elapsed, final=final, encounter_kind=encounter_kind)
        result["idempotency_key"] = key
        result["duplicate"] = False
        chest_ledger[key] = result
        return result

    def resolve_encounter(encounter: Dict[str, Any], wall_clock: float, run_clock: float) -> None:
        checkpoint_id = str(encounter["checkpoint_id"])
        encounter_kind = str(encounter["encounter_kind"])
        final = bool(encounter.get("is_final", False))
        ttk = wall_clock - encounter["boss_start_wall_time"]
        if final:
            target_range = target_policy["final_boss_ttk_seconds"]
        elif encounter_kind == "MINI_BOSS":
            target_range = target_policy["mini_boss_ttk_seconds"]
        elif number(encounter["boss_start_run_clock"]) >= late_main_boss_start_seconds(model):
            target_range = target_policy["late_main_boss_ttk_seconds"]
        else:
            target_range = target_policy["first_slice_boss_ttk_seconds"]
        target_pass = number(target_range[0]) <= ttk <= number(target_range[1])
        within_window = (not final) or ttk <= number(simulation["post_final_boss_window_seconds"])
        status = "DEFEATED" if (not final or within_window) else "POST_RUN_WINDOW_EXCEEDED"
        if final and not within_window:
            state["final_boss_outcome_valid"] = False
        boss_results.append({
            "checkpoint_id": checkpoint_id,
            "boss_id": encounter["enemy_id"],
            "encounter_kind": encounter_kind,
            "status": status,
            "spawn_time": round(encounter["boss_start_run_clock"], 3),
            "encounter_start_wall_time": round(encounter["boss_start_wall_time"], 3),
            "defeat_time": round(wall_clock, 3),
            "defeat_time_wall_seconds": round(wall_clock, 3),
            "defeat_time_run_clock_seconds": round(run_clock, 3),
            "ttk_seconds": round(ttk, 3),
            "target_range": list(target_range),
            "target_pass": target_pass,
            "within_post_run_window": within_window,
            "clock_policy": "FREEZE_MAIN" if encounter_kind == "MAIN_BOSS" else "ADVANCE_MINI",
        })
        clock_events.append({
            "checkpoint_id": checkpoint_id,
            "encounter_kind": encounter_kind,
            "checkpoint_seconds": round(encounter["boss_start_run_clock"], 3),
            "run_clock_stop_seconds": round(encounter["boss_start_run_clock"], 3) if encounter_kind == "MAIN_BOSS" else None,
            "run_clock_resume_seconds": round(run_clock, 3) if encounter_kind == "MAIN_BOSS" and not final else None,
            "encounter_duration_seconds": round(ttk, 3),
            "run_clock_advanced_during_encounter": encounter_kind == "MINI_BOSS",
            "wave_xp_spawn_clock_advanced_during_encounter": encounter_kind == "MINI_BOSS",
            "status": status,
        })
        if not final or within_window:
            reward_row = boss_reward_map(model).get(checkpoint_id)
            if reward_row is None:
                raise KeyError(f"missing reward row for {checkpoint_id}")
            reward_results.append(resolve_reward(model, ledger, run_id, checkpoint_id, reward_amount(reward_row)))
            first_chest = resolve_chest_once(checkpoint_id, run_clock, final, encounter_kind)
            duplicate_chest = resolve_chest_once(checkpoint_id, run_clock, final, encounter_kind)
            first_chest["duplicate_attempt_idempotent"] = duplicate_chest.get("duplicate", False)
            chest_results.append(first_chest)
            if encounter_kind == "MINI_BOSS":
                spawn_elite_pack(
                    next(row for row in mini_schedule if str(row["checkpoint_id"]) == checkpoint_id),
                    run_clock,
                    wall_clock,
                    wave_state_at(model, min(run_clock, main_duration - dt)),
                )
        if final and within_window:
            first_clear = model["rewards"]["first_clear_bonus"]
            reward_results.append(resolve_reward(model, ledger, run_id, "run_result", reward_amount(first_clear)))
            artifact_model = simulation["artifact_offer_model"]
            artifact_offer_results.append({
                "offer_id": f"{run_id}:first_clear_artifact",
                "source_kind": "FIRST_CLEAR_REWARD",
                "source_id": "reward_first_clear_bonus",
                "choice_count": integer(artifact_model["choice_count"]),
                "status": "OFFER_CREATED_PENDING_SELECTION",
                "effect_status": artifact_model["effect_parameters_status"],
            })

    while True:
        loop_guard += 1
        if loop_guard > 300000:
            raise RuntimeError("30-minute simulation loop exceeded deterministic guard")
        if death_time is not None:
            break

        if main_boss is None and mini_boss is None:
            if next_main_index < len(main_schedule) and run_elapsed + 1e-9 >= number(main_schedule[next_main_index]["time_seconds"]):
                row = main_schedule[next_main_index]
                checkpoint_id = str(row["checkpoint_id"])
                main_boss = make_entity(
                    model,
                    str(row["boss_id"]),
                    wall_elapsed,
                    wave_at(model, min(run_elapsed, main_duration - dt)),
                    next_entity_id,
                    True,
                    checkpoint_id,
                    run_elapsed=run_elapsed,
                    encounter_kind="MAIN_BOSS",
                )
                next_entity_id += 1
                main_boss["checkpoint_id"] = checkpoint_id
                main_boss["boss_start_run_clock"] = run_elapsed
                main_boss["boss_start_wall_time"] = wall_elapsed
                main_boss["encounter_kind"] = "MAIN_BOSS"
                main_boss["is_final"] = bool(row.get("is_final", False))
                next_main_index += 1
            elif next_mini_index < len(mini_schedule) and run_elapsed + 1e-9 >= number(mini_schedule[next_mini_index]["time_seconds"]):
                row = mini_schedule[next_mini_index]
                checkpoint_id = str(row["checkpoint_id"])
                mini_boss = make_entity(
                    model,
                    str(row["boss_id"]),
                    wall_elapsed,
                    wave_state_at(model, run_elapsed),
                    next_entity_id,
                    True,
                    str(row["boss_id"]),
                    run_elapsed=run_elapsed,
                    encounter_kind="MINI_BOSS",
                )
                next_entity_id += 1
                mini_boss["checkpoint_id"] = checkpoint_id
                mini_boss["boss_start_run_clock"] = run_elapsed
                mini_boss["boss_start_wall_time"] = wall_elapsed
                mini_boss["encounter_kind"] = "MINI_BOSS"
                mini_boss["is_final"] = False
                next_mini_index += 1

        main_active = main_boss is not None
        if not main_active and run_elapsed < main_duration - 1e-9:
            band = wave_state_at(model, run_elapsed)
            collect_xp(run_elapsed, band)
            spawn_accumulator += number(band["spawn_budget_per_second"]) * dt * boss_interruption_factor(model, run_elapsed)
            while spawn_accumulator >= 1.0:
                spawn_accumulator -= 1.0
                cap = integer(band["active_cap"])
                if len(active) >= cap:
                    suppressed_spawn_attempts += 1
                    continue
                enemy_id = weighted_choice(rng, band.get("composition_weights", weights[band["wave_band_id"]]))
                entity = make_entity(model, enemy_id, wall_elapsed, band, next_entity_id, run_elapsed=run_elapsed)
                next_entity_id += 1
                active.append(entity)

        occupied = len(active)
        if not main_active:
            cap_samples.append(occupied)
            band_now = wave_state_at(model, min(run_elapsed, main_duration - dt))
            if occupied >= integer(band_now["active_cap"]):
                cap_seconds += dt

        incoming_this_step = 0.0
        candidates = sorted(active, key=lambda entity: (entity["contact_delay"], entity["entity_id"]))
        if main_boss is not None and main_boss["hp"] > 0.0:
            candidates.append(main_boss)
        if mini_boss is not None and mini_boss["hp"] > 0.0:
            candidates.append(mini_boss)
        attacker_limit = integer(combat["engaged_attacker_limit"])
        for entity in candidates[:attacker_limit]:
            if wall_elapsed + dt < entity["spawn_wall_time"] + entity["contact_delay"]:
                continue
            if wall_elapsed + 1e-9 < entity["next_attack"]:
                continue
            interval = entity["attack_interval"]
            while entity["next_attack"] <= wall_elapsed + 1e-9:
                entity["next_attack"] += interval
            if rng.random() > number(profile["hit_probability"]):
                continue
            damage_taken = entity["base_damage"] * entity["wave_damage"] * (1.0 - profile_stats["damage_reduction"])
            incoming_this_step += damage_taken
            max_single_incoming_hit = max(max_single_incoming_hit, damage_taken)
        player_hp -= incoming_this_step
        total_incoming += incoming_this_step
        peak_incoming_step = max(peak_incoming_step, incoming_this_step / dt)
        min_hp = min(min_hp, player_hp)
        if player_hp <= 0.0:
            player_hp = 0.0
            death_time = wall_elapsed
            death_run_clock = run_elapsed
            break

        damage = damage_components(model, profile, hero_id, state)
        if wall_elapsed + 1e-9 >= next_player_attack:
            while next_player_attack <= wall_elapsed + 1e-9:
                next_player_attack += damage["attack_interval"]
            total_damage = damage["total_attack_damage"]
            focused = main_boss if main_boss is not None else mini_boss
            boss_damage = 0.0
            if focused is not None and focused["hp"] > 0.0:
                boss_damage = total_damage * number(combat["boss_focus_fraction"])
                focused["hp"] -= boss_damage
                focused["damage_taken"] += boss_damage
                if focused["hp"] <= 0.0:
                    resolve_encounter(focused, wall_elapsed, run_elapsed)
                    if focused is main_boss:
                        main_boss = None
                    else:
                        mini_boss = None
            remaining = total_damage - boss_damage
            targets = sorted(active, key=lambda entity: (entity["spawn_wall_time"], entity["entity_id"]))[: damage["targets_per_attack"]]
            if targets:
                per_target = remaining / len(targets)
                for entity in list(targets):
                    hit_damage = per_target
                    if entity["enemy_id"] == "enemy_bell_crab":
                        crab = enemy_catalog[entity["enemy_id"]]
                        if rng.random() < number(crab["rear_hit_probability"]):
                            hit_damage *= number(crab["rear_weakness_multiplier"])
                    entity["hp"] -= hit_damage
                    entity["damage_taken"] += hit_damage
                    if entity.get("first_damage_time") is None:
                        entity["first_damage_time"] = wall_elapsed

        survivors = []
        for entity in active:
            if entity["hp"] <= 0.0:
                register_kill(entity, wall_elapsed, run_elapsed)
            else:
                survivors.append(entity)
        active = survivors

        for checkpoint_time in progression_checkpoint_seconds(model):
            key = f"{int(checkpoint_time)}"
            if run_elapsed + 1e-9 >= checkpoint_time and key not in checkpoint_levels:
                checkpoint_levels[key] = state["level"]

        if main_boss is None and next_main_index >= len(main_schedule) and run_elapsed >= main_duration - 1e-9:
            break

        wall_elapsed = round(wall_elapsed + dt, 9)
        if main_boss is None and run_elapsed < main_duration - 1e-9:
            run_elapsed = round(min(main_duration, run_elapsed + dt), 9)

    failed_encounter = main_boss if main_boss is not None else mini_boss
    if failed_encounter is not None and death_time is not None:
        encounter_duration = wall_elapsed - failed_encounter["boss_start_wall_time"]
        kind = str(failed_encounter["encounter_kind"])
        final = bool(failed_encounter.get("is_final", False))
        target_range = target_policy["final_boss_ttk_seconds"] if final else target_policy["mini_boss_ttk_seconds"] if kind == "MINI_BOSS" else target_policy["late_main_boss_ttk_seconds"] if failed_encounter["boss_start_run_clock"] >= late_main_boss_start_seconds(model) else target_policy["first_slice_boss_ttk_seconds"]
        boss_results.append({
            "checkpoint_id": failed_encounter["checkpoint_id"],
            "boss_id": failed_encounter["enemy_id"],
            "encounter_kind": kind,
            "status": "RUN_FAILED_DURING_ENCOUNTER",
            "spawn_time": round(failed_encounter["boss_start_run_clock"], 3),
            "encounter_start_wall_time": round(failed_encounter["boss_start_wall_time"], 3),
            "defeat_time": None,
            "defeat_time_wall_seconds": None,
            "defeat_time_run_clock_seconds": None,
            "ttk_seconds": None,
            "target_range": list(target_range),
            "target_pass": False,
            "within_post_run_window": False,
        })
        clock_events.append({
            "checkpoint_id": failed_encounter["checkpoint_id"],
            "encounter_kind": kind,
            "checkpoint_seconds": round(failed_encounter["boss_start_run_clock"], 3),
            "run_clock_stop_seconds": round(failed_encounter["boss_start_run_clock"], 3) if kind == "MAIN_BOSS" else None,
            "run_clock_resume_seconds": None,
            "encounter_duration_seconds": round(encounter_duration, 3),
            "run_clock_advanced_during_encounter": kind == "MINI_BOSS",
            "wave_xp_spawn_clock_advanced_during_encounter": kind == "MINI_BOSS",
            "status": "RUN_FAILED_DURING_ENCOUNTER",
        })

    ordinary_ttks = [row["focused_ttk_seconds"] for row in kills if row["kind"] == "ordinary"]
    elite_ttks = [row["focused_ttk_seconds"] for row in kills if row["kind"] in ("elite", "elite_variant")]
    elite_variant_ttks = [row["focused_ttk_seconds"] for row in kills if row["kind"] == "elite_variant"]
    elite_variant_ids_used = sorted({row.get("variant_id") for row in kills if row["kind"] == "elite_variant" and row.get("variant_id")})
    ttk_by_enemy: Dict[str, List[float]] = {}
    for row in kills:
        ttk_by_enemy.setdefault(row["enemy_id"], []).append(row["focused_ttk_seconds"])
    cap_stats = {
        "max_occupancy": max(cap_samples) if cap_samples else 0,
        "mean_occupancy": round(statistics.mean(cap_samples), 3) if cap_samples else 0.0,
        "p95_occupancy": percentile([float(value) for value in cap_samples], 0.95),
        "cap_seconds": round(cap_seconds, 3),
        "occupancy_fraction_of_sample": round(statistics.mean(cap_samples) / max(1, max(integer(b["active_cap"]) for b in model["wave_bands"])), 6) if cap_samples else 0.0,
        "suppressed_spawn_attempts": suppressed_spawn_attempts,
        "sample_clock": "RUN_CLOCK_EXCLUDING_MAIN_BOSS_ENCOUNTER_PAUSE",
        "sample_seconds": round(sum(dt for _ in cap_samples), 3),
    }
    reward_balance = sum_ledger(ledger)
    survived = death_time is None
    run_completed = survived and state["final_boss_outcome_valid"] and main_boss is None and mini_boss is None and next_main_index >= len(main_schedule) and next_mini_index >= len(mini_schedule) and run_elapsed >= main_duration - 1e-9
    return {
        "status": "SIMULATED_MODEL_ONLY",
        "source_revision": model["source_of_truth"]["source_revision"],
        "architecture_revision": model["architecture_contract"]["source_revision"],
        "seed": seed,
        "profile": profile_name,
        "hero_id": hero_id,
        "model_inputs": {
            "profile_meta_ranks": profile["meta_ranks"],
            "profile_stats": {key: round(value, 6) for key, value in profile_stats.items()},
            "build_rules": {
                "weapon_slots": integer(simulation["build_catalog"]["weapon_slot_limit"]),
                "passive_slots": integer(simulation["build_catalog"]["passive_slot_limit"]),
                "weapon_max_level": integer(simulation["build_catalog"]["weapon_max_level"]),
                "passive_max_rank": integer(simulation["build_catalog"]["passive_max_rank"]),
                "max_synergy_claims_per_run": integer(simulation["build_catalog"]["max_synergy_claims_per_run"]),
            },
            "ordinary_roster_size": len(unwrap(simulation["content_roster"]["ordinary_enemy_ids"])),
            "elite_variant_proposal_count": len(unwrap(simulation["content_roster"]["elite_variant_ids"])),
            "elite_variant_registered_cap": integer(simulation["content_roster"]["registered_variant_cap"]),
            "proposed_build": {
                "weapon_id": model["simulation_model"]["heroes_and_profiles"]["heroes"][hero_id]["starting_weapon_id"],
                "passive_id": model["simulation_model"]["heroes_and_profiles"]["heroes"][hero_id]["starting_passive_id"],
            },
        },
        "progression": {
            "final_level_at_30_minutes": state["level"],
            "final_xp_at_30_minutes": round(state["xp"], 3),
            "levels_at_checkpoints": {
                str(int(checkpoint_time)): checkpoint_levels.get(str(int(checkpoint_time)))
                for checkpoint_time in progression_checkpoint_seconds(model)
            },
            "xp_at_30_minutes": round(state["xp"], 3),
            "xp_dropped": state["xp_dropped"],
            "xp_collected": state["xp_collected"],
            "xp_pending_at_end": sum(drop["value"] for drop in state["pending_xp_drops"]),
            "level_up_times": level_times,
            "upgrade_events": upgrade_events,
            "synergy_path": list(state["synergy_path"]),
            "pair_progress_at_30_minutes": {
                pair_id: dict(pair)
                for pair_id, pair in state["pair_progress"].items()
            },
            "xp_formula_status": "CANON_FORMULA_SIMULATED_WITH_PROPOSED_30M_PICKUP_CAPACITY",
        },
        "combat": {
            "ordinary_kills": len(ordinary_ttks),
            "elite_kills": len(elite_ttks),
            "elite_variant_kills": len(elite_variant_ttks),
            "elite_variant_ids_used": elite_variant_ids_used,
            "ordinary_ttk_seconds": {"mean": percentile(ordinary_ttks, 0.5), "p95": percentile(ordinary_ttks, 0.95), "target": list(target_policy["ordinary_ttk_seconds"])},
            "elite_ttk_seconds": {"mean": percentile(elite_ttks, 0.5), "p95": percentile(elite_ttks, 0.95), "target": list(target_policy["elite_ttk_seconds"])},
            "elite_variant_ttk_seconds": {"mean": percentile(elite_variant_ttks, 0.5), "p95": percentile(elite_variant_ttks, 0.95), "target": list(target_policy["elite_variant_ttk_seconds"])},
            "ttk_by_enemy_seconds": {enemy_id: {"median": percentile(values, 0.5), "p95": percentile(values, 0.95), "samples": len(values)} for enemy_id, values in sorted(ttk_by_enemy.items())},
            "boss_results": boss_results,
            "synergy_id": state["synergy_id"],
            "synergy_ids": list(state["claimed_synergy_ids"]),
            "claimed_synergy_count": state["claimed_synergy_count"],
            "fallback_damage_bonus": round(state["fallback_damage_bonus"], 6),
            "chest_results": chest_results,
            "artifact_offer_results": artifact_offer_results,
            "elite_pack_offer_results": elite_pack_offer_results,
        },
        "risk": {
            "survived_main_run": survived,
            "death_time_seconds": death_time,
            "death_time_wall_seconds": death_time,
            "death_time_run_clock_seconds": death_run_clock,
            "min_hp": round(min_hp, 3),
            "max_hp": round(profile_stats["max_hp"], 3),
            "total_incoming_damage": round(total_incoming, 3),
            "peak_incoming_dps": round(peak_incoming_step, 3),
            "max_single_incoming_hit": round(max_single_incoming_hit, 3),
            "max_single_hit_fraction_of_base_hp": round(max_single_incoming_hit / number(model["hero_stats"]["base"]["hp"]), 6),
            "telegraph_bound_target": number(target_policy["incoming_untelegraphed_hit_fraction_of_base_hp"]),
            "conservative_single_hit_bound_pass": max_single_incoming_hit / number(model["hero_stats"]["base"]["hp"]) <= number(target_policy["incoming_untelegraphed_hit_fraction_of_base_hp"]),
        },
        "waves": {
            "active_cap": cap_stats,
            "boss_encounter_wall_seconds": round(sum(event["encounter_duration_seconds"] for event in clock_events), 3),
            "main_boss_encounter_wall_seconds": round(sum(event["encounter_duration_seconds"] for event in clock_events if event["encounter_kind"] == "MAIN_BOSS"), 3),
            "mini_boss_encounter_wall_seconds": round(sum(event["encounter_duration_seconds"] for event in clock_events if event["encounter_kind"] == "MINI_BOSS"), 3),
            "visible_run_clock_final_seconds": round(run_elapsed, 3),
            "wall_clock_final_seconds": round(wall_elapsed, 3),
            "boss_clock_events": clock_events,
            "boss_wave_ramp": {"status": simulation["boss_wave_ramp"]["status"], "applies_to": simulation["boss_wave_ramp"]["applies_to"], "phase_order": simulation["boss_wave_ramp"]["phase_order"], "samples": wave_ramp_samples(model)},
            "boss_interruption_checkpoints": [
                {"time_seconds": number(row["time_seconds"]), "factor_at_checkpoint": round(boss_interruption_factor(model, number(row["time_seconds"])), 6), "factor_at_plus_8": round(boss_interruption_factor(model, number(row["time_seconds"]) + number(simulation["boss_interruption"]["suppression_seconds"])), 6)}
                for row in main_schedule
            ],
            "mini_boss_clock_policy": mini_clock_policy,
        },
        "rewards": {
            "ledger_balance": reward_balance,
            "reward_events": reward_results,
            "scenario_audit": reward_scenario_audit(model),
            "idempotency_pass": all(not attempt.get("duplicate_accepted", False) for event in reward_results for attempt in event.get("attempts", [])),
            "chest_idempotency_pass": all(event.get("duplicate_attempt_idempotent", True) for event in chest_results),
            "final_boss_chest_offer_created": any(
                checkpoint_is_final(model, str(event.get("checkpoint_id", "")))
                and event.get("outcome") not in ("NO_CHEST", "IDEMPOTENT_NOOP")
                for event in chest_results
            ),
            "first_clear_artifact_offer_created": bool(artifact_offer_results),
            "elite_pack_offer_count": len(elite_pack_offer_results),
            "elite_pack_offer_idempotency_pass": all(
                event.get("offer_created", False) or event.get("duplicate_attempt_idempotent", False)
                for event in elite_pack_offer_results
            ),
            "artifact_offer_choice_count": integer(simulation["artifact_offer_model"]["choice_count"]) if artifact_offer_results else 0,
        },
        "run_outcome": {
            "completed_model_run": run_completed,
            "main_run_clock_duration_seconds": round(main_duration, 3),
            "visible_run_clock_final_seconds": round(run_elapsed, 3),
            "wall_clock_duration_seconds": round(wall_elapsed, 3),
            "main_boss_clock_pause_seconds": round(sum(event["encounter_duration_seconds"] for event in clock_events if event["encounter_kind"] == "MAIN_BOSS"), 3),
            "mini_boss_clock_advance_seconds": round(sum(event["encounter_duration_seconds"] for event in clock_events if event["encounter_kind"] == "MINI_BOSS"), 3),
        },
        "runtime_boundary": {
            "godot_runtime_executed": False,
            "collision_and_telegraph_evidence": "NOT_IMPLEMENTED",
            "android_fps_evidence": "BLOCKED",
            "model_status": "SIMULATED_MODEL_ONLY_WITH_PROPOSED_30M_INPUTS",
        },
        "clock_policy": {
            "main": clock_policy,
            "mini": mini_clock_policy,
            "main_bosses_freeze_visible_clock": True,
            "mini_bosses_advance_visible_clock": True,
            "wave_xp_spawn_clock_advances_during_main_boss": False,
            "wave_xp_spawn_clock_advances_during_mini_boss": True,
        },
        "provenance_boundary": {
            "status": "PROPOSED_MODEL_ONLY",
            "runtime_verified": False,
            "architecture_sync": "BLOCKED",
            "content_registry_sync": "BLOCKED",
        },
    }


def run_all(model: Dict[str, Any], seeds: List[int]) -> Dict[str, Any]:
    profiles = list(model["simulation_model"]["heroes_and_profiles"]["profiles"].keys())
    heroes = list(model["simulation_model"]["heroes_and_profiles"]["heroes"].keys())
    runs = []
    for seed in seeds:
        for profile in profiles:
            for hero in heroes:
                runs.append(simulate(model, profile, hero, seed))
    return {
        "status": "SIMULATED_MODEL_ONLY",
        "source_revision": model["source_of_truth"]["source_revision"],
        "architecture_revision": model["architecture_contract"]["source_revision"],
        "seeds": seeds,
        "run_count": len(runs),
        "content_balance_audit": content_balance_audit(model),
        "runs": runs,
    }


def assert_result_shape(model: Dict[str, Any], result: Dict[str, Any]) -> None:
    if result["status"] != "SIMULATED_MODEL_ONLY":
        raise AssertionError("unexpected simulation status")
    coverage = result.get("content_balance_audit", {}).get("coverage", {})
    expected_coverage = {
        "weapons": 10,
        "passives": 10,
        "synergies": 10,
        "artifacts": 10,
        "ordinary_enemies": 10,
        "elite_variants": 10,
        "main_bosses": 6,
        "mini_bosses": 5,
    }
    if coverage != expected_coverage:
        raise AssertionError(f"full content audit coverage drifted: {coverage}")
    if not all(row["guard_pass"] for row in result["content_balance_audit"]["synergies"].values()):
        raise AssertionError("one or more content synergies exceeds the damage-share guard")
    expected_duration = number(model["simulation_model"]["main_run_duration_seconds"])
    expected_bosses = len(main_checkpoints(model))
    expected_minibosses = len(mini_checkpoints(model))
    target_policy = model["simulation_model"]["target_policy"]
    target_final_level = integer(target_policy["target_final_level"])
    acceptable_final_level_floor = integer(target_policy["acceptable_final_level_floor"])
    minimum_synergy_claims = integer(target_policy["minimum_synergy_claims"])
    allowed_variant_ids = set(unwrap(model["simulation_model"]["elite_variation_policy"]["variant_ids"]))
    for run in result["runs"]:
        if run["runtime_boundary"]["godot_runtime_executed"]:
            raise AssertionError("model simulator must not claim Godot runtime execution")
        if run["waves"]["active_cap"]["max_occupancy"] < 0:
            raise AssertionError("negative occupancy")
        if run["progression"]["final_level_at_30_minutes"] < acceptable_final_level_floor:
            raise AssertionError(
                f"30-minute acceptable level floor missed: {run['progression']['final_level_at_30_minutes']} < {acceptable_final_level_floor}"
            )
        if run["combat"]["claimed_synergy_count"] < minimum_synergy_claims:
            raise AssertionError(
                f"synergy target missed: {run['combat']['claimed_synergy_count']} < {minimum_synergy_claims}"
            )
        if len(set(run["combat"].get("synergy_ids", []))) < minimum_synergy_claims:
            raise AssertionError("synergy target counted duplicate IDs")
        if run["progression"]["levels_at_checkpoints"]["120"] is None and run["risk"]["survived_main_run"]:
            raise AssertionError("surviving run must report the two-minute level")
        for boss in run["combat"]["boss_results"]:
            if boss.get("spawn_time", expected_duration) < 0:
                raise AssertionError("invalid boss spawn time")
        if not run["rewards"]["idempotency_pass"]:
            raise AssertionError("duplicate reward grant accepted")
        if not set(run["combat"].get("elite_variant_ids_used", [])).issubset(allowed_variant_ids):
            raise AssertionError("simulator emitted an unregistered elite variant ID")
        if run["clock_policy"]["main_bosses_freeze_visible_clock"] is not True:
            raise AssertionError("main-boss freeze policy drifted")
        if run["clock_policy"]["mini_bosses_advance_visible_clock"] is not True:
            raise AssertionError("mini-boss advance policy drifted")
        if run["clock_policy"]["wave_xp_spawn_clock_advances_during_main_boss"] is not False:
            raise AssertionError("wave/XP/spawn clock advanced during a main boss")
        if run["clock_policy"]["wave_xp_spawn_clock_advances_during_mini_boss"] is not True:
            raise AssertionError("wave/XP/spawn clock stopped during a mini-boss")
        if run["risk"]["survived_main_run"]:
            main_events = [event for event in run["waves"]["boss_clock_events"] if event["encounter_kind"] == "MAIN_BOSS"]
            mini_events = [event for event in run["waves"]["boss_clock_events"] if event["encounter_kind"] == "MINI_BOSS"]
            if len(main_events) != expected_bosses:
                raise AssertionError("surviving run must resolve every main boss checkpoint")
            if len(mini_events) != expected_minibosses:
                raise AssertionError("surviving run must resolve every mini-boss checkpoint")
        for event in run["waves"]["boss_clock_events"]:
            if event["encounter_kind"] == "MAIN_BOSS" and event["run_clock_advanced_during_encounter"]:
                raise AssertionError("visible run clock advanced during a main boss")
            if event["encounter_kind"] == "MAIN_BOSS" and event["wave_xp_spawn_clock_advanced_during_encounter"]:
                raise AssertionError("wave/XP/spawn clock advanced during a main boss")
            if event["encounter_kind"] == "MINI_BOSS" and not event["run_clock_advanced_during_encounter"]:
                raise AssertionError("visible run clock stopped during a mini-boss")
        ramp_samples = run["waves"]["boss_wave_ramp"]["samples"]
        cycle_ids = sorted({sample["cycle_id"] for sample in ramp_samples})
        if len(cycle_ids) != expected_bosses - 1:
            raise AssertionError("wave ramp must cover every non-final boss cycle")
        for cycle_id in cycle_ids:
            samples = [sample for sample in ramp_samples if sample["cycle_id"] == cycle_id]
            density = [sample["density_factor_of_peak"] for sample in samples]
            if any(later + 1e-9 < earlier for earlier, later in zip(density, density[1:])):
                raise AssertionError(f"wave density is not monotonic for {cycle_id}")
            if samples[-1]["phase"] != "SIEGE":
                raise AssertionError(f"wave ramp has no siege phase for {cycle_id}")
            if abs(samples[-1]["density_factor_of_peak"] - 1.0) > 1e-6:
                raise AssertionError(f"siege is not at peak density for {cycle_id}")
    final_levels = [run["progression"]["final_level_at_30_minutes"] for run in result["runs"]]
    if max(final_levels) < target_final_level:
        raise AssertionError(f"no model run reached target level {target_final_level}")
    if statistics.mean(final_levels) < target_final_level:
        raise AssertionError(f"mean model level is below target {target_final_level}: {statistics.mean(final_levels):.3f}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=str(Path(__file__).with_name("BALANCE_MODEL.json")))
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    model = load_model(Path(args.model))
    configured_seeds = [int(seed) for seed in unwrap(model["simulation_model"]["default_seed_set"])]
    seeds = [args.seed] if args.seed is not None else configured_seeds
    result = run_all(model, seeds)
    assert_result_shape(model, result)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"status={result['status']}")
        print(f"source_revision={result['source_revision']}")
        print(f"run_count={result['run_count']}")
        print("shape_check=PASS")


if __name__ == "__main__":
    main()
