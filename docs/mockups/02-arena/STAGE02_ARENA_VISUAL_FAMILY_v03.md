# Stage 02 — Lotus Garden Environment Family v03

Статус: USER REVIEW
Primary route: ART
Secondary route: MOCKUP
Family ID: moonveil-lotus-garden-environment-soft-tonal-v03
Candidate ID: vl-20260910-lotus-garden-topdown-v03

## Решение

v03 переводит арену из composite-постера в top-down environment family. Сначала существует чистая подложка; каждый пруд, мост, камень, корень, камыш, фонарь, лотос, shrine и ствол — отдельный прозрачный ассет с asset_id. Composite собирается из тех же элементов и placement map, что будет использовать будущая Godot-сцена.

Референс пользователя задаёт только язык камеры, вертикальный survival-ритм и читаемость поля. Качество следует GAME_MANIFEST: premium mobile 2D fantasy, читаемые боевые масштабы, единый material/palette language. Кислотные FX, чёрные rings и грубая sketch-текстура reference не переносятся.

## Визуальный код

- deep blue-gray: вода и ночной воздух;
- smoky desaturated teal: грунт и дальние плоскости;
- mist jade: растительность, мягкие края, XP-friendly separation;
- warm ivory: камень, лунный свет, lantern light;
- muted brass: старое дерево и архитектурные кромки;
- restrained desaturated garnet: редкий shrine/lotus accent.

Запрещены toxic neon, чистый чёрный контур, baked HUD, full-body character poster, dense obstacle carpet и отдельный color grade для поздней фазы.

## Scale

- target viewport: 390×844 portrait;
- world: 1560×2532 units, frame is a camera window;
- ordinary open playfield: 65–75%;
- single prop footprint: max 16% of target frame;
- props размещаются на периферии и в landmark pockets;
- центр оставлен для кругового движения, XP и telegraph readability.

## Master and layers

Representative master: arena.prop.lotus_pond_edge.v03.
It proves top-down silhouette, water/stone material separation, muted warm accent, transparent background and pivot at the support edge. Остальные props derived from the same environment family.

z0 base -> z10 landscape props -> z20 authoritative terrain collision -> z30 pooled ambient -> z40 remains -> z50 XP -> z60 hero/enemies -> z70 foreground -> z100 HUD.

## Files and boundary

Exact candidate: docs/mockups/02-arena/STAGE02_ARENA_TOPDOWN_COMPOSITE_v03.svg
Inspection: docs/mockups/02-arena/STAGE02_ARENA_TOPDOWN_INSPECTION_v03.svg
Asset board: docs/mockups/02-arena/STAGE02_ARENA_ASSET_BOARD_v03.svg
Asset manifest: docs/mockups/02-arena/STAGE02_ARENA_ASSET_MANIFEST_v03.json
Placement map: docs/mockups/02-arena/STAGE02_ARENA_PLACEMENT_MAP_v03.json
Base and props: docs/mockups/02-arena/assets/

This is USER REVIEW evidence. Godot import, collision, Android FPS, raster export, runtime promotion and artistic approval remain open. Existing v02 runtime fallback is unchanged.
