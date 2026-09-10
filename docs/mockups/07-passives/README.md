# Stage 07 — Passives
Status: PLANNED.
Иконки и карточки пассивных навыков.
Фактические результаты этапа, preview и evidence добавляются сюда после начала этапа. Пустая папка или этот README сами по себе не означают DONE.
Naming: STAGE##_AREA_TYPE_v##.

## Content-design brief v01 — ten global run passives

Пассивка в этом каталоге — общий run modifier. Связь с оружием ниже является только eligibility anchor для synergy; passive не превращается в апгрейд этого оружия.

| Field | Value |
|---|---|
| status | PROPOSAL |
| technical_status | NOT_RUN |
| artistic_status | PENDING |
| runtime | NOT_PROMOTED |
| source | docs/agents/content-design/C1_WEAPONS_PASSIVES_SYNERGIES.md |
| visual route | SPRITE + UI_ART |
| asset_id / family_id / candidate_id | null до intake Visual Lab |
| run slot rule | пул 10; в одном забеге максимум 6 passive slots |
| synergy gate | weapon level 6 + passive rank 5 + matching synergy ID + weapon not evolved |
| dependencies | C1 synergy resolver, StatsCalculator, Health/Targeting/Progression contracts |

### Passive catalogue

| stable passive ID | name | global axis and benefit | bound weapon for eligibility only | synergy |
|---|---|---|---|---|
| passive_wind_of_travel | Ветер странствий | mobility/momentum: улучшает управление движением и даёт общий MOMENTUM context после непрерывного движения | weapon_moon_blade | synergy_moon_dance |
| passive_jade_focus | Нефритовый фокус | targeting/consistency: auto-targeted sources дольше удерживают valid priority target; manual aim не перехватывается | weapon_jade_talismans | synergy_heavenly_seals |
| passive_ember_heart | Сердце углей | overkill/chain tempo: подтверждённое убийство создаёт bounded ember charge, следующий eligible hit выпускает afterspark | weapon_crimson_flame_fan | synergy_phoenix_sky |
| passive_frost_thread | Морозная нить | control/cooldown-tempo: после slow/freeze следующий hit по controlled target даёт общий ограниченный tempo response | weapon_frost_pearl | synergy_winter_palace |
| passive_heavenly_seal | Небесная печать | damage sequencing/vulnerability: distinct hits по одной цели открывают короткое universal vulnerability window | weapon_thunder_needles | synergy_heavenly_judgment |
| passive_iron_bell | Железный колокол | defense/poise: снижает допустимый incoming damage и даёт bounded grace против повторного stagger/chain-hit | weapon_spirit_bell | synergy_guardian_bell |
| passive_mirror_shard | Осколок зеркала | bounded replication: периодически повторяет часть eligible hit любого оружия/ability с отдельным event ID | weapon_fox_mirage | synergy_nine_reflections |
| passive_lotus_heart | Сердце лотоса | health/healing conversion: повышает survival axis и превращает approved healing в один Petal state для следующего hit | weapon_lotus_mines | synergy_lotus_sanctuary |
| passive_star_compass | Звёздный компас | critical rhythm: серия обычных hit открывает общий precision window для eligible sources | weapon_star_bow | synergy_constellation_rain |
| passive_spirit_lens | Духовная линза | pickup/information utility: расширяет сбор eligible drops и XP/mana и коротко подсвечивает resource path | weapon_black_eclipse_umbrella | synergy_eclipse_vortex |

### Passive invariants

- Каждая passive усиливает общую ось билда и не читает/не мутирует состояние bound weapon.
- Повторный offer повышает rank этой passive; hidden per-weapon modifier и nested invulnerability запрещены.
- Все значения modifier, sequence length, charge/window duration, target whitelist, mitigation, rank curve, crit response и pickup radius — PENDING_BALANCE.
- UI copy должна объяснять общий результат: что меняется для build, когда срабатывает, что сбрасывает/потребляет состояние.
- Passive icon и card показывают axis, trigger state и synergy hint, но не подменяют weapon icon.
- Runtime consumer proposal: StatsCalculator, MovementSystem, TargetingSystem, CombatSystem, HealthSystem, Magnet/Progression, SynergyResolver.
- Boss/mini-boss chest может предложить synergy только при полной паре; обычный passive upgrade не расходует synergy cap.

### Visual Lab intake boundary

- route: SPRITE + UI_ART;
- stage_path: docs/mockups/07-passives/;
- asset_id/family_id/candidate_id: null;
- status: PROPOSAL;
- technical_status: NOT_RUN;
- artistic_status: PENDING;
- manifest/consumer: NOT_PROMOTED; consumer proposal — PassiveRegistry + UpgradeOffer projection + SynergyInfo;
- evidence: отсутствует до фактического mockup/review.
