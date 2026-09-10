
# Content Handoff — C3: будущие противники и боссы

## 1. Идентичность

- Repository: xxiamadelxx-blip/mac
- Branch: main
- HEAD: 3ec40016722244164a90c06024672fcb313f4e92 (baseline, проверенный перед записью C3)
- Slice: C3
- Status: CONTENT_SPECIFIED
- Catalog version: 1
- Date: 2026-09-10

C3 — content design package. Он не является runtime implementation, balance lock, visual approval или production delivery.

## 2. Scope

### Созданные entries

| content_id | type | stage | status | source | next owner |
|---|---|---|---|---|---|
| enemy_lotus_usher | future enemy | future stage proposal | PROPOSAL / REGISTRY_SYNC_PENDING | C3_MINI_BOSSES_AND_CHEST_FLOW.md | Architecture, Balance, Visual Lab |
| enemy_moonroot_burrower | future enemy | future stage proposal | PROPOSAL / REGISTRY_SYNC_PENDING | C3_MINI_BOSSES_AND_CHEST_FLOW.md | Architecture, Balance, Visual Lab |
| enemy_silver_reed_seer | future enemy | future stage proposal | PROPOSAL / REGISTRY_SYNC_PENDING | C3_MINI_BOSSES_AND_CHEST_FLOW.md | Architecture, Balance, Visual Lab |
| enemy_moontrail_stalker | future enemy | future stage proposal | PROPOSAL / REGISTRY_SYNC_PENDING | C3_MINI_BOSSES_AND_CHEST_FLOW.md | Architecture, Balance, Visual Lab |
| miniboss_ink_jade_warden | mini-boss | checkpoint proposal | PROPOSAL / REGISTRY_SYNC_PENDING | C3_MINI_BOSSES_AND_CHEST_FLOW.md | Architecture, Balance, Visual Lab |
| miniboss_veil_harvester | mini-boss | checkpoint proposal | PROPOSAL / REGISTRY_SYNC_PENDING | C3_MINI_BOSSES_AND_CHEST_FLOW.md | Architecture, Balance, Visual Lab |

Existing first-run enemies, bosses, weapons, passives and synergies were not replaced.

### Защищённые области

- Existing first-run content не изменён: PASS — C3 только описывает proposal IDs.
- docs/architecture/first-run не изменялась: PASS.
- docs/agents/balance-economy не изменялась: PASS.
- docs/agents/core-gameplay-runtime не изменялась: PASS.
- scripts/, scenes/ и project.godot не изменялись: PASS.
- visual_lab и production assets не изменялись: PASS.

## 3. Balance handoff

Balance Agent должен назначить или подтвердить:

- future enemy HP, damage, speed, durability, XP grade/value, wave band, spawn budget и active cap;
- link guard/refresh для enemy_lotus_usher;
- trail, patch, interruptibility и recovery для enemy_moonroot_burrower;
- line lead time, width class, damage category и recovery для enemy_silver_reed_seer;
- prediction horizon, dash geometry, recovery и safe-spawn для enemy_moontrail_stalker;
- mini-boss HP/damage/speed, phase threshold, warning lead time, recovery, adds, resistances и reward weights;
- exact fallback pool/value и deterministic priority при нескольких eligible synergies;
- overlap/performance budget для новых telegraphs.

Все неизвестные числа и частоты имеют статус PENDING_BALANCE или PENDING_B1.

## 4. Runtime handoff

### IDs and state

- four future enemy IDs and two mini-boss IDs;
- boss_encounter_id per run, boss_id, checkpoint_id, encounter_kind and safe_spawn_ref;
- authoritative claimed_synergy_count, claimed_synergy_ids, chest_offer_id, outcome_id and state_revision;
- phase/telegraph lifecycle and cleanup references;
- XP drop and aftermath remain separate stores.

### Existing event consumers

C3 uses existing events only: checkpoint_reached.v1, boss_spawned.v1, boss_defeated.v1, checkpoint_reward_requested.v1, checkpoint_reward_committed.v1, boss_chest_opened.v1, boss_chest_claimed.v1 and stage_advanced.v1.

Rules:

- mini-boss chest is a non-final BOSS_CHEST proposal;
- one chest applies at most one synergy or fallback;
- duplicate defeat/open/claim returns the stored outcome;
- final boss remains no-chest;
- boss chest never becomes an artifact offer;
- future enemies do not mutate wallet and do not create artifact offers.

## 5. Visual Lab handoff

| Visual item | Route | Stage path | Asset metadata |
|---|---|---|---|
| four future enemy families | SPRITE + VFX + UI_ART | docs/mockups/04-enemies/ or future stage after approval | asset_id/family_id/candidate_id: null; PROPOSAL; technical NOT_RUN; artistic PENDING |
| Ink Jade Warden | SPRITE + VFX + UI_ART | docs/mockups/05-bosses/ | asset_id/family_id/candidate_id: null; PROPOSAL; technical NOT_RUN; artistic PENDING |
| Veil Harvester | SPRITE + VFX + UI_ART | docs/mockups/05-bosses/ | asset_id/family_id/candidate_id: null; PROPOSAL; technical NOT_RUN; artistic PENDING |
| chest/evolution explanation | UI_ART + VFX | docs/mockups/19-synergy-info/ | asset metadata assigned only by Visual Lab |

Readability target: true 1× gameplay context at 390×844, warm ivory telegraphs, soft jade/smoky teal body language, muted brass structure, no toxic neon and no black-on-black danger signal. No mockups were created.

## 6. Checks

- ID uniqueness: PASS — proposed IDs are distinct from the live first-run enemy/boss IDs and from the C1/C2 catalog IDs; checked against the current Content Registry and catalog index before commit.
- Required-field coverage: PASS — six C3 entries each contain silhouette, role/signature, telegraph, arena interaction, counter-decision, phase/spawn, VFX/audio/haptic hooks, reward boundary and balance questions.
- Chest boundary: PASS — five non-final windows are described; final boss has no chest; fallback is separate from synergy claim.
- Protected-scope review: PASS — planned write set is limited to docs/agents/content-design/.
- JSON validation: PASS — updated CONTENT_CATALOG_INDEX.json parses and keeps run_1 counts unchanged.
- Remote diff review: performed after commit; exact commit SHA is reported in the delivery note.

## 7. Незакрытые вопросы

| Question | Impact | Owner | Status | Next action |
|---|---|---|---|---|
| Future enemy batch insertion stage and wave bands | controls first-run scope and pacing | Project Owner + Balance | PENDING_PRODUCT_DECISION | approve a future stage |
| Mini-boss cadence and encounter_kind schema | controls five chest windows and BossDirector ownership | Architecture + Balance | PENDING_ARCHITECTURE/PENDING_BALANCE | sync checkpoint contract |
| Future enemy base stats and spawn caps | controls readability, difficulty and Android performance | Balance | PENDING_BALANCE/PENDING_B1 | bind from B1/derived model |
| Fallback pool and simultaneous synergy priority | controls chest usefulness without fake evolution | Balance + Product | PENDING_PRODUCT_DECISION | choose deterministic rule |
| Registry/save quarantine for unapproved future IDs | controls restore safety | Architecture | PENDING_ARCHITECTURE | confirm unknown-ID policy |
| Visual family and candidate production | controls asset route and approval | Visual Lab | PENDING_ARTISTIC_REVIEW | intake briefs only |

## 8. Следующий шаг

- Balance Agent: numeric binding and future-stage pacing review.
- Architecture/Runtime Agent: Registry, encounter_kind, safe-spawn, event and idempotency sync.
- Visual Lab: review briefs and create representative masters in protected visual stages.
- Content Agent: proceed to C4 arena drop catalogue after C3 handoff is accepted; do not call C3 runtime-ready.

