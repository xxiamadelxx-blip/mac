# Stage 04 — Enemy Visual Contract v01

Status: IN PROGRESS  
Primary route: MOCKUP  
Secondary route: SPRITE  
Family ID: `family.enemy.moonveil_soft_tonal.v01`

## Purpose

Stage 04 creates ten readable enemy families for Moonveil: Eclipse. The enemy roster must remain legible at the real 390×844 gameplay camera while dozens of targets, XP, projectiles, telegraphs and persistent aftermath share the scene.

This stage does not redefine combat rules. Canonical behavior and balance come from `GAME_MANIFEST.md` and `docs/BALANCE_ECONOMY_SPEC.md`.

## Family direction

The enemy roster belongs to the same soft-tonal visual family as the current menu/arena revision:

- night blue-grey and smoky teal as the environment base;
- warm ivory, muted brass, soft jade and restrained crimson/violet as role accents;
- no acid neon palette;
- silhouette and motion language carry role recognition before color;
- dangerous attacks use clear geometric telegraphs that remain brighter than body decoration but never saturate the entire screen.

## Roster silhouette law

Each family must be recognizable in black silhouette at target scale.

| enemy_id | Silhouette anchor | Role read |
|---|---|---|
| `ink_beetle` | low shell, forward horns, six splayed legs | direct rusher |
| `lantern_moth` | wide wings + hanging lantern abdomen | ranged kiter |
| `bone_carp` | long skeletal fish body | line dash |
| `paper_ghost` | tall paper talisman body + torn sleeves | teleport threat |
| `jade_toad` | squat wide body + oversized back legs | jump / area denial |
| `mirror_fox` | low fox body + oversized tail + shard collar | decoy skirmisher |
| `bell_crab` | huge bell shell + broad claws | frontal tank |
| `thread_doll` | narrow jointed body + long hanging sleeves | beam controller |
| `stone_oni` | massive shoulder triangle + broken horn | elite slam |
| `eclipse_serpent` | long segmented body + crescent head fin | elite trail dash |

No two enemies may rely on a simple recolor of the same body plan.

## Telegraph language

Telegraphs must be readable before damage and stay separate from attack VFX.

- rusher: body compression / pitch + short directional streak;
- ranged: warm-up glow at projectile source;
- line dash: thin locked path line;
- teleport: flicker / dissolve before relocation;
- jump impact: landing circle appears before impact;
- clone: mirror flash before duplicate creation;
- frontal tank: shell/bell cue before guarded claw action;
- slow beam: tension line before slow is applied;
- elite slam: large circular ground telegraph;
- elite serpent: path arc / crescent marker before dash.

Telegraph color is role-coded but restrained. Shape must remain sufficient for readability when color perception is reduced.

## Gameplay scale

Target gameplay viewport: `390x844`.

Scale classes are relative, not final collision sizes:

- small: approx. 18–28 px visual height at 1×;
- small_medium: approx. 24–34 px;
- medium: approx. 30–42 px;
- large: approx. 42–58 px;
- elite: approx. 58–84 px or long equivalent.

Exact collision footprint remains a runtime/data decision and must not be inferred from decorative overhangs such as wings, ribbons, tails or telegraph halos.

## Mass-wave readability

At representative 1× scale:

- at least one silhouette anchor survives even when the enemy is partially obscured;
- elite bodies remain distinguishable without inflating ordinary enemies;
- enemy body, projectile, telegraph, XP and aftermath use separate value bands;
- telegraphs render above aftermath and environment effects;
- XP remains the brightest pickup layer;
- no ambient or body glow may permanently occupy the full telegraph brightness range.

## Representative master gate

The first representative master is `ink_beetle` / Чернильный жук.

Required evidence before batching the remaining nine visual candidates:

1. enlarged master inspection;
2. true 1× gameplay preview at 390×844;
3. silhouette read without labels;
4. rusher telegraph visible before contact;
5. palette compatible with the arena soft-tonal family;
6. candidate ID + provenance + technical/artistic status.

The first master is a family calibration object, not a production sprite.

## Balance linkage

`docs/BALANCE_ECONOMY_SPEC.md` currently defines durability multipliers, XP bands, phase composition and behavior rules. Absolute base HP/damage/speed per `enemy_id` are not yet canonically enumerated there. Stage 04 must not invent those values in isolation.

Therefore:

- durability multiplier and XP band are recorded now;
- absolute base HP/damage/speed remain `PENDING_B1_CONFIRMATION`;
- Stage 04 cannot be marked DONE until B1 contains or explicitly derives those values and the manifest is synchronized.

## Visual Lab handoff

- route: `MOCKUP`
- secondary route: `SPRITE`
- stage_path: `docs/mockups/04-enemies/`
- asset_kind: enemy family + representative master
- family_id: `family.enemy.moonveil_soft_tonal.v01`
- representative asset_id: `enemy.ink_beetle.master`
- candidate_id: `vl-20260909-enemy-ink-beetle-master-v01`
- status: `CANDIDATE`
- technical_status: `PENDING REVIEW EVIDENCE`
- artistic_status: `PENDING`
- manifest/consumer: `STAGE04_ENEMIES_MANIFEST_v01.json`; runtime not promoted
- open_decisions: approve/revise representative Ink Beetle family direction
- next_action: inspect representative master and true 1× review, then batch the remaining nine enemies under this contract
