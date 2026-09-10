# Runtime Handoff — SYNC-04 R2 registry reconciliation checkpoint

## 1. Work identity

- Repository: `xxiamadelxx-blip/mac`
- Branch: `main`
- Parent HEAD: `4dce51b2b86957533faa20b668f8725a112b4a20`
- Resulting HEAD: exact SHA is supplied with the GitHub commit handoff
- Slice: `SYNC-04` / R2 registry reconciliation after the content `SYNC-01` handoff
- Status: `PARTIAL` / `BLOCKED`
- Runtime implementation baseline: `af2b7fbdd4d155e1d8e2ae3ad48690eac342792c`
- Content version: `moonveil_first_run_balance:0.1@6aa4ec96afc8a8c9e6a35c164c99e7d62910a687`
- Runtime test inputs: 101, 202, 303

## 2. This follow-up

This commit refreshes this handoff against the live `main` after external Content and Balance updates. It changes no runtime source, architecture, balance, content or visual files.

The content handoff `SYNC-01` is present and valid as a content-only proposal: five records, all `PROPOSED`, all `PENDING_ARCHITECTURE`. Its promotion guard explicitly forbids runtime registration before Architecture and Balance reconciliation.

## 3. Live registry join

| Input | Live evidence | Runtime consequence | Status |
|---|---|---|---|
| Main bosses | B1 `boss_checkpoints`: 6 records | `ContentRegistry.get_main_bosses()` can consume the six-record main roster | PASS for count; numeric extension values remain proposed |
| Mini bosses | B1 exposes no top-level `mini_bosses` array and no `simulation_model.mini_bosses` array | Runtime must return `MINI_BOSS_CONTENT_PENDING`; it must not read proposal IDs as canonical | BLOCKED |
| Elite variants | B1 exposes no top-level `elite_variants` array and no `simulation_model.elite_variants` array | Runtime must return pending content status; no elite encounter or offer is invented | BLOCKED |
| Run envelope | B1 has 7 wave bands, contiguous=true, coverage=1800 seconds; declared duration=1800 | The envelope is structurally available, while extension values remain `PROPOSED`/model-only | PARTIAL |
| Architecture | Contract declares 6 main, 3 intermediate and 15 chest windows | Target is five mini-bosses; three intermediate records are insufficient | BLOCKED |

## 4. Canonical policy reconciliation

- Runtime code implements the user-canonical policy: `MAIN_BOSS` freezes visible run time, wave progression, XP and ordinary spawning; `MINI_BOSS` keeps them moving.
- The current architecture contract still states that the clock advances during `BOSS_INTRO` and `BOSS_ACTIVE` for every boss. This remains an unresolved cross-system conflict; runtime does not silently change the architecture document.
- Final main boss remains chest-free.
- Artifact offers remain separate from boss chest windows and do not become pre-run loadout slots.

## 5. Implemented runtime seams

- `ContentRegistry.get_r2_content_status()` exposes `READY` versus `PENDING_CONTENT_SYNC` instead of hiding missing content.
- `ContentRegistry.get_wave_band_for_time()` does not extend the last source band beyond its declared end.
- `WaveDirector.evaluate_spawn()` applies registry active-cap admission.
- `BossDirector` normalizes stable IDs and stores replay-safe defeat outcomes.
- `RunSession` snapshots boss-defeat and checkpoint-settlement replay maps.
- `RunCoordinator` carries chest source fields and preserves duplicate-safe boss, settlement and chest behavior.
- `r2_runtime_test.gd` fails closed when content is incomplete; it does not silently pass an empty mini roster.

## 6. Verification

- `CONTENT_CATALOG_INDEX.json` parse: PASS; `SYNC-01` has 5 records, all `PROPOSED`.
- `FIRST_RUN_DATA_CONTRACT.json` parse: PASS; architecture status is `VERIFIED_ARCHITECTURE`, but its intermediate-boss registry contains 3 records.
- `BALANCE_MODEL.json` parse: PASS; model status is `PARTIAL`, simulation is model-only, runtime integration is not implemented.
- Live R2 projection: `PENDING_CONTENT_SYNC`; blockers are `MINI_BOSS_ROSTER_COUNT` and `ELITE_VARIANT_CONTENT`.
- Static runtime source review from implementation baseline: PASS for delimiter balance, duplicate function/top-level variable scan, trailing whitespace and forbidden artifact-slot terminology.
- Godot focused runtime execution: not available in the workspace; no stdout or exit code is claimed.
- CI runtime evidence: no valid Godot stdout/exit-code evidence; previous runner failures occurred before step allocation.

## 7. Scope and status separation

- This follow-up changes only `docs/agents/core-gameplay-runtime/RUNTIME_HANDOFF.md`.
- No architecture, B1, content-design, Visual Lab, mockup, scene, asset or APK file is changed.
- `R1`: prior `RUNTIME_VERIFIED` evidence remains separate.
- `R2`: `PARTIAL/BLOCKED`; implementation seams exist, but joined mini/elite content and executable evidence are missing.
- `R3`: `RUNTIME_VERIFICATION_BLOCKED`.
- `R4`: `BLOCKED`; Android/APK is outside this slice.

## 8. Blockers and one next action

### Blockers

1. Architecture must reconcile the five mini-boss target and replace the advancing-all-boss clock statement with the user-canonical `MAIN_BOSS` freeze / `MINI_BOSS` continue policy.
2. Balance must publish consumable `mini_bosses[5]` and bounded `elite_variants` records with stable IDs, while keeping proposed numbers explicitly labelled.
3. CI/QA must provide a working Godot runner and capture the R2 command, stdout and exit code.

### Next action

After Architecture and Balance publish the reconciled registry, Runtime runs `godot --headless --path . --script res://scripts/runtime/r2_runtime_test.gd` and records the deterministic policy trace.