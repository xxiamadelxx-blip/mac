# R1 runtime handoff

Status: `RUNTIME_VERIFIED`

R1 runtime verification source commit: `ff06451b15b0040f61ccf3f43e8ee3baec19f202` (tested on GitHub Actions job `102889083984`).

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

## Verification evidence

The R1 acceptance run completed on GitHub Actions job
[102889083984](https://github.com/xxiamadelxx-blip/mac/actions/runs/34482674171/job/102889083984)
using the existing `barichello/godot-ci:4.7.2` container. The checkout SHA
was `ff06451b15b0040f61ccf3f43e8ee3baec19f202`.

The workflow captured each Godot process status from `PIPESTATUS[0]`. All three
commands returned exit code `0`, the final R1 check step completed
successfully, and the required stdout markers were present:

| Command | Exit code | Observed stdout |
| --- | ---: | --- |
| `godot --headless --path . --script scripts/runtime/r1_runtime_test.gd` | `0` | `R1_RUNTIME_TEST {"failures":[],"ok":true}` |
| `godot --headless --path . --editor --quit` | `0` | Godot 4.7.2 editor/import bootstrap completed |
| `godot --headless --path . res://scenes/arena/arena.tscn --quit-after 1` | `0` | `R1_RUNTIME_TRACE {...,"ok":true,...}` |

The trace reports an empty diagnostics array and a successful R1 run. The
scene-facing smoke command also produced the trace marker, so the R1 runtime
verification gate is closed.

The editor/import stdout contains non-fatal Godot errors for 14 corrupt PNGs
under `docs/mockups` (including `ERR_FILE_CORRUPT`, `Error loading image`
and `Error importing`). These are content/asset import issues outside the R1
runtime slice; they remain unresolved and are not hidden by this handoff.
The full-project asset import is therefore not declared clean.

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
