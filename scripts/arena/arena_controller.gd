extends Node2D
## Stage 02 arena proof-of-concept.
##
## The background is a fixed art-direction reference. The independent ambient,
## ripple, plant, particle and aftermath layers are driven here so the scene can
## be tested without waiting for a full 20-minute gameplay implementation.

const VIEWPORT_SIZE := Vector2(390.0, 844.0)
const ART_PATH := "res://docs/mockups/02-arena/layers/STAGE02_ARENA_ART_v01.png"
const AMBIENT_PATH := "res://docs/mockups/02-arena/layers/STAGE02_ARENA_AMBIENT_VFX_v01.png"
const PREVIEW_DURATION_SECONDS := 60.0

const INK := Color("#241A25")
const INK_SOFT := Color("#4A2631")
const BONE := Color("#D1C2A2")
const RIPPLE := Color("#A8FFF0")
const PLANT := Color("#9EE8D2")
const DUST := Color("#D8FFF3")
const MOON := Color("#F4EAD2")

@export var preview_mode := true
@export var show_preview_overlay := true

var elapsed_real_seconds := 0.0
var run_minutes := 0.0
var impact_events: Array[Dictionary] = []
var preview_label: Label

var ripple_centers := [
    Vector2(52, 178),
    Vector2(322, 329),
    Vector2(82, 671),
    Vector2(306, 735)
]

var plant_markers := [
    Vector2(34, 205), Vector2(70, 232), Vector2(343, 285), Vector2(361, 303),
    Vector2(30, 506), Vector2(64, 530), Vector2(326, 550), Vector2(356, 566),
    Vector2(40, 716), Vector2(84, 741), Vector2(312, 744), Vector2(354, 760)
]

var aftermath_markers := [
    {"center": Vector2(30, 150), "angle": -0.31, "length": 27.0},
    {"center": Vector2(68, 260), "angle": 0.42, "length": 30.0},
    {"center": Vector2(31, 389), "angle": -0.22, "length": 25.0},
    {"center": Vector2(77, 474), "angle": 0.30, "length": 31.0},
    {"center": Vector2(34, 588), "angle": -0.49, "length": 28.0},
    {"center": Vector2(74, 739), "angle": 0.24, "length": 32.0},
    {"center": Vector2(351, 132), "angle": 0.36, "length": 30.0},
    {"center": Vector2(322, 240), "angle": -0.35, "length": 26.0},
    {"center": Vector2(356, 374), "angle": 0.23, "length": 32.0},
    {"center": Vector2(317, 481), "angle": -0.42, "length": 29.0},
    {"center": Vector2(356, 575), "angle": 0.44, "length": 27.0},
    {"center": Vector2(310, 698), "angle": -0.23, "length": 32.0},
    {"center": Vector2(352, 790), "angle": 0.33, "length": 30.0},
    {"center": Vector2(103, 314), "angle": -0.14, "length": 18.0},
    {"center": Vector2(284, 416), "angle": 0.21, "length": 19.0},
    {"center": Vector2(112, 646), "angle": 0.37, "length": 20.0},
    {"center": Vector2(274, 625), "angle": -0.29, "length": 20.0},
    {"center": Vector2(22, 224), "angle": 0.16, "length": 16.0},
    {"center": Vector2(54, 340), "angle": -0.38, "length": 15.0},
    {"center": Vector2(22, 535), "angle": 0.28, "length": 17.0},
    {"center": Vector2(79, 811), "angle": -0.18, "length": 17.0},
    {"center": Vector2(367, 208), "angle": 0.28, "length": 16.0},
    {"center": Vector2(333, 334), "angle": -0.22, "length": 15.0},
    {"center": Vector2(371, 532), "angle": 0.31, "length": 17.0},
    {"center": Vector2(294, 765), "angle": -0.26, "length": 18.0},
    {"center": Vector2(47, 292), "angle": 0.54, "length": 13.0},
    {"center": Vector2(343, 306), "angle": -0.56, "length": 13.0},
    {"center": Vector2(48, 438), "angle": 0.47, "length": 14.0},
    {"center": Vector2(342, 447), "angle": -0.44, "length": 14.0},
    {"center": Vector2(91, 548), "angle": -0.35, "length": 14.0},
    {"center": Vector2(292, 569), "angle": 0.40, "length": 14.0},
    {"center": Vector2(94, 707), "angle": 0.52, "length": 15.0},
    {"center": Vector2(291, 744), "angle": -0.49, "length": 15.0},
    {"center": Vector2(20, 680), "angle": 0.19, "length": 12.0},
    {"center": Vector2(370, 680), "angle": -0.21, "length": 12.0},
    {"center": Vector2(21, 776), "angle": 0.41, "length": 13.0},
    {"center": Vector2(367, 112), "angle": -0.33, "length": 12.0},
    {"center": Vector2(92, 180), "angle": 0.34, "length": 12.0},
    {"center": Vector2(299, 190), "angle": -0.29, "length": 12.0},
    {"center": Vector2(104, 770), "angle": -0.42, "length": 13.0},
    {"center": Vector2(282, 812), "angle": 0.37, "length": 13.0},
    {"center": Vector2(55, 365), "angle": -0.51, "length": 12.0},
    {"center": Vector2(335, 612), "angle": 0.50, "length": 12.0}
]


func _ready() -> void:
    _create_background()
    _create_ambient_layer()
    _create_preview_overlay()
    queue_redraw()


func _process(delta: float) -> void:
    elapsed_real_seconds += delta
    if preview_mode:
        run_minutes = min(20.0, elapsed_real_seconds * 20.0 / PREVIEW_DURATION_SECONDS)
    else:
        run_minutes = min(20.0, elapsed_real_seconds / 60.0)

    for index in range(impact_events.size() - 1, -1, -1):
        impact_events[index]["age"] = float(impact_events[index]["age"]) + delta
        if float(impact_events[index]["age"]) > 1.2:
            impact_events.remove_at(index)

    if preview_label and show_preview_overlay:
        var total_seconds := int(run_minutes * 60.0)
        preview_label.text = "ПРЕДПРОСМОТР АРЕНЫ  ·  %02d:%02d" % [total_seconds / 60, total_seconds % 60]
    queue_redraw()


func _input(event: InputEvent) -> void:
    if event is InputEventScreenTouch and event.pressed:
        _register_impact(event.position)
    elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
        _register_impact(event.position)


func _create_background() -> void:
    var background := Sprite2D.new()
    background.name = "ArenaArt"
    background.texture = load(ART_PATH) as Texture2D
    background.centered = false
    background.position = Vector2.ZERO
    background.z_index = -10
    add_child(background)


func _create_ambient_layer() -> void:
    var ambient := Sprite2D.new()
    ambient.name = "AmbientPreviewLayer"
    ambient.texture = load(AMBIENT_PATH) as Texture2D
    ambient.centered = false
    ambient.position = Vector2.ZERO
    ambient.z_index = -5
    ambient.modulate = Color(1, 1, 1, 0.82)
    add_child(ambient)


func _create_preview_overlay() -> void:
    if not show_preview_overlay:
        return

    var canvas := CanvasLayer.new()
    canvas.name = "PreviewOverlay"
    canvas.layer = 20
    add_child(canvas)

    var back_button := Button.new()
    back_button.text = "‹ МЕНЮ"
    back_button.position = Vector2(12, 14)
    back_button.size = Vector2(92, 34)
    back_button.add_theme_font_size_override("font_size", 13)
    back_button.add_theme_color_override("font_color", MOON)
    back_button.add_theme_color_override("font_hover_color", Color.WHITE)
    back_button.add_theme_stylebox_override("normal", _button_style(Color("#061416cc"), Color("#3D9F99")))
    back_button.add_theme_stylebox_override("hover", _button_style(Color("#174244ee"), Color("#A8FFF0")))
    back_button.pressed.connect(_return_to_menu)
    canvas.add_child(back_button)

    preview_label = Label.new()
    preview_label.position = Vector2(108, 16)
    preview_label.size = Vector2(270, 30)
    preview_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
    preview_label.add_theme_font_size_override("font_size", 11)
    preview_label.add_theme_color_override("font_color", Color("#D8FFF3CC"))
    canvas.add_child(preview_label)


func _button_style(background: Color, border: Color) -> StyleBoxFlat:
    var style := StyleBoxFlat.new()
    style.bg_color = background
    style.border_color = border
    style.border_width_left = 1
    style.border_width_top = 1
    style.border_width_right = 1
    style.border_width_bottom = 1
    style.corner_radius_top_left = 10
    style.corner_radius_top_right = 10
    style.corner_radius_bottom_left = 10
    style.corner_radius_bottom_right = 10
    return style


func _return_to_menu() -> void:
    get_tree().change_scene_to_file("res://scenes/menu/menu.tscn")


func _register_impact(point: Vector2) -> void:
    if point.y < 100.0 or point.y > VIEWPORT_SIZE.y:
        return
    impact_events.append({"center": point, "age": 0.0})


func _draw() -> void:
    _draw_ripples()
    _draw_swaying_plants()
    _draw_air_particles()
    _draw_aftermath()
    _draw_impacts()


func _draw_ripples() -> void:
    for index in range(ripple_centers.size()):
        var cycle := fmod(elapsed_real_seconds * 0.9 + float(index) * 0.55, 2.4)
        var fade := 1.0 - cycle / 2.4
        var radius := 5.0 + cycle * 8.0
        draw_set_transform(ripple_centers[index], 0.0, Vector2(1.0, 0.45))
        draw_arc(Vector2.ZERO, radius, 0.0, TAU, 24, Color(RIPPLE, 0.48 * fade), 1.4)
        if cycle > 0.8:
            draw_arc(Vector2.ZERO, radius * 0.62, 0.0, TAU, 24, Color(RIPPLE, 0.26 * fade), 1.0)
        draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _draw_swaying_plants() -> void:
    for index in range(plant_markers.size()):
        var base: Vector2 = plant_markers[index]
        var phase := float(index) * 0.71
        var sway := sin(elapsed_real_seconds * 2.1 + phase) * 4.0
        var height := 11.0 + float(index % 3) * 3.0
        draw_line(base, base + Vector2(sway, -height), Color(PLANT, 0.52), 1.6, true)
        draw_line(base + Vector2(2, 0), base + Vector2(-sway * 0.65, -height * 0.78), Color(PLANT, 0.42), 1.3, true)


func _draw_air_particles() -> void:
    for index in range(18):
        var x := fmod(float(index * 83) + elapsed_real_seconds * (7.0 + float(index % 4)), 360.0) + 15.0
        var y := fmod(float(index * 47) + sin(elapsed_real_seconds * 0.8 + float(index)) * 18.0, 620.0) + 112.0
        var alpha := 0.12 + float(index % 3) * 0.05
        draw_circle(Vector2(x, y), 0.8 + float(index % 2) * 0.45, Color(DUST, alpha))

    if run_minutes >= 10.0:
        for index in range(8):
            var angle := elapsed_real_seconds * 0.45 + float(index) * 0.78
            var center := Vector2(195, 420) + Vector2(cos(angle), sin(angle) * 0.6) * (105.0 + float(index % 3) * 20.0)
            draw_circle(center, 1.2, Color("#D56B75AA"))


func _draw_aftermath() -> void:
    var visible_count := int(round(float(aftermath_markers.size()) * run_minutes / 20.0))
    for index in range(visible_count):
        var marker: Dictionary = aftermath_markers[index]
        _draw_remain(marker["center"], float(marker["angle"]), float(marker["length"]), index)


func _draw_remain(center: Vector2, angle: float, length: float, index: int) -> void:
    var direction := Vector2.RIGHT.rotated(angle)
    var perpendicular := Vector2(-direction.y, direction.x)
    var body_color := INK if index % 3 != 1 else INK_SOFT
    draw_line(center - direction * length * 0.45, center + direction * length * 0.45, Color(body_color, 0.72), 4.0, true)
    draw_circle(center + direction * length * 0.38, 3.2, Color(body_color, 0.82))
    draw_line(center - direction * length * 0.10, center - direction * length * 0.48 + perpendicular * 5.0, Color(body_color, 0.68), 2.0, true)
    draw_line(center - direction * length * 0.10, center - direction * length * 0.48 - perpendicular * 5.0, Color(body_color, 0.68), 2.0, true)

    if index % 3 == 0:
        draw_line(center + perpendicular * 4.0, center + perpendicular * 9.0 + direction * 5.0, Color(BONE, 0.70), 1.4, true)
        draw_line(center + perpendicular * 4.0, center + perpendicular * 9.0 - direction * 5.0, Color(BONE, 0.70), 1.4, true)
    elif index % 3 == 2:
        draw_circle(center - direction * length * 0.20, 5.0, Color("#4A263188"))


func _draw_impacts() -> void:
    for event in impact_events:
        var age: float = event["age"]
        var center: Vector2 = event["center"]
        var fade := 1.0 - age / 1.2
        var radius := 6.0 + age * 34.0
        draw_set_transform(center, 0.0, Vector2(1.0, 0.45))
        draw_arc(Vector2.ZERO, radius, 0.0, TAU, 24, Color(RIPPLE, 0.66 * fade), 2.0)
        draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
        draw_circle(center + Vector2(0, -age * 7.0), 1.5, Color(MOON, 0.48 * fade))
