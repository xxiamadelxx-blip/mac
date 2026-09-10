<!-- LIVE-AGENT-SYNC: read docs/AGENT_SYNC_STATE.md at current main before using this file -->
> **Live coordination pointer:** continuation work is routed through [`docs/AGENT_SYNC_STATE.md`](../../AGENT_SYNC_STATE.md). Legacy 20-minute/4-boss passages below are historical until reconciled.

# Content Handoff — C5: cross-system reconciliation

## 1. Идентичность

- Repository: xxiamadelxx-blip/mac
- Branch: main
- HEAD baseline: 17803bde8e38dbf07a72e4033beacf2de5e29281 (проверен перед записью C5)
- Slice: C5
- Status: HANDOFF_READY_WITH_OPEN_RECONCILIATIONS
- Catalog version: 1
- Date: 2026-09-10

C5 закрывает content-design handoff между C1–C4, META passive tree, Architecture, Balance, Runtime и Visual Lab. Документ не объявляет runtime playable, balance locked, visual approved или production-ready.

## 2. Переданный content package

| Package | Stable content | Status | Next owner |
|---|---|---|---|
| C1 weapons/passives/synergies | 10 weapons, 10 global run passives, 10 direct evolutions; passive binding используется для synergy eligibility | CONTENT_SPECIFIED | Balance + Runtime + Visual Lab |
| C2 artifacts | 10 run artifacts, three-card offer boundary, no weapon/passive slot usage | CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING | Product + Architecture + Balance |
| C3 bosses/chests | 4 future enemy proposals, 5 named mini-boss proposals, 2 main-boss extension proposals, synergy/fallback flow | CONTENT_SPECIFIED / ROSTER_RECONCILIATION | Product + Architecture + Runtime |
| C4 arena drops | 7 typed content intents: heal, Gold, XP magnet, destruction, wave freeze, ward, vacuum | CONTENT_SPECIFIED / RUNTIME_PENDING | Architecture + Runtime + Balance |
| META passive tree | 6 branches, 17 stat nodes, Gold, next-run application | CONTENT_SPECIFIED / BALANCE_PENDING | Balance + Runtime/UI |

Detailed dependency matrix, conflict review, open decisions and acceptance evidence are in `C5_CROSS_SYSTEM_HANDOFF.md`.


## SYNC-01 — Proposed encounter registry handoff

- Canonical payload: `CONTENT_CATALOG_INDEX.json` → `sync_01`.
- Recipient owners: Architecture and Balance.
- Status: `PROPOSED`; registry status remains `PENDING_ARCHITECTURE`.
- Records: `boss_tideglass_regent` (MAIN_BOSS, 20:00 / 1200s), `boss_omen_paper_archivist` (MAIN_BOSS, 25:00 / 1500s), `miniboss_lotus_ritekeeper` (MINI_BOSS, 17:30 / 1050s), `miniboss_bell_rhythm_ascetic` (MINI_BOSS, 22:30 / 1350s), `miniboss_moonroot_ferryman` (MINI_BOSS, 27:30 / 1650s).
- Dependencies are listed per record in `sync_01.pending_records[].dependencies`.
- Promotion guard: IDs remain proposals; no runtime registration, artistic approval, balance lock or architecture approval is claimed.

## 3. Integration blockers

| ID | Blocker | Evidence | Owner |
|---|---|---|---|
| C5-P1-01 | Main-boss freeze in Runtime conflicts with all-boss advancing clock in data contract | `RUNTIME_CONTEXT.md`/`RUNTIME_ACCEPTANCE.md` vs `FIRST_RUN_DATA_CONTRACT.json` | Architecture + Runtime |
| C5-P1-02 | Mini roster is 5 in C3, 3 in data contract, 5 in runtime acceptance and 0 in live B1 Registry | Named content and live contract counts; R3 runtime handoff | Product + Content + Architecture |
| C5-P1-03 | Content/index has 10 artifacts, registry has 8 and typed effect definitions are empty | `artifact_tideglass`, `artifact_silent_lantern`, `artifact_effects.definitions` | Product + Architecture + Balance |
| C5-P1-04 | Architecture target is 30:00 while manifest/B1 evidence is legacy 20:00; Balance model extension remains proposed | `FIRST_RUN_DATA_CONTRACT.json`, `GAME_MANIFEST.md`, `BALANCE_MODEL.json` | Product + Architecture + Balance |
| C5-P1-05 | 15 chest windows are not mapped to the 5 content synergy checkpoints | 8 configured + 7 reserved vs C3 content snapshot | Product + Architecture + Balance |

До закрытия этих пунктов каталог остаётся handoff-ready, но не APPROVED/IMPLEMENTED.

## 4. Required handoff actions

1. Product/Architecture publish one decision for envelope, clock policy, mini roster and chest taxonomy.
2. Architecture syncs approved registry records, typed artifact effects, arena-drop instances/events and idempotency.
3. Balance binds numeric values, 30-minute wave/reward extension, chest cadence, C4 drop frequency/quantity and performance caps; proposed model values are not treated as lock.
4. Visual Lab ingests existing C1–C4 briefs; extension bosses/variants wait for stable identities. No mockups were created by Content.
5. Runtime/QA proves main freeze, mini continuation, five-claim cap, one offer per chest window, three artifact cards and final no-chest behavior.

## 5. Evidence and scope

- Baseline was read from live main at `17803bde8e38dbf07a72e4033beacf2de5e29281`.
- C5 updates only content-design documentation and catalog metadata.
- No architecture, balance, runtime source, Visual Lab policy or mockup files are changed.
- Existing R1 runtime verification does not prove R2/R3 boss, chest, artifact or full-wave implementation; current runtime acceptance remains NOT_IMPLEMENTED for those slices.
- R3 handoff records a verification blocker before runner/step allocation; Godot stdout and exit codes were not observed, so C5 does not claim runtime verification.
- Legacy 20-minute material is recorded as a conflict, not silently rewritten.

## 6. Next owner

Architecture/Project Owner resolves C5-P1-01…05. After that, Balance, Runtime and Visual Lab consume the handoff in the order stated above. New content ideas after C5 require a separate proposal and do not reopen this completed documentation slice.
