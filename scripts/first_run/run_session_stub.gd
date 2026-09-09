extends RefCounted
class_name FirstRunSessionStub

## Minimal data-first RunSession seam for the first playable slice.
## All values prefixed with STUB are intentionally temporary and are not B1 balance.

const RUN_DURATION_SECONDS := 1200.0
const XP_FORMULA_NOTE := "round(30 + 12 * (L - 1) + 3 * (L - 1)^1.35)"

const WAVE_BANDS: Array[Dictionary] = [
    {
        "id": "wave_0_2m",
        "start_seconds": 0.0,
        "end_seconds": 120.0,
        "spawn_budget_per_second": 6,
        "active_cap": 40,
        "enemy_hp_multiplier": 1.0,
        "enemy_damage_multiplier": 0.70,
        "enemy_speed_multiplier": 0.90
    },
    {
        "id": "wave_2_5m",
        "start_seconds": 120.0,
        "end_seconds": 300.0,
        "spawn_budget_per_second": 10,
        "active_cap": 80,
        "enemy_hp_multiplier": 1.10,
        "enemy_damage_multiplier": 0.85,
        "enemy_speed_multiplier": 1.00
    },
    {
        "id": "wave_5_10m",
        "start_seconds": 300.0,
        "end_seconds": 600.0,
        "spawn_budget_per_second": 15,
        "active_cap": 130,
        "enemy_hp_multiplier": 1.35,
        "enemy_damage_multiplier": 1.00,
        "enemy_speed_multiplier": 1.02
    },
    {
        "id": "wave_10_15m",
        "start_seconds": 600.0,
        "end_seconds": 900.0,
        "spawn_budget_per_second": 22,
        "active_cap": 200,
        "enemy_hp_multiplier": 1.70,
        "enemy_damage_multiplier": 1.25,
        "enemy_speed_multiplier": 1.05
    },
    {
        "id": "wave_15_20m",
        "start_seconds": 900.0,
        "end_seconds": 1200.0,
        "spawn_budget_per_second": 30,
        "active_cap": 280,
        "enemy_hp_multiplier": 2.20,
        "enemy_damage_multiplier": 1.55,
        "enemy_speed_multiplier": 1.08
    }
]

const UPGRADE_DEFINITIONS: Array[Dictionary] = [
    {
        "id": "stub_attack",
        "title": "УСИЛИТЬ АТАКУ",
        "description": "Заглушка: +1 к урону автоматической атаки.",
        "kind": "weapon"
    },
    {
        "id": "stub_cooldown",
        "title": "УСКОРИТЬ АТАКИ",
        "description": "Заглушка: уменьшить cooldown автоматической атаки.",
        "kind": "weapon"
    },
    {
        "id": "stub_health",
        "title": "УВЕЛИЧИТЬ HP",
        "description": "Заглушка: +2 максимального HP и восстановление.",
        "kind": "passive"
    }
]

const STUB_INITIAL_HP := 12
const STUB_INITIAL_ATTACK := 1
const STUB_INITIAL_COOLDOWN := 0.80
const STUB_XP_PER_ENEMY := 5

var state: Dictionary


func _init(selected_hero_id: String = "lin_yue", seed_value: int = 20260910) -> void:
    state = {
        "run_id": "stub_run_%d" % seed_value,
        "seed": seed_value,
        "content_version": "stub-v1",
        "phase": "RUN_ACTIVE",
        "revision": 0,
        "elapsed_seconds": 0.0,
        "selected_hero_id": selected_hero_id,
        "current_wave_band_id": "wave_0_2m",
        "checkpoint_id": null,
        "hp": STUB_INITIAL_HP,
        "max_hp": STUB_INITIAL_HP,
        "attack": STUB_INITIAL_ATTACK,
        "cooldown": STUB_INITIAL_COOLDOWN,
        "level": 1,
        "xp_current": 0,
        "kills": 0,
        "upgrades": [],
        "pending_offer_ids": []
    }


func advance_time(seconds: float) -> void:
    if state["phase"] != "RUN_ACTIVE":
        return
    state["elapsed_seconds"] = min(
        RUN_DURATION_SECONDS,
        float(state["elapsed_seconds"]) + maxf(0.0, seconds)
    )
    state["current_wave_band_id"] = get_wave_band()["id"]
    state["revision"] += 1


func get_wave_band() -> Dictionary:
    var elapsed := float(state["elapsed_seconds"])
    for band in WAVE_BANDS:
        if elapsed < float(band["end_seconds"]):
            return band
    return WAVE_BANDS[WAVE_BANDS.size() - 1]


func get_xp_to_next() -> int:
    var level := int(state["level"])
    return maxi(1, int(round(30.0 + 12.0 * float(level - 1) + 3.0 * pow(float(level - 1), 1.35))))


func collect_xp(value: int) -> bool:
    if state["phase"] != "RUN_ACTIVE":
        return false
    state["xp_current"] = int(state["xp_current"]) + maxi(0, value)
    if int(state["xp_current"]) < get_xp_to_next():
        state["revision"] += 1
        return false

    state["xp_current"] = int(state["xp_current"]) - get_xp_to_next()
    state["level"] = int(state["level"]) + 1
    state["pending_offer_ids"] = [
        UPGRADE_DEFINITIONS[0]["id"],
        UPGRADE_DEFINITIONS[1]["id"],
        UPGRADE_DEFINITIONS[2]["id"]
    ]
    state["phase"] = "UPGRADE_CHOICE"
    state["revision"] += 1
    return true


func get_upgrade_definitions() -> Array[Dictionary]:
    return UPGRADE_DEFINITIONS.duplicate(true)


func choose_upgrade(index: int) -> Dictionary:
    if state["phase"] != "UPGRADE_CHOICE":
        return {"accepted": false, "reason": "NOT_WAITING_FOR_UPGRADE"}

    if index < 0 or index >= UPGRADE_DEFINITIONS.size():
        return {"accepted": false, "reason": "OFFER_INDEX_OUT_OF_RANGE"}

    var definition: Dictionary = UPGRADE_DEFINITIONS[index]
    match definition["id"]:
        "stub_attack":
            state["attack"] = int(state["attack"]) + 1
        "stub_cooldown":
            state["cooldown"] = maxf(0.25, float(state["cooldown"]) - 0.08)
        "stub_health":
            state["max_hp"] = int(state["max_hp"]) + 2
            state["hp"] = int(state["max_hp"])
        _:
            return {"accepted": false, "reason": "UNKNOWN_STUB_UPGRADE"}

    state["upgrades"].append(definition["id"])
    state["pending_offer_ids"] = []
    state["phase"] = "RUN_ACTIVE"
    state["revision"] += 1
    return {
        "accepted": true,
        "upgrade_id": definition["id"],
        "revision": state["revision"]
    }


func record_kill() -> void:
    state["kills"] = int(state["kills"]) + 1
    state["revision"] += 1


func take_damage(amount: int) -> bool:
    if state["phase"] != "RUN_ACTIVE":
        return false
    state["hp"] = int(state["hp"]) - maxi(0, amount)
    state["revision"] += 1
    if int(state["hp"]) <= 0:
        state["hp"] = 0
        state["phase"] = "DEFEAT"
        return true
    return false


func pause() -> bool:
    if state["phase"] != "RUN_ACTIVE":
        return false
    state["phase"] = "PAUSED"
    state["revision"] += 1
    return true


func resume() -> bool:
    if state["phase"] != "PAUSED":
        return false
    state["phase"] = "RUN_ACTIVE"
    state["revision"] += 1
    return true


func is_frozen() -> bool:
    return state["phase"] != "RUN_ACTIVE"


func get_phase() -> String:
    return state["phase"]


func get_attack() -> int:
    return int(state["attack"])


func get_cooldown() -> float:
    return float(state["cooldown"])


func get_state() -> Dictionary:
    return state.duplicate(true)
