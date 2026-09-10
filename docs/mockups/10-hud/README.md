# Stage 10 — HUD
Status: PLANNED.
HUD игрового забега.
Фактические результаты этапа, preview и evidence добавляются сюда после начала этапа. Пустая папка или этот README сами по себе не означают DONE.
Naming: STAGE##_AREA_TYPE_v##.

## Content-design brief v01 — run HUD information contract

Это текстовый content/UX brief для будущего mockup. Он описывает информацию, состояния и readable hierarchy, но не создаёт layout, PNG/SVG, font treatment или production asset.

| Field | Value |
|---|---|
| status | PROPOSAL |
| technical_status | NOT_RUN |
| artistic_status | PENDING |
| runtime | NOT_PROMOTED |
| source | docs/agents/content-design/C1_WEAPONS_PASSIVES_SYNERGIES.md; C2_ARTIFACTS.md; C3_MINI_BOSSES_AND_CHEST_FLOW.md + screenshot reference supplied by owner |
| visual route | UI_ART + MOCKUP |
| asset_id / family_id / candidate_id | null до Visual Lab intake |
| target viewport | 390×844 safe-area reference; exact responsive rules — PENDING_VISUAL/ENGINEERING |
| dependencies | runtime telemetry, StatsCalculator, UpgradeOffer, ArtifactOffer, SynergyInfo, BossDirector |

### HUD information blocks

| block | content that must be readable | source/consumer | state rules |
|---|---|---|---|
| run_context | elapsed run time, level and XP/progression bar, pause affordance | RunClock, Progression, Pause | target run is 30:00/1800 s; exact clock behavior follows Architecture, not this brief |
| hero_state | health/current max health, healing-per-second state, healing mote/ward feedback, damage-taken/defense state | HealthSystem, Meta tree, passives, artifacts | never hide a lethal/active hazard behind a persistent aura; temporary ward has explicit active/consumed state |
| movement_and_tempo | movement-speed axis, evasion/poise feedback, active MOMENTUM or shared tempo state | MovementSystem, passive_wind_of_travel, passive_iron_bell, passive_frost_thread | show state transition only when active; no permanent screen-wide effect |
| loadout | six weapon slots and six passive slots, stable icon/name, current level/rank, empty/locked/maxed state | WeaponRegistry, PassiveRegistry, UpgradeOffer | bound weapon hint may show synergy eligibility; passive remains a global run modifier |
| combat_stats | attack power, attack multiplier, all magic damage, spell size, spell duration, spell cooldown, crit chance, crit power | StatsCalculator + pause/stat projection | values come from authoritative stats; no hard-coded numbers in content layer |
| defense_and_enemy_stats | received damage modifier, evasion, enemy max HP modifier | StatsCalculator + pause/stat projection | negative/positive direction and source tooltip must be unambiguous |
| collection | XP/mana gain and pickup radius; pickup/route feedback | Magnet/Progression, passive_spirit_lens, meta_magnet | XP, mana, gold, healing and artifacts remain distinct resource semantics |
| encounter | current main boss/mini-boss/elite banner, checkpoint label, phase/telegraph cue and recovery cue | BossDirector, TelegraphResolver, ChestResolver | main-boss clock-freeze behavior and mini-boss continue behavior are shown only after Architecture contract; no invented animation timing |
| synergy | progress 0/5 claims, eligible pair, required weapon/passive levels, chest source, claimed/evolved state | SynergyResolver, SynergyInfo | claim counter never exceeds 5; final boss has no synergy chest |
| artifact | owned artifact markers, active trigger feedback, three-card offer → choose one state | ArtifactEffectSystem, Artifact UI | artifacts use separate collection, never weapon/passive slots |
| feedback_layers | XP gain, pickup confirmation, damage/heal, chest, artifact offer and upgrade offer channels | runtime event projections | avoid competing full-screen layers; each event has source and expiry |
| pause_detail | detailed stat sheet matching canonical stat keys plus Continue action | Pause/Stats projection | pause is informational; it must not imply runtime/balance values not supplied by authoritative systems |

### Canonical stat labels for pause/stat surface

The reference screen's semantic list is retained: Здоровье, Исцеление в сек, Исцеление от крупицы, Получаемый урон, Уклонение, Скорость движения, Шанс крит. удара, Усиление крит. удара, Сила атаки, Приумножение атаки, Весь магический урон, Размер заклинаний, Длительность заклинаний, Перезарядка заклинаний, Макс. HP врага, Получение маны/опыта, Радиус сбора предметов. Exact values, signs, order of calculation and localization remain owned by Balance/Architecture/Product.

### Readability and state rules

- Gameplay HUD uses compact persistent indicators; detail belongs to pause/stat state and tooltips.
- Boss and mini-boss telegraphs remain in the arena layer; HUD may label the phase but must not replace world-space warning.
- Artifact, passive and synergy colors follow the visual code: deep blue-grey, smoky teal, warm ivory, muted brass, soft jade; crimson/violet are role/status accents.
- Icons need shape distinction at true 1×; color alone cannot distinguish weapon, passive, artifact, pickup or telegraph.
- Locked, unavailable, cap-reached, consumed and active states require different copy/icons; never use an empty/blank card as an error state.
- All numeric fields and responsive spacing are PENDING_BALANCE/PENDING_ARCHITECTURE/PENDING_VISUAL.

### Visual Lab intake boundary

- route: UI_ART + MOCKUP;
- stage_path: docs/mockups/10-hud/;
- asset_id/family_id/candidate_id: null;
- status: PROPOSAL;
- technical_status: NOT_RUN;
- artistic_status: PENDING;
- manifest/consumer: NOT_PROMOTED; consumer proposal — HUD projection, Pause/Stats, UpgradeOffer, Artifact UI, SynergyInfo;
- evidence: отсутствует до фактического mockup/review.
