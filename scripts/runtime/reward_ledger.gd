extends RefCounted
class_name RewardLedger

## Idempotent reward settlement boundary.

var entries: Dictionary = {}


func settle(run_id: String, reward_scope: String, checkpoint_id: String, reward_type: String, payload: Dictionary) -> Dictionary:
    var key := "%s:%s:%s:%s" % [run_id, reward_scope, checkpoint_id, reward_type]
    if entries.has(key):
        var duplicate: Dictionary = entries[key].duplicate(true)
        duplicate["duplicate"] = true
        return duplicate

    var entry := {
        "ok": true,
        "duplicate": false,
        "ledger_key": key,
        "run_id": run_id,
        "reward_scope": reward_scope,
        "checkpoint_id": checkpoint_id,
        "reward_type": reward_type,
        "payload": payload.duplicate(true)
    }
    entries[key] = entry.duplicate(true)
    return entry


func snapshot() -> Dictionary:
    return entries.duplicate(true)
