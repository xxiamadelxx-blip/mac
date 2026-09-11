---
name: github-png-batch-contract
description: Enforce delivery of real PNG assets into the MAC GitHub repository in bounded batches of at most 40 files per agent run. Use whenever visual PNGs are generated, uploaded, checked, or wired into the game.
---

# github-png-batch-contract

GitHub repository `xxiamadelxx-blip/mac`, branch `main`, is the canonical binary store for MAC PNG mockups and visual assets.

- Commit every real PNG as an individual repository file under its canonical stage path.
- One agent execution handles one batch only: exactly 40 PNG files when 40 or more remain; if fewer than 40 remain, upload exactly the remainder. Never begin the next batch in the same run.
- A single USER REVIEW preview may be committed before a package so the Creative Director can approve the exact appearance. It is not a package.
- Record batch index, paths, per-file size/SHA-256, asset commit SHA and evidence in `docs/asset_batches/<stage>/batch-<NNN>.json`.
- `PLACED` is allowed only after actual GitHub paths/blobs and every file's size and SHA-256 are checked.
- GitHub Release assets are not repository files and are not used. Do not use archives, ZIP files, SVG/HTML/data-URL substitutes, or procedural code as a PNG replacement.
- Any Base64 needed internally by an API is implementation detail; never paste or transmit it through chat, issues, comments, manifests or README.
- The transport agent only delivers existing files. It must not generate, mutate, regenerate, recolor or approve Lin Yue, Soyeon Han or any other artwork.
- Before the next batch, reread live `main`, verify the previous evidence and start only at the recorded next batch index.
- Runtime code references imported local asset paths; it does not draw final visual art.
