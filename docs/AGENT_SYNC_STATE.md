# Agent Sync State — Live Coordination Baseline

> **Operational router, not a release/approval claim.** Read this file from the current `main` before any work. Re-check `main` immediately before writing.

- Snapshot HEAD: `15458f6df8148a6337cdeb9e27a9f82359eef4c6`
- Snapshot tree: `3cc96c0ded01bc8d5720eac7e9dfab7becc3b055`
- Snapshot date: 2026-09-11 UTC
- Repository: `xxiamadelxx-blip/mac`, branch `main`

## 0. Anti-context-loss rule

One task has one observable result, one owned write set, and one evidence bundle. Do not paste binary files or Base64 into chat. Visual binaries are committed as individual PNG files in GitHub; each agent run places exactly 40 files when 40 or more remain, or the complete final remainder when fewer than 40 remain, and the evidence manifest carries metadata only.

Before work: read this file; claim one task ID; record the parent SHA; edit only the assigned paths; report exact evidence and one next action.



## 1. Observed repository state

| Area | Observed state at this snapshot | Truth label |
|---|---|---|
| Lin Yue runtime folder | 0 PNG files; reference layer PNGs: 10 | **BINARY_INTAKE_PENDING** |
| Soyeon Han runtime folder | 0 PNG files | **BINARY_INTAKE_PENDING** |
| Enemies | Ink Beetle root PNG: 10; Lantern Moth root PNG: 10; no full 8×12 directional packs | **PARTIAL / NOT PROMOTED** |
| Arena v03 | 19 v03 SVG/JSON/MD assets; v03 is user review, v02 is fallback | **USER REVIEW** |
| Content C1/C2 | 10 weapons, 10 passives, 10 synergies; max 5 synergy claims | **CONTENT SPECIFIED** |
| Balance B1 | 7 wave bands and 6 main checkpoint records through 1800s; extensions still proposed/pending | **PARTIAL / SIMULATION ONLY** |
| Runtime registry | Targets 1800s, 6 main, 5 mini; current JSON shape does not expose consumable `mini_bosses` or `elite_variants` arrays | **R2/R3 BLOCKED** |
| CI/Godot | No current R2/R3 or Android proof; recent evidence is incomplete/failing | **NO RELEASE EVIDENCE** |

Tree entries at snapshot: 232.

## 2. Active locks for continuation

- Run: **30:00 / 1800 seconds**.
- Main bosses: **6** at 05:00, 10:00, 15:00, 20:00, 25:00, 30:00. Two extension identities are pending reconciliation; do not silently invent final names.
- Mini-bosses: **5** at 07:30, 12:30, 17:30, 22:30, 27:30. Documents currently disagree between 2, 3 and 5; runtime target is 5, and three records are missing.
- `MAIN_BOSS`: freeze visible run clock, wave clock, XP and ordinary spawning from intro through settlement; use a separate encounter clock.
- `MINI_BOSS`: run clock, waves, XP and ordinary spawning continue.
- Elite variants: bounded, maximum 5 registered variants, finite selection, no permanent roster mutation, no automatic artifact offer.
- Final main boss at 30:00 has no boss chest.
- Boss reward, ordinary chest and artifact offer are separate channels. Artifact offer is exactly three cards; no pre-run slots.
- Artifact reconciliation is open: content has 10 IDs while architecture counts 8. Do not delete or silently remap IDs.
- Arena v03 stays candidate/user-review; v02 remains fallback until artistic approval plus technical import/collision proof.
- No `APPROVED GOLDEN`/`PRODUCTION` without the Visual Lab approval route.
- **Base64/PNG in chat is prohibited.**

## 3. Critical audit findings

1. Root docs still contain legacy 20-minute / 4-boss language. Treat it as historical, not as the active implementation contract.
2. Architecture says 3 intermediate bosses in places, while runtime acceptance targets 5. This is a contract gap.
3. Balance has 30-minute wave/checkpoint material, but `scripts/runtime/content_registry.gd` reads top-level (or `simulation_model`) `mini_bosses` and `elite_variants`; current model exposes neither in that shape. Static R2 join therefore remains red.
4. Hero v02 manifests claimed `PNG_RGBA_1024_PASS`, but no runtime PNGs exist in either hero target folder. Keep binary intake pending.
5. Enemy target breadth exceeds binary reality: a 10-ID roster and 8×12 target exist, but two masters have only partial root frames and nine derived candidates are absent.
6. Simulation is not Godot/Android evidence. A successful model run cannot close R2/R3.
7. C5 and several handoffs are historical snapshots with old baseline SHAs; useful history, not green gates.

## 4. Assignment board

### Phase A — contract reconciliation

| ID | Owner | Allowed write set | Deliverable / acceptance |
|---|---|---|---|
| `SYNC-01` | Content | `docs/agents/content-design/` | Stable semantic IDs for 2 pending main extensions and 3 missing mini records; checkpoint/kind/dependencies; explicit `PROPOSED`; no code/art claims. |
| `SYNC-02` | Architecture | `docs/architecture/first-run/` | One consistent contract for 6 main + 5 mini, MAIN freeze/MINI continue, and mapping of 15 chest windows to reward channels; validator/invariants; no gameplay code. |

### Phase B — registry and runtime

| ID | Owner | Allowed write set | Deliverable / acceptance |
|---|---|---|---|
| `SYNC-03` | Balance | `docs/agents/balance-economy/` and `BALANCE_MODEL.json` | One parseable 30-minute registry shape: 7 waves, 6 main, 5 mini, bounded elite records, XP/reward/chest records; exact arrays consumed by `content_registry.gd`; seeds 101/202/303/404/505; proposed values stay labeled. |
| `SYNC-04` | Runtime | `scripts/runtime/` and runtime handoffs | Consume one registry; test main freeze, mini continuation, bounded elite, separate chest/artifact, final no-chest, idempotent settlement; actual command/stdout/artifact/exit code. Block honestly if runner unavailable. |
| `SYNC-05` | CI/QA | `.github/workflows/`, CI handoffs, evidence only | Fresh R1/R2/R3 checks on current parent; distinguish code/import/runner failure; run IDs and exact failing step or artifact. No retry loop without new evidence. |

### Parallel visual/binary lanes

| ID | Owner | Allowed write set | Deliverable / acceptance |
|---|---|---|---|
| `VIS-02` | Visual Lab / Arena | `docs/mockups/02-arena/` | Review v03 and preserve v02 fallback; no scene promotion or production claim without approval/import/collision proof. |
| `VIS-04` | Visual Lab / Enemies | `docs/mockups/04-enemies/` | Inventory actual partial files first; correct manifest; approve representative master before deriving nine candidates; no full-pack claim. |
| `ASSET-03` | Binary transport | Individual GitHub PNG batch commits + Stage 03 evidence | Exact 96/192 PNG files under `docs/mockups/03-heroes/`; one run places 40 or the final remainder; evidence has paths, blob SHA, size and SHA-256. No chat encoding. |
| `PROJECT-INTEGRATOR` | Single docs integrator | root docs after accepted handoffs | Update legacy markers/indexes from accepted Phase A/B results in one small commit; no parallel root rewrites. |

Dependency order:

```text
SYNC-01 + SYNC-02  →  SYNC-03  →  SYNC-04  →  SYNC-05
VIS-02, VIS-04 and ASSET-03 may run in parallel, but cannot promote unapproved/unverified assets.
```

## 5. Required handoff

```text
TASK-ID: SYNC-04
Parent HEAD: <SHA read immediately before work>
Changed paths: <exact list>
Status: READY | PARTIAL | BLOCKED | VERIFIED
Evidence: <command, run ID, artifact path, exit code, or exact candidate list>
Open blockers: <concrete list>
Next action: <exactly one>
```

Never write only `done`. Manifest ≠ binary, simulation ≠ runtime, screenshot ≠ approval.

## 6. Copy/paste task for an agent

```text
Read docs/AGENT_SYNC_STATE.md from current main first.
Claim TASK-ID: <one ID only>.
Goal: <one observable result>.
Allowed paths: <exact write set>.
Inputs: <exact source files>.
Do not: edit another task's write set; paste Base64/PNG in chat; invent pending IDs/numbers; promote candidate art.
Acceptance: <exact validator/command/evidence and exit code>.
Report: parent HEAD, resulting HEAD, changed paths, status, evidence, blockers, exactly one next action.
```

## 7. Stop list

- Do not use old 20:00 / 4-boss text as active contract.
- Do not count 2 or 3 mini records as runtime target 5.
- Do not claim hero assets until actual files are imported and counted.
- Do not call model output Godot/Android proof.
- Do not promote Arena v03 or enemy candidates without Visual Lab gates.
- If `main` moved, stop, re-read this file, and rebase the task mentally before writing.

## 8. GitHub PNG batch transport

- Каноническое бинарное хранилище — repository `xxiamadelxx-blip/mac`, branch `main`; PNG лежат отдельными файлами под `docs/mockups/<stage>/`.
- GitHub Release assets не считаются файлами репозитория и не используются для intake.
- Отдельный `USER REVIEW` preview допускается до открытия большой партии для утверждения внешнего вида.
- Один агентский запуск обрабатывает одну партию: ровно 40 PNG, если осталось 40 или больше, либо весь остаток, если осталось меньше 40.
- После каждой партии создаётся `docs/asset_batches/<stage>/batch-<NNN>.json` с фактическими paths, blob SHA, размером, SHA-256 и commit SHA.
- `PLACED` ставится только после проверки фактических GitHub blobs. Manifest, список имён, скриншот и сообщение агента не являются binary evidence.
- `docs/ci/STAGE03_IMPORT_REQUEST.json` остаётся `PENDING_GITHUB_UPLOAD` до размещения 192 отдельных PNG Stage 03; ожидаемый порядок: `40 + 40 + 40 + 40 + 32`.
- ZIP, архивы, PNG/Base64 в чат и кодовая отрисовка финального визуала запрещены. Внутреннее кодирование GitHub API не передаётся в чат.
- Этот transport reset не утверждает, не мутирует и не перегенерирует Линь Юэ, Соён Хан, арену или другой арт.

Current conclusion: **coordination baseline is published by this file; the project is not release-ready.**
