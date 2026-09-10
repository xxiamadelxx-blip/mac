# Balance Decisions and Unknowns — current 30-minute slice

Status: `PARTIAL`. This file records the Balance handling of missing inputs; it
does not amend B1, Architecture, Content IDs or runtime policy.

## Applied model decisions

| Decision | Source | Model handling | Status |
|---|---|---|---|
| Run length is 30:00 | user decision + `AGENT_SYNC_STATE.md` | 1800-second model envelope | `PROPOSED` until B1/root reconciliation |
| Six main checkpoints | sync lock | 300/600/900/1200/1500/1800 | `DERIVED` schedule shape |
| Five mini windows | sync lock | 450/750/1050/1350/1650 | `PROPOSED` IDs pending registry |
| Main clock freeze | sync lock | visible run/wave/XP/spawn stop during every main boss | `CANON` coordination lock; architecture conflict remains |
| Mini clock continuation | sync lock | visible run/wave/XP/spawn continue | `CANON` coordination lock |
| Post-boss low-to-peak ramp | user rule + B1 relief principle | reset 0.80, linear ramp, 60s siege | `PROPOSED` numeric extension |
| Elite registration cap | sync lock + REF-ARCH-02 | full catalog 10; selected run projection ≤5 | cap `CANON`, selection `PROPOSED` |
| Final boss chest | sync lock/architecture policy | no boss chest; first-clear artifact is separate | `CANON` policy |

## Missing B1/product inputs

| Missing value | Source | Derived formula / proposed handling | Status / owner |
|---|---|---|---|
| Absolute HP/ATK/speed for new ordinary families | B1 has roles/multipliers, not absolute stats | `HP = reference DPS × target TTK ÷ durability`; ATK from telegraph/contact budget; speed from engagement distance ÷ delay | `PENDING_B1`, Balance |
| Elite HP/ATK/speed/XP overlays | B1 has no variant numeric table | linked ordinary stat × per-family overlay; all 10 records are explicit and capped to 5 active IDs | `PROPOSED`, Balance/B1 |
| Late 20:00–30:00 wave anchors | B1 ends at 20:00 | continuation of last canonical slope; 38/340 then 48/400 at 25/30 | `PROPOSED`, Product/B1 |
| Late XP targets | B1 target table ends at 20:00 | extend level slope to model anchors 20/24/26 at 30 by profile | `PROPOSED`, Product/B1 |
| Mini-boss stats | content intent only | 20–55s target, `base_hp = target TTK midpoint × reference mini DPS`; records remain proposed | `PROPOSED`, Balance/B1 |
| Elite pack cadence/size | content says finite offers, B1 is silent | one pack after each mini, 3 members, one 3-card offer | `PROPOSED`, Product/Balance |
| Reward rows after 20:00 | B1 has no late rows | monotonic gold/seal/essence extension, first-clear sum + bonus | `PROPOSED`, Product/B1 |
| Hit probability/crit pipeline | B1 acceptance only | profile-specific landed-hit assumptions and expected crit equation | `PROPOSED`, Product/B1 |
| Artifact refresh/duplicate/stacking | product contract incomplete | model only enforces separate three-card/idempotent offer boundary | `PENDING_PRODUCT_DECISION`, Product/Runtime |

## External join blockers

1. The first-run architecture JSON still declares 1200 seconds, four main
   checkpoints and three intermediate records; it also contains the opposite
   boss clock wording. Balance does not rewrite that file.
2. Content has five named mini proposals, while the consumed architecture/B1
   registry has no five promoted mini records. Balance keeps placeholder slots
   visibly pending and does not rename them.
3. Runtime/Godot/Android evidence is absent. A Python model cannot promote the
   package to `VERIFIED`.

Next action: Architecture/Runtime reconciles the 30-minute roster and clock
contract, then runs the R2 trace against the published Balance model.
