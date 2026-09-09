# Этап 03 — героини

Статус: **DONE** — пакет Visual Lab mockup/evidence заменён на художественную ревизию **v02**.

## Что заменено

Старые визуальные PNG/JPG из layers удалены. Вместо них добавлены десять предоставленных пользователем PNG из ChatGPT Images:

- full-body и portrait для меню;
- combat-state boards для боевой анимационной разметки;
- четыре направления движения;
- экран выбора героинь;
- два отдельных gameplay mockup среди массовой волны.

Документы этапа сохранены и синхронизированы с новым набором. VFX bindings не менялись: их ID остаются контрактом для арены.

## Карта героинь

| Героиня | Menu anchors | Combat board | Direction kit | Gameplay |
|---|---|---|---|---|
| Линь Юэ — Нефритовая ведьма | fullbody v02, portrait v02 | combat states v02 | direction kit v02 | gameplay review v02 |
| Соён Хан — Алый клинок | portrait v02; fullbody reference отсутствует в новом наборе | combat states v02 | direction kit v02 | gameplay review v02 |

Полные пути и размеры зафиксированы в STAGE03_HEROES_MANIFEST_v01.json и STAGE03_HEROES_COMBAT_SPRITE_SPEC_v01.md.

## Важная техническая граница

Новые изображения сохранены без преобразований. Все PNG имеют opaque canvas без alpha-канала; combat/direction boards используют чёрный фон. Поэтому они являются Visual Lab candidates/references. До использования в игре нужны background removal, frame extraction, pivot, VFX separation и Godot/Android-проверка.

Gameplay и selection images имеют размер 711×1536. Это портретный source canvas с пропорцией целевого viewport 390×844, но не точный runtime screenshot 390×844.

## Состояния

Для обеих героинь зафиксирован порядок: idle, move, basic_attack, ability, hit, death.

## Документы

- STAGE03_HEROES_MANIFEST_v01.json — карта ассетов и статусы.
- STAGE03_HEROES_COMBAT_CONTRACT_v01.md — identity, состояния, направления и VFX contract.
- STAGE03_HEROES_COMBAT_SPRITE_SPEC_v01.md — размеры, фон и runtime handoff.
- STAGE03_HEROES_VFX_BINDINGS_v01.json — отдельные VFX bindings.
- STAGE03_HEROES_PROVENANCE_v01.json — источник, SHA-256 и Git blob SHA новых файлов.
