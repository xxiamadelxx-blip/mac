# Balance XP and Rewards

Status: SPECIFIED / PARTIAL

This document is the progression and wallet contract derived from docs/BALANCE_ECONOMY_SPEC.md at revision 6aa4ec96afc8a8c9e6a35c164c99e7d62910a687. Values marked CANON are copied from B1. Values marked DERIVED are arithmetic from those values. Missing offer, chest, and ledger rules remain explicitly open.

## XP drops

| Drop value | Status | Source | Rule |
|---:|---|---|---|
| 1 | CANON | B1 section 6 | ordinary low-value enemy drop |
| 5 | CANON | B1 section 6 | ordinary/early pressure drop |
| 15 | CANON | B1 section 6 | advanced enemy drop |
| 40 | CANON | B1 section 6 | elite-range drop |
| 80 | CANON | B1 section 6 | high elite drop |
| 250 | CANON | B1 section 6 | special/high-value drop |

Enemy-specific ranges are listed in BALANCE_COMBAT_MODEL.md. Ordinary enemies do not drop gold; their economy contribution is XP and run pressure.

## XP threshold formula

For level L:

    XP_to_next(L) = round(30 + 12 × (L - 1) + 3 × (L - 1)^1.35)

The formula is CANON. The following table is DERIVED by evaluating it with round-to-nearest integer and accumulating thresholds from level 1.

| Current level | XP to next level | Cumulative XP from level 1 |
|---:|---:|---:|
| 1 | 30 | 30 |
| 2 | 45 | 75 |
| 3 | 62 | 137 |
| 4 | 79 | 216 |
| 5 | 97 | 313 |
| 6 | 116 | 429 |
| 7 | 136 | 565 |
| 8 | 155 | 720 |
| 9 | 176 | 896 |
| 10 | 196 | 1,092 |
| 11 | 217 | 1,309 |
| 12 | 238 | 1,547 |

The runtime must document how XP overflow is carried across a level-up and whether multiple level-ups in one pickup frame are allowed. Those are PENDING_PRODUCT_DECISION until a run-session implementation exists.

## Progression timing targets

| Target | Value | Status |
|---|---:|---|
| First level | 30–45 seconds | CANON, B1 section 6 |
| First significant build decision | at or before 90 seconds | CANON, B1 section 6 |
| Level at 10 minutes | approximately 9 | CANON, B1 section 6 |
| First evolution | 8–12 minutes | CANON, B1 section 6 |
| Separate XP aftermath state | required | CANON, B1/AGENT_CONTEXT |
| Actual level-up timing in current runtime | not observed | NOT_IMPLEMENTED |

The first level and level-9 target are not derivable from the threshold formula alone because enemy composition, kill rate, XP pickup latency, and player routing are not implemented.

## Pickup and aftermath contract

- Magnet percentage is a hero/meta input; base is 100% and Lin Yue is 120%, CANON.
- XP must remain readable after combat and remain separate from the aftermath/loot presentation, CANON.
- Exact pickup radius units, attraction speed, pooling, wall handling, merge behavior, and overflow behavior are PENDING_PRODUCT_DECISION.
- The simulator may calculate threshold timelines from an explicit XP-per-second TEST_PLACEHOLDER, but that is not a gameplay result.

## Checkpoint and clear rewards

| Event | Gold | Moon Seals | Boss Essence | Extra | Status |
|---|---:|---:|---:|---|---|
| Boss 1 at 5:00 | 50 | 15 | 1 | — | CANON, B1 section 7 |
| Boss 2 at 10:00 | 75 | 20 | 1 | — | CANON, B1 section 7 |
| Boss 3 at 15:00 | 100 | 25 | 1 | — | CANON, B1 section 7 |
| Final boss at 20:00 | 200 | 60 | 2 | — | CANON, B1 section 7 |
| First-clear bonus | 300 | 180 | 1 | Artifact chest | CANON, B1 section 7 |
| Full first clear total | 725 | 300 | 6 | includes first-clear bonus | CANON, B1 section 7 |
| Repeat clear total | 425 | 120 | 5 | — | CANON, B1 section 7 |

Defeat after checkpoint: gold is multiplied by 0.5, earned essence is retained, and Moon Seals are awarded only for the defeated boss. This is CANON, B1 section 7. The exact definition of "earned" and the transaction boundary are PENDING_PRODUCT_DECISION.

## Reward ledger and idempotency

The ledger must make one reward grant safe to retry. B1 requires reward idempotency but does not provide the key schema. Before implementation, Product/Architecture must decide:

- run identifier and immutable run-start identifier;
- checkpoint identifier and boss outcome;
- first-clear versus repeat-clear state;
- source revision or reward-table version;
- one transaction or a two-phase pending/committed state;
- replay and reconnect behavior;
- whether a defeated run can grant the same checkpoint twice.

Current status: PENDING_PRODUCT_DECISION / NOT_IMPLEMENTED. The simulator includes a deterministic duplicate-attempt check, but it is a contract exercise, not a wallet integration test.

## Meta economy

Each branch starts at rank 0 and has 10 ranks.

| Branch | Effect per rank | Max ranks | Status |
|---|---:|---:|---|
| Vitality | +2% max HP | 10 | CANON, B1 section 8 |
| Power | +2% total damage | 10 | CANON, B1 section 8 |
| Agility | +1.5% move speed | 10 | CANON, B1 section 8 |
| Focus | -1.5% weapon cooldown | 10 | CANON, B1 section 8 |
| Magnet | +4% pickup radius | 10 | CANON, B1 section 8 |
| Defense | +1% damage reduction | 10 | CANON, B1 section 8 |

Rank r cost:

    cost(r) = round(100 × 1.45^r)

The formula and rank range are CANON. Derived rank costs for the next purchase from rank 0 through rank 9 are:

| Current rank | Cost |
|---:|---:|
| 0 | 100 |
| 1 | 145 |
| 2 | 210 |
| 3 | 305 |
| 4 | 442 |
| 5 | 641 |
| 6 | 929 |
| 7 | 1,348 |
| 8 | 1,954 |
| 9 | 2,833 |

M1 has no paid gacha, CANON, B1 section 9. Summon pricing/guarantee wording is copied to the model but the available summon pool and progression pacing are not wired to runtime.

## Upgrade offers, synergies, and chests

Weapon IDs, passive IDs, synergy IDs, eligibility, offer weighting, slot limits, reroll cost, banish rules, duplicate fallback, and chest contents are PENDING_PRODUCT_DECISION. This document intentionally does not invent those values. Any later simulation that uses them must provide a separate fixture with TEST_PLACEHOLDER labels and a power-budget rationale.
