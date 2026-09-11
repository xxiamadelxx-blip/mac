# Контекст репозитория для агента архитектуры первого забега

## Снимок

Аудит начат на branch main, parent HEAD 75a559b74e10c487e79c76db47d5ce887a46454c. Работа должна быть опубликована поверх этого HEAD без переписывания истории. Все записи этой задачи ограничены docs/architecture/first-run/.

## Технологический контракт

MAC — Godot 4.x, native 2D, GDScript. Runtime boundaries: AppShell, ContentLoader, RunCoordinator, RunSession, SimulationClock, WaveCycleDirector, EnemyVariantResolver, RewardLedger и SaveSnapshot. Unity-репозитории служат только reference material.

## Канонический target

- 1800 секунд.
- Main checkpoints: 300, 600, 900, 1200, 1500, 1800.
- Mini checkpoints: 450, 750, 1050, 1350, 1650.
- Ordered encounters: 11.
- Chest registry: 15 typed windows — 10 BOSS_CHEST и 5 ELITE_CHEST.
- Registry map: 10 ordinary, 10 elite catalog, max 5 active elite, 2 legacy compatibility.
- Three beetle ordinary visual variants inherit base reward boundaries.
- MAIN_BOSS freezes visible run/wave/XP/spawn clocks through settlement. MINI_BOSS continues them. Separate encounter clock advances for both.
- Artifact offer is exactly three cards and one choice, separate from build slots and first-clear result boundary.

## Read-only evidence from other zones

At this audit snapshot:

| Zone | Observed status | Architecture handling |
|---|---|---|
| Balance | PARTIAL / MODEL_ONLY; late numeric profiles remain proposed | Keep numeric fields PENDING_B1 |
| Runtime | PARTIAL / BLOCKED; no current Godot stdout and exit-code evidence | Do not claim implementation |
| Content | Handoff ready with open reconciliations; proposals remain proposed | Consume IDs as registry references, not artistic approval |
| Visual Lab | No approval for variant assets | Keep visual records PENDING_VISUAL |
| Root/B1 | Read-only source material | No edits |

## Status vocabulary

- designed: described in docs.
- target: intended contract.
- implemented: runtime code exists.
- verified: evidence proves the stated gate.
- This package is verified only for architecture documents and static consistency.