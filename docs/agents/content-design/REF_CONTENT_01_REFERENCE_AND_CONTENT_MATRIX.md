# REF-CONTENT-01 — MAC reference и content matrix

Status: PARTIAL / CONTENT_SPECIFIED_REFERENCE_ONLY  
Task ID: REF-CONTENT-01  
Parent HEAD: 9687d10a8e7cea4dd214a67fe63f11cdecf70e8f  
Write scope: docs/agents/content-design/ only

Этот срез не вводит новые content IDs. Он собирает в одну проверяемую матрицу уже существующие MAC IDs из C1–C3 и Stage 04, добавляет reference provenance и явно фиксирует unresolved reconciliation. Поэтому для этого файла не существует нового ID, который можно было бы ошибочно считать approved. Existing records остаются CONTENT_SPECIFIED или PROPOSED согласно их исходным документам.

Runtime approval: NOT_REQUESTED  
Balance lock: NOT_GRANTED  
Artistic approval: PENDING  
Runtime implementation: NOT_CHANGED  
Binary/mockup changes: NONE

## 1. Правило оригинальности

Все MAC названия, роли, механики и короткие описания в следующих таблицах являются самостоятельным контентным дизайном Moonveil: Eclipse. Указанные ниже внешние репозитории использовались только как structural reference для разделения ответственности:

- XP pickup → threshold/level-up → separate offer;
- time-keyed composition/density;
- отдельный boss или special encounter;
- typed weapon/projectile/zone lifecycle;
- отдельный reward/chest path.

Из внешних проектов не перенесены числа, IDs, названия, персонажи, описания, изображения, loot odds или asset paths.

## 2. Evidence по разрешённым reference repositories

| Репозиторий и прочитанные файлы | Наблюдаемый общий паттерн | MAC application | Что не импортировано |
|---|---|---|---|
| [Vampire clone: ExperienceManager](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/main/scenes/managers/experience_manager.gd), [UpgradeManager](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/main/scenes/managers/upgrade_manager.gd), [EnemyManager](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/main/scenes/managers/enemy_manager.gd), [ExperienceVial](https://github.com/murparreira/vampire-survivors-clone-godot-4/blob/main/scenes/game_objects/experience_vial/experience_vial.gd) | XP collection, level transition, weighted upgrade pool, enemy composition and boss path are separate responsibilities; pickup has its own collect/cleanup lifecycle | ProgressionSystem, UpgradeOfferSystem, WaveDirector, BossDirector и XPDrop остаются раздельными MAC consumers | Ни один foreign value, ID, enemy, boss или asset |
| [20 Minutes: PlayerController](https://github.com/ParsaSabzei/20-Minutes-till-dawn/blob/main/core/src/main/java/ap/project/controller/PlayerController.java), [AbilityController](https://github.com/ParsaSabzei/20-Minutes-till-dawn/blob/main/core/src/main/java/ap/project/controller/AbilityController.java), [MonsterController](https://github.com/ParsaSabzei/20-Minutes-till-dawn/blob/main/core/src/main/java/ap/project/controller/MonsterController.java), [GameView](https://github.com/ParsaSabzei/20-Minutes-till-dawn/blob/main/core/src/main/java/ap/project/view/GameView.java) | XP pickup can trigger a level state; ability choice is a separate state with three visible choices; normal spawning and a special encounter are distinct paths | MAC keeps three-card upgrade/artifact presentation, separate encounter records and explicit checkpoint ownership | Не копируются level curve, timers, monster types, UI text или names |
| [Blaze Magic: enemies.py](https://github.com/Blaze-master/Magic_Survival_Clone/blob/master/enemies.py), [magic.py](https://github.com/Blaze-master/Magic_Survival_Clone/blob/master/magic.py), [objects.py](https://github.com/Blaze-master/Magic_Survival_Clone/blob/master/objects.py), [artifacts.py](https://github.com/Blaze-master/Magic_Survival_Clone/blob/master/artifacts.py) | Enemy data and time-keyed spawn composition are external to object behavior; weapon records describe lifecycle properties; projectiles, lines and zones have distinct object lifecycles; artifact module is a separate boundary | MAC content stays data-driven, with weapon/zone/telegraph/reward consumers named in each entry | Не копируются tables, coefficients, timing, sprites или artifact emptiness as a MAC rule |
| [syncXL Magic: gamedata.py](https://github.com/syncXL/Magic_Survival_Clone/blob/master/gamedata.py), [magic.py](https://github.com/syncXL/Magic_Survival_Clone/blob/master/magic.py), [objects.py](https://github.com/syncXL/Magic_Survival_Clone/blob/master/objects.py), [artifacts.py](https://github.com/syncXL/Magic_Survival_Clone/blob/master/artifacts.py) | A smaller fork keeps global run data, magic definitions and runtime object shapes separate; field items/chests and attack objects remain distinct | MAC preserves one registry boundary and separate XP, chest and artifact channels | Не копируются fork differences, field sizes, counts, values или implementation defects |

Источник MAC-контрактов: C1_WEAPONS_PASSIVES_SYNERGIES.md, C2_ARTIFACTS.md, C3_MINI_BOSSES_AND_CHEST_FLOW.md, Stage 04 enemy manifests, GAME_MANIFEST.md и FIRST_RUN_DATA_CONTRACT.json. Reference repositories имеют статус REFERENCE_ONLY.

## 3. Weapon ability → passive → synergy

В этой таблице ability означает автоматически применяемое run weapon. Hero active abilities и их runtime IDs в этот срез не добавляются: они остаются отдельным protected/runtime contract. Точные damage, cadence, cooldown, range, quantity, duration, chance и power budget принадлежат Balance Agent и здесь не назначаются.

| Weapon ID / ability | Role и player decision | Passive ID / axis | Synergy ID / transformed behavior | Tags | Dependencies | Status |
|---|---|---|---|---|---|---|
| weapon_moon_blade / Лунный клинок | close-area mobility; вести орду по касательной или держать защитную дугу | passive_wind_of_travel / movement и lane choice | synergy_moon_dance / орбитальные дорожки меняют ценность движения | close, arc, movement, lane | BuildInventory; CombatSystem; SynergyEvaluator; Visual Lab weapon family | EXISTING_CONTENT_SPECIFIED |
| weapon_jade_talismans / Нефритовые талисманы | ranged control; распределять метки по группе или удерживать priority target | passive_jade_focus / mark consistency | synergy_heavenly_seals / цепочка печатей с visited-set | ranged, mark, homing, chain | MarkStore; CombatSystem; UpgradeOfferSystem; SynergyResolver | EXISTING_CONTENT_SPECIFIED |
| weapon_crimson_flame_fan / Веер багрового пламени | area/status; закрыть опасный коридор очагом или оставить путь для движения | passive_ember_heart / burn/status axis | synergy_phoenix_sky / phoenix lane проходит через разрешённые ember zones | cone, burn, zone, lane | StatusSystem; ZoneStore; TelegraphResolver; SynergyResolver | EXISTING_CONTENT_SPECIFIED |
| weapon_frost_pearl / Ледяная жемчужина | control; удержать кластер в выгодной точке или уйти до нового telegraph | passive_frost_thread / control link | synergy_winter_palace / временная морозная lattice с безопасным маршрутом | slow, burst, lattice, control | StatusSystem; ZoneStore; CombatSystem; Boss immunity policy | EXISTING_CONTENT_SPECIFIED |
| weapon_thunder_needles / Иглы грома | burst/chain; собрать допустимую плотность или не терять чтение угроз | passive_heavenly_seal / conductive/precision axis | synergy_heavenly_judgment / видимый overhead strike по marked nodes | chain, conductive, burst, priority | CombatSystem; MarkStore; TelegraphResolver; SynergyResolver | EXISTING_CONTENT_SPECIFIED |
| weapon_spirit_bell / Колокол духов | defense/utility; остаться возле ward или выйти за XP/priority target | passive_iron_bell / guard/resonance axis | synergy_guardian_bell / движущийся ward rim для допустимых снарядов | ward, guard, pulse, displacement | HealthSystem; ProjectileResolver; CombatSystem; cleanup registry | EXISTING_CONTENT_SPECIFIED |
| weapon_fox_mirage / Лисий мираж | skirmish/route; прокладывать echoes по коридору или флангу | passive_mirror_shard / delayed echo axis | synergy_nine_reflections / staggered mirror echoes с source attribution | mirror, echo, corridor, delayed | CombatSystem; EchoGuard; VFX cleanup; SynergyResolver | EXISTING_CONTENT_SPECIFIED |
| weapon_lotus_mines / Лотосовые мины | area denial; заранее создать sanctuary или отказаться от опасной позиции | passive_lotus_heart / health/healing conversion | synergy_lotus_sanctuary / временное поле контроля с разрешённым recovery hook | mine, zone, sanctuary, healing | ZoneStore; HealthSystem; ArenaDrop/Healing contract; SynergyResolver | EXISTING_CONTENT_SPECIFIED |
| weapon_star_bow / Звёздный лук | ranged priority; связать дальние точки или локализовать плотную группу | passive_star_compass / critical rhythm | synergy_constellation_rain / anchors соединяются и дают читаемый rain path | ranged, anchor, line, precision | TargetingSystem; TelegraphResolver; CombatSystem; SynergyResolver | EXISTING_CONTENT_SPECIFIED |
| weapon_black_eclipse_umbrella / Чёрный зонт затмения | utility/control; кластеризовать допустимых врагов и drops или сохранить pull для elite | passive_spirit_lens / pickup/information utility | synergy_eclipse_vortex / ограниченная воронка и contained burst | pull, pickup, vortex, utility | Magnet/Progression; TargetFilter; CombatSystem; SynergyResolver | EXISTING_CONTENT_SPECIFIED |

Общий gate для десяти пар: weapon max level 6, passive max rank 5, matching pair, weapon не evolved, non-final BOSS_CHEST, encounter kind MAIN_BOSS или MINI_BOSS и общий лимит claims не выше пяти. Эти условия — существующий MAC content/architecture contract; дополнительные числовые правила остаются PENDING_BALANCE или PENDING_PRODUCT_DECISION.

## 4. Run passives и их dependency rule

Все десять run-passives являются общими модификаторами билда, занимают passive slot и не усиливают скрыто только парное оружие. Weapon ID используется как synergy anchor, а не как источник эффекта passive.

| Passive ID | Axis и readable promise | Main dependencies | Balance-owned fields | Status |
|---|---|---|---|---|
| passive_wind_of_travel | движение меняет качество lane и следующий выбор позиции | StatsCalculator; MovementSystem | derived move/trajectory values, caps, rank curve | EXISTING_CONTENT_SPECIFIED |
| passive_jade_focus | стабильнее удерживать и разрешать marks | StatsCalculator; MarkStore | mark response, eligible tags, rank curve | EXISTING_CONTENT_SPECIFIED |
| passive_ember_heart | burn/status остаётся осмысленной зоной решения | StatsCalculator; StatusSystem; ZoneStore | status response, zone interaction, rank curve | EXISTING_CONTENT_SPECIFIED |
| passive_frost_thread | control effects связывают поток, но не выключают telegraphs | StatsCalculator; StatusSystem; TelegraphResolver | slow/link response, immunity, rank curve | EXISTING_CONTENT_SPECIFIED |
| passive_heavenly_seal | conductive hit открывает ограниченное precision решение | StatsCalculator; CombatSystem | charge/crit interaction, source tags, rank curve | EXISTING_CONTENT_SPECIFIED |
| passive_iron_bell | guard превращает один рискованный hit в читаемый resonance choice | StatsCalculator; HealthSystem | guard/resonance rule, cap, rank curve | EXISTING_CONTENT_SPECIFIED |
| passive_mirror_shard | eligible hit может дать задержанный echo без рекурсии | CombatSystem; EchoGuard | trigger rule, delay, echo cap, rank curve | EXISTING_CONTENT_SPECIFIED |
| passive_lotus_heart | здоровье и разрешённое лечение создают bounded survival choice | HealthSystem; HealingSource | max HP/heal/ward fields, rank curve | EXISTING_CONTENT_SPECIFIED |
| passive_star_compass | серия обычных hits открывает один общий precision moment | CombatSystem; CritResolver | sequence/window/reset, rank curve | EXISTING_CONTENT_SPECIFIED |
| passive_spirit_lens | безопаснее читать и собирать eligible resources, не сквозь стены | Magnet/Progression; PickupFilter | radius/path pulse/wall rule, rank curve | EXISTING_CONTENT_SPECIFIED |

## 5. Artifact matrix

Артефакты не занимают weapon/passive slots, не образуют pre-run loadout и выдаются через отдельный source с ровно тремя cards и одним выбором. Первые восемь IDs уже присутствуют в architecture registry, но их typed effect definitions ещё не синхронизированы. Два последних ID — существующие content proposals и остаются PROPOSED.

| Artifact ID | Effect family / trigger | Original player decision | Dependencies | Numeric/semantic boundary | Status |
|---|---|---|---|---|---|
| artifact_jade_compass | AURA / arena drop collected | забрать drop через route field или обойти риск | ArtifactEffectSystem; PickupFilter; ArenaDrop registry | aura size/lifetime/displacement/drop whitelist: PENDING_BALANCE | EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING |
| artifact_mirror_shard | TRIGGERED_EFFECT / critical weapon hit | принять delayed echo ради критического окна | ArtifactEffectSystem; CombatSystem; source_event dedupe | delay/coefficient/tags/internal cooldown: PENDING_BALANCE | EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING |
| artifact_phoenix_feather | TRIGGERED_EFFECT / elite defeated | провести угрозу через короткий ember path | ArtifactEffectSystem; Elite event; ZoneStore | path/damage/cooldown/pack target: PENDING_BALANCE | EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING |
| artifact_frost_bead | WEAPON_MODIFIER / slow or freeze applied | сохранить marked target до следующего bloom | ArtifactEffectSystem; StatusSystem; TargetFilter | mark/bloom/boss resistance: PENDING_BALANCE | EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING |
| artifact_bell_fragment | TRIGGERED_EFFECT / post-mitigation guarded hit | допустить ограниченный риск ради resonance pulse | HealthSystem; CombatSystem; idempotent damage fact | threshold/radius/knockback/boss rule: PENDING_BALANCE | EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING |
| artifact_lotus_seed | TRIGGERED_EFFECT / full-health heal or overheal | не тратить лечение сразу и сохранить ward | HealthSystem; HealingSource; artifact trigger dedupe | ward/source whitelist/hazard whitelist: PENDING_BALANCE / PENDING_PRODUCT_DECISION | EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING |
| artifact_moon_crown | TARGET_MODIFIER / boss phase started | пережить telegraph и попасть в короткое phase window | BossDirector; TelegraphResolver; ArtifactEffectSystem | phase whitelist/window/missed rule: PENDING_BALANCE | EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING |
| artifact_black_bead | WEAPON_MODIFIER / eligible elite weapon hit | менять pull/burst mode под угрозу | CombatSystem; TargetFilter; ArtifactEffectSystem | mode coefficient/radius/elite immunity: PENDING_BALANCE | EXISTING_CONTENT_SPECIFIED / REGISTRY_SYNC_PENDING |
| artifact_tideglass | AURA / arena drop collected | провести путь от drop к герою и изменить маршрут угроз | ArenaDrop registry; ZoneStore; replay state | path/width/displacement/wall interaction: PENDING_BALANCE | PROPOSED / REGISTRY_SYNC_PENDING |
| artifact_silent_lantern | TARGET_MODIFIER / elite or high-threat target selected | прочитать следующую угрозу, но всё равно выполнить dodge | TargetSelector; TelegraphResolver; ArtifactEffectSystem | threat selector/lead time/eligibility: PENDING_BALANCE / PENDING_ARCHITECTURE | PROPOSED / REGISTRY_SYNC_PENDING |

## 6. Enemy matrix: ten existing MAC enemy records

Current Stage 04 calls this a ten-family roster. Eight records are ordinary role families and two are explicitly elite-family records. This distinction is preserved instead of silently reclassifying elite enemies as ordinary.

Exact spawn weights, absolute HP/ATK/speed, elite cadence, variant overlay and active-cap allocation belong to Balance/Content Registry. The time bands below are existing MAC first-appearance points, not copied reference values.

| Enemy ID | Role / signature | Tags | First appearance / spawn point | Counter-decision | Dependencies | Status |
|---|---|---|---|---|---|---|
| ink_beetle | direct rusher; low shell and short committed contact line | rusher, contact, low_durability | 0–2 min warm-up band; continues in later bands | move tangentially or clear the nearest lane | WaveDirector; CombatSystem; XPDrop; enemy visual manifest | EXISTING_CONTENT_SPECIFIED |
| lantern_moth | ranged kiter; warm-up lantern projectile | ranged, projectile, spacing | 2–5 min first pressure band | close distance or preserve cover/route | TargetingSystem; ProjectileResolver; TelegraphResolver | EXISTING_CONTENT_SPECIFIED |
| bone_carp | line dasher; locked path before dash | line_dash, telegraph, recovery | 2–5 min first pressure band | leave the locked line, punish recovery | TelegraphResolver; MovementSystem; CombatSystem | EXISTING_CONTENT_SPECIFIED |
| paper_ghost | teleporter; visible flicker before reappearance | teleporter, reposition, contact | 5–10 min threat expansion band | read reappear window instead of chasing the vanish | EncounterState; TelegraphResolver; TargetingSystem | EXISTING_CONTENT_SPECIFIED |
| jade_toad | leap area-denial; landing circle and poison zone | leap, zone, area_denial | 5–10 min threat expansion band | leave landing marker, return after recovery | ZoneStore; TelegraphResolver; StatusSystem | EXISTING_CONTENT_SPECIFIED |
| mirror_fox | decoy skirmisher; weaker copy and flank | decoy, flank, mirror, target_confusion | 5–10 min threat expansion band | identify source and avoid being pulled into the wrong lane | TargetFilter; DecoyResolver; CombatSystem | EXISTING_CONTENT_SPECIFIED |
| bell_crab | frontal guard tank; rear knot is readable weakness | guard, tank, directional, contact | 10–15 min elite band | circle behind instead of trading into guard | DirectionalHitResolver; CombatSystem; TelegraphResolver | EXISTING_CONTENT_SPECIFIED |
| thread_doll | slow-beam controller; distance breaks beam | controller, beam, slow, spacing | 10–15 min elite band | break line/distance before slow locks | ProjectileResolver; StatusSystem; TelegraphResolver | EXISTING_CONTENT_SPECIFIED |
| stone_oni | elite ground-slam; long wind-up and recovery | elite, slam, zone, heavy | 10–15 min elite entry | leave large telegraph, attack recovery | EliteDirector; TelegraphResolver; ZoneStore; XPDrop | EXISTING_CONTENT_SPECIFIED / ELITE_FAMILY |
| eclipse_serpent | elite trail dasher; curved path and visible arc edge | elite, dash, trail, arc | 15–20 min eclipse band | cut across after committed turn, avoid trail | EliteDirector; TelegraphResolver; ZoneStore; XPDrop | EXISTING_CONTENT_SPECIFIED / ELITE_FAMILY |

Spawn boundary for 20:00–30:00: no new enemy ID is introduced in this slice. Existing records may continue through the proposed late wave bands only after Balance binds composition, cap and variant policy. Elite records must not spawn at instant contact range.

## 7. Requested four-boss core matrix

These are the four protected first-run boss identities requested for the content matrix. The active 30-minute contract separately contains two proposed extension slots and five mini-boss slots; that reconciliation is intentionally not hidden.

| Boss ID | Checkpoint / spawn point | Role, phase and telegraph | Tags | Reward/dependency boundary | Status |
|---|---|---|---|---|---|
| boss_hua_lin | 05:00 / 300s first main checkpoint | area-denial route test; fire circles, lantern fan and safe-zone teleport; each danger has a pre-attack signal | main_boss, fire, lantern, teleport, zone | BossDirector → TelegraphResolver → defeat fact → non-final BOSS_CHEST/SynergyResolver; RewardLedger settles separately | EXISTING_PROTECTED_CONTENT |
| boss_miyeon | 10:00 / 600s second main checkpoint | deception/target test; true body and two copies, temporary projectile redirection and mirror walls; copy reveal is the read window | main_boss, mirror, decoy, wall, redirect | BossDirector → DecoyResolver → ChestResolver; copy death cannot duplicate XP/chest/reward | EXISTING_PROTECTED_CONTENT |
| boss_seika | 15:00 / 900s third main checkpoint | armored melee/space test; sword arcs, jade columns and marked ground slam; armor break opens phase two | main_boss, guard, melee, column, phase_break | BossDirector → DirectionalHitResolver → phase state → non-final BOSS_CHEST; reward remains RewardLedger-owned | EXISTING_PROTECTED_CONTENT |
| boss_black_moon_empress | 30:00 / 1800s final checkpoint in active extension target; legacy root text says 20:00 | final build test; rotating blades, diagonal beams, elite summons, then darkness and three seal-break vulnerability | final_boss, darkness, seal, elite_summon, final_settlement | BossDirector → final defeat → final settlement/victory; final boss chest is forbidden and artifact offer remains separate | EXISTING_ID_RETIMED_BY_EXTENSION / RECONCILIATION_PENDING |

All boss numbers not explicitly inherited from the live contract—HP, phase thresholds, warning lead, damage, summon count, recovery, resistance and target TTK—are PENDING_BALANCE. This matrix does not assign them.

## 8. Dependency map

| Content surface | Required consumer/boundary | Must not own |
|---|---|---|
| Weapon and passive records | Content Registry, BuildInventory, UpgradeOfferSystem, StatsCalculator | exact balance numbers, wallet, UI authority |
| Synergy/evolution records | SynergyEvaluator, BossChestSystem, EvolutionState, VFX cleanup | artifact offer, final chest, hidden passive rewrite |
| Artifact records | ArtifactOfferSystem, ArtifactEffectSystem, typed trigger/target/stack policy | weapon/passive slots, boss chest, persistent wallet mutation |
| Enemy records | WaveDirector, EnemyRegistry, TelegraphResolver, CombatSystem, XPDrop | checkpoint rewards, permanent roster mutation |
| Four boss records | BossDirector, SimulationClock encounter clock, TelegraphResolver, ChestResolver/RewardLedger | direct wallet mutation, artistic approval |
| Visual briefs | Visual Lab family/template/manifest route | PNG/SVG production, golden approval, runtime promotion |
| Balance handoff | B1/BALANCE_MODEL and profile simulation | silent test numbers or second source of truth |

## 9. Disputed points for Balance-Economy

| Decision / risk | Current evidence | Required balance treatment | Status |
|---|---|---|---|
| Enemy absolute HP/ATK/speed by ID | B1 gives bands and durability multipliers but not a complete per-ID absolute table | bind in one balance source; no values in this content file | PENDING_BALANCE |
| Spawn weights and 30-minute composition | Stage 04 gives first appearance only; B1 has bands; late extension is model proposal | define weights, spawn budget share, active-cap share and late-band continuation in BALANCE_MODEL | PENDING_BALANCE |
| Eight ordinary plus two elite-family interpretation | Stage 04 labels stone_oni/eclipsed_serpent elite; task says ten ordinary enemies | Product/Balance confirms whether count means ten total families or ten non-elite plus bounded variants | PENDING_PRODUCT_DECISION |
| Four requested bosses versus active 30-minute roster | Root content has four protected identities; architecture target is six main plus five mini; two main extensions and three missing mini records remain | keep four rows protected; reconcile extension/mini registry without reusing or renaming silently | PENDING_ARCHITECTURE / PENDING_PRODUCT_DECISION |
| boss clock policy | Sync/Runtime target freezes MAIN_BOSS visible clocks; architecture documents contain conflict | Architecture/Runtime owns final clock contract; Balance consumes it | PENDING_ARCHITECTURE |
| Artifact count and typed effects | Content has ten IDs; architecture registry has eight and zero typed effect definitions | add two only through registry sync; decide effect keys, stacking, refresh and duplicate policy | REGISTRY_SYNC_PENDING |
| Chest and synergy sources | Content cap is five claims; final boss no chest; architecture has fifteen windows with reserved slots | Balance binds cadence/reward quantities; boss chest and artifact offer stay separate | PENDING_BALANCE / PENDING_ARCHITECTURE |
| Boss phase and TTK targets | Root B1 has legacy 20-minute targets; 30-minute extensions are model proposals | import no foreign values; derive all late values with source and formula in BALANCE_MODEL | PENDING_BALANCE |
| Visual identity | Stage 04 and Stage 05 are candidate/proposal material | Visual Lab performs hero-master, provenance, review and approval; content only supplies briefs | ARTISTIC_PENDING |

## 10. Acceptance and evidence boundary

- Matrix covers 10 weapon/passive/synergy links, 10 passive axes, 10 artifact records, 10 enemy records and 4 protected core bosses.
- Every referenced ID already exists in current MAC content/architecture documents; no new ID is introduced here.
- Existing proposal IDs artifact_tideglass, artifact_silent_lantern, boss_tideglass_regent, boss_omen_paper_archivist and the three missing mini records remain PROPOSED/PENDING and are not promoted by this task.
- No PNG/SVG or mockup file was created or modified. The permitted content-design directory contained no empty text/JSON mockup placeholder that required filling; existing stage assets remain protected.
- No runtime, architecture, balance, root document or content ID was changed.
- Reference evidence is structural only; all MAC-specific semantics remain sourced to the existing content, architecture and balance documents.
- A valid content matrix is not runtime proof, balance lock, artistic approval or Android evidence.

## 11. Open blockers

1. Architecture must reconcile the requested four-boss core with the active 30-minute six-main/five-mini target and resolve extension slot identities without silent remapping.
2. Balance must bind the absent per-ID numeric fields, late-wave composition, elite policy, boss phase targets and reward quantities in the single balance source.
3. Architecture/Runtime must reconcile artifact registry count/effect definitions and enemy semantic ID shape before implementation.
4. Visual Lab approval is still required for any weapon, enemy, boss, artifact or VFX production asset.

## 12. Next action

Architecture/Product owner accepts or rejects one explicit reconciliation for the 30-minute encounter envelope—four protected core bosses versus six main plus five mini records—and publishes the resulting ID/checkpoint mapping for Balance and Runtime consumption.
