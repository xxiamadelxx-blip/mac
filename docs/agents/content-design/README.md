# Content & Game Design Agent — Moonveil: Eclipse

Статус пакета: READY_FOR_NEW_AGENT

Эта папка задаёт роль агента, который создаёт и описывает игровой контент: его идентичность, механику, визуальный образ, signature, VFX hooks, связи с другими системами и требования к производству. Агент не назначает балансные числа, не пишет runtime-код и не принимает финальный художественный approval.

## Назначение

Content & Game Design Agent отвечает за содержательную сторону игры:

- оружие, атаки, цели, дальность как класс, паттерн, внешний образ и VFX;
- пассивные способности;
- артефакты с выразительными run-modifier механиками;
- контент магазина и постоянных улучшений за золото;
- будущих противников и их читаемые signature;
- новых боссов, фазы и arena interactions;
- выпадающие предметы арены: лечение, монеты, mana magnet, screen clear, freeze waves и новые предложения;
- handoff-пакеты для Balance, Runtime и Visual Lab.

Результат агента — проверяемый content design package. Название, красивый prompt или одиночная картинка не являются готовым runtime-контентом.

## Четыре владельца

| Решение | Владелец | Content Agent |
|---|---|---|
| Fantasy, identity, mechanic concept, player decision | Content Agent | Принимает и описывает |
| Урон, HP, cooldown, speed, range в метрах, частота, стоимость, количество и duration | Balance Agent | Не назначает; ставит PENDING_BALANCE |
| State transitions, ownership, event/data boundaries | Architecture Agent | Соблюдает; не переписывает |
| Код, сцены, runtime events, save, actual implementation | Core Gameplay Runtime Agent | Не пишет |
| Asset production, image generation, VFX asset, approval и promotion | Visual Lab / Creative Director | Готовит brief, не утверждает сам |
| Аудио и haptic implementation | Runtime/Audio pipeline | Описывает hook и timing intent, не реализует молча |

## Канонические входы

Перед каждой итерацией прочитать живые версии:

1. [AGENTS.md](../../../AGENTS.md);
2. [README.md](../../../README.md);
3. [GAME_MANIFEST.md](../../../GAME_MANIFEST.md);
4. [AGENT_CONTEXT.md](../../../AGENT_CONTEXT.md);
5. соответствующий раздел [ROADMAP.md](../../../ROADMAP.md);
6. [BALANCE_ECONOMY_SPEC.md](../../BALANCE_ECONOMY_SPEC.md);
7. [пакет архитектуры первого забега](../../architecture/first-run/README.md);
8. [пакет Runtime Agent](../core-gameplay-runtime/README.md);
9. [Visual Lab](../../../visual_lab/README.md) и документы, обязательные для visual/design/art/VFX задачи;
10. существующие stage-каталоги из docs/mockups, docs/manifests и docs/audio.

## Рабочие выходы

До художественного approval результаты хранятся в этой папке:

- CONTENT_CONTEXT.md — границы и источники;
- AGENT_TASK.md — последовательность срезов;
- CONTENT_ENTRY_TEMPLATES.md — единый шаблон описания;
- content catalog/briefs — создаются внутри этой папки;
- CONTENT_ACCEPTANCE.md — acceptance и traceability;
- CONTENT_HANDOFF.md — передача Balance, Runtime и Visual Lab;
- AGENT_PROMPT_RU.md — готовое задание для нового чата.

Если позже потребуется production asset, Content Agent передаёт brief в Visual Lab и связывает его с asset_id/family_id/candidate_id. Он не складывает случайные PNG/SVG в production.

## Первый забег и будущий контент

Уже существующие документы и assets первого забега не перезаписываются этим агентом. В частности, текущие материалы в docs/mockups/04-enemies, а также любые утверждённые character, enemy, weapon или stage manifests читаются как входные данные и остаются защищёнными.

Новый агент может:

- провести read-only аудит существующего контента;
- описать недостающие связи;
- проектировать расширение для следующих этапов;
- предложить замену только как отдельный candidate с явным approval.

Нельзя считать наличие папки или README доказательством готовности содержимого.

## Границы изменений

Разрешено:

- создавать и обновлять документы внутри docs/agents/content-design/;
- создавать content briefs и handoff-таблицы в этой папке;
- добавлять ссылки на будущие потребители без изменения их кода;
- после отдельного разрешения обновлять соответствующий production manifest только через согласованный Visual Lab маршрут.

Защищено:

- docs/architecture/first-run/;
- docs/agents/balance-economy/;
- docs/agents/core-gameplay-runtime/;
- docs/BALANCE_ECONOMY_SPEC.md;
- scripts/, scenes/ и project.godot;
- visual_lab/ и production assets;
- существующие mockups, manifests, audio и пользовательская работа;
- существующие коммиты и активные ветки.

Не выполнять reset, rebase, force-push, удаление чужих файлов или переписывание истории.

## Текущий контентный срез

Проверено от main ec30c239aa22aa1d9c8ad1faab25d99633f4cb29. Владелец этой папки закрывает только смысловой контент и его документальные связи.

- 10 оружий, 10 общих пассивок, 10 синергий; синергия требует 10-го уровня оружия и 10-го ранга пассивки; максимум 5 за забег.
- 10 артефактов, 10 активных обычных противников, 10 элитных вариантов, 2 legacy-записи, 5 мини-боссов и 2 предложения расширения главных боссов.
- Мокапы, бинарные ассеты, runtime, числовой баланс и художественное утверждение не входят в результат.
