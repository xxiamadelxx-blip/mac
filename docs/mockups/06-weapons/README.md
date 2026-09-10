# Stage 06 — Weapons
Status: PLANNED.
Иконки, боевые эффекты и эволюции оружия.
Фактические результаты этапа, preview и evidence добавляются сюда после начала этапа. Пустая папка или этот README сами по себе не означают DONE.
Naming: STAGE##_AREA_TYPE_v##.

## Content-design brief v01 — ten-weapon roster

Это текстовая спецификация контента для будущего Visual Lab intake. Она не является иконкой, VFX, animation preview или production asset.

| Field | Value |
|---|---|
| status | PROPOSAL |
| technical_status | NOT_RUN |
| artistic_status | PENDING |
| runtime | NOT_PROMOTED |
| source | docs/agents/content-design/C1_WEAPONS_PASSIVES_SYNERGIES.md |
| visual route | SPRITE + ART + VFX |
| asset_id / family_id / candidate_id | null до intake Visual Lab |
| run slot rule | пул 10; в одном забеге максимум 6 weapon slots; эволюция не добавляет slot |
| progression rule | weapon level gate для synergy — 6; точные числа и cadence — PENDING_BALANCE |
| dependencies | C1 passive pair, C1 synergy resolver, StatsCalculator/CombatSystem contracts |

### Weapon catalogue

| stable weapon ID | name | role / geometry | player decision and counterplay | synergy → new weapon behavior |
|---|---|---|---|---|
| weapon_moon_blade | Лунный клинок | mobility / close_area; cone + returning arc | вести орду по касательной и заранее выбрать сторону выхода; дальние и рассеянные цели остаются слабым match-up | synergy_moon_dance: crescent traces идут по орбитальной траектории; движение прокладывает lanes, остановка оставляет ближнюю дугу |
| weapon_jade_talismans | Нефритовые талисманы | control / ranged_sustain; homing projectile + mark | распределять метки или удерживать high-threat target; teleport/decoy снижает ценность lock | synergy_heavenly_seals: активированные метки связываются в controlled chain без повторного узла |
| weapon_crimson_flame_fan | Веер багрового пламени | area / status_burn; alternating cone + zone | закрыть путь перед собой или отрезать фланг; быстрые и разреженные враги обходят очаг | synergy_phoenix_sky: burning zones кормят проход феникса, который зажигает читаемую lane и выходит |
| weapon_frost_pearl | Ледяная жемчужина | control / mid_area; projectile + impact burst | замедлить опасный коридор и решить, добивать controlled cluster или менять позицию | synergy_winter_palace: controlled targets соединяются frost lattice с временным safe route |
| weapon_thunder_needles | Иглы грома | burst / chain; chain | держать врагов в читаемой плотности и выбирать priority node; рассеянная волна обрывает цепь | synergy_heavenly_judgment: conductive marks вызывают видимый overhead judgment с вторичными дугами |
| weapon_spirit_bell | Колокол духов | defense / area_control; radial pulse | использовать pulse как окно выхода и снятие projectile pressure, а не как постоянную неуязвимость | synergy_guardian_bell: pulse оставляет moving ward rim, который deflect-ит допустимые telegraphed projectiles |
| weapon_fox_mirage | Лисий мираж | mobility / summon_line; dash-linked summon | вести поток так, чтобы fox-route пересёк следующий lane; неверная линия уводит урон от угрозы | synergy_nine_reflections: маршрут оставляет staggered mirror echoes с отдельным cleanup |
| weapon_lotus_mines | Лотосовые мины | area / delayed_control; delayed zone | заранее занять projected enemy path, не оставив бутоны за потоком; хаотичный rush наказывает задержку | synergy_lotus_sanctuary: сработавшие мины связываются во временное святилище с control/recovery boundary |
| weapon_star_bow | Звёздный лук | ranged / pierce / priority; line projectile + anchor | выбирать дальнюю угрозу или собрать локальную constellation; swarm может перегрузить target priority | synergy_constellation_rain: anchors соединяются, стрелы падают по читаемым сегментам и схлопывают старый anchor |
| weapon_black_eclipse_umbrella | Чёрный зонт затмения | defense / utility / pull; orbit + cone/vortex | чередовать guard orbit и open sweep, выбирая между защитой и clustering; bosses/immune tags не тянутся молча | synergy_eclipse_vortex: bounded vortex стягивает eligible enemies и nearby pickups, затем даёт contained burst |

Каждое оружие получает отдельный cast → travel → hit → persist → expire lifecycle, читаемый origin и cleanup. Цвет не является единственным differentiator: форма, геометрия и timing обязательны.

### Global content rules

- Все 10 weapon entries — run content с stable IDs; exact damage, cadence, cooldown, range, area, duration, target cap, pierce/bounce limits и evolution power budget — PENDING_BALANCE.
- Synergy/evolution заменяет behavior конкретного оружия после pair gate; она не добавляет слот и не является отдельным одиннадцатым базовым оружием.
- Не использовать passive как скрытый per-weapon modifier: соответствующая passive работает на общий eligible build, а bound weapon нужен только для eligibility пары.
- Boss/mini-boss BOSS_CHEST может предложить eligible synergy; общий cap забега — 5 claims, final boss chest отсутствует.
- Runtime consumer proposal: WeaponRegistry, TargetingSystem, CombatSystem, ZoneStore, SynergyResolver.
- Visual Lab не получает выдуманные asset IDs: candidate_id остаётся null до intake.

### Visual Lab intake boundary

- route: SPRITE + ART + VFX;
- stage_path: docs/mockups/06-weapons/;
- asset_id/family_id/candidate_id: null;
- status: PROPOSAL;
- technical_status: NOT_RUN;
- artistic_status: PENDING;
- manifest/consumer: NOT_PROMOTED; consumer proposal — WeaponRegistry + CombatSystem + SynergyInfo;
- evidence: отсутствует до фактического mockup/review.
