# Stage 16 — Upgrade Offers
Status: PLANNED.
Карточки предложений улучшений.
Фактические результаты этапа, preview и evidence добавляются сюда после начала этапа. Пустая папка или этот README сами по себе не означают DONE.
Naming: STAGE##_AREA_TYPE_v##.

## Content-design brief v01 — run upgrades and shop boundary

Это текстовый contract карточек, не готовый UI mockup. Он связывает 10 weapons и 10 global run passives с понятным выбором игрока и отдельно обозначает постоянное дерево магазина.

| Field | Value |
|---|---|
| status | PROPOSAL |
| technical_status | NOT_RUN |
| artistic_status | PENDING |
| runtime | NOT_PROMOTED |
| source | docs/agents/content-design/C1_WEAPONS_PASSIVES_SYNERGIES.md; META_PASSIVE_TREE.md |
| visual route | UI_ART + MOCKUP |
| asset_id / family_id / candidate_id | null до intake Visual Lab |
| run slots | максимум 6 weapon slots и 6 passive slots |
| dependencies | XP/Progression, UpgradeOfferResolver, WeaponRegistry, PassiveRegistry, SynergyInfo, StatsCalculator |

### Run upgrade card contract

Каждый level-up offer показывает три distinct cards и разрешает выбрать одну. Кандидат обязан иметь stable content ID из C1; offer ID не должен подменять content ID.

| card field | required content |
|---|---|
| category | WEAPON или RUN_PASSIVE |
| content_id | один из 10 weapon_* или 10 passive_* IDs |
| title/promise | короткая fantasy и понятный результат для общего билда |
| current state | NEW, owned rank, maxed, locked или synergy-ready |
| next effect intent | qualitative change; exact coefficient/cadence/cooldown/range/duration — PENDING_BALANCE |
| decision cue | что игрок получает сейчас и какой trade-off/маршрут открывается |
| synergy hint | matching weapon/passive pair и gate without promising automatic evolution |
| source | XP/level-up offer; no direct wallet mutation |
| unavailable copy | почему карточка недоступна и какое действие нужно для eligibility |

### Offer states

- NEW: entry ещё не занята в соответствующем run slot; показывается role и first promise.
- UPGRADE: entry уже в билде; показывается текущий rank/level и qualitative next step.
- MAXED: дальнейший rank запрещён authoritative rule; карточка не притворяется доступной.
- LOCKED: источник/слот/gate ещё не выполнен; причина видна.
- SYNERGY_READY: pair gate выполнен, но evolution появляется только через eligible non-final BOSS_CHEST.
- EVOLVED: weapon behavior заменён synergy; новая weapon card не добавляет слот.
- NO_VALID_OFFER: resolver сообщает readable fallback, а не пустой экран.

### Pool and pair visibility

| pool | entries | card copy must emphasize |
|---|---|---|
| weapon | weapon_moon_blade, weapon_jade_talismans, weapon_crimson_flame_fan, weapon_frost_pearl, weapon_thunder_needles, weapon_spirit_bell, weapon_fox_mirage, weapon_lotus_mines, weapon_star_bow, weapon_black_eclipse_umbrella | geometry, target role, weakness/counterplay, matching passive |
| run passive | passive_wind_of_travel, passive_jade_focus, passive_ember_heart, passive_frost_thread, passive_heavenly_seal, passive_iron_bell, passive_mirror_shard, passive_lotus_heart, passive_star_compass, passive_spirit_lens | global axis/trigger, build-wide benefit, matching weapon only as synergy anchor |
| evolution | synergy_moon_dance through synergy_eclipse_vortex | appears in chest/synergy info after weapon level 6 + passive rank 5; no extra slot |

### Persistent shop branch — separate from run cards

The full persistent tree is specified in docs/agents/content-design/META_PASSIVE_TREE.md and must not be mixed with the ten passive_* run entries.

- six branches: meta_vitality, meta_force, meta_agility, meta_focus, meta_magnet, meta_defense;
- 17 stat nodes cover the screenshot/stat-sheet axes: max HP, regen, healing mote, attack power, attack multiplier, magic damage, movement speed, evasion, crit chance, crit power, cooldown, duration, size, pickup radius, mana/XP gain, damage taken, enemy max HP;
- meta_* node is bought between runs for Gold and applies according to its persistent contract; it never occupies a temporary passive slot;
- dependency topology and player-facing copy are content-defined; price, exact effect, rank budget, currency mutation and persistence are PENDING_BALANCE/PENDING_PRODUCT/RUNTIME;
- shop card status is PROPOSAL and must not be presented as a run upgrade or as an artifact.

### Visual Lab intake boundary

- route: UI_ART + MOCKUP;
- stage_path: docs/mockups/16-upgrade-offers/;
- asset_id/family_id/candidate_id: null;
- status: PROPOSAL;
- technical_status: NOT_RUN;
- artistic_status: PENDING;
- manifest/consumer: NOT_PROMOTED; consumer proposal — UpgradeOffer projection + Shop/Meta tree navigation;
- evidence: отсутствует до фактического mockup/review.
