# Moonveil: Eclipse — Asset Pipeline Code

Статус: CANONICAL PROJECT ASSET-PRODUCTION LAW.

Этот документ определяет, как визуальные assets планируются, создаются, проверяются, переиспользуются и подключаются во всей игре. Цель — не собирать Moonveil из несвязанных одноразовых PNG.

## 1. Prime rule

Не строить игру как серию one-off images.

Канонический порядок:

FULL-GAME ASSET CENSUS -> VISUAL FAMILY -> MASTER TEMPLATE -> VALIDATED VARIANT KIT -> NAMED/UNIQUE VARIANT -> ANIMATION/VFX PACKAGE -> RUNTIME MANIFEST -> SCENE/UI PLACEMENT

Scene или экран может запросить asset, но не владеет его visual law.

## 2. Full-game census до mass production

До массового производства поддерживается инвентарь потребностей всей игры:

- героини, portrait/full-body/combat representations;
- обычные и элитные враги;
- боссы и уникальные creatures;
- environment/location/material families;
- props, water, plants, lights, ruins, bridges, hazards и interactables;
- weapons, passive skills, artifacts, XP и reward icons;
- UI panels, buttons, states, typography/icon families;
- spell, attack, hit, death, status, telegraph и ambient VFX;
- loading, victory, defeat и result presentation;
- animation/cutscene-specific assets;
- mobile and accessibility variants.

Census нужен, чтобы повторяющаяся family проектировалась один раз и затем применялась в разных этапах.

## 3. Production hierarchy

### Level 1 — Global visual laws

README.md, GAME_MANIFEST.md, AGENT_CONTEXT.md, Visual Lab law и утверждённые global palette/scale/typography rules.

### Level 2 — Visual family

Примеры: Moonveil heroine family, enemy melee family, enemy ranged family, boss family, lotus-garden environment family, jade/ember/frost VFX family, menu panel family.

Family определяет morphology или geometry, material language, palette, scale, animation compatibility и attachment conventions.

### Level 3 — Master template / role template

Примеры: Lin Yue combat master, Seoyeon Han combat master, small melee enemy, ranged enemy, elite caster, boss body, lotus pond prop, HUD card, reward icon.

Template определяет production standard, а не конкретный named asset.

### Level 4 — Named/unique variant

Named asset наследует family/template и добавляет identity-bearing traits: лицо, волосы, костюм, оружие, rank, scars, palette deviation, unique VFX или animation mannerism.

### Level 5 — Scene/runtime instance

Runtime применяет текущие state: pose, animation frame, equipment, damage/status, VFX, lighting, target/selection и локальный context. Scene не меняет permanent identity или master law.

## 4. Master template contract

Каждый reusable character, enemy, boss, prop, UI или VFX template фиксирует, где применимо:

- canonical camera angle и viewport;
- base pose или base geometry;
- silhouette envelope;
- proportions/mass;
- grid/world footprint или UI bounds;
- target runtime scale;
- identity/readability anchors;
- layer/attachment zones;
- weapon/shield/effect origin points;
- contact shadow convention;
- palette/material family;
- allowed variant dimensions;
- required idle/move/attack/ability/hit/death states;
- forbidden intersections/clipping;
- export naming and manifest IDs;
- accepted fallback, если runtime asset временно недоступен.

Template считается пригодным только после проверки hero master и хотя бы одного representative variant.

## 5. Tactical/gameplay scale first

Красивый portrait или splash image не становится боевым asset автоматически.

World/battle asset проверяется на actual gameplay scale:

- silhouette читается на representative arena;
- head/upper body и role различимы;
- weapon, shield, projectile/effect origin читаемы;
- feet/ground contact ясны;
- крупные garments, wings, tails и weapons не создают ложный footprint;
- transparent edges и pixel density чистые;
- asset не выглядит как вставленный portrait;
- сохраняется идентичность при downscale.

UI asset проверяется в настоящем viewport 390x844 и на безопасной зоне, а не только в увеличенном макете.

## 6. Anatomy, equipment и layout collision tests

Каждый family/template pass проверяет подходящие риски:

- руки, grip и continuity weapon;
- left/right consistency;
- shield, bow, staff, blade и attachment origin;
- hair/ears/horns/limbs intersections;
- duplicated/missing limbs;
- armor/robe/cape clipping;
- feet/contact shadow;
- creature limb/wing/eye/head count;
- UI text overflow, overlap, clipped icon, unsafe touch target;
- VFX origin, telegraph bounds, damage text readability;
- mobile safe-area and z-order.

Если один дефект повторяется в нескольких variants, исправляется источник: family, template, prompt, export rule или validation test.

## 7. Fix upstream

Повторяющийся дефект — pipeline defect.

Примеры:

- weapons теряются в масштабе -> repair weapon readability/template;
- героини выглядят как разные IP -> repair heroine family/reference profile;
- вода, лужи и растения меняют стиль по stage -> repair environment family;
- VFX перекрывает героиню или телеграф -> repair effect envelope and z-order;
- UI cards не выдерживают русский текст -> repair typography/layout template;
- enemy variants выглядят одинаково -> repair role silhouette and material hierarchy.

Локальный патч допустим только для действительно уникального дефекта и не должен скрывать общий источник проблемы.

## 8. Named asset inheritance

Профиль named asset хранит:

- stable identity ID;
- source/reference notes;
- inherited family/template IDs;
- face/head/hair and body traits;
- clothing/armor/equipment;
- palette and material deviations;
- portrait identity;
- world/combat identity;
- unique VFX/animation notes;
- candidate/master/approval links.

Так сохраняется индивидуальность без повторного изобретения всей visual language.

## 9. Variant and animation rule

После hero-master approval создаются только совместимые variants. Направления, locomotion и combat states не являются независимыми картинками.

Каждая derived family сохраняет:

- apparent height и body mass;
- pivot/anchor semantics;
- palette/material hierarchy;
- camera/scale;
- collision-free visual bounds;
- state naming;
- stable asset IDs.

Animation и VFX представляют уже определённые игровые события. Они не меняют gameplay rules и не маскируют отсутствующий state.

## 10. Runtime manifest

Перед production promotion каждый asset получает manifest entry с минимумом:

- asset_id и family_id;
- source/editable path;
- runtime export path;
- dimensions, scale, pivot и anchors;
- state/direction semantics;
- hashes и producing commit;
- provenance reference;
- approval status;
- fallback status;
- consumer scene/UI.

Manifest не может помечать candidate как production только по факту существования файла.


## 10A. Binary delivery boundary

Visual Lab governs provenance, technical status, artistic review and promotion. It
does not require GitHub to store binary payloads. Runtime exports are transported
as exact ZIP objects through private Supabase Storage; GitHub keeps the text
manifest, checksum, request and CI code.

The Storage manifest records bucket/object, byte size, SHA-256, archive member
count and producing evidence. CI verifies those fields before importing. Upload
success is not artistic approval, and import success is not APPROVED GOLDEN or
PRODUCTION. If the binary channel is unavailable, the status is
BLOCKED_BINARY_ARTIFACT; no PNG or ZIP is pasted into chat or reconstructed
from text.

## 11. Stage integration

Stage-папка отвечает за композицию и конкретный пользовательский сценарий. Visual Lab отвечает за производственную дисциплину. Для каждого stage:

1. stage document перечисляет потребность и canonical context;
2. family/template задаёт reusable identity;
3. candidate pack проходит technical QA;
4. Creative Director принимает или отклоняет визуал;
5. manifest связывает approved output с runtime;
6. только после этого сцена/UI получает production asset.

## 12. Acceptance

Asset family готова к следующему уровню только когда:

- существует census/profile и stable IDs;
- hero master явно reviewed;
- representative variant проверен в target scale;
- provenance/editable source сохранены, где возможно;
- collision/readability/layout checks пройдены;
- review pack показывает exact candidate;
- approval status не спутан с technical status;
- runtime manifest и consumer stage связаны;
- нет повторяющегося дефекта, который оставлен на уровне отдельных patch-ов.

Название папки, список ассетов, generated preview или README без exact evidence не являются готовностью.
