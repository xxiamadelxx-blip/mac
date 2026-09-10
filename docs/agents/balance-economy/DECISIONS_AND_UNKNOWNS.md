# Decisions and Unknowns — 30-minute balance extension

## Decisions captured

| Decision | Status | Model consequence |
|---|---|---|
| Run lasts 30 minutes | USER DECISION / PROPOSED UNTIL B1 SYNC | duration = 1800s |
| Two additional main bosses | USER DECISION / IDs PENDING | six main slots at 05/10/15/20/25/30 |
| Five mini-bosses | USER DECISION / 2 IDs KNOWN, 3 PENDING | mini slots at 07:30/12:30/17:30/22:30/27:30 |
| Main bosses freeze visible timer and wave/XP/spawn clocks | CANON USER RULE | separate main encounter clock |
| Mini-bosses do not freeze timer or waves | PROPOSED CLOCK CONTRACT | same wall/run clock; waves and XP continue |
| Elite variations are not continuous | CANON USER INTENT | finite post-mini packs only |
| Elite variation purpose | PROPOSED MODEL | horde pressure plus artifact offer, no wallet mutation |
| Final boss has no boss chest | ARCHITECTURE LEGACY RULE / EXTENSION PENDING | final 30:00 remains no-chest in the model |

## Values that are explicitly proposed

All values below live in `BALANCE_MODEL.json` with source, formula, rationale and status:

- 20:00–25:00 and 25:00–30:00 wave budgets/caps/multipliers;
- five mini-boss HP/damage/cadence values;
- two new main-boss HP/damage/cadence values;
- elite overlay HP ×8, damage ×1.25, speed ×1.05, XP ×2;
- three-member finite pack and one pack after each mini-boss;
- mini/main extension wallet rewards;
- 30-minute XP pickup capacities;
- proposed post-boss reset factor 0.80, 60s siege and 8s+20s recovery interaction.

## Exact blockers

| Missing input | Why it matters | Owner | Status |
|---|---|---|---|
| 1800s architecture contract | runtime schedule and save shape | Architecture/Runtime | BLOCKED |
| new main-boss stable IDs, phase kits and final role | join, TTK and final chest policy | Content/Architecture | BLOCKED |
| three missing mini-boss IDs and kits | five encounters cannot be production-joined | Content/Architecture | BLOCKED |
| mini-boss timer semantics in runtime | prevents accidental freeze | Architecture/Runtime | BLOCKED |
| B1 20–30 wave anchors and XP curve | proposed numbers cannot become canon | Product/Balance | PENDING_B1 |
| elite variant identity/stats/cadence | determines TTK and Android occupancy | Content/Balance | PENDING_B1 |
| exact fallback/offer stacking | determines chest economy | Product/Balance | PENDING_PRODUCT_DECISION |
| fresh-profile completion target | current model completes 1/10 fresh runs | Product/Balance | PENDING_PRODUCT_DECISION |
| runtime trace and Android profile | model cannot prove playability/performance | Runtime | BLOCKED |

## Next slice

Architecture/Runtime should sync the 30-minute run schedule, encounter kinds, main-vs-mini clock policy, five mini-boss slots, elite event state and idempotency fields. Balance then reruns the exact model and updates only proposed values whose canon/source changed. Do not mark this package VERIFIED before runtime evidence exists.
