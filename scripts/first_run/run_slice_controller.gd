extends Node2D
class_name FirstRunSliceController

## First playable vertical slice.
## All visuals are procedural placeholders; no production assets are loaded.

const SESSION_SCRIPT = preload("res://scripts/first_run/run_session_stub.gd")

const VIEWPORT_SIZE := Vector2(390.0, 844.0)
const PLAYFIELD_RECT := Rect2(24.0, 116.0, 342.0, 690.0)
const PLAYER_RADIUS := 12.0

const STUB_TIME_SCALE := 10.0
const STUB_SPAWN_INTERVAL := 1.10
const STUB_ACTIVE_CAP := 12
const STUB_ENEMY_HP := 2
const STUB_ENEMY_SPEED := 38.0
const STUB_ENEMY_DAMAGE := 1
const STUB_ENEMY_HIT_COOLDOWN := 0.90
const STUB_PROJECTILE_SPEED := 220.0
const STUB_PROJECTILE_LIFETIME := 1.40
const STUB_XP_VALUE := 5
const STUB_XP_PICKUP_RADIUS := 24.0

const INK := Color("#07171b")
const WATER := Color("#0d3032")
const GRID := Color("#195052")
const JADE := Color("#a8fff0")
const JADE_DARK := Color("#3d9f99")
const MOON := Color("#f4ead2")
const CRIMSON := Color("#bc4c4f")
const XP_COLOR := Color("#d9a6ff")
const ENEMY_COLOR := Color("#d56b75")
const PROJECTILE_COLOR := Color("#ffe2a6")

var session
var rng := RandomNumberGenerator.new()
var player_position := VIEWPORT_SIZE * 0.5
var move_input := Vector2.ZERO
var touch_active := false
var touch_anchor := Vector2.ZERO
var spawn_timer := 0.0
var attack_timer := 0.0
var enemy_serial := 0

var enemies: Array[Dictionary] = []
var projectiles: Array[Dictionary] = []
var xp_drops: Array[Dictionary] = []

var hud_label: Label
var hint_label: Label
var pause_button: Button
var pause_panel: Control
var upgrade_panel: Control
var terminal_panel: Control
var upgrade_title: Label
var upgrade_buttons: Array[Button] = []


func _ready() -> void:
    process_mode = Node.PROCESS_MODE_ALWAYS
    rng.seed = 20260910
    session = SESSION_SCRIPT.new("lin_yue", 20260910)
    _build_hud()
    _refresh_hud()
    queue_redraw()


func _process(delta: float) -> void:
    if session.get_phase() == "RUN_ACTIVE":
        session.advance_time(delta * STUB_TIME_SCALE)
        _read_movement_input()
        _move_player(delta)
        _spawn_enemy(delta)
        _process_enemies(delta)
        _process_projectiles(delta)
        _process_xp_drops()
        _process_auto_attack(delta)

    _refresh_hud()
    queue_redraw()


func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventScreenTouch:
        if event.pressed:
            touch_active = true
            touch_anchor = event.position
            _update_touch_input(event.position)
        else:
            touch_active = false
            move_input = Vector2.ZERO
    elif event is InputEventScreenDrag and touch_active:
        _update_touch_input(event.position)
    elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
        if event.pressed:
            touch_active = true
            touch_anchor = event.position
            _update_touch_input(event.position)
        else:
            touch_active = false
            move_input = Vector2.ZERO
    elif event is InputEventMouseMotion and touch_active:
        _update_touch_input(event.position)


func _read_movement_input() -> void:
    var keyboard_input := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    if keyboard_input.length_squared() > 0.0:
        move_input = keyboard_input


func _update_touch_input(point: Vector2) -> void:
    if point.y < PLAYFIELD_RECT.position.y:
        return
    var delta := point - touch_anchor
    move_input = delta.limit_length(1.0)


func _move_player(delta: float) -> void:
    if move_input.length_squared() <= 0.001:
        return
    player_position += move_input * 96.0 * delta
    player_position.x = clampf(
        player_position.x,
        PLAYFIELD_RECT.position.x + PLAYER_RADIUS,
        PLAYFIELD_RECT.end.x - PLAYER_RADIUS
    )
    player_position.y = clampf(
        player_position.y,
        PLAYFIELD_RECT.position.y + PLAYER_RADIUS,
        PLAYFIELD_RECT.end.y - PLAYER_RADIUS
    )


func _spawn_enemy(delta: float) -> void:
    if enemies.size() >= STUB_ACTIVE_CAP:
        return

    spawn_timer += delta
    if spawn_timer < STUB_SPAWN_INTERVAL:
        return
    spawn_timer = 0.0

    var side := rng.randi_range(0, 3)
    var position := Vector2.ZERO
    match side:
        0:
            position = Vector2(
                rng.randf_range(PLAYFIELD_RECT.position.x, PLAYFIELD_RECT.end.x),
                PLAYFIELD_RECT.position.y - 18.0
            )
        1:
            position = Vector2(
                PLAYFIELD_RECT.end.x + 18.0,
                rng.randf_range(PLAYFIELD_RECT.position.y, PLAYFIELD_RECT.end.y)
            )
        2:
            position = Vector2(
                rng.randf_range(PLAYFIELD_RECT.position.x, PLAYFIELD_RECT.end.x),
                PLAYFIELD_RECT.end.y + 18.0
            )
        _:
            position = Vector2(
                PLAYFIELD_RECT.position.x - 18.0,
                rng.randf_range(PLAYFIELD_RECT.position.y, PLAYFIELD_RECT.end.y)
            )

    enemy_serial += 1
    enemies.append({
        "id": enemy_serial,
        "position": position,
        "hp": STUB_ENEMY_HP,
        "speed": STUB_ENEMY_SPEED,
        "hit_cooldown": 0.0,
        "radius": 10.0
    })


func _process_enemies(delta: float) -> void:
    for index in range(enemies.size() - 1, -1, -1):
        var enemy: Dictionary = enemies[index]
        var enemy_position: Vector2 = enemy["position"]
        var direction := player_position - enemy_position
        if direction.length_squared() > 0.01:
            enemy_position += direction.normalized() * float(enemy["speed"]) * delta
        enemy["position"] = enemy_position
        enemy["hit_cooldown"] = maxf(0.0, float(enemy["hit_cooldown"]) - delta)
        enemies[index] = enemy

        if enemy_position.distance_to(player_position) <= PLAYER_RADIUS + float(enemy["radius"]):
            if float(enemy["hit_cooldown"]) <= 0.0:
                var defeated := session.take_damage(STUB_ENEMY_DAMAGE)
                enemy["hit_cooldown"] = STUB_ENEMY_HIT_COOLDOWN
                enemies[index] = enemy
                if defeated:
                    _show_terminal("ПОРАЖЕНИЕ", "Заглушка: RunSession зафиксировал смерть.")
                    return


func _process_auto_attack(delta: float) -> void:
    if enemies.is_empty():
        return
    attack_timer -= delta
    if attack_timer > 0.0:
        return

    attack_timer = session.get_cooldown()
    var target_index := _nearest_enemy_index()
    if target_index < 0:
        return

    var target_position: Vector2 = enemies[target_index]["position"]
    var direction := (target_position - player_position).normalized()
    projectiles.append({
        "position": player_position,
        "velocity": direction * STUB_PROJECTILE_SPEED,
        "life": STUB_PROJECTILE_LIFETIME,
        "damage": session.get_attack()
    })


func _process_projectiles(delta: float) -> void:
    for projectile_index in range(projectiles.size() - 1, -1, -1):
        var projectile: Dictionary = projectiles[projectile_index]
        var projectile_position: Vector2 = projectile["position"]
        projectile_position += projectile["velocity"] * delta
        projectile["position"] = projectile_position
        projectile["life"] = float(projectile["life"]) - delta

        var hit_enemy := false
        for enemy_index in range(enemies.size() - 1, -1, -1):
            var enemy: Dictionary = enemies[enemy_index]
            if projectile_position.distance_to(enemy["position"]) > float(enemy["radius"]) + 4.0:
                continue

            enemy["hp"] = int(enemy["hp"]) - int(projectile["damage"])
            projectiles.remove_at(projectile_index)
            hit_enemy = true
            if int(enemy["hp"]) <= 0:
                _defeat_enemy(enemy_index)
            else:
                enemies[enemy_index] = enemy
            break

        if hit_enemy:
            continue
        if float(projectile["life"]) <= 0.0:
            projectiles.remove_at(projectile_index)
        else:
            projectiles[projectile_index] = projectile


func _defeat_enemy(enemy_index: int) -> void:
    if enemy_index < 0 or enemy_index >= enemies.size():
        return
    var enemy: Dictionary = enemies[enemy_index]
    enemies.remove_at(enemy_index)
    session.record_kill()
    xp_drops.append({
        "position": enemy["position"],
        "value": STUB_XP_VALUE
    })


func _process_xp_drops() -> void:
    for index in range(xp_drops.size() - 1, -1, -1):
        var drop: Dictionary = xp_drops[index]
        if player_position.distance_to(drop["position"]) > STUB_XP_PICKUP_RADIUS:
            continue

        xp_drops.remove_at(index)
        if session.collect_xp(int(drop["value"])):
            _open_upgrade_panel()
            return


func _nearest_enemy_index() -> int:
    var nearest_index := -1
    var nearest_distance := INF
    for index in range(enemies.size()):
        var distance := player_position.distance_squared_to(enemies[index]["position"])
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_index = index
    return nearest_index


func _build_hud() -> void:
    var canvas := CanvasLayer.new()
    canvas.name = "StubHud"
    canvas.layer = 10
    add_child(canvas)

    var root := Control.new()
    root.name = "Root"
    root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    canvas.add_child(root)

    hud_label = Label.new()
    hud_label.position = Vector2(12.0, 12.0)
    hud_label.size = Vector2(280.0, 82.0)
    hud_label.add_theme_font_size_override("font_size", 13)
    hud_label.add_theme_color_override("font_color", MOON)
    hud_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
    root.add_child(hud_label)

    hint_label = Label.new()
    hint_label.position = Vector2(24.0, 778.0)
    hint_label.size = Vector2(342.0, 42.0)
    hint_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    hint_label.add_theme_font_size_override("font_size", 11)
    hint_label.add_theme_color_override("font_color", Color("#b8d8d0"))
    hint_label.text = "DRAG / стрелки — движение  ·  автоатака  ·  STUB ×10"
    hint_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
    root.add_child(hint_label)

    pause_button = _make_button("ПАУЗА", Rect2(302.0, 14.0, 76.0, 38.0))
    pause_button.pressed.connect(_toggle_pause)
    root.add_child(pause_button)

    pause_panel = _make_overlay(root, "ПАУЗА")
    var resume_button := _make_button("ПРОДОЛЖИТЬ", Rect2(74.0, 380.0, 242.0, 52.0))
    resume_button.pressed.connect(_toggle_pause)
    pause_panel.add_child(resume_button)

    upgrade_panel = _make_overlay(root, "УЛУЧШЕНИЕ")
    upgrade_title = upgrade_panel.get_node("Title")
    for index in range(3):
        var button := _make_button("", Rect2(48.0, 300.0 + float(index) * 82.0, 294.0, 64.0))
        var choice_index := index
        button.pressed.connect(_choose_upgrade.bind(choice_index))
        upgrade_buttons.append(button)
        upgrade_panel.add_child(button)

    terminal_panel = _make_overlay(root, "ЗАБЕГ ОКОНЧЕН")
    var retry_button := _make_button("ПОВТОРИТЬ", Rect2(74.0, 380.0, 242.0, 52.0))
    retry_button.pressed.connect(_restart_stub)
    terminal_panel.add_child(retry_button)
    var menu_button := _make_button("В МЕНЮ", Rect2(74.0, 448.0, 242.0, 52.0))
    menu_button.pressed.connect(_return_to_menu)
    terminal_panel.add_child(menu_button)

    pause_panel.visible = false
    upgrade_panel.visible = false
    terminal_panel.visible = false


func _make_overlay(parent: Control, title: String) -> Control:
    var overlay := Control.new()
    overlay.name = title if title != "УЛУЧШЕНИЕ" else "UpgradeOverlay"
    overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    overlay.mouse_filter = Control.MOUSE_FILTER_STOP
    parent.add_child(overlay)

    var shade := ColorRect.new()
    shade.color = Color("#061416dd")
    shade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    shade.mouse_filter = Control.MOUSE_FILTER_IGNORE
    overlay.add_child(shade)

    var panel := Panel.new()
    panel.position = Vector2(24.0, 238.0)
    panel.size = Vector2(342.0, 352.0)
    panel.add_theme_stylebox_override("panel", _panel_style())
    panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
    overlay.add_child(panel)

    var label := Label.new()
    label.name = "Title"
    label.position = Vector2(34.0, 266.0)
    label.size = Vector2(322.0, 46.0)
    label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    label.add_theme_font_size_override("font_size", 22)
    label.add_theme_color_override("font_color", JADE)
    label.text = title
    label.mouse_filter = Control.MOUSE_FILTER_IGNORE
    overlay.add_child(label)

    return overlay


func _make_button(value: String, rect: Rect2) -> Button:
    var button := Button.new()
    button.text = value
    button.position = rect.position
    button.size = rect.size
    button.add_theme_font_size_override("font_size", 14)
    button.add_theme_color_override("font_color", MOON)
    button.add_theme_color_override("font_hover_color", INK)
    button.add_theme_stylebox_override("normal", _button_style(Color("#0b2426ee"), JADE_DARK))
    button.add_theme_stylebox_override("hover", _button_style(Color("#a8fff0"), MOON))
    button.add_theme_stylebox_override("pressed", _button_style(Color("#7bd6c9"), MOON))
    return button


func _button_style(background: Color, border: Color) -> StyleBoxFlat:
    var style := StyleBoxFlat.new()
    style.bg_color = background
    style.border_color = border
    style.border_width_left = 1
    style.border_width_top = 1
    style.border_width_right = 1
    style.border_width_bottom = 1
    style.corner_radius_top_left = 12
    style.corner_radius_top_right = 12
    style.corner_radius_bottom_left = 12
    style.corner_radius_bottom_right = 12
    return style


func _panel_style() -> StyleBoxFlat:
    return _button_style(Color("#0b2426f2"), JADE_DARK)


func _toggle_pause() -> void:
    if session.get_phase() == "RUN_ACTIVE":
        session.pause()
        pause_panel.visible = true
    elif session.get_phase() == "PAUSED":
        session.resume()
        pause_panel.visible = false
    _refresh_hud()


func _open_upgrade_panel() -> void:
    var definitions: Array[Dictionary] = session.get_upgrade_definitions()
    for index in range(upgrade_buttons.size()):
        var definition: Dictionary = definitions[index]
        upgrade_buttons[index].text = "%s\n%s" % [definition["title"], definition["description"]]
    upgrade_panel.visible = true
    pause_button.visible = false
    upgrade_title.text = "УРОВЕНЬ %d" % int(session.get_state()["level"])
    _refresh_hud()


func _choose_upgrade(index: int) -> void:
    var result: Dictionary = session.choose_upgrade(index)
    if not bool(result["accepted"]):
        return
    upgrade_panel.visible = false
    pause_button.visible = true
    _refresh_hud()


func _show_terminal(title: String, detail: String) -> void:
    terminal_panel.visible = true
    pause_button.visible = false
    var title_label: Label = terminal_panel.get_node("Title")
    title_label.text = title
    var detail_label := Label.new()
    detail_label.position = Vector2(42.0, 320.0)
    detail_label.size = Vector2(306.0, 48.0)
    detail_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    detail_label.add_theme_font_size_override("font_size", 12)
    detail_label.add_theme_color_override("font_color", MOON)
    detail_label.text = detail
    detail_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
    terminal_panel.add_child(detail_label)


func _restart_stub() -> void:
    get_tree().reload_current_scene()


func _return_to_menu() -> void:
    get_tree().change_scene_to_file("res://scenes/menu/menu.tscn")


func _refresh_hud() -> void:
    if not hud_label or not session:
        return
    var state: Dictionary = session.get_state()
    var band: Dictionary = session.get_wave_band()
    var total_seconds := int(float(state["elapsed_seconds"]))
    var minutes := total_seconds / 60
    var seconds := total_seconds % 60
    hud_label.text = (
        "ЗАБЕГ  %02d:%02d   %s\nHP %d/%d   LV %d   XP %d/%d\n"
        + "УБИЙСТВА %d   ATK %d   CD %.2fs"
    ) % [
        minutes,
        seconds,
        band["id"],
        int(state["hp"]),
        int(state["max_hp"]),
        int(state["level"]),
        int(state["xp_current"]),
        session.get_xp_to_next(),
        int(state["kills"]),
        session.get_attack(),
        session.get_cooldown()
    ]

    if state["phase"] == "DEFEAT":
        hint_label.text = "ЗАБЕГ ОКОНЧЕН  ·  заглушка результата"
    elif state["phase"] == "UPGRADE_CHOICE":
        hint_label.text = "ВЫБЕРИТЕ ОДНО ИЗ ТРЁХ УЛУЧШЕНИЙ"
    elif state["phase"] == "PAUSED":
        hint_label.text = "ПАУЗА  ·  симуляция и часы остановлены"
    else:
        hint_label.text = "DRAG / стрелки — движение  ·  автоатака  ·  STUB ×10"


func _draw() -> void:
    draw_rect(Rect2(Vector2.ZERO, VIEWPORT_SIZE), INK)
    draw_rect(PLAYFIELD_RECT, WATER)

    for x in range(24, 367, 48):
        draw_line(Vector2(x, 116), Vector2(x, 806), Color(GRID, 0.42), 1.0)
    for y in range(116, 807, 48):
        draw_line(Vector2(24, y), Vector2(366, y), Color(GRID, 0.42), 1.0)

    draw_circle(Vector2(82.0, 214.0), 28.0, Color("#19505288"))
    draw_circle(Vector2(302.0, 684.0), 40.0, Color("#19505288"))
    draw_arc(Vector2(82.0, 214.0), 28.0, 0.0, TAU, 32, Color(JADE, 0.35), 1.0)
    draw_arc(Vector2(302.0, 684.0), 40.0, 0.0, TAU, 32, Color(JADE, 0.28), 1.0)

    for drop in xp_drops:
        var point: Vector2 = drop["position"]
        var diamond := PackedVector2Array([
            point + Vector2(0.0, -6.0),
            point + Vector2(6.0, 0.0),
            point + Vector2(0.0, 6.0),
            point + Vector2(-6.0, 0.0)
        ])
        draw_colored_polygon(diamond, XP_COLOR)
        draw_circle(point, 2.0, MOON)

    for projectile in projectiles:
        draw_circle(projectile["position"], 4.0, PROJECTILE_COLOR)
        draw_line(
            projectile["position"],
            projectile["position"] - projectile["velocity"].normalized() * 8.0,
            Color(PROJECTILE_COLOR, 0.45),
            2.0
        )

    for enemy in enemies:
        var enemy_position: Vector2 = enemy["position"]
        draw_circle(enemy_position, float(enemy["radius"]), ENEMY_COLOR)
        draw_circle(enemy_position, 4.0, INK)
        draw_arc(enemy_position, float(enemy["radius"]) + 3.0, 0.0, TAU, 20, Color(CRIMSON, 0.55), 1.0)

    var player_points := PackedVector2Array([
        player_position + Vector2(0.0, -PLAYER_RADIUS),
        player_position + Vector2(PLAYER_RADIUS, 0.0),
        player_position + Vector2(0.0, PLAYER_RADIUS),
        player_position + Vector2(-PLAYER_RADIUS, 0.0)
    ])
    draw_colored_polygon(player_points, JADE)
    draw_circle(player_position, 5.0, INK)
    draw_arc(player_position, PLAYER_RADIUS + 5.0, 0.0, TAU, 24, Color(MOON, 0.68), 1.2)
