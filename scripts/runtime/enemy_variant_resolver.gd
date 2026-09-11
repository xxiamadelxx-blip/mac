extends RefCounted
class_name EnemyVariantResolver

## Deterministic, finite elite-pressure projection from the live registry.
## Proposal records remain blocked; this class never invents IDs or tuning.

const MAX_VARIANTS_PER_EVENT := 5
const REWARD_BOUNDARY := "ELITE_CHEST"

var registry: Object


func _init(p_registry: Object) -> void:
    registry = p_registry


func resolve_event(seed: int, event_revision: int, wave_band_id: String) -> Dictionary:
    if wave_band_id.is_empty():
        return {
            "ok": false,
            "code": "ELITE_VARIANT_WAVE_BAND_MISSING",
            "status": "PENDING_CONTENT_SYNC",
            "reward_boundary": REWARD_BOUNDARY
        }

    var eligible: Array[Dictionary] = []
    for record in registry.get_elite_variants():
        if not (record is Dictionary):
            continue
        if not bool(registry.is_runtime_record_ready(record)):
            continue
        var variant_id := str(record.get("variant_id", ""))
        var base_enemy_id := str(record.get(
            "base_enemy_id",
            record.get("enemy_id", record.get("base_id", ""))
        ))
        if variant_id.is_empty() or base_enemy_id.is_empty():
            continue
        eligible.append(record.duplicate(true))

    if eligible.is_empty():
        return {
            "ok": false,
            "code": "ELITE_VARIANT_CONTENT_PENDING",
            "status": "PENDING_CONTENT_SYNC",
            "reward_boundary": REWARD_BOUNDARY,
            "automatic_artifact_offer": false,
            "persistent_roster_mutation": false,
            "content_status": registry.get_r2_content_status()
        }

    var start_index := posmod(seed + event_revision, eligible.size())
    var selection_count: int = mini(MAX_VARIANTS_PER_EVENT, eligible.size())
    var selected: Array[Dictionary] = []
    for offset in range(selection_count):
        var record: Dictionary = eligible[(start_index + offset) % eligible.size()].duplicate(true)
        selected.append({
            "variant_id": str(record.get("variant_id", "")),
            "base_enemy_id": str(record.get(
                "base_enemy_id",
                record.get("enemy_id", record.get("base_id", ""))
            )),
            "wave_band_id": wave_band_id,
            "record": record,
            "reward_boundary": REWARD_BOUNDARY,
            "automatic_artifact_offer": false,
            "persistent_roster_mutation": false
        })

    return {
        "ok": true,
        "event_kind": "FINITE_ELITE_PRESSURE",
        "seed": seed,
        "event_revision": event_revision,
        "wave_band_id": wave_band_id,
        "max_variants_per_event": MAX_VARIANTS_PER_EVENT,
        "variants": selected,
        "reward_boundary": REWARD_BOUNDARY,
        "automatic_artifact_offer": false,
        "persistent_roster_mutation": false,
        "registry_source": "BALANCE_MODEL.json.elite_variants"
    }
