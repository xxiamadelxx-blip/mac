# Balance & Economy Audit — Moonveil: Eclipse

## Status

- Overall: **PARTIAL**
- Audit scope: живой аудит числового baseline, runtime seams, тестовой доказуемости и блокеров первого 20-минутного забега.
- No-fix status: **аудит выполнен; runtime, B1 и соседние домены не изменялись**.
- Date: 2026-09-09 UTC
- Рабочая граница: \`docs/agents/balance-economy/\`

Этот документ фиксирует состояние на фактическом \`main\` и не выдаёт design baseline, preview или JSON-шаблон за работающий баланс.

## Live repository evidence

| Поле | Evidence |
|---|---|
| Repository | \`xxiamadelxx-blip/mac\` |
| Branch | \`main\` |
| HEAD | \`df61e063b319e15f8acdc4dde17f21e26ccac69c\` |
| HEAD message | \`docs: add balance economy agent package\` |
| HEAD date | 2026-09-09 23:18:52 UTC |
| Working tree | Не наблюдаем через GitHub read API: доступен committed tree ветки, локальный checkout отсутствует. Чистоту незакоммиченных изменений не заявляю. |
| B1 | \`docs/BALANCE_ECONOMY_SPEC.md\` |
| B1 source revision | \`6aa4ec96afc8a8c9e6a35c164c99e7d62910a687\` |
| Architecture package | \`docs/architecture/first-run/\` на том же HEAD |
| Balance package | \`docs/agents/balance-economy/\` на том же HEAD |

## Sources inspected

### Canonical and repository-level

- \`AGENTS.md\` — \`e67939bdb567f0c41c7a912548fba35601b691ba\`
- \`README.md\` — \`e833211d101907f1fa96f84c10d7e38cdbfe3bbc\`
- \`GAME_MANIFEST.md\` — \`c567dd8757bcd279933ac9fb9cea7179e7762bbc\`
- \`AGENT_CONTEXT.md\` — \`1fa9bf527c227aba68d83fc0d4198fcc8a9d3dd9\`
- \`ROADMAP.md\` — \`85371503047ab881ef1a0baf887273f052ef9ead\`
- \`docs/BALANCE_ECONOMY_SPEC.md\` — \`6aa4ec96afc8a8c9e6a35c164c99e7d62910a687\`

### Balance-agent package

- \`README.md\`
- \`AGENT_PROMPT_RU.md\`
- \`AGENT_TASK.md\`
- \`B1_SOURCE_CONTRACT.md\`
- \`BALANCE_MODEL.template.json\`
- \`DECISIONS_AND_UNKNOWNS.md\`
- \`DELIVERABLES.md\`
- \`REPORT_TEMPLATE.md\`
- \`REPO_CONTEXT.md\`
- \`SKILLS_AND_INSTRUCTIONS.md\`

### Architecture package

- \`docs/architecture/first-run/README.md\`
- \`docs/architecture/first-run/REPO_CONTEXT.md\`
- \`docs/architecture/first-run/AGENT_TASK.md\`
- \`docs/architecture/first-run/DECISIONS_AND_UNKNOWNS.md\`
- \`docs/architecture/first-run/FIRST_RUN_DATA_CONTRACT.template.json\`
- \`docs/architecture/first-run/DELIVERABLES.md\`
- \`docs/architecture/first-run/SKILLS_AND_INSTRUCTIONS.md\`

### Runtime, CI and stage evidence

- \`project.godot\`
- \`export_presets.cfg\`
- \`.circleci/config.yml\`
- \`scenes/menu/menu.tscn\`
- \`scripts/menu/menu_controller.gd\`
- \`scenes/arena/arena.tscn\`
- \`scripts/arena/arena_controller.gd\`
- \`docs/MOCKUP_INDEX.md\`
- \`docs/mockups/04-enemies/README.md\`
- \`docs/mockups/04-enemies/STAGE04_ENEMIES_MANIFEST_v01.json\`
- \`docs/mockups/04-enemies/STAGE04_ENEMY_ROSTER_MANIFEST_v01.json\`
- \`docs/mockups/04-enemies/STAGE04_ENEMIES_VISUAL_CONTRACT_v01.md\`
- \`docs/mockups/04-enemies/STAGE04_ENEMIES_PROVENANCE_v01.json\`

## B1 source / derived / pending matrix

| Domain | Value or rule | Status | Evidence | Impact |
|---|---|---|---|---|
| Base hero | HP 100, move speed 100%, damage x1.00, cooldown x1.00, armor 0, magnet 100% | CANON | B1 §3 | Можно включить в модель без догадок |
| Hero modifiers | Линь Юэ: HP 90, magnet 120%, ranged/control; Соён Хан: HP 110, speed 112%, dash/melee/crit windows | CANON | B1 §3, GAME_MANIFEST §5 | Числовая часть задана; exact crit pipeline отсутствует |
| Wave bands | 0–2/2–5/5–10/10–15/15–20 мин; spawn 6/10/15/22/30 в секунду; active cap 40/80/130/200/280 | CANON | B1 §4 | Можно строить wave table и load model |
| Wave multipliers | HP x1.00/1.10/1.35/1.70/2.20; damage x0.70/0.85/1.00/1.25/1.55; speed x0.90/1.00/1.02/1.05/1.08 | CANON | B1 §4 | Можно считать давление; нельзя утверждать playability без combat inputs |
| Boss interruption | Обычный spawn снижается на 8 секунд; factor 0.70 → 1.00 за 20 секунд | CANON | B1 §4 | Можно формализовать director contract |
| Enemy roles/durability/XP bands | 10 enemy archetypes, durability x1.0–x8.0 и XP bands 1–80 | CANON | B1 §5 | Можно описать роли и XP budget |
| Enemy absolute base stats | Base HP, base damage, base speed и точные contact/ranged values по каждому enemy_id отсутствуют | PENDING_B1 | B1 §5, B1_SOURCE_CONTRACT §3, Stage 04 manifests | Нельзя честно доказать TTK, входящий DPS и no-lethal-hit |
| Combat safety | Contact cooldown 0.8 с; telegraph до опасного урона; elite safe spawn; same-frame damage stack forbidden | CANON | B1 §5 | Правила безопасности известны, runtime их не реализует |
| Damage/armor pipeline | Точная формула mitigation и границы брони не закреплены | PENDING_PRODUCT_DECISION | BALANCE_MODEL.template.json \`damage_pipeline_status\` | Нельзя замкнуть расчёт урона |
| Crit pipeline | Критический шанс/множитель и их формула не закреплены | PENDING_B1 | BALANCE_MODEL.template.json | Нельзя доказать вклад Соён и synergy power |
| XP drops | 1/5/15/40/80/250 | CANON | B1 §6 | Можно строить XP ledger |
| XP curve | \`round(30 + 12 * (L - 1) + 3 * (L - 1)^1.35)\` | CANON | B1 §6 | Можно вычислять derived level thresholds |
| Progression targets | Первый уровень 30–45 секунд, level ~9 к 10 минуте, evolution 8–12 минут | CANON | B1 §6 | Acceptance targets; фактически не проверены |
| Weapon/passive/synergy offers | IDs, offer pool, slots split, reroll/banish, exact eligibility и fallback не закреплены | PENDING_PRODUCT_DECISION | B1 §6, GAME_MANIFEST §6, decisions U-02/U-04 | Нельзя доказать legal offers, build routes и synergy power |
| Boss numeric contract | Имена и общие механики есть в GAME_MANIFEST; boss HP/damage/phase numeric values и arena constraints отсутствуют | PENDING_B1 | GAME_MANIFEST §8, B1 §3/§5, model template | Нельзя доказать boss TTK 45–80/90–120 секунд |
| Checkpoint rewards | 5/10/15/20 мин: 50/75/100/200 Gold; 15/20/25/60 Seals; 1/1/1/2 Essence | CANON | B1 §7 | Можно формализовать ledger rules |
| First/repeat/defeat rewards | First clear bonus 300/180/1 + artifact chest; repeat totals 425/120/5; defeat gold factor 0.5, earned essence retained, seals only for defeated bosses | CANON | B1 §7 | Само начисление не реализовано и не проверено |
| Wallet separation/meta sinks | Gold, Moon Seals, Boss Essence; 6 passive branches; rank cost \`round(100 * 1.45^rank)\`; paid gacha false | CANON | B1 §8–§9 | Можно проверить арифметику и ограничения |
| Reward idempotency key | Точный формат ключа не задан | PENDING_PRODUCT_DECISION | B1/GAME_MANIFEST, model template | Нельзя проверить replay/reopen без ledger contract |
| Profiles | Fresh defined as 0 global upgrades; moderate/max definitions absent | PENDING_PRODUCT_DECISION | BALANCE_MODEL.template.json, B1 §10 | Три acceptance-профиля нельзя воспроизвести одинаково |
| Acceptance | No untelegraphed hit >15% base HP, level gap ≤45 s, synergy ≤40%, two routes per hero, cap safety, 30 FPS, economy bounds | CANON | B1 §10 | Все targets пока SPECIFIED, не SIMULATED/RUNTIME_VERIFIED |

## Derived values available without new product decisions

Следующие значения можно вычислять только из CANON и явно помечать как DERIVED:

- длительность каждой wave band;
- spawn opportunity по полосе: \`spawn_budget_per_second × duration\`;
- XP threshold для каждого уровня из формулы B1;
- суммы checkpoint и first-clear/repeat rewards;
- rank cost для заданного \`rank\`;
- boss recovery curve: линейная интерполяция 0.70 → 1.00 за 20 секунд, если runtime contract подтверждает линейную интерпретацию.

Эти derived values ещё не являются наблюдением runtime и не доказывают проходимость.

## Runtime audit

### Что фактически существует

1. **Menu prototype**
   - \`scenes/menu/menu.tscn\` содержит один \`Control\` со скриптом.
   - \`scripts/menu/menu_controller.gd\` создаёт экраны и кнопки вручную.
   - Переход после loading выполняется через \`change_scene_to_file("res://scenes/arena/arena.tscn")\`.
   - Нет выбранного персонажа, \`RunSession\`, seed, build, wave director, reward ledger или save contract.
   - Arsenal, artifacts и settings explicitly остаются placeholders.
   - В runtime-коде используется архивный v01 background path; это визуальный/prototype drift, не balance runtime.

2. **Arena preview**
   - \`scenes/arena/arena.tscn\` содержит один \`Node2D\` со скриптом.
   - \`scripts/arena/arena_controller.gd\` имеет \`@export var preview_mode := true\`.
   - При \`preview_mode\` 60 реальных секунд ускоряются до 20 отображаемых минут; это preview timer, а не run clock.
   - Реализованы только фон, ambient VFX, ripple/plant/air draw, preview aftermath markers и touch/mouse impact markers.
   - Нет героя, движения, enemy entities, damage/HP, projectiles, XP drops, magnet, upgrades, synergies, bosses, checkpoint, rewards, persistence или HUD.

3. **Runtime data seam**
   - В live tree нет runtime balance data/content registry/enemy combat data.
   - \`BALANCE_MODEL.template.json\` и Stage 04 manifests находятся в \`docs/\` и являются документами/visual manifests, не загружаемым Godot data source.
   - Архитектурный пакет содержит только входные материалы и шаблон \`FIRST_RUN_DATA_CONTRACT.template.json\`; обязательные готовые architecture deliverables отсутствуют.

### Tooling / CI / test evidence

- \`.circleci/config.yml\` запускает только:
  - наличие пяти Godot-файлов;
  - \`godot --headless --path . --editor --quit\`;
  - Android debug export.
- В CI нет balance simulation, combat test, XP/reward test, profile run, cap test или performance test.
- Recursive tree на HEAD содержит 242 paths, но test-like paths не обнаружены.
- Godot CI image зафиксирована как \`barichello/godot-ci:4.7.2\`; project/export files не фиксируют точные Godot/Android SDK/min/target versions.
- JSON syntax validation проведена на read API для:
  - \`docs/agents/balance-economy/BALANCE_MODEL.template.json\`;
  - Stage 04 manifests/provenance.
  Все четыре файла корректны как JSON. Это не доказывает подключение к runtime.

## Findings

### F-01 — Critical: executable run-loop and balance seam are absent

- Finding: проект имеет menu/arena preview, но не имеет исполняемого 20-minute run-loop, который Balance Agent мог бы измерять.
- Evidence: \`scripts/menu/menu_controller.gd\`, \`scripts/arena/arena_controller.gd\`, \`scenes/*/*.tscn\`; \`preview_mode := true\`; отсутствуют RunSession/enemies/XP/waves/bosses/reward/persistence.
- Impact: невозможно заявить IMPLEMENTED, RUNTIME_VERIFIED, playable или M1-ready; balance numbers currently cannot affect the game.
- Confidence: **High**.
- Next Keystone module: \`task-creation\` для тонкого runtime slice после модели; затем \`implementation\`.

### F-02 — Critical: combat inputs required for TTK and safety proof are missing

- Finding: B1 задаёт durability multipliers и XP bands, но не задаёт absolute base HP/damage/speed по enemy_id, точные ranged/contact values, boss numeric stats и mitigation/crit pipeline.
- Evidence: B1 §3/§5; \`B1_SOURCE_CONTRACT.md\`; \`BALANCE_MODEL.template.json\`; Stage 04 manifests сохраняют \`PENDING_B1\`.
- Impact: нельзя честно проверить обычный удар ≤15% HP, enemy/elite/boss TTK, incoming DPS, два устойчивых пути героев или synergy ceiling.
- Confidence: **High**.
- Next Keystone module: \`product-planning\` для решений, которые должны попасть в B1; затем \`task-creation\`.

### F-03 — Critical: no deterministic simulation or balance regression suite

- Finding: нет dependency-free simulator/test suite и нет test-like paths; CI не проверяет ни один B1 acceptance target.
- Evidence: recursive tree audit; \`.circleci/config.yml\`; отсутствие \`BALANCE_SIMULATION_REPORT.md\` и balance tests.
- Impact: уровень/XP cadence, cap occupancy, boss recovery, TTK, reward idempotency и три профиля не воспроизводятся.
- Confidence: **High**.
- Next Keystone module: \`task-creation\` для вертикального simulator slice; затем \`implementation\` и \`code-verification\`.

### F-04 — Watch: build legality and synergy economy are under-specified

- Finding: десять пар оружие-пассивка перечислены в GAME_MANIFEST, но exact offer pool, slot rules, reroll/banish, eligibility, chest fallback and idempotency key отсутствуют.
- Evidence: GAME_MANIFEST §6; B1 §6–§7; decisions U-02/U-04; model template.
- Impact: нельзя доказать, что обе героини имеют два устойчивых build routes и что одна synergy не превышает 40% итогового урона.
- Confidence: **High**.
- Next Keystone module: \`product-planning\`.

### F-05 — Watch: reproducibility and performance evidence are not pinned

- Finding: CI image фиксирует Godot 4.7.2, но exact project/SDK/export environment and target Android device are not locked; no 30 FPS evidence exists.
- Evidence: \`.circleci/config.yml\`, \`project.godot\`, \`export_presets.cfg\`, decisions U-09.
- Impact: simulator/runtime measurements and Android performance claims may not be comparable between runs.
- Confidence: **Medium**.
- Next Keystone module: \`task-creation\` for environment/performance gate.

### F-06 — Watch: stage-status drift affects progress truth

- Finding: \`ROADMAP.md\` says Stage 04 is \`PLANNED\`, while \`AGENT_CONTEXT.md\` and \`docs/MOCKUP_INDEX.md\` say Stage 04 is started/in progress. Architecture context already records this conflict.
- Evidence: \`ROADMAP.md\` stage 4; \`AGENT_CONTEXT.md\` §1; \`docs/MOCKUP_INDEX.md\`; \`docs/architecture/first-run/DECISIONS_AND_UNKNOWNS.md\`.
- Impact: agents may choose different active scopes or incorrectly treat stage work as closed.
- Confidence: **High**.
- Next Keystone module: \`task-creation\` or \`change-review\` for one authoritative status update; not changed by Balance Agent.

## Safe work that is not blocked

- Populate \`BALANCE_MODEL.json\` from the live B1 while preserving source/status/formula for every field.
- Produce wave, XP/reward and combat contracts with unresolved values explicitly pending.
- Calculate derived thresholds, spawn opportunities, reward totals and meta rank costs.
- Create a dependency-free simulator using only canonical inputs plus clearly marked \`TEST_PLACEHOLDER\` profiles/combats; placeholder output cannot be presented as production balance.
- Define the acceptance matrix and a runtime handoff without touching visual assets or unrelated controllers.

## Blocked until decisions or runtime exist

- Production TTK tuning and incoming-DPS claims.
- Boss damage/health tuning and runtime boss proof.
- Exact offer legality, synergy probability and synergy power proof.
- Runtime balance integration and Android performance verification.
- Claims that the 20-minute run is playable or balanced.

## Open decisions carried forward

| ID | Question | Current audit handling |
|---|---|---|
| U-01 | Absolute enemy base HP/damage/speed and contact/ranged values | PENDING_B1; no production values invented |
| U-02 | Exact weapon/passive/synergy IDs and eligibility | PENDING_PRODUCT_DECISION |
| U-03 | Semantics of bonus/streak state | PENDING_PRODUCT_DECISION |
| U-04 | Slot split, offer pool, reroll/banish, chest fallback | PENDING_PRODUCT_DECISION |
| U-05 | Composition ratios inside each wave band | PENDING_B1/DERIVED role-level table only |
| U-06 | Boss numeric stats/arena constraints | PENDING_B1; identities are described in GAME_MANIFEST |
| U-07 | Success-rate definition for fresh profile | PENDING_PRODUCT_DECISION |
| U-08 | Runtime owner of balance data | PENDING_PRODUCT_DECISION; simulator/contract stays in this folder |
| U-09 | Target Android device for 30 FPS evidence | PENDING_PRODUCT_DECISION |
| U-10 | Permission/process for changing B1 | PENDING_PRODUCT_DECISION; no B1 edit made |

## Next implementation slice

**B1.1 — Balance contract and evidence skeleton**

1. Create \`BALANCE_MODEL.json\` from the template using live B1 revision \`6aa4ec96afc8a8c9e6a35c164c99e7d62910a687\`.
2. Create wave, combat, XP/reward and acceptance documents that preserve CANON/DERIVED/PENDING/NOT_IMPLEMENTED.
3. Add a dependency-free deterministic simulator only after its input schema is explicit; keep any non-canonical enemy/boss values as \`TEST_PLACEHOLDER\`.
4. Run JSON validation and an independent consistency check for formula, wave bands, reward sums and idempotency invariants.
5. Do not modify \`docs/BALANCE_ECONOMY_SPEC.md\`, visual manifests, menu, arena preview or visual assets in this slice.

Expected handoff evidence: file paths, live source revision, JSON parse exit status, deterministic command/seed, observed results, and a statement separating simulated from runtime-verified behavior.
