# Runtime Handoff — R2 content gate and replay-safe outcomes

## 1. Work identity

- Repository: `xxiamadelxx-blip/mac`
- Branch: `main`
- HEAD: the publication commit containing this report; exact SHA is supplied with the GitHub commit handoff
- Parent: `9a025c2186ba30280f1e68e122a554fa262bd0f8`
- Slice: R2 — content readiness, wave admission and boss/chest replay seams
- Status: `PARTIAL` / `BLOCKED`
- Content version: `moonveil_first_run_balance:0.1@6aa4ec96afc8a8c9e6a35c164c99e7d62910a687`
- Runtime test inputs: 101, 202, 303

## 2. Scope

### Changed files

- `scripts/runtime/content_registry.gd` — explicit R2 content status, normalized main/mini/elite records, bounded wave-envelope lookup and per-chest eligibility lookup.
- `scripts/runtime/wave_director.gd` — registry-backed spawn admission and active-cap rejection.
- `scripts/runtime/boss_director.gd` — stable ID normalization and replay-safe defeat facts.
- `scripts/runtime/run_session.gd` — snapshot/restore fields for boss defeat and checkpoint settlement outcomes.
- `scripts/runtime/run_coordinator.gd` — wave admission integration, generic chest source fields and duplicate-safe boss/checkpoint outcomes.
- `scripts/runtime/r2_runtime_test.gd` — focused R2 gate and policy test.

### Boundary check

- Runtime scripts and runtime evidence only: PASS.
- `docs/architecture/first-run/` changed: NO.
- `docs/agents/balance-economy/` or B1 changed: NO.
- `visual_lab/`, `docs/mockups/`, scenes, assets, audio changed: NO.
- Reset, rebase, force-push or history rewrite: NO.

## 3. Implemented contract

| Contract | Source | Runtime seam | Current evidence | Status |
|---|---|---|---|---|
| Content readiness | RUNTIME_CONTEXT + synchronized B1 boundary | `ContentRegistry.get_r2_content_status()` | Live B1 exposes 4 main, 0 mini, 0 elite, 1200-second duration and 1200-second wave coverage; status is `PENDING_CONTENT_SYNC` | BLOCKED by source sync |
| Wave band lookup | B1 `wave_bands` | `ContentRegistry.get_wave_band_for_time()` and `WaveDirector.evaluate_spawn()` | Last band is no longer silently extended beyond its declared end; active-cap admission is explicit | IMPLEMENTED, runtime unverified |
| Main/mini boss IDs | Registry records | `ContentRegistry` normalization + `BossDirector` lookup | Supports `boss_id`, `mini_boss_id` and future `id` records without inventing roster entries | IMPLEMENTED, runtime unverified |
| Main boss policy | RUNTIME_CONTEXT | Existing `SimulationClock` plus R2 test seam | Main freeze remains in existing code; duplicate defeat now returns the stored outcome | IMPLEMENTED, runtime unverified |
| Mini boss policy | RUNTIME_CONTEXT | Existing `SimulationClock` plus explicit missing-content result | Missing mini content returns `MINI_BOSS_CONTENT_PENDING`; no encounter is invented | BLOCKED by source sync |
| Chest separation | Architecture/runtime contract | `BOSS_CHEST`, `MINI_BOSS_CHEST`, `ELITE_CHEST` source fields | Offers carry `source_kind`, `source_id`, `chest_window_id` and independent eligibility lookup; final main boss path remains chest-free | IMPLEMENTED, runtime unverified |
| Reward idempotency | Architecture reward contract | `RewardLedger` plus session outcome replay maps | Boss defeat and checkpoint settlement replays return stored outcomes | IMPLEMENTED, runtime unverified |
| R2 gate | Runtime acceptance | `r2_runtime_test.gd` | Current expected result is `status=BLOCKED` with explicit content blockers; it must not report green R2 | BLOCKED |

## 4. Verification

- Pre-change red signal: PASS by inspection of live B1 and `r3_runtime_test.gd`; current source had 4/0/0 content and a silent mini-roster return.
- B1 JSON parse: PASS.
- Static GDScript delimiter/function scan on changed files: PASS; no duplicate function names, unbalanced delimiters or trailing whitespace.
- Expected R2 gate result from live content: `PENDING_CONTENT_SYNC` with blockers `MAIN_BOSS_ROSTER_COUNT`, `MINI_BOSS_ROSTER_COUNT`, `ELITE_VARIANT_CONTENT`, `RUN_DURATION_CONTENT`, `WAVE_ENVELOPE_CONTENT`.
- Godot focused test: not run locally; no Godot executable is installed in the workspace.
- CI runtime stdout/exit code: unavailable; the configured GitHub runner previously failed before allocating steps. No fabricated Godot trace is claimed.
- Local `git diff --check`: unavailable because there is no local checkout; whitespace scan on the prepared tree passed.

## 5. Status separation

- R1: `RUNTIME_VERIFIED` only by the prior R1 handoff evidence.
- R2: `PARTIAL/BLOCKED`; code seams are implemented, but synchronized content and executable Godot evidence are missing.
- R3: `RUNTIME_VERIFICATION_BLOCKED`; no new R3 claim is made by this slice.
- R4: `BLOCKED`; Android/APK is out of scope.

## 6. Blockers and next action

### Blocked

1. Balance/content owner must publish the synchronized 30-minute B1 records: six main bosses, five mini-bosses, bounded elite variants and wave bands covering the target envelope.
2. A functional Godot runner must execute `r2_runtime_test.gd` and capture stdout plus exit status.
3. Only after both checks pass may R2 move to `RUNTIME_VERIFIED`.

### Pending product decisions

- Exact elite eligibility, expiry and chest mapping remain source-owned; runtime returns pending status instead of inventing values.
- Mini-boss and elite numeric cadence remain pending synchronized content.

## 7. Handoff

- Balance/content owner: synchronize the missing R2 records without changing runtime-owned idempotency rules.
- Runtime owner: run the focused R2 test after synchronization and attach deterministic policy traces.
- Next slice: R2 full wave/boss/mini/elite runtime execution evidence.
- First check: parse the new B1 model and assert `ContentRegistry.get_r2_content_status().status == READY` before running gameplay traces.
