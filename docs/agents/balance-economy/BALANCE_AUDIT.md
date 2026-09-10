# Balance Audit — SYNC-03 / REF-BALANCE-REF-01

Status: `PARTIAL / MODEL_ONLY`

This is the current Balance handoff. It is not a Godot, Android, playable, or
runtime-verification claim.

## Live source and audit boundary

| Field | Evidence |
|---|---|
| Repository / branch | `xxiamadelxx-blip/mac` / `main` |
| Parent HEAD read before this slice | `86eaf6a94593d09e2c8620351cf8186ce736158c` |
| Live B1 source | `docs/BALANCE_ECONOMY_SPEC.md`, SHA `6aa4ec96afc8a8c9e6a35c164c99e7d62910a687` |
| Architecture map | `docs/agents/architecture/REGISTRY_VARIANT_MAP.json`, published at parent `0ec954c7f6aed51fc309a6b59e7ec3a5e16371d2` |
| Model | `BALANCE_MODEL.json`, model version `0.5`, status `PARTIAL` |
| Runtime claim | `NOT_IMPLEMENTED`; no Godot/Android command was used |
| Scope | Balance-owned model, simulator, validator and evidence documents only |

The root `README.md`, `GAME_MANIFEST.md`, `ROADMAP.md` and first-run
architecture documents still contain labelled legacy 20-minute/four-main or
three-intermediate language. `docs/AGENT_SYNC_STATE.md` and the published
architecture variant map are the current coordination inputs; this Balance
slice does not rewrite another agent's write set.

## Closed Balance-owned work

- Added explicit top-level `main_bosses`, `mini_bosses` and `elite_variants`
  arrays consumed by `scripts/runtime/content_registry.gd`.
- Bound ten ordinary content IDs to numeric model records and ten mapped elite
  IDs to proposed overlays. Runtime selection remains capped at five.
- Kept all extension values labelled `PROPOSED`, `DERIVED`, `PENDING_B1` or
  `PENDING_PRODUCT_DECISION`; no missing B1 value was promoted to `CANON`.
- Replaced the placeholder simulation slice with a deterministic 30-minute
  model covering waves, cap, XP/levels, combat, TTK, incoming risk, six main
  bosses, five mini-bosses, post-boss relief/ramp/siege, elite packs,
  rewards, chests, fallback, artifact offers and idempotency.

## Evidence

Commands run on the candidate model:

```text
python3 -m json.tool current_balance_model.json
python3 -m py_compile current_balance_simulator.py current_balance_validator.py verify_balance_30m.py
python3 current_balance_validator.py --model current_balance_model.json --architecture current_architecture_contract.json
python3 verify_balance_30m.py --model current_balance_model.json --simulator current_balance_simulator.py
```

Observed:

```text
BALANCE_MODEL_CHECK=PASS
waves=7 main_bosses=6 mini_bosses=5 elite_variants=10
runtime_claim=NOT_IMPLEMENTED
ARCHITECTURE_JOIN=BLOCKED
INDEPENDENT_30M_CHECK=PASS
run_count=30
repeat_hash=e3fea44d1bda986bfae372d83ee7efabf9549e212ad63f2e61fa0242c22b758c
survived=30
completed=30
runtime_claim=NOT_IMPLEMENTED
```

The independent check runs seeds `101, 202, 303, 404, 505` across fresh,
moderate and max M1 profiles for both heroes. A single seed 101 run also
reported six main events, five mini events, visible clock `1800.0`, wall clock
`2261.5`, final boss with no chest, first-clear ledger
`1575 Gold / 520 Lunar Seals / 16 Boss Essence`, and maximum landed hit
`12.25%` of base HP.

## Unresolved blockers

1. `ARCHITECTURE_JOIN=BLOCKED`: the first-run data contract still exposes the
   legacy 1200-second/four-main/three-intermediate shape and the opposing
   clock wording. Architecture/Runtime owns reconciliation.
2. B1 has no canonical absolute base HP/ATK/speed for the new ordinary and
   elite families, no late 20:00–30:00 numeric anchors, and no exact mini/elite
   cadence. These remain proposed model inputs, not balance lock.
3. Content/Architecture have not promoted five stable mini-boss IDs or the two
   extension main-boss identities into the consumed registry.
4. No Godot trace, collision/telegraph proof, Android occupancy or FPS evidence
   exists. Python simulation cannot close R2/R3/R4.

## Handoff status

The balance model is structurally checkable and independently reproducible, but
the package remains `PARTIAL / MODEL_ONLY`. The resulting commit SHA must be
recorded by the GitHub publication handoff; the parent above is the exact live
HEAD used for this slice.

Next action: Architecture/Runtime publishes one reconciled 30-minute registry
and clock contract, then Runtime runs the R2 Godot trace against this model.
