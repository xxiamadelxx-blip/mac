#!/usr/bin/env python3
"""Dependency-free balance contract simulator.

This program intentionally separates canonical arithmetic from test fixtures.
It does not read or write production game data and it cannot prove runtime
balance. Values in TEST_PLACEHOLDER_PROFILES and TTK_PLACEHOLDER_FIXTURE are
only harness inputs for checking formulas and report plumbing.
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Tuple


SOURCE_REVISION = "6aa4ec96afc8a8c9e6a35c164c99e7d62910a687"
DEFAULT_SEED = 20260909


WAVE_BANDS: Tuple[Dict[str, Any], ...] = (
    {
        "id": "wave_00_02",
        "start": 0,
        "end": 120,
        "spawn_budget_per_second": 6,
        "active_cap": 40,
        "hp_multiplier": 1.0,
        "damage_multiplier": 0.70,
        "speed_multiplier": 0.90,
        "level_target": 2,
    },
    {
        "id": "wave_02_05",
        "start": 120,
        "end": 300,
        "spawn_budget_per_second": 10,
        "active_cap": 80,
        "hp_multiplier": 1.10,
        "damage_multiplier": 0.85,
        "speed_multiplier": 1.00,
        "level_target": 5,
    },
    {
        "id": "wave_05_10",
        "start": 300,
        "end": 600,
        "spawn_budget_per_second": 15,
        "active_cap": 130,
        "hp_multiplier": 1.35,
        "damage_multiplier": 1.00,
        "speed_multiplier": 1.02,
        "level_target": 9,
    },
    {
        "id": "wave_10_15",
        "start": 600,
        "end": 900,
        "spawn_budget_per_second": 22,
        "active_cap": 200,
        "hp_multiplier": 1.70,
        "damage_multiplier": 1.25,
        "speed_multiplier": 1.05,
        "level_target": 13,
    },
    {
        "id": "wave_15_20",
        "start": 900,
        "end": 1200,
        "spawn_budget_per_second": 30,
        "active_cap": 280,
        "hp_multiplier": 2.20,
        "damage_multiplier": 1.55,
        "speed_multiplier": 1.08,
        "level_target": "17-18",
    },
)


XP_DROPS = (1, 5, 15, 40, 80, 250)


CHECKPOINT_REWARDS: Tuple[Dict[str, Any], ...] = (
    {"checkpoint_id": "boss_01_05", "time_seconds": 300, "gold": 50, "moon_seals": 15, "boss_essence": 1},
    {"checkpoint_id": "boss_02_10", "time_seconds": 600, "gold": 75, "moon_seals": 20, "boss_essence": 1},
    {"checkpoint_id": "boss_03_15", "time_seconds": 900, "gold": 100, "moon_seals": 25, "boss_essence": 1},
    {"checkpoint_id": "boss_final_20", "time_seconds": 1200, "gold": 200, "moon_seals": 60, "boss_essence": 2},
)


FIRST_CLEAR_BONUS = {"gold": 300, "moon_seals": 180, "boss_essence": 1}
REPEAT_CLEAR_TOTAL = {"gold": 425, "moon_seals": 120, "boss_essence": 5}


# These are deliberately not production definitions. They make the report
# exercise profile plumbing while the real profile rules remain pending.
TEST_PLACEHOLDER_PROFILES: Dict[str, Dict[str, Any]] = {
    "fresh": {
        "status": "TEST_PLACEHOLDER",
        "xp_per_second": 1.00,
        "damage_scale": 1.00,
        "note": "Harness-only baseline; not a shipped progression profile.",
    },
    "moderate": {
        "status": "TEST_PLACEHOLDER",
        "xp_per_second": 1.20,
        "damage_scale": 1.15,
        "note": "Harness-only mid-progression assumption; product definition pending.",
    },
    "max_m1": {
        "status": "TEST_PLACEHOLDER",
        "xp_per_second": 1.40,
        "damage_scale": 1.30,
        "note": "Harness-only upper-bound assumption; product definition pending.",
    },
}


# This fixture only checks the TTK equation and target-range guard. Its values
# are not enemy stats and must never be copied into runtime content.
TTK_PLACEHOLDER_FIXTURE: Dict[str, Dict[str, float]] = {
    "ordinary": {"effective_hp": 100.0, "sustained_dps": 60.0, "target_min": 0.5, "target_max": 2.5},
    "elite": {"effective_hp": 1000.0, "sustained_dps": 50.0, "target_min": 10.0, "target_max": 25.0},
    "first_slice_boss": {"effective_hp": 3000.0, "sustained_dps": 50.0, "target_min": 45.0, "target_max": 80.0},
    "final_boss": {"effective_hp": 5250.0, "sustained_dps": 50.0, "target_min": 90.0, "target_max": 120.0},
}


def round_half_up(value: float) -> int:
    """Match the positive-value rounding intended by the B1 formula."""

    return int(value + 0.5)


def xp_to_next(level: int) -> int:
    value = 30 + 12 * (level - 1) + 3 * ((level - 1) ** 1.35)
    return round_half_up(value)


def xp_thresholds(max_level: int = 12) -> List[Dict[str, int]]:
    cumulative = 0
    rows: List[Dict[str, int]] = []
    for level in range(1, max_level + 1):
        next_xp = xp_to_next(level)
        cumulative += next_xp
        rows.append(
            {
                "level": level,
                "xp_to_next": next_xp,
                "cumulative_xp": cumulative,
            }
        )
    return rows


def level_for_total_xp(total_xp: float, thresholds: Iterable[Dict[str, int]]) -> int:
    level = 1
    for row in thresholds:
        if total_xp >= row["cumulative_xp"]:
            level = row["level"] + 1
    return level


def rank_costs(max_rank: int = 10) -> List[Dict[str, int]]:
    return [
        {"current_rank": rank, "cost": round_half_up(100 * (1.45**rank))}
        for rank in range(max_rank)
    ]


def wave_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for band in WAVE_BANDS:
        duration = band["end"] - band["start"]
        rows.append(
            {
                "wave_band_id": band["id"],
                "duration_seconds": duration,
                "spawn_budget_per_second": band["spawn_budget_per_second"],
                "active_cap": band["active_cap"],
                "hp_multiplier": band["hp_multiplier"],
                "damage_multiplier": band["damage_multiplier"],
                "speed_multiplier": band["speed_multiplier"],
                "level_target": band["level_target"],
                "theoretical_spawn_opportunity": duration * band["spawn_budget_per_second"],
            }
        )
    return rows


def boss_interruption_projection() -> Dict[str, Any]:
    start_factor = 0.70
    end_factor = 1.00
    duration = 20
    return {
        "reduction_seconds": 8,
        "start_factor": start_factor,
        "end_factor": end_factor,
        "recovery_duration_seconds": duration,
        "linear_average_factor": (start_factor + end_factor) / 2,
        "linear_equivalent_nominal_spawn_seconds": duration * (start_factor + end_factor) / 2,
        "status": "DERIVED_CONDITIONAL",
        "condition": "single uninterrupted recovery with linear interpolation; overlap semantics are pending",
    }


def reward_totals() -> Dict[str, Dict[str, int]]:
    checkpoint_total = {
        wallet: sum(row[wallet] for row in CHECKPOINT_REWARDS)
        for wallet in ("gold", "moon_seals", "boss_essence")
    }
    first_clear_total = {
        wallet: checkpoint_total[wallet] + FIRST_CLEAR_BONUS[wallet]
        for wallet in checkpoint_total
    }
    return {
        "checkpoint_sum": checkpoint_total,
        "first_clear_total": first_clear_total,
        "repeat_clear_total": dict(REPEAT_CLEAR_TOTAL),
    }


@dataclass
class TestLedger:
    """A minimal duplicate-grant harness, not a wallet implementation."""

    granted_keys: set
    grants: List[Dict[str, Any]]

    def grant_once(self, key: Tuple[str, str, str, str], reward: Dict[str, int]) -> bool:
        if key in self.granted_keys:
            return False
        self.granted_keys.add(key)
        self.grants.append({"key": list(key), "reward": dict(reward)})
        return True


def idempotency_harness(seed: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    run_id = f"test-run-{rng.randrange(1000000):06d}"
    table_version = SOURCE_REVISION[:12]
    ledger = TestLedger(set(), [])
    attempts = []
    for checkpoint in CHECKPOINT_REWARDS[:2]:
        key = (run_id, checkpoint["checkpoint_id"], "defeated_boss", table_version)
        accepted = ledger.grant_once(
            key,
            {
                "gold": checkpoint["gold"],
                "moon_seals": checkpoint["moon_seals"],
                "boss_essence": checkpoint["boss_essence"],
            },
        )
        attempts.append({"key": list(key), "accepted": accepted})
        duplicate = ledger.grant_once(
            key,
            {
                "gold": checkpoint["gold"],
                "moon_seals": checkpoint["moon_seals"],
                "boss_essence": checkpoint["boss_essence"],
            },
        )
        attempts.append({"key": list(key), "accepted": duplicate})
    return {
        "status": "SIMULATED_TEST_PLACEHOLDER",
        "schema_status": "PENDING_PRODUCT_DECISION",
        "attempt_count": len(attempts),
        "accepted_count": sum(1 for attempt in attempts if attempt["accepted"]),
        "grant_count": len(ledger.grants),
        "duplicate_attempts_rejected": all(
            not attempt["accepted"] for attempt in attempts if attempts.index(attempt) % 2 == 1
        ),
        "attempts": attempts,
        "grants": ledger.grants,
        "note": "The key shape is a test fixture; production idempotency schema remains pending.",
    }


def ttk_harness() -> Dict[str, Any]:
    rows = []
    for encounter, fixture in TTK_PLACEHOLDER_FIXTURE.items():
        ttk = fixture["effective_hp"] / fixture["sustained_dps"]
        rows.append(
            {
                "encounter": encounter,
                "effective_hp": fixture["effective_hp"],
                "sustained_dps": fixture["sustained_dps"],
                "ttk_seconds": round(ttk, 3),
                "target_min": fixture["target_min"],
                "target_max": fixture["target_max"],
                "target_guard_passes": fixture["target_min"] <= ttk <= fixture["target_max"],
                "status": "TEST_PLACEHOLDER",
            }
        )
    return {
        "status": "SIMULATED_TEST_PLACEHOLDER",
        "rows": rows,
        "note": "This validates the TTK equation and guard ranges only; it is not enemy or hero runtime evidence.",
    }


def profile_projection(profile: Dict[str, Any], thresholds: List[Dict[str, int]]) -> Dict[str, Any]:
    xp_rate = profile["xp_per_second"]
    at_10_minutes = xp_rate * 600
    first_level_seconds = thresholds[0]["xp_to_next"] / xp_rate
    return {
        "status": profile["status"],
        "xp_per_second": xp_rate,
        "damage_scale": profile["damage_scale"],
        "first_level_seconds": round(first_level_seconds, 3),
        "level_at_10_minutes": level_for_total_xp(at_10_minutes, thresholds),
        "total_xp_at_10_minutes": round(at_10_minutes, 3),
        "note": profile["note"],
    }


def build_result(seed: int) -> Dict[str, Any]:
    thresholds = xp_thresholds()
    waves = wave_rows()
    result = {
        "status": "SIMULATED_TEST_PLACEHOLDER",
        "source_revision": SOURCE_REVISION,
        "seed": seed,
        "canonical_contract_checks": {
            "xp_drop_values": list(XP_DROPS),
            "xp_thresholds": thresholds,
            "wave_rows": waves,
            "nominal_spawn_opportunity_total": sum(row["theoretical_spawn_opportunity"] for row in waves),
            "boss_interruption_projection": boss_interruption_projection(),
            "reward_totals": reward_totals(),
            "meta_rank_costs": rank_costs(),
        },
        "test_placeholder_profiles": {
            name: profile_projection(profile, thresholds)
            for name, profile in TEST_PLACEHOLDER_PROFILES.items()
        },
        "ttk_harness": ttk_harness(),
        "reward_idempotency_harness": idempotency_harness(seed),
        "runtime_verification": {
            "wave_runtime": "NOT_IMPLEMENTED",
            "combat_runtime": "NOT_IMPLEMENTED",
            "reward_ledger_runtime": "NOT_IMPLEMENTED",
            "android_performance": "BLOCKED",
        },
    }
    return result


def assert_contract(result: Dict[str, Any]) -> None:
    checks = result["canonical_contract_checks"]
    assert checks["nominal_spawn_opportunity_total"] == 22620
    assert checks["reward_totals"]["checkpoint_sum"] == {
        "gold": 425,
        "moon_seals": 120,
        "boss_essence": 5,
    }
    assert checks["reward_totals"]["first_clear_total"] == {
        "gold": 725,
        "moon_seals": 300,
        "boss_essence": 6,
    }
    assert checks["reward_totals"]["repeat_clear_total"] == REPEAT_CLEAR_TOTAL
    assert checks["xp_thresholds"][0]["xp_to_next"] == 30
    assert checks["xp_thresholds"][8]["cumulative_xp"] == 896
    harness = result["reward_idempotency_harness"]
    assert harness["accepted_count"] == 2
    assert harness["grant_count"] == 2
    assert harness["duplicate_attempts_rejected"] is True
    assert all(row["target_guard_passes"] for row in result["ttk_harness"]["rows"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    result = build_result(args.seed)
    assert_contract(result)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("status=SIMULATED_TEST_PLACEHOLDER")
        print(f"seed={args.seed}")
        print(f"nominal_spawn_opportunity_total={result['canonical_contract_checks']['nominal_spawn_opportunity_total']}")
        print(f"first_clear_total={result['canonical_contract_checks']['reward_totals']['first_clear_total']}")
        print("contract_checks=PASS")
        print("runtime_verification=NOT_IMPLEMENTED")


if __name__ == "__main__":
    main()
