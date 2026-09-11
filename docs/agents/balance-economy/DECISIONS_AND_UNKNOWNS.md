# Balance Decisions and Unknowns — current 30-minute slice

Status: `PARTIAL / MODEL_ONLY`.

This file records how missing inputs are represented. It does not amend B1,
Architecture, Content IDs or Runtime policy.

## Applied model decisions

| Decision | Source | Model handling | Status |
|---|---|---|---|
| Run length 30:00 | user decision + sync lock | 1800-second envelope | PROPOSED extension |
| Six main checkpoints | sync lock | 300/600/900/1200/1500/1800 | DERIVED schedule shape |
| Five mini windows | sync lock | 450/750/1050/1350/1650 | PROPOSED IDs pending join |
| Main clock freeze | sync lock | visible run/wave/XP/spawn stop during encounter | CANON coordination lock; runtime join pending |
| Mini clock continuation | sync lock | visible run/wave/XP/spawn continue | CANON coordination lock; runtime join pending |
| Low-to-peak post-boss shape | user rule + B1 relief principle | reset 0.80; 0.70→1.00 recovery; 60s siege | PROPOSED numeric policy |
| Elite registration | sync lock + REF-ARCH-02 | catalog 10; run projection at most 5 | cap CANON; overlays PROPOSED |
| Final boss chest | sync lock / architecture policy | no boss chest; separate first-clear artifact offer | CANON policy |

## Missing values and exact handling

| Missing value | Source | Derived formula / proposed value | Why it serves B1 | Status |
|---|---|---|---|---|
| Absolute ordinary HP/ATK/speed | B1 gives roles/durability, not absolutes | HP from reference DPS × target TTK ÷ durability; ATK from telegraph/contact budget; speed from engagement distance ÷ delay | Keeps ordinary TTK in the 0.5–2.5s envelope while preserving role differences | PENDING_B1; model PROPOSED |
| Elite HP/ATK/speed/XP | B1 has no variant table | linked ordinary record × explicit per-family overlay; resolved and late stats stored | Keeps finite elite threats below/near proposed 5–15s target and avoids hidden runtime numbers | PENDING_B1; model PROPOSED/DERIVED |
| Late wave anchors | B1 ends at 20:00 | 38/340 at 20–25; 48/400 at 25–30; explicit linear post-boss ramp | Extends pressure without an immediate post-boss wall | PROPOSED |
| Late XP targets | B1 target table ends at 20:00 | profile results 20/24/26 at 30:00, read from the same XP formula | Preserves level decisions before late bosses | PROPOSED |
| Mini-boss stats | C3 role intent, no absolutes | 20–55s target; HP = target mini TTK × reference mini DPS; telegraph bound | Adds pressure while waves continue, without main-boss-length interruption | PROPOSED |
| Elite cadence/pack | B1 silent; sync says finite | one finite pack after each mini; 3-card artifact offer; max 5 selected variants | Prevents permanent roster inflation and uncontrolled pressure | PROPOSED / PENDING_PRODUCT_DECISION |
| Late rewards | B1 has no post-20 rows | explicit monotonic 25/30 rows; first-clear and repeat formulas | Keeps checkpoint value legible and separate from ordinary XP | PROPOSED |
| Weapon/passive/synergy gate | C1 says 10/10; mockups say 6/5 | model uses 10/10 and stores conflict metadata | Keeps one explicit gate until Product resolves the conflicting documents | PENDING_PRODUCT_DECISION |
| Artifact refresh/duplicates | product contract incomplete | three-card offer, idempotent key, no hidden duplicate; stacking/refresh remain null | Prevents economy duplication without inventing a shop rule | PENDING_PRODUCT_DECISION |
| Hit probability/crit pipeline | B1 acceptance only | deterministic profile assumptions and expected-crit equation are model inputs | Makes incoming/TTK evidence reproducible without claiming runtime hit proof | PENDING_B1 |

## External blockers

1. The live Architecture contract still reports legacy duration/schedule and
   lacks five mini registry records; Balance does not edit that write set.
2. B1 must promote or revise the explicit proposed absolute table before these
   values can become `CANON`.
3. Runtime/Godot/Android evidence is absent. Python model evidence cannot close
   R2/R3/R4.

Next action: Product/B1 resolves the absolute-stat table and the 10/10 versus 6/5 progression gate, then Runtime binds the accepted model.
