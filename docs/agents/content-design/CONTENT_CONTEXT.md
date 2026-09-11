# Content Context — Moonveil: Eclipse

Этот файл фиксирует, как Content Agent взаимодействует с балансом, архитектурой, runtime и Visual Lab. Он не является вторым источником истины для чисел или state machine.

## 1. Порядок доверия

1. явно принятое решение владельца проекта;
2. AGENTS.md, GAME_MANIFEST.md и AGENT_CONTEXT.md;
3. архитектурный пакет первого забега;
4. BALANCE_ECONOMY_SPEC.md и BALANCE_MODEL.json — для чисел;
5. Visual Lab production law — для визуального production pipeline;
6. фактический runtime и existing manifests;
7. content proposals и старые отчёты.

При конфликте Content Agent не выбирает молча. Он фиксирует конфликт, impact, owner и next action в handoff.

## 2. Факты текущего репозитория

- docs/mockups/04-enemies содержит уже существующий пакет enemy-контента и его визуальных контрактов; его нельзя заменять ради новых идей.
- docs/mockups/05-bosses, 06-weapons, 07-passives и 08-artifacts являются stage-направлениями; наличие README не доказывает, что полный production roster создан.
- docs/mockups/09-xp, 16-upgrade-offers, 17-artifact-ui и 19-synergy-info относятся к связанным визуальным и UX-поверхностям.
- Visual Lab — обязательный production-gate для visual, art, asset, UI-visual, animation и VFX задач.
- Balance Agent владеет числовым baseline, поэтому Content Agent описывает смысл и границы механики, а не окончательные коэффициенты.

## 3. Что именно создаёт Content Agent

Каждая content entry должна иметь:

- стабильный content_id;
- тип и stage/availability;
- короткую fantasy и player promise;
- визуальный silhouette/shape language;
- core mechanic и player decision;
- trigger, target, area или interaction в качественных терминах;
- failure/edge cases;
- VFX lifecycle и readable telegraph;
- audio/haptic hooks как timing intent;
- связи с weapon/passive/synergy/artifact/shop/drop системами;
- необходимые данные для HUD и tooltip;
- поля PENDING_BALANCE;
- asset brief для Visual Lab;
- consumers для Runtime;
- статус и next action.

Content Agent может использовать классы дальности close, mid, long, global или arena-wide. Точные метры, радиусы, скорости, damage, cooldown, duration, chance, frequency, quantity и prices назначает Balance Agent.

## 4. Правила по категориям

### Оружие

Оружие должно отличаться способом принятия решения и поведением атаки, а не только цветом и процентом урона.

Описываются:

- источник/оружие и его fantasy;
- target selection;
- attack pattern: projectile, beam, orbit, cone, zone, chain, dash-linked и другое;
- геометрия и качественный класс дальности;
- hit/pierce/bounce/return/persist behavior;
- telegraph, cast, travel, hit, persist и expire VFX;
- возможные evolution/synergy tags;
- trade-off и ситуации, где оружие слабее;
- animation/audio/haptic hooks.

Числовые поля остаются PENDING_BALANCE.

### Пассивные способности

Пассивка усиливает понятную ось билда, меняет решение игрока или открывает взаимодействие. Не создавать десятки копий «+X% к атаке» без отдельной причины.

Описываются:

- axis;
- trigger или always-on boundary;
- affected systems;
- stacking/duplicate intent;
- compatible weapons and synergies;
- UI explanation;
- visual/icon brief;
- balance questions.

### Артефакты

Артефакт — отдельный выразительный run modifier, не обычная passive slot entry и не pre-run equipment.

Допустимые effect families:

- AURA;
- DERIVED_STAT;
- TARGET_MODIFIER;
- WEAPON_MODIFIER;
- TRIGGERED_EFFECT;
- COOLDOWN_MODIFIER;
- другие типы только с описанием trigger, target и observable result.

Каждый артефакт должен иметь:

- особую механику, которую игрок замечает в бою;
- источник offer;
- три-card presentation contract;
- выбор одной карты;
- отсутствие weapon/passive slot consumption;
- conflict/duplicate/stacking вопросы;
- clear VFX/feedback;
- PENDING_BALANCE для значений, cadence, refresh и stacking.

Не превращать артефакт в неописанный flat passive.

### Магазин и постоянные пассивные улучшения

Content Agent создаёт fantasy веток, названия рангов, смысл долгосрочного выбора, UI copy и unlock relationships.

Balance Agent назначает:

- цену;
- величину эффекта;
- число рангов;
- валюту;
- caps и refund policy.

Runtime Agent реализует wallet mutation и persistence. Content Agent не меняет кошельки и не прячет цену в тексте.

### Противники

Первый забег и существующие enemy assets защищены. Новые противники проектируются прежде всего для следующих этапов или как explicit candidate replacement.

Каждый enemy должен иметь:

- роль в орде;
- silhouette и визуальный маркер;
- signature behavior;
- readable telegraph;
- movement/targeting intent;
- arena interaction;
- контр-решение игрока;
- drop semantics;
- VFX/audio/haptic hooks;
- числа PENDING_BALANCE.

Новый враг обязан менять решение игрока, а не только иметь больше HP.

### Боссы

Каждый новый boss должен иметь:

- fantasy и silhouette;
- arena relationship;
- intro;
- минимум одну различимую phase identity;
- telegraphed attacks;
- safe spawn и реакционное окно;
- movement/targeting rules;
- transition/enrage intent;
- defeat/readability contract;
- chest/reward boundary reference без прямого wallet mutation;
- VFX/audio/haptic timing hooks.

Boss design не должен писать собственные reward numbers или нарушать правило: final boss не создаёт boss chest.

### Выпадающие предметы арены

Каждый drop — отдельный pickup type, не маскированная награда за обычного врага.

Базовый пул для проектирования:

- heal pickup — восстанавливает HP;
- coin pickup — выдаёт определённую валюту после решения Balance;
- mana magnet — притягивает кристаллы XP/маны в пределах заданной механики;
- destruction crystal — уничтожает или поражает врагов вокруг;
- freeze crystal — замораживает обычные волны по определённому правилу;
- shield/ward pickup — временно предотвращает часть угрозы;
- vacuum/harvest pickup — собирает drops по арене;
- time/tempo pickup — меняет темп только если это согласовано с clock contract;
- новый proposal от Content Agent.

Для каждого предмета описать визуальный отличительный сигнал, pickup feedback, effect intent, target и ограничения. Balance Agent решает frequency, quantity, heal amount, duration, radius, chance и relation to economy. Runtime Agent решает фактическое применение effect.

## 5. Жизненный цикл статуса

- PROPOSAL — идея, ещё не готовая к передаче;
- CONTENT_SPECIFIED — механика и контентная спецификация полны;
- BALANCE_PENDING — content готов, числовой binding отсутствует;
- VISUAL_BRIEF_READY — brief готов для Visual Lab;
- RUNTIME_HANDOFF_READY — consumer contract готов;
- USER_REVIEW — требуется решение Creative Director или владельца;
- APPROVED — explicit approval получен;
- IMPLEMENTED — runtime подтвердил фактическое подключение;
- RETIRED — контент снят без удаления истории.

Нельзя объявлять PRODUCTION или PLAYABLE только по документу Content Agent.

## Актуальная граница состава

Сверка от main ec30c239aa22aa1d9c8ad1faab25d99633f4cb29: активный набор обычных противников — 10 записей из архитектурной карты; enemy_stone_oni и enemy_eclipse_serpent сохранены только для совместимости; enemy_silver_reed_seer и enemy_moontrail_stalker остаются будущими.

Пять мини-боссов и два расширения главных боссов имеют зависимости от C3, FIRST_RUN_DATA_CONTRACT, BALANCE_MODEL и runtime handoff. Зависимость не означает approval.

Статус: CONTENT_SCOPE_CLOSED; runtime, balance и visual gates остаются у владельцев.
