# Decisions and Unknowns — 30-minute balance extension

## Decisions captured

| Decision | Status | Model consequence |
|---|---|---|
| Run lasts 30 minutes | architecture duration synced; B1 numeric extension still pending | duration = 1800s |
| Two additional main bosses | architecture slots exist but content is pending | six main slots at 05/10/15/20/25/30 |
| Five mini-bosses | user/model decision; architecture currently has three intermediate slots | model slots at 07:30/12:30/17:30/22:30/27:30; 1050 and 1650 remain pending |
| Main bosses freeze visible timer and wave/XP/spawn clocks | user balance rule; conflicts with current architecture clock policy | separate main encounter clock |
| Mini-bosses do not freeze timer or waves | balance model proposal | same wall/run clock; waves and XP continue |
| Elite variations are not continuous | user intent and architecture variant policy | finite post-mini packs only |
| Elite variation purpose | proposed model | horde pressure plus artifact offer, no wallet mutation |
| Final boss has no boss chest | current architecture final outcome policy | 30:00 final remains no-chest in the model |

## Values explicitly proposed

All values below live in `BALANCE_MODEL.json` with source, formula, rationale and status:

- 20:00–25:00 and 25:00–30:00 wave budgets/caps/multipliers;
- five mini-boss HP/damage/cadence values;
- two new main-boss HP/damage/cadence values;
- elite overlay HP ×8, damage ×1.25, speed ×1.05, XP ×2;
- three-member finite pack and one pack after each mini-boss;
- mini/main extension wallet rewards;
- 30-minute XP pickup capacities;
- proposed post-main reset factor 0.80, 60s siege and 8s+20s recovery interaction.

## Exact blockers

| Missing input | Why it matters | Owner | Status |
|---|---|---|---|
| main-boss clock contract alignment | architecture currently advances time through bosses; balance freezes it | Architecture/Runtime | BLOCKED |
| five-vs-three mini schedule decision | model has five; architecture registry has 450/750/1350 only | Product + Content/Architecture | BLOCKED |
| new main-boss stable content records and kits | join, TTK and final-role proof | Content/Architecture | BLOCKED |
| two additional mini IDs and all mini skill kits | five encounters cannot be production-joined | Content/Architecture | BLOCKED |
| B1 20–30 wave anchors and XP curve | proposed numbers cannot become canon | Product/Balance | PENDING_B1 |
| elite variant numeric overrides/cadence/visuals | determines TTK and Android occupancy | Content/Balance | PENDING_B1/PENDING_VISUAL |
| exact fallback/offer stacking | determines chest economy | Product/Balance | PENDING_PRODUCT_DECISION |
| fresh-profile completion target | current model completes 2/10 fresh runs | Product/Balance | PENDING_PRODUCT_DECISION |
| runtime trace and Android profile | model cannot prove playability/performance | Runtime | BLOCKED |

## Next slice

Architecture/Runtime should first reconcile the boss clock policy and decide whether the product target is five mini-bosses or the current three intermediate slots. Then register every chosen encounter and variant record, wire runtime consumers to `BALANCE_MODEL.json`, and rerun the exact independent seed set. Do not mark this package VERIFIED before runtime evidence exists.