# Stage 05 — Bosses
Status: PLANNED.
Мокапы четырёх боссов и фаз.
Фактические результаты этапа, preview и evidence добавляются сюда после начала этапа. Пустая папка или этот README сами по себе не означают DONE.
Naming: STAGE##_AREA_TYPE_v##.

## Content-design brief v01 — text-only input

Это контентный бриф для Visual Lab, а не готовый мокап, preview или production asset. Он заполняет content-зону стадии и не меняет protected first-run enemy/boss assets.

| Field | Value |
|---|---|
| status | PROPOSAL |
| technical_status | NOT_RUN |
| artistic_status | PENDING |
| runtime | NOT_PROMOTED |
| source | docs/agents/content-design/C3_MINI_BOSSES_AND_CHEST_FLOW.md |
| visual route | SPRITE + VFX + UI_ART |
| asset_id / family_id / candidate_id | null до intake Visual Lab |
| dependencies | BossDirector/checkpoint registry, C1 synergy resolver, Balance telegraph/encounter budget |
| next action | Visual Lab выбирает representative encounter после content/architecture reconciliation |

### Encounter roster input

Первые три main-boss записи и финальный boss остаются protected existing content. Ниже — две новые main-boss записи и пять mini-boss записей из C3; их ID имеют статус PROPOSAL/REGISTRY_SYNC_PENDING до подтверждения Architecture.

| checkpoint | encounter_kind | stable content ID | identity and player decision | readable counterplay | reward boundary | dependencies |
|---:|---|---|---|---|---|---|
| 1200 s / 20:00 | MAIN_BOSS | boss_tideglass_regent | Регент Чёрного Прилива — flow director; выбрать безопасный коридор или переждать convergence ради окна уязвимости | источник прилива и дуга сначала читаемо предупреждают, затем разрешаются; дуги не становятся невидимыми стенами | один non-final BOSS_CHEST: synergy если есть eligible pair, иначе fallback | C1 synergy resolver; BossDirector; PENDING_BALANCE |
| 1500 s / 25:00 | MAIN_BOSS | boss_omen_paper_archivist | Архивариус Лунных Знаков — pattern sequencer; уничтожить активный знак, сменить позицию или сохранить cooldown под vulnerability window | warm-ivory порядок печатей и линия активации видны заранее; phase меняет ритм, не grammar telegraph | один non-final BOSS_CHEST; final-boss no-chest rule сохраняется | C1 synergy resolver; BossDirector; PENDING_BALANCE/PENDING_B1 |
| 450 s / 07:30 | MINI_BOSS | miniboss_ink_jade_warden | Чернильный Нефритовый Страж — space controller; найти следующий проход между складывающимися линиями | ground seals → visible lines → resolve; gap остаётся проходимым | один MINI_BOSS BOSS_CHEST; synergy/fallback | C3 checkpoint flow; C1 resolver; PENDING_BALANCE |
| 750 s / 12:30 | MINI_BOSS | miniboss_veil_harvester | Жнец Завесы — priority hunter; продолжать damage или сначала очистить delayed threat route | shadow marker и порядок разрешения видны; decoy не скрывает реальный telegraph | один MINI_BOSS BOSS_CHEST; claim расходует общий cap только при synergy | C3 checkpoint flow; C1 resolver; PENDING_BALANCE/PENDING_ARCHITECTURE |
| 1050 s / 17:30 | MINI_BOSS | miniboss_lotus_ritekeeper | Хранительница Лотосового Обряда — support ritual controller; ломать anchor или использовать окно для damage | ivory anchor, link и exposed anchor читаемы; ритуал не создаёт full-arena lock | один MINI_BOSS BOSS_CHEST; synergy/fallback, без artifact offer | C3 checkpoint flow; C1 resolver; PENDING_BALANCE |
| 1350 s / 22:30 | MINI_BOSS | miniboss_bell_rhythm_ascetic | Колокольный аскет — timing/rhythm controller; пересечь gap, держать позицию или отступить | внешний и внутренний resonance ring видны до resolve; audio/haptic лишь усиливают сигнал | один MINI_BOSS BOSS_CHEST; synergy/fallback | C3 checkpoint flow; C1 resolver; PENDING_BALANCE |
| 1650 s / 27:30 | MINI_BOSS | miniboss_moonroot_ferryman | Луннокорневой перевозчик — convoy pressure; выбрать точку перехвата маршрута | route и endpoint видны, convoy не телепортируется и не создаёт permanent collision wall | один MINI_BOSS BOSS_CHEST; synergy/fallback, без wallet mutation | C3 checkpoint flow; C1 resolver; PENDING_BALANCE |

### Encounter and visual language

- Регент: высокий силуэт из тёмных полупрозрачных пластин, три приливных кольца, warm-ivory crest; smoky teal resolve и jade edge.
- Архивариус: бумажный веер талисманов, прямоугольная лунная маска, подвесные печати; ivory outline, muted brass resolve, smoky teal impact.
- Страж: broad shoulders, smoky-jade mask, ink ribbons as geometric lines; no toxic neon ink.
- Жнец: blue-grey hood, crescent mask, restrained violet status accent; telegraph не должен сливаться с тенью.
- Хранительница: folded lotus crown, three anchor seals, smoky-teal links.
- Аскет: narrow silhouette, visible brass bell, concentric ivory rings; читаемость не зависит от звука.
- Перевозчик: low moonroot barge, crescent lantern, ivory route line; distinct from moonroot_burrower and Bell Crab.

Каждый encounter обязан иметь safe external spawn, phase identity, visible warning → resolve → cleanup lifecycle, defeat attribution и один reward boundary. Точные HP, damage, speed, warning lead, duration, resistance, add budget, phase threshold и VFX cap — PENDING_BALANCE/PENDING_B1.

### Chest cadence and synergy boundary

C01–C10 дают десять отдельных non-final boss chest opportunities: main checkpoints 300/600/900/1200/1500 и mini checkpoints 450/750/1050/1350/1650. Общий лимит — максимум 5 synergy claims за забег. При отсутствии eligible pair или после cap применяется fallback; ELITE_CHEST и final boss не превращаются в synergy chest.

Final boss на 1800 s / 30:00 не создаёт boss chest. Artifact offer не выдаётся из BOSS_CHEST: артефакты идут через ELITE_PACK/FIRST_CLEAR_REWARD по C2.

### Visual Lab intake boundary

- route: SPRITE + VFX + UI_ART;
- stage_path: docs/mockups/05-bosses/;
- asset_id, family_id, candidate_id: null;
- status: PROPOSAL;
- technical_status: NOT_RUN;
- artistic_status: PENDING;
- manifest/consumer: NOT_PROMOTED; consumer proposal — BossDirector, TelegraphResolver, ChestResolver, SynergyInfo;
- evidence: отсутствует до фактического mockup/review;
- нельзя объявлять эту текстовую запись завершённой, утверждённой или готовой к игре.
