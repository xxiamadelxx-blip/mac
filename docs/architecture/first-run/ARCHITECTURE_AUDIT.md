# ARCHITECTURE_AUDIT — 30-minute first-run architecture

## Status

**VERIFIED** for the architecture-document gate. **DONE** means the allowed static architecture work is complete. This is not a project-wide runtime or balance status.

## Repository identity

- Repository: xxiamadelxx-blip/mac
- Branch: main
- Parent HEAD: 75a559b74e10c487e79c76db47d5ce887a46454c
- Resulting HEAD (audited architecture tree before this report file): a5e74ca4c12328d8cae2744410e8e534970cf5d2
- Audit-file publication follows this audited tree; the final main squash SHA is recorded in the handoff.
- Engine: Godot 4.x / GDScript
- Task: REF-ARCH-01 / ARCH-30M-FINAL

## Changed files

Exactly the following files are changed by the architecture package:

1. AGENT_PROMPT_RU.md
2. AGENT_TASK.md
3. README.md
4. REPO_CONTEXT.md
5. FIRST_RUN_FLOW.md
6. FIRST_RUN_STATE_MACHINE.md
7. FIRST_RUN_ARCHITECTURE.md
8. FIRST_RUN_DATA_CONTRACT.json
9. FIRST_RUN_DATA_CONTRACT.template.json
10. FIRST_RUN_EVENT_CATALOG.md
11. FIRST_RUN_ACCEPTANCE_MATRIX.md
12. DECISIONS_AND_UNKNOWNS.md
13. ARCHITECTURE_AUDIT.md

No file outside docs/architecture/first-run/ is part of this change.

## Requirements checked

- Six main records and five MINI_BOSS records are present.
- The ordered schedule contains 11 encounters at the canonical checkpoints.
- Chest registry contains 10 BOSS_CHEST and 5 ELITE_CHEST windows.
- Terminal encounter has no chest; first-clear artifact offer is separate.
- MAIN_BOSS and MINI_BOSS clock policies are distinct and explicit.
- Wave pressure has post-boss relief before ramp and peak.
- Registry map is reconciled to 10 ordinary, 10 elite catalog, max 5 active elite and 2 legacy records.
- Three beetle variants require palette plus readable detail and inherit base reward boundaries.
- Artifact offer is exactly three cards and one choice without build-slot consumption.
- Full boot → menu → run → waves → XP/level → encounters → pause/recovery → defeat/victory → result → rewards → menu path is documented.
- Every one of 33 transition rows has trigger, guard, owner, side effects, failure, recovery and duplicate/idempotency behavior.
- Event catalog aligns names, producers, consumers, payloads, ordering and retry behavior with state machine and JSON.
- XP, aftermath, chest, artifact and result boundaries are distinct and idempotent.
- Designed, target, implemented and verified statuses are separated.

## Evidence

- JSON parse: FIRST_RUN_DATA_CONTRACT.json PASS.
- JSON parse: FIRST_RUN_DATA_CONTRACT.template.json PASS.
- Static counts: main 6, mini 5, schedule 11, ordinary 10, elite catalog 10, legacy 2, beetle visual 3, windows 15, BOSS_CHEST 10, ELITE_CHEST 5 PASS.
- Transition completeness: 33/33 rows with all required fields PASS.
- Acceptance traceability: AGENT_TASK R-01…R-18 mapped to AT-01…AT-18 PASS.
- Internal links: package-local links resolve PASS.
- Stale-term scan: obsolete slot/loadout/source wording removed; canonical terminal no-chest wording retained PASS.
- Whitespace: git diff --check equivalent PASS on published text.
- Scope: changed paths are confined to docs/architecture/first-run/ PASS.
- Runtime evidence: not run by this agent and not claimed.

## Found and resolved contradictions

- Replaced three-record mini target with five named records from Content sync_01.
- Replaced placeholder late encounter IDs with stable content proposal IDs.
- Replaced mixed chest source model with typed 10 BOSS_CHEST plus 5 ELITE_CHEST.
- Removed the old all-encounter clock rule: MAIN_BOSS freezes visible clocks while MINI_BOSS continues them.
- Kept the terminal encounter outside chest flow.
- Added explicit registry map binding and legacy compatibility boundary.
- Added transition/event/data traceability and explicit schema v3 migration gate.

## Read-only repository audit

The audit read AGENTS.md, docs/AGENT_SYNC_STATE.md, all files in docs/agents/architecture, Balance, Content, Runtime and Asset Transport handoff areas, the root architecture references, B1 and the existing Godot seams. Only this first-run architecture folder is in the write set. The published registry map was consumed without editing it.

## Pending decisions with owner and next action

| Pending item | Owner | Next action |
|---|---|---|
| Late-run wave, spawn, active-cap and reward numbers | Balance | Publish the B1 extension profiles |
| Elite selection weights and ELITE_CHEST cadence | Balance | Bind the ten catalog IDs to numeric profiles |
| Chest fallback and ELITE_CHEST outcome copy | Product + Balance | Publish typed resolver policy |
| Palette plus detail records and real asset references | Visual Lab | Approve visual records |
| v3 save adapter and Android recovery behavior | Runtime + Product | Implement adapter and publish evidence |
| Godot stdout and exit-code evidence | Runtime | Run R3 verification |

## External blockers

- Balance remains PARTIAL/MODEL_ONLY; late numeric profiles and elite cadence are PENDING_B1.
- Runtime remains PARTIAL/BLOCKED; R3 Godot stdout and exit-code evidence is absent.
- Content extension entries remain PROPOSED until their own promotion process.
- Visual Lab approval and real asset references for variants are pending.
- Android save migration adapter and product recovery policy are outside this folder.

## Designed, implemented, verified

- Designed: schedule, state machine, modules, events, data contract, chest/variant/artifact policies.
- Implemented: no runtime code in this task; no claim is made for Godot behavior.
- Verified: static JSON, links, counts, transition completeness, acceptance mapping, terminology and scope.
- Not verified here: Godot execution, Android lifecycle, APK, balance lock, content promotion or artistic approval.

## Handoff

Следующее действие: Balance Agent consumes the reconciled schedule and registry IDs, then publishes the remaining B1 numeric profiles and ELITE_CHEST cadence without changing this architecture folder.
