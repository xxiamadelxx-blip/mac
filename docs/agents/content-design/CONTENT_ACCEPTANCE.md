# Content Acceptance — критерии каталога

Статус нового контента до проверок: PROPOSAL. Статус CONTENT_SPECIFIED возможен только при выполнении критериев ниже.

## 1. Матрица

| Область | Обязательный результат | Evidence | Владелец следующего шага |
|---|---|---|---|
| Weapon | Уникальный attack decision, qualitative range, VFX lifecycle, trade-off и runtime fields | Entry + template check + handoff | Balance, Runtime, Visual Lab |
| Passive | Понятная axis, trigger, affected systems, stacking intent и UI copy | Entry + duplicate review | Balance, Runtime |
| Artifact | Выразительный typed run modifier, не slot passive, три-card source contract | Entry + artifact invariant check | Balance, Runtime, Visual Lab |
| Shop | Persistent branch fantasy, rank loop, wallet boundary и UI copy | Entry + economy handoff | Balance, Runtime/UI |
| Future enemy | Роль, silhouette, signature, telegraph и counter-decision | Entry + visual brief | Balance, Runtime, Visual Lab |
| Boss | Phase identity, telegraph, reaction window, arena interaction и defeat contract | Entry + boss boundary check | Balance, Runtime, Visual Lab |
| Arena drop | Pickup identity, effect intent, limitation, feedback и pending frequency/quantity | Entry + drop taxonomy check | Balance, Runtime |
| Cross-system | Stable IDs, source refs, consumers, statuses, no protected edits | Catalog/index + diff/scope review | Architecture/Project Owner |

## 2. Обязательные инварианты

1. Content Agent не владеет damage, HP, cooldown, speed, exact range, price, frequency, quantity или duration.
2. Каждый неизвестный numeric field имеет статус PENDING_BALANCE.
3. Артефакты не используют pre-run loadout, weapon slots или passive slots.
4. Каждый artifact offer имеет ровно три cards и один chosen result.
5. Boss chest и artifact offer остаются разными системами.
6. Final boss не создаёт boss chest.
7. Existing first-run content не переписывается новыми proposals.
8. Новый enemy/boss изменяет решение игрока, а не только числовую выносливость.
9. Каждый VFX brief имеет trigger, phase, readable signal и lifecycle.
10. Каждый content entry имеет stable ID, source/status и next owner.
11. Shop upgrades не смешиваются с temporary run artifacts.
12. Drop effect не мутирует wallet или RunSession напрямую из content description.
13. Для синергии weapon достигает 10-го уровня и связанная passive достигает 10-го ранга; это не меняет вместимость билда (6 weapon slots и 6 passive slots).

## 3. Статусы

- PROPOSAL — идея;
- CONTENT_SPECIFIED — content contract заполнен;
- BALANCE_PENDING — ждёт числовой binding;
- VISUAL_BRIEF_READY — brief передан Visual Lab;
- RUNTIME_HANDOFF_READY — consumer contract готов;
- APPROVED — explicit product/creative approval;
- IMPLEMENTED — подтверждено runtime;
- BLOCKED — конкретная причина;
- RETIRED — снято с дальнейшего использования.

Не использовать VERIFIED, PLAYABLE или PRODUCTION, если доказан только текстовый дизайн.

## Статические контентные ворота после аудита

База проверки: main ec30c239aa22aa1d9c8ad1faab25d99633f4cb29. Эти ворота не требуют запуска Godot.

| Ворота | Ожидание | Результат |
|---|---|---|
| Каталог | 10 оружий, 10 пассивок, 10 синергий, 10 артефактов | PASS |
| Уникальность | нет повторов внутри каждого типа ID | PASS |
| Условие синергии | оружие 10 + пассивка 10; максимум 5 подтверждений | PASS |
| Расписание | 6 главных боссов, 5 мини-боссов, 1800 секунд | PASS |
| Окна | C01–C10 BOSS_CHEST, C11–C15 ELITE_CHEST, финальный без сундука | PASS |
| Противники | 10 активных обычных, 10 элитных вариантов, 2 совместимости отдельно | PASS |
| Статусы | новые ID только PROPOSED; нет approval или balance lock | PASS |
| Область | изменяется только docs/agents/content-design | PASS |

Не являются этими воротами: runtime proof, Android, numeric balance promotion, visual/artistic approval и импорт ассетов.
