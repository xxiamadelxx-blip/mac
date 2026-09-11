# Решения и открытые вопросы

Source: [data contract](./FIRST_RUN_DATA_CONTRACT.json) and [audit](./ARCHITECTURE_AUDIT.md).

## 1. Подтверждённые решения

| ID | Status | Decision | Evidence |
|---|---|---|---|
| C-01 | CONFIRMED | Target run is 1800 seconds | AGENT_SYNC_STATE and JSON |
| C-02 | CONFIRMED | Six main checkpoints are 300, 600, 900, 1200, 1500 and 1800 | JSON schedule |
| C-03 | CONFIRMED | Five mini checkpoints are 450, 750, 1050, 1350 and 1650 | Content sync_01 and JSON |
| C-04 | CONFIRMED | Ten non-terminal encounters create typed BOSS_CHEST windows | JSON chest registry |
| C-05 | CONFIRMED | Five additional windows are typed ELITE_CHEST and remain reserved pending cadence | JSON chest registry |
| C-06 | CONFIRMED | Terminal encounter has no chest; first-clear artifact offer is post-result and separate | Flow and state machine |
| C-07 | CONFIRMED | MAIN_BOSS freezes visible run/wave/XP/spawn clocks through settlement | Clock policy |
| C-08 | CONFIRMED | MINI_BOSS keeps those clocks and ordinary spawn advancing; encounter clock advances for both | Clock policy |
| C-09 | CONFIRMED | Artifact offer has exactly three cards and one choice; artifacts do not use build slots | JSON artifact contract |
| C-10 | CONFIRMED | Registry map has 10 ordinary, 10 elite catalog, max 5 active elite and 2 legacy compatibility records | REGISTRY_VARIANT_MAP.json |
| C-11 | CONFIRMED | Three beetle records are ordinary visual variants with palette plus detail marker | JSON variant policy |
| C-12 | CONFIRMED | XP, aftermath, chest, artifact and result are separate idempotent boundaries | State machine and event catalog |
| C-13 | CONFIRMED | B1 remains the authority for numeric wave, spawn, active-cap and reward values | Read-only B1 |

## 2. Pending questions

| ID | Status | Question | Owner | Next action |
|---|---|---|---|---|
| U-01 | PENDING_PRODUCT_DECISION | What are optional bonus-state semantics? | Product | Approve before result slice |
| U-04 | PENDING_PRODUCT_DECISION | What exact fallback reward and copy does a BOSS_CHEST use when no eligible pair exists? | Product | Publish fallback table |
| U-06 | PENDING_PRODUCT_DECISION | What is the Android recovery window and abandon behavior? | Product + Runtime | Approve recovery policy |
| U-08 | PENDING_PRODUCT_DECISION | Which optional HUD/result fields are required? | Product | Publish presentation matrix |
| U-11 | PENDING_B1 | How are odd defeat rewards rounded? | Balance | Add rule to B1 |
| U-12 | PENDING_PRODUCT_DECISION | What are artifact refresh cost and limit? | Product | Approve artifact policy |
| U-13 | PENDING_PRODUCT_DECISION | How do artifact duplicates and stacking behave? | Product | Approve stacking policy |
| U-14 | PENDING_B1 | Which elite IDs are selected by phase and what is their cadence? | Balance | Bind catalog to numeric profiles |
| U-15 | PENDING_PRODUCT_DECISION | What are artifact effect definitions? | Product | Approve effect catalog |
| U-17 | PENDING_B1 | What are late-run wave, spawn, active-cap and reward numbers? | Balance | Publish B1 extension |
| U-18 | PENDING_VISUAL | Which palette/detail records and real asset references are approved? | Visual Lab | Approve visual records |
| U-19 | PENDING_PRODUCT_DECISION | What trigger, cadence and outcome resolve the five ELITE_CHEST windows? | Product + Balance | Publish typed resolver policy |
| U-20 | BLOCKED_EXTERNAL_SYNC | How will v1/v2 saves migrate to schema v3? | Runtime + Product | Implement adapter and evidence |
| U-21 | BLOCKED_EXTERNAL_SYNC | When will successful Godot stdout and exit-code evidence be published? | Runtime | Run R3 verification |

## 3. Scope conclusion

Architecture-owned static blockers are closed by this package. External Balance, Runtime, Visual Lab and product approvals remain explicitly pending. This folder does not modify or certify those systems.
