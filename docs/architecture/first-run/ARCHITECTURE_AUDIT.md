# ARCHITECTURE_AUDIT — расширение первого забега до 30 минут

Статус: VERIFIED
Scope: логическая архитектура первого забега, revision 2
Runtime implemented: NO
Android/APK acceptance: NOT_PERFORMED; Godot-код, сцены, APK, балансный файл и визуальные assets намеренно не входят в завершение этого агента.

## 1. Repository identity

- Repository: xxiamadelxx-blip/mac
- Branch: main
- Parent HEAD inspected before write: afa1aff37d90ac7b90497c1b37a2ab7504485bb4
- Final commit SHA: сообщается в handoff; self-reference намеренно не встраивается в этот однокоммитный audit.
- Local checkout/status/diff: недоступны; использован GitHub tree/file/API fallback.
- No force-push, reset, rebase, deletion or rewrite of existing commits.

## 2. Change contract and interpretation

The user extension brief changes the architecture target to a 30-minute run. The package preserves the two C3 intermediate bosses and adds one more intermediate slot; it preserves the four existing main-boss identities, adds two main-boss slots, and moves the existing final identity to the terminal 30:00 target slot. The 22:30 intermediate placement and five-minute main cadence are explicitly marked working assumptions/pending approval.

Chest architecture now supports up to 15 logical windows: eight configured non-final boss/mini-boss windows and seven reserved non-boss source windows. Chest count is independent from the five synergy-claim cap, artifact offers remain separate, and the final boss creates no chest.

Wave architecture is cycle/phase based: opening or post-boss relief → gradual ramp → pre-boss peak → boss active. Exact extension budgets, caps, multipliers, variant weights and rewards are not invented; they remain pending B1 extension.

Enemy architecture retains ten existing families, reserves three new enemy slots, and defines three data-driven variants for enemy_ink_beetle. Variants preserve base reward boundaries and require a readable detail/marker beyond hue.

## 3. Files changed by the single commit

Only files under docs/architecture/first-run/ are changed:

- AGENT_TASK.md
- AGENT_PROMPT_RU.md
- README.md
- REPO_CONTEXT.md
- DECISIONS_AND_UNKNOWNS.md
- FIRST_RUN_FLOW.md
- FIRST_RUN_STATE_MACHINE.md
- FIRST_RUN_ARCHITECTURE.md
- FIRST_RUN_DATA_CONTRACT.json
- FIRST_RUN_DATA_CONTRACT.template.json
- FIRST_RUN_EVENT_CATALOG.md
- FIRST_RUN_ACCEPTANCE_MATRIX.md
- ARCHITECTURE_AUDIT.md

No duplicate deliverable names or parallel versioned documents were created.

## 4. Read set

Read before editing: AGENTS.md, root README.md, GAME_MANIFEST.md, AGENT_CONTEXT.md, ROADMAP.md, docs/BALANCE_ECONOMY_SPEC.md, docs/MOCKUP_INDEX.md, docs/agents/content-design/C3_MINI_BOSSES_AND_CHEST_FLOW.md, docs/agents/content-design/CONTENT_CATALOG_AND_HANDOFF.md, docs/architecture/first-run/README.md, AGENT_TASK.md, DELIVERABLES.md, REPO_CONTEXT.md, SKILLS_AND_INSTRUCTIONS.md, DECISIONS_AND_UNKNOWNS.md, all six deliverables and the prior audit. Runtime/menu/arena files were inspected only as read-only evidence.

## 5. Requirements checked

- Six required deliverables remain present; actual and template data contracts are both updated to schema version 2 and remain parseable.
- Boot → menu → ПЕРСОНАЖИ → run setup → arena → cycle-based waves → XP/level → weapon/passive offer → scheduled encounters → checkpoint → chest/fallback → next cycle → pause/resume → defeat/victory → result → rewards → menu remains continuous.
- Six main-boss slots, three intermediate slots, terminal final-boss rule and explicit pending content slots are represented.
- ChestWindowRegistry supports 15 windows, with one offer/claim per window and separate BOSS_CHEST, additional source and artifact boundaries.
- Final boss has no boss chest or generic defeat chest; first-clear artifact offer remains a separate post-result source.
- Clock continues through BOSS_INTRO/BOSS_ACTIVE for every scheduled encounter and freezes only at offer/pause/settlement/terminal boundaries.
- WaveDirector explicitly performs post-boss relief before gradual ramp; no hidden per-second HP growth or immediate peak jump is introduced.
- XP, artifact, chest and aftermath remain separate; variant selection does not create a second reward boundary.
- Pause/background, save/restore, reward ledger idempotency, death, victory, no pre-run artifact loadout and prototype/target/implemented/verified distinctions remain in the package.
- Three beetle variants and three new enemy slots are data-driven and explicitly pending where names, visual records or B1 tuning are absent.

## 6. Pending decisions and external boundaries

| ID | Owner | Next action |
|---|---|---|
| U-17 | Balance owner | Publish B1 extension for 30-minute wave phases, caps, budgets, variant tuning and new checkpoint rewards. |
| U-18 | Content owner | Publish stable IDs, names, mechanics and telegraph contracts for two new main bosses, the third intermediate boss and three new enemies. |
| U-19 | Product + Balance owner | Define seven additional chest sources, cadence, outcomes and UI copy; move reserved windows to configured only after approval. |
| U-20 | Product owner | Confirm 22:30 intermediate placement and main five-minute cadence. |
| U-21 | Runtime + Product owner | Define explicit v1→v2 snapshot migration or keep legacy restore blocked. |
| Existing U-01–U-16 | Listed in DECISIONS_AND_UNKNOWNS.md | Resolve through their original owners; this revision does not hide or overwrite them. |

No pending decision was silently written into root docs or B1.

## 7. Designed / implemented / verified

Designed: 30-minute schedule registry, six main/three intermediate encounter model, 15-window chest resolver, post-boss relief/ramp cycle, beetle variant resolver, three pending enemy slots, schema migration boundary and traceability updates.

Implemented by this agent: documentation-only changes inside docs/architecture/first-run/; no runtime behavior or assets.

Verified by this agent: fresh JSON parsing, required-file existence, internal-link/path checks, transition completeness, event/state/data cross-reference, acceptance-to-task coverage, stale-term classification, whitespace scan and scope review after publication. No runtime/APK proof is claimed.

## 8. Mandatory checks and result contract

The post-commit verification records:

| Check | Required evidence | Result |
|---|---|---|
| JSON parse actual/template | JSON.parse for both files | PASS |
| Required deliverables | tree inspection | PASS |
| Internal links | resolver against repository tree | PASS |
| Transition completeness | every transition has trigger/guard/owner/side effects/failure/recovery/idempotency | PASS |
| Event/state/data alignment | names, payload refs, producer/consumer and retry policy | PASS |
| Acceptance vs AGENT_TASK | every task requirement has a matrix row | PASS |
| Stale-term scan | no unqualified active 20-minute/1200-final/final-chest claim; labelled legacy refs only | PASS_WITH_LABELLED_LEGACY |
| git diff --check | local checkout unavailable; remote content whitespace scan | LIMITATION_LOCAL_GIT; REMOTE_SCAN_PASS |
| Scope diff | parent→commit changed paths all under docs/architecture/first-run/ | PASS |
| Rewrite guard | one new commit with parent afa1aff37d90ac7b90497c1b37a2ab7504485bb4, no force update | PASS |

## 9. Handoff

Next agent: Core Gameplay Runtime Agent.

First runtime slice must read the six deliverables and implement only the smallest contract path. Before full M1, runtime must consume the B1 extension/content registry, implement schedule-driven RunSession, WaveCycleDirector, EnemyVariantResolver, ChestWindowRegistry, and schema migration/recovery tests. It must produce fresh evidence for the 30-minute scenario, intermediate encounters, 15-window cap behavior, post-boss relief/ramp, duplicate ledger protection and Android performance. Runtime/APK, balance completion and visual production are intentionally not complete in this architecture commit.
