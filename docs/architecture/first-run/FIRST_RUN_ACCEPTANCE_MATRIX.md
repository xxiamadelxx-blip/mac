# FIRST_RUN_ACCEPTANCE_MATRIX — traceability первого забега

Статус: DRAFT ARCHITECTURE SPECIFICATION
Runtime implemented: NO
Правило: VERIFIED_BY_DOC_CHECK означает проверку архитектурного артефакта/ссылки, а не работу Godot runtime или Android APK.

## 1. Матрица требований

| Requirement | Source | Observable behavior / contract | Evidence/check | Status | Owner/next slice |
|---|---|---|---|---|---|
| Boot и splash/loading | AGENT_TASK §2; GAME_MANIFEST | AppShell загружает registry/save и показывает error без blank screen | FIRST_RUN_FLOW §§3, 10; event catalog content_load_* | SPECIFIED | Runtime Iteration 1: AppShell/ContentLoader |
| Главный экран | AGENT_TASK §2 | MAIN_MENU имеет навигацию и read model | FLOW step 3; STATE T-04/T-05 | SPECIFIED | Runtime Iteration 1 |
| Settings и возврат | AGENT_TASK §2 | Settings доступен из menu и pause, invalid values не меняют valid state | FLOW step 4/23; STATE T-04/T-20 | SPECIFIED | Runtime Iteration 2 |
| ПЕРСОНАЖИ | AGENT_CONTEXT; AGENT_TASK | Нейтральный label, карточки character и selected state | FLOW step 5/6; DATA content_registry.characters | SPECIFIED | Runtime Iteration 1 |
| Создание RunSession | AGENT_TASK §2 | Confirm start создаёт новый run_id, seed, content version и revision | FLOW step 8; STATE T-07/T-08; DATA run_session | SPECIFIED | Runtime Iteration 1 |
| Menu/run bridge | AGENT_TASK §3 | MenuFlow отправляет command, RunCoordinator создаёт session; UI не владеет state | ARCHITECTURE §§2–3 | SPECIFIED | Runtime Iteration 1 |
| Arena loading | GAME_MANIFEST; live prototype evidence | Сессия стартует только после validation обязательных gameplay resources | FLOW step 9; ARCHITECTURE ContentLoader | SPECIFIED | Runtime Iteration 1 |
| Movement/combat | GAME_MANIFEST; AGENT_TASK | Simulation consumes clock and emits combat facts, not wallet/UI mutation | ARCHITECTURE Simulation; EVENT combat boundary | SPECIFIED | Runtime Iteration 1 |
| Wave timing | B1 §§4–5 | WaveDirector выбирает B1 bands, spawn budget и active cap, без скрытого роста | DATA wave_bands; FLOW steps 11/16 | SPECIFIED | Runtime Iteration 2 |
| Bosses at 5/10/15/20 min | GAME_MANIFEST; B1 | Boss checkpoint возникает один раз на каждой canonical boundary | STATE T-11/T-12; DATA bosses | SPECIFIED | Runtime Iteration 2 |
| Next stage semantics | AGENT_TASK; DECISIONS U-05 | После нефинального settlement/chest меняется stage projection; финальный босс заканчивает забег без следующей стадии | FLOW §§6, 11; STATE T-15 | PENDING | Product/runtime owner confirms U-05 |
| XP formula and grades | B1 §§6; GAME_MANIFEST | XPDrop collection credits value once and opens level offer at threshold | DATA xp_grades; EVENT xp_* / level_up | SPECIFIED | Runtime Iteration 2 |
| XP versus aftermath | GAME_MANIFEST; B1 §4 | XPDrop и AftermathItem имеют разные IDs, stores, layers и lifecycle | DATA entity_shapes; ARCHITECTURE §7 | SPECIFIED | Runtime Iteration 1 then 2 |
| Kills and stats | AGENT_TASK §2/§4 | RunSession counts kills and projects required combat/progression stats | FLOW §9; DATA run_session.stats | SPECIFIED | Runtime Iteration 1/2 |
| Bonus/series | AGENT_TASK; DECISIONS U-01 | Extensible bonus_state exists; no unconfirmed formula is invented | DATA stats.bonus_state | PENDING | Product owner confirms U-01 |
| Level-up freeze | GAME_MANIFEST; AGENT_TASK | Clock stops, exactly three valid offer projections are shown | STATE T-09/T-10; EVENT level_up/offer_* | SPECIFIED | Runtime Iteration 1/2 |
| Weapon acquisition/upgrade | GAME_MANIFEST | BuildInventory validates New/Upgrade and emits one mutation per offer | DATA weapons/build_entry; EVENT upgrade_applied | SPECIFIED | Runtime Iteration 1/2 |
| Passive acquisition/upgrade | GAME_MANIFEST | Passive slots/ranks and modifiers are data-driven | DATA passives/build_entry | SPECIFIED | Runtime Iteration 2 |
| Slot limits | GAME_MANIFEST; AGENT_TASK | Six weapon and six passive slots; artifacts have no fixed slot capacity and do not consume either build slot type | DATA canonical/build; ARCHITECTURE BuildInventory | SPECIFIED | Runtime Iteration 2 |
| Artifact offer choice | GAME_MANIFEST; product decision | An elite-pack or first-clear source opens an offer with exactly three cards; `Get` selects one effect | DATA artifact_offer; EVENT artifact_offer_created/artifact_chosen | SPECIFIED | Runtime Iteration 2 |
| Artifact refresh | Product decision | `Refresh` is a separate idempotent command; cost, limit and reroll policy remain explicit pending fields | DATA artifact_offer.refresh_policy; EVENT artifact_offer_refresh_* | PENDING | Product owner |
| Artifact effect boundary | GAME_MANIFEST; AGENT_TASK | Active artifact effects are typed run modifiers (aura, derived stat, target, weapon or triggered effect), separate from ordinary passive modifiers | DATA content_registry.artifact_effects; ARCHITECTURE ArtifactEffectSystem | SPECIFIED / PENDING_DEFINITIONS | Product + runtime |
| Artifact sources | Product decision; B1 first-clear reward | Elite packs may create offers between bosses; first-clear creates a separate post-result offer; boss chest remains synergy/fallback only | FLOW; STATE; EVENT elite_pack_defeated/artifact_offer_created | SPECIFIED / PENDING_CADENCE | Product + balance |
| Synergy eligibility | GAME_MANIFEST; AGENT_TASK | Matching pair, max weapon/passive, non-evolved, non-final boss-chest context and claim guard are checked | DATA synergy_evaluator; FLOW §5 | SPECIFIED | Runtime Iteration 2 |
| Synergy/evolution duplicate guard | AGENT_TASK | Repeated claim returns existing outcome; no second evolution | STATE T-15; EVENT synergy_claimed | SPECIFIED | Runtime Iteration 2 |
| Chest eligible path | GAME_MANIFEST; AGENT_TASK | Only non-final boss settlement creates a stable boss-chest offer; eligible synergy/evolution or fallback can be claimed once; final boss chest отсутствует | FLOW §6; STATE T-14/T-15; EVENT chest_* | SPECIFIED | Runtime Iteration 2 |
| Chest fallback path | AGENT_TASK; DECISIONS U-04 | Для нефинального chest fallback_required is representable but exact value is not fabricated; final boss has no fallback chest | DATA chest_offer.fallback_policy | PENDING | Product owner confirms U-04 |
| HUD/read model | AGENT_TASK §4 | UI can show HP, attack, crit, speed, cooldown, build, active artifact effects, pending three-card offer, XP, time, stage, kills, rewards | FLOW §9; ARCHITECTURE §8 | SPECIFIED | Runtime Iteration 2 |
| Pause | AGENT_TASK §4 | Manual pause freezes clock and preserves resume_state | STATE RUN_PAUSED/T-18/T-19; EVENT run_paused | SPECIFIED | Runtime Iteration 1 |
| Settings from pause | AGENT_TASK | Settings returns to exact blocking/resume context | FLOW §7; STATE pause model | SPECIFIED | Runtime Iteration 2 |
| Exit to menu | AGENT_TASK | Confirmation distinguishes cancel from abandon; no unearned rewards | FLOW §7; STATE T-22 | SPECIFIED | Runtime Iteration 2 |
| Android background/resume | GAME_MANIFEST; AGENT_TASK | Background forces pause; restore validates snapshot/checksum/content | ARCHITECTURE §6; EVENT run_resumed | SPECIFIED | Runtime Iteration 3 |
| Save boundary | GAME_MANIFEST; DECISIONS U-06/U-07 | Checkpoint/explicit pause/terminal snapshots are versioned and atomic; arbitrary frame not promised | DATA save_snapshot; ARCHITECTURE §6 | PENDING | Product/runtime owner confirms recovery policy |
| Death | GAME_MANIFEST; B1 | HP zero yields one terminal defeat result and allowed partial rewards | FLOW §8; STATE T-16; EVENT run_defeated | SPECIFIED | Runtime Iteration 2 |
| Victory | GAME_MANIFEST | Final victory requires final boss defeat and final settlement, not timer alone; final boss has no boss chest and first-clear artifact is separate | FLOW §8; STATE T-17/T-14F; invariant 6 | SPECIFIED | Runtime Iteration 2 |
| Result stats | AGENT_TASK | Result projection contains build, kills, XP, stats, checkpoints and reward status | FLOW §9; ARCHITECTURE §8 | SPECIFIED | Runtime Iteration 2 |
| Reward bundles | B1 §§7–9 | RewardCalculator reads deterministic bundles and separate wallets | DATA reward_bundles; ARCHITECTURE §5 | SPECIFIED | Runtime Iteration 2 |
| Checkpoint ledger | GAME_MANIFEST; B1 | 5/10/15/20 checkpoint reward settles once | STATE T-14/T-14F; EVENT checkpoint_reward_* | SPECIFIED | Runtime Iteration 2 |
| First clear/repeat/defeat | B1 §7 | Scopes are separate; defeat after checkpoint uses allowed partial path | FLOW §8; DATA reward ledger | SPECIFIED | Runtime Iteration 2 |
| Ledger idempotency | AGENT_TASK; GAME_MANIFEST | Duplicate checkpoint/boss-chest/artifact-offer/result commands return existing outcome without wallet mutation or duplicate effect | ARCHITECTURE §5; EVENT §2/§4 | SPECIFIED | Runtime Iteration 1 test then 2 |
| Save restore idempotency | AGENT_TASK | Restore cannot replay settled ledger entries | STATE T-19/T-21; DATA reward_ledger_ref | SPECIFIED | Runtime Iteration 2 |
| Diagnostics/fallback | GAME_MANIFEST; AGENT_CONTEXT | Missing resources produce code/path/severity/recovery, never blank screen | ARCHITECTURE §7; EVENT content_load_failed | SPECIFIED | Runtime Iteration 1 |
| Data-driven content | GAME_MANIFEST; AGENT_TASK | Registry owns content and version; UI does not encode invariants | ARCHITECTURE §4; DATA registry | SPECIFIED | Runtime Iteration 1/2 |
| Controlled spawn/pooling | GAME_MANIFEST; B1 | Enemy/projectile/XP/aftermath pools enforce cap and do not drop XP silently | ARCHITECTURE Simulation; DATA entity shapes | SPECIFIED | Runtime Iteration 2/3 |
| Performance | B1 §10; GAME_MANIFEST | Full wave has target/safe FPS evidence on Android | B1 acceptance targets; future runtime profiling | NOT_IMPLEMENTED | Runtime Iteration 3 |
| No unapproved assets | AGENTS; Visual Lab law | Architecture references IDs/manifests only; no asset promotion or runtime dependency added | Scope inspection and explicit non-goals | VERIFIED_BY_DOC_CHECK | Separate visual/runtime owners |
| Current prototype distinction | REPO_CONTEXT; live code | Menu/arena prototypes are adapters/evidence, not target runtime | ARCHITECTURE §3 and FLOW §10 | VERIFIED_BY_DOC_CHECK | Runtime migration review |
| JSON schema validity | DELIVERABLES; AGENT_TASK | Contract parses without comments/trailing comma | json validator after commit | VERIFIED_BY_DOC_CHECK | Architecture verification |
| Internal path validity | README; AGENT_TASK | Links point to existing repository paths or same-folder deliverables | repository path audit after commit | VERIFIED_BY_DOC_CHECK | Architecture verification |
| Scope boundary | README; AGENT_TASK; explicit product decision | Only the architecture package plus explicitly synchronized canonical/balance documents changed; no runtime/scenes/assets | changed-path inspection | VERIFIED_BY_DOC_CHECK | Architecture verification |

## 2. Status interpretation

- SPECIFIED — logical behavior and owner are described; runtime proof is not implied.
- VERIFIED_BY_DOC_CHECK — repository/document check directly verified the artifact or boundary.
- PENDING — exact product/B1 decision is intentionally open.
- NOT_IMPLEMENTED — runtime/Android evidence is absent and must be produced by a later slice.
- BLOCKED — use only for a concrete blocker that prevents the specified contract; no current row is marked BLOCKED solely because runtime is not yet implemented.

## 3. Required implementation gates

Before a runtime slice may claim completion:

1. read all six architecture deliverables;
2. implement only the slice scope;
3. add deterministic checks for duplicate effects and stale revisions;
4. run JSON/content validation against the contract;
5. record fresh evidence for the observable rows;
6. do not change pending decisions silently;
7. keep runtime changes outside this architecture folder and review them separately.