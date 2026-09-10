# R1 runtime handoff

Status: `IMPLEMENTED_LOCALLY / RUNTIME_VERIFICATION_BLOCKED`

Base `main` checked for this change set: `3f5b903a27b17f5a9f0818a3a5a479c1090a10cc`.

This handoff covers only the R1 runtime slice. It does not claim that the
first run is production-ready or that the balance model is final.

## Scope

- `ContentRegistry` loads and validates `res://docs/agents/balance-economy/BALANCE_MODEL.json`.
- `RunSession` owns the authoritative run aggregate and revision counter.
- `RunCoordinator` is the command boundary for run start, wave fixture, combat
  fixture, XP collection, upgrade offer, pause/resume and recovery.
- `SimulationClock` keeps visible run time and encounter time as separate
  deterministic clocks. Boss orchestration remains R2.
- `R1RuntimeEntry` is attached to the arena scene and emits a deterministic
  diagnostic trace when the scene is run.
- `r1_runtime_test.gd` is a headless acceptance fixture for the R1 matrix.

## Balance and provenance boundary

Canonical wave bands, contact cooldown, XP formula and hero/build IDs are read
from `BALANCE_MODEL.json` at runtime. The combat enemy and weapon records are
explicitly marked `PROPOSED_MODEL_ONLY` in the trace because the source model
itself marks those numeric fixtures as proposed. No new tuning values were
added to the runtime scripts.

The R1 fixture intentionally does not implement bosses, boss chests, artifacts,
full wave spawning or Android packaging. Those remain later slices.

## Expected commands

From the repository root:

```text
godot --headless --path . --script scripts/runtime/r1_runtime_test.gd
godot --headless --path . --editor --quit
```

The scene-facing smoke path is:

```text
godot --headless --path . res://scenes/arena/arena.tscn --quit-after 1
```

Expected markers are `R1_RUNTIME_TEST` and `R1_RUNTIME_TRACE`. The test should
cover content load, duplicate start, fixture hit cooldown, defeat and XP
collection, duplicate pickup, blocking offer, frozen offer clock, claim and
duplicate claim, pause/resume, invalid-save recovery, independent encounter
clock, and deterministic replay.

## Verification boundary for this handoff

The current execution workspace does not contain the Godot executable, so a
Godot exit code and runtime trace could not be produced locally. Until the
commands above run in a Godot-enabled environment, the runtime status is
`RUNTIME_VERIFICATION_BLOCKED`, not `RUNTIME_VERIFIED`.

## Commit boundary

The intended R1 change set is limited to:

- `scripts/runtime/content_registry.gd`
- `scripts/runtime/run_session.gd`
- `scripts/runtime/simulation_clock.gd`
- `scripts/runtime/run_coordinator.gd`
- `scripts/runtime/r1_runtime_entry.gd`
- `scripts/runtime/r1_runtime_test.gd`
- `scenes/arena/arena.tscn`
- this handoff file

Protected root, architecture, balance, asset, menu and arena-preview scripts
are not part of the change set.
