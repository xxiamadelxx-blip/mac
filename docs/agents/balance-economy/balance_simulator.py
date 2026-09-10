#!/usr/bin/env python3
"""Data-driven deterministic 20-minute balance model.

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
    for key in ("main_run_duration_seconds", "simulation_step_seconds", "default_seed_set"):
        if key not in simulation:
            raise ValueError(f"simulation_model missing {key}")
    if model["architecture_contract"]["final_boss_policy"] != "CHECKPOINT_REWARD_THEN_RUN_VICTORY_NO_CHEST":
        raise ValueError("final-boss chest policy drifted from the live architecture contract")
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


def wave_at(model: Dict[str, Any], elapsed: float) -> Dict[str, Any]:
    bands = model["wave_bands"]
    for band in bands:
        start = number(band["start_seconds"])
        end = number(band["end_seconds"])
        if start <= elapsed < end:
            return band
    return bands[-1]


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
    for checkpoint in model["boss_checkpoints"]:
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
    elapsed: float,
    band: Dict[str, Any],
    entity_id: int,
    boss: bool = False,
    boss_key: Optional[str] = None,
) -> Dict[str, Any]:
    simulation = model["simulation_model"]
    if boss:
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
    return {
        "entity_id": entity_id,
        "enemy_id": enemy_id,
        "boss": boss,
        "boss_key": boss_key,
        "spawn_time": elapsed,
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
        "next_attack": elapsed + attack_interval,
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
    catalog = model["architecture_contract"]
    weapon_max = integer(catalog["weapon_max_level"])
    passive_max = integer(catalog["passive_max_rank"])
    if state["weapon_level"] < weapon_max:
        state["weapon_level"] += 1
        return {"type": "weapon_level", "level": state["weapon_level"]}
    if state["passive_rank"] < passive_max:
        state["passive_rank"] += 1
        return {"type": "passive_rank", "rank": state["passive_rank"]}
    return {"type": "no_slot_available", "level": state["level"]}


def damage_components(model: Dict[str, Any], profile: Dict[str, Any], hero_id: str, state: Dict[str, Any]) -> Dict[str, float]:
    catalog = model["simulation_model"]["build_catalog"]
    hero = model["simulation_model"]["heroes_and_profiles"]["heroes"][hero_id]
    weapon = catalog["weapons"][hero["starting_weapon_id"]]
    passive = catalog["passives"][hero["starting_passive_id"]]
    combat = model["simulation_model"]["combat_math"]
    weapon_level_bonus = number(combat["weapon_level_damage_per_level"])
    weapon_level_multiplier = 1.0 + weapon_level_bonus * (state["weapon_level"] - 1)
    passive_multiplier = 1.0
    passive_multiplier += number(passive["damage_per_rank"]) * state["passive_rank"]
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
    synergy_id = state.get("synergy_id")
    if synergy_id is not None:
        synergy = catalog["synergies"][synergy_id]
        proposed_synergy = base_attack_damage * number(synergy["damage_multiplier"])
        share_cap = number(model["simulation_model"]["target_policy"]["synergy_damage_share_max"])
        synergy_damage = min(proposed_synergy, base_attack_damage * share_cap / (1.0 - share_cap))
    return {
        "base_attack_damage": base_attack_damage,
        "synergy_attack_damage": synergy_damage,
        "total_attack_damage": base_attack_damage + synergy_damage,
        "targets_per_attack": targets,
        "attack_interval": number(weapon["attack_interval_seconds"]) * number(profile["cooldown_multiplier"]),
    }


def resolve_chest(model: Dict[str, Any], state: Dict[str, Any], checkpoint_id: str, elapsed: float) -> Dict[str, Any]:
    catalog = model["simulation_model"]["build_catalog"]
    if checkpoint_id == "boss_final_20":
        return {"checkpoint_id": checkpoint_id, "outcome": "NO_CHEST", "time": elapsed, "status": "CANON_ARCHITECTURE"}
    hero = model["simulation_model"]["heroes_and_profiles"]["heroes"][state["hero_id"]]
    synergy_id = catalog["weapons"][hero["starting_weapon_id"]]["synergy_id"] if "synergy_id" in catalog["weapons"][hero["starting_weapon_id"]] else None
    if synergy_id is None:
        return {"checkpoint_id": checkpoint_id, "outcome": "FALLBACK_REQUIRED", "time": elapsed, "status": "PROPOSED"}
    synergy = catalog["synergies"].get(synergy_id)
    eligible = (
        synergy is not None
        and state["weapon_level"] >= integer(synergy["requires_weapon_level"])
        and state["passive_rank"] >= integer(synergy["requires_passive_rank"])
        and not state.get("synergy_id")
    )
    if eligible:
        state["synergy_id"] = synergy_id
        outcome = "SYNERGY_GRANTED"
    else:
        fallback = catalog["offer_model"]["fallback"]
        state["fallback_damage_bonus"] += number(fallback["damage_multiplier_additive"])
        outcome = "FALLBACK_UPGRADE"
    return {"checkpoint_id": checkpoint_id, "outcome": outcome, "time": elapsed, "synergy_id": synergy_id}


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


def simulate(model: Dict[str, Any], profile_name: str, hero_id: str, seed: int) -> Dict[str, Any]:
    simulation = model["simulation_model"]
    profile = simulation["heroes_and_profiles"]["profiles"][profile_name]
    dt = number(simulation["simulation_step_seconds"])
    main_duration = number(simulation["main_run_duration_seconds"])
    thresholds = xp_thresholds(model)
    rng = random.Random(seed)
    enemy_catalog = simulation["enemy_stats"]
    archetypes = stat_map(model)
    weights = simulation["wave_selection"]["composition_weights"]
    target_policy = simulation["target_policy"]
    combat = simulation["combat_math"]
    profile_stats = calculate_profile_stats(model, profile, hero_id)
    state = {
        "hero_id": hero_id,
        "profile": profile_name,
        "level": 1,
        "xp": 0.0,
        "weapon_level": 1,
        "passive_rank": 0,
        "synergy_id": None,
        "fallback_damage_bonus": 0.0,
        "pending_xp_drops": [],
        "xp_pickup_budget": 0.0,
        "xp_dropped": 0,
        "xp_collected": 0,
    }
    active: List[Dict[str, Any]] = []
    boss: Optional[Dict[str, Any]] = None
    next_entity_id = 1
    spawn_accumulator = 0.0
    next_player_attack = 0.0
    player_hp = profile_stats["max_hp"]
    min_hp = player_hp
    total_incoming = 0.0
    peak_incoming_step = 0.0
    max_single_incoming_hit = 0.0
    death_time: Optional[float] = None
    cap_samples: List[int] = []
    cap_seconds = 0.0
    suppressed_spawn_attempts = 0
    kills: List[Dict[str, Any]] = []
    boss_results: List[Dict[str, Any]] = []
    level_times: Dict[str, float] = {}
    checkpoint_levels: Dict[str, int] = {}
    upgrade_events: List[Dict[str, Any]] = []
    chest_results: List[Dict[str, Any]] = []
    artifact_offer_results: List[Dict[str, Any]] = []
    reward_results: List[Dict[str, Any]] = []
    ledger: Dict[str, Dict[str, Any]] = {}
    run_id = f"{profile_name}:{hero_id}:{seed}"
    last_t = 0.0
    checkpoints = {number(row["time_seconds"]): row["checkpoint_id"] for row in model["boss_checkpoints"]}
    xp_pickup = simulation["xp_pickup_model"]
    magnet_per_rank = number(xp_pickup["magnet_capacity_per_rank"])

    def add_xp(amount: int, elapsed: float) -> None:
        state["xp"] += amount
        while state["level"] <= len(thresholds) and state["xp"] >= thresholds[state["level"] - 1]:
            state["level"] += 1
            level_times[str(state["level"])] = elapsed
            upgrade = apply_level_upgrade(model, state)
            upgrade["time"] = elapsed
            upgrade_events.append(upgrade)

    def register_kill(entity: Dict[str, Any], elapsed: float) -> None:
        spawn_ttk = elapsed - entity["spawn_time"]
        focused_start = entity.get("first_damage_time")
        focused_ttk = elapsed - focused_start if focused_start is not None else spawn_ttk
        enemy_id = entity["enemy_id"]
        role = str(archetypes[enemy_id].get("role", ""))
        kind = "elite" if "elite" in role else "ordinary"
        kills.append({
            "enemy_id": enemy_id,
            "kind": kind,
            "spawn_to_kill_seconds": round(spawn_ttk, 3),
            "focused_ttk_seconds": round(focused_ttk, 3),
            "xp": entity["xp"],
        })
        state["pending_xp_drops"].append({
            "available_time": elapsed + number(xp_pickup["drop_delay_seconds"]),
            "value": entity["xp"],
        })
        state["xp_dropped"] += entity["xp"]

    def collect_xp(elapsed: float, band: Dict[str, Any]) -> None:
        if elapsed < number(xp_pickup["first_level_window_seconds"]):
            capacity = number(xp_pickup["first_level_capacity_per_second"])
        else:
            capacity = number(xp_pickup["capacity_per_second_by_wave"][band["wave_band_id"]])
        capacity_multiplier = 1.0 + number(profile["meta_ranks"]["magnet"]) * magnet_per_rank
        state["xp_pickup_budget"] += capacity * capacity_multiplier * dt
        ready = sorted(
            [drop for drop in state["pending_xp_drops"] if drop["available_time"] <= elapsed + 1e-9],
            key=lambda drop: (drop["available_time"], drop["value"]),
        )
        for drop in ready:
            if state["xp_pickup_budget"] + 1e-9 < drop["value"]:
                continue
            state["xp_pickup_budget"] -= drop["value"]
            state["pending_xp_drops"].remove(drop)
            state["xp_collected"] += drop["value"]
            add_xp(drop["value"], elapsed)

    total_steps = int(round(main_duration / dt))
    for step in range(total_steps + 1):
        elapsed = round(step * dt, 9)
        last_t = elapsed
        if elapsed in checkpoints:
            checkpoint_id = checkpoints[elapsed]
            boss_key = checkpoint_id
            if boss is not None:
                boss_results.append({"checkpoint_id": checkpoint_id, "status": "OVERLAP_BLOCKED", "previous_boss_alive": True})
            boss = make_entity(model, simulation["boss_stats"][boss_key]["boss_id"], elapsed, wave_at(model, min(elapsed, main_duration - dt)), next_entity_id, True, boss_key)
            next_entity_id += 1
            boss["checkpoint_id"] = checkpoint_id
            boss["boss_start_time"] = elapsed
        if elapsed < main_duration and death_time is None:
            band = wave_at(model, elapsed)
            collect_xp(elapsed, band)
            spawn_accumulator += number(band["spawn_budget_per_second"]) * dt * boss_interruption_factor(model, elapsed)
            while spawn_accumulator >= 1.0:
                spawn_accumulator -= 1.0
                cap = integer(band["active_cap"])
                if len(active) >= cap:
                    suppressed_spawn_attempts += 1
                    continue
                enemy_id = weighted_choice(rng, weights[band["wave_band_id"]])
                entity = make_entity(model, enemy_id, elapsed, band, next_entity_id)
                next_entity_id += 1
                active.append(entity)
        occupied = len(active)
        cap_samples.append(occupied)
        band_now = wave_at(model, min(elapsed, main_duration - dt))
        if occupied >= integer(band_now["active_cap"]):
            cap_seconds += dt

        if death_time is not None:
            continue

        # Incoming attacks are deterministic Bernoulli events driven by the
        # profile's explicit landed-hit probability.
        incoming_this_step = 0.0
        candidates = sorted(active, key=lambda entity: (entity["contact_delay"], entity["entity_id"]))
        if boss is not None and boss["hp"] > 0.0:
            candidates.append(boss)
        attacker_limit = integer(combat["engaged_attacker_limit"])
        for entity in candidates[:attacker_limit]:
            if elapsed + dt < entity["spawn_time"] + entity["contact_delay"]:
                continue
            if elapsed + 1e-9 < entity["next_attack"]:
                continue
            interval = entity["attack_interval"]
            while entity["next_attack"] <= elapsed + 1e-9:
                entity["next_attack"] += interval
            if rng.random() > number(profile["hit_probability"]):
                continue
            damage = entity["base_damage"] * entity["wave_damage"] * (1.0 - profile_stats["damage_reduction"])
            incoming_this_step += damage
            max_single_incoming_hit = max(max_single_incoming_hit, damage)
        player_hp -= incoming_this_step
        total_incoming += incoming_this_step
        peak_incoming_step = max(peak_incoming_step, incoming_this_step / dt)
        min_hp = min(min_hp, player_hp)
        if player_hp <= 0.0:
            player_hp = 0.0
            death_time = elapsed
            continue

        # Outgoing attacks are continuous in model time but emitted at the
        # weapon cadence from the model.  Boss focus and synergy share are
        # explicit inputs in BALANCE_MODEL.json.
        damage = damage_components(model, profile, hero_id, state)
        if elapsed + 1e-9 >= next_player_attack:
            while next_player_attack <= elapsed + 1e-9:
                next_player_attack += damage["attack_interval"]
            total_damage = damage["total_attack_damage"]
            boss_damage = 0.0
            if boss is not None and boss["hp"] > 0.0:
                boss_damage = total_damage * number(combat["boss_focus_fraction"])
                boss["hp"] -= boss_damage
                boss["damage_taken"] += boss_damage
                if boss["hp"] <= 0.0:
                    boss_ttk = elapsed - boss["boss_start_time"]
                    checkpoint_id = boss["checkpoint_id"]
                    boss_results.append({
                        "checkpoint_id": checkpoint_id,
                        "boss_id": boss["enemy_id"],
                        "status": "DEFEATED",
                        "spawn_time": boss["boss_start_time"],
                        "defeat_time": elapsed,
                        "ttk_seconds": round(boss_ttk, 3),
                        "target_range": list(target_policy["first_slice_boss_ttk_seconds"] if checkpoint_id != "boss_final_20" else target_policy["final_boss_ttk_seconds"]),
                        "target_pass": target_policy["first_slice_boss_ttk_seconds"][0] <= boss_ttk <= target_policy["first_slice_boss_ttk_seconds"][1] if checkpoint_id != "boss_final_20" else target_policy["final_boss_ttk_seconds"][0] <= boss_ttk <= target_policy["final_boss_ttk_seconds"][1],
                    })
                    reward_row = boss_reward_map(model)[checkpoint_id]
                    reward_results.append(resolve_reward(model, ledger, run_id, checkpoint_id, reward_amount(reward_row)))
                    chest_results.append(resolve_chest(model, state, checkpoint_id, elapsed))
                    boss = None
            remaining = total_damage - boss_damage
            targets = sorted(active, key=lambda entity: (entity["spawn_time"], entity["entity_id"]))[: damage["targets_per_attack"]]
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
                        entity["first_damage_time"] = elapsed

        survivors = []
        for entity in active:
            if entity["hp"] <= 0.0:
                register_kill(entity, elapsed)
            else:
                survivors.append(entity)
        active = survivors

        for checkpoint_time in (120.0, 300.0, 600.0, 900.0, 1200.0):
            key = f"{int(checkpoint_time)}"
            if elapsed >= checkpoint_time and key not in checkpoint_levels:
                checkpoint_levels[key] = state["level"]

    # The final boss is spawned at the 20-minute checkpoint.  Resolve its
    # target TTK in the explicit post-run window without advancing waves/XP.
    if boss is not None and death_time is None:
        final_damage = damage_components(model, profile, hero_id, state)
        focused_dps = final_damage["total_attack_damage"] / final_damage["attack_interval"] * number(combat["boss_focus_fraction"])
        final_ttk = boss["hp"] / focused_dps if focused_dps > 0 else math.inf
        checkpoint_id = boss["checkpoint_id"]
        target_range = target_policy["final_boss_ttk_seconds"]
        within_window = final_ttk <= number(simulation["post_final_boss_window_seconds"])
        boss_results.append({
            "checkpoint_id": checkpoint_id,
            "boss_id": boss["enemy_id"],
            "status": "PROJECTED_POST_RUN_DEFEAT" if within_window else "POST_RUN_WINDOW_EXCEEDED",
            "spawn_time": boss["boss_start_time"],
            "defeat_time": main_duration + final_ttk,
            "ttk_seconds": round(final_ttk, 3),
            "target_range": list(target_range),
            "target_pass": number(target_range[0]) <= final_ttk <= number(target_range[1]),
            "within_post_run_window": within_window,
        })
        if within_window:
            reward_row = boss_reward_map(model)[checkpoint_id]
            reward_results.append(resolve_reward(model, ledger, run_id, checkpoint_id, reward_amount(reward_row)))
            first_clear = model["rewards"]["first_clear_bonus"]
            first_clear_reward = reward_amount(first_clear)
            reward_results.append(resolve_reward(model, ledger, run_id, "run_result", first_clear_reward))
            artifact_model = simulation["artifact_offer_model"]
            artifact_offer_results.append({
                "offer_id": f"{run_id}:first_clear_artifact",
                "source_kind": "FIRST_CLEAR_REWARD",
                "source_id": "reward_first_clear_bonus",
                "choice_count": integer(artifact_model["choice_count"]),
                "status": "OFFER_CREATED_PENDING_SELECTION",
                "effect_status": artifact_model["effect_parameters_status"],
            })
            chest_results.append({"checkpoint_id": checkpoint_id, "outcome": "NO_BOSS_CHEST", "status": "CANON_ARCHITECTURE"})

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
    }
    reward_balance = sum_ledger(ledger)
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
            "proposed_build": {
                "weapon_id": model["simulation_model"]["heroes_and_profiles"]["heroes"][hero_id]["starting_weapon_id"],
                "passive_id": model["simulation_model"]["heroes_and_profiles"]["heroes"][hero_id]["starting_passive_id"],
            },
        },
        "progression": {
            "final_level_at_20_minutes": state["level"],
            "final_xp_at_20_minutes": round(state["xp"], 3),
            "levels_at_checkpoints": {key: checkpoint_levels.get(key) for key in ("120", "300", "600", "900", "1200")},
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
            "survived_main_run": death_time is None,
            "death_time_seconds": death_time,
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
            "boss_interruption_checkpoints": [
                {"time_seconds": checkpoint, "factor_at_checkpoint": round(boss_interruption_factor(model, checkpoint), 6), "factor_at_plus_8": round(boss_interruption_factor(model, checkpoint + number(simulation["boss_interruption"]["suppression_seconds"])), 6)}
                for checkpoint in (300.0, 600.0, 900.0, 1200.0)
            ],
        },
        "rewards": {
            "ledger_balance": reward_balance,
            "reward_events": reward_results,
            "idempotency_pass": all(not attempt.get("duplicate_accepted", False) for event in reward_results for attempt in event.get("attempts", [])),
            "final_boss_chest_offer_created": False,
            "first_clear_artifact_offer_created": bool(artifact_offer_results),
            "artifact_offer_choice_count": integer(simulation["artifact_offer_model"]["choice_count"]) if artifact_offer_results else 0,
        },
        "runtime_boundary": {
            "godot_runtime_executed": False,
            "collision_and_telegraph_evidence": "NOT_IMPLEMENTED",
            "android_fps_evidence": "BLOCKED",
            "model_status": "SIMULATED_MODEL_ONLY",
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
        "runs": runs,
    }


def assert_result_shape(model: Dict[str, Any], result: Dict[str, Any]) -> None:
    if result["status"] != "SIMULATED_MODEL_ONLY":
        raise AssertionError("unexpected simulation status")
    expected_duration = number(model["simulation_model"]["main_run_duration_seconds"])
    for run in result["runs"]:
        if run["runtime_boundary"]["godot_runtime_executed"]:
            raise AssertionError("model simulator must not claim Godot runtime execution")
        if run["waves"]["active_cap"]["max_occupancy"] < 0:
            raise AssertionError("negative occupancy")
        if run["progression"]["levels_at_checkpoints"]["120"] is None and run["risk"]["survived_main_run"]:
            raise AssertionError("surviving run must report the two-minute level")
        for boss in run["combat"]["boss_results"]:
            if boss.get("spawn_time", expected_duration) < 0:
                raise AssertionError("invalid boss spawn time")
        if not run["rewards"]["idempotency_pass"]:
            raise AssertionError("duplicate reward grant accepted")


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
