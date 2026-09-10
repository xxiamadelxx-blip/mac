# Контракт работы с B1

## 1. Источник

Канонический файл: docs/BALANCE_ECONOMY_SPEC.md  
Официальная ссылка: https://github.com/xxiamadelxx-blip/mac/blob/main/docs%2FBALANCE_ECONOMY_SPEC.md

Файл нужно читать из фактической рабочей ветки, а не из старого URL-кэша, скриншота или пересказа. SHA B1 не зашивается в этот пакет: он может измениться. В отчёте каждой работы указывай фактическую ветку, HEAD и source revision, который был прочитан.

Текущий заявленный статус B1: Version 0.1, design baseline; numeric params are not wired to code.

## 2. Что B1 уже задаёт

Агент обязан проверить по живому файлу следующие группы:

- базовые stats героев и модификаторы Линь Юэ/Соён Хан;
- целевые time-to-kill;
- five-minute wave bands, spawn budget, active cap и HP/damage/speed multipliers;
- boss spawn interruption и восстановление потока;
- роли, durability multipliers, XP bands и поведение десяти противников;
- contact damage cooldown, telegraph, safe spawn и правила ranged pressure;
- XP drop values, magnet/merge rules и XP_to_next(L);
- цели уровня и первой эволюции;
- checkpoint, first-clear, repeat и defeat rewards;
- три отдельных кошелька и meta sinks;
- шесть пассивных веток и формулу стоимости;
- summon rules;
- acceptance targets для combat, progression, synergy, boss, performance и aftermath.

Если актуальная версия B1 отличается, живой файл имеет приоритет над этим описанием.

## 3. Что нельзя silently invent

B1 не доказывает наличие всех данных, которые нужны runtime. В частности, отдельно проверь, заданы ли:

- абсолютные base HP, base damage, base speed и точные contact/ranged values каждого enemy_id;
- точные коэффициенты состава внутри каждой wave band;
- точные boss identities, skills, health/damage и arena rules;
- полный список weapon/passive/synergy IDs и их exact eligibility conditions;
- число слотов, порядок offer pool и правила reroll/banish;
- семантика «накопления бонуса» и kill streak;
- точный success-rate, который продукт считает «проходимо»;
- target Android device для performance evidence.

Если значение отсутствует, используй статус PENDING_B1 или PENDING_PRODUCT_DECISION. Можно сделать placeholder для симулятора только если он помечен как TEST_PLACEHOLDER, не выдаётся за канон и не попадает в production data.

## 4. Иерархия решений

- Пользовательский brief определяет цель и явные продуктовые решения.
- GAME_MANIFEST.md и AGENT_CONTEXT.md определяют scope и канон.
- B1 определяет числа, формулы, wave/reward rules и acceptance targets.
- Runtime определяет только фактически реализованное поведение, но не переопределяет B1 молча.
- Derived values должны содержать формулу и входные значения.
- Product decisions не должны маскироваться под математический вывод.

При конфликте:

1. останови только зависимую часть расчёта;
2. запиши конфликт в DECISIONS_AND_UNKNOWNS.md;
3. укажи временный безопасный handling;
4. перечисли владельца решения и next action;
5. продолжи независимые deliverables.

## 5. Правило изменения B1

Balance Agent не редактирует docs/BALANCE_ECONOMY_SPEC.md в рамках обычного запуска.

Если обнаружена ошибка:

- зафиксируй evidence;
- покажи влияние на модель/runtime;
- предложи минимальный patch или decision request;
- не переписывай источник в том же изменении без явного разрешения владельца проекта;
- после принятия изменения пересобери derived tables и симуляции.
