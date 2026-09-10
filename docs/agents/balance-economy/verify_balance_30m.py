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
    allowed_variant_ids = set(model["simulation_model"]["elite_variation_policy"]["variant_ids"]["value"])
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
        fail(errors, run["rewards"]["elite_pack_offer_idempotency_pass"], "elite offer idempotency failed")
        fail(errors, set(run["combat"].get("elite_variant_ids_used", [])).issubset(allowed_variant_ids), "unregistered elite variant emitted")
        for cycle_id in {sample["cycle_id"] for sample in run["waves"]["boss_wave_ramp"]["samples"]}:
            samples = [sample for sample in run["waves"]["boss_wave_ramp"]["samples"] if sample["cycle_id"] == cycle_id]
            density = [sample["density_factor_of_peak"] for sample in samples]
            fail(errors, all(a <= b for a, b in zip(density, density[1:])), f"non-monotonic density in {cycle_id}")
            fail(errors, samples[-1]["phase"] == "SIEGE" and samples[-1]["density_factor_of_peak"] == 1.0, f"{cycle_id} lacks peak siege")
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
    print("runtime_claim=NOT_IMPLEMENTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

