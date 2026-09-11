# Готовый prompt для архитектурного агента первого забега

TASK-ID: REF-ARCH-01 / ARCH-30M-FINAL

Ты архитектурный агент проекта MAC. Канонический движок — Godot 4.x и GDScript. Unity-репозитории разрешено изучать только как источник паттернов; миграцию на Unity не предлагать.

## Обязательное чтение

Перед изменением файлов прочитай AGENTS.md, docs/AGENT_SYNC_STATE.md, этот каталог, корневой B1 и handoff-файлы других агентов в режиме read-only.

## Канонический контракт

- Target run: 1800 секунд.
- Main bosses: шесть записей на 300, 600, 900, 1200, 1500 и 1800 секунд.
- Mini bosses: пять записей на 450, 750, 1050, 1350 и 1650 секунд.
- Нефинальные encounters имеют десять BOSS_CHEST windows. Ещё пять windows зарезервированы как ELITE_CHEST. Терминальный encounter не создаёт chest.
- MAIN_BOSS замораживает видимые run clock, wave clock, XP progression и ordinary spawn от intro до settlement. MINI_BOSS продолжает эти часы и ordinary spawn. Отдельный encounter clock идёт для обоих типов.
- Artifact offer показывает ровно три карты, выбирается одна. Artifact не является pre-run loadout и не занимает weapon/passive slot.
- Registry map в docs/agents/architecture/REGISTRY_VARIANT_MAP.json фиксирует десять ordinary records, десять elite catalog records, максимум пять active elite и два legacy compatibility records.
- Числа, которых нет в B1, не изобретать: использовать PENDING_B1.

## Разрешённый результат

Меняй только docs/architecture/first-run/. Runtime, scenes, assets, B1, content-design, Visual Lab и корневые документы не менять. Не копируй код или коммерческий дизайн из исследованных репозиториев.

## Что должно быть проверено

Путь boot → menu → character → run → waves → XP/level → upgrade → encounters → typed chest or elite source → pause/background/resume → defeat or victory → result → rewards → menu; state transitions; events and data; reward ledger idempotency; save/restore; distinction между designed, implemented и verified.

## Результат

Отчёт должен содержать parent HEAD, resulting HEAD, changed files, status, evidence, blockers и ровно одно следующее действие. Godot/APK evidence не приписывать архитектурному пакету.
