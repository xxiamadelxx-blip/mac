# Runtime Handoff — SYNC-04 R2 live registry verification

## 1. Work identity

- Repository: xxiamadelxx-blip/mac
- Branch: main
- Parent HEAD: 560ced8b23013449f70d240567617fd7e6833956
- Resulting HEAD: publication commit returned with this handoff update
- Slice: SYNC-04 / R2 BALANCE_MODEL-to-live-registry reconciliation
- Status: RUNTIME_VERIFIED for the R2 registry, wave and boss-policy acceptance slice
- Canonical engine: Godot 4.x / GDScript
- Historical requested trace SHA: 7af78c63997b54edc78a6905613cbd61f489265b; it is not the current main HEAD and is not used as current evidence
- Current content version: moonveil_first_run_balance:0.1@6aa4ec96afc8a8c9e6a35c164c99e7d62910a687
- Balance model status: PARTIAL remains unchanged by design; proposed late-run values are not promoted by R2

## 2. Outcome

The live runtime now reads BALANCE_MODEL.json through ContentRegistry and validates a joined view against the verified architecture contract and the Architecture/Product registry map. R2 fails closed on a missing or inconsistent join; it does not invent mini-bosses, elite variants, chest windows, or numeric balance values.

No Balance or architecture data file was modified for this reconciliation. The existing contract already contains the reconciled target: six main bosses, five mini-bosses, ten elite catalog records, a five-record active elite projection, fifteen chest windows, and the MAIN_BOSS freeze / MINI_BOSS continue clock policy.

## 3. Live registry join

| Input | Runtime source and check | Current evidence | Status |
|---|---|---|---|
| Balance model | res://docs/agents/balance-economy/BALANCE_MODEL.json via ContentRegistry.DEFAULT_PATH | model_id moonveil_first_run_balance; declared and covered duration 1800 seconds | PASS |
| Main bosses | BALANCE_MODEL.json main_bosses joined to contract content_registry.bosses | 6 stable IDs joined | PASS |
| Mini bosses | BALANCE_MODEL.json mini_bosses joined to contract content_registry.mini_bosses and encounter_schedule | 5 stable IDs joined | PASS |
| Ordinary roster | REGISTRY_VARIANT_MAP.json ordinary_roster joined to contract and simulation_model.enemy_stats | 10 mapped records; 2 legacy records quarantined separately | PASS |
| Elite variants | BALANCE_MODEL.json elite_variants joined to contract and elite_variant_catalog | 10 catalog IDs joined; active runtime projection limit is 5 | PASS |
| Chest windows | architecture contract content_registry.chest_windows | 15 total: 10 BOSS_CHEST and 5 ELITE_CHEST; final main boss has no chest reference | PASS |
| Encounter schedule | architecture encounter_schedule joined by ID, kind, time and final flag | all 11 encounter records joined | PASS |
| Clock policy | architecture canonical.clock_policy | MAIN_BOSS freezes visible run clock; MINI_BOSS continues it | PASS |
| Wave envelope | BALANCE_MODEL.json wave_bands | contiguous coverage from 0 through 1800 seconds | PASS |

## 4. Implemented runtime seam

The live implementation includes:

- ContentRegistry loading BALANCE_MODEL.json plus the architecture contract and registry map.
- ContentRegistry.get_live_registry_join_status() with stable-ID, schedule, count, chest and clock-policy diagnostics.
- ContentRegistry.get_r2_content_status() returning READY only when the joined registry is valid.
- Deterministic elite selection from the ten-record catalog with a maximum active projection of five.
- WaveDirector and SpawnDirector enforcing the registry-backed wave and active-cap policy.
- RunCoordinator and R2 acceptance coverage for main-boss freeze, mini-boss continuation, final-boss chest absence, checkpoint chest claims and duplicate-safe outcomes.
- A bounded GitHub Actions R2 command that records Godot import and test exit files plus stdout artifacts.

The following runtime/CI commits are part of the live main history: 4109881 (registry parser fix), 6842616 (coordinator types), 75e2828 (wave/director types), fdd8e82 (spawn/director types), 4f0582f (final null chest policy), 560ced8 (R2 marker check).

## 5. Fresh R2 evidence

The fresh trace was executed from an evidence branch created from live `main` HEAD `105b5ca75bda73fd61ddca52c169a14e193e32ae`. The evidence branch changed only the R2 workflow branch filter so GitHub Actions could start a push-triggered run; the runtime code, architecture contract, registry map and published `BALANCE_MODEL.json` were inherited unchanged from `main`.

- Source baseline: `main` `105b5ca75bda73fd61ddca52c169a14e193e32ae`
- Published balance blob: `docs/agents/balance-economy/BALANCE_MODEL.json` SHA `5732a34c0eaa27b7d429b75b0343e1015daa0cb0`
- Evidence branch: `agent/runtime-r2-fresh-105b5ca`
- Evidence HEAD: `c8471f7532052aa00cb2fbbfcde18b9092398c0a`
- Run: https://github.com/xxiamadelxx-blip/mac/actions/runs/34645155164
- Run number: 12
- Job: `103414041567` — Godot R2 registry and policy acceptance
- Runner image: `barichello/godot-ci:4.7.2`
- Godot: `4.7.2.stable.official.ed1daf0bf`
- Workflow/job conclusion: success
- Artifact: https://github.com/xxiamadelxx-blip/mac/actions/runs/34645155164/artifacts/10281057852
- Artifact ID/digest: `10281057852` / `sha256:fc040fad282e8de0e9b1897a2f2468eb12def310e6492b8dbb860cc9f87ccf6b`
- Artifact exit evidence: `godot-import.exit=0`; `r2-runtime-test.exit=0`
- Stdout markers: `R2_RUNTIME_TEST {"ok":true,...,"status":"TESTED"}`; `R2_RUNTIME_TRACE {"ok":true,...,"status":"TESTED"}`
- Joined registry: `READY`; model status remains `PARTIAL` as a balance-governance status, not a runtime failure
- 30-minute envelope: `target_duration_seconds=1800.0`; `wave_coverage_end_seconds=1800.0`
- Joined counts: 6 main bosses, 5 mini-bosses, 10 elite catalog records, 5 active elite limit, 15 chest windows
- Policy assertions: `main_boss_freezes=true`, `mini_boss_continues=true`, final main boss has no chest, all five mini-boss paths produce `MINI_BOSS_CHEST`, seed 505 selects 5 from the 10-record elite catalog

The log contains only environment warnings for missing fontconfig/ADB support; it contains no Godot/GDScript parse or script errors. The exact stdout and exit files are retained in the artifact above.

## 6. Verification and status separation

- BALANCE_MODEL.json remains PARTIAL because late extension values are still proposed; R2 verifies consumption and structural joins, not balance approval.
- R2 registry/policy acceptance is RUNTIME_VERIFIED by the successful Godot CI evidence above.
- Full combat gameplay, Android background lifecycle, APK packaging and device performance are not claimed complete by this handoff.
- R3/full gameplay verification requires its own acceptance scope and evidence; it is not silently promoted by R2.
- No Unity migration, visual asset generation, PNG/SVG/Base64/ZIP creation, or balance-file edit was performed.

## 7. Blockers and one next action

No blocker remains for the R2 BALANCE_MODEL-to-live-registry join.

External pending work remains intentionally separated: Balance owns promotion of proposed late-run numbers, while the broader gameplay/APK evidence belongs to later runtime/QA slices.

### Next action

Core Gameplay Runtime Agent extends this verified registry seam into the next gameplay vertical slice and attaches a separate Godot trace.
