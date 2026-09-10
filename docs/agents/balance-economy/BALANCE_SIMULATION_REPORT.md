# Balance Simulation Report — 30-minute MAC model

Status: \`PARTIAL / SIMULATED_MODEL_ONLY\`

## Scope and provenance

- Task: \`REF-BALANCE-REF-01\`.
- Parent HEAD before writes: \`488c5bbd6b0ad412f0c1647eb99e17d31a6953a0\`.
- B1: \`docs/BALANCE_ECONOMY_SPEC.md\`, revision \`6aa4ec96afc8a8c9e6a35c164c99e7d62910a687\`, design baseline.
- Model: \`docs/agents/balance-economy/BALANCE_MODEL.json\`, 30-minute v0.4.
- Runtime claim: \`NOT_IMPLEMENTED\`; no Godot or Android run was used.
- External repositories were pattern references only. No external number, ID, loot odds or content asset was copied.

Reference pattern evidence: [VampireSurvivorsClone](https://github.com/matthiasbroske/VampireSurvivorsClone), [20-Minutes-till-dawn](https://github.com/ParsaSabzei/20-Minutes-till-dawn), [Sentaur Survivors](https://github.com/sentry-demos/unity). The extracted common shape is XP threshold → upgrade offer, time/level-keyed wave pressure, explicit boss/special encounter state, finite elite/special windows and separate loot/offer resolution.

## Reproduction commands and exit status

The following ran against the current 30-minute model snapshot and fresh architecture snapshot:

\`\`\`
python3 current_balance_validator.py --model current_balance_model.json --architecture fresh_architecture_contract.json
# exit 0
# BALANCE_CONTRACT_CHECK=PASS

python3 verify_balance_30m.py --model current_balance_model.json --simulator current_balance_simulator.py
# exit 0
# INDEPENDENT_30M_CHECK=PASS
\`\`\`

Independent result:

- runs: 30 (two heroes × three profiles × five seeds);
- seeds: 101, 202, 303, 404, 505;
- repeat hash: \`2d901903a59cc88926b4413c5caa71cb92e2321cd3b446e93e6ee14db5f43d92\`;
- survived: 24/30;
- completed inside the final-boss target window: 21/30.

## Profiles and progression

| Profile | Inputs | Survived | Completed | Level at 02/05/10/15/20/25/30 min | Incoming damage mean |
|---|---|---:|---:|---|---:|
| fresh | all meta ranks 0; proposed hit probability 0.08; two heroes × five seeds | 5/10 | 2/10 | 2 / 5 / 9 / 13 / 17 / 20 / 24 | 86.110 |
| moderate | vitality/power 3; agility/focus/magnet/defense 2; two heroes × five seeds | 9/10 | 9/10 | 2 / 6 / 10 / 13 / 17 / 21 / 24 | 68.468 |
| max_m1 | all six meta branches rank 10; two heroes × five seeds | 10/10 | 10/10 | 2 / 6 / 10 / 14 / 18 / 22 / 26 | 52.488 |

Profile definitions and all proposed values are in the JSON with \`source\`, \`derived_formula\`, \`rationale\` and \`status\`. Fresh completion target is still a product decision; the current proposed model yields 2/10 completed.

## TTK and incoming pressure

| Encounter | Fresh | Moderate | Max M1 | Target / status |
|---|---:|---:|---:|---|
| Ordinary | 0.75–1.25s | 0.75–1.25s | 0.50–0.75s | B1 0.5–2.5s; SIMULATED |
| Existing elite | 17.25–27.75s | 18.25–25.25s | 14.00–20.00s | B1 10–25s; PARTIAL |
| Elite variant | 7.00–20.25s | 5.75–14.50s | 7.00–15.25s | proposed 5–15s; PARTIAL |
| Mini-boss | 42.50–54.75s | 39.00–50.25s | 30.25–38.25s | proposed 20–55s; SIMULATED |
| Main 05/10/15 | 63.25–78.00s | 58.25–70.50s | 44.75–54.50s | B1 45–80s; SIMULATED |
| Main 20/25 | 110.25–123.75s | 100.50–113.25s | 78.00–87.75s | proposed 60–100s; PARTIAL |
| Final 30 | 117.25–130.50s | 107.25–119.75s | 82.75–92.75s | B1 90–120s; PARTIAL |

Mean peak incoming DPS ranges: fresh 40.0–56.0, moderate 48.608–54.880, max M1 36.0–63.0. The single-hit telegraph-bound check passed in the model; it is not runtime collision evidence.

## Active cap and boss results

- Proposed maximum active cap: 400.
- Maximum occupancy ranges: fresh 340–400; moderate 330–400; max M1 400.
- p95 occupancy ranges: fresh 324–382; moderate 291–382; max M1 382.
- Overflow attempts are discarded; no spawn debt accumulates.
- Main bosses: six checkpoints at 05:00/10:00/15:00/20:00/25:00/30:00; model freezes visible run/wave/XP/spawn clocks.
- Mini-bosses: five windows at 07:30/12:30/17:30/22:30/27:30; model continues visible clock, waves and XP.
- Moderate sample \`hero_lin_yue/seed 101\`: main TTK 59.5 / 62.5 / 58.25 / 101.5 / 100.5 / 107.25s; mini TTK 45.5 / 43.5 / 39.0 / 39.75 / 42.25s.
- Post-main ramp: every cycle emits suppression → recovery → linear ramp → siege; independent check verified monotonic density and the low-entry reset.
- Elite variants: all three architecture variant IDs observed; at most five finite packs/run.

## Rewards and idempotency

Completed model total for the proposed 30-minute schedule: **1575 Gold / 520 Moon Seals / 16 Boss Essence**. Failed runs keep only rewards settled before defeat.

- wallet duplicate commit: PASS;
- non-final boss chest duplicate/open/reopen: PASS;
- elite artifact offer duplicate resolution: PASS;
- every offer has exactly three cards and one selected card;
- final 30:00 boss emits no boss chest;
- first-clear artifact offer is a separate after-result channel;
- elite offers do not mutate wallet.

## Remaining blockers

1. Architecture clock policy still conflicts with the balance main-boss freeze rule.
2. Architecture/content registry has three intermediate records while the balance target has five mini-boss slots.
3. New main/mini numeric kits, elite numeric overrides and visual records are not joined to production content.
4. B1 does not yet canonize 20:00–30:00 wave, XP, combat or reward values.
5. Runtime and Android profiling have not produced traces.

This report is model evidence only. It must not be read as game/runtime verification.
