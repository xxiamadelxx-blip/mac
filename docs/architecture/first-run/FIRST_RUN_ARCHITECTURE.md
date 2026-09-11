# FIRST_RUN_ARCHITECTURE — логические границы и data flow

> Revision 3. Godot 4.x / GDScript target architecture. No runtime code is changed by this package.

Source: [data contract](./FIRST_RUN_DATA_CONTRACT.json); static acceptance: [matrix](./FIRST_RUN_ACCEPTANCE_MATRIX.md).

## 1. Цель и ограничения

Architecture separates orchestration, simulation, content and persistence so the first vertical slice can be small without making UI authoritative. The contract is for a 1800-second run with six main and five mini encounters.

## 2. Sources and registry

ContentLoader reads the v3 JSON contract and the published registry map at docs/agents/architecture/REGISTRY_VARIANT_MAP.json. The map is the authority for 10 ordinary records, 10 elite catalog IDs, max 5 run-active elite records and 2 compatibility records. Content CATALOG_INDEX sync_01 supplies the five proposed extension encounters. B1 supplies numbers; unresolved values retain PENDING_B1.

## 3. Module boundaries

### AppShell and ContentLoader

AppShell owns boot, menu, Android pause/foreground signal and diagnostics. ContentLoader validates schema version, content version, required IDs, resource references and registry map checksum. Neither module mutates RunSession rewards.

### MenuFlow and RunSetupModel

MenuFlow owns navigation. RunSetupModel owns selected hero, seed and run creation request. Artifact effects are not selected here and are not a pre-run loadout.

### RunCoordinator

RunCoordinator orchestrates transition requests, delegates domain work and increments state revision after committed effects. It does not calculate XP, damage, chest outcome or wallet values.

### RunSession aggregate

RunSession owns run ID, hero, content version, seed, elapsed clocks, wave cycle, encounter cursor, build, active artifacts, drops, pending offers, diagnostics and ledger reference.

### Simulation layer

SimulationClock exposes visible elapsed time and separate encounter elapsed time. WaveCycleDirector consumes schedule boundaries and emits relief/ramp/peak phase changes. CombatSystem resolves damage and contact. ProgressionSystem consumes XPDrop once per item. ControlledSpawner allocates ordinary and elite instances through pools. BossDirector owns telegraph, encounter pattern and authoritative defeat.

### EncounterSchedule and checkpoint registry

The registry contains 11 ordered records:

| Order | Time | Seconds | Kind | ID | Outcome |
| --- | --- | --- | --- | --- | --- |
| 1 | 05:00 | 300 | MAIN_BOSS | boss_hua_lin | reward then BOSS_CHEST |
| 2 | 07:30 | 450 | MINI_BOSS | miniboss_ink_jade_warden | reward then BOSS_CHEST |
| 3 | 10:00 | 600 | MAIN_BOSS | boss_miyeon | reward then BOSS_CHEST |
| 4 | 12:30 | 750 | MINI_BOSS | miniboss_veil_harvester | reward then BOSS_CHEST |
| 5 | 15:00 | 900 | MAIN_BOSS | boss_seika | reward then BOSS_CHEST |
| 6 | 17:30 | 1050 | MINI_BOSS | miniboss_lotus_ritekeeper | reward then BOSS_CHEST |
| 7 | 20:00 | 1200 | MAIN_BOSS | boss_tideglass_regent | reward then BOSS_CHEST |
| 8 | 22:30 | 1350 | MINI_BOSS | miniboss_bell_rhythm_ascetic | reward then BOSS_CHEST |
| 9 | 25:00 | 1500 | MAIN_BOSS | boss_omen_paper_archivist | reward then BOSS_CHEST |
| 10 | 27:30 | 1650 | MINI_BOSS | miniboss_moonroot_ferryman | reward then BOSS_CHEST |
| 11 | 30:00 | 1800 | MAIN_BOSS | boss_black_moon_empress | victory after settlement |

UI renders a projection; it cannot create an encounter. MAIN_BOSS and MINI_BOSS are explicit encounter kinds. The terminal record has no chest reference.

### WaveCycleDirector

After every non-final encounter it emits POST_BOSS_RELIEF, then RAMP, then PRE_BOSS_PEAK. MAIN_BOSS freezes visible pressure and ordinary spawning through settlement. MINI_BOSS does not. Budget, active-cap and multiplier numbers are B1 data.

### EnemyVariantResolver

Inputs are content version, run seed, wave cycle ID, base enemy ID and state revision. It resolves ordinary visual variants and elite catalog candidates deterministically, records variant ID and variant class, and never creates a second reward boundary. A palette-only distinction is invalid; each beetle variant requires a readable detail.

### ChestWindowRegistry and ChestResolver

There are 10 configured BOSS_CHEST windows, one per non-final main or mini encounter, and 5 reserved ELITE_CHEST windows. Each window has one source, one offer and one claim boundary. BOSS_CHEST resolves synergy/evolution or fallback. ELITE_CHEST resolver remains pending Balance/Product policy. The terminal encounter cannot open a chest.

## 4. Content and build modules

### Content Registry

Registry fields include stable IDs, encounter kind, checkpoint seconds, status, source registry reference and pending binding references. Names and mechanics may remain proposed; architecture must not hide that status.

### BuildInventory

Weapons and passives have independent slots and level/rank rules. Artifact instances are run modifiers and are not stored in either slot collection.

### SynergyEvaluator

It evaluates eligible weapon/passive pairs at a non-final BOSS_CHEST. It uses the global synergy claim cap and idempotency key. If no pair exists, it delegates to pending fallback policy.

### ArtifactOfferSystem

An elite source or first-clear boundary creates exactly three candidate cards. Get selects one. Refresh is subject to a pending product policy. The chosen artifact effect is scoped to the run and is separate from chest and result commit boundaries.

## 5. Reward boundary and idempotency

XP collection, aftermath cleanup, checkpoint settlement, chest claim, artifact choice and result wallet commit are distinct operations. Every operation carries run ID, state revision, source ID and idempotency key. RewardLedger is the only persistent commit owner. Replayed events return the existing committed result.

## 6. Persistence and recovery

SaveSnapshot includes schema version 3, content version, registry map reference, run seed, schedule cursor, encounter kind, visible clock state, separate encounter clock, state revision, ledger revision, pending offers and checksum. Unknown IDs are quarantined and block authoritative restore. v1/v2 snapshots need an explicit adapter; no silent reinterpretation.

## 7. Data and event flow

ContentLoader → RunCoordinator → RunSession → SimulationClock/WaveCycleDirector → CombatSystem/ProgressionSystem/BossDirector → RewardLedger/SaveSnapshot → UI projections. Events are transport and diagnostics, not a second source of truth. Event payloads carry stable registry IDs and state revision.

## 8. Vertical delivery slices

1. Static loader and RunSession construction with the v3 schema.
2. One ordinary enemy, one XP pickup, one level-up offer and one upgrade choice.
3. One mini encounter proving clocks continue and one main encounter proving visible clocks freeze.
4. Checkpoint settlement, BOSS_CHEST idempotency and terminal no-chest path.
5. Pause/background/restore and result ledger replay tests.
6. Elite resolver projection with max-five limit and three beetle visual-variant records.

## 9. Status boundary

Designed and target are documented above. Implemented means Runtime has code. Verified means a reproducible test or Godot evidence exists. This architecture package verifies static contracts only.

## 10. Explicit non-goals

No runtime code, scenes, assets, balance values, artistic approval, APK or Godot stdout are changed or declared complete.
