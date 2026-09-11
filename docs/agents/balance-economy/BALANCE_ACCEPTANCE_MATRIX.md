# Balance Acceptance Matrix — SYNC-04

Status: `PARTIAL / MODEL_ONLY`. Structural R2 rows are runtime-verified on the prior model; numeric balance rows remain model-only.

| Requirement | Source | Evidence | Status | Next gate |
|---|---|---|---|---|
| Live B1 read | `docs/BALANCE_ECONOMY_SPEC.md` | SHA `6aa4ec96afc8a8c9e6a35c164c99e7d62910a687` | PASS / source | Balance |
| Parent synchronization | live `main` | `7a8112e9bb3175d6c86030b14e680ce01b4e1254` | PASS / source | Publication |
| Full content catalog | mockups + C1/C2/C3 | 10 weapons, 10 passives, 10 synergies, 10 artifacts, 10 ordinary, 10 elite, 6 main, 5 mini | PASS / MODEL | Content/Architecture |
| Numeric provenance | B1 boundary | every content number has source/formula/rationale/status | PASS / MODEL | B1/Product promotion |
| B1 numeric profiles | B1 roles/targets + mockup descriptions | explicit HP/ATK/speed/XP profiles for 10 ordinary, 10 elite, 6 main and 5 mini records; absent absolutes remain PROPOSED/DERIVED | PASS / MODEL / PROPOSED | B1 promotion |
| 30-minute envelope | user decision + sync lock | 1800s, 7 contiguous bands | PASS / MODEL | Architecture/B1 |
| Main roster | sync lock | 6 at 300/600/900/1200/1500/1800 | PASS / R2 structural join; numeric model pending fresh trace | Runtime |
| Mini roster | sync lock | 5 at 450/750/1050/1350/1650 | PASS / R2 structural join; numeric model pending fresh trace | Runtime |
| Registry ID join | REF-ARCH-02 live map `0b8cb1bb96d4ab2d0bd14bd7a21b042e53d8c5e8` | 10 ordinary + 10 elite IDs; 2 legacy IDs excluded | PASS / R2 structural join | Runtime/Architecture |
| Elite selection | sync lock / REF-ARCH-02 | catalog 10, deterministic ELITE_CHEST projection ≤5 | PASS / R2 structural join; values model-only | Runtime/Visual |
| Main-boss freeze | sync lock | visible/wave/XP/spawn stop in all 6 model events | PASS / R2 policy trace; new numeric trace pending | Runtime |
| Mini continuation | sync lock | visible/wave/XP/spawn continue in all 5 model events | PASS / R2 policy trace; new numeric trace pending | Runtime |
| Post-boss ramp | user rule + B1 relief principle | relief → monotonic ramp → peak siege, 5 cycles | PASS / MODEL | Runtime |
| Active cap | B1 cap rule | no model occupancy over selected cap | PASS / MODEL | Runtime/CI |
| XP formula and target | B1 §6 + user XP request | unchanged threshold formula; target level 40, accepted floor 38; late pickup 22/27 XP/s | PASS / MODEL | B1/Product promotion |
| Fresh/moderate/max replay | B1 profile target + user XP request | 30 runs; 30 survive and complete; every run has 3 distinct synergies; final levels 40/41/44 | PASS / MODEL | Product/B1 |
| Three distinct synergies | C1 10/10 gate + user XP request | paired progression reaches 3 unique synergy IDs in all 30 model runs | PASS / MODEL / PROPOSED | Runtime progression join |
| Ordinary TTK | B1 target | means 0.50–1.25s; p95 outliers exposed | PASS / MODEL; watch | Balance/B1 |
| Elite-variant TTK | proposed 5–15s | representative means 3.75–9.00s; p95 up to 15.50s | PARTIAL / PROPOSED | Balance/B1 |
| Main/mini TTK | B1 + proposed extension | concrete sequences in combat report | PARTIAL / PROPOSED | Balance/B1 |
| Incoming risk | B1 15% base-HP target | worst model hit 13.72/100 = 13.72% | PASS / MODEL; runtime watch | Balance/B1/Runtime |
| Rewards | B1 + proposed extension | first clear 1575/520/16; repeat 1275/340/15 | PARTIAL / PROPOSED | Product/B1 |
| Chests/fallback | architecture policy | final no chest; fallback and separate artifact offers | PASS / MODEL | Runtime |
| ELITE_CHEST cadence | reserved five-window policy + proposed B1 overlay | 07:30/12:30/17:30/22:30/27:30; 3 cards; no wallet mutation; one idempotency key per window | PASS / MODEL / PROPOSED | Runtime/Product |
| Idempotency | ledger policy | wallet/chest/elite/first-clear duplicate checks pass | PASS / MODEL | Runtime |
| Godot 30-minute numeric run | Runtime acceptance | R2 structural evidence exists; fresh trace for this resulting model absent | BLOCKED | Runtime/CI |
| Android FPS/occupancy | B1 performance gate | no device/runner evidence | BLOCKED | CI/QA |

## Provenance rule

`CANON` is reserved for values actually stated in B1. `DERIVED` means a
calculation from explicit records. `PROPOSED` means a missing absolute value
chosen to make the model checkable. The validator rejects missing provenance;
it does not convert Architecture/Content drift into a false green join.

## Boundary

The model and independent replay are reproducible. The package cannot be
`VERIFIED` for numeric gameplay until the runtime produces a fresh trace for
this resulting model and the later R3/R4 gates are satisfied.
