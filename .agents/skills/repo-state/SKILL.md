---
name: repo-state
description: Establish the live MAC repository baseline before any task. Use when an agent must determine the current branch, HEAD, canonical documents, drift, ownership, or whether a previous handoff is still valid.
---

# repo-state

Use the live repository as the only source of current state.

1. Confirm repository `xxiamadelxx-blip/mac` and branch `main`.
2. Read the current `main` ref and record its exact HEAD before writing.
3. Read `AGENTS.md`, `README.md`, `GAME_MANIFEST.md`, `AGENT_CONTEXT.md`, the relevant `ROADMAP.md` section, and `docs/AGENT_SYNC_STATE.md`.
4. Read the domain instructions for the requested task and inspect the actual files they describe.
5. Treat old handoffs, screenshots, release pages, cached context, and earlier HEADs as historical until the live tree confirms them.
6. Re-check `main` immediately before every write. If HEAD moved, stop, reread the changed coordination documents, and recalculate the scope.

Report the repository, branch, parent HEAD, canonical contract, relevant paths, and contradictions before implementation. Never infer that a file, asset, test, or release exists from a name or a document alone.
