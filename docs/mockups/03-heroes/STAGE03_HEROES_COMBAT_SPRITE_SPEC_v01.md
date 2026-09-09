# Этап 03 — боевые 2D-спрайты героинь v01

Статус пакета: **DONE** — Visual Lab mockup/evidence обновлён до художественной ревизии **v02**.  
Статус ассетов: **CANDIDATE**.  
Runtime promotion: **NOT_PROMOTED**.

## Источник и границы

Десять PNG предоставлены пользователем как результаты ChatGPT Images. Codex не менял их размеры, фон, палитру или композицию. Это референсные boards/mockups для дальнейшего production pipeline, а не готовые игровые текстуры.

Все новые изображения имеют цветовое пространство sRGB и не содержат alpha-канала. Чёрный фон combat/direction boards и светлый фон иллюстрационных листов сохраняются намеренно как часть исходного референса.

## Файловая карта

| Назначение | Файл | Размер |
|---|---|---:|
| Линь Юэ full-body | docs/mockups/03-heroes/layers/STAGE03_HERO_LIN_YUE_FULLBODY_v02.png | 1024×1536 |
| Линь Юэ portrait | docs/mockups/03-heroes/layers/STAGE03_HERO_LIN_YUE_PORTRAIT_v02.png | 1536×1536 |
| Соён Хан portrait | docs/mockups/03-heroes/layers/STAGE03_HERO_SOYEON_HAN_PORTRAIT_v02.png | 1536×1536 |
| Линь Юэ combat states | docs/mockups/03-heroes/layers/STAGE03_HERO_LIN_YUE_COMBAT_STATES_v02.png | 1536×512 |
| Соён Хан combat states | docs/mockups/03-heroes/layers/STAGE03_HERO_SOYEON_HAN_COMBAT_STATES_v02.png | 1536×512 |
| Соён Хан direction kit | docs/mockups/03-heroes/layers/STAGE03_HERO_SOYEON_HAN_DIRECTION_KIT_v02.png | 1536×559 |
| Линь Юэ direction kit | docs/mockups/03-heroes/layers/STAGE03_HERO_LIN_YUE_DIRECTION_KIT_v02.png | 1536×559 |
| Экран выбора | docs/mockups/03-heroes/layers/STAGE03_HEROES_SELECTION_v02.png | 711×1536 |
| Gameplay: Линь Юэ | docs/mockups/03-heroes/layers/STAGE03_HERO_LIN_YUE_GAMEPLAY_REVIEW_v02.png | 711×1536 |
| Gameplay: Соён Хан | docs/mockups/03-heroes/layers/STAGE03_HERO_SOYEON_HAN_GAMEPLAY_REVIEW_v02.png | 711×1536 |

## Разметка boards

Combat states — горизонтальная доска из шести состояний в порядке idle, move, basic_attack, ability, hit, death. Direction kit — горизонтальная доска из четырёх направлений в порядке front, back, left, right. Эти boards не считаются спрайт-листами с готовыми рамками: координаты кадров и pivot будут назначены после art approval.

Для runtime-подготовки требуется:

- выделить каждый кадр;
- убрать непрозрачный фон и сохранить корректный alpha-канал;
- проверить читаемость силуэта на целевом масштабе;
- вынести отдельные VFX;
- импортировать в Godot как AnimatedSprite2D/AnimationPlayer с pivot под основанием персонажа;
- выполнить Android-проверку после появления сборочной среды.

## Gameplay scale evidence

Два gameplay mockup имеют canvas 711×1536. Его пропорция практически совпадает с целевым 390×844, но это не точный runtime capture и не доказательство работы Godot. На сценах должны читаться:

- Линь Юэ: нефритовая аура, веер, печати и контрольная зона;
- Соён Хан: красный след клинка, рывок и контрастный силуэт;
- массовая волна врагов и раздельные телеграфы/VFX.

## Visual Lab status

- Stage: DONE.
- Asset status: CANDIDATE.
- Artistic approval: PENDING.
- Runtime status: NOT_PROMOTED.
- Следующий обязательный шаг: art review, alpha/frame extraction и Godot/Android smoke test.
