extends RefCounted
class_name ArtifactOfferSystem

## Three-card, typed, unbounded-within-run artifact source.
##
## Effect parameters remain explicit pending data when the balance source has
## not supplied them. This system never converts an artifact into a build slot.

var registry: Object


func _init(p_registry: Object) -> void:
    registry = p_registry


func create_offer(run_id: String, seed: int, source: String, sequence: int, created_revision: int) -> Dictionary:
    var model: Dictionary = registry.get_artifact_offer_model()
    var sources: Array = model.get("sources", [])
    var choice_count := int(model.get("choice_count", 0))
    var effect_types: Array = model.get("effect_types", [])
    if not sources.has(source):
        return {"ok": false, "code": "ARTIFACT_SOURCE_INVALID", "source": source}
    if choice_count != 3 or effect_types.size() < choice_count:
        return {"ok": false, "code": "ARTIFACT_OFFER_CONTRACT_INVALID", "choice_count": choice_count, "effect_type_count": effect_types.size()}

    var candidates: Array[Dictionary] = []
    var choice_ids: Array[String] = []
    var base_index := posmod(seed + sequence * 7 + (17 if source == "ELITE_PACK" else 53), effect_types.size())
    for index in range(choice_count):
        var effect_type := str(effect_types[(base_index + index) % effect_types.size()])
        var artifact_id := "artifact_%s" % effect_type.to_lower()
        var candidate := {
            "choice_id": artifact_id,
            "artifact_id": artifact_id,
            "source": source,
            "effect": {
                "type": effect_type,
                "trigger": "PENDING_PRODUCT_DECISION",
                "target": "PENDING_PRODUCT_DECISION",
                "parameters": {},
                "parameters_status": str(model.get("exact_definitions", model.get("effect_parameters_status", "PENDING_PRODUCT_DECISION")))
            },
            "capacity": "UNBOUNDED_WITHIN_RUN",
            "build_slot_mutation": false,
            "source_path": "simulation_model.build_catalog.artifact_offer"
        }
        candidates.append(candidate)
        choice_ids.append(artifact_id)

    return {
        "ok": true,
        "offer_id": "%s:artifact:%d" % [run_id, sequence],
        "offer_type": "ARTIFACT_OFFER",
        "source": source,
        "choice_count": choice_count,
        "choice_ids": choice_ids,
        "candidates": candidates,
        "refresh_count": 0,
        "created_at_revision": created_revision,
        "claimed": false
    }


func refresh_offer(offer: Dictionary, seed: int) -> Dictionary:
    var refreshed := offer.duplicate(true)
    var candidates: Array[Dictionary] = []
    var choice_ids: Array[String] = []
    var effect_types: Array = registry.get_artifact_effect_types()
    var count := int(offer.get("choice_count", 0))
    var refresh_count := int(offer.get("refresh_count", 0)) + 1
    var base_index := posmod(seed + refresh_count * 11, effect_types.size()) if not effect_types.is_empty() else 0
    var model: Dictionary = registry.get_artifact_offer_model()
    for index in range(count):
        var effect_type := str(effect_types[(base_index + index) % effect_types.size()])
        var artifact_id := "artifact_%s" % effect_type.to_lower()
        var candidate := {
            "choice_id": artifact_id,
            "artifact_id": artifact_id,
            "source": offer.get("source", ""),
            "effect": {
                "type": effect_type,
                "trigger": "PENDING_PRODUCT_DECISION",
                "target": "PENDING_PRODUCT_DECISION",
                "parameters": {},
                "parameters_status": str(model.get("exact_definitions", model.get("effect_parameters_status", "PENDING_PRODUCT_DECISION")))
            },
            "capacity": "UNBOUNDED_WITHIN_RUN",
            "build_slot_mutation": false,
            "source_path": "simulation_model.build_catalog.artifact_offer"
        }
        candidates.append(candidate)
        choice_ids.append(artifact_id)
    refreshed["candidates"] = candidates
    refreshed["choice_ids"] = choice_ids
    refreshed["refresh_count"] = refresh_count
    refreshed["claimed"] = false
    return refreshed


func select(offer: Dictionary, choice_id: String) -> Dictionary:
    var choice_ids: Array = offer.get("choice_ids", [])
    if not choice_ids.has(choice_id):
        return {"ok": false, "code": "INVALID_ARTIFACT_CHOICE", "choice_id": choice_id}
    for candidate in offer.get("candidates", []):
        if str(candidate.get("choice_id", "")) == choice_id:
            return {"ok": true, "selected": candidate.duplicate(true)}
    return {"ok": false, "code": "ARTIFACT_CANDIDATE_MISSING", "choice_id": choice_id}
