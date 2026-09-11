# Задание агенту: логическая архитектура первого забега

## 1. Цель

Финализировать архитектурный контракт 30-минутного забега MAC и передать его Runtime, Balance и Content без изменения чужих зон. Этот пакет описывает target architecture; он не объявляет runtime, APK, баланс или visual approval готовыми.

## 1.1. Актуальная revision brief

| Решение | Канон |
|---|---|
| Duration | 1800 секунд |
| Main bosses | 6 на 300, 600, 900, 1200, 1500, 1800 |
| Mini bosses | 5 на 450, 750, 1050, 1350, 1650 |
| Chest windows | 15 typed windows: 10 BOSS_CHEST и 5 ELITE_CHEST |
| Terminal encounter | boss_black_moon_empress; после settlement победа; chest не создаётся |
| Clock | MAIN_BOSS freezes visible run/wave/XP/spawn; MINI_BOSS continues; encounter clock advances for both |
| Registry | 10 ordinary, 10 elite catalog, max 5 active elite, 2 legacy compatibility |
| Artifact offer | ровно 3 cards, выбрать 1; не pre-run loadout и не weapon/passive slot |
| Beetle variants | 3 ordinary visual variants; palette плюс читаемая деталь; отдельная reward boundary запрещена |

Schedule и IDs берутся из FIRST_RUN_DATA_CONTRACT.json и registry map. Numeric phase budgets остаются PENDING_B1.

## 2. Обязательная пользовательская цепочка

Опиши boot, menu, character selection, run setup, arena loading, active waves, XP pickup, level-up, upgrade offer, six main and five mini encounters, ten typed boss-chest windows, five reserved elite windows, pause, Android background, restore, death, victory, result, rewards and return to menu.

## 3. Обязательные архитектурные требования

1. R-01: зафиксировать 1800-second run и terminal schedule.
2. R-02: зарегистрировать шесть main boss records с exact IDs и checkpoints.
3. R-03: зарегистрировать пять MINI_BOSS records с exact IDs и checkpoints.
4. R-04: дать единый ordered encounter schedule без UI branching.
5. R-05: описать пятнадцать typed chest windows: десять BOSS_CHEST и пять ELITE_CHEST.
6. R-06: запретить chest у terminal encounter и отделить first-clear artifact offer от result.
7. R-07: зафиксировать conditional clock policy для MAIN_BOSS и MINI_BOSS.
8. R-08: описать post-boss relief → ramp → pre-boss peak и pending B1 profiles.
9. R-09: связать 10 ordinary, 10 elite, max-five active и 2 legacy с registry map.
10. R-10: описать три beetle visual variants без второй XP/aftermath boundary.
11. R-11: зафиксировать artifact offer из ровно трёх карт без slot consumption.
12. R-12: провести сквозной путь от boot до menu.
13. R-13: описать pause, Android background, resume и recovery.
14. R-14: описать save/restore, schema version и unknown-content quarantine.
15. R-15: описать XP, aftermath, reward ledger и duplicate/idempotency rules.
16. R-16: согласовать state transitions, event catalog и JSON data contract.
17. R-17: разделить designed, target, implemented и verified; не заявлять Godot/APK evidence.
18. R-18: закрыть архитектурные проверки и явно передать внешние Balance/Runtime/Visual blockers.

## 4. Источники истины

1. Поставленная задача и AGENT_SYNC_STATE.md.
2. Registry map: docs/agents/architecture/REGISTRY_VARIANT_MAP.json.
3. B1 и Balance handoff для чисел; B1 read-only.
4. Content catalog и handoff для IDs; proposals не превращаются в artistic approval.
5. Runtime handoff и существующий Godot код read-only для seam alignment.
6. Этот каталог — authoritative architecture contract.

## 5. Жёсткие границы

Только docs/architecture/first-run/. Не менять runtime, scenes, assets, Balance, Content, Visual Lab или корневые документы. Не делать force-push, rebase, reset, удаление чужой работы. Все внешние статусы отражать честно.

## 6. Обязательные файлы результата

FIRST_RUN_FLOW.md, FIRST_RUN_STATE_MACHINE.md, FIRST_RUN_ARCHITECTURE.md, FIRST_RUN_DATA_CONTRACT.json, FIRST_RUN_DATA_CONTRACT.template.json, FIRST_RUN_EVENT_CATALOG.md, FIRST_RUN_ACCEPTANCE_MATRIX.md, DECISIONS_AND_UNKNOWNS.md и ARCHITECTURE_AUDIT.md.

## 7. Критерии приёмки

Все R-01…R-18 имеют строку в acceptance matrix. Каждая transition row содержит trigger, guard, owner, side effects, failure path, recovery path и duplicate/idempotency. JSON actual/template парсятся. Внутренние ссылки существуют. Scope и whitespace проходят проверку. Pending values имеют owner и next action.

## 8. Формат финального отчёта агента

Status, parent HEAD, resulting HEAD, changed files, evidence, blockers и ровно одно следующее действие.
