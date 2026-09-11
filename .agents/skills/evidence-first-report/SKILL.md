---
name: evidence-first-report
description: Require every MAC status claim to be backed by exact evidence. Use for handoffs, audits, CI, Storage, runtime, balance, content, visual, and release reports.
---

# evidence-first-report

Report what was proven, not what was intended.

Every handoff must contain:

- task ID and one-line observable result;
- parent HEAD and resulting HEAD, when a repository change was made;
- exact changed paths and write scope;
- commands or API operations actually run, with exit codes or HTTP results;
- artifact/object path, size, SHA-256, run URL/ID, or an exact file inventory where applicable;
- status chosen from `READY`, `IMPLEMENTED`, `VERIFIED`, `PARTIAL`, or `BLOCKED`;
- concrete open blockers and exactly one next action.

Do not use `DONE` for a plan, manifest, screenshot, job creation, cached result, old commit, or agent message without the acceptance evidence. If evidence is missing, say `BLOCKED` or `PARTIAL`; never invent output, success, file existence, artistic approval, or release readiness.
