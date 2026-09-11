# FIRST_RUN_ACCEPTANCE_MATRIX — traceability первого забега

> Revision 3. Each AGENT_TASK R-item has exactly one acceptance row.

Source: [task](./AGENT_TASK.md).

## 1. Matrix

| ID | Requirement | Acceptance | Evidence | Status |
| --- | --- | --- | --- | --- |
| AT-01 | R-01 | 1800-second target and terminal slot | FIRST_RUN_DATA_CONTRACT.json canonical.duration_seconds and schedule | VERIFIED_ARCHITECTURE |
| AT-02 | R-02 | Six main boss records and IDs | JSON content_registry.bosses length 6 | VERIFIED_ARCHITECTURE |
| AT-03 | R-03 | Five MINI_BOSS records and IDs | JSON content_registry.mini_bosses length 5 | VERIFIED_ARCHITECTURE |
| AT-04 | R-04 | Ordered 11-record encounter schedule | JSON content_registry.encounter_schedule sorted by checkpoint | VERIFIED_ARCHITECTURE |
| AT-05 | R-05 | 10 BOSS_CHEST plus 5 ELITE_CHEST | JSON content_registry.chest_windows typed count 15 | VERIFIED_ARCHITECTURE |
| AT-06 | R-06 | Terminal encounter no chest and separate first-clear offer | Flow, state machine and JSON terminal policy | VERIFIED_ARCHITECTURE |
| AT-07 | R-07 | Conditional clock behavior by encounter kind | Flow/state clock tables and canonical.clock_policy | VERIFIED_ARCHITECTURE |
| AT-08 | R-08 | Relief then ramp then peak | Architecture WaveCycleDirector section and canonical.wave_policy | VERIFIED_ARCHITECTURE |
| AT-09 | R-09 | Registry map reconciled to 10/10/5/2 | JSON enemy_registry and REGISTRY_VARIANT_MAP.json | VERIFIED_ARCHITECTURE |
| AT-10 | R-10 | Three beetle variants with non-color marker | JSON enemy_variants and EnemyVariantResolver section | VERIFIED_ARCHITECTURE |
| AT-11 | R-11 | Exactly three artifact cards and no slot consumption | Flow, architecture ArtifactOfferSystem and JSON artifact_offer | VERIFIED_ARCHITECTURE |
| AT-12 | R-12 | Boot-to-menu end-to-end path | FIRST_RUN_FLOW.md section 2 and state graph | VERIFIED_ARCHITECTURE |
| AT-13 | R-13 | Pause, Android background, resume and recovery | Flow section 7 and state transitions T-18 to T-26 | VERIFIED_ARCHITECTURE |
| AT-14 | R-14 | Save/restore schema and quarantine | Architecture persistence section and JSON schema_migration | VERIFIED_ARCHITECTURE |
| AT-15 | R-15 | XP, aftermath, ledger and idempotency | Event catalog critical payload rules and state transition table | VERIFIED_ARCHITECTURE |
| AT-16 | R-16 | State/event/data alignment | 33 transitions, event catalog and JSON contract cross-check | VERIFIED_ARCHITECTURE |
| AT-17 | R-17 | Status separation and no runtime/APK claim | README, REPO_CONTEXT and ARCHITECTURE_AUDIT | VERIFIED_ARCHITECTURE |
| AT-18 | R-18 | Architecture gate plus external handoffs | ARCHITECTURE_AUDIT pending owners and blockers | VERIFIED_ARCHITECTURE |

## 2. Status interpretation

VERIFIED_ARCHITECTURE means static documents and cross-references satisfy the architecture gate. It does not mean Runtime implemented, Balance locked, visual approved or APK tested. PARTIAL/BLOCKED external statuses are recorded in ARCHITECTURE_AUDIT.md.

## 3. Required static gates

- Both JSON files parse.
- Encounter schedule is sorted and contains six main plus five mini records.
- Chest registry contains ten BOSS_CHEST and five ELITE_CHEST records; terminal record has no chest.
- Transition table has 33 rows, each with trigger, guard, owner, side effects, failure, recovery and duplicate behavior.
- Event names, producers, consumers and payload fields align with state machine and JSON.
- Internal links resolve inside this package.
- No changes leave docs/architecture/first-run/.
- No numeric value absent from B1 is promoted to canonical.
