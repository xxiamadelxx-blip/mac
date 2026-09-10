<!-- LIVE-AGENT-SYNC: read docs/AGENT_SYNC_STATE.md at current main before using this file -->

# Balance Audit — REF-BALANCE-REF-01

Status: \`PARTIAL / SIMULATED_MODEL_ONLY\`

## Live repository evidence

- Repository: \`xxiamadelxx-blip/mac\`.
- Branch: \`main\`.
- Task parent HEAD before the first write: \`488c5bbd6b0ad412f0c1647eb99e17d31a6953a0\`.
- Audit write parent HEAD: \`e269b2ea812a87a374c2585e7bea61770ec69a93\`.
- B1: \`docs/BALANCE_ECONOMY_SPEC.md\`, SHA \`6aa4ec96afc8a8c9e6a35c164c99e7d62910a687\`.
- B1 status: Version 0.1, design baseline; numeric parameters are not wired to code.
- Coordination snapshot: \`docs/AGENT_SYNC_STATE.md\` still records snapshot \`ceb9781c24adcd8737f6953573f4ebc9103ae366\`; live main was re-read immediately before this write.
- Architecture contract revision: \`bd1d4d44f9c0a525b26ac136d98ace3cf76a3d00\`.
- Runtime status: \`NOT_IMPLEMENTED\` for this balance contract; no Godot/Android evidence was created.

## What was corrected

The published \`BALANCE_MODEL.json\` was a stale 20-minute model while the balance handoff and current coordination lock require 30 minutes. It is now synchronized to the existing 30-minute v0.4 model:

- one JSON source for 7 bands, 6 main checkpoints and 5 model mini checkpoints;
- main-boss visible clock/wave/XP/spawn freeze;
- mini-boss visible clock/wave/XP continuation;
- post-main recovery → monotonic ramp → peak siege;
- no immediate mini-boss density spike; finite elite pack after defeat;
- XP, HP/ATK scaling, TTK, incoming risk, weapon/passive/synergy/fallback and reward/idempotency fields;
- external pattern provenance with no imported foreign numbers, IDs, loot odds or assets.

B1 CANON values were not rewritten. All absent 30-minute, elite, mini, base enemy and artifact values remain PROPOSED, PENDING_B1 or PENDING_PRODUCT_DECISION in the model.

## Reference pattern extraction

Only these common patterns were accepted:

| Pattern | Evidence | MAC application | Numeric import |
|---|---|---|---|
| XP → level threshold → offer | [VampireSurvivorsClone](https://github.com/matthiasbroske/VampireSurvivorsClone), [20-Minutes-till-dawn PlayerController](https://github.com/ParsaSabzei/20-Minutes-till-dawn/blob/main/core/src/main/java/ap/project/controller/PlayerController.java), [Sentaur LevelProgression](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/SceneManagers/LevelProgression.cs) | keep B1 XP formula; resolve a separate three-card choice | none |
| time/level-keyed wave density | [MonsterSpawnTable](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Scripts/Monsters/MonsterSpawnTable.cs), [DifficultyCurve](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/SceneManagers/DifficultyCurve.cs), [SpawnDirector](https://github.com/sentry-demos/unity/blob/main/Assets/Scripts/SceneManagers/SpawnDirector.cs) | read MAC bands, composition and cap from JSON | none |
| explicit boss/special encounter | [BossMonster](https://github.com/matthiasbroske/VampireSurvivorsClone/blob/main/Assets/Scripts/Monsters/BossMonster.cs), [MonsterController](https://github.com/ParsaSabzei/20-Minutes-till-dawn/blob/main/core/src/main/java/ap/project/controller/MonsterController.java) | typed checkpoint events with separate encounter clock | none |
| post-boss pressure state | keyed spawn/ramp systems above plus B1 interruption rule | suppression → recovery → low entry → linear ramp → siege | none |
| elite/variant window | special/boss separation in the three references | bounded seeded overlay event, then return to ordinary roster | none |
| rewards/chests | [Chest/LootTable](https://github.com/matthiasbroske/VampireSurvivorsClone/tree/main/Assets/Scripts/Gameplay), [Sentaur XP/upgrade flow](https://github.com/sentry-demos/unity/tree/main/Assets/Scripts) | XP, boss chest, elite offer, first-clear offer and wallet ledger are separate channels | none |

## Evidence

- Remote model parses as JSON; current model fields: duration 1800, 6 main, 5 mini, 6 reference-pattern rules, runtime \`NOT_IMPLEMENTED\`.
- Contract validator: \`BALANCE_CONTRACT_CHECK=PASS\`, exit 0, against architecture snapshot.
- Independent deterministic checker: \`INDEPENDENT_30M_CHECK=PASS\`, exit 0.
- 30 runs: two heroes × three profiles × five seeds; repeat hash \`2d901903a59cc88926b4413c5caa71cb92e2321cd3b446e93e6ee14db5f43d92\`.
- Results: 24/30 survived, 21/30 completed; fresh 5/10 survived and 2/10 completed; moderate 9/10; max M1 10/10.
- Occupancy stayed at or below proposed cap 400; wallet/chest/elite-offer idempotency passed in the model.
- Full levels, TTK, incoming damage, boss results and reward output are in \`BALANCE_SIMULATION_REPORT.md\`.

## Changed files in this task

- \`docs/agents/balance-economy/BALANCE_MODEL.json\`
- \`docs/agents/balance-economy/BALANCE_WAVE_TABLE.md\`
- \`docs/agents/balance-economy/BALANCE_COMBAT_MODEL.md\`
- \`docs/agents/balance-economy/BALANCE_XP_REWARDS.md\`
- \`docs/agents/balance-economy/BALANCE_SIMULATION_REPORT.md\`
- \`docs/agents/balance-economy/BALANCE_ACCEPTANCE_MATRIX.md\`
- \`docs/agents/balance-economy/DECISIONS_AND_UNKNOWNS.md\`
- \`docs/agents/balance-economy/BALANCE_AUDIT.md\`

Runtime code and content IDs were not modified.

## Remaining blockers

1. Architecture clock contract still advances elapsed time through bosses while this balance rule freezes main-boss visible clocks.
2. Architecture/content registry exposes three intermediate records while the requested model has five mini-boss slots.
3. Pending main/mini content records, absolute enemy combat values, elite numeric/visual records and extension reward values are not canonical.
4. Artifact effects, refresh/stacking policy and fresh-profile completion target remain product decisions.
5. Godot runtime traces and Android FPS/occupancy evidence are absent; the Python model cannot close those gates.

## Next implementation slice

Architecture/Runtime must reconcile the main-boss freeze and five-mini registry, then consume the single \`BALANCE_MODEL.json\` and emit the same timer, wave, XP, combat and idempotency traces before this package can leave PARTIAL.
