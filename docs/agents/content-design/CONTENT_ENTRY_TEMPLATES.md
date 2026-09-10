# Content Entry Templates

Все content entries создаются в этой папке до передачи другим владельцам. Поля с числовыми значениями без канонического источника указываются как PENDING_BALANCE.

## 1. Общий заголовок entry

~~~yaml
content_id: pending_or_stable_id
content_type: weapon | passive | artifact | shop_upgrade | enemy | boss | arena_drop
stage: first_run_reference | future_stage | proposal
status: PROPOSAL
source_refs:
  - repository/path
owner: content-design
balance_owner: balance-economy
runtime_consumer: pending
visual_route: UI_ART | SPRITE | ART | MOCKUP | VFX
asset_id: pending
family_id: pending
open_decisions:
  - question
next_action: pending
~~~

## 2. Weapon

~~~yaml
content_id: weapon_example
name_ru: Название
fantasy: Одно предложение о том, что игрок чувствует
player_promise: Почему это оружие хочется выбрать
progression:
  max_level: 10
role: control | burst | sustain | defense | mobility | area | utility
targeting:
  acquisition: nearest | cone | line | random | area | self | marked_target
  qualitative_range: close | mid | long | global
  geometry: projectile | beam | cone | orbit | zone | chain | dash
  behavior:
    travel: direct | homing | boomerang | stationary | delayed
    hit: pierce | bounce | split | pull | knockback | mark | persist
decision_and_counterplay:
  strength:
  weakness:
  best_when:
  bad_when:
vfx:
  cast:
  travel:
  hit:
  persistent:
  expire:
  readability:
audio_haptic_hooks:
  cast:
  hit:
  cooldown_ready:
synergy_tags: []
evolution_tags: []
balance_fields_pending:
  - base_damage
  - attacks_per_second
  - cooldown
  - exact_range
  - projectile_count
  - duration
runtime_contract:
  events:
  data_fields:
visual_brief:
  silhouette:
  palette:
  motion_language:
  forbidden_drift:
~~~

## 3. Passive ability

~~~yaml
content_id: passive_example
name_ru: Название
fantasy:
player_promise:
progression:
  max_rank: 10
  synergy_gate: paired_weapon_level_10_and_passive_rank_10
axis: offense | defense | mobility | economy | pickup | crit | status | summon | hybrid
activation: always_on | on_hit | on_kill | on_pickup | threshold | timed_window
affected_systems: []
mechanic:
decision_and_tradeoff:
stacking_intent: pending_balance
compatible_content:
  weapons: []
  synergies: []
ui_copy:
  short:
  detail:
visual_brief:
  icon:
  color_language:
  feedback:
balance_fields_pending:
  - magnitude
  - cap
  - trigger_chance
  - duration
runtime_contract:
  stats_or_events:
~~~

## 4. Artifact

~~~yaml
content_id: artifact_example
name_ru: Название
rarity: proposal
fantasy:
player_promise:
effect_family: AURA | DERIVED_STAT | TARGET_MODIFIER | WEAPON_MODIFIER | TRIGGERED_EFFECT | COOLDOWN_MODIFIER
trigger:
target:
observable_effect:
source: ELITE_PACK | FIRST_CLEAR_REWARD
offer_contract:
  cards_per_offer: 3
  selected_cards: 1
  consumes_weapon_slot: false
  consumes_passive_slot: false
  pre_run_loadout: false
  capacity: UNBOUNDED_WITHIN_RUN
vfx_feedback:
audio_haptic_hooks:
duplicate_and_stacking_intent: pending_balance_or_product
balance_fields_pending:
  - effect_value
  - trigger_frequency
  - refresh_cost
  - refresh_limit
  - duplicate_policy
runtime_contract:
  effect_payload:
  events:
visual_brief:
  silhouette:
  effect_language:
  gameplay_scale_readability:
~~~

## 5. Shop upgrade

~~~yaml
content_id: shop_upgrade_example
name_ru: Название ветки
fantasy:
player_promise:
wallet: GOLD
upgrade_axis:
rank_loop:
  display:
  unlock:
  reset_or_refund: pending_product
effect_description:
price_fields_pending:
  - rank_cost
  - rank_cap
  - effect_magnitude
persistence_contract:
ui_copy:
visual_brief:
~~~

## 6. Enemy

~~~yaml
content_id: enemy_example
name_ru: Название
stage: future_stage
role: rusher | ranged | flanker | blocker | support | elite | swarm
silhouette:
signature_behavior:
player_read:
  telegraph:
  warning_time: PENDING_BALANCE
  counter_decision:
movement_and_targeting:
arena_interaction:
death_and_drop_semantics:
vfx:
audio_haptic_hooks:
balance_fields_pending:
  - hp
  - damage
  - speed
  - spawn_weight
  - active_cap_cost
runtime_contract:
visual_brief:
  master:
  variants:
  forbidden_drift:
~~~

## 7. Boss

~~~yaml
content_id: boss_example
name_ru: Название
stage:
fantasy:
silhouette:
arena_relationship:
intro:
phases:
  - phase_id:
    identity:
    attacks:
    telegraphs:
    counterplay:
    transition:
safe_spawn:
reaction_window: PENDING_BALANCE
enrage_intent:
defeat_readability:
reward_boundary:
  non_final_chest: synergy_evolution_or_fallback
  final_boss_chest: forbidden
vfx:
  intro:
  phase_change:
  attacks:
  damage:
  defeat:
audio_haptic_hooks:
balance_fields_pending:
  - hp
  - damage
  - phase_threshold
  - attack_cooldown
  - reward_values
runtime_contract:
~~~

## 8. Arena drop

~~~yaml
content_id: drop_example
name_ru: Название
drop_type: HEAL | CURRENCY | XP_MAGNET | DESTRUCTION | WAVE_FREEZE | SHIELD | VACUUM | OTHER
player_promise:
visual_signal:
pickup_rule:
effect_intent:
target:
limitations_and_counterplay:
feedback:
  vfx:
  audio:
  haptic:
balance_fields_pending:
  - drop_frequency
  - amount
  - duration
  - radius
  - chance
  - eligible_sources
wallet_or_progression_boundary:
runtime_contract:
~~~

## 9. Quality rules

- Не заполняй PENDING_BALANCE догадкой.
- Не используй один и тот же content_id для разных механик.
- Не называй flat stat bonus artifact, если у него нет отдельного trigger/target/observable behavior.
- Любой VFX должен иметь trigger и readability purpose.
- Любой enemy/boss должен иметь player counter-decision.
- Любой drop должен иметь ограничение, чтобы Balance Agent мог определить power budget.
