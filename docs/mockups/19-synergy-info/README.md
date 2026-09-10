# Stage 19 — Synergy Info
Status: PLANNED.
Информационный интерфейс синергий.
Фактические результаты этапа, preview и evidence добавляются сюда после начала этапа. Пустая папка или этот README сами по себе не означают DONE.
Naming: STAGE##_AREA_TYPE_v##.

## Content-design brief v01 — ten synergy/evolution entries

Это текстовый explanatory brief для будущего synergy-info mockup. Он не объявляет эволюции runtime-activated и не создаёт final art.

| Field | Value |
|---|---|
| status | PROPOSAL |
| technical_status | NOT_RUN |
| artistic_status | PENDING |
| runtime | NOT_PROMOTED |
| source | docs/agents/content-design/C1_WEAPONS_PASSIVES_SYNERGIES.md + C3_MINI_BOSSES_AND_CHEST_FLOW.md |
| visual route | UI_ART + MOCKUP |
| asset_id / family_id / candidate_id | null до intake Visual Lab |
| dependencies | SynergyResolver, weapon/passive level state, BOSS_CHEST outcome, WeaponRegistry |
| run limit | maximum 5 synergy claims; final boss creates no chest |

### Synergy catalogue

| synergy ID | required pair | evolved weapon / new behavior | player decision |
|---|---|---|---|
| synergy_moon_dance | weapon_moon_blade + passive_wind_of_travel | Танец Луны: orbital crescent lanes around hero trajectory; stop keeps close defensive arc | пройти по краю волны и проложить lane или держать позицию для radial coverage |
| synergy_heavenly_seals | weapon_jade_talismans + passive_jade_focus | Небесные печати: resolved marks seed a controlled jade chain without revisiting a node | spread marks по pack или потратить resolve на elite |
| synergy_phoenix_sky | weapon_crimson_flame_fan + passive_ember_heart | Феникс алого неба: burning zones feed a temporary phoenix flight lane | держать огонь на маршруте следующего flight или менять позицию |
| synergy_winter_palace | weapon_frost_pearl + passive_frost_thread | Дворец вечной зимы: controlled targets form a temporary frost lattice and safe route | строить compact control field или уйти до нового telegraph |
| synergy_heavenly_judgment | weapon_thunder_needles + passive_heavenly_seal | Приговор небес: conductive marks call visible overhead judgment and secondary arcs | выбрать marked elite или позволить chain thin wave |
| synergy_guardian_bell | weapon_spirit_bell + passive_iron_bell | Звон защитницы: radial pulse leaves moving ward rim for eligible deflect/knockback | остаться у rim ради защиты или уйти за XP/priority target |
| synergy_nine_reflections | weapon_fox_mirage + passive_mirror_shard | Девять отражений: fox route leaves staggered mirror echoes with deterministic cleanup | проложить corridor по pack или направить echoes на flank |
| synergy_lotus_sanctuary | weapon_lotus_mines + passive_lotus_heart | Святилище лотоса: triggered mines link into control field with bounded recovery interaction | драться вокруг sanctuary или оставить опасную точку |
| synergy_constellation_rain | weapon_star_bow + passive_star_compass | Дождь созвездий: anchors connect and arrows descend along readable segments | aim across arena at ranged threats или собрать local constellation |
| synergy_eclipse_vortex | weapon_black_eclipse_umbrella + passive_spirit_lens | Воронка затмения: bounded vortex pulls eligible enemies and pickups, then collapses into burst | кластеризовать/собирать сейчас или беречь под elite |

### Eligibility and chest states

- Full pair gate: weapon_level = 6, passive_rank = 5, matching synergy ID, weapon not evolved.
- Source gate: only non-final BOSS_CHEST with encounter_kind MAIN_BOSS or MINI_BOSS; ELITE_CHEST is artifact/upgrade/fallback flow.
- Counter gate: claimed_synergy_count < 5. Ten non-final boss chest windows create opportunities, not guaranteed claims.
- If no pair is eligible, or the cap is reached, the chest must resolve to documented fallback without consuming a synergy claim.
- Final boss at 1800 s / 30:00 has no boss chest and cannot claim an evolution.

### Required info states

| state | copy/behavior |
|---|---|
| LOCKED | show required weapon/passive names and which gate is missing |
| ELIGIBLE | show pair, new behavior promise, chest source and “может появиться в сундуке” |
| OFFERED | show current chest opportunity and choose-one/fallback resolution |
| CLAIMED | show evolution applied and the weapon behavior now active |
| ALREADY_EVOLVED | show that the weapon no longer accepts a second evolution |
| CAP_REACHED | show 5-claim cap and fallback path |
| NO_PAIR | show that this chest cannot invent a missing passive/weapon pair |
| FINAL_NO_CHEST | show final boss reward rule without empty synergy offer |

### Visual Lab intake boundary

- route: UI_ART + MOCKUP;
- stage_path: docs/mockups/19-synergy-info/;
- asset_id/family_id/candidate_id: null;
- status: PROPOSAL;
- technical_status: NOT_RUN;
- artistic_status: PENDING;
- manifest/consumer: NOT_PROMOTED; consumer proposal — SynergyResolver + ChestResolver + WeaponRegistry + HUD;
- evidence: отсутствует до фактического mockup/review.
