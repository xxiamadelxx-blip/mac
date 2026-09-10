# Stage 17 — Artifact UI
Status: PLANNED.
Интерфейс выбора и постоянного улучшения артефактов.
Фактические результаты этапа, preview и evidence добавляются сюда после начала этапа. Пустая папка или этот README сами по себе не означают DONE.
Naming: STAGE##_AREA_TYPE_v##.

## Content-design brief v01 — artifact offer and Codex states

Это текстовый UI/content brief. Он не создаёт mockup, icon, Codex art или production asset.

| Field | Value |
|---|---|
| status | PROPOSAL |
| technical_status | NOT_RUN |
| artistic_status | PENDING |
| runtime | NOT_PROMOTED |
| source | docs/agents/content-design/C2_ARTIFACTS.md |
| visual route | UI_ART + MOCKUP + SPRITE |
| asset_id / family_id / candidate_id | null до intake Visual Lab |
| offer source | ELITE_PACK или FIRST_CLEAR_REWARD |
| offer rule | 3 distinct artifact cards → select exactly 1 |
| slot rule | artifacts do not consume weapon/passive slots; no fixed artifact slot cap in content |
| dependencies | ArtifactRegistry, ArtifactEffectSystem, OfferResolver, Codex persistence scope |

### Ten artifact entries

| artifact ID | name | card promise | active feedback |
|---|---|---|---|
| artifact_jade_compass | Нефритовый компас | подбор drop оставляет управляемый route bias вокруг точки | jade route pulse, pickup remains visible |
| artifact_mirror_shard | Грань зеркала | eligible critical hit получает отдельный echo | source-shaped ivory/jade echo with clear delay |
| artifact_phoenix_feather | Перо феникса | defeat элиты прокладывает короткий ember path | staged crimson ember line with visible expiry |
| artifact_frost_bead | Ледяная бусина | control event оставляет bloom, который consumes следующий hit | frost mark then one readable ring |
| artifact_bell_fragment | Осколок колокола | guarded hit заполняет bounded resonance response | ring fill → knockback/interruption threshold |
| artifact_lotus_seed | Семя лотоса | full-health heal/overheal создаёт ward на следующий hit | petal charge near hero → consumed state |
| artifact_moon_crown | Лунная корона | boss phase открывает readable phase-window modifier | crown mark attached to phase indicator |
| artifact_black_bead | Чёрная бусина | hit по elite переключает следующий polarity state | bead orientation → PULL/BURST preview |
| artifact_tideglass | Приливное стекло | pickup строит snapshot tide path по threat route | two-beat path from drop to hero, then cleanup |
| artifact_silent_lantern | Безмолвный фонарь | target selection показывает compact preview следующего telegraph | mark one highest-threat target; no hidden cancel |

### Offer and state flow

1. Source event creates one offer with three distinct artifact cards.
2. Player inspects card promise, trigger, target boundary and current state.
3. Player selects one card; selected state is explicit before confirmation/close.
4. Artifact is added to the separate run collection; weapon/passive slots remain unchanged.
5. Duplicate/upgrade or refresh fallback is readable; exact fallback value and refresh policy are PENDING_BALANCE/PENDING_PRODUCT.
6. Codex entry may show discovered/undiscovered state, but FIRST_CLEAR_REWARD persistence scope is PENDING_ARCHITECTURE.

### Required UI states

| state | content behavior |
|---|---|
| OFFER_OPEN | three cards, source label, trigger/target summary, choose-one instruction |
| CARD_FOCUSED | expanded promise, observable result, current stack/duplicate note, synergy interaction warning if any |
| CARD_SELECTED | selected border/state, confirm or resolved choice; other cards visibly dismissed |
| OWNED_DUPLICATE | explicit duplicate/upgrade/fallback message; never silently grants another slot |
| SOURCE_LOCKED | explains ELITE_PACK/FIRST_CLEAR_REWARD requirement |
| CODEX_DISCOVERED | full content text and semantic effect key |
| CODEX_UNDISCOVERED | silhouette/name treatment owned by Visual Lab, no hidden mechanics revealed accidentally |
| OFFER_RESOLVED | outcome and active artifact marker return to HUD |
| ERROR_OR_EMPTY | readable fallback message; never blank cards |

### Semantic key display contract

The card/tooltip may expose the semantic key only as internal/debug evidence; player copy uses the content promise. Canonical keys are:
aura.drop_route_compass, trigger.critical_echo, trigger.elite_ember_path, modifier.control_bloom, trigger.guard_resonance, trigger.overheal_ward, target.boss_phase_window, modifier.elite_polarity, aura.drop_tide_path, target.threat_telegraph.

All coefficient, cooldown, duration, radius, rarity, refresh cost and persistence values are PENDING_BALANCE/PENDING_ARCHITECTURE/PENDING_PRODUCT.

### Visual Lab intake boundary

- route: UI_ART + MOCKUP + SPRITE;
- stage_path: docs/mockups/17-artifact-ui/;
- asset_id/family_id/candidate_id: null;
- status: PROPOSAL;
- technical_status: NOT_RUN;
- artistic_status: PENDING;
- manifest/consumer: NOT_PROMOTED; consumer proposal — ArtifactOffer projection + Artifact HUD marker + Codex;
- evidence: отсутствует до фактического mockup/review.
