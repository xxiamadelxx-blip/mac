# Skills и рабочие инструкции Content Agent

Эта папка не копирует системные skill-файлы. Она задаёт обязательную маршрутизацию для content design и visual briefs.

## Обязательные навыки

| Skill | Назначение | Evidence |
|---|---|---|
| keystone:project-audit | Read-only аудит live repository и существующего контента | HEAD, paths, IDs, protected scope и findings |
| keystone:product-planning | Формализация player promise, decisions, trade-offs и content acceptance | Goal, audience, mechanic, counterplay и open decisions |
| keystone:task-creation | Разбиение C0 → C5 на ограниченные срезы | Dependencies, acceptance и handoff order |
| codex-engineering-guardrails:code-verification | Проверка схем, ссылок, ID и traceability | Команды, exit status и результаты |
| keystone:change-review | Read-only review каталога и границ после content slice | Blockers/non-blockers и evidence |
| keystone:root-cause-analysis | Только при противоречии источников или непонятном конфликте | Доказанная причина конфликта |

## Обязательный Visual Lab маршрут

Поскольку оружие, противники, боссы, VFX и магазин имеют visual surface, перед подготовкой briefs прочитай:

1. AGENTS.md;
2. visual_lab/README.md;
3. visual_lab/VISUAL_POLICY_RULE.md;
4. visual_lab/VISUAL_LAB_PRODUCTION_LAW.md;
5. visual_lab/ASSET_PIPELINE_CODE.md;
6. visual_lab/REVIEW_CHECKLIST.md.

Для UI, sprite, mockup или UI-art дополнительно прочитай visual_lab/UI_ART_SPRITE_MOCKUP_WORKFLOW.md.

Content Agent не производит и не утверждает финальный визуал. Он передаёт route, stage_path, asset_kind, asset_id, family_id, candidate_id, status, technical_status, artistic_status, manifest/consumer и open_decisions.

## Fallback без Atlas Scout

Atlas Scout — опциональный инструмент. Если он недоступен:

- используй GitHub tree/file reads и точечный поиск;
- при checkout используй rg;
- не называй fallback локальным structural index;
- зафиксируй ограничение одной строкой и продолжай.

## Протокол итерации

1. Прочитать root instructions и этот пакет.
2. Проверить live branch/HEAD и существующие IDs.
3. Отделить canonical, existing, proposal, pending и retired.
4. Выполнить C-срез только в пределах разрешённой папки.
5. Для каждого entry проверить mechanic, player decision, counterplay и content dependencies.
6. Проставить PENDING_BALANCE для всех чисел, которых нет в каноне.
7. Подготовить Visual Lab brief, Runtime consumer contract и Balance handoff.
8. Запустить link/schema/ID checks.
9. Провести change-review до заявления о завершении.

## Не считать доказательством

- созданную папку;
- список названий;
- красивый арт или prompt;
- технически валидный PNG;
- наличие чисел без source;
- запись «готово» в статусе;
- runtime-код, который не потребляет entry;
- один удачный балансный пример.

## Ограничения

- Не писать GDScript или менять runtime.
- Не менять Balance Model и B1.
- Не менять architecture contracts.
- Не изменять существующие first-run content files.
- Не создавать production assets в обход Visual Lab.
- Не назначать самостоятельно частоту и количество drops.
- Не использовать неизвестные IDs или скрытые aliases.
- Не делать destructive git operations.
