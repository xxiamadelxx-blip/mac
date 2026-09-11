---
name: bounded-task
description: Keep a MAC agent inside one explicitly assigned task, write set, and acceptance result. Use for implementation, audit, documentation, visual, runtime, CI, or storage work to prevent scope drift and endless refactoring.
---

# bounded-task

Treat each task as one bounded change.

- Claim one task ID, one observable result, and one owned write set.
- Read the task's acceptance condition before editing. Do not widen it because another issue is interesting.
- Change only the allowed paths. Do not perform unrelated cleanup, architecture rewrites, visual regeneration, or repository-wide formatting.
- Close static work that does not require a runner, but do not label runner-dependent work complete without its evidence.
- Do not create placeholders, fake artifacts, simulated logs, or status-only commits to bypass a dependency.
- If a dependency blocks the acceptance condition, preserve completed work, report the exact blocker, and give exactly one next action.
- Re-check the live parent HEAD before writing and report every changed path.

The task is complete only when its stated acceptance evidence exists. Anything outside that evidence remains a separate task.
