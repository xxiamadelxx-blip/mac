---
name: godot-release-gate
description: Gate MAC Godot Android release claims on a real build, artifact, installation, and launch evidence. Use whenever an agent builds, validates, publishes, or reports an APK/AAB as ready.
---

# godot-release-gate

Never call an Android build ready from source code, a successful static check, a workflow start, or a screenshot of a build page.

Require all applicable evidence:

- a real successful Godot export job on the current commit;
- the actual APK/AAB download, exact filename, byte size, SHA-256, package ID, version name, and version code;
- no parse errors, import errors, missing asset errors, or unfinished placeholders in the build log;
- installation on the target Android device or an equivalent real device check;
- launch evidence showing the app opens and the acceptance flow works, including the first playable slice;
- the workflow run URL/ID and command exit codes.

Use `BLOCKED` when the runner, artifact, install, or launch proof is unavailable. Do not generate a substitute APK, reconstruct an artifact from text, mark a pending job successful, or promote an old build as proof for a new commit. A code change can be `IMPLEMENTED`; it is not `RELEASED` until this gate passes.
