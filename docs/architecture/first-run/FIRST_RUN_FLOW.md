# FIRST_RUN_FLOW — логический пользовательский маршрут первого забега

> Revision 3. Target run: 30 minutes. Runtime implemented: NO. Этот файл описывает contract, а не готовность APK.

Sources: [state machine](./FIRST_RUN_STATE_MACHINE.md), [data contract](./FIRST_RUN_DATA_CONTRACT.json), [registry map](../../agents/architecture/REGISTRY_VARIANT_MAP.json).


## 1. Границы и authority

AppShell владеет boot/menu navigation. ContentLoader загружает versioned registry. RunCoordinator оркестрирует lifecycle. RunSession владеет active state. SimulationClock и WaveCycleDirector не получают authority из UI. RewardLedger — единственная граница persistent reward commit.

## 2. Сквозной маршрут

1. Boot проверяет content version и создаёт diagnostic context.
2. Main menu открывает character selection.
3. Character selection передаёт stable hero ID в run setup.
4. Run setup фиксирует run ID, seed и content version.
5. Loading валидирует arena, schedule, registry map и required resource references.
6. Active run запускает ordinary waves и visible HUD.
7. XP pickup меняет XP ровно один раз; level-up открывает offer из трёх карт.
8. Upgrade choice меняет weapon/passive build только через BuildInventory.
9. WaveCycleDirector ведёт OPENING → RAMP → PRE_BOSS_PEAK; после каждого non-final defeat проходит POST_BOSS_RELIEF.
10. Schedule запускает main или mini encounter.
11. Non-final defeat проходит settlement, затем открывает один typed BOSS_CHEST. ELITE_CHEST имеет отдельный reserved resolver.
12. Pause и Android background создают snapshot по policy; resume восстанавливает state revision или открывает recovery.
13. Смерть идёт в defeat result. Terminal encounter после settlement идёт в victory result без chest.
14. Result finalization коммитит rewards через ledger.
15. First-clear artifact offer открывается как отдельная post-result boundary.
16. После committed result игрок возвращается в main menu.

## 3. Encounter schedule

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

Main boss на 1800 секунд — terminal encounter. Mini records не являются заменой main records. Schedule data-driven и не кодируется UI-ветками.

## 4. Clock и волны

| Encounter | Visible run clock | Wave clock | XP progression | Ordinary spawn | Separate encounter clock |
|---|---|---|---|---|---|
| MAIN_BOSS intro/active до settlement | freezes | freezes | freezes | freezes | advances |
| MINI_BOSS intro/active | advances | advances | advances | advances | advances |
| offer, pause, settlement, result | freezes | freezes | freezes | freezes | not ticked |

Boss intro не поглощает elapsed time для main visible clocks, но encounter clock продолжает измерять фазу. Mini boss остаётся частью active simulation timeline.

WaveCycleDirector обязан выполнять POST_BOSS_RELIEF перед RAMP и PRE_BOSS_PEAK. Числа budget/cap/multiplier остаются PENDING_B1.

## 5. XP, upgrades и variants

XPDrop и aftermath item — разные entities. Повторный pickup по XP item ID — no-op. Level-up создаёт ровно один offer revision. Weapon/passive slots ограничены контрактом; artifact effect туда не записывается.

EnemyVariantResolver принимает content version, run seed, wave cycle, base enemy ID и state revision. Три beetle variants имеют palette плюс читаемую detail marker. Ordinary visual variant не создаёт отдельную XP, drop, aftermath или reward boundary. Elite catalog содержит десять IDs; за один run projection активирует не более пяти.

## 6. Chest-window registry

| # | Window | Type | Encounter | Source | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | chest_window_main_01 | BOSS_CHEST | MAIN_BOSS | boss_hua_lin | CONFIGURED |
| 2 | chest_window_main_02 | BOSS_CHEST | MAIN_BOSS | boss_miyeon | CONFIGURED |
| 3 | chest_window_main_03 | BOSS_CHEST | MAIN_BOSS | boss_seika | CONFIGURED |
| 4 | chest_window_main_04 | BOSS_CHEST | MAIN_BOSS | boss_tideglass_regent | CONFIGURED |
| 5 | chest_window_main_05 | BOSS_CHEST | MAIN_BOSS | boss_omen_paper_archivist | CONFIGURED |
| 6 | chest_window_mini_01 | BOSS_CHEST | MINI_BOSS | miniboss_ink_jade_warden | CONFIGURED |
| 7 | chest_window_mini_02 | BOSS_CHEST | MINI_BOSS | miniboss_veil_harvester | CONFIGURED |
| 8 | chest_window_mini_03 | BOSS_CHEST | MINI_BOSS | miniboss_lotus_ritekeeper | CONFIGURED |
| 9 | chest_window_mini_04 | BOSS_CHEST | MINI_BOSS | miniboss_bell_rhythm_ascetic | CONFIGURED |
| 10 | chest_window_mini_05 | BOSS_CHEST | MINI_BOSS | miniboss_moonroot_ferryman | CONFIGURED |
| 11 | chest_window_elite_01 | ELITE_CHEST | ELITE_VARIANT | runtime elite projection | RESERVED_PENDING_B1 |
| 12 | chest_window_elite_02 | ELITE_CHEST | ELITE_VARIANT | runtime elite projection | RESERVED_PENDING_B1 |
| 13 | chest_window_elite_03 | ELITE_CHEST | ELITE_VARIANT | runtime elite projection | RESERVED_PENDING_B1 |
| 14 | chest_window_elite_04 | ELITE_CHEST | ELITE_VARIANT | runtime elite projection | RESERVED_PENDING_B1 |
| 15 | chest_window_elite_05 | ELITE_CHEST | ELITE_VARIANT | runtime elite projection | RESERVED_PENDING_B1 |

Каждое BOSS_CHEST — нефинальный checkpoint-owned offer для synergy/evolution или fallback. Пять ELITE_CHEST — typed reserved source; trigger, cadence и numerical outcome остаются pending Balance/Product. Terminal encounter не создаёт chest. Один window имеет один claim boundary и idempotency key.

Artifact offer не является chest window: источник после first clear создаёт ровно три candidate cards, игрок выбирает одну, effect scoped RUN и не потребляет weapon/passive slot.

## 7. Pause, Android background и recovery

User pause и application background переводят resumable run в RUN_PAUSED, останавливают clocks и сохраняют last safe snapshot по policy. Foreground проверяет schema version, content version, checksum, state revision и ledger revision. Valid snapshot resumes without time jump. Invalid or missing snapshot открывает RECOVERY_REVIEW; automatic reward grant запрещён. Exit из pause требует explicit confirmation and follows product policy.

## 8. Death, victory и result

Death is authoritative HP-zero transition and is settled once. Final victory requires defeat of boss_black_moon_empress plus final settlement. Timer alone cannot win. Terminal encounter has no chest. Result is immutable read model; ledger commit is idempotent. Return to menu occurs only after committed result or confirmed abandon.

## 9. Status boundary

- Designed/target: этот flow, state machine, JSON и event catalog.
- Implemented: только то, что доказано Runtime handoff; эта задача runtime не меняет.
- Verified: static architecture checks listed in ARCHITECTURE_AUDIT.md.
- Not claimed: Godot run, Android behavior, APK, balance lock, visual approval.
