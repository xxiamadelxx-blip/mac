# Stage 08 — Artifacts
Status: PLANNED.
Артефакты и Кодекс реликвий.
Фактические результаты этапа, preview и evidence добавляются сюда после начала этапа. Пустая папка или этот README сами по себе не означают DONE.
Naming: STAGE##_AREA_TYPE_v##.

## Content-design brief v01 — ten run artifacts

Артефакты — отдельные run modifiers. Они не занимают weapon/passive slots, не являются pre-run loadout и не превращаются в безымянные flat passives.

| Field | Value |
|---|---|
| status | PROPOSAL |
| technical_status | NOT_RUN |
| artistic_status | PENDING |
| runtime | NOT_PROMOTED |
| source | docs/agents/content-design/C2_ARTIFACTS.md |
| visual route | SPRITE + VFX + UI_ART |
| asset_id / family_id / candidate_id | null до intake Visual Lab |
| offer source | ELITE_PACK или FIRST_CLEAR_REWARD |
| offer rule | 3 cards → player selects 1 |
| capacity | отдельный artifact collection; weapon/passive slot capacity не расходуется |
| dependencies | ArtifactEffectSystem, typed semantic effect keys, Architecture source events, Balance coefficients |

### Artifact catalogue

| stable artifact ID | name | effect family | trigger → target | observable combat result | semantic effect key |
|---|---|---|---|---|---|
| artifact_jade_compass | Нефритовый компас | AURA | arena drop collected → nearby enemies and route | маршрут врагов слегка смещается к краю/от safe center; pickup остаётся видимым | aura.drop_route_compass |
| artifact_mirror_shard | Грань зеркала | TRIGGERED_EFFECT | critical weapon hit → source hit zone | echo повторяет форму/направление исходного hit с отдельным timing | trigger.critical_echo |
| artifact_phoenix_feather | Перо феникса | TRIGGERED_EFFECT | elite defeated → enemies crossing path | поэтапная полоса углей проходит от death point к threat cluster и затухает | trigger.elite_ember_path |
| artifact_frost_bead | Ледяная бусина | WEAPON_MODIFIER | slow/freeze applied → controlled target and nearby area | ледяная метка consumed первым eligible hit и создаёт frost ring | modifier.control_bloom |
| artifact_bell_fragment | Осколок колокола | TRIGGERED_EFFECT | post-mitigation guarded hit → nearby threats | resonance ring заполняется и по threshold даёт bounded knockback/interruption | trigger.guard_resonance |
| artifact_lotus_seed | Семя лотоса | TRIGGERED_EFFECT | full-health heal/overheal → next eligible incoming hit | petal charge смягчает следующее допустимое попадание и исчезает | trigger.overheal_ward |
| artifact_moon_crown | Лунная корона | TARGET_MODIFIER | boss phase started → current boss phase | crown mark меняет state после resolve phase telegraph, не на spawn | target.boss_phase_window |
| artifact_black_bead | Чёрная бусина | WEAPON_MODIFIER | eligible elite weapon hit → elite/last eligible weapon source | bead меняет orientation; следующий event показывает PULL или BURST до resolve | modifier.elite_polarity |
| artifact_tideglass | Приливное стекло | AURA | arena drop collected → enemies crossing snapshot path | путь рисуется от drop point к hero в два beat и даёт один displacement/slow response | aura.drop_tide_path |
| artifact_silent_lantern | Безмолвный фонарь | TARGET_MODIFIER | elite/high-threat target selected → one current threat | target mark показывает compact preview следующего attack telegraph, не отменяя его | target.threat_telegraph |

### Offer, stacking and failure rules

- Один offer всегда содержит три distinct artifact cards, затем игрок выбирает одну. Offer не добавляет weapon/passive card.
- Повторный artifact не создаёт скрытый новый слот: показывается upgrade/duplicate state по C2 policy; exact refresh/fallback value — PENDING_BALANCE/PENDING_PRODUCT_DECISION.
- Каждый effect имеет source event, target whitelist, cleanup/expiry, recursion guard и replay identity.
- Artifact effect не меняет wallet напрямую. BOSS_CHEST предназначен для synergy/fallback, не для artifact offer.
- ELITE_PACK и FIRST_CLEAR_REWARD — proposal sources; cadence, rarity, refresh и Codex unlock scope — PENDING_BALANCE/PENDING_ARCHITECTURE.
- Runtime consumer proposal: ArtifactRegistry, ArtifactEffectSystem, ArtifactOffer projection, Codex.

### Visual Lab intake boundary

- route: SPRITE для identity/icon, VFX для trigger response, UI_ART для offer/Codex;
- stage_path: docs/mockups/08-artifacts/ и docs/mockups/17-artifact-ui/;
- asset_id/family_id/candidate_id: null;
- status: PROPOSAL;
- technical_status: NOT_RUN;
- artistic_status: PENDING;
- manifest/consumer: NOT_PROMOTED; consumer proposal — ArtifactRegistry + ArtifactEffectSystem + Artifact UI;
- visual code: deep blue-grey, smoky teal, warm ivory, muted brass, soft jade; crimson/violet только как role/status accent;
- evidence: отсутствует до фактического mockup/review.
