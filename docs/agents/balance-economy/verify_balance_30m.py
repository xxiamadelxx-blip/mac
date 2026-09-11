#!/usr/bin/env python3
"""Independent checks for the proposed 30-minute balance model.

This checker does not use the simulator's internal shape assertions.  It runs
the simulator twice, compares canonical JSON hashes, and checks the public
result contract for main/mini clock separation, ramp monotonicity, occupancy,
and idempotent rewards.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import statistics
from pathlib import Path
from typing import Any, Dict, List


def run_once(simulator: Path, model: Path) -> Dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(simulator), "--model", str(model), "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def canonical_hash(value: Dict[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def fail(errors: List[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    here = Path(__file__).resolve().parent
    parser.add_argument("--model", type=Path, default=here / "BALANCE_MODEL.json")
    parser.add_argument("--simulator", type=Path, default=here / "balance_simulator.py")
    args = parser.parse_args()

    first = run_once(args.simulator, args.model)
    second = run_once(args.simulator, args.model)
    errors: List[str] = []
    model = json.loads(args.model.read_text(encoding="utf-8"))
    schedule = model["simulation_model"]["run_schedule"]
    duration = model["simulation_model"]["main_run_duration_seconds"]["value"]
    max_cap = max(int(row["active_cap"]["value"]) for row in model["wave_bands"])
    target_final_level = int(model["simulation_model"]["target_policy"]["target_final_level"])
    acceptable_final_level_floor = int(model["simulation_model"]["target_policy"]["acceptable_final_level_floor"])
    minimum_synergy_claims = int(model["simulation_model"]["target_policy"]["minimum_synergy_claims"])
    allowed_variant_ids = set(model["simulation_model"]["elite_variation_policy"]["variant_ids"]["value"])
    elite_windows = model["simulation_model"]["build_catalog"]["offer_model"]["elite_chest"]["windows"]
    expected_elite_window_ids = {str(row["window_id"]) for row in elite_windows}
    fail(errors, canonical_hash(first) == canonical_hash(second), "repeat simulation hash differs")
    fail(errors, first.get("run_count") == 30, "expected 30 profile/hero/seed runs")
    fail(errors, duration == 1800, "model duration is not 1800 seconds")
    fail(errors, len(schedule["main_boss_checkpoints"]) == 6, "expected six main checkpoints")
    fail(errors, len(schedule["mini_boss_checkpoints"]) == 5, "expected five mini checkpoints")
    for run in first["runs"]:
        events = run["waves"]["boss_clock_events"]
        mains = [event for event in events if event["encounter_kind"] == "MAIN_BOSS"]
        minis = [event for event in events if event["encounter_kind"] == "MINI_BOSS"]
        if run["risk"]["survived_main_run"]:
            fail(errors, len(mains) == 6, f"{run['profile']}/{run['hero_id']}/{run['seed']} missing main events")
            fail(errors, len(minis) == 5, f"{run['profile']}/{run['hero_id']}/{run['seed']} missing mini events")
        fail(errors, all(not event["run_clock_advanced_during_encounter"] for event in mains), "main boss advanced visible clock")
        fail(errors, all(event["run_clock_advanced_during_encounter"] for event in minis), "mini boss froze visible clock")
        fail(errors, run["waves"]["active_cap"]["max_occupancy"] <= max_cap, "active occupancy exceeded model cap")
        fail(errors, run["rewards"]["idempotency_pass"], "wallet reward idempotency failed")
        fail(errors, run["rewards"]["chest_idempotency_pass"], "chest idempotency failed")
        fail(errors, run["rewards"]["elite_chest_offer_idempotency_pass"], "elite chest offer idempotency failed")
        elite_offers = run["combat"].get("elite_chest_offer_results", [])
        unique_elite_windows = {str(row.get("window_id")) for row in elite_offers}
        fail(errors, len(unique_elite_windows) == len(elite_offers) // 2, "elite chest offer attempts are not one initial plus one duplicate per window")
        if run["risk"]["survived_main_run"]:
            fail(errors, unique_elite_windows == expected_elite_window_ids, "surviving run did not resolve all five ELITE_CHEST windows")
            pack_states = run["combat"].get("elite_chest_pack_states", [])
            fail(errors, len(pack_states) == 5 and all(state.get("offer_committed") for state in pack_states), "surviving run did not commit all five finite elite windows")
        fail(errors, all(row.get("source_kind") == "ELITE_CHEST" for row in elite_offers), "elite offer used a non-ELITE_CHEST source kind")
        fail(errors, all(int(row.get("choice_count", 0)) == 3 for row in elite_offers), "elite chest offer did not expose three choices")
        for projection in run["combat"].get("elite_chest_active_projections", []):
            fail(errors, projection.get("active_variant_count", 0) <= 5, "elite active projection exceeded five records")
            fail(errors, set(projection.get("active_variant_ids", [])).issubset(allowed_variant_ids), "elite active projection emitted an unregistered ID")
        fail(errors, run["progression"]["final_level_at_30_minutes"] >= acceptable_final_level_floor, f"{run['profile']}/{run['hero_id']}/{run['seed']} fell below acceptable level floor {acceptable_final_level_floor}")
        fail(errors, run["combat"]["claimed_synergy_count"] >= minimum_synergy_claims, f"{run['profile']}/{run['hero_id']}/{run['seed']} missed synergy target")
        fail(errors, len(set(run["combat"].get("synergy_ids", []))) >= minimum_synergy_claims, f"{run['profile']}/{run['hero_id']}/{run['seed']} counted duplicate synergies")
        fail(errors, set(run["combat"].get("elite_variant_ids_used", [])).issubset(allowed_variant_ids), "unregistered elite variant emitted")
        for cycle_id in {sample["cycle_id"] for sample in run["waves"]["boss_wave_ramp"]["samples"]}:
            samples = [sample for sample in run["waves"]["boss_wave_ramp"]["samples"] if sample["cycle_id"] == cycle_id]
            density = [sample["density_factor_of_peak"] for sample in samples]
            fail(errors, all(a <= b for a, b in zip(density, density[1:])), f"non-monotonic density in {cycle_id}")
            fail(errors, samples[-1]["phase"] == "SIEGE" and samples[-1]["density_factor_of_peak"] == 1.0, f"{cycle_id} lacks peak siege")
    final_levels = [run["progression"]["final_level_at_30_minutes"] for run in first["runs"]]
    fail(errors, max(final_levels) >= target_final_level, f"no run reached target level {target_final_level}")
    fail(errors, statistics.mean(final_levels) >= target_final_level, f"mean final level {statistics.mean(final_levels):.3f} is below target {target_final_level}")
    if errors:
        print("INDEPENDENT_30M_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("INDEPENDENT_30M_CHECK=PASS")
    print(f"run_count={first['run_count']}")
    print(f"repeat_hash={canonical_hash(first)}")
    print(f"survived={sum(run['risk']['survived_main_run'] for run in first['runs'])}")
    print(f"completed={sum(run['run_outcome']['completed_model_run'] for run in first['runs'])}")
    print(f"runtime_claim={first.get('runtime_claim', model.get('runtime_status', 'NOT_IMPLEMENTED'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
