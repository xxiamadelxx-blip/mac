# C0 — Content Audit и границы нового каталога

Статус среза: `READ_ONLY_AUDIT_COMPLETE`

Этот документ фиксирует, от чего строится новый content package. Он не переписывает канонические документы и не объявляет runtime или визуалы готовыми.

### Revision note после product review

Первоначальный C1-дизайн passives, слишком прямо усиливавших свои парные weapons, отклонён. Текущая revision в `C1_WEAPONS_PASSIVES_SYNERGIES.md` делает все 10 run-passives общими модификаторами билда; weapon ID сохраняется только как synergy anchor для evolution gate. Лимит synergy claims пересмотрен с 3 до 5, а два дополнительных chest windows оформлены в `C3_MINI_BOSSES_AND_CHEST_FLOW.md`.

## 1. Идентичность и evidence

| Поле | Значение |
|---|---|
| Repository | `xxiamadelxx-blip/mac` |
| Branch | `main` |
| Live HEAD на момент аудита | `3f5b903a27b17f5a9f0818a3a5a479c1090a10cc` |
| Рабочая область этого среза | `docs/agents/content-design/` |
| Изображение-референс | Пользовательский файл `1000046711.jpg`; в репозиторий не добавляется |
| Runtime status | `NOT_IMPLEMENTED` по runtime-пакету |
| Visual status | briefs only; production assets не создаются |

## 2. Прочитанные источники

### Канон и продукт

- `AGENTS.md`
- `README.md`
- `GAME_MANIFEST.md`
- `AGENT_CONTEXT.md`
- `ROADMAP.md`
- `docs/BALANCE_ECONOMY_SPEC.md`
- `docs/MOCKUP_INDEX.md`

### Архитектурный контракт первого забега

- весь `docs/architecture/first-run/`, включая `FIRST_RUN_ARCHITECTURE.md`, `FIRST_RUN_DATA_CONTRACT.json`, `FIRST_RUN_EVENT_CATALOG.md`, state machine, flow, acceptance и decisions;
- зафиксированные границы текущей архитектуры: шесть weapon slots, шесть passive slots, weapon max level 6, passive max rank 5, отдельные boss chest и artifact offer, отсутствие pre-run artifact loadout. Новый content target синергии 10/10 отмечен ниже как открытый конфликт, а не как уже синхронизированная архитектура.

### Владельцы баланса и runtime

- весь `docs/agents/balance-economy/` в части README, B1 combat/XP/reward/acceptance/decisions и живой модели;
- весь `docs/agents/core-gameplay-runtime/`;
- вывод: B1 — источник чисел, Runtime — владелец фактического применения, Content Agent не дублирует их значения.

### Visual Lab и существующие stage-пакеты

- `visual_lab/README.md`
- `visual_lab/VISUAL_POLICY_RULE.md`
- `visual_lab/VISUAL_LAB_PRODUCTION_LAW.md`
- `visual_lab/ASSET_PIPELINE_CODE.md`
- `visual_lab/REVIEW_CHECKLIST.md`
- `visual_lab/UI_ART_SPRITE_MOCKUP_WORKFLOW.md`
- README/manifest текущего `docs/mockups/04-enemies/`
- README текущих `docs/mockups/05-bosses/`, `06-weapons/`, `07-passives/`, `08-artifacts/`, `09-xp/`, `10-hud/`, `16-upgrade-offers/`, `17-artifact-ui/`, `19-synergy-info/`
- README текущих `docs/manifests/11-weapon-animation/`, `12-passive-binding/`, `18-synergy-logic/` и `docs/audio/13-plan/`.

## 3. Что уже существует

| Область | Фактическое состояние | Источник | Решение Content Agent |
|---|---|---|---|
| Weapons | 10 стабильных ID и названий есть в `FIRST_RUN_DATA_CONTRACT.json` и `GAME_MANIFEST.md`; подробных entries нет | architecture contract, manifest | сохранить ID и разработать полную механику |
| Run passives | 10 стабильных ID и названий есть; подробных entries нет | architecture contract, manifest | сохранить ID и разработать ось/триггеры/контр-решения |
| Synergies/evolutions | 10 прямых пар уже перечислены; detailed evolution contract отсутствует | architecture contract, manifest | сохранить пары и описать результат; текущий product decision — не более 5 claimed synergy за run |
| Artifacts | В registry перечислены 8 ID; effect definitions пусты и имеют `PENDING_PRODUCT_DECISION` | `FIRST_RUN_DATA_CONTRACT.json` | сохранить 8, добавить 2 новые как `PROPOSAL`, не притворяться, что registry уже синхронизирован |
| Meta passives | B1 описывает 6 плоских веток по 10 рангов: Vitality, Force, Agility, Focus, Magnet, Defense | `docs/BALANCE_ECONOMY_SPEC.md` | сохранить 6 macro-веток и спроектировать внутри них 17 stat nodes с pending numeric binding |
| Stage 06–08 | Существуют только плановые README; production icons/effects отсутствуют | `docs/mockups/*` | передать briefs в Visual Lab, не создавать mockups |
| Stage 16–19 | Существуют только плановые README | `docs/mockups/*`, `docs/manifests/*` | зафиксировать UI/manifest потребности, не изменять stage-папки |
| Enemies | Stage 04 — отдельный IN PROGRESS пакет из 10 enemy families | `docs/mockups/04-enemies/` | читать как protected dependency, не переписывать |

## 4. Канонический roster и ID policy

### Weapons

`weapon_moon_blade`, `weapon_jade_talismans`, `weapon_crimson_flame_fan`, `weapon_frost_pearl`, `weapon_thunder_needles`, `weapon_spirit_bell`, `weapon_fox_mirage`, `weapon_lotus_mines`, `weapon_star_bow`, `weapon_black_eclipse_umbrella`.

### Passives

`passive_wind_of_travel`, `passive_jade_focus`, `passive_ember_heart`, `passive_frost_thread`, `passive_heavenly_seal`, `passive_iron_bell`, `passive_mirror_shard`, `passive_lotus_heart`, `passive_star_compass`, `passive_spirit_lens`.

### Synergies

`synergy_moon_dance`, `synergy_heavenly_seals`, `synergy_phoenix_sky`, `synergy_winter_palace`, `synergy_heavenly_judgment`, `synergy_guardian_bell`, `synergy_nine_reflections`, `synergy_lotus_sanctuary`, `synergy_constellation_rain`, `synergy_eclipse_vortex`.

### Artifact IDs

Существующие: `artifact_jade_compass`, `artifact_mirror_shard`, `artifact_phoenix_feather`, `artifact_frost_bead`, `artifact_bell_fragment`, `artifact_lotus_seed`, `artifact_moon_crown`, `artifact_black_bead`.

Новые предложения: `artifact_tideglass`, `artifact_silent_lantern`.

Новые ID не являются утверждёнными runtime registry records до отдельной синхронизации Architecture/Runtime.

## 5. Защищённые области

В этом срезе не изменяются:

- `AGENTS.md`, `README.md`, `GAME_MANIFEST.md`, `AGENT_CONTEXT.md`, `ROADMAP.md`;
- `docs/BALANCE_ECONOMY_SPEC.md` и `docs/agents/balance-economy/`;
- `docs/architecture/first-run/`;
- `docs/agents/core-gameplay-runtime/`;
- `scripts/`, `scenes/`, `project.godot`, `export_presets.cfg`;
- `visual_lab/`;
- все `docs/mockups/`, `docs/manifests/`, `docs/audio/` и существующие assets;
- существующие commits и чужие branches.

Допустимая запись: только новые документы внутри `docs/agents/content-design/`.

## 6. Продуктовые решения этого среза

1. Каталог первого забега содержит 10 weapons, 10 run passives, 10 direct synergy/evolution pairs и 10 artifacts.
2. Первый забег рассчитан на 30 минут / 1800 секунд и 10 нефинальных BOSS_CHEST windows: main bosses на 5/10/15/20/25 минутах и mini-bosses на 7:30/12:30/17:30/22:30/27:30; final boss chest не создаёт.
3. Для каждой synergy/evolution weapon должен быть на 10-м уровне, а связанная run passive — на 10-м ранге. Это content target, который требует сверки с текущей архитектурой 6/5.
4. Шесть weapon slots и шесть passive slots сохраняются; наличие десяти записей означает пул контента, а не расширение слотов.
5. Run passive и persistent shop node — разные сущности: первые сбрасываются между забегами, вторые живут в `MetaProgression`.
6. Artifact effect — run modifier, не slot item и не pre-run loadout. Каждый offer имеет ровно три cards и один выбор.
7. Shop tree проектируется сейчас как долгосрочный content contract, хотя текущий M1 canonical text откладывает полноценный магазин за пределы runtime vertical slice. Его дизайн не означает, что магазин уже реализован.

## 7. Зафиксированные конфликты и gaps

| ID | Наблюдение | Impact | Временная обработка | Владелец следующего решения |
|---|---|---|---|---|
| C0-01 | B1 описывает 6 flat branches × 10 ranks, пользователь запросил дерево по 17 характеристикам | меняется rank allocation и мета-экономика | сохранить шесть macro roots, 17 nodes и не писать новые числа | Balance + Product |
| C0-02 | Architecture JSON содержит устаревший `boss_rule` о продолжении таймера финального босса, а Runtime Context/B1 фиксируют freeze для всех боссов | может влиять на timing synergy/chest | content не зависит от clock; конфликт передан Architecture owner | Architecture + Product |
| C0-03 | Registry содержит 8 artifacts, пользователь запросил 10 | два новых ID пока не известны runtime | новые записи marked `PROPOSAL/REGISTRY_SYNC_PENDING` | Architecture + Runtime |
| C0-04 | В screenshot есть «Исцеление от крупицы», «Получение маны» и «Макс. HP врага», но их точная семантика не описана в B1 | требуется согласовать display и stat semantics | сделать отдельные stat nodes с явными open decisions | Product + Balance |
| C0-05 | Artifact effect values, refresh, duplicate/stacking и elite cadence pending | нельзя доказать power budget | entries fully describe behavior, all numbers pending | Product + Balance + Runtime |
| C0-06 | Полноценный shop исключён из M1 runtime scope, но нужен как persistent design | нельзя объявлять shop playable | design now, runtime integration later | Product + Runtime |
| C0-07 | Product review отклонил passives, привязанные механикой к одному weapon | старый passive contract давал узкий билд | passive effect общий для eligible build; weapon остаётся только hidden synergy anchor | Product + Balance |
| C0-08 | Product review увеличил cap с 3 до 5 и добавил 2 mini-boss encounters | меняется chest cadence, reward fallback и snapshot contract | сохранить десять нефинальных chest windows в 30-минутном забеге; final boss без chest | Architecture + Balance |
| C0-09 | Новый content gate требует weapon level 10 и passive rank 10, а текущая architecture boundary остаётся 6/5 | без сверки нельзя корректно объявить eligibility для synergy | C1/C3 фиксируют 10/10 как content target; runtime/architecture values не переписываются в C0 | Product + Architecture + Balance |

## 8. C0 verdict

Аудит подтверждает достаточную основу для C1/C2/C3: стабильные weapon/passive/synergy IDs есть, визуальная tonal family закреплена, архитектурные consumers определены. После product review узкая weapon-bound passive logic отклонена; новая общая passive logic и mini-boss chest flow вынесены в отдельную revision. Основные unresolved items вынесены в handoff и не скрыты в описаниях.

Следующий результат: `C1_WEAPONS_PASSIVES_SYNERGIES.md`, `C2_ARTIFACTS.md`, `C3_MINI_BOSSES_AND_CHEST_FLOW.md`, `META_PASSIVE_TREE.md` и сводный handoff.

## Актуальная граница C0

Аудит обновлён от живого main ec30c239aa22aa1d9c8ad1faab25d99633f4cb29.

- Контентная область закрыта структурно: каталоги, зависимости, 10/10 gate, 5 мини-боссов, 2 расширения главных боссов, active/legacy/future boundary и окна C01–C15.
- Сняты документальные расхождения, которые уже исправлены в живой архитектуре: 30-минутная сетка, 6 главных боссов, 5 мини-боссов, 10 BOSS_CHEST + 5 ELITE_CHEST и clock policy.
- Остались внешние блокеры: architecture consumer cap всё ещё 6/5 вместо content target 10/10; architecture содержит 8 артефактов и 0 typed effect definitions; Balance остаётся PARTIAL; runtime/Godot/Android и visual approval не доказаны.
- Контент не меняет эти внешние области и не объявляет их исправленными.
