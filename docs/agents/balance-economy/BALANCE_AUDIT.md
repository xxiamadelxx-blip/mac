# Balance Audit — SYNC-04 / REF-BALANCE-REF-01

Status: `PARTIAL / MODEL_ONLY` (R2 structural join verified; fresh numeric trace pending)

This handoff closes the Balance-owned model/content binding work. It does not
claim Godot, Android, playable, collision or runtime verification.

## Live source boundary

| Field | Evidence |
|---|---|
| Repository / branch | `xxiamadelxx-blip/mac` / `main` |
| Parent HEAD read immediately before this slice | `7a8112e9bb3175d6c86030b14e680ce01b4e1254` |
| Live B1 | `docs/BALANCE_ECONOMY_SPEC.md`, `6aa4ec96afc8a8c9e6a35c164c99e7d62910a687` |
| Live sync router | `docs/AGENT_SYNC_STATE.md`, current live read; R2 handoff at `7a8112e9bb3175d6c86030b14e680ce01b4e1254` |
| Live architecture contract | `e9a50971f61f204cbbda39edaad2c48a08e2228b` |
| Live registry map | `0b8cb1bb96d4ab2d0bd14bd7a21b042e53d8c5e8` |
| Balance model | `BALANCE_MODEL.json`, `0.8-registry-ids-elite-chest`, status `PARTIAL` |
| Runtime status | R2 structural join `RUNTIME_VERIFIED` on the prior model; this numeric publication still needs a fresh post-publication trace |
| Numeric authority | `BALANCE_MODEL.json`; simulator reads this same data |

The latest parent contains later mockup handoffs. This slice does not rewrite
Content, Architecture, Runtime, visual assets or root docs.

The live R2 handoff proves consumption of the registry shape and policy seam:
6 main bosses, 5 mini bosses, 10 ordinary IDs, 10 elite IDs, active projection
cap 5, 15 chest windows, main-boss freeze and mini-boss continuation. It does
not promote absent B1 absolute numbers or prove the new model's combat results.

## What is now closed in Balance

- Full model catalog: 10 weapons, 10 passives, 10 synergies, 10 artifacts, 10
  ordinary enemies, 10 elite variants, 6 main bosses and 5 mini-bosses.
- Absolute HP/ATK/speed, cadence, weapon, passive, synergy and artifact values
  are written as explicit `PROPOSED` records when B1 is silent; derived
  resolved/late values are explicit `DERIVED` records.
- Main IDs and numeric status are separated: a canonical existing boss ID does
  not make its missing absolute stats canonical.
- Registry join is explicit in the Balance model: the ten ordinary IDs and ten
  elite IDs match the live REF-ARCH-02 map; the two legacy enemy IDs remain
  outside the 30-minute ordinary roster. Each elite window projects at most
  five catalog IDs using the deterministic model key.
- The simulator is a deterministic 30-minute model: seven wave bands, active
  cap, XP/levels, combat/TTK, HP/incoming damage/death risk, main-boss clock
  freeze, mini-boss continuation, post-boss relief/ramp/siege, elite packs,
  reward/chest/fallback and idempotency.
- ELITE_CHEST cadence is five windows after mini-boss checkpoints at
  07:30/12:30/17:30/22:30/27:30. Each offer has three cards, no wallet
  mutation and an idempotency key. If a finite pack remains at the next main
  checkpoint, the model settles it at that boundary before the main-boss
  freeze and commits the reserved window exactly once.
- The model includes the requested low-to-peak post-boss shape: relief, low
  entry, monotonic ramp, peak-density siege, then the next boss.
- Late-run XP throughput is now proposed at 22.0 XP/s for 20:00–25:00 and
  27.0 XP/s for 25:00–30:00; the B1 threshold formula remains unchanged.
- The model target is level 40 and three distinct synergies. Level 38 is an
  accepted lower variance floor; the simulator does not force every seed to
  land on the exact target.
- Three 10/10 weapon-passive pairs are represented through an explicit proposed
  paired-offer progression, so synergy claims are distinct IDs rather than a
  repeated claim of one starter synergy.

## Fresh evidence

```text
python3 -m json.tool BALANCE_MODEL.json
python3 -m py_compile balance_simulator.py balance_contract_validator.py verify_balance_30m.py
python3 balance_contract_validator.py --model BALANCE_MODEL.json
python3 balance_simulator.py --model BALANCE_MODEL.json --seed 101
python3 verify_balance_30m.py --model BALANCE_MODEL.json --simulator balance_simulator.py
```

Observed after the final model edit:

```text
BALANCE_MODEL_CHECK=PASS
waves=7 main_bosses=6 mini_bosses=5 elite_variants=10
runtime_claim=R2_STRUCTURAL_ONLY_PENDING_FRESH_TRACE
ARCHITECTURE_JOIN=PASS on live R2 contract/map; local legacy helper warning is not release evidence
single-seed shape_check=PASS, run_count=6
INDEPENDENT_30M_CHECK=PASS
run_count=30
repeat_hash=da5a6c752d2665e5d92f5cc5a1a6a9f8bbd0b7932eabe2e8005ff7ba431c3715
survived=30
completed=30
runtime_claim=R2_STRUCTURAL_ONLY_PENDING_FRESH_TRACE
```

Independent seeds are `101, 202, 303, 404, 505`; profiles are `fresh`,
`moderate`, `max_m1`; both heroes are included. The independent checker is a
model replay, not a game run.

## Remaining blockers

1. B1 still has no canonical absolute per-ID HP/ATK/speed for the new ordinary,
   elite and mini families, no 20:00–30:00 late anchors, and no exact elite
   cadence. The model values and five-window ELITE_CHEST trigger are therefore
   not a balance lock; each missing value has explicit source, formula,
   proposed value, rationale and status in the JSON.
2. Content/Architecture still have a 10/10 versus mockup 6/5 weapon/passive
   progression-gate conflict; the model records it as pending rather than
   choosing silently.
3. R2 structural consumption is proven on the prior model shape, but no fresh
   post-publication trace proves these new numeric profiles, TTK or economy
   outcomes. The balance package does not claim gameplay verification.
4. No collision/telegraph, player-behaviour, save/reload or Android occupancy/
   FPS evidence exists for this numeric slice.

## Handoff

The balance package is structurally validated and independently replayable, but
the project status remains `PARTIAL / MODEL_ONLY`, not `DONE` or `VERIFIED`.

Next action: Runtime/Architecture runs a fresh R2 30-minute trace against this published `BALANCE_MODEL.json` and returns the numeric-model evidence.
