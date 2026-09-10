# Balance Acceptance Matrix — SYNC-03

Status: `PARTIAL / MODEL_ONLY`. No row below is `RUNTIME_VERIFIED`.

| Requirement | Source | Model/evidence | Status | Owner of next gate |
|---|---|---|---|---|
| Live B1 read | `docs/BALANCE_ECONOMY_SPEC.md` | SHA `6aa4ec96afc8a8c9e6a35c164c99e7d62910a687` stored in model | PASS / source | Balance |
| 30-minute envelope | user decision + sync lock | `1800s`, 7 contiguous bands | PASS / MODEL | Architecture/B1 |
| Main roster | sync lock | 6 arrays at 05/10/15/20/25/30 | PASS / MODEL; join pending | Architecture/Content |
| Mini roster | sync lock | 5 arrays at 07:30/12:30/17:30/22:30/27:30 | PASS / MODEL; IDs pending | Content/Architecture |
| Elite catalog | REF-ARCH-02 | 10 mapped IDs, numeric overlays, run projection ≤5 | PASS / MODEL | Runtime/Visual |
| ContentRegistry shape | `scripts/runtime/content_registry.gd` | top-level `main_bosses`, `mini_bosses`, `elite_variants` now present | PASS / Balance shape | Runtime |
| Main-boss freeze | sync lock | all 6 model events freeze visible/wave/XP/spawn clock | PASS / MODEL | Architecture/Runtime |
| Mini continuation | sync lock | all 5 model events advance visible/wave/XP/spawn clock | PASS / MODEL | Runtime |
| Post-boss ramp | B1 principle + user rule | relief → linear ramp → peak siege; 5 cycles monotonic | PASS / MODEL | Runtime |
| Active cap | B1 cap rule | no occupancy above selected cap; no spawn debt | PASS / MODEL | Runtime/CI |
| XP formula | B1 §6 | exact formula read from JSON; levels reported at 2/5/10/15/20/25/30 | PASS / MODEL | Balance/B1 for late anchors |
| Fresh/moderate/max profiles | B1 profile target | 5 seeds × 2 heroes × 3 profiles; 30/30 completed | PASS / MODEL | Product for fresh target |
| Ordinary TTK | B1 target | model means 0.50–1.25s; p95 role outliers reported | PASS / MODEL / watch | Balance/B1 |
| Elite TTK | B1 target + proposed overlay | means 3.75–12s; p95 outliers to 23.25s | PARTIAL / PROPOSED | Balance/B1/Runtime |
| Main/mini TTK | B1 + proposed extension | concrete sequences in combat report | PARTIAL / PROPOSED | Balance/B1 |
| Incoming risk | B1 15% single-hit bound | worst landed hit 12.25% of base HP | PASS / MODEL | Runtime |
| Rewards | B1 + proposed extension rows | first clear 1575/520/16; repeat 1275/340/15 | PARTIAL / PROPOSED | Product/B1 |
| Chests/fallback | architecture policy | final no chest; non-final fallback path; elite offer 3 | PASS / MODEL | Runtime |
| Idempotency | architecture ledger | wallet/chest/elite/first-clear duplicate checks pass | PASS / MODEL | Runtime |
| Godot 30-minute run | Runtime acceptance | no invocation/stdout/exit code | BLOCKED | Runtime/CI |
| Android FPS/occupancy | B1 performance gate | no device/runner evidence | BLOCKED | CI/QA |

## Required provenance rule

Every absent B1 number is represented in the model with `source`,
`derived_formula`, proposed value, rationale and a non-canonical status. The
validator rejects missing model-owned registry shape, but it does not silently
turn Architecture/Content drift into a false green join.

## Status boundary

The model and independent replay are reproducible. The overall package remains
`PARTIAL`; `VERIFIED` is intentionally unavailable until a real runtime trace
and performance evidence exist.
