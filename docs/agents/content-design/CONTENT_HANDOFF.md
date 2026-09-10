# Content Handoff — передача контента

Этот шаблон заполняется после каждого content slice. Он не даёт Content Agent права менять код, баланс или production assets.

## 1. Идентичность

- Repository:
- Branch:
- HEAD:
- Slice: C0 / C1 / C2 / C3 / C4 / C5
- Status:
- Catalog version:
- Date:

## 2. Scope

### Созданные entries

| content_id | type | stage | status | source | next owner |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Защищённые области

- Existing first-run content не изменён: PASS/FAIL.
- docs/architecture/first-run не изменялась: PASS/FAIL.
- docs/agents/balance-economy не изменялась: PASS/FAIL.
- docs/agents/core-gameplay-runtime не изменялась: PASS/FAIL.
- scripts/, scenes/ и project.godot не изменялись: PASS/FAIL.
- visual_lab и production assets не изменялись: PASS/FAIL.

## 3. Balance handoff

Передать Balance Agent:

- список numeric fields, которые нужно назначить;
- intended power budget и qualitative priority;
- frequency/quantity questions для drops;
- damage/HP/speed/cooldown/range/cost/duration questions;
- source/status каждого ограничения;
- conflicts and open decisions.

Content Agent не утверждает числа сам.

## 4. Runtime handoff

Передать Runtime Agent:

- content IDs и schema/data fields;
- events/commands, которые нужно потреблять;
- trigger/target/effect semantics;
- VFX/audio/haptic hooks;
- UI/HUD/tooltip fields;
- invalid state and failure behavior;
- dependency on Balance Model;
- pending policies.

## 5. Visual Lab handoff

Для каждого visual item указать:

- route: UI_ART / SPRITE / ART / MOCKUP / VFX;
- stage_path;
- asset_kind;
- asset_id;
- family_id;
- candidate_id;
- status;
- technical_status;
- artistic_status;
- manifest/consumer;
- master/variant requirements;
- gameplay-scale preview requirement;
- open creative decisions;
- prohibited drift.

Content brief не равен approved asset.

## 6. Проверки

Укажи реальные команды, exit status и output:

- ID uniqueness:
- schema/template validation:
- internal link/path check:
- balance handoff check:
- runtime consumer check:
- Visual Lab metadata check:
- change-review:

Если проверка недоступна, укажи точную ошибку и статус PARTIAL/BLOCKED.

## 7. Незакрытые вопросы

| Question | Impact | Owner | Status | Next action |
|---|---|---|---|---|
|  |  |  |  |  |

## 8. Следующий шаг

- Что проверяет Balance Agent:
- Что проверяет Runtime Agent:
- Что проверяет Visual Lab:
- Какая первая проверка следующего агента:

Не переписывать исходные документы других агентов ради обновления handoff.
