# Runtime Acceptance — критерии первого игрового среза

Статус до реализации: NOT_IMPLEMENTED. Каждая строка переводится в IMPLEMENTED, TESTED или RUNTIME_VERIFIED только после evidence.

## 1. Матрица приёмки

| Требование | Source | Нужное evidence | Slice |
|---|---|---|---|
| BALANCE_MODEL реально загружается | B1, BALANCE_MODEL.json | Content Registry test/trace с content_version и конкретными прочитанными полями | R1 |
| Новый run создаёт один RunSession | Architecture data/state contract | duplicate start test: один run_id и сохранённый outcome | R1 |
| RunCoordinator владеет transitions | FIRST_RUN_STATE_MACHINE | command/event trace без прямой мутации UI | R1 |
| Есть run-clock и encounter-clock | Architecture runtime contract | before/after values на RUN_ACTIVE, pause, main-boss freeze и mini-boss continuation | R1 |
| Уровень/волна не живут в UI | Architecture ownership | focused test показывает domain state как source of truth | R1 |
| Обычный combat работает | B1 и event catalog | damage/HP/death trace, hit cooldown и defeat fact | R1 |
| XP начисляется один раз | Data contract | duplicate pickup replay не меняет XP второй раз | R1 |
| Level-up offer блокирует run | State machine | clock freeze, ровно одна claim mutation, stale choice rejection | R1 |
| Pause/resume безопасны | State/event contract | pause snapshot, resume state и no hidden time advancement | R1 |
| B1 wave bands data-driven | B1 wave table/model | trace на всём 30-минутном envelope; при сохранении пятиминутного baseline — границы 2/5/10/15/20/25/30 минут, budget/cap evidence | R2 |
| Spawn соблюдает active cap | B1 acceptance | occupancy trace и controlled fallback при переполнении | R2 |
| Boss spawn безопасен и читаем | Architecture/B1 | main/mini encounter ID, safe distance, telegraph/reaction evidence | R2 |
| Main-boss freeze policy | Решение владельца проекта; RUNTIME_CONTEXT | trace для каждого main-boss boundary: run time и ordinary wave/XP/spawn unchanged от intro через active/settlement; encounter time advances only in active phase | R2 |
| Mini-boss pressure policy | Решение владельца проекта; RUNTIME_CONTEXT | trace показывает, что run clock, waves, XP и ordinary spawn продолжаются в mini-boss intro/active; count = 5 | R2 |
| Main/mini roster count | Каноническое решение владельца проекта | 6 main bosses (4+2) и 5 mini-bosses из versioned content/config, без локальной подмены состава | R2 |
| Bounded elite variants | Каноническое решение владельца проекта; B1 | elite-tagged ordinary enemy создаёт отдельный ELITE_CHEST для дополнительного сундука под bounded eligibility/budget/cap; не входит в постоянный roster и не открывает artifact offer автоматически | R2 |
| Нефинальный boss settlement один раз | State/event/data contract | duplicate defeat/checkpoint replay returns existing ledger result | R2 |
| Нефинальный boss chest отдельный | Architecture contract | chest_offer_id, eligibility/fallback, claim idempotency; MINI_BOSS_CHEST и ELITE_CHEST не смешаны с artifact offer | R2 |
| Final main boss не создаёт boss chest | State machine and data contract | final trace на границе 30:00: final settlement → victory и no chest_offer | R2 |
| Следующая стадия начинается после claim | Flow/state contract | stage projection changes only after valid chest outcome | R2 |

| Артефакт не является slot loadout | Product decision and architecture | pre-run artifact selection rejected; weapon/passive capacities unchanged | R3 |
| Artifact offer содержит ровно три карты | Data/event contract | ELITE_PACK and FIRST_CLEAR_REWARD traces with three candidates | R3 |
| Выбирается ровно один артефакт | Artifact event contract | one artifact_instance_id, duplicate choice returns same instance | R3 |
| Artifact effect typed и отдельный | Architecture artifact boundary | effect type/trigger/target/parameters preserved through Stats/HUD projection | R3 |
| Refresh не дублирует charge/reroll | State/event contract | repeated idempotency key returns stored refresh outcome | R3 |
| First-clear offer отдельна от final boss chest | Architecture contract | result_finalized → artifact offer; no boss chest relation | R3 |
| RewardLedger атомарен | Architecture/B1 | crash/retry or simulated retry shows one wallet revision and ledger entry | R2/R3 |
| Save restore не повторяет rewards | Persistence contract | restore test with settled ledger has no duplicate wallet mutation | R3 |
| Seeds воспроизводимы | Balance task | seeds 101/202/303/404/505 produce stable domain hashes or equivalent summaries | R3 |
| Android performance evidence | B1 acceptance | actual build/run measurement on target or declared equivalent | R4 |
| Full APK ready | Project roadmap | build, install and launch evidence; never inferred from source | R4 |

## 2. Инварианты

1. RunSession — единственный источник истины активного забега.
2. Content Registry immutable/versioned на протяжении run.
3. RunCoordinator не превращается в god controller.
4. UI не меняет время, HP, build или rewards напрямую.
5. XP, chest, artifact, aftermath и wallet entry имеют разные типы.
6. На основном боссе run-clock и обычные wave/XP/spawn clocks не продвигаются; на мини-боссе run-clock, волны, XP и ordinary spawn продолжаются.
7. Финальный основной босс не открывает boss chest.
8. Каждый artifact offer содержит ровно три кандидата; выбор создаёт ровно один artifact instance.
9. Артефакты не занимают weapon/passive slots и не используют pre-run loadout.
10. Повторное событие не дублирует mutation, effect, offer или reward.
11. Таймер сам по себе не завершает забег победой.
12. Неизвестное число или policy не превращается в hardcoded догадку.

## 3. Статусная дисциплина

- IMPLEMENTED: код существует и подключён к entry point.
- TESTED: focused test/contract check прошёл.
- RUNTIME_VERIFIED: фактический runtime trace подтверждает поведение.
- PARTIAL: часть acceptance доказана.
- BLOCKED: указан конкретный технический блокер.
- PENDING_PRODUCT_DECISION: отсутствует решение продукта.

Не использовать VERIFIED, PLAYABLE, DONE или APK READY для более слабого статуса.
