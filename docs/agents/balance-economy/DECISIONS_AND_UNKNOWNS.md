# Decisions and Unknowns — REF-BALANCE-REF-01

This file records decisions for the 30-minute balance model. It does not amend B1, runtime code or content IDs.

## Decisions captured

| Decision | Status | Model consequence |
|---|---|---|
| Run lasts 30 minutes | USER / ARCHITECTURE DURATION | visible duration = 1800s; B1 numeric extension remains proposed |
| Six main checkpoints | USER / ARCHITECTURE SHAPE | 05:00, 10:00, 15:00, 20:00, 25:00, 30:00 |
| Five mini-boss windows | USER / SYNC LOCK | 07:30, 12:30, 17:30, 22:30, 27:30; two IDs/kits remain pending |
| Main boss clock behavior | USER PRODUCT RULE | visible run, wave, XP and ordinary-spawn clocks freeze; encounter clock continues |
| Mini-boss clock behavior | SYNC LOCK / MODEL PROPOSAL | visible run, wave, XP and ordinary spawning continue |
| Post-main density | USER PRODUCT RULE | recovery below prior peak, then monotonic ramp, then peak siege |
| Post-mini density | MODEL PROPOSAL | no reset/no immediate hard spike; current ramp continues and one finite elite pack may follow defeat |
| Elite variants | USER / ARCHITECTURE BOUNDARY | finite, max five event packs, no permanent roster mutation |
| Final boss chest | ARCHITECTURE CANON | final main boss has no boss chest |
| Offer surface | PRODUCT / ARCHITECTURE | artifact offer is exactly three cards; choose one; separate from boss chest and wallet |
| External references | TASK RULE | structural patterns only; no foreign numbers, IDs, loot odds, assets or code copied |

## Numeric provenance boundary

- B1 CANON remains unchanged for hero stats, five bands, XP formula/drop vocabulary, 0.8s contact gate, checkpoint reward arithmetic and acceptance targets.
- DERIVED values are formulas over B1/architecture/user schedule and are labeled in \`BALANCE_MODEL.json\`.
- 20:00–30:00 wave/XP anchors, late boss/mini kits, elite overlay, pack size/cadence, fallback strength and extension wallet rows are PROPOSED or PENDING.
- No absent value is silently promoted to CANON. Each model field has source, formula, rationale and status.
- External references establish only separable system boundaries: threshold progression, keyed wave pressure, explicit encounter states and separate loot/offer resolution.

## Open blockers

| Missing input / conflict | Impact | Owner | Status |
|---|---|---|---|
| Architecture says elapsed time advances through bosses | runtime cannot satisfy main freeze without contract reconciliation | Architecture/Runtime | BLOCKED |
| Architecture registry has three intermediate records, model target has five | two mini IDs/kits cannot be joined | Content/Architecture | BLOCKED |
| Two new main IDs and three missing mini records | no production encounter join | Content/Architecture | BLOCKED |
| B1 ends its numeric run at 20:00 | late bands, XP and rewards cannot become CANON | Product/B1 owner | PENDING_B1 |
| Absolute enemy base HP/ATK/speed and exact ranged/crit values | TTK/damage remains model proposal | Balance/B1 owner | PENDING_B1 |
| Elite variant numeric/visual records | TTK, cap and readability cannot be runtime-verified | Content/Balance/Visual | PENDING |
| Artifact exact effects, refresh, duplicate stacking and cadence | reward economy cannot be closed | Product/Balance | PENDING_PRODUCT_DECISION |
| Fresh-profile success target | current model completes 2/10 fresh runs | Product/Balance | PENDING_PRODUCT_DECISION |
| Godot trace and Android FPS | model cannot prove playability or performance | Runtime/CI | BLOCKED |

## What was completed in this slice

- Read live B1 and root instructions.
- Added pattern provenance to the single balance model.
- Replaced the published stale 20-minute model with the existing 30-minute v0.4 model; no numeric B1 values were changed.
- Synchronized wave, combat, XP/reward and acceptance documents.
- Re-ran deterministic validator and independent 30-run repeat check.

## Next action

Runtime/Architecture must reconcile the main-boss freeze and five-mini registry, then consume \`BALANCE_MODEL.json\` and emit the same seed-set traces.
