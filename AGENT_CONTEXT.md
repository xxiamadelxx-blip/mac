<!-- LIVE-AGENT-SYNC: read docs/AGENT_SYNC_STATE.md at current main before using this file -->
> **Live coordination pointer:** continuation work is routed through [`docs/AGENT_SYNC_STATE.md`](docs/AGENT_SYNC_STATE.md). Legacy 20-minute/4-boss passages below are historical until reconciled.

# AGENT_CONTEXT — Moonveil: Eclipse

Этот файл — каноническая точка передачи проекта следующему агенту без потери решений и статусов.

## 1. Репозиторий и текущая точка

- Репозиторий: `xxiamadelxx-blip/mac`.
- Основная ветка: `main`.
- Целевая платформа M1: Android.
- Движок: Godot 4.x, native 2D, GDScript.
- Пользователь не обязан иметь ПК; сборка и проверка APK должны быть доступны через удалённую среду.

Текущий содержательный этап: **4 — мокапы противников**.

Фактический статус этапов:

- Этап 1, меню: `IN PROGRESS`. Есть русские UI-слои, Godot navigation prototype и soft-tonal v02 candidate family. Artistic approval и полный runtime/APK evidence ещё не закрыты.
- Этап 2, арена: `IN PROGRESS`. Зафиксирован большой мир минимум 1560×2532 world units, камера 390×844, открытое поле, живой ландшафт, вода/растения/частицы, накопление следа боя и runtime-preview. Godot/Android acceptance 0→20 минут ещё не закрыт.
- Этап 3, две героини: `DONE` как visual mockup/evidence package. Линь Юэ и Соён Хан имеют portrait/full-body reference, шесть боевых состояний, четыре направления, true 1x и enlarged gameplay review, VFX bindings и provenance. Эти визуалы остаются `CANDIDATE` / artistic `PENDING`, не `APPROVED GOLDEN` и не `PRODUCTION`.
- Этап 4, противники: **начат**. Канон берётся из `GAME_MANIFEST.md` и `docs/BALANCE_ECONOMY_SPEC.md`; stage package хранится в `docs/mockups/04-enemies/`.

Нельзя писать, что игра, APK, M1 или visual production готовы, если это не подтверждено фактическим evidence.

## 2. Что строим

Moonveil: Eclipse / «Падение Лунного сада» — оригинальная мобильная 2D survivors-like / bullet heaven игра. Первый вертикальный срез — один завершённый 20-минутный забег:

- две героини;
- одна большая карта Затопленного сада Лунного лотоса;
- 10 противников;
- 4 босса на 5/10/15/20 минутах;
- 10 оружий;
- 10 пассивок;
- 10 синергий/эволюций;
- артефакты, XP, HUD, upgrade choice, пауза, смерть, победа и локальное сохранение.

Не копировать персонажей, ассеты, интерфейсы, сюжет или названия Crimsonland, Magic Survival, Vampire Survivors и конкретных гача-игр.

## 3. Технологический контракт

- Godot 4.x, native 2D renderer, GDScript.
- Вертикальный viewport 9:16; рабочий контрольный viewport `390x844`.
- Android APK для ручного тестирования, AAB для релиза.
- Офлайн-first; локальное версионируемое сохранение.
- Данные оружия, врагов, боссов и артефактов должны быть data-driven.
- Массовые враги, снаряды, XP и VFX используют pooling/controlled spawn.
- Цель 60 FPS, безопасный режим не ниже 30 FPS на Android среднего класса.
- Ошибки ресурсов должны иметь диагностируемый fallback, а не белый экран.

## 4. Визуальная система

Текущее направление после пользовательской правки — **единая мягкая tonal family**, без токсичной кислотности и вырвиглазных неонов.

База:

- глубокий сине-серый ночной фон;
- дымчатый teal;
- тёплый ivory;
- приглушённая brass-фурнитура;
- мягкий jade как основной магический акцент;
- приглушённый crimson только там, где он несёт identity/опасность;
- читаемые силуэты и телеграфы важнее декоративной детализации;
- портреты могут быть детальнее, combat sprites должны хорошо читаться в массовой волне.

Меню использует гендерно-нейтральную категорию **ПЕРСОНАЖИ**, а не «героини», поскольку roster может включать мужчин и зооморфов.

Арена — не пустой фон и не тесная комнатка. `390x844` — окно камеры, а не размер карты. Мир минимум 4×3 viewport. Центральное поле оставляет пространство для кругового движения; вода, дорожки, корни, мостики, камни и растения создают ландшафт, а не стены декора.

После смерти враги оставляют persistent aftermath: тела, конечности, обломки, ткань, кость, чернильно-кровавые следы или другие фрагменты по `enemy_id`. Этот слой не имеет collision и не заменяет XP.

## 5. Visual Lab обязателен

Для UI/art/sprite/mockup всегда выполнять маршрут из:

1. `AGENTS.md`;
2. `visual_lab/README.md`;
3. `visual_lab/VISUAL_POLICY_RULE.md`;
4. `visual_lab/VISUAL_LAB_PRODUCTION_LAW.md`;
5. `visual_lab/ASSET_PIPELINE_CODE.md`;
6. `visual_lab/REVIEW_CHECKLIST.md`;
7. `visual_lab/UI_ART_SPRITE_MOCKUP_WORKFLOW.md`;
8. README/contract/manifest целевого stage.

Обязательная цепочка:

`SOURCE/CANON AUDIT -> VISUAL FAMILY -> REPRESENTATIVE MASTER -> CANDIDATE + PROVENANCE -> USER REVIEW -> EDITABLE MASTER -> VARIANTS -> RUNTIME EXPORT -> TECHNICAL QA -> TRUE 1X PREVIEW -> USER FINAL APPROVAL -> GOLDEN/MANIFEST -> PRODUCTION`.

Technical PASS не равен artistic approval. PNG/SVG/mockup/capture не становится production art автоматически.

Допустимые visual statuses:

`PROPOSAL / CANDIDATE / TECHNICAL PASS / USER REVIEW / APPROVED GOLDEN / PRODUCTION / REJECTED NON-PROMOTABLE`.

## 6. Balance & Economy

Единственный числовой источник текущего baseline: `docs/BALANCE_ECONOMY_SPEC.md`.

Нельзя подправлять числа ad hoc в коде или мокапах. Сначала меняется B1 source, затем связанные manifests/cards/tests.

Волны первого среза:

- 0–2 мин: жуки;
- 2–5 мин: жуки, мотыльки, карпы;
- 5–10 мин: добавляются призраки, жабы, лисы;
- 10–15 мин: добавляются крабы, куклы, элиты;
- 15–20 мин: весь roster и усиленные элиты.

Канонические противники этапа 4:

1. Чернильный жук — быстрый rusher.
2. Фонарь-мотылёк — ranged, медленные снаряды.
3. Костяной карп — фиксирует линию и делает рывок.
4. Бумажный призрак — телепорт после видимого мерцания.
5. Нефритовая жаба — прыжок и ядовитая зона приземления.
6. Зеркальный лисёнок — ложная копия с меньшим HP.
7. Колокольный краб — защита спереди, уязвимость сзади.
8. Нитяная кукла — луч-замедление с контролем дистанции.
9. Каменный они — медленный elite, круговой удар по земле.
10. Змей затмения — быстрый elite, тёмный след и дуги.

B1 уже фиксирует durability multipliers и XP bands, но абсолютные base HP/damage/speed по enemy_id должны быть подтверждены в B1 до закрытия этапа 4. Их нельзя выдумывать только внутри visual manifest.

## 7. Правило работы по этапу

Перед началом:

- проверить stage status и существующие файлы;
- отделить канон от creative choice;
- определить deliverables, stable IDs, family IDs и candidate IDs;
- не расширять текущий этап задачами следующих этапов.

Во время:

- один representative master до production batch;
- enlarged inspection + true 1x gameplay context для world/sprite candidate;
- телеграф и роль должны читаться по силуэту/действию, а не только по подписи;
- массовые сущности проектировать с performance budget;
- open decisions и отсутствующее evidence помечать `PENDING/UNVERIFIED`, а не додумывать.

После:

- сверить deliverables;
- приложить evidence/provenance;
- обновить stage README/index/context;
- отдельно записать technical и artistic status;
- передать один проверяемый следующий шаг.

## 8. Definition of Done

Этап нельзя объявлять `DONE` по наличию папки, описания или красивого preview.

Для этапа 4 нужны как минимум:

- 10 узнаваемых enemy families;
- стабильный `enemy_id` для каждого;
- размер/scale class, цветовой маркер, силуэт, роль, движение, атака, уязвимость, phase appearance;
- B1-согласованные durability/HP, damage, speed, wave multipliers, spawn restrictions и XP grade/value;
- readable attack telegraphs;
- enlarged и true 1x representative gameplay evidence;
- provenance и техническая проверка;
- явный artistic status пользователя;
- отсутствие незаявленных production placeholders.

## 9. Канонические пути

- `/README.md`
- `/GAME_MANIFEST.md`
- `/ROADMAP.md`
- `/AGENT_CONTEXT.md`
- `/docs/MOCKUP_INDEX.md`
- `/docs/BALANCE_ECONOMY_SPEC.md`
- `/docs/mockups/04-enemies/`
- `/visual_lab/`

## 10. Точка продолжения

Этап 4 начинается с route `MOCKUP` + secondary `SPRITE`.

Первый пакет должен:

1. зафиксировать source/canon audit десяти противников;
2. задать общий enemy visual family в мягком tonal-направлении;
3. создать silhouette board для различимости roster;
4. создать один representative master — **Чернильный жук** — и true 1x gameplay review;
5. зафиксировать provenance и gaps B1;
6. остановить production batch до review representative master, если пользователь не утвердил направление явно.

Следующее содержательное действие после representative master review: выпуск кандидатов остальных девяти противников с тем же family contract, затем telegraph/readability board и проверка полного roster.