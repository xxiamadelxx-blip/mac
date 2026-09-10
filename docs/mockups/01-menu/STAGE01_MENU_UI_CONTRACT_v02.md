# Stage 01 — Menu UI Contract v02

Status: USER REVIEW — soft tonal candidate family prepared; Godot implementation and artistic approval are pending.

## Current visual family

- Family: moonveil-menu-soft-tonal-v02.
- Target viewport: 390×844 portrait.
- Safe area: at least 16 dp on sides and 24 dp top/bottom.
- Materials: matte deep blue-gray panels, smoky teal environment, warm ivory type, muted brass borders, mist-jade selected state.
- Red/garnet is a restrained identity accent only; no toxic/neon state.
- Current visual candidates: STAGE01_MENU_VISUAL_FAMILY_v02.md.

## Screen inventory

| screen_id | Russian label | Main action |
|---|---|---|
| home | Home | ПЕРСОНАЖИ, Арсенал, Артефакты, Настройки, Начать забег |
| characters | Персонажи | выбрать Линь Юэ или Соён Хан |
| run_setup | Подготовка забега | выбрать персонажа/артефакты, начать забег |
| loading | Загрузка | показать прогресс и подсказку |
| victory | Победа | посмотреть результат, забрать награды, в меню |
| run_ended | Поражение | повторить, забрать сохранённую награду, в меню |

## Navigation contract

Home → Персонажи → Подготовка забега → Загрузка → Арена  
Home → Подготовка забега → Загрузка → Арена  
Арена → Победа → Забрать награды → Home  
Арена → Поражение → Повторить → Подготовка забега

Claim Rewards атомарно завершает reward ledger. Повторное нажатие не начисляет Gold, Lunar Seals или Boss Essence повторно.

## Russian string baseline

| key | Русский baseline |
|---|---|
| menu.start_run | Начать забег |
| menu.characters | Персонажи |
| menu.arsenal | Арсенал |
| menu.artifacts | Артефакты |
| menu.settings | Настройки |
| menu.select_character | Выбрать персонажа |
| menu.run_setup | Подготовка забега |
| menu.loading | Загрузка |
| menu.claim_rewards | Забрать награды |
| menu.try_again | Повторить |
| menu.return_home | В меню |
| menu.run_ended | Поражение |
| menu.victory | Победа |
| menu.checkpoint_saved | Награда контрольной точки сохранена |

ПЕРСОНАЖИ и Выбрать персонажа намеренно не ограничивают будущий roster только героинями.

## Layer contract

Generated composites are visual candidates only. Runtime screen remains split into:

1. background/environment;
2. character art;
3. decorative VFX;
4. panels/frames;
5. icons;
6. localization text;
7. buttons and interaction states;
8. accessibility feedback.

Required button states: normal, pressed, disabled, locked, loading. Touch target: minimum 48×48 dp.

## Handoff

route: UI_ART + secondary MOCKUP  
status: USER REVIEW  
technical_status: 390×844/sRGB verified; Godot import pending  
artistic_status: PENDING  
runtime_manifest: not promoted  
next_action: Creative Director reviews the exact v02 family, then UI is reconstructed as real Godot controls.
