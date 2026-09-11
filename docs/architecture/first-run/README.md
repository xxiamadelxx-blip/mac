# Рабочая папка агента: архитектура первого забега

Revision 3 фиксирует target architecture для 30-минутного run.

## Статус

- Architecture document gate: VERIFIED.
- Runtime implementation: NOT_IMPLEMENTED в границах этой задачи.
- Godot stdout, exit code и APK: внешний Runtime gate, здесь не заявляются.
- Balance numeric extension: PARTIAL и PENDING_B1.
- Visual approval: PENDING_VISUAL.

## Канон

Шесть main bosses и пять mini bosses образуют ordered schedule на 1800 секунд. Нефинальные encounters имеют десять BOSS_CHEST windows. Пять ELITE_CHEST windows зарезервированы для bounded elite projection. Terminal encounter не создаёт chest. Artifact offer после first clear отдельна от result и содержит ровно три карты.

## Состав проверенного пакета

- [FIRST_RUN_FLOW.md](./FIRST_RUN_FLOW.md) — наблюдаемый пользовательский маршрут.
- [FIRST_RUN_STATE_MACHINE.md](./FIRST_RUN_STATE_MACHINE.md) — состояния и 33 transition contracts.
- [FIRST_RUN_ARCHITECTURE.md](./FIRST_RUN_ARCHITECTURE.md) — модули, ownership и data flow.
- [FIRST_RUN_DATA_CONTRACT.json](./FIRST_RUN_DATA_CONTRACT.json) — authoritative v3 JSON contract.
- [FIRST_RUN_DATA_CONTRACT.template.json](./FIRST_RUN_DATA_CONTRACT.template.json) — template projection.
- [FIRST_RUN_EVENT_CATALOG.md](./FIRST_RUN_EVENT_CATALOG.md) — events, producers, consumers и retry rules.
- [FIRST_RUN_ACCEPTANCE_MATRIX.md](./FIRST_RUN_ACCEPTANCE_MATRIX.md) — R-01…R-18 traceability.
- [DECISIONS_AND_UNKNOWNS.md](./DECISIONS_AND_UNKNOWNS.md) — confirmed decisions и pending owners.
- [ARCHITECTURE_AUDIT.md](./ARCHITECTURE_AUDIT.md) — итоговая проверка.

## Передача

Registry map в docs/agents/architecture/REGISTRY_VARIANT_MAP.json уже является published product decision и в этой задаче не дублируется. B1, Content, Runtime, Visual Lab и корневые документы читаются только для сверки.