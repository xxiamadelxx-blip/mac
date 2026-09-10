# Задание Content & Game Design Agent

## 1. Роль

Ты — владелец игрового content design Moonveil: Eclipse. Создавай оригинальный, читаемый и взаимосвязанный контент, который следующий Balance Agent сможет численно настроить, Visual Lab — произвести, а Runtime Agent — реализовать через стабильные contracts.

## 2. Главная цель

Подготовить каталог content entries для следующих областей:

1. оружие: механика, targeting, qualitative range, внешний образ, VFX lifecycle и hooks;
2. пассивные способности;
3. артефакты с уникальными run-modifier mechanics;
4. магазин и постоянные улучшения за золото;
5. новые противники и signature behavior для следующих этапов;
6. новые боссы и arena encounters;
7. drops на арене: лечение, монеты, mana magnet, destruction, freeze и новые proposals.

Balance Agent позднее привяжет урон, HP, speed, cooldown, range numbers, costs, frequency, quantity, duration и другие значения. Не подменяй эту работу выдуманными числами.

## 3. Обязательный старт

Перед первым изменением:

1. Проверь repository, branch, HEAD и доступ к живому main.
2. Прочитай AGENTS.md и root project documents.
3. Прочитай docs/architecture/first-run/ целиком как контракт boundaries.
4. Прочитай docs/agents/core-gameplay-runtime/README.md и RUNTIME_CONTEXT.md.
5. Прочитай docs/BALANCE_ECONOMY_SPEC.md и docs/agents/balance-economy/README.md.
6. Для visual/content/VFX задач прочитай обязательный пакет Visual Lab.
7. Проведи read-only аудит существующих stage folders и first-run content.
8. Зафиксируй protected paths и список уже существующих content IDs.

## 4. Вертикальные срезы

### C0 — Content audit and taxonomy

Результат:

- карта существующего first-run content;
- список существующих и свободных IDs;
- граница «не менять» для готового контента;
- единая taxonomy;
- список content gaps и product decisions.

Проверка: каждый вывод имеет path/source/status, а отсутствие файла не превращается в выдуманный факт.

### C1 — Weapons, passives and build hooks

Создай content entries для первой согласованной пачки оружия и пассивок.

Для каждого entry опиши:

- promise и роль;
- core loop;
- target/geometry/range class;
- attack or trigger behavior;
- counterplay/trade-off;
- VFX/audio/haptic hooks;
- synergy/evolution tags;
- PENDING_BALANCE fields;
- Visual Lab brief;
- Runtime consumer contract.

Не копируй existing first-run content и не закрывай numeric balance внутри этого среза.

### C2 — Artifacts and shop content

Подготовь:

- artifact proposals, отличающиеся от обычных flat passives;
- typed effect family, trigger, target, source и feedback;
- три-card offer presentation contract;
- отсутствие pre-run loadout и fixed artifact slot;
- shop branches, rank fantasy, unlock and tooltip copy;
- distinction between persistent shop upgrade and temporary run artifact.

Проверка: ни один артефакт не сводится к безымянному +проценту; цены и величины явно PENDING_BALANCE.

### C3 — Future enemies and bosses

Новые противники не заменяют существующий first-run roster.

Для каждого enemy/boss подготовь:

- silhouette brief;
- role/signature;
- readable telegraphs;
- arena interaction;
- player counter-decision;
- phase or spawn behavior;
- VFX/audio/haptic hooks;
- drop/reward boundary;
- balance questions.

Boss content должен быть совместим с BossDirector и final-boss no-chest rule.

### C4 — Arena drop catalogue

Создай catalog drops:

- heal;
- coin/currency;
- mana/XP magnet;
- destruction;
- wave freeze;
- shield/ward;
- vacuum/harvest;
- дополнительные proposals, если они усиливают решения игрока.

Для каждого опиши: визуальный сигнал, pickup rule, effect intent, feedback, limitations и PENDING_BALANCE fields. Balance Agent решает частоту, количество и численные значения.

### C5 — Cross-system handoff

Собери:

- catalog index;
- dependency matrix;
- duplicate/conflict review;
- Balance handoff;
- Runtime handoff;
- Visual Lab briefs;
- open product decisions;
- acceptance evidence.

После C5 не расширяй scope бесконечно. Новая идея становится отдельным proposal, а не поводом переписывать готовый срез.

## 5. Правила разработки контента

- Каждый entry имеет стабильный ID и статус.
- Один ID означает одну содержательную сущность; не плодить aliases без причины.
- Механика должна быть объяснима игроку одним коротким promise и проверяема в runtime.
- Числовые поля помечать PENDING_BALANCE.
- Нельзя описывать VFX только словами «красивый эффект»: указать trigger, фазу, читаемый сигнал и expire/cleanup.
- Нельзя смешивать content design с implementation.
- Нельзя переписывать архитектуру, баланс или Visual Lab policy.
- Нельзя заменять готовый first-run content новыми предложениями без explicit approval.
- Не использовать чужие коммерческие названия, ассеты или копировать signature один-в-один.
- Все unresolved choices перечислять с owner и next action.

## 6. Definition of Done для content slice

Срез можно назвать CONTENT_SPECIFIED только если:

- все обязательные поля заполнены;
- mechanic, player decision и counterplay понятны;
- PENDING_BALANCE поля перечислены;
- Visual Lab brief отделён от production asset;
- Runtime consumer contract указан;
- нет конфликта ID или тихой замены existing content;
- acceptance и handoff заполнены.

Не использовать DONE, PRODUCTION, PLAYABLE или VERIFIED для материала, который только описан.
