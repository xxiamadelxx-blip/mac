# Content Handoff — C4: каталог дропов арены

## 1. Идентичность

- Repository: xxiamadelxx-blip/mac
- Branch: main
- HEAD: 894e4c35fa626d5c41cfa0d38a3e1e646fa89118 (baseline, проверенный перед записью C4)
- Slice: C4
- Status: CONTENT_SPECIFIED
- Catalog version: 1
- Date: 2026-09-10

C4 — content design package. Он не является runtime implementation, balance lock, visual approval или production delivery.

## 2. Scope

| content_id | type | status | source | next owner |
|---|---|---|---|---|
| arena_drop_heal_mote | arena drop / нефритовая капля | PROPOSAL / REGISTRY_SYNC_PENDING | C4_ARENA_DROP_CATALOGUE.md | Balance, Architecture, Visual Lab |
| arena_drop_coin_cache | arena drop / лунная монета | PROPOSAL / REGISTRY_SYNC_PENDING | C4_ARENA_DROP_CATALOGUE.md | Balance, Architecture, Visual Lab |
| arena_drop_xp_magnet | arena drop / лунный магнит опыта | PROPOSAL / REGISTRY_SYNC_PENDING | C4_ARENA_DROP_CATALOGUE.md | Balance, Architecture, Visual Lab |
| arena_drop_destruction_seal | arena drop / печать разрушения | PROPOSAL / REGISTRY_SYNC_PENDING | C4_ARENA_DROP_CATALOGUE.md | Balance, Architecture, Visual Lab |
| arena_drop_wave_freeze | arena drop / печать остановленной волны | PROPOSAL / REGISTRY_SYNC_PENDING | C4_ARENA_DROP_CATALOGUE.md | Balance, Architecture, Visual Lab |
| arena_drop_ward_shard | arena drop / осколок оберега | PROPOSAL / REGISTRY_SYNC_PENDING | C4_ARENA_DROP_CATALOGUE.md | Balance, Architecture, Visual Lab |
| arena_drop_vacuum_bloom | arena drop / цветок сбора | PROPOSAL / REGISTRY_SYNC_PENDING | C4_ARENA_DROP_CATALOGUE.md | Balance, Architecture, Visual Lab |

Existing first-run roster, C1/C2/C3 IDs and meta tree were not replaced. Write set is limited to content-design docs.

## 3. Content decisions

- Ровно семь обязательных drop families: heal, coin/Gold, XP magnet, destruction, wave freeze, shield/ward и vacuum/harvest.
- XP magnet использует current canonical XP source; «mana» — открытый product decision, второй resource ID не создан.
- Coin cache предлагает Gold через RewardLedger; direct persistent wallet mutation не предложена.
- Destruction не получает silent kill-credit/reward rule: defeat vs removed outcome выбирают владельцы.
- Freeze не останавливает run clock, checkpoints, boss/mini-boss encounter или offer/settlement states.
- Ward не является flat passive, max-HP upgrade или unconditional invulnerability.
- Vacuum по умолчанию harvest-ит XP и coin, но не активирует utility drops.
- XP и aftermath, boss chest, artifact offer и final reward остаются отдельными surfaces.

## 4. Balance handoff

- source tiers, drop-table weights, cadence/frequency, safe-spawn и performance caps;
- Gold/healing quantity/value и resource ownership;
- XP magnet radius/duration/attraction/target cap;
- destruction scope/whitelist, elite behavior, defeat/removal, kill credit и reward output;
- freeze duration, ordinary spawn pressure, actor/projectile/wind-up lifecycle и resistance;
- ward mitigation/absorption, eligible damage, lethal boundary, charge, stacking/refresh;
- vacuum radius, target cap, wall/LOS policy и XP/Gold eligible set;
- interaction с meta pickup/healing nodes и artifact triggers.

Все неизвестные числа и частоты имеют PENDING_BALANCE/PENDING_PRODUCT_DECISION; B1 XP formula/grades и RewardLedger totals не меняются.

## 5. Runtime handoff

- stable drop_id и уникальный drop_instance_id на run;
- source context, world position, pickup/effect/cleanup state и target references;
- per-instance/per-target/per-reward idempotency;
- wall/line-of-sight/safe-spawn и reconnect/restore policy;
- owner systems для health, Gold, XP collection, destruction, freeze и ward;
- canonical names/schema для новых activation/resolve events.

Существующий xp_drop_collected.v1 сохраняется для фактического XP collect. XpDropStore/ProgressionSystem владеют XP, RewardLedger — Gold settlement, CombatSystem/WaveDirector — combat/wave resolution. Ни один arena drop не открывает chest, claim-ит synergy, создаёт artifact offer или обходит final-boss no-chest.

## 6. Visual Lab handoff

| Visual item | Route | Stage path | Asset metadata |
|---|---|---|---|
| Heal mote / coin cache | SPRITE + VFX + UI_ART | docs/mockups/02-arena/, docs/mockups/09-xp/ | asset_id/family_id/candidate_id: null; PROPOSAL; technical NOT_RUN; artistic PENDING |
| XP magnet / vacuum bloom | SPRITE + VFX + UI_ART | docs/mockups/09-xp/, docs/mockups/02-arena/ | asset_id/family_id/candidate_id: null; PROPOSAL; technical NOT_RUN; artistic PENDING |
| Destruction seal / wave freeze | SPRITE + VFX + UI_ART | docs/mockups/02-arena/ | asset_id/family_id/candidate_id: null; PROPOSAL; technical NOT_RUN; artistic PENDING |
| Ward shard | SPRITE + VFX + UI_ART | docs/mockups/02-arena/ | asset_id/family_id/candidate_id: null; PROPOSAL; technical NOT_RUN; artistic PENDING |

Visual code: deep blue-grey, smoky teal, warm ivory, muted brass, soft jade; muted crimson/violet only for role/status accent. Проверка — true 1× arena scale, 390×844 UI/combat, cluttered aftermath/XP, telegraph visibility, pickup feedback and cleanup. Mockups этим commit не создаются.

## 7. Checks

- ID uniqueness: PASS — семь C4 IDs distinct from live first-run, C1/C2/C3 and meta IDs.
- Required fields: PASS — each entry has visual signal, pickup rule, effect intent, feedback, limitations, PENDING_BALANCE, player decision and owner boundary.
- Semantic separation: PASS — XP magnet = attraction over time; vacuum = bounded harvest pulse; heal/ward are not passives.
- Reward boundary: PASS — no direct wallet write, duplicate XP/aftermath, boss chest/artifact/synergy mutation or final-boss exception.
- Numeric boundary: PASS — frequency, quantity, duration, radius, cap and value remain open.
- Protected-scope review: PASS — write set is limited to docs/agents/content-design/.
- JSON/roster validation: PASS — index parses, Run 1 IDs/limits are preserved, seven drop IDs are unique.
- Remote diff review: performed after commit; final SHA is reported in delivery note.

## 8. Open decisions

| Question | Owner | Status | Next action |
|---|---|---|---|
| Source cadence/drop-table ownership | Balance + Product | PENDING_BALANCE/PENDING_PRODUCT_DECISION | bind source tiers and weights |
| Gold target and settlement UI | Product + Architecture | PENDING_PRODUCT_DECISION | approve wallet/timing |
| XP vs mana label/semantics | Product + Architecture | PENDING_PRODUCT_DECISION | resolve before data/UI mapping |
| Destruction defeat vs removal reward | Product + Balance + Runtime | PENDING_PRODUCT_DECISION/PENDING_ARCHITECTURE | choose idempotent path |
| Freeze actor/telegraph lifecycle | Architecture + Balance | PENDING_ARCHITECTURE/PENDING_BALANCE | define scope and resume |
| Ward mitigation/lethal/duplicate rules | Balance + Runtime | PENDING_BALANCE/PENDING_ARCHITECTURE | bind guards |
| Vacuum target whitelist | Product + Balance | PENDING_PRODUCT_DECISION/PENDING_BALANCE | approve resource-only set |
| Drop schema/events/reconnect | Architecture/Runtime | PENDING_ARCHITECTURE | add canonical contract/tests |
| Visual candidate production | Visual Lab | PENDING_ARTISTIC_REVIEW | intake brief only |

## 9. Следующий шаг

- Balance Agent: numeric binding, source cadence and performance review.
- Architecture/Runtime Agent: Registry, instance/effect schema, event versioning, idempotency and reconnect.
- Visual Lab: review briefs and create masters in protected stages.
- Content Agent: C5 catalog consolidation and acceptance review after C4 is accepted; do not call C4 runtime-ready.
