---
name: supabase-asset-contract
description: Enforce MAC visual asset paths, manifests, and Supabase Storage transport. Use whenever an agent uploads, downloads, deletes, inventories, or connects PNG/SVG, sprites, portraits, arena art, VFX, UI art, or other binary assets.
---

# supabase-asset-contract

Use the canonical MAC Supabase project `ylhbihgrchtqzaphuxvy` and private bucket `visual-assets` unless the live repository explicitly changes that contract.

- Store each PNG/SVG as its own Storage object mirroring the canonical asset path, for example `moonevil-eclipse/docs/mockups/<stage>/<asset>.png`.
- Do not use archives, Base64, data URLs, chat messages, GitHub Contents blobs, or GitHub Release assets as the binary transport.
- GitHub stores code, scenes, manifests, instructions, and evidence metadata. Godot code references stable asset IDs and build-local paths; it does not draw final visual art.
- Every manifest entry must identify `asset_id`, `local_path`, `storage.bucket`, `storage.object`, `content_type`, `size_bytes`, `sha256`, provenance, and technical/artistic status.
- Upload with an authorized Supabase Storage API/CLI/CI secret and stream the individual file. A database-management connection can verify the project and metadata but cannot by itself carry binary bytes.
- After upload, download or otherwise byte-verify each object and compare its size and SHA-256. `READY`, `IMPORTED`, or `PRODUCTION` requires that evidence.
- Keep `visual-assets` private. Never expose service/secret keys to Godot or an APK.
- Never change or weaken RLS to work around a missing binary channel. If the authorized Storage upload path is absent, return `BLOCKED_BINARY_ARTIFACT` with the exact missing capability.
- Visual Lab approval and technical Storage verification are separate gates. Uploading a file never approves, mutates, or regenerates a heroine or any other art.
