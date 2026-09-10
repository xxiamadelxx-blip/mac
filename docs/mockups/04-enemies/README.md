# Stage 04 — Enemies

Status: **IN PROGRESS**.

Primary route: `MOCKUP`  
Secondary route: `SPRITE`  
Stage path: `docs/mockups/04-enemies/`  
Family ID: `family.enemy.moonveil-soft-tonal.v01`

## Цель

Создать единый читаемый roster из десяти противников для массового top-down survivors-like боя. Враг должен распознаваться по силуэту, движению и телеграфу на true 1x камере 390×844, а не только по цвету или подписи.

## Канонический roster

| enemy_id | Имя | Роль | B1 durability | XP | Первая полоса |
|---|---|---|---:|---:|---|
| `ink_beetle` | Чернильный жук | прямой быстрый rusher | ×1.0 | 1–5 | 0–2 мин |
| `lantern_moth` | Фонарь-мотылёк | ranged, медленные снаряды | ×1.2 | 5 | 2–5 мин |
| `bone_carp` | Костяной карп | line-lock dash | ×1.4 | 5–15 | 2–5 мин |
| `paper_ghost` | Бумажный призрак | telegraphed teleport | ×1.3 | 5–15 | 5–10 мин |
| `jade_toad` | Нефритовая жаба | leap + poison landing zone | ×1.6 | 15 | 5–10 мин |
| `mirror_fox` | Зеркальный лисёнок | decoy / direction confusion | ×1.5 | 15 | 5–10 мин |
| `bell_crab` | Колокольный краб | frontal guard / rear weakness | ×2.4 | 15–40 | 10–15 мин |
| `thread_doll` | Нитяная кукла | slow beam / distance control | ×1.8 | 15–40 | 10–15 мин |
| `stone_oni` | Каменный они | slow elite / ground slam | ×7.0 | 40–80 | 10–15 мин |
| `eclipse_serpent` | Змей затмения | fast elite / dark trail + arcs | ×8.0 | 80 | 15–20 мин |

Источник чисел и поведения: `docs/BALANCE_ECONOMY_SPEC.md`. Абсолютные base HP/damage/speed по enemy_id в текущем B1 не заданы, поэтому они остаются `PENDING_B1` и не выдумываются в visual package.

## Visual family v01

Общее направление наследует актуальную soft-tonal family проекта:

- тёмный сине-серый/чернильный body mass;
- дымчатый teal и muted jade для сверхъестественных деталей;
- warm ivory для бумаги, кости и слабых зон;
- muted brass для колоколов/фурнитуры;
- приглушённый crimson только для опасных телеграфов и eclipse corruption;
- никаких кислотных cyan/green/red заливок;
- silhouette-first: форма тела и способ движения различаются сильнее, чем hue;
- combat sprite проще портретного арта и не превращается в крупного персонажа, забивающего поле.

## Scale classes

- `S`: ink_beetle, lantern_moth.
- `M`: bone_carp, paper_ghost, jade_toad, mirror_fox, thread_doll.
- `L`: bell_crab.
- `XL_ELITE`: stone_oni, eclipse_serpent.

Scale class — относительная визуальная категория, не абсолютный pixel size. Точный runtime footprint фиксируется после representative true 1x review и не должен лгать о collision.

## Telegraph language

- rusher: короткий body lean / ink wake, без большой warning zone;
- ranged moth: warm-ivory lantern pulse перед projectile;
- carp dash: тонкая line-lock полоса до рывка;
- ghost teleport: flicker + paper fragments в точке исчезновения/появления;
- toad leap: landing circle появляется до приземления;
- mirror fox: копия визуально слабее по value/opacity, но силуэт тот же;
- crab: frontal shell plate читается как блок, rear seam как weakness;
- thread doll: тонкий beam-telegraph до slow connection;
- stone oni: большой ground circle до slam;
- eclipse serpent: dark trail не маскирует damaging arcs; дуги имеют отдельный warning edge.

## Фактическое evidence текущей итерации

Созданы и лежат в stage-папке:

- `STAGE04_ENEMIES_MANIFEST_v01.json` — stable enemy_id, роли, фазы, B1 durability/XP, silhouette keys и telegraph contracts для всех 10 врагов;
- `STAGE04_ENEMIES_VISUAL_CONTRACT_v01.md` — единая soft-tonal family, scale/readability и representative-master gate;
- `STAGE04_ENEMY_ROSTER_SILHOUETTES_v01.svg` — silhouette calibration board полного roster;
- `STAGE04_ENEMY_INK_BEETLE_MASTER_v01.svg` — enlarged representative master Чернильного жука;
- `STAGE04_ENEMY_INK_BEETLE_GAMEPLAY_REVIEW_v01.svg` — true 1× 390×844 gameplay review;
- `STAGE04_ENEMIES_PROVENANCE_v01.json` — provenance и раздельные technical/artistic statuses.

## Representative master gate

Первый representative master: `ink_beetle` / Чернильный жук.

Asset ID: `enemy.ink_beetle.master`  
Candidate ID: `vl-20260909-enemy-ink-beetle-master-v01`  
Asset kind: `enemy master mockup / sprite direction`  
Status: `CANDIDATE`  
Technical status: `REFERENCE_PASS_PENDING_RUNTIME`  
Artistic status: `PENDING`  
Runtime: `NOT_PROMOTED`

Representative master и true 1× evidence уже созданы. До artistic review production batch остальных девяти врагов не получает статус `APPROVED GOLDEN`/`PRODUCTION`.

## Deliverables этапа

- [x] source/canon audit;
- [x] enemy family contract;
- [x] roster manifest с десятью stable enemy_id;
- [x] silhouette/readability board;
- [x] representative master + enlarged inspection + true 1x arena context;
- [ ] девять derived enemy candidates;
- [ ] telegraph board полного roster;
- [x] provenance для текущих candidates;
- [ ] B1 reconciliation для абсолютных HP/damage/speed;
- [ ] финальный stage handoff и closure evidence.

## Handoff

- `route`: MOCKUP + secondary SPRITE
- `stage_path`: docs/mockups/04-enemies/
- `asset_kind`: enemy family / enemy master / sprite mockup
- `family_id`: family.enemy.moonveil-soft-tonal.v01
- `candidate_id`: vl-20260909-enemy-ink-beetle-master-v01
- `status`: CANDIDATE
- `technical_status`: REFERENCE_PASS_PENDING_RUNTIME
- `artistic_status`: PENDING
- `manifest/consumer`: STAGE04_ENEMIES_MANIFEST_v01.json; runtime not promoted
- `open_decisions`: artistic review representative master; exact runtime footprint; B1 absolute base HP/damage/speed
- `next_action`: generate nine derived enemy candidates under the locked family contract, then assemble the complete telegraph/readability board
