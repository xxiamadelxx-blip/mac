# Visual Lab — Review Checklist

Этот чеклист используется для каждого нового или существенно переработанного visual candidate.

## 1. Перед производством

- [ ] Репозиторий и target stage проверены.
- [ ] Прочитаны AGENTS.md и весь входной пакет Visual Lab.
- [ ] Источник/канон отделён от открытой creative choice.
- [ ] Определены asset_id и family_id.
- [ ] Понятно, это hero master, variant, UI state, VFX, animation или runtime instance.
- [ ] Для новой существенной визуальной единицы получен выбор Creative Director до production batch.

## 2. Candidate package

- [ ] Immutable candidate_id.
- [ ] Provenance заполнен по CANDIDATE_PROVENANCE_TEMPLATE.json.
- [ ] Source/reference IDs или hashes указаны.
- [ ] Editable source path/hash указан, если применимо.
- [ ] Tool/model/version/workflow/seed указаны, если применимо.
- [ ] Post-processing перечислен.
- [ ] Runtime export path/hash и producing commit указаны.
- [ ] Parent approved master указан для derived variant.

## 3. Identity review

- [ ] Identity, silhouette и role читаются.
- [ ] Body proportions, face/hair, outfit/material и equipment согласованы с family.
- [ ] Palette/value separation соответствуют проекту.
- [ ] Asymmetry и direction semantics не сломаны зеркалированием.
- [ ] Ground contact, pivot и semantic anchors корректны.
- [ ] Повторяющийся дефект не замаскирован локальным patch-ом.

## 4. Gameplay/UI review

Для world/battle assets:

- [ ] Есть enlarged inspection view.
- [ ] Есть true 1x gameplay-scale view.
- [ ] Есть representative arena/map context.
- [ ] Герой, враг, projectile, telegraph и XP остаются читаемыми.
- [ ] Нет misleading footprint, clipping или broken transparency.
- [ ] Останки, VFX и ambient layers не скрывают playable/readability-critical элементы.

Для UI/design assets:

- [ ] Проверен viewport 390x844.
- [ ] Safe area соблюдена.
- [ ] Normal/pressed/disabled/locked states различимы.
- [ ] Русский текст не обрезается и не ломает иерархию.
- [ ] Touch targets не становятся слишком маленькими.
- [ ] Слой не перехватывает ввод у более высокого слоя.

## 5. Technical QA

- [ ] Размеры, формат, color mode и alpha корректны.
- [ ] Pivot, anchors, frame order и direction semantics корректны.
- [ ] Имена и пути соответствуют manifest.
- [ ] Нет внешних или случайных абсолютных зависимостей.
- [ ] Экспорт воспроизводится и не создаёт uncontrolled drift.
- [ ] Godot/runtime import проверен, если asset уже подключается.
- [ ] Performance budget проверен, если asset массовый или particle-heavy.

Technical PASS фиксируется отдельно и не меняет artistic status.

## 6. Human approval

- [ ] Review pack показывает exact candidate, ID и commit.
- [ ] Creative Director явно выбрал APPROVE, REJECT или REVISION.
- [ ] Решение записано в stage/family/approval record.
- [ ] REJECTED candidate помечен non-promotable.
- [ ] При APPROVE сохранён exact approved output/capture/hash.
- [ ] Golden baseline не создан автоматически тестом или предыдущим запуском.

## 7. Promotion

- [ ] Approved candidate имеет runtime manifest entry.
- [ ] Manifest ссылается на stable asset/family ID.
- [ ] Consumer scene/UI использует approved path.
- [ ] Fallback обозначен отдельно и диагностируем.
- [ ] Production promotion проверен после интеграции.
- [ ] Stage README и handoff обновлены, если задача это включает.

## 8. Итоговый статус

Используй только одно из значений:

PROPOSAL / CANDIDATE / TECHNICAL PASS / USER REVIEW / APPROVED GOLDEN / PRODUCTION / REJECTED NON-PROMOTABLE

Нельзя писать DONE, если обязательное evidence отсутствует.
