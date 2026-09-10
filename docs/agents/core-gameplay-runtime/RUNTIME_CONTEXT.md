# Runtime Context — первый игровой забег

Этот файл — рабочая карта связей между архитектурой, балансом и runtime. Он не заменяет канонические документы. Если источник изменился, агент использует живой источник и фиксирует новый HEAD в отчёте.

## 1. Иерархия источников

При конфликте используется следующий порядок:

1. явно принятое решение владельца проекта;
2. AGENTS.md и root-контекст проекта;
3. docs/architecture/first-run/;
4. docs/BALANCE_ECONOMY_SPEC.md и docs/agents/balance-economy/BALANCE_MODEL.json для чисел;
5. фактический runtime-код и тесты;
6. вспомогательные README и старые отчёты.

Конфликт не исправляется молча. Агент записывает source, impact, temporary handling, owner и next action в handoff.

## 2. Обязательные доменные владельцы

| Компонент | Единственная ответственность | Не должен делать |
|---|---|---|
| ContentLoader / Content Registry | Загрузить, провалидировать и заморозить версионированные data records на run | Читать числа из UI или случайных controller constants |
| RunCoordinator | Проверить команды, вызвать доменного владельца, провести transition и корреляцию | Считать DPS, рисовать UI, напрямую менять wallet |
| RunSession | Authoritative state активного забега: state, clocks, stage, build, stats, drops, offers, diagnostics | Ссылаться на UI nodes, textures, scene paths или network services |
| SimulationClock | Согласованно вести run-clock и encounter-clock, применять freeze policy | Самостоятельно решать награды или переходы |
| WaveDirector | Выбирать B1 wave band, spawn budget, active cap и обычный spawn lifecycle | Менять wallet или скрыто масштабировать HP каждую секунду |
| BossDirector | Создать безопасное boss encounter, telegraph, phases и defeat fact | Создавать награды напрямую |
| CombatSystem | Урон, HP, hit cooldown, invulnerability, telegraph и combat facts | Выдавать валюту или управлять UI |
| ProgressionSystem | XP, level threshold, upgrade offer и collection | Менять persistent wallet |
| BuildInventory | Weapon/passive slots, levels, evolution eligibility | Владеть artifact capacity или artifact effects |
| SynergyEvaluator / BossChestSystem | Нефинальный boss-chest: synergy/evolution/fallback и claim guard | Открывать artifact offer или final chest |
| ArtifactOfferSystem | Three-card artifact source offer, refresh boundary и выбор одной карты | Занимать weapon/passive slots или создавать boss chest |
| ArtifactEffectSystem | Typed run-modifier effects и их trigger/target/stacking evaluation | Сводить артефакт к безымянному flat passive |
| RewardCalculator / RewardLedger | Детерминированный результат, checkpoint settlement, wallet/unlock transaction и idempotency | Раздавать награды при каждом повторном event |
| PersistenceGateway | Atomic snapshot, checksum, schema/content version и recovery | Продолжать run из непроверенного snapshot |
| Projections / UI adapters | Показывать authoritative state и отправлять commands | Быть источником времени, HP, build или rewards |

## 3. Обязательный жизненный цикл

Минимальный поток:

boot → content loading → menu → character select → run setup → run loading → run active → waves/combat/XP → upgrade offer → run active → boss intro → boss active → checkpoint settlement → non-final chest или final victory → next stage либо result → result review → rewards/unlocks → menu.

Все переходы проходят через RunCoordinator и должны иметь guard, owner, side effects, failure/recovery и duplicate policy согласно FIRST_RUN_STATE_MACHINE.md.

## 4. Часы и боссы

Принятое правило владельца проекта:

- на каждом боссе, без исключений, отображаемое время забега останавливается;
- на BOSS_INTRO, BOSS_ACTIVE и CHECKPOINT_SETTLEMENT обычные wave, XP и spawn clocks не продвигаются;
- внутренний encounter clock босса может продвигаться только пока фактически идёт BOSS_ACTIVE;
- ручная пауза и Android background/resume замораживают все игровые часы;
- после claim сундука промежуточного босса обычный run продолжается с того же времени;
- после финального босса забег переходит в settlement/victory и не создаёт boss chest;
- таймер сам по себе не является победой: победа требует defeat финального босса и успешного final settlement.

Freeze policy должна быть видна в коде, тестах и trace. Нельзя заморозить только HUD, оставив waves или rewards продвигаться в фоне.

## 5. Волны, XP и drops

Числа берутся из B1/BALANCE_MODEL через Content Registry. Для первого среза допустим минимальный fixture, но он обязан иметь тот же контракт.

Разделены:

- XPDrop и XP collection;
- chest offer;
- artifact offer;
- corpse/aftermath;
- combat fact;
- reward ledger entry.

XP не начисляется дважды при повторной доставке pickup event. Persistent aftermath не считается XP, не блокирует путь и не входит в active enemy cap.

WaveDirector должен поддерживать полосы 0–2, 2–5, 5–10, 10–15 и 15–20 минут, active cap и spawn budget. Скрытое непрерывное увеличение HP вместо объяснимой смены состава запрещено.

## 6. Артефакты и сундуки

Артефакты — не три экипируемых слота и не обычные пассивки вида «+10% к атаке».

Контракт:

- фиксированного artifact slot cap нет;
- pre-run artifact loadout отсутствует;
- артефакт не расходует weapon/passive slot;
- каждый источник предлагает ровно три карточки;
- игрок выбирает одну карточку;
- выбранная карта создаёт один artifact instance и активный typed run effect;
- эффект может быть AURA, DERIVED_STAT, TARGET_MODIFIER, WEAPON_MODIFIER, TRIGGERED_EFFECT или COOLDOWN_MODIFIER;
- количество активных артефактов ограничивается не количеством сунчков, а явной политикой производительности, stacking и duplicate, если такая политика будет принята;
- elite pack между боссами может открыть отдельный ARTIFACT_OFFER;
- first-clear reward открывает отдельный post-result ARTIFACT_OFFER;
- boss chest никогда не превращается в artifact offer;
- нефинальный boss chest даёт synergy/evolution или fallback;
- финальный босс не создаёт boss chest.

Точные effect values, refresh cost/limit, duplicate/stacking policy и elite-pack cadence остаются pending, если их нет в живом каноне. Runtime обязан хранить typed contract и не подменять неизвестное число догадкой.

## 7. Идемпотентность

Для повторяемых команд и событий используются stable IDs и idempotency keys:

- run_id;
- state_revision;
- checkpoint_id;
- boss_encounter_id;
- chest_offer_id;
- artifact_offer_id;
- artifact_instance_id;
- offer_id;
- result_id;
- reward ledger key.

Повторная доставка не должна:

- создать второй RunSession;
- начислить XP повторно;
- открыть второй chest/artifact offer;
- списать refresh дважды;
- создать второй artifact instance;
- провести checkpoint или wallet settlement дважды;
- превратить final boss в boss chest.

Ожидаемое поведение duplicate — вернуть сохранённый outcome или безопасный no-op, а не молча повторить mutation.

## 8. Детерминизм

Каждый trace фиксирует:

- seed;
- content_version;
- выбранного персонажа;
- стартовый профиль;
- команды игрока или policy;
- события и revisions;
- wave band;
- boss boundaries;
- XP/level/kills;
- build и active artifact instances;
- ledger outcomes;
- terminal result.

Одинаковые seed и входы должны давать одинаковые доменные результаты. Если визуальная или физическая часть недетерминирована, она не должна менять reward, eligibility или terminal outcome без зафиксированного правила.
