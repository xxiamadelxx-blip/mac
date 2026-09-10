# Visual Lab — Transfer Provenance

Статус: TRANSFERRED AND ADAPTED.
Дата: 2026-09-09.
Target repository: xxiamadelxx-blip/mac.

Пакет перенесён из ранее собранного Visual Lab в xxiamadelxx-blip/out-of-abyys. Перенос сделан как отдельный target-specific process package; D&D/Underdark-specific production content и runtime-код исходного проекта не переносились.

## Источники переноса

| Перенесённый принцип | Source repository commit |
| --- | --- |
| Visual Lab production law v2 | ead7f58faa75797a78a81acc515dad2ddf5302c4 |
| Mandatory visual policy gate | 52dca8d05b5b18c157f568f18edfed2dbf8cc701 |
| Visual Lab roadmap addendum | cda8857e0ff82aff1a06d8b2ffe348d2325b6805 |
| Visual Lab tooling/radar decision | 9ba0c5e19cab41698183777254923bc913fbb2f5 |
| Campaign-wide asset pipeline law | 1147b20a6e1b08f961b66ae2c24486c2b531425c |
| Mandatory design/art routing precedent | 67997398baa54133597b149bb5fc8190b5b9677a and ea851549f33a5c319919d8e4ec8fd9cc19c65b4a |

## Адаптация к Moonveil

- Out of the Abyss, Drow Guard, Velkynvelve и другие source-specific identities заменены на Moonveil visual families, stage-папки, Линь Юэ, Соён Хан и Затопленный сад Лунного лотоса.
- D&D/design-law, относящиеся только к исходной кампании, не объявляются каноном Moonveil.
- Godot runtime остаётся offline-first и не получает authoring/QA dependency.
- Existing Moonveil mockups остаются со своими честными статусами; этот перенос не выдаёт им задним числом artistic approval.
- Для future assets обязательны stable IDs, provenance, hero-master gate, true gameplay-scale review и explicit Creative Director approval.

## Проверка переноса

Целевой пакет должен содержать:

- root AGENTS.md с обязательной маршрутизацией;
- visual_lab/README.md как entrypoint;
- mandatory policy и production law;
- asset pipeline law;
- review checklist;
- machine-readable provenance template;
- этот transfer record.

Любой агент, который не прочитал entrypoint и policy, не должен начинать visual/design/art production работу.
