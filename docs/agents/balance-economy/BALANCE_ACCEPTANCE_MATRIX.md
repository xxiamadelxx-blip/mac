# Balance Acceptance Matrix — SYNC-03

Status: `PARTIAL / MODEL_ONLY`. No row below is runtime-verified.

| Requirement | Source | Evidence | Status | Next gate |
|---|---|---|---|---|
| Live B1 read | `docs/BALANCE_ECONOMY_SPEC.md` | SHA `6aa4ec96afc8a8c9e6a35c164c99e7d62910a687` | PASS / source | Balance |
| Parent synchronization | live `main` | `68ac3cc141f889381a458e08f9042d18e2fd3a7a` | PASS / source | Publication |
| Full content catalog | mockups + C1/C2/C3 | 10 weapons, 10 passives, 10 synergies, 10 artifacts, 10 ordinary, 10 elite, 6 main, 5 mini | PASS / MODEL | Content/Architecture |
| Numeric provenance | B1 boundary | every content number has source/formula/rationale/status | PASS / MODEL | B1/Product promotion |
| 30-minute envelope | user decision + sync lock | 1800s, 7 contiguous bands | PASS / MODEL | Architecture/B1 |
| Main roster | sync lock | 6 at 300/600/900/1200/1500/1800 | PASS / MODEL; join pending | Architecture/Content |
| Mini roster | sync lock | 5 at 450/750/1050/1350/1650 | PASS / MODEL; join pending | Architecture/Content |
| Elite selection | sync lock / REF-ARCH-02 | catalog 10, runtime projection ≤5 | PASS / MODEL | Runtime/Visual |
| Main-boss freeze | sync lock | visible/wave/XP/spawn stop in all 6 model events | PASS / MODEL | Runtime |
| Mini continuation | sync lock | visible/wave/XP/spawn continue in all 5 model events | PASS / MODEL | Runtime |
| Post-boss ramp | user rule + B1 relief principle | relief → monotonic ramp → peak siege, 5 cycles | PASS / MODEL | Runtime |
| Active cap | B1 cap rule | no model occupancy over selected cap | PASS / MODEL | Runtime/CI |
| XP formula | B1 §6 | formula read from JSON; levels at 2/5/10/15/20/25/30 | PASS / MODEL | B1 for late anchors |
| Fresh/moderate/max replay | B1 profile target | 30 runs; 29 survive and complete | PASS / MODEL; fresh Lin watch | Product/B1 |
| Ordinary TTK | B1 target | means 0.50–1.25s; p95 outliers exposed | PASS / MODEL; watch | Balance/B1 |
| Elite-variant TTK | proposed 5–15s | representative means 3.75–9.00s; p95 up to 15.50s | PARTIAL / PROPOSED | Balance/B1 |
| Main/mini TTK | B1 + proposed extension | concrete sequences in combat report | PARTIAL / PROPOSED | Balance/B1 |
| Incoming risk | B1 15% base-HP target | worst model hit 14/90 = 15.56% | PARTIAL / WATCH | Balance/B1/Runtime |
| Rewards | B1 + proposed extension | first clear 1575/520/16; repeat 1275/340/15 | PARTIAL / PROPOSED | Product/B1 |
| Chests/fallback | architecture policy | final no chest; fallback and separate artifact offers | PASS / MODEL | Runtime |
| Idempotency | ledger policy | wallet/chest/elite/first-clear duplicate checks pass | PASS / MODEL | Runtime |
| Godot 30-minute run | Runtime acceptance | no invocation/stdout/exit code | BLOCKED | Runtime/CI |
| Android FPS/occupancy | B1 performance gate | no device/runner evidence | BLOCKED | CI/QA |

## Provenance rule

`CANON` is reserved for values actually stated in B1. `DERIVED` means a
calculation from explicit records. `PROPOSED` means a missing absolute value
chosen to make the model checkable. The validator rejects missing provenance;
it does not convert Architecture/Content drift into a false green join.

## Boundary

The model and independent replay are reproducible. The package cannot be
`VERIFIED` until the live runtime consumes the JSON and produces R2/R3 evidence.
