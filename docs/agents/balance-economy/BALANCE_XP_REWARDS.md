# Balance XP and Rewards — 30-minute MAC model

Status: \`PARTIAL / SIMULATED_MODEL_ONLY\`

Source baseline: B1 revision \`6aa4ec96afc8a8c9e6a35c164c99e7d62910a687\`. The simulator reads the single \`BALANCE_MODEL.json\`; it does not duplicate XP, wave, reward or profile values in Python.

## XP and level-up

Canonical formula from B1 §6:

\`\`\`
XP_to_next(L) = round(30 + 12 × (L − 1) + 3 × (L − 1)^1.35)
\`\`\`

Canonical drop vocabulary is \`[1, 5, 15, 40, 80, 250]\`. B1 does not specify pickup latency, collection capacity, boss-XP placement in the main curve or 20:00–30:00 progression targets. Those inputs are explicit PROPOSED/PENDING fields in the model.

| Input | Model handling | Status |
|---|---|---|
| XP drop values and formula | read from B1 | CANON |
| Pickup delay and band capacity | data fields used by simulation | PROPOSED / PENDING_B1 |
| Magnet effect on pickup | B1 radius is CANON; capacity link is proposed | CANON + PROPOSED |
| Boss XP in level curve | excluded until B1 maps it to progression | PROPOSED / PENDING_B1 |
| Level-up choice | one resolved level transition, then exactly three candidates | DERIVED from B1/architecture surface |
| Upgrade/synergy/fallback numbers | read from model; no UI/controller constants | PROPOSED / PENDING_PRODUCT_DECISION |

The requested common pattern is also visible in the references: XP pickup feeds a threshold/milestone transition and the upgrade choice is a separate state. See [20-Minutes-till-dawn PlayerController](https://github.com/ParsaSabzei/20-Minutes-till-dawn/blob/main/core/src/main/java/ap/project/controller/PlayerController.java), [Sentaur LevelProgression](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/SceneManagers/LevelProgression.cs) and [Sentaur UpgradeManager](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/Upgrades/UpgradeManager.cs). Their numbers are not imported.

## Five-seed model result

Across heroes \`hero_lin_yue\` and \`hero_seoyeon_han\`, seeds \`101/202/303/404/505\`:

| Profile | First level | Level at 02:00 | 05:00 | 10:00 | 15:00 | 20:00 | 25:00 | 30:00 | Final-level range |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fresh | 39.75s | 2 | 5 | 9 | 13 | 17 | 20 | 24 | model run dependent |
| moderate | 38.25s | 2 | 6 | 10 | 13 | 17 | 21 | 24 | model run dependent |
| max_m1 | 33.25s | 2 | 6 | 10 | 14 | 18 | 22 | 26 | model run dependent |

The level rows are aggregate checkpoint values for runs reaching that checkpoint; deaths can end a row early. Fresh matches B1's early targets in the model; later extension levels are not B1 CANON.

## Reward channels

The model keeps these channels separate:

1. ordinary XP drops;
2. non-final boss chest for synergy/evolution or fallback;
3. finite elite-pack artifact offer;
4. first-clear artifact offer after result settlement;
5. final main boss reward without a boss chest.

B1's canonical 20-minute reward arithmetic remains:

- full first clear: 725 Gold / 300 Moon Seals / 6 Boss Essence plus an artifact chest;
- repeat full clear: 425 Gold / 120 Moon Seals / 5 Boss Essence;
- defeat after a checkpoint: 50% checkpoint Gold and 100% earned Essence; Moon Seals only for defeated bosses.

The 30-minute model adds proposed late checkpoint rows; completed model runs currently settle the proposed extension total at **1575 Gold / 520 Moon Seals / 16 Boss Essence**. This is PROPOSED model output, not a new CANON reward.

## Idempotency and offer rules

| Event | Key / invariant | Observed model |
|---|---|---|
| Wallet checkpoint | \`{run_id}:{reward_scope}:{checkpoint_id}:{reward_type}\` | duplicate commit returns existing entry; PASS |
| Boss chest | one settlement per non-final checkpoint | duplicate open/reopen does not grant again; PASS |
| Elite offer | exactly three cards, one choice, no wallet mutation | duplicate resolution returns stored offer; PASS |
| First-clear offer | after result finalization, separate from final boss chest | no automatic pre-result grant; PASS in model |
| Final boss | no boss chest | no final boss chest emitted; PASS in model |

Artifact effect values, refresh cost/limit, duplicate stacking and exact elite cadence remain PENDING_PRODUCT_DECISION/B1. The model never treats a three-card offer as a fixed pre-run loadout or weapon/passive slot.

## Boundary

This is deterministic model evidence, not Godot, save/reconnect, UI, Android or player-telemetry evidence.
