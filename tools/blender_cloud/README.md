# MAC Blender Cloud — isolated headless trial

**TASK-ID:** MAC-BLENDER-CLOUD-01. **Status:** infrastructure trial only; no hero assets regenerated. **Working branch:** tooling/blender-cloud-20261009.

## What this provides

GitHub Actions installs real Blender on an Ubuntu cloud runner, launches CPU Cycles in background mode, renders a technical transparent 256×256 PNG, verifies RGBA dimensions and SHA-256, and publishes PNG/JSON as an Actions artifact. User needs no local computer or GPU.

## Acceptance test

Any push changing the workflow or tools/blender_cloud in this branch triggers "Blender Cloud | headless rendering smoke". A successful run contains actual Blender version output, CLOUD_BLENDER_SMOKE_OK, CLOUD_BLENDER_PNG_VERIFIED, and an artifact named blender-cloud-smoke-<run_id>. Technical PNG is NOT a game asset.

## Limitations

- On-demand GitHub Actions cloud runner, not an interactive GUI or always-on Blender API.
- Do not promote any test output to docs/mockups, runtime manifests, or APPROVED GOLDEN.
- Future approved heroine rig workflow needs actual approved source layers, an editable rig/master, provenance, user approval, and true 1x gameplay-scale QA.
- Do not mutate or regenerate Lin Yue, Soyeon Han or any already approved identity.
- Github Actions proof artifacts expire; canonical PNGs need one-file-per-PNG GitHub commits following the project batch contract.
- Render Free has 512 MB RAM, temporary local storage, and idle sleep. Production-quality rendering may require a more capable worker.
- Creating a Render web service requires the user to select/confirm the Render workspace first and must not start paid resources implicitly.
