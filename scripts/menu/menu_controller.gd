extends Control
## Stage 01 navigation prototype.
## This scene uses concept PNGs as art-direction backgrounds and real Godot controls
## for navigation. It is intentionally not marked as the finished menu.

const VIEWPORT_SIZE := Vector2(390.0, 844.0)

const INK := Color("#061416")
const PANEL := Color("#0b2426")
const PANEL_SOFT := Color("#0b2426cc")
const JADE := Color("#a8fff0")
const JADE_DARK := Color("#3d9f99")
const MOON := Color("#f4ead2")
const CRIMSON := Color("#bc4c4f")
const MUTED := Color("#9aa9a8")

var current_screen := "home"
var screen_layer: Control


func _ready() -> void:
    screen_layer = Control.new()
    screen_layer.name = "ScreenLayer"
    screen_layer.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    add_child(screen_layer)
    _show_home()


func _clear_screen() -> void:
    for child in screen_layer.get_children():
        child.free()


func _background(asset_path: String, ui_asset_path := "") -> void:
    var background := TextureRect.new()
    background.name = "ArtDirectionBackground"
    background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    background.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
    background.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
    background.mouse_filter = Control.MOUSE_FILTER_IGNORE

    var texture := load(asset_path) as Texture2D
    if texture:
        background.texture = texture
    else:
        background.texture = _fallback_texture()

    screen_layer.add_child(background)
    screen_layer.move_child(background, 0)

    if ui_asset_path.is_empty():
        return

    var ui_layer := TextureRect.new()
    ui_layer.name = "RussianUiLayer"
    ui_layer.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    ui_layer.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
    ui_layer.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
    ui_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
    var ui_texture := load(ui_asset_path) as Texture2D
    if ui_texture:
        ui_layer.texture = ui_texture
        screen_layer.add_child(ui_layer)


func _fallback_texture() -> GradientTexture2D:
    var gradient := Gradient.new()
    gradient.colors = PackedColorArray([INK, Color("#112e30")])
    var texture := GradientTexture2D.new()
    texture.gradient = gradient
    texture.width = 390
    texture.height = 844
    return texture


func _style(background: Color, border: Color, radius := 16) -> StyleBoxFlat:
    var style := StyleBoxFlat.new()
    style.bg_color = background
    style.border_color = border
    style.border_width_left = 1
    style.border_width_top = 1
    style.border_width_right = 1
    style.border_width_bottom = 1
    style.corner_radius_top_left = radius
    style.corner_radius_top_right = radius
    style.corner_radius_bottom_left = radius
    style.corner_radius_bottom_right = radius
    style.content_margin_left = 12
    style.content_margin_right = 12
    style.content_margin_top = 8
    style.content_margin_bottom = 8
    return style


func _label(value: String, rect: Rect2, font_size := 16, color := MOON) -> Label:
    var label := Label.new()
    label.text = value
    label.position = rect.position
    label.size = rect.size
    label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
    label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
    label.add_theme_font_size_override("font_size", font_size)
    label.add_theme_color_override("font_color", color)
    label.mouse_filter = Control.MOUSE_FILTER_IGNORE
    screen_layer.add_child(label)
    return label


func _panel(rect: Rect2, background := PANEL_SOFT, border := JADE_DARK) -> Panel:
    var panel := Panel.new()
    panel.position = rect.position
    panel.size = rect.size
    panel.add_theme_stylebox_override("panel", _style(background, border, 18))
    panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
    screen_layer.add_child(panel)
    return panel


func _button(
        value: String,
        rect: Rect2,
        callback: Callable,
        accent := false,
        compact := false
    ) -> Button:
    var button := Button.new()
    button.text = value
    button.position = rect.position
    button.size = rect.size
    button.tooltip_text = value
    button.focus_mode = Control.FOCUS_ALL
    button.add_theme_font_size_override("font_size", 14 if compact else 18)
    button.add_theme_color_override("font_color", MOON if not accent else INK)
    button.add_theme_color_override("font_hover_color", MOON if not accent else INK)
    button.add_theme_color_override("font_pressed_color", MOON if not accent else INK)
    button.add_theme_stylebox_override(
        "normal",
        _style(PANEL_SOFT if not accent else JADE_DARK, JADE_DARK if not accent else JADE, 14)
    )
    button.add_theme_stylebox_override(
        "hover",
        _style(Color("#174244cc") if not accent else JADE, JADE if not accent else MOON, 14)
    )
    button.add_theme_stylebox_override(
        "pressed",
        _style(Color("#24595acc") if not accent else Color("#7bd6c9"), JADE, 14)
    )
    button.pressed.connect(callback)
    screen_layer.add_child(button)
    return button


func _hit(value: String, rect: Rect2, callback: Callable) -> Button:
    var button := Button.new()
    button.text = ""
    button.tooltip_text = value
    button.position = rect.position
    button.size = rect.size
    button.focus_mode = Control.FOCUS_ALL
    button.add_theme_stylebox_override("normal", StyleBoxEmpty.new())
    button.add_theme_stylebox_override("hover", _style(Color("#a8fff033"), JADE, 14))
    button.add_theme_stylebox_override("pressed", _style(Color("#a8fff066"), JADE, 14))
    button.pressed.connect(callback)
    screen_layer.add_child(button)
    return button


func _bottom_nav(active: String) -> void:
    var items := [
        ["ГЛАВНАЯ", Callable(self, "_show_home")],
        ["ГЕРОИНИ", Callable(self, "_show_heroes")],
        ["АРСЕНАЛ", Callable(self, "_show_arsenal")],
        ["АРТЕФАКТЫ", Callable(self, "_show_artifacts")],
        ["НАСТРОЙКИ", Callable(self, "_show_settings")]
    ]
    var width := 78.0
    for index in range(items.size()):
        var item: Array = items[index]
        var name: String = item[0]
        var action: Callable = item[1]
        var button := _hit(name, Rect2(width * index, 764, width, 70), action)
        if name == active:
            button.add_theme_stylebox_override("hover", _style(Color("#a8fff022"), JADE, 10))


func _show_home() -> void:
    current_screen = "home"
    _clear_screen()
    _background("res://docs/mockups/01-menu/layers/STAGE01_HOME_ART_v01.png", "res://docs/mockups/01-menu/layers/STAGE01_HOME_UI_RU_v01.png")
    _hit("Начать забег", Rect2(56, 560, 278, 70), Callable(self, "_show_run_setup"))
    _bottom_nav("ГЛАВНАЯ")


func _show_heroes() -> void:
    current_screen = "heroes"
    _clear_screen()
    _background("res://docs/mockups/01-menu/layers/STAGE01_HEROES_ART_v01.png", "res://docs/mockups/01-menu/layers/STAGE01_HEROES_UI_RU_v01.png")
    _hit("Выбрать героиню", Rect2(68, 590, 254, 68), Callable(self, "_show_run_setup"))
    _hit("Назад", Rect2(14, 684, 96, 48), Callable(self, "_show_home"))
    _bottom_nav("ГЕРОИНИ")


func _show_run_setup() -> void:
    current_screen = "run_setup"
    _clear_screen()
    _background("res://docs/mockups/01-menu/layers/STAGE01_RUN_SETUP_ART_v01.png", "res://docs/mockups/01-menu/layers/STAGE01_RUN_SETUP_UI_RU_v01.png")
    _hit("Начать забег", Rect2(86, 655, 218, 66), Callable(self, "_show_loading"))
    _hit("Назад", Rect2(14, 655, 70, 66), Callable(self, "_show_home"))
    _bottom_nav("ГЛАВНАЯ")


func _show_loading() -> void:
    current_screen = "loading"
    _clear_screen()
    _background("res://docs/mockups/01-menu/layers/STAGE01_LOADING_ART_v01.png", "res://docs/mockups/01-menu/layers/STAGE01_LOADING_UI_RU_v01.png")
    _label("ЗАГРУЗКА", Rect2(90, 620, 210, 40), 18, JADE)
    _label("ГЛАВА 1 — ПЕРВАЯ ВОЛНА", Rect2(62, 660, 266, 32), 12, MOON)
    get_tree().create_timer(1.2).timeout.connect(_on_loading_complete)


func _on_loading_complete() -> void:
    if current_screen == "loading":
        _show_arena_handoff()


func _show_arena_handoff() -> void:
    current_screen = "arena_handoff"
    _clear_screen()
    _background("res://docs/mockups/01-menu/layers/STAGE01_HOME_ART_v01.png", "res://docs/mockups/01-menu/layers/STAGE01_HOME_UI_RU_v01.png")
    _panel(Rect2(28, 250, 334, 300), Color("#061416ee"), JADE_DARK)
    _label("ПЕРЕХОД К АРЕНЕ", Rect2(48, 278, 294, 42), 24, JADE)
    _label(
        "Сцена арены этапа 2 ещё не подключена.\nЭтот экран нужен только для проверки маршрута меню.",
        Rect2(54, 330, 282, 74),
        14,
        MOON
    )
    _button("ПРЕДПРОСМОТР ПОБЕДЫ", Rect2(54, 424, 282, 48), Callable(self, "_show_victory"), false, true)
    _button("ПРЕДПРОСМОТР ПОРАЖЕНИЯ", Rect2(54, 480, 282, 48), Callable(self, "_show_run_ended"), false, true)
    _button("К ПОДГОТОВКЕ", Rect2(54, 548, 282, 44), Callable(self, "_show_run_setup"), false, true)


func _show_victory() -> void:
    current_screen = "victory"
    _clear_screen()
    _background("res://docs/mockups/01-menu/layers/STAGE01_VICTORY_ART_v01.png", "res://docs/mockups/01-menu/layers/STAGE01_VICTORY_UI_RU_v01.png")
    _hit("Забрать награды", Rect2(64, 677, 262, 58), Callable(self, "_show_home"))
    _hit("В меню", Rect2(112, 742, 166, 42), Callable(self, "_show_home"))


func _show_run_ended() -> void:
    current_screen = "run_ended"
    _clear_screen()
    _background("res://docs/mockups/01-menu/layers/STAGE01_DEFEAT_ART_v01.png", "res://docs/mockups/01-menu/layers/STAGE01_DEFEAT_UI_RU_v01.png")
    _hit("Забрать награды", Rect2(62, 674, 266, 58), Callable(self, "_show_home"))
    _hit("Повторить", Rect2(104, 740, 182, 44), Callable(self, "_show_run_setup"))
    _hit("В меню", Rect2(118, 790, 154, 34), Callable(self, "_show_home"))


func _show_arsenal() -> void:
    _show_section_placeholder("АРСЕНАЛ", "Карточки оружия и эволюции относятся к этапу 6.")


func _show_artifacts() -> void:
    _show_section_placeholder("АРТЕФАКТЫ", "Кодекс артефактов относится к этапу 8.")


func _show_settings() -> void:
    _show_section_placeholder("НАСТРОЙКИ", "Звук, доступность и вибрация относятся к этапам 13 и 20.")


func _show_section_placeholder(title: String, detail: String) -> void:
    current_screen = title.to_lower()
    _clear_screen()
    _background("res://docs/mockups/01-menu/layers/STAGE01_HOME_ART_v01.png", "res://docs/mockups/01-menu/layers/STAGE01_HOME_UI_RU_v01.png")
    _panel(Rect2(28, 310, 334, 224), Color("#061416ee"), JADE_DARK)
    _label(title, Rect2(50, 344, 290, 44), 24, JADE)
    _label(detail, Rect2(56, 404, 278, 58), 14, MOON)
    _button("В МЕНЮ", Rect2(76, 478, 238, 48), Callable(self, "_show_home"), false)
